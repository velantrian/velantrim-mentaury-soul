# 🧬 Mentaury Soul

A substrate-neutral research architecture for persistent digital individuality,
memory, identity continuity, character and governed self-development.

```text
P0-001…P0-015_IMPLEMENTED_IN_MAIN
P1-001…P1-001_IMPLEMENTED_IN_MAIN
P1-002…P1-002_IMPLEMENTED_IN_MAIN
```

## 🚦 Current engineering checkpoint

```text
Canon v0.1                         FROZEN
P0 foundation                      IMPLEMENTED
P1-001 Capability Lease resolver   IMPLEMENTED_BOUNDED
P1-002 Privacy classifier          IMPLEMENTED_BOUNDED
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

Adversarial review fixed implicit empty-allowlist wildcard authority, impossible
result pairs, raw canonical-JSON exception leakage, nondeterministic budget
validation order and incomplete byte-budget accounting.

## 🛑 Explicit boundaries

```text
no privacy persistence or scanning
no deletion/redaction/quarantine/rebuild execution
no retrieval execution
no Action Gate or tool execution
no event/replay integration from P1 classifiers
no belief, relationship, identity or M3 mutation
no backend selection or production deployment
```

Both P1 Owner GO receipts are consumed. Any new runtime-capable milestone needs
a new bounded contract, threat model, explicit Owner GO, Tier A PR and green
resulting-main CI.

## 🔗 Authoritative documents

- [Current status](docs/CURRENT_STATUS.md)
- [Governance](docs/GOVERNANCE.md)
- [P1-001 receipt](docs/P1_001_IMPLEMENTATION_AUTHORIZATION.md)
- [P1-002 receipt](docs/P1_002_IMPLEMENTATION_AUTHORIZATION.md)
- [P1-002 frozen contract](docs/research/P1_002_PRIVACY_RECONCILIATION_CLASSIFIER_NOTES.md)
- [Post-P0 roadmap](docs/research/POST_P0_ROADMAP_V0.1.md)
- [Research Index](docs/research/RESEARCH_INDEX.md)
- [Environment manifest](docs/ENVIRONMENT_MANIFEST.md)
