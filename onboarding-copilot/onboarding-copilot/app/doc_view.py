"""
Renders any mock doc as a real, browsable HTML page.

Each source gets its own visual skin so a judge clicking a citation feels
they've landed on Confluence, GitHub, or SharePoint - even though the doc
lives inside our own backend.

The body of every doc supports a tiny markdown-lite dialect:
  ## heading  ->  <h2>
  ### heading ->  <h3>
  - bullet    ->  <ul><li>
  1. numbered ->  <ol><li>
  ```code```  ->  <pre>
  | a | b |   ->  <table>
  **bold**    ->  <strong>
Anything not matching falls through as a paragraph.
"""
from __future__ import annotations

import html
import re
from typing import Dict, List

from dateutil.parser import isoparse


# =============================================================================
# markdown-lite renderer (shared across skins)
# =============================================================================

_LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")


def _inline(text: str) -> str:
    """Escape then apply inline formatting: [text](url), **bold**, `code`."""
    # Pull out link tokens first so escaping doesn't mangle their URLs
    tokens: List[str] = []

    def _stash(m: re.Match) -> str:
        label = html.escape(m.group(1))
        url = html.escape(m.group(2), quote=True)
        tokens.append(f'<a href="{url}">{label}</a>')
        return f"\x00L{len(tokens) - 1}\x00"

    text = _LINK_RE.sub(_stash, text)
    text = html.escape(text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    for i, tok in enumerate(tokens):
        text = text.replace(f"\x00L{i}\x00", tok)
    return text


def _render_table(rows: List[str]) -> str:
    """Turn `| a | b |` block into a real HTML table."""
    cells = []
    for row in rows:
        parts = [c.strip() for c in row.strip().strip("|").split("|")]
        cells.append(parts)
    if not cells:
        return ""
    header = cells[0]
    body_rows = cells[1:]
    if body_rows and all(set(c.replace(" ", "")) <= set("-:") for c in body_rows[0]):
        body_rows = body_rows[1:]
    out = ["<table class='md-table'><thead><tr>"]
    for h in header:
        out.append(f"<th>{_inline(h)}</th>")
    out.append("</tr></thead><tbody>")
    for row in body_rows:
        out.append("<tr>")
        for c in row:
            out.append(f"<td>{_inline(c)}</td>")
        out.append("</tr>")
    out.append("</tbody></table>")
    return "".join(out)


def render_markdown(text: str) -> str:
    """Very small markdown-lite renderer sufficient for our mock docs."""
    lines = text.splitlines()
    i = 0
    out: List[str] = []

    def flush_paragraph(buf: List[str]):
        if buf:
            out.append(f"<p>{_inline(' '.join(buf).strip())}</p>")

    para_buf: List[str] = []

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # code fence
        if stripped.startswith("```"):
            flush_paragraph(para_buf); para_buf = []
            i += 1
            code_lines = []
            while i < len(lines) and not lines[i].strip().startswith("```"):
                code_lines.append(lines[i])
                i += 1
            out.append("<pre class='md-pre'>" + html.escape("\n".join(code_lines)) + "</pre>")
            i += 1
            continue

        # table
        if stripped.startswith("|") and stripped.endswith("|"):
            flush_paragraph(para_buf); para_buf = []
            table_rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                table_rows.append(lines[i])
                i += 1
            out.append(_render_table(table_rows))
            continue

        # heading
        if stripped.startswith("### "):
            flush_paragraph(para_buf); para_buf = []
            out.append(f"<h3>{_inline(stripped[4:])}</h3>")
            i += 1; continue
        if stripped.startswith("## "):
            flush_paragraph(para_buf); para_buf = []
            out.append(f"<h2>{_inline(stripped[3:])}</h2>")
            i += 1; continue
        if stripped.startswith("# "):
            flush_paragraph(para_buf); para_buf = []
            out.append(f"<h1>{_inline(stripped[2:])}</h1>")
            i += 1; continue

        # bullet list
        if re.match(r"^\s*[-*] ", line):
            flush_paragraph(para_buf); para_buf = []
            out.append("<ul>")
            while i < len(lines) and re.match(r"^\s*[-*] ", lines[i]):
                item = re.sub(r"^\s*[-*] ", "", lines[i])
                out.append(f"<li>{_inline(item)}</li>")
                i += 1
            out.append("</ul>")
            continue

        # numbered list
        if re.match(r"^\s*\d+\. ", line):
            flush_paragraph(para_buf); para_buf = []
            out.append("<ol>")
            while i < len(lines) and re.match(r"^\s*\d+\. ", lines[i]):
                item = re.sub(r"^\s*\d+\. ", "", lines[i])
                out.append(f"<li>{_inline(item)}</li>")
                i += 1
            out.append("</ol>")
            continue

        # blank line = paragraph break
        if not stripped:
            flush_paragraph(para_buf); para_buf = []
            i += 1
            continue

        para_buf.append(stripped)
        i += 1

    flush_paragraph(para_buf)
    return "\n".join(out)


def _fmt_date(iso: str) -> str:
    return isoparse(iso).strftime("%b %d, %Y at %H:%M UTC")


def _fmt_date_short(iso: str) -> str:
    return isoparse(iso).strftime("%m/%d/%Y %H:%M")


# =============================================================================
# CONFLUENCE skin
# =============================================================================

CONFLUENCE_CSS = """
  * { box-sizing: border-box; }
  body { margin:0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; background:#fafbfc; color:#172B4D; font-size:14px; }
  /* top brand bar */
  .cf-topbar { background:#0052CC; color:#fff; height:44px; display:flex; align-items:center; padding: 0 16px; gap:14px; }
  .cf-topbar .apps { font-size:18px; opacity:.9; }
  .cf-topbar .logo { font-weight:700; letter-spacing:.2px; display:flex; align-items:center; gap:6px; font-size:15px; }
  .cf-topbar .logo svg { display:block; }
  .cf-topbar .search { flex:1; max-width:520px; margin: 0 24px; }
  .cf-topbar .search input { width:100%; padding:6px 10px; border-radius:3px; border:none; font-size:13px; }
  .cf-topbar .actions { display:flex; gap:14px; align-items:center; font-size:13px; opacity:.95; }
  .cf-topbar .create { background:#fff; color:#0052CC; font-weight:600; padding:6px 12px; border-radius:3px; font-size:13px; }
  /* secondary nav */
  .cf-subnav { background:#fff; border-bottom:1px solid #dfe1e6; padding: 0 24px; display:flex; gap:22px; height:40px; align-items:center; font-size:13px; color:#42526E; }
  .cf-subnav a { color:#42526E; text-decoration:none; padding: 10px 4px; border-bottom:2px solid transparent; }
  .cf-subnav a.active { color:#0052CC; border-bottom-color:#0052CC; font-weight:600; }
  /* layout */
  .cf-layout { display:grid; grid-template-columns: 260px 1fr 260px; gap:0; max-width:1400px; margin:0 auto; }
  .cf-side { border-right:1px solid #dfe1e6; background:#fafbfc; padding:16px 12px; min-height:calc(100vh - 84px); font-size:13px; }
  .cf-side h4 { font-size:11px; text-transform:uppercase; letter-spacing:.08em; color:#6B778C; margin: 10px 6px 6px; }
  .cf-side .tree-item { padding:5px 8px; border-radius:3px; color:#172B4D; display:block; text-decoration:none; }
  .cf-side .tree-item:hover { background:#EBECF0; }
  .cf-side .tree-item.current { background:#DEEBFF; color:#0052CC; font-weight:600; }
  .cf-side .tree-item.nested { padding-left:22px; color:#42526E; }
  .cf-main { padding: 24px 40px; background:#fff; min-height:calc(100vh - 84px); }
  .cf-right { border-left:1px solid #dfe1e6; padding:16px 12px; font-size:12px; color:#42526E; background:#fafbfc; }
  .cf-right .rail-btn { display:flex; gap:8px; align-items:center; padding:6px 8px; border-radius:3px; cursor:pointer; }
  .cf-right .rail-btn:hover { background:#EBECF0; }
  /* content */
  .cf-breadcrumb { color:#6B778C; font-size:12px; margin-bottom:8px; }
  .cf-breadcrumb a { color:#6B778C; text-decoration:none; }
  .cf-breadcrumb a:hover { text-decoration:underline; }
  h1.cf-title { font-size:28px; font-weight:500; color:#172B4D; margin: 0 0 8px; letter-spacing:-.01em; }
  .cf-byline { color:#6B778C; font-size:12.5px; margin-bottom: 20px; display:flex; gap:14px; align-items:center; }
  .cf-byline .avatar { width:24px; height:24px; border-radius:50%; background:#0052CC; color:#fff; display:inline-flex; align-items:center; justify-content:center; font-size:11px; font-weight:600; }
  .cf-body h2 { font-size:22px; font-weight:500; color:#172B4D; margin: 24px 0 10px; }
  .cf-body h3 { font-size:17px; font-weight:600; color:#172B4D; margin: 18px 0 8px; }
  .cf-body p { line-height: 1.55; margin: 8px 0; color:#172B4D; }
  .cf-body ul, .cf-body ol { line-height: 1.55; margin: 8px 0; padding-left: 24px; }
  .cf-body li { margin: 3px 0; }
  .cf-body code { background:#F4F5F7; padding: 1px 5px; border-radius:3px; font-family: SFMono-Regular, Consolas, monospace; font-size:.9em; color:#172B4D; }
  .cf-body pre.md-pre { background:#F4F5F7; border:1px solid #dfe1e6; padding:12px 14px; border-radius:3px; overflow:auto; font-family: SFMono-Regular, Consolas, monospace; font-size:12.5px; line-height:1.5; color:#172B4D; }
  .cf-body table.md-table { border-collapse: collapse; margin: 10px 0; font-size:13.5px; width:100%; }
  .cf-body table.md-table th { background:#F4F5F7; text-align:left; padding:8px 10px; border:1px solid #dfe1e6; font-weight:600; color:#172B4D; }
  .cf-body table.md-table td { padding:8px 10px; border:1px solid #dfe1e6; vertical-align:top; }
  .cf-tags { margin-top: 24px; padding-top:16px; border-top:1px dashed #dfe1e6; }
  .cf-tags .pill { display:inline-block; background:#DEEBFF; color:#0052CC; font-size:11px; font-weight:600; padding:2px 8px; border-radius:3px; margin-right:4px; }
  .demo-banner { background:#FFFAE6; color:#5D4037; border-bottom:1px solid #FFE380; padding:6px 24px; font-size:12px; text-align:center; }
  .back { display:inline-block; margin: 24px 0 0; color:#0052CC; text-decoration:none; font-size:13px; font-weight:600; }
  .back:hover { text-decoration:underline; }
"""

CONFLUENCE_LOGO_SVG = """
<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
  <path d="M1 18.2c-.3.5-.1 1.1.4 1.4l3.5 2.2c.5.3 1.2.1 1.5-.4 3-4.6 4.8-5 8-4 3.5 1.1 5.4 3.3 8.1 3.3.9 0 1.5-.4 1.5-1.2v-3c0-.5-.4-1-1-1.1-3-.6-4.6-3.1-7.8-4.2-3.3-1.2-8.1-1-14.2 7z" fill="#2684FF"/>
  <path d="M23 5.8c.3-.5.1-1.1-.4-1.4l-3.5-2.2c-.5-.3-1.2-.1-1.5.4-3 4.6-4.8 5-8 4-3.5-1.1-5.4-3.3-8.1-3.3-.9 0-1.5.4-1.5 1.2v3c0 .5.4 1 1 1.1 3 .6 4.6 3.1 7.8 4.2 3.3 1.2 8.1 1 14.2-7z" fill="#0052CC"/>
</svg>
"""


def _confluence_avatar(author: str) -> str:
    initials = "".join([p[0] for p in author.replace("(", " ").split() if p and p[0].isalpha()][:2]).upper()
    return initials or "?"


def render_confluence(doc: Dict, index_docs: List[Dict]) -> str:
    title = html.escape(doc["title"])
    author = html.escape(doc["author"])
    fake_url = html.escape(doc["url"])
    body_html = render_markdown(doc["body"])
    updated = _fmt_date(doc["updated_at"])
    avatar = _confluence_avatar(doc["author"])

    # Build sidebar page tree from other confluence docs (max 15)
    tree_items = []
    for d in index_docs:
        if d.get("source") != "confluence":
            continue
        is_current = d["id"] == doc["id"]
        cls = "tree-item current" if is_current else "tree-item nested"
        tree_items.append(
            f'<a class="{cls}" href="/doc/{html.escape(d["id"])}">{html.escape(d["title"])}</a>'
        )
    tree_html = "\n".join(tree_items[:20])
    space_name = doc.get("tags", ["Space"])[0].upper() if doc.get("tags") else "SPACE"

    tags_html = "".join(f'<span class="pill">{html.escape(t)}</span>' for t in doc.get("tags", []))

    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<title>{title} - Confluence</title>
<meta name="viewport" content="width=device-width, initial-scale=1" />
<style>{CONFLUENCE_CSS}</style>
</head>
<body>

<div class="cf-topbar">
  <span class="apps">&#9776;</span>
  <span class="logo">{CONFLUENCE_LOGO_SVG}<span>Confluence</span></span>
  <div class="search"><input placeholder="Search" /></div>
  <div class="actions">
    <span>Help</span>
    <span>Spaces</span>
    <span>People</span>
    <span>Calendars</span>
    <span>Analytics</span>
    <span class="create">+ Create</span>
  </div>
</div>

<div class="cf-subnav">
  <a href="#">Space Home</a>
  <a href="#" class="active">Pages</a>
  <a href="#">Blog</a>
  <a href="#">Space Tools</a>
</div>

<div class="demo-banner">
  This page is served by the <strong>Compass</strong> demo. In production this would be the real Confluence page at <code>{fake_url}</code>.
</div>

<div class="cf-layout">
  <aside class="cf-side">
    <h4>Space: {html.escape(space_name)}</h4>
    <a class="tree-item" href="#">Overview</a>
    <a class="tree-item" href="#">Pages</a>
    <h4>Page tree</h4>
    {tree_html}
  </aside>

  <main class="cf-main">
    <div class="cf-breadcrumb">
      <a href="#">Pages</a> / <a href="#">{html.escape(space_name)}</a> / {title}
    </div>
    <h1 class="cf-title">{title}</h1>
    <div class="cf-byline">
      <span class="avatar">{avatar}</span>
      <span>Created by <strong>{author}</strong>, last updated on {updated}</span>
    </div>

    <div class="cf-body">
      {body_html}
    </div>

    <div class="cf-tags">
      Labels: {tags_html}
    </div>

    <a class="back" href="/">&larr; Back to Compass</a>
  </main>

  <aside class="cf-right">
    <div class="rail-btn">&#9734; Save for later</div>
    <div class="rail-btn">&#128172; View sitting comments</div>
    <div class="rail-btn">&#128065; Watching</div>
    <div class="rail-btn">&#8635; Page history</div>
    <hr style="border:none;border-top:1px solid #dfe1e6;margin:12px 0;" />
    <h4 style="font-size:11px;text-transform:uppercase;letter-spacing:.08em;color:#6B778C;margin:8px 0;">Page info</h4>
    <div>Owner: {author}</div>
    <div>Updated: {updated}</div>
    <div>Page ID: {html.escape(doc["id"])}</div>
  </aside>
</div>

</body>
</html>
"""


# =============================================================================
# SHAREPOINT skin
# =============================================================================

SHAREPOINT_CSS = """
  * { box-sizing: border-box; }
  body { margin:0; font-family: "Segoe UI", -apple-system, BlinkMacSystemFont, Roboto, sans-serif; background:#fff; color:#333; font-size:13.5px; }
  /* top brand bar */
  .sp-topbar { background:#fff; border-bottom:1px solid #edebe9; height:52px; display:flex; align-items:center; padding: 0 20px; gap:18px; }
  .sp-topbar .sp-brand { display:flex; align-items:center; gap:10px; }
  .sp-topbar .sp-brand svg { display:block; }
  .sp-topbar .sp-word { font-size:16px; color:#333; font-weight:600; }
  .sp-topbar .sp-word .accent { color:#036C70; font-weight:700; }
  .sp-topbar .search { margin-left:20px; flex:1; max-width:520px; }
  .sp-topbar .search input { width:100%; padding:6px 10px; border-radius:2px; border:1px solid #d1d1d1; background:#f3f2f1; font-size:13px; }
  .sp-topbar .avatar { margin-left:auto; width:32px; height:32px; border-radius:50%; background:#036C70; color:#fff; display:flex; align-items:center; justify-content:center; font-size:12px; font-weight:600; }
  /* layout */
  .sp-layout { display:grid; grid-template-columns: 220px 1fr; }
  .sp-side { background:#f3f2f1; padding: 16px 0; min-height:calc(100vh - 52px); border-right:1px solid #edebe9; font-size:13px; }
  .sp-side .sp-rail-item { display:flex; align-items:center; gap:10px; padding:8px 20px; color:#333; text-decoration:none; }
  .sp-side .sp-rail-item:hover { background:#edebe9; }
  .sp-side .sp-rail-item.active { background:#e1dfdd; font-weight:600; color:#036C70; }
  .sp-side .sp-rail-item .ico { width:18px; text-align:center; font-size:14px; }
  .sp-side h4 { font-size:11px; text-transform:uppercase; letter-spacing:.06em; color:#605e5c; margin: 18px 20px 6px; }
  .sp-side .sp-rail-item .badge { margin-left:auto; background:#036C70; color:#fff; font-size:10px; padding:1px 6px; border-radius:8px; }
  .sp-main { padding: 20px 32px; min-height:calc(100vh - 52px); }
  .sp-crumbs { color:#605e5c; font-size:12px; margin-bottom:6px; }
  .sp-crumbs a { color:#036C70; text-decoration:none; }
  .sp-site-header { display:flex; align-items:center; gap:14px; margin-bottom:16px; }
  .sp-site-icon { width:48px; height:48px; background:#036C70; color:#fff; border-radius:3px; display:flex; align-items:center; justify-content:center; font-weight:700; font-size:16px; letter-spacing:-.5px; }
  .sp-site-title h1 { margin:0; font-size:22px; font-weight:600; color:#333; }
  .sp-site-title .sub { font-size:12px; color:#605e5c; }
  .sp-tabs { border-bottom:1px solid #edebe9; margin-bottom:14px; display:flex; gap:16px; }
  .sp-tabs a { padding:8px 4px; font-size:13px; color:#605e5c; text-decoration:none; border-bottom:2px solid transparent; }
  .sp-tabs a.active { color:#036C70; border-bottom-color:#036C70; font-weight:600; }
  .sp-actions { display:flex; gap:12px; margin-bottom:14px; font-size:13px; }
  .sp-actions .btn { padding:6px 12px; border:1px solid #d1d1d1; background:#fff; border-radius:2px; color:#036C70; font-weight:600; cursor:pointer; }
  .sp-actions .btn:hover { background:#f3f2f1; }
  .sp-view { color:#036C70; font-size:12px; margin-bottom:6px; }
  .sp-view .divider { color:#d1d1d1; margin: 0 8px; }
  /* file library table */
  .sp-body h2, .sp-body h3 { color:#333; margin: 18px 0 8px; }
  .sp-body h2 { font-size:18px; font-weight:600; }
  .sp-body h3 { font-size:15px; font-weight:600; }
  .sp-body p { line-height:1.55; margin: 6px 0; }
  .sp-body ul, .sp-body ol { line-height:1.55; padding-left:24px; }
  .sp-body code { background:#f3f2f1; padding:1px 5px; border-radius:2px; font-family: Consolas, monospace; font-size:.9em; }
  .sp-body pre.md-pre { background:#faf9f8; border:1px solid #edebe9; padding:12px 14px; border-radius:2px; overflow:auto; font-family: Consolas, monospace; font-size:12.5px; line-height:1.5; }
  .sp-body table.md-table { border-collapse: collapse; margin: 10px 0; font-size:13px; width:100%; }
  .sp-body table.md-table th { background:#faf9f8; text-align:left; padding:8px 10px; border-bottom:2px solid #036C70; font-weight:600; color:#333; }
  .sp-body table.md-table td { padding:8px 10px; border-bottom:1px solid #edebe9; }
  .sp-body table.md-table tbody tr:hover { background:#f3f2f1; }
  .sp-body a { color:#036C70; text-decoration:none; font-weight:500; }
  .sp-body a:hover { text-decoration:underline; }
  .demo-banner { background:#FFF4CE; color:#8a6d3b; border-bottom:1px solid #f0d78d; padding:6px 24px; font-size:12px; text-align:center; }
  .back { display:inline-block; margin: 22px 0 0; color:#036C70; text-decoration:none; font-size:13px; font-weight:600; }
"""


SHAREPOINT_LOGO_SVG = """
<svg width="34" height="34" viewBox="0 0 34 34" xmlns="http://www.w3.org/2000/svg">
  <rect x="1" y="1" width="32" height="32" rx="3" fill="#036C70"/>
  <text x="17" y="21" font-family="Segoe UI, Arial, sans-serif" font-size="13" font-weight="700" fill="#ffffff" text-anchor="middle">SP</text>
</svg>
"""

# Static definition of the three application sites and their folders.
# Used both by the left rail and by the breadcrumb builder.
SP_APPS = [
    {
        "code": "ABC",
        "name": "ABC - Analytics & Compliance",
        "home_id": "SP-ABC-HOME",
        "folders": [
            ("ADHOC Requests", "SP-ABC-ADHOC-INDEX", "abc-adhoc"),
            ("Analysis", "SP-ABC-ANALYSIS-INDEX", "abc-analysis"),
            ("Releases", "SP-ABC-RELEASES-INDEX", "abc-releases"),
            ("Business Data Requirements", "SP-ABC-BDR-INDEX", "abc-bdr"),
            ("Onboarding New Member", "SP-ABC-ONBOARDING-INDEX", "abc-onboarding"),
            ("Planning", "SP-ABC-PLANNING-INDEX", "abc-planning"),
        ],
    },
    {
        "code": "SSM",
        "name": "SSM - Shared Services & Migration",
        "home_id": "SP-SSM-HOME",
        "folders": [
            ("ADHOC Requests", "SP-SSM-ADHOC-INDEX", "ssm-adhoc"),
            ("Analysis", "SP-SSM-ANALYSIS-INDEX", "ssm-analysis"),
            ("Releases", "SP-SSM-RELEASES-INDEX", "ssm-releases"),
            ("Business Data Requirements", "SP-SSM-BDR-INDEX", "ssm-bdr"),
            ("Onboarding New Member", "SP-SSM-ONBOARDING-INDEX", "ssm-onboarding"),
            ("Planning", "SP-SSM-PLANNING-INDEX", "ssm-planning"),
        ],
    },
    {
        "code": "EPM",
        "name": "EPM - Enterprise Performance Mgmt",
        "home_id": "SP-EPM-HOME",
        "folders": [
            ("ADHOC Requests", "SP-EPM-ADHOC-INDEX", "epm-adhoc"),
            ("Analysis", "SP-EPM-ANALYSIS-INDEX", "epm-analysis"),
            ("Releases", "SP-EPM-RELEASES-INDEX", "epm-releases"),
            ("Business Data Requirements", "SP-EPM-BDR-INDEX", "epm-bdr"),
            ("Onboarding New Member", "SP-EPM-ONBOARDING-INDEX", "epm-onboarding"),
            ("Planning", "SP-EPM-PLANNING-INDEX", "epm-planning"),
        ],
    },
]


def _resolve_sp_context(doc: Dict) -> Dict:
    """
    Figure out which app and folder a SharePoint doc belongs to based on tag prefix.
    Returns {app, folder, folder_id, folder_label, app_label, is_app_home, is_folder_index}.
    """
    tags = [t.lower() for t in doc.get("tags", [])]
    doc_id = doc.get("id", "")

    app_entry = None
    for a in SP_APPS:
        if a["code"].lower() in tags:
            app_entry = a
            break

    is_app_home = doc_id.endswith("-HOME")
    is_folder_index = doc_id.endswith("-INDEX")

    folder = None
    if app_entry:
        for label, fid, ftag in app_entry["folders"]:
            if ftag.split("-", 1)[1] in tags or fid == doc_id:
                folder = (label, fid, ftag)
                break

    return {
        "app": app_entry,
        "folder": folder,
        "is_app_home": is_app_home,
        "is_folder_index": is_folder_index,
    }


def render_sharepoint(doc: Dict, index_docs: List[Dict]) -> str:
    title = html.escape(doc["title"])
    author = html.escape(doc["author"])
    fake_url = html.escape(doc["url"])
    body_html = render_markdown(doc["body"])
    updated = _fmt_date(doc["updated_at"])
    ctx = _resolve_sp_context(doc)
    app_entry = ctx["app"]
    folder = ctx["folder"]

    site_initials = app_entry["code"] if app_entry else "SP"
    site_name = app_entry["name"] if app_entry else "Shared Documents"

    # Breadcrumb path back to the app home and folder index
    crumbs = ['<a href="/">Home</a>']
    if app_entry:
        crumbs.append(f'<a href="/doc/{app_entry["home_id"]}">{html.escape(app_entry["code"])}</a>')
    if folder and not ctx["is_folder_index"]:
        f_label, f_id, _ = folder
        crumbs.append(f'<a href="/doc/{f_id}">{html.escape(f_label)}</a>')
    crumbs.append(f'<span>{title}</span>')
    crumbs_html = " &gt; ".join(crumbs)

    # Left rail: three apps and their folders. Current app is expanded.
    rail_parts: List[str] = []
    rail_parts.append('<a class="sp-rail-item" href="/"><span class="ico">&#127968;</span> Home</a>')
    rail_parts.append('<h4>Applications</h4>')
    for a in SP_APPS:
        is_active_app = app_entry is not None and a["code"] == app_entry["code"]
        cls = "sp-rail-item active" if is_active_app else "sp-rail-item"
        rail_parts.append(
            f'<a class="{cls}" href="/doc/{a["home_id"]}"><span class="ico">&#128194;</span> {html.escape(a["code"])}</a>'
        )
        if is_active_app:
            for f_label, f_id, _ in a["folders"]:
                is_active_folder = (folder is not None and f_id == folder[1]) or f_id == doc.get("id")
                sub_cls = "sp-rail-item active" if is_active_folder else "sp-rail-item"
                rail_parts.append(
                    f'<a class="{sub_cls}" style="padding-left:44px;" href="/doc/{f_id}">'
                    f'<span class="ico">&#128462;</span> {html.escape(f_label)}</a>'
                )
    rail_parts.append('<h4>Shortcuts</h4>')
    rail_parts.append('<a class="sp-rail-item" href="/"><span class="ico">&#128269;</span> Ask Compass</a>')
    rail_parts.append('<a class="sp-rail-item" href="/doc/SP-ABC-HOME"><span class="ico">&#11088;</span> ABC Home</a>')
    rail_parts.append('<a class="sp-rail-item" href="/doc/SP-SSM-HOME"><span class="ico">&#11088;</span> SSM Home</a>')
    rail_parts.append('<a class="sp-rail-item" href="/doc/SP-EPM-HOME"><span class="ico">&#11088;</span> EPM Home</a>')
    rail_html = "\n".join(rail_parts)

    # Tabs - Documents active on library pages, Home active on app landing
    docs_active = "" if ctx["is_app_home"] else "active"
    home_active = "active" if ctx["is_app_home"] else ""
    app_home_href = f"/doc/{app_entry['home_id']}" if app_entry else "/"

    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<title>{title} - {html.escape(site_name)} - SharePoint</title>
<meta name="viewport" content="width=device-width, initial-scale=1" />
<style>{SHAREPOINT_CSS}</style>
</head>
<body>

<div class="sp-topbar">
  <div class="sp-brand">
    {SHAREPOINT_LOGO_SVG}
    <div class="sp-word">Share<span class="accent">Point</span></div>
  </div>
  <div class="search"><input placeholder="Search this site" /></div>
  <div class="avatar">{_confluence_avatar(doc["author"])}</div>
</div>

<div class="demo-banner">
  This page is served by the <strong>Compass</strong> demo. In production this would be the real SharePoint page at <code>{fake_url}</code>.
</div>

<div class="sp-layout">
  <aside class="sp-side">
    {rail_html}
  </aside>

  <main class="sp-main">
    <div class="sp-crumbs">{crumbs_html}</div>
    <div class="sp-site-header">
      <div class="sp-site-icon">{html.escape(site_initials)}</div>
      <div class="sp-site-title">
        <h1>{title}</h1>
        <div class="sub">Modified {updated} by {author}</div>
      </div>
    </div>

    <div class="sp-tabs">
      <a href="{app_home_href}" class="{home_active}">Home</a>
      <a href="{app_home_href}" class="{docs_active}">Documents</a>
      <a href="/">Ask Compass</a>
    </div>

    <div class="sp-view">All Documents <span class="divider">|</span> Modified {updated}</div>
    <div class="sp-actions">
      <a class="btn" href="{app_home_href}">&#8629; Back to library</a>
      <a class="btn" href="/">&#128269; Search in Compass</a>
    </div>

    <div class="sp-body">
      {body_html}
    </div>

    <a class="back" href="/">&larr; Back to Compass</a>
  </main>
</div>

</body>
</html>
"""


# =============================================================================
# GITHUB skin
# =============================================================================

GITHUB_CSS = """
  * { box-sizing: border-box; }
  body { margin:0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans", Helvetica, Arial, sans-serif; background:#ffffff; color:#1F2328; font-size:14px; }
  .gh-topbar { background:#24292f; color:#fff; padding:12px 24px; display:flex; align-items:center; gap:16px; }
  .gh-topbar .octocat { font-size:22px; }
  .gh-topbar .search { background:#161b22; border:1px solid #30363d; border-radius:6px; padding:5px 10px; color:#c9d1d9; font-size:13px; flex:1; max-width:320px; }
  .gh-topbar .nav { margin-left:auto; display:flex; gap:16px; font-size:14px; color:#c9d1d9; }
  .gh-repo-header { padding: 16px 32px 0; border-bottom:1px solid #d1d9e0; background:#ffffff; }
  .gh-repo-title { font-size:20px; margin: 4px 0 12px; }
  .gh-repo-title .octicon { color:#59636e; margin-right:6px; }
  .gh-repo-title a { color:#0969DA; text-decoration:none; }
  .gh-repo-title .sep { color:#59636e; margin: 0 2px; }
  .gh-repo-title .visibility { border:1px solid #d1d9e0; padding:1px 8px; border-radius:12px; font-size:11px; margin-left:8px; color:#59636e; font-weight:500; vertical-align:middle; }
  .gh-repo-tabs { display:flex; gap:6px; }
  .gh-repo-tabs a { padding:8px 12px; font-size:14px; color:#1F2328; text-decoration:none; border-bottom:2px solid transparent; display:flex; align-items:center; gap:6px; }
  .gh-repo-tabs a.active { border-bottom-color:#FD8C73; font-weight:600; }
  .gh-repo-tabs a .count { background:#eaeef2; padding:1px 6px; border-radius:20px; font-size:11px; color:#1F2328; }
  .gh-layout { max-width: 1280px; margin: 24px auto; padding: 0 32px; display:grid; grid-template-columns: 1fr 296px; gap: 24px; }
  .gh-file-header { border:1px solid #d1d9e0; border-radius:6px 6px 0 0; background:#f6f8fa; padding:8px 16px; font-size:12px; color:#59636e; display:flex; gap:12px; align-items:center; }
  .gh-file-header .branch { background:#ffffff; border:1px solid #d1d9e0; padding:2px 8px; border-radius:6px; font-size:12px; color:#1F2328; font-weight:500; }
  .gh-readme { border:1px solid #d1d9e0; border-top:none; border-radius:0 0 6px 6px; padding: 32px 40px; background:#ffffff; }
  .gh-readme h1 { font-size:2em; padding-bottom:.3em; border-bottom:1px solid #d1d9e0; margin: 24px 0 16px; font-weight:600; }
  .gh-readme h1:first-child { margin-top:0; }
  .gh-readme h2 { font-size:1.5em; padding-bottom:.3em; border-bottom:1px solid #d1d9e0; margin: 24px 0 16px; font-weight:600; }
  .gh-readme h3 { font-size:1.25em; margin: 24px 0 16px; font-weight:600; }
  .gh-readme p { margin:0 0 16px; line-height:1.6; }
  .gh-readme ul, .gh-readme ol { margin:0 0 16px; padding-left:28px; }
  .gh-readme li { margin:2px 0; line-height:1.5; }
  .gh-readme code { background:rgba(175,184,193,0.2); padding: 0.2em 0.4em; border-radius:6px; font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; font-size:85%; }
  .gh-readme pre.md-pre { background:#f6f8fa; border-radius:6px; padding:16px; overflow:auto; font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; font-size:85%; line-height:1.45; margin: 0 0 16px; }
  .gh-readme table.md-table { border-collapse: collapse; margin: 0 0 16px; font-size:14px; }
  .gh-readme table.md-table th { background:#f6f8fa; text-align:left; padding:6px 13px; border:1px solid #d1d9e0; font-weight:600; }
  .gh-readme table.md-table td { padding:6px 13px; border:1px solid #d1d9e0; }
  .gh-side { font-size:14px; }
  .gh-side h3 { font-size:14px; font-weight:600; margin: 0 0 8px; color:#1F2328; }
  .gh-side .about { color:#59636e; margin-bottom:12px; line-height:1.5; }
  .gh-side .topics { display:flex; flex-wrap:wrap; gap:6px; margin-bottom:16px; }
  .gh-side .topic { background:#DDF4FF; color:#0969DA; font-size:12px; padding:0 10px; border-radius:20px; line-height:22px; font-weight:500; }
  .gh-side .stats { border-top:1px solid #d1d9e0; padding-top:12px; color:#59636e; font-size:13px; }
  .gh-side .stats div { margin:6px 0; }
  .demo-banner { background:#DDF4FF; color:#0969DA; border-bottom:1px solid #b6e3ff; padding:6px 24px; font-size:12px; text-align:center; }
  .back { display:inline-block; margin: 24px 0 0; color:#0969DA; text-decoration:none; font-size:14px; font-weight:500; }
"""

GITHUB_OCTOCAT_SVG = """
<svg height="32" viewBox="0 0 16 16" width="32" fill="#fff" xmlns="http://www.w3.org/2000/svg">
  <path fill-rule="evenodd" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"/>
</svg>
"""


def _repo_path_from_url(url: str) -> str:
    m = re.match(r"https?://[^/]+/(.+)", url)
    return m.group(1) if m else "org/repo"


def render_github(doc: Dict, index_docs: List[Dict]) -> str:
    title = html.escape(doc["title"])
    author = html.escape(doc["author"])
    fake_url = html.escape(doc["url"])
    body_html = render_markdown(doc["body"])
    updated = _fmt_date(doc["updated_at"])
    repo_path = _repo_path_from_url(doc["url"])
    parts = repo_path.split("/", 1)
    org = html.escape(parts[0]) if parts else "org"
    repo = html.escape(parts[1]) if len(parts) > 1 else "repo"
    tags = doc.get("tags", [])
    topics_html = "".join(f'<span class="topic">{html.escape(t)}</span>' for t in tags)

    about = doc["body"].strip().split("\n")[0].lstrip("# ").strip()
    about = html.escape(about[:180])

    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<title>{org}/{repo} - GitHub Enterprise</title>
<meta name="viewport" content="width=device-width, initial-scale=1" />
<style>{GITHUB_CSS}</style>
</head>
<body>

<div class="gh-topbar">
  {GITHUB_OCTOCAT_SVG}
  <div class="search">Type / to search</div>
  <div class="nav">
    <span>Pull requests</span>
    <span>Issues</span>
    <span>Marketplace</span>
    <span>Explore</span>
  </div>
</div>

<div class="demo-banner">
  This page is served by the <strong>Compass</strong> demo. In production this would be the real GitHub page at <code>{fake_url}</code>.
</div>

<div class="gh-repo-header">
  <div class="gh-repo-title">
    <span class="octicon">&#128193;</span>
    <a href="#">{org}</a><span class="sep"> / </span><a href="#"><strong>{repo}</strong></a>
    <span class="visibility">Private</span>
  </div>
  <div class="gh-repo-tabs">
    <a href="#" class="active">&#60;&#62; Code</a>
    <a href="#">&#9432; Issues <span class="count">12</span></a>
    <a href="#">&#8644; Pull requests <span class="count">3</span></a>
    <a href="#">&#9654; Actions</a>
    <a href="#">&#128194; Projects</a>
    <a href="#">&#128218; Wiki</a>
    <a href="#">&#128274; Security</a>
    <a href="#">&#128200; Insights</a>
    <a href="#">&#9881; Settings</a>
  </div>
</div>

<div class="gh-layout">
  <div>
    <div class="gh-file-header">
      <span class="branch">&#128194; main</span>
      <span>Go to file</span>
      <span>Add file</span>
      <span style="margin-left:auto;">Latest commit by <strong>{author}</strong> on {updated}</span>
    </div>
    <article class="gh-readme markdown-body">
      {body_html}
    </article>
    <a class="back" href="/">&larr; Back to Compass</a>
  </div>

  <aside class="gh-side">
    <h3>About</h3>
    <div class="about">{about}</div>
    <div class="topics">{topics_html}</div>
    <div class="stats">
      <div>&#9734; 42 stars</div>
      <div>&#128065; 8 watching</div>
      <div>&#128110; 6 contributors</div>
      <div>&#128218; MIT License</div>
    </div>
    <h3 style="margin-top:16px;">Releases</h3>
    <div class="about">No releases published</div>
    <h3 style="margin-top:16px;">Packages</h3>
    <div class="about">No packages published</div>
  </aside>
</div>

</body>
</html>
"""


# =============================================================================
# dispatcher
# =============================================================================

def render_doc(doc: Dict, index_docs: List[Dict] | None = None) -> str:
    """Render a doc using the skin appropriate for its source."""
    index_docs = index_docs or []
    src = doc.get("source", "confluence")
    if src == "confluence":
        return render_confluence(doc, index_docs)
    if src == "github":
        return render_github(doc, index_docs)
    if src == "sharepoint":
        return render_sharepoint(doc, index_docs)
    return render_confluence(doc, index_docs)
