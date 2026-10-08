"""
Rule-based answer synthesizer.

Not a real LLM — but produces a coherent, cited answer from the top-ranked
docs. Structure mirrors how an LLM-backed answer would look, so swapping in
an LLM later is a drop-in change (see `answer_with_llm()` stub).

Design choices for the banking demo:
- Always cite. Every claim points to a numbered source.
- Highlight the newest doc. Show a "Latest source" chip so users can trust
  what they're reading in a regulated environment.
- Detect a version conflict (same topic, different dates) and warn the user.
"""
from __future__ import annotations

import re
from typing import List, Dict, Tuple
from dateutil.parser import isoparse


_SENT_SPLIT = re.compile(r"(?<=[.!?])\s+")
_MD_HEADING = re.compile(r"^\s{0,3}#{1,6}\s+")
_MD_LIST_BULLET = re.compile(r"^\s*[-*+]\s+")
_MD_ORDERED_BULLET = re.compile(r"^\s*\d+\.\s+")
_MD_LINK_ONLY = re.compile(r"^\s*\[[^\]]+\]\([^)]+\)\s*[.,;]?\s*$")


def _split_sentences(text: str) -> List[str]:
    """Split into sentences, but first flatten markdown noise so the sentence
    picker doesn't return a `### Heading` line or a raw markdown-link line."""
    cleaned_lines: List[str] = []
    for raw in text.splitlines():
        line = raw.rstrip()
        if not line.strip():
            cleaned_lines.append("")
            continue
        # Drop markdown table rows entirely - the table extractor owns them.
        if _MD_TABLE_ROW.match(line):
            continue
        # Drop lines that are just a markdown link (attachment refs).
        if _MD_LINK_ONLY.match(line):
            continue
        # Strip heading hashes so the text remains but doesn't render as "###".
        line = _MD_HEADING.sub("", line)
        # Strip leading bullet markers so list items read as sentences.
        line = _MD_LIST_BULLET.sub("", line)
        line = _MD_ORDERED_BULLET.sub("", line)
        cleaned_lines.append(line)

    flat = " ".join(l for l in cleaned_lines if l.strip())
    return [s.strip() for s in _SENT_SPLIT.split(flat) if s.strip()]


def _score_sentence(sentence: str, query_tokens: set) -> float:
    tokens = re.findall(r"[a-zA-Z0-9]+", sentence.lower())
    if not tokens:
        return 0.0
    # Favor sentences that are substantive (>= 6 tokens) so we don't return a
    # short header-y fragment when a full-context sentence is available.
    hits = sum(1 for t in tokens if t in query_tokens)
    length_bonus = 0.15 if len(tokens) >= 6 else 0.0
    return hits / (len(tokens) ** 0.5) + length_bonus


def _pick_snippets(doc: Dict, query: str, max_sentences: int = 2) -> str:
    q_tokens = set(re.findall(r"[a-zA-Z0-9]+", query.lower()))
    sentences = _split_sentences(doc["body"])
    if not sentences:
        # Fallback: strip any leading markdown heading from the raw body.
        return _MD_HEADING.sub("", doc["body"].lstrip())[:280]
    scored = sorted(
        ((s, _score_sentence(s, q_tokens)) for s in sentences),
        key=lambda x: x[1],
        reverse=True,
    )
    top = [s for s, sc in scored[:max_sentences] if sc > 0]
    if not top:
        top = sentences[:max_sentences]
    return " ".join(top)


def _extract_lead(body: str, max_sentences: int = 3) -> str:
    """First substantive prose from the doc - used as a 'hero' paragraph on
    the top card so the #1 result reads like a real answer rather than a
    two-sentence teaser. Skips markdown noise via _split_sentences."""
    sentences = _split_sentences(body)
    if not sentences:
        return ""
    return " ".join(sentences[:max_sentences])


_MD_TABLE_ROW = re.compile(r"^\s*\|.+\|\s*$")

# Downloadable file attachments referenced inside a doc body as
# `[filename.ext](/path/to/file.ext)` — surfaced as chips on the source card
# so users can click a real download button instead of parsing a snippet.
_ATTACHMENT_EXTS = (
    "xlsx", "xls", "csv",
    "docx", "doc",
    "pptx", "ppt",
    "pdf",
    "zip",
)
_ATTACHMENT_LINK = re.compile(
    r"\[([^\]]+\.(?:" + "|".join(_ATTACHMENT_EXTS) + r"))\]\(([^)]+)\)",
    re.IGNORECASE,
)


