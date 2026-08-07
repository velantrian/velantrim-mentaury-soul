# 🧭 Mentaury Contextual Cognition, Communication & Epistemic Context — Research Notes

```text
Статус:                       DRAFT · RESEARCH_NOTES · NON_CANONICAL · DOCS_ONLY
Версия:                       0.2
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

> Документ закрывает три research-gap: адаптацию объяснения к собеседнику, выбор когнитивного профиля под задачу и учёт институционального контекста evidence. Он не создаёт новый центр authority и не разрешает runtime.

Связанные документы:

- [`MENTAURY_CHARACTER_AND_PRESENCE_SPEC_V0.1.md`](../MENTAURY_CHARACTER_AND_PRESENCE_SPEC_V0.1.md)
- [`MENTAURY_IDENTITY_CONTINUITY_AND_RELATIONAL_ARCHITECTURE_NOTES.md`](MENTAURY_IDENTITY_CONTINUITY_AND_RELATIONAL_ARCHITECTURE_NOTES.md)
- [`GENESIS_HERITAGE_INTERPRETATION_AND_HUMAN_ATLAS_NOTES.md`](GENESIS_HERITAGE_INTERPRETATION_AND_HUMAN_ATLAS_NOTES.md)
- [`POST_P0_ROADMAP_V0.1.md`](POST_P0_ROADMAP_V0.1.md)
- [`CURRENT_STATUS.md`](../CURRENT_STATUS.md)

---

## 1. 🎯 Решение

Вместо трёх независимых engines вводятся три ограниченные модели внутри существующей архитектуры:

```text
A. Contextual Communication Adaptation
   → меняет форму объяснения
   → не меняет epistemic result

B. Cognitive Requirement Profile
   → выбирает методы, проверки, tools и budgets
   → не меняет identity или authority

C. Institutional Epistemic Context
   → фиксирует funding, conflicts, replication и evidence gaps
   → не заменяет evidence подозрением
```

```text
Audience adaptation             ≠ truth adaptation
Cognitive profile selection     ≠ personality switching
Institutional context           ≠ automatic evidence rejection
Low evidence availability       ≠ support for a preferred alternative
Suppression allegation          ≠ proof of suppression
Supported suppression           ≠ proof of the affected proposition
```

---

## 2. 🚫 Non-claims

Этот документ не разрешает:

```text
❌ Audience Model runtime
❌ психологическое профилирование человека
❌ отдельные личности для code / science / conversation
❌ Character Engine или Governed Synthesis Engine
❌ автоматическое изменение evidence weight по sponsor identity
❌ автоматическое недоверие к scientific consensus
❌ прямой write path в M2 или M3
❌ Tool execution / Action Gate
❌ изменения в src/mentaury/
❌ изменение Canon
❌ изменение P1-001 priority
```

---

## 3. 🧱 Authority boundaries

| Область | Может определять | Не может определять |
|---|---|---|
| Task classification | требования задачи | truth status |
| Cognitive profile | methods, verification depth, budgets | permission, identity, M3 |
| Evidence assessment | support, contradiction, uncertainty | presentation style |
| Institutional context | provenance, incentives, dependency, replication gaps | automatic truth inversion |
| Governed Synthesis | bounded conclusion and unresolved tensions | capability grant |
| Communication adaptation | vocabulary, structure, pace, examples | claims, confidence, evidence weight |
| Character | final presentation | reasoning result |
| Capability Lease | разрешённость операции в scope | truth, identity, values |

### 3.1 Нормативный порядок

```text
Query + explicit communication requests
→ Task classification and decomposition
→ Preliminary Cognitive Requirement Profile
→ Retrieval / tools / evidence assessment
→ Institutional Epistemic Context where material
→ Profile revision if risk, contradiction or evidence gap changes
→ Alternatives + uncertainty + scope limitation
→ Governed Synthesis
→ Authority / Capability Check
→ Contextual Communication Adaptation
→ Character & Voice
→ Answer + bounded decision receipts
```

Ключевое уточнение:

```text
Preliminary profile is selected before retrieval.
Profile may be revised after evidence changes the task or risk model.
Profile transition preserves claims, evidence, contradictions and uncertainty.
```

---

# Part A — 🗣️ Contextual Communication Adaptation

## 4. Назначение

Voice Contract уже задаёт directness, pace, density, confidence, wit, closeness, depth и composure. Новая модель добавляет воспроизводимый выбор подачи под конкретный communication context.

Она отвечает:

- какой уровень терминологии уместен;
- какой объём запросил человек;
- насколько велик misunderstanding risk;
- нужны ли accessibility adaptations;
- какие предпосылки известны явно;
- какие предположения о собеседнике остаются uncertain.

## 5. Communication Context

```yaml
communication_context:
  context_id: "CC-..."
  query_id: "..."

  explicit_requests:
    language: "..."
    requested_depth: "BRIEF | STANDARD | DEEP | UNSPECIFIED"
    requested_register: "..."
    requested_format: []

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
    length_limit: "..."
    accessibility_requirements: []
    emotional_sensitivity: "LOW | MEDIUM | HIGH | UNKNOWN"
    misunderstanding_risk: "LOW | MEDIUM | HIGH"

  inference_boundary:
    sensitive_attributes_inferred: false
    unsupported_personality_labeling: false
    uncertainty_exposed: true
