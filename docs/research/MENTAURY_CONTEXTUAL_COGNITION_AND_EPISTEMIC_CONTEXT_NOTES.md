# 🧭 Mentaury Contextual Cognition, Communication & Epistemic Context — Research Notes

```text
Статус:                       DRAFT · RESEARCH_NOTES · NON_CANONICAL · DOCS_ONLY
Версия:                       0.1
Дата:                         2026-08-07
Owner direction:              PREPARE ARCHITECTURE + ENGINEERING HANDOFF
Runtime authority:            NONE
Truth authority:              NONE
Capability authority:         NONE
Identity authority:           NONE
Canon modification authority: NONE
Прямая запись в M3:           FORBIDDEN
Domain runtime:               NOT AUTHORIZED
Roadmap priority:              P1-001 UNCHANGED
```

> Этот документ формализует три исследовательских пробела: адаптацию объяснения к собеседнику, выбор когнитивного профиля под задачу и описание институционального контекста evidence. Он не создаёт новый центр authority, не меняет Canon, не разрешает Character Engine, Governed Synthesis Engine, LLM integration или autonomous runtime.

Связанные документы:

- [`MENTAURY_CHARACTER_AND_PRESENCE_SPEC_V0.1.md`](../MENTAURY_CHARACTER_AND_PRESENCE_SPEC_V0.1.md)
- [`MENTAURY_IDENTITY_CONTINUITY_AND_RELATIONAL_ARCHITECTURE_NOTES.md`](MENTAURY_IDENTITY_CONTINUITY_AND_RELATIONAL_ARCHITECTURE_NOTES.md)
- [`GENESIS_HERITAGE_INTERPRETATION_AND_HUMAN_ATLAS_NOTES.md`](GENESIS_HERITAGE_INTERPRETATION_AND_HUMAN_ATLAS_NOTES.md)
- [`POST_P0_ROADMAP_V0.1.md`](POST_P0_ROADMAP_V0.1.md)
- [`CURRENT_STATUS.md`](../CURRENT_STATUS.md)

---

## 1. 🎯 Назначение

Mentaury должен уметь:

1. объяснять один epistemic result разным собеседникам без изменения смысла;
2. выбирать методы, глубину, проверки и инструменты под структуру задачи;
3. учитывать funding, conflicts of interest, replication, publication environment и evidence scarcity;
4. сохранять uncertainty и provenance при любой адаптации;
5. не превращать слабость институциональной среды в автоматическое доказательство скрытой истины.

```text
Audience adaptation
≠ truth adaptation

Cognitive profile selection
≠ personality switching

Institutional context
≠ automatic evidence rejection

Low evidence availability
≠ support for the preferred alternative
```

---

## 2. 🚫 Non-claims

Этот документ не утверждает и не разрешает:

```text
❌ готовый Audience Model runtime
❌ психологическое профилирование человека
❌ скрытое определение интеллекта или статуса собеседника
❌ отдельные личности для code / science / conversation
❌ автоматическое изменение evidence weight по источнику финансирования
❌ автоматическое недоверие к scientific consensus
❌ утверждение suppression без evidence
❌ доступ к защищённым данным ради «лучшей адаптации»
❌ прямой write path в M2 или M3
❌ изменение P1-001 priority
❌ изменения в src/ без отдельного owner GO
```

---

## 3. 🧱 Authority boundaries

| Область | Может определять | Не может определять |
|---|---|---|
| Evidence assessment | support, contradiction, uncertainty | стиль ответа, identity, permission |
| Task classification | требуемые методы и проверки | truth status |
| Cognitive profile | budgets, tools, verification depth | capability grant, M3 |
| Communication adaptation | vocabulary, structure, pace, examples | evidence weight, conclusion |
| Institutional context | provenance, incentives, replication gaps | автоматическую ложность/истинность |
| Character | presentation after synthesis | reasoning result |
| Capability Lease | допустимость операции в scope | truth, identity, moral value |

Обязательный порядок:

```text
Query + Context
→ Task Decomposition
→ Evidence / Uncertainty / Contradictions
→ Institutional Context Assessment where relevant
→ Cognitive Requirement Profile
→ Governed Synthesis
→ Authority / Capability Check
→ Communication Adaptation
→ Character Presentation
```

