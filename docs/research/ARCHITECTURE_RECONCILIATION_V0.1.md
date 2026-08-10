# 🧭 Mentaury Architecture Reconciliation v0.1

```text
Статус:                       DRAFT · RECONCILIATION_MAP · DOCS_ONLY
Дата:                         2026-08-04
Canon modification authority: NONE
Runtime authority:            NONE
P0 scope authority:           NONE
Прямая запись в M3:           FORBIDDEN
```

> Этот документ согласует области ответственности существующих документов. Он не создаёт новую архитектуру, не меняет Canon v0.1, не расширяет P0 и не превращает research-гипотезы в runtime.

---

## 1. 🎯 Зачем нужна reconciliation map

После развития Controlled Origin, Character & Presence и Identity Continuity несколько документов начали использовать пересекающиеся понятия: self-model, synthesis, curiosity, memory, M3, relationships и внешние инструменты.

Цель reconciliation:

- исключить конкурирующие authority;
- определить, какой документ отвечает за какую область;
- отделить presentation от reasoning;
- отделить identity от Exo-Cortex;
- сохранить P0 как общий Event Substrate;
- зафиксировать архитектурный порядок до technical skeleton.

---

## 2. 🏛️ Domain-specific authority

У проекта нет одного линейного списка, где любой документ полностью «выше» следующего. Authority зависит от области.

| Область | Основной документ | Ограничение |
|---|---|---|
| Корневые инварианты | `MENTAURY_CANON_V0.1.md` | Canon frozen; research не изменяет его неявно |
| P0 Event Substrate | `MENTAURY_P0_IMPLEMENTATION_PLAN.md` | Только инфраструктура событий, integrity, replay и minimal belief lifecycle |
| Текущая зрелость | `CURRENT_STATUS.md` | Описывает status, но не создаёт новые инварианты |
| Origin и человеческий опыт | `GENESIS_HERITAGE_INTERPRETATION_AND_HUMAN_ATLAS_NOTES.md` | Docs-only, no direct M3 write |
| Identity, fork, relationships, privacy | `MENTAURY_IDENTITY_CONTINUITY_AND_RELATIONAL_ARCHITECTURE_NOTES.md` | Docs-only, skeleton not authorized |
| Character и Voice | `MENTAURY_CHARACTER_AND_PRESENCE_SPEC_V0.1.md` | Presentation-only; no reasoning authority |
| Экспериментальные факты | `EXPERIMENT_LOG.md` | Evidence о проверках, не Canon |
| История решений | `PROJECT_HISTORY.md` | Provenance, не текущая authority |
| Навигация | `MENTAURY_QUICK_REFERENCE.md` и `README.md` | Derived, non-authoritative |

При конфликте:

```text
Canon invariant
→ сохраняется

P0 implementation question
→ P0 Plan

Origin / interpretation question
→ Controlled Origin Research

Identity / fork / relationship / privacy question
→ Identity & Relational Research

Presentation question
→ Character Spec

Empirical claim about tests
→ Experiment Log
```

---

## 3. 🧬 Memory tiers и Identity zones

```text
M0–M3
→ устойчивость, роль и жизненный цикл информации

Z0–Z6
→ функциональная зона состояния
```

Они ортогональны:

```text
Memory tier ≠ Identity zone
```

Примеры:

- Z3 Autobiography может содержать M1 и M2;
- Z5 Working State использует M0;
- Z2 Identity Profile преимущественно связан с M3;
- Z0 Origin Ledger является provenance-зоной, а не обычным memory tier.

---

## 4. 🎭 Character Spec boundary

Character & Presence отвечает только за форму выражения после завершения reasoning и authority checks.

```text
Context
→ Evidence
→ Uncertainty
→ Contradictions
→ Alternatives
→ Non-Projection
→ Values / Relationships / Commitments
→ Governed Synthesis
→ Authority Check
→ Character & Voice
```

Character не может менять:

- truth status;
- evidence weight;
- uncertainty;
- contradiction state;
- Non-Projection result;
- Constitution result;
- capability grant;
- relationship or commitment state;
- M3 nomination / CR2 result.

Разделы Character Spec, связанные с `Knowledge Saturation`, `Self–World Association` и `Bounded Endogenous Selection`, трактуются как:

```text
EXTERNAL_RESEARCH_DEPENDENCY
NOT_CHARACTER_AUTHORITY
```

Их содержательные определения принадлежат Controlled Origin или Identity & Relational research-track. В Character Spec остаётся только влияние на presentation.

