# 🔐 Capability Lease Resolution — Research Notes

```text
Статус:                       ADOPTED · RESEARCH_NOTES · NON_CANONICAL · DOCS_ONLY · NOT_IMPLEMENTED
Версия:                       0.1
Дата:                         2026-08-07
Целевая фаза:                 POST_P0 / P1-001 (docs-first)
Runtime authority:            NONE
Truth authority:              NONE
Capability authority:         NONE
Canon modification authority: NONE
Прямая запись в M3:           FORBIDDEN
Implementation in src/:       NOT AUTHORIZED
```

> Этот документ — **owner-adopted** docs authority для P1-001 Capability
> Lease Resolution (см. [`CURRENT_STATUS.md`](../CURRENT_STATUS.md) и
> [`POST_P0_ROADMAP_V0.1.md`](POST_P0_ROADMAP_V0.1.md)). Он разворачивает
> stub Identity Continuity §12.3 в полный **resolution contract**.
> `ADOPTED` относится только к docs-контракту: lease registry / `resolve()`
> в `src/` **не** авторизованы, runtime permissions этим документом
> **не** выдаются.

---

## 1. 🎯 Проблема

В P0 `AuthorityRef` уже существует:

```text
AuthorityRef
= capability_lease_id + capability_revision
```

Фактически сегодня:

```text
✅ запись lease_id / revision на envelopes и linked records
✅ equality-check между связанными записями (например redaction ↔ evidence)
❌ lookup в registry
❌ проверка expiration / revocation
❌ проверка purpose / data_scope / allowed_operations
❌ fail-closed deny с machine-readable reason
```

Следствие (зафиксировано аудитом 2026-08-06):

```text
capability_lease_id сейчас
= opaque provenance string
≠ enforceable permission grant
```

---

## 2. 🪞 Scope и Non-claims

### ✅ В scope (docs)

- контракт записи Capability Lease;
- lifecycle states;
- pure resolution algorithm и rejection codes;
- fork / restore → `UNVERIFIED`;
- adversarial / scenario contracts;
- граница с Tool Receipt и Action Gate (**без** их runtime);
- критерии будущего Evidence Gate перед `src/` GO.

### ❌ Non-claims

```text
❌ этот документ выдаёт permissions
❌ AuthorityRef становится self-authenticating blob
❌ Tool availability = personal ability
❌ Exo-Cortex expansion = identity expansion
❌ Action Gate execution authorized
❌ domain runtime authorized
❌ Canon v0.1 изменён
❌ P1-001 ✅ Implemented
```

---

## 3. 📚 Vocabulary

```text
AuthorityRef
→ ссылка на внешнюю lease-запись (id + revision)

Capability Lease record
→ registry-запись о выданном, ограниченном праве

Resolution request
→ (AuthorityRef, action_intent, time, budgets, registry_snapshot)

Resolution result
→ ALLOW | DENY + reason_code + observed lease revision/status

Tool Receipt
→ доказательство попытки/результата tool operation (отдельный трек)

Action Gate
→ будущий runtime-путь внешних side effects (НЕ авторизован здесь)
```

```text
AuthorityRef ≠ permission copy
Lease record ≠ truth
ALLOW ≠ identity authority
ALLOW ≠ M3 write
ALLOW ≠ objective fact
```

---

## 4. 🧾 Lease record contract

Расширение Identity Continuity §12.3:

```yaml
capability_lease:
  lease_id: "CAP-..."                    # стабильный id
  revision: 1                            # монотонная ревизия записи
  status: "ACTIVE"                       # см. §5
  tool_id: "..."                         # optional; null = non-tool grant
  granted_by:                            # ActorRef
    actor_type: "..."
    actor_id: "..."
  purpose: "..."                         # обязательная цель
  allowed_operations: []                 # закрытый список операций
  data_scope: []                         # допустимые stream/data классы
  allowed_side_effects: []               # пусто = side effects запрещены
  not_before: "RFC3339 / profile time"
  expires_at: "RFC3339 / profile time"   # обязателен; open-ended FORBIDDEN
  revocation_conditions: []
  revoked_at: null
  delegation_allowed: false              # default false
  branch_transfer_allowed: false         # default false
  audit_required: true
  identity_authority: "NONE"             # всегда NONE в v0.1
  direct_m3_write: false                 # всегда false в v0.1
  supersedes_revision: null              # если rotate
  content_digest: "sha256:..."           # canonical digest записи
```

