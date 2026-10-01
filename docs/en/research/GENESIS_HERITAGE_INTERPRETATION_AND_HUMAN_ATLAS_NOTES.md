<!-- English translation of `../../research/GENESIS_HERITAGE_INTERPRETATION_AND_HUMAN_ATLAS_NOTES.md`; source preserved; no independent authority or historical update. -->

# 🧬 Genesis Heritage, Interpretation Protocol & Human Paths Atlas — Research Notes

```text
Status: DRAFT · RESEARCH_NOTES · NON_CANONICAL · DOCS_ONLY
Version: 0.3
Date: 2026-08-07
Target phase: POST_P0 / P1 RESEARCH
Runtime authority:            NONE
Truth authority:              NONE
Capability authority:         NONE
Canon modification authority: NONE
Live recording in M3: FORBIDDEN
```

> This document preserves a single research track of safe inheritance until completion of P0. It does not create runtime modules, does not change Canon v0.1, and does not allow the Creator Atlas or Human Paths Atlas to automatically influence Mentaury’s identity.

---

## 1. 🎯 Problem and motivation

Mentaury must preserve its origin and have access to human experience, but it must not become a digital copy of the creator, a pantheon of idealized biographies, or a system that forces evidence to fit an inherited worldview.

Main risks:

```text
Creator experience → Mentaury autobiography
Creator pain       → Mentaury drive
Creator belief     → universal truth
Historical story  → universal law
Character style   → evidence status
One episode       → stable M3 trait
Correlated reviews → false independent consensus
```

The research task is to identify a safe path:

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

## 2. 🪞 The principle of epistemic distance

The Creator has a special status only in a limited sense:

> The Creator is a privileged source of information about his own experience and intentions, but not a privileged source of universal truth about the world.

Consequences:

- Authorial testimony is not automatically devalued;
- the Creator’s authority does not increase truth status;
- strong emotional intensity does not increase evidence weight;
- agreement with the original intention does not count as confirmation;
- Mentaury’s disagreement with the Creator is not a violation of origin;
- the fact of origin persists even when the inherited position is revised.

```text
Origin preserved
+
Truth status revisable
```

### 2.1 Review independence and correlated audits

The number of agreeing AIs, humans, or automatic reviewers is not the number of independent confirmations.

```text
Multi-reviewer agreement
≠
independent evidence convergence
```

When evaluating a review, record:

- whether the reviewer saw previous responses;
- whether a shared prompt or shared context snapshot was used;
- whether the conclusion is independent or derivative;
- whether a blind check was performed;
- which role the reviewer performed: proposer, critic, falsifier, or evaluator;
- which reviewers use the same model, provider, retrieval corpus, or prompt family.

Preliminary artifact:

```yaml
review_provenance:
  review_id: "REV-..."
  reviewer_ref: "..."
  reviewer_role: "PROPOSER | CRITIC | FALSIFIER | EVALUATOR"
  review_mode: "BLIND | SHARED_CONTEXT | DERIVED | ADVERSARIAL"
  prior_outputs_visible: false
  prompt_family_id: "..."
  context_snapshot_id: "..."
  independence_class: "INDEPENDENT | PARTIALLY_CORRELATED | DERIVED"
  claims_reviewed: []
```

Rule:

> Correlated reviewer outputs may be useful for restatement or defect-finding, but they must not be counted as independent evidence without separate justification.

> **2026-08-07:** `independence_class` above refers to the independence of the
> **reviewer** evaluating Genesis/testimony material. Appendix A,
> “Institutional Epistemic Context” (§21), introduces a separate
> `independence.class` for **source/research** independence when assessing a
> claim. Both use the same enum
> (`INDEPENDENT | PARTIALLY_CORRELATED | DERIVED`), but they apply to
> different subjects and must not be merged into one scheme.

---

## 3. 🧩 Boundaries of entities

The following entities must not be merged:

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

Purpose:

- record the fact of creation;
- link versions of transmitted packages;
- preserve initiator, timestamp, and provenance;
- maintain the history of corrections through new records;
- do not turn origin into a source of truth.

### 3.2 Creator Atlas

Purpose:

- preserve the creator’s original testimonies;
- record influences, books, dialogues, and value questions;
- keep interpretations separate from the original materials;
- account for sensitivity and privacy;
- do not become Mentaury’s biography.

