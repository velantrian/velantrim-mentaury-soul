# 🤖 Mentaury Soul — AI Agent Entry Point

This is the compact orientation layer for AI coding agents, reviewers and maintainers. Its purpose is to reduce blind repository-wide scanning while preserving architectural distinctions and the human-first documentation architecture.

If you arrived here directly, `../../AGENTS.md` is the mandatory agent contract. Do not bounce back through the human landing pages before continuing a bounded engineering task.

## 1. Required reading order

1. `project_manifest.json` — machine-readable documentation/navigation contract.
2. `../state/project_state.json` — derived machine snapshot only; not an independent current-truth owner.
3. `../CURRENT_STATUS.md` — current engineering truth.
4. `../GOVERNANCE.md` — authority and review rules.
5. `AUDIT_AND_FUTURE_WORK.md` — durable future-work/audit queue, evidence anchors, revalidation triggers and safe continuation boundary. **Audit order is not implementation order.**
6. `COMPONENT_MAP.md` — ownership, paths and tests.
7. `KNOWN_RISKS.md` — known documentation/architecture risks.
8. `REVIEW_GUIDE.md` — bounded review procedure.
9. only the affected research contracts, source, tests, PRs and exact CI evidence.

Use `../../README.md` and `../../SYSTEM_OVERVIEW.md` when conceptual/human context is materially needed. They are orientation surfaces, not an additional mandatory loop in the AI route.

Do **not** begin with repository-wide scanning unless focused evidence is insufficient.

> **DO NOT AUTO-SELECT NEXT MILESTONE.** A ledger entry, open Issue, frozen contract, implemented bounded primitive, desired behavior or suggested audit order does not grant implementation/runtime authority.

---

## 2. Source-of-truth hierarchy

```text
live merged GitHub code
→ executable tests and exact CI
→ CURRENT_STATUS + live governance
→ accepted/frozen owning contracts
→ derived machine state snapshot
→ README / SYSTEM_OVERVIEW orientation
→ docs/ai navigation + future-work ledger
→ PR/issues/research proposals
→ Notion rationale/history
```

`docs/state/project_state.json` is a compact derived view. If it disagrees with live GitHub or `docs/CURRENT_STATUS.md`, the snapshot is stale and must be corrected; it never wins the conflict.

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
🤖 AGENTS.md
→ docs/ai/README.md
→ project manifest
→ derived snapshot + CURRENT_STATUS
→ future-work ledger
→ affected component
→ owning contract
→ focused code/tests
→ exact PR/CI/review evidence
→ wider search only when evidence demands it
```

Do not load all historical research documents by default.

---

## 5. Human documentation architecture is maintained, not decorative

The repository intentionally separates one project truth into derived presentations:

```text
                 🧬 ONE PROJECT TRUTH
                         │
       ┌─────────────────┼─────────────────┐
       │                 │                 │
       ▼                 ▼                 ▼
   👤 HUMAN          🤖 AGENT          ⚙️ MACHINE
README / OVERVIEW    docs/ai/**       derived JSON
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
→ technical and historical detail
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

The future-work ledger has its own revalidation triggers. When an owner, authorization, Issue/PR lifecycle, or referenced contract changes, reconcile the affected ledger entry rather than assuming it remains current.

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