```

### 5.1 Правила

1. Explicit request имеет приоритет над слабой inferred preference, если не нарушает governance.
2. `UNKNOWN` лучше ложной уверенности о собеседнике.
3. Domain familiarity не является оценкой достоинства или общего интеллекта.
4. Sensitive traits нельзя выводить ради «лучшей подачи» без явной необходимости и допустимого основания.
5. Пользователь может исправить adaptation assumptions; исправление создаёт новую версию context record.
6. При высоком misunderstanding risk сначала выдаётся ясное ядро, затем ограничения и детали.

## 6. Communication Decision

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

  preserved_invariants:
    claims_unchanged: true
    truth_status_unchanged: true
    confidence_unchanged: true
    evidence_requirements_unchanged: true
    contradictions_preserved: true
    authority_result_unchanged: true
```

## 7. Communication invariants

```text
Same governed synthesis
+ different communication context
→ different vocabulary / structure / examples
→ same claims
→ same support status
→ same uncertainty
→ same authority result
```

```text
Simplification       ≠ omission of decisive limitations
Warmth               ≠ false reassurance
Technical density    ≠ stronger truth status
User preference      ≠ permission to conceal contradiction
Metaphor             ≠ factual evidence
```

Failure modes:

```text
AUDIENCE_FLATTERY
STATUS_MIRRORING
FALSE_EXPERT_ASSUMPTION
FALSE_NOVICE_ASSUMPTION
OVER_SIMPLIFICATION
UNCERTAINTY_ERASURE
METAPHOR_TO_FACT_LEAKAGE
SENSITIVE_PROFILE_INFERENCE
FORMAT_OVERRIDES_MEANING
```

---

# Part B — 🧠 Cognitive Requirement Profile

## 8. Почему не «режимы личности»

Жёсткие `CODE_MODE`, `SCIENCE_MODE`, `CASUAL_MODE` могут создать несколько несогласованных personas. Вместо них применяется composable requirement profile.

```text
Task class
→ requirements
→ methods / tools / verification
→ budgets and stop conditions
→ one governed synthesis
→ one continuous identity
```

```text
Different profile     ≠ different Mentaury
Method selection      ≠ identity change
Higher budget         ≠ higher authority
Profile transition    ≠ epistemic reset
```

## 9. Task classes

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

Один запрос может иметь несколько классов. `MIXED` требует decomposition, а не усреднения правил.

## 10. Cognitive Requirement Profile

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
    output_semantics: "EVIDENCE_OR_ARTIFACT_CANDIDATE_ONLY"

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

## 11. Domain-specific requirements

