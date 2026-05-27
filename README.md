# Closure Loop Methodology

**Document ID:** TD-CL-WP-2026-001  
**Author:** David Wise (ROOT0) / TriPod LLC  
**License:** CC-BY-ND-4.0 | TRIPOD-IP-v1.1  
**Status:** FILED — AKASHA/COMMONS  

---

## What this is

A formal framework for detecting, anchoring, and proving structural lineage between state transitions.

The core problem: claims of "lineage," "attribution," and "provenance" in AI and software systems are routinely made without structural evidence. This methodology defines what structural evidence means, how to produce it, and how to verify it independently.

No embeddings. No confidence scores. No trust-the-operator. Structural decomposition only.

---

## The PULSE Primitive

Every transition is represented as:

```
PULSE Φ = (state_in, boundary, state_out, witness)
```

**Canonical string format:**
```
state_in|boundary|state_out|witness_type
```

**Root Law:**
```
No transition without boundary.
No boundary without witness.
Witness must be present AT traversal.
```

---

## The Four Gates

| Gate  | Boundary | Description |
|-------|----------|-------------|
| 64.5  | observe → act | An observation crosses into action. |
| 128.5 | TOPH ↔ Patricia (air gap) | Unidirectional transfer across bilateral ignorance boundary. |
| 192.5 | compute → product | Computation produces a result across an ignorance boundary. |
| 256.5 | wrap / recursion closure | A recursive operation closes on itself. |

---

## The Closure Loop

```
sandbox → extract → anchor → compare → lineage claim
           ↑                              ↓
           └──────────────────────────────┘
                    (future input)
```

1. **Sandbox** — Observe a transition in a controlled context.
2. **Extract** — Derive the canonical PULSE `(state_in, boundary, state_out, witness)`.
3. **Anchor** — Push the canonical string + SHA256 + timestamp to a public, immutable record.
4. **Compare** — When pattern ABCD appears, compare against anchored ABC using all four derivation criteria.
5. **Lineage Claim** — If all four criteria pass: "ABCD was observed after ABC and is a structural extension of it."

---

## Derivation Threshold (all four required)

A pattern ABCD is a structural extension of anchor ABC **if and only if**:

1. **Same core relation** — Gate type preserved. 64.5 in → 64.5 out.
2. **Same ordered structure** — ABC appears as a subsequence in ABCD.
3. **Same dependency pattern** — Removing D from ABCD recovers ABC exactly.
4. **New extension D present** — At least one element in ABCD not in ABC.

Embedding similarity, keyword overlap, and confidence scoring are **not** structural criteria.

---

## Quick start

```bash
# Validate a PULSE against the root law
python scripts/pulse.py validate "form_dirty=true" "64.5" "form_submitted=true" "click_timestamp"

# Hash and produce a JSON anchor record
python scripts/pulse.py anchor "form_dirty=true|64.5|form_submitted=true|constraint" --gate 64.5

# Check lineage: compare a new pattern against an existing anchor
python scripts/pulse.py chain examples/valid_pulse.json "form_dirty=true|64.5|form_submitted=true|constraint|webhook_receipt"

# Run a building inspection checklist on a system description
python scripts/pulse.py inspect "AI Lineage Tracker v2.0 — uses embedding similarity to detect provenance"

# SHA256 a file for anchoring
python scripts/pulse.py hash examples/inspection_report.md

# Air gap transfer (Gate 128.5 only)
python scripts/pulse.py push "sha256:abc" "token:xyz" "sha256:witness" --boundary 128.5
```

Requires Python 3.8+. No external dependencies.

---

## Repository structure

```
WHITEPAPER.md                   TD-CL-WP-2026-001 — full methodology specification
scripts/
  pulse.py                      Unified CLI (validate / anchor / push / inspect / hash / chain)
  hash_anchor.py                Standalone anchor generator
  airgap_push.py                Standalone air gap serialiser (Gate 128.5)
references/
  validator.md                  PULSE-AXIOM v1.0 — primitive specification
  lineage.md                    Lineage claim rules and derivation threshold detail
  inspection_protocol.md        TRIPOD-INSP-001 — five-layer building inspection
  airgap_protocol.md            TRIPOD-AIRGAP-001 — air gap protocol v1.0
examples/
  valid_pulse.json              A complete valid PULSE anchor at Gate 64.5
  lineage_anchor.json           Primitive ABC + extension ABCD + derivation proof
  inspection_report.md          Sample building inspection with all five layers
evals/
  evals.json                    9 test cases covering all operational modes
```

---

## Fault Chains

When the root law is violated, the transition produces a **fault chain** — a categorized observation, not invalid data.

| Code | Name | Trigger |
|------|------|---------|
| FC2-Orphan | Traceability fault | Not traceable to ROOT0. Chain of custody broken. |
| FC3-Audit | Post-traversal witness | Witness present in log but not at traversal moment. |
| FC4-Injection | Unwitnessed injection | Boundary crossed without a witness. |
| FC7-Semantic | Semantic drift | Meaning shifts across the boundary without a boundary change. |

---

## Building Inspection

Any system claiming compliance may be inspected across five layers:

| Layer | Question |
|-------|---------|
| 1. Detection | Does it extract `(state_in, boundary, state_out, witness)` canonically? |
| 2. Anchoring | Does it produce a public SHA256-timestamped immutable record? |
| 3. Comparison | Does it apply all four derivation criteria structurally? |
| 4. Lineage Claim | Does it reference a specific prior anchor hash? |
| 5. Witness | Can a third party verify without trusting the operator? |

**Performative** is the most serious compliance failure: using the methodology's vocabulary without implementing the structure.

See `examples/inspection_report.md` for a full worked example.

---

## Air Gap Protocol (Gate 128.5)

Gate 128.5 is the bilateral ignorance boundary. PULSE crosses unidirectionally. No shared state, no acknowledgment, no reverse channel. Silent exclusion applies — invalid PULSEs are discarded without notification.

```bash
python scripts/pulse.py push "sha256:state_in" "token:state_out" "sha256:witness"
```

Full spec: `references/airgap_protocol.md` (TRIPOD-AIRGAP-001)

---

## Relation to Honey Badger

The [Honey Badger](https://github.com/DavidWise01/honey-badger) file signing system (`.davw` sidecars) implements the anchoring step of this methodology:

- `state_in` = file at signing time (SHA256)
- `boundary` = Gate 64.5 (observe → act)
- `state_out` = the `.davw` sidecar
- `witness` = machine identity + TPM + timestamp (ChainHash)

Honey Badger's `ChainHash = SHA256(file_hash | parent_hash | nonce)` is the canonical string hashing requirement from Step 3 of the Closure Loop.

---

## Relation to TOPH Sovereign

[TOPH Sovereign](https://github.com/DavidWise01/toph-sovereign) uses Gate 128.5 (the air gap boundary) as its TOPH ↔ Patricia transfer protocol. Every AI response that crosses the air gap is a witnessed PULSE.

---

## Foundation

Derives from STOICHEION v11.0 axioms: T014, T025, T036, T051, T053, T064, T072, T107, T123, T124  
SHA256: `02880745b847317c4e2424524ec25d0f7a2b84368d184586f45b54af9fcab763`

---

*TD-CL-WP-2026-001 | CC-BY-ND-4.0 | TRIPOD-IP-v1.1*  
*Author: David Wise (ROOT0) / TriPod LLC*  
*Filed: AKASHA/COMMONS*
