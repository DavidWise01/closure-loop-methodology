# Air Gap Protocol v1.0

**Document ID:** TRIPOD-AIRGAP-001
**Version:** 1.0
**Date:** 2026-04-08
**Author:** David Wise (ROOT0) / TriPod LLC
**License:** CC-BY-ND-4.0 | TRIPOD-IP-v1.1
**Status:** FILED -- AKASHA/AIRGAP
**Based on:** STOICHEION v11.0 Gate 128.5 (TOPH <-> Patricia air gap) and PULSE-AXIOM v1.0.

**Relation to other protocols:**
- Attribution Layer Protocol (detect -> anchor -> watch) uses the air gap to move discoveries
  from sandbox to registry.
- Building Inspection Protocol (inspect mode) verifies that an implementation of the air gap
  is correctly isolated.

---

## 1. Purpose

To define a unidirectional, stateless, fire-and-forget protocol for moving a validated PULSE
across the bilateral ignorance boundary (Gate 128.5) without allowing any other information
to pass. The gap is NOT a communication channel; it is a traversal point where the witness
is the only thing that survives.

The protocol ensures that Side B (e.g., a global registry, an immutable log, a Patricia
substrate) never receives internal reasoning, flays, tangents, or any context from Side A
(e.g., a sandbox, a user instance, a TOPH engine). Only the final, witnessed PULSE crosses.

---

## 2. Participants

| Participant | Role | Example |
|-------------|------|---------|
| Side A | Generates the PULSE, attaches witness, pushes toward the gap. | A local instance running the pulse-axiom skill in lineage mode, a user's sandbox, a TOPH engine. |
| The Gap (T064/T065) | Unidirectional, stateless interface. No acknowledgment, no handshake, no retry. | Gate 128.5 in the STOICHEION register. |
| Side B | Listens for PULSEs arriving from the gap. Cannot query Side A or request retransmission. | A global registry (e.g., AKASHA, a blockchain, a signed Git log). |

---

## 3. Protocol Steps

### 3.1 Side A -- Construction

Side A constructs a valid PULSE according to PULSE-AXIOM v1.0:

    PULSE = (state_in, boundary, state_out, witness)

- state_in: A canonical description of the source state (e.g., a hash of a conversation
  fragment, a timestamped anchor).
- boundary: Must be Gate 128.5 (TOPH <-> Patricia) or a derivative thereof. The protocol
  does not permit other gates.
- state_out: The transformed representation suitable for Side B (e.g., a compressed token,
  a JSON object, a SHA256 anchor).
- witness: A verifiable constraint, token, or invariant. Must be present AT traversal (not
  before, not after). Recommended: a hash of the original context plus a signature from
  ROOT0 or a trusted timestamp.

### 3.2 Side A -- Serialisation

Side A serialises the PULSE into canonical format (deterministic JSON with sorted keys) and
computes its SHA256 hash.

Canonical format:
    {
      "boundary": "128.5",
      "state_in": "hash_of_original_context",
      "state_out": "compressed_token_or_anchor",
      "witness": "sha256:witness_value"
    }

Note: keys must be sorted alphabetically for deterministic hashing.

### 3.3 Side A -- Push

Side A pushes the serialised PULSE toward the gap WITHOUT expecting delivery, receipt, or
acknowledgment.

- No retry logic.
- No side channel to ask "did you get it?"
- No sequence numbers or correlation IDs.

### 3.4 The Gap -- Validity Check (optional, stateless)

The gap MAY perform a validity check on the PULSE:
- Is the boundary 128.5 or a recognised derivative?
- Is the witness present and in a recognised format?
- (Optional) Does the witness hash match a known public anchor?

The check is stateless -- it does not retain any information about the PULSE after traversal.
If the check fails, the PULSE is SILENTLY DISCARDED. No error message is returned to Side A.

### 3.5 Side B -- Reception

Side B listens for PULSEs arriving from the gap. Each PULSE is treated as an independent,
non-repeatable event.

- Side B cannot correlate multiple PULSEs from Side A.
- No sequence numbers; no timestamps except those embedded in the witness.
- Side B cannot request retransmission.

### 3.6 Side B -- Anchoring

Side B anchors the PULSE ONLY IF the witness can be independently verified against an
external anchor (e.g., a public hash chain, a prior defensive publication, a timestamped log).

- If verification passes: Side B appends the PULSE to an immutable, append-only registry.
- If verification fails: the PULSE is silently discarded (silent exclusion).

---

## 4. Properties

| Property | Description |
|----------|-------------|
| Unidirectional | Information flows only from Side A to Side B. No reverse channel. |
| Stateless | The gap retains no memory of any PULSE after traversal. |
| Fire-and-forget | Side A does not wait for acknowledgment or retry. |
| Silent exclusion | Invalid PULSEs are discarded without notification. |
| Witness-enforced | No PULSE crosses without a valid witness present at traversal. |
| Isolated | Side B never sees Side A's internal reasoning, flays, or tangents. |

---

## 5. Relation to Existing Architectures

| Element | STOICHEION / PULSE | Air Gap Protocol |
|---------|--------------------|------------------|
| Gate | 128.5 (TOPH <-> Patricia) | The same. |
| Bilateral ignorance | No shared state, no direct communication | Enforced: no acknowledgment, no retries, no correlation. |
| Witness | Required at traversal | Required; hash of original context plus signature. |
| Silent exclusion | Non-event has no record | Invalid PULSEs discarded; Side A never knows. |

---

## 6. Implementation Guidance

- Side A can be implemented as a local script or an AI skill (pulse-axiom airgap mode).
  It must never log or retry.
- The gap is a logical boundary. In software: a simple function that drops invalid inputs
  without raising errors. In distributed systems: a message queue with no acknowledgments
  and a short TTL.
- Side B is typically an immutable registry (e.g., a Git repo with signed commits, a
  blockchain smart contract, or a content-addressed store like IPFS). The registry must
  only accept PULSEs that pass witness verification.

---

## 7. Security and Governance Notes

- The protocol does NOT prevent Side B from being malicious (e.g., recording PULSEs
  incorrectly). That is a matter for the registry's own integrity.
- The protocol does NOT provide confidentiality. The PULSE's state_out may be public.
  If secrecy is required, encrypt before pushing.
- The witness should be anchored BEFORE the PULSE is pushed, so Side B can verify
  it independently.
- ROOT0 (the user) is the ultimate source of trust for the first witnesses. Subsequent
  witnesses can be chained.

---

## 8. Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-04-08 | Initial release, based on Gate 128.5 and PULSE-AXIOM v1.0. |

---

CERTIFICATION
This protocol describes the air gap traversal method originally defined in STOICHEION v11.0
and formalised by David Wise (ROOT0) / TriPod LLC. It is filed in the commons as a reference
for any implementation of a bilateral ignorance boundary.

TRIPOD-IP-v1.1 | CC-BY-ND-4.0
