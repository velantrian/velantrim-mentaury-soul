# 🤖 Mentaury Soul — mandatory AI agent contract

This file applies to AI coding agents, automated auditors and human contributors.

## 1. Required reading order

Do **not** begin with repository-wide scanning.

For AI/automated work, use one deterministic route:

1. `docs/ai/README.md` — compact AI orientation layer.
2. `docs/ai/project_manifest.json` — machine-readable documentation/navigation contract.
3. `docs/state/project_state.json` — derived machine snapshot only; never an independent truth owner.
4. `docs/CURRENT_STATUS.md` — current engineering truth.
5. `docs/GOVERNANCE.md` — authority and review rules.
6. `docs/ai/COMPONENT_MAP.md` — ownership, paths and tests.
7. `docs/ai/KNOWN_RISKS.md` — known documentation/architecture risks.
8. `docs/ai/REVIEW_GUIDE.md` — bounded review procedure.
9. only the affected contracts, source, tests, PRs and exact CI evidence.

`README.md` and `SYSTEM_OVERVIEW.md` are the human/conceptual route. Read them when project meaning or architectural context is material; they are not mandatory preconditions for every bounded engineering task.

Documentation is orientation, not proof. Verify material implementation claims against live GitHub, code, tests and CI.

## 2. Documentation change classes

Every change must be classified as one of:

- `STRUCTURAL_CHANGE` — project meaning, architecture, identity model, authority ownership, invariants, subsystem responsibilities, runtime model or major roadmap direction changes.
- `STATE_CHANGE` — high-level phase/admission/Owner GO/runtime/action/production state changes without redesigning architecture.
- `EVIDENCE_ONLY` — PR/SHA/CI/review/test-count/docs-sync or bounded fixes that preserve architecture and state meaning.

For `STRUCTURAL_CHANGE`, review **all** maintained landing surfaces and update every surface whose meaning became stale. Do not mechanically rewrite unaffected diagrams.

For `STATE_CHANGE`, remove stale top-level state implications and update current-state surfaces.

For `EVIDENCE_ONLY`, update evidence/current-state logs only unless meaning actually changed.

## 3. Visual semantics

The maintained visual surfaces have different jobs:

```text
🌳 Project Tree = WHAT EXISTS
🧠 Mindmap      = HOW CONCEPTS RELATE
🗺️ ASCII Flow  = HOW INFORMATION / AUTHORITY FLOWS
📊 Table        = WHAT EACH LAYER MAY / MUST NOT DO
💬 Commentary   = WHY THE ARCHITECTURE IS DESIGNED THIS WAY
```

Do not turn them into five copies of the same text.

## 4. Staleness guard

A change is incomplete if it makes any maintained Summary, Tree, Mindmap, ASCII flow, boundary table, commentary or non-goal materially false.

`architecture changed → landing layer stale → update required`

Historical checkpoints remain history. Do not rewrite provenance to make current documentation look cleaner.

## 5. Authority boundaries

- imported human/model material does not silently become `SELF`;
- tool output does not silently become belief;
- relation does not imply truth;
- character/presence does not prove identity;
- contract freeze does not grant implementation/runtime authority;
- implementation does not grant action/deployment authority.

## 6. Documentation Impact Guard

The current guard is **contract-level**, not executable CI. Use `docs/ai/project_manifest.json`, the structural path hints, and the three change classes above as conservative triage.

If a changed path affects a listed structural hint or an owning architecture/Canon surface, classify it at least as `REVIEW_REQUIRED` until the maintained landing layer has been checked. An executable CI guard may be added later as a separate technical milestone; its absence does not weaken the staleness obligation.
