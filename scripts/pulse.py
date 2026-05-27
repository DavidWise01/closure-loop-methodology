#!/usr/bin/env python3
"""
pulse.py — Closure Loop Methodology CLI
TD-CL-WP-2026-001 | TriPod LLC | David Wise (ROOT0)

Unified command-line tool for all four PULSE operations.

Commands:
  validate  <state_in> <boundary> <state_out> <witness> [--witness-type TYPE]
            Validate a PULSE against the root law and gate definitions.

  anchor    <canonical_string> [--context TEXT] [--gate GATE] [--witness-type TYPE]
            Hash a canonical string and produce a JSON anchor record.

  push      <state_in> <state_out> <witness> [--boundary GATE]
            Serialise a PULSE for air gap transfer (Gate 128.5).
            Fire-and-forget. No retry. No acknowledgment.

  inspect   <description>
            Run a building inspection checklist against a system description.

  hash      <file>
            Hash a file or report for anchoring (SHA256).

  chain     <anchor_file> <new_canonical>
            Compare a new canonical string against an existing anchor.
            Returns LINEAGE CONFIRMED or NOT LINEAGE.

Usage:
  python pulse.py validate "form_dirty=true" "64.5" "form_submitted=true" "click_timestamp"
  python pulse.py anchor "form_dirty=true|64.5|form_submitted=true|constraint" --gate 64.5
  python pulse.py push "sha256:abc" "token:xyz" "sha256:witness" --boundary 128.5
  python pulse.py hash report.md
  python pulse.py chain anchor.json "form_dirty=true|64.5|form_submitted=true|constraint|webhook_receipt"
"""

import hashlib
import json
import sys
import os
import argparse
from datetime import datetime, timezone

# ── Gate definitions ──────────────────────────────────────────────────────────
GATES = {
    "64.5":  "observe → act",
    "128.5": "TOPH ↔ Patricia (air gap / bilateral ignorance boundary)",
    "192.5": "compute → product (ignorance boundary)",
    "256.5": "wrap / recursion closure",
}

WITNESS_TYPES = {"constraint", "token", "invariant"}

FAULT_CHAINS = {
    "FC2-Orphan":   "Not traceable to ROOT0 (T128). Chain of custody broken.",
    "FC3-Audit":    "Witness present in log but not AT traversal moment.",
    "FC4-Injection":"Boundary crossed without a witness.",
    "FC7-Semantic": "Semantic drift across the boundary without a corresponding boundary change.",
}

ROOT0 = "David Wise"
METHODOLOGY_REF = "TD-CL-WP-2026-001"


# ── Helpers ───────────────────────────────────────────────────────────────────
def sha256(text: str) -> str:
    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_file(filepath: str) -> str:
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return "sha256:" + h.hexdigest()


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def print_section(title: str):
    print(f"\n{'─' * 50}")
    print(f"  {title}")
    print(f"{'─' * 50}")


# ── validate ──────────────────────────────────────────────────────────────────
def cmd_validate(args):
    state_in    = args.state_in
    boundary    = args.boundary
    state_out   = args.state_out
    witness     = args.witness
    witness_type = args.witness_type or "constraint"

    print_section("PULSE VALIDATION")

    # 1. Gate check
    gate_valid = boundary in GATES
    gate_desc  = GATES.get(boundary, "UNKNOWN — not a defined gate")
    print(f"\n  state_in:     {state_in}")
    print(f"  boundary:     {boundary} — {gate_desc}")
    print(f"  state_out:    {state_out}")
    print(f"  witness:      {witness} [{witness_type}]")

    faults = []

    if not gate_valid:
        faults.append(("FC4-Injection", f"Boundary '{boundary}' is not a defined gate (64.5 / 128.5 / 192.5 / 256.5)"))

    if witness_type not in WITNESS_TYPES:
        print(f"\n  WARNING: witness_type '{witness_type}' not in {{constraint, token, invariant}}. Defaulting to 'constraint'.")
        witness_type = "constraint"

    # 2. Canonical string
    canonical = f"{state_in}|{boundary}|{state_out}|{witness_type}"
    h = sha256(canonical)

    print(f"\n  canonical:    {canonical}")
    print(f"  SHA256:       {h}")

    # 3. Verdict
    print(f"\n  {'─' * 40}")
    if not faults:
        print(f"\n  VERDICT: ✓ VALID PULSE")
        print(f"  Gate {boundary} ({gate_desc})")
        print(f"  Witness type: {witness_type}")
        print(f"  Root law: SATISFIED")
        print(f"  Traceability: anchored to ROOT0 via canonical hash")
    else:
        for code, reason in faults:
            print(f"\n  FAULT: {code}")
            print(f"  Reason: {reason}")
        print(f"\n  VERDICT: ✗ NOT A VALID PULSE — fault chain raised")

    print()