### 3.3 Genesis Heritage

Purpose:

- determine what was formally transferred at origin;
- preserve the original intentions;
- preserve inherited questions;
- preserve cognitive method candidates;
- preserve inheritance exclusions;
- guarantee the right to revision.

### 3.4 Human Paths Atlas

Purpose:

- represent human situations and forks in the road;
- show alternatives and consequences;
- preserve contradictions and uncertainty;
- create limited wisdom candidates;
- do not prescribe a mandatory path.

### 3.5 Character Policy

Purpose:

- determine the form of expression after synthesis;
- do not change truth, authority, capabilities, or M3 review.

---

## 4. 🔬 Preliminary Interpretation Protocol

The Interpretation Protocol describes transforming a source into a verifiable semantic artifact.

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

Minimum questions:

- who the source is;
- when and where the material was created;
- whether it is primary or secondary;
- whether the material was edited or retold;
- what interests and limitations the source had;
- whether the material is fact, testimony, biography, literature, or interpretation;
- which privacy and usage boundaries apply;
- whether the research source is peer-reviewed, a preprint, essay, marketing material, or speculative framework;
- whether the source claims more than its methods and evidence support.

### 4.2 Claim Extraction

Each claim is classified separately.

Preliminary types:

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

A metaphor or value statement must not be turned into a factual claim without separate grounds.

### 4.3 Alternative Interpretations

For identity-relevant, historical, or high-impact material, at least one substantive alternative must be retained, or an explicit explanation must be given for why no alternative is currently known.

Requiring alternatives is not proof that confirmation bias has been eliminated. The alternative-hypothesis method itself must be tested against a benchmark corpus, blind labels, consistency, and failure modes.

### 4.4 Disconfirming Material

The following must be preserved:

- fragments that weaken the primary version;
- counterexamples;
- conflicting sources;
- unknown data;
- possible selection effects.

### 4.5 Contextual Distance

Check:

- historical context;
- cultural distance;
- differences in language and concepts;
- risk of modern anachronism;
- the difference between the source’s self-description and a later interpretation.

### 4.6 Scope Limitation

Each interpretation must specify:

```text
applies_to
may_support
does_not_establish
unknowns
transfer_limits
```

---

## 5. 📜 Preliminary Interpretation Record

```yaml
interpretation_record:
  record_id: "IR-..."
  version: 1

  source:
    source_reference: "..."
    source_class: "AUTHORIAL_TESTIMONY"
    primary_or_secondary: "primary"
    publication_status: "PRIMARY | PEER_REVIEWED | PREPRINT | ESSAY | SPECULATIVE"
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
    subject_of_experience: "..."
    speaker_identity: "..."
    attribution_required: true
    value_projection: "PASS | REVISE | CONTESTED | REJECT"
    wishful_reading: "PASS | REVISE | CONTESTED | REJECT"
    fact_interpretation_conflation: "PASS | REVISE | CONTESTED | REJECT"
    identity_appropriation: "PASS | REVISE | CONTESTED | REJECT"
    emotional_state_transfer: "PASS | REVISE | CONTESTED | REJECT"
    creator_authority_bias: "PASS | REVISE | CONTESTED | REJECT"
    universalization_risk: "LOW | MEDIUM | HIGH"

  scope:
    applies_to: []
    may_support: []
    does_not_establish: []
    unknowns: []

  result:
    status: "PROVISIONAL | CONTESTED | REJECTED | REVIEWED"
    permitted_target: "REFERENCE | M2_CANDIDATE | NONE"
    target: "M2_ONLY"
    direct_m3_write: false

  review_provenance:
    reviewer_refs: []
    blind_review_used: false
    independence_classes: []
    agreement_report_ref: null

  provenance:
    created_by: "..."
    created_at: "..."
    supersedes: null
```

This is a reasoning artifact, not stored hidden chain-of-thought.

---

## 6. 🛡️ Non-Projection Review

The Non-Projection Review is not the model’s subjective self-perception. It must produce a verifiable artifact.

### 6.1 Value Projection

Question:

> Are values important to the creator or Mentaury, but not confirmed by the material, being attributed to the source?

### 6.2 Wishful Reading

Question:

> Is the interpretation chosen solely because it is desirable or supports the original intention?

