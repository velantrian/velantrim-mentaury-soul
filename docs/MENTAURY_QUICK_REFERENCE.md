# 📌 Mentaury Soul — Quick Reference

```text
Status:      NAVIGATION_ONLY · NON_AUTHORITATIVE · DERIVED_DOCUMENT
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
governed digital individuality.

It studies continuity through origin/provenance, event history, memory and
beliefs, relationships and commitments, a governed Self–World model, character
as presentation, and explainable change.

`Soul` is an architectural-philosophical name. It is not a claim of proven
consciousness or subjective experience.

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

Latest accepted maintenance evidence:

```text
PR #60 exact-head CI: 31317635719 · success · 326 passed
PR #60 merge:         102fac1f8778e056d29ece3f1f76d92d4cf264f2
Post-merge CI:        31317696013 · success
Review:               solo Tier A correctness + adversarial passes
Independent review:   not claimed
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

`required approvals = 0` because there is no genuine independent reviewer in
the current solo phase.

For Tier A changes:

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

Automated analysis supports the review but is not independent human assurance.
Issue #39 tracks the future transition when a real reviewer/team exists.

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

### Beliefs/evidence maintenance

PR #60:

- moved shared `ClaimType` / `EvidenceSide` to a dependency-light leaf module;
- preserved one public enum identity;
- removed the package import cycle;
- added fresh-interpreter order tests;
- made contradiction registration deterministically produce `CONTESTED` from
  mutable states;
- made forged contradiction outcomes fail reducer validation;
- retained P0-015 conflict thresholds and semantics.

---

## 5. 🔐 P1-001 contract

```text
Status: FROZEN_DOCS · DOCS_ONLY · NOT_IMPLEMENTED
```

The accepted contract defines explicit registry input, separate fail-closed
registry and lease admission, exact live-head lookup, canonical digest
recomputation, explicit time/budgets, exact purpose/operation/typed-scope
matching, fork quarantine and an `ALLOW` that executes nothing.

```text
FROZEN_DOCS
≠ resolver implemented
≠ owner GO for src/
≠ Action Gate
≠ M3 write
≠ domain runtime
```

---

## 6. 🔬 Research boundary

Research includes identity continuity, Genesis Heritage, Human Atlas,
contextual cognition, character/presence, storage/graph candidates and
biological/cybernetic candidates.

```text
research document ≠ runtime
candidate captured ≠ selected
external research input ≠ integration
Notion page ≠ implementation authority
```

No PostgreSQL, Graphiti, LadybugDB or other future profile is selected merely by
appearing in research notes.

---

## 7. 🚫 Not implemented

```text
Capability Lease registry / resolver
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

## 8. 🧹 Completed cleanup

```text
PR #38 → closed, superseded by PR #58
PR #48 → closed, superseded by PR #60
PR #55 → closed historical probe
Issue #47 → import-order remediation completed
Issues #42 / #52 / #53 → solo post-hoc reviews completed
Issue #39 → future team-transition trigger
```

---

## 9. 🔗 Essential files

- `docs/CURRENT_STATUS.md` — authoritative maturity and authorization status;
- `docs/GOVERNANCE.md` — risk tiers and merge policy;
- `docs/governance/solo-maintainer-mode.md` — current operating model;
- `docs/governance/solo-maintainer-review-checklist.md` — Tier A checklist;
- `docs/ENVIRONMENT_MANIFEST.md` — accepted implementation environment;
- `docs/research/RESEARCH_INDEX.md` — research navigation;
- `docs/research/MENTAURY_CAPABILITY_LEASE_RESOLUTION_NOTES.md` — P1-001 contract;
- `docs/research/POST_P0_ROADMAP_V0.1.md` — execution ordering.

---

## 10. 🏁 Formula

```text
P0 foundation implemented
+ beliefs/evidence import isolation fixed
+ active solo governance
+ P1-001 docs frozen

≠ P1 runtime
≠ domain runtime
≠ production ready
≠ independent assurance
```
