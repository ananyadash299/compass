"""Generate Compass_Presentation.docx from the Markdown pitch."""
from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

BRAND = RGBColor(0x1E, 0x3A, 0x8A)
ACCENT = RGBColor(0x4F, 0x46, 0xE5)
MUTED = RGBColor(0x64, 0x74, 0x8B)
INK = RGBColor(0x0F, 0x17, 0x2A)

doc = Document()

# --- default style ---
style = doc.styles["Normal"]
style.font.name = "Calibri"
style.font.size = Pt(11)

def set_cell_shading(cell, color_hex):
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), color_hex)
    tc_pr.append(shd)

def h1(text):
    p = doc.add_paragraph()
    r = p.add_run(text)
    r.bold = True
    r.font.size = Pt(28)
    r.font.color.rgb = BRAND

def h2(text):
    p = doc.add_paragraph()
    r = p.add_run(text)
    r.bold = True
    r.font.size = Pt(18)
    r.font.color.rgb = BRAND
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(4)

def h3(text):
    p = doc.add_paragraph()
    r = p.add_run(text)
    r.bold = True
    r.font.size = Pt(13)
    r.font.color.rgb = ACCENT
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(2)

def para(text, italic=False, color=None, size=11):
    p = doc.add_paragraph()
    r = p.add_run(text)
    r.font.size = Pt(size)
    if italic:
        r.italic = True
    if color:
        r.font.color.rgb = color
    return p

def bullet(text):
    p = doc.add_paragraph(style="List Bullet")
    r = p.runs[0] if p.runs else p.add_run(text)
    if not p.runs:
        r = p.add_run(text)
    else:
        r.text = text
    r.font.size = Pt(11)

def quote(text):
    p = doc.add_paragraph()
    r = p.add_run(text)
    r.italic = True
    r.font.size = Pt(12)
    p.paragraph_format.left_indent = Inches(0.4)
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(6)

def code_block(text):
    p = doc.add_paragraph()
    r = p.add_run(text)
    r.font.name = "Consolas"
    r.font.size = Pt(9)
    p.paragraph_format.left_indent = Inches(0.3)
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(4)

def hrule():
    p = doc.add_paragraph()
    r = p.add_run("_" * 60)
    r.font.color.rgb = MUTED
    p.paragraph_format.space_after = Pt(6)

def slide_header(num, title):
    p = doc.add_paragraph()
    r = p.add_run(f"Slide {num}  ·  ")
    r.bold = True
    r.font.color.rgb = MUTED
    r.font.size = Pt(10)
    r2 = p.add_run(title)
    r2.bold = True
    r2.font.color.rgb = BRAND
    r2.font.size = Pt(16)
    p.paragraph_format.space_before = Pt(18)

def table_from_rows(headers, rows, header_shade="1E3A8A"):
    t = doc.add_table(rows=1 + len(rows), cols=len(headers))
    t.style = "Light Grid Accent 1"
    hdr = t.rows[0].cells
    for i, h in enumerate(headers):
        hdr[i].text = ""
        p = hdr[i].paragraphs[0]
        r = p.add_run(h)
        r.bold = True
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        r.font.size = Pt(11)
        set_cell_shading(hdr[i], header_shade)
    for ri, row in enumerate(rows, start=1):
        for ci, val in enumerate(row):
            c = t.rows[ri].cells[ci]
            c.text = ""
            p = c.paragraphs[0]
            r = p.add_run(str(val))
            r.font.size = Pt(10)
    doc.add_paragraph()

# ============================================================
# COVER
# ============================================================
p = doc.add_paragraph()
r = p.add_run("COMPASS")
r.bold = True
r.font.size = Pt(40)
r.font.color.rgb = BRAND
p.alignment = WD_ALIGN_PARAGRAPH.CENTER