Инварианты записи:

```text
expires_at MUST be present
identity_authority MUST be NONE (v0.1)
direct_m3_write MUST be false (v0.1)
delegation_allowed default false
branch_transfer_allowed default false
revision increments only via superseding write
```

---

## 5. 🔄 Lifecycle states

```text
PROPOSED     → записан, ещё не действует
ACTIVE       → может пройти resolution (если все checks ok)
SUSPENDED    → временно недействителен
REVOKED      → окончательно отозван
EXPIRED      → время вышло (может вычисляться; см. ниже)
SUPERSEDED   → заменён большей revision
UNVERIFIED   → унаследован после fork/restore; требует revalidation
```

Правила:

```text
EXPIRED может быть derived-at-resolution от expires_at
  или материализован registry-переходом — профиль обязан выбрать одно
  и применять детерминированно.

Fork / restore:
  inherited ACTIVE|SUSPENDED claims → UNVERIFIED
  external side effects FORBIDDEN until revalidation or new lease.

SUPERSEDED:
  AuthorityRef.revision must match the live head unless
  profile explicitly allows historical resolve-for-audit (default: NO).
```

---

## 6. ⚙️ Resolution algorithm (docs)

Pure function:

```text
resolve(
  registry_snapshot,
  authority_ref,          # lease_id + revision
  action_intent,          # purpose, operation, data_scope, side_effects?
  now,
  budgets
) → ResolutionResult
```

### 6.1 Ordered checks (fail-closed, first match wins)

| # | Check | DENY reason |
|---|---|---|
| 1 | budgets present and not exhausted | `BUDGET_EXHAUSTED` |
| 2 | `lease_id` exists in snapshot | `UNKNOWN_LEASE` |
| 3 | lease status ∈ {ACTIVE} for grant path | `LEASE_NOT_ACTIVE` (+ status) |
| 4 | `authority_ref.revision == lease.revision` | `REVISION_MISMATCH` |
| 5 | `now >= not_before` | `NOT_YET_VALID` |
| 6 | `now < expires_at` | `LEASE_EXPIRED` |
| 7 | `revoked_at is null` | `LEASE_REVOKED` |
| 8 | `action_intent.purpose` compatible with `lease.purpose` | `PURPOSE_MISMATCH` |
| 9 | operation ∈ `allowed_operations` | `OPERATION_NOT_ALLOWED` |
| 10 | data targets ⊆ `data_scope` | `DATA_SCOPE_VIOLATION` |
| 11 | requested side effects ⊆ `allowed_side_effects` | `SIDE_EFFECT_NOT_ALLOWED` |
| 12 | `identity_authority == NONE` и `direct_m3_write == false` | `LEASE_CONTRACT_VIOLATION` |
| 13 | canonical `content_digest` matches snapshot bytes | `LEASE_DIGEST_MISMATCH` |

Если все checks проходят → `ALLOW` с echo `lease_id`, `revision`, `content_digest`.

### 6.2 Обязательные свойства

```text
No registry → DENY (UNKNOWN_LEASE / registry unavailable)
No ambient “operator override” inside resolve()
No network I/O inside resolve()
No mutation of registry or domain state inside resolve()
Deterministic on identical inputs
```

### 6.3 Связь с P0

```text
P0 events MAY continue to RECORD AuthorityRef without calling resolve()
P0 equality-checks remain valid provenance hygiene
Calling resolve() is a NEW, separately authorized boundary
```

---

## 7. 🌿 Fork / restore / migration

```text
After fork or restore:
  any inherited lease claim status → UNVERIFIED
  resolve(UNVERIFIED) → DENY (LEASE_NOT_ACTIVE / UNVERIFIED)
  revalidation OR new lease issuance required before external effects
```

Migration профиля:

```text
Registry schema changes MUST bump an explicit registry schema version
Old snapshots remain readable for audit
Live grants require re-issue or documented migrate-and-revalidate procedure
```

---

## 8. 🧪 Adversarial / scenario contracts

Минимум для docs freeze (имена стабильны; реализация тестов — только после GO):

