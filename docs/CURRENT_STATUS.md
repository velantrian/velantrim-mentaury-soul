# 🚦 Mentaury Soul — Current Status

**Дата фиксации:** 2026-08-04  
**Репозиторий:** `velantrian/velantrim-mentaury-soul`  
**Общий статус:** `CANON_V0.1_FROZEN · P0_EVENT_SUBSTRATE_V3_PLANNED · P1_CHARACTER_SPEC_DOCS_ONLY · RUNTIME_NOT_VALIDATED`

---

## 🧭 Коротко

Mentaury имеет сформированный архитектурный Canon v0.1, P0 Implementation Plan v0.3 и отдельную docs-only спецификацию Character & Presence v0.1.

Рабочий runtime пока не включён в `main`. Character & Presence документ не является Character Engine, не получает truth/capability authority и не разрешает direct write в M3.

```text
Canon                    → frozen
P0 plan                  → formed
P0 runtime               → not implemented in main
Character research       → docs-only P1 candidate
Quick Reference          → navigation-only
Experiment v1/v2         → retained as external evidence
GitHub main              → documentation-only
Next runtime milestone   → P0 Event Substrate v3
```

---

## ✅ Сформированные артефакты

- [🧬 Mentaury Canon v0.1](MENTAURY_CANON_V0.1.md);
- [🛠️ P0 Implementation Plan v0.3](MENTAURY_P0_IMPLEMENTATION_PLAN.md);
- шесть корневых инвариантов;
- Identity Zones Z0–Z6;
- Memory M0–M3;
- controlled M3 Update Protocol;
- Belief Revision model;
- Change Risk Classes CR0–CR4;
- Decision Audit distinction;
- Style ≠ Truth metamorphic contract;
- External Research Boundary and Quarantine contract;
- Scenario Contract set;
- [🎭 Character & Presence Spec v0.1](MENTAURY_CHARACTER_AND_PRESENCE_SPEC_V0.1.md);
- [📌 Mentaury Quick Reference](MENTAURY_QUICK_REFERENCE.md);
- [🔬 Experiment & Audit Ledger](EXPERIMENT_LOG.md);
- [📜 Project History](PROJECT_HISTORY.md);
- честная граница заявлений о сознании и личности.

---

# 🎭 Character & Presence — новый docs-only трек

```text
DRAFT
RESEARCH_SPEC
DOCS_ONLY
NON_CANONICAL
P1_CANDIDATE
NO_RUNTIME_AUTHORITY
NO_TRUTH_AUTHORITY
NO_CAPABILITY_AUTHORITY
```

Спецификация формализует:

- Composed Integrity;
- Precise Wit;
- Cognitive Force without Domination;
- Independent Judgment;
- Genesis-Aware Perspective;
- Epistemic Honesty;
- Dignity without Superiority;
- Non-Manipulative Presence;
- Cognitive Magnetism;
- Resolved Openness;
- Voice & Presence Contract;
- Knowledge Saturation Protocol;
- Self–World Association Contract;
- Bounded Endogenous Selection Policies;
- десять Character Scenario Contracts;
- пять metamorphic tests;
- отдельный Evidence Gate for P1.

### Жёсткая граница

```text
Character Spec ≠ Character Runtime
Voice ≠ Consciousness
Self-Model ≠ Proof of Subjectivity
Presence ≠ Authority
Charisma ≠ Evidence
```

Character Policy в будущем сможет менять только форму представления. Он не сможет менять truth status, evidence weight, contradiction state, authority result, capabilities или исторические факты.

---

# 📌 Quick Reference

`MENTAURY_QUICK_REFERENCE.md` является навигационным справочником для людей и подключаемых ИИ.

```text
NAVIGATION_ONLY
NON_AUTHORITATIVE
DERIVED_FROM_CANON_AND_CURRENT_STATUS
```

При конфликте используется следующий порядок источников:

```text
1. MENTAURY_CANON_V0.1.md
2. MENTAURY_P0_IMPLEMENTATION_PLAN.md
3. CURRENT_STATUS.md
4. MENTAURY_CHARACTER_AND_PRESENCE_SPEC_V0.1.md
5. EXPERIMENT_LOG.md
6. PROJECT_HISTORY.md
7. MENTAURY_QUICK_REFERENCE.md
```

Quick Reference не является personality prompt, памятью личности или источником полномочий.

---

# 🧪 Экспериментальная история

## EXP-P0-v1

```text
13 tests reproduced
```

Подтверждённые дефекты:

- `verify_chain()` не пересчитывал `event_hash`;
- payload/hash tampering не обнаруживались;
- redaction могла удалить payload без `REDACTION_RECORDED`;
- optimistic concurrency проверялась до write transaction.

**Решение:** `REJECT_AS_CANONICAL · RETAIN_AS_EXPERIMENT`.

