# 🔬 Mentaury P0 — Experiment & Audit Ledger

**Статус:** `RESEARCH RECORD · NON-CANONICAL IMPLEMENTATIONS`  
**Назначение:** сохранять воспроизводимую историю экспериментальных прототипов, аудитов, исправлений и решений Evidence Gate.

---

## 🧭 Правило журнала

Экспериментальный код не становится канонической реализацией только потому, что его тесты проходят.

```text
code exists
≠ invariant proven

tests pass
≠ complete adversarial coverage

replay works
≠ knowledge is true
```

Для каждого эксперимента фиксируются:

- artifact identifier;
- environment manifest;
- code hash;
- test command;
- observed result;
- independently reproduced result;
- known gaps;
- gate decision.

---

# EXP-P0-v1

## 📦 Artifact

```text
mentaury-soul-P0.zip
```

## 🧪 Reproduced Result

```text
13 tests passed
```

## ✅ Что работало

- basic canonical subset;
- basic SQLite append;
- ordinary version conflict;
- simple idempotent retry;
- WAL + synchronous FULL configuration.

## 🚨 Независимо воспроизведённые дефекты

```text
payload tampering
→ verify_chain returned ok

event_hash tampering
→ verify_chain returned ok

stale redaction
→ VERSION_CONFLICT
→ payload already deleted
→ REDACTION_RECORDED absent
```

Дополнительные проблемы:

- version read до write transaction;
- single-event API назывался atomic batch;
- incomplete envelope persistence;
- short identifiers;
- payload/schema validation only nominal.

## 🧊 Gate Decision

```text
REJECT_AS_CANONICAL
RETAIN_AS_EXPERIMENT
```

---

# EXP-P0-v2

## 📦 Artifact

```text
mentaury-soul-P0-v2.zip
```

## 🧪 Reproduced Result

```text
21 tests passed
```

## ✅ Подтверждённые исправления

- R0 recomputes event hash;
- payload tampering detected;
- event hash tampering detected;
- redaction rollback fixed;
- `BEGIN IMMEDIATE` before version read;
- two-connection conflict controlled;
- full UUID identifiers;
- `MENTAURY_CANONICAL_JSON_V1` naming;
- float and unsafe integer rejection;
- event/schema pair registry;
- basic idempotency conflict;
- richer environment manifest.

## 🚨 Новые независимо воспроизведённые дефекты

### Event-aware idempotency gap

Одинаковый command fingerprint и key могли сопровождаться другим фактическим event payload/type и возвращать `ALREADY_APPLIED` вместо conflict.

### Cross-stream redaction

Команда могла удалить payload события stream A и записать audit event в stream B.

### Physical immutability violation

Redaction продолжала изменять committed row в `events`.

### Stream metadata gap

R0 не проверял согласованность `stream_meta` с tail event.

### Incomplete batch semantics

Append API по-прежнему принимал одно событие.

### Nominal schema validation

Проверялось имя schema, но не вся структура payload.

## 🧊 Gate Decision

```text
RETAIN_AS_EXP-P0-v2
USE_AS_PATCH SOURCE
DO_NOT MERGE DIRECTLY
```

---

# 🧩 Что переносится в P0-v3

```text
✅ hash recomputation
✅ payload_digest model
✅ BEGIN IMMEDIATE
✅ rollback discipline
✅ full UUID
✅ canonical profile
✅ adversarial tampering tests
✅ environment manifest
✅ controlled concurrency result
```

Переписывается:

```text
🔧 immutable event/payload split
🔧 command + pending batch fingerprint
🔧 same-stream redaction
🔧 stream_meta verification
🔧 real list[PendingEvent] batch
🔧 structural schema validation
🔧 full EventEnvelope storage boundary
```

---

# 🧪 Required P0-v3 Regression Cases

```text
same key + changed event payload
same key + changed event type
same key + changed event count/order
cross-stream redaction
stream_meta version tampering
stream_meta hash tampering
historical row byte-for-byte immutability
schema structural violation
partial multi-event batch failure
payload-store failure rollback
```

---

# 🏁 Decision at the time of EXP-P0-v1/v2 (superseded)

> ⚠️ **Устарело.** Блок ниже фиксирует решение на момент экспериментов
> EXP-P0-v1/v2, когда `main` действительно был documentation-only. С тех пор
> `agent/p0-event-substrate-v3` был реализован и смержен (PR #6, P0-001), и
> вся линия P0-001…P0-015 реализована и валидирована в `main`. Этот блок
> сохранён как исторический протокол, а не переписан, в соответствии с
> собственным принципом проекта "Continuity with Correctability" (ошибки и
> устаревшие записи исправляются новыми версиями, а не скрытой перезаписью
> прошлого). За актуальным статусом всегда обращайтесь к
> [`CURRENT_STATUS.md`](CURRENT_STATUS.md).

```text
NEXT IMPLEMENTATION (as of EXP-P0-v1/v2):
agent/p0-event-substrate-v3

CURRENT MAIN (as of EXP-P0-v1/v2):
documentation-only

R1 ALLOWED:
only after adversarial R0 Gate
```

Этот журнал не заменяет Canon или P0 Plan. Он сохраняет историю того, **что реально было проверено, что сломалось и почему эксперимент не был преждевременно объявлен фундаментом Mentaury**.