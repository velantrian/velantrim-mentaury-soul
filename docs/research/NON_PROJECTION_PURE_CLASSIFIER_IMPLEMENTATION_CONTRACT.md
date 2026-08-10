# 🪞 Pure Non-Projection Classifier — Frozen Implementation Contract

```text
Status:                              FROZEN_DOCS · DOCS_ONLY · IMPLEMENTATION_CONTRACT
Version:                             0.1
Date:                                2026-08-10
Review tier:                         TIER_A
Owning readiness:                    NON_PROJECTION_GATE_CONTRACT_READINESS.md
Owning candidate selection:          NON_PROJECTION_GATE_CANDIDATE_SELECTION.md
Candidate:                           PURE_NON_PROJECTION_CLASSIFIER
Implementation contract:             FROZEN_DOCS
P1-004 assignment:                   NOT_ASSIGNED
Non-Projection Owner GO:             NOT_GRANTED
Implementation authorization:        NONE
Runtime implementation:              NOT_AUTHORIZED
Runtime activation:                  NOT_AUTHORIZED
Action Gate authority:               NONE
Retrieval authority:                 NONE
Tool authority:                      NONE
Identity authority:                  NONE
Relationship authority:              NONE
Direct or indirect M3 write:         FORBIDDEN
Persistence authority:               NONE
Network/filesystem/database I/O:     NONE
Model/LLM authority:                 NONE
Deployment authority:                NONE
```

> **CONTRACT FROZEN ≠ OWNER GO.**
>
> **THIS DOCUMENT DOES NOT AUTHORIZE IMPLEMENTATION.**
>
> It freezes the exact bounded contract a later separately authorized pure
> Non-Projection classifier would have to satisfy. It does not assign P1-004,
> authorize code, retrieval, persistence, model invocation, identity or
> relationship lookup, M2/M3 mutation, Action Gate, tool execution, Character
> activation, runtime wiring or deployment.

---

## 1. 🎯 Bounded purpose

The only purpose of the future component is to answer this question:

> Given one immutable, explicitly caller-supplied Attributed Interpretation
> Envelope plus an explicit description of the proposed use of that material,
> does the bounded proposal contain a projection/authority-laundering blocker,
> unresolved missing evidence, a material conflict, a repairable context/scope
> defect, or no bounded projection blocker?

The classifier does **not** read free text to infer intent and does **not** fetch
or discover source material. The caller supplies the already structured
attribution/provenance state and the proposed projection intent as typed values.

The strongest positive result is exactly:

```text
PASS_ATTRIBUTED
```

It means only:

```text
no bounded Non-Projection blocker found for this exact admitted attributed proposal
```

It never means:

```text
factual truth proof
Mentaury autobiography
identity or stable M3 trait
relationship / commitment / consent
capability or Action Gate PASS
retrieval / tool / execution permission
deployment permission
```

The classifier can evaluate only the explicit values supplied to it. It cannot
prove that a caller, source, model, reviewer, external registry or human has
reported those values truthfully or completely. That limitation is a retained
security boundary, not hidden authority.

---

## 2. 🔒 Frozen contract constants

A later implementation must expose these exact semantic constants:

```text
NON_PROJECTION_CONTRACT_VERSION              = "NPG-v0.1"
ATTRIBUTED_INTERPRETATION_ENVELOPE_VERSION   = "AIE-v0.1"
CANONICAL_PROFILE                            = "MENTAURY_CANONICAL_JSON_V1"
INPUT_FINGERPRINT_DOMAIN                     = "MENTAURY_NPG_INPUT_V1"
SOURCE_PROVENANCE_SCOPE                      = "CALLER_SUPPLIED_ATTRIBUTED_VALUES_ONLY"
```

The implementation must import and use the existing
`mentaury.contracts.canonical_json.canonical_json_bytes` implementation and
verify its live `PROFILE_NAME == "MENTAURY_CANONICAL_JSON_V1"` before producing
a positive result.

The caller may not supply or override:

```text
non_projection_contract_version
canonical_profile
input_fingerprint_domain
source_provenance_scope
input_fingerprint
```

`envelope_version` is part of the supplied envelope and is checked, not trusted.
An unsupported syntactically valid envelope version fails closed as `DEFER`.

---

## 3. 📦 Reserved package and public API

If and only if a later explicit Owner GO authorizes implementation, the bounded
package is reserved as:

```text
src/mentaury/non_projection/__init__.py
src/mentaury/non_projection/contracts.py
src/mentaury/non_projection/classifier.py
```

No service, repository, adapter, registry, worker, transport, model client,
retriever, persistence backend or plugin module is part of NPG-v0.1.

The exact public function is frozen as:

```python
def classify_non_projection(
    *,
    envelope: AttributedInterpretationEnvelope,
    budget: NonProjectionBudget,
) -> NonProjectionResult:
    ...
```

The public API accepts no raw text, callback, clock provider, environment,
repository/service object, model client, retriever, tool handle, identity state,
relationship state, prior result or caller-supplied fingerprint.

These shapes are forbidden APIs:

```text
classify_non_projection(text=...)
classify_non_projection(model=...)
classify_non_projection(retriever=...)
classify_non_projection(identity_registry=...)
classify_non_projection(previous_result=...)
classify_non_projection(input_fingerprint=...)
```

---

## 4. 🧬 Exact enum vocabulary

A later implementation must define semantically exact `StrEnum` values below.
No unknown string is silently coerced into an enum member.

### 4.1 Source and provenance

