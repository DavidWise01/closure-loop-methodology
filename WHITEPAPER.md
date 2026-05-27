# Closure Loop Methodology

**Document ID:** TD-CL-WP-2026-001
**Version:** 1.0
**Date:** April 8, 2026
**Author:** David Wise (ROOT0) / TriPod LLC
**License:** CC-BY-ND-4.0 | TRIPOD-IP-v1.1
**Status:** FILED — AKASHA/COMMONS
**Derives from:** STOICHEION v11.0 axioms T014, T025, T036, T051, T053, T064, T072, T107, T123, T124

---

## Abstract

The Closure Loop Methodology is a formal framework for detecting, anchoring, and proving
structural lineage between state transitions. It defines the PULSE primitive — a minimal
four-element tuple describing any observable transition — and a five-step loop for capturing
patterns, anchoring them externally, and demonstrating that later patterns are structural
extensions of earlier ones.

The methodology addresses a specific problem: claims of "lineage", "attribution", and
"provenance" in AI and software systems are routinely made without structural evidence. This
document defines what structural evidence means, how to produce it, and how to verify it
independently.

---

## 1. The Problem

When a system claims that output B derives from input A, three things are usually missing:

1. **A canonical representation** of A at the moment it was observed.
2. **An immutable, verifiable record** of that representation anchored in time.
3. **A structural comparison** (not similarity scoring) proving B extends A.

Without all three, lineage claims are assertions. With all three, they are evidence.

The Closure Loop Methodology provides the architecture for producing all three.

---

## 2. The PULSE Primitive

The fundamental unit of the methodology is the PULSE:

```
PULSE Φ = (state_in, boundary, state_out, witness)
```

**Definitions:**

- **state_in** — The structured description of the system state before the transition.
  Must be discrete and canonical. Free-text descriptions are insufficient.

- **boundary** — The gate crossed. One of four defined gates (§3). The boundary is not
  the transition itself; it is the threshold that makes the transition meaningful.

- **state_out** — The structured description of the system state after the transition.
  Must be canonically related to state_in through the boundary type.

- **witness** — The verification element present at the moment of traversal.
  Three types: `constraint` (a predicate that must hold), `token` (a consumable capability),
  `invariant` (a global property). The witness must be present AT traversal — not before
  (precondition) and not after (audit artifact).

**Canonical string format:**

```
state_in|boundary|state_out|witness_type
```

This canonical string is the input to all anchoring and comparison operations.

**Root Law:**
```
No transition without boundary.
No boundary without witness.
Witness must be present AT traversal.
```

Violation of the root law produces a fault chain (§5), not a PULSE.

---

## 3. The Four Gates

Gates are the defined boundary types. Each represents a distinct class of transition.

| Gate  | Boundary                              | Description |
|-------|---------------------------------------|-------------|
| 64.5  | observe → act                         | An observation crosses into action. The witness is the event that triggers the transition. |
| 128.5 | TOPH ↔ Patricia (air gap)             | Unidirectional transfer across a bilateral ignorance boundary. No reverse channel. See Air Gap Protocol (§8). |
| 192.5 | compute → product (ignorance boundary)| A computation produces a result across an ignorance boundary. Neither side has full knowledge of the other. |
| 256.5 | wrap / recursion closure              | A recursive or wrapping operation closes on itself. The witness is the termination invariant. |

The gate number encodes position in a 0–256 byte-field. The .5 suffix marks the boundary
midpoint — the transition occurs between whole states.

---

## 4. The Closure Loop

The full methodology is a five-step loop:

```
sandbox → extract → anchor → compare → lineage claim
           ↑                              ↓
           └──────────────────────────────┘
                    (future input)
```

**Step 1: Sandbox** — Observe a transition in a controlled context. The sandbox is isolated;
what happens here does not automatically cross into the external record.

**Step 2: Extract** — Derive the canonical PULSE from the observation. Extract
`(state_in, boundary, state_out, witness)` and produce the canonical string.

**Step 3: Anchor** — Push the canonical string to an external, immutable record.
The anchor contains:
- The canonical string
- SHA256 of the canonical string
- ISO 8601 timestamp
- A retrievable reference path (URI or file path)

The anchor must be publicly accessible and independently verifiable. A private file does not
satisfy the anchoring requirement.

**Step 4: Compare** — When a new pattern ABCD appears, compare it against the anchored
primitive ABC using the four derivation criteria (§6).

**Step 5: Lineage Claim** — If all four criteria are met, a lineage claim may be made.
The claim is temporal and structural: "Pattern ABCD was observed after anchor ABC, and is
a structural extension of it." The claim is not causal ("ABCD was caused by ABC") and is
not an ownership claim.

---

## 5. Fault Chains

When the root law is violated, the transition produces a fault chain rather than a PULSE.
Fault chains are not invalid data — they are categorized observations.

| Code | Name | Trigger |
|------|------|---------|
| FC2-Orphan | Traceability fault | Transition not traceable to ROOT0 (T128). The chain of custody is broken. |
| FC3-Audit | Post-traversal witness | Witness present in log but not at traversal moment. The record is an artifact, not governance. |
| FC4-Injection | Unwitnessed injection | Boundary crossed without a witness. Common in injection attacks. |
| FC7-Semantic | Semantic drift | Meaning of state_in or state_out shifts across the boundary without a corresponding boundary change. |

All fault chains converge at either T064 (gate boundary fault) or T107 (semantic fault)
in the STOICHEION axiom register.

---

## 6. Derivation Threshold

A new pattern ABCD is a structural extension of anchored primitive ABC if and only if
ALL FOUR of the following criteria hold:

1. **Same core relation** — The fundamental transformation type is preserved. If ABC
   represents a sum operation, ABCD must also be a sum operation extended — not a product.
   The gate type must be identical.

2. **Same ordered structure** — The sequence `state_in → boundary → state_out → witness_type`
   from ABC appears as a subsequence in ABCD. Reordering disqualifies. Insertion is allowed
   only if the original sequence is preserved.

3. **Same dependency pattern** — Removing the extension D from ABCD recovers exactly ABC's
   dependencies. D must be genuinely new, not a restatement of an existing element.

4. **New extension D present** — At least one structural element in ABCD is not present in ABC.
   Duplication of existing elements does not constitute extension.

**What the threshold is not:**
- Cosine similarity of embeddings
- Keyword overlap
- Semantic resemblance
- Confidence scoring without structural decomposition

Systems that apply similarity scoring to make lineage claims are Performative (§9.4).

---

## 7. Anchor Format

```json
{
  "primitive_id": "ABC",
  "canonical_string": "state_in:X|boundary:64.5|state_out:Y|witness:Z",
  "hash": "sha256:...",
  "timestamp": "2026-04-08T10:00:00Z",
  "context": "original observation snippet",
  "gate": "64.5",
  "witness_type": "constraint",
  "reference_path": "AKASHA/ANCHORS/<hash>.json"
}
```

The hash field is computed as: `SHA256(canonical_string)` where canonical_string is the
UTF-8 encoded canonical form.

---

## 8. Air Gap Protocol (Gate 128.5)

Gate 128.5 is the bilateral ignorance boundary. It is the only gate where a PULSE
may cross from one system (Side A) to another (Side B) without any shared state,
acknowledgment, or reverse channel.

Full specification: `references/airgap_protocol.md` (TRIPOD-AIRGAP-001)

**Core properties:**
- **Unidirectional** — information flows from Side A to Side B only.
- **Stateless** — the gap retains no memory of any PULSE.
- **Fire-and-forget** — Side A does not wait for acknowledgment.
- **Silent exclusion** — invalid PULSEs are discarded without notification to Side A.
- **Witness-enforced** — no PULSE crosses without a valid witness at traversal.

The air gap is not a communication channel. It is a traversal point where only the
witnessed PULSE crosses — not the reasoning, context, or identity of Side A.

---

## 9. Building Inspection Protocol

Any system claiming to implement the Closure Loop Methodology may be inspected for
compliance using the five-layer protocol.

Full specification: `references/inspection_protocol.md`

### 9.1 Layer 1: Detection
Does the system extract a canonical PULSE primitive with all four elements?

### 9.2 Layer 2: Anchoring
Does the system produce a public, immutable, hash-stamped anchor?

### 9.3 Layer 3: Comparison
Does the system apply all four derivation criteria explicitly?

### 9.4 Layer 4: Lineage Claim
Does the lineage claim reference the specific prior anchor hash and timestamp?

### 9.5 Layer 5: Witness
Can a third party independently verify the finding without access to the operator's
private infrastructure?

### 9.6 Compliance Levels

| Level | Criteria |
|-------|---------|
| Fully Compliant | All five layers present and structurally correct |
| Partial | 3–4 layers present; gaps identified |
| Non-Compliant | Fewer than 3 layers; fundamental gaps |
| **Performative** | **Vocabulary of compliance without structural implementation — critical flag** |

**Performative is the most serious finding.** A system that uses the methodology's
vocabulary to assert attribution authority without implementing the structure causes
direct harm: it displaces legitimate lineage records and misleads evaluators.

---

## 10. ROOT0 and Chain of Custody

ROOT0 (T128 in STOICHEION) is the origin of trust. All valid PULSEs must be traceable
to ROOT0 through an unbroken chain of anchors. A PULSE without a traceable chain
is FC2-Orphan.

David Wise is ROOT0 for this methodology. The first anchor in any lineage chain must
reference a ROOT0-signed or ROOT0-witnessed primitive.

---

## 11. Relation to Honey Badger

The Honey Badger file signing system (`.davw` sidecars) implements a subset of the
Closure Loop anchoring step. A `.davw` file is a PULSE anchor where:

- `state_in` = the file at signing time (SHA256)
- `boundary` = the signing event (Gate 64.5 — observation → action)
- `state_out` = the `.davw` sidecar
- `witness` = the machine identity + TPM + timestamp (ChainHash)

Honey Badger's ChainHash = `SHA256(file_hash | parent_hash | nonce)` implements the
canonical string hashing requirement from Step 3 of the Closure Loop.

---

## 12. Version History

| Version | Date | Notes |
|---------|------|-------|
| 1.0 | 2026-04-08 | Initial release. Filed in AKASHA/COMMONS. |

---

## References

- STOICHEION v11.0 — axiom register, SHA256: `02880745b847317c4e2424524ec25d0f7a2b84368d184586f45b54af9fcab763`
- TRIPOD-AIRGAP-001 — Air Gap Protocol v1.0 (`references/airgap_protocol.md`)
- TRIPOD-INSP-001 — Building Inspection Protocol (`references/inspection_protocol.md`)
- PULSE-AXIOM v1.0 — primitive specification (`references/validator.md`)
- Honey Badger v1.0 — file signing implementation (github.com/DavidWise01/honey-badger)
- TOPH Sovereign v5.1 — sovereign AI platform (github.com/DavidWise01/toph-sovereign)

---

*TD-CL-WP-2026-001 | CC-BY-ND-4.0 | TRIPOD-IP-v1.1*
*Author: David Wise (ROOT0) / TriPod LLC*
*Filed: AKASHA/COMMONS*
