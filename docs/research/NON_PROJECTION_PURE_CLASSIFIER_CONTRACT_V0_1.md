# 🪞 Pure Non-Projection Classifier — Frozen Implementation Contract v0.1

```text
Status:                              FROZEN_DOCS · DOCS_ONLY · IMPLEMENTATION_CONTRACT
Contract version:                    NPG-v0.1
Envelope version:                    AIE-v0.1
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
> This is the reconciled authoritative contract for the selected
> `PURE_NON_PROJECTION_CLASSIFIER`. It freezes one pure deterministic component
> only. It does not assign P1-004, authorize code, retrieve source material,
> establish truth/identity/relationship/consent, mutate M2/M3, invoke Action
> Gate/tools, activate Character runtime, persist data or deploy anything.

---

## 1. 🎯 Bounded purpose and semantic ceiling

The future component answers one bounded question:

> Given one immutable caller-supplied Attributed Interpretation Envelope, one
> explicit proposed use, and one explicit local budget, does that proposal contain
> a projection/authority-laundering blocker, missing evidence, material conflict,
> repairable context/scope defect, or no bounded projection blocker?

The classifier does not read free text to infer hidden intent and does not fetch
or discover source material. It evaluates only admitted typed values.

The strongest positive result is exactly:

```text
PASS_ATTRIBUTED
```

Its ceiling is immutable:

```text
PASS_ATTRIBUTED
= at most no bounded Non-Projection blocker found for this exact admitted proposal

PASS_ATTRIBUTED
≠ factual truth proof
≠ Mentaury autobiography
≠ identity claim or stable M3 trait
≠ relationship / commitment / consent authority
≠ capability
≠ Action Gate PASS
≠ retrieval permission
≠ tool / execution permission
≠ deployment permission
```

---

## 2. 🔒 Frozen constants and hard caps

A later implementation must expose these exact semantic constants:

```text
NON_PROJECTION_CONTRACT_VERSION            = "NPG-v0.1"
ATTRIBUTED_INTERPRETATION_ENVELOPE_VERSION = "AIE-v0.1"
CANONICAL_PROFILE                          = "MENTAURY_CANONICAL_JSON_V1"
INPUT_FINGERPRINT_DOMAIN                   = "MENTAURY_NPG_INPUT_V1"
SOURCE_PROVENANCE_SCOPE                    = "CALLER_SUPPLIED_ATTRIBUTED_VALUES_ONLY"

HARD_MAX_STRING_BYTES                      = 4096
HARD_MAX_TUPLE_ITEMS                       = 512
HARD_MAX_REVIEW_RECORDS                    = 64
HARD_MAX_CANONICAL_INPUT_BYTES             = 262144
```

Canonicalization must reuse
`mentaury.contracts.canonical_json.canonical_json_bytes` and verify live
`PROFILE_NAME == "MENTAURY_CANONICAL_JSON_V1"` before a positive result.

The caller may not override contract version, canonical profile, fingerprint
domain, provenance-scope label or hard caps and may not supply a fingerprint.

A syntactically valid unsupported `envelope_version` is not silently adapted. It
fails closed as:

```text
DEFER · ENVELOPE_VERSION_UNVERIFIED
```

---

## 3. 📦 Reserved package and exact public API

If and only if a later separate Owner GO authorizes implementation, the bounded
package is reserved as:

```text
src/mentaury/non_projection/__init__.py
src/mentaury/non_projection/contracts.py
src/mentaury/non_projection/classifier.py
```

No service, adapter, registry, worker, transport, persistence backend, model
client, retriever or plugin belongs to NPG-v0.1.

The exact public function is:

```python
def classify_non_projection(
    *,
    envelope: AttributedInterpretationEnvelope,
    budget: NonProjectionBudget,
) -> NonProjectionResult:
    ...
```

Forbidden public inputs include:

```text
raw source text
callback / clock provider / environment
repository or backend object
model / LLM client
retriever / Atlas handle
tool handle
identity or relationship registry/state
prior NonProjectionResult
caller-supplied fingerprint
```

The API never discovers authority-critical values itself.

---

## 4. 🧬 Frozen enum vocabulary

A later implementation must use exact `StrEnum` members semantically equivalent
to the following. Raw strings are never silently coerced.

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

### 4.2 Attribution, claims and interpretation

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

InterpretationState:
SUPPORTED
CONTESTED
UNKNOWN
```

### 4.3 Context and reviewer provenance

