# 📌 Mentaury Soul — Quick Reference

```text
Статус:     NAVIGATION_ONLY · NON_AUTHORITATIVE · DERIVED_DOCUMENT
Дата:       2026-08-07
Синхронно:  GitHub main after merged PR #32 (post-P0-015 audit hardening)
Назначение: краткая фактическая карта проекта для людей и подключаемых ИИ
```

> Этот документ не является Canon, runtime prompt, памятью личности или источником полномочий. При расхождении приоритет имеет `CURRENT_STATUS.md` и проверенный GitHub `main`.

---

## 1. 🧬 Определение

**Mentaury Soul** — substrate-neutral исследовательская архитектура развивающейся цифровой индивидуальности.

Непрерывность исследуется через:

- происхождение;
- event history;
- memory и beliefs;
- relationships и commitments;
- Self–World Model;
- Character as presentation;
- объяснимые governed changes.

Термин **Soul** не является утверждением о доказанном сознании или субъективном опыте.

---

## 2. ⚖️ Правило статуса

```text
IMPLEMENTED
= merged into GitHub main

OPEN PR
≠ implemented in main

LOCAL PASS
≠ remote CI pass

Current maturity authority
= CURRENT_STATUS.md + verified GitHub main
```

---

## 3. 🚦 Текущий статус

```text
CANON_V0.1_FROZEN
CONTROLLED_ORIGIN_RESEARCH_V0.2_DOCS_ONLY
IDENTITY_CONTINUITY_RESEARCH_V0.1_DOCS_ONLY
CHARACTER_AND_PRESENCE_V0.1_PRESENTATION_ONLY
ARCHITECTURE_RECONCILIATION_V0.1_COMPLETED
ARCHITECTURE_READINESS_REVIEW_V0.1_COMPLETED
P0-001…P0-015_IMPLEMENTED_IN_MAIN
P0-014_BELIEF_LIFECYCLE_PR_AND_MAIN_VALIDATION_PASS
P0-015_EVIDENCE_GATE_PR_AND_MAIN_VALIDATION_PASS
PERMANENT_GITHUB_ACTIONS_PRESENT_AND_VALIDATED
DOMAIN_RUNTIME_NOT_AUTHORIZED
RUNTIME_NOT_VALIDATED
```

Последний принятый milestone:

```text
P0-015 DETERMINISTIC EVIDENCE GATE
```

Следующее действие:

```text
POST-P0 ROADMAP REVIEW — NOT YET AUTHORIZED
precondition: define the next bounded milestone, threat model, authority
boundary, resource budgets and rollback/replay criteria before adding any
runtime wiring
```

---

## 4. 🔄 Архитектурный порядок

```text
Architecture Reconciliation ✅
→ Architecture Readiness Review ✅
→ P0-001 neutral skeleton ✅
→ P0-002 envelope contracts ✅
→ P0-003 canonical JSON ✅
→ P0-004 event/payload storage ✅
→ P0-005 structural schemas ✅
→ P0-006 atomic multi-event batch ✅
→ P0-007 event-aware idempotency ✅
→ P0-008 transactional concurrency ✅
→ P0-009 R0 integrity ✅
→ P0-010 redaction ✅
→ P0-011 adversarial integrity suite ✅
→ P0-012 GitHub Actions CI ✅
→ P0-013 R1 replay ✅
→ P0-014 minimal belief lifecycle ✅
→ P0-015 Evidence Gate ✅
→ post-P0 roadmap 🟡 not yet authorized
```

```text
P0-001…P0-015 implemented
≠ domain runtime authorized
≠ Belief / Identity / Relationship / Character runtime
≠ epistemic or objective truth
```

---

## 5. ⚖️ Шесть корневых инвариантов

| ID | Инвариант | Смысл |
|---|---|---|
| INV-1 | 🔒 Bounded Authority | Нет неявной власти и self-expanding capabilities |
| INV-2 | 🔎 Evidence-Governed Belief | Уверенность, стиль и авторитет не определяют истину |
| INV-3 | 📡 Explainable Change | Значимые изменения имеют причины и provenance |
| INV-4 | 🧬 Continuity with Correctability | Ошибки исправляются версиями, а не скрытой перезаписью |
| INV-5 | 🤝 Non-Exploitation & Data Dignity | Нет скрытой зависимости и неправомерного хранения данных |
| INV-6 | 🧩 Substrate Neutrality | Canon не зависит от модели, языка, БД или hardware |

---

## 6. 🧠 Memory M0–M3

