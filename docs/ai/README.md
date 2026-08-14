# 🤖 Mentaury Soul — AI Agent Entry Point

This is the compact orientation layer for AI coding agents, reviewers and maintainers. Its purpose is to reduce blind repository-wide scanning while preserving architectural distinctions and the human-first documentation architecture.

## 1. Required reading order

1. `../../README.md` — stable human project identity and conceptual portrait.
2. `../../SYSTEM_OVERVIEW.md` — deep human mental model and architecture map.
3. `../../AGENTS.md` — mandatory agent contract.
4. `project_manifest.json` — machine-readable documentation/navigation contract.
5. `../state/project_state.json` — machine state snapshot.
6. `../CURRENT_STATUS.md` — current engineering truth.
7. `../GOVERNANCE.md` — authority and review rules.
8. `COMPONENT_MAP.md` — ownership, paths and tests.
9. `KNOWN_RISKS.md` — known documentation/architecture risks.
10. `REVIEW_GUIDE.md` — bounded review procedure.
11. only the affected research contracts, source, tests, PRs and exact CI evidence.

Do **not** begin with repository-wide scanning unless focused evidence is insufficient.

---

## 2. Source-of-truth hierarchy

```text
live merged GitHub code
→ executable tests and exact CI
→ CURRENT_STATUS + live governance
→ accepted/frozen owning contracts
→ machine state snapshot
→ README / SYSTEM_OVERVIEW orientation
→ docs/ai navigation
→ PR/issues/research proposals
→ Notion rationale/history
```

Human-facing visuals are **orientation, not proof**. Never infer implementation, runtime or authority state from a diagram, table, emoji, prose summary or roadmap arrow.

---

## 3. Project identity

Mentaury Soul is a substrate-neutral research architecture for evolving digital individuality in which provenance, claims, beliefs, relations, identity continuity, character and authority remain distinct and governed.

```text
tool output != belief
source != provenance
claim != belief
relation != truth
character != evidence
memory != identity
continuity != identity proof
heritage != autobiography
contract freeze != implementation authority
implementation != runtime authority
runtime capability != action authority
```

---

## 4. Context-budget route

```text
🤖 AI entry
→ project manifest
→ machine/current state
→ affected component
→ owning contract
→ focused code/tests
→ exact PR/CI/review evidence
→ wider search only when evidence demands it
```

Do not load all historical research documents by default.

---

## 5. Human documentation architecture is maintained, not decorative

The repository intentionally separates one project truth into four presentations:

```text
                 🧬 ONE PROJECT TRUTH
                         │
       ┌─────────────────┼─────────────────┐
       │                 │                 │
       ▼                 ▼                 ▼
   👤 HUMAN          🤖 AGENT          ⚙️ MACHINE
README / OVERVIEW    docs/ai/**       JSON state
       │                 │                 │
       └─────────────────┴────────┬────────┘
                                  ▼
                         📚 EVIDENCE / HISTORY
```

The human layer must remain readable from meaning → mental model → current capability → research boundary → engineering detail.

A structural change is incomplete if it makes a maintained human visual materially false.

---

## 6. Visual roles

Each visual representation has a distinct semantic job:

```text
🗺️ Mindmap    = HOW CONCEPTS RELATE
⚙️ ASCII      = HOW INFORMATION / AUTHORITY FLOWS
🌳 Tree       = WHAT EXISTS
🔄 Diagram    = HOW ARCHITECTURAL LAYERS CONNECT
📊 Table      = WHAT EXISTS / MAY / MUST NOT DO
💬 Commentary = WHY THE ARCHITECTURE IS DESIGNED THIS WAY
```

Do not mechanically duplicate the same content into every visual. Update only the representations whose assigned meaning became stale.

---

## 7. Documentation maintenance

Use `DOCUMENTATION_STANDARD.md` and `project_manifest.json`.

Every documentation-affecting change must be classified as one of:

- `STRUCTURAL_CHANGE`
- `STATE_CHANGE`
- `EVIDENCE_ONLY`

### STRUCTURAL_CHANGE

Review the full maintained human landing sequence:

```text
project identity
→ human explanation
→ mental model
→ mindmap / ASCII / tree / architecture diagram
→ human capability table
→ positioning / non-goals
→ reading routes
→ research boundary
→ quickstart implications
```

Update every affected representation and leave unaffected ones alone.

### STATE_CHANGE

Update current-state surfaces and remove stale high-level implications. Do not redraw architecture unless the meaning changed.

### EVIDENCE_ONLY

Update evidence/current-state logs where required. Do not churn stable landing visuals for new SHA/CI/test-count values.

---

## 8. Staleness rule

```text
meaning changed
→ classify documentation impact
→ verify owning architecture/contract
→ review maintained human landing roles
→ refresh affected agent/machine routes
→ refresh current truth
→ preserve historical provenance
→ read back
```

Historical checkpoints remain history. Do not rewrite them merely to make current documentation look cleaner.

---

## 9. Authority ceiling

Documentation work never grants:

```text
Owner GO
runtime activation
retrieval
model/LLM execution
filesystem/network/database authority
tool execution
Action Gate PASS
identity mutation
relationship mutation
M3 write
deployment
```

If a documentation change appears to imply any of those, stop and verify the owning authorization surface.