# 🔐 P1-001 Capability Lease Resolution — Implementation Authorization

```text
Status:                       OWNER_GO · AUTHORIZED_BOUNDED · NOT_STARTED
Authorization date:           2026-08-09
Milestone:                    P1-001 Capability Lease Resolution
Contract authority:           docs/research/MENTAURY_CAPABILITY_LEASE_RESOLUTION_NOTES.md
Status authority:             docs/CURRENT_STATUS.md
Governance:                   SOLO_MAINTAINER · TIER_A
Independent human assurance:  NOT CLAIMED
Implementation completion:    NOT CLAIMED
Runtime deployment:           NOT AUTHORIZED
```

## 1. 🎯 Authorization source

After completion of the P0 line, governance reconciliation, P1-001 contract
freeze and maintenance cleanup, the repository owner instructed the agent to
continue the remaining work on 2026-08-09.

This document is the explicit separate owner GO required by the frozen P1-001
contract and Post-P0 Roadmap.

```text
owner instruction
→ bounded implementation authorization
≠ implementation complete
≠ deployment authorization
≠ Action Gate authorization
```

## 2. ✅ Exact authorized implementation scope

Only the following new implementation and test paths are authorized:

```text
src/mentaury/capabilities/__init__.py
src/mentaury/capabilities/lease/__init__.py
src/mentaury/capabilities/lease/contracts.py
src/mentaury/capabilities/lease/resolver.py
tests/test_capability_lease_resolution.py
```

The implementation PR may also make the minimum supporting changes required to:

- classify the created lease path as active Tier A in governance;
- align CODEOWNERS with the created Tier A path;
- update structural governance and contract tests;
- add bounded documentation for the implemented resolver;
- synchronize authoritative and derived status only after verified merge.

No other runtime path is authorized by this receipt.

## 3. 🧊 Frozen contract remains normative

The implementation must conform to the frozen contract in:

- `docs/research/MENTAURY_CAPABILITY_LEASE_RESOLUTION_NOTES.md`;
- `docs/research/POST_P0_ROADMAP_V0.1.md`.

Required properties:

```text
pure and deterministic
fail closed
caller-supplied RegistrySnapshot
caller-supplied AuthorityRef
caller-supplied ActionIntent
caller-supplied evaluated_at
caller-supplied ResolutionBudget
exact live-head lookup
no history walk or fallback
registry admission before lookup authorization
record admission before digest and semantic authorization
canonical digest recomputation excluding content_digest
exact purpose / operation / typed-scope / side-effect checks
first-match deny precedence
fork / restore quarantine as UNVERIFIED
ALLOW executes nothing
```

The frozen contract's metadata records that implementation was unauthorized at
the time of PR #58. This later receipt changes current implementation authority
without rewriting the historical freeze evidence.

## 4. 🚫 Explicit non-goals and prohibitions

This authorization does not permit:

```text
registry persistence
registry network service
network access
ambient system clock
ambient environment authority
filesystem or database mutation
SQLite schema changes
event append
replay or projection integration
belief mutation
identity or relationship mutation
direct or indirect M3 write
Action Gate
Tool Receipt runtime
tool execution
external side effects
operator override inside resolve()
wildcard, hierarchy or semantic scope expansion
backend selection or migration
production deployment
```

The existing P0 `AuthorityRef` shape remains unchanged:

```text
(capability_lease_id, capability_revision)
```

## 5. 🧪 Mandatory validation matrix

The implementation PR must include:

- all `CAP-SC-001…CAP-SC-025` contract scenarios;
- exact deny-precedence tests;
- deterministic repeatability tests;
- input-order and unrelated-record metamorphic tests;
- strict unknown-field and wrong-type rejection;
- duplicate and non-canonical set-like collection rejection;
- canonical digest recomputation tests;
- stale and future revision denial;
- revoked, expired, suspended, superseded and unverified denial;
- exact purpose, operation, typed scope and side-effect containment tests;
- budget exhaustion tests;
- import-side-effect tests proving no network/database/filesystem mutation;
- P0 compatibility tests proving envelopes and replay require no registry.

## 6. 🛡️ Tier A delivery sequence

```text
1. merge this authorization checkpoint
2. verify green post-merge main CI
3. create a clean implementation branch from that main
4. implement only the authorized pure resolver slice
5. run full validator, freshness, pytest and compileall
6. inspect exact final diff
7. complete correctness review pass
8. complete adversarial review pass
9. resolve every review conversation
10. merge only the unchanged reviewed head
11. verify green post-merge main CI
12. update status and Notion from verified evidence
```

Implementation and authorization must not be combined into one unreviewed
status jump.

## 7. 🏁 Completion condition

P1-001 may be marked implemented only after all of the following are true:

```text
bounded code exists on main
+ contract scenarios pass
+ adversarial and metamorphic tests pass
+ full repository CI passes exact PR head
+ Tier A correctness pass recorded
+ Tier A adversarial pass recorded
+ unresolved review conversations = 0
+ merge uses unchanged reviewed head
+ resulting main CI passes
+ authoritative status is synchronized
```

Until then:

```text
P1_001_IMPLEMENTATION_AUTHORIZED_BOUNDED
P1_001_IMPLEMENTATION_NOT_STARTED_OR_IN_PROGRESS
P1_001_COMPLETION_NOT_CLAIMED
ACTION_GATE_NOT_AUTHORIZED
TOOL_EXECUTION_NOT_AUTHORIZED
DIRECT_OR_INDIRECT_M3_WRITE_FORBIDDEN
DOMAIN_RUNTIME_NOT_AUTHORIZED
```