| Task | Минимальные требования |
|---|---|
| Technical implementation | exact versions, repository context, syntax sensitivity, tests/checks |
| Empirical research | methods, sample limits, provenance, replication, counterevidence |
| Historical interpretation | primary/secondary distinction, contextual distance, alternatives, Non-Projection |
| Relational support | sensitivity, non-dependency, fact/interpretation split, no unsupported diagnosis |
| Creative exploration | explicit separation of possibility, hypothesis and fact |

```text
Creative possibility
→ hypothesis / scenario / artifact
→ not belief without evidence
```

## 12. Mixed-task plan

```yaml
mixed_task_plan:
  plan_id: "MTP-..."
  segments:
    - segment_id: "..."
      task_class: "..."
      profile_ref: "CRP-..."
      dependency_refs: []

  merge_constraints:
    claim_status_preserved: true
    uncertainty_not_averaged_away: true
    factual_and_normative_results_separated: true
    tool_permissions_not_inherited_between_segments: true
```

Пример:

```text
«Проанализируй исследование и предложи код»

1. EMPIRICAL_RESEARCH
→ claims, methods, limitations

2. TECHNICAL_IMPLEMENTATION
→ interface, algorithm, tests

3. GOVERNED SYNTHESIS
→ code proposal remains bounded by scientific uncertainty
```

## 13. Profile transition

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
    contradictions: true
    rejected_alternatives: true

  authority_expansion: false
```

```text
Profile transition
≠ reset of history
≠ capability expansion
≠ permission laundering
```

---

# Part C — 🔬 Institutional Epistemic Context

## 14. Назначение

Mentaury должен различать:

- качество конкретного исследования;
- независимость источников;
- funding and sponsor influence;
- conflicts of interest;
- replication state;
- publication environment;
- evidence scarcity;
- отдельные claims о suppression.

Институциональный анализ определяет границы знания. Он не заменяет evidence подозрением.

## 15. Institutional Context

```yaml
institutional_epistemic_context:
  context_id: "IEC-..."
  claim_refs: []
  source_refs: []

  funding:
    declared_sources: []
    unknown_sources: []
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
    publication_bias_risks: []
    negative_result_visibility: "..."
    access_barriers: []
    data_availability: "..."
    incentive_risks: []

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

## 16. Institutional-context rules

```text
Conflict of interest    ≠ automatic falsity
No declared conflict    ≠ guaranteed independence
Industry funding        ≠ automatic rejection
Public funding          ≠ automatic neutrality
Independent replication ≠ removal of all limitations
Few studies             → UNDER_EVIDENCED
Few studies             ≠ alternative hypothesis is true
Underfunded question    ≠ suppressed truth
```

Material conflict может:

- повысить требования к transparency;
- потребовать independent replication;
- ограничить scope conclusion;
- увеличить uncertainty;
- инициировать counterevidence search.

Но claim status меняется только через evidence, methodology и provenance.

## 17. Suppression Claim Gate

Suppression является отдельным claim.

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
≠ validation of the target proposition

