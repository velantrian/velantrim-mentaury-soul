# 📚 Velantrim Documentation Standard v1

This repository uses four documentation layers:

```text
👤 Human landing / stable project portrait
        ↓
🤖 AI orientation + maintenance contract
        ↓
🚦 Current technical / machine truth
        ↓
🧾 Evidence + historical checkpoints
```

## Core rule

`overview != current state != evidence != history`

## Change classification

### STRUCTURAL_CHANGE
Changes architecture, project meaning, ownership, authority boundaries, invariants, subsystem responsibilities, runtime model or major roadmap direction.

Action: review all maintained landing surfaces and update each surface whose meaning became stale. Update owning architecture/current-state docs and the machine manifest when navigation or ownership changes. Do not mechanically rewrite unaffected visual blocks.

### STATE_CHANGE
Changes phase, admission, Owner GO, implementation/readiness/runtime/action/production state without redesigning architecture.

Action: remove stale landing-state implications and update current-state surfaces.

### EVIDENCE_ONLY
Changes PR/SHA/CI/review/test counts/sync evidence or bounded implementation evidence without changing architecture or high-level state meaning.

Action: update evidence/current-state logs. Stable landing visuals normally remain unchanged.

## Visual semantics

```text
🌳 Tree       = WHAT EXISTS
🧠 Mindmap    = HOW CONCEPTS RELATE
🗺️ ASCII      = HOW INFORMATION / AUTHORITY FLOWS
📊 Table       = WHAT LAYERS MAY / MUST NOT DO
💬 Commentary = WHY THE ARCHITECTURE IS DESIGNED THIS WAY
```

A visual is stale only when its assigned meaning is materially wrong.

## Stable vs volatile content

Stable portrait: purpose, core architecture, persistent invariants, non-goals, documentation routes.

Volatile surfaces: current phase, PR/SHA/CI/test counts, temporary blockers, review state and exact checkpoints.

Avoid copying volatile evidence into stable visual blocks.

## Machine-readable contract

`project_manifest.json` is the navigation and maintenance contract, not implementation truth. Current implementation truth remains in the repository-designated current-state surface and live GitHub evidence.

## Staleness guard

```text
meaning changed
→ landing surfaces reviewed
→ affected representations refreshed
→ current truth refreshed
→ history preserved
```

## Documentation impact guard

The current guard is contract-level: use `project_manifest.json`, structural path hints and the three change classes as conservative triage. A path that touches an owning architecture/Canon surface must be treated as `REVIEW_REQUIRED` until landing documentation has been checked. An executable CI guard is a separate future technical milestone.
