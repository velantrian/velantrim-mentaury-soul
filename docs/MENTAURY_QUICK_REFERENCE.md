# 📌 Mentaury Soul — Quick Reference

```text
Status:      NAVIGATION_ONLY · NONAUTHORITATIVE · DERIVED_DOCUMENT
Updated:     2026-08-09
Authority:   docs/CURRENT_STATUS.md + verified GitHub main
Governance:  SOLO_MAINTAINER · required approvals 0
```

---

## 1. 🚦 Current status

```text
CANON_V0.1_FROZEN
P0-001…P0-015_IMPLEMENTED_IN_MAIN
P1_001_CAPABILITY_LEASE_RESOLUTION_IMPLEMENTED_BOUNDED
P1_001_PURE_RESOLVER_VALIDATED

NO_POST_P1_001_RUNTIME_MILESTONE_AUTHORIZED
ACTION_GATE_NOT_AUTHORIZED
TOOL_EXECUTION_NOT_AUTHORIZED
DIRECT_OR_INDIRECT_M3_WRITE_FORBIDDEN
DOMAIN_RUNTIME_NOT_AUTHORIZED
RUNTIME_DEPLOYMENT_NOT_AUTHORIZED
```

---

## 2. ✅ P1-001 evidence

```text
Authorization PR #62
merge:          d5e9e2fb11ea5a9c123c1cb1cc2b6f16dac53b98
main CI:        31322210843 · success

Implementation PR #63
reviewed head:  e873e43331fa7273b92f896b371707e4779b17d4
exact-head CI:  31323051934 · success · 387 passed
merge:          f21809d8f31a457bd7acfe1d766230973ba9ecf5
main CI:        31323138053 · success
review:         solo Tier A correctness + adversarial passes
```

Implemented:

```text
pure caller-supplied resolver
immutable typed lease contracts
exact admitted live-head lookup
strict registry and record admission
canonical digest verification
exact purpose / operation / typed scope / effects
first-match deterministic denial
recursive snapshot immutability
ALLOW executes nothing
```

---

## 3. 🛡️ Solo governance

```text
pull request
+ required CI
+ up-to-date branch
+ resolved conversations
+ no force push
+ no main deletion
+ empty bypass list
```

Tier A adds correctness and adversarial passes on the exact final head plus
green post-merge `main` CI. Automated review is not independent human assurance.
Issue #39 is a future team-transition trigger only.

---

## 4. 🚫 P1-001 boundaries

```text
IMPLEMENTED_BOUNDED
≠ registry persistence/service
≠ network registry lookup
≠ Action Gate
≠ Tool Receipt or tool execution
≠ event/replay integration
≠ belief, identity, relationship or M3 mutation
≠ backend selection
≠ deployment
```

The P1-001 Owner GO is consumed. A next runtime milestone requires a new bounded
contract, threat model and explicit Owner GO.

---

## 5. ✅ Implemented foundation

```text
P0-001…P0-013 integrity, storage and replay foundation
P0-014 minimal belief lifecycle
P0-015 deterministic Evidence Gate
P1-001 pure Capability Lease resolver
```

Implementation profile:

```text
Python 3.13
standard-library runtime
SQLite P0 storage profile
runtime dependencies: none
ambient I/O at import: forbidden
```

---

## 6. 🔬 Research boundary

```text
research document ≠ runtime
candidate captured ≠ selected
external research input ≠ integration
Notion page ≠ implementation authority
```

No backend or next execution milestone is selected.

---

## 7. 🔗 Essential files

- `docs/CURRENT_STATUS.md` — maturity and authorization authority;
- `docs/GOVERNANCE.md` — risk tiers and merge policy;
- `docs/P1_001_IMPLEMENTATION_AUTHORIZATION.md` — authorization/completion receipt;
- `docs/research/MENTAURY_CAPABILITY_LEASE_RESOLUTION_NOTES.md` — frozen contract;
- `docs/research/POST_P0_ROADMAP_V0.1.md` — completed sequence and stop gate;
- `docs/research/RESEARCH_INDEX.md` — research navigation;
- `docs/ENVIRONMENT_MANIFEST.md` — implementation environment.

---

## 8. 🏁 Formula

```text
P0 implemented
+ P1-001 implemented bounded
+ active solo governance

≠ registry service
≠ external actions
≠ domain runtime
≠ production ready
≠ independent assurance
```