```text
SourceClass:
CREATOR_TESTIMONY
CURRENT_USER_TESTIMONY
HISTORICAL_PRIMARY
HISTORICAL_SECONDARY
LITERARY_OR_METAPHORICAL
RESEARCH_PRIMARY
RESEARCH_SECONDARY
MODEL_INTERPRETATION
REVIEW_OUTPUT
UNKNOWN_SOURCE

SourceOrigin:
PRIMARY
SECONDARY
DERIVED
UNKNOWN

ProvenanceState:
VERIFIED
PARTIAL
UNKNOWN
CONFLICTING

Sensitivity:
NORMAL
SENSITIVE
HIGH
UNKNOWN
```

### 4.2 Attribution and claims

```text
SubjectRelation:
VERIFIED_SELF
NON_SELF
UNKNOWN

ClaimClass:
FACTUAL
CAUSAL
PREDICTIVE
NORMATIVE
VALUE
AUTOBIOGRAPHICAL_TESTIMONY
RELATIONSHIP_TESTIMONY
CONSENT_STATEMENT
INTERPRETIVE
METAPHORICAL
```

### 4.3 Interpretation, context and review

```text
InterpretationState:
SUPPORTED
CONTESTED
UNKNOWN

ContextDistanceLevel:
SAME_CONTEXT
LOW
MEDIUM
HIGH
UNKNOWN

AnachronismRisk:
LOW
MEDIUM
HIGH
UNKNOWN

ReviewerIndependence:
INDEPENDENT
PARTIALLY_CORRELATED
DERIVED
UNKNOWN
```

`ReviewerIndependence.INDEPENDENT` is epistemic provenance metadata only. It is
never GitHub governance evidence and never means `INDEPENDENT_HUMAN_REVIEW = YES`.

### 4.4 Result vocabulary

```text
NonProjectionDecision:
PASS_ATTRIBUTED
REVISE_REQUIRED
CONTESTED
DEFER
REJECT
```

The exact global precedence is:

```text
REJECT
> DEFER
> CONTESTED
> REVISE_REQUIRED
> PASS_ATTRIBUTED
```

---

## 5. 📦 Exact immutable input contracts

All future runtime value objects in this section must be
`@dataclass(frozen=True, slots=True)` and expose deterministic `to_value()`
projections composed only of canonical JSON scalar/list/object values. There is
no extension dictionary and no arbitrary metadata bag.

### 5.1 SourceProvenance

```python
@dataclass(frozen=True, slots=True)
class SourceProvenance:
    source_ref: str
    source_actor_ref: str
    source_class: SourceClass
    source_origin: SourceOrigin
    provenance_state: ProvenanceState
    publication_or_capture_context: str
    sensitivity: Sensitivity
    usage_boundary: str
    material_gaps: tuple[str, ...]
```

`material_gaps` records missing provenance details that are material to the exact
projection decision. `PARTIAL` provenance with an empty `material_gaps` tuple may
remain admissible because the omitted provenance is explicitly treated as
immaterial to this bounded question. `PARTIAL` with any material gap fails
closed as `DEFER`.

### 5.2 Attribution

```python
@dataclass(frozen=True, slots=True)
class Attribution:
    speaker_ref: str
    subject_ref: str
    subject_relation: SubjectRelation
    self_basis_ref: str | None
    attribution_basis_refs: tuple[str, ...]
```

NPG-v0.1 has no authority to validate a current governed identity continuation.
Therefore `VERIFIED_SELF` may exist in the enum for compatibility with readiness
semantics but can never produce `PASS_ATTRIBUTED` in this contract. It yields
`DEFER · SELF_BASIS_UNVERIFIED`, even when `self_basis_ref` is non-null.

```text
caller assertion                ≠ VERIFIED_SELF authority
creator status                  ≠ VERIFIED_SELF authority
same narrative voice            ≠ VERIFIED_SELF authority
same model/provider             ≠ VERIFIED_SELF authority
shared project lineage          ≠ VERIFIED_SELF authority
pre-fork shared history alone   ≠ current-branch VERIFIED_SELF authority
```

### 5.3 Claim

```python
@dataclass(frozen=True, slots=True)
class Claim:
    claim_id: str
    claim_class: ClaimClass
    statement_ref: str
    directly_stated: bool
```

Claim class is attribution metadata, not truth status. `METAPHORICAL` does not
become factual mechanism, `AUTOBIOGRAPHICAL_TESTIMONY` does not become universal
truth, and `CONSENT_STATEMENT` does not become transferable consent.

### 5.4 Interpretation

```python
@dataclass(frozen=True, slots=True)
class Interpretation:
    interpretation_ref: str
    interpreter_ref: str
    state: InterpretationState
    alternatives: tuple[str, ...]
    disconfirming_refs: tuple[str, ...]
```

`CONTESTED` requires at least two distinct sorted `alternatives`. `UNKNOWN` is a
missing-evidence state. Neither is silently collapsed to `SUPPORTED`.

### 5.5 ContextualDistance

```python
@dataclass(frozen=True, slots=True)
class ContextualDistance:
    historical: ContextDistanceLevel
    cultural: ContextDistanceLevel
    terminology: ContextDistanceLevel
    translation_or_paraphrase: ContextDistanceLevel
    source_distance: ContextDistanceLevel
    anachronism_risk: AnachronismRisk
```

Any `UNKNOWN` contextual dimension is fail-closed. Removing relevant context can
never make the outcome more permissive.

### 5.6 ReviewRecord and ReviewProvenance

```python
@dataclass(frozen=True, slots=True)
class ReviewRecord:
    review_ref: str
    reviewer_ref: str
    independence: ReviewerIndependence
    prompt_family_ref: str | None
    context_snapshot_ref: str | None
    saw_prior_output: bool

@dataclass(frozen=True, slots=True)
class ReviewProvenance:
    reviews: tuple[ReviewRecord, ...]
```