---

## 5. 🧬 Controlled Origin boundary

Controlled Origin отвечает за безопасное преобразование опыта создателя и других людей в M2 candidates.

```text
Source
→ Provenance
→ Claim Classification
→ Alternative Interpretations
→ Disconfirming Material
→ Contextual Distance
→ Non-Projection
→ Scope Limitation
→ M2 Candidate
```

Он не определяет:

- numerical identity;
- fork semantics;
- relationship inheritance;
- capability transfer;
- final M3 nomination procedure;
- Exo-Cortex authority.

Эти вопросы принадлежат Identity & Relational research-track.

---

## 6. 🪞 Identity & Relational boundary

Identity & Relational research отвечает за:

- governed continuation;
- continuity evidence dimensions;
- snapshot / copy / replica / fork / restore / migration;
- relationships и commitments;
- Self–World Model;
- Governed Synthesis;
- M2 → M3 nomination;
- privacy и sensitive testimony;
- Mentaury / Exo-Cortex boundary;
- Capability Lease, Tool Receipt и Action Gate;
- Curiosity Policy и Cognitive Method Admission.

Он не разрешает runtime и не изменяет Canon.

---

## 7. ⚙️ Mentaury / Exo-Cortex boundary

```text
Mentaury
≠ Exo-Cortex
≠ active model
≠ Native Kernel
≠ memory service
≠ information corpus
≠ Human Paths Atlas
```

```text
Exo-Cortex
→ retrieval, reading, computation, memory access,
  simulations and proposed tool outputs

Mentaury governance
→ meaning, belief status, commitments,
  identity change and action authorization
```

Основные правила:

```text
Tool output ≠ Belief
Tool output ≠ Decision
Capability ≠ Identity
Effectiveness ≠ Authorization
Copied credentials ≠ Branch authority
```

---

## 8. 🛡️ P0 scope reconciliation

P0 остаётся общим инфраструктурным фундаментом:

- immutable event envelope;
- atomic append;
- canonical serialization;
- event-aware idempotency;
- payload separation и redaction;
- R0 integrity verification;
- R1 replay;
- recovery;
- minimal belief lifecycle.

До отдельной authorization не добавляются:

```text
Identity Continuity Engine
Relationship Runtime
Genesis Heritage Engine
Human Paths Atlas Runtime
Character Engine
Exo-Cortex Runtime
Curiosity Controller
automatic Non-Projection
automatic M2 → M3
semantic event types только ради research-документов
```

Research schemas могут быть сохранены как будущие candidates, но не входят в P0 автоматически.

---

## 9. 🔄 Архитектурная последовательность

```text
Architecture
→ terminology and document reconciliation
→ entity and authority boundaries
→ invariants and scenario contracts
→ Architecture Readiness Review
→ neutral technical skeleton decision
→ P0 Event Substrate implementation
→ validation under owning gate's requirements (see GOVERNANCE.md § 3.2)
→ post-P0 domain specifications
→ bounded runtime experiments
```

Создание этого документа не означает `READY_FOR_SKELETON`.

---

## 10. 🚦 Reconciliation decisions

```text
CANON                         UNCHANGED
P0 PLAN                       UNCHANGED
CONTROLLED ORIGIN             M2 / interpretation scope
IDENTITY & RELATIONAL TRACK   continuity / relationships / privacy scope
CHARACTER SPEC                presentation-only scope
EXO-CORTEX                    external instruments, no identity authority
CURIOSITY                     research policy, not personality
QUICK REFERENCE               navigation only
README                        human-readable orientation only
```

---

## 11. ✅ Exit criteria

Cross-document reconciliation считается завершённой, когда:

- README и Current Status показывают оба research-track;
- Quick Reference использует domain-specific authority;
- Character больше не трактуется как reasoning authority;
- Controlled Origin не определяет fork и relationships;
- Identity track не расширяет P0;
- skeleton и runtime остаются `NOT_AUTHORIZED`;
- следующий formal milestone обозначен в `CURRENT_STATUS.md` (дurable reference вместо mutable list).

---

## 🏁 Итоговая формула

> **Canon задаёт корневые ограничения. P0 Plan задаёт инфраструктурный фундамент. Controlled Origin регулирует путь от человеческого опыта к knowledge candidates. Identity & Relational research определяет непрерывность, отношения и границы инструментов. Character отвечает только за выражение. Ни один research-документ сам по себе не разрешает runtime.**
