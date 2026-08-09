# 🗺️ Post-P0 Roadmap

```text
Status:                       ADOPTED ROADMAP · DOCS_ONLY
Version:                      0.3
Updated:                      2026-08-09
Current review mode:          SOLO_MAINTAINER · TIER_A
P1-001 docs status:           FROZEN_DOCS
P1-001 implementation:        AUTHORIZED_BOUNDED · NOT_STARTED
Implementation completion:    NOT CLAIMED
Runtime deployment authority: NONE
Truth authority:              NONE
Capability grant authority:   NONE
Canon modification authority: NONE
Direct or indirect M3 write:  FORBIDDEN
Domain runtime:               NOT AUTHORIZED
```

```text
Roadmap adopted ≠ runtime deployed
FROZEN_DOCS ≠ implementation complete
AUTHORIZED_BOUNDED ≠ permission to widen scope
Research presence ≠ roadmap priority
Solo review ≠ independent certification
```

The filename retains `V0.1` for stable historical links. Document metadata is
the current version authority.

---

## 1. 🎯 Current sequence

```text
P0-001…P0-015 implemented
→ P1-001 contract frozen by PR #58
→ separate owner GO recorded
→ bounded pure implementation authorized
→ implementation not started
→ separate Tier A implementation PR required
```

P1-001 remains the first post-P0 execution milestone because authority-sensitive
future runtime cannot rely on an opaque lease reference.

Owning surfaces:

- [Frozen contract](MENTAURY_CAPABILITY_LEASE_RESOLUTION_NOTES.md)
- [Implementation authorization](../P1_001_IMPLEMENTATION_AUTHORIZATION.md)
- [Current status](../CURRENT_STATUS.md)

---

## 2. ✅ P1-001 frozen contract boundary

```text
RegistrySnapshot is explicit and caller supplied
registry admission precedes lookup
exact live-head lookup; no history walk
record admission precedes digest and authorization
digest excludes content_digest
lifecycle uses caller-supplied evaluated_at
purpose / operation / typed scope are exact
budgets are explicit and fail closed
fork/restore grants become UNVERIFIED
ALLOW executes nothing
```

Threat handling includes:

| Threat | Contract response |
|---|---|
| Registry unavailable | `REGISTRY_UNAVAILABLE` |
| Malformed registry | `REGISTRY_CONTRACT_VIOLATION` |
| Unknown lease | `UNKNOWN_LEASE` |
| Stale/future revision | `REVISION_MISMATCH` |
| Oversized record | `BUDGET_EXHAUSTED` |
| Malformed record | `LEASE_CONTRACT_VIOLATION` |
| Forged digest | `LEASE_DIGEST_MISMATCH` |
| Revoked/expired grant | deterministic lifecycle denial |
| Wildcard/semantic expansion | forbidden |
| Ambient network/clock authority | forbidden |
| Fork/restore authority carryover | quarantine as `UNVERIFIED` |

Resource vocabulary remains:

```text
max_registry_lookups
max_record_bytes
max_scope_items
```

---

## 3. 🧾 Contract freeze evidence

```text
PR:              #58
Reviewed head:   a32b0e4fe55382f76a70b2205104af2e28f99451
Exact-head CI:   31317003807 · success
Merge:           8e89063fd74f5ae6d337366c299fa5f4e0164618
Post-merge CI:   31317057193 · success
Review:          correctness + adversarial maintainer passes
Independent human assurance: not claimed
```

The frozen document remains the normative contract. Its freeze-time statement
that implementation was not authorized is historical evidence of the state at
PR #58; current authorization is recorded separately and does not rewrite that
receipt.

---

## 4. 🔐 Owner authorization checkpoint

The repository owner instructed the agent on 2026-08-09 to continue the
remaining work. The separate authorization receipt defines the exact bounded
implementation scope.

```text
P1_001_IMPLEMENTATION_AUTHORIZED_BOUNDED
P1_001_IMPLEMENTATION_NOT_STARTED
P1_001_COMPLETION_NOT_CLAIMED
```

Authorized source/test slice:

```text
src/mentaury/capabilities/__init__.py
src/mentaury/capabilities/lease/__init__.py
src/mentaury/capabilities/lease/contracts.py
src/mentaury/capabilities/lease/resolver.py
tests/test_capability_lease_resolution.py
```

Minimum governance/test/documentation support may accompany the implementation
only to classify and validate that exact Tier A path.

---

## 5. 🛠️ Implementation requirements

The implementation PR must be:

```text
pure
+ deterministic
+ caller supplied
+ fail closed
+ standard-library only
+ side-effect free
```

It must implement the frozen deny ordering and all `CAP-SC-001…CAP-SC-025`
scenarios, plus adversarial and metamorphic validation.

It must not:

```text
persist or fetch a registry
read network, environment or system clock
mutate files, databases, events or projections
change P0 AuthorityRef
perform action execution
write beliefs, identity, relationships or M3
select a backend
```

The implementation result `ALLOW` remains a pure classification and executes
nothing.

---

## 6. 🚫 Deferred work

Not part of P1-001:

```text
registry persistence or service
Identity Continuity runtime
Controlled Origin ingestion
Non-Projection runtime
Character / Curiosity engines
Human Paths runtime
Knowledge Density / Humor / Conflict Navigator
Tool Receipt runtime
Action Gate execution
Governed Synthesis engine
LLM integration
backend selection or migration
```

These remain research or future milestones and gain no priority merely by being
documented.

Until separately authorized:

```text
DOMAIN_RUNTIME_NOT_AUTHORIZED
ACTION_GATE_NOT_AUTHORIZED
TOOL_EXECUTION_NOT_AUTHORIZED
DIRECT_OR_INDIRECT_M3_WRITE_FORBIDDEN
```

---

## 7. 🔬 Research promotion

The [Research Index](RESEARCH_INDEX.md) preserves hypotheses and candidates.
Promotion requires:

```text
demonstrated problem
+ bounded slice
+ invariants and non-goals
+ threat model
+ P0 / Canon compatibility
+ current-governance correctness review
+ current-governance adversarial review
+ explicit owner authorization
```

Issue #39 governs the future transition when a genuine independent reviewer or
team exists. Its current absence is not a solo-mode blocker.

---

## 8. 🔄 Status rules

| Event | Status result |
|---|---|
| Research captured | no runtime status change |
| P1 docs frozen | `FROZEN_DOCS · NOT_IMPLEMENTED` |
| Owner GO merged | `AUTHORIZED_BOUNDED · NOT_STARTED` |
| Implementation PR opened | `AUTHORIZED_BOUNDED · IN_PROGRESS` only in live PR state |
| Code PR merged + main CI | bounded implementation may then be marked implemented |
| Action Gate or deployment | remains unauthorized without a separate milestone |

GitHub `main` and `docs/CURRENT_STATUS.md` are authoritative. Notion is synced
after verified merge evidence.

---

## 9. 🏁 Formula

```text
P0 complete
→ P1-001 docs frozen
→ bounded owner GO
→ pure resolver implementation PR
→ exact-head Tier A review
→ post-merge main CI
→ bounded implementation status sync

Action Gate / tools / M3 / domain runtime remain forbidden
```

### Related

- [`MENTAURY_CAPABILITY_LEASE_RESOLUTION_NOTES.md`](MENTAURY_CAPABILITY_LEASE_RESOLUTION_NOTES.md)
- [`../P1_001_IMPLEMENTATION_AUTHORIZATION.md`](../P1_001_IMPLEMENTATION_AUTHORIZATION.md)
- [`RESEARCH_INDEX.md`](RESEARCH_INDEX.md)
- [`../CURRENT_STATUS.md`](../CURRENT_STATUS.md)
- [`../GOVERNANCE.md`](../GOVERNANCE.md)
