# Lineage Mode — Local Closure Loop

## Core Concept
sandbox → extract ABC → anchor (hash + timestamp + repo) → future input ABCD → compare → lineage claim

## Derivation Threshold (ALL four must be true)

1. **Same core relation** — fundamental transformation type identical; gate type preserved.
2. **Same ordered structure** — state_in → boundary → state_out → witness_type appears as
   subsequence in ABCD. No reordering. Insertion allowed only if original sequence preserved.
3. **Same dependency pattern** — removing D recovers exactly ABC's dependencies.
4. **New extension D present** — at least one element not in ABC. Duplicates do not qualify.

## Anchor Format
```json
{
  "primitive_id": "ABC",
  "canonical_string": "state_in:X|boundary:64.5|state_out:Y|witness:Z",
  "hash": "sha256:...",
  "timestamp": "ISO8601",
  "context": "original snippet",
  "gate": "64.5",
  "witness_type": "constraint"
}
```

## Comparison Algorithm (pseudocode)
```
def is_lineage(anchor, new_pattern):
    if anchor.gate != new_pattern.gate:
        return False
    if not subsequence(anchor.ordered_structure, new_pattern.ordered_structure):
        return False
    if not same_dependencies(anchor.dependencies, new_pattern.dependencies - new_extension):
        return False
    if no_new_extension(anchor, new_pattern):
        return False
    return True
```

## What Lineage Is Not
- Not ownership of the structural primitive
- Not proof that ABC caused ABCD
- Not similarity scoring or embedding distance
- Not a legal claim without additional proceedings

## Reference
TD-CL-WP-2026-001 §4–§5 is the authoritative specification.
