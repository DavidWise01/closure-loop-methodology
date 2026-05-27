#!/usr/bin/env python3
"""
hash_anchor.py — PULSE Axiom Skill v2.0
Generates SHA256 hash + JSON anchor template for any canonical string.
Works for lineage anchors AND inspection report anchors.

Usage:
  python hash_anchor.py <canonical_string> [context] [gate] [witness_type]
  python hash_anchor.py --report <report_text_file>
"""
import hashlib
import json
import sys
from datetime import datetime, timezone


def hash_anchor(canonical_string, context="", gate="", witness_type=""):
    sha = hashlib.sha256(canonical_string.encode('utf-8')).hexdigest()
    return {
        "canonical_string": canonical_string,
        "hash": f"sha256:{sha}",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "context": context,
        "gate": gate,
        "witness_type": witness_type
    }


def hash_report(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    sha = hashlib.sha256(content.encode('utf-8')).hexdigest()
    return {
        "type": "inspection_report",
        "source_file": filepath,
        "hash": f"sha256:{sha}",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "suggested_filing": f"AKASHA/INSPECTIONS/INSP-{datetime.now().strftime('%Y%m%d')}-report.json"
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python hash_anchor.py <canonical_string> [context] [gate] [witness_type]")
        print("       python hash_anchor.py --report <report_text_file>")
        sys.exit(1)

    if sys.argv[1] == "--report":
        if len(sys.argv) < 3:
            print("Error: provide report file path")
            sys.exit(1)
        result = hash_report(sys.argv[2])
    else:
        args = sys.argv[1:]
        result = hash_anchor(*args[:4])

    print(json.dumps(result, indent=2))