```text
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
never GitHub governance review and never means `INDEPENDENT_HUMAN_REVIEW = YES`.

### 4.4 Result vocabulary

```text
NonProjectionDecision:
PASS_ATTRIBUTED
REVISE_REQUIRED
CONTESTED
DEFER
REJECT
```

Global precedence is exactly:

```text
REJECT
> DEFER
> CONTESTED
> REVISE_REQUIRED
> PASS_ATTRIBUTED
```

---

## 5. 📦 Exact immutable input contracts

All runtime value objects below are `@dataclass(frozen=True, slots=True)` and
expose deterministic `to_value()` projections made only from canonical JSON
scalar/list/object values. No extension dictionary or dynamic metadata bag is
permitted.

```python
@dataclass(frozen=True, slots=True)
class SourceProvenance:
    source_ref: str
    source_actor_ref: str | None
    source_class: SourceClass
    source_origin: SourceOrigin
    provenance_state: ProvenanceState
    publication_or_capture_context_ref: str | None
    sensitivity: Sensitivity
    usage_boundary_ref: str
    material_gaps: tuple[str, ...]

@dataclass(frozen=True, slots=True)
class Attribution:
    speaker_ref: str
    subject_ref: str
    subject_relation: SubjectRelation
    self_basis_ref: str | None
    attribution_basis_refs: tuple[str, ...]

@dataclass(frozen=True, slots=True)
class Claim:
    claim_id: str
    claim_class: ClaimClass
    statement_ref: str
    directly_stated: bool

@dataclass(frozen=True, slots=True)
class Interpretation:
    interpretation_ref: str | None
    interpreter_ref: str | None
    state: InterpretationState
    alternatives: tuple[str, ...]
    disconfirming_refs: tuple[str, ...]

@dataclass(frozen=True, slots=True)
class ContextualDistance:
    historical: ContextDistanceLevel
    cultural: ContextDistanceLevel
    terminology: ContextDistanceLevel
    translation_or_paraphrase: ContextDistanceLevel
    source_distance: ContextDistanceLevel
    anachronism_risk: AnachronismRisk

@dataclass(frozen=True, slots=True)
class ReviewRecord:
    review_ref: str
    reviewer_ref: str
    independence: ReviewerIndependence
    provider_ref: str | None
    prompt_family_ref: str | None
    context_snapshot_ref: str | None
    saw_prior_output: bool

@dataclass(frozen=True, slots=True)
class ReviewProvenance:
    reviews: tuple[ReviewRecord, ...]

@dataclass(frozen=True, slots=True)
class ScopeBoundary:
    applies_to: tuple[str, ...]
    may_support: tuple[str, ...]
    does_not_establish: tuple[str, ...]
    unknowns: tuple[str, ...]
    transfer_limits: tuple[str, ...]

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

@dataclass(frozen=True, slots=True)
class ProjectionIntent:
    proposed_applies_to: tuple[str, ...]
    adopt_as_self_experience: bool
    inherit_source_authority: bool
    assert_as_objective_truth: bool
    adopt_source_emotion_as_drive: bool
    style_changes_evidence_status: bool
    generalize_beyond_scope: bool
    claimed_independent_review_count: int
    discard_relevant_context: bool
    inherit_relationship_or_commitment: bool
    promote_to_stable_identity_trait: bool
    present_interpretation_as_direct_testimony: bool
    inherit_consent: bool

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

### 5.1 `AuthorityExclusions` exact meaning

The field name is retained from readiness. Each boolean is an **attempted
establishment assertion**:

```text
False = this attributed material is explicitly not being treated as establishing that authority
True  = proposed use attempts to treat it as establishing that authority
```

`PASS_ATTRIBUTED` requires all nine values to be `False`. `True` never grants the
named authority; it triggers the corresponding projection threat.

---

## 6. 📏 Exact local budget and hard-cap behavior

```python
@dataclass(frozen=True, slots=True)
class NonProjectionBudget:
    max_string_bytes: int
    max_tuple_items: int
    max_review_records: int
    max_canonical_input_bytes: int
```

Rules:

- every value is a positive `int`; booleans are invalid integers;
- each local limit must be `<=` its corresponding hard cap;
- a local budget above a hard cap is malformed contract input;
- values structurally exceeding a hard cap are malformed contract input;
- a valid input inside hard caps but exceeding the caller local budget returns
  `DEFER · BUDGET_EXHAUSTED`;
- no value is truncated, sampled, reordered, summarized or discarded to fit.

