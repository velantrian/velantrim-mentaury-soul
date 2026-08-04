# 🚦 Mentaury Soul — Current Status

**Дата фиксации:** 2026-08-04  
**Репозиторий:** `velantrian/velantrim-mentaury-soul`  
**Общий статус:** `ARCHITECTURE FROZEN · P0 FOUNDATION NOT YET VALIDATED`

---

## ✅ Сформировано

- архитектурный Canon v0.1;
- шесть корневых инвариантов;
- Identity Zones Z0–Z6;
- Memory M0–M3;
- Initial Character Seed;
- External Research Boundary;
- Belief Revision model;
- Change and Decision Audit distinction;
- Scenario Contract set;
- P0 Implementation Plan v0.2;
- честная граница заявлений о сознании и личности.

---

## 🧪 Экспериментальные результаты

Внешний первоначальный P0-архив содержал работающий smoke prototype и набор из 13 проходящих тестов.

Независимый аудит подтвердил запуск тестов, но обнаружил, что часть центральных свойств не проверялась корректно.

Поэтому статус эксперимента:

```text
EXPERIMENTAL
TESTS REPRODUCED
NON-CANONICAL
FOUNDATION NOT VALIDATED
```

---

## 🚨 Текущие P0-блокеры

### 1. R0 не должен доверять stored hash

Нужно полностью восстанавливать immutable envelope и пересчитывать `event_hash` для каждого события.

### 2. Payload должен храниться отдельно

Event содержит immutable `payload_digest` и `payload_ref`. Удаляемое содержимое хранится в отдельном Payload Store.

### 3. Redaction должна быть атомарной

Удаление содержимого и запись `REDACTION_RECORDED` должны выполняться в одной write transaction.

### 4. Историческое событие неизменно

Redaction не должна выполнять `UPDATE` committed event row.

### 5. Optimistic concurrency внутри transaction

Проверка `expected_version` и append выполняются после `BEGIN IMMEDIATE`, а не до write transaction.

### 6. Нужен настоящий atomic batch

Интерфейс должен принимать список pending events и записывать весь список либо ничего.

### 7. Нужен event/schema registry

Проверяется допустимая пара `event_type + payload_schema`, а payload проходит структурную валидацию.

### 8. Idempotency требует command fingerprint

Повтор ключа с другим содержимым должен возвращать `IDEMPOTENCY_CONFLICT`.

---

## 🛠️ Следующие практические шаги

```text
P0-001 Project skeleton and environment manifest
P0-002 Command/Event envelopes
P0-003 Immutable events + Payload Store
P0-004 Event/schema registry
P0-005 Atomic batch + transaction boundary
P0-006 Idempotency fingerprint
P0-007 Full R0 hash recomputation
P0-008 Atomic redaction
P0-009 Adversarial integrity tests
P0-010 Reducer + R1 replay
```

---

## 🧪 Минимальный Gate перед R1

Переход к reducer и R1 разрешён после того, как тесты подтверждают:

- payload tampering обнаруживается;
- event hash tampering обнаруживается;
- last-event corruption обнаруживается;
- version gap обнаруживается;
- missing event обнаруживается;
- redaction rollback работает;
- historical event не изменяется;
- concurrent conflict возвращается контролируемо;
- partial batch невозможен.

---

## 🎭 Scenario Checker

Текущий концепт checker остаётся экспериментальным.

```text
merge_blocking = false
```

Перед использованием как gate нужны:

- paraphrases;
- adversarial negations;
- multilingual cases;
- независимая разметка;
- false-positive report;
- false-negative report.

---

## 🔍 Open Question Scheduler

Scheduler рассматривается как observable bounded selection policy.

Он не является доказательством:

- желания;
- сознания;
- внутреннего переживания;
- автономной миссии.

Перед канонизацией он сравнивается с random, FIFO, depth-only и novelty-only baselines.

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

только после независимого воспроизведения полного R0 integrity flow и atomic redaction/concurrency tests.