def _extract_attachments(body: str):
    """Pull downloadable file links out of the doc body.

    Returns a list of {name, url, ext} dicts (dedup'd by url) so the UI can
    render a proper download chip on the source card instead of relying on
    the plain-text snippet.
    """
    seen = set()
    out = []
    for m in _ATTACHMENT_LINK.finditer(body):
        name, url = m.group(1).strip(), m.group(2).strip()
        if url in seen:
            continue
        seen.add(url)
        ext = name.rsplit(".", 1)[-1].lower() if "." in name else ""
        out.append({"name": name, "url": url, "ext": ext})
    return out


def _extract_best_table(body: str, query: str, max_rows: int = 8):
    """
    If the doc body contains one or more markdown tables, return a compact
    slice of the most query-relevant one. Returns None when the doc isn't
    table-heavy — the caller falls back to sentence snippets.
    """
    lines = body.splitlines()
    tables = []
    cur = []
    for ln in lines:
        if _MD_TABLE_ROW.match(ln):
            cur.append(ln)
        else:
            if len(cur) >= 3:
                tables.append(cur)
            cur = []
    if len(cur) >= 3:
        tables.append(cur)
    if not tables:
        return None

    q_tokens = set(re.findall(r"[a-zA-Z0-9]+", query.lower()))

    def _row_score(row: str) -> float:
        toks = re.findall(r"[a-zA-Z0-9]+", row.lower())
        if not toks:
            return 0.0
        return sum(1 for t in toks if t in q_tokens) / (len(toks) ** 0.5)

    best = max(tables, key=lambda t: sum(_row_score(r) for r in t))
    if len(best) < 3:
        return None

    header, sep, *data = best
    if not data:
        return None
    scored_rows = sorted(data, key=_row_score, reverse=True)
    kept = scored_rows[:max_rows]
    # Preserve original ordering after ranking so the table still reads top-to-bottom.
    kept_set = set(id(r) for r in kept)
    kept_in_order = [r for r in data if id(r) in kept_set]

    truncated = len(data) > max_rows
    md = "\n".join([header, sep, *kept_in_order])
    if truncated:
        md += f"\n\n_Showing top {len(kept_in_order)} of {len(data)} rows — open the source for the full table._"
    return md


def _fmt_date(iso: str) -> str:
    return isoparse(iso).strftime("%b %d, %Y")


def _detect_conflict(top_docs: List[Dict]) -> Dict | None:
    """Detect a likely v1-vs-v2 policy conflict — same tag family, very different dates."""
    if len(top_docs) < 2:
        return None
    for i in range(len(top_docs)):
        for j in range(i + 1, len(top_docs)):
            a, b = top_docs[i], top_docs[j]
            shared_tags = set(a.get("tags", [])) & set(b.get("tags", []))
            shared_tags -= {"onboarding", "hr", "policy", "mandatory"}
            if not shared_tags:
                continue
            da = isoparse(a["updated_at"])
            db = isoparse(b["updated_at"])
            gap_days = abs((da - db).days)
            if gap_days > 300:
                newer, older = (a, b) if da > db else (b, a)
                return {
                    "newer": newer,
                    "older": older,
                    "gap_days": gap_days,
                    "topic": ", ".join(sorted(shared_tags)),
                }
    return None


