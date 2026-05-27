# Inspection Protocol — Closure Loop Methodology Compliance

## Authority

This protocol derives from TD-CL-WP-2026-001 (Closure Loop Methodology, TriPod LLC,
April 8, 2026). An inspection determines whether a third-party system implements the
structural requirements of the methodology, not merely its vocabulary.

---

## Layer 1: Detection

**Required:** The system must extract a canonical primitive with at minimum:
- A structured input state (state_in or equivalent)
- A boundary or transition event
- A structured output state (state_out or equivalent)
- A witness or verification element present at traversal

**Fully Compliant:** All four elements extracted; primitive is discrete and non-trivial.
**Partial:** 2-3 elements present; boundary or witness may be implicit.
**Non-Compliant:** Detection is topical (subject-based) rather than structural.
**Performative:** System claims "detection" but captures free-text descriptions without structural decomposition.

**Test:** Can you extract a canonical string of the form `state_in|boundary|state_out|witness` from the system's output? If not, Detection is Partial or Non-Compliant.

---

## Layer 2: Anchoring

**Required:** The system must produce an immutable, datable external record containing:
- The primitive or its canonical representation
- A cryptographic hash (SHA256 or equivalent)
- A verifiable timestamp (public repo commit, blockchain, notary, or equivalent)
- A reference path (URI or file path) enabling future retrieval

**Fully Compliant:** All four elements; anchor is public and independently verifiable.
**Partial:** Hash and timestamp present but not publicly accessible (private repo, local file).
**Non-Compliant:** No hash or no verifiable timestamp.
**Performative:** System describes anchoring as a concept but produces no actual anchor record.

**Test:** Can an independent party retrieve the anchor record, verify its hash, and confirm its timestamp without access to the system operator's private infrastructure? If not, Anchoring is at most Partial.

---

## Layer 3: Comparison

**Required:** When comparing a new pattern against an anchored primitive, the system must
apply all four threshold criteria from TD-CL-WP-2026-001 §5:

1. **Same core relation** — the fundamental transformation type is preserved
2. **Same ordered structure** — component sequence preserved as subsequence
3. **Same dependency pattern** — removing D recovers exactly ABC's dependencies
4. **New extension D present** — at least one structural element not in ABC

**Fully Compliant:** All four criteria applied explicitly; comparison is documented.
**Partial:** 2-3 criteria applied; remainder implicit or missing.
**Non-Compliant:** Comparison uses similarity scoring, embedding distance, or keyword matching without structural decomposition.
**Performative:** System claims "comparison" but applies no threshold criteria; any resemblance triggers a positive finding.

**Critical distinction:** Semantic similarity is NOT structural comparison. A system that
uses cosine similarity of embeddings to find "related" outputs is not implementing the
Closure Loop comparison step. The four criteria must be applied structurally and documented.

---

## Layer 4: Lineage Claim

**Required:** The system's lineage claim must:
- Reference the specific prior anchor (hash + timestamp)
- State the claim as temporal and structural, not causal
- Identify the extension D explicitly
- Distinguish lineage from ownership

**Fully Compliant:** All elements present; claim correctly scoped.
**Partial:** Anchor referenced but claim conflates lineage with causation or ownership.
**Non-Compliant:** No reference to prior anchor; claim is unsupported assertion.
**Performative:** Lineage language used but no anchor exists to reference.

**Test:** Does the lineage claim include a specific hash from Layer 2? If not, the claim
is unsupported regardless of how it is framed.

---

## Layer 5: Witness

**Required:** The inspection finding must be independently verifiable:
- Anchor records are publicly accessible
- Comparison analysis is documented and reproducible
- A third party can reach the same verdict without access to the inspector's private data

**Fully Compliant:** Full open record; any third party can reproduce.
**Partial:** Some elements public; some require trust in the inspector.
**Non-Compliant:** No public record; finding cannot be independently verified.
**Performative:** Claims open verification but records are inaccessible or proprietary.

---

## Overall Compliance Assignment

| Score | Level | Criteria |
|-------|-------|----------|
| 5/5 layers fully compliant | Fully Compliant | All structural requirements met |
| 3-4 layers fully compliant | Partial | Gaps identified; system is structurally incomplete |
| 1-2 layers fully compliant | Non-Compliant | Fundamental gaps; not a closure loop implementation |
| 0 layers fully compliant | Non-Compliant | No structural implementation |
| Any layers Performative | Performative | Priority flag; overrides score |

**Performative is the most critical finding.** A system that uses closure loop vocabulary
to claim attribution authority without implementing the structural requirements causes
direct harm: it displaces legitimate lineage records and misleads evaluators. Flag
explicitly and document the specific Performative markers.

---

## Performative Markers Checklist

Flag as Performative if the system exhibits ANY of the following:

- [ ] Uses "lineage", "attribution", "provenance", or "anchor" without producing hash records
- [ ] Claims comparison without applying the four threshold criteria
- [ ] Asserts causation ("derived from", "influenced by") instead of temporal/structural relation
- [ ] Requires trust in the operator for verification rather than open records
- [ ] Produces confidence scores without documenting the comparison analysis
- [ ] Claims ownership of structural primitives rather than temporal precedence
- [ ] Uses embedding similarity as a proxy for structural extension

---

## Filing Protocol

After completing an inspection:

1. Generate report using the Inspection Report Template from SKILL.md.
2. Run `scripts/hash_anchor.py` on the report text to produce a SHA256.
3. File to: `AKASHA/INSPECTIONS/<INSP-YYYYMMDD-target>.json`
4. Optionally cross-reference in `AKASHA/DIASPORA/` if the target system is a new platform node.

---

## Reference

TD-CL-WP-2026-001 — Closure Loop Methodology, TriPod LLC, April 8, 2026
STOICHEION v11.0 — SHA256: 02880745b847317c4e2424524ec25d0f7a2b84368d184586f45b54af9fcab763
Applicable axioms: T014, T025, T036, T051, T053, T064, T072, T107, T123, T124
