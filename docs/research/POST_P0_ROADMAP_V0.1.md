# 🗺️ Post-P0 Roadmap

```text
Status:                       ADOPTED ROADMAP · DOCS_ONLY
Version:                      0.2
Updated:                      2026-08-09
Current review mode:          SOLO_MAINTAINER · TIER_A
P1-001 docs status:           FROZEN_DOCS
P1-001 implementation:        NOT AUTHORIZED
Runtime authority:            NONE
Truth authority:              NONE
Capability authority:         NONE
Canon modification authority: NONE
Direct or indirect M3 write:  FORBIDDEN
Domain runtime:               NOT AUTHORIZED
```

```text
Roadmap adopted ≠ runtime authorized
FROZEN_DOCS ≠ implementation
Research presence ≠ roadmap priority
Solo review ≠ independent certification
```

The filename retains `V0.1` only for stable historical links. This document's
metadata is the current version authority.

---

## 1. 🎯 Current sequence

```text
P0-001…P0-015 implemented
→ P1-001 Capability Lease Resolution contract frozen
→ implementation remains unauthorized
→ separate bounded owner GO required before src/
```

P1-001 remains the first post-P0 execution candidate because authority-sensitive
runtime cannot rely on an opaque lease reference. The accepted docs define a
pure fail-closed contract without enabling runtime.

Owning contract:

[`MENTAURY_CAPABILITY_LEASE_RESOLUTION_NOTES.md`](MENTAURY_CAPABILITY_LEASE_RESOLUTION_NOTES.md)

---

## 2. ✅ P1-001 frozen docs boundary

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

Resource vocabulary:

```text
max_registry_lookups
max_record_bytes
max_scope_items
```

---

## 3. 🧾 Freeze evidence

```text
PR:              #58
Reviewed head:   a32b0e4fe55382f76a70b2205104af2e28f99451
Exact-head CI:   31317003807 · success
Merge:           8e89063fd74f5ae6d337366c299fa5f4e0164618
Post-merge CI:   31317057193 · success
Review:          correctness + adversarial maintainer passes
Independent human assurance: not claimed
```

The review corrected malformed-registry and premature-EXPIRED ambiguities before
acceptance. Structural tests enforce deny ordering, scenario numbering and
cross-document non-authorization boundaries.

---

## 4. 🔐 Authorization gate before implementation

Any future registry or resolver implementation requires all of:

1. separate explicit owner GO in `docs/CURRENT_STATUS.md`;
2. minimal pure implementation scope;
3. a new Tier A exact-head correctness and adversarial review;
4. deterministic, adversarial and metamorphic tests;
5. preserved P0 event/replay compatibility;
6. no Action Gate, tool execution, M3 or domain-runtime expansion;
7. green exact-head and post-merge CI.

Until such a GO exists:

```text
CAPABILITY_LEASE_RESOLVER_NOT_AUTHORIZED
DOMAIN_RUNTIME_NOT_AUTHORIZED
ACTION_GATE_NOT_AUTHORIZED
DIRECT_OR_INDIRECT_M3_WRITE_FORBIDDEN
```

---

## 5. 🚫 Deferred work

Not part of P1-001:

```text
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

---

## 6. 🔬 Research promotion

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

## 7. 🔄 Status rules

| Event | Status result |
|---|---|
| Research captured | no runtime status change |
| P1 docs frozen | `FROZEN_DOCS · NOT_IMPLEMENTED` |
| Owner authorizes bounded code | explicit scope added to `CURRENT_STATUS` |
| Code PR merged + main CI | only then may bounded implementation be marked complete |

GitHub `main` and `docs/CURRENT_STATUS.md` are authoritative. Notion is synced
after verified merge evidence.

---

## 8. 🏁 Formula

```text
P0 complete
→ P1-001 docs frozen
→ implementation still unauthorized
→ separate owner GO
→ possible future pure resolver
→ Action Gate / M3 / domain runtime remain forbidden
```

### Related

- [`MENTAURY_CAPABILITY_LEASE_RESOLUTION_NOTES.md`](MENTAURY_CAPABILITY_LEASE_RESOLUTION_NOTES.md)
- [`RESEARCH_INDEX.md`](RESEARCH_INDEX.md)
- [`../CURRENT_STATUS.md`](../CURRENT_STATUS.md)
- [`../GOVERNANCE.md`](../GOVERNANCE.md)