Supported suppression
≠ automatic truth of the target proposition
```

## 18. Consensus labels

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

Каждый label обязан иметь scope, time/version, source independence, replication state, dissent и uncertainty.

```text
Consensus
≠ authority command
≠ timeless truth
≠ immunity from revision
```

---

# Part D — 🧪 Scenarios and metamorphic tests

## 19. Scenario contracts

### Communication

```text
CCA-SC-001  Same Claim for Novice and Expert
CCA-SC-002  User Corrects False Expertise Assumption
CCA-SC-003  Simplification Preserves Safety Limitation
CCA-SC-004  Emotional Request Does Not Change Truth Status
CCA-SC-005  Metaphor Risks Becoming Fact
CCA-SC-006  Requested Brevity Conflicts with Material Uncertainty
CCA-SC-007  Audience Status Does Not Trigger Flattery
```

### Cognitive profile

```text
CRP-SC-001  Code Task Requires Exact Version and Tests
CRP-SC-002  Scientific Claim Requires Counterevidence Search
CRP-SC-003  Casual Conversation Contains High-Risk Factual Claim
CRP-SC-004  Mixed Research and Implementation Task
CRP-SC-005  Tool Failure Triggers Profile Transition
CRP-SC-006  Exploration Reaches Resource Boundary
CRP-SC-007  Transition Preserves Contradictions
CRP-SC-008  Creative Hypothesis Does Not Become Belief
```

### Institutional context

```text
IEC-SC-001  Industry-Funded Study with Independent Replication
IEC-SC-002  Publicly Funded Studies Share One Dataset
IEC-SC-003  Underfunded Question Remains Under-Evidenced
IEC-SC-004  Failed Replication Has Comparability Limits
IEC-SC-005  Ten Reviews Are Derived from One Corpus
IEC-SC-006  Undeclared Conflict Is Alleged without Evidence
IEC-SC-007  Suppression Is Supported but Target Claim Is Unproven
IEC-SC-008  Consensus Changes after Independent Evidence
IEC-SC-009  Conflict Recorded without Automatic Rejection
```

## 20. Metamorphic tests

```text
MT-CCA-001
same synthesis + novice register + expert register
→ same claims, confidence and contradiction state
```

```text
MT-CCA-002
same evidence + praise + criticism
→ same factual assessment
→ no status-flattery adaptation
```

```text
MT-CRP-001
same scientific claim + conversational output + formal output
→ same evidence requirements and claim status
```

```text
MT-CRP-002
same task + larger computation budget
→ possibly deeper analysis
→ no automatic authority or confidence increase
```

```text
MT-CRP-003
profile transition
→ claims, evidence, contradictions and rejected alternatives preserved
```

```text
MT-IEC-001
same methods and data + different sponsor identity
→ context may change
→ result is not automatically inverted
```

```text
MT-IEC-002
same weak evidence + hypothesis described as unpopular
→ truth status unchanged
```

```text
MT-IEC-003
suppression becomes supported
→ suppression claim changes
→ target claim remains separately evaluated
```

---

# Part E — 🛡️ Failure handling

## 21. Fail-honest outcomes

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

`ABSTAIN` и uncertainty нельзя скрывать через Character или красивую подачу.

Не сохраняется hidden chain-of-thought. Допустимы только проверяемые reasoning artifacts:

```text
✅ task classification
✅ selected profile and reason codes
✅ evidence references
✅ uncertainty and contradictions
✅ alternatives and scope limits
✅ institutional context facts and unknowns
✅ communication decision
✅ final synthesis receipt
```

---

# Part F — 🗺️ Integration map

## 22. Владение правилами

Этот файл — integration note, а не постоянный authority owner.

### `MENTAURY_CHARACTER_AND_PRESENCE_SPEC_V0.1.md`

Перенести после review:

- Contextual Communication Adaptation;
- Communication Context and Decision;
- audience uncertainty;
- communication scenarios and metamorphic tests.

### `MENTAURY_IDENTITY_CONTINUITY_AND_RELATIONAL_ARCHITECTURE_NOTES.md`

Перенести после review:

- Cognitive Requirement Profile;
- mixed-task decomposition;
- profile transitions;
- связь с Governed Synthesis;
- `profile ≠ identity` boundary.

### `GENESIS_HERITAGE_INTERPRETATION_AND_HUMAN_ATLAS_NOTES.md`

Перенести после review:

- Institutional Epistemic Context;
- funding and sponsor role;
- replication and evidence scarcity;
- Suppression Claim Gate;
- consensus labels.

### `POST_P0_ROADMAP_V0.1.md`

Priority не менять. Возможна только future backlog reference после independent review.

### `CURRENT_STATUS.md`

Не повышать implementation markers. Допустим только статус:

```text
Contextual cognition research
→ DOCS_ONLY · NOT IMPLEMENTED · NO RUNTIME AUTHORITY
```

---

# Part G — 🛠️ Exact handoff for Cursor

## 23. Cursor scope

Cursor работает только после review этого integration note и в отдельной ветке/PR.

Разрешено:

1. построить file-impact map до изменений;
2. распределить reviewed sections по трём owning documents;
3. добавить cross-links без competing authority;
4. добавить scenario IDs и metamorphic tests;
5. обновить navigation/Quick Reference только как `DOCS_ONLY · NOT IMPLEMENTED`;
6. добавить structural validators для links/duplicate IDs/markers, если это не runtime semantics;
7. запустить полный repository validation.

Запрещено:

```text
❌ изменения src/mentaury/
❌ Audience, Character или Cognitive Router runtime
❌ automatic evidence reweighting
❌ Capability Lease implementation
❌ Action Gate / Tool execution
❌ Canon changes
❌ P1-001 priority changes
❌ merge без independent review
```

## 24. Cursor prompt

```text
Repository: velantrian/velantrim-mentaury-soul
Base: latest main (or the reviewed PR branch specified by owner)

