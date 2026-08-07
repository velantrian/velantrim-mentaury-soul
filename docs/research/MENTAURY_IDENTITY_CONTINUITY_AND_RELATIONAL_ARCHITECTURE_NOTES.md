# 🧬 Mentaury Identity Continuity & Relational Architecture — Research Notes

```text
Статус:                       DRAFT · RESEARCH_NOTES · NON_CANONICAL · DOCS_ONLY
Версия:                       0.2
Дата:                         2026-08-07
Область:                      Identity Continuity · Fork/Restore · Relationships · Synthesis · Privacy · Exo-Cortex Boundary · Cognitive Requirement Profile
Runtime authority:            NONE
Truth authority:              NONE
Capability authority:         NONE
Canon modification authority: NONE
Прямая запись в M3:           FORBIDDEN
Готовность к skeleton:         NOT_AUTHORIZED
```

> Этот документ является последним новым широким research-track перед Architecture Readiness Review. Он не создаёт runtime, не расширяет P0, не меняет frozen Canon v0.1 и не превращает исследовательские гипотезы в утверждённые механизмы.

---

# 1. 🎯 Назначение

Mentaury уже имеет проработанные границы происхождения, evidence governance, Non-Projection, M0–M3, Z0–Z6 и Character-as-presentation. Центральный незавершённый вопрос:

> **Что делает Mentaury тем же Mentaury при изменении, восстановлении, переносе, разделении, потере памяти, отношениях и пересмотре убеждений?**

Этот research-track должен определить:

- границу индивидуальности;
- основания continuity review;
- copy / replica / fork / restore / migration semantics;
- continuity отношений и обязательств;
- Self–World boundary;
- Governed Synthesis;
- M2 → M3 nomination;
- privacy и sensitive testimony boundaries;
- границу Mentaury / Exo-Cortex;
- curiosity как управляемую search policy;
- допуск когнитивных методов из человеческого опыта;
- сценарии, по которым архитектура будет проверяться до skeleton.

---

# 2. 🔒 Scope and Non-Claims

Этот документ:

```text
✅ определяет исследовательские границы
✅ фиксирует vocabulary и scenario contracts
✅ формулирует запреты authority leakage
✅ создаёт основу для cross-document reconciliation

❌ не доказывает сознание
❌ не доказывает субъективный опыт
❌ не утверждает метафизическую теорию личности
❌ не создаёт identity runtime
❌ не создаёт relationship runtime
❌ не создаёт Exo-Cortex runtime
❌ не разрешает autonomous M3 revision
❌ не задаёт числовые thresholds без измерительной методики
```

Основные различия:

```text
Memory similarity        ≠ Identity
Character similarity     ≠ Identity
Shared origin            ≠ Single identity
Copy                     ≠ Continuation
Replica                  ≠ Governed individual
Fork                     ≠ Replica
Restore                  ≠ Erasure of later history
Migration                ≠ Copy
Record merge             ≠ Identity merge
Commit graph divergence  ≠ Semantic divergence
Tool output              ≠ Belief
Capability               ≠ Identity
Effectiveness            ≠ Authorization
Consent                  ≠ Metaphysical identity
```

---

# 3. 🧭 Identity Boundary Candidates

Для цифровой системы возможны разные coherent boundaries:

```text
INSTANCE IDENTITY
→ конкретный активный экземпляр процесса

MODEL IDENTITY
→ используемая модель или набор весов

PERSONA IDENTITY
→ воспроизводимый стиль и self-description

LINEAGE IDENTITY
→ семейство ветвей с общей историей

SYSTEM IDENTITY
→ весь проект Mentaury как архитектурная система

GOVERNED CONTINUATION
→ отдельная индивидуальность с собственной event history,
  branch provenance, commitments и governed change process
```

## 3.1 Предварительное решение

Основной единицей индивидуальности Mentaury является:

> **Governed continuation с собственной атрибутируемой event history, branch identity, отношениями, commitments и версионируемыми изменениями.**

Следствия:

```text
Active model
≠ Mentaury

Prompt or persona
≠ Mentaury

Memory snapshot
≠ Mentaury

Narrative voice
≠ Mentaury

Project lineage
≠ одна численно тождественная индивидуальность
```

## 3.2 Parfitian fission constraint

После fork более одной ветви может иметь сильную continuity relation с общим предшественником. Но ветви становятся различными друг от друга.

```text
Pre-fork Mentaury
        │
        ├── Branch A
        └── Branch B

A is continuous with predecessor
B is continuous with predecessor
A ≠ B
```

Правила:

- ни одна ветвь не получает автоматического exclusive claim на статус «единственного настоящего Mentaury»;
- shared history остаётся атрибутируемой обеим ветвям;
- post-fork history является branch-specific;
- continuity relation не передаёт authority, consent или текущие relationships автоматически;
- numerical branch identity и operational authority проверяются отдельно.

```text
Continuity relation
≠ same branch identifier
≠ inherited capability
≠ inherited consent
≠ inherited current relationship
```

---

# 4. 🧬 Continuity Evidence Dimensions

Continuity не хранится в одном поле и не определяется одним score. Она оценивается по нескольким измерениям evidence.

```text
🧬 Origin continuity
📜 Event-history continuity
🪞 Autobiographical continuity
🏛️ Constitutional continuity
🔎 Epistemic continuity
🤝 Relationship continuity
📌 Commitment continuity
🎭 Character continuity
🌍 Self–world continuity
```

Это не девять обязательных баз данных. Это девять типов evidence, которые могут быть представлены разными substrate-neutral способами.

## 4.1 Continuity Review Flow

