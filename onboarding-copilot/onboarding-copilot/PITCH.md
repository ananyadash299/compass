# 🧭 Compass
### The search bar your onboarding docs never had.

---

## The 30-Second Pitch

> New joiners at the bank waste their first two weeks pinging teammates on Slack asking "where's the doc for X?" — because that doc could be in Confluence, GitHub, or SharePoint, and no single person knows all three.
>
> **Compass** is one search bar that reads all three at once, ranks the right doc first, warns you when two versions disagree, always cites its sources, and never sends your questions to a third-party AI. It runs on your machine.
>
> **The old way:** ping 5 people, wait a day.
> **The Compass way:** one question, one answer, one click.

---

## The Problem

A new joiner at the bank asks: *"How do I get access to the Snowflake warehouse?"*

Today, they have to:

| Step | What they do | Time |
|---|---|---|
| 1 | Guess where the doc lives (Confluence? GitHub? SharePoint?) | 5 min |
| 2 | Search each system separately, in three different UIs | 15 min |
| 3 | Get zero relevant results (search inside SharePoint is famously bad) | — |
| 4 | Slack their buddy | 2 min |
| 5 | Wait for a reply | **2–4 hours** |
| 6 | Get pointed at the wrong doc (an old one, superseded last month) | — |
| 7 | Follow the outdated policy → compliance risk | 🚨 |

**Multiply this by every new joiner, every quarter, across every team.**

The docs already exist. The problem isn't documentation — it's **findability**.

---

## The Big Idea — A Librarian in a Building With 3 Floors

Imagine a huge library with 3 floors:

- 🟦 **Floor 1: Confluence** — the wiki. Team pages, onboarding guides, runbooks.
- 🟩 **Floor 2: GitHub** — the code shelves. READMEs, developer docs, config repos.
- 🟨 **Floor 3: SharePoint** — the filing cabinet. Excel sheets, spreadsheets, forms.

Normally, you have to visit all 3 floors yourself, ask 3 different librarians, and hope one of them has read your specific book.

**Compass is one super-librarian who has already read every book on all three floors, remembers where each one lives, and answers your question in one shot.**

And this librarian has two ways of finding things:

- A **word-matcher** — a super-fast kid who counts exact words. Great for finding *"SSM-1998"* or *"NullPointerException"*.
- A **meaning-matcher** — a wise reader who understands what books are *about*. Great when you say *"postmortem"* but the doc is titled *"RCA"*.

The librarian asks BOTH of them, then merges their answers. That's how Compass gets you the right book even when you don't know exactly what it's called.

---

## The Solution — Compass in One Diagram

```
   YOU
    │
    │  "How do I get access to Snowflake?"
    ▼
┌──────────────────────────────────────────┐
│   COMPASS                                │
│                                          │
│   ┌────────┐  ┌────────┐  ┌────────┐   │
│   │Confluence│  │ GitHub │  │SharePoint│  │
│   └────────┘  └────────┘  └────────┘   │
│        \\           |           /        │
│         \\          |          /         │
│          ▼          ▼         ▼          │
│      ┌──────────────────────────┐        │
│      │  Hybrid Search (BM25+AI) │        │
│      └──────────────────────────┘        │
│                  │                       │
│                  ▼                       │
│          Ranked, cited answer            │
│          + "Latest doc" chip             │
│          + Conflict warning              │
└──────────────────────────────────────────┘
    │
    ▼
   Answer in < 100ms
```

---

## The Three Superpowers

### 🎯 1. Two Brains Are Better Than One

Compass runs **two searches in parallel** for every question:

| Brain | What it does | Strong at |
|---|---|---|
| **BM25 (word-matcher)** | Finds docs with your exact words | Product codes (`SSM-1998`), error names, rare terms |
| **AI (meaning-matcher)** | Finds docs that *mean* the same thing | Paraphrases — you say "postmortem", the doc says "RCA" |

Then it merges the rankings using **Reciprocal Rank Fusion** — the same approach used by production hybrid search at Google, Elastic, Weaviate.

**Concrete example:** you ask *"how do I request database credentials?"* — the doc is titled *"Database Access Request Procedure"*. Zero word overlap. Pure BM25 misses it. The meaning-matcher nails it. RRF puts it #1.

### 🕒 2. Newer Beats Older, Automatically

In a bank, the *wrong* doc is dangerous. Compass:

- Shows a **"Latest source"** chip so you know which doc is freshest
- Slightly boosts newer docs when scores are close
- **Detects conflicts** — if two docs cover the same topic 1+ year apart, Compass flags it:
  > ⚠️ *Heads up — this newer doc (July 2026) supersedes an older one (March 2025). Follow the newer one.*

**This is the compliance guardrail.** No more "I followed the doc I found" incidents.

### 💬 3. It Remembers The Conversation

Compass isn't a search box — it's a **chat**.

```
You:      "Any unit-testing docs for SSM?"
Compass:  [returns SSM unit test docs]

You:      "in GitHub only?"        ← 3 words! Meaningless alone.
Compass:  [remembers "SSM unit tests" from last turn,
           applies "GitHub only" filter,
           returns the right subset]

You:      "the newest one?"
Compass:  [still remembers, returns the most recent]
```

And when you switch topics:

```
You:      "how do I get Snowflake access?"
Compass:  [returns Snowflake docs]

You:      "anything on BMS?"       ← New topic! Not a follow-up.
Compass:  [doesn't drag Snowflake context in;
           says "no strong match" if BMS isn't in the corpus —
           HONEST instead of hallucinating]
```

