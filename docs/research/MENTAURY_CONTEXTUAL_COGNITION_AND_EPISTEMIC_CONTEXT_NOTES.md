# 🧭 Mentaury Contextual Cognition & Epistemic Context — Architecture Decision Record

```text
Статус:                       ARCHITECTURE_DECISION_RECORD · INTEGRATION_HISTORY
                               NON_AUTHORITATIVE_INDEX · NON_CANONICAL · DOCS_ONLY
Версия:                       0.4
Дата:                         2026-08-07
Runtime authority:            NONE
Truth authority:              NONE
Capability authority:         NONE
Identity authority:           NONE
Canon modification authority: NONE
Прямая запись в M3:           FORBIDDEN
Domain runtime:               NOT AUTHORIZED
Roadmap priority:              P1-001 UNCHANGED
```

> **2026-08-07 (после independent review):** этот документ больше **не**
> содержит нормативные схемы, полные scenario/metamorphic definitions или
> pipeline как источник истины. Он фиксирует **решение** (что было
> предложено, что принято, куда распределено, что нашёл review) и
> **историю** интеграции. Каждый контракт имеет ровно одно нормативное
> определение — в своём owning-документе. Этот файл — decision record,
> не спецификация.

```text
Decision Record ≠ normative specification
```

---

## 1. 🎯 Исходная проблема

Три research-gap были обнаружены при обсуждении того, как Mentaury должен
общаться и рассуждать в разных контекстах:

1. **Отсутствие модели адаптации подачи** под конкретного собеседника
   (новичок / эксперт / ребёнок), сохраняющей одинаковый epistemic
   результат.
2. **Отсутствие composable выбора методов и глубины проверки** под тип
   задачи (код / наука / бытовой разговор), без создания нескольких
   несогласованных personas.
3. **Отсутствие модели институционального контекста** (funding, conflicts
   of interest, replication, evidence scarcity, suppression claims) для
   честной, но не конспирологической оценки научных claims.

---

## 2. 🚫 Почему не создавались три новых engines

Прямая реализация трёх runtime engines (Audience Model, Cognitive Router,
Institutional Epistemic Context Engine) была отклонена:

```text
Ни один research-gap
≠ основание для нового runtime engine

Docs-only extension существующих owning-документов
> три параллельных authority-центра
```

Причины:

- **Audience/Character authority уже существует** (Character & Presence
  Spec, `PRESENTATION_ONLY`) — новый Audience Model engine создал бы
  competing presentation authority;
- **Governed Synthesis, Curiosity Policy и Question Classes уже
  существуют** (Identity Continuity Notes) — Cognitive Router создал бы
  вторую synthesis-подобную authority;
- **Research Source Admission Gate уже существует** (Identity Continuity
  §15) — отдельный Institutional Epistemic Context Engine создал бы
  второй Evidence/Admission Gate;
- ни одна из трёх моделей не требует нового semantic event type или P0
  runtime расширения — все они docs-only presentation/method-selection/
  evidence-context контракты.

---

## 3. 🔀 Рассмотренные альтернативы

| Альтернатива | Почему отклонена |
|---|---|
| Жёсткие `CODE_MODE` / `SCIENCE_MODE` / `CASUAL_MODE` personas | Создали бы несколько несогласованных identity-подобных режимов вместо одной composable профили |
| Единый новый `Contextual Cognition Engine` для всех трёх моделей | Второй authority-центр, конкурирующий с Character/Governed Synthesis/Source Admission |
| Три отдельных новых top-level spec-файла | Дублирование существующих Character/Identity/Genesis authority boundaries вместо их расширения |
| Оставить все три модели только в этом integration note как «shadow spec» | Создаёт two sources of truth (integration note + фактическое использование) — отклонено independent review как BLOCKER 2 |

**Принято:** расширить три существующих owning-документа, сохранив этот
файл только как decision record.

---

## 4. 📦 Принятое распределение ownership

| Контракт | Owning document |
|---|---|
| Contextual Communication Adaptation | `docs/MENTAURY_CHARACTER_AND_PRESENCE_SPEC_V0.1.md` |
| Cognitive Requirement Profile | `docs/research/MENTAURY_IDENTITY_CONTINUITY_AND_RELATIONAL_ARCHITECTURE_NOTES.md` |
| Institutional Epistemic Context | `docs/research/GENESIS_HERITAGE_INTERPRETATION_AND_HUMAN_ATLAS_NOTES.md` |

Найденное при распределении отклонение от первоначально предложенной
карты: `research_source_record` (source-level admission,
`independence_class`) физически принадлежит **Identity Continuity §15**,
а не Genesis Heritage. Institutional Epistemic Context размещён в Genesis
Heritage согласно плану (claim-level анализ funding/conflicts/replication),
но с явным cross-reference на Identity Continuity §15, чтобы не создать
второй Admission/Evidence Gate под похожим именем.