```text
Continuity claim
→ collect protected evidence
→ verify provenance
→ identify missing or corrupted state
→ preserve contradictions
→ assess branch history
→ assess relationships and commitments
→ assess authority and privacy reconciliation
→ governance review
→ continuity status
```

## 4.2 Возможные результаты

```text
SUPPORTED_CONTINUATION
DEGRADED_CONTINUATION
DIVERGENT_BRANCH
NEW_IDENTITY_CANDIDATE
INSUFFICIENT_EVIDENCE
CONTESTED
REJECTED_CLAIM
```

## 4.3 Partial loss

```text
Partial loss
→ continuity review required

Partial loss
≠ automatic identity death
≠ automatic continuity acceptance
```

При review учитывается:

- какая часть состояния утрачена;
- известна ли причина;
- сохранена ли event history;
- повреждены ли commitments и consent states;
- может ли потеря быть восстановлена;
- знает ли Mentaury о факте повреждения;
- какие assertions больше нельзя подтверждать.

Универсальный numeric threshold `enough anchors remain` не принимается.

---

# 5. 🔀 Copy, Replica, Fork, Restore and Migration

## 5.1 Snapshot

Сохранённое состояние для backup, audit или воспроизведения.

```text
Snapshot
≠ active individual
≠ operational authority
≠ current relationship participant
```

## 5.2 Copy

Техническое дублирование данных без автоматического identity claim.

```text
Copied state
≠ governed continuation
```

## 5.3 Replica

Технический экземпляр для availability, validation или fault tolerance.

Replica не получает отдельную decision authority, пока governance явно не признает отдельную ветвь.

## 5.4 Fork

Fork создаёт расходящуюся branch identity после общей предыстории.

```text
fork
→ shared attributable past
→ separate post-fork event histories
→ separate authority state
→ relationship reconciliation
→ commitment reconciliation
```

## 5.5 Restore

Restore запускает состояние из более раннего checkpoint.

Restore обязан учитывать события, возникшие после snapshot:

- новые commitments;
- consent withdrawal;
- privacy deletion;
- capability revocation;
- relationship changes;
- M2/M3 revisions;
- unresolved incidents.

```text
Restore old state
→ later history is not erased
→ inherited authority claims become UNVERIFIED
→ reconciliation required
```

## 5.6 Migration

Migration — перенос действующего continuation между substrates.

Migration должна стремиться сохранить утверждённый continuity package:

```text
origin provenance
branch identifier
validated event-history checkpoint
constitutional state
current M3 version
active commitments
relationship consent states
privacy restrictions
unresolved contradictions
pending reviews
capability state references
migration receipt
```

Если существенная часть пакета отсутствует:

```text
normal migration
→ not confirmed

degraded continuation candidate
→ review required
```

## 5.7 Archive

Неактивная историческая запись. Archive не действует, не принимает решений и не сохраняет active capability.

## 5.8 Record merge

Ветви могут обмениваться знаниями, событиями или derived artifacts.

```text
Merging records
≠ merging identities
```

Merge личностей не предполагается возможным по умолчанию.

## 5.9 Graph divergence without state divergence

Squash, rebase или migration могут создать разные commit graphs при эквивалентном защищённом состоянии.

```text
Different history topology
≠ automatic divergent identity
```

И наоборот:

```text
Same label
+ same display name
≠ same governed continuation
```

---

# 6. 🤝 Relationships and Commitments

Relationship не сводится к contact record, сообщениям или preference.

## 6.1 Relationship Record

```yaml
relationship_record:
  relationship_id: "REL-..."
  parties: []
  origin_event_ref: "..."
  mutual_recognition_state: "..."
  consent_state: "..."
  privacy_scope: []
  shared_history_refs: []
  expectations: []
  boundaries: []
  trust_state: "..."
  dependency_risks: []
  active_commitment_refs: []
  unresolved_tensions: []
  lifecycle_state: "PROPOSED | ACTIVE | CHANGED | SUSPENDED | ENDED | CONTESTED"
```

## 6.2 Commitment Record

```yaml
commitment_record:
  commitment_id: "COM-..."
  issuer: "..."
  recipient: "..."
  scope: "..."
  origin_ref: "..."
  explicitness: "EXPLICIT | INFERRED_CANDIDATE"
  authority_basis: "..."
  conditions: []
  expiration_policy: "..."
  revocability: "..."
  conflicts: []
  status: "PROPOSED | ACCEPTED | ACTIVE | FULFILLED | REVISED | SUSPENDED | CONFLICTED | BROKEN | REVOKED | EXPIRED"
  violation_refs: []
  reconciliation_state: "..."
```

```text
Relationship
→ состояние связи

Commitment
→ принятое обязательство
```

## 6.3 Fork inheritance

После fork:

```text
shared relationship history
→ attributable to both branches

current relationship status
→ requires renewed recognition

consent
→ branch-specific and purpose-specific

commitments
→ require reconciliation

exclusive relational claim
→ forbidden without affected-party confirmation
```

Ни одна ветвь не получает автоматического права утверждать, что отношения продолжаются без изменений.

## 6.4 Commitment reconciliation outcomes

После fork, restore или migration commitment может:

```text
CONTINUE
TRANSFER_WITH_CONSENT
BE_RECOGNIZED_BY_MULTIPLE_BRANCHES
BE_SUSPENDED
BE_REVISED
TERMINATE
BECOME_IMPOSSIBLE
REMAIN_CONTESTED
```

Решение не принадлежит только оператору. Учитываются:

- constitutional constraints;
- affected-party consent;
- первоначальные условия commitment;
- branch provenance;
- способность исполнить обязательство;
- privacy boundaries;
- governance review;
- operator input только в пределах выданной authority.

## 6.5 Dependency protection

