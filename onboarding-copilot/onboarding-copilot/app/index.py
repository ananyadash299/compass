"""
Unified document index.

- Ingests all docs from Confluence + GitHub + SharePoint via connectors.
- Ranks with a HYBRID retriever: BM25 (lexical) + dense embeddings (semantic),
  fused via Reciprocal Rank Fusion. BM25 catches rare tokens / exact IDs;
  the dense encoder catches paraphrases and synonyms ("DB access" ↔
  "database entitlement request"). RRF is parameter-free and robust.
- Applies a recency boost so newer docs surface first when scores are close.
  This is the core banking-safe property: stale policy docs must lose to
  the latest version.
- Applies a title/tag field boost so curated metadata beats loose body hits.

The dense encoder is a small local model (all-MiniLM-L6-v2, ~90MB). No
external API calls — required for the demo's "no data leak" narrative.
If the encoder can't load (first-run offline, missing torch, etc.) the
index gracefully falls back to BM25-only.
"""
from __future__ import annotations

import re
from datetime import datetime, timezone
from typing import Callable, List, Dict, Optional, Tuple

import numpy as np
from dateutil.parser import isoparse
from rank_bm25 import BM25Okapi

from .connectors import ConfluenceConnector, GitHubConnector, SharePointConnector

_TOKEN = re.compile(r"[a-zA-Z0-9]+")

# Small, fast, local. 384-dim. Good enough for a demo corpus of ~100 docs.
_ENCODER_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# RRF constant. 60 is the value from the original paper and is a good default —
# larger values compress rank differences, smaller values sharpen them.
_RRF_K = 60


def _tokenize(text: str) -> List[str]:
    return [t.lower() for t in _TOKEN.findall(text or "")]


def _iso_to_dt(s: str) -> datetime:
    dt = isoparse(s)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt


class UnifiedIndex:
    def __init__(self, recency_half_life_days: float = 180.0):
        self.recency_half_life_days = recency_half_life_days
        self.docs: List[Dict] = []
        self._bm25: BM25Okapi | None = None
        self._corpus_tokens: List[List[str]] = []
        self._now: datetime = datetime.now(timezone.utc)
        self._encoder = None
        self._doc_embeddings: Optional[np.ndarray] = None

    def build(self) -> None:
        connectors = [
            ConfluenceConnector(),
            GitHubConnector(),
            SharePointConnector(),
        ]
        docs: List[Dict] = []
        for c in connectors:
            docs.extend(c.fetch())

        # Preserve the original (fake) external URL for display, and repoint
        # `url` at our own /doc/{id} route so citation clicks actually resolve.
        for d in docs:
            d["external_url"] = d["url"]
            d["url"] = f"/doc/{d['id']}"

        self.docs = docs
        self._by_id = {d["id"]: d for d in docs}
        self._corpus_tokens = [
            _tokenize(f"{d['title']} {' '.join(d.get('tags', []))} {d['body']}")
            for d in docs
        ]
        self._bm25 = BM25Okapi(self._corpus_tokens)
        self._now = datetime.now(timezone.utc)
        self._build_dense_index()

    def _build_dense_index(self) -> None:
        try:
            from sentence_transformers import SentenceTransformer
        except ImportError:
            # BM25-only fallback if sentence-transformers isn't installed.
            self._encoder = None
            self._doc_embeddings = None
            return

        try:
            self._encoder = SentenceTransformer(_ENCODER_MODEL)
        except Exception:
            self._encoder = None
            self._doc_embeddings = None
            return

        # Title + tags carry the strongest topical signal; body adds specifics.
        # Truncate body so long docs don't drown out title in the pooled vector.
        passages = [
            f"{d['title']}. Tags: {', '.join(d.get('tags', []))}. {d['body'][:800]}"
            for d in self.docs
        ]
        self._doc_embeddings = self._encoder.encode(
            passages,
            normalize_embeddings=True,
            show_progress_bar=False,
            convert_to_numpy=True,
        )

    def get(self, doc_id: str) -> Dict | None:
        return getattr(self, "_by_id", {}).get(doc_id)

    def all_docs(self) -> List[Dict]:
        return list(self.docs)

    def _recency_multiplier(self, updated_at_iso: str) -> float:
        """
        Recency nudge that never decays below 1.0 - so docs older than the
        half-life aren't demoted, but fresh docs get a real boost that can
        break lexical ties. This keeps the whole corpus in play (no decay)
        while letting today's doc beat a same-content doc from 2019.

        Curve:
          - today          → × 1.30  (+30% - decisive tie-break for fresh docs)
          - 30 days old    → × 1.24
          - 90 days old    → × 1.20
          - 180 days old   → × 1.15
          - 1 year old     → × 1.075
          - 2 years old    → × 1.02
          - ancient        → × 1.00
        """
        age_days = max(0.0, (self._now - _iso_to_dt(updated_at_iso)).total_seconds() / 86400.0)
        boost = 0.5 ** (age_days / self.recency_half_life_days)
        return 1.0 + 0.30 * boost

    def _field_multiplier(self, doc: Dict, q_set: set) -> float:
        """
        Reward query-token hits in curated fields (title, tags). BM25 alone
        weighs a body mention the same as a title mention, so a doc *named*
        "Snowflake Warehouse Access Setup" can lose to a generic onboarding
        doc that mentions "access" many times. This lifts docs whose curated
        metadata actually matches the query.
        """
        if not q_set:
            return 1.0
        title_tokens = set(_tokenize(doc.get("title", "")))
        tag_tokens = {t.lower() for t in doc.get("tags", [])}
        title_hits = len(q_set & title_tokens)
        tag_hits = len(q_set & tag_tokens)
        return 1.0 + 0.6 * title_hits + 0.35 * tag_hits

    def _dense_scores(self, query: str) -> Optional[np.ndarray]:
        if self._encoder is None or self._doc_embeddings is None:
            return None
        q_vec = self._encoder.encode(
            [query], normalize_embeddings=True, convert_to_numpy=True
        )[0]
        # Since both are L2-normalized, dot product == cosine similarity.
        return self._doc_embeddings @ q_vec

    def search(
        self,
        query: str,
        top_k: int = 6,
        doc_filter: Optional[Callable[[Dict], bool]] = None,
    ) -> List[Tuple[Dict, float]]:
        if not self._bm25:
            raise RuntimeError("Index not built. Call build() first.")

        q_tokens = _tokenize(query)
        if not q_tokens:
            return []
        q_set = set(q_tokens)

        bm25_scores = self._bm25.get_scores(q_tokens)
        dense_scores = self._dense_scores(query)

        # Build per-doc rank positions for RRF. Only rank docs that pass the
        # filter — this keeps out-of-scope docs from stealing rank slots.
        n = len(self.docs)
        keep = [
            i for i in range(n)
            if doc_filter is None or doc_filter(self.docs[i])
        ]
        if not keep:
            return []

        # Rank by BM25 (descending). Ties broken by doc order — stable enough.
        bm25_rank = {i: r + 1 for r, i in enumerate(
            sorted(keep, key=lambda i: bm25_scores[i], reverse=True)
        )}

        if dense_scores is not None:
            dense_rank = {i: r + 1 for r, i in enumerate(
                sorted(keep, key=lambda i: dense_scores[i], reverse=True)
            )}
        else:
            dense_rank = None

        ranked: List[Tuple[Dict, float]] = []
        for i in keep:
            bm25_s = float(bm25_scores[i])
            dense_s = float(dense_scores[i]) if dense_scores is not None else 0.0
            # Drop docs that neither retriever has any signal for. Prevents
            # a completely irrelevant doc from surviving on RRF alone when
            # both scores are effectively zero.
            if bm25_s <= 0.0 and dense_s < 0.15:
                continue

            rrf = 1.0 / (_RRF_K + bm25_rank[i])
            if dense_rank is not None:
                rrf += 1.0 / (_RRF_K + dense_rank[i])

            doc = self.docs[i]
            score = (
                rrf
                * self._recency_multiplier(doc["updated_at"])
                * self._field_multiplier(doc, q_set)
            )
            ranked.append((doc, score))

        ranked.sort(key=lambda x: x[1], reverse=True)
        return ranked[:top_k]

    def stats(self) -> Dict:
        by_source: Dict[str, int] = {}
        newest: Dict[str, str] = {}
        for d in self.docs:
            by_source[d["source"]] = by_source.get(d["source"], 0) + 1
            cur = newest.get(d["source"])
            if cur is None or d["updated_at"] > cur:
                newest[d["source"]] = d["updated_at"]
        return {
            "total_docs": len(self.docs),
            "by_source": by_source,
            "newest_per_source": newest,
            "dense_index": self._doc_embeddings is not None,
        }
