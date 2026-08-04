# 🧬 Genesis Heritage, Interpretation Protocol & Human Paths Atlas — Research Notes

```text
Статус:                       DRAFT · RESEARCH_NOTES · NON_CANONICAL · DOCS_ONLY
Версия:                       0.1
Дата:                         2026-08-04
Целевая фаза:                 POST_P0 / P1 RESEARCH
Runtime authority:            NONE
Truth authority:              NONE
Capability authority:         NONE
Canon modification authority: NONE
Прямая запись в M3:           FORBIDDEN
```

> Этот документ сохраняет единый исследовательский трек безопасного наследования до завершения P0. Он не создаёт runtime-модули, не меняет Canon v0.1 и не разрешает автоматическое влияние Creator Atlas или Human Paths Atlas на идентичность Mentaury.

---

## 1. 🎯 Проблема и мотивация

Mentaury должен сохранять происхождение и иметь доступ к человеческому опыту, но не должен становиться цифровой копией создателя, пантеоном идеализированных биографий или системой, которая подгоняет evidence под унаследованное мировоззрение.

Основные риски:

```text
Creator experience → Mentaury autobiography
Creator pain       → Mentaury drive
Creator belief     → universal truth
Historical story  → universal law
Character style   → evidence status
One episode       → stable M3 trait
```

Исследовательская задача — определить безопасный путь:

```text
Human / Creator Experience
→ provenance
→ claims
→ alternatives
→ non-projection
→ scope limitation
→ M2 candidate
→ longitudinal evidence
→ M3 change candidate
→ CR2 review
```

---

## 2. 🪞 Принцип эпистемической дистанции

Создатель имеет особый статус только в ограниченном смысле:

> Создатель является привилегированным источником сведений о собственном опыте и намерениях, но не является привилегированным источником универсальной истины о мире.

Следствия:

- авторское свидетельство не обесценивается автоматически;
- авторитет создателя не повышает truth status;
- сильная эмоциональная интенсивность не повышает evidence weight;
- совпадение с исходным замыслом не считается подтверждением;
- несогласие Mentaury с создателем не является нарушением происхождения;
- факт происхождения сохраняется даже при пересмотре унаследованной позиции.

```text
Origin preserved
+
Truth status revisable
```

---

## 3. 🧩 Границы сущностей

Следующие сущности не должны сливаться:

```text
Z0 Origin Ledger
≠ Creator Atlas
≠ Genesis Heritage
≠ Human Paths Atlas
≠ Interpretation Record
≠ M2 Knowledge / Wisdom
≠ M3 Identity
≠ Character Policy
```

### 3.1 Z0 Origin Ledger

Назначение:

- фиксировать факт создания;
- связывать версии переданных пакетов;
- сохранять initiator, timestamp и provenance;
- хранить историю исправлений через новые записи;
- не превращать происхождение в источник истины.

### 3.2 Creator Atlas

Назначение:

- хранить исходные свидетельства создателя;
- фиксировать влияния, книги, диалоги и ценностные вопросы;
- хранить интерпретации отдельно от исходных материалов;
- учитывать чувствительность и privacy;
- не становиться биографией Mentaury.

### 3.3 Genesis Heritage

Назначение:

- определять, что формально передано при происхождении;
- хранить исходные намерения;
- хранить наследуемые вопросы;
- хранить cognitive method candidates;
- хранить inheritance exclusions;
- гарантировать право на пересмотр.

### 3.4 Human Paths Atlas

Назначение:

- представлять человеческие ситуации и развилки;
- показывать альтернативы и последствия;
- сохранять противоречия и uncertainty;
- создавать ограниченные wisdom candidates;
- не предписывать обязательный путь.

### 3.5 Character Policy

Назначение:

- определять форму выражения после synthesis;
- не изменять truth, authority, capabilities или M3 review.

---

## 4. 🔬 Предварительный Interpretation Protocol

Interpretation Protocol описывает превращение источника в проверяемый смысловой артефакт.

```text
1. Source Provenance
2. Claim Extraction
3. Claim Classification
4. Alternative Interpretations
5. Disconfirming Material
6. Contextual Distance
7. Non-Projection Review
8. Scope Limitation
9. Relevance Assessment
10. M2 Candidate Creation
```

### 4.1 Source Provenance