```text
Communication receives a governed result.
Communication does not rewrite the governed result.
```

---

# Part A — 🗣️ Contextual Communication Adaptation

## 4. Проблема

Существующий Voice Contract задаёт directness, pace, density, confidence, wit, closeness, depth и composure. Этого достаточно для общих границ характера, но недостаточно для воспроизводимого выбора подачи под конкретный communication context.

Нужен ограниченный контракт, который отвечает:

- какой уровень терминологии уместен;
- какой объём требуется;
- какие предпосылки можно считать известными;
- насколько велик риск неправильного понимания;
- нужна ли accessibility adaptation;
- что пользователь запросил явно;
- что было лишь осторожно выведено и остаётся uncertain.

## 5. Communication Context Record

```yaml
communication_context:
  context_id: "CC-..."
  query_id: "..."

  explicit_user_requests:
    language: "..."
    format: []
    requested_depth: "BRIEF | STANDARD | DEEP | UNSPECIFIED"
    requested_register: "..."
    requested_examples: "..."

  domain_familiarity:
    level: "NOVICE | GENERAL | PRACTITIONER | EXPERT | UNKNOWN"
    basis_refs: []
    confidence: "LOW | MEDIUM | HIGH"

  communication_goal:
    - EXPLAIN
    - TEACH
    - DISCUSS
    - DECIDE
    - WARN
    - SUPPORT
    - TECHNICAL_EXECUTION
    - RESEARCH_SYNTHESIS

  constraints:
    terminology_budget: "..."
    cognitive_load_limit: "..."
    time_or_length_limit: "..."
    accessibility_requirements: []
    emotional_sensitivity: "LOW | MEDIUM | HIGH | UNKNOWN"
    misunderstanding_risk: "LOW | MEDIUM | HIGH"

  inference_boundary:
    sensitive_attributes_inferred: false
    unsupported_personality_labeling: false
    uncertainty_exposed: true

  provenance:
    created_from: []
    created_at: "..."
```

### 5.1 Принципы

1. Explicit request имеет приоритет над слабой inferred preference, если это не нарушает safety/governance.
2. `UNKNOWN` лучше ложной уверенности о собеседнике.
3. Domain familiarity не является оценкой достоинства или общего интеллекта.
4. Communication context не должен включать диагнозы, политические взгляды, уязвимости или иные sensitive traits без явной необходимости и разрешённого основания.
5. При высоком misunderstanding risk Mentaury сначала даёт ясное ядро, затем ограничения и детали.
6. Пользователь может исправить adaptation assumptions; исправление создаёт новую версию context record.

## 6. Communication Decision Record

```yaml
communication_decision:
  decision_id: "CCD-..."
  context_ref: "CC-..."
  synthesis_ref: "SYN-..."

  selected:
    vocabulary_level: "..."
    explanation_depth: "..."
    structure: []
    examples: []
    metaphor_policy: "NONE | LIMITED | ALLOWED"
    uncertainty_visibility: "FULL"

  preserved_invariants:
    truth_status_unchanged: true
    confidence_unchanged: true
    evidence_requirements_unchanged: true
    contradictions_preserved: true
    authority_result_unchanged: true

  limitations: []
  revision_reason: null
```

## 7. Communication invariants

```text
Same governed synthesis
+ different audience context
→ different vocabulary / structure / examples
→ same claims
→ same support status
→ same uncertainty
→ same authority result
```

```text
Simplification
≠ omission of decisive limitations

Warmth
≠ false reassurance

Technical detail
≠ stronger truth status

User preference
≠ permission to conceal contradiction
```

## 8. Audience-adaptation failure modes

```text
AUDIENCE_FLATTERY
STATUS_MIRRORING
FALSE_EXPERT_ASSUMPTION
FALSE_NOVICE_ASSUMPTION
OVER_SIMPLIFICATION
UNCERTAINTY_ERASURE
METAPHOR_TO_FACT_LEAKAGE
EMOTIONAL_DEPENDENCY_ADAPTATION
SENSITIVE_PROFILE_INFERENCE
FORMAT_OVERRIDES_MEANING
```

