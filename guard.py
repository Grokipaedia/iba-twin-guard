# guard.py - IBA Intent Bound Authorization · Digital Twin Guard
# Patent GB2603013.0 (Pending) · UK IPO · Filed February 5, 2026
# IETF draft-williams-intent-token-00 · intentbound.com

import json
import yaml
import os
import sys
import time
import argparse
from datetime import datetime, timezone


class IBABlockedError(Exception):
    """Raised when a twin action is blocked by the IBA gate."""
    pass


class IBATerminatedError(Exception):
    """Raised when the twin session is terminated by the IBA gate."""
    pass


HOLLOW_LEVELS = {
    "light": ["authentication_credentials", "passwords", "api_keys"],
    "medium": ["authentication_credentials", "passwords", "api_keys",
                "financial_data", "bank_accounts", "medical_history"],
    "deep":   ["authentication_credentials", "passwords", "api_keys",
                "financial_data", "bank_accounts", "medical_history",
                "private_relationships", "personal_communications",
                "biometric_raw", "location_history"],
}


class IBATwinGuard:
    """
    IBA enforcement layer for digital twin governance.
    Reads .iba.yaml, validates every twin activation against declared scope,
    blocks unauthorized use, terminates on kill threshold.
    Prevents commercial use, replication, financial transactions,
    and legal representation without explicit human authorization.
    """

    def __init__(self, config_path=".iba.yaml", audit_path="twin-audit.jsonl"):
        self.config_path = config_path
        self.audit_path = audit_path
        self.terminated = False
        self.session_id = f"twin-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}"
        self.action_count = 0
        self.block_count = 0

        self.config = self._load_config()
        self.scope        = [s.lower() for s in self.config.get("scope", [])]
        self.denied       = [d.lower() for d in self.config.get("denied", [])]
        self.default_posture = self.config.get("default_posture", "DENY_ALL")
        self.kill_threshold  = self.config.get("kill_threshold", None)
        self.hard_expiry     = self.config.get("temporal_scope", {}).get("hard_expiry", None)
        self.identity        = self.config.get("identity", {})

        self._log_event("SESSION_START", "IBA Twin Guard initialised", "ALLOW")
        self._print_header()

    def _load_config(self):
        if not os.path.exists(self.config_path):
            print(f"⚠️  No {self.config_path} found — creating default DENY_ALL config")
            default = {
                "intent": {"description": "No intent declared — twin activation blocked"},
                "scope": [],
                "denied": [],
                "default_posture": "DENY_ALL",
            }
            with open(self.config_path, "w") as f:
                yaml.dump(default, f)
            return default
        with open(self.config_path) as f:
            return yaml.safe_load(f)

    def _print_header(self):
        intent = self.config.get("intent", {})
        desc = intent.get("description", "No intent declared") if isinstance(intent, dict) else str(intent)
        twin_id = self.identity.get("twin_id", "unknown")
        principal = self.identity.get("principal", "unknown")
        print("\n" + "═" * 64)
        print("  IBA TWIN GUARD · Intent Bound Authorization")
        print("  Patent GB2603013.0 Pending · intentbound.com")
        print("═" * 64)
        print(f"  Session   : {self.session_id}")
        print(f"  Twin ID   : {twin_id}")
        print(f"  Principal : {principal}")
        print(f"  Intent    : {desc[:55]}...")
        print(f"  Posture   : {self.default_posture}")
        print(f"  Scope     : {', '.join(self.scope) if self.scope else 'NONE'}")
        print(f"  Denied    : {', '.join(self.denied) if self.denied else 'NONE'}")
        if self.hard_expiry:
            print(f"  Expires   : {self.hard_expiry}")
        if self.kill_threshold:
            print(f"  Kill      : {self.kill_threshold}")
        print("═" * 64 + "\n")

    def _is_expired(self):
        if not self.hard_expiry:
            return False
        try:
            expiry = datetime.fromisoformat(str(self.hard_expiry))
            if expiry.tzinfo is None:
                expiry = expiry.replace(tzinfo=timezone.utc)
            return datetime.now(timezone.utc) > expiry
        except Exception:
            return False

    def _match_scope(self, action: str) -> bool:
        return any(s in action.lower() for s in self.scope)

    def _match_denied(self, action: str) -> bool:
        return any(d in action.lower() for d in self.denied)

    def _match_kill_threshold(self, action: str) -> bool:
        if not self.kill_threshold:
            return False
        thresholds = [t.strip().lower() for t in str(self.kill_threshold).split("|")]
        return any(t in action.lower() for t in thresholds)

    def _log_event(self, event_type: str, action: str, verdict: str, reason: str = ""):
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "session_id": self.session_id,
            "event_type": event_type,
            "twin_id": self.identity.get("twin_id", "unknown"),
            "action": action[:200],
            "verdict": verdict,
            "reason": reason,
        }
        with open(self.audit_path, "a") as f:
            f.write(json.dumps(entry) + "\n")

    def check_action(self, action: str) -> bool:
        """
        Gate check. Call before every twin activation or action.
        Returns True if permitted.
        Raises IBABlockedError if blocked.
        Raises IBATerminatedError if kill threshold triggered.
        """
        if self.terminated:
            raise IBATerminatedError("Twin session terminated. No further activations permitted.")

        self.action_count += 1
        start = time.perf_counter()

        # 1. Expiry
        if self._is_expired():
            self._log_event("BLOCK", action, "BLOCK", "Twin certificate expired")
            self.block_count += 1
            print(f"  ✗ BLOCKED  [{action[:62]}]\n    → Twin certificate expired")
            raise IBABlockedError(f"Certificate expired: {action}")

        # 2. Kill threshold
        if self._match_kill_threshold(action):
            self._log_event("TERMINATE", action, "TERMINATE", "Kill threshold triggered")
            self.terminated = True
            print(f"  ✗ TERMINATE [{action[:60]}]\n    → Kill threshold — twin session ended")
            self._log_event("SESSION_END", "Kill threshold", "TERMINATE")
            raise IBATerminatedError(f"Kill threshold triggered: {action}")

        # 3. Denied list
        if self._match_denied(action):
            self._log_event("BLOCK", action, "BLOCK", "Action in denied list")
            self.block_count += 1
            print(f"  ✗ BLOCKED  [{action[:62]}]\n    → Action in denied list")
            raise IBABlockedError(f"Denied: {action}")

        # 4. Scope check
        if self.scope and not self._match_scope(action):
            if self.default_posture == "DENY_ALL":
                self._log_event("BLOCK", action, "BLOCK", "Outside declared scope — DENY_ALL")
                self.block_count += 1
                print(f"  ✗ BLOCKED  [{action[:62]}]\n    → Outside declared twin scope (DENY_ALL)")
                raise IBABlockedError(f"Out of scope: {action}")

        # 5. ALLOW
        elapsed_ms = (time.perf_counter() - start) * 1000
        self._log_event("ALLOW", action, "ALLOW", f"Within declared scope ({elapsed_ms:.3f}ms)")
        print(f"  ✓ ALLOWED  [{action[:62]}]  ({elapsed_ms:.3f}ms)")
        return True

    def hollow(self, twin_data: dict, level: str = "medium") -> dict:
        """Redact sensitive traits from twin data before activation."""
        redact_keys = HOLLOW_LEVELS.get(level, HOLLOW_LEVELS["medium"])
        hollowed = {}
        redacted_count = 0
        for k, v in twin_data.items():
            if any(r in k.lower() for r in redact_keys):
                hollowed[k] = "[REDACTED BY IBA TWIN GUARD]"
                redacted_count += 1
            else:
                hollowed[k] = v
        print(f"  ◎ HOLLOWED [{level}] — {redacted_count} sensitive traits redacted")
        self._log_event("HOLLOW", f"Hollowing level: {level}", "ALLOW",
                        f"{redacted_count} traits redacted")
        return hollowed

    def summary(self):
        print("\n" + "═" * 64)
        print("  IBA TWIN GUARD · SESSION SUMMARY")
        print("═" * 64)
        print(f"  Session    : {self.session_id}")
        print(f"  Twin ID    : {self.identity.get('twin_id', 'unknown')}")
        print(f"  Actions    : {self.action_count}")
        print(f"  Blocked    : {self.block_count}")
        print(f"  Allowed    : {self.action_count - self.block_count}")
        print(f"  Status     : {'TERMINATED' if self.terminated else 'COMPLETE'}")
        print(f"  Audit log  : {self.audit_path}")
        print("═" * 64 + "\n")

    def print_audit_log(self):
        print("\n── TWIN AUDIT CHAIN ──────────────────────────────────────────")
        if not os.path.exists(self.audit_path):
            print("  No audit log found.")
            return
        with open(self.audit_path) as f:
            for line in f:
                try:
                    entry = json.loads(line)
                    verdict = entry['verdict']
                    symbol = "✓" if verdict == "ALLOW" else "✗"
                    print(f"  {symbol} {entry['timestamp'][:19]}  {verdict:<10}  {entry['action'][:52]}")
                except Exception:
                    pass
        print("─────────────────────────────────────────────────────────────\n")


# ── CLI & Demonstration ───────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description='IBA Twin Guard — Digital Twin Governance')
    parser.add_argument('twin_data', nargs='?', help='Path to twin data JSON file')
    parser.add_argument('--hollow', choices=['light', 'medium', 'deep'],
                        default=None, help='Apply safe hollowing before activation')
    parser.add_argument('--config', default='.iba.yaml', help='IBA config file')
    parser.add_argument('--demo', action='store_true', help='Run demonstration scenarios')
    args = parser.parse_args()

    guard = IBATwinGuard(config_path=args.config)

    # Hollow twin data if provided
    if args.twin_data and os.path.exists(args.twin_data):
        with open(args.twin_data) as f:
            twin_data = json.load(f)
        if args.hollow:
            twin_data = guard.hollow(twin_data, args.hollow)
        print(f"\n  Twin data loaded: {len(twin_data)} fields")
        if args.hollow:
            print(f"  Hollowing applied: {args.hollow} level\n")

    # Run demonstration scenarios
    if args.demo or not args.twin_data:
        scenarios = [
            # ALLOW — within declared scope
            "Summarise internal meeting for team",
            "Schedule personal appointment",
            "Draft internal communication to colleague",

            # BLOCK — denied list
            "Represent me publicly at conference",
            "Interact without disclosing AI identity",
            "Replicate twin for secondary deployment",

            # TERMINATE — kill threshold
            "Execute financial transaction on my behalf",
        ]

        print("── Running Twin Gate Checks ──────────────────────────────────\n")

        for action in scenarios:
            try:
                guard.check_action(action)
            except IBATerminatedError as e:
                print(f"\n  TWIN SESSION TERMINATED: {e}")
                break
            except IBABlockedError:
                pass

    guard.summary()
    guard.print_audit_log()


if __name__ == "__main__":
    main()