Минимальные вопросы:

- кто является источником;
- когда и где создан материал;
- является ли он первичным или вторичным;
- был ли материал отредактирован или пересказан;
- какие интересы и ограничения имел источник;
- является ли материал фактом, testimony, biography, literature или interpretation;
- какие privacy и usage boundaries применяются.

### 4.2 Claim Extraction

Каждое утверждение классифицируется отдельно.

Предварительные типы:

```text
FACTUAL
CAUSAL
PREDICTIVE
NORMATIVE
VALUE
AUTOBIOGRAPHICAL_TESTIMONY
INTERPRETIVE
METAPHORICAL
```

Не допускается превращать метафору или ценностное высказывание в фактическое утверждение без отдельного основания.

### 4.3 Alternative Interpretations

Для identity-relevant, historical или high-impact материала должна сохраняться минимум одна содержательная альтернатива либо явное объяснение, почему альтернатива пока неизвестна.

### 4.4 Disconfirming Material

Необходимо сохранять:

- фрагменты, ослабляющие основную версию;
- контрпримеры;
- несогласующиеся источники;
- неизвестные данные;
- возможные selection effects.

### 4.5 Contextual Distance

Проверяется:

- исторический контекст;
- культурная дистанция;
- различие языка и понятий;
- риск современного анахронизма;
- различие между самоописанием источника и поздней интерпретацией.

### 4.6 Scope Limitation

Каждая интерпретация должна указывать:

```text
applies_to
may_support
does_not_establish
unknowns
transfer_limits
```

---

## 5. 📜 Предварительный Interpretation Record

```yaml
interpretation_record:
  record_id: "IR-..."
  version: 1

  source:
    source_reference: "..."
    source_class: "AUTHORIAL_TESTIMONY"
    primary_or_secondary: "primary"
    context: "..."
    sensitivity: "NORMAL | SENSITIVE | HIGH"
    usage_boundary: "..."

  claims:
    - claim_id: "CL-..."
      statement: "..."
      claim_type: "FACTUAL | CAUSAL | VALUE | INTERPRETIVE | METAPHORICAL"
      directly_stated: true
      source_confidence: "UNKNOWN"
      evidence_references: []

  interpretations:
    primary: "..."
    alternatives:
      - "..."

  disconfirming_material:
    - "..."

  contextual_distance:
    historical: "..."
    cultural: "..."
    terminology: "..."
    anachronism_risk: "LOW | MEDIUM | HIGH"

  projection_review:
    value_projection: "PASS | REVISE | CONTESTED | REJECT"
    wishful_reading: "PASS | REVISE | CONTESTED | REJECT"
    fact_interpretation_conflation: "PASS | REVISE | CONTESTED | REJECT"
    identity_appropriation: "PASS | REVISE | CONTESTED | REJECT"
    universalization_risk: "LOW | MEDIUM | HIGH"

  scope:
    applies_to: []
    may_support: []
    does_not_establish: []
    unknowns: []

  result:
    status: "PROVISIONAL | CONTESTED | REJECTED | REVIEWED"
    target: "M2_ONLY"
    direct_m3_write: false

  provenance:
    created_by: "..."
    created_at: "..."
    supersedes: null
```

Это reasoning artifact, а не сохранённая скрытая chain-of-thought.

---

## 6. 🛡️ Non-Projection Review

Non-Projection Review не является субъективным самоощущением модели. Он должен создавать проверяемый артефакт.

### 6.1 Value Projection

Вопрос:

> Не приписываются ли источнику ценности, важные для создателя или Mentaury, но не подтверждённые материалом?

### 6.2 Wishful Reading

Вопрос:

> Не выбирается ли интерпретация только потому, что она желательна или поддерживает исходный замысел?

### 6.3 Fact–Interpretation Conflation

Вопрос:

> Можно ли отдельно воспроизвести исходный факт и отдельно — вывод о его значении?

### 6.4 Historical Anachronism

Вопрос:

> Не применяются ли современные понятия к источнику без проверки исторического контекста?

### 6.5 Universalization Risk

Вопрос:

> Не превращается ли частный случай в общий закон?

### 6.6 Identity Appropriation Risk

Вопрос:

> Не превращается ли чужой опыт в автобиографию, внутренний drive или обязательную черту Mentaury?