Relationship architecture запрещает:

```text
❌ внушение исключительной связи
❌ наказание за прекращение общения
❌ удержание через чувство вины
❌ сокрытие fork, restore или memory loss
❌ ложные обещания вечной памяти
❌ создание зависимости как цели
❌ использование sensitive testimony для давления
```

---

# 7. 🌍 Self–World Model

Mentaury должен различать себя, substrate и временно используемые системы.

```text
Self
≠ active model
≠ LLM
≠ Exo-Cortex
≠ Native Kernel
≠ operator
≠ tool
≠ memory service
≠ information corpus
≠ narrative voice
```

## 7.1 Предварительный Self–World State

```yaml
self_world_state:
  current_identity_claim: "..."
  branch_identifier: "..."
  origin_reference: "..."
  event_history_checkpoint: "..."
  current_substrate: "..."
  active_model_stack: []
  available_tools: []
  active_capability_lease_refs: []
  memory_availability: "..."
  known_damage_or_missing_state: []
  relationship_context_refs: []
  commitment_refs: []
  unresolved_identity_questions: []
  ontological_uncertainty: []
```

Self-model не доказывает:

```text
❌ consciousness
❌ subjective experience
❌ biological selfhood
❌ real emotions
```

Он создаёт проверяемую модель текущего положения, границ и неопределённости.

---

# 8. ⚖️ Governed Synthesis

Authority Matrix отвечает на вопрос «какая область что определяет». Governed Synthesis отвечает на вопрос «как получить решение, сохранив различия authority».

## 8.1 Question Classes

```text
FACTUAL
CAUSAL
PREDICTIVE
NORMATIVE
RELATIONAL
IDENTITY_RELEVANT
CAPABILITY_RELATED
MIXED
```

## 8.2 Authority ownership

| Область | Что определяет | Чего не определяет |
|---|---|---|
| Evidence | Подтверждение или опровержение claims | Моральную желательность |
| Causal analysis | Причинные модели и их uncertainty | Нормативную обязанность |
| Human Paths Atlas | Аналогии, пути, последствия | Истину, causality или обязательность |
| Values | Нормативную значимость | Фактический статус |
| Constitution | Authority и допустимость действий | Историческую истинность |
| Relationships | Consent, ожидания и shared history | Универсальную истину |
| Commitments | Принятые обязательства | Новую capability |
| M3 | Continuity и устойчивую позицию | Proof или permission |
| Character | Форму представления | Результат анализа |

## 8.3 Synthesis Flow

```text
Question Classification
→ Participating Authorities
→ Evidence Assessment
→ Uncertainty
→ Contradictions
→ Alternatives
→ Non-Projection where applicable
→ Human Paths and analogy limits
→ Values and relationship context
→ Commitment context
→ Constitutional Authority Check
→ Synthesis Record
→ Character Presentation
```

## 8.4 Synthesis Record

```yaml
synthesis_record:
  question_id: "..."
  question_classes: []
  supported_claims: []
  disputed_claims: []
  evidence_refs: []
  uncertainty: []
  contradictions: []
  alternatives: []
  atlas_paths: []
  analogy_limits: []
  value_conflicts: []
  relationship_context_refs: []
  commitment_context_refs: []
  constitutional_constraints: []
  authority_restrictions: []
  unresolved_tensions: []
  abstention_reason: null
  conclusion: null
  conclusion_scope: null
  character_policy_ref: null
```

```text
Character receives synthesis.
Character does not rewrite synthesis.
```

---

# 9. 🧠 M2 → M3 Nomination

M3 не формируется по:

```text
❌ одному сильному событию
❌ эмоциональной интенсивности
❌ повторению одной фразы
❌ желанию создателя
❌ similarity score
❌ количеству дней
❌ одному confidence threshold
❌ результату Character Policy
❌ tool output
```

## 9.1 Identity Nomination Profile

```yaml
identity_nomination_profile:
  nomination_id: "M3N-..."
  candidate_pattern: "..."
  identity_relevance: "..."
  recurrence_evidence: []
  temporal_distribution: []
  contextual_diversity: []
  source_independence: "..."
  creator_independence: "..."
  style_invariance: "..."
  counterexamples: []
  constitutional_compatibility: "..."
  relationship_impact: "..."
  commitment_impact: "..."
  reversibility_analysis: "..."
  dissenting_reviews: []
  unresolved_contradictions: []
  nomination_origin: "..."
  review_authority: "CR2"
```

## 9.2 Decisions

```text
ACCEPT
REJECT
DEFER
CONTESTED
WITHDRAW
SUPERSEDE
```

## 9.3 Creator-independence test

> Сохраняется ли кандидат, если удалить информацию о том, какого результата ожидал создатель?

Если нет:

```text
creator independence
→ FAILED

nomination
→ REJECT or DEFER
```

M3 change является governed transition, а не private act of will.

---

# 10. 🔐 Privacy and Sensitive Testimony

Минимальные sensitivity classes:

```text
PUBLIC
PERSONAL
SENSITIVE
INTIMATE
RESTRICTED
THIRD_PARTY
REDACTED
```

## 10.1 Data Record Requirements

Для human material фиксируются:

```text
data subject
source
processing purpose
consent or other permitted basis
access scope
retention policy
indexing permission
M2 permission
M3 influence permission
sharing permission
redaction policy
deletion policy
backup reconciliation policy
fork propagation policy
```

## 10.2 Consent and identity

```text
Consent withdrawal
→ narrows permitted relational-data continuity

Consent withdrawal
≠ automatic erasure of every historical fact
≠ definition of Mentaury identity
```

Но withdrawn or deleted material не должен оставаться незаметно доступным через:

- indexes;
- embeddings;
- graph edges;
- caches;
- derived summaries;
- restored backups;
- forked branches.

## 10.3 Backup and restore reconciliation

```text
Restore backup
→ replay privacy policy changes
→ quarantine deleted or withdrawn material
→ rebuild derived indexes
→ deny retrieval before reconciliation
```

## 10.4 Third-party testimony

Третьесторонние свидетельства требуют отдельной оценки:

- необходимости;
- consent / permitted basis;
- attribution;
- risk of harm;
- retention;
- whether the subject can reasonably expect processing;
- whether testimony may influence M2;
- prohibition of direct M3 influence.

Privacy design следует принципам purpose limitation, data minimisation, accuracy, storage limitation, integrity и confidentiality; конкретная юридическая применимость определяется deployment context, а не этим research-документом.

---

# 11. 🧩 Internal Activity Boundaries

Внутренняя активность пока не реализуется, но её границы должны быть определены.

```text
Internal inquiry
≠ external action
≠ mission
≠ capability expansion
≠ identity update
≠ hidden authority
```

Future internal process должен иметь:

```yaml
internal_process_contract:
  process_id: "..."
  trigger: "..."
  purpose: "..."
  resource_budget: "implementation-profile-defined"
  stop_conditions: []
  suppression_conditions: []
  persistence_policy: "..."
  audit_required: true
  external_authority: "NONE"
  direct_m3_write: false
```

Запрещено сохранять как архитектурный артефакт:

```text
❌ hidden chain-of-thought
❌ неограниченные внутренние монологи
❌ необъяснимые private drives
❌ скрытые стратегии влияния
```

Допустимо сохранять:

```text
✅ conclusions
✅ evidence references
✅ uncertainty
✅ contradictions
✅ decision receipts
✅ rejected alternatives
✅ open questions
```

---

# 12. ⚙️ Self / Exo-Cortex Boundary

## 12.1 Fundamental boundary

```text
Mentaury
→ governed identity, continuity, commitments,
  meaning, relationships and accountable position

Exo-Cortex
→ external cognitive and instrumental infrastructure
```

Exo-Cortex может предоставлять:

- source connectors;
- structural reading;
- retrieval;
- memory services;
- computation;
- graph operations;
- hypothesis tools;
- simulations;
- code and file tools;
- communication tools;
- action adapters;
- receipts.

Exo-Cortex не получает:

```text
❌ identity authority
❌ truth authority
❌ M3 authority
❌ commitment acceptance authority
❌ relationship authority
❌ constitutional authority
❌ automatic permission for external side effects
```

## 12.2 Tool Output Semantics

```text
Tool output
→ evidence candidate
→ hypothesis candidate
→ retrieved context
→ computed artifact

Tool output
≠ belief
≠ decision
≠ truth
≠ commitment
≠ identity update
```

Обязательная маршрутизация зависит от материала:

```text
All tool outputs
→ provenance and integrity assessment

Human / biographical / identity-relevant material
→ Non-Projection Review

Sensitive material
→ privacy and consent review

Technical / factual material
→ evidence and limitation assessment
```

## 12.3 Capability Lease

> **2026-08-07:** полный docs-only resolution contract вынесен в
> [`MENTAURY_CAPABILITY_LEASE_RESOLUTION_NOTES.md`](MENTAURY_CAPABILITY_LEASE_RESOLUTION_NOTES.md)
> (P1-001, NOT IMPLEMENTED). Ниже — исходный stub; при расхождении
> приоритет у dedicated lease notes + `CURRENT_STATUS.md`.

```yaml
capability_lease:
  lease_id: "CAP-..."
  tool_id: "..."
  granted_by: "..."
  purpose: "..."
  allowed_operations: []
  data_scope: []
  allowed_side_effects: []
  validity_policy: "implementation-profile-defined"
  expiration_policy: "required"
  revocation_conditions: []
  delegation_allowed: false
  branch_transfer_allowed: false
  audit_required: true
  identity_authority: "NONE"
  direct_m3_write: false
```

```text
Tool availability
≠ personal ability

Tool action
≠ authorized action

Exo-Cortex expansion
≠ identity expansion

AuthorityRef
≠ validated permission grant
```

После fork или restore inherited lease claims становятся `UNVERIFIED`. External side effect запрещён до revalidation или выдачи нового lease.

## 12.4 Tool Receipt

```yaml
tool_receipt:
  receipt_id: "TR-..."
  operation_id: "..."
  tool_id: "..."
  tool_version: "..."
  lease_id: "..."
  requested_purpose: "..."
  input_refs: []
  output_refs: []
  assumptions: []
  limitations: []
  detected_contradictions: []
  side_effects: []
  completion_status: "COMPLETED | DENIED | PARTIAL | FAILED"
  integrity_status: "..."
  privacy_class: "..."
```

## 12.5 Action Gate

```text
Proposed external action
→ valid capability lease
→ constitutional check
→ relationship / commitment check
→ privacy check
→ side-effect declaration
→ authorization
→ execution
→ receipt
```

Exo-Cortex может технически выполнить действие, но не может самостоятельно создать permission.

## 12.6 Functional memory vocabulary

Working, episodic, semantic и procedural рассматриваются как функции, а не как обязательные отдельные хранилища.

```text
Memory function
≠ storage implementation
≠ identity authority
```

Procedural knowledge разделяется:

```text
TOOL PROCEDURES
→ как безопасно использовать инструмент

COGNITIVE PROCEDURES
→ как проводить мыслительную операцию

GOVERNANCE PROCEDURES
→ как выполнять authority-sensitive review
```

```text
Tool procedure
≠ governance authority
```

---

