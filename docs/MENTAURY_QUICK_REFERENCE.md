# 🧭 Mentaury Quick Reference

```text
P0-001…P0-015_IMPLEMENTED_IN_MAIN
P1-001…P1-001_IMPLEMENTED_IN_MAIN
P1-002…P1-002_IMPLEMENTED_IN_MAIN
```

## Current state

| Area | State |
|---|---|
| Canon v0.1 | FROZEN |
| P0 foundation | IMPLEMENTED |
| P1-001 Capability Lease resolver | IMPLEMENTED_BOUNDED |
| P1-002 Privacy Reconciliation Classifier | IMPLEMENTED_BOUNDED |
| Governance | SOLO_MAINTAINER · TIER_A |
| Next runtime milestone | NOT SELECTED · NOT AUTHORIZED |

## P1-002 in one diagram

```text
caller-supplied material
+ caller-supplied copy
+ caller-supplied access intent
+ caller-supplied budgets
              │
              ▼
pure fail-closed classifier
              │
              ├─ ALLOW_REFERENCE
              ├─ DENY_RETRIEVAL
              ├─ QUARANTINE_REQUIRED
              └─ REBUILD_REQUIRED
```

The result performs no action and grants no retrieval permission.

## Verified evidence

```text
Contract PR #65
→ CI 31331396018 · 401 passed
→ merge 1dc7bcf97986f455f48beb121c2048dfc34bd11c

Authorization PR #66
→ CI 31331910395 · 398 passed
→ merge 8f4c444e2144d1dffde20fc60d6d5250148d07e6

Implementation PR #67
→ reviewed head 74662fb626a545ed63b426e98aa03524449019db
→ CI 31332728486 · 461 passed
→ merge d64679fd745e859527a70746df5e69dc9aca0408
→ main CI 31332793742 · success · 461 passed
```

## Fail-closed properties

- exact typed-or-mapping admission;
- immutable values;
- sorted unique allowlists;
- exact linkage and policy revision checks;
- canonical byte-budget across all four inputs;
- fixed budget validation order;
- empty allowlists grant nothing;
- exact first-match precedence;
- impossible result pairs rejected;
- no network, database, filesystem, environment or clock authority.

## Not authorized

```text
deletion or redaction execution
quarantine or rebuild execution
retrieval execution
registry persistence or copy scanning
Action Gate, Tool Receipt or tools
event/replay integration
belief, relationship, identity or M3 mutation
backend selection or deployment
```

## Navigation

- `docs/CURRENT_STATUS.md`
- `docs/GOVERNANCE.md`
- `docs/P1_002_IMPLEMENTATION_AUTHORIZATION.md`
- `docs/research/P1_002_PRIVACY_RECONCILIATION_CLASSIFIER_NOTES.md`
- `docs/research/POST_P0_ROADMAP_V0.1.md`
