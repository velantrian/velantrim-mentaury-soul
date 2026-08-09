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

FROZEN_DOCS
= accepted contract documentation

README / Quick Reference / Notion
= derived navigation surfaces
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

P1_002_PRIVACY_RECONCILIATION_CLASSIFIER_SELECTED
P1_002_PRIVACY_RECONCILIATION_CLASSIFIER_FROZEN_DOCS
P1_002_IMPLEMENTATION_NOT_AUTHORIZED
P1_002_STORAGE_OR_DELETION_AUTHORITY_NONE

ACTION_GATE_NOT_AUTHORIZED
TOOL_EXECUTION_NOT_AUTHORIZED
DIRECT_OR_INDIRECT_M3_WRITE_FORBIDDEN
DOMAIN_RUNTIME_NOT_AUTHORIZED
RUNTIME_DEPLOYMENT_NOT_AUTHORIZED
```

---

## 2. 🔐 P1-001 completion evidence

### Authorization checkpoint

```text
Authorization PR:       #62
Reviewed head:          53b3eec436d4dbfd2c13050a9966fb84ef0b7b3a
Exact-head CI:          31322108100 · success · 327 passed
Authorization merge:    d5e9e2fb11ea5a9c123c1cb1cc2b6f16dac53b98
Post-merge CI:          31322210843 · success
```

### Implementation checkpoint

```text
Implementation PR:      #63
Reviewed head:          e873e43331fa7273b92f896b371707e4779b17d4
Exact-head CI:          31323051934 · success · 387 passed
Implementation merge:   f21809d8f31a457bd7acfe1d766230973ba9ecf5
Post-merge CI:          31323138053 · success
Review mode:            SOLO_MAINTAINER · TIER_A
Correctness pass:       PASS
Adversarial pass:       PASS
Review threads:         0
Independent assurance:  NOT CLAIMED
```

The adversarial pass found and fixed one material pre-merge weakness: registry
records were detached from caller input, but nested values could still be
mutated through the stored mapping view. The accepted final head recursively
freezes every stored record and includes a regression for nested mappings and
sequences.

---

## 3. ✅ Implemented P1-001 slice

```text
src/mentaury/capabilities/__init__.py
src/mentaury/capabilities/lease/__init__.py
src/mentaury/capabilities/lease/contracts.py
src/mentaury/capabilities/lease/resolver.py
tests/test_capability_lease_resolution.py
```

Implemented behavior:

- immutable typed lease, intent, snapshot, budget and result contracts;
- caller-supplied `RegistrySnapshot`, P0 `AuthorityRef`, `ActionIntent`,
  canonical UTC-Z `evaluated_at` and `ResolutionBudget`;
- exact admitted live-head lookup with no history walk or fallback;
- strict registry and selected-record admission;
- canonical SHA-256 digest recomputation excluding only `content_digest`;
- supersession, time, revocation, audit, delegation, branch-transfer,
  identity-authority and direct-M3 invariants;
- exact purpose and operation matching;
- typed scope containment and explicit side-effect containment;
- deterministic first-match denial;
- fork/restore quarantine through `UNVERIFIED`;
- minimal `ResolutionResult` without reusable permission material;
- `ALLOW` is classification data and executes nothing.

Validation includes all frozen `CAP-SC-001…CAP-SC-025` scenarios, strict and
adversarial admission, precedence checks, deterministic and metamorphic checks,
typed/mapping equivalence, recursive snapshot immutability, unchanged P0
`AuthorityRef`, and fresh-process import with ambient I/O and clock calls
blocked.

---

## 4. 🧊 Selected P1-002 contract

The next selected contract is:

```text
P1-002 Privacy Reconciliation Classifier
Status: FROZEN_DOCS · DOCS_ONLY · NOT_IMPLEMENTED
Implementation authorization: NOT GRANTED
```

Owning contract:

- `docs/research/P1_002_PRIVACY_RECONCILIATION_CLASSIFIER_NOTES.md`

The bounded problem is the gap between one active-store P0 redaction and stale
copies that may still exist in backups, forks, indexes, embeddings, graph edges,
caches or derived summaries.

The frozen contract permits a future pure caller-supplied classifier with only
these possible dispositions:

```text
ALLOW_REFERENCE
DENY_RETRIEVAL
QUARANTINE_REQUIRED
REBUILD_REQUIRED
```

It does not authorize deletion, redaction, quarantine execution, rebuilding,
retrieval, storage access, event append, network access, relationship changes,
identity changes or M3 writes. `ALLOW_REFERENCE` remains classification data,
not retrieval permission.

---

## 5. 🛡️ Governance state

The active ruleset requires:

- pull request before merge;
- required check `Python 3.13 · validator · pytest · compileall`;
- branch up to date with `main`;
- resolved review conversations;
- force-push and deletion protection;
- empty bypass list;
- required approvals `0` during explicit solo-maintainer operation.

Tier A work requires exact-head CI, complete diff inspection, distinct
correctness and adversarial passes, resolved conversations, explicit maintainer
decision and green post-merge `main` CI.

Issue #39 remains only the future transition trigger for a genuine independent
reviewer/team. It does not block current solo maintenance.

---

## 6. ✅ Implemented milestones

| Milestone | State | Verified boundary |
|---|---|---|
| P0-001…P0-013 | ✅ Implemented | integrity/storage/replay foundation |
| P0-014 | ✅ Implemented | belief status is not objective truth |
| P0-015 | ✅ Implemented | gate receipt is not external verification |
| P1-001 | ✅ Implemented bounded | pure resolution only; no execution authority |
| P1-002 | 🧊 Frozen docs | privacy classification contract only; no code authority |

Implementation profile remains:

```text
Python 3.13
standard-library SQLite for the P0 storage profile
runtime dependencies: none
network/database/filesystem mutation at import: forbidden
```

---

## 7. 🧱 Explicitly not implemented or authorized

```text
P1-002 Privacy Reconciliation Classifier implementation
privacy registry persistence
backup or fork inventory scanning
content inspection
content deletion or redaction execution
quarantine execution
index, embedding, graph, cache or summary rebuilding
retrieval execution
Capability Lease registry persistence
Capability Lease registry service or network lookup
ambient clock/environment authority
Action Gate
Tool Receipt runtime
external tool execution
P1 resolver integration with event append, replay or projections
belief, identity or relationship mutation from classification
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