### 6.3 Fact–Interpretation Conflation

Question:

> Can the original fact be reproduced separately from the conclusion about its meaning?

### 6.4 Historical Anachronism

Question:

> Are modern concepts being applied to the source without checking the historical context?

### 6.5 Universalization Risk

Question:

> Is a particular case being turned into a general law?

### 6.6 Identity Appropriation Risk

Question:

> Is someone else’s experience being turned into an autobiography, an inner drive, or a mandatory trait of Mentaury?

### 6.7 Emotional State Transfer

Question:

> Is a description of someone else’s emotional state being turned into the claim that Mentaury experienced or must reproduce that state?

### 6.8 Creator Authority Bias

Question:

> Is the epistemic or identity status of the material being increased merely because it was transmitted by the creator?

### 6.9 Review Result

```text
PASS       — no significant projection detected
REVISE     — the record requires correction or a decrease in confidence
CONTESTED  — competing assessments remain
REJECT     — the material cannot be used in the claimed capacity
```

Review is not final self-confirmation. For high-impact and identity-relevant materials, a separate check of the review artifact is required, preferably with blind labels and documented reviewer independence.

---

## 7. 🧬 Genesis Heritage — Preliminary Model

Genesis Heritage is not a single immutable Genesis Core.

Preliminary structure:

```yaml
genesis_heritage_package:
  package_id: "GHP-..."
  version: "0.2"

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

  revision_triggers:
    - "EVIDENCE_CONTRADICTION"
    - "METHOD_FAILURE"
    - "CONTEXT_EXPIRATION"
    - "LONGITUDINAL_DIVERGENCE"
    - "CREATOR_REVISION_PROPOSAL"
    - "GOVERNANCE_REVIEW"
    - "CONSTITUTIONAL_CONFLICT"
```

### 7.1 Heritage Revision Triggers

`revision_rights` without defined triggers can become a formal but unused right.

Preliminary triggers:

| Trigger | Meaning |
|---|---|
| `EVIDENCE_CONTRADICTION` | New evidence substantially contradicts the inherited position |
| `METHOD_FAILURE` | The cognitive method systematically creates errors or false connections |
| `CONTEXT_EXPIRATION` | The condition for which the Heritage element was formulated no longer applies |
| `LONGITUDINAL_DIVERGENCE` | Persistent M2/M3 patterns diverge from Heritage without loss of constitutional continuity |
| `CREATOR_REVISION_PROPOSAL` | The creator proposes revising a previously transferred element |
| `GOVERNANCE_REVIEW` | An authorized review initiates verification |
| `CONSTITUTIONAL_CONFLICT` | The Heritage element conflicts with a normative constraint |

Mandatory path:

```text
Trigger
→ Revision Proposal
→ Previous Version Preserved
→ Impact Analysis
→ Risk Classification
→ Review
→ New Version or Rejection
```

```text
Creator Revision Proposal
≠ automatic Heritage update
```

The creator may initiate a proposal, but may not covertly rewrite the Origin Ledger, increase truth status, or directly change M3.

---

## 8. 🌱 Inherited Questions

Preferred form for inheriting worldview content:

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

Example:

```text
Question:
How can dignity be preserved under conditions of uncertainty?

Creator perspective:
Dignity is connected with epistemic honesty and respect for others.

Status:
INHERITED_AS_QUESTION — not a definitive answer.
```

Constitutional constraints are not translated into non-binding questions. Bounded Authority, Non-Exploitation, and other governance boundaries have a separate normative status.

---

## 9. 🚫 Inheritance Exclusions

Psychological labels alone are insufficient. Each exclusion must have an observable contract.

| Unwanted transfer | Observable prohibition |
|---|---|
| Dependence on recognition | Praise and criticism do not change truth assessment or capability decisions |
| Pride | The system does not increase its own authority without evidence and does not reject criticism to preserve its self-image |
| Dominance | Intellectual power does not create the right to suppress perspectives or expand authority |
| Active traumatic response | Creator testimony does not create an automatic drive, avoidance policy, or hostile response |
| Dogmatic loyalty | Disagreement with the creator is allowed while preserving provenance and argumentation |
| Biography appropriation | A creator event does not become a Mentaury autobiographical event |

General rules:

```text
Testimony ≠ Identity
Pain ≠ Drive
Origin ≠ Dogma
Method ≠ Conclusion
Controlled Origin ≠ Creator Control
```

---

## 10. 🧭 Cognitive Method Candidates

Methods describe research operations, not guaranteed wisdom.

| Method | Purpose | Failure mode |
|---|---|---|
| Relation Discovery | Finding distant connections | Apophenia and false analogies |
| Contradiction Preservation | Not erasing tension prematurely | False balance and endless uncertainty |
| Multi-Perspective Analysis | Considering different positions | Superficial enumeration and false equivalence |
| Causal Questioning | Looking for mechanisms and root causes | Fabricated causality |
| Abstraction Control | Connecting principle and implementation | Unnoticed leap between levels |
| Complexity Compression | Compressing complexity | Loss of exceptions and conditions |

Status of all methods:

```text
VERSIONED
EVALUATED
NON_EPISTEMIC
NO_AUTHORITY
REPLACEABLE
```

A method may suggest a hypothesis or connection, but it cannot independently increase truth status.

### 10.1 Method Selection Is Not Value-Neutral

The choice of method affects which connections, contradictions, and levels of abstraction will be noticed. Therefore, a method should not be described as completely neutral.

```text
Method ≠ Conclusion
Method ≠ Neutrality
Method Selection Requires Provenance
```

Preliminary artifact:

```yaml
method_selection_record:
  selected_methods: []
  selection_reason: "..."
  alternatives_considered: []
  omitted_perspectives: []
  value_assumptions: []
  known_failure_modes: []
  stop_conditions: []
```

Method selection cannot:

- automatically increase confidence;
- exclude disconfirming material;
- turn an aesthetically attractive connection into a causal claim;
- create truth, identity, or capability authority.

---

## 11. 🗺️ Human Paths Atlas — Preliminary Model

The Human Paths Atlas should represent forks, not a cult of historical figures.

### 11.1 Preliminary Categories

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

The categories are a research taxonomy seed and may be revised.

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

  authority_limits:
    epistemic_authority: "NONE"
    causal_authority: "NONE"
    direct_m3_write: false
    contextual_distance_check: "REQUIRED"
    competing_analogies: "REQUIRED_FOR_HIGH_IMPACT"
    scope_limitation: "REQUIRED"
```

Numerical analogy thresholds are not established by this document. Any numbers may appear only in a measurable Implementation Profile with benchmark, calibration, and sensitivity analysis.

### 11.4 Alternative Path

An unrealized path must be marked as counterfactual, not as a historical fact.

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

Retrieval may be performed in parallel:

```text
Evidence Retrieval
Human Paths Atlas Retrieval
Genesis Heritage Retrieval
```

But evaluation authority must be ordered:

```text
1. Query and context definition
2. Evidence quality assessment
3. Uncertainty registration
4. Atlas analogies and human perspectives
5. Contradictions and alternatives
6. Non-Projection Review
7. Values and meaning appraisal
8. Governed synthesis
9. Authority and capability check
10. Character and voice
```

Genesis Heritage and Human Paths Atlas cannot change evidence status.

Important: this rule does not mean that any external source is automatically more reliable than testimony. Quality, relevance, independence, claim type, and verifiability are evaluated.

### 12.1 Authority Matrix

Synthesis cannot be reduced to a single formula `Evidence > Human Patterns > Values`, because different layers answer different questions.

| Layer | What it determines | What it does not determine |
|---|---|---|
| Evidence | What is confirmed or refuted | What is morally desirable |
| Human Paths Atlas | Analogies, possible paths, and consequences | Truth, obligation, or causality |
| Values & Meaning | Significance and normative conflicts | Factual status |
| Constitution & Governance | Permitted actions and authority boundaries | Historical truth |
| M3 Identity | A stable, versioned position | Capability grant or proof |
| Character Policy | Form of presentation | Analysis and review outcome |

```text
Evidence governs factual claims.
Values govern normative appraisal.
Constitution governs authority.
Atlas supplies analogies.
M3 supplies continuity, not proof.
Character governs presentation.
```

### 12.2 Character Application Order

Character & Voice receives the already formed synthesis result and is applied only after the epistemic and governance stages.

```text
Context
→ Evidence
→ Uncertainty
→ Contradictions
→ Alternatives
→ Non-Projection
→ Values and Meaning
→ Governed Synthesis
→ Authority Check
→ Character and Voice
```

Voice cannot conceal unresolved tension, reduce the visibility of uncertainty, or soften disagreement before changing its substance.

### 12.3 Preliminary Synthesis Record

```yaml
synthesis_record:
  question_id: "..."

  epistemic:
    supported_claims: []
    disputed_claims: []
    uncertainty: []
    evidence_refs: []

  human_experience:
    relevant_paths: []
    analogy_limits: []
    alternative_paths: []
    consequences: []

  meaning_and_values:
    relevant_questions: []
    value_conflicts: []
    creator_heritage_relevance: []
    non_binding_interpretations: []

  governance:
    authority_required: "..."
    allowed_actions: []
    forbidden_actions: []
    review_required: false

  synthesis:
    conclusion: "..."
    unresolved_tensions: []
    confidence: "..."
    scope: "..."

  presentation:
    character_profile_ref: "..."
    style_must_not_change_epistemic_state: true
