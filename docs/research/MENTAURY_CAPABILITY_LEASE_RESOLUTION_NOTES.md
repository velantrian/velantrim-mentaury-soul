# 🔐 Capability Lease Resolution — Contract Notes

```text
Статус:                       ADOPTED · RESEARCH_NOTES · NON_CANONICAL · DOCS_ONLY · NOT_IMPLEMENTED
Версия:                       0.2-draft
Дата:                         2026-08-07
Целевая фаза:                 POST_P0 / P1-001 (docs-first)
Runtime authority:            NONE
Truth authority:              NONE
Capability authority:         NONE
Canon modification authority: NONE
Прямая запись в M3:           FORBIDDEN
Implementation in src/:       NOT AUTHORIZED
```

> Этот документ — owner-adopted docs authority для P1-001 Capability Lease
> Resolution. Версия `0.2-draft` устраняет противоречия v0.1, но не считается
> frozen до отдельного independent review. `ADOPTED` относится только к
> docs-first направлению: lease registry / `resolve()` в `src/` не разрешены.
> Language policy: см. [`RESEARCH_INDEX.md`](RESEARCH_INDEX.md) — русский для
> narrative/context; English для identifiers, schemas, reason codes, algorithms
> и normative contract terms; при конфликте побеждают exact English contracts.

```text
Docs contract ≠ runtime permission
ALLOW decision ≠ action execution
AuthorityRef ≠ permission blob
P1-001 docs hardening ≠ P1-001 implementation
```

---

## 1. 🎯 Problem statement

В P0 уже существует:

```text
AuthorityRef
= capability_lease_id + capability_revision
```

Сегодня это обеспечивает provenance и equality checks, но не разрешение:

```text
✅ lease id / revision записываются в envelopes и linked records
✅ связанные записи могут проверять equality
❌ отсутствует exact registry lookup
❌ отсутствует lifecycle / expiry / revocation validation
❌ отсутствует purpose / operation / scope / side-effect validation
❌ отсутствует детерминированный fail-closed result
```

```text
Opaque authority reference
≠ enforceable permission grant
```

---

## 2. 🪞 Scope and non-claims

### In scope — docs only

- immutable Capability Lease record contract;
- exact live-head registry semantics;
- pure deterministic resolver contract;
- normative deny precedence;
- lifecycle and time semantics;
- typed exact purpose / operation / scope matching;
- explicit caller-supplied resource budgets;
- fork / restore quarantine semantics;
- named adversarial and boundary scenarios;
- authorization gate before any future `src/` work.

### Out of scope

```text
❌ changing AuthorityRef fields
❌ embedding grant data in EventEnvelope
❌ registry implementation
❌ resolver implementation
❌ network lookup
❌ ambient system clock
❌ Action Gate or Tool Receipt runtime
❌ tool execution or external side effects
❌ belief / identity / relationship mutation
❌ direct or indirect M3 write
❌ operator override inside resolve()
❌ Canon modification
❌ proving registry-snapshot authenticity inside resolve()
```

The resolver may validate the internal structure and digest of a supplied record,
but registry-snapshot provenance and authenticity remain a separate caller-side
boundary.

---

## 3. 📚 Vocabulary and typed inputs

```text
AuthorityRef
→ immutable reference: (lease_id, revision)

CapabilityLeaseRecord
→ immutable registry record carrying bounded grant data

RegistrySnapshot
→ immutable caller-supplied snapshot or explicit UNAVAILABLE marker

ActionIntent
→ exact requested purpose, operation, typed data scope and side effects

ResolutionBudget
→ caller-supplied resource ceilings; not a permission grant

ResolutionResult
→ ALLOW | DENY + one primary machine-readable reason + observations
```

Recommended language-neutral shapes:

```yaml
registry_snapshot:
  availability: "AVAILABLE"              # or UNAVAILABLE
  unavailable_reason: null
  registry_schema_version: 1
  live_heads:
    "CAP-...": 3                         # exactly one live revision per lease_id
  records:
    - capability_lease_record

action_intent:
  purpose_id: "PURPOSE-..."              # exact identifier
  operation_id: "OP-..."                 # exact identifier
  data_scope:
    - kind: "stream"
      identifier: "..."
  requested_side_effects: []              # exact set

resolution_budget:
  max_registry_lookups: 1
  max_canonical_bytes: "caller-supplied positive integer"
  max_scope_items: "caller-supplied positive integer"
```

