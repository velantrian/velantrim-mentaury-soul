# 🧭 Mentaury Soul — Component Map

Use this map after the AI entry point. Open only the affected slice.

| Domain | Purpose | Primary docs/code | Authority boundary |
|---|---|---|---|
| 🌱 Provenance / claims | represent attributed material without promotion | PCR docs + `src/mentaury/claims/**` | claim ≠ belief |
| 🧷 Claim→belief binding | preserve exact PCR identity at belief genesis without promoting truth/evidence | CBP docs + `src/mentaury/claim_belief_binding/**` | binding ≠ evidence support / truth authority |
| ⚖️ Epistemic governance | route bounded epistemic change without taking over belief/evidence ownership | EPR docs + `src/mentaury/epistemic_change/**` | routing ≠ mutation authority |
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
CBP-v0.1   IMPLEMENTED_BOUNDED · MERGED_BY_PR_147
EPR-v0.1   IMPLEMENTED_BOUNDED · MERGED_BY_PR_148
ATR-v0.1   IMPLEMENTED_BOUNDED
HDE-v0.1   IMPLEMENTED_BOUNDED

V1 offline epistemic E2E            VERIFIED · MERGED_BY_PR_150
V1 Research/Core                    1.0.0 · FINAL_ACCEPTANCE
terminal reconsideration lineage    NOT_IMPLEMENTED · V1.1/V2_BACKLOG
runtime / retrieval / tools         NOT_AUTHORIZED
Action Gate / deployment            NOT_AUTHORIZED
```

Issue `#129` is a **closed/superseded historical research checkpoint**, not the current execution frontier. Its selected EPR route and claim→belief prerequisite were subsequently implemented bounded through PRs #147 and #148.

Terminal reconsideration / successor lineage remains explicit V1.1/V2 backlog with no current implementation or runtime authority.

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
Evidence Gate authority from PCR, CBP, EPR, ATR or HDE outputs.