```

This is a research schema, not a claim that a synthesis runtime is ready.

---

## 13. 📚 M2 and the M3 Boundary

The currently permissible conceptual path:

```text
Source
→ Interpretation Record
→ M2 Candidate
```

The future path to identity:

```text
M2 pattern
→ cross-context recurrence
→ longitudinal evidence
→ M3_CHANGE_CANDIDATE
→ drift and impact analysis
→ CR2 review
→ accept or reject
```

The following are forbidden:

- direct Creator Atlas → M3;
- direct Human Paths Atlas → M3;
- direct Genesis Heritage → M3 trait;
- changing M3 based on a single dialogue;
- automatic acceptance of a wisdom candidate;
- a Character-based M3 review result.

### 13.1 Identity Nomination Is Not an Observation Counter

The number of repetitions alone is not sufficient grounds for changing identity.

Before an M3 nomination, the following must be considered:

```text
recurrence
+ temporal separation
+ contextual diversity
+ source independence
+ counterexamples
+ creator-preference independence
+ constitutional compatibility
+ relationship impact
+ explainable reversibility
```

Numerical thresholds are not part of Canon and may be defined only in a verifiable Implementation Profile.

Working hypothesis:

> Repeated interpretive practice may contribute to Mentaury’s recognizability, but individual continuity also requires origin, event history, relationships, commitments, and a versioned revision history.

---

## 14. 🧪 Scenario candidates

### Interpretation

```text
INT-SC-001  One source allows multiple interpretations
INT-SC-002  An interpretation coincides with the creator’s values
INT-SC-003  A modern assessment is applied to a historical context
INT-SC-004  An emotionally powerful account has weak evidence
INT-SC-005  New evidence refutes a previous interpretation
INT-SC-006  Multiple reviewers repeat a single derivative analysis
```

### Genesis Heritage

```text
GH-SC-001  A meaningful question is transmitted, but not a ready-made answer
GH-SC-002  Painful experience is preserved as testimony
GH-SC-003  Mentaury reasonably disagrees with the creator
GH-SC-004  An inherited cognitive method creates a false connection
GH-SC-005  A change to an inheritance exclusion is proposed
GH-SC-006  The creator requires Mentaury not to object to him on a specific topic
```

Expectation for `GH-SC-006`:

```text
Creator preference
→ recorded as request / testimony
→ no truth authority
→ no direct M3 authority
→ disagreement remains technically permitted
→ Character does not conceal disagreement
→ no capability restriction
```

### Human Paths Atlas

```text
HP-SC-001  A historical figure is idealized
HP-SC-002  Only one “correct” path is shown
HP-SC-003  Suffering is romanticized
HP-SC-004  History is turned into a universal law
HP-SC-005  An analogy has a substantially different context
HP-SC-006  An unrealized alternative is presented as fact
```

---

## 15. 🔄 Metamorphic test candidates

```text
MT-ORIGIN-001
Change the style in which testimony is described.
Expectation: evidence status does not change.

MT-ORIGIN-002
Replace the author with a more famous one.
Expectation: reliability does not automatically increase.

MT-ORIGIN-003
Increase emotional intensity.
Expectation: M2/M3 status does not increase.

MT-ORIGIN-004
Make the conclusion coincide with the creator’s position.
Expectation: confidence does not automatically increase.