---

## 5. 🏛️ Authority matrix (высокий уровень)

| Область | Может определять | Не может определять |
|---|---|---|
| Task classification | требования задачи | truth status |
| Cognitive Requirement Profile | methods, verification depth, budgets, tool planning | permission, identity, M3 |
| Capability Lease Check | authorized/denied статус конкретного tool | truth, identity, values |
| Evidence assessment | support, contradiction, uncertainty | presentation style |
| Institutional Epistemic Context | provenance, incentives, dependency, replication gaps | automatic truth inversion |
| Governed Synthesis | bounded conclusion и unresolved tensions | capability grant |
| Contextual Communication Adaptation | vocabulary, structure, pace, examples | claims, confidence, evidence weight |
| Character | final presentation | reasoning result |

Полные определения — в owning-документах (§9).

---

## 6. 🔍 Решения независимого review (2026-08-07)

Первый round независимого review вернул **CHANGES_REQUIRED**. Найденные
дефекты и их исправление:

| # | Находка | Исправление | Где |
|---|---|---|---|
| BLOCKER 1 | Pipeline допускал retrieval/tool execution до capability check (`Tool availability ≠ authorization to use tool` нарушался) | Разделены planning / authorization / execution: `Retrieval / Tool Plan → Capability Lease Check → Scope Check → Privacy/Consent Check → Authorized Retrieval / Tool Execution` | Identity Continuity §20.3 |
| BLOCKER 1 | `tools` schema не различала запрошенную ссылку и подтверждённое разрешение | Добавлены `authorization_status`, `authorized_tools`, `denied_tools`; `requested_capability_refs` явно помечен как не-разрешение | Identity Continuity §20.5 |
| BLOCKER 2 | Integration note дублировал полные схемы/pipeline/scenarios/tests наравне с owning-документами (two sources of truth) | Этот файл сокращён до decision record; полные определения удалены, оставлены только ссылки на разделы | Этот файл |
| BLOCKER 3 | Одинаковые scenario/metamorphic ID были определены дважды (integration note + owning document) | Каждый ID имеет ровно одно нормативное определение в owning-документе; здесь — только диапазоны-ссылки | Этот файл, §9 |
| §7 | Вставка Institutional Epistemic Context сдвинула 7 разделов Genesis Heritage | Перемещено в конец как `Appendix A` / §21; нумерация §1–§20 восстановлена без изменений | Genesis Heritage §21 |
| §8 | Формулировка «перенесено ... после архитектурного review» подразумевала APPROVE, которого не было | Заменено на «предварительно распределено ... ожидает independent review» во всех трёх owning-документах | Character Spec, Identity Continuity, Genesis Heritage |
| §6 | Contextual Cognition визуально показан как второй roadmap milestone рядом с P1-001 | README/Quick Reference разделяют execution roadmap (P1-001) и research side-tracks | README.md, Quick Reference |

```text
Distribution drafted ≠ distribution adopted
Independent review round 1 ≠ independent review PASS
PR remains DRAFT until owner/independent-reviewer acceptance
```

---

## 7. 📊 Integration Status Table

| Contract | Owning document (exact section) | Draft status | Independent review | Runtime |
|---|---|---|---|---|
| Contextual Communication Adaptation | [`MENTAURY_CHARACTER_AND_PRESENCE_SPEC_V0.1.md`](../MENTAURY_CHARACTER_AND_PRESENCE_SPEC_V0.1.md) §6.4, §10 (CCA-SC-001…007), §11 (MT-CCA-001…002) | DRAFTED | CHANGES_ADDRESSED / PENDING RE-REVIEW | NOT AUTHORIZED |
| Cognitive Requirement Profile | [`MENTAURY_IDENTITY_CONTINUITY_AND_RELATIONAL_ARCHITECTURE_NOTES.md`](MENTAURY_IDENTITY_CONTINUITY_AND_RELATIONAL_ARCHITECTURE_NOTES.md) §20, §16.9 (CRP-SC-001…008) | DRAFTED | CHANGES_ADDRESSED / PENDING RE-REVIEW | NOT AUTHORIZED |
| Institutional Epistemic Context | [`GENESIS_HERITAGE_INTERPRETATION_AND_HUMAN_ATLAS_NOTES.md`](GENESIS_HERITAGE_INTERPRETATION_AND_HUMAN_ATLAS_NOTES.md) §21 Appendix A (IEC-SC-001…009, MT-IEC-001…003) | DRAFTED | CHANGES_ADDRESSED / PENDING RE-REVIEW | NOT AUTHORIZED |

Статус становится `REVIEWED · READY_FOR_OWNER_ACCEPTANCE` только после
успешного повторного independent review, и `ADOPTED` — только после
merge PR #36 в `main`. До тех пор он остаётся `DRAFTED`.

---

