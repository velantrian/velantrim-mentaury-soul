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
Production deployment:       not authorized
```

## Implemented bounded source surfaces

```text
src/mentaury/capabilities/lease/
src/mentaury/privacy/reconciliation/
src/mentaury/composition/governed_constraints/
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

## Explicitly absent

```text
privacy registry or copy inventory service
backup/fork scanning
content inspection
deletion/redaction/quarantine/rebuild execution
retrieval execution
network, filesystem or database authority in P1 bounded gates/composer
event/replay integration from P1 gates/composer
relationship, identity or M3 mutation
Action Gate or tool runtime
P1-003 runtime assignment or activation
backend/plugin discovery
backend migration or production deployment
```

## Governance

The repository operates in explicit solo-maintainer mode. Tier A work requires
exact-head CI, correctness and adversarial passes, resolved conversations,
explicit acceptance and green post-merge `main` CI. Independent human assurance
is not claimed.