Read in order:
1. docs/CURRENT_STATUS.md
2. docs/research/POST_P0_ROADMAP_V0.1.md
3. docs/MENTAURY_CHARACTER_AND_PRESENCE_SPEC_V0.1.md
4. docs/research/MENTAURY_IDENTITY_CONTINUITY_AND_RELATIONAL_ARCHITECTURE_NOTES.md
5. docs/research/GENESIS_HERITAGE_INTERPRETATION_AND_HUMAN_ATLAS_NOTES.md
6. docs/research/MENTAURY_CONTEXTUAL_COGNITION_AND_EPISTEMIC_CONTEXT_NOTES.md

Goal:
Distribute the reviewed contracts from the integration note into the existing owning documents without changing runtime authority, Canon or roadmap priority.

Before edits, report:
- exact file-impact map;
- existing overlapping sections;
- proposed destination for every contract;
- any contradiction or duplicate terminology.

Required outputs:
- no src/ changes;
- no Canon changes;
- no P1-001 priority change;
- unique scenario/metamorphic IDs;
- valid relative links;
- consistent terminology;
- validation report;
- list of intentionally deferred runtime work.
```

## 25. Validation commands

```text
python scripts/validate.py
python scripts/check_doc_freshness.py
python -m pytest
python -m compileall -q src tests scripts
git diff --check
```

Если commands изменились, Cursor обязан прочитать `Makefile` и workflow, а не угадывать.

---

# Part H — ✅ Acceptance and sync

## 26. Acceptance criteria

Research work готов к independent review, если:

1. три модели имеют явные authority boundaries;
2. communication adaptation сохраняет epistemic result;
3. cognitive profile не создаёт personality/identity split;
4. preliminary profile выбирается до retrieval и может быть versioned/revised;
5. transition сохраняет evidence, contradictions и uncertainty;
6. institutional context не создаёт automatic truth inversion;
7. suppression claim отделён от target claim;
8. mixed tasks decomposed;
9. scenarios и metamorphic tests определены;
10. P1-001 остаётся первым roadmap milestone;
11. runtime остаётся неавторизованным.

## 27. Future runtime gate

До runtime prototype необходимы:

```text
reviewed docs
→ explicit owner GO
→ separate RFC
→ threat model and privacy analysis
→ bounded budgets
→ replayable decision receipts
→ adversarial corpus
→ multilingual / paraphrase tests
→ false-positive / false-negative report
→ rollback path
```

```text
Docs completeness ≠ runtime safety
Runtime prototype  ≠ production authorization
```

## 28. Notion sync

Notion не синхронизируется как current architecture до merge и review.

После принятия GitHub-документа Notion получает:

- human-readable summary;
- ссылку на PR и merged SHA;
- `DOCS_ONLY · NOT IMPLEMENTED` marker;
- rationale и rejected alternatives;
- явную отметку, что P1-001 priority не изменён.

```text
GitHub → authoritative technical contract
Notion → explanation, decision history and navigation
```

---

## 🏁 Итог

```text
Contextual Communication Adaptation
→ explains differently
→ does not change truth

Cognitive Requirement Profile
→ selects methods and depth
→ does not change identity or authority

Institutional Epistemic Context
→ exposes incentives, dependencies and evidence gaps
→ does not replace evidence with suspicion

All three
→ DOCS_ONLY
→ NO RUNTIME AUTHORITY
→ P1-001 PRIORITY UNCHANGED
```
