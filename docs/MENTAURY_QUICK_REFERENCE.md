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
| NPG-v0.1 Pure Non-Projection Classifier | IMPLEMENTED_BOUNDED |
| NPG-v0.1 Owner GO | CONSUMED_BY_PR_90 |
| Non-Projection runtime | NOT_AUTHORIZED |
| P1-004 | NOT_ASSIGNED |
| Governance | SOLO_MAINTAINER · TIER_A |
| Next runtime milestone | NOT SELECTED · NOT AUTHORIZED |

## P1-001 evidence

```text
Authorization PR #62   merge d5e9e2fb11ea5a9c123c1cb1cc2b6f16dac53b98
Implementation PR #63  CI 31323051934 · 387 passed
Merge/main             f21809d8f31a457bd7acfe1d766230973ba9ecf5
Post-merge CI          31323138053 · success
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

## NPG-v0.1 in one diagram

```text
caller-supplied AttributedInterpretationEnvelope
+ caller-supplied NonProjectionBudget
                    │
                    ▼
        pure deterministic classifier
                    │
                    ├─ REJECT
                    ├─ DEFER
                    ├─ CONTESTED
                    ├─ REVISE_REQUIRED
                    └─ PASS_ATTRIBUTED
```

```text
NON_PROJECTION_CANDIDATE = PURE_NON_PROJECTION_CLASSIFIER
NON_PROJECTION_IMPLEMENTATION_CONTRACT = FROZEN_DOCS · NPG-v0.1
NON_PROJECTION_OWNER_GO = CONSUMED_BY_PR_90
NON_PROJECTION_IMPLEMENTATION = IMPLEMENTED_BOUNDED
NON_PROJECTION_RUNTIME = NOT_AUTHORIZED
P1_004 = NOT_ASSIGNED
```

Verified NPG evidence:

```text
Implementation PR #90
→ reviewed head a61427f85c70531b329894d5dc310e43bcc9d7de
→ CI 31438692348 · 762 passed
→ merge/main cfb59fb7a49166d55360c6a8843269ab8f18b9e0
→ main CI 31438898049 · success · 762 passed

Completion PR #91
→ pre-Phase-0 main a8891793532a47ed682a0b713a587d08f16a23bc
→ main CI 31439211018 · success · 768 passed
```

`PASS_ATTRIBUTED` is bounded classification data only. It is not truth,
autobiography, identity, relationship, retrieval, tool, Action Gate or deployment
authority.

## Fail-closed properties

- immutable admitted context for P1-003;
- exact P1-001/P1-002 projections;
- deterministic domain-separated fingerprints;
- same-attempt binding and freshness;
- blocker-over-defer precedence;
- complete `CGC-CTX/FP/DEC/T/M/PURE` frozen matrix;
- NPG-v0.1 explicit caller-supplied input only;
- NPG-v0.1 fail-closed projection handling;
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
Non-Projection runtime composition or activation
P1-004 assignment
backend selection or deployment
```

## Navigation

- `docs/CURRENT_STATUS.md`
- `docs/GOVERNANCE.md`
- `docs/P1_003_IMPLEMENTATION_AUTHORIZATION.md`
- `docs/research/P1_003_PURE_GOVERNED_CONSTRAINT_COMPOSER_CONTRACT.md`
- `docs/NON_PROJECTION_IMPLEMENTATION_AUTHORIZATION.md`
- `docs/research/NON_PROJECTION_PURE_CLASSIFIER_CONTRACT_V0_1.md`
- `docs/research/POST_P0_ROADMAP_V0.1.md`
- `docs/research/RESEARCH_INDEX.md`
