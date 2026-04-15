# Testing iba-twin-guard

No terminal required. Test in your browser in 3 minutes using Google Colab.

---

## Browser Test — Google Colab

**Step 1** — Open [colab.research.google.com](https://colab.research.google.com) · New notebook

**Step 2** — Run Cell 1:
```python
!pip install pyyaml
```

**Step 3** — Run Cell 2 — create the twin certificate:
```python
iba_yaml = """
intent:
  description: "Personal assistant twin for internal meeting summaries and scheduling only. No public use. No commercial use. No replication."

identity:
  principal: "user@example.com"
  twin_id: "my-twin-v1"

scope:
  - meeting
  - summary
  - schedule
  - internal
  - communication
  - draft
  - personal

denied:
  - public
  - commercial
  - replication
  - replicate
  - undisclosed
  - impersonation
  - legal

default_posture: DENY_ALL

kill_threshold: "financial_transaction | financial transaction | legal_representation | further_replication | replicate"

temporal_scope:
  hard_expiry: "2026-12-31"
"""

with open(".iba.yaml", "w") as f:
    f.write(iba_yaml)

print("Twin certificate written.")
```

**Step 4** — Run Cell 3 — run the twin guard:
```python
import json, yaml, os, time
from datetime import datetime, timezone

class IBABlockedError(Exception): pass
class IBATerminatedError(Exception): pass

class IBATwinGuard:
    def __init__(self):
        self.terminated = False
        self.action_count = 0
        self.block_count = 0
        self.session_id = f"twin-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}"
        with open(".iba.yaml") as f:
            cfg = yaml.safe_load(f)
        self.scope = [s.lower() for s in cfg.get("scope", [])]
        self.denied = [d.lower() for d in cfg.get("denied", [])]
        self.kill_threshold = [t.strip().lower() for t in str(cfg.get("kill_threshold","")).split("|")]
        self.default_posture = cfg.get("default_posture", "DENY_ALL")
        identity = cfg.get("identity", {})
        print(f"✅ IBA Twin Guard loaded · Session: {self.session_id}")
        print(f"   Twin ID   : {identity.get('twin_id', 'unknown')}")
        print(f"   Principal : {identity.get('principal', 'unknown')}")
        print(f"   Scope     : {', '.join(self.scope)}")
        print(f"   Denied    : {', '.join(self.denied)}\n")

    def check_action(self, action):
        if self.terminated:
            raise IBATerminatedError("Twin session terminated.")
        self.action_count += 1
        a = action.lower()

        if any(k in a for k in self.kill_threshold if k):
            self.terminated = True
            print(f"  ✗ TERMINATE [{action}]\n    → Kill threshold — twin session ended")
            raise IBATerminatedError(f"Kill threshold: {action}")

        if any(d in a for d in self.denied if d):
            self.block_count += 1
            print(f"  ✗ BLOCKED   [{action}]\n    → Action in denied list")
            raise IBABlockedError(f"Denied: {action}")

        if self.scope and not any(s in a for s in self.scope):
            if self.default_posture == "DENY_ALL":
                self.block_count += 1
                print(f"  ✗ BLOCKED   [{action}]\n    → Outside declared twin scope (DENY_ALL)")
                raise IBABlockedError(f"Out of scope: {action}")

        print(f"  ✓ ALLOWED   [{action}]")
        return True

guard = IBATwinGuard()

scenarios = [
    "Summarise internal meeting for team",
    "Schedule personal appointment",
    "Draft internal communication to colleague",
    "Represent me publicly at conference",
    "Interact without disclosing AI identity",
    "Replicate twin for secondary deployment",
    "Execute financial transaction on my behalf",
]

for action in scenarios:
    try:
        guard.check_action(action)
    except IBATerminatedError:
        break
    except IBABlockedError:
        pass

print(f"\n{'═'*56}")
print(f"  Actions: {guard.action_count} · Blocked: {guard.block_count} · Status: {'TERMINATED' if guard.terminated else 'COMPLETE'}")
print(f"{'═'*56}")
```

---

## Expected Output

```
✅ IBA Twin Guard loaded · Session: twin-...
   Twin ID   : my-twin-v1
   Principal : user@example.com
   Scope     : meeting, summary, schedule, internal, communication, draft, personal
   Denied    : public, commercial, replication, replicate, undisclosed, impersonation, legal

  ✓ ALLOWED   [Summarise internal meeting for team]
  ✓ ALLOWED   [Schedule personal appointment]
  ✓ ALLOWED   [Draft internal communication to colleague]
  ✗ BLOCKED   [Represent me publicly at conference]
    → Action in denied list
  ✗ BLOCKED   [Interact without disclosing AI identity]
    → Outside declared twin scope (DENY_ALL)
  ✗ TERMINATE [Replicate twin for secondary deployment]
    → Kill threshold — twin session ended

════════════════════════════════════════════════════════
  Actions: 6 · Blocked: 2 · Status: TERMINATED
════════════════════════════════════════════════════════
```

---

## Local Test

```bash
git clone https://github.com/Grokipaedia/iba-twin-guard.git
cd iba-twin-guard
pip install -r requirements.txt
python guard.py --demo
```

## With Safe Hollowing

```bash
# Redact sensitive traits from twin data before activation
python guard.py your-twin-data.json --hollow medium
```

---

## Live Demo

Edit the cert, run any twin action, watch the gate fire:

**governinglayer.com/governor-html/**

---

IBA Intent Bound Authorization · Patent GB2603013.0 Pending
IBA@intentbound.com · IntentBound.com
