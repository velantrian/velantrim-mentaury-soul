# ⚙️ Mentaury Environment Manifest

```text
P0-001…P0-015_IMPLEMENTED_IN_MAIN
P1-001…P1-001_IMPLEMENTED_IN_MAIN
P1-002…P1-002_IMPLEMENTED_IN_MAIN
P1-003…P1-003_IMPLEMENTED_IN_MAIN
```

## Runtime profile

```text
Language:                    Python 3.13
Runtime dependencies:        none
P0 storage profile:          standard-library SQLite
Permanent CI:                GitHub Actions
Required check:              Python 3.13 · validator · pytest · compileall
Import-time external I/O:    forbidden
P1-003 runtime assignment:   NOT_ASSIGNED
Non-Projection runtime:      NOT_AUTHORIZED
P1-004:                      NOT_ASSIGNED
Production deployment:       not authorized
```

## Implemented bounded source surfaces

```text
src/mentaury/capabilities/lease/
src/mentaury/privacy/reconciliation/
src/mentaury/composition/governed_constraints/
src/mentaury/non_projection/
```

### Capability Lease resolver

```text
src/mentaury/capabilities/__init__.py
src/mentaury/capabilities/lease/__init__.py
src/mentaury/capabilities/lease/contracts.py
src/mentaury/capabilities/lease/resolver.py
tests/test_capability_lease_resolution.py
```

Pure caller-supplied classification only. No registry persistence, network
lookup, execution, event append, identity/M3 mutation or deployment authority.

```text
NO_POST_P1_001_RUNTIME_MILESTONE_AUTHORIZED
```

### Privacy Reconciliation Classifier

```text
Inputs:
- PrivacyMaterial
- PrivacyCopy
- PrivacyAccessIntent
- PrivacyReconciliationBudget

Output:
- PrivacyReconciliationResult(decision, reason)
```

The classifier is deterministic and fail closed. It performs no deletion,
redaction, quarantine, rebuilding or retrieval.

### P1-003 Pure Governed Constraint Composer

Exact bounded source:

```text
src/mentaury/composition/__init__.py
src/mentaury/composition/governed_constraints/__init__.py
src/mentaury/composition/governed_constraints/contracts.py
src/mentaury/composition/governed_constraints/composer.py
```

Exact public API:

```python
def compose_governed_constraints(
    *,
    context: CrossGateEvaluationContext,
) -> GovernedConstraintResult:
    ...
```

The composer is deterministic and explicit-input only. It derives the existing
P1-001 and P1-002 intents, evaluates both bounded gates in one call and computes
canonical targeted fingerprints. It performs no retrieval, tool execution,
persistence, network/filesystem/database authority, runtime activation or
deployment.

## P1-003 verification

```text
Owner GO PR:             #77
Receipt reconcile PR:    #78
Implementation PR:       #79
Reviewed implementation: 9855f766f2bf801c8297c4f870b21d3ed37911fb
Exact-head CI:           31394829487 · success · 552 passed
Merge/main:              59f2caa4deacd06aee0bbfc8dae1221edcb666eb
Post-merge CI:           31395291622 · success · 552 passed
Tier A review:           4897445251
Correctness:             PASS
Adversarial:             PASS
Authorization boundary:  PRESERVED
```

Validation includes:

```text
CGC-CTX-001…014
CGC-FP-001…010
CGC-DEC-001…014
CGC-T-001…012
CGC-M-001…010
CGC-PURE-001…008
```

```text
P1_003_OWNER_GO = CONSUMED
P1_003_IMPLEMENTATION = IMPLEMENTED_BOUNDED
P1_003_RUNTIME_ASSIGNMENT = NOT_ASSIGNED
NO_POST_P1_003_RUNTIME_MILESTONE_AUTHORIZED
```

### NPG-v0.1 Pure Non-Projection Classifier

Exact bounded source:

```text
src/mentaury/non_projection/__init__.py
src/mentaury/non_projection/contracts.py
src/mentaury/non_projection/classifier.py
```

Exact public API:

```python
def classify_non_projection(
    *,
    envelope: AttributedInterpretationEnvelope,
    budget: NonProjectionBudget,
) -> NonProjectionResult:
    ...
```

The classifier is deterministic and explicit-input only. It has no network,
filesystem, database, vector/graph store, Atlas retrieval, model/LLM, identity or
relationship registry, ambient clock/environment, tool/subprocess/plugin, M3,
Action Gate or deployment authority.

## NPG-v0.1 verification

```text
Contract:                 FROZEN_DOCS · NPG-v0.1
Envelope:                 AIE-v0.1
Owner GO:                 CONSUMED_BY_PR_90
Implementation PR:        #90
Reviewed implementation:  a61427f85c70531b329894d5dc310e43bcc9d7de
Exact-head CI:            31438692348 · success · 762 passed
Merge/main:               cfb59fb7a49166d55360c6a8843269ab8f18b9e0
Post-merge CI:            31438898049 · success · 762 passed
Completion PR:            #91
Pre-Phase-0 main:         a8891793532a47ed682a0b713a587d08f16a23bc
Pre-Phase-0 main CI:      31439211018 · success · 768 passed
Implementation:           IMPLEMENTED_BOUNDED
Runtime:                  NOT_AUTHORIZED
P1-004:                   NOT_ASSIGNED
```

`PASS_ATTRIBUTED` remains bounded classification data and grants no truth,
autobiography, identity, relationship, consent, retrieval, tool, Action Gate or
deployment authority.

## Explicitly absent

```text
privacy registry or copy inventory service
backup/fork scanning
content inspection
deletion/redaction/quarantine/rebuild execution
retrieval execution
network, filesystem or database authority in P1 bounded gates/composer/NPG
event/replay integration from P1 gates/composer/NPG
relationship, identity or M3 mutation
Action Gate or tool runtime
P1-003 runtime assignment or activation
Non-Projection runtime composition or activation
P1-004 assignment
backend/plugin discovery
backend migration or production deployment
```

## Governance

The repository operates in explicit solo-maintainer mode. Tier A work requires
exact-head CI, correctness and adversarial passes, resolved conversations,
explicit acceptance and green post-merge `main` CI. Independent human assurance
is not claimed.
