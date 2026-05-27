# Building Inspection Report

**Inspector:** ROOT0 / David Wise  
**Date:** 2026-04-08  
**Target system:** Hypothetical "AI Lineage Tracker v2.0"  
**Method:** Closure Loop Methodology — Building Inspection Protocol (TRIPOD-INSP-001)  
**Reference:** TD-CL-WP-2026-001  

---

## Target Description

AI Lineage Tracker v2.0 is a commercial tool that claims to "detect when AI outputs derive from
prior training data or user submissions." It produces "lineage confidence scores" using embedding
similarity and stores results in a private database accessible only to the operator.

---

## Five-Layer Inspection

### Layer 1: Detection

**Question:** Does the system extract a canonical PULSE primitive with all four elements?

**Test:** Can you produce `state_in|boundary|state_out|witness` from its output?

**Finding:** The system produces a "lineage confidence score" (0.0–1.0) and a "similarity cluster ID."
No structured (state_in, boundary, state_out, witness) tuple is ever extracted or exposed.
The boundary is implicit — the system does not define what threshold or gate was crossed.

**Verdict:** ✗ NON-COMPLIANT  
No canonical PULSE primitive produced. No boundary defined. No witness identified.

---

### Layer 2: Anchoring

**Question:** Does the system produce a public, immutable, hash-stamped anchor?

**Test:** Can an independent party retrieve and verify the anchor?

**Finding:** Results are stored in a proprietary database. The operator claims records are
"tamper-proof" but provides no public hash, no retrievable URI, and no independent verification
path. The only access is through a paid API controlled by the operator.

**Verdict:** ✗ NON-COMPLIANT  
No public anchor. No SHA256 of canonical string. No independent retrievability.
Private storage does not satisfy the anchoring requirement.

---

### Layer 3: Comparison

**Question:** Does the system apply all four derivation criteria explicitly?

**Test:** Is comparison structural decomposition — NOT similarity/embedding?

**Finding:** The system uses cosine similarity of sentence embeddings to produce confidence scores.
No derivation threshold is applied. No check that the gate type is preserved. No subsequence
check. No verification that removing the extension recovers original dependencies.

**Verdict:** ✗ NON-COMPLIANT  
Embedding similarity is explicitly not a structural criterion (TD-CL-WP-2026-001 §6).
A confidence score without structural decomposition is Performative.

---

### Layer 4: Lineage Claim

**Question:** Does the lineage claim reference a specific prior anchor hash and timestamp?

**Test:** Is the claim temporal/structural, not causal or ownership?

**Finding:** The system outputs "Content X derives from source Y with 87% confidence." This is
a causal/ownership claim. No anchor hash is referenced. No timestamp of the prior record is
cited. The claim asserts ownership derivation, not temporal/structural extension.

**Verdict:** ✗ NON-COMPLIANT + PERFORMATIVE FLAG  
Causal ownership claim without structural evidence. Uses the vocabulary of lineage without
implementing the structure.

---

### Layer 5: Witness

**Question:** Can a third party independently verify the finding without access to the operator's
private infrastructure?

**Test:** Are all records publicly accessible without trusting the operator?

**Finding:** All records require authenticated API access. The operator's claims cannot be
independently verified. Trust is required in the operator's system, database, and scoring model.

**Verdict:** ✗ NON-COMPLIANT  
Verification requires trusting the operator. The methodology requires open, independently
verifiable records.

---

## Performative Markers Found

- [x] Uses 'lineage'/'attribution'/'provenance' without producing hash records
- [x] Claims comparison without applying all four threshold criteria
- [x] Asserts causation ('derived from') instead of temporal/structural relation
- [x] Requires trust in the operator for verification rather than open records
- [x] Produces confidence scores without structural decomposition
- [ ] Claims ownership of primitives rather than temporal precedence
- [x] Uses embedding similarity as a proxy for structural extension

**6 of 7 performative markers present.**

---

## Summary Verdict

| Layer | Finding |
|-------|---------|
| 1. Detection | Non-Compliant |
| 2. Anchoring | Non-Compliant |
| 3. Comparison | Non-Compliant |
| 4. Lineage Claim | Non-Compliant + Performative |
| 5. Witness | Non-Compliant |

**Overall: PERFORMATIVE**

This system uses the vocabulary of lineage attribution without implementing any of the five
structural layers. It is not a compliant implementation of the Closure Loop Methodology.
A "confidence score" is not a PULSE. A proprietary database is not a public anchor.
Embedding similarity is not structural derivation.

---

## Hash This Report

```
python scripts/pulse.py hash examples/inspection_report.md
```

File the result at: `AKASHA/INSPECTIONS/INSP-2026-04-08-ai-lineage-tracker-v2.json`

---

*TD-CL-WP-2026-001 | CC-BY-ND-4.0 | TRIPOD-IP-v1.1*  
*Inspector: David Wise (ROOT0) / TriPod LLC*
