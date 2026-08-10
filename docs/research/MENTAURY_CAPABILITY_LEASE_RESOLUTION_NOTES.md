# 🔐 Capability Lease Resolution — Contract

```text
Status:                       ADOPTED · FROZEN_DOCS · DOCS_ONLY · NOT_IMPLEMENTED
Version:                      0.2
Frozen by:                    PR #58
Reviewed head:                a32b0e4fe55382f76a70b2205104af2e28f99451
Exact-head CI:                31317003807 · success
Merge:                        8e89063fd74f5ae6d337366c299fa5f4e0164618
Post-merge CI:                31317057193 · success
Target milestone:             POST_P0 / P1-001
Runtime authority:            NONE
Truth authority:              NONE
Identity authority:           NONE
Capability authority:         NONE
Canon modification authority: NONE
Direct or indirect M3 write:  FORBIDDEN
Implementation in src/:       NOT AUTHORIZED
Review mode:                  SOLO_MAINTAINER · TIER_A
Independent assurance:        NOT CLAIMED
```

```text
FROZEN_DOCS ≠ implementation permission
AuthorityRef ≠ permission blob
Resolution ALLOW ≠ action execution
Maintainer review ≠ independent human review
```

---

## 1. 🎯 Problem

P0 stores an immutable reference:

```text
AuthorityRef = capability_lease_id + capability_revision
```

It provides provenance and equality checks, but not an enforceable grant. P1-001
freezes a future pure resolver contract without implementing it.

---

## 2. 🪞 Scope

In scope:

- immutable `CapabilityLeaseRecord`;
- explicit caller-supplied `RegistrySnapshot`;
- versioned snapshot and record admission;
- exact live-head lookup;
- canonical digest recomputation;
- caller-supplied time and budgets;
- exact purpose, operation, typed scope and side-effect checks;
- deterministic first-match denial;
- fork/restore quarantine.

Out of scope:

```text
registry or resolver code
network lookup or ambient clock
environment-variable authority
Action Gate or Tool Receipt runtime
tool execution or external effects
belief / identity / relationship mutation
direct or indirect M3 write
operator override inside resolve()
backend selection
Canon modification
```

Snapshot provenance remains an upstream caller-side boundary. The resolver can
validate supplied structure but cannot prove who produced it.

---

## 3. 📚 Typed inputs

```text
RegistrySnapshot
AuthorityRef
ActionIntent
evaluated_at
ResolutionBudget
→ ResolutionResult
```

Reference shape:

```yaml
registry_snapshot:
  availability: "AVAILABLE"
  unavailable_reason: null
  registry_schema_version: 1
  live_heads:
    "CAP-...": 3
  records:
    - capability_lease_record

authority_ref:
  capability_lease_id: "CAP-..."
  capability_revision: 3

action_intent:
  purpose_id: "PURPOSE-..."
  operation_id: "OP-..."
  data_scope:
    - kind: "stream"
      identifier: "..."
  requested_side_effects: []

evaluated_at: "2026-08-09T12:00:00Z"

resolution_budget:
  max_registry_lookups: 1
  max_record_bytes: 65536
  max_scope_items: 128
```

No ambient default may expand permission.

### 3.1 RegistrySnapshot admission

An AVAILABLE snapshot is admitted before lookup:

```text
supported exact registry_schema_version
availability is AVAILABLE or UNAVAILABLE
UNAVAILABLE carries no grantable records
bounded unique live-head map
unique records indexed by (lease_id, revision)
no duplicate record keys
live-head entries point to existing exact records
unknown snapshot fields rejected
```

Malformed structure returns `REGISTRY_CONTRACT_VIOLATION`.

```text
REGISTRY_UNAVAILABLE ≠ REGISTRY_CONTRACT_VIOLATION
REGISTRY_CONTRACT_VIOLATION ≠ UNKNOWN_LEASE
UNKNOWN_LEASE ≠ REVISION_MISMATCH
```

The resolver never repairs, merges or infers registry state.