p = doc.add_paragraph()
r = p.add_run("Navigating direction to appropriate docs")
r.italic = True
r.font.size = Pt(16)
r.font.color.rgb = ACCENT
p.alignment = WD_ALIGN_PARAGRAPH.CENTER

p = doc.add_paragraph()
r = p.add_run("A unified AI copilot for banking onboarding.")
r.font.size = Pt(12)
r.font.color.rgb = INK
p.alignment = WD_ALIGN_PARAGRAPH.CENTER

p = doc.add_paragraph()
r = p.add_run("One question. Every source. Always current.")
r.font.size = Pt(11)
r.font.color.rgb = MUTED
p.alignment = WD_ALIGN_PARAGRAPH.CENTER

p = doc.add_paragraph()
r = p.add_run("Live demo:  http://localhost:8000/")
r.font.size = Pt(11)
r.font.color.rgb = ACCENT
r.bold = True
p.alignment = WD_ALIGN_PARAGRAPH.CENTER

p = doc.add_paragraph()
r = p.add_run("Built for the banking hackathon")
r.font.size = Pt(10)
r.font.color.rgb = MUTED
p.alignment = WD_ALIGN_PARAGRAPH.CENTER

doc.add_page_break()

# ============================================================
# 1. COVER RECAP
# ============================================================
slide_header(1, "The Cover")
para(
    "Compass is an AI copilot that unifies onboarding documentation scattered across "
    "Confluence, GitHub, and SharePoint into a single chat interface."
)
para(
    "A new joiner asks a question in plain English. Compass finds the answer across all "
    "three systems, prefers the most recently updated source, and cites every claim "
    "with a clickable link and a timestamp."
)

# ============================================================
# 2. THE PROBLEM
# ============================================================
slide_header(2, "The Problem")
h3("New joiners lose weeks before they write a single line of code.")
para(
    "Onboarding docs live in three or more different systems. Nobody knows which copy "
    "is the real one."
)
bullet("Policies on Confluence, sometimes 2 years stale")
bullet("Repo READMEs on GitHub, only devs know they exist")
bullet("HR / IT / compliance PDFs buried on SharePoint")
bullet("Real answer? Ask a colleague. Wait. Guess.")

h3("By the numbers")
table_from_rows(
    ["Metric", "Value"],
    [
        ["Time to productivity", "2-3 weeks"],
        ["Tools to log into", "30+"],
        ["'Go-to' bottleneck person", "1"],
    ],
)
para(
    "In a regulated bank, following a stale policy is not just annoying. "
    "It is an audit finding.",
    italic=True,
    color=BRAND,
)

# ============================================================
# 3. THE INSIGHT
# ============================================================
slide_header(3, "The Insight")
h3("The docs are not missing. They are fragmented and out of date.")
quote(
    '"I don\'t need someone to write more documentation. '
    "I need someone to find the RIGHT doc, and tell me it is still current.\""
)
h3("Two principles drive Compass")
bullet("Cite the source. Every claim points to a numbered, clickable, timestamped document. This is auditability.")
bullet("Prefer the latest. When two docs disagree, the newer one wins and we say why. This is compliance.")

# ============================================================
# 4. MEET COMPASS
# ============================================================
slide_header(4, "Meet Compass")
h3("A single chat that speaks every system.")
para("Ask a question in plain English. Get the answer, the citation, the timestamp.")
h3("Three pillars")
bullet("Unified search. One query fans out to Confluence, GitHub, and SharePoint. No more tab-juggling.")
bullet("Recency-aware ranking. Most recently updated doc wins ties. Stale KYC v2 loses to fresh KYC v4, every time.")
bullet("Version-conflict alerts. When two docs disagree on the same topic, we flag it, and steer to the newer one.")