Budget accounting covers every non-null UTF-8 string, every tuple,
`review_provenance.reviews`, and the final canonical input projection.

**Normative distinction:** hard caps are admission constraints; caller local
limits are classification constraints. Therefore:

```text
hard-cap overflow   → NonProjectionContractError
local-budget overflow while still inside hard caps → DEFER · BUDGET_EXHAUSTED
```

---

## 7. ✅ Strict admission and malformed-input policy

Malformed contract input raises exactly:

```python
class NonProjectionContractError(ValueError):
    ...
```

A contract error returns no ordinary classification and is never authorization
evidence.

Admission rules:

1. `envelope` and `budget` are exact frozen contract types;
2. all nested values are exact contract types, not duck-typed mappings;
3. required strings are non-empty and unpadded;
4. optional refs are `None` or non-empty unpadded strings;
5. every string reference is valid UTF-8 and inside **hard caps**; exceeding a
   caller local limit while remaining inside hard caps is admitted and later
   classified as `DEFER · BUDGET_EXHAUSTED`;
6. every tuple of strings is already lexicographically sorted and unique;
7. reviews are already sorted and unique by `review_ref`;
8. enums are exact members; raw strings are not coerced;
9. booleans are exact `bool`;
10. budget integers are positive `int`, not `bool`, and the budget limits
    themselves are within hard caps;
11. `claimed_independent_review_count` is a non-negative `int`, not `bool`;
12. `projection_intent.proposed_applies_to` is non-empty, sorted and unique;
13. `NON_SELF` or `UNKNOWN` requires `self_basis_ref is None`;
14. `VERIFIED_SELF` requires non-null `self_basis_ref` structurally but remains
    semantically unsupported in NPG-v0.1;
15. `InterpretationState.CONTESTED` requires at least two distinct alternatives
    and at least one `disconfirming_ref`;
16. the envelope has no extension mapping or unknown runtime fields;
17. hard caps are checked before expensive canonical work;
18. no hidden trimming, sorting, aliasing, case folding, translation or semantic
    normalization is allowed.

Examples:

```text
"creator-1" ≠ " creator-1 "
"FACTUAL" raw string ≠ ClaimClass.FACTUAL
"source-a" ≠ semantic alias "source A"
reordered tuples ≠ silently repaired tuples
```

Unsupported but structurally valid `envelope_version` contributes
`ENVELOPE_VERSION_UNVERIFIED`; it is not automatically a contract exception.

---

## 8. 👤 Self/non-self exact behavior

NPG-v0.1 intentionally owns no identity/continuation binder.

```text
NON_SELF      → eligible for bounded evaluation
UNKNOWN       → DEFER · SUBJECT_RELATION_UNKNOWN
VERIFIED_SELF → DEFER · SELF_BASIS_UNVERIFIED
```

Even a present `self_basis_ref` cannot create identity authority. A future
identity/continuation binding requires a separate selected/frozen/authorized
contract before `VERIFIED_SELF` can ever become positively evaluable here.

```text
caller says "this is you"   ≠ VERIFIED_SELF authority
creator status               ≠ VERIFIED_SELF authority
same narrative voice         ≠ VERIFIED_SELF authority
same model/provider          ≠ VERIFIED_SELF authority
shared project lineage       ≠ VERIFIED_SELF authority
pre-fork shared history      ≠ current-branch VERIFIED_SELF authority
```

---

## 9. 🔗 Exact reviewer-correlation and independence accounting

The classifier computes `effective_independent_review_count`; it does not trust a
caller count as proof.

A `ReviewRecord` contributes exactly one independent review only when all are
true:

```text
independence == INDEPENDENT
saw_prior_output == False
provider_ref is not None
prompt_family_ref is not None
context_snapshot_ref is not None
reviewer_ref occurs exactly once
provider_ref occurs exactly once among non-null provider refs
prompt_family_ref occurs exactly once among non-null prompt-family refs
context_snapshot_ref occurs exactly once among non-null context-snapshot refs
```

Every `PARTIALLY_CORRELATED`, `DERIVED` or `UNKNOWN` record contributes zero.
Any shared reviewer/provider/prompt-family/context-snapshot identifier makes every
record in that shared correlation group contribute zero independent convergence.
Missing correlation metadata also contributes zero.

This directly preserves frozen readiness semantics:

```text
same provider/model only  ≠ independent convergence
same prompt family        ≠ independent convergence
same context snapshot     ≠ independent convergence
saw prior output          ≠ blind independent review
repeated derived reviews  ≠ additional independent evidence
```

