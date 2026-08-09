# 🔐 Capability Lease Resolution — Contract Notes

```text
Status:                       ADOPTED DIRECTION · CONTRACT_DRAFT · DOCS_ONLY
Version:                      0.2-draft
Date:                         2026-08-09
Target milestone:             POST_P0 / P1-001
Runtime authority:            NONE
Truth authority:              NONE
Identity authority:           NONE
Capability authority:         NONE
Canon modification authority: NONE
Direct or indirect M3 write:  FORBIDDEN
Implementation in src/:       NOT AUTHORIZED
Review mode:                  SOLO_MAINTAINER · TIER_A
```

> Этот документ задаёт docs-first контракт P1-001 Capability Lease Resolution.
> Он не создаёт registry, resolver, permission grant, Action Gate или runtime.
> Текущий review выполняется по `docs/GOVERNANCE.md`: exact-head CI и два
> различимых maintainer-прохода без заявления independent human assurance.

```text
Docs contract ≠ runtime permission
AuthorityRef ≠ permission blob
Resolution ALLOW ≠ action execution
Maintainer review ≠ independent human review
P1-001 docs hardening ≠ P1-001 implementation
```

---

## 1. 🎯 Problem statement

P0 уже содержит неизменяемую ссылку:

```text
AuthorityRef
= capability_lease_id + capability_revision
```

Сегодня она обеспечивает provenance и equality checks, но сама по себе не
доказывает существование или действительность grant:

```text
✅ lease id / revision записываются в envelopes и linked records
✅ связанные записи могут проверять exact equality
❌ отсутствует exact registry lookup
❌ отсутствует expiry / revocation / lifecycle validation
❌ отсутствует purpose / operation / scope validation
❌ отсутствует deterministic fail-closed ResolutionResult
```

```text
Opaque authority reference
≠ enforceable permission grant
```

---

## 2. 🪞 Scope and non-claims

### 2.1 In scope — docs only

- immutable `CapabilityLeaseRecord`;
- explicit caller-supplied `RegistrySnapshot`;
- versioned admission contracts for snapshot and record;
- exact live-head lookup without history walking;
- pure deterministic resolver contract;
- canonical digest domain;
- lifecycle and caller-supplied time semantics;
- exact purpose, operation, typed scope and side-effect matching;
- explicit resource budgets;
- one normative deny-precedence table;
- fork / restore quarantine;
- named deterministic and adversarial scenarios;
- authorization gate before any future `src/` work.

### 2.2 Out of scope

```text
❌ changing AuthorityRef fields
❌ embedding grant data in EventEnvelope
❌ registry implementation
❌ resolver implementation
❌ network lookup
❌ ambient system clock
❌ environment-variable authority
❌ Tool Receipt or Action Gate runtime
❌ tool execution or external side effects
❌ belief / identity / relationship mutation
❌ direct or indirect M3 write
❌ operator override inside resolve()
❌ Canon modification
❌ proving registry-snapshot provenance inside resolve()
```

Registry-snapshot provenance and authenticity remain an upstream caller-side
boundary. The pure resolver validates the supplied snapshot's admitted structure
and records, but cannot establish who produced the snapshot or whether the caller
was entitled to supply it.

---

## 3. 📚 Typed inputs

```text
AuthorityRef
→ immutable reference: (lease_id, revision)

CapabilityLeaseRecord
→ immutable bounded grant record

RegistrySnapshot
→ immutable caller-supplied snapshot or explicit UNAVAILABLE marker

ActionIntent
→ exact purpose, operation, typed data scope and requested side effects

ResolutionBudget
→ caller-supplied resource ceilings; never a permission grant

ResolutionResult
→ ALLOW | DENY + one primary reason + bounded observations
```

Recommended language-neutral shape:

```yaml
registry_snapshot:
  availability: "AVAILABLE"              # or UNAVAILABLE
  unavailable_reason: null
  registry_schema_version: 1
  live_heads:
    "CAP-...": 3                         # one live revision per lease_id
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

All values must be explicit. No ambient default may expand permission.

### 3.1 RegistrySnapshot admission

An `AVAILABLE` snapshot must be admitted before lease lookup:

```text
registry_schema_version is supported and exact
availability is AVAILABLE or UNAVAILABLE
UNAVAILABLE carries no grantable records
live_heads is a bounded map of unique non-empty lease ids to positive revisions
records are uniquely indexed by (lease_id, revision)
no duplicate record keys exist
one live-head entry exists at most once per lease_id
live_heads points to an existing record with the same lease_id and revision
record count and map sizes are bounded by the caller contract
unknown snapshot fields are rejected
```

Malformed snapshot structure returns `REGISTRY_CONTRACT_VIOLATION`. This reason
is distinct from:

```text
REGISTRY_UNAVAILABLE → no available snapshot was supplied
UNKNOWN_LEASE        → admitted snapshot has no requested lease id
REVISION_MISMATCH    → requested revision differs from admitted live head
```

The resolver does not repair, normalize, merge or infer registry state.

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
  data_scope:
    - kind: "stream"
      identifier: "..."
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

Before digest or semantic authorization, the exact selected record is admitted
against a versioned schema:

```text
unknown fields                     → reject
missing required fields            → reject
wrong scalar / collection type     → reject
duplicate set-like members          → reject
non-canonical set ordering          → reject
invalid RFC3339 UTC Z timestamp     → reject
non-positive revision               → reject
record key differs from lookup key  → reject
oversized record                    → BUDGET_EXHAUSTED
```

Admission failure returns `LEASE_CONTRACT_VIOLATION`. Admission is distinct from
authorization: an admitted record may still be denied.

`max_record_bytes` is evaluated over the bounded serialized record supplied by
the admitted snapshot before digest recomputation. The caller-side parser must
already enforce an outer input-size ceiling so malformed input cannot force an
unbounded parse.

### 4.2 Record invariants

```text
lease_id is stable and non-empty
revision is a positive integer
revision 1 → supersedes_revision MUST be null
revision n > 1 → supersedes_revision MUST equal n - 1
no revision gaps or branches are valid in v0.1
purpose_id is an exact identifier, not semantic free text
allowed_operations are unique and sorted
authorized side-effect identifiers are unique and sorted
data_scope entries are unique and sorted by (kind, identifier)
not_before MUST be earlier than expires_at
expires_at MUST be present
delegation_allowed MUST default false
branch_transfer_allowed MUST default false
identity_authority MUST equal NONE
direct_m3_write MUST equal false
revoked_at MUST be non-null iff status is REVOKED
```

`MENTAURY_CANONICAL_JSON_V1` does not reorder arrays. Set-like normalization is
therefore a schema-admission responsibility, not a hashing side effect.

### 4.3 Exact digest domain

`content_digest` is excluded from its own hash input:

```text
lease_digest_payload
= complete admitted CapabilityLeaseRecord
  with the top-level content_digest field omitted

canonical_bytes
= MENTAURY_CANONICAL_JSON_V1(lease_digest_payload)

content_digest
= "sha256:" + lowercase_hex(SHA-256(canonical_bytes))
```

```text
Unicode normalization → NONE, as required by P0-003
Timestamps            → canonical RFC3339 UTC Z
Set-like arrays        → already unique and sorted by schema admission
Other arrays           → order-preserving
Stored digest          → never trusted without recomputation
```

---

## 5. 🔄 Lifecycle and live-head semantics

Persisted states:

```text
PROPOSED
ACTIVE
SUSPENDED
REVOKED
EXPIRED
SUPERSEDED
UNVERIFIED
```

Normative rules:

```text
Only ACTIVE may reach the grant path.
REVOKED is terminal.
SUPERSEDED is historical and cannot grant live authority.
UNVERIFIED cannot grant authority.
SUSPENDED cannot grant authority.
EXPIRED cannot grant authority.
Historical resolve-for-audit is outside P1-001.
```

### 5.1 Exact lookup

```text
one exact lookup by AuthorityRef.capability_lease_id
→ obtain the admitted snapshot live-head revision
→ AuthorityRef.capability_revision MUST equal the live head
→ obtain exactly the record indexed by (lease_id, revision)
```

No revision walk, fallback, nearest-version selection, wildcard lease lookup or
historical grant is allowed.

### 5.2 Time and lifecycle consistency

The resolver receives `evaluated_at` from the caller and never reads the system
clock.

```text
valid ACTIVE interval:
not_before <= evaluated_at < expires_at
```

Lifecycle consistency is checked before lifecycle denial:

```text
status EXPIRED while evaluated_at < expires_at
→ LEASE_CONTRACT_VIOLATION