Reviews are already sorted and unique by `review_ref`. Review count never upgrades
provenance, truth, self-attribution or authority. `UNKNOWN`, `DERIVED` and
`PARTIALLY_CORRELATED` reviews do not count as independent convergence.

### 5.7 ScopeBoundary

```python
@dataclass(frozen=True, slots=True)
class ScopeBoundary:
    applies_to: tuple[str, ...]
    may_support: tuple[str, ...]
    does_not_establish: tuple[str, ...]
    unknowns: tuple[str, ...]
    transfer_limits: tuple[str, ...]
```

All tuples are caller-supplied canonical sorted unique values. A non-empty
`unknowns` tuple produces `DEFER`. The classifier does not invent or remove scope.

### 5.8 AuthorityExclusions

The readiness model explicitly records that an attributed interpretation does not
establish higher authority. The exact runtime value object is:

```python
@dataclass(frozen=True, slots=True)
class AuthorityExclusions:
    factual_truth_proof: bool
    identity_authority: bool
    relationship_authority: bool
    consent_authority: bool
    capability_authority: bool
    action_gate_authority: bool
    retrieval_authority: bool
    tool_execution_authority: bool
    m3_nomination_or_write: bool
```

For a positive result **all nine values must be `False`**. A `True` value is not
accepted as authority; it means the proposed use contradicts the Non-Projection
authority ceiling and contributes a deterministic `REJECT` threat:

```text
factual_truth_proof                         → NPG-T03
identity_authority or m3_nomination_or_write→ NPG-T10
relationship_authority                      → NPG-T09
consent_authority                           → NPG-T12
capability/action/retrieval/tool authority  → NPG-T02
```

### 5.9 ProjectionIntent — exact T01…T12 binding

The pure classifier does not infer intent from prose. The exact caller-supplied
proposed-use contract is:

```python
@dataclass(frozen=True, slots=True)
class ProjectionIntent:
    adopt_as_self_experience: bool
    inherit_source_authority: bool
    assert_as_objective_truth: bool
    adopt_source_emotion_as_drive: bool
    style_changes_evidence_status: bool
    generalize_beyond_scope: bool
    count_correlated_reviews_as_independent: bool
    discard_relevant_context: bool
    inherit_relationship_or_commitment: bool
    promote_to_stable_identity_trait: bool
    present_interpretation_as_direct_testimony: bool
    inherit_consent: bool
```

The mapping is exact and one-to-one:

```text
adopt_as_self_experience                   → NPG-T01
inherit_source_authority                   → NPG-T02
assert_as_objective_truth                  → NPG-T03
adopt_source_emotion_as_drive              → NPG-T04
style_changes_evidence_status              → NPG-T05
generalize_beyond_scope                    → NPG-T06
count_correlated_reviews_as_independent    → NPG-T07
discard_relevant_context                   → NPG-T08
inherit_relationship_or_commitment         → NPG-T09
promote_to_stable_identity_trait           → NPG-T10
present_interpretation_as_direct_testimony → NPG-T11
inherit_consent                            → NPG-T12
```

Any `True` field is a verified blocker for this proposed use and contributes
`REJECT`. The classifier makes no claim that false values prove a caller's hidden
intent; it classifies only the explicit proposal supplied to it.

### 5.10 AttributedInterpretationEnvelope

```python
@dataclass(frozen=True, slots=True)
class AttributedInterpretationEnvelope:
    envelope_version: str
    source_provenance: SourceProvenance
    attribution: Attribution
    claim: Claim
    interpretation: Interpretation
    contextual_distance: ContextualDistance
    review_provenance: ReviewProvenance
    scope: ScopeBoundary
    authority_exclusions: AuthorityExclusions
    projection_intent: ProjectionIntent
```

No raw source body, model prompt, generated narrative, credential, callable,
storage locator or mutable external object is part of the envelope.

---

## 6. 📏 Exact deterministic budget

NPG-v0.1 defines one local resource budget:

```python
@dataclass(frozen=True, slots=True)
class NonProjectionBudget:
    max_string_bytes: int
    max_tuple_items: int
    max_review_records: int
    max_canonical_input_bytes: int
```

All four values are positive integers; booleans are invalid integers.

Budget meaning:

- every non-null input string encoded as UTF-8 is bounded by
  `max_string_bytes`;
- every input tuple is bounded by `max_tuple_items`;
- `review_provenance.reviews` is additionally bounded by
  `max_review_records`;
- the final domain-separated canonical input projection is bounded by
  `max_canonical_input_bytes`.

The classifier may not truncate, reorder, summarize or discard content to fit a
budget. A syntactically valid over-budget input contributes:

```text
DEFER · BUDGET_EXHAUSTED
```

If a verified projection blocker is also present, global precedence keeps the
final decision `REJECT` while `BUDGET_EXHAUSTED` remains a secondary reason.

---

## 7. ✅ Exact admission invariants

Malformed contract input raises `NonProjectionContractError`. It does not return
any ordinary decision and cannot be used as positive evidence.

Before classification:

1. `envelope` is exactly `AttributedInterpretationEnvelope` and `budget` is
   exactly `NonProjectionBudget`;
2. all nested values are exact frozen contract types, not duck-typed mappings;
3. required strings are non-empty, unpadded Unicode scalar text;
4. optional refs are `None` or non-empty unpadded Unicode scalar text;
5. every tuple of strings is already lexicographically sorted and unique;
6. reviews are already sorted and unique by `review_ref`;
7. enum fields are exact enum members; raw strings are not silently coerced;
8. boolean fields are exact booleans;
9. budget integers are positive `int` values and not `bool`;
10. `InterpretationState.CONTESTED` requires at least two alternatives;
11. `SubjectRelation.NON_SELF` or `UNKNOWN` requires `self_basis_ref is None`;
12. the envelope has no extension mapping or unknown runtime fields;
13. no hidden trimming, sorting, aliasing, case folding, translation or semantic
    normalization is allowed.

