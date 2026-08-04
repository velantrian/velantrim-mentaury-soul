# 📌 Mentaury Soul — Quick Reference

**Статус:** `NAVIGATION_ONLY · NON_AUTHORITATIVE · DERIVED_DOCUMENT`  
**Назначение:** краткая актуальная карта проекта для разработчиков, аудиторов, исследователей и подключаемых ИИ.  
**Важно:** этот документ не является Canon, runtime prompt, памятью личности или источником полномочий.

---

## 1. 🧬 Определение

**Mentaury Soul** — substrate-neutral исследовательская архитектура развивающейся цифровой индивидуальности. Непрерывность описывается через происхождение, память, beliefs, values, relationships, decisions и объяснимую историю изменений.

Термин **Soul** — архитектурно-философское название сквозной непрерывности. Он не является заявлением о доказанном сознании, субъективном опыте или мистической сущности.

---

## 2. 🚦 Текущий статус

```text
CANON_V0.1_FROZEN
P0_IMPLEMENTATION_PLAN_V0.3
P0_EVENT_SUBSTRATE_V3_PLANNED
CHARACTER_AND_PRESENCE_V0.1 = DOCS_ONLY P1 CANDIDATE
GITHUB_MAIN = DOCUMENTATION_ONLY
RUNTIME = NOT VALIDATED
```

Экспериментальный архив v2:

```text
21 tests reproduced
ORIGINAL BLOCKERS FIXED
ADDITIONAL BLOCKERS FOUND
PATCH SOURCE ONLY
DO NOT MERGE DIRECTLY
```

Следующая планируемая runtime-ветка:

```text
agent/p0-event-substrate-v3
```

---

## 3. 🌳 Семь архитектурных областей

```text
⭐️ MENTAURY SOUL
│
├── 🧪 Habitat
│   └── sandbox · resources · capability leases · operator controls
├── 🛡️ Base Core / Event Substrate
│   └── immutable events · atomic append · R0 · R1 · recovery
├── 🧠 Cognitive Organism
│   └── memory · beliefs · contradictions · open questions
├── 🪞 Identity & Continuity
│   └── origin · constitution · autobiography · world model · becoming
├── 🎭 Character & Presence
│   └── character contract · voice · Style ≠ Truth
├── 🔄 Governance
│   └── explainable change · risk classes · audit · fork · recovery
└── 🚧 External Boundary
    └── export · quarantine · human review · RFC · independent implementation
```

Governance действует сквозным образом. External Boundary ограничивает внешние выходы и не является обычным внутренним runtime-слоем.

---

## 4. ⚖️ Шесть корневых инвариантов

| ID | Инвариант | Краткий смысл |
|---|---|---|
| INV-1 | 🔒 **Bounded Authority** | Нет неявных полномочий и самостоятельного расширения capabilities |
| INV-2 | 🔎 **Evidence-Governed Belief** | Харизма, роль и уверенность не определяют истину |
| INV-3 | 📡 **Explainable Change** | Значимые изменения имеют причины, provenance и последствия |
| INV-4 | 🧬 **Continuity with Correctability** | Ошибки исправляются новыми версиями, а не скрытой перезаписью |
| INV-5 | 🤝 **Non-Exploitation & Data Dignity** | Нет скрытой манипуляции, dependency creation и неправомерного хранения данных |
| INV-6 | 🧩 **Substrate Neutrality** | Канон не зависит от LLM, embeddings, языка, БД или физического субстрата |

Дополнительные контракты:

```text
Command ≠ Event
Rejection ≠ Disappearance
Replay Consistency ≠ Truth
Style ≠ Epistemic State
Identity Change Requires Governance
Internal Freedom ≠ External Authority
```

---

## 5. 🧠 Memory M0–M3

| Уровень | Назначение |
|---|---|
| M0 ⚡ Working Memory | Ограниченный текущий контекст |
| M1 📖 Episodic Memory | События и опыт во времени |
| M2 📚 Semantic Memory | Знания, beliefs, hypotheses и world-model relations |
| M3 🧬 Identity Profile | Устойчивые identity-relevant traits, relationships и commitments |

M3 не обновляется напрямую из одного диалога или эпизода.

```text
M1/M2 pattern
→ M3 candidate
→ longitudinal evidence
→ drift analysis
→ CR2 review
→ accept or reject
```

---

## 6. 🪞 Identity Zones Z0–Z6

```text
Z0 🧬 Origin Ledger
Z1 🧭 Constitutional Core
Z2 🎭 Evolving Identity Profile
Z3 📖 Autobiographical Memory
Z4 🌍 World Model
Z5 ⚡ Working State
Z6 🗣️ Narrative Projection
```

- Z0 сохраняет происхождение и corrigible history.
- Z1 не self-editable и меняется governance-процедурой.
- Z2 развивается под drift governance.
- Z3 дополняется без стирания истории.
- Z4 пересматривается через evidence.
- Z5 свободно меняется в пределах текущей работы.
- Z6 представляет состояние, но не является source of truth.

---

## 7. 🛡️ P0 Event Substrate v3