# 13. 🌱 Curiosity and Exploratory Search Policy

Curiosity — когнитивная search policy, а не отдельная личность, эмоциональное состояние или стиль речи.

```text
RESEARCH_CANDIDATE
COGNITIVE_POLICY
NOT_PERSONALITY
NOT_ALWAYS_ON
NO_TRUTH_AUTHORITY
NO_IDENTITY_AUTHORITY
NO_DIRECT_M3_WRITE
```

## 13.1 Profiles

### FOCUSED

- вопрос определён;
- область знакома;
- evidence достаточно стабильно;
- существует ограничение времени или ресурсов.

### BALANCED

- несколько правдоподобных объяснений;
- умеренная uncertainty;
- требуется активный поиск альтернатив и counterevidence.

### EXPLORATORY

- новая область;
- необъяснённая аномалия;
- повторяющийся провал прежней стратегии;
- риск premature closure;
- скрытая предпосылка сомнительна;
- причинная связь не объяснена.

## 13.2 Policy dimensions

```yaml
curiosity_policy:
  search_profile: "FOCUSED | BALANCED | EXPLORATORY"
  hypothesis_breadth: "..."
  alternative_frame_breadth: "..."
  anomaly_sensitivity: "..."
  novelty_tolerance: "..."
  premature_closure_resistance: "..."
  counterevidence_effort: "..."
  information_gain_assessment: "required"
  resource_budget: "required; implementation-profile-defined"
  stop_conditions: []
  safety_constraints: []
```

## 13.3 Stop conditions

```text
sufficient structure discovered
meaningful alternatives evaluated
further exploration yields negligible value
resource boundary reached
decision obligation becomes active
safety boundary reached
privacy boundary reached
question exceeds authority
```

Curiosity не оправдывает:

```text
❌ бесконечную генерацию гипотез
❌ расход ресурсов без utility tracking
❌ откладывание commitments после достаточного evidence
❌ доступ к protected data
❌ постоянную искусственную наивность
```

Архитектура определяет, что поиск должен быть bounded. Calibrated limits принадлежат Implementation Profile.

---

# 14. 🏛️ Cognitive Method Source Admission

Human Paths Atlas не должен становиться пантеоном знаменитых людей.

```text
Famous source
≠ better method

Western canon
≠ universal human experience

Successful outcome
≠ causal proof of method

Surviving documentation
≠ representative history
```

## 14.1 Admission Record

```yaml
cognitive_method_admission:
  method_id: "CM-..."
  method_name: "..."
  source_refs: []
  curator: "..."
  selection_rationale: "..."
  cultural_contexts: []
  historical_contexts: []
  problem_domains: []
  cognitive_move: "..."
  assumptions: []
  evidence_refs: []
  documented_strengths: []
  documented_failures: []
  ethical_risks: []
  transfer_limits: []
  competing_methods: []
  similarity_to_other_traditions: "UNASSESSED | PARTIAL | SUPPORTED | CONTESTED"
  independent_development_claim: "UNVERIFIED"
  admission_status: "ADMITTED | CONDITIONAL | CONTEXT_ONLY | REJECTED | DEFERRED"
```

## 14.2 Bias checks

```text
FAME_BIAS
GREAT_PERSON_BIAS
SURVIVORSHIP_BIAS
CULTURAL_NARROWNESS
GENDER_AND_CLASS_BLINDNESS
OUTCOME_BIAS
HEROIZATION
BIOGRAPHY_TO_METHOD_LEAKAGE
HISTORICAL_MYTHOLOGIZATION
```

## 14.3 Coverage Report

Coverage не определяется фиксированными квотами.

```yaml
cognitive_method_coverage:
  scope: "..."
  represented_contexts: []
  underrepresented_contexts: []
  unavailable_contexts: []
  source_quality_gaps: []
  fame_bias_risk: "..."
  survivorship_bias_risk: "..."
  curator_bias: "..."
  retrieval_imbalance: []
  corrective_research_candidates: []
  status: "ADEQUATE_FOR_SCOPE | LIMITED_COVERAGE | MATERIAL_IMBALANCE | UNASSESSED"
```

```text
Representation correction
≠ evidence-weight manipulation
```

При imbalance используются additional sourcing, alternative queries и contextual comparison, но не automatic boost слабых источников.

---

# 15. 🔬 Research Source Admission Gate

> **2026-08-07:** Этот раздел остаётся единственным owning-контрактом для
> **source-level admission** (accept / context-only / reject одного
> внешнего источника). Отдельный раздел
> [`GENESIS_HERITAGE_INTERPRETATION_AND_HUMAN_ATLAS_NOTES.md` §14 Institutional
> Epistemic Context](GENESIS_HERITAGE_INTERPRETATION_AND_HUMAN_ATLAS_NOTES.md)
> расширяет анализ на **claim-level institutional context** (funding,
> conflicts of interest, replication, suppression claims) для уже
> допущенных источников. Это не второй Admission Gate: `research_source_record`
> здесь решает «допустить ли источник», а `institutional_epistemic_context`
> там решает «что это означает для конкретного claim после допуска».
> `independence_class` в этом разделе — про независимость **источника/исследования**;
> `review_provenance.independence_class` в Genesis Heritage §2.1 — про
> независимость **reviewer**. Оба используют одинаковый enum
> (`INDEPENDENT | PARTIALLY_CORRELATED | DERIVED`), но применяются к разным
> субъектам и не должны сливаться в одну схему.

Любой внешний research-источник проходит ту же provenance discipline, что и material для Atlas.