The concrete upper ceilings remain reviewable before implementation GO, but the
units, absence of ambient defaults and fail-closed semantics are normative.

---

## 4. 🧾 Capability Lease record contract

```yaml
capability_lease:
  lease_id: "CAP-..."
  revision: 1
  supersedes_revision: null
  status: "ACTIVE"
  tool_id: null
  granted_by:
    actor_type: "..."
    actor_id: "..."
  purpose_id: "PURPOSE-..."
  allowed_operations: []
  data_scope:
    - kind: "stream"
      identifier: "..."
  allowed_side_effects: []
  not_before: "2026-08-07T00:00:00Z"
  expires_at: "2026-08-08T00:00:00Z"
  revocation_conditions: []
  revoked_at: null
  delegation_allowed: false
  branch_transfer_allowed: false
  audit_required: true
  identity_authority: "NONE"
  direct_m3_write: false
  content_digest: "sha256:..."
```

### 4.1 Record invariants

```text
lease_id is stable and non-empty
revision is a positive integer
revision 1 → supersedes_revision MUST be null
revision n > 1 → supersedes_revision MUST equal n - 1
no revision gaps or branches are valid in v0.1
one lease_id has exactly one live-head revision in a snapshot
purpose_id is an exact identifier, not free-form semantic text
data_scope contains typed exact identifiers
allowed_operations and allowed_side_effects use explicit closed sets
allowed_operations are unique and sorted by operation identifier
data_scope entries are unique and sorted by (kind, identifier)
allowed_side_effects are unique and sorted by side-effect identifier
requested set-like fields follow the same unique/sorted admission rules
expires_at MUST be present
not_before MUST be earlier than expires_at
delegation_allowed MUST default false
branch_transfer_allowed MUST default false
identity_authority MUST equal NONE
direct_m3_write MUST equal false
revoked_at MUST be non-null iff the record is REVOKED
```

The schema owns set normalization by rejecting duplicates and non-canonical
ordering. `MENTAURY_CANONICAL_JSON_V1` itself does not reorder arrays.

### 4.2 Exact digest domain

`content_digest` is never included in its own hash input.

```text
lease_digest_payload
= the complete admitted lease record
  with the top-level content_digest field omitted

canonical_bytes
= MENTAURY_CANONICAL_JSON_V1(lease_digest_payload)

content_digest
= "sha256:" + lowercase_hex(SHA-256(canonical_bytes))
```

Rules:

```text
Unicode normalization follows MENTAURY_CANONICAL_JSON_V1: NONE
Timestamp canonicalization follows P0-003: RFC3339 UTC Z
Schema-admitted set-like arrays are already unique and sorted
Other arrays remain ordered
A stored digest string is never trusted without recomputation
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
REVOKED is terminal and cannot be automatically restored.
SUPERSEDED is historical and cannot be resolved for a live grant.
UNVERIFIED cannot grant authority.
SUSPENDED cannot grant authority.
EXPIRED cannot grant authority.
Historical resolve-for-audit is outside P1-001.
```

### 5.1 Exact lookup

```text
1 exact lookup by AuthorityRef.lease_id
→ obtain snapshot live-head revision
→ AuthorityRef.revision MUST equal that live head
→ obtain that exact record
```

No revision walk, fallback, nearest-version selection or historical grant is
allowed. Historical records remain audit-readable only.

### 5.2 Expiry model

Expiry is always evaluated from caller-supplied `evaluated_at` and `expires_at`.
A materialized `EXPIRED` status is allowed only if consistent with time.

```text
valid temporal interval:
not_before <= evaluated_at < expires_at
```

If `status == EXPIRED` while `evaluated_at < expires_at`, the record is
contract-invalid. If an ACTIVE record reaches `evaluated_at >= expires_at`, the
resolver returns `LEASE_EXPIRED` without mutating the registry.

### 5.3 Fork / restore quarantine

Fork or restore never copies an ACTIVE grant as an ACTIVE live head in the
destination authority domain.

```text
source record remains immutable and audit-readable
→ destination registry creates a new revision
→ destination revision status = UNVERIFIED
→ supersedes_revision = prior revision
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
no belief / M3 / relationship mutation
no tool execution
no ambient operator override
```

