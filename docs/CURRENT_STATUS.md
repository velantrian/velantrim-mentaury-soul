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
tips, open-PR heads and current workflow state must be read from GitHub rather
than copied into long-lived maturity text.

```text
IMPLEMENTED
= merged into GitHub main and retained by validation

FROZEN_DOCS
= accepted contract documentation
≠ implementation authorization

OPEN PR
≠ implemented

Notion / README / Quick Reference
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
P1_001_CAPABILITY_LEASE_RESOLUTION_DOCS_ONLY_NOT_IMPLEMENTED
P1_001_CAPABILITY_LEASE_RESOLUTION_FROZEN_DOCS
CAPABILITY_LEASE_RESOLVER_NOT_AUTHORIZED

DOMAIN_RUNTIME_NOT_AUTHORIZED
ACTION_GATE_NOT_AUTHORIZED
TOOL_EXECUTION_NOT_AUTHORIZED
DIRECT_OR_INDIRECT_M3_WRITE_FORBIDDEN
RUNTIME_NOT_VALIDATED
```

Accepted governance and contract evidence:

```text
PR #56 → solo-maintainer mode documented
PR #57 → governance, CODEOWNERS and tests reconciled with solo mode
PR #58 → P1-001 contract hardened and accepted under Tier A review
PR #59 → authoritative and derived status synchronized
```

Verified P1-001 docs evidence:

```text
Reviewed head:   a32b0e4fe55382f76a70b2205104af2e28f99451
Exact-head CI:   31317003807 · success
Merge commit:    8e89063fd74f5ae6d337366c299fa5f4e0164618
Post-merge CI:   31317057193 · success
Review mode:     SOLO_MAINTAINER · correctness + adversarial passes
Independent assurance: NOT CLAIMED
```

Verified beliefs/evidence remediation evidence:

```text
Issue:           #47 · completed
Successor PR:    #60
Reviewed head:   7afe7e1bdd47913732f6e3d1e8b479c46e95b06e
Exact-head CI:   31317635719 · success · 326 passed
Merge commit:    102fac1f8778e056d29ece3f1f76d92d4cf264f2
Post-merge CI:   31317696013 · success
Legacy PR #48:   closed without merge · superseded
Review mode:     SOLO_MAINTAINER · correctness + adversarial passes
Independent assurance: NOT CLAIMED
```

---

## 2. 🛡️ Live governance model

The active `Mentaury main governance` ruleset protects `main`:

- pull request required;
- required check `Python 3.13 · validator · pytest · compileall`;
- branch must be up to date with `main`;
- review conversations must be resolved;
- force pushes blocked;
- branch deletion blocked;
- bypass list empty;
- required approvals set to `0` during the explicit solo-maintainer phase.

Risk-sensitive changes use the Tier A procedure in `docs/GOVERNANCE.md`:

```text
exact final head
+ exact-head CI
+ complete diff inspection
+ correctness pass
+ adversarial pass
+ resolved conversations
+ explicit maintainer decision
+ post-merge main CI
```

Automated agents may support review but do not constitute independent human
approval. Issue #39 is a future transition trigger: when a genuine independent
reviewer or team exists, approvals and stale/latest-push review gates must be
restored and verified.

---

## 3. ✅ Implemented milestones

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

The implementation profile remains:

```text
Python 3.13
standard-library SQLite
runtime dependencies: none
network at import: forbidden
database at import: forbidden
```

### P0-014 / P0-015 maintenance state

PR #60 removed the confirmed import-order dependency between
`mentaury.beliefs` and `mentaury.evidence` by introducing dependency-light
shared epistemic leaf types.

```text
ClaimType / EvidenceSide → one shared type identity
beliefs ↔ evidence import order → fresh-interpreter validated
mutable contradiction result → deterministic CONTESTED
forged CONTRADICTED result → reducer rejection
qualifying evidence on both sides → unchanged fail-closed CONFLICT semantics
```

The remediation changes no status enum, policy threshold, event schema, storage
format or replay profile.

---

## 4. 🔐 P1-001 Capability Lease Resolution

Owning documents:

- `docs/research/MENTAURY_CAPABILITY_LEASE_RESOLUTION_NOTES.md`;
- `docs/research/POST_P0_ROADMAP_V0.1.md`;
- `docs/research/RESEARCH_INDEX.md`.

Accepted docs boundary:

```text
Status: FROZEN_DOCS · DOCS_ONLY · NOT_IMPLEMENTED
AuthorityRef remains: (capability_lease_id, capability_revision)
RegistrySnapshot: explicit caller-supplied input
Lookup: exact live head; no history walk
Admission: registry and record contracts fail closed
Digest: canonical recomputation excluding content_digest
Lifecycle: explicit revoked / expired / active ordering
Matching: exact purpose, operation and typed scope
Budgets: explicit and fail closed
Fork / restore: inherited grants quarantined as UNVERIFIED
ALLOW: executes nothing
```

PR #58 corrected two contract ambiguities before acceptance:

1. malformed registry structure returns `REGISTRY_CONTRACT_VIOLATION`;
2. premature materialized `EXPIRED` returns `LEASE_CONTRACT_VIOLATION`, while
   ACTIVE at/after expiry returns `LEASE_EXPIRED`.

### Implementation gate

No registry or resolver code is authorized. A future implementation requires:

```text
FROZEN_DOCS on main
+ separate explicit owner GO in this status document
+ bounded pure implementation scope
+ new Tier A review on exact head
+ deterministic / adversarial / metamorphic tests
+ preserved P0 replay compatibility
+ no Action Gate, tools, M3 or domain-runtime expansion
```

---

## 5. 🔬 Research boundary

Active research documents may capture hypotheses and candidates but provide no
runtime authority.

```text
Research presence ≠ roadmap priority
Candidate captured ≠ candidate selected
External research input ≠ integration
Notion page ≠ implementation authority
```

Current retained tracks include:

- identity continuity and relational architecture;
- Genesis Heritage / Human Atlas;
- contextual cognition and epistemic context;
- character and presence;
- Native Kernel external research input;
- storage and graph profile candidates;
- biological, cybernetic and cognitive candidates.

No PostgreSQL, Graphiti, LadybugDB or other future backend/profile is selected by
research presence alone.

---

## 6. 🧱 Explicitly not implemented or authorized

```text
Capability Lease registry / resolver runtime
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

## 7. 🧹 Completed governance and maintenance cleanup

```text
PR #38 → closed without merge; superseded by merged PR #58
PR #48 → closed without merge; superseded by merged PR #60
PR #55 → closed without merge; historical ruleset probe
Issue #47 → import-order and contradiction-path remediation completed
Issue #42 → solo security post-hoc review completed
Issue #52 → solo validator post-hoc review completed
Issue #53 → solo storage-integrity post-hoc review completed
Issue #39 → open only as future public/team transition gate
```

There is no remaining reviewer-identity blocker in the current solo phase.
Future work is evaluated by actual technical scope, exact-head evidence and the
current authorization boundaries.

---

## 8. 🔗 Authoritative navigation

- Canon: `docs/MENTAURY_CANON_V0.1.md`
- Governance: `docs/GOVERNANCE.md`
- Solo mode: `docs/governance/solo-maintainer-mode.md`
- Tier A checklist: `docs/governance/solo-maintainer-review-checklist.md`
- Environment: `docs/ENVIRONMENT_MANIFEST.md`
- Quick Reference: `docs/MENTAURY_QUICK_REFERENCE.md`
- Project history: `docs/PROJECT_HISTORY.md`
- Research Index: `docs/research/RESEARCH_INDEX.md`
- P1-001 contract: `docs/research/MENTAURY_CAPABILITY_LEASE_RESOLUTION_NOTES.md`

---

## 9. 🏁 Current formula

```text
P0-001…P0-015 implemented
+ import-order defect fixed
+ permanent CI
+ active solo-main ruleset
+ honest two-pass Tier A review
+ P1-001 docs frozen

≠ P1-001 runtime implemented
≠ domain runtime authorized
≠ production ready
≠ independent human assurance
```
