# Validator Reference — PULSE Axiom

## Canonical Form
PULSE Δ = (state_in, boundary, state_out, witness)

## Gates
| Gate  | Boundary                          |
|-------|-----------------------------------|
| 64.5  | observe ↔ act                    |
| 128.5 | TOPH ↔ Patricia (air gap)        |
| 192.5 | compute ↔ product (ignorance boundary) |
| 256.5 | wrap / recursion closure          |

## Witness Types
- `constraint` — predicate that must hold (e.g., `x > 0`)
- `token` — consumable capability (e.g., UUID, capability grant)
- `invariant` — global property (e.g., `total_balance == sum(accounts)`)

## Timing Rule
Witness must be present AT traversal. Post-traversal witness = audit artifact only,
not governance. Pre-traversal witness without traversal = precondition, not witness.

## Fault Chains
| Code | Trigger |
|------|---------|
| FC2-Orphan  | Not traceable to T128 (ROOT0) |
| FC3-Audit   | Witness absent at traversal; present only in log |
| FC4-Injection | Boundary injection without witness |
| FC7-Semantic  | Semantic drift across transition |

All fault chains converge at T064 (GATE-BOUNDARY) or T107 (semantic fault).

## Root Law
No transition without boundary.
No boundary without witness.
Witness must be present AT traversal.