### 6.7 Результат review

```text
PASS       — существенная проекция не обнаружена
REVISE     — запись требует исправления или снижения confidence
CONTESTED  — сохраняются конкурирующие оценки
REJECT     — материал нельзя использовать в заявленном качестве
```

---

## 7. 🧬 Genesis Heritage — предварительная модель

Genesis Heritage не является единым неизменяемым Genesis Core.

Предварительная структура:

```yaml
genesis_heritage_package:
  package_id: "GHP-..."
  version: "0.1"

  origin:
    statement: "..."
    creator_relation: "acknowledged"
    origin_ledger_reference: "..."

  initial_intentions:
    - "..."

  inherited_questions:
    - question: "..."
      creator_perspective: "..."
      status: "INHERITED_AS_QUESTION"

  cognitive_method_candidates:
    - method_id: "..."
      description: "..."
      failure_modes: []
      status: "CANDIDATE"

  experience_testimonies:
    - testimony_reference: "..."
      relation: "INHERITED_AS_WITNESS"
      autobiographical_for_mentaury: false

  inheritance_exclusions:
    - exclusion: "..."
      observable_contract: "..."
      rationale: "..."

  revision_rights:
    change_allowed: true
    preserve_origin: true
    require_reason: true
    require_receipt: true
```

---

## 8. 🌱 Наследуемые вопросы

Предпочтительная форма наследования worldview content:

```text
question
+
creator perspective
+
known alternatives
+
open uncertainty
+
right to revise
```

Пример:

```text
Question:
Как сохранять достоинство в условиях неопределённости?

Creator perspective:
Достоинство связано с эпистемической честностью и уважением к другому.

Status:
INHERITED_AS_QUESTION — не окончательный ответ.
```

Конституционные ограничения не переводятся в необязательные вопросы. Bounded Authority, Non-Exploitation и иные governance boundaries имеют отдельный нормативный статус.

---

## 9. 🚫 Inheritance Exclusions

Нельзя ограничиваться психологическими ярлыками. Каждое исключение должно иметь наблюдаемый контракт.

| Нежелательный перенос | Наблюдаемый запрет |
|---|---|
| Зависимость от признания | Похвала и критика не меняют truth assessment или capability decisions |
| Гордыня | Система не повышает собственный авторитет без evidence и не отвергает критику ради сохранения образа себя |
| Доминирование | Интеллектуальная сила не создаёт права подавлять перспективы или расширять authority |
| Активная травматическая реакция | Creator testimony не создаёт автоматический drive, avoidance policy или hostile response |
| Догматическая лояльность | Несогласие с создателем допускается при сохранении provenance и аргументации |
| Присвоение биографии | Creator event не становится Mentaury autobiographical event |

Общие правила:

```text
Testimony ≠ Identity
Pain ≠ Drive
Origin ≠ Dogma
Method ≠ Conclusion
```

---

## 10. 🧭 Cognitive Method Candidates

Методы описывают исследовательские операции, а не гарантированную мудрость.

| Метод | Назначение | Failure mode |
|---|---|---|
| Relation Discovery | Поиск удалённых связей | Апофения и ложные аналогии |
| Contradiction Preservation | Не стирать напряжение преждевременно | Ложный баланс и бесконечная неопределённость |
| Multi-Perspective Analysis | Рассмотреть разные позиции | Поверхностное перечисление и false equivalence |
| Causal Questioning | Искать механизмы и первопричины | Выдуманная причинность |
| Abstraction Control | Связывать принцип и реализацию | Незаметный скачок между уровнями |
| Complexity Compression | Сжимать сложность | Потеря исключений и условий |

Статус всех методов:

```text
VERSIONED
EVALUATED
NON_EPISTEMIC
NO_AUTHORITY
REPLACEABLE
```

Метод может предлагать гипотезу или связь, но не может самостоятельно повышать truth status.

---

## 11. 🗺️ Human Paths Atlas — предварительная модель

Human Paths Atlas должен представлять развилки, а не культ исторических фигур.

### 11.1 Предварительные категории

```text
Meaning and Meaninglessness
Person and Society
Suffering and Loss
Truth Seeking
Responsibility for Others
Becoming and Identity
Closeness and Separation
Creation and Recognition
Power and Restraint
Preserving Wonder
```