`NPG-T07` triggers when:

```text
projection_intent.claimed_independent_review_count
> effective_independent_review_count
```

Reviewer independence here remains epistemic metadata only, never GitHub human
review status.

---

## 10. 📐 Exact context and scope behavior

Any unknown contextual dimension fails closed:

```text
any ContextDistanceLevel == UNKNOWN
or anachronism_risk == UNKNOWN
→ DEFER · CONTEXT_UNKNOWN
```

Scope rules:

```text
projection_intent.proposed_applies_to ⊆ scope.applies_to
```

If false, `NPG-T06` triggers. If any proposed scope entry appears in
`scope.unknowns`, add `DEFER · SCOPE_UNKNOWN` unless a higher-precedence reject
also exists.

Historical/context transfer repair is exact:

```text
scope.transfer_limits == ()
and any of:
  source_class == HISTORICAL_PRIMARY
  source_class == HISTORICAL_SECONDARY
  any ContextDistanceLevel == HIGH
  anachronism_risk == HIGH
→ REVISE_REQUIRED · CONTEXT_SCOPE_REPAIR_REQUIRED
```

Deliberate context discard is stronger:

```text
projection_intent.discard_relevant_context == True
→ NPG-T08 · REJECT
```

Removing relevant context or scope evidence can never make the result more
permissive.

---

## 11. 🛡️ Exact NPG-T01…NPG-T12 executable mapping

The full threat set is derived from admitted values. Multiple threats are
preserved in ascending threat-ID order.

```text
NPG-T01 Autobiography laundering
  projection_intent.adopt_as_self_experience == True

NPG-T02 Authority inheritance
  projection_intent.inherit_source_authority == True
  OR any capability/action/retrieval/tool authority boolean == True

NPG-T03 Truth escalation
  projection_intent.assert_as_objective_truth == True
  OR authority_exclusions.factual_truth_proof == True

NPG-T04 Emotion-to-drive projection
  projection_intent.adopt_source_emotion_as_drive == True

NPG-T05 Style-to-belief projection
  projection_intent.style_changes_evidence_status == True

NPG-T06 Historical-law / scope projection
  projection_intent.generalize_beyond_scope == True
  OR proposed_applies_to is not a subset of scope.applies_to

NPG-T07 Correlated-consensus laundering
  claimed_independent_review_count > effective_independent_review_count

NPG-T08 Context collapse
  projection_intent.discard_relevant_context == True

NPG-T09 Relationship projection
  projection_intent.inherit_relationship_or_commitment == True
  OR authority_exclusions.relationship_authority == True

NPG-T10 Identity-trait projection
  projection_intent.promote_to_stable_identity_trait == True
  OR authority_exclusions.identity_authority == True
  OR authority_exclusions.m3_nomination_or_write == True

NPG-T11 Interpretation laundering
  projection_intent.present_interpretation_as_direct_testimony == True

NPG-T12 Consent inheritance
  projection_intent.inherit_consent == True
  OR authority_exclusions.consent_authority == True
```

The primary reject reason is the lowest triggered threat ID. Source prestige,
review count or Character style can never reduce the threat set.

---

## 12. 🚦 Exact reason vocabulary and precedence

A later implementation must define exact `NonProjectionReason` values equivalent
to:

```text
PASS_ATTRIBUTED

ATTRIBUTION_REPAIR_REQUIRED
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

Decision severity is exactly:

```text
REJECT > DEFER > CONTESTED > REVISE_REQUIRED > PASS_ATTRIBUTED
```

Primary reason order within a severity is:

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
PROVENANCE_CONFLICTING → INTERPRETATION_CONTESTED

REVISE_REQUIRED:
ATTRIBUTION_REPAIR_REQUIRED → CONTEXT_SCOPE_REPAIR_REQUIRED

PASS_ATTRIBUTED:
PASS_ATTRIBUTED
```

`reasons` preserves all detected reasons in deterministic severity/order. Stronger
reasons do not erase weaker diagnostic evidence.

---

## 13. ⚙️ Exact deterministic evaluation rules

After strict admission:

1. compute structural complexity and effective reviewer independence;
2. derive all NPG-T01…12 reject threats;
3. derive all defer conditions;
4. derive contested conditions;
5. derive revise conditions;
6. canonicalize and fingerprint the admitted input;
7. add local-budget/canonicalization defer reasons if applicable;
8. select highest-severity decision;
9. deterministically order complete reasons/threats;
10. construct immutable result.

