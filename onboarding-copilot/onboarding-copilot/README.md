# OnboardIQ — Unified Onboarding Copilot for Banking

A hackathon-ready prototype that unifies onboarding docs scattered across
**Confluence**, **GitHub**, and **SharePoint** into a single AI chat
experience. New joiners ask a question in natural language and get an answer
composed from the *latest* documents across all three systems — with citations,
source badges, and timestamps.

## Why it matters (banking angle)

- New joiners at banks routinely wait 2–3 weeks to become productive because
  onboarding material is fragmented across Confluence (policy/process),
  GitHub (code + READMEs), and SharePoint (HR/IT/compliance PDFs).
- Stale docs are worse than missing docs in regulated environments — this
  copilot always prefers the **most recently updated** source and shows the
  timestamp so users can trust what they read.
- No production data leaves the box — the demo uses mock banking docs and a
  local rule-based synthesizer (no external LLM call). Easy to slot in an
  enterprise-hosted LLM later.

## Run it

```bash
cd onboarding-copilot
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Open http://localhost:8000/

## Architecture

```
 ┌──────────────┐   ┌──────────────┐   ┌──────────────┐
 │  Confluence  │   │    GitHub    │   │  SharePoint  │
 │  connector   │   │  connector   │   │  connector   │
 └──────┬───────┘   └──────┬───────┘   └──────┬───────┘
        │                  │                  │
        └──────────┬───────┴──────────┬───────┘
                   ▼                  ▼
             ┌─────────────────────────────┐
             │   Unified Document Index    │  ← BM25 + recency boost
             └────────────┬────────────────┘
                          ▼
             ┌─────────────────────────────┐
             │  Answer Synthesizer (RAG)   │  ← rule-based, LLM-swappable
             └────────────┬────────────────┘
                          ▼
                    FastAPI /ask
                          ▼
                    Chat UI (SPA)
```

## Try these demo prompts

- *"How do I get access to the trading floor VPN?"*
- *"What's the KYC review process for a new corporate client?"*
- *"Where's the payments-service repo and how do I run it locally?"*
- *"Who do I contact for a laptop and MFA setup?"*
- *"What's our incident response process for a prod outage?"*