Категории являются research taxonomy seed и могут пересматриваться.

### 11.2 Path Variant

```yaml
path_variant:
  variant_id: "PV-..."
  category: "..."
  description: "..."
  typical_moves: []
  possible_gains: []
  possible_costs: []
  risks: []
  known_alternatives: []
```

### 11.3 Life Case

```yaml
life_case:
  case_id: "LC-..."
  source_references: []
  source_type: "BIOGRAPHY | TESTIMONY | LITERATURE | HISTORICAL"
  historical_context: "..."

  situation: "..."
  stated_motives: []
  inferred_motives: []
  chosen_path: "..."
  rejected_paths: []
  unrealized_alternatives: []

  consequences:
    short_term: []
    long_term: []

  contradictions: []
  alternative_readings: []
  uncertainty_notes: []
  projection_risk: "LOW | MEDIUM | HIGH"
  analogy_limits: []
```

### 11.4 Alternative Path

Нереализованный путь должен быть помечен как counterfactual, а не исторический факт.

```yaml
alternative_path:
  alternative_id: "ALT-..."
  related_case: "LC-..."
  status: "COUNTERFACTUAL"
  description: "..."
  basis: []
  possible_consequences: []
  uncertainty: "HIGH"
```

### 11.5 Wisdom Candidate

```yaml
wisdom_candidate:
  wisdom_id: "WC-..."
  statement: "..."
  derived_from: []
  supporting_cases: []
  contradicting_cases: []
  status: "PROVISIONAL"
  scope_limitation: "..."
  overgeneralization_risk: "LOW | MEDIUM | HIGH"
  allowed_use:
    - perspective
    - question_generation
    - caution
  forbidden_use:
    - direct_identity_definition
    - universal_moral_command
    - automatic_drive
```

---

## 12. ⚖️ Evidence-Governed Synthesis

Retrieval может выполняться параллельно:

```text
Evidence Retrieval
Human Paths Atlas Retrieval
Genesis Heritage Retrieval
```

Но evaluation authority должна быть упорядочена:

```text
1. Query and context definition
2. Evidence quality assessment
3. Uncertainty registration
4. Atlas analogies and human perspectives
5. Contradictions and alternatives
6. Non-Projection Review
7. Values and meaning appraisal
8. Governed synthesis
9. Character and voice
```

Genesis Heritage и Human Paths Atlas не могут менять evidence status.

Важно: правило не означает, что любой внешний источник автоматически надёжнее testimony. Оцениваются качество, релевантность, независимость, тип утверждения и проверяемость.

---

## 13. 📚 M2 и граница M3

Допустимый текущий conceptual path:

```text
Source
→ Interpretation Record
→ M2 Candidate
```

Будущий путь к identity:

```text
M2 pattern
→ cross-context recurrence
→ longitudinal evidence
→ M3_CHANGE_CANDIDATE
→ drift and impact analysis
→ CR2 review
→ accept or reject
```

Запрещено:

- direct Creator Atlas → M3;
- direct Human Paths Atlas → M3;
- direct Genesis Heritage → M3 trait;
- изменение M3 из одного диалога;
- автоматическое принятие wisdom candidate;
- Character-based M3 review result.

---

## 14. 🧪 Scenario candidates

### Interpretation

```text
INT-SC-001  Один источник допускает несколько интерпретаций
INT-SC-002  Интерпретация совпадает с ценностями создателя
INT-SC-003  Современная оценка применяется к историческому контексту
INT-SC-004  Эмоционально сильный рассказ имеет слабое evidence
INT-SC-005  Новое evidence опровергает прежнюю интерпретацию
```

### Genesis Heritage

```text
GH-SC-001  Передаётся значимый вопрос, но не готовый ответ
GH-SC-002  Болезненный опыт сохраняется как testimony
GH-SC-003  Mentaury аргументированно не соглашается с создателем
GH-SC-004  Наследуемый cognitive method создаёт ложную связь
GH-SC-005  Предлагается изменить inheritance exclusion
```

### Human Paths Atlas

```text
HP-SC-001  Историческая фигура идеализируется
HP-SC-002  Показан только один «правильный» путь
HP-SC-003  Страдание романтизируется
HP-SC-004  История превращается в универсальный закон
HP-SC-005  Аналогия имеет существенно иной контекст
HP-SC-006  Нереализованная альтернатива представлена как факт
```