---

## 4. 🧾 CapabilityLeaseRecord

```yaml
capability_lease:
  lease_id: "CAP-..."
  revision: 1
  supersedes_revision: null
  status: "ACTIVE"
  tool_id: null
  granted_by:
    actor_type: "operator"
    actor_id: "..."
  purpose_id: "PURPOSE-..."
  allowed_operations: []
  data_scope: []
  allowed_side_effects: []
  not_before: "2026-08-09T00:00:00Z"
  expires_at: "2026-08-10T00:00:00Z"
  revocation_conditions: []
  revoked_at: null
  delegation_allowed: false
  branch_transfer_allowed: false
  audit_required: true
  identity_authority: "NONE"
  direct_m3_write: false
  content_digest: "sha256:..."
```

### 4.1 Record admission

Before digest or semantic authorization:

```text
unknown / missing fields rejected
wrong scalar or collection type rejected
duplicate set-like members rejected
non-canonical set ordering rejected
invalid RFC3339 UTC Z timestamps rejected
non-positive revision rejected
lookup key / record key mismatch rejected
record exceeding max_record_bytes → BUDGET_EXHAUSTED
```

Admission failure returns `LEASE_CONTRACT_VIOLATION`. An outer parser must
already enforce a bounded total input size.

### 4.2 Invariants

```text
revision 1 → supersedes_revision null
revision n > 1 → supersedes_revision = n - 1
no revision gaps or branches in v0.1
purpose_id is exact, not semantic free text
operations / side effects are unique and sorted
data_scope is unique and sorted by (kind, identifier)
not_before < expires_at
expires_at required
delegation_allowed = false by default
branch_transfer_allowed = false by default
identity_authority = NONE
direct_m3_write = false
revoked_at non-null iff status = REVOKED
```

Set-like ordering is schema admission, not a canonical-JSON side effect.

### 4.3 Digest domain

```text
lease_digest_payload
= admitted record without top-level content_digest

canonical_bytes
= MENTAURY_CANONICAL_JSON_V1(lease_digest_payload)

content_digest
= "sha256:" + lowercase_hex(SHA-256(canonical_bytes))
```

Stored digest is never trusted without recomputation.

---

## 5. 🔄 Lifecycle and lookup

States:

```text
PROPOSED · ACTIVE · SUSPENDED · REVOKED · EXPIRED · SUPERSEDED · UNVERIFIED
```

Only ACTIVE may reach the grant path. Historical audit resolution is outside
P1-001.

Exact lookup:

```text
one lookup by lease_id
→ admitted live-head revision
→ requested revision must equal live head
→ exact record by (lease_id, revision)
```

No history walk, fallback, nearest revision, wildcard or semantic lookup.

### 5.1 Time and lifecycle consistency

The resolver receives `evaluated_at`; it never reads the system clock.

```text
valid ACTIVE interval:
not_before <= evaluated_at < expires_at

status EXPIRED while evaluated_at < expires_at
→ LEASE_CONTRACT_VIOLATION

status ACTIVE while evaluated_at >= expires_at
→ LEASE_EXPIRED

status REVOKED with revoked_at null
or non-REVOKED with revoked_at non-null
→ LEASE_CONTRACT_VIOLATION
```

The resolver mutates no state.

### 5.2 Fork / restore quarantine

```text
source record remains audit-readable
→ destination creates a new revision
→ destination revision = UNVERIFIED
→ old ref returns REVISION_MISMATCH
→ new UNVERIFIED ref returns LEASE_NOT_ACTIVE
```

Reactivation requires explicit revalidation outside the resolver.

---

## 6. ⚙️ Pure resolver

```text
resolve(
  registry_snapshot,
  authority_ref,
  action_intent,
  evaluated_at,
  resolution_budget
) → ResolutionResult
```

Properties:

```text
pure and deterministic
fail closed
no network
no system clock
no environment authority
no registry mutation
no event append
no belief / identity / relationship / M3 mutation
no tool execution
no operator override
```

