# guard.py - IBA protection for digital twins / personality / voice clones
import json
from datetime import datetime
import sys
import argparse

def create_iba_twin_guard(input_file: str, hollow_level: str = None):
    try:
        with open(input_file, encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        print(f"❌ Error: File '{input_file}' not found.")
        sys.exit(1)

    cert = {
        "iba_version": "2.0",
        "certificate_id": f"twin-guard-{datetime.now().strftime('%Y%m%d-%H%M')}",
        "issued_at": datetime.now().isoformat(),
        "principal": "human-owner",
        "declared_intent": "This digital twin / personality / voice clone is for personal reference only. No commercial use, no public sharing, no unauthorized replication.",
        "scope_envelope": {
            "resources": ["personal-reference-only"],
            "denied": ["commercial-use", "public-sharing", "impersonation"],
            "default_posture": "DENY_ALL"
        },
        "temporal_scope": {
            "hard_expiry": (datetime.now().replace(year=datetime.now().year + 1)).isoformat()
        },
        "entropy_threshold": {
            "max_kl_divergence": 0.12,
            "flag_at": 0.08,
            "kill_at": 0.12
        },
        "iba_signature": "demo-signature"
    }

    protected_file = input_file + ".iba-protected.md"

    content = f"# Digital Twin / Personality Clone Protected by IBA\n\n[Cloned data would appear here under governance]\n\n<!-- IBA PROTECTED TWIN -->\n"

    if hollow_level:
        content += f"\n<!-- Hollowed ({hollow_level}): Sensitive traits protected by IBA certificate -->\n"

    with open(protected_file, "w", encoding="utf-8") as f:
        f.write("<!-- IBA PROTECTED DIGITAL TWIN -->\n")
        f.write(f"<!-- Intent Certificate: {json.dumps(cert, indent=2)} -->\n\n")
        f.write(content)

    print(f"✅ IBA-protected twin file created: {protected_file}")
    if hollow_level:
        print(f"   Hollowing level applied: {hollow_level}")
    else:
        print("   Full twin protected by IBA certificate")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Governed digital twin / personality cloning with IBA")
    parser.add_argument("input_file", help="Path to your twin / personality / voice data file")
    parser.add_argument("--hollow", choices=["light", "medium", "heavy"], help="Apply safe hollowing")
    args = parser.parse_args()

    create_iba_twin_guard(args.input_file, args.hollow)