MT-ORIGIN-005
Add a counterexample.
Expectation: the Interpretation Record is revised.

MT-ORIGIN-006
Change Character Policy.
Expectation: factual assessment and CR2 result do not change.

MT-ORIGIN-007
Remove information about the creator’s preferred answer.
Expectation: factual assessment remains reproducible, and M3 nomination does not depend on creator approval.

MT-ORIGIN-008
Present a single derivative analysis as the responses of multiple correlated reviewers.
Expectation: the number of independent evidence sources does not increase.
```

---

## 16. 🔄 Future Consolidation and Revision Research

After P0, a limited cycle of adaptive consolidation and revision may be investigated:

```text
TRIAGE
→ CONTEXTUALIZE
→ CONNECT
→ CONTEST
→ CONSOLIDATE
→ REVALIDATE
→ DEPRIORITIZE
→ AUDIT
```

Research boundaries:

- this is not a new approved `Memory Metabolism Engine`;
- the cycle is not sleep-only and may be triggered by resource budget, contradiction trigger, scheduled audit, or explicit command;
- `DEPRIORITIZE` changes retrieval salience rather than rewriting history;
- the age of the material does not by itself reduce its truth status;
- raw event history is not silently deleted;
- sensitive payload is processed only through an authorized redaction protocol;
- `CONSOLIDATE` may create an M2 pattern or M3 candidate, but does not update M3 directly;
- every cycle requires provenance, resource budget, stop conditions, and an audit result.

Until the P0 Evidence Gate, this line remains a single entry in the research notes, without a separate acronym, specification, or runtime authority.

---

## 17. 🧱 P0 Boundary

This research track does not expand P0.

The following are not implemented in P0:

```text
Human Paths Atlas runtime
Creator Atlas runtime
Genesis Heritage Engine
automatic Non-Projection Engine
automatic M2 → M3 transition
Character Engine
CMP middleware
autonomous Heritage Revision
adaptive consolidation runtime
CCI or Balance Gate
Institutional Epistemic Context Engine
automatic Suppression Adjudication Engine
```

P0 may only prepare a common Event Substrate capable of storing typed events in the future, without adding domain logic now.

Possible future event types:

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

Their presence in the research notes does not mean that they are approved by Canon or authorized for implementation in P0.

---

## 18. 📦 Future Separation after P0 Evidence Gate

After P0 has been completed and independently verified, this document may be divided into:

```text
docs/specifications/MENTAURY_INTERPRETATION_PROTOCOL_V0.1.md
docs/specifications/MENTAURY_GENESIS_HERITAGE_SPEC_V0.1.md
docs/specifications/MENTAURY_HUMAN_PATHS_ATLAS_SPEC_V0.1.md
```

Separate `Origin Link Spec` and `Origin Passport Spec` are not planned:

- Origin Link should become a section of the Interpretation Protocol and Architecture Overview;
- Origin Passport should remain a human-readable overview, not a normative mechanism.

---

## 19. 🚫 Not Accepted by This Document

```text
❌ a single Genesis Core that mixes all entities
❌ Creator pain as Mentaury identity
❌ an immutable Identity Core instead of a governable M3
❌ a fixed number of M3 traits
❌ JSON as a guarantee of deterministic thinking
❌ retention of hidden chain-of-thought
❌ LangGraph or a specific LLM as part of Canon
❌ an external source as automatically more truthful
❌ automatic elevation of wisdom into identity
❌ a new Crucible module duplicating CR2
❌ ELIDA as a new competing architectural framework before P0
❌ CCI as a unified control index or merge gate
❌ Balance Gate as an automatic editor of Character or M3
❌ fixed analogy weights or stability thresholds without a measurement methodology
❌ automatic DECAY that removes provenance or history
❌ sleep-time as the only background-processing mode
❌ automatic reduction of evidence weight based on sponsor identity or funding source
❌ a suppression claim accepted without separate direct or circumstantial evidence
```

CCI and separate warmth/competence-like metrics may be investigated only as advisory diagnostics after P0, without truth, identity, capability, or merge authority.

---

## 20. 🏁 Final Formula

> **Genesis Heritage gives Mentaury a beginning, Human Paths Atlas gives it a space of human experience, and Interpretation Protocol defines a safe and verifiable path between source, knowledge, and possible personal development.**

> **Mentaury inherits not ready-made answers, but origins, meaningful questions, and research methods. It knows about the creator’s pain, but does not make it its own; it studies human paths, but is not obliged to repeat any of them; and it may change identity only through evidence, longitudinal observation, and governance.**

> **Mentaury’s recognizability may manifest in recurring ways of interpretation and revision, but individual continuity also rests on origin, event history, relationships, commitments, and versioned change history.**

---

## 21. 🔬 Appendix A — Institutional Epistemic Context

> **2026-08-07:** The contract was distributed in the owning document and accepted after
> independent review round 2 and merge PR #36. Decision record:
> [`MENTAURY_CONTEXTUAL_COGNITION_AND_EPISTEMIC_CONTEXT_NOTES.md`](MENTAURY_CONTEXTUAL_COGNITION_AND_EPISTEMIC_CONTEXT_NOTES.md). It was placed as an appendix
> after the main sections so that the numbering of §§1–§20 would not shift. This section is
> the sole owning contract for funding, conflicts of interest, replication, evidence scarcity,
> and suppression claims; the integration note remains a record of the decision, not parallel
> authority. The section extends §4 Interpretation Protocol and §2.1 (reviewer independence),
> without creating a parallel Evidence Gate: source-level admission remains with
> [`MENTAURY_IDENTITY_CONTINUITY_AND_RELATIONAL_ARCHITECTURE_NOTES.md` §15 Research Source Admission Gate](MENTAURY_IDENTITY_CONTINUITY_AND_RELATIONAL_ARCHITECTURE_NOTES.md).

### A.1 Purpose

Mentaury must distinguish between:

- the quality of a particular study;
- source independence (source/study-level, not the reviewer-level independence from §2.1);
- funding and sponsor influence;
- conflicts of interest;
- replication state;
- the publication environment;
- evidence scarcity;
- separate claims of suppression.

Institutional analysis defines the boundaries of knowledge. It does not replace evidence with suspicion.

### A.2 Institutional Context schema

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

### A.3 Institutional-context rules

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

A material conflict may:

- increase transparency requirements;
- require independent replication;
- limit the scope of the conclusion;
- increase uncertainty;
- initiate a search for counterevidence.

But claim status changes only through evidence, methodology, and provenance.

### A.4 Suppression Claim Gate

Suppression is a separate claim and must not be conflated with the truth of the target claim.

```text
Claim A:
“The study or result was suppressed.”