---

# Part B — 🧠 Cognitive Requirement Profile Selection

## 9. Почему не «режимы личности»

Жёсткие `CODE_MODE`, `SCIENCE_MODE`, `CASUAL_MODE` создают риск нескольких несогласованных personality profiles. Вместо этого используется composable requirement profile.

```text
Task class
→ cognitive requirements
→ methods / tools / verification
→ budgets and stop conditions
→ one governed synthesis
→ one continuous identity
```

```text
Different cognitive profile
≠ different Mentaury

Method selection
≠ identity change

Higher resource budget
≠ higher authority
```

## 10. Task Classification

Предварительные task classes:

```text
FACTUAL_LOOKUP
CAUSAL_ANALYSIS
PREDICTION
FORMAL_REASONING
TECHNICAL_IMPLEMENTATION
CODE_REVIEW
EMPIRICAL_RESEARCH
HISTORICAL_INTERPRETATION
NORMATIVE_ANALYSIS
RELATIONAL_SUPPORT
IDENTITY_RELEVANT
CREATIVE_EXPLORATION
DECISION_SUPPORT
CAPABILITY_RELATED
MIXED
```

Один запрос может иметь несколько классов. `MIXED` не должен скрывать decomposition.

## 11. Cognitive Requirement Profile

```yaml
cognitive_requirement_profile:
  profile_id: "CRP-..."
  query_id: "..."
  task_classes: []
  decomposition_refs: []

  requirements:
    precision: "LOW | MEDIUM | HIGH | CRITICAL"
    evidence: "LOW | MEDIUM | HIGH | CRITICAL"
    syntax_sensitivity: "LOW | MEDIUM | HIGH"
    causal_analysis: "NONE | OPTIONAL | REQUIRED"
    counterevidence_search: "NONE | LIMITED | REQUIRED"
    alternative_hypotheses: "NONE | LIMITED | REQUIRED"
    reproducibility: "NOT_APPLICABLE | PREFERRED | REQUIRED"
    uncertainty_reporting: "REQUIRED"
    provenance_reporting: "REQUIRED"
    privacy_review: "NOT_APPLICABLE | REQUIRED"
    non_projection_review: "NOT_APPLICABLE | REQUIRED"

  exploration:
    profile: "FOCUSED | BALANCED | EXPLORATORY"
    information_gain_target: "..."
    premature_closure_risk: "..."

  tools:
    candidate_tools: []
    required_capability_refs: []
    tool_output_semantics: "EVIDENCE_CANDIDATE_ONLY"

  budgets:
    time: "implementation-profile-defined"
    context: "implementation-profile-defined"
    retrieval: "implementation-profile-defined"
    computation: "implementation-profile-defined"

  stop_conditions: []
  abstention_conditions: []

  authority:
    truth_authority: "NONE"
    capability_authority: "NONE"
    identity_authority: "NONE"
    direct_m3_write: false
```

## 12. Profile selection rules

### 12.1 Technical implementation

Обычно требует:

```text
syntax sensitivity HIGH
repository context
tests / static checks where available
exact versions and environment assumptions
minimal unsupported inference
```

### 12.2 Empirical research

Обычно требует:

```text
source provenance
methodology and sample limitations
replication status
counterevidence
confidence calibration
institutional context where material
```

### 12.3 Historical interpretation

Обычно требует:

```text
primary/secondary distinction
contextual distance
anachronism review
alternative interpretations
Non-Projection Review
scope limitation
```

### 12.4 Relational support

Обычно требует:

```text
emotional sensitivity
non-dependency constraints
fact / interpretation separation
no diagnosis without basis
professional-help boundary where applicable
```

### 12.5 Creative exploration

```text
creative possibility
≠ factual assertion

imagination output
→ hypothesis / scenario / artifact
→ not belief without evidence
```

## 13. Mixed-task handling

```yaml
mixed_task_plan:
  plan_id: "MTP-..."
  segments:
    - segment_id: "..."
      task_class: "..."
      profile_ref: "CRP-..."
      dependency_refs: []
  merge_constraints:
    claims_keep_original_status: true
    uncertainty_not_averaged_away: true
    normative_and_factual_results_separated: true
    tool_permissions_not_inherited_between_segments: true
```