def synthesize_answer(
    query: str,
    ranked: List[Tuple[Dict, float]],
    followup: Dict | None = None,
) -> Dict:
    # Confidence gate. Hybrid RRF scores are small (~0.05-0.15 for real hits;
    # noise sits around 0.02-0.035). Below this floor the retriever is
    # basically guessing — surface a "no strong match" message instead of
    # pretending we found something. Prevents queries like "anything on bms?"
    # (a term not in the corpus) from returning loose lexical noise.
    MIN_TOP_SCORE = 0.035
    if not ranked or ranked[0][1] < MIN_TOP_SCORE:
        return {
            "answer": (
                "I couldn't find anything matching that in the connected sources"
                "(selected in sidebar). Try rephrasing, or ask your buddy "
                "to point you at the right space."
            ),
            "source_cards": [],
            "citations": [],
            "latest_source": None,
            "conflict": None,
            "followup": followup,
        }

    top_docs = [d for d, _ in ranked]
    # Only consider the docs we actually cite when picking the "latest" chip —
    # avoids surfacing a low-relevance-but-recent doc as the trust signal.
    cited_docs = top_docs[:4]

    latest = max(cited_docs, key=lambda d: d["updated_at"])

    conflict = _detect_conflict(cited_docs)

    intro_lines: List[str] = []
    if followup and followup.get("prior_query"):
        prior = followup["prior_query"]
        # Truncate so a long prior question doesn't blow up the header line.
        if len(prior) > 90:
            prior = prior[:87].rstrip() + "…"
        intro_lines.append(f"↪️ _Following up on: **{prior}**_")
        intro_lines.append("")
    intro_lines.append(
        f"Here's what I found across your connected sources — {len(cited_docs)} "
        f"relevant doc{'s' if len(cited_docs) != 1 else ''}, with the most recent surfaced first."
    )

    # Structured cards for the UI to render. Keeping snippets out of the answer
    # markdown is what stops the response from looking like a data dump.
    # Content amount decays by rank: the #1 card is the "hero" with the most
    # substance, and #4 gets a one-liner teaser. This mirrors how a user's
    # attention naturally cascades - top-of-list should read like the answer,
    # bottom-of-list should read like a see-also.
    #
    # Budget per rank:
    #   rank 1 (hero): lead paragraph + up to 12 table rows / 5 sentences
    #   rank 2       :                   up to 8  table rows / 3 sentences
    #   rank 3       :                   up to 5  table rows / 2 sentences
    #   rank 4       :                   up to 3  table rows / 1 sentence
    ROWS_BY_RANK = {1: 12, 2: 8, 3: 5, 4: 3}
    SENTS_BY_RANK = {1: 5, 2: 3, 3: 2, 4: 1}

    source_cards: List[Dict] = []
    for i, doc in enumerate(top_docs[:4], start=1):
        is_top = i == 1
        max_rows = ROWS_BY_RANK.get(i, 3)
        n_sents = SENTS_BY_RANK.get(i, 1)
        table_md = _extract_best_table(doc["body"], query, max_rows=max_rows)
        if table_md:
            snippet, snippet_kind = table_md, "table"
        else:
            snippet, snippet_kind = _pick_snippets(doc, query, max_sentences=n_sents), "text"
        source_cards.append({
            "n": i,
            "id": doc["id"],
            "title": doc["title"],
            "source": doc["source"],
            "url": doc["url"],
            "author": doc["author"],
            "updated_at": doc["updated_at"],
            "updated_at_pretty": _fmt_date(doc["updated_at"]),
            "snippet": snippet,
            "snippet_kind": snippet_kind,
            "hero_lead": _extract_lead(doc["body"]) if is_top else "",
            "attachments": _extract_attachments(doc["body"]),
            "is_latest": doc["id"] == latest["id"],
            "is_top": is_top,
            "rank_tier": i,  # UI can use this to further tune density if needed
        })

    outro_lines: List[str] = []
    if conflict:
        outro_lines.append(
            f"⚠️ **Heads up — possible version conflict on _{conflict['topic']}_.** "
            f"The newer doc ({_fmt_date(conflict['newer']['updated_at'])}) supersedes an older one "
            f"({_fmt_date(conflict['older']['updated_at'])}, {conflict['gap_days']} days older). "
            f"Follow the newer one."
        )

    # Legacy `answer` field: keep the intro + optional conflict warning so any
    # client that hasn't upgraded still gets a readable message.
    lines: List[str] = list(intro_lines)
    if outro_lines:
        lines.append("")
        lines.extend(outro_lines)

    citations = [
        {
            "n": i + 1,
            "id": d["id"],
            "source": d["source"],
            "title": d["title"],
            "url": d["url"],
            "author": d["author"],
            "updated_at": d["updated_at"],
            "updated_at_pretty": _fmt_date(d["updated_at"]),
        }
        for i, d in enumerate(top_docs)
    ]

    return {
        "answer": "\n".join(lines),
        "source_cards": source_cards,
        "citations": citations,
        "latest_source": {
            "title": latest["title"],
            "source": latest["source"],
            "updated_at": latest["updated_at"],
            "updated_at_pretty": _fmt_date(latest["updated_at"]),
            "url": latest["url"],
        },
        "conflict": (
            {
                "topic": conflict["topic"],
                "newer_id": conflict["newer"]["id"],
                "older_id": conflict["older"]["id"],
            }
            if conflict
            else None
        ),
        "followup": followup,
    }


def answer_with_llm(query: str, ranked: List[Tuple[Dict, float]]) -> Dict:  # pragma: no cover
    """
    Drop-in slot for a real LLM. Not wired in this demo.

    In prod you'd build a prompt like:
        system: "You are the bank's onboarding copilot. Cite every claim."
        user: query + numbered doc snippets from `ranked`.
    and post to the enterprise-hosted LLM. The response shape must match
    synthesize_answer() so the UI is agnostic.
    """
    return synthesize_answer(query, ranked)