---

## 7. 🚦 Normative deny precedence

The first matching failure is the only primary reason. Implementations may add
non-authoritative diagnostics, but they may not change the primary result.

| Order | Check | Primary DENY reason |
|---:|---|---|
| 1 | request shape / required fields admitted | `REQUEST_INVALID` |
| 2 | budget object present | `BUDGET_MISSING` |
| 3 | budget fields are admitted, non-negative and allow one exact lookup | `BUDGET_EXHAUSTED` |
| 4 | registry snapshot available | `REGISTRY_UNAVAILABLE` |
| 5 | exact `lease_id` exists | `UNKNOWN_LEASE` |
| 6 | snapshot has one valid live head and `AuthorityRef.revision` equals it | `REVISION_MISMATCH` |
| 7 | exact record canonical bytes fit `max_canonical_bytes` | `BUDGET_EXHAUSTED` |
| 8 | recomputed digest equals stored `content_digest` | `LEASE_DIGEST_MISMATCH` |
| 9 | record invariants / supersession chain / schema are valid | `LEASE_CONTRACT_VIOLATION` |
| 10 | revoked state or non-null `revoked_at` | `LEASE_REVOKED` |
| 11 | materialized or derived expiry | `LEASE_EXPIRED` |
| 12 | status is exactly ACTIVE | `LEASE_NOT_ACTIVE` |
| 13 | `evaluated_at >= not_before` | `NOT_YET_VALID` |
| 14 | exact `purpose_id` equality | `PURPOSE_MISMATCH` |
| 15 | exact operation membership | `OPERATION_NOT_ALLOWED` |
| 16 | requested and allowed scope counts fit `max_scope_items` | `BUDGET_EXHAUSTED` |
| 17 | requested typed scope is a subset of allowed typed scope | `DATA_SCOPE_VIOLATION` |
| 18 | requested side effects are a subset of allowed side effects | `SIDE_EFFECT_NOT_ALLOWED` |
| 19 | all checks pass | `ALLOW` |

Clarifications:

```text
Every row has exactly one primary result.
REGISTRY_UNAVAILABLE ≠ UNKNOWN_LEASE.
BUDGET_MISSING ≠ BUDGET_EXHAUSTED.
Revision ahead or behind live head → REVISION_MISMATCH.
Purpose compatibility in v0.1 = exact identifier equality.
Scope compatibility in v0.1 = exact typed-set containment.
Wildcards, hierarchy expansion and semantic similarity are forbidden.
```

---

## 8. 📤 ResolutionResult contract

```yaml
resolution_result:
  decision: "DENY"                       # or ALLOW
  primary_reason: "REVISION_MISMATCH"
  lease_id: "CAP-..."
  requested_revision: 2
  observed_live_revision: 3
  observed_status: "ACTIVE"
  observed_digest: "sha256:..."
  evaluated_at: "2026-08-07T12:00:00Z"
  resolver_contract_version: "P1-001-v0.2"
```

For failures before record observation, observed fields are null. Results must
not contain copied permission material that could be reused as authority.

```text
ALLOW
≠ Tool Receipt
≠ Action Gate approval
≠ execution success
≠ truth
≠ identity authority
```

---

## 9. 🧪 Resolver scenario contract