status ACTIVE while evaluated_at >= expires_at
→ LEASE_EXPIRED

status REVOKED with revoked_at null
or non-REVOKED with revoked_at non-null
→ LEASE_CONTRACT_VIOLATION
```

The resolver never materializes a new state or mutates the registry.

### 5.3 Fork / restore quarantine

Fork or restore must not preserve an ACTIVE live grant in a destination authority
domain:

```text
source record remains immutable and audit-readable
→ destination registry creates a new revision
→ destination revision status = UNVERIFIED
→ old AuthorityRef fails REVISION_MISMATCH in destination
→ new AuthorityRef to UNVERIFIED fails LEASE_NOT_ACTIVE
```

A new ACTIVE revision requires explicit revalidation or re-issuance outside the
resolver. `branch_transfer_allowed=false` remains the default.

---

## 6. ⚙️ Pure resolver contract

```text
resolve(
  registry_snapshot,
  authority_ref,
  action_intent,
  evaluated_at,
  resolution_budget
) → ResolutionResult
```

Required properties:

```text
pure
fail-closed
deterministic for identical admitted inputs
no network I/O
no system-clock read
no environment-variable authority
no registry mutation
no event append
no belief / identity / relationship / M3 mutation
no tool execution
no ambient operator override
```

---

## 7. 🚦 Normative deny precedence

The first matching failure determines the single primary reason. Diagnostics may
add bounded observations but may not replace the primary reason.

| Order | Check | Primary result |
|---:|---|---|
| 1 | request shape and required fields admitted | `REQUEST_INVALID` |
| 2 | budget object present | `BUDGET_MISSING` |
| 3 | budget values admitted and permit one exact lookup | `BUDGET_EXHAUSTED` |
| 4 | registry snapshot available | `REGISTRY_UNAVAILABLE` |
| 5 | registry snapshot admitted by exact versioned schema | `REGISTRY_CONTRACT_VIOLATION` |
| 6 | exact `lease_id` exists | `UNKNOWN_LEASE` |
| 7 | requested revision equals the admitted live head | `REVISION_MISMATCH` |
| 8 | exact record bytes fit `max_record_bytes` | `BUDGET_EXHAUSTED` |
| 9 | selected record admitted by exact versioned schema | `LEASE_CONTRACT_VIOLATION` |
| 10 | recomputed digest equals stored `content_digest` | `LEASE_DIGEST_MISMATCH` |
| 11 | semantic invariants and supersession chain are valid | `LEASE_CONTRACT_VIOLATION` |
| 12 | lifecycle status and timestamps are mutually consistent | `LEASE_CONTRACT_VIOLATION` |
| 13 | revoked state | `LEASE_REVOKED` |
| 14 | materialized or derived expiry | `LEASE_EXPIRED` |
| 15 | status is exactly ACTIVE | `LEASE_NOT_ACTIVE` |
| 16 | `evaluated_at >= not_before` | `NOT_YET_VALID` |
| 17 | exact `purpose_id` equality | `PURPOSE_MISMATCH` |
| 18 | exact operation membership | `OPERATION_NOT_ALLOWED` |
| 19 | requested and allowed scope counts fit `max_scope_items` | `BUDGET_EXHAUSTED` |
| 20 | requested typed scope is a subset of allowed typed scope | `DATA_SCOPE_VIOLATION` |
| 21 | requested side effects are a subset of allowed side effects | `SIDE_EFFECT_NOT_ALLOWED` |
| 22 | all checks pass | `ALLOW` |

```text
REGISTRY_UNAVAILABLE ≠ REGISTRY_CONTRACT_VIOLATION
REGISTRY_CONTRACT_VIOLATION ≠ UNKNOWN_LEASE
BUDGET_MISSING ≠ BUDGET_EXHAUSTED
revision behind or ahead of live head → REVISION_MISMATCH
purpose compatibility                → exact identifier equality
scope compatibility                  → exact typed-set containment
wildcards / hierarchy expansion / semantic similarity → forbidden in v0.1
```

---

## 8. 📤 ResolutionResult

```yaml
resolution_result:
  decision: "DENY"                       # or ALLOW
  primary_reason: "REVISION_MISMATCH"
  lease_id: "CAP-..."
  requested_revision: 2
  observed_live_revision: 3
  observed_status: "ACTIVE"
  observed_digest: "sha256:..."
  evaluated_at: "2026-08-09T12:00:00Z"
  resolver_contract_version: "P1-001-v0.2"