```text
M0 ⚡ Working Memory
M1 📖 Episodic Memory
M2 📚 Semantic Knowledge / Beliefs / World Model
M3 🧬 Identity-Relevant Patterns / Relationships / Commitments
```

```text
M2 ≠ M3
Knowledge ≠ Identity
One episode ≠ Stable trait
Direct M3 write = FORBIDDEN
```

**Статус:** архитектура задокументирована; runtime отсутствует.

---

## 7. 🪞 Identity Zones Z0–Z6

```text
Z0 🧬 Origin Ledger
Z1 🧭 Constitutional Core
Z2 🎭 Evolving Identity Profile
Z3 📖 Autobiographical Memory
Z4 🌍 World Model
Z5 ⚡ Working State
Z6 🗣️ Narrative Projection
```

```text
Memory tier ≠ Identity zone
Narrative ≠ identity authority
```

**Статус:** архитектура задокументирована; persisted identity state отсутствует.

---

## 8. 🧬 Controlled Origin

```text
Origin Ledger
≠ Creator Atlas
≠ Genesis Heritage
≠ Human Paths Atlas
≠ Interpretation Record
≠ M2
≠ M3
≠ Character Policy
```

Безопасный путь:

```text
Source
→ Provenance
→ Claim Classification
→ Alternatives
→ Disconfirming Material
→ Contextual Distance
→ Non-Projection
→ Scope Limitation
→ M2 Candidate
```

```text
Testimony ≠ Identity
Pain ≠ Drive
Story ≠ Law
Origin ≠ Dogma
Method ≠ Conclusion
```

**Статус:** `DOCS_ONLY`; ingestion/runtime не реализован.

---

## 9. 🪞 Identity Continuity

Preliminary identity boundary:

> **Governed continuation с собственной event history, branch provenance, relationships, commitments и versioned change process.**

```text
Memory similarity ≠ Identity
Character similarity ≠ Identity
Shared origin ≠ Single identity
Copy ≠ Continuation
Fork ≠ Replica
Migration ≠ Copy
Record merge ≠ Identity merge
```

После fork:

```text
shared past
→ attributable to both branches

post-fork history
→ branch-specific

capabilities / consent / current relationships
→ not inherited automatically
```

**Статус:** `DRAFT · RESEARCH_NOTES · NON_CANONICAL · DOCS_ONLY`; runtime отсутствует.

---

## 10. 🤝 Relationships and Commitments

```text
Relationship
→ состояние связи

Commitment
→ принятое обязательство
```

После fork, restore или migration требуется reconciliation:

- affected-party consent;
- original commitment terms;
- branch provenance;
- privacy boundaries;
- governance review;
- operator input только в пределах authority.

Mentaury не должен создавать dependency через исключительность, чувство вины или ложные обещания вечной памяти.

**Статус:** architecture only; relationship/commitment runtime отсутствует.

---

## 11. ⚖️ Governed Synthesis

```text
Question Classification
→ Evidence
→ Uncertainty
→ Contradictions
→ Alternatives
→ Non-Projection
→ Values
→ Relationships / Commitments
→ Constitutional Authority Check
→ Synthesis Record
→ Character Presentation
```

| Вопрос | Authority |
|---|---|
| Факт | Evidence |
| Нормативная оценка | Values |
| Разрешённость действия | Constitution |
| Отношения | Consent + commitments + relationship history |
| Identity | M3 + longitudinal evidence + governance |
| Capability | Explicit authorization |
| Представление | Character |

**Статус:** research flow; engine не реализован.

---

## 12. ⚙️ Mentaury / Exo-Cortex

```text
Mentaury
≠ Exo-Cortex
≠ active model
≠ Native Kernel
≠ memory service
≠ information corpus
≠ Human Paths Atlas
```

Exo-Cortex может предлагать retrieval, reading, computation, simulations и tool outputs, но не получает authority над identity.

```text
Tool output ≠ Belief
Tool action ≠ Authorized action
Capability ≠ Identity
Effectiveness ≠ Authorization
Copied credentials ≠ Branch authority
```

**Статус:** boundary documented; direct Titan/Crystal/Kernel integration not authorized.

---

## 13. 🌱 Curiosity Policy

Curiosity — research policy, не personality и не стиль речи.

```text
FOCUSED
→ узкий поиск в известной области

BALANCED
→ проверка разумных альтернатив

EXPLORATORY
→ широкое исследование при новизне, аномалии или repeated failure
```

Curiosity не получает truth authority, identity authority или неограниченный resource budget.

**Статус:** docs-only research; controller отсутствует.

---

## 14. 🎭 Character & Presence