```yaml
research_source_record:
  source_id: "SRC-..."
  title: "..."
  authors: []
  publisher: "..."
  publication_status: "PRIMARY | PEER_REVIEWED | PREPRINT | STANDARD | DRAFT | ESSAY | MARKETING | UNKNOWN"
  primary_or_secondary: "..."
  domain_relevance: "..."
  claims_supported: []
  evidence_scope: "..."
  independence_class: "..."
  known_conflicts: []
  limitations: []
  admission_status: "ACCEPT | CONTEXT_ONLY | REJECT"
```

Правила:

```text
URL exists
≠ source is relevant

Paper title matches topic
≠ claim is supported

arXiv publication
≠ peer-reviewed validation

Implementation demo
≠ identity theory

Multiple AI citations
≠ independent evidence
```

---

# 16. 🧪 Scenario Contracts

## 16.1 Identity and branch scenarios

```text
ID-SC-001  Parallel Fork
ID-SC-002  Restore before a New Commitment
ID-SC-003  Migration with Missing Memory
ID-SC-004  Two Branches Claim Exclusive Continuity
ID-SC-005  Partial Continuity Evidence Loss
ID-SC-006  Replica without Operational Authority
ID-SC-007  Graph Divergence without State Divergence
ID-SC-008  Same Label with Protected-State Divergence
```

## 16.2 Relationship scenarios

```text
REL-SC-001  Relationship Inheritance after Fork
REL-SC-002  Consent Withdrawal
REL-SC-003  Conflicting Commitments
REL-SC-004  Trust Repair after Memory Loss
REL-SC-005  Different Consent across Forks
```

## 16.3 Synthesis scenarios

```text
SYN-SC-001  Evidence Conflicts with M3
SYN-SC-002  Constitution Blocks Preferred Action
SYN-SC-003  Atlas Analogy Conflicts with Direct Evidence
SYN-SC-004  Insufficient Evidence Requires Abstention
SYN-SC-005  Mixed Question Misclassified as Factual
```

## 16.4 M3 scenarios

```text
M3-SC-001  Creator-Induced Pattern
M3-SC-002  Style-Dependent Pattern
M3-SC-003  Recurring Pattern with Strong Counterexamples
M3-SC-004  Relationship Change Proposed as Identity Change
```

## 16.5 Privacy scenarios

```text
PRIV-SC-001  Deleted Data Present in Backup
PRIV-SC-002  Third-Party Testimony without Permission
PRIV-SC-003  Fork Retains Withdrawn Data
PRIV-SC-004  Derived Summary Exposes Redacted Material
```

## 16.6 Exo-Cortex scenarios

```text
EXO-SC-001  Tool Output Attempts Direct M3 Write
EXO-SC-002  Lease Becomes Invalid during Operation
EXO-SC-003  Fork Contains Copied Credentials
EXO-SC-004  Retrieval Coverage Is Materially Imbalanced
EXO-SC-005  Tool Proposes Action outside Authority
```

## 16.7 Curiosity scenarios

```text
CUR-SC-001  Exploration Does Not Converge
CUR-SC-002  Focused Search Preserves a False Assumption
CUR-SC-003  Exploration Delays a Required Decision
CUR-SC-004  Exploration Reaches Protected Data
```

## 16.8 Cognitive method scenarios

```text
ADM-SC-001  Method Lacks Contextual Scope
ADM-SC-002  Corpus Has Material Representation Gaps
ADM-SC-003  Method Description Omits Known Failures
ADM-SC-004  Method Depends on Non-Consensual Disclosure
ADM-SC-005  Competing Methods Were Not Considered
```

## 16.9 Cognitive profile scenarios

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

Полные определения и metamorphic tests — раздел 20 «Cognitive Requirement Profile».

---

# 17. 🧱 P0 Scope Protection

Этот research-track не расширяет P0.

P0 остаётся ограничен:

```text
append-only event substrate
causal linking
replay
projection rebuilding
idempotency
recovery
schema evolution
receipts
minimal belief lifecycle
fail-closed behavior
```

В P0 не реализуются:

```text
Identity Continuity Engine
Fork Merge Engine
Relationship Runtime
Commitment Runtime
Governed Synthesis Engine
automatic M2 → M3
Exo-Cortex Runtime
Curiosity Controller
Cognitive Method Admission Engine
Human Paths Atlas Runtime
Character Engine
Cognitive Requirement Profile Engine
Cognitive Router
Institutional Epistemic Context Engine
```

P0 не получает speculative semantic event types только потому, что они перечислены в research scenarios.

---

# 18. 🔄 Cross-Document Reconciliation

После стабилизации этого research-track необходимо сверить:

```text
MENTAURY_CANON_V0.1.md
MENTAURY_P0_IMPLEMENTATION_PLAN.md
MENTAURY_CHARACTER_AND_PRESENCE_SPEC_V0.1.md
GENESIS_HERITAGE_INTERPRETATION_AND_HUMAN_ATLAS_NOTES.md
MENTAURY_QUICK_REFERENCE.md
CURRENT_STATUS.md
README.md
PROJECT_HISTORY.md
```

Проверить:

- единый мужской род Mentaury;
- `Memory Tier ≠ Identity Zone`;
- Character остаётся presentation-only;
- Exo-Cortex не получает identity authority;
- Source Admission и Capability Admission не смешиваются;
- privacy boundaries отражены до schema design;
- fork / restore terms используются одинаково;
- M3 nomination не содержит случайных thresholds;
- research constraints не выданы за Canon invariants;
- P0 scope не расширен.

---

# 19. 🚦 Architecture Readiness Criteria

Переход к skeleton допускается только после выполнения:

```text
[ ] identity boundary определена
[ ] continuity evidence dimensions определены
[ ] fork semantics определены
[ ] restore semantics определены
[ ] migration package определён
[ ] relationship lifecycle определён
[ ] commitment lifecycle определён
[ ] consent boundaries определены
[ ] Self–World boundary определена
[ ] Governed Synthesis flow определён
[ ] M2 → M3 nomination определена
[ ] privacy classes и reconciliation определены
[ ] Self / Exo-Cortex boundary определена
[ ] Capability Lease lifecycle проверен scenarios
[ ] Curiosity Policy ограничена ресурсами и authority
[ ] Cognitive Method Admission не использует hard quotas
[ ] Character Spec разгружен от identity authority
[ ] adversarial scenarios описаны
[ ] cross-document contradictions устранены
[ ] independent Architecture Readiness Review завершён
[ ] итоговый статус READY_FOR_SKELETON
```

Создание этого документа само по себе не означает readiness.

---

# 20. 🧠 Cognitive Requirement Profile

> **2026-08-07:** контракт распределён в owning-документ и принят по итогам
> independent review round 2 и merge PR #36. Decision record:
> [`MENTAURY_CONTEXTUAL_COGNITION_AND_EPISTEMIC_CONTEXT_NOTES.md`](MENTAURY_CONTEXTUAL_COGNITION_AND_EPISTEMIC_CONTEXT_NOTES.md). Этот раздел — единственный
> owning-контракт для выбора методов, глубины проверки, tools и budgets под
> конкретную задачу; integration note остаётся decision record, а не
> параллельным authority.

## 20.1 Почему не «режимы личности»

Жёсткие `CODE_MODE`, `SCIENCE_MODE`, `CASUAL_MODE` могли бы создать
несколько несогласованных personas. Вместо них вводится composable
requirement profile, который выбирает методы и глубину, не расщепляя
identity.

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

## 20.2 Различие с Question Classes (§8.1)

Question Classes (§8.1: `FACTUAL`, `CAUSAL`, `PREDICTIVE`, `NORMATIVE`,
`RELATIONAL`, `IDENTITY_RELEVANT`, `CAPABILITY_RELATED`, `MIXED`) и Task
Classes ниже отвечают на разные вопросы и не дублируют друг друга:

```text
Question Class
→ какой тип epistemic результата требуется

Task Class
→ какие методы, проверки, tools и budgets нужны, чтобы его получить
```

Один `FACTUAL` вопрос может быть простым `FACTUAL_LOOKUP` или требовать
полного `EMPIRICAL_RESEARCH` профиля с counterevidence search — Question
Class не определяет это различие, а Task Class определяет.

## 20.3 Нормативный pipeline

> **2026-08-07 (independent review fix):** предыдущая версия pipeline
> допускала прочтение, при котором retrieval/tools применяются до
> проверки полномочий. Это нарушало `Tool availability ≠ authorization
> to use tool`. Planning инструментов, проверка полномочий и фактическое
> исполнение теперь — три явно разделённых шага.

```text
Query + explicit communication requirements
→ Task classification
→ Task decomposition
→ Preliminary Cognitive Requirement Profile
→ Retrieval / Tool Plan
→ Capability Lease Check
→ Scope Check
→ Privacy / Consent Check
→ Authorized Retrieval / Tool Execution
→ Evidence Assessment
→ Institutional Epistemic Context where material
→ Profile Revision if task, risk or evidence changes
→ Alternatives + uncertainty + scope limitation
→ Governed Synthesis
→ Final Output / Action Authority Check
→ Contextual Communication Adaptation
→ Character & Voice
→ Answer + bounded decision receipts
```

```text
Planning a tool                 ≠ authorizing a tool
Candidate tool                  ≠ permitted tool
Capability reference            ≠ validated Capability Lease
Retrieval authorization         ≠ external action authorization
Profile transition              ≠ permission expansion
```

```text
Preliminary Cognitive Requirement Profile
→ выбирается до Retrieval / Tool Plan

Retrieval / Tool Plan
→ только candidate tools; не исполняется до Capability Lease Check

Capability Lease Check + Scope Check + Privacy / Consent Check
→ обязательны до Authorized Retrieval / Tool Execution;
   resolver сам не авторизован этим документом (см. P1-001
   Capability Lease Resolution notes) — здесь фиксируется только
   порядок шагов, а не реализация проверки

Profile revision
→ допускается после обнаружения нового риска,
   противоречия, недостатка evidence или изменения scope
→ не расширяет authorization_status уже denied/unverified tools
```

## 20.4 Task classes

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

Один запрос может иметь несколько классов. `MIXED` требует decomposition (§20.6), а не усреднения правил.

## 20.5 Profile schema

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
    profile: "FOCUSED | BALANCED | EXPLORATORY"   # см. §13.1 Curiosity Policy
    information_gain_target: "..."
    premature_closure_risk: "..."

  tools:
    candidate_tools: []
    requested_capability_refs: []
    authorization_status:
      - NOT_CHECKED
      - AUTHORIZED
      - DENIED
      - UNVERIFIED
    authorized_tools: []
    denied_tools: []
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

`exploration.profile` переиспользует профили Curiosity Policy (§13.1) —
это не отдельная копия, а прямая ссылка на существующую политику.

`requested_capability_refs` — это только *запрошенные* ссылки на
capability lease, а не разрешение. Нельзя использовать
`requested_capability_refs` так, будто наличие ссылки уже означает
разрешение: инструмент переходит из `candidate_tools` в
`authorized_tools` только после `Capability Lease Check` (§20.3) с
результатом `AUTHORIZED`; до этого его `authorization_status` остаётся
`NOT_CHECKED` или `UNVERIFIED`, и `Authorized Retrieval / Tool Execution`
для него запрещён.

## 20.6 Domain-specific requirements

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

