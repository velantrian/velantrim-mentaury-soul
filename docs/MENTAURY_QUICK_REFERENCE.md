# 📌 Mentaury Soul — Quick Reference

```text
Status:      NAVIGATION_ONLY · NONAUTHORITATIVE · DERIVED_DOCUMENT
Updated:     2026-08-09
Authority:   docs/CURRENT_STATUS.md + verified GitHub main
Governance:  SOLO_MAINTAINER · required approvals 0
Purpose:     compact map for people and connected agents
```

> This page summarizes current facts. It is not Canon, a runtime prompt, a
> personality memory or a source of authority.

---

## 1. 🧬 Definition

**Mentaury Soul** is a substrate-neutral research architecture for persistent,
governed digital individuality. `Soul` is an architectural-philosophical name,
not a claim of proven consciousness or subjective experience.

---

## 2. 🚦 Current status

```text
CANON_V0.1_FROZEN
P0-001…P0-015_IMPLEMENTED_IN_MAIN
BELIEFS_EVIDENCE_IMPORT_ORDER_FIXED
PERMANENT_GITHUB_ACTIONS_PRESENT_AND_VALIDATED

SOLO_MAINTAINER_GOVERNANCE_ACTIVE
TIER_A_TWO_PASS_MAINTAINER_REVIEW_REQUIRED
INDEPENDENT_HUMAN_REVIEW_NOT_CLAIMED

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

## 3. 🛡️ Solo governance

The active ruleset requires:

```text
pull request
+ required CI
+ branch up to date with main
+ resolved conversations
+ no force push
+ no main deletion
+ empty bypass list
```

Tier A procedure:

```text
exact head
→ complete diff
→ correctness pass
→ adversarial pass
→ green exact-head CI
→ resolved conversations
→ explicit maintainer decision
→ green post-merge main CI
```

Automated analysis is not independent human assurance. Issue #39 is the future
team-transition trigger, not a current blocker.

---

## 4. ✅ Implemented foundation

```text
P0-001 neutral skeleton
P0-002 envelope contracts
P0-003 canonical JSON v1
P0-004 immutable event and payload storage
P0-005 structural schema validation
P0-006 atomic multi-event batch
P0-007 event-aware idempotency
P0-008 transactional concurrency
P0-009 trusted commit + full R0
P0-010 atomic same-stream redaction
P0-011 adversarial integrity suite
P0-012 permanent GitHub Actions CI
P0-013 R1 deterministic replay
P0-014 minimal belief lifecycle
P0-015 deterministic Evidence Gate
```

Implementation profile:

```text
Python 3.13
standard-library SQLite
runtime dependencies: none
network/database at import: forbidden
```

---

## 5. 🔐 P1-001 current state

```text
Contract:       FROZEN_DOCS
Owner GO:       AUTHORIZED_BOUNDED
Implementation: NOT_STARTED
Completion:     NOT_CLAIMED
```

Authorized files:

```text
src/mentaury/capabilities/__init__.py
src/mentaury/capabilities/lease/__init__.py
src/mentaury/capabilities/lease/contracts.py
src/mentaury/capabilities/lease/resolver.py
tests/test_capability_lease_resolution.py
```

Required boundary:

```text
pure caller-supplied resolver
exact live-head lookup
strict registry and record admission
canonical digest recomputation
exact purpose / operation / typed scope / side effects
first-match deny precedence
ALLOW executes nothing
```

```text
AUTHORIZED_BOUNDED
≠ implementation complete
≠ registry service
≠ Action Gate
≠ tool execution
≠ M3 write
≠ domain runtime
```

---

## 6. 🔬 Research boundary

```text
research document ≠ runtime
candidate captured ≠ selected
external research input ≠ integration
Notion page ≠ implementation authority
```

No PostgreSQL, Graphiti, LadybugDB or other future profile is selected merely by
appearing in research notes.

---

## 7. 🚫 Not implemented or authorized

```text
P1-001 implementation completion
Capability Lease registry persistence/service
Action Gate / Tool Receipt runtime
external tool execution
identity / character / relationship runtime
Controlled Origin ingestion runtime
Human Paths runtime
Non-Projection runtime
M3 identity writes
production deployment readiness
objective truth authority
consciousness claims
```

---

## 8. 🔗 Essential files

- `docs/CURRENT_STATUS.md` — authoritative maturity and authorization status;
- `docs/GOVERNANCE.md` — risk tiers and merge policy;
- `docs/P1_001_IMPLEMENTATION_AUTHORIZATION.md` — exact bounded owner GO;
- `docs/research/MENTAURY_CAPABILITY_LEASE_RESOLUTION_NOTES.md` — frozen P1-001 contract;
- `docs/research/POST_P0_ROADMAP_V0.1.md` — execution ordering;
- `docs/research/RESEARCH_INDEX.md` — research navigation;
- `docs/ENVIRONMENT_MANIFEST.md` — implementation environment.

---

## 9. 🏁 Formula

```text
P0 foundation implemented
+ active solo governance
+ P1-001 contract frozen
+ bounded P1-001 owner GO

≠ P1-001 implementation complete
≠ domain runtime
≠ production ready
≠ independent assurance
```
