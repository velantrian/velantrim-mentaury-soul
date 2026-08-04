# 🚦 Mentaury Soul — Current Status

**Дата фиксации:** 2026-08-04  
**Репозиторий:** `velantrian/velantrim-mentaury-soul`  
**Общий статус:** `ARCHITECTURE FROZEN · P0 EVENT SUBSTRATE V3 PLANNED · RUNTIME NOT VALIDATED`

---

## 🧭 Коротко

Mentaury имеет сформированный архитектурный Canon v0.1 и проверяемый P0-план, но рабочий runtime пока не включён в `main`.

Два внешних экспериментальных прототипа подтвердили, что выбранное направление реализуемо, однако независимые adversarial-аудиты обнаружили дефекты, которые необходимо закрыть до первого канонического кодового PR.

```text
Документация      → сформирована
Canon             → заморожен
Эксперимент v1    → воспроизведён, фундаментальные дефекты
Эксперимент v2    → первые дефекты исправлены, новые дефекты найдены
GitHub main       → documentation-only
Следующий runtime → P0 Event Substrate v3
```

---

## ✅ Сформировано

- архитектурный Canon v0.1;
- шесть корневых инвариантов;
- Identity Zones Z0–Z6;
- Memory M0–M3;
- Initial Character Seed;
- controlled M3 Update Protocol;
- Belief Revision model;
- Change Risk Classes CR0–CR4;
- Decision Audit distinction;
- Style ≠ Truth metamorphic contract;
- External Research Boundary and Quarantine contract;
- Scenario Contract set;
- P0 Implementation Plan v0.3;
- честная граница заявлений о сознании и личности.

---

# 🧪 Экспериментальная история

## EXP-P0-v1

```text
13 tests reproduced
```

Подтверждённые дефекты:

- `verify_chain()` не пересчитывал `event_hash`;
- подмена payload не обнаруживалась;
- подмена последнего hash не обнаруживалась;
- redaction могла удалить payload без `REDACTION_RECORDED`;
- optimistic concurrency проверялась до write transaction.

**Решение:** `REJECT_AS_CANONICAL · RETAIN_AS_EXPERIMENT`.

## EXP-P0-v2

```text
21 tests reproduced
```

Подтверждённые исправления:

- R0 начал пересчитывать hash;
- payload tampering и hash tampering обнаруживаются;
- redaction rollback исправлен;
- `BEGIN IMMEDIATE` используется до version check;
- real two-connection concurrency возвращает controlled conflict;
- введены полные UUID;
- добавлен `MENTAURY_CANONICAL_JSON_V1`;
- запрещены float и небезопасные integer;
- добавлены event/schema pairs и basic idempotency conflict.

Новые дефекты, найденные независимым аудитом:

- idempotency fingerprint не включает фактический pending event batch;
- возможна cross-stream redaction;
- redaction всё ещё изменяет committed row в `events`;
- R0 не проверяет `stream_meta`;
- настоящий atomic batch отсутствует;
- payload schema проверяется по имени, но не по структуре;
- полный Event Envelope не является реальной storage boundary.

**Решение:** `RETAIN_AS_EXP-P0-v2 · USE_AS_PATCH SOURCE · DO NOT MERGE DIRECTLY`.

---

# 🚨 Текущие P0-v3 блокеры

## 1. 🧾 Physical Event Immutability

Таблица `events` не должна изменяться после commit.

```text
events
└── immutable envelope + payload_digest + payload_ref

event_payloads
└── erasable payload bytes / encrypted blob
```

Redaction удаляет содержимое из `event_payloads`, но не выполняет `UPDATE` исторической строки события.

## 2. 🔐 Event-aware Idempotency

Fingerprint должен связывать idempotency key не только с command payload, но и со всем фактически создаваемым event batch.

```text
same key + same command + same batch
→ ALREADY_APPLIED

same key + changed type/schema/payload/count
→ IDEMPOTENCY_CONFLICT
```

## 3. 🚧 Same-stream Redaction

`redacting_command.target_stream`, `target_event.stream_id` и audit stream обязаны совпадать.

Cross-stream redaction должна завершаться fail-closed.

## 4. 🧭 R0 Stream Metadata Verification

R0 дополнительно проверяет:

```text
stream_meta.current_version == tail.stream_version
stream_meta.last_event_hash == tail.event_hash
```

## 5. 📦 Настоящий Atomic Batch

Интерфейс принимает `list[PendingEvent]` и гарантирует:

```text
all events committed
или
zero events committed
```

## 6. 📋 Structural Payload Validation

Недостаточно проверить строку `payload_schema`. Каждая schema обязана иметь реальный validator и reject unknown/missing fields по правилам профиля.

## 7. 🧬 Full Event Envelope Storage

Все hash-поля должны быть сохранены, восстановимы, неизменяемы и однозначно сериализуемы.

## 8. ⚙️ Supported SQLite Runtime

Перед concurrency/WAL тестами environment gate фиксирует безопасную версию SQLite или проверенный backport. Неподдерживаемая версия не может использоваться как evidence для production-intent.

---

# 🛠️ Следующая рабочая ветка

```text
agent/p0-event-substrate-v3
```

Архив v2 не переносится в `main` целиком. Из него выборочно берутся подтверждённые исправления и regression tests.

---

# 🔨 Порядок реализации

```text
P0-001 Project skeleton + locked environment
P0-002 CommandEnvelope / EventEnvelope / PendingEvent
P0-003 MENTAURY_CANONICAL_JSON_V1 + conformance vectors
P0-004 Immutable events + external event_payloads
P0-005 Structural event/schema validation
P0-006 Real atomic event batch
P0-007 Event-aware idempotency
P0-008 BEGIN IMMEDIATE concurrency boundary
P0-009 Full R0 + stream_meta verification
P0-010 Atomic same-stream redaction
P0-011 Adversarial integrity suite
P0-012 GitHub Actions CI
P0-013 Pure reducer + R1 replay
P0-014 Minimal Belief Lifecycle
```

Каждый commit обязан оставлять branch зелёной.

---

# 🧪 Минимальный Gate перед R1

Переход к reducer и R1 разрешён только после подтверждения:

- payload tampering обнаруживается;
- payload digest tampering обнаруживается;
- event hash tampering обнаруживается;
- previous hash corruption обнаруживается;
- metadata tampering обнаруживается;
- version gap и missing event обнаруживаются;
- `stream_meta` corruption обнаруживается;
- historical event row не изменяется;
- redaction остаётся атомарной и same-stream;
- different event batch under same idempotency key вызывает conflict;
- concurrent writer получает controlled `VERSION_CONFLICT`;
- partial batch невозможен;
- unsupported payload fail-closed.

---

# 🎭 Scenario Checker

```yaml
experimental: true
advisory_only: true
merge_blocking: false
```

Он может стать кандидатом на gate только после:

```text
benchmark corpus
→ blinded independent labels
→ baseline comparison
→ paraphrase/adversarial/multilingual tests
→ FP/FN report
→ governance review
```

---

# 🧬 M3 Identity Profile

M3 не обновляется из одного эпизода или одного ответа.

```text
M1/M2 pattern
→ M3 change candidate
→ longitudinal evidence
→ drift analysis
→ CR2 review
→ IDENTITY_PROFILE_UPDATED
   или IDENTITY_UPDATE_REJECTED
```

Предыдущая версия профиля всегда остаётся восстанавливаемой.

---

# 🚧 External Quarantine

Mentaury не интегрируется напрямую в Titan, Crystal или Native Kernel.

```text
MENTAURY EXPERIMENT
→ EXPORT PACKAGE
→ QUARANTINE
→ HUMAN REVIEW
→ RFC
→ INDEPENDENT REIMPLEMENTATION
→ TARGET-SYSTEM TESTS
```

Self-state, autobiographical memory, internal goals, character state, relationships и capability state не экспортируются.

---

## 🚫 Пока не заявляется

- production readiness;
- validated security;
- доказанное сознание;
- субъективная личность;
- абсолютная tamper-proof history;
- готовый autonomous cognition runtime;
- готовый Character Engine;
- прямая интеграция в Titan, Crystal или Native Kernel.

---

## 🏁 Критерий следующего статуса

Статус может измениться на:

```text
P0 EVENT SUBSTRATE VALIDATED
```

только после независимого воспроизведения полного adversarial R0 flow, atomic batch, event-aware idempotency, immutable redaction и R1 reconstruction.