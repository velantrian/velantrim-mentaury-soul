# 🗺️ Post-P0 Roadmap v0.1

```text
Статус:                       ADOPTED · ROADMAP · NON_CANONICAL · DOCS_ONLY
Версия:                       0.1
Дата:                         2026-08-07
Owner decision:               ACCEPTED (repository owner)
Runtime authority:            NONE
Truth authority:              NONE
Capability authority:         NONE
Canon modification authority: NONE
Прямая запись в M3:           FORBIDDEN
Domain runtime:               STILL NOT AUTHORIZED
```

> Этот документ закрывает precondition `POST-P0 ROADMAP REVIEW` из
> [`CURRENT_STATUS.md`](../CURRENT_STATUS.md). Он определяет **один**
> следующий bounded milestone и явно **не** разрешает domain runtime,
> Tool execution, Action Gate или автоматические внешние side effects.

---

## 1. 🎯 Назначение

После P0-001…P0-015 в `main` есть replay-проверяемый event substrate,
минимальный belief lifecycle и Evidence Gate. Следующий шаг — не
«подключить runtime», а выбрать **один** ограниченный milestone с явными:

- threat model;
- authority boundary;
- resource budgets;
- rollback / replay criteria;
- exit criteria до любого `src/` wiring.

```text
Roadmap adopted
≠
runtime authorized

First milestone named
≠
milestone implemented
```

---

## 2. 🚫 Non-claims

Этот документ **не**:

```text
❌ авторизует domain runtime / M0–M3 engines
❌ меняет Canon v0.1
❌ делает AuthorityRef «валидированным permission grant»
❌ добавляет Tool Receipt / Action Gate runtime
❌ помечает P1-001 как ✅ Implemented
❌ поднимает freshness-markers выше P0-015
❌ разрешает LLM-integration или autonomous goals
```

---

## 3. 📦 Закрытие P0 (входные условия)

```text
P0-001…P0-015     → IMPLEMENTED IN MAIN
PR #32            → post-P0-015 audit hardening merged
PR #33            → authoritative status sync merged
DOMAIN_RUNTIME    → NOT AUTHORIZED (сохраняется)
```

Оставшийся критический gap (из аудита 2026-08-06):

```text
AuthorityRef.capability_lease_id
→ записывается и сравнивается на equality
→ НЕ резолвится против lease registry
→ сейчас НЕ несёт enforceable permission
```

---

## 4. ✅ Выбор первого milestone

**P1-001 — Capability Lease Resolution (docs-first).**

Почему именно он:

1. уже записан как owner-accepted governance recommendation;
2. блокирует любой честный authority-sensitive runtime;
3. расширяет существующий stub Identity Continuity §12.3 без domain engines;
4. узкий scope: resolution contract, lifecycle, fail-closed outcomes, adversarial scenarios — без Action Gate execution.

```text
P1-001 docs freeze
→ независимый review
→ только затем возможен отдельный, явно авторизованный
   implementation PR (если owner даст GO)
```

Отложено (не часть P1-001):

```text
Identity Continuity engine
Controlled Origin ingestion
Character / Curiosity engines
Tool Receipt runtime
Action Gate execution
Governed Synthesis engine
LLM integration
```

---

## 5. 🃏 Карточка milestone: P1-001

### 5.1 Goal

Заморозить docs-only спецификацию **разрешения** `AuthorityRef` против
записи Capability Lease так, чтобы будущий resolver мог быть fail-closed,
replay-aware и adversarial-testable — **без** выдачи runtime permissions
этим документом.

Authoritative notes:

[`MENTAURY_CAPABILITY_LEASE_RESOLUTION_NOTES.md`](MENTAURY_CAPABILITY_LEASE_RESOLUTION_NOTES.md)

### 5.2 Threat model (кратко)

| Угроза | Почему важна | Требование к спеке |
|---|---|---|
| Поддельный / неизвестный `lease_id` | equality ≠ existence | fail-closed `UNKNOWN_LEASE` |
| Stale `capability_revision` | старый grant после revoke/rotate | fail-closed `REVISION_MISMATCH` |
| Expired / revoked lease | side effect после отзыва | fail-closed; fork → `UNVERIFIED` |
| Cross-stream / cross-purpose reuse | lease выдан на другое | purpose + scope match required |
| Embedded permission copy | обход registry | `AuthorityRef` остаётся ссылкой |
| Docs → silent runtime GO | authority expansion | явный owner GO на `src/` |

### 5.3 Authority boundary

