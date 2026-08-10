# 🧭 Mentaury Quick Reference

```text
P0-001…P0-015_IMPLEMENTED_IN_MAIN
P1-001…P1-001_IMPLEMENTED_IN_MAIN
P1-002…P1-002_IMPLEMENTED_IN_MAIN
P1-003…P1-003_IMPLEMENTED_IN_MAIN
```

## Current state

| Area | State |
|---|---|
| Canon v0.1 | FROZEN |
| P0 foundation | IMPLEMENTED |
| P1-001 Capability Lease resolver | IMPLEMENTED_BOUNDED |
| P1-002 Privacy Reconciliation Classifier | IMPLEMENTED_BOUNDED |
| P1-003 Pure Governed Constraint Composer | IMPLEMENTED_BOUNDED |
| P1-003 runtime assignment | NOT_ASSIGNED |
| Governance | SOLO_MAINTAINER · TIER_A |
| Next runtime milestone | NOT SELECTED · NOT AUTHORIZED |

## P1-001 evidence

```text
Authorization PR #62   merge d5e9e2fb11ea5a9c123c1cb1cc2b6f16dac53b98
Implementation PR #63  CI 31323051934 · 387 passed
Merge/main             f21809d8f31a457bd7acfe1d766230973ba9ecf5
Post-merge CI           31323138053 · success
NO_POST_P1_001_RUNTIME_MILESTONE_AUTHORIZED
```

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

`ALLOW_REFERENCE` performs no action and grants no retrieval permission.

## P1-003 in one diagram

```text
immutable CrossGateEvaluationContext
              │
              ├─ derive P1-001 ActionIntent
              ├─ derive P1-002 PrivacyAccessIntent
              │
              ▼
same-attempt pure bounded evaluation
              │
              ├─ NOT_ELIGIBLE
              ├─ DEFER
              └─ ELIGIBLE_FOR_NEXT_GATE
```

`ELIGIBLE_FOR_NEXT_GATE` remains next-gate readiness only.

## P1-003 verified evidence

```text
Owner GO PR #77
→ reviewed head 79fcedc8fe7dee64acad8dfffd8c8a17122ae97c
→ CI 31389769422 · 482 passed

Receipt reconciliation PR #78
→ reviewed head 0f52e683a03fe9fe27428e7effe0349fd496bd26
→ CI 31393515732 · 482 passed

Implementation PR #79
→ reviewed head 9855f766f2bf801c8297c4f870b21d3ed37911fb
→ CI 31394829487 · 552 passed
→ merge/main 59f2caa4deacd06aee0bbfc8dae1221edcb666eb
→ main CI 31395291622 · success · 552 passed
→ review 4897445251 · correctness PASS · adversarial PASS
```

```text
P1_003_OWNER_GO = CONSUMED
P1_003_IMPLEMENTATION = IMPLEMENTED_BOUNDED
P1_003_RUNTIME_ASSIGNMENT = NOT_ASSIGNED
NO_POST_P1_003_RUNTIME_MILESTONE_AUTHORIZED
```

## Fail-closed properties

- immutable admitted context;
- exact P1-001/P1-002 projections;
- deterministic domain-separated fingerprints;
- same-attempt binding and freshness;
- blocker-over-defer precedence;
- complete `CGC-CTX/FP/DEC/T/M/PURE` frozen matrix;
- no hidden network, database, filesystem, environment or clock authority;
- no authority amplification from positive gate results.

## Not authorized

```text
deletion or redaction execution
quarantine or rebuild execution
retrieval execution
registry persistence or scanning
Action Gate, Tool Receipt or tools
event/replay integration
belief, relationship, identity or M3 mutation
P1-003 runtime assignment or activation
backend selection or deployment
```

## Navigation

- `docs/CURRENT_STATUS.md`
- `docs/GOVERNANCE.md`
- `docs/P1_003_IMPLEMENTATION_AUTHORIZATION.md`
- `docs/research/P1_003_PURE_GOVERNED_CONSTRAINT_COMPOSER_CONTRACT.md`
- `docs/research/POST_P0_ROADMAP_V0.1.md`
- `docs/research/RESEARCH_INDEX.md`