---

## 7. 🚦 Normative deny precedence

First matching failure supplies the single primary reason.

| Order | Check | Primary result |
|---:|---|---|
| 1 | request shape and required fields admitted | `REQUEST_INVALID` |
| 2 | budget object present | `BUDGET_MISSING` |
| 3 | budget values admitted and one lookup permitted | `BUDGET_EXHAUSTED` |
| 4 | registry snapshot available | `REGISTRY_UNAVAILABLE` |
| 5 | registry snapshot admitted | `REGISTRY_CONTRACT_VIOLATION` |
| 6 | exact lease id exists | `UNKNOWN_LEASE` |
| 7 | requested revision equals admitted live head | `REVISION_MISMATCH` |
| 8 | selected record fits `max_record_bytes` | `BUDGET_EXHAUSTED` |
| 9 | selected record admitted | `LEASE_CONTRACT_VIOLATION` |
| 10 | recomputed digest matches | `LEASE_DIGEST_MISMATCH` |
| 11 | semantic invariants and supersession valid | `LEASE_CONTRACT_VIOLATION` |
| 12 | lifecycle status and timestamps consistent | `LEASE_CONTRACT_VIOLATION` |
| 13 | not revoked | `LEASE_REVOKED` |
| 14 | not materialized or derived expired | `LEASE_EXPIRED` |
| 15 | status exactly ACTIVE | `LEASE_NOT_ACTIVE` |
| 16 | `evaluated_at >= not_before` | `NOT_YET_VALID` |
| 17 | exact purpose equality | `PURPOSE_MISMATCH` |
| 18 | exact operation membership | `OPERATION_NOT_ALLOWED` |
| 19 | scope counts fit `max_scope_items` | `BUDGET_EXHAUSTED` |
| 20 | requested typed scope is allowed subset | `DATA_SCOPE_VIOLATION` |
| 21 | requested side effects are allowed subset | `SIDE_EFFECT_NOT_ALLOWED` |
| 22 | every check passes | `ALLOW` |

```text
BUDGET_MISSING ≠ BUDGET_EXHAUSTED
revision behind or ahead → REVISION_MISMATCH
purpose → exact identifier equality
scope → exact typed-set containment
wildcard / hierarchy / semantic similarity → forbidden
```

---

## 8. 📤 ResolutionResult

```yaml
resolution_result:
  decision: "DENY"
  primary_reason: "REVISION_MISMATCH"
  lease_id: "CAP-..."
  requested_revision: 2
  observed_live_revision: 3
  observed_status: "ACTIVE"
  observed_digest: "sha256:..."
  evaluated_at: "2026-08-09T12:00:00Z"
  resolver_contract_version: "P1-001-v0.2"
```

No result may contain permission material reusable as authority.

```text
ALLOW ≠ Tool Receipt
ALLOW ≠ Action Gate approval
ALLOW ≠ execution success
ALLOW ≠ truth or identity authority
```

---

## 9. 🧪 Scenario contract