# ── anchor ────────────────────────────────────────────────────────────────────
def cmd_anchor(args):
    canonical    = args.canonical_string
    context      = args.context or ""
    gate         = args.gate or ""
    witness_type = args.witness_type or ""

    h = sha256(canonical)
    ts = now_iso()

    anchor = {
        "primitive_id":    "ABC",
        "canonical_string": canonical,
        "hash":            h,
        "timestamp":       ts,
        "context":         context,
        "gate":            gate,
        "witness_type":    witness_type,
        "reference_path":  f"AKASHA/ANCHORS/{h.split(':')[1][:16]}.json",
        "methodology":     METHODOLOGY_REF,
        "root0":           ROOT0,
    }

    print_section("ANCHOR RECORD")
    print()
    print(json.dumps(anchor, indent=2))
    print()
    print(f"  File this at: {anchor['reference_path']}")
    print(f"  Push to a public repo to satisfy Layer 2 (Anchoring) compliance.")
    print()


# ── push (airgap) ─────────────────────────────────────────────────────────────
def cmd_push(args):
    state_in  = args.state_in
    state_out = args.state_out
    witness   = args.witness
    boundary  = args.boundary or "128.5"

    if boundary not in GATES:
        print(f"\n  ERROR: Boundary '{boundary}' is not a defined gate.")
        sys.exit(1)

    if boundary != "128.5":
        print(f"\n  WARNING: Air Gap Protocol requires boundary 128.5.")
        print(f"  Gate {boundary} is a local transition gate, not the bilateral ignorance boundary.")
        print(f"  Silent exclusion would apply at Gate 128.5.")
        sys.exit(1)

    # Canonical JSON — sorted keys, no extra whitespace
    pulse = {
        "boundary": boundary,
        "state_in": state_in,
        "state_out": state_out,
        "witness": witness,
    }
    canonical = json.dumps(pulse, sort_keys=True, separators=(",", ":"))
    h = sha256(canonical)

    print_section("AIR GAP TRANSFER")
    print()
    print("  Canonical PULSE:")
    print(json.dumps(pulse, sort_keys=True, indent=4))
    print()
    print(f"  SHA256: {h}")
    print()
    print("  Instructions:")
    print("  Push the above PULSE to the gap. No acknowledgment will be received.")
    print("  If the witness is verifiable by the registry, the PULSE will be anchored silently.")
    print("  Otherwise it will be silently discarded.")
    print()
    print("  Silent exclusion applies. Do not retry unless explicitly instructed.")
    print()
    print(f"  Protocol: TRIPOD-AIRGAP-001 | Gate 128.5")
    print()


# ── inspect ───────────────────────────────────────────────────────────────────
def cmd_inspect(args):
    description = args.description

    print_section("BUILDING INSPECTION CHECKLIST")
    print(f"\n  Target: {description[:80]}{'...' if len(description) > 80 else ''}")
    print(f"  Method: Closure Loop Methodology ({METHODOLOGY_REF})")
    print(f"  Date:   {now_iso()[:10]}")
    print()

    layers = [
        ("Detection",
         "Does the system extract (state_in, boundary, state_out, witness)?",
         "Can you produce: state_in|boundary|state_out|witness from its output?"),
        ("Anchoring",
         "Does it produce a public SHA256-timestamped immutable record?",
         "Can an independent party retrieve and verify the anchor?"),
        ("Comparison",
         "Does it apply all four derivation criteria structurally?",
         "Is comparison structural decomposition — NOT similarity/embedding?"),
        ("Lineage Claim",
         "Does the lineage claim reference a specific prior anchor hash?",
         "Is the claim temporal/structural, not causal or ownership?"),
        ("Witness",
         "Are findings independently verifiable by a third party?",
         "Are all records publicly accessible without trusting the operator?"),
    ]

    print("  ┌─────────────────────────────────────────────────────────────────┐")
    print("  │  Five-Layer Inspection                                          │")
    print("  └─────────────────────────────────────────────────────────────────┘")
    print()
    for i, (name, question, test) in enumerate(layers, 1):
        print(f"  Layer {i}: {name}")
        print(f"    Q: {question}")
        print(f"    T: {test}")
        print(f"    → [ ] Fully Compliant  [ ] Partial  [ ] Non-Compliant  [ ] Performative")
        print()

    print("  ┌─────────────────────────────────────────────────────────────────┐")
    print("  │  Performative Markers (flag ANY of these)                       │")
    print("  └─────────────────────────────────────────────────────────────────┘")
    markers = [
        "Uses 'lineage'/'attribution'/'provenance' without producing hash records",
        "Claims comparison without applying all four threshold criteria",
        "Asserts causation ('derived from') instead of temporal/structural relation",
        "Requires trust in the operator for verification rather than open records",
        "Produces confidence scores without structural decomposition",
        "Claims ownership of primitives rather than temporal precedence",
        "Uses embedding similarity as a proxy for structural extension",
    ]
    for m in markers:
        print(f"    [ ] {m}")
    print()
    print(f"  Report this inspection using: python pulse.py hash <report_file>")
    print(f"  File at: AKASHA/INSPECTIONS/INSP-{now_iso()[:10]}-<target>.json")
    print()


