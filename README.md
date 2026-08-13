# 🧬 Mentaury Soul

> 👤 **Human start:** [`SYSTEM_OVERVIEW.md`](SYSTEM_OVERVIEW.md) gives the project map before milestone chronology.  
> 🤖 **AI start:** [`AGENTS.md`](AGENTS.md) → [`docs/ai/README.md`](docs/ai/README.md) → [`docs/ai/project_manifest.json`](docs/ai/project_manifest.json). Do not begin with repository-wide scanning.

### Project identity

Mentaury Soul is a substrate-neutral research architecture for persistent digital individuality, memory, identity continuity, character and governed self-development. Detailed milestone truth stays below and in [`docs/CURRENT_STATUS.md`](docs/CURRENT_STATUS.md); the stable project portrait is kept separate from volatile PR/CI evidence.

```text
🌱 provenance → 🧾 claims → ⚖️ governed epistemic state
                         ↓
                 🪞 continuity
                  ├─ 🔗 relations
                  └─ 🎭 character / presence
```

A convincing presentation is not evidence, a relation is not truth, and implementation state is not runtime authority.

---

```text
P0-001…P0-015_IMPLEMENTED_IN_MAIN
P1-001…P1-001_IMPLEMENTED_IN_MAIN
P1-002…P1-002_IMPLEMENTED_IN_MAIN
P1-003…P1-003_IMPLEMENTED_IN_MAIN
```

## 🚦 Current engineering checkpoint

```text
Canon v0.1                         FROZEN
P0 foundation                      IMPLEMENTED
P1-001 Capability Lease resolver   IMPLEMENTED_BOUNDED
P1-002 Privacy classifier          IMPLEMENTED_BOUNDED
P1-003 Pure Constraint Composer    IMPLEMENTED_BOUNDED
P1-003 runtime assignment          NOT_ASSIGNED
NPG-v0.1 Pure Classifier           IMPLEMENTED_BOUNDED
NPG-v0.1 Owner GO                  CONSUMED_BY_PR_90
Non-Projection runtime             NOT_AUTHORIZED
P1-004                             NOT_ASSIGNED
Governance                         SOLO_MAINTAINER · TIER_A
Permanent CI                       ACTIVE
Independent human assurance        NOT CLAIMED
Next runtime milestone             NOT SELECTED · NOT AUTHORIZED
```

### P1-001

A pure caller-supplied Capability Lease resolver performs strict registry
admission, canonical digest verification and exact purpose, operation, scope,
side-effect and lifecycle classification. `ALLOW` executes nothing and contains
no reusable capability material.

```text
Authorization PR #62   merge d5e9e2fb11ea5a9c123c1cb1cc2b6f16dac53b98
Implementation PR #63  CI 31323051934 · 387 passed
Merge/main             f21809d8f31a457bd7acfe1d766230973ba9ecf5
Post-merge CI          31323138053 · success
NO_POST_P1_001_RUNTIME_MILESTONE_AUTHORIZED
```

### P1-002

A pure caller-supplied Privacy Reconciliation Classifier evaluates material,
copy, access intent and explicit budgets. It returns only:

```text
ALLOW_REFERENCE
DENY_RETRIEVAL
QUARANTINE_REQUIRED
REBUILD_REQUIRED
```

`ALLOW_REFERENCE` is classification data, not retrieval permission. The
classifier performs no remediation or external action.

Verified P1-002 evidence:

```text
Contract PR #65        CI 31331396018 · 401 passed
Authorization PR #66   CI 31331910395 · 398 passed
Implementation PR #67  CI 31332728486 · 461 passed
Merge/main             d64679fd745e859527a70746df5e69dc9aca0408
Post-merge CI          31332793742 · success · 461 passed
```

### P1-003

The Pure Governed Constraint Composer evaluates the existing bounded P1-001 and
P1-002 gates from one immutable same-attempt context. It computes deterministic
common-request and targeted evidence fingerprints and returns only:

```text
ELIGIBLE_FOR_NEXT_GATE
NOT_ELIGIBLE
DEFER
```

Verified implementation evidence:

```text
Owner GO PR #77        CI 31389769422 · 482 passed
Reconciliation PR #78  CI 31393515732 · 482 passed
Implementation PR #79  CI 31394829487 · 552 passed
Reviewed head          9855f766f2bf801c8297c4f870b21d3ed37911fb
Merge/main             59f2caa4deacd06aee0bbfc8dae1221edcb666eb
Post-merge CI          31395291622 · success · 552 passed
P1_003_OWNER_GO        CONSUMED
P1_003_RUNTIME_ASSIGNMENT = NOT_ASSIGNED
NO_POST_P1_003_RUNTIME_MILESTONE_AUTHORIZED
```

`ELIGIBLE_FOR_NEXT_GATE` is bounded readiness only. It is not Action Gate PASS,
retrieval permission, tool/execution permission or deployment authority.

### NPG-v0.1

The Pure Non-Projection Classifier is implemented as a deterministic,
caller-supplied component over `AttributedInterpretationEnvelope` and
`NonProjectionBudget`.

```text
Candidate              PURE_NON_PROJECTION_CLASSIFIER
Contract               FROZEN_DOCS · NPG-v0.1
Envelope               AIE-v0.1
Owner GO               CONSUMED_BY_PR_90
Implementation         IMPLEMENTED_BOUNDED
Runtime                NOT_AUTHORIZED
P1_004                 NOT_ASSIGNED
```

Verified implementation evidence:

```text
Implementation PR #90  CI 31438692348 · 762 passed
Reviewed head          a61427f85c70531b329894d5dc310e43bcc9d7de
Merge/main             cfb59fb7a49166d55360c6a8843269ab8f18b9e0
Post-merge CI          31438898049 · success · 762 passed
Completion PR #91      final pre-Phase-0 main a8891793532a47ed682a0b713a587d08f16a23bc
Final main CI          31439211018 · success · 768 passed
```

`PASS_ATTRIBUTED` means only that no bounded Non-Projection blocker was found
for the exact admitted proposal. It is not truth, autobiography, identity,
relationship, retrieval, tool, action or deployment authority.

## 🛑 Explicit boundaries

```text
no privacy persistence or scanning
no deletion/redaction/quarantine/rebuild execution
no retrieval execution
no Action Gate or tool execution
no event/replay integration from P1 classifiers/composer/NPG
no belief, relationship, identity or M3 mutation
no P1-003 runtime activation or assignment
no Non-Projection runtime composition or activation
no P1-004 assignment
no backend selection or production deployment
```

P1-001, P1-002, P1-003 and NPG-v0.1 bounded Owner GO receipts are consumed. Any
new runtime-capable milestone needs a new bounded authority cycle, Tier A
evidence and green resulting-main CI.

## 🔗 Authoritative documents

- [System overview](SYSTEM_OVERVIEW.md)
- [AI entry point](docs/ai/README.md)
- [Machine-readable documentation map](docs/ai/project_manifest.json)
- [Current status](docs/CURRENT_STATUS.md)
- [Governance](docs/GOVERNANCE.md)
- [P1-001 receipt](docs/P1_001_IMPLEMENTATION_AUTHORIZATION.md)
- [P1-002 receipt](docs/P1_002_IMPLEMENTATION_AUTHORIZATION.md)
- [P1-003 authorization/completion receipt](docs/P1_003_IMPLEMENTATION_AUTHORIZATION.md)
- [P1-003 frozen contract](docs/research/P1_003_PURE_GOVERNED_CONSTRAINT_COMPOSER_CONTRACT.md)
- [NPG-v0.1 completion receipt](docs/NON_PROJECTION_IMPLEMENTATION_AUTHORIZATION.md)
- [NPG-v0.1 frozen contract](docs/research/NON_PROJECTION_PURE_CLASSIFIER_CONTRACT_V0_1.md)
- [Post-P0 roadmap](docs/research/POST_P0_ROADMAP_V0.1.md)
- [Research Index](docs/research/RESEARCH_INDEX.md)
- [Environment manifest](docs/ENVIRONMENT_MANIFEST.md)
