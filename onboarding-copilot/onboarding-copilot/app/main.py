"""
FastAPI entrypoint for Compass.

Endpoints:
  GET  /             → the single-page chat UI
  GET  /api/health   → basic health + index stats
  GET  /api/sources  → per-source stats for the UI header
  POST /api/ask      → main Q&A endpoint

Run:
  uvicorn app.main:app --reload --port 8000
"""
from __future__ import annotations

from pathlib import Path
from typing import List, Optional

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from .doc_view import render_doc
from .faq_store import record_question, top_faqs
from .index import UnifiedIndex
from .synthesizer import synthesize_answer

STATIC_DIR = Path(__file__).resolve().parent.parent / "static"

app = FastAPI(title="Compass", version="0.1.0")

# Build the index once at startup. The mock corpus is tiny so this is instant.
_index = UnifiedIndex()
_index.build()


APP_CODES = ("abc", "ssm", "epm")


def _doc_apps(doc: dict) -> set:
    """Which SharePoint applications a doc belongs to (by tag). Empty set = not tied to an app."""
    tags = {t.lower() for t in doc.get("tags", [])}
    return {code for code in APP_CODES if code in tags}


# --- Query-driven intent scoping ------------------------------------------------
# When a user asks "give me the unit testing document for SSM", we want:
#   - the app narrowed to SSM (even if the left-rail has all apps selected), and
#   - the doc-type narrowed to unit-testing (never show migration/entitlement etc.).
# We do this by detecting a "doc type" hint in the query and, if present,
# requiring a matching tag on candidate docs.

_DOC_TYPE_HINTS = {
    "unit-testing": (
        "unit testing", "unit-test", "unit tests", "unit test",
        "ut doc", "ut docs", "ut sheet", "test cases", "testcases",
    ),
    "entitlements": (
        "entitlement", "entitlements", "oim entitlement", "oim role",
        "access role", "access roles", "role register",
    ),
    "components": (
        "migration components", "components list", "component list",
        "components doc", "components sheet", "migration component",
    ),
}


def _detect_doc_type(query: str):
    q = query.lower()
    for tag, hints in _DOC_TYPE_HINTS.items():
        if any(h in q for h in hints):
            return tag
    return None


def _detect_query_apps(query: str) -> set:
    """Pick up ABC/SSM/EPM mentioned in the query itself (word-boundary match)."""
    q = f" {query.lower()} "
    hits = set()
    for code in APP_CODES:
        if f" {code} " in q or f" {code}-" in q or f" {code}." in q:
            hits.add(code)
    return hits


# Common ways users refer to each source in a query. Anything here narrows the
# search to those sources — so "any UT docs in confluence and github?" won't
# silently fall back to SharePoint hits.
_SOURCE_HINTS = {
    "confluence": ("confluence", "conf",),
    "github": ("github", "gh", "git repo", "git repos", "repo", "repos"),
    "sharepoint": ("sharepoint", "share point", "sp"),
}


def _detect_query_sources(query: str) -> set:
    q = f" {query.lower()} "
    hits = set()
    for name, hints in _SOURCE_HINTS.items():
        for h in hints:
            if f" {h} " in q or f" {h}," in q or f" {h}." in q or f" {h}?" in q:
                hits.add(name)
                break
    return hits


class HistoryTurn(BaseModel):
    role: str = Field(..., description="'user' or 'ai'")
    text: str = Field(default="", max_length=2000)


class AskRequest(BaseModel):
    query: str = Field(..., min_length=2, max_length=500)
    sources: Optional[List[str]] = Field(
        default=None,
        description="Optional filter, e.g. ['confluence','github']",
    )
    apps: Optional[List[str]] = Field(
        default=None,
        description="Optional SharePoint app filter, e.g. ['abc','ssm','epm']",
    )
    history: Optional[List[HistoryTurn]] = Field(
        default=None,
        description="Recent conversation turns for pronoun/follow-up resolution. Client-supplied, capped to last few turns.",
    )
    top_k: int = Field(default=6, ge=1, le=15)


# True anaphora — words that need prior context to resolve. Kept tight on
# purpose: WH-words like "how/why/who" are legitimate self-contained openers.
_ANAPHORIC = {
    "it", "its", "that", "this", "these", "those", "them", "they",
    "one", "same", "there", "instead",
}

# Function words / meta chatter that shouldn't count as a "novel topic" token.
# If a short query's ONLY substantive token is one of these, it's still a
# follow-up; if it introduces a real content word (like "bms"), it isn't.
_STOPWORDS = {
    "a", "an", "the", "and", "or", "but", "of", "for", "to", "in", "on", "at",
    "by", "with", "from", "as", "is", "are", "was", "were", "be", "been", "being",
    "do", "does", "did", "doing", "have", "has", "had", "having",
    "i", "you", "we", "they", "he", "she", "it",
    "me", "my", "our", "your", "their", "his", "her",
    "any", "some", "all", "more", "less", "few", "many",
    "what", "which", "who", "whom", "whose", "when", "where", "why", "how",
    "can", "could", "would", "should", "may", "might", "shall", "will",
    "please", "kindly", "thanks", "thank",
    "show", "give", "tell", "list", "find", "get", "point", "share",
    "docs", "doc", "documents", "document", "info", "information", "detail",
    "details", "about", "on", "regarding", "re", "only", "just", "same",
    "other", "another", "different", "similar", "instead", "rather",
    "one", "ones",
    # Intent modifiers used in follow-ups — not real topic shifts.
    "newest", "latest", "oldest", "newer", "older", "recent",
    "first", "last", "next", "previous", "prior",
    "top", "bottom", "best", "worst",
    "here", "now", "then", "also", "too",
}