| ID | Scenario | Expected primary result |
|---|---|---|
| CAP-SC-001 | unavailable registry snapshot | `REGISTRY_UNAVAILABLE` |
| CAP-SC-002 | unknown `lease_id` | `UNKNOWN_LEASE` |
| CAP-SC-003 | requested revision behind live head | `REVISION_MISMATCH` |
| CAP-SC-004 | requested revision ahead of live head | `REVISION_MISMATCH` |
| CAP-SC-005 | forged or stale `content_digest` | `LEASE_DIGEST_MISMATCH` |
| CAP-SC-006 | malformed supersession chain | `LEASE_CONTRACT_VIOLATION` |
| CAP-SC-007 | revoked lease | `LEASE_REVOKED` |
| CAP-SC-008 | active record at or after `expires_at` | `LEASE_EXPIRED` |
| CAP-SC-009 | suspended / proposed / superseded / unverified lease | `LEASE_NOT_ACTIVE` |
| CAP-SC-010 | before `not_before` | `NOT_YET_VALID` |
| CAP-SC-011 | exact purpose mismatch | `PURPOSE_MISMATCH` |
| CAP-SC-012 | operation not in closed allow-list | `OPERATION_NOT_ALLOWED` |
| CAP-SC-013 | typed data-scope violation | `DATA_SCOPE_VIOLATION` |
| CAP-SC-014 | undeclared side effect | `SIDE_EFFECT_NOT_ALLOWED` |
| CAP-SC-015 | missing budget object | `BUDGET_MISSING` |
| CAP-SC-016 | canonical bytes / lookup / scope exceed budget | `BUDGET_EXHAUSTED` |
| CAP-SC-017 | record has `direct_m3_write=true` or identity authority | `LEASE_CONTRACT_VIOLATION` |
| CAP-SC-018 | restored/forked record presented as old ACTIVE revision | `REVISION_MISMATCH`; new UNVERIFIED ref → `LEASE_NOT_ACTIVE` |
| CAP-SC-019 | same admitted inputs repeated | byte-equivalent result |
| CAP-SC-020 | unrelated registry record added | result unchanged |

### Execution-boundary scenario deliberately excluded

A lease that becomes invalid after an external operation starts is an Action
Gate / execution-receipt concern, not a pure resolver concern. The historical
`EXO-SC-002` requirement is retained as a future cross-boundary research item,
but it is not part of the P1-001 resolver test suite and cannot authorize
execution runtime.

---

## 10. 🧱 P0 compatibility boundary

Already present in `main` and unchanged:

```text
src/mentaury/contracts/primitives.py → AuthorityRef
P0 envelopes / storage / redaction / idempotency
→ record and compare capability_lease_id + revision
```

Forbidden without a separate owner GO:

```text
❌ adding grant fields to AuthorityRef
❌ embedding lease payload in P0 envelopes
❌ calling resolve() implicitly from append/replay paths
❌ changing historical event hashes or canonical projections
```

P0 events may continue recording AuthorityRef without invoking the future
resolver. Resolution is a new boundary, not a retroactive reinterpretation of
P0 history.

---

## 11. 🔍 Docs-freeze and implementation authorization gates

P1-001 docs may be declared frozen only when:

1. this draft receives independent exact-head review;
2. deny precedence is accepted without contradictory tables elsewhere;
3. exact lookup / no-history-walk semantics are consistent across roadmap;
4. digest, time, fork/restore and supersession semantics are accepted;
5. named scenarios CAP-SC-001…020 are internally consistent;
6. `CURRENT_STATUS` still says resolver implementation is not authorized.

Any future implementation PR additionally requires:

```text
explicit owner GO in CURRENT_STATUS
+ minimal pure resolver scope
+ protected-path independent code review
+ deterministic / adversarial / metamorphic tests
+ no network / clock / LLM / state mutation dependency
```

---

## 12. 🏁 Final formula

```text
AuthorityRef remains (lease_id, revision)
Lease record carries bounded expiring revocable grant data
Registry snapshot is explicit and may be UNAVAILABLE
Resolver uses exact live-head lookup with no history walk
Digest is recomputed over canonical record bytes excluding content_digest
Purpose, operation and typed scope are exact in v0.1
Budgets are explicit and distinguish missing from exhausted
Fork / restore quarantines inherited grants as UNVERIFIED
ALLOW does not execute anything and grants no truth or identity authority
Docs remain non-runtime until explicit owner GO
```

### Related documents

- [`RESEARCH_INDEX.md`](RESEARCH_INDEX.md)
- [`POST_P0_ROADMAP_V0.1.md`](POST_P0_ROADMAP_V0.1.md)
- [`MENTAURY_IDENTITY_CONTINUITY_AND_RELATIONAL_ARCHITECTURE_NOTES.md`](MENTAURY_IDENTITY_CONTINUITY_AND_RELATIONAL_ARCHITECTURE_NOTES.md)
- [`../P0_002_ENVELOPE_CONTRACTS.md`](../P0_002_ENVELOPE_CONTRACTS.md)
- [`../P0_003_CANONICAL_JSON.md`](../P0_003_CANONICAL_JSON.md)
- [`../CURRENT_STATUS.md`](../CURRENT_STATUS.md)