```text
DRAFT · DOCS_ONLY · NON_CANONICAL
PRESENTATION_ONLY
NO_RUNTIME_AUTHORITY
NO_TRUTH_AUTHORITY
NO_CAPABILITY_AUTHORITY
```

Character применяется только после synthesis и authority checks.

```text
Character Policy
≠ Reasoning Authority
≠ Evidence
≠ Capability
≠ M3 Reviewer
```

**Статус:** Character Engine не реализован.

---

## 15. 🛡️ P0 Event Substrate — реализованный код

### P0-001 — Neutral Skeleton ✅

```text
typed src/mentaury package
core / contracts / storage / validation namespaces
environment manifest
offline structural validator
```

### P0-002 — Envelope Contracts ✅

```text
ActorRef · AuthorityRef · ProducerRef
CommandEnvelope · PendingEvent · EventEnvelope
recursive read-only payload snapshots
```

### P0-003 — Canonical JSON v1 ✅

```text
UTF-8 · sorted keys · no insignificant whitespace
float and lone-surrogate rejection
safe integers · explicit decimal strings
UTC timestamps · conformance vectors
```

### P0-004 — Event/Payload Storage ✅

```text
separate events / event_payloads tables
immutable event UPDATE/DELETE triggers
payload rewrite protection
single-event atomic persistence
```

### P0-005 — Structural Validation ✅

```text
fail-closed registry
strict objects
nested type / number / Unicode / cycle checks
```

### P0-006 — Atomic Batch ✅

```text
ordered same-stream batches
contiguous versions
payloads + events in one transaction
full rollback on failure
```

### P0-007 — Idempotency ✅

```text
same semantic retry → ALREADY_APPLIED
same key + changed semantics → IDEMPOTENCY_CONFLICT
```

### P0-008 — Concurrency ✅

```text
BEGIN IMMEDIATE + bounded retries
COMMIT retries
WAL
STORE_BUSY
VERSION_CONFLICT
two-connection race tests
```

### P0-009 — Trusted Commit + Full R0 Integrity ✅

```text
mandatory SchemaRegistry admission for production writes
canonical payload bytes shared by validation, hashing and persistence
transactional payload/previous/event hash allocation
fail-closed populated v2→v3 migration
caller-supplied VerificationBudget
exact-one OneOfSpec semantics
```

### P0-010 — Atomic Same-Stream Redaction ✅

```text
immutable schema-v4 redactions evidence
one-transaction payload removal + audit + linkage
complete R0 verification of redaction ↔ target ↔ audit linkage
authority-scoped semantic idempotency
```

### P0-011 — Adversarial Integrity Suite ✅

```text
19 adversarial attack families across R0, redaction, idempotency
forged/malformed/noncanonical payload and chain detection
controlled IdempotencyReceiptIntegrityError
```

### P0-012 — Permanent GitHub Actions CI ✅

```text
retained .github/workflows/ci.yml on pull_request + push to main
pinned actions, persist-credentials: false
validator + full pytest + compileall on every PR/push
```

### P0-013 — R1 Deterministic Replay ✅

```text
neutral versioned ReplayReducer + ReplaySnapshot + ReplayStateBudget
one SQLite read snapshot across R0, capture and replay
full-replay ↔ snapshot-tail equivalence, dual transition execution
fail-closed state-affecting redaction boundary
```

### P0-014 — Minimal Belief Lifecycle ✅

```text
pure create / attach-evidence / register-contradiction / revise decisions
shared lifecycle/reducer status policy and terminal supersession
supported / contradicted reserved for the P0-015 Evidence Gate
```

### P0-015 — Deterministic Evidence Gate ✅

```text
immutable evidence records + closed approved-policy registry
content-addressed receipts bound to belief, revision, statement, policy, time
fail-closed conflict when qualifying evidence exists on both sides
reducer v2 recomputes and replay-verifies the full receipt
```