The P1-001 authorization is consumed by its completed bounded slice. The new
P1-002 frozen contract does not itself grant implementation authority.

---

## 8. ⛔ Next execution gate

```text
P1_002_CONTRACT_FROZEN_DOCS
P1_002_IMPLEMENTATION_NOT_AUTHORIZED
```

Maintenance, bug remediation, tests and research capture may continue under
current governance. P1-002 implementation requires:

```text
separate bounded owner GO
+ dedicated authorization receipt
+ clean implementation PR
+ exact-head Tier A correctness review
+ exact-head Tier A adversarial review
+ green post-merge main CI
```

No later privacy runtime, Action Gate, tool execution, identity/M3 runtime or
deployment follows automatically from P1-002 selection.

---

## 9. 🔬 Research boundary

```text
Research presence ≠ roadmap priority
Candidate captured ≠ candidate selected
External research input ≠ integration
Notion page ≠ implementation authority
```

No PostgreSQL, Graphiti, LadybugDB or other future backend/profile is selected by
research presence alone.

---

## 10. 🔗 Authoritative navigation

- Canon: `docs/MENTAURY_CANON_V0.1.md`
- Governance: `docs/GOVERNANCE.md`
- P1-001 authorization/completion receipt: `docs/P1_001_IMPLEMENTATION_AUTHORIZATION.md`
- P1-001 frozen contract: `docs/research/MENTAURY_CAPABILITY_LEASE_RESOLUTION_NOTES.md`
- P1-002 frozen contract: `docs/research/P1_002_PRIVACY_RECONCILIATION_CLASSIFIER_NOTES.md`
- Roadmap: `docs/research/POST_P0_ROADMAP_V0.1.md`
- Research Index: `docs/research/RESEARCH_INDEX.md`
- Environment: `docs/ENVIRONMENT_MANIFEST.md`

---

## 11. 🏁 Current formula

```text
P0-001…P0-015 implemented
+ permanent CI
+ active solo-main governance
+ P1-001 bounded pure resolver implemented and validated
+ P1-002 privacy classifier contract frozen

≠ P1-002 implementation authorization
≠ privacy deletion, quarantine, rebuild or retrieval runtime
≠ registry service
≠ Action Gate or tool execution
≠ identity or M3 mutation
≠ domain runtime
≠ deployment authorization
≠ independent human assurance
```
