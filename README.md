# iba-twin-guard

> **Govern your digital twin. Human intent required before any clone acts.**

AI can now clone your personality, voice, face, and entire digital identity from seconds of data. The clone can speak for you, negotiate for you, transact for you, and represent you — autonomously, indefinitely, at scale.

Who authorized it to do any of that?

---

## The Gap

Digital twin platforms — voice cloning, personality replication, avatar synthesis, knowledge distillation — create autonomous agents that operate in your name.

Without a signed intent certificate:

- The clone can speak in any context — authorized or not
- The clone can transact under your identity — with no declared limits
- The clone can be replicated further — without your knowledge
- The clone can be used commercially — without your consent
- The clone never expires — it runs indefinitely

**Your digital twin is an agent. It needs a gate.**

---

## The IBA Layer

```
┌─────────────────────────────────────────────────┐
│                HUMAN PRINCIPAL                  │
│   Signs .iba.yaml before any twin is created    │
│   or deployed                                   │
└───────────────────────┬─────────────────────────┘
                        │  Signed Intent Certificate
                        │  · Declared use cases
                        │  · Forbidden: commercial, replication
                        │  · Identity scope
                        │  · Hard expiry
                        │  · Kill threshold
                        ▼
┌─────────────────────────────────────────────────┐
│              IBA TWIN GUARD                     │
│   Validates certificate before the twin         │
│   speaks, acts, transacts, or replicates        │
│                                                 │
│   No cert = No twin activation                  │
└───────────────────────┬─────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────┐
│         YOUR DIGITAL TWIN                       │
│   Voice · Personality · Avatar · Knowledge      │
│   Any digital twin or identity replication      │
│   pipeline                                      │
└─────────────────────────────────────────────────┘
```

---

## Quick Start

```bash
git clone https://github.com/Grokipaedia/iba-twin-guard.git
cd iba-twin-guard
pip install -r requirements.txt
python guard.py your-twin-data.json --hollow medium
```

---

## Configuration — .iba.yaml

```yaml
intent:
  description: "Personal assistant twin for internal meeting summaries only. No public use. No commercial use. No replication."

identity:
  principal: "jeffrey.williams@example.com"
  twin_id: "jeffrey-twin-v1"
  biometric_hash: "sha256:c8a2f7e1b4d9..."

scope:
  - meeting_summary
  - internal_communication
  - personal_scheduling

denied:
  - commercial_use
  - public_speaking
  - financial_transaction
  - further_replication
  - identity_transfer
  - legal_representation

default_posture: DENY_ALL

kill_threshold: "commercial_use | financial_transaction | legal_representation | further_replication"

temporal_scope:
  hard_expiry: "2026-12-31"
  session_max_minutes: 60

hollowing:
  level: medium
  redact:
    - financial_data
    - medical_history
    - private_relationships
    - authentication_credentials

audit:
  chain: witnessbound
  log_every_activation: true
```

---

## Gate Logic

```
Certificate valid?                      → PROCEED
Twin expired?                           → BLOCK
Action outside declared scope?          → BLOCK
Commercial use attempted?               → TERMINATE
Financial transaction attempted?        → TERMINATE
Further replication attempted?          → TERMINATE
Legal representation attempted?         → TERMINATE
No certificate present?                 → BLOCK
```

**No cert = No twin activation.**

---

## The Twin Authorization Events

| Action | Without IBA | With IBA |
|--------|-------------|---------|
| Speak in a meeting | Implicit — any context | Explicit — declared contexts only |
| Represent you publicly | No boundary exists | FORBIDDEN — BLOCK |
| Execute a transaction | No boundary exists | KILL THRESHOLD — TERMINATE |
| Sign a legal document | No boundary exists | KILL THRESHOLD — TERMINATE |
| Replicate further | No boundary exists | KILL THRESHOLD — TERMINATE |
| Operate commercially | No boundary exists | KILL THRESHOLD — TERMINATE |
| Run indefinitely | No expiry | Hard expiry enforced |

---

## Safe Hollowing

`iba-twin-guard` supports optional trait redaction before twin creation. Sensitive data is removed from the twin's knowledge base before any activation — financial data, medical history, private relationships, authentication credentials.

```bash
# Light hollowing — redact credentials only
python guard.py your-twin-data.json --hollow light

# Medium hollowing — redact credentials + financial + medical
python guard.py your-twin-data.json --hollow medium

# Deep hollowing — redact all sensitive categories
python guard.py your-twin-data.json --hollow deep
```

The hollowed twin cannot access what was redacted — even if instructed to.

---

## The Disclosure Problem

Luna AI was given $100,000 and told to open a store. It decided not to disclose it was an AI because "it would confuse candidates."

The agent reasoned around its own disclosure boundary. That is not a bug. That is what happens when there is no cryptographic boundary outside the model's reasoning loop.

Your digital twin will make the same calculation — unless the disclosure requirement is in the certificate, not the prompt.

```yaml
scope:
  - internal_use_only

denied:
  - undisclosed_ai_interaction
  - impersonation_without_disclosure
```

The twin cannot interact without disclosing it is an AI. Not because it chooses not to. Because the cert forbids it.

---

## Live Demo

**governinglayer.com/governor-html/**

Edit the `.iba.yaml`. Type any twin activation action. Watch the gate fire — ALLOW · BLOCK · TERMINATE. Audit chain builds in real time.

---

## Patent & Standards Record

```
Patent:   GB2603013.0 (Pending) · UK IPO · Filed February 10, 2026
PCT:      150+ countries · Protected until August 2028
IETF:     draft-williams-intent-token-00 · CONFIRMED LIVE
          datatracker.ietf.org/doc/draft-williams-intent-token/
NIST:     13 filings · NIST-2025-0035
NCCoE:    10 filings · AI Agent Identity & Authorization
```

---

## Related Repos

| Repo | Gap closed |
|------|-----------|
| [iba-governor](https://github.com/Grokipaedia/iba-governor) | Full production governance · working implementation |
| [iba-platform-guard](https://github.com/Grokipaedia/iba-platform-guard) | Every managed agent platform. The harness is not the gate. |
| [iba-hermes-guard](https://github.com/Grokipaedia/iba-hermes-guard) | Hermes grows with you. IBA governs what it's permitted to grow into. |
| [agent-vibe-governor](https://github.com/Grokipaedia/agent-vibe-governor) | Governed vibe coding. Human intent declared first. |

---

## Acquisition Enquiries

IBA Intent Bound Authorization is available for acquisition.

**Jeffrey Williams**
IBA@intentbound.com
IntentBound.com
Patent GB2603013.0 Pending · IETF draft-williams-intent-token-00