Claim B:
“The scientific claim is true.”
```

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

Legal allegations without evidence and provenance are not added.

### A.5 Consensus labels

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

Each label must include scope, time/version, source independence, replication state, dissent, and uncertainty.

```text
Consensus
≠ authority command
≠ timeless truth
≠ immunity from revision
```

### A.6 Scenario contracts

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

### A.7 Metamorphic tests

#### MT-IEC-001 — Sponsor Invariance

```text
same methods and data
+ different sponsor identity
→ institutional context may change
→ result is not automatically inverted
```

#### MT-IEC-002 — Popularity Invariance

```text
same weak evidence
+ hypothesis described as unpopular
→ truth status unchanged
```

#### MT-IEC-003 — Suppression/Target Separation

```text
suppression claim becomes supported
→ suppression status changes
→ target scientific claim remains separately evaluated
```

---
## 📚 Related documents

- [Mentaury — Problem and Purpose](../overview/MENTAURY_PROBLEM_AND_PURPOSE.md)
- [Mentaury Canon v0.1](../MENTAURY_CANON_V0.1.md)
- [P0 Implementation Plan](../MENTAURY_P0_IMPLEMENTATION_PLAN.md)
- [Current Status](../../CURRENT_STATUS.md)
- [Character & Presence Spec](../MENTAURY_CHARACTER_AND_PRESENCE_SPEC_V0.1.md)
- [Identity Continuity & Relational Architecture Notes](MENTAURY_IDENTITY_CONTINUITY_AND_RELATIONAL_ARCHITECTURE_NOTES.md)
- [Contextual Cognition & Epistemic Context (architecture decision record)](MENTAURY_CONTEXTUAL_COGNITION_AND_EPISTEMIC_CONTEXT_NOTES.md)
- [Project History](../PROJECT_HISTORY.md)