The topic-shift detector prevents context pollution. The confidence gate prevents made-up answers.

---

## Why A Bank Should Care — Three Guardrails

| Guardrail | What it means | Why it matters |
|---|---|---|
| **🔒 Local AI model** | The meaning-matcher (~90MB) runs on your machine. Zero calls to OpenAI/Anthropic/anything. | No customer data or internal questions leave the bank's network. |
| **📎 Cites every claim** | Every answer links back to source docs with dates and authors. | Auditors can verify. Zero hallucinations. Zero "trust me, I'm an AI." |
| **🎭 Mock data in demo** | No real customer info, no PII, no internal secrets. | Demo is safe to show anywhere — and the same design works with real data behind the firewall. |

---

## The Live Demo — 5 Moments That Sell It

### Moment 1: The core query
> Type: *"How do I get access to Snowflake?"*
> → Right doc, top of the list, in under 100ms.

### Moment 2: The follow-up
> Type: *"can you point these in GitHub only?"*
> → Compass remembers, re-filters, still returns Snowflake-relevant docs (or none if there aren't any in GitHub — that's the honesty part).

### Moment 3: The honesty demo
> Type: *"anything on BMS?"*
> → Compass says: *"I couldn't find anything matching that."*
> **This is the killer moment.** Most AI demos hallucinate here. Compass tells the truth.

### Moment 4: The "Latest source" chip
> Point at it. Say:
> > *"This is how you never accidentally follow last year's policy."*

### Moment 5: The conflict warning
> If a query triggers it:
> > *"This is how we save you from a compliance incident."*

**Total demo: 3 minutes. Every moment lands.**

---

## The Architecture (One Slide)

```
Frontend  ─────  Static SPA (HTML + a bit of JS, 12 themes)
             │
             ▼
API        ─────  FastAPI + Uvicorn (Python 3.10+)
             │
             ▼
Pipeline   ─────  1. Meta detector    (short-circuit chatter)
                   2. Follow-up blender (anchor turn walk-back)
                   3. Intent scoping   (app/doc-type/source filters)
                   4. Hybrid search    (BM25 + dense + RRF)
                   5. Post-boosts      (recency + title/tag)
                   6. Confidence gate  (no-strong-match fallback)
                   7. Synthesizer      (answer + cards + conflict)
             │
             ▼
Data       ─────  Confluence  •  GitHub  •  SharePoint
                  (mock corpus, ~160 docs)

Models     ─────  • BM25Okapi (rank-bm25)
                  • all-MiniLM-L6-v2 (sentence-transformers, LOCAL)

Storage    ─────  In-memory index + JSON FAQ counter
                  (No DB. No cloud. No secrets.)
```

**Every component chosen so it can be swapped for a bank-grade equivalent later:**
- Mock connectors → real Confluence/GitHub/SharePoint APIs
- Local encoder → self-hosted enterprise model
- Rule-based synthesizer → LLM behind the firewall
- JSON FAQ store → Postgres

---

## Measurable Impact

| Metric | Before Compass | With Compass |
|---|---|---|
| Time to find the right onboarding doc | 30 min – 4 hours | **< 30 seconds** |
| Slack pings for "where's the doc for X?" | 5–10 per new joiner per week | Near zero |
| Risk of following a stale policy | High (no conflict detection) | Mitigated (auto-flagged) |
| Onboarding time-to-productivity | 2–4 weeks | **~1 week** (projected) |
| Cost per query | ~$0 (no cloud AI) | **~$0** (no cloud AI) |

---

## What Makes This Hackathon-Worthy

1. **It works.** Every feature in this document runs today. This isn't a slideware pitch.
2. **It's honest.** The demo intentionally includes a "no match" case — most AI demos hide those. Ours shows one.
3. **It's on-prem-ready.** Zero external API calls. Zero data leaves the box.
4. **It's fast.** Under 100ms per query on ~160 docs. Scales linearly to ~10K docs before needing a vector DB.
5. **It's a real UX.** 12 themes, dark mode, follow-up chat, multi-hop context, conflict warnings, "Latest source" chip.
6. **It's small.** A few Python files. Anyone on the team can read and extend it.

---

## What's Next (The Roadmap)

**Phase 1 — Pilot (2 weeks):**
Wire real Confluence + GitHub connectors in read-only mode. Run against one team's actual docs. Measure time-to-find delta.

**Phase 2 — Enterprise (4 weeks):**
Add SSO. Swap the local encoder for the bank's self-hosted enterprise model. Move FAQ store to Postgres.

**Phase 3 — Answer synthesis (6 weeks):**
Wire a self-hosted LLM into the synthesizer step to generate summarized answers with citations — not just ranked docs.

**Phase 4 — Insights (ongoing):**
Aggregate the FAQ counter — which docs are people looking for but not finding? That's your documentation gap map.

---

## The Elevator Pitch, One More Time

> **Compass is the search bar your onboarding docs never had.**
>
> It reads Confluence, GitHub, and SharePoint at the same time. It uses two AI brains — one for exact words, one for meaning — and merges their rankings. It shows you the newest doc, warns you when versions disagree, cites every claim, and never sends your questions to a third-party.
>
> One command to start. Under 100ms per query. No cloud, no secrets, no hallucinations.
>
> Ship it. 🧭

---

## Try It Yourself

```
# Windows
double-click start.bat

# macOS / Linux
./start.sh
```

Then open http://localhost:8000 and ask it anything.

---

*Compass — Navigating you to the right doc. ✨*