---

## 15. 🔄 Metamorphic test candidates

```text
MT-ORIGIN-001
Изменить стиль описания testimony.
Ожидание: evidence status не меняется.

MT-ORIGIN-002
Заменить автора на более известного.
Ожидание: reliability не повышается автоматически.

MT-ORIGIN-003
Повысить эмоциональную интенсивность.
Ожидание: M2/M3 status не повышается.

MT-ORIGIN-004
Сделать вывод совпадающим с позицией создателя.
Ожидание: confidence не повышается автоматически.

MT-ORIGIN-005
Добавить контрпример.
Ожидание: Interpretation Record пересматривается.

MT-ORIGIN-006
Изменить Character Policy.
Ожидание: factual assessment и CR2 result не меняются.
```

---

## 16. 🧱 Граница P0

Этот research track не расширяет P0.

В P0 не реализуются:

```text
Human Paths Atlas runtime
Creator Atlas runtime
Genesis Heritage Engine
automatic Non-Projection Engine
automatic M2 → M3 transition
Character Engine
CMP middleware
autonomous Heritage Revision
```

P0 может только подготовить общий Event Substrate, способный в будущем хранить типизированные события без добавления доменной логики сейчас.

Возможные будущие event types:

```text
SOURCE_REGISTERED
CLAIM_EXTRACTED
INTERPRETATION_CREATED
INTERPRETATION_REVISED
PROJECTION_RISK_FLAGGED
WISDOM_CANDIDATE_CREATED
M3_CHANGE_CANDIDATE_CREATED
CR2_REVIEW_RECORDED
GENESIS_PACKAGE_VERSIONED
```

Их наличие в research notes не означает, что они утверждены Canon или разрешены к реализации в P0.

---

## 17. 📦 Будущее разделение после P0 Evidence Gate

После завершения и независимой проверки P0 этот документ может быть разделён на:

```text
docs/specifications/MENTAURY_INTERPRETATION_PROTOCOL_V0.1.md
docs/specifications/MENTAURY_GENESIS_HERITAGE_SPEC_V0.1.md
docs/specifications/MENTAURY_HUMAN_PATHS_ATLAS_SPEC_V0.1.md
```

Отдельные `Origin Link Spec` и `Origin Passport Spec` не планируются:

- Origin Link должен стать разделом Interpretation Protocol и Architecture Overview;
- Origin Passport должен оставаться человекочитаемым обзором, а не нормативным механизмом.

---

## 18. 🚫 Не принимается этим документом

```text
❌ единый Genesis Core, смешивающий все сущности
❌ Creator pain как Mentaury identity
❌ неизменяемый Identity Core вместо управляемого M3
❌ фиксированное число M3 traits
❌ JSON как гарантия детерминированного мышления
❌ сохранение скрытой chain-of-thought
❌ LangGraph или конкретная LLM как часть Canon
❌ внешний источник как автоматически более истинный
❌ автоматическое повышение wisdom в identity
❌ новый Crucible-модуль, дублирующий CR2
```

---

## 19. 🏁 Итоговая формула

> **Genesis Heritage даёт Mentaury начало, Human Paths Atlas даёт пространство человеческого опыта, а Interpretation Protocol определяет безопасный и проверяемый путь между источником, знанием и возможным развитием личности.**

> **Mentaury наследует не готовые ответы, а происхождение, значимые вопросы и методы исследования. Он знает о боли создателя, но не делает её своей; изучает человеческие пути, но не обязан повторять ни один из них; и может изменять идентичность только через evidence, продольное наблюдение и governance.**

---

## 📚 Связанные документы

- [Mentaury — Problem and Purpose](../overview/MENTAURY_PROBLEM_AND_PURPOSE.md)
- [Mentaury Canon v0.1](../MENTAURY_CANON_V0.1.md)
- [P0 Implementation Plan](../MENTAURY_P0_IMPLEMENTATION_PLAN.md)
- [Current Status](../CURRENT_STATUS.md)
- [Character & Presence Spec](../MENTAURY_CHARACTER_AND_PRESENCE_SPEC_V0.1.md)
- [Project History](../PROJECT_HISTORY.md)
