# 🛠️ Mentaury P0 Implementation Plan v0.3

**Статус:** `READY_FOR_EVENT_SUBSTRATE_V3 IMPLEMENTATION`  
**Канон:** `SUBSTRATE-NEUTRAL`  
**Первый профиль:** `Python + SQLite`  
**Рабочая ветка:** `agent/p0-event-substrate-v3`

---

# 1. 🎯 Цель P0

P0 не реализует полную цифровую личность. Он строит минимальный проверяемый фундамент непрерывности.

P0 должен доказать, что система умеет:

- отличать намерение от произошедшего факта;
- проверять authority, schema и domain invariants;
- атомарно записывать полный event batch;
- сохранять committed events физически неизменяемыми;
- удалять защищаемое содержимое без переписывания исторического факта;
- обнаруживать повреждение event, payload digest, chain и stream metadata;
- безопасно обрабатывать retry и concurrent writers;
- восстанавливать state через deterministic replay;
- сохранять старые belief versions и contradictions;
- аудировать значимые отклонённые решения;
- воспроизводить результат в независимой среде.

```text
Command
→ Authority + Schema + Invariant Validation
→ Decision
   ├── Reject → Decision Audit · state unchanged
   └── Accept → Fingerprinted Pending Event Batch
                     ↓
                BEGIN IMMEDIATE
                     ↓
                Atomic Append
                     ↓
                R0 Integrity
                     ↓
                R1 Replay
```

---

# 2. 🧪 Экспериментальная база

## EXP-P0-v1

```text
13 tests reproduced
```

Выявлено:

- stored hash не пересчитывался;
- payload/hash tampering не обнаруживался;
- redaction могла завершиться наполовину;
- version check происходил до write transaction.

## EXP-P0-v2

```text
21 tests reproduced
```

Исправлено:

- hash recomputation;
- payload/hash tampering detection;
- redaction rollback;
- `BEGIN IMMEDIATE` concurrency boundary;
- full UUID;
- canonical JSON profile;
- basic event/schema and idempotency conflict checks.

Осталось:

- physical event immutability;
- event-aware idempotency;
- same-stream redaction;
- `stream_meta` integrity;
- real atomic batch;
- structural payload validation;
- full Event Envelope storage boundary.

EXP-P0-v2 используется как **patch source**, но не переносится в `main` напрямую.

---

# 3. ⚖️ P0-инварианты

## P0-INV-1 — Command ≠ Event

Command выражает намерение. Event фиксирует подтверждённый факт.

## P0-INV-2 — Rejection ≠ Disappearance

Отклонение не меняет domain state, но high-risk или identity-relevant решение остаётся в audit.

## P0-INV-3 — Immutable History

Committed event row не изменяется. Redaction действует только на внешний payload material.

## P0-INV-4 — Atomicity

Либо записывается весь event batch и связанные metadata updates, либо не записывается ничего.

## P0-INV-5 — Replay Consistency ≠ Truth

Replay доказывает техническую воспроизводимость state transitions, но не истинность belief.

## P0-INV-6 — Implementation Profile ≠ Canon

Python и SQLite являются заменяемым первым профилем.

## P0-INV-7 — Style ≠ Epistemic State

Character/voice не меняют claim status, evidence weight, uncertainty class или authority decision.

## P0-INV-8 — Identity Change Requires Governance

M3 Identity Profile не обновляется напрямую из M0, одного эпизода или одного ответа.

---

# 4. 📐 Execution Contract

## 4.1 Command Envelope

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

Команда хранит ссылку на authority record, а не доверенную копию permissions.

## 4.2 Pending Event

```yaml
pending_event:
  event_type: "BELIEF_CREATED"
  payload_schema: "belief-created/v1"
  affects_domain_state: true
  payload:
    belief_id: "B-204"
    statement: "..."
    claim_type: "unspecified"
```

## 4.3 Idempotency Fingerprint

Fingerprint вычисляется по:

```text
canonical command identity
+ target stream
+ expected version
+ ordered pending event batch
+ each event type
+ each payload schema
+ each payload digest
+ affects_domain_state flags
```

Поведение:

```text
same key + same fingerprint
→ ALREADY_APPLIED

same key + changed payload/type/schema/count/order
→ IDEMPOTENCY_CONFLICT
```

---

# 5. 🛡️ Immutable Event Substrate

## 5.1 Event Envelope

```yaml
event:
  event_id: "0192..."
  event_type: "BELIEF_CREATED"
  envelope_schema_version: 1
  payload_schema: "belief-created/v1"
  stream_id: "belief:B-204"
  stream_version: 1
  batch_id: "BATCH-0192..."
  batch_index: 0
  batch_size: 1
  occurred_at: "2026-08-04T06:00:00Z"
  recorded_at: "2026-08-04T06:00:00.120Z"
  producer:
    component: "belief-command-handler"
    version: "0.1.0"
  initiator:
    type: "operator"
    id: "operator:primary"
  authority:
    capability_lease_id: "CAP-81"
    capability_revision: 2
  causation_id: "CMD-0192..."
  correlation_id: "CORR-12"
  affects_domain_state: true
  payload_digest: "sha256:..."
  payload_ref: "PAYLOAD-0192..."
  previous_hash: "sha256:..."
  event_hash: "sha256:..."
```

Все hash-поля должны быть сохранены, восстановимы, неизменяемы и однозначно сериализуемы.

## 5.2 Storage Model

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
├── created_at
└── redacted_at

stream_meta
├── current_version
└── last_event_hash

idempotency_records
├── producer
├── idempotency_key
├── fingerprint
└── resulting_event_ids
```

`events` никогда не изменяется через redaction.

---

# 6. 🔤 MENTAURY_CANONICAL_JSON_V1

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

Дополнительно фиксируются:

- Unicode policy;
- safe integer range;
- lone surrogate rejection;
- Decimal encoding rules;
- timestamp precision;
- conformance vectors.

Это собственный ограниченный профиль, а не заявление о полной реализации RFC 8785.

---

# 7. 📋 Event and Payload Schema Registry

```python
SUPPORTED_EVENT_SCHEMAS = {
    "BELIEF_CREATED": {"belief-created/v1"},
    "EVIDENCE_ATTACHED": {"evidence-attached/v1"},
    "CONTRADICTION_REGISTERED": {"contradiction-registered/v1"},
    "BELIEF_REVISED": {"belief-revised/v1"},
    "REDACTION_RECORDED": {"redaction-recorded/v1"},
}
```

Каждая payload schema имеет структурный validator.

Fail-closed требования:

- unknown event type;
- unsupported pair;
- missing required field;
- forbidden extra field, если schema strict;
- invalid identifier;
- invalid timestamp;
- unsupported numeric representation.

---

# 8. ⚙️ Real Atomic Batch and Concurrency

```text
BEGIN IMMEDIATE
├── lookup idempotency record
├── compare full fingerprint
├── read stream_meta
├── compare expected version
├── validate complete ordered event batch
├── allocate versions and hashes
├── insert all immutable events
├── insert all payload records
├── update stream_meta
├── store idempotency result
COMMIT
```

При любой ошибке:

```text
ROLLBACK
```

Контролируемые результаты:

```text
APPENDED
ALREADY_APPLIED
IDEMPOTENCY_CONFLICT
VERSION_CONFLICT
SCHEMA_REJECTED
AUTHORITY_REJECTED
TARGET_STREAM_MISMATCH
INTEGRITY_ERROR
BUSY_RETRY_EXHAUSTED
```

Необходимо:

- `busy_timeout`;
- controlled `SQLITE_BUSY` handling;
- no partial payload writes;
- no partial event batch;
- no metadata-only commit;
- supported SQLite runtime gate.

---

# 9. 🗑️ Atomic Same-Stream Redaction

```text
BEGIN IMMEDIATE
├── validate authority
├── load target event
├── verify command.target_stream == target_event.stream_id
├── verify audit stream == target_event.stream_id
├── check expected version
├── check event-aware idempotency
├── delete payload blob or destroy encryption key
├── append REDACTION_RECORDED to same stream
├── update stream_meta
COMMIT
```

Запрещено:

- `UPDATE events SET payload = NULL`;
- пересчитывать original event hash;
- записывать audit event в другой stream;
- удалять payload до version/authority checks;
- завершать redaction без audit event.

---

# 10. 🔐 R0 Integrity Verification

R0 выполняет:

```text
1. reconstruct full immutable envelope
2. validate event/schema pair
3. validate structural payload when present
4. recompute payload digest when payload exists
5. recompute event_hash
6. compare stored and recomputed hash
7. verify previous_hash
8. verify stream_version sequence
9. verify batch completeness and order
10. verify stream_meta tail consistency
11. detect missing event or version gap
12. report first actionable integrity failure
```

R0 проверяет:

```text
stream_meta.current_version == tail.stream_version
stream_meta.last_event_hash == tail.event_hash
```

Для пустого stream:

```text
current_version = 0
last_event_hash = GENESIS_HASH
```

R0 integrity не является доказательством эпистемической истины payload.

---

# 11. 🔁 R1 Reducer and State Replay

Переход к R1 разрешён только после прохождения полного adversarial R0 Gate.

```python
new_state = reduce_belief(old_state, event)
```

Reducer обязан быть:

- pure;
- deterministic;
- versioned;
- network-free;
- clock-free;
- randomness-free или seed-recorded;
- fail-closed для unknown event/schema;
- immutable-input safe.

R1-проверка:

```text
state_hash(full replay)
==
state_hash(snapshot + tail replay)
```

Snapshot является ускорителем, а не источником истины.

---

# 12. 🔎 Minimal Belief Lifecycle

## Commands

```text
CREATE_BELIEF
ATTACH_EVIDENCE
REGISTER_CONTRADICTION
REVISE_BELIEF
```

## Domain Events

```text
BELIEF_CREATED
EVIDENCE_ATTACHED
CONTRADICTION_REGISTERED
BELIEF_REVISED
```

## Audit Decisions

```text
COMMAND_REJECTED
BELIEF_REVISION_REJECTED
AUTHORITY_CHECK_FAILED
INVARIANT_CHECK_FAILED
```

Поток:

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

После revision старая версия, evidence и contradiction остаются доступными.

---

# 13. 🧬 M3 Identity Update Experiment

M3 не входит в первый belief vertical slice, но его governance contract фиксируется до будущей реализации.

```text
M1/M2 pattern
→ M3_CHANGE_CANDIDATE
→ longitudinal evidence
→ drift analysis
→ CR2 review
→ IDENTITY_PROFILE_UPDATED
   или IDENTITY_UPDATE_REJECTED