# Purely conversational / meta messages that don't have a retrieval target.
# We short-circuit these with a helpful canned reply instead of returning
# BM25 noise for a topicless prompt.
#
# STRONG_META: phrases that are meta regardless of surrounding words —
# "can I ask another query?" is meta even though "ask" and "query" are
# content tokens. Matching one of these always short-circuits.
_STRONG_META = (
    "can i ask", "may i ask", "another question", "different question",
    "one more question", "some other query", "another query",
    "who are you", "what are you", "what can you do",
    "how do you work", "how does this work",
)
# WEAK_META: polite acks. Only meta when the query is *just* the ack —
# so "thanks, now show me the RCA doc" still runs retrieval.
_WEAK_META = ("thanks", "thank you", "ok", "okay", "cool", "great", "nice", "got it")


def _is_meta_chatter(query: str) -> bool:
    q = query.lower().strip().rstrip("?.!")
    if not q:
        return True
    if any(p in q for p in _STRONG_META):
        return True
    if any(q == p or q.startswith(p + " ") or q.endswith(" " + p) for p in _WEAK_META):
        # Guard: don't classify "thanks, now show me the RCA doc" as meta.
        tokens = [t for t in q.split() if t.isalpha() and t not in _STOPWORDS]
        return len(tokens) <= 1
    return False


def _content_tokens(query: str) -> set:
    """Alpha tokens with stopwords removed — the substantive words in a query."""
    return {
        t for t in query.lower().split()
        if t.isalpha() and t not in _STOPWORDS and len(t) > 1
    }


def _looks_like_followup(query: str, prior_content: Optional[set] = None) -> bool:
    """
    Short query, or one that leans on anaphora, likely refers to prior context.

    If we know the prior turn's content tokens, a query that introduces its
    OWN novel content word (e.g. "anything on bms?") is treated as a topic
    shift, NOT a follow-up — even though it's short. This prevents the
    anaphora blender from polluting a fresh question with stale context.
    """
    tokens = [t for t in query.lower().split() if t.isalpha()]
    if not tokens:
        return False

    has_anaphor = any(t in _ANAPHORIC for t in tokens)
    is_short = len(tokens) <= 4

    if not (has_anaphor or is_short):
        return False

    # Topic-shift guard: if this query has content tokens the prior turn
    # didn't, treat as a new topic. Anaphora still counts as follow-up
    # ("what about that?" has no content tokens — always inherits).
    if prior_content is not None and not has_anaphor:
        own_content = _content_tokens(query)
        novel = own_content - prior_content
        if novel:
            return False

    return True


def _prior_user_turn(history: Optional[List[HistoryTurn]]) -> Optional[str]:
    """The single most recent user turn — used for surfacing "Following up on:"."""
    if not history:
        return None
    for turn in reversed(history):
        if turn.role == "user" and turn.text.strip():
            return turn.text.strip()
    return None


def _anchor_user_turn(history: Optional[List[HistoryTurn]]) -> Optional[str]:
    """
    The topic anchor for follow-up blending: walk backwards through user
    turns and skip over ones that were themselves short follow-ups, so a
    3-hop chain like

        "unit testing docs for SSM"     ← anchor
        "in github only?"               ← follow-up
        "show me the newest one"        ← follow-up

    still retrieves against "unit testing docs for SSM" instead of drifting
    to the last one-liner. Falls back to the most recent user turn if the
    whole chain looks like follow-ups (unlikely in practice).
    """
    if not history:
        return None
    user_turns = [t.text.strip() for t in history if t.role == "user" and t.text.strip()]
    if not user_turns:
        return None
    for text in reversed(user_turns):
        if not _looks_like_followup(text):
            return text
    return user_turns[-1]


@app.get("/api/health")
def health():
    return {"status": "ok", **_index.stats()}


@app.get("/api/sources")
def sources():
    stats = _index.stats()
    all_docs = _index.all_docs()
    app_counts = {code: 0 for code in APP_CODES}
    for d in all_docs:
        for code in _doc_apps(d):
            app_counts[code] += 1
    return {
        "sources": [
            {
                "name": name,
                "doc_count": stats["by_source"].get(name, 0),
                "newest": stats["newest_per_source"].get(name),
            }
            for name in ("confluence", "github", "sharepoint")
        ],
        "apps": [
            {"code": code.upper(), "id": code, "doc_count": app_counts[code]}
            for code in APP_CODES
        ],
    }


@app.post("/api/ask")
def ask(req: AskRequest):
    # Left-rail filters are authoritative. The user opted into a specific
    # source/app scope, so the answer must come from within that scope even
    # if they didn't name it in the query.
    allowed_sources = {s.lower() for s in (req.sources or [])} or None
    raw_apps = {a.lower() for a in (req.apps or [])}

    # Only treat the app filter as a real narrowing signal when the user has
    # deselected at least one app. If all three are on (or none are on), the
    # filter is a no-op and app-tagged docs should still be reachable.
    apps_narrowing = 0 < len(raw_apps) < len(APP_CODES)
    allowed_apps = raw_apps if apps_narrowing else None

    # Meta / conversational chatter short-circuit: "can I ask another query?",
    # "thanks", "who are you". No retrieval — return a canned response so we
    # don't pollute the UI with BM25 noise on a topicless prompt.
    if _is_meta_chatter(req.query):
        record_question(req.query)
        return JSONResponse({
            "query": req.query,
            "answer": (
                "Of course — go ahead and ask. I can pull from Confluence, GitHub, "
                "and SharePoint. Try naming an app (ABC/SSM/EPM), a doc type "
                "(runbook, RCA, entitlement register, unit-testing), or a topic "
                "(Snowflake access, VPN, CRQ)."
            ),
            "source_cards": [],
            "citations": [],
            "latest_source": None,
            "conflict": None,
            "followup": None,
            "ranking_debug": [],
        })

    # Follow-up handling. We compute *two* prior references:
    #   - prior_user: the immediately-preceding user turn (for the UI's
    #     "Following up on:" chip — what the user just said).
    #   - anchor_user: the last non-follow-up user turn (for retrieval blending
    #     — the topic that anchors this whole thread).
    # A chain like "unit tests for SSM" → "github only?" → "newest?" should
    # keep retrieving against the SSM anchor, not against the one-word tails.
    prior_user = _prior_user_turn(req.history)
    anchor_user = _anchor_user_turn(req.history)
    prior_content = _content_tokens(anchor_user) if anchor_user else None
    is_followup = bool(anchor_user) and _looks_like_followup(req.query, prior_content)
    retrieval_query = f"{anchor_user} {req.query}" if is_followup else req.query

    # Intent-driven scoping: if the user's query names an app (e.g. "SSM") or a
    # doc-type ("unit testing"), we treat that as an authoritative narrowing.
    # For follow-ups we look at the *blended* query so "can you point these
    # docs in github only?" inherits "unit testing" / "SSM" from the prior turn.
    intent_query = retrieval_query
    query_apps = _detect_query_apps(intent_query)
    if query_apps:
        allowed_apps = (query_apps & allowed_apps) if allowed_apps else query_apps

    # Sources: "in confluence and github?" must NOT fall back to SharePoint hits.
    # A follow-up saying "github only" should scope the *current* turn to
    # github regardless of what the prior turn scoped to — so we detect sources
    # on the current query first, and only fall back to the blended query when
    # the current query didn't name any source.
    query_sources = _detect_query_sources(req.query)
    if not query_sources and is_followup:
        query_sources = _detect_query_sources(intent_query)
    if query_sources:
        allowed_sources = (
            (query_sources & allowed_sources) if allowed_sources else query_sources
        )

    doc_type = _detect_doc_type(intent_query)

    def passes(doc: dict) -> bool:
        if allowed_sources is not None and doc["source"] not in allowed_sources:
            return False
        if allowed_apps is not None:
            doc_apps = _doc_apps(doc)
            # SharePoint docs must be in the allowed app set. Non-SharePoint
            # docs (Confluence/GitHub) that carry an app tag must also match;
            # docs with no app tag are cross-cutting and always pass.
            if doc_apps and not (doc_apps & allowed_apps):
                return False
        if doc_type is not None:
            tags = {t.lower() for t in doc.get("tags", [])}
            if doc_type not in tags:
                return False
        return True

    ranked = _index.search(retrieval_query, top_k=req.top_k, doc_filter=passes)

    # Record the raw user question (not the blended query) for the FAQ counter.
    record_question(req.query)

    followup_ctx = (
        {"prior_query": prior_user, "blended_query": retrieval_query}
        if is_followup
        else None
    )
    result = synthesize_answer(req.query, ranked, followup=followup_ctx)
    return JSONResponse(
        {
            "query": req.query,
            **result,
            "ranking_debug": [
                {
                    "id": d["id"],
                    "source": d["source"],
                    "title": d["title"],
                    "score": round(s, 3),
                    "updated_at": d["updated_at"],
                }
                for (d, s) in ranked
            ],
        }
    )


@app.get("/api/faqs")
def faqs(limit: int = 6):
    """Dynamic Frequently Asked Questions — top N by ask-count, backfilled
    with seeded defaults so we always return `limit` rows."""
    return {"faqs": top_faqs(limit=limit)}


@app.get("/doc/{doc_id}", response_class=HTMLResponse)
def get_doc(doc_id: str):
    doc = _index.get(doc_id)
    if not doc:
        raise HTTPException(status_code=404, detail=f"No such doc: {doc_id}")
    return HTMLResponse(render_doc(doc, _index.all_docs()))


# Serve the SPA at "/"
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/")
def root():
    return FileResponse(STATIC_DIR / "index.html")
