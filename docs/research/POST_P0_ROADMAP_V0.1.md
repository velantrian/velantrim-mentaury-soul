# 🗺️ Post-P0 Roadmap

```text
Status:                       ADOPTED ROADMAP · DOCS_ONLY
Version:                      0.4
Updated:                      2026-08-09
Current review mode:          SOLO_MAINTAINER · TIER_A
P1-001 contract:              FROZEN_DOCS
P1-001 implementation:        IMPLEMENTED_BOUNDED
P1-001 validation:            EXACT_HEAD_AND_MAIN_CI_PASS
Next runtime milestone:       NOT SELECTED · NOT AUTHORIZED
Runtime deployment authority: NONE
Truth authority:              NONE
Capability grant authority:   NONE
Canon modification authority: NONE
Direct or indirect M3 write:  FORBIDDEN
Domain runtime:               NOT AUTHORIZED
DOMAIN_RUNTIME_NOT_AUTHORIZED
```

```text
IMPLEMENTED_BOUNDED ≠ registry service
IMPLEMENTED_BOUNDED ≠ Action Gate
IMPLEMENTED_BOUNDED ≠ tool execution
IMPLEMENTED_BOUNDED ≠ deployment
Research presence ≠ roadmap priority
Solo review ≠ independent certification
```

The filename retains `V0.1` for stable historical links. Document metadata is
the current version authority.

---

## 1. ✅ Completed P1-001 sequence

```text
P0-001…P0-015 implemented
→ P1-001 contract frozen by PR #58
→ bounded owner GO merged through PR #62
→ pure resolver implemented through PR #63
→ exact-head Tier A review passed
→ resulting main CI passed
→ P1-001 IMPLEMENTED_BOUNDED
```

Owning surfaces:

- [Frozen contract](MENTAURY_CAPABILITY_LEASE_RESOLUTION_NOTES.md)
- [Authorization and completion receipt](../P1_001_IMPLEMENTATION_AUTHORIZATION.md)
- [Current status](../CURRENT_STATUS.md)

---

## 2. 🔐 Implemented P1-001 boundary

```text
RegistrySnapshot is explicit and caller supplied
registry admission precedes lookup
exact live-head lookup; no history walk or fallback
selected-record admission precedes digest and authorization
digest excludes only top-level content_digest
lifecycle uses caller-supplied evaluated_at
purpose / operation / typed scope are exact
budgets are explicit and fail closed
fork/restore grants remain UNVERIFIED
ALLOW executes nothing
```

Implemented paths:

```text
src/mentaury/capabilities/__init__.py
src/mentaury/capabilities/lease/__init__.py
src/mentaury/capabilities/lease/contracts.py
src/mentaury/capabilities/lease/resolver.py
tests/test_capability_lease_resolution.py
```

Threat handling includes:

| Threat | Result |
|---|---|
| Registry unavailable | `REGISTRY_UNAVAILABLE` |
| Malformed registry | `REGISTRY_CONTRACT_VIOLATION` |
| Unknown lease | `UNKNOWN_LEASE` |
| Stale/future revision | `REVISION_MISMATCH` |
| Oversized record/scope | `BUDGET_EXHAUSTED` |
| Malformed record/invariants | `LEASE_CONTRACT_VIOLATION` |
| Forged digest | `LEASE_DIGEST_MISMATCH` |
| Revoked/expired/non-active grant | deterministic lifecycle denial |
| Purpose/operation/scope/effect mismatch | exact denial |
| Ambient authority | absent by construction and tests |

---

## 3. 🧾 Completion evidence

### Authorization PR #62

```text
Reviewed head:   53b3eec436d4dbfd2c13050a9966fb84ef0b7b3a
Exact-head CI:   31322108100 · success · 327 passed
Merge:           d5e9e2fb11ea5a9c123c1cb1cc2b6f16dac53b98
Post-merge CI:   31322210843 · success
```

### Implementation PR #63

```text
Reviewed head:   e873e43331fa7273b92f896b371707e4779b17d4
Exact-head CI:   31323051934 · success · 387 passed
Merge:           f21809d8f31a457bd7acfe1d766230973ba9ecf5
Post-merge CI:   31323138053 · success
Review:          correctness + adversarial passes
Review threads:  0
Independent human assurance: not claimed
```

The final head includes recursive registry-record immutability added after the
adversarial pass found that nested stored values could otherwise remain
mutable despite caller detachment.

---

## 4. 🚫 Work not included in P1-001

```text
registry persistence or service
network registry lookup
ambient clock/environment authority
Action Gate
Tool Receipt runtime
tool execution or external effects
event append or replay/projection integration
belief, identity, relationship or M3 mutation
Identity Continuity runtime
Controlled Origin ingestion
Non-Projection runtime
Character / Curiosity engines
Human Paths runtime
Governed Synthesis engine
LLM integration
backend selection or migration
production deployment
```

---

## 5. ⛔ Next execution gate

```text
NO_POST_P1_001_RUNTIME_MILESTONE_AUTHORIZED
DOMAIN_RUNTIME_NOT_AUTHORIZED
```

No registry service, Action Gate, P1-002 or other runtime milestone follows
automatically from P1-001 completion.

A new runtime milestone requires:

```text
demonstrated problem
+ minimal bounded slice
+ explicit contract and non-goals
+ threat model
+ P0 / Canon compatibility
+ explicit owner GO
+ clean Tier A implementation PR
+ exact-head correctness and adversarial review
+ green resulting main CI
```

Maintenance, bug remediation and research capture remain allowed under current
governance without implying new runtime authority.

---

## 6. 🔬 Research promotion

The [Research Index](RESEARCH_INDEX.md) preserves hypotheses and candidates.
Promotion requires evidence and explicit authorization; documentation alone
cannot select the next milestone.

Issue #39 governs only the future transition to genuine independent review. Its
current absence is not a solo-mode blocker.

---

## 7. 🔄 Status rules

| Event | Status result |
|---|---|
| Research captured | no runtime status change |
| Contract frozen | `FROZEN_DOCS` |
| Bounded Owner GO merged | `AUTHORIZED_BOUNDED` |
| Code PR merged + main CI | `IMPLEMENTED_BOUNDED` |
| Registry/Action Gate/deployment proposal | requires a new independent authorization cycle |

GitHub `main` and `docs/CURRENT_STATUS.md` remain authoritative. Notion is a
derived navigation/status surface synchronized only after verified evidence.

---

## 8. 🏁 Formula

```text
P0 complete
→ P1-001 contract frozen
→ bounded owner GO
→ pure resolver implementation
→ exact-head Tier A review
→ green post-merge main CI
→ P1-001 IMPLEMENTED_BOUNDED
→ STOP until a new bounded Owner GO
```

### Related

- [`MENTAURY_CAPABILITY_LEASE_RESOLUTION_NOTES.md`](MENTAURY_CAPABILITY_LEASE_RESOLUTION_NOTES.md)
- [`../P1_001_IMPLEMENTATION_AUTHORIZATION.md`](../P1_001_IMPLEMENTATION_AUTHORIZATION.md)
- [`RESEARCH_INDEX.md`](RESEARCH_INDEX.md)
- [`../CURRENT_STATUS.md`](../CURRENT_STATUS.md)
- [`../GOVERNANCE.md`](../GOVERNANCE.md)
