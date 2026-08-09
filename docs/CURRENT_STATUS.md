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

FROZEN_DOCS
= accepted contract documentation
≠ implementation by itself

AUTHORIZED_BOUNDED
= implementation may begin only inside the exact recorded scope
≠ completion
≠ runtime deployment

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

POST_P0_ROADMAP_ADOPTED_DOCS_ONLY
P1_001_CAPABILITY_LEASE_RESOLUTION_FROZEN_DOCS
P1_001_IMPLEMENTATION_AUTHORIZED_BOUNDED
P1_001_IMPLEMENTATION_NOT_STARTED
P1_001_COMPLETION_NOT_CLAIMED

DOMAIN_RUNTIME_NOT_AUTHORIZED
ACTION_GATE_NOT_AUTHORIZED
TOOL_EXECUTION_NOT_AUTHORIZED
DIRECT_OR_INDIRECT_M3_WRITE_FORBIDDEN
RUNTIME_NOT_VALIDATED
```

---

## 2. 🔐 P1-001 owner GO

The repository owner instructed the agent on 2026-08-09 to continue the
remaining work after the P1-001 contract freeze. This is the separate owner GO
required by the frozen roadmap.

The authoritative authorization receipt is:

- `docs/P1_001_IMPLEMENTATION_AUTHORIZATION.md`.

Authorized implementation is limited to a pure, deterministic, caller-supplied
Capability Lease resolver:

```text
src/mentaury/capabilities/__init__.py
src/mentaury/capabilities/lease/__init__.py
src/mentaury/capabilities/lease/contracts.py
src/mentaury/capabilities/lease/resolver.py
tests/test_capability_lease_resolution.py
```

Governance-only supporting edits are allowed where required to classify the new
path as Tier A and keep documentation/tests consistent.

Explicitly outside the GO:

```text
registry persistence or registry service
network lookup
ambient system clock or environment authority
Action Gate or Tool Receipt runtime
tool execution or external effects
event append or replay integration
belief, identity, relationship or M3 mutation
operator override inside resolve()
backend selection or migration
production deployment
```

The frozen contract remains an immutable freeze receipt. Its freeze-time marker
`Implementation in src/: NOT AUTHORIZED` records the state at PR #58 and does
not override this later owner authorization. Current authorization authority is
this file plus `docs/P1_001_IMPLEMENTATION_AUTHORIZATION.md`.

Completion requires a separate implementation PR with exact-head Tier A
correctness and adversarial review, deterministic/adversarial/metamorphic tests,
all conversations resolved, squash merge with unchanged reviewed head, and
green post-merge `main` CI.

---

## 3. 🛡️ Live governance model

The active `Mentaury main governance` ruleset protects `main`:

- pull request required;
- required check `Python 3.13 · validator · pytest · compileall`;
- branch must be up to date with `main`;
- review conversations must be resolved;
- force pushes blocked;
- branch deletion blocked;
- bypass list empty;
- required approvals `0` during explicit solo-maintainer operation.

Tier A work requires:

```text
exact final head
+ complete diff inspection
+ correctness pass
+ adversarial pass
+ green exact-head CI
+ resolved conversations
+ explicit maintainer decision
+ green post-merge main CI
```

Issue #39 remains only the future transition trigger for a genuine independent
reviewer/team. It does not block current solo work.

---

## 4. ✅ Implemented milestones

| Milestone | State | Verified boundary |
|---|---|---|
| P0-001 Neutral Skeleton | ✅ Implemented | package/project boundary only |
| P0-002 Envelope Contracts | ✅ Implemented | construction does not grant authority |
| P0-003 Canonical JSON v1 | ✅ Implemented | canonical bytes do not prove truth |
| P0-004 Event/Payload Storage | ✅ Implemented | persistence does not prove total integrity |
| P0-005 Structural Schema Validation | ✅ Implemented | schema validity does not prove semantics |
| P0-006 Atomic Multi-Event Batch | ✅ Implemented | atomicity is not idempotency or consensus |
| P0-007 Event-Aware Idempotency | ✅ Implemented | receipt is not integrity proof |
| P0-008 Transactional Concurrency | ✅ Implemented | SQLite locking is not distributed consensus |
| P0-009 Trusted Commit + Full R0 | ✅ Implemented | R0 consistency is not truth |
| P0-010 Atomic Same-Stream Redaction | ✅ Implemented | payload removal preserves event provenance |
| P0-011 Adversarial Integrity Suite | ✅ Implemented | tested attack families are not exhaustive proof |
| P0-012 Permanent GitHub Actions CI | ✅ Implemented | green CI is not production readiness |
| P0-013 R1 Deterministic Replay | ✅ Implemented | replay equivalence is not epistemic truth |
| P0-014 Minimal Belief Lifecycle | ✅ Implemented | belief status is not objective truth |
| P0-015 Deterministic Evidence Gate | ✅ Implemented | gate receipt is not external verification |

Implementation profile remains:

```text
Python 3.13
standard-library SQLite
runtime dependencies: none
network at import: forbidden
database at import: forbidden
```

---

## 5. 🔐 P1-001 contract and implementation state

Owning frozen contract:

- `docs/research/MENTAURY_CAPABILITY_LEASE_RESOLUTION_NOTES.md`.

Ordering:

- `docs/research/POST_P0_ROADMAP_V0.1.md`.

Authorization:

- `docs/P1_001_IMPLEMENTATION_AUTHORIZATION.md`.

```text
Contract:       FROZEN_DOCS
Implementation: AUTHORIZED_BOUNDED · NOT_STARTED
Completion:     NOT_CLAIMED
```

The planned resolver must preserve:

```text
AuthorityRef = (capability_lease_id, capability_revision)
explicit caller-supplied RegistrySnapshot
exact live-head lookup; no history walk
registry and record admission before authorization
digest recomputation excluding content_digest
caller-supplied evaluated_at and budgets
exact purpose, operation, typed scope and side-effect checks
fork/restore quarantine as UNVERIFIED
ALLOW executes nothing
```

No implementation status may become `Implemented` until the code PR and its
resulting `main` SHA both pass retained CI.

---

## 6. 🧱 Explicitly not implemented or authorized

```text
P1-001 implementation completion
Capability Lease registry persistence or service
Action Gate
Tool Receipt runtime
external tool execution
M3 identity writes
Character runtime
Identity Continuity runtime
Human Paths runtime
Controlled Origin ingestion runtime
Non-Projection runtime
bounded self-development runtime
LLM-dependent domain runtime
production deployment readiness
objective-truth authority
consciousness or subjective-experience claims
```

---

## 7. 🔬 Research boundary

Research documents may capture hypotheses and candidates but provide no runtime
authority.

```text
Research presence ≠ roadmap priority
Candidate captured ≠ candidate selected
External research input ≠ integration
Notion page ≠ implementation authority
```

No PostgreSQL, Graphiti, LadybugDB or other future backend/profile is selected by
research presence alone.

---

## 8. 🧹 Completed cleanup

```text
PR #38 → closed without merge; superseded by merged PR #58
PR #48 → closed without merge; superseded by merged PR #60
PR #55 → closed without merge; historical ruleset probe
Issue #47 → import-order and contradiction-path remediation completed
Issues #42 / #52 / #53 → solo post-hoc reviews completed
Issue #49 → status-authority B+C+D decision adopted
Issue #39 → future public/team transition gate only
```

Three obsolete remote branches remain cosmetic cleanup only because the current
connector exposes no delete-ref operation and local `gh` is unavailable. They
do not affect `main`, PR state or authorization.

---

## 9. 🔗 Authoritative navigation

- Canon: `docs/MENTAURY_CANON_V0.1.md`
- Governance: `docs/GOVERNANCE.md`
- Solo mode: `docs/governance/solo-maintainer-mode.md`
- Tier A checklist: `docs/governance/solo-maintainer-review-checklist.md`
- Environment: `docs/ENVIRONMENT_MANIFEST.md`
- P1 authorization: `docs/P1_001_IMPLEMENTATION_AUTHORIZATION.md`
- P1 contract: `docs/research/MENTAURY_CAPABILITY_LEASE_RESOLUTION_NOTES.md`
- Roadmap: `docs/research/POST_P0_ROADMAP_V0.1.md`
- Research Index: `docs/research/RESEARCH_INDEX.md`

---

## 10. 🏁 Current formula

```text
P0-001…P0-015 implemented
+ import-order defect fixed
+ permanent CI
+ active solo-main ruleset
+ P1-001 contract frozen
+ bounded P1-001 implementation authorized

≠ P1-001 implementation completed
≠ Action Gate or tool execution authorized
≠ domain runtime authorized
≠ production ready
≠ independent human assurance
```
