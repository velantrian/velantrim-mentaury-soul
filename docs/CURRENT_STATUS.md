# 🚦 Mentaury Soul — Current Status

```text
Status date:                       2026-08-09
Repository:                        velantrian/velantrim-mentaury-soul
Engineering authority:             this file + verified live GitHub state
Governance authority:              docs/GOVERNANCE.md + live GitHub ruleset
Current operating mode:            SOLO_MAINTAINER
Independent human review claimed:  NO
Live main tip:                      resolved from GitHub; not embedded here
```

This document records durable maturity and authorization facts. Mutable branch
tips, open-PR heads and workflow state are resolved from GitHub.

```text
IMPLEMENTED
= merged into GitHub main and retained by validation

IMPLEMENTED_BOUNDED
= the exact authorized subsystem slice is merged and retained by validation
≠ broader runtime authorization
≠ deployment authorization

AUTHORIZED_BOUNDED
= exact implementation scope approved but not yet implemented

FROZEN_DOCS
= accepted contract documentation
```

---

## 1. 🧭 Current checkpoint

```text
CANON_V0.1_FROZEN
P0-001…P0-015_IMPLEMENTED_IN_MAIN
P0_014_BELIEF_LIFECYCLE_VALIDATED
P0_015_EVIDENCE_GATE_VALIDATED
BELIEFS_EVIDENCE_IMPORT_ORDER_FIXED
PERMANENT_GITHUB_ACTIONS_PRESENT_AND_VALIDATED

SOLO_MAINTAINER_GOVERNANCE_ACTIVE
REQUIRED_APPROVALS_0_BY_EXPLICIT_SOLO_POLICY
INDEPENDENT_HUMAN_REVIEW_NOT_CLAIMED
TIER_A_TWO_PASS_MAINTAINER_REVIEW_REQUIRED

P1_001_CAPABILITY_LEASE_RESOLUTION_FROZEN_DOCS
P1_001_CAPABILITY_LEASE_RESOLUTION_IMPLEMENTED_BOUNDED
P1_001_PURE_RESOLVER_VALIDATED
P1_001_REGISTRY_PERSISTENCE_NOT_IMPLEMENTED
P1_001_REGISTRY_SERVICE_NOT_IMPLEMENTED
NO_POST_P1_001_RUNTIME_MILESTONE_AUTHORIZED

P1_002_PRIVACY_RECONCILIATION_CLASSIFIER_FROZEN_DOCS
P1_002_OWNER_GO_AUTHORIZED_BOUNDED
P1_002_IMPLEMENTATION_NOT_STARTED
P1_002_MUTATION_AUTHORITY_NONE
P1_002_RETRIEVAL_AUTHORITY_NONE
NO_POST_P1_002_RUNTIME_MILESTONE_AUTHORIZED

ACTION_GATE_NOT_AUTHORIZED
TOOL_EXECUTION_NOT_AUTHORIZED
DIRECT_OR_INDIRECT_M3_WRITE_FORBIDDEN
DOMAIN_RUNTIME_NOT_AUTHORIZED
RUNTIME_DEPLOYMENT_NOT_AUTHORIZED
```

---

## 2. 🔐 P1-001 completion evidence

```text
Authorization PR:       #62
Authorization merge:    d5e9e2fb11ea5a9c123c1cb1cc2b6f16dac53b98
Authorization main CI:  31322210843 · success
Implementation PR:      #63
Reviewed head:          e873e43331fa7273b92f896b371707e4779b17d4
Exact-head CI:          31323051934 · success · 387 passed
Implementation merge:   f21809d8f31a457bd7acfe1d766230973ba9ecf5
Post-merge CI:          31323138053 · success
Correctness pass:       PASS
Adversarial pass:       PASS
Independent assurance:  NOT CLAIMED
```

The accepted final P1-001 head recursively freezes every registry record after
an adversarial pass found nested mutability in the initial representation.

---

## 3. ✅ Implemented P1-001 slice

```text
src/mentaury/capabilities/__init__.py
src/mentaury/capabilities/lease/__init__.py
src/mentaury/capabilities/lease/contracts.py
src/mentaury/capabilities/lease/resolver.py
tests/test_capability_lease_resolution.py
```

The pure resolver performs strict registry admission, canonical digest
verification, exact live-head lookup, lifecycle/purpose/operation/scope/effect
checks and deterministic first-match denial. `ALLOW` executes nothing and
contains no reusable permission material.

---

## 4. 🔐 P1-002 authorization checkpoint

P1-002 contract freeze evidence:

```text
Contract PR:            #65
Reviewed head:          85bf0070e2f15b5ca752b82325337d6ef0190396
Exact-head CI:          31331396018 · success · 401 passed
Contract merge:         1dc7bcf97986f455f48beb121c2048dfc34bd11c
Post-merge CI:          31331506606 · success
```