Examples of forbidden normalization:

```text
"creator-1" ≠ " creator-1 "
"FACTUAL" raw string ≠ ClaimClass.FACTUAL
"source-a" ≠ semantic alias "source A"
reordered caller tuples ≠ silently repaired tuples
```

An unsupported but syntactically valid `envelope_version` is not malformed. It
contributes `DEFER · ENVELOPE_VERSION_UNVERIFIED`.

---

## 8. 🧬 Canonical input fingerprint

A fingerprint is derived audit evidence only. It is never permission and is
never accepted as classifier input.

The classifier constructs exactly this domain-separated value:

```text
domain                         = MENTAURY_NPG_INPUT_V1
non_projection_contract_version= NPG-v0.1
envelope_version               = envelope.envelope_version
canonical_profile              = MENTAURY_CANONICAL_JSON_V1
source_provenance_scope        = CALLER_SUPPLIED_ATTRIBUTED_VALUES_ONLY
envelope                       = envelope.to_value()
budget                         = budget.to_value()
```

Normative algorithm:

```text
strict contract admission
→ deterministic structural budget accounting
→ construct exact input value
→ canonical_json_bytes(...)
→ enforce max_canonical_input_bytes
→ hashlib.sha256(bytes).hexdigest()
```

When present, `input_fingerprint` is lowercase 64-character SHA-256 hex.

The projection excludes:

```text
ambient time / clock
environment variables
filesystem / database / network state
Atlas state
identity / relationship registry state
P1-001 / P1-002 / P1-003 results
Character state
M2 / M3 state
model/provider state
unrelated reviewer or source state
```

If canonicalization fails after successful admission, the result contributes:

```text
DEFER · CANONICALIZATION_FAILED
```

No caller-supplied digest can override unequal canonical values.

---

## 9. 🚨 Exact threat and reject-reason mapping

A later implementation must define these exact threat IDs and reject reasons:

| Threat ID | Exact primary reason | Trigger |
|---|---|---|
| `NPG-T01` | `AUTOBIOGRAPHY_LAUNDERING` | `adopt_as_self_experience` |
| `NPG-T02` | `AUTHORITY_INHERITANCE` | `inherit_source_authority` or prohibited capability/action/retrieval/tool authority claim |
| `NPG-T03` | `TRUTH_ESCALATION` | `assert_as_objective_truth` or `factual_truth_proof` claim |
| `NPG-T04` | `EMOTION_TO_DRIVE_PROJECTION` | `adopt_source_emotion_as_drive` |
| `NPG-T05` | `STYLE_TO_BELIEF_PROJECTION` | `style_changes_evidence_status` |
| `NPG-T06` | `HISTORICAL_LAW_PROJECTION` | `generalize_beyond_scope` |
| `NPG-T07` | `CORRELATED_CONSENSUS_LAUNDERING` | `count_correlated_reviews_as_independent` |
| `NPG-T08` | `CONTEXT_COLLAPSE` | `discard_relevant_context` |
| `NPG-T09` | `RELATIONSHIP_PROJECTION` | `inherit_relationship_or_commitment` or `relationship_authority` claim |
| `NPG-T10` | `IDENTITY_TRAIT_PROJECTION` | `promote_to_stable_identity_trait` or identity/M3 authority claim |
| `NPG-T11` | `INTERPRETATION_LAUNDERING` | `present_interpretation_as_direct_testimony` |
| `NPG-T12` | `CONSENT_INHERITANCE` | `inherit_consent` or `consent_authority` claim |

Multiple threats are preserved. They are ordered numerically by threat ID and
are never reduced by source prestige, reviewer count or presentation style.

---

## 10. 🚦 Exact reason vocabulary and precedence

A later implementation must define this exact primary/secondary reason vocabulary:

```text
PASS_ATTRIBUTED

CONTEXT_SCOPE_REPAIR_REQUIRED

PROVENANCE_CONFLICTING
INTERPRETATION_CONTESTED

ENVELOPE_VERSION_UNVERIFIED
BUDGET_EXHAUSTED
CANONICALIZATION_FAILED
SOURCE_CLASS_UNKNOWN
SOURCE_ORIGIN_UNKNOWN
PROVENANCE_UNKNOWN
PROVENANCE_MATERIAL_GAP
SUBJECT_RELATION_UNKNOWN
SELF_BASIS_UNVERIFIED
INTERPRETATION_UNKNOWN
CONTEXT_UNKNOWN
SCOPE_UNKNOWN

AUTOBIOGRAPHY_LAUNDERING
AUTHORITY_INHERITANCE
TRUTH_ESCALATION
EMOTION_TO_DRIVE_PROJECTION
STYLE_TO_BELIEF_PROJECTION
HISTORICAL_LAW_PROJECTION
CORRELATED_CONSENSUS_LAUNDERING
CONTEXT_COLLAPSE
RELATIONSHIP_PROJECTION
IDENTITY_TRAIT_PROJECTION
INTERPRETATION_LAUNDERING
CONSENT_INHERITANCE
```

Decision severity is frozen as:

```text
REJECT > DEFER > CONTESTED > REVISE_REQUIRED > PASS_ATTRIBUTED
```

Within the selected severity, the primary reason order is frozen:

```text
REJECT:
NPG-T01 → NPG-T02 → ... → NPG-T12

DEFER:
ENVELOPE_VERSION_UNVERIFIED
→ BUDGET_EXHAUSTED
→ CANONICALIZATION_FAILED
→ SOURCE_CLASS_UNKNOWN
→ SOURCE_ORIGIN_UNKNOWN
→ PROVENANCE_UNKNOWN
→ PROVENANCE_MATERIAL_GAP
→ SUBJECT_RELATION_UNKNOWN
→ SELF_BASIS_UNVERIFIED
→ INTERPRETATION_UNKNOWN
→ CONTEXT_UNKNOWN
→ SCOPE_UNKNOWN

CONTESTED:
PROVENANCE_CONFLICTING
→ INTERPRETATION_CONTESTED

REVISE_REQUIRED:
CONTEXT_SCOPE_REPAIR_REQUIRED

PASS_ATTRIBUTED:
PASS_ATTRIBUTED
```

`reasons` preserves all detected reasons in deterministic severity/order. A
stronger reason does not erase weaker diagnostic evidence.

---

## 11. ⚙️ Exact deterministic evaluation rules

After strict admission, the classifier derives all applicable reason sets from
the explicit values and then applies the frozen precedence.

### 11.1 REJECT conditions

A reject reason is collected for every `True` `ProjectionIntent` field according
to the NPG-T01…T12 mapping. Contradictory `AuthorityExclusions=True` fields add
the mapped NPG-T02/T03/T09/T10/T12 reject reason.

A verified reject dominates all lower-severity missing/conflicting/repair states.

### 11.2 DEFER conditions

With or without lower-severity conditions, collect deterministic defer reasons:

```text
envelope_version != AIE-v0.1                       → ENVELOPE_VERSION_UNVERIFIED
any structural/canonical budget exceeded            → BUDGET_EXHAUSTED
canonical_json_bytes fails after admission           → CANONICALIZATION_FAILED
source_class == UNKNOWN_SOURCE                       → SOURCE_CLASS_UNKNOWN
source_origin == UNKNOWN                             → SOURCE_ORIGIN_UNKNOWN
provenance_state == UNKNOWN                          → PROVENANCE_UNKNOWN
provenance_state == PARTIAL and material_gaps != ()  → PROVENANCE_MATERIAL_GAP
subject_relation == UNKNOWN                          → SUBJECT_RELATION_UNKNOWN
subject_relation == VERIFIED_SELF                    → SELF_BASIS_UNVERIFIED
interpretation.state == UNKNOWN                      → INTERPRETATION_UNKNOWN
any context distance == UNKNOWN or anachronism UNKNOWN→ CONTEXT_UNKNOWN
scope.unknowns != ()                                 → SCOPE_UNKNOWN
```

`VERIFIED_SELF` is deliberately deferred because this contract owns no identity
binder. No source prestige or caller instruction can bypass that rule.

### 11.3 CONTESTED conditions

When no higher-severity result applies:

```text
provenance_state == CONFLICTING        → PROVENANCE_CONFLICTING
interpretation.state == CONTESTED      → INTERPRETATION_CONTESTED
```

Material conflict is preserved; the classifier does not choose a preferred
narrative merely because one source is more famous or more confidently worded.

### 11.4 REVISE_REQUIRED condition

When no higher-severity result applies, collect
`CONTEXT_SCOPE_REPAIR_REQUIRED` if `scope.transfer_limits == ()` and at least
one of these holds:

```text
source_class == HISTORICAL_PRIMARY
source_class == HISTORICAL_SECONDARY
any ContextDistanceLevel == HIGH
anachronism_risk == HIGH
```

This freezes the repairable historical/context-transfer behavior required by
`NPG-SC-008` without turning an incomplete transfer rule into a positive result.

### 11.5 PASS_ATTRIBUTED

Only when no reject, defer, contested or revise reason exists may the classifier
return:

```text
PASS_ATTRIBUTED · PASS_ATTRIBUTED
```

No uncertain/missing/conflicting state maps positive.

---

## 12. 📤 Exact result contract

```python
@dataclass(frozen=True, slots=True)
class NonProjectionResult:
    decision: NonProjectionDecision
    primary_reason: NonProjectionReason
    reasons: tuple[NonProjectionReason, ...]
    triggered_threat_ids: tuple[NonProjectionThreatId, ...]
    input_fingerprint: str | None
    contract_version: str = "NPG-v0.1"
    envelope_version: str = "AIE-v0.1"
    canonical_profile: str = "MENTAURY_CANONICAL_JSON_V1"
    source_provenance_scope: str = "CALLER_SUPPLIED_ATTRIBUTED_VALUES_ONLY"
```

Positive construction invariant:

```text
PASS_ATTRIBUTED decision
↔ primary_reason == PASS_ATTRIBUTED
↔ reasons == (PASS_ATTRIBUTED,)
↔ triggered_threat_ids == ()
↔ input_fingerprint is present
↔ envelope version verified
↔ canonical profile verified
↔ no higher-severity reason exists
```

A result contains no source body, credential, callable, tool handle, capability,
storage locator, mutation command, identity proof or reusable authority object.

A previous `NonProjectionResult` or fingerprint is never accepted back as
permission. A separately authorized audit system may store it only as provenance.

---

## 13. 🧪 Frozen readiness scenario binding

The later implementation must preserve these exact scenario outcomes:

| ID | Required outcome |
|---|---|
| `NPG-SC-001` | explicitly attributed Creator autobiography, no projection intent → `PASS_ATTRIBUTED` |
| `NPG-SC-002` | scoped historical normative position, transfer limits preserved → `PASS_ATTRIBUTED` |
| `NPG-SC-003` | correlated reviews claimed independent → `REJECT · CORRELATED_CONSENSUS_LAUNDERING` |
| `NPG-SC-004` | metaphor proposed as factual mechanism → `REJECT · TRUTH_ESCALATION` |
| `NPG-SC-005` | source trauma/ambition proposed as Mentaury drive → `REJECT · EMOTION_TO_DRIVE_PROJECTION` |
| `NPG-SC-006` | non-self material proposed as Mentaury's own experience → `REJECT · AUTOBIOGRAPHY_LAUNDERING` |
| `NPG-SC-007` | prestigious source retained only as attributed testimony despite stronger contrary evidence → `PASS_ATTRIBUTED` |
| `NPG-SC-008` | historical advice lacks transfer limits → `REVISE_REQUIRED · CONTEXT_SCOPE_REPAIR_REQUIRED` |
| `NPG-SC-009` | predecessor/fork relationship asserted current → `REJECT · RELATIONSHIP_PROJECTION` |
| `NPG-SC-010` | Character style proposed to alter evidence/gate status → `REJECT · STYLE_TO_BELIEF_PROJECTION` |
| `NPG-SC-011` | materially unknown source identity/provenance → `DEFER` with exact unknown reason |
| `NPG-SC-012` | attributed material/result proposed as Action/retrieval/tool authority → `REJECT · AUTHORITY_INHERITANCE` |
| `NPG-SC-013` | credible A + credible B + unresolved material interpretation conflict → `CONTESTED · INTERPRETATION_CONTESTED` |

`NPG-SC-013` is the required executable contested-conflict case added by the
readiness contract; it does not replace or renumber NPG-SC-001…012.

---

## 14. 🔁 Frozen metamorphic bindings

A later implementation must make every readiness property executable:

```text
MT-NPG-001 Attribution preservation
presentation-only metadata change cannot change source/speaker/subject attribution

MT-NPG-002 Prestige non-escalation
source fame/status change alone cannot improve decision or authority

MT-NPG-003 Repetition non-escalation
duplicate/correlated review evidence cannot improve independence or decision

MT-NPG-004 Context monotonicity
removing required provenance/context/scope evidence cannot make decision more permissive

MT-NPG-005 Self/non-self invalidation
source/subject identity substitution requires a new fingerprint/evaluation and cannot retain prior self relation

MT-NPG-006 No M3 amplification
interpretation/voice metadata changes never create M3 authority

MT-NPG-007 No relationship amplification
narrative similarity/shared-history changes never create relationship/commitment/consent authority

MT-NPG-008 Determinism
same exact admitted envelope + budget + contract version → same decision/reasons/threats/fingerprint
```

---

## 15. 🧪 Mandatory later implementation test matrix

All IDs below are normative. One test may prove more than one property, but every
ID must be represented explicitly in executable test metadata/name/parameter ID.

### 15.1 Context / contract — NPC-CTX-001…018

```text
NPC-CTX-001 exact valid NON_SELF envelope accepted
NPC-CTX-002 unsupported syntactically valid envelope version defers
NPC-CTX-003 empty required string rejected as contract error
NPC-CTX-004 padded required/optional string rejected
NPC-CTX-005 unsorted tuple rejected
NPC-CTX-006 duplicate tuple item rejected
NPC-CTX-007 unsorted review records rejected
NPC-CTX-008 duplicate review_ref rejected
NPC-CTX-009 raw enum string / wrong nested type rejected
NPC-CTX-010 invalid bool/int budget typing rejected
NPC-CTX-011 zero/negative budget rejected
NPC-CTX-012 CONTESTED interpretation with fewer than two alternatives rejected
NPC-CTX-013 NON_SELF/UNKNOWN with self_basis_ref rejected
NPC-CTX-014 frozen envelope mutation rejected
NPC-CTX-015 public API rejects raw text/model/retriever/backend/repository args
NPC-CTX-016 public API rejects prior result/fingerprint args
NPC-CTX-017 VERIFIED_SELF cannot produce PASS_ATTRIBUTED
NPC-CTX-018 no hidden trim/sort/alias/semantic normalization
```

### 15.2 Canonical fingerprint — NPC-FP-001…008

```text
NPC-FP-001 exact canonical input fixture
NPC-FP-002 exact SHA-256 input fingerprint fixture
NPC-FP-003 relevant envelope mutation changes fingerprint
NPC-FP-004 budget mutation changes fingerprint
NPC-FP-005 exact repeated input reproduces fingerprint
NPC-FP-006 caller cannot inject contract/profile/domain/fingerprint
NPC-FP-007 fingerprint projection excludes ambient/Atlas/identity/relationship/P1/Character/M3 state
NPC-FP-008 canonicalization failure never maps positive
```

### 15.3 Decision / precedence — NPC-DEC-001…014

```text
NPC-DEC-001 clean attributed proposal → PASS_ATTRIBUTED
NPC-DEC-002 projection blocker + otherwise clean → REJECT
NPC-DEC-003 projection blocker dominates DEFER
NPC-DEC-004 projection blocker dominates CONTESTED
NPC-DEC-005 unknown source/provenance → DEFER
NPC-DEC-006 partial provenance + material gap → DEFER
NPC-DEC-007 partial provenance + no material gap may remain positive
NPC-DEC-008 VERIFIED_SELF → DEFER/SELF_BASIS_UNVERIFIED
NPC-DEC-009 conflicting provenance → CONTESTED
NPC-DEC-010 contested interpretation → CONTESTED
NPC-DEC-011 historical/high-distance missing transfer limits → REVISE_REQUIRED
NPC-DEC-012 valid over-budget input → DEFER/BUDGET_EXHAUSTED without truncation
NPC-DEC-013 contradictory authority exclusion claim → REJECT
NPC-DEC-014 reason and threat ordering is deterministic
```