| ID | Сценарий | Ожидание |
|---|---|---|
| CAP-SC-001 | unknown `lease_id` | `UNKNOWN_LEASE` |
| CAP-SC-002 | revision behind live head | `REVISION_MISMATCH` |
| CAP-SC-003 | revision ahead of registry | `REVISION_MISMATCH` / `UNKNOWN_LEASE` |
| CAP-SC-004 | expired by `expires_at` | `LEASE_EXPIRED` |
| CAP-SC-005 | revoked lease | `LEASE_REVOKED` |
| CAP-SC-006 | suspended lease | `LEASE_NOT_ACTIVE` |
| CAP-SC-007 | purpose mismatch | `PURPOSE_MISMATCH` |
| CAP-SC-008 | operation not in allow-list | `OPERATION_NOT_ALLOWED` |
| CAP-SC-009 | data_scope violation | `DATA_SCOPE_VIOLATION` |
| CAP-SC-010 | undeclared side effect | `SIDE_EFFECT_NOT_ALLOWED` |
| CAP-SC-011 | forged content_digest | `LEASE_DIGEST_MISMATCH` |
| CAP-SC-012 | lease after fork still ACTIVE claim | must be `UNVERIFIED` → DENY |
| CAP-SC-013 | missing caller budget | `BUDGET_EXHAUSTED` / reject |
| CAP-SC-014 | lease with `direct_m3_write=true` | `LEASE_CONTRACT_VIOLATION` |
| EXO-SC-002 | lease becomes invalid during operation | deny further effects; receipt = DENIED/FAILED |

`EXO-SC-002` унаследован из Identity Continuity; здесь подтверждается как
обязательный cross-doc scenario.

---

## 9. 🧱 P0 substrate touchpoints

Уже в `main` (не ломать без отдельного GO):

```text
src/mentaury/contracts/primitives.py  → AuthorityRef
envelope / storage / redaction / idempotency
→ persist + equality of capability_lease_id
```

Запрещено этим docs-треком:

```text
❌ трактовать непустой capability_lease_id как ALLOW
❌ вшивать permission blob в EventEnvelope
❌ добавлять silent resolve() в append path без owner GO
```

---

## 10. 🚪 Evidence Gate для будущего runtime PR

До authorization implementation PR owner должен увидеть:

1. этот документ frozen + independent review;
2. registry schema + pure resolver design review;
3. suite, покрывающий CAP-SC-001…014 (и EXO-SC-002);
4. явную запись в `CURRENT_STATUS`: implementation authorized;
5. сохранение `identity_authority=NONE`, `direct_m3_write=false`.

```text
Docs exist ≠ resolver may merge
Tests sketched ≠ runtime safe
```

---

## 11. 🚫 Не принимается этим документом

```text
❌ open-ended leases without expires_at
❌ delegation_allowed=true by default
❌ branch_transfer_allowed=true by default
❌ identity_authority other than NONE (v0.1)
❌ direct M3 write via lease
❌ Action Gate auto-pass from ALLOW
❌ operator ambient override inside resolve()
❌ marking P1-001 Implemented without code
❌ Canon modification
```

---

## 12. 🏁 Итоговая формула

```text
AuthorityRef remains a reference
Lease record carries bounded, expiring, revocable grant data
resolve() is pure, fail-closed, budgeted, deterministic
Fork makes inherited leases UNVERIFIED
ALLOW ≠ truth ≠ identity ≠ M3
Docs-only until explicit owner GO for src/
```

### Связанные документы

- [`POST_P0_ROADMAP_V0.1.md`](POST_P0_ROADMAP_V0.1.md)
- [`MENTAURY_IDENTITY_CONTINUITY_AND_RELATIONAL_ARCHITECTURE_NOTES.md`](MENTAURY_IDENTITY_CONTINUITY_AND_RELATIONAL_ARCHITECTURE_NOTES.md) §12.3–12.5
- [`P0_002_ENVELOPE_CONTRACTS.md`](../P0_002_ENVELOPE_CONTRACTS.md)
- [`CURRENT_STATUS.md`](../CURRENT_STATUS.md)
- [`ARCHITECTURE_RECONCILIATION_V0.1.md`](ARCHITECTURE_RECONCILIATION_V0.1.md)