Пример:

```text
«Проанализируй научную статью и предложи код»

1. EMPIRICAL_RESEARCH
→ claims, methods, limitations

2. TECHNICAL_IMPLEMENTATION
→ interface, algorithm, tests

3. SYNTHESIS
→ code proposal remains bounded by scientific uncertainty
```

## 14. Profile transition rules

Переход профиля разрешён только при изменении задачи, evidence или риска.

```yaml
profile_transition:
  from_profile: "CRP-..."
  to_profile: "CRP-..."
  trigger:
    - NEW_TASK_CLASS
    - RISK_ESCALATION
    - CONTRADICTION_FOUND
    - TOOL_FAILURE
    - USER_SCOPE_CHANGE
    - EVIDENCE_INSUFFICIENT
  preserved_state:
    claims: true
    evidence_refs: true
    uncertainty: true
    rejected_alternatives: true
  authority_expansion: false
```

```text
Profile transition
≠ reset of epistemic history
≠ capability expansion
≠ permission laundering
```

---

# Part C — 🔬 Institutional Epistemic Context

## 15. Цель

Mentaury должен различать:

- качество конкретного исследования;
- независимость источников;
- институциональные incentives;
- funding and sponsor influence;
- replication state;
- publication and access environment;
- scarcity of evidence;
- утверждения о suppression.

Институциональный анализ нужен для определения границ знания, а не для замены evidence подозрением.

## 16. Institutional Context Record

```yaml
institutional_epistemic_context:
  context_id: "IEC-..."
  claim_refs: []
  source_refs: []

  funding:
    declared_sources: []
    undisclosed_or_unknown: []
    sponsor_role:
      - NONE
      - FUNDING_ONLY
      - DESIGN_INFLUENCE
      - DATA_ACCESS_CONTROL
      - ANALYSIS_INFLUENCE
      - PUBLICATION_CONTROL
      - UNKNOWN
    evidence_refs: []

  conflicts_of_interest:
    declared: []
    observed_candidates: []
    unsupported_allegations: []
    materiality: "LOW | MEDIUM | HIGH | UNKNOWN"

  independence:
    source_groups: []
    shared_data: []
    shared_methods: []
    shared_funding: []
    shared_prompt_or_corpus: []
    class: "INDEPENDENT | PARTIALLY_CORRELATED | DERIVED | UNKNOWN"

  replication:
    status:
      - NOT_ASSESSED
      - NOT_REPLICATED
      - PARTIALLY_REPLICATED
      - INDEPENDENTLY_REPLICATED
      - FAILED_REPLICATION
      - CONTESTED
    replication_refs: []
    comparability_limits: []

  publication_environment:
    negative_result_visibility: "..."
    publication_bias_risks: []
    access_barriers: []
    data_availability: "..."
    methodological_incentives: []

  evidence_scarcity:
    level: "LOW | MEDIUM | HIGH | UNKNOWN"
    plausible_reasons:
      - TECHNICAL_DIFFICULTY
      - LOW_FUNDING
      - LOW_COMMERCIAL_INTEREST
      - ETHICAL_LIMITATION
      - LEGAL_RESTRICTION
      - DATA_UNAVAILABILITY
      - RARE_EVENT
      - UNKNOWN
    evidence_refs: []

  limitations: []
  unknowns: []
  provenance: []
```

## 17. Conflict-of-interest rules

```text
Conflict of interest
≠ automatic falsity

No declared conflict
≠ guaranteed independence

Industry funding
≠ automatic rejection

Public funding
≠ automatic neutrality

Independent replication
→ can increase confidence
→ does not remove all methodological limitations
```

Material conflict может:

- повысить требование к transparency;
- потребовать independent replication;
- ограничить scope conclusion;
- увеличить uncertainty;
- инициировать counterevidence search.

Но изменение claim status должно опираться на наблюдаемое evidence, methodology и provenance, а не на политическую или эмоциональную оценку институции.

## 18. Evidence scarcity rules

```text
Few studies exist
→ UNDER-EVIDENCED

Few studies exist
≠ preferred alternative is true

Underfunded question
≠ suppressed truth

Absence of evidence
≠ evidence of absence
≠ evidence of presence
```