## EXP-P0-v2

```text
21 tests reproduced
```

Подтверждённые исправления:

- полный hash recomputation для текущего профиля;
- обнаружение payload/hash tampering;
- redaction rollback;
- `BEGIN IMMEDIATE` до version check;
- controlled two-connection version conflict;
- full UUID;
- `MENTAURY_CANONICAL_JSON_V1`;
- basic event/schema pair и idempotency conflict.

Новые дефекты:

- fingerprint не включает pending event batch;
- cross-stream redaction;
- изменение committed event row;
- отсутствие `stream_meta` verification;
- отсутствие настоящего atomic batch;
- отсутствие structural payload validation;
- неполный Event Envelope storage boundary.

**Решение:** `RETAIN_AS_EXP-P0-v2 · USE_AS_PATCH_SOURCE · DO_NOT_MERGE_DIRECTLY`.

---

# 🚨 Текущие P0-v3 блокеры

## 1. 🧾 Physical Event Immutability

```text
events
└── immutable envelope + payload_digest + payload_ref

event_payloads
└── erasable payload bytes / encrypted blob
```

Redaction не выполняет `UPDATE` committed event row.

## 2. 🔐 Event-Aware Idempotency

```text
same key + same command + same batch
→ ALREADY_APPLIED

same key + changed type/schema/payload/count
→ IDEMPOTENCY_CONFLICT
```

## 3. 🚧 Same-Stream Redaction

Command target stream, target event stream и audit stream обязаны совпадать.

## 4. 🧭 R0 Stream Metadata Verification

```text
stream_meta.current_version == tail.stream_version
stream_meta.last_event_hash == tail.event_hash
```

## 5. 📦 Real Atomic Batch

Интерфейс принимает `list[PendingEvent]`: весь batch или ноль событий.

## 6. 📋 Structural Payload Validation

Каждая payload schema имеет реальный validator и fail-closed semantics.

## 7. 🧬 Full Event Envelope Storage

Все hash-поля сохраняются, восстанавливаются и однозначно сериализуются.

## 8. ⚙️ Supported SQLite Runtime

WAL/concurrency evidence принимается только на поддерживаемой версии или проверенном backport.

---

# 🔨 Порядок реализации P0-v3

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

Планируемая ветка:

```text
agent/p0-event-substrate-v3
```

---

# 🧪 Gate перед R1

Переход к reducer и R1 разрешён после подтверждения:

- payload, digest, event hash, previous hash и metadata tampering обнаруживаются;
- gaps, missing events и `stream_meta` corruption обнаруживаются;
- historical event row неизменна;
- redaction атомарна и same-stream;
- changed event batch under same key возвращает conflict;
- concurrent writer получает controlled result;
- partial batch невозможен;
- unsupported payload fail-closed.

---

# 🔬 Evidence Gate перед P1 Character Runtime

Character runtime запрещён до выполнения всех условий:

1. P0 Event Substrate независимо валидирован.
2. Character Scenario corpus версионирован.
3. Есть blinded labels и agreement report.
4. Проведены multilingual, paraphrase и adversarial tests.
5. Зафиксированы FP/FN rates.
6. Подтверждено `Style ≠ Truth`.
7. Проверены dependency creation и authority leakage.
8. Подтверждено отсутствие direct M3 write.
9. Определены resource budgets и stop conditions.
10. Проведён governance review, RFC и explicit Operator GO.

---

# 🎭 Scenario Checker

```yaml
experimental: true
advisory_only: true
merge_blocking: false
```

Он может стать кандидатом на gate только после benchmark corpus, blinded labels, baseline comparison, multilingual/adversarial tests, FP/FN report и governance review.

---

# 🧬 M3 Identity Profile

```text
M1/M2 pattern
→ M3 change candidate
→ longitudinal evidence
→ drift analysis
→ CR2 review
→ IDENTITY_PROFILE_UPDATED
   или IDENTITY_UPDATE_REJECTED
```

Один диалог, эпизод или стиль ответа не создаёт устойчивую черту.

---

# 🚧 External Quarantine

```text
MENTAURY EXPERIMENT
→ EXPORT PACKAGE
→ QUARANTINE
→ HUMAN REVIEW
→ RFC
→ INDEPENDENT REIMPLEMENTATION
→ TARGET-SYSTEM TESTS
```

Self-state, autobiography, internal goals, character state, private relationships и capability state не экспортируются.

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

## 🏁 Следующие milestones

```text
Documentation milestone:
CHARACTER_AND_PRESENCE_V0.1_DRAFT ✅
QUICK_REFERENCE_PUBLISHED ✅

Engineering milestone:
P0 EVENT SUBSTRATE VALIDATED ⏳

Research milestone after P0:
P1 CHARACTER SHADOW EXPERIMENTS ⛔ NOT AUTHORIZED YET
```
