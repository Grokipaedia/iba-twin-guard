# iba-twin-guard

**Govern your digital twin. Human intent required.**

As AI clones personalities, voices, faces, and entire digital twins from seconds of data, the risk of uncontrolled identity replication has never been higher.

This tool adds real cryptographic governance.

Wrap any digital twin, personality file, voice sample, or knowledge dump with a signed **IBA Intent Certificate** so the clone can only be used under your exact approved rules.

## Patent & Filings
- **Patent Pending**: GB2603013.0 (filed 5 Feb 2026, PCT route open — 150+ countries)
- **NIST Docket**: NIST-2025-0035 (13 IBA filings)
- **NCCoE Filings**: 10 submissions on AI agent authorization

## Features
- Requires IBA-signed intent before any twin creation or use
- Enforces scope (personal use only, no commercial replication, no public sharing)
- Optional safe hollowing / redaction of sensitive traits
- Works with any digital twin, voice cloning, or personality cloning pipeline

## Quick Start
```bash
git clone https://github.com/Grokipaedia/iba-twin-guard.git
cd iba-twin-guard
pip install -r requirements.txt
python guard.py your-twin-data.json --hollow medium
