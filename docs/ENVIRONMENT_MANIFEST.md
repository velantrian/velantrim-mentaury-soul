# ⚙️ Mentaury Environment Manifest

```text
P0-001…P0-015_IMPLEMENTED_IN_MAIN
P1-001…P1-001_IMPLEMENTED_IN_MAIN
P1-002…P1-002_IMPLEMENTED_IN_MAIN
```

## Runtime profile

```text
Language:                    Python 3.13
Runtime dependencies:        none
P0 storage profile:          standard-library SQLite
Permanent CI:                GitHub Actions
Required check:              Python 3.13 · validator · pytest · compileall
Import-time external I/O:    forbidden
Production deployment:       not authorized
```

## Implemented bounded source surfaces

```text
src/mentaury/capabilities/lease/
src/mentaury/privacy/reconciliation/
```

### Capability Lease resolver

Pure caller-supplied classification only. No registry persistence, network
lookup, execution, event append, identity/M3 mutation or deployment authority.

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

## P1-002 verification

```text
Contract PR:             #65
Authorization PR:        #66
Implementation PR:       #67
Reviewed implementation: 74662fb626a545ed63b426e98aa03524449019db
Exact-head CI:           31332728486 · success · 461 passed
Merge/main:              d64679fd745e859527a70746df5e69dc9aca0408
Post-merge CI:           31332793742 · success · 461 passed
```

Validation covers all frozen `PRIV-SC-001…PRIV-SC-015` scenarios, exact
precedence, typed/mapping equivalence, deterministic repeatability, canonical
budgets, empty-allowlist denial, impossible-result rejection and fresh-process
imports with ambient I/O/clock access blocked.

## Explicitly absent

```text
privacy registry or copy inventory service
backup/fork scanning
content inspection
deletion/redaction/quarantine/rebuild execution
retrieval execution
network, filesystem or database authority in P1-002
event/replay integration from P1 classifiers
relationship, identity or M3 mutation
Action Gate or tool runtime
backend migration or production deployment
```

## Governance

The repository operates in explicit solo-maintainer mode. Tier A work requires
exact-head CI, correctness and adversarial passes, resolved conversations,
explicit acceptance and green post-merge `main` CI. Independent human assurance
is not claimed.