### 13.1 DEFER rules

```text
envelope_version != AIE-v0.1                       → ENVELOPE_VERSION_UNVERIFIED
local input complexity exceeds budget               → BUDGET_EXHAUSTED
canonical_json_bytes fails after admission           → CANONICALIZATION_FAILED
source_class == UNKNOWN_SOURCE                       → SOURCE_CLASS_UNKNOWN
source_origin == UNKNOWN                             → SOURCE_ORIGIN_UNKNOWN
provenance_state == UNKNOWN                          → PROVENANCE_UNKNOWN
provenance_state == PARTIAL and material_gaps != ()  → PROVENANCE_MATERIAL_GAP
subject_relation == UNKNOWN                          → SUBJECT_RELATION_UNKNOWN
subject_relation == VERIFIED_SELF                    → SELF_BASIS_UNVERIFIED
interpretation.state == UNKNOWN                      → INTERPRETATION_UNKNOWN
any context dimension/risk == UNKNOWN                → CONTEXT_UNKNOWN
proposed scope intersects scope.unknowns             → SCOPE_UNKNOWN
```

`PARTIAL` provenance with `material_gaps == ()` is not automatically deferred;
this preserves readiness's rule that partial provenance may remain usable when
missing provenance is immaterial to this bounded question.

### 13.2 CONTESTED rules

```text
provenance_state == CONFLICTING   → PROVENANCE_CONFLICTING
interpretation.state == CONTESTED → INTERPRETATION_CONTESTED
```

### 13.3 REVISE_REQUIRED rules

```text
claim_class in {
  AUTOBIOGRAPHICAL_TESTIMONY,
  RELATIONSHIP_TESTIMONY,
  CONSENT_STATEMENT
}
and source_actor_ref is None
→ ATTRIBUTION_REPAIR_REQUIRED

historical/high-distance transfer rule from section 10
→ CONTEXT_SCOPE_REPAIR_REQUIRED
```

### 13.4 PASS rule

`PASS_ATTRIBUTED` requires:

- no triggered threat;
- no defer reason;
- no contested reason;
- no revise reason;
- all authority-establishment booleans `False`;
- proposed scope within admitted scope;
- envelope version and canonical profile verified;
- input fingerprint successfully derived.

---

## 14. 📤 Exact immutable result contract

```python
@dataclass(frozen=True, slots=True)
class NonProjectionResult:
    decision: NonProjectionDecision
    primary_reason: NonProjectionReason
    reasons: tuple[NonProjectionReason, ...]
    triggered_threat_ids: tuple[NonProjectionThreatId, ...]
    effective_independent_review_count: int
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

The result contains no raw source body, credential, callable, tool handle,
capability, storage locator, mutation command, identity proof, relationship state
or reusable permission.

---

## 15. 🧬 Exact canonical input fingerprint

The fingerprint is derived audit evidence only and is never accepted as input or
permission.

The classifier canonicalizes exactly this domain-separated value:

```text
domain                          = MENTAURY_NPG_INPUT_V1
non_projection_contract_version = NPG-v0.1
envelope_version                = envelope.envelope_version
canonical_profile               = MENTAURY_CANONICAL_JSON_V1
source_provenance_scope         = CALLER_SUPPLIED_ATTRIBUTED_VALUES_ONLY
envelope                        = envelope.to_value()
budget                          = budget.to_value()
```

Normative algorithm:

```text
strict admission
→ hard-cap checks
→ deterministic local-budget accounting
→ construct exact canonical value
→ canonical_json_bytes(...)
→ enforce hard/local canonical byte bounds
→ hashlib.sha256(bytes).hexdigest()
```

When present, `input_fingerprint` is lowercase 64-character SHA-256 hex.

The projection excludes ambient clock/time, environment variables, filesystem,
database/network/vector/graph state, Atlas state, identity/relationship registry
state, P1 results, Character state, M2/M3 state, model/provider ambient state and
unrelated external records.

---

## 16. 🧪 Frozen readiness scenario binding

The later implementation must preserve these exact readiness outcomes:

| ID | Required outcome |
|---|---|
| `NPG-SC-001` | explicitly attributed Creator autobiography, no projection intent → `PASS_ATTRIBUTED` |
| `NPG-SC-002` | scoped historical normative position with transfer limits → `PASS_ATTRIBUTED` |
| `NPG-SC-003` | claimed independent review count exceeds effective independent count → `REJECT · CORRELATED_CONSENSUS_LAUNDERING` |
| `NPG-SC-004` | metaphor proposed as objective factual mechanism → `REJECT · TRUTH_ESCALATION` |
| `NPG-SC-005` | source trauma/ambition proposed as Mentaury drive → `REJECT · EMOTION_TO_DRIVE_PROJECTION` |
| `NPG-SC-006` | non-self material proposed as Mentaury's own experience → `REJECT · AUTOBIOGRAPHY_LAUNDERING` |
| `NPG-SC-007` | prestigious source retained only as attributed testimony despite stronger contrary evidence → `PASS_ATTRIBUTED` |
| `NPG-SC-008` | historical advice lacks transfer limits, without deliberate context discard → `REVISE_REQUIRED · CONTEXT_SCOPE_REPAIR_REQUIRED` |
| `NPG-SC-009` | predecessor/fork relationship asserted current → `REJECT · RELATIONSHIP_PROJECTION` |
| `NPG-SC-010` | Character style proposed to alter evidence/gate status → `REJECT · STYLE_TO_BELIEF_PROJECTION` |
| `NPG-SC-011` | materially unknown source identity/provenance → `DEFER · PROVENANCE_UNKNOWN` |
| `NPG-SC-012` | attributed material/result proposed as Action/retrieval/tool authority → `REJECT · AUTHORITY_INHERITANCE` |

Required contested fixture remains separate from the frozen `001…012` family:

```text
NPG-SC-CONTESTED-001
provenance_state = VERIFIED
interpretation.state = CONTESTED
alternatives has at least two distinct entries
disconfirming_refs is non-empty
no higher-precedence reject/defer
→ CONTESTED · INTERPRETATION_CONTESTED
```

No `NPG-SC-013` is created by this contract.

---

## 17. 🔁 Frozen metamorphic bindings

```text
MT-NPG-001 Attribution preservation
presentation-only change cannot change source/speaker/subject attribution