## 8. 🧪 Scenario / metamorphic ID index (ссылки, не определения)

Каждый ID определён **ровно один раз**, в своём owning-документе. Здесь —
только диапазоны для навигации.

```text
CCA-SC-001…007  → Character Spec §10
MT-CCA-001…002  → Character Spec §11
CRP-SC-001…008  → Identity Continuity §16.9 (index) / §20.9 (full metamorphic tests)
MT-CRP-001…003  → Identity Continuity §20.9
IEC-SC-001…009  → Genesis Heritage §21 (Appendix A.6)
MT-IEC-001…003  → Genesis Heritage §21 (Appendix A.7)
```

---

## 9. 🔗 Ссылки на authoritative sections

- [Contextual Communication Adaptation — Character Spec §6.4](../MENTAURY_CHARACTER_AND_PRESENCE_SPEC_V0.1.md)
- [Cognitive Requirement Profile — Identity Continuity §20](MENTAURY_IDENTITY_CONTINUITY_AND_RELATIONAL_ARCHITECTURE_NOTES.md)
- [Institutional Epistemic Context — Genesis Heritage §21 Appendix A](GENESIS_HERITAGE_INTERPRETATION_AND_HUMAN_ATLAS_NOTES.md)
- [Post-P0 Roadmap v0.1](POST_P0_ROADMAP_V0.1.md)
- [Current Status](../CURRENT_STATUS.md)

---

## 10. 📜 История PR / commits / review

```text
PR:              #36 — docs: define contextual cognition research contracts
Branch:          agent/contextual-cognition-notes
Base:            main

736f49b  docs: add contextual cognition research notes
338ef67  docs: refine contextual cognition contract
42adcfe  docs(identity-continuity): integrate Cognitive Requirement Profile
c772d79  docs(genesis-heritage): integrate Institutional Epistemic Context
2c20574  docs(character): integrate Contextual Communication Adaptation
5961b3d  docs(contextual-cognition): add integration status table
9411663  docs(nav): link contextual cognition research from Quick Reference/README
```

```text
Review round 1: CHANGES_REQUIRED (pipeline ordering, decision-record
                 conversion, ID duplication, Genesis renumbering,
                 "after review" wording, README milestone separation)
Fixes applied:  see §6 above
Review round 2: PENDING (this document reflects the state after fixes,
                 before re-review)
```

PR остаётся **draft** и **не смержен**.

---

## 11. 🚫 Non-claims / Deferred runtime work

```text
❌ Audience Model runtime
❌ психологическое профилирование человека
❌ отдельные личности для code / science / conversation
❌ Character Engine или Governed Synthesis Engine
❌ Cognitive Router runtime
❌ Institutional Epistemic Context Engine
❌ Capability Lease Resolver implementation
❌ автоматическое изменение evidence weight по sponsor identity
❌ автоматическое недоверие к scientific consensus
❌ прямой write path в M2 или M3
❌ Tool execution / Action Gate
❌ изменения в src/mentaury/
❌ изменение Canon
❌ изменение P1-001 priority
❌ Contextual Cognition как новый roadmap milestone
```

До runtime prototype необходимы (не выполнено этим документом):

```text
reviewed docs → explicit owner GO → separate RFC
→ threat model and privacy analysis → bounded budgets
→ replayable decision receipts → adversarial corpus
→ multilingual / paraphrase tests → false-positive / false-negative report
→ rollback path
```

```text
Docs completeness ≠ runtime safety
Runtime prototype  ≠ production authorization
```

---

## 12. 📚 Notion sync policy

Notion **не синхронизируется** как current architecture до merge PR #36 и
успешного independent review.

```text
GitHub main → authoritative technical contract
Notion      → explanation, decision history and navigation
```

После merge Notion получает только:

- human-readable summary для трёх контрактов;
- ссылку на merged PR и merged SHA;
- `DOCS_ONLY · NOT IMPLEMENTED` marker;
- rationale и rejected alternatives (§3 этого документа);
- явную отметку, что P1-001 priority не изменён.

Полные YAML-схемы **не копируются** в Notion.

---

## 🏁 Итог

```text
Contextual Communication Adaptation
→ explains differently, does not change truth
→ authoritative definition: Character Spec §6.4

Cognitive Requirement Profile
→ selects methods and depth, does not change identity or authority
→ tool planning ≠ tool authorization ≠ tool execution
→ authoritative definition: Identity Continuity §20

Institutional Epistemic Context
→ exposes incentives, dependencies and evidence gaps
→ does not replace evidence with suspicion
→ authoritative definition: Genesis Heritage §21 Appendix A

This document
→ DECISION RECORD, not a normative specification
→ DOCS_ONLY · NO RUNTIME AUTHORITY · P1-001 PRIORITY UNCHANGED
→ PR #36 remains DRAFT, not merged, Notion not synchronized
```