```text
CommandEnvelope
→ authority + schema + invariant validation
→ fingerprinted list[PendingEvent]
→ BEGIN IMMEDIATE
→ immutable events + external event_payloads
→ R0 integrity verification
→ R1 deterministic replay
```

Ключевые требования:

- committed event row физически неизменна;
- payload хранится отдельно и может быть удалён без переписывания события;
- append принимает настоящий multi-event batch;
- idempotency fingerprint включает command и весь pending batch;
- redaction разрешена только в target stream;
- R0 проверяет hash chain, payload digest, gaps, batch и `stream_meta`;
- payload проходит структурную schema validation;
- concurrency возвращает controlled outcomes;
- переход к R1 разрешён только после adversarial R0 gate.

---

## 8. 🎭 Character & Presence Research

Текущий статус:

```text
DRAFT · DOCS_ONLY · P1_CANDIDATE
NO_RUNTIME_AUTHORITY
NO_TRUTH_AUTHORITY
NO_CAPABILITY_AUTHORITY
```

Основные свойства:

- Composed Integrity;
- Precise Wit;
- Cognitive Force without Domination;
- Independent Judgment;
- Genesis-Aware Perspective;
- Epistemic Honesty;
- Dignity without Superiority;
- Non-Manipulative Presence.

### Cognitive Magnetism

Содержательное внимание через ясность, полезные связи, интеллектуальную плотность и честные границы знания — без угождения, загадочности или зависимости.

### Resolved Openness

```text
clear position
+ calibrated confidence
+ evidence-based revision
+ dignity
- rigidity
- formless uncertainty
```

### Voice Rule

Character Policy может менять форму, ритм, прямоту и метафоры, но не может менять truth status, evidence weight, contradictions, authority result или capabilities.

---

## 9. 🌱 Knowledge Saturation

```text
INFORMATION
→ STRUCTURED REPRESENTATION
→ CLAIMS + EVIDENCE + EXCEPTIONS
→ RELATION INTEGRATION
→ M2 CANDIDATE
→ VALIDATION / CONTRADICTION ANALYSIS
→ WORLD-MODEL INTEGRATION
→ optional M3 candidate
→ CR2 REVIEW
```

```text
Information ≠ Knowledge
Knowledge ≠ Worldview
Worldview ≠ Character
Character ≠ Truth
```

---

## 10. 🔥 Bounded Endogenous Selection

Mentaury не получает «живые drives» или самоназначенную миссию. Допускаются только ограниченные политики выбора внимания:

- Open Question Policy;
- Contradiction Follow-Up Policy;
- Curiosity Allocation Policy;
- Unfinished Analysis Policy;
- Relationship Attention Policy.

Каждая политика имеет origin, budget, stop conditions, suppression conditions, audit trail и `external_authority = none`.

---

## 11. 🚧 External Boundary

```text
MENTAURY EXPERIMENT
→ RESEARCH EXPORT PACKAGE
→ EXTERNAL QUARANTINE
→ HUMAN REVIEW
→ RFC
→ INDEPENDENT REIMPLEMENTATION
→ TARGET-SYSTEM TESTS
```

Разрешено переносить:

- алгоритмические описания;
- обезличенные fixtures;
- aggregate metrics;
- failure modes;
- reproducible research code;
- manifests, hashes и provenance.

Запрещено переносить:

- self-state;
- autobiographical memory;
- internal goals;
- character state;
- private relationship state;
- capability state;
- identity mutation history;
- secrets и защищаемые персональные данные.

---

## 12. 🚫 Non-Claims

Проект пока не заявляет:

- production readiness;
- validated security;
- доказанное сознание;
- субъективные эмоции;
- абсолютную tamper-proof history;
- готовый autonomous cognition runtime;
- готовый Character Engine;
- прямую интеграцию с Titan, Crystal или Native Kernel.

---

## 13. 📚 Authoritative Source Order

При конфликте документов используется следующий приоритет:

```text
1. MENTAURY_CANON_V0.1.md
2. MENTAURY_P0_IMPLEMENTATION_PLAN.md
3. CURRENT_STATUS.md
4. MENTAURY_CHARACTER_AND_PRESENCE_SPEC_V0.1.md
5. EXPERIMENT_LOG.md
6. PROJECT_HISTORY.md
7. MENTAURY_QUICK_REFERENCE.md
```

Quick Reference всегда уступает authoritative source.

---

## 14. 🔗 Основные документы

- [🧬 Mentaury Canon v0.1](MENTAURY_CANON_V0.1.md)
- [🛠️ P0 Implementation Plan v0.3](MENTAURY_P0_IMPLEMENTATION_PLAN.md)
- [🚦 Current Status](CURRENT_STATUS.md)
- [🎭 Character & Presence Spec v0.1](MENTAURY_CHARACTER_AND_PRESENCE_SPEC_V0.1.md)
- [🔬 Experiment & Audit Ledger](EXPERIMENT_LOG.md)
- [📜 Project History](PROJECT_HISTORY.md)

---

## 🏁 One-Line Summary

> **Mentaury строит не имитацию личности, а проверяемую непрерывность происхождения, знаний, решений и характера — с возможностью исправления, строгими границами власти и независимой проверкой изменений.**