# ============================================================
# 5. LIVE DEMO
# ============================================================
slide_header(5, "Live Demo")
para("Prompts a new joiner would actually ask:")
bullet('"How do I set up MFA and get a laptop?"')
bullet('"What is the KYC review process for corporate clients?"')
bullet('"Where is the payments-service repo and how do I run it locally?"')
bullet('"What is the incident-response process for a production outage?"')
para("")
p = doc.add_paragraph()
r = p.add_run("Try it: ")
r.bold = True
r2 = p.add_run("http://localhost:8000/")
r2.font.color.rgb = ACCENT
r2.bold = True
para("Run the KYC prompt to see the version-conflict banner fire live.", italic=True, color=MUTED)

# ============================================================
# 6. NOT JUST ANOTHER CHATBOT
# ============================================================
slide_header(6, "Not Just Another Chatbot")
h3("Purpose-built for banks.")
table_from_rows(
    ["Dimension", "Generic AI chat", "Compass"],
    [
        ["Sources", "Whatever it was trained on", "Only your systems, nothing else"],
        ["Freshness", "Frozen at training time", "Reads live from source of truth"],
        ["Citations", "Often hallucinated", "Every claim, clickable and timestamped"],
        ["Version conflicts", "Silently blends both", "Flags them, prefers the newest"],
        ["Data leaves the bank?", "Yes", "No. On-prem LLM ready."],
    ],
)

# ============================================================
# 7. ARCHITECTURE
# ============================================================
slide_header(7, "Architecture")
h3("Simple architecture. Boring is good.")
code_block(
    " Confluence          GitHub            SharePoint\n"
    " connector           connector         connector\n"
    "     |                   |                 |\n"
    "     +---------+---------+--------+--------+\n"
    "               v                  v\n"
    "     +----------------------------------+\n"
    "     |  Unified Index (BM25 + recency)  |\n"
    "     +----------------------------------+\n"
    "                        v\n"
    "     +----------------------------------+\n"
    "     |  Answer Synthesizer (RAG-ready)  |\n"
    "     +----------------------------------+\n"
    "                        v\n"
    "               FastAPI  ==>  Chat UI"
)
para(
    "The connector abstraction means each source has the same shape. "
    "Swapping mock data for real APIs is a one-file change per system."
)

# ============================================================
# 8. HOW THE AI FINDS THE BEST ANSWER
# ============================================================
slide_header(8, "How the AI Finds the Best Answer")
h3("From your question to a cited answer, in 5 steps.")
para(
    "This is Retrieval-Augmented Generation (RAG), tuned for banking."
)

h3("The pipeline")
bullet("Understand. Parse the question. Extract key terms and intent (policy, code, HR).  [tokenizer]")
bullet("Retrieve. Fan out across all connected sources. Pull top matching docs.  [BM25 + vector search]")
bullet("Re-rank. Boost fresh docs. Penalize stale ones. Detect version conflicts.  [recency decay]")
bullet("Ground. Feed only the top-K passages to the LLM as context. Nothing else.  [RAG prompt]")
bullet("Cite & verify. Every claim mapped back to a source ID. Uncited claims dropped.  [citation guard]")

h3("The ranking formula")
code_block(
    "score = BM25(query, doc)  x  recency_boost(doc)\n"
    "\n"
    "recency_boost = 0.7 + 0.6 x (0.5 ^ (age_days / 180))"
)
bullet("A doc updated today gets a ~1.3x boost.")
bullet("A doc from 3 years ago gets ~0.7x.")
bullet("Freshness never overrules relevance, but it breaks ties the right way.")

h3("Why this beats 'ask ChatGPT'")
bullet("Grounded, not guessed. The LLM only sees your bank's docs. It cannot invent a policy that doesn't exist.")
bullet("Freshness-aware. Public LLMs are frozen at training time. Ours reads live from your source of truth.")
bullet("Every claim traceable. Answer text is linked to source IDs. An auditor can reconstruct why we said it.")

h3("Model choice")
para(
    "Today: a rule-based synthesizer (no external model, easy demo)."
)
para(
    "Prod path: any enterprise-hosted LLM - Azure OpenAI, AWS Bedrock (Claude / Titan), "
    "or an on-prem Llama-3 / Mistral. The RAG pipeline is model-agnostic - the model is a "
    "swappable component, not a lock-in."
)