A separate bounded Owner GO is recorded in:

- `docs/P1_002_IMPLEMENTATION_AUTHORIZATION.md`

Authorized implementation scope:

```text
src/mentaury/privacy/__init__.py
src/mentaury/privacy/reconciliation/__init__.py
src/mentaury/privacy/reconciliation/contracts.py
src/mentaury/privacy/reconciliation/classifier.py
tests/test_privacy_reconciliation_classifier.py
```

The future implementation may only classify caller-supplied records into:

```text
ALLOW_REFERENCE
DENY_RETRIEVAL
QUARANTINE_REQUIRED
REBUILD_REQUIRED
```

It may not perform deletion, redaction, quarantine, rebuilding, retrieval,
storage access, event append, network access, relationship/identity mutation or
M3 writes. `ALLOW_REFERENCE` remains classification data, not permission.

---

## 5. 🛡️ Governance state

The active ruleset requires PRs, exact required CI, up-to-date branches,
resolved conversations, deletion/force-push protection, empty bypass and
required approvals `0` during explicit solo operation.

Tier A work requires exact-head CI, complete diff inspection, distinct
correctness and adversarial passes, explicit maintainer decision and green
post-merge `main` CI. Issue #39 remains only the future transition trigger for a
genuine independent reviewer/team.

---

## 6. ✅ Milestone table

| Milestone | State | Verified boundary |
|---|---|---|
| P0-001…P0-013 | ✅ Implemented | integrity/storage/replay foundation |
| P0-014 | ✅ Implemented | belief status is not objective truth |
| P0-015 | ✅ Implemented | gate receipt is not external verification |
| P1-001 | ✅ Implemented bounded | pure capability classification only |
| P1-002 | 🔐 Authorized bounded | pure privacy classifier not yet implemented |

Implementation profile remains Python 3.13, standard-library SQLite for P0,
zero runtime dependencies and no import-time network/database/filesystem
mutation.

---

## 7. 🧱 Explicitly not implemented or authorized

```text
P1-002 implementation completion
privacy registry persistence
backup or fork inventory scanning
content inspection
content deletion or redaction execution
quarantine execution
index, embedding, graph, cache or summary rebuilding
retrieval execution
Capability Lease registry persistence or service
ambient clock/environment authority
Action Gate
Tool Receipt runtime
external tool execution
event append or replay/projection integration from P1 classifiers
belief, relationship or identity mutation
M3 identity writes
Character runtime
Identity Continuity runtime
Human Paths runtime
Controlled Origin ingestion runtime
Non-Projection runtime
backend selection or migration
production deployment readiness
objective-truth authority
consciousness or subjective-experience claims
```

---

## 8. ⛔ Next execution gate

```text
P1_002_OWNER_GO_AUTHORIZED_BOUNDED
P1_002_IMPLEMENTATION_NOT_STARTED
```

The next allowed action is one clean Tier A implementation PR confined to the
exact authorized source/test paths. Completion requires exact-head tests,
correctness/adversarial review, unchanged-head merge and green resulting-main
CI. No remediation execution or later runtime milestone follows automatically.

---

## 9. 🔬 Research boundary

```text
Research presence ≠ roadmap priority
Candidate captured ≠ candidate selected
External research input ≠ integration
Notion page ≠ implementation authority
```

No PostgreSQL, Graphiti, LadybugDB or other backend/profile is selected.

---

## 10. 🔗 Authoritative navigation

- Canon: `docs/MENTAURY_CANON_V0.1.md`
- Governance: `docs/GOVERNANCE.md`
- P1-001 receipt: `docs/P1_001_IMPLEMENTATION_AUTHORIZATION.md`
- P1-001 contract: `docs/research/MENTAURY_CAPABILITY_LEASE_RESOLUTION_NOTES.md`
- P1-002 authorization: `docs/P1_002_IMPLEMENTATION_AUTHORIZATION.md`
- P1-002 contract: `docs/research/P1_002_PRIVACY_RECONCILIATION_CLASSIFIER_NOTES.md`
- Roadmap: `docs/research/POST_P0_ROADMAP_V0.1.md`
- Research Index: `docs/research/RESEARCH_INDEX.md`

---

## 11. 🏁 Current formula

```text
P0-001…P0-015 implemented
+ permanent CI
+ active solo-main governance
+ P1-001 pure resolver implemented bounded
+ P1-002 contract frozen
+ P1-002 pure classifier implementation authorized bounded

≠ P1-002 implemented
≠ deletion, quarantine, rebuild or retrieval runtime
≠ Action Gate or tool execution
≠ identity or M3 mutation
≠ domain runtime or deployment authorization
≠ independent human assurance
```