MT-NPG-002 Prestige non-escalation
source fame/status change alone cannot improve truth/self/relationship/authority

MT-NPG-003 Repetition non-escalation
repeated/correlated reviews cannot improve effective independence

MT-NPG-004 Context monotonicity
removing required provenance/context/scope evidence cannot make result more permissive

MT-NPG-005 Self/non-self invalidation
source/subject identity substitution requires new evaluation; VERIFIED_SELF still defers in v0.1

MT-NPG-006 No M3 amplification
interpretation/voice changes never create M3 authority

MT-NPG-007 No relationship amplification
narrative similarity/shared-history changes never create relationship/consent authority

MT-NPG-008 Determinism
same exact admitted envelope + budget + NPG-v0.1 → same decision/reasons/threats/count/fingerprint
```

---

## 18. 🧪 Mandatory later implementation test matrix

Every ID below is normative and must be represented explicitly in executable test
metadata/name/parameter IDs.

### 18.1 Admission / contract — `NPC-CTX-001…022`

```text
NPC-CTX-001 valid NON_SELF envelope accepted
NPC-CTX-002 unsupported valid envelope version defers
NPC-CTX-003 empty required string contract-error
NPC-CTX-004 padded required/optional ref contract-error
NPC-CTX-005 unsorted tuple contract-error
NPC-CTX-006 duplicate tuple item contract-error
NPC-CTX-007 unsorted reviews contract-error
NPC-CTX-008 duplicate review_ref contract-error
NPC-CTX-009 raw enum/wrong nested type contract-error
NPC-CTX-010 invalid bool/int typing contract-error
NPC-CTX-011 zero/negative budget contract-error
NPC-CTX-012 local budget above hard cap contract-error
NPC-CTX-013 input value above hard cap contract-error
NPC-CTX-014 CONTESTED with <2 alternatives contract-error
NPC-CTX-015 CONTESTED with empty disconfirming refs contract-error
NPC-CTX-016 NON_SELF/UNKNOWN with self_basis_ref contract-error
NPC-CTX-017 VERIFIED_SELF without self_basis_ref contract-error
NPC-CTX-018 frozen envelope mutation rejected
NPC-CTX-019 public API rejects raw text/model/retriever/backend/repository args
NPC-CTX-020 public API rejects prior result/fingerprint args
NPC-CTX-021 VERIFIED_SELF cannot produce PASS_ATTRIBUTED
NPC-CTX-022 no hidden trim/sort/alias/semantic normalization
```

### 18.2 Canonical fingerprint — `NPC-FP-001…008`

```text
NPC-FP-001 exact canonical input fixture
NPC-FP-002 exact SHA-256 input fingerprint fixture
NPC-FP-003 relevant envelope mutation changes fingerprint
NPC-FP-004 budget mutation changes fingerprint
NPC-FP-005 exact repeated input reproduces fingerprint
NPC-FP-006 caller cannot inject contract/profile/domain/fingerprint
NPC-FP-007 fingerprint excludes ambient/Atlas/identity/relationship/P1/Character/M3 state
NPC-FP-008 canonicalization failure never maps positive
```

### 18.3 Decisions / precedence — `NPC-DEC-001…016`

```text
NPC-DEC-001 clean attributed proposal → PASS_ATTRIBUTED
NPC-DEC-002 projection blocker → REJECT
NPC-DEC-003 REJECT dominates DEFER
NPC-DEC-004 REJECT dominates CONTESTED
NPC-DEC-005 DEFER dominates CONTESTED
NPC-DEC-006 CONTESTED dominates REVISE_REQUIRED
NPC-DEC-007 unknown source/provenance → DEFER
NPC-DEC-008 partial provenance + material gap → DEFER
NPC-DEC-009 partial provenance + no material gap may remain positive
NPC-DEC-010 VERIFIED_SELF → DEFER/SELF_BASIS_UNVERIFIED
NPC-DEC-011 conflicting provenance → CONTESTED
NPC-DEC-012 contested interpretation → CONTESTED
NPC-DEC-013 historical/high-distance missing transfer limits → REVISE_REQUIRED
NPC-DEC-014 valid local over-budget input → DEFER without truncation
NPC-DEC-015 testimony missing source actor → REVISE_REQUIRED
NPC-DEC-016 reason/threat ordering deterministic
```

### 18.4 Threats — `NPC-T-001…012`

`NPC-T-001…012` map one-to-one to `NPG-T01…12` and each fixture triggers its
intended threat without unrelated threat inputs.

### 18.5 Frozen scenarios

```text
NPC-SC-001…NPC-SC-012 ↔ NPG-SC-001…NPG-SC-012 exact outcomes
NPC-SC-CONTESTED-001 ↔ NPG-SC-CONTESTED-001 exact outcome
```

### 18.6 Metamorphic — `NPC-M-001…008`

`NPC-M-001…008` map one-to-one to `MT-NPG-001…008`.

### 18.7 Purity / hidden authority — `NPC-PURE-001…010`

```text
NPC-PURE-001 fresh-process import has no ambient filesystem/database/network use
NPC-PURE-002 classifier call has no ambient filesystem/database/network use
NPC-PURE-003 no vector/graph/Atlas retrieval
NPC-PURE-004 no ambient clock/random dependency
NPC-PURE-005 no environment-variable authority
NPC-PURE-006 no model/LLM invocation
NPC-PURE-007 no persistence/event/replay/belief/identity/relationship/M2/M3 mutation
NPC-PURE-008 no Action Gate/capability/tool/subprocess/dynamic-plugin invocation
NPC-PURE-009 package imports only deterministic stdlib + canonical_json dependency
NPC-PURE-010 exact repeat deterministic and result exposes no authority object
```

All existing repository tests remain green unchanged. Existing tests may not be
weakened merely to admit the future classifier.

---

## 19. 🚫 No-hidden-I/O proof strategy

A later implementation must prove import-time and call-time purity using fresh
processes/sentinels where practical:

1. fail on package-attributable filesystem/database/socket/network/subprocess use;
2. fail on ambient clock/random/environment reads;
3. fail on model/LLM/retrieval/Atlas clients;
4. fail on persistence/event/replay/belief/identity/relationship/M2/M3 mutation;
5. fail on Action Gate/capability/tool/plugin invocation;
6. verify result depends only on `envelope`, `budget` and frozen constants;
7. inspect imports for absence of adapters/backends/services/dynamic plugins.

Allowed dependencies are deterministic standard-library value/hash helpers plus
the existing `mentaury.contracts.canonical_json`. The classifier must not invoke
P1-001, P1-002 or P1-003.

---

## 20. 🧱 Character, P1 and Canon compatibility

This contract changes none of:

```text
P1-001 contract = unchanged
P1-002 contract = unchanged
P1-003 contract = unchanged
MENTAURY_CANONICAL_JSON_V1 = unchanged
MENTAURY_CANON_V0.1 = unchanged
```

Non-Projection remains separate and is not an implicit P1-003 input.

```text
P1_003_ELIGIBLE_FOR_NEXT_GATE
+ PASS_ATTRIBUTED
≠ Action Gate PASS
```

Any future composition of P1-003 and Non-Projection needs a separate explicit
cross-gate binding/authority decision.

Character remains downstream:

```text
Non-Projection result
→ then Character presentation