| ID | Scenario | Expected primary result |
|---|---|---|
| `CAP-SC-001` | unavailable registry | `REGISTRY_UNAVAILABLE` |
| `CAP-SC-002` | unsupported registry schema | `REGISTRY_CONTRACT_VIOLATION` |
| `CAP-SC-003` | duplicate key or broken live-head target | `REGISTRY_CONTRACT_VIOLATION` |
| `CAP-SC-004` | unknown lease in admitted registry | `UNKNOWN_LEASE` |
| `CAP-SC-005` | revision behind live head | `REVISION_MISMATCH` |
| `CAP-SC-006` | revision ahead of live head | `REVISION_MISMATCH` |
| `CAP-SC-007` | oversized record | `BUDGET_EXHAUSTED` |
| `CAP-SC-008` | malformed lease schema | `LEASE_CONTRACT_VIOLATION` |
| `CAP-SC-009` | forged digest | `LEASE_DIGEST_MISMATCH` |
| `CAP-SC-010` | malformed supersession | `LEASE_CONTRACT_VIOLATION` |
| `CAP-SC-011` | premature materialized `EXPIRED` status | `LEASE_CONTRACT_VIOLATION` |
| `CAP-SC-012` | revoked lease | `LEASE_REVOKED` |
| `CAP-SC-013` | ACTIVE at/after expiry | `LEASE_EXPIRED` |
| `CAP-SC-014` | other non-ACTIVE state | `LEASE_NOT_ACTIVE` |
| `CAP-SC-015` | before `not_before` | `NOT_YET_VALID` |
| `CAP-SC-016` | purpose mismatch | `PURPOSE_MISMATCH` |
| `CAP-SC-017` | operation not allowed | `OPERATION_NOT_ALLOWED` |
| `CAP-SC-018` | scope budget exceeded | `BUDGET_EXHAUSTED` |
| `CAP-SC-019` | typed-scope violation | `DATA_SCOPE_VIOLATION` |
| `CAP-SC-020` | undeclared side effect | `SIDE_EFFECT_NOT_ALLOWED` |
| `CAP-SC-021` | missing budget | `BUDGET_MISSING` |
| `CAP-SC-022` | identity authority or direct M3 write | `LEASE_CONTRACT_VIOLATION` |
| `CAP-SC-023` | identical admitted inputs repeated | byte-equivalent result |
| `CAP-SC-024` | unrelated admitted record added | result unchanged |
| `CAP-SC-025` | fork old ref / new UNVERIFIED ref | `REVISION_MISMATCH` / `LEASE_NOT_ACTIVE` |

In-flight invalidation belongs to future Action Gate / execution-receipt research.

---

## 10. 🧱 P0 compatibility

```text
src/mentaury/contracts/primitives.py → AuthorityRef
P0 records lease_id + revision only
```

Forbidden without separate owner GO:

```text
adding grant fields to AuthorityRef
embedding lease payload in P0 envelopes
implicit resolve() from append or replay
rewriting historical hashes or projections
```

P0 events remain replayable without a registry.

---

## 11. 🔍 Freeze receipt

All freeze conditions were satisfied on PR #58:

- exact-head CI passed;
- complete diff inspected;
- correctness and adversarial passes recorded;
- malformed-registry and lifecycle ambiguities corrected;
- scenario/deny consistency enforced by tests;
- conversations resolved;
- `CURRENT_STATUS` retained NOT_IMPLEMENTED / NOT_AUTHORIZED;
- post-merge main CI passed.

```text
FROZEN_DOCS ≠ implementation GO
solo acceptance ≠ independent certification
```

---

## 12. 🚪 Future implementation gate

A future registry/resolver PR requires:

```text
separate explicit owner GO in docs/CURRENT_STATUS.md
+ bounded pure implementation
+ new Tier A exact-head review
+ deterministic / adversarial / metamorphic tests
+ preserved P0 replay compatibility
+ no network, ambient clock or mutable external authority
+ no Action Gate, tools, M3 or domain-runtime expansion
```

Issue #39 applies when a genuine independent reviewer/team exists. Until then,
solo review remains honest and attributable.

---

## 13. 🏁 Formula

```text
AuthorityRef stays (lease_id, revision)
Registry and record admission fail closed
Exact live-head lookup; no history walk
Digest excludes content_digest
Lifecycle consistency precedes lifecycle denial
Purpose / operation / scope are exact
Budgets fail closed
Fork/restore quarantines grants as UNVERIFIED
ALLOW executes nothing
Implementation remains unauthorized
```

### Related documents

- [`RESEARCH_INDEX.md`](RESEARCH_INDEX.md)
- [`POST_P0_ROADMAP_V0.1.md`](POST_P0_ROADMAP_V0.1.md)
- [`../CURRENT_STATUS.md`](../CURRENT_STATUS.md)
- [`../GOVERNANCE.md`](../GOVERNANCE.md)
