# 🧬 Native Kernel как внешний research input — заметки v0.1

```text
Статус:                       DOCS_ONLY · NON_CANONICAL · RESEARCH_NOTES · DRAFT
Версия:                       0.1
Дата:                         2026-08-07
Источник:                     preserved from claude/audit-relationships-6866cw@a00001bcf7244dbb9d5dbbf162a830eafe329699
Область:                      Cross-project research input · Replay · Redaction · Evidence Gate · Relations
Runtime authority:            NONE
Truth authority:              NONE
Capability authority:         NONE
Canon modification authority: NONE
P0 scope authority:           NONE
Прямая запись в M3:           FORBIDDEN
Готовность к skeleton:         NOT_AUTHORIZED
NO RUNTIME AUTHORITY:         CONFIRMED
NO TRUTH AUTHORITY:           CONFIRMED
NO CAPABILITY AUTHORITY:      CONFIRMED
NO DIRECT M3 WRITE:           CONFIRMED
```

> Этот документ фиксирует, как Mentaury может относиться к research-треку
> `velantrim-native-kernel` как к внешнему источнику идей. Он не создаёт
> runtime, не расширяет P0, не меняет frozen Canon v0.1 и не превращает
> предложения Native Kernel в утверждённые механизмы Mentaury. Соответствует
> границам [`docs/VELANTRIM_ECOSYSTEM.md`](../VELANTRIM_ECOSYSTEM.md) и внешнему
> документу Native Kernel
> [`INTEGRATION_BOUNDARIES.md`](https://github.com/velantrian/velantrim-native-kernel/blob/main/docs/INTEGRATION_BOUNDARIES.md)
> (раздел «Native Kernel and Mentaury Soul»).

---

## 1. 🎯 Назначение

Кросс-репозиторный аудит (см. [`docs/VELANTRIM_ECOSYSTEM.md`](../VELANTRIM_ECOSYSTEM.md),
роль Native Kernel и обязательные границы) показал, что уже реализованные и
протестированные механизмы Mentaury структурно пересекаются с абстрактными
контрактами, которые только предлагает Native Kernel:

| Mentaury (реализовано и протестировано) | Native Kernel (предложено / contract-level, runtime `NOT_STARTED`) |
|---|---|
| `P0-013` — детерминированный R1 replay: `state_hash(full replay) == state_hash(snapshot + tail)` | [`ADR-0002`](https://github.com/velantrian/velantrim-native-kernel/blob/main/docs/adr/0002-state-checkpoints-are-disposable.md) (disposable State Checkpoints) и [`ADR-0004`](https://github.com/velantrian/velantrim-native-kernel/blob/main/docs/adr/0004-rebuild-from-authoritative-history.md) (rebuild from authoritative history) |
| `P0-010` — governed same-stream redaction с byte-for-byte immutable event row | будущая примитива "redaction-aware history" (см. внешний [`INTEGRATION_BOUNDARIES.md`](https://github.com/velantrian/velantrim-native-kernel/blob/main/docs/INTEGRATION_BOUNDARIES.md); отдельный ADR в Native Kernel пока не принят как реализация) |
| `P0-015` — Deterministic Evidence Gate: evidence set → deterministic receipt → belief status | Receipts и предложенный Audit Curiosity profile (внешний [`INTEGRATION_BOUNDARIES.md`](https://github.com/velantrian/velantrim-native-kernel/blob/main/docs/INTEGRATION_BOUNDARIES.md)) |
| Relationships / commitments как first-class объекты (`MENTAURY_IDENTITY_CONTINUITY_AND_RELATIONAL_ARCHITECTURE_NOTES.md`) | [`ADR-0006`](https://github.com/velantrian/velantrim-native-kernel/blob/main/docs/adr/0006-causal-links-are-relations.md) — causal/typed relations as relations, отдельные от lineage (`ACCEPTED` contract direction; implementation `NOT_STARTED`) |

Цель этой заметки — зафиксировать, как Mentaury может использовать Native Kernel
как research input, симметрично тому, как Native Kernel описывает независимую
границу с Mentaury в
[`INTEGRATION_BOUNDARIES.md`](https://github.com/velantrian/velantrim-native-kernel/blob/main/docs/INTEGRATION_BOUNDARIES.md)
(«Native Kernel and Mentaury Soul»). Это **не** утверждает существование
отдельного Native Kernel ADR с названием «Mentaury as external research input»
и **не** ссылается на несуществующий local `INTEGRATION_BOUNDARIES.md` внутри
Mentaury.

---

## 2. 🔍 Что это НЕ означает

```text
Native Kernel ADR-0006 существует
≠ у Mentaury появилась typed-relation storage-схема

Native Kernel предлагает redaction-aware history
≠ P0-010 переписывается под чужой контракт

Совпадение проблемы
≠ совместный runtime
≠ shared package
≠ shared schema
≠ authority transfer
≠ automatic M2/M3 promotion
≠ Native Kernel integration authorized
```

Как и в основном ecosystem-документе: Native Kernel events, projections или
Receipts не становятся Mentaury M2/M3 автоматически. Эта заметка не отменяет и
не ослабляет ни одну границу из [`docs/VELANTRIM_ECOSYSTEM.md`](../VELANTRIM_ECOSYSTEM.md).

---

## 3. 🧭 Как Mentaury может использовать Native Kernel как research input

- **Relationships / typed relations.** Если [`ADR-0006`](https://github.com/velantrian/velantrim-native-kernel/blob/main/docs/adr/0006-causal-links-are-relations.md) Native Kernel (relations как отдельная ось, не смешанная с lineage) созреет до реализации, это — возможный будущий кандидат на storage-форму для relationship-модели Mentaury (`Identity & Relational Research v0.1`). Признание идеи ≠ немедленное принятие; требуется отдельный research-проход и explicit schema review внутри Mentaury, прежде чем что-либо попадёт даже в M2 candidate.
- **Redaction-aware history как более общая абстракция.** P0-010 Mentaury уже решает узкую версию проблемы (одна SQLite-реализация, один stream). Если Native Kernel спроектирует более общую substrate-neutral redaction-примитиву, это может стать источником идей для будущей ревизии P0-010 — не наоборот: Mentaury не импортирует чужой код, а independently реализует любую принятую идею.
- **Словарь для evidence-gated переходов.** Evidence Gate (P0-015) и Receipts Native Kernel решают структурно одну и ту же задачу («evidence → deterministic gate → state change»). Общий словарь может облегчить будущее обсуждение, но не создаёт общий runtime и не заменяет Non-Projection review.

## 4. 🚧 Обязательные условия перед любым конкретным шагом

Как и в [`docs/VELANTRIM_ECOSYSTEM.md`](../VELANTRIM_ECOSYSTEM.md), любое движение от «идея показалась похожей» к «Mentaury что-то меняет» требует:

```text
внешняя идея (Native Kernel ADR/RFC)
→ отдельный Mentaury research-документ, разбирающий применимость
→ явная схема и provenance
→ Non-Projection review
→ детерминированные тесты
→ rollback
→ Receipts
→ одобрение оператора
```

Эта заметка сама не является таким research-документом уровня ниже — она только
фиксирует, что задача существует и где искать соответствующие Native Kernel ADR
при следующем шаге.

---

## 5. 📌 Текущее решение

```text
Статус:            RESEARCH INPUT NOTED · NO ACTION TAKEN
Canon v0.1:         UNCHANGED
P0 scope:           UNCHANGED
Skeleton authority: NOT_AUTHORIZED
Execution milestone: NOT CREATED
P1-001 priority:    UNCHANGED
```

Эта заметка не переносится в `MENTAURY_P0_IMPLEMENTATION_PLAN.md` и не создаёт
новую P0/P1-задачу сама по себе. Она служит навигационной точкой для будущего
решения, если и когда Native Kernel ADR-0002/0004/0006 перейдут из
contract/docs статуса в `REPOSITORY_REPRODUCED` / реализованный runtime — и даже
тогда потребуется отдельный Mentaury promotion gate.

### Preservation note

```text
Source branch: claude/audit-relationships-6866cw
Source head:   a00001bcf7244dbb9d5dbbf162a830eafe329699
Unique file:   docs/research/NATIVE_KERNEL_RESEARCH_INPUT_NOTES_V0.1.md
Fixes on preserve:
- local INTEGRATION_BOUNDARIES.md reference → external Native Kernel URL
- stale ADR-0010 mentaury-research-input URL removed (ADR-0010 is now foundational-contract-families)
- complementarity section pointer aligned to current main ecosystem doc
- explicit non-claims: no shared runtime, no authority transfer, no automatic M2/M3
```

См. также:
[`docs/VELANTRIM_ECOSYSTEM.md`](../VELANTRIM_ECOSYSTEM.md) ·
внешний [`INTEGRATION_BOUNDARIES.md`](https://github.com/velantrian/velantrim-native-kernel/blob/main/docs/INTEGRATION_BOUNDARIES.md) ·
[`ADR-0002`](https://github.com/velantrian/velantrim-native-kernel/blob/main/docs/adr/0002-state-checkpoints-are-disposable.md) ·
[`ADR-0004`](https://github.com/velantrian/velantrim-native-kernel/blob/main/docs/adr/0004-rebuild-from-authoritative-history.md) ·
[`ADR-0006`](https://github.com/velantrian/velantrim-native-kernel/blob/main/docs/adr/0006-causal-links-are-relations.md) ·
[`ADR-0010`](https://github.com/velantrian/velantrim-native-kernel/blob/main/docs/adr/0010-foundational-contract-families.md) (foundational contract families; не mentaury-import ADR).