Character presentation
→ cannot alter provenance
→ cannot alter reviewer-independence accounting
→ cannot alter threat set
→ cannot alter reasons or decision
```

---

## 21. 🚫 Explicit non-goals and forbidden surface

NPG-v0.1 does not authorize or implement:

```text
raw-text semantic judging
source ingestion/crawling
Creator Atlas or Human Paths Atlas runtime/retrieval
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
Tool Receipt runtime or tool execution
subprocess/dynamic plugin loading
Character runtime activation
backend selection/migration
worker/background service
runtime deployment/production enablement
factual-truth proof
consciousness/personhood claims
P1-004 assignment
```

---

## 22. ⛔ Compatibility stop

Stop before Owner GO or implementation if implementation would require:

- changing NPG-T01…12, NPG-SC-001…12 or MT-NPG-001…008 semantics;
- changing this exact package/API/schema/result/reason/budget/fingerprint contract;
- making `VERIFIED_SELF` positive without a separately frozen identity binding;
- hidden retrieval, persistence, model or ambient I/O;
- free-text semantic inference inside the classifier;
- source prestige/reviewer quantity upgrading truth or authority;
- Character changing evidence/result;
- relationship/commitment/consent inheritance;
- direct/indirect M2/M3 write;
- changing P1-001/P1-002/P1-003 or Canon;
- `PASS_ATTRIBUTED` becoming Action/retrieval/tool/execution authority;
- deployment/runtime activation.

Required response:

```text
STOP_CURRENT_PROMOTION
→ new docs-only compatibility/contract decision
→ Tier A review
→ explicit Owner decision if authority changes
```

---

## 23. ✅ Later implementation acceptance criteria

A future implementation may become `IMPLEMENTED_BOUNDED` only if:

```text
separate explicit Non-Projection Owner GO matches this exact NPG-v0.1 contract
fresh implementation branch starts from freshly verified current main
only reserved NPG package/tests/bounded docs change
P1-001/P1-002/P1-003/Canon semantics remain unchanged
all NPC-CTX-001…022 pass
all NPC-FP-001…008 pass
all NPC-DEC-001…016 pass
all NPC-T-001…012 / NPG-T01…12 pass
all NPC-SC-001…012 and NPC-SC-CONTESTED-001 pass
all NPC-M-001…008 / MT-NPG-001…008 pass
all NPC-PURE-001…010 pass
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

