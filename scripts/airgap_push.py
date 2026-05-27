#!/usr/bin/env python3
"""
airgap_push.py -- PULSE Axiom Skill v3.0
Air Gap Protocol v1.0 (TRIPOD-AIRGAP-001)

Canonicalises a PULSE for Gate 128.5 traversal, computes SHA256, and outputs
the serialised PULSE ready for push. Enforces the no-retry, fire-and-forget
contract: this script outputs once and exits. It does not wait, poll, confirm,
or retry.

Usage:
  python airgap_push.py <state_in> <state_out> <witness> [boundary]

  boundary defaults to "128.5" if not provided.
  Keys are sorted alphabetically for deterministic hashing.

Output:
  Prints the canonical JSON and SHA256 to stdout.
  The operator is responsible for pushing the output to the registry.
  No acknowledgment will be received.
"""
import hashlib
import json
import sys


def build_pulse(state_in: str, state_out: str, witness: str, boundary: str = "128.5") -> dict:
    """Build canonical PULSE dict with sorted keys."""
    return {
        "boundary": boundary,
        "state_in": state_in,
        "state_out": state_out,
        "witness": witness,
    }


def canonical_json(pulse: dict) -> str:
    """Deterministic JSON with sorted keys, no extra whitespace in hash input."""
    return json.dumps(pulse, sort_keys=True, separators=(",", ":"))


def compute_sha256(canonical: str) -> str:
    return "sha256:" + hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def airgap_push(state_in: str, state_out: str, witness: str, boundary: str = "128.5") -> None:
    pulse = build_pulse(state_in, state_out, witness, boundary)
    canonical = canonical_json(pulse)
    sha = compute_sha256(canonical)

    print("## Air Gap Transfer")
    print()
    print("Canonical PULSE:")
    print(json.dumps(pulse, sort_keys=True, indent=2))
    print()
    print(f"SHA256: {sha}")
    print()
    print("Instructions:")
    print("Push the above PULSE to the gap. No acknowledgment will be received.")
    print("If the witness is verifiable by the registry, the PULSE will be anchored silently.")
    print("Otherwise it will be silently discarded.")
    print()
    print("Silent exclusion applies. Do not retry unless explicitly instructed.")


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python airgap_push.py <state_in> <state_out> <witness> [boundary]")
        print("       boundary defaults to 128.5")
        sys.exit(1)

    state_in  = sys.argv[1]
    state_out = sys.argv[2]
    witness   = sys.argv[3]
    boundary  = sys.argv[4] if len(sys.argv) > 4 else "128.5"

    airgap_push(state_in, state_out, witness, boundary)