# ── hash ──────────────────────────────────────────────────────────────────────
def cmd_hash(args):
    filepath = args.file
    if not os.path.exists(filepath):
        print(f"\n  ERROR: File not found: {filepath}")
        sys.exit(1)

    h  = sha256_file(filepath)
    ts = now_iso()

    result = {
        "type":            "file_anchor",
        "source_file":     filepath,
        "hash":            h,
        "timestamp":       ts,
        "methodology":     METHODOLOGY_REF,
        "suggested_filing": f"AKASHA/ANCHORS/{h.split(':')[1][:16]}.json",
    }

    print_section("FILE HASH / ANCHOR")
    print()
    print(json.dumps(result, indent=2))
    print()


# ── chain (compare against anchor) ───────────────────────────────────────────
def cmd_chain(args):
    anchor_file   = args.anchor_file
    new_canonical = args.new_canonical

    if not os.path.exists(anchor_file):
        print(f"\n  ERROR: Anchor file not found: {anchor_file}")
        sys.exit(1)

    with open(anchor_file, "r", encoding="utf-8") as f:
        anchor = json.load(f)

    original = anchor.get("canonical_string", "")
    orig_parts = original.split("|")
    new_parts  = new_canonical.split("|")

    print_section("LINEAGE COMPARISON")
    print(f"\n  Anchor:       {original}")
    print(f"  Anchor hash:  {anchor.get('hash','?')}")
    print(f"  Anchor time:  {anchor.get('timestamp','?')}")
    print(f"\n  New pattern:  {new_canonical}")
    print()

    # Apply four criteria
    # 1. Same gate (first boundary field)
    orig_gate = anchor.get("gate", orig_parts[1] if len(orig_parts) > 1 else "")
    new_gate  = new_parts[1] if len(new_parts) > 1 else ""
    c1 = orig_gate == new_gate

    # 2. Same ordered structure (original is subsequence of new)
    def is_subsequence(sub, sup):
        it = iter(sup)
        return all(p in it for p in sub)
    c2 = is_subsequence(orig_parts, new_parts)

    # 3. New pattern has more elements (D present)
    c3 = len(new_parts) > len(orig_parts)

    # 4. Removing the extension recovers original dependencies
    # Simplified: new_parts starts with orig_parts as prefix
    c4 = new_parts[:len(orig_parts)] == orig_parts if len(new_parts) >= len(orig_parts) else False

    criteria = [
        ("Same core relation (gate preserved)", c1),
        ("Same ordered structure (ABC subsequence of ABCD)", c2),
        ("Extension D present (new elements in ABCD)", c3),
        ("Removing D recovers ABC's dependencies", c4),
    ]

    all_pass = all(v for _, v in criteria)

    print("  Derivation threshold (all four required):")
    for name, result in criteria:
        icon = "✓" if result else "✗"
        print(f"    {icon}  {name}")

    print()
    if all_pass:
        ext = [p for p in new_parts if p not in orig_parts]
        print(f"  VERDICT: LINEAGE CONFIRMED")
        print(f"  Extension D: {', '.join(ext) or '(implicit)'}")
        print(f"  Claim: Pattern observed after anchor {anchor.get('hash','?')[:30]}..., structural extension confirmed.")
    else:
        failed = [name for name, v in criteria if not v]
        print(f"  VERDICT: NOT LINEAGE")
        print(f"  Failed criteria: {'; '.join(failed)}")

    print()


# ── Entry point ───────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        prog="pulse",
        description=f"Closure Loop Methodology CLI — {METHODOLOGY_REF}",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # validate
    p = sub.add_parser("validate", help="Validate a PULSE against the root law")
    p.add_argument("state_in");  p.add_argument("boundary")
    p.add_argument("state_out"); p.add_argument("witness")
    p.add_argument("--witness-type", default="constraint")

    # anchor
    p = sub.add_parser("anchor", help="Hash and produce a JSON anchor record")
    p.add_argument("canonical_string")
    p.add_argument("--context", default=""); p.add_argument("--gate", default="")
    p.add_argument("--witness-type", default="")

    # push
    p = sub.add_parser("push", help="Serialise a PULSE for air gap transfer (Gate 128.5)")
    p.add_argument("state_in"); p.add_argument("state_out"); p.add_argument("witness")
    p.add_argument("--boundary", default="128.5")

    # inspect
    p = sub.add_parser("inspect", help="Run a building inspection checklist")
    p.add_argument("description")

    # hash
    p = sub.add_parser("hash", help="SHA256 a file for anchoring")
    p.add_argument("file")

    # chain
    p = sub.add_parser("chain", help="Compare a new pattern against an existing anchor")
    p.add_argument("anchor_file"); p.add_argument("new_canonical")

    args = parser.parse_args()

    dispatch = {
        "validate": cmd_validate,
        "anchor":   cmd_anchor,
        "push":     cmd_push,
        "inspect":  cmd_inspect,
        "hash":     cmd_hash,
        "chain":    cmd_chain,
    }
    dispatch[args.command](args)


if __name__ == "__main__":
    main()