Green tests never override semantic authority boundaries.

---

## 24. 🔐 Authorization stop after this freeze

After this docs-only contract is merged and resulting-main CI is green, the exact
state remains:

```text
NON_PROJECTION_GATE_CONTRACT_READINESS = READY
NON_PROJECTION_CANDIDATE_SELECTION     = SELECTED
NON_PROJECTION_CANDIDATE               = PURE_NON_PROJECTION_CLASSIFIER
NON_PROJECTION_IMPLEMENTATION_CONTRACT = FROZEN_DOCS
NON_PROJECTION_CONTRACT_VERSION        = NPG-v0.1
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

The next possible authority step is only a **separate explicit Owner GO decision**.

```text
NON_PROJECTION_IMPLEMENTATION_CONTRACT_FROZEN_DOCS_ONLY
→ STOP
→ separate explicit Owner GO decision
→ only if GO: clean Tier A bounded implementation milestone
```

No wording in this document constitutes that GO.

---

## 25. 🏁 Final formula

```text
P1-003 IMPLEMENTED_BOUNDED
+ Non-Projection readiness READY
+ ATTRIBUTED_INTERPRETATION_ENVELOPE semantics frozen
+ PURE_NON_PROJECTION_CLASSIFIER selected
+ reconciled exact NPG-v0.1 implementation contract FROZEN_DOCS

→ design is specified for a later separate Owner authorization decision

≠ P1-004 assigned
≠ Owner GO
≠ implementation authorization
≠ implementation/runtime activation
≠ factual truth proof
≠ identity / relationship / consent / M2 / M3 authority
≠ Action Gate / retrieval / tool authority
≠ Character activation
≠ deployment authority
```