# ============================================================
# 9. BANKING-SAFE BY DESIGN
# ============================================================
slide_header(9, "Banking-Safe by Design")
h3("What your security team will ask, and how we answer.")
bullet("No data leaves the bank. Demo runs locally. Prod pairs with on-prem or private-cloud LLM.")
bullet("Per-user access controls. Connectors know identity. Results filtered before ranking.")
bullet("Every answer auditable. Citations + timestamps trace any answer to a specific version.")
bullet("Latest wins, conflicts flagged. No more following a deprecated policy by accident.")
para(
    "Known risks (tracked, addressable): LLM hallucination outside cited sources, "
    "connector rate limits, initial ingestion cost.",
    italic=True,
    color=MUTED,
)

# ============================================================
# 10. BUSINESS IMPACT
# ============================================================
slide_header(10, "Business Impact")
h3("What it saves, and who benefits.")
table_from_rows(
    ["Metric", "Value"],
    [
        ["Time to first productive week", "-70%"],
        ["The 'go-to' person", "Scales 1:infinite"],
        ["Answers cited and traceable", "100%"],
    ],
)
para(
    "Bigger than onboarding. The same unified-search fabric works for engineers "
    "hunting a policy at 2am, auditors reconstructing what a doc said last quarter, "
    "and support agents finding the right playbook. Instantly.",
    color=BRAND,
)

# ============================================================
# 11. ROADMAP
# ============================================================
slide_header(11, "Roadmap")
h3("From prototype to production copilot.")

h3("Next 2 weeks")
bullet("Real Confluence + GitHub Enterprise APIs")
bullet("Vector search (semantic, not just keyword)")
bullet("Slack bot front-end")

h3("Next 2 months")
bullet("SSO + per-user ACLs")
bullet("SharePoint via MS Graph")
bullet("Enterprise LLM integration")
bullet("Feedback loop, learn from thumbs-up")

h3("Next 2 quarters")
bullet("Beyond onboarding: bank-wide policy Q&A")
bullet("Proactive nudges when a doc you rely on changes")
bullet("Regulator-ready audit trail")

# ============================================================
# 12. THE ASK
# ============================================================
slide_header(12, "The Ask")
h3("Give us a pilot. We give you back weeks of ramp-up.")

h3("What we need")
bullet("1 pilot team (5-6 people)")
bullet("Read access to 1 Confluence space, 1 GitHub org, 1 SharePoint site")
bullet("4 weeks of runway")
para("Low commitment. Read-only.", italic=True, color=MUTED)

h3("What you get")
bullet("New joiners productive on day 3, not day 21")
bullet("Every answer cited, timestamped, auditable")
bullet("A pattern that generalizes to every knowledge system in the bank")
para("Fast ROI. Audit-ready.", italic=True, color=MUTED)

quote("Four weeks. One team. A repeatable playbook for the whole bank.")

# ============================================================
# 13. THANK YOU
# ============================================================
slide_header(13, "Thank You")
p = doc.add_paragraph()
r = p.add_run("Questions?")
r.bold = True
r.font.size = Pt(20)
r.font.color.rgb = BRAND

para("")
p = doc.add_paragraph()
r = p.add_run("Try it yourself:  ")
r.bold = True
r2 = p.add_run("http://localhost:8000/")
r2.font.color.rgb = ACCENT
r2.bold = True

para("")
para(
    "Compass - Built for the banking hackathon.",
    italic=True,
    color=MUTED,
)
para(
    "Ask a question. Get a cited answer. In seconds.",
    italic=True,
    color=MUTED,
)

out = "/Users/rudrasish.pradhan/onboarding-copilot/Compass_Presentation.docx"
doc.save(out)
print(f"Written: {out}")
