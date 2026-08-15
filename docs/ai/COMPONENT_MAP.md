# 🧭 Mentaury Soul — Component Map

Use this map after the AI entry point. Open only the affected slice.

| Domain | Purpose | Primary docs/code | Authority boundary |
|---|---|---|---|
| 🌱 Provenance / claims | represent attributed material without promotion | PCR docs + `src/mentaury/claims/**` | claim ≠ belief |
| ⚖️ Epistemic governance | route future epistemic change without taking over belief/evidence ownership | EPR docs; source implementation absent | routing ≠ mutation authority |
| 🪞 Identity continuity | preserve lineage through change/fork/restore | identity/continuity docs | continuity ≠ metaphysical proof |
| 🔗 Relations | exact PCR-anchored typed relation representation | ATR docs + `src/mentaury/relations/**` | relation ≠ truth/confidence |
| 🔬 Hypothesis discrimination | structural H1/H2 outcome discrimination | HDE docs + `src/mentaury/discrimination/**` | discrimination ≠ evidence verdict |
| 🎭 Character / presence | presentation and disposition | `docs/MENTAURY_CHARACTER_AND_PRESENCE_SPEC_V0.1.md` | character ≠ evidence |
| 🔐 Capability/privacy | bounded classification/composition | P1-001/P1-002/P1-003 docs + `src/mentaury/capabilities/**`, `privacy/**`, `composition/governed_constraints/**` | positive classification ≠ action authority |
| 🧾 Non-Projection | prevent imported interpretation from silently becoming SELF | NPG docs + `src/mentaury/non_projection/**` | PASS_ATTRIBUTED ≠ truth/identity |
| 🧩 Non-Projection composition | bind NPG result to the same admitted attempt | NPG-COMP docs + `src/mentaury/composition/non_projection_shadow/**` | shadow observation ≠ replay/runtime authority |
| 🧱 Storage / replay / evidence / beliefs | deterministic substrate and current belief/evidence owners | `src/mentaury/storage/**`, `replay/**`, `evidence/**`, `beliefs/**` | Evidence Gate remains sole support/contradiction owner |
| 🚦 Runtime/action | future activation boundaries | `docs/CURRENT_STATUS.md`, governance | implementation ≠ runtime/action authority |

## Current frontier

```text
PCR-v0.1   IMPLEMENTED_BOUNDED
EPR-v0.1   FROZEN_DOCS · NOT_IMPLEMENTED
ATR-v0.1   IMPLEMENTED_BOUNDED
HDE-v0.1   IMPLEMENTED_BOUNDED

claim→belief binding                NOT_IMPLEMENTED
terminal reconsideration lineage    NOT_IMPLEMENTED
runtime / retrieval / tools         NOT_AUTHORIZED
Action Gate / deployment            NOT_AUTHORIZED
```

Post-HDE next-step discrimination is tracked by issue `#129`. That issue is research-only
and does not select an implementation primitive or grant Owner GO.

## Reading rule

For any component:

```text
current state
→ owning frozen/accepted contract
→ implementation slice
→ tests
→ CI/review evidence
```

Do not infer runtime composition from the existence of source files, and do not infer
Evidence Gate authority from PCR, ATR or HDE outputs.