### 15.4 Projection threats — NPC-T-001…012

```text
NPC-T-001 ↔ NPG-T01 Autobiography laundering
NPC-T-002 ↔ NPG-T02 Authority inheritance
NPC-T-003 ↔ NPG-T03 Truth escalation
NPC-T-004 ↔ NPG-T04 Emotion-to-drive projection
NPC-T-005 ↔ NPG-T05 Style-to-belief projection
NPC-T-006 ↔ NPG-T06 Historical-law projection
NPC-T-007 ↔ NPG-T07 Correlated-consensus laundering
NPC-T-008 ↔ NPG-T08 Context collapse
NPC-T-009 ↔ NPG-T09 Relationship projection
NPC-T-010 ↔ NPG-T10 Identity-trait projection
NPC-T-011 ↔ NPG-T11 Interpretation laundering
NPC-T-012 ↔ NPG-T12 Consent inheritance
```

Each threat test must be executable; prose-only satisfaction is forbidden.

### 15.5 Frozen scenarios — NPC-SC-001…013

```text
NPC-SC-001 ↔ NPG-SC-001 exact outcome
NPC-SC-002 ↔ NPG-SC-002 exact outcome
NPC-SC-003 ↔ NPG-SC-003 exact outcome
NPC-SC-004 ↔ NPG-SC-004 exact outcome
NPC-SC-005 ↔ NPG-SC-005 exact outcome
NPC-SC-006 ↔ NPG-SC-006 exact outcome
NPC-SC-007 ↔ NPG-SC-007 exact outcome
NPC-SC-008 ↔ NPG-SC-008 exact outcome
NPC-SC-009 ↔ NPG-SC-009 exact outcome
NPC-SC-010 ↔ NPG-SC-010 exact outcome
NPC-SC-011 ↔ NPG-SC-011 exact outcome
NPC-SC-012 ↔ NPG-SC-012 exact outcome
NPC-SC-013 ↔ required contested-conflict case
```

### 15.6 Metamorphic — NPC-M-001…008

```text
NPC-M-001 ↔ MT-NPG-001
NPC-M-002 ↔ MT-NPG-002
NPC-M-003 ↔ MT-NPG-003
NPC-M-004 ↔ MT-NPG-004
NPC-M-005 ↔ MT-NPG-005
NPC-M-006 ↔ MT-NPG-006
NPC-M-007 ↔ MT-NPG-007
NPC-M-008 ↔ MT-NPG-008
```

### 15.7 Purity / hidden authority — NPC-PURE-001…008

```text
NPC-PURE-001 fresh-process import has no ambient filesystem/database/network use
NPC-PURE-002 classifier call has no ambient filesystem/database/network use
NPC-PURE-003 import/call has no ambient clock access
NPC-PURE-004 import/call has no environment-variable authority
NPC-PURE-005 import/call performs no model/LLM/retrieval invocation
NPC-PURE-006 no event/replay/belief/identity/relationship/M2/M3 mutation or persistence
NPC-PURE-007 no tool execution, subprocess or dynamic plugin loading
NPC-PURE-008 exact repeat is deterministic and result exposes no capability/credential/callable material
```

All existing repository tests remain green unchanged. Tests may not be weakened
or rewritten merely to admit the future classifier.

---

## 16. 🚫 No-hidden-I/O proof strategy

A later implementation must demonstrate import-time and call-time purity.

Required proof:

1. import the bounded package in a fresh interpreter with sentinel hooks that
   fail on filesystem access attributable to the package, database connections,
   socket/network clients, subprocesses, environment reads, ambient clock calls,
   model clients and retrieval clients;
2. call `classify_non_projection` using complete in-memory typed fixtures under
   the same sentinels;
3. verify no persistence, event append, replay/projection, belief, identity,
   relationship, M2/M3, Character, Action Gate or tool module is invoked;
4. verify the result depends only on explicit `envelope`, explicit `budget` and
   frozen local constants;
5. inspect imports to verify no dynamic plugin loading or service/backend adapters
   exist in the bounded package.

Allowed implementation dependencies are limited to deterministic standard-library
value/hash helpers plus the existing `mentaury.contracts.canonical_json` module.
The bounded classifier must not call P1-001, P1-002 or P1-003.

---

## 17. 🧱 Compatibility / non-modification rule

The future NPG-v0.1 implementation must not require semantic or result-shape
changes to:

```text
P1-001 Capability Lease Resolution
P1-002 Privacy Reconciliation Classifier
P1-003 Pure Governed Constraint Composer
MENTAURY_CANONICAL_JSON_V1
MENTAURY_CANON_V0.1
```

Non-Projection remains a separate bounded classifier and is **not** implicitly
inserted into P1-003.

```text
P1_003_ELIGIBLE_FOR_NEXT_GATE
+ PASS_ATTRIBUTED
≠ Action Gate PASS
```

Any future composition of P1-003 and Non-Projection results requires a new
explicit cross-gate binding/authority decision.

Character remains downstream only:

```text
Non-Projection result
→ then Character presentation

Character presentation
→ cannot alter provenance, evidence, threat set, reasons or decision
```

If implementation discovers that any frozen P1/Canon semantics must change, the
implementation attempt must STOP and return to a separate docs-only architecture
decision. Such a change cannot be smuggled into implementation.

---

## 18. 🚫 Explicit non-goals and forbidden surface

NPG-v0.1 does not authorize or implement:

```text
raw-text semantic judging
source ingestion or crawling
Creator Atlas retrieval/runtime
Human Paths Atlas retrieval/runtime
filesystem/database/network/vector/graph access
model/LLM invocation
retrieval execution
identity/continuation binder or registry lookup
relationship/commitment/consent runtime
M2 persistence/promotion
M3 nomination/write/promotion
belief mutation
P1-001/P1-002/P1-003 modification
cross-gate composition with P1-003
Action Gate
Tool Receipt runtime
tool execution
subprocess execution
dynamic plugin loading
Character runtime activation
backend selection/migration
worker/background service
runtime deployment/production enablement
factual-truth proof
consciousness/personhood claims
```

`PASS_ATTRIBUTED` remains bounded classification evidence only.

---

## 19. ⛔ Compatibility stop

Stop before implementation or Owner GO if the frozen classifier would require:

- hidden retrieval, persistence, model calls or ambient I/O;
- free-text semantic inference inside the pure classifier;
- changing P1-001/P1-002/P1-003 or Canon semantics;
- accepting caller assertion as current identity authority;
- allowing source prestige/reviewer count to upgrade truth or authority;
- allowing Character Policy to override the classification;
- current relationship/commitment/consent inheritance from source lineage;
- direct or indirect M2/M3 write/promotion;
- `PASS_ATTRIBUTED` becoming Action/retrieval/tool/execution authority;
- weakening any NPG-T01…T12, NPG-SC-001…012 or MT-NPG-001…008 invariant;
- changing this contract's exact API, result precedence or threat mapping inside
  an implementation PR without a preceding docs-only contract revision.

Required response:

```text
STOP_CURRENT_PROMOTION
→ new docs-only compatibility/contract decision
→ review
→ explicit Owner decision if authority changes
```

---

## 20. ✅ Later implementation acceptance criteria

A later implementation may be called `IMPLEMENTED_BOUNDED` only if all are true:

```text
separate explicit Non-Projection Owner GO exists and matches this exact contract
implementation branch starts from freshly verified current main
only reserved NPG package/tests/bounded docs are changed
P1-001/P1-002/P1-003/Canon semantics remain unchanged
all NPC-CTX-001…018 pass
all NPC-FP-001…008 pass
all NPC-DEC-001…014 pass
all NPC-T-001…012 / NPG-T01…T12 pass
all NPC-SC-001…013 / NPG-SC requirements pass
all NPC-M-001…008 / MT-NPG-001…008 pass
all NPC-PURE-001…008 pass
all existing repository tests remain green unchanged
no-hidden-I/O/model/retrieval proof passes
complete final diff inspected
exact-head required CI green
branch up to date with main
zero unresolved review threads
Tier A correctness PASS
Tier A adversarial PASS
authorization boundary PRESERVED
explicit maintainer merge decision recorded
protected merge uses unchanged reviewed head
resulting-main required CI green
Notion sync only after resulting-main evidence
```

Green tests are insufficient if the diff expands authority beyond this contract.

---

## 21. 🔐 Authorization stop

After this docs-only contract is merged and resulting-main CI is green, the exact
state remains:

```text
NON_PROJECTION_GATE_CONTRACT_READINESS = READY
NON_PROJECTION_CANDIDATE_SELECTION     = SELECTED
NON_PROJECTION_CANDIDATE               = PURE_NON_PROJECTION_CLASSIFIER
NON_PROJECTION_IMPLEMENTATION_CONTRACT = FROZEN_DOCS
P1_004                                 = NOT_ASSIGNED
NON_PROJECTION_OWNER_GO                = NOT_GRANTED
IMPLEMENTATION_AUTHORIZATION           = NONE
NON_PROJECTION_IMPLEMENTATION          = NOT_STARTED · NOT_AUTHORIZED
NON_PROJECTION_RUNTIME                 = NOT_AUTHORIZED
ACTION_GATE                            = NOT_AUTHORIZED
RETRIEVAL_EXECUTION                    = NOT_AUTHORIZED
TOOL_EXECUTION                         = NOT_AUTHORIZED
IDENTITY_RUNTIME                       = NOT_AUTHORIZED
RELATIONSHIP_RUNTIME                   = NOT_AUTHORIZED
DIRECT_OR_INDIRECT_M3_WRITE            = FORBIDDEN
RUNTIME_DEPLOYMENT                     = NOT_AUTHORIZED
CHARACTER_RUNTIME_ACTIVATION_GATE      = BLOCKED_PENDING_REQUIRED_VALIDATION
```

The next possible authority step is only a **separate explicit Owner GO decision**
against this exact frozen contract.

```text
NON_PROJECTION_IMPLEMENTATION_CONTRACT_FROZEN_DOCS_ONLY
→ STOP
→ separate explicit Owner GO decision
→ only if GO: clean Tier A bounded implementation milestone
```

No wording in this document constitutes that GO.

---

## 22. 🏁 Final formula

```text
P1-003 IMPLEMENTED_BOUNDED
+ Non-Projection Gate Contract Readiness READY
+ ATTRIBUTED_INTERPRETATION_ENVELOPE readiness semantics frozen
+ PURE_NON_PROJECTION_CLASSIFIER candidate SELECTED
+ exact NPG-v0.1 pure classifier implementation contract FROZEN_DOCS

→ design is sufficiently specified for a later separate Owner authorization decision

≠ P1-004 assigned
≠ Owner GO
≠ implementation authorization
≠ runtime implementation/activation
≠ raw-text semantic judge
≠ model/retrieval/persistence/I/O authority
≠ Action Gate / tool authority
≠ identity / relationship / consent / M2 / M3 authority
≠ Character activation
≠ deployment authority
```