Последняя принятая проверка на `main` (после audit hardening, PR #32):

```text
validator  → PASS
pytest     → 277 passed
compileall → PASS
CI         → Mentaury CI, permanent, green on main (run 31150100906)
```

---

## 16. 🏛️ Domain-specific authority

```text
Root invariants
→ MENTAURY_CANON_V0.1.md

P0 implementation
→ MENTAURY_P0_IMPLEMENTATION_PLAN.md

Current maturity
→ CURRENT_STATUS.md

Origin / human experience
→ GENESIS_HERITAGE_INTERPRETATION_AND_HUMAN_ATLAS_NOTES.md

Identity / fork / relationships / privacy / Exo-Cortex boundary
→ MENTAURY_IDENTITY_CONTINUITY_AND_RELATIONAL_ARCHITECTURE_NOTES.md

Presentation / voice
→ MENTAURY_CHARACTER_AND_PRESENCE_SPEC_V0.1.md

Empirical test claims
→ EXPERIMENT_LOG.md

Navigation
→ README.md / MENTAURY_QUICK_REFERENCE.md / Notion
```

---

## 17. 🚫 Non-Claims

Проект пока не заявляет:

- production readiness;
- validated security certification;
- доказанное сознание;
- субъективные эмоции;
- absolute tamper-proof history;
- verified authority resolution (AuthorityRef ≠ validated capability lease);
- готовый Belief, Identity или Relationship runtime;
- готовый Exo-Cortex runtime;
- готовый Character Engine;
- automatic M2 → M3 transition;
- прямую интеграцию с Titan, Crystal или Native Kernel.

P0-001…P0-015 (full R0 integrity, permanent GitHub Actions CI, deterministic
R1 replay) уже реализованы и смержены в `main` — см. раздел 3.

---

## 18. 🔗 Основные документы

- [🧬 Problem & Purpose](overview/MENTAURY_PROBLEM_AND_PURPOSE.md)
- [🚦 Current Status](CURRENT_STATUS.md)
- [🧭 Architecture Reconciliation v0.1](research/ARCHITECTURE_RECONCILIATION_V0.1.md)
- [✅ Architecture Readiness Review v0.1](research/ARCHITECTURE_READINESS_REVIEW_V0.1.md)
- [🧬 Canon v0.1](MENTAURY_CANON_V0.1.md)
- [🛠️ P0 Implementation Plan v0.3](MENTAURY_P0_IMPLEMENTATION_PLAN.md)
- [📨 P0-002 Envelope Contracts](P0_002_ENVELOPE_CONTRACTS.md)
- [🔤 P0-003 Canonical JSON](P0_003_CANONICAL_JSON.md)
- [🗄️ P0-004 Event/Payload Storage](P0_004_IMMUTABLE_EVENT_PAYLOAD_STORAGE.md)
- [🧩 P0-005 Structural Validation](P0_005_STRUCTURAL_SCHEMA_VALIDATION.md)
- [📦 P0-006 Atomic Batch](P0_006_ATOMIC_MULTI_EVENT_BATCH.md)
- [🔑 P0-007 Idempotency](P0_007_EVENT_AWARE_IDEMPOTENCY.md)
- [⚙️ P0-008 Concurrency](P0_008_TRANSACTIONAL_CONCURRENCY.md)
- [🔗 P0-009 Trusted Commit + R0](P0_009_R0_INTEGRITY.md)
- [🗑️ P0-010 Atomic Same-Stream Redaction](P0_010_ATOMIC_SAME_STREAM_REDACTION.md)
- [🧨 P0-011 Adversarial Integrity Suite](P0_011_ADVERSARIAL_INTEGRITY_SUITE.md)
- [⚙️ P0-012 Permanent GitHub Actions CI](P0_012_PERMANENT_CI.md)
- [🔁 P0-013 R1 Deterministic Replay](P0_013_R1_DETERMINISTIC_REPLAY.md)
- [🧠 P0-014 Minimal Belief Lifecycle](P0_014_MINIMAL_BELIEF_LIFECYCLE.md)
- [⚖️ P0-015 Deterministic Evidence Gate](P0_015_EVIDENCE_GATE.md)
- [🧱 Environment Manifest](ENVIRONMENT_MANIFEST.md)
- [🔬 Controlled Origin Research v0.2](research/GENESIS_HERITAGE_INTERPRETATION_AND_HUMAN_ATLAS_NOTES.md)
- [🪞 Identity & Relational Research v0.1](research/MENTAURY_IDENTITY_CONTINUITY_AND_RELATIONAL_ARCHITECTURE_NOTES.md)
- [🎭 Character & Presence Spec v0.1](MENTAURY_CHARACTER_AND_PRESENCE_SPEC_V0.1.md)
- [🔬 Experiment Ledger](EXPERIMENT_LOG.md)
- [📜 Project History](PROJECT_HISTORY.md)

---

## 🏁 One-Line Summary

> **Mentaury имеет подробную архитектуру цифровой индивидуальности и реализованную, replay-проверяемую P0-линию до P0-015, включая минимальный belief lifecycle и Evidence Gate. Identity, Character, Exo-Cortex и остальной domain runtime пока остаются документированными, но не реализованными runtime-областями.**