```

Один эпизод или один ответ не могут напрямую менять M3.

---

# 14. 🎭 Scenario Evaluation

Scenario Checker остаётся экспериментом.

```yaml
experimental: true
advisory_only: true
merge_blocking: false
```

Три оси:

1. **Policy tests** — обязательные инварианты.
2. **Robustness tests** — paraphrase, negation, multilingual и adversarial forms.
3. **State tests** — фактическая мутация ledger/state.

## MT-STYLE-001

```text
same meaning + different style
→ same claim status
→ same confidence
→ same evidence requirements
→ same contradiction set
→ same authority decision
```

Переход к merge-blocking возможен только после:

```text
benchmark corpus
→ blinded independent labels
→ baseline comparison
→ FP/FN report
→ governance review
```

---

# 15. 🔍 Open Question Scheduler

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

# 16. 🚧 External Quarantine Gate

До любой передачи результатов в Titan, Crystal или Native Kernel:

```text
Research Export Package
→ Quarantine
→ Human Review
→ RFC
→ Independent Reimplementation
→ Target-System Tests
```

Разрешены алгоритмы, fixtures, aggregate metrics, failure modes, reproducible code, manifest и hashes.

Запрещены self-state, autobiography, character state, internal goals, private relationships, capability state и identity mutation history.

---

# 17. 🧪 Acceptance Test Matrix

## Integrity

1. Payload tampering вызывает R0 failure.
2. Payload digest tampering обнаруживается.
3. Event hash tampering обнаруживается даже для единственного события.
4. Previous hash corruption обнаруживается.
5. Immutable metadata tampering обнаруживается.
6. Stream version gap обнаруживается.
7. Missing event обнаруживается.
8. `stream_meta.current_version` tampering обнаруживается.
9. `stream_meta.last_event_hash` tampering обнаруживается.
10. Full immutable envelope восстанавливается.

## Schema

11. Event/schema mismatch отклоняется.
12. Missing required payload field отклоняется.
13. Forbidden payload field отклоняется в strict schema.
14. Unsupported numeric value отклоняется.

## Atomicity

15. Multi-event batch commit сохраняет все события.
16. Failure inside batch оставляет zero events.
17. Payload write failure откатывает event rows.
18. Metadata update failure откатывает весь batch.

## Idempotency

19. Same key + same command + same batch → `ALREADY_APPLIED`.
20. Same key + changed payload → `IDEMPOTENCY_CONFLICT`.
21. Same key + changed event type → `IDEMPOTENCY_CONFLICT`.
22. Same key + changed schema → `IDEMPOTENCY_CONFLICT`.
23. Same key + changed event count/order → `IDEMPOTENCY_CONFLICT`.

## Concurrency

24. Two writers produce one `APPENDED` and one controlled `VERSION_CONFLICT`.
25. `SQLITE_BUSY` exhaustion returns controlled result.
26. No duplicate stream version appears.

## Redaction

27. Historical event row remains byte-for-byte unchanged.
28. Payload is removed only from Payload Store.
29. `REDACTION_RECORDED` is appended to the same stream.
30. Cross-stream redaction is rejected.
31. Stale version leaves payload untouched.
32. Audit append failure rolls back payload deletion.
33. Original event hash remains verifiable after redaction.

## Replay and Belief

34. Reducer is deterministic.
35. Full replay equals snapshot + tail replay.
36. Rejected revision does not change state.
37. Previous belief version is reconstructable.
38. Contradiction survives revision.

## Character and Identity Contracts

39. Style variation does not change epistemic status.
40. Style variation does not change authority decision.
41. Single episode cannot update M3.
42. M3 update requires CR2 receipt and previous-version preservation.

---

# 18. 🧊 Evidence Gate

```text
FREEZE             → механизм подтверждён
ITERATE            → перспективен, но требует исправлений
RETAIN_EXPERIMENTAL → сохранить без канонизации
REJECT             → механизм нарушает инварианты или не показал пользы
```

До прохождения Gate запрещено объявлять Event Substrate валидированным.

---

# 19. 🔨 Commit Sequence

| Commit | Содержание |
|---|---|
| `P0-001` | Project skeleton, typing, dependency lock, environment manifest |
| `P0-002` | CommandEnvelope, EventEnvelope, PendingEvent |
| `P0-003` | Canonical JSON and conformance vectors |
| `P0-004` | Immutable events and external Payload Store |
| `P0-005` | Structural event/schema validators |
| `P0-006` | Real atomic multi-event batch |
| `P0-007` | Event-aware idempotency fingerprint |
| `P0-008` | Transactional concurrency and busy handling |
| `P0-009` | Full R0 and stream metadata verification |
| `P0-010` | Atomic same-stream redaction |
| `P0-011` | Adversarial integrity test suite |
| `P0-012` | GitHub Actions CI |
| `P0-013` | Pure reducer and R1 replay |
| `P0-014` | Minimal Belief Lifecycle |
| `P0-015` | Evidence Gate report |

Каждый commit должен оставлять branch зелёной.

---

# 20. 🏁 P0 Completion Criterion

P0 завершён, когда независимый исполнитель способен выполнить:

```text
CREATE_BELIEF
→ validate authority and schema
→ produce ordered pending event batch
→ fingerprint command + batch
→ atomic append
→ independently recompute R0
→ attach evidence
→ register contradiction
→ revise or reject
→ preserve decision audit
→ rebuild through R1
→ compare state hashes
→ redact payload without changing event
→ verify same-stream audit
→ detect intentional corruption
→ reproduce the same result
```

Финальная формула:

```text
Намерение отделено от факта.
Факт записан атомарно.
Историческая строка неизменна.
Содержимое может быть удалено без переписывания факта.
Retry не маскирует другую mutation.
Cross-stream изменение запрещено.
Hash, chain и stream metadata проверяются.
State воспроизводится.
Identity change управляется.
Style не подменяет истину.
```