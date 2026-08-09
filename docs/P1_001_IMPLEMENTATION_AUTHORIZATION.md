# 🔐 P1-001 Capability Lease Resolution — Authorization and Completion Receipt

```text
Status:                       OWNER_GO_CONSUMED · IMPLEMENTED_BOUNDED
Authorization date:           2026-08-09
Completion date:              2026-08-09
Milestone:                    P1-001 Capability Lease Resolution
Contract authority:           docs/research/MENTAURY_CAPABILITY_LEASE_RESOLUTION_NOTES.md
Status authority:             docs/CURRENT_STATUS.md
Governance:                   SOLO_MAINTAINER · TIER_A
Independent human assurance:  NOT CLAIMED
Runtime deployment:           NOT AUTHORIZED
Next runtime milestone:       NOT AUTHORIZED
```

## 1. 🎯 Authorization source and disposition

The repository owner instructed the agent on 2026-08-09 to continue the
remaining work after the P1-001 contract freeze. PR #62 recorded the separate
bounded owner GO required by the frozen contract and roadmap.

That authorization has now been consumed by the exact bounded implementation in
PR #63.

```text
owner instruction
→ bounded authorization PR #62
→ pure resolver implementation PR #63
→ green resulting main CI
→ IMPLEMENTED_BOUNDED
```

The authorization does not roll forward to any registry, Action Gate, tool,
deployment or later P1 milestone.

---

## 2. ✅ Exact completed implementation scope

```text
src/mentaury/capabilities/__init__.py
src/mentaury/capabilities/lease/__init__.py
src/mentaury/capabilities/lease/contracts.py
src/mentaury/capabilities/lease/resolver.py
tests/test_capability_lease_resolution.py
```

Minimum Tier A support completed with the implementation:

- active lease path added to `docs/GOVERNANCE.md`;
- active lease path added to `CODEOWNERS`;
- structural governance tests updated.

No other runtime path was authorized or implemented by this receipt.

---

## 3. 🧊 Frozen contract conformance

The implementation conforms to the frozen contract in:

- `docs/research/MENTAURY_CAPABILITY_LEASE_RESOLUTION_NOTES.md`;
- `docs/research/POST_P0_ROADMAP_V0.1.md`.

Implemented properties:

```text
pure and deterministic
fail closed
caller-supplied RegistrySnapshot
caller-supplied P0 AuthorityRef
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

The frozen document's metadata remains historical evidence that implementation
was not authorized at the time of PR #58. PR #62 provided the later bounded GO;
PR #63 completed it without rewriting the freeze receipt.

---

## 4. 🧾 Verified evidence

### Authorization

```text
PR:                    #62
Reviewed head:         53b3eec436d4dbfd2c13050a9966fb84ef0b7b3a
Exact-head CI:         31322108100 · success · 327 passed
Merge:                 d5e9e2fb11ea5a9c123c1cb1cc2b6f16dac53b98
Post-merge CI:         31322210843 · success
```

### Implementation

```text
PR:                    #63
Reviewed head:         e873e43331fa7273b92f896b371707e4779b17d4
Exact-head CI:         31323051934 · success · 387 passed
Merge:                 f21809d8f31a457bd7acfe1d766230973ba9ecf5
Post-merge CI:         31323138053 · success
Correctness pass:      PASS
Adversarial pass:      PASS
Review conversations:  0
Independent assurance: NOT CLAIMED
```

The adversarial pass identified nested mutability in the initial snapshot
representation despite an already green CI run. The final reviewed head reused
the P0 recursive payload freezer and added a regression proving that nested
mappings and sequences cannot be mutated through the stored snapshot.

---

## 5. 🧪 Retained validation boundary

The accepted suite covers:

- all `CAP-SC-001…CAP-SC-025` frozen scenarios;
- exact first-match denial precedence;
- deterministic byte-equivalent repeatability;
- typed and mapping input equivalence;
- unrelated-record metamorphic invariance;
- strict unknown-field and wrong-type rejection;
- duplicate and non-canonical set-like collection rejection;
- canonical digest recomputation;
- stale and future revision denial;
- revoked, expired, suspended, superseded and unverified denial;
- exact purpose, operation, typed scope and side-effect containment;
- explicit budget denial;
- recursive snapshot immutability;
- fresh-process no-network/database/filesystem/clock import checks;
- unchanged two-field P0 `AuthorityRef`;
- absence of storage, replay, beliefs and evidence integration.

---

## 6. 🚫 Preserved prohibitions

The completed bounded implementation does not include or authorize:

```text
registry persistence
registry network service
network access
ambient system clock or environment authority
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

The P0 `AuthorityRef` remains exactly:

```text
(capability_lease_id, capability_revision)
```

`ResolutionResult(ALLOW)` is observation/classification data and contains no
reusable capability material.

---

## 7. ⛔ Authorization stop

```text
P1_001_CAPABILITY_LEASE_RESOLUTION_IMPLEMENTED_BOUNDED
P1_001_PURE_RESOLVER_VALIDATED
NO_POST_P1_001_RUNTIME_MILESTONE_AUTHORIZED
ACTION_GATE_NOT_AUTHORIZED
TOOL_EXECUTION_NOT_AUTHORIZED
DIRECT_OR_INDIRECT_M3_WRITE_FORBIDDEN
DOMAIN_RUNTIME_NOT_AUTHORIZED
```

Any next runtime-capable step requires a new bounded contract, threat model,
explicit owner GO, independent implementation PR, exact-head Tier A review and
green post-merge `main` CI.