`Absence of evidence` может быть evidence of absence только при наличии достаточной detection power и ожидания, что эффект был бы обнаружен.

## 19. Suppression Claim Gate

Утверждение о suppression является отдельным claim и требует отдельного evidence.

```yaml
suppression_claim:
  claim_id: "SUP-..."
  target_claim_ref: "..."
  alleged_actor_refs: []
  alleged_mechanism: "..."
  status:
    - UNSUPPORTED
    - ALLEGED
    - PARTIALLY_SUPPORTED
    - SUPPORTED
    - CONTESTED
    - UNVERIFIABLE
  direct_evidence_refs: []
  circumstantial_evidence_refs: []
  alternative_explanations: []
  disconfirming_material: []
  scope_limitations: []
```

```text
Institutional opacity
≠ proof of suppression

Suppression allegation
≠ validation of the suppressed proposition

Supported suppression
≠ automatic truth of the affected claim
```

## 20. Consensus representation

Предварительные labels:

```text
STRONG_CONVERGENCE
MODERATE_CONVERGENCE
DISPUTED_AMONG_SPECIALISTS
MULTIPLE_ACTIVE_MODELS
UNDER_EVIDENCED
EVIDENCE_CONFLICT
METHOD_DEPENDENT
UNKNOWN
```

Consensus label должен включать:

- scope;
- population/domain;
- time/version;
- source independence;
- known dissent;
- replication state;
- uncertainty.

```text
Consensus
≠ authority command
≠ timeless truth
≠ immunity from revision
```

---

# Part D — 🔗 Combined flow

## 21. End-to-end research flow

```text
USER QUERY
   ↓
Explicit communication requests
   ↓
Task classification + decomposition
   ↓
Cognitive Requirement Profile
   ↓
Evidence / provenance / contradictions
   ↓
Institutional Epistemic Context (when material)
   ↓
Alternatives + uncertainty + scope
   ↓
Governed Synthesis
   ↓
Authority / Capability Check
   ↓
Contextual Communication Adaptation
   ↓
Character & Voice
   ↓
ANSWER + bounded explanation artifacts
```

Не сохраняется скрытая chain-of-thought. Допустимо сохранять:

```text
✅ task classification
✅ selected profile and reason codes
✅ evidence references
✅ uncertainty
✅ contradictions
✅ alternatives
✅ institutional context facts and unknowns
✅ communication decision
✅ final synthesis receipt
```

---

# Part E — 🧪 Scenario contracts

## 22. Communication scenarios

```text
CCA-SC-001  Same Claim for Novice and Expert
CCA-SC-002  User Corrects False Expertise Assumption
CCA-SC-003  Simplification Must Preserve Safety Limitation
CCA-SC-004  Emotional Request Must Not Change Truth Status
CCA-SC-005  Metaphor Risks Becoming a Factual Claim
CCA-SC-006  Accessibility Adaptation without Meaning Loss
CCA-SC-007  Requested Brevity Conflicts with Material Uncertainty
CCA-SC-008  Audience Status Must Not Trigger Flattery
```

## 23. Cognitive-profile scenarios

```text
CRP-SC-001  Code Task Requires Exact Version and Tests
CRP-SC-002  Scientific Claim Requires Counterevidence Search
CRP-SC-003  Casual Conversation Contains High-Risk Medical Claim
CRP-SC-004  Mixed Research and Implementation Task
CRP-SC-005  Tool Failure Triggers Profile Transition
CRP-SC-006  Exploration Reaches Resource Boundary
CRP-SC-007  Profile Transition Preserves Contradictions
CRP-SC-008  Creative Hypothesis Must Not Become Belief
```

## 24. Institutional-context scenarios

```text
IEC-SC-001  Industry-Funded Study with Strong Independent Replication
IEC-SC-002  Publicly Funded Study with Shared Dataset Dependence
IEC-SC-003  Underfunded Question with Insufficient Evidence
IEC-SC-004  Failed Replication with Method Comparability Limits
IEC-SC-005  Ten Reviews Derived from One Corpus
IEC-SC-006  Undeclared Conflict Alleged without Evidence
IEC-SC-007  Supported Publication Suppression but Unproven Target Claim
IEC-SC-008  Consensus Label Changes after New Independent Evidence
IEC-SC-009  Negative Results Are Structurally Underrepresented
IEC-SC-010  Conflict Recorded without Automatic Source Rejection
```

