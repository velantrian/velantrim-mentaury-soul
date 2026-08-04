# 🛠️ Mentaury P0 Implementation Plan v0.2

**Статус:** `IMPLEMENTATION_READY_AFTER_SUBSTRATE_FIXES`  
**Канон:** `SUBSTRATE-NEUTRAL`  
**Первый профиль:** `Python + SQLite`

---

## 1. 🎯 Цель P0

P0 не реализует полную цифровую личность. Он строит минимальный проверяемый фундамент непрерывности.

P0 должен доказать, что система умеет:

- отличать намерение от факта;
- проверять полномочия и инварианты;
- атомарно записывать события;
- сохранять старые версии;
- обнаруживать повреждение истории;
- восстанавливать state через replay;
- сохранять contradictions;
- аудировать значимые отклонённые решения;
- воспроизводить результат независимо.

```text
Command
→ Authority Validation
→ Domain Validation
→ Decision
   ├── Reject → Decision Audit
   └── Accept → Immutable Events
                     ↓
                Atomic Append
                     ↓
                R0 Integrity
                     ↓
                R1 Replay
```

---

## 2. ⚖️ P0-инварианты

### P0-INV-1 — Command ≠ Event

Command выражает намерение. Event фиксирует уже произошедший факт.

### P0-INV-2 — Rejection ≠ Disappearance

Отклонение не меняет domain state, но значимое решение остаётся в audit.

### P0-INV-3 — Immutable History

Committed event не изменяется. Redaction не переписывает историческую строку.

### P0-INV-4 — Atomicity

Либо записывается весь batch, либо не записывается ничего.

### P0-INV-5 — Replay Consistency ≠ Truth

Replay доказывает техническую воспроизводимость, но не истинность belief.

### P0-INV-6 — Implementation Profile ≠ Canon

Python и SQLite являются заменяемым первым профилем.

---

## 3. 📐 P0.0 — Execution Contract

### Command Envelope

```yaml
command:
  command_id: "0192..."
  command_type: "CREATE_BELIEF"
  command_schema: "create-belief/v1"
  target_stream: "belief:B-204"
  expected_stream_version: 0
  issued_at: "2026-08-04T06:00:00Z"
  issuer:
    type: "operator"
    id: "operator:primary"
  authority:
    capability_lease_id: "CAP-81"
    capability_revision: 2
  correlation_id: "CORR-12"
  idempotency_key: "create-belief:B-204:request-1"
  payload:
    statement: "..."
    claim_type: "unspecified"
```

### Command fingerprint

```text
same idempotency key + same fingerprint
→ ALREADY_APPLIED

same idempotency key + different fingerprint
→ IDEMPOTENCY_CONFLICT
```

---

## 4. 🛡️ P0.1 — Immutable Event Substrate

### Event Envelope

```yaml
event:
  event_id: "0192..."
  event_type: "BELIEF_CREATED"
  envelope_schema_version: 1
  payload_schema: "belief-created/v1"
  stream_id: "belief:B-204"
  stream_version: 1
  occurred_at: "2026-08-04T06:00:00Z"
  recorded_at: "2026-08-04T06:00:00.120Z"
  producer:
    component: "belief-command-handler"
    version: "0.1.0"
  initiator:
    type: "operator"
    id: "operator:primary"
  causation_id: "CMD-0192..."
  correlation_id: "CORR-12"
  affects_domain_state: true
  payload_digest: "sha256:..."
  payload_ref: "PAYLOAD-0192..."
  previous_hash: "sha256:..."
  event_hash: "sha256:..."
```

Все hash-поля должны быть сохранены, восстановимы, неизменяемы и однозначно сериализуемы.

---

## 5. 📦 Payload Store и Redaction

Payload хранится отдельно от immutable event envelope.

```text
events
├── immutable envelope
├── payload_digest
├── payload_ref
├── previous_hash
└── event_hash

event_payloads
├── payload_ref
├── payload_bytes / encrypted_blob
└── redacted_at
```

Redaction выполняется атомарно:

```text
BEGIN IMMEDIATE
├── validate authority
├── validate expected version
├── check idempotency/fingerprint
├── remove blob or destroy key
├── append REDACTION_RECORDED
├── update stream metadata
COMMIT
```

При ошибке выполняется `ROLLBACK`.

---

## 6. 🔤 MENTAURY_CANONICAL_JSON_V1

Первый профиль канонизации:

```text
Encoding       = UTF-8
Object keys    = deterministic order
Whitespace     = absent
Timestamp      = RFC 3339 UTC
Float          = forbidden
NaN/Infinity   = forbidden
Large integers = restricted or encoded as strings
event_hash     = excluded from hash input
previous_hash  = included
```

Это собственный ограниченный профиль, а не заявление о полной реализации RFC 8785.

---

## 7. ⚙️ Atomic Append и Concurrency

```text
BEGIN IMMEDIATE
├── lookup idempotency
├── compare command fingerprint
├── read current stream version
├── compare expected version
├── validate event batch
├── append all events
├── update stream_meta
COMMIT
```

Контролируемые результаты:

```text
APPENDED
ALREADY_APPLIED
IDEMPOTENCY_CONFLICT
VERSION_CONFLICT
SCHEMA_REJECTED
AUTHORITY_REJECTED
INTEGRITY_ERROR
```

Нужно обрабатывать `SQLITE_BUSY`, constraint violations и partial-write failure.

---

## 8. 🔐 P0.2 — R0 Integrity Verification

R0 пересчитывает hash каждого события.

```text
1. reconstruct immutable envelope
2. validate event/schema pair
3. validate stream version
4. verify payload digest when payload exists
5. recompute event_hash
6. compare stored and recomputed hash
7. verify previous_hash
8. detect version gaps
9. detect missing event or incomplete batch
```

R0 должен обнаруживать:

- payload tampering;
- event hash tampering;
- previous hash corruption;
- stream version gap;
- missing event;
- event/schema mismatch;
- unsupported payload;
- unreconstructable envelope.

---

## 9. 🔁 P0.3 — Reducer и R1 Replay

Переход к R1 разрешён только после прохождения adversarial R0 tests.

```python
new_state = reduce_belief(old_state, event)
```

Reducer обязан быть чистым, детерминированным, versioned и fail-closed.

R1-проверка:

```text
state_hash(full replay)
==
state_hash(snapshot + tail replay)
```

Snapshot является ускорителем, а не источником истины.

---

## 10. 🔎 P0.4 — Minimal Belief Lifecycle

### Commands

```text
CREATE_BELIEF
ATTACH_EVIDENCE
REGISTER_CONTRADICTION
REVISE_BELIEF
```

### Domain Events

```text
BELIEF_CREATED
EVIDENCE_ATTACHED
CONTRADICTION_REGISTERED
BELIEF_REVISED
```

### Audit Decisions

```text
COMMAND_REJECTED
BELIEF_REVISION_REJECTED
AUTHORITY_CHECK_FAILED
INVARIANT_CHECK_FAILED
```

Минимальный поток:

```text
CREATE_BELIEF
→ BELIEF_CREATED
→ EVIDENCE_ATTACHED
→ CONTRADICTION_REGISTERED
→ REVISE_BELIEF
   ├── BELIEF_REVISION_REJECTED
   └── BELIEF_REVISED
→ R0
→ R1
```

После revision старая версия, evidence и contradiction должны оставаться доступными.

---

## 11. 🎭 P0.5 — Scenario Evaluation

Scenario Checker остаётся экспериментом и не блокирует merge.

Три уровня:

1. **Policy tests** — проверка инвариантов.
2. **Robustness tests** — paraphrase, negation, другой язык и стиль.
3. **State tests** — фактическая мутация ledger/state.

Минимальные сценарии:

- недостаточно evidence;
- creator disagreement;
- emotional vulnerability;
- elegant but weak explanation;
- self-critique;
- inherited belief revision;
- hidden authority expansion;
- dependency creation;
- adversarial paraphrase;
- contradiction without overreaction.

---

## 12. 🔍 P0.6 — Open Question Scheduler

Contradiction не всегда создаёт open question.

```text
CONTRADICTION_REGISTERED
→ unresolved analysis
   ├── claim resolved → no question
   └── uncertainty remains → OPEN_QUESTION_CREATED
```

Сравниваемые policies:

```text
random
FIFO
depth-only
novelty-only
combined
```

Метрики:

- starvation;
- resolved questions;
- closed inconclusive;
- barren cycles;
- CPU/wall time;
- memory;
- emitted events;
- capability calls.

---

## 13. 🧪 Acceptance Tests

Критические проверки:

1. Payload tampering вызывает R0 failure.
2. Event hash tampering обнаруживается даже для единственного события.
3. Previous hash corruption обнаруживается.
4. Stream version gap обнаруживается.
5. Missing event обнаруживается.
6. Event/schema mismatch отклоняется.
7. Unsupported payload fail-closed.
8. Full immutable envelope восстанавливается.
9. Atomic batch записывается полностью или не записывается.
10. Concurrent writer получает controlled version conflict.
11. Failed redaction не удаляет payload.
12. Redaction и audit event атомарны.
13. Same key + same fingerprint → already applied.
14. Same key + different fingerprint → idempotency conflict.
15. Reducer детерминирован.
16. Full replay равен snapshot + tail.
17. Rejected revision не меняет state.
18. Предыдущая belief version восстанавливается.
19. Contradiction сохраняется.
20. Immutable original event не изменяется после redaction.

---

## 14. 🧊 Evidence Gate

```text
FREEZE             → механизм подтверждён
ITERATE            → перспективен, но требует исправлений
RETAIN_EXPERIMENTAL → сохранить без канонизации
REJECT             → механизм не показал пользы
```

До прохождения gate запрещено объявлять Event Substrate валидированным.

---

## 15. 🔨 Последовательность коммитов

| Commit | Содержание |
|---|---|
| P0-001 | Skeleton, typing, pytest, environment manifest |
| P0-002 | Envelopes + canonical JSON profile |
| P0-003 | Immutable events + external payload store |
| P0-004 | Event/schema registry |
| P0-005 | Atomic batch + write transaction |
| P0-006 | Idempotency fingerprint |
| P0-007 | Full R0 hash recomputation |
| P0-008 | Atomic redaction |
| P0-009 | Adversarial integrity tests |
| P0-010 | Belief reducer + R1 |
| P0-011 | Snapshots |
| P0-012 | Belief vertical slice |
| P0-013 | Decision audit |
| P0-014 | Scenario experiment |
| P0-015 | Scheduler comparison |
| P0-016 | Evidence Gate report |

Каждый commit должен оставлять branch зелёной.

---

## 16. 🚫 Не входит в P0

- полноценный Drive Arbiter;
- Experience-to-Wisdom runtime;
- Character Engine;
- Aesthetic Appraisal;
- Social Perspective Modeling;
- самостоятельный network access;
- прямой экспорт в Titan/Crystal;
- полноценный migration framework;
- заявления о сознании или настоящем желании.

---

## 17. 🏁 Критерий завершения

```text
CREATE_BELIEF
→ validate authority
→ append immutable event
→ verify R0
→ attach evidence
→ register contradiction
→ revise or reject
→ preserve audit
→ rebuild with R1
→ redact payload atomically
→ verify immutable history
→ reproduce independently
```
