# Compass
### Navigating direction to appropriate docs

**A unified AI copilot for banking onboarding.**
One question. Every source. Always current.

Live demo: `http://localhost:8000/`
Built for the banking hackathon.

---

## 1. The Cover

**Compass** is an AI copilot that unifies onboarding documentation scattered across **Confluence**, **GitHub**, and **SharePoint** into a single chat interface.

A new joiner asks a question in plain English. Compass finds the answer across all three systems, prefers the most recently updated source, and cites every claim with a clickable link and a timestamp.

---

## 2. The Problem

New joiners lose weeks before they write a single line of code.

Onboarding docs live in three or more different systems. Nobody knows which copy is the real one.

- Policies on Confluence, sometimes 2 years stale
- Repo READMEs on GitHub, only devs know they exist
- HR / IT / compliance PDFs buried on SharePoint
- Real answer? Ask a colleague. Wait. Guess.

**By the numbers:**

| Metric | Value |
|---|---|
| Time to productivity | 2-3 weeks |
| Tools to log into | 30+ |
| "Go-to" bottleneck person | 1 |

In a regulated bank, following a stale policy is not just annoying. It is an audit finding.

---

## 3. The Insight

The docs are not missing. They are just **fragmented** and **out of date**.

> "I don't need someone to write more documentation.
> I need someone to find the **right** doc, and tell me it is still current."

Two principles drive Compass:

1. **Cite the source.** Every claim points to a numbered, clickable, timestamped document. This is auditability.
2. **Prefer the latest.** When two docs disagree, the newer one wins and we say why. This is compliance.

---

## 4. Meet Compass

A single chat that speaks every system.

Ask a question in plain English. Get the answer, the citation, the timestamp.

**Three pillars:**

- **Unified search.** One query fans out to Confluence, GitHub, and SharePoint. No more tab-juggling.
- **Recency-aware ranking.** Most recently updated doc wins ties. Stale KYC v2 loses to fresh KYC v4, every time.
- **Version-conflict alerts.** When two docs disagree on the same topic, we flag it, and steer to the newer one.

---

## 5. Live Demo

Prompts a new joiner would actually ask:

- *"How do I set up MFA and get a laptop?"*
- *"What is the KYC review process for corporate clients?"*
- *"Where is the payments-service repo and how do I run it locally?"*
- *"What is the incident-response process for a production outage?"*

**Try it:** `http://localhost:8000/`

Run the KYC prompt to see the version-conflict banner fire live.

---

## 6. Not Just Another Chatbot

Purpose-built for banks.

| Dimension | Generic AI chat | Compass |
|---|---|---|
| Sources | Whatever it was trained on | Only your systems, nothing else |
| Freshness | Frozen at training time | Reads live from source of truth |
| Citations | Often hallucinated | Every claim, clickable and timestamped |
| Version conflicts | Silently blends both | Flags them, prefers the newest |
| Data leaves the bank? | Yes | No. On-prem LLM ready. |

---

## 7. Architecture

Simple architecture. Boring is good.

```
 ┌──────────────┐   ┌──────────────┐   ┌──────────────┐
 │  Confluence  │   │    GitHub    │   │  SharePoint  │
 │  connector   │   │  connector   │   │  connector   │
 └──────┬───────┘   └──────┬───────┘   └──────┬───────┘
        │                  │                  │
        └──────────┬───────┴──────────┬───────┘
                   ▼                  ▼
         ┌─────────────────────────────┐
         │  Unified Index, BM25 + recency  │
         └────────────┬────────────────┘
                      ▼
         ┌─────────────────────────────┐
         │  Answer Synthesizer (RAG-ready)  │
         └────────────┬────────────────┘
                      ▼
                FastAPI  ➜  Chat UI
```

The connector abstraction means each source has the same shape. Swapping mock data for real APIs is a one-file change per system.

---

## 8. How the AI Finds the Best Answer

From your question to a cited answer, in 5 steps. This is Retrieval-Augmented Generation (RAG), tuned for banking.

### The pipeline

1. **Understand.** Parse the question. Extract key terms and intent (policy, code, HR).
   *Tech: tokenizer*

2. **Retrieve.** Fan out across all connected sources. Pull top matching docs.
   *Tech: BM25 + vector search*

3. **Re-rank.** Boost fresh docs. Penalize stale ones. Detect version conflicts.
   *Tech: recency decay*

4. **Ground.** Feed only the top-K passages to the LLM as context. Nothing else.
   *Tech: RAG prompt*

5. **Cite & verify.** Every claim mapped back to a source ID. Uncited claims dropped.
   *Tech: citation guard*

### The ranking formula

```
score = BM25(query, doc) × recency_boost(doc)

recency_boost = 0.7 + 0.6 × (0.5 ^ age_days / 180)
```

- A doc updated today gets a ~1.3× boost.
- A doc from 3 years ago gets ~0.7×.
- Freshness never overrules relevance, but it breaks ties the right way.

### Why this beats "ask ChatGPT"

- **Grounded, not guessed.** The LLM only sees your bank's docs. It cannot invent a policy that doesn't exist.
- **Freshness-aware.** Public LLMs are frozen at training time. Ours reads live from your source of truth.
- **Every claim traceable.** Answer text is linked to source IDs. An auditor can reconstruct *why* we said it.

### Model choice

Today: a rule-based synthesizer (no external model, easy demo).

Prod path: any enterprise-hosted LLM - Azure OpenAI, AWS Bedrock (Claude / Titan), or an on-prem Llama-3 / Mistral. The RAG pipeline is model-agnostic - the model is a swappable component, not a lock-in.

---

## 9. Banking-Safe by Design

What your security team will ask, and how we answer.

- **No data leaves the bank.** Demo runs locally. Prod pairs with on-prem or private-cloud LLM.
- **Per-user access controls.** Connectors know identity. Results filtered before ranking.
- **Every answer auditable.** Citations + timestamps trace any answer to a specific version.
- **Latest wins, conflicts flagged.** No more following a deprecated policy by accident.

**Known risks (tracked, addressable):** LLM hallucination outside cited sources · connector rate limits · initial ingestion cost.

---

## 10. Business Impact

What it saves, and who benefits.

| Metric | Value |
|---|---|
| Time to first productive week | -70% |
| The "go-to" person | Scales 1:∞ |
| Answers cited and traceable | 100% |

**Bigger than onboarding.** The same unified-search fabric works for engineers hunting a policy at 2am, auditors reconstructing what a doc said last quarter, and support agents finding the right playbook. Instantly.

---

## 11. Roadmap

From prototype to production copilot.

**Next 2 weeks**
- Real Confluence + GitHub Enterprise APIs
- Vector search (semantic, not just keyword)
- Slack bot front-end

**Next 2 months**
- SSO + per-user ACLs
- SharePoint via MS Graph
- Enterprise LLM integration
- Feedback loop, learn from thumbs-up

**Next 2 quarters**
- Beyond onboarding: bank-wide policy Q&A
- Proactive nudges when a doc you rely on changes
- Regulator-ready audit trail

---

## 12. The Ask

Give us a pilot. We give you back weeks of ramp-up.

### What we need

- **1 pilot team** (5-6 people)
- **Read access** to 1 Confluence space, 1 GitHub org, 1 SharePoint site
- **4 weeks** of runway

Low commitment. Read-only.

### What you get

- New joiners productive on **day 3**, not day 21
- Every answer **cited, timestamped, auditable**
- A pattern that **generalizes** to every knowledge system in the bank

Fast ROI. Audit-ready.

> Four weeks. One team. A repeatable playbook for the whole bank.

---

## 13. Thank You

Questions?

Try it yourself: `http://localhost:8000/`

*Compass - Built for the banking hackathon. Ask a question. Get a cited answer. In seconds.*