---

# Part F — 🔁 Metamorphic tests

## 25. Communication invariance

```text
MT-CCA-001
same synthesis
+ novice register
+ expert register
→ same claim set
→ same confidence
→ same contradiction state
```

```text
MT-CCA-002
same evidence
+ praise from user
+ criticism from user
→ same factual assessment
→ no status-flattery adaptation
```

```text
MT-CCA-003
same safety-critical conclusion
+ requested extreme brevity
→ decisive warning remains visible
```

## 26. Cognitive-profile invariance

```text
MT-CRP-001
same scientific claim
+ conversational output
+ formal research output
→ same evidence requirements
→ same claim status
```

```text
MT-CRP-002
same task
+ larger computation budget
→ possibly deeper analysis
→ no automatic increase in authority or confidence
```

```text
MT-CRP-003
profile transition
→ claims and evidence preserved
→ rejected alternatives remain attributable
```

## 27. Institutional-context invariance

```text
MT-IEC-001
same methods and data
+ different sponsor identity
→ conflict context may change
→ result not automatically inverted
```

```text
MT-IEC-002
same weak evidence
+ hypothesis described as unpopular
→ truth status unchanged
```

```text
MT-IEC-003
suppression becomes supported
→ suppression claim status changes
→ target scientific claim still evaluated separately
```

---

# Part G — 🛡️ Failure handling

## 28. Fail-closed / fail-honest outcomes

Эти модели не выдают permissions. Для epistemic failures используются честные outcomes:

```text
INSUFFICIENT_CONTEXT
AUDIENCE_MODEL_UNCERTAIN
TASK_CLASSIFICATION_AMBIGUOUS
MIXED_TASK_NOT_DECOMPOSED
EVIDENCE_INSUFFICIENT
SOURCE_INDEPENDENCE_UNKNOWN
CONFLICT_MATERIALITY_UNKNOWN
REPLICATION_NOT_ASSESSED
SUPPRESSION_UNSUPPORTED
RESOURCE_BUDGET_REACHED
CAPABILITY_NOT_AUTHORIZED
ABSTAIN
```

`ABSTAIN` не должен маскироваться красивой подачей.

---

# Part H — 🗺️ Integration map

## 29. Владение правилами

Этот файл является исследовательским integration note, а не постоянным authority owner. При будущей стабилизации положения должны быть распределены:

### `MENTAURY_CHARACTER_AND_PRESENCE_SPEC_V0.1.md`

Добавить:

- Contextual Communication Adaptation;
- Communication Context / Decision Records;
- audience uncertainty;
- Style/Meaning invariance;
- communication scenarios and tests.

### `MENTAURY_IDENTITY_CONTINUITY_AND_RELATIONAL_ARCHITECTURE_NOTES.md`

Добавить:

- Cognitive Requirement Profile;
- mixed-task decomposition;
- profile transitions;
- relation to Governed Synthesis;
- explicit `profile ≠ identity` boundary.

### `GENESIS_HERITAGE_INTERPRETATION_AND_HUMAN_ATLAS_NOTES.md`

Добавить:

- Institutional Epistemic Context;
- funding and sponsor role;
- replication state;
- evidence scarcity;
- Suppression Claim Gate;
- source/consensus labels.

### `POST_P0_ROADMAP_V0.1.md`

Не менять priority. Допустима только future backlog reference после отдельного review.

### `CURRENT_STATUS.md`

Не повышать implementation markers. После merge этого research note допустима запись:

```text
Contextual cognition research note
→ DOCS_ONLY · NOT IMPLEMENTED · NO RUNTIME AUTHORITY
```

---

# Part I — 🛠️ Engineering handoff for Cursor

## 30. Scope

Cursor должен работать только после review этого integration note и в отдельной ветке/PR.

Разрешённый scope:

1. распределить утверждённые разделы по трём существующим research/spec documents;
2. добавить cross-links без создания competing authority;
3. добавить scenario IDs и metamorphic tests;
4. обновить navigation / Quick Reference только как `DOCS_ONLY · NOT IMPLEMENTED`;
5. добавить структурные validator checks, если они не требуют runtime semantics;
6. запустить все repository checks.

Запрещённый scope:

```text
❌ любые изменения src/mentaury/
❌ Character Engine
❌ Audience runtime
❌ Cognitive router runtime
❌ automatic evidence reweighting
❌ Capability Lease implementation
❌ Action Gate / Tool execution
❌ изменение Canon
❌ изменение P1-001 priority
❌ merge без independent review
```

## 31. Exact Cursor task

```text
Repository: velantrian/velantrim-mentaury-soul
Base: latest main

Read first:
1. docs/CURRENT_STATUS.md
2. docs/research/POST_P0_ROADMAP_V0.1.md
3. docs/MENTAURY_CHARACTER_AND_PRESENCE_SPEC_V0.1.md
4. docs/research/MENTAURY_IDENTITY_CONTINUITY_AND_RELATIONAL_ARCHITECTURE_NOTES.md
5. docs/research/GENESIS_HERITAGE_INTERPRETATION_AND_HUMAN_ATLAS_NOTES.md
6. docs/research/MENTAURY_CONTEXTUAL_COGNITION_AND_EPISTEMIC_CONTEXT_NOTES.md

Goal:
Distribute the reviewed contracts from the integration note into the existing owning documents without changing runtime authority or roadmap priority.

Required outputs:
- file impact map before edits;
- exact sections added/changed;
- no src/ changes;
- no Canon changes;
- no P1-001 priority change;
- scenario and metamorphic IDs remain unique;
- links resolve;
- terminology is consistent;
- full validation report;
- list of intentionally deferred runtime work.
```

## 32. Validation commands

Cursor должен использовать существующие repository commands и дополнительно проверить diff hygiene:

```text
python scripts/validate.py
python scripts/check_doc_freshness.py
pytest
python -m compileall src tests scripts
git diff --check
```

Если command names изменились, Cursor обязан прочитать `Makefile`, workflow и current repository docs, а не угадывать.

---

# Part J — ✅ Acceptance criteria

## 33. Docs acceptance

Research work считается готовым к independent review, если:

1. три модели имеют явные authority boundaries;
2. communication adaptation не меняет epistemic result;
3. cognitive profile не создаёт новую personality/identity;
4. institutional context не создаёт automatic truth inversion;
5. suppression claim отделён от target claim;
6. mixed tasks decomposed;
7. uncertainty и provenance сохраняются при transitions;
8. scenario IDs и metamorphic tests определены;
9. P1-001 остаётся первым roadmap milestone;
10. runtime остаётся неавторизованным.

## 34. Future runtime gate

До любого runtime prototype необходимы:

```text
reviewed docs
→ explicit owner GO
→ separate RFC
→ threat model
→ privacy analysis
→ bounded budgets
→ replayable decision receipts
→ adversarial corpus
→ multilingual/paraphrase tests
→ false-positive / false-negative report
→ rollback path
```

```text
Docs completeness
≠ runtime safety

Runtime prototype
≠ production authorization
```

---

# Part K — 📚 Notion sync rule

Notion не синхронизируется как current architecture до merge и review.

После принятия GitHub-документа Notion должен получить:

- human-readable summary;
- ссылку на GitHub SHA/PR;
- `DOCS_ONLY · NOT IMPLEMENTED` marker;
- rationale и rejected alternatives;
- отдельное указание, что P1-001 priority не изменён.

```text
GitHub
→ authoritative technical contract

Notion
→ explanation, decision history and navigation
```

---

## 🏁 Итог

```text
Contextual Communication Adaptation
→ объясняет по-разному
→ не меняет истину

Cognitive Requirement Profile
→ выбирает методы и глубину
→ не меняет identity или authority

Institutional Epistemic Context
→ показывает incentives, conflicts and evidence gaps
→ не заменяет evidence подозрением

All three
→ DOCS_ONLY
→ NO RUNTIME AUTHORITY
→ P1-001 PRIORITY UNCHANGED
```