```text
AuthorityRef
→ ссылка (lease_id + revision)

Capability Lease record
→ внешняя (будущая) registry-запись

Resolution result
→ ALLOW / DENY + machine reason code
≠ truth
≠ identity authority
≠ M3 write permission
≠ automatic Action Gate pass
```

### 5.4 In scope / Out of scope

**In scope (docs):**

- lease record contract и lifecycle states;
- pure resolution algorithm (inputs → fail-closed outcomes);
- fork / restore → `UNVERIFIED`;
- adversarial scenario IDs;
- P0 touchpoints (что уже есть; чего нельзя трогать без GO);
- Evidence Gate / exit criteria для будущего runtime PR.

**Out of scope:**

- любой production resolver в `src/`;
- Tool execution, network, side effects;
- branch protection / GitHub settings automation;
- изменение Canon.

### 5.5 Resource budgets (для будущего runtime; фиксируются уже сейчас)

```text
max leases consulted per resolution     ≤ 1 exact lease_id lookup
max revision history walk               ≤ 32
max wall-clock (caller-supplied)        required; no unbounded scan
max adversarial cases in first suite    ≥ 12 named scenarios
```

Бюджеты — контракт спеки. Числа могут быть уточнены до implementation GO,
но «без бюджета» не допускается.

### 5.6 Rollback / replay criteria

```text
Resolution MUST be a pure function of:
  (lease registry snapshot, AuthorityRef, action intent, time, budgets)

R1 replay of events that only *record* AuthorityRef
→ не требует lease registry (P0 поведение сохраняется)

Future events that *depend* on resolution
→ MUST embed enough evidence (receipt) to re-verify without ambient trust
```

Rollback: отказ resolution **никогда** не пишет domain state и не
создаёт side effects.

### 5.7 Exit criteria (docs freeze)

P1-001 docs считаются frozen, когда:

1. notes имеют явные Non-claims и rejection codes;
2. lifecycle + resolution algorithm полны для fail-closed решений;
3. ≥ 12 adversarial / scenario contracts названы;
4. независимый review по adopted governance policy пройден
   (см. `CURRENT_STATUS.md` § Governance policy);
5. `CURRENT_STATUS` **не** помечает P1-001 как `✅ Implemented`
   до появления кода в `main`.

```text
Docs freeze ≠ runtime GO
Independent review of docs ≠ permission to merge resolver code
```

---

## 6. 🔐 Authorization gate перед `src/`

Любой PR, добавляющий lease registry / resolver в `src/mentaury/`, требует:

1. frozen P1-001 docs + independent review;
2. отдельный owner GO в `CURRENT_STATUS` («P1-001 implementation authorized»);
3. threat model / budgets / replay criteria из §5 без ослабления;
4. merge-blocking review на путях `beliefs` / `evidence` / `replay` /
   и на новом authority/lease пути.

До выполнения всех четырёх пунктов:

```text
DOMAIN_RUNTIME_NOT_AUTHORIZED
CAPABILITY_LEASE_RESOLVER_NOT_AUTHORIZED
```

---

## 7. 🧭 Правила sync статусной документации

| Событие | Что делать с markers |
|---|---|
| Этот roadmap принят | **не** менять `P0-001…P0-015_IMPLEMENTED_IN_MAIN` |
| P1-001 docs merged | статус `DOCS_ONLY · NOT IMPLEMENTED` |
| P1-001 code merged | только тогда `✅ Implemented` + bump derived markers на P1 |

`scripts/check_doc_freshness.py` остаётся на P0-015, пока нет кода P1.

---

## 8. 🏁 Итоговая формула

```text
P0 closed
→ Post-P0 Roadmap v0.1 adopted (docs-only)
→ first milestone = P1-001 Capability Lease Resolution (docs-first)
→ domain runtime still forbidden
→ AuthorityRef still ≠ validated permission
```

### Связанные документы

- [`CURRENT_STATUS.md`](../CURRENT_STATUS.md)
- [`MENTAURY_CAPABILITY_LEASE_RESOLUTION_NOTES.md`](MENTAURY_CAPABILITY_LEASE_RESOLUTION_NOTES.md)
- [`MENTAURY_IDENTITY_CONTINUITY_AND_RELATIONAL_ARCHITECTURE_NOTES.md`](MENTAURY_IDENTITY_CONTINUITY_AND_RELATIONAL_ARCHITECTURE_NOTES.md) §12.3
- [`P0_002_ENVELOPE_CONTRACTS.md`](../P0_002_ENVELOPE_CONTRACTS.md)
- [`ARCHITECTURE_RECONCILIATION_V0.1.md`](ARCHITECTURE_RECONCILIATION_V0.1.md)