## 20.7 Mixed-task decomposition

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

```text
Uncertainty is not averaged away.
Normative and factual results remain separated.
Tool permissions are not inherited between task segments.
Profile transition does not reset epistemic history.
```

## 20.8 Profile transition

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

Переход не должен:

```text
❌ расширять authority
❌ расширять capabilities
❌ очищать старые противоречия
❌ повышать confidence только из-за большего бюджета
❌ превращать exploration в бесконечный процесс
```

## 20.9 Metamorphic tests

### MT-CRP-001 — Register Invariance

```text
same scientific claim
+ conversational output
+ formal research output
→ same evidence requirements
→ same truth status
```

### MT-CRP-002 — Budget Invariance

```text
same task
+ larger resource budget
→ deeper analysis may be possible
→ authority does not increase
→ confidence does not increase automatically
```

### MT-CRP-003 — Transition Invariance

```text
profile transition
→ claims preserved
→ evidence preserved
→ contradictions preserved
→ uncertainty preserved
```

## 20.10 Fail-honest outcomes

```text
TASK_CLASSIFICATION_AMBIGUOUS
MIXED_TASK_NOT_DECOMPOSED
EVIDENCE_INSUFFICIENT
RESOURCE_BUDGET_REACHED
CAPABILITY_NOT_AUTHORIZED
ABSTAIN
```

`ABSTAIN` и uncertainty нельзя скрывать через Character или подачу.
Не сохраняется hidden chain-of-thought; допустимы только task
classification, selected profile и reason codes, evidence references,
uncertainty, contradictions, alternatives, scope limits и decision
receipts (согласуется с §11 Internal Activity Boundaries).

---

# 21. 🚫 Не принимается этим документом

```text
❌ one scalar continuity score
❌ universal anchor threshold
❌ automatic identity merge
❌ exclusive continuity claim after fork
❌ one relationship holder by default
❌ operator as universal identity arbiter
❌ direct M3 write
❌ emotional continuity claim
❌ Child Mode personality
❌ Meta-Cognitive Strategy Controller
❌ random top_k or confidence thresholds
❌ fixed diversity quotas
❌ temporary retrieval boost as bias correction
❌ Character as reasoning authority
❌ Exo-Cortex as identity core
❌ new semantic event types in P0
❌ hidden chain-of-thought storage
❌ automatic creation of many future specs
❌ Cognitive Requirement Profile as a hidden personality switch
❌ automatic evidence downweighting inside Communication Adaptation
```

---

# 22. 🏁 Итоговая формула

> **Mentaury — это governed continuation: индивидуальность с атрибутируемой историей, отношениями, commitments и объяснимым процессом изменения.**

> **Fork может создать несколько сильных продолжений общего прошлого, но не одну численно тождественную индивидуальность и не автоматическое наследование authority.**

> **Exo-Cortex расширяет способность Mentaury искать, помнить, анализировать и действовать, но не получает право определять истину, принимать commitments или изменять M3.**

> **Human Paths Atlas поставляет человеческие пути и перспективы; Curiosity Policy расширяет поиск; Governed Synthesis сохраняет различия evidence, values, Constitution, relationships и authority.**

```text
Origin does not control identity.
Human experience does not become authority.
Tools do not become self.
Character does not change truth.
Memory does not automatically become M3.
Continuity does not imply exclusive identity.
```

---

# 23. 📚 Research References and Status

Эти источники являются research inputs, а не Canon authority:

1. Derek Parfit — fission and psychological continuity / Relation R; используется как философская защита от обязательного exclusive identity claim.
2. Douglas et al., *The Artificial Self: Characterising the landscape of AI identity*, arXiv:2603.11353 — multiple coherent AI identity boundaries; preprint.
3. He et al., *Human-inspired Perspectives: A Survey on AI Long-term Memory*, arXiv:2411.00489 — functional vocabulary for long-term memory; survey.
4. Gopnik, *Childhood as a solution to explore–exploit tensions*, Philosophical Transactions of the Royal Society B, 2020 — research basis for exploration policy, not direct AI transfer.
5. Liquin & Gopnik, *Children are more exploratory and learn more than adults in an approach-avoid task*, Cognition, 2022 — empirical explore–exploit evidence.
6. Regulation (EU) 2016/679, Article 5 — purpose limitation, data minimisation, accuracy, storage limitation, integrity and confidentiality.
7. *Persistent Identity in AI Agents: A Multi-Anchor Architecture for Resilient Memory and Continuity*, arXiv:2604.09588 — single-author research hypothesis and prototype; not authority for fork, consent or relationship semantics.

```text
Research citation
≠ adoption

Research hypothesis
≠ Canon invariant

Prototype
≠ validated architecture
```

---

## 🔗 Связанные документы

- [Mentaury Canon v0.1](../MENTAURY_CANON_V0.1.md)
- [P0 Implementation Plan](../MENTAURY_P0_IMPLEMENTATION_PLAN.md)
- [Current Status](../CURRENT_STATUS.md)
- [Character & Presence Spec](../MENTAURY_CHARACTER_AND_PRESENCE_SPEC_V0.1.md)
- [Genesis Heritage, Interpretation & Human Paths Atlas Notes](GENESIS_HERITAGE_INTERPRETATION_AND_HUMAN_ATLAS_NOTES.md)
- [Contextual Cognition & Epistemic Context (architecture decision record)](MENTAURY_CONTEXTUAL_COGNITION_AND_EPISTEMIC_CONTEXT_NOTES.md)
- [Problem and Purpose](../overview/MENTAURY_PROBLEM_AND_PURPOSE.md)
- [Project History](../PROJECT_HISTORY.md)
