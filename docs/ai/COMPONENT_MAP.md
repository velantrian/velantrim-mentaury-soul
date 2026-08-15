# 🧭 Mentaury Soul — Component Map

Use this map after the AI entry point. Open only the affected slice.

| Domain | Purpose | Primary docs/code | Authority boundary |
|---|---|---|---|
| 🌱 Provenance / claims | represent attributed material without promotion | `docs/research/*PROVENANCE*`, `src/mentaury/**` | claim != belief |
| ⚖️ Epistemic governance | bounded promotion/revision decisions | `docs/research/*EPISTEMIC*` | routing != mutation authority |
| 🪞 Identity continuity | preserve lineage through change/fork/restore | identity/continuity docs | continuity != metaphysical proof |
| 🔗 Relations | typed anchored relations | Phase 5 / `ATR-v0.1` docs | relation != truth/confidence |
| 🎭 Character / presence | presentation and disposition | `docs/MENTAURY_CHARACTER_AND_PRESENCE_SPEC_V0.1.md` | character != evidence |
| 🔐 Capability/privacy | bounded classification/composition | P1-001/P1-002/P1-003 docs and source | positive classification != action authority |
| 🧾 Non-Projection | prevent imported interpretation from silently becoming SELF | NPG docs/source | PASS_ATTRIBUTED != truth/identity |
| 🚦 Runtime/action | future activation boundaries | `docs/CURRENT_STATUS.md`, governance | implementation != runtime/action authority |

## Reading rule

For any component:

```text
current state
→ owning frozen/accepted contract
→ implementation slice
→ tests
→ CI/review evidence
```

Do not infer runtime composition from the existence of source files.