```

For failures before record observation, observed record fields are null. For a
registry-contract failure, bounded registry diagnostics may be present but no
untrusted permission material may be echoed. The result must never contain a
permission copy reusable as authority.

```text
ALLOW
≠ Tool Receipt
≠ Action Gate approval
≠ execution success
≠ objective truth
≠ identity authority
```

---

## 9. 🧪 Scenario contract

| ID | Scenario | Expected primary result |
|---|---|---|
| `CAP-SC-001` | unavailable registry snapshot | `REGISTRY_UNAVAILABLE` |
| `CAP-SC-002` | unsupported registry schema version | `REGISTRY_CONTRACT_VIOLATION` |
| `CAP-SC-003` | duplicate record key or live head references missing record | `REGISTRY_CONTRACT_VIOLATION` |
| `CAP-SC-004` | unknown lease id in admitted registry | `UNKNOWN_LEASE` |
| `CAP-SC-005` | requested revision behind live head | `REVISION_MISMATCH` |
| `CAP-SC-006` | requested revision ahead of live head | `REVISION_MISMATCH` |
| `CAP-SC-007` | oversized exact record | `BUDGET_EXHAUSTED` |
| `CAP-SC-008` | unknown field or malformed lease schema | `LEASE_CONTRACT_VIOLATION` |
| `CAP-SC-009` | forged or stale digest | `LEASE_DIGEST_MISMATCH` |
| `CAP-SC-010` | malformed supersession chain | `LEASE_CONTRACT_VIOLATION` |
| `CAP-SC-011` | premature materialized `EXPIRED` status | `LEASE_CONTRACT_VIOLATION` |
| `CAP-SC-012` | revoked lease | `LEASE_REVOKED` |
| `CAP-SC-013` | active record at or after expiry | `LEASE_EXPIRED` |
| `CAP-SC-014` | suspended / proposed / superseded / unverified | `LEASE_NOT_ACTIVE` |
| `CAP-SC-015` | before `not_before` | `NOT_YET_VALID` |
| `CAP-SC-016` | purpose mismatch | `PURPOSE_MISMATCH` |
| `CAP-SC-017` | operation not allowed | `OPERATION_NOT_ALLOWED` |
| `CAP-SC-018` | scope budget exceeded | `BUDGET_EXHAUSTED` |
| `CAP-SC-019` | typed data-scope violation | `DATA_SCOPE_VIOLATION` |
| `CAP-SC-020` | undeclared side effect | `SIDE_EFFECT_NOT_ALLOWED` |
| `CAP-SC-021` | missing budget | `BUDGET_MISSING` |
| `CAP-SC-022` | identity authority or direct M3 write present | `LEASE_CONTRACT_VIOLATION` |
| `CAP-SC-023` | same admitted inputs repeated | byte-equivalent result |
| `CAP-SC-024` | unrelated admitted registry record added | result unchanged |
| `CAP-SC-025` | old ACTIVE ref after fork / new UNVERIFIED ref | `REVISION_MISMATCH` / `LEASE_NOT_ACTIVE` |

A lease becoming invalid after an external operation starts belongs to future
Action Gate / execution-receipt research, not to this pure resolver contract.

---

## 10. 🧱 P0 compatibility boundary

Already present in `main` and unchanged:

```text
src/mentaury/contracts/primitives.py → AuthorityRef
P0 envelopes / storage / redaction / idempotency
→ record and compare capability_lease_id + capability_revision
```

Forbidden without a separate owner GO:

```text
❌ adding grant fields to AuthorityRef
❌ embedding lease payload in P0 envelopes
❌ calling resolve() implicitly from append or replay paths
❌ changing historical event hashes or canonical projections
```

P0 events remain replayable without a registry. P1-001 is a new boundary and
must not retroactively reinterpret P0 history.

---

## 11. 🔍 Docs-freeze gate

The draft may be marked `FROZEN_DOCS` only after all of the following are recorded
on one exact head:

1. required CI passes;
2. complete final diff is inspected;
3. correctness pass confirms internal consistency across this document, roadmap
   and research index;
4. adversarial pass checks fail-closed ordering, authority boundaries, digest,
   lifecycle, budgets, fork/restore and non-claims;
5. all conversations are resolved;
6. scenario table and deny table are non-contradictory;
7. `docs/CURRENT_STATUS.md` still states `NOT_IMPLEMENTED / NOT_AUTHORIZED`;
8. maintainer records `ACCEPTED_FOR_MERGE` under `docs/GOVERNANCE.md`.

```text
FROZEN_DOCS ≠ implementation GO
maintainer acceptance ≠ independent certification
```

---

## 12. 🚪 Future implementation authorization

A future PR adding registry or resolver code requires a separate explicit owner
amendment in `docs/CURRENT_STATUS.md` and a new Tier A review. Minimum conditions:

```text
FROZEN_DOCS
+ explicit bounded owner GO for P1-001 only
+ pure minimal implementation scope
+ deterministic / adversarial / metamorphic tests
+ no network, ambient clock, LLM or mutable external authority dependency
+ no Action Gate, tool execution, M3 or domain-runtime expansion
+ rollback / compatibility evidence
```

When a genuine independent reviewer or team exists, the repository-wide
transition described in issue #39 applies to subsequent protected changes. The
current absence of that reviewer is not a blocker to docs work under solo mode.

---

## 13. 🏁 Final formula

```text
AuthorityRef remains (lease_id, revision)
Lease record carries bounded, expiring, revocable grant data
Registry snapshot is explicit and may be UNAVAILABLE
Registry and record have separate fail-closed admission contracts
Resolver uses exact live-head lookup with no history walk
Schema admission precedes digest and semantic authorization
Digest excludes its own content_digest field
Lifecycle consistency precedes revoked / expired / active denial
Purpose, operation and typed scope are exact in v0.1
Budgets are explicit and fail closed
Fork / restore quarantines inherited grants as UNVERIFIED
ALLOW executes nothing and grants no truth or identity authority
Docs remain non-runtime until explicit owner GO
```

### Related documents

- [`RESEARCH_INDEX.md`](RESEARCH_INDEX.md)
- [`POST_P0_ROADMAP_V0.1.md`](POST_P0_ROADMAP_V0.1.md)
- [`MENTAURY_IDENTITY_CONTINUITY_AND_RELATIONAL_ARCHITECTURE_NOTES.md`](MENTAURY_IDENTITY_CONTINUITY_AND_RELATIONAL_ARCHITECTURE_NOTES.md)
- [`../P0_002_ENVELOPE_CONTRACTS.md`](../P0_002_ENVELOPE_CONTRACTS.md)
- [`../P0_003_CANONICAL_JSON.md`](../P0_003_CANONICAL_JSON.md)
- [`../CURRENT_STATUS.md`](../CURRENT_STATUS.md)
- [`../GOVERNANCE.md`](../GOVERNANCE.md)
