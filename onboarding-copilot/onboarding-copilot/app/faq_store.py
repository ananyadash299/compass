"""
Lightweight JSON-backed FAQ counter.

Tracks how often each question is asked so the landing screen can surface
the popular ones. Deliberately dumb: normalizes the query text, bumps a
counter, and writes atomically. No DB — this is a demo store.
"""
from __future__ import annotations

import json
import os
import re
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional

_STORE_PATH = Path(__file__).resolve().parent / "data" / "faq_counts.json"
_LOCK = threading.Lock()

# Seeded so the demo isn't empty on first load. Any user question that
# normalizes to one of these keys will merge into the same counter.
DEFAULT_FAQS = [
    {"icon": "📦", "q": "What's the latest component list for the current CRQ release?"},
    {"icon": "🔐", "q": "How do I get access to the Finance BI Snowflake warehouse?"},
    {"icon": "📁", "q": "Where do I find the ABC ADHOC register and the intake form?"},
    {"icon": "🚀", "q": "What's the UCP → ENT Wave 2 cutover runbook?"},
    {"icon": "📝", "q": "Show me the RCA template for a payment gateway outage."},
    {"icon": "🏷️", "q": "What's the LDAP group naming convention for entitlements?"},
]

# Rough icon guesser for user-supplied questions so the UI stays consistent.
_ICON_RULES = [
    (re.compile(r"\b(ldap|entitlement|access|role|group)\b", re.I), "🔐"),
    (re.compile(r"\b(runbook|cutover|deploy|release|crq)\b", re.I), "🚀"),
    (re.compile(r"\b(rca|incident|outage|postmortem)\b", re.I), "📝"),
    (re.compile(r"\b(snowflake|warehouse|bi|analytics|dashboard)\b", re.I), "📊"),
    (re.compile(r"\b(register|intake|form|request)\b", re.I), "📁"),
    (re.compile(r"\b(component|artifact|package|build)\b", re.I), "📦"),
    (re.compile(r"\b(onboard|new hire|new joiner|welcome)\b", re.I), "👋"),
    (re.compile(r"\b(vpn|network|firewall|proxy)\b", re.I), "🌐"),
    (re.compile(r"\b(mfa|2fa|password|okta|badge)\b", re.I), "🛡️"),
]


def _guess_icon(text: str) -> str:
    for rx, icon in _ICON_RULES:
        if rx.search(text):
            return icon
    return "💬"


_WS = re.compile(r"\s+")


def _normalize(q: str) -> str:
    """Trim + collapse whitespace + lowercase. Used as the dedupe key."""
    return _WS.sub(" ", q.strip().lower())


def _load() -> Dict:
    if not _STORE_PATH.exists():
        return {"counts": {}}
    try:
        with _STORE_PATH.open("r") as f:
            data = json.load(f)
        if not isinstance(data, dict) or "counts" not in data:
            return {"counts": {}}
        return data
    except (json.JSONDecodeError, OSError):
        return {"counts": {}}


def _save(data: Dict) -> None:
    _STORE_PATH.parent.mkdir(parents=True, exist_ok=True)
    tmp = _STORE_PATH.with_suffix(".tmp")
    with tmp.open("w") as f:
        json.dump(data, f, indent=2)
    os.replace(tmp, _STORE_PATH)


def record_question(raw_query: str) -> None:
    """Bump the counter for this query. Safe to call on every /api/ask."""
    q = raw_query.strip()
    if len(q) < 3:
        return
    key = _normalize(q)
    now = datetime.now(timezone.utc).isoformat()
    with _LOCK:
        data = _load()
        entry = data["counts"].get(key)
        if entry is None:
            entry = {
                "display": q,
                "count": 0,
                "first_seen": now,
                "last_seen": now,
                "icon": _guess_icon(q),
            }
        entry["count"] += 1
        entry["last_seen"] = now
        # Keep the shortest reasonable display form so a later verbose phrasing
        # doesn't overwrite a clean earlier one.
        if len(q) < len(entry.get("display", q)) and len(q) > 8:
            entry["display"] = q
        data["counts"][key] = entry
        _save(data)


def top_faqs(limit: int = 6, trending_hours: int = 24) -> List[Dict]:
    """
    Return the top-N most-asked questions. Backfilled with seeded defaults
    so we always return exactly `limit` items even on a cold store.
    """
    with _LOCK:
        data = _load()
    entries = list(data.get("counts", {}).values())
    # Sort by count desc, then most-recent last_seen as a tiebreaker.
    entries.sort(key=lambda e: (e.get("count", 0), e.get("last_seen", "")), reverse=True)

    now = datetime.now(timezone.utc)
    result: List[Dict] = []
    seen_keys = set()
    for e in entries[:limit]:
        try:
            last = datetime.fromisoformat(e["last_seen"])
            trending = (now - last).total_seconds() / 3600.0 <= trending_hours and e["count"] >= 2
        except (KeyError, ValueError):
            trending = False
        result.append({
            "q": e["display"],
            "icon": e.get("icon") or _guess_icon(e["display"]),
            "count": e.get("count", 0),
            "trending": trending,
        })
        seen_keys.add(_normalize(e["display"]))

    # Backfill with defaults so a fresh demo still shows 6 rows.
    for d in DEFAULT_FAQS:
        if len(result) >= limit:
            break
        if _normalize(d["q"]) in seen_keys:
            continue
        result.append({"q": d["q"], "icon": d["icon"], "count": 0, "trending": False})
        seen_keys.add(_normalize(d["q"]))

    return result[:limit]
