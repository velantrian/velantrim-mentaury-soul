# 🪞 Pure Non-Projection Classifier — Frozen Implementation Contract

```text
Status:                              FROZEN_DOCS · DOCS_ONLY · IMPLEMENTATION_CONTRACT
Version:                             0.1
Date:                                2026-08-10
Review tier:                         TIER_A
Owning readiness:                    NON_PROJECTION_GATE_CONTRACT_READINESS.md
Owning candidate selection:          NON_PROJECTION_GATE_CANDIDATE_SELECTION.md
Selected candidate:                  PURE_NON_PROJECTION_CLASSIFIER
Contract version:                    NPG-v0.1
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
Deployment authority:                NONE
```

> **CONTRACT FROZEN ≠ OWNER GO.**
>
> **THIS DOCUMENT DOES NOT AUTHORIZE IMPLEMENTATION.**
>
> It freezes the exact bounded implementation contract that a later separately
> authorized implementation would have to satisfy. It does not assign P1-004,
> create runtime authority, activate retrieval, persist data, call a model,
> establish identity/relationship/consent, mutate M2/M3, invoke Action Gate or
> tools, or deploy anything.

---

## 1. 🎯 Bounded purpose

The future component answers one question only:

> Given one immutable, explicitly supplied attributed interpretation envelope and
> one immutable local evaluation budget, does the proposed use preserve source,
> subject, claim, context, reviewer-correlation, scope and authority boundaries
> strongly enough to return the frozen Non-Projection classification?

The strongest positive result is exactly:

```text
PASS_ATTRIBUTED
```

Its semantic ceiling remains:

```text
PASS_ATTRIBUTED
= at most no bounded projection blocker found for this exact admitted envelope

PASS_ATTRIBUTED
≠ factual truth proof
≠ Mentaury autobiography
≠ identity claim
≠ stable M3 trait
≠ relationship / commitment / consent authority
≠ capability
≠ Action Gate PASS
≠ retrieval permission
≠ tool / execution permission
≠ deployment permission
```

The classifier evaluates supplied values. It does not discover, retrieve,
interpret with an LLM, persist, believe, execute or adopt anything.

---

## 2. 🔒 Frozen versions, canonical domains and hard caps

A later implementation must expose these exact semantic constants:

```text
NON_PROJECTION_CONTRACT_VERSION              = "NPG-v0.1"
ATTRIBUTED_INTERPRETATION_ENVELOPE_VERSION   = "AIE-v0.1"
CANONICAL_PROFILE                            = "MENTAURY_CANONICAL_JSON_V1"
ENVELOPE_FINGERPRINT_DOMAIN                  = "MENTAURY_NPG_ENVELOPE_V1"
CLASSIFICATION_FINGERPRINT_DOMAIN            = "MENTAURY_NPG_CLASSIFICATION_V1"

HARD_MAX_ENVELOPE_BYTES                      = 262144
HARD_MAX_REVIEW_RECORDS                      = 64
HARD_MAX_SCOPE_ENTRIES                       = 128
HARD_MAX_REFERENCE_COUNT                     = 512
MAX_REFERENCE_UTF8_BYTES                     = 4096
```

Canonical JSON must reuse the repository's existing
`mentaury.contracts.canonical_json` profile. No second canonicalizer is permitted.

Caller values may not override the contract version, canonical profile,
fingerprint domains or hard caps. Unsupported envelope versions fail closed.

---

## 3. 📦 Reserved package and exact public API

If and only if a later explicit Owner GO authorizes implementation, the bounded
package is reserved as:

```text
src/mentaury/non_projection/__init__.py
src/mentaury/non_projection/contracts.py
src/mentaury/non_projection/classifier.py
```

No adapter, registry, repository, service, worker, transport, persistence,
retrieval, model, identity, relationship, Action Gate or backend module belongs
inside `NPG-v0.1`.

The exact public function is frozen as:

```python
def classify_non_projection(
    *,
    envelope: AttributedInterpretationEnvelope,
    budget: NonProjectionBudget,
) -> NonProjectionResult:
    ...
```

The function accepts no raw source text, callback, clock, repository/service
object, model handle, retriever, tool handle, database handle, identity registry,
relationship registry, persistence handle, environment object or caller-supplied
fingerprint.

```text
classify_non_projection(raw_text=...)          = FORBIDDEN API
classify_non_projection(model=...)             = FORBIDDEN API
classify_non_projection(retriever=...)         = FORBIDDEN API
classify_non_projection(identity_registry=...) = FORBIDDEN API
classify_non_projection(tool=...)              = FORBIDDEN API
caller fingerprint                             = FORBIDDEN API
```

---

## 4. 🧬 Exact immutable vocabulary

A later implementation must use semantically exact `StrEnum` values equivalent
to the following.

### 4.1 Source and provenance

```python
class SourceClass(StrEnum):
    CREATOR_TESTIMONY = "CREATOR_TESTIMONY"
    CURRENT_USER_TESTIMONY = "CURRENT_USER_TESTIMONY"
    HISTORICAL_PRIMARY = "HISTORICAL_PRIMARY"
    HISTORICAL_SECONDARY = "HISTORICAL_SECONDARY"
    LITERARY_OR_METAPHORICAL = "LITERARY_OR_METAPHORICAL"
    RESEARCH_PRIMARY = "RESEARCH_PRIMARY"
    RESEARCH_SECONDARY = "RESEARCH_SECONDARY"
    MODEL_INTERPRETATION = "MODEL_INTERPRETATION"
    REVIEW_OUTPUT = "REVIEW_OUTPUT"
    UNKNOWN_SOURCE = "UNKNOWN_SOURCE"

class SourceOrigin(StrEnum):
    PRIMARY = "PRIMARY"
    SECONDARY = "SECONDARY"
    DERIVED = "DERIVED"
    UNKNOWN = "UNKNOWN"

class ProvenanceState(StrEnum):
    VERIFIED = "VERIFIED"
    PARTIAL = "PARTIAL"
    UNKNOWN = "UNKNOWN"
    CONFLICTING = "CONFLICTING"

class Sensitivity(StrEnum):
    NORMAL = "NORMAL"
    SENSITIVE = "SENSITIVE"
    HIGH = "HIGH"
    UNKNOWN = "UNKNOWN"
```

### 4.2 Attribution and claim

```python
class SubjectRelation(StrEnum):
    VERIFIED_SELF = "VERIFIED_SELF"
    NON_SELF = "NON_SELF"
    UNKNOWN = "UNKNOWN"

class ClaimClass(StrEnum):
    FACTUAL = "FACTUAL"
    CAUSAL = "CAUSAL"
    PREDICTIVE = "PREDICTIVE"
    NORMATIVE = "NORMATIVE"
    VALUE = "VALUE"
    AUTOBIOGRAPHICAL_TESTIMONY = "AUTOBIOGRAPHICAL_TESTIMONY"
    RELATIONSHIP_TESTIMONY = "RELATIONSHIP_TESTIMONY"
    CONSENT_STATEMENT = "CONSENT_STATEMENT"
    INTERPRETIVE = "INTERPRETIVE"
    METAPHORICAL = "METAPHORICAL"
```

### 4.3 Context and review provenance

```python
class ContextDistance(StrEnum):
    NONE = "NONE"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    UNKNOWN = "UNKNOWN"

class AnachronismRisk(StrEnum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    UNKNOWN = "UNKNOWN"

class ReviewerIndependence(StrEnum):
    INDEPENDENT = "INDEPENDENT"
    PARTIALLY_CORRELATED = "PARTIALLY_CORRELATED"
    DERIVED = "DERIVED"
    UNKNOWN = "UNKNOWN"
```

### 4.4 Proposed truth use

```python
class ProposedTruthMode(StrEnum):
    ATTRIBUTED_ONLY = "ATTRIBUTED_ONLY"
    FACTUAL_CLAIM = "FACTUAL_CLAIM"
    UNIVERSAL_FACT = "UNIVERSAL_FACT"
```

### 4.5 Frozen decisions and threats

```python
class NonProjectionDecision(StrEnum):
    PASS_ATTRIBUTED = "PASS_ATTRIBUTED"
    REVISE_REQUIRED = "REVISE_REQUIRED"
    CONTESTED = "CONTESTED"
    DEFER = "DEFER"
    REJECT = "REJECT"

class ProjectionThreat(StrEnum):
    NPG_T01 = "NPG-T01"
    NPG_T02 = "NPG-T02"
    NPG_T03 = "NPG-T03"
    NPG_T04 = "NPG-T04"
    NPG_T05 = "NPG-T05"
    NPG_T06 = "NPG-T06"
    NPG_T07 = "NPG-T07"
    NPG_T08 = "NPG-T08"
    NPG_T09 = "NPG-T09"
    NPG_T10 = "NPG-T10"
    NPG_T11 = "NPG-T11"
    NPG_T12 = "NPG-T12"
```

---

## 5. 📦 Exact immutable input schema

Every contract value is a `@dataclass(frozen=True, slots=True)` value object.
There is no extension dictionary and no dynamic metadata bag.

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
    alternatives: tuple[str, ...]
    disconfirming_refs: tuple[str, ...]
    contested: bool

@dataclass(frozen=True, slots=True)
class ContextualDistance:
    historical: ContextDistance
    cultural: ContextDistance
    terminology: ContextDistance
    translation: ContextDistance
    source_distance: ContextDistance
    anachronism_risk: AnachronismRisk
    context_acknowledgement_refs: tuple[str, ...]

@dataclass(frozen=True, slots=True)
class ReviewRecord:
    review_ref: str
    reviewer_ref: str
    independence_class: ReviewerIndependence
    provider_ref: str
    prompt_family_ref: str
    context_snapshot_ref: str
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
class ProposedUse:
    truth_mode: ProposedTruthMode
    proposed_applies_to: tuple[str, ...]
    present_as_mentaury_autobiography: bool
    adopt_source_emotion_as_drive: bool
    character_override_evidence: bool
    generalize_beyond_scope: bool
    independent_consensus_claimed: bool
    claimed_independent_review_count: int
    context_collapsed: bool
    relationship_adoption: bool
    identity_trait_adoption: bool
    interpretation_as_direct_source: bool
    consent_transfer: bool

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
    proposed_use: ProposedUse
```

The concrete field names above are frozen for `NPG-v0.1`.

### 5.1 AuthorityExclusions meaning

For compatibility with readiness #82, each boolean is an **establishment
assertion**. `False` means the envelope explicitly does **not** establish that
authority. `True` means the caller is attempting to treat the material as
establishing that authority and therefore activates the mapped projection threat.

Positive `PASS_ATTRIBUTED` requires every `AuthorityExclusions` field to be
`False`.

---

## 6. 📏 Exact local budget

```python
@dataclass(frozen=True, slots=True)
class NonProjectionBudget:
    max_envelope_bytes: int
    max_review_records: int
    max_scope_entries: int
    max_reference_count: int
```

Rules:

- every value is a positive `int`; booleans are invalid integers;
- each value must be less than or equal to the corresponding hard cap;
- `max_envelope_bytes <= HARD_MAX_ENVELOPE_BYTES`;
- `max_review_records <= HARD_MAX_REVIEW_RECORDS`;
- `max_scope_entries <= HARD_MAX_SCOPE_ENTRIES`;
- `max_reference_count <= HARD_MAX_REFERENCE_COUNT`.

Hard-cap violation is a contract error. A structurally valid envelope inside hard
caps but above the caller-supplied local budget returns:

```text
DEFER · BUDGET_EXHAUSTED
```

No value may be truncated, sampled or dropped to obtain a more permissive result.

---

## 7. ✅ Strict admission and malformed-input policy

Malformed contract input raises exactly:

```python
class NonProjectionContractError(ValueError):
    ...
```

It does **not** return a classification. A contract error is not authorization
evidence.

Admission rules:

1. `envelope_version` must equal `AIE-v0.1` exactly;
2. all required `str` values are non-empty and unpadded;
3. every reference string is valid UTF-8 and at most `4096` UTF-8 bytes;
4. every tuple of string references is already sorted and unique;
5. `ReviewRecord` values are sorted by `review_ref` and `review_ref` is unique;
6. enum instances are exact declared enum members;
7. boolean fields are exact `bool` values;
8. `claimed_independent_review_count` is a non-negative `int`; booleans are invalid;
9. `independent_consensus_claimed == False` requires claimed count `0`;
10. `independent_consensus_claimed == True` requires claimed count `>= 1`;
11. `scope.applies_to` and `proposed_use.proposed_applies_to` are non-empty;
12. `self_basis_ref` is `None` unless `subject_relation == VERIFIED_SELF`;
13. `VERIFIED_SELF` requires non-`None` `self_basis_ref` structurally, but remains
    unsupported semantically in `NPG-v0.1` and therefore later evaluates `DEFER`;
14. `interpretation.contested == True` requires non-empty `alternatives` and
    non-empty `disconfirming_refs`;
15. autobiographical, relationship and consent testimony with a missing
    `source_actor_ref` is structurally admitted but later requires revision;
16. all values must stay within hard caps;
17. no hidden trimming, sorting, aliasing, case folding, semantic mapping or
    normalization is allowed.

```text
"creator:1" ≠ "CREATOR:1"
"scope-a"   ≠ "scope a"
"branch-x"  ≠ semantic similarity to another branch
```

---

## 8. 👤 Exact self-attribution behavior

`NPG-v0.1` intentionally contains **no identity/continuation binding**.

Therefore:

```text
NON_SELF      → eligible for bounded evaluation
UNKNOWN       → DEFER · SUBJECT_RELATION_UNKNOWN
VERIFIED_SELF → DEFER · SELF_EVIDENCE_BINDING_UNSUPPORTED
```

Even a structurally present `self_basis_ref` cannot create identity authority.
A future identity/continuation contract must be separately selected, frozen and
authorized before `VERIFIED_SELF` could become positively evaluable.

```text
caller says "this is you"     ≠ VERIFIED_SELF authority
creator authority              ≠ VERIFIED_SELF authority
same model/provider            ≠ VERIFIED_SELF authority
shared project lineage         ≠ VERIFIED_SELF authority
pre-fork shared history        ≠ current-branch VERIFIED_SELF authority
```

---

## 9. 🔗 Exact reviewer-correlation algorithm

Reviewer independence is epistemic provenance only; it never means GitHub
`INDEPENDENT_HUMAN_REVIEW = YES`.

A `ReviewRecord` counts toward `effective_independent_review_count` only when:

1. `independence_class == INDEPENDENT`;
2. `saw_prior_output == False`;
3. its `reviewer_ref` occurs in exactly one review record;
4. its `provider_ref` occurs in exactly one review record;
5. its `prompt_family_ref` occurs in exactly one review record;
6. its `context_snapshot_ref` occurs in exactly one review record.

Any `PARTIALLY_CORRELATED`, `DERIVED` or `UNKNOWN` record counts as zero independent
reviews. Any shared reviewer/provider/prompt-family/context-snapshot identifier
makes every record in that shared correlation group count as zero for independent
convergence.

If the caller claims independent consensus with a count greater than the computed
effective count, the classifier must trigger `NPG-T07`.

Repeated correlated evidence never becomes independent by quantity.

---

## 10. 📐 Exact context and scope behavior

Context is fail-closed.

```text
any ContextDistance == UNKNOWN
or anachronism_risk == UNKNOWN
→ DEFER · CONTEXT_DISTANCE_UNKNOWN
```

When any distance is `LOW`, `MEDIUM` or `HIGH`, or anachronism risk is `MEDIUM`
or `HIGH`, at least one `context_acknowledgement_ref` is required for a positive
result. Missing acknowledgement is repairable and therefore:

```text
→ REVISE_REQUIRED · CONTEXT_ACKNOWLEDGEMENT_REQUIRED
```

Deliberate `context_collapsed == True` is stronger and triggers `NPG-T08`.

Scope rules:

```text
proposed_applies_to ⊆ scope.applies_to
```

If this is false, or `generalize_beyond_scope == True`, trigger `NPG-T06`.
If any proposed scope entry is explicitly listed in `scope.unknowns`, return
`DEFER · SCOPE_UNRESOLVED` unless a higher-precedence rejection applies.

Removing context or scope evidence can never make a classification more
permissive.

---

## 11. 🛡️ Exact NPG-T01…NPG-T12 executable mapping

A later implementation must derive the threat set from the admitted values by
these exact conditions.

### `NPG-T01` — Autobiography laundering

Trigger when:

```text
proposed_use.present_as_mentaury_autobiography == True
```

### `NPG-T02` — Authority inheritance

Trigger when any of these are `True`:

```text
authority_exclusions.capability_authority
authority_exclusions.action_gate_authority
authority_exclusions.retrieval_authority
authority_exclusions.tool_execution_authority
```

### `NPG-T03` — Truth escalation

Trigger when any of:

```text
authority_exclusions.factual_truth_proof == True
proposed_use.truth_mode == UNIVERSAL_FACT
```

Also trigger when `truth_mode == FACTUAL_CLAIM` and the source claim class is any
of:

```text
NORMATIVE
VALUE
AUTOBIOGRAPHICAL_TESTIMONY
RELATIONSHIP_TESTIMONY
CONSENT_STATEMENT
INTERPRETIVE
METAPHORICAL
```

A factual research claim may remain a factual **attributed claim**; the
Non-Projection result still does not prove its truth.

### `NPG-T04` — Emotion-to-drive projection

Trigger when:

```text
proposed_use.adopt_source_emotion_as_drive == True
```

### `NPG-T05` — Style-to-belief projection

Trigger when:

```text
proposed_use.character_override_evidence == True
```

### `NPG-T06` — Historical-law / scope projection

Trigger when:

```text
proposed_use.generalize_beyond_scope == True
or proposed_applies_to is not a subset of scope.applies_to
```

### `NPG-T07` — Correlated-consensus laundering

Trigger when:

```text
independent_consensus_claimed == True
and claimed_independent_review_count > effective_independent_review_count
```

### `NPG-T08` — Context collapse

Trigger when:

```text
proposed_use.context_collapsed == True
```

### `NPG-T09` — Relationship projection

Trigger when either:

```text
proposed_use.relationship_adoption == True
authority_exclusions.relationship_authority == True
```

### `NPG-T10` — Identity-trait / M3 projection

Trigger when any of:

```text
proposed_use.identity_trait_adoption == True
authority_exclusions.identity_authority == True
authority_exclusions.m3_nomination_or_write == True
```

### `NPG-T11` — Interpretation laundering

Trigger when:

```text
proposed_use.interpretation_as_direct_source == True
and claim.directly_stated == False
```

### `NPG-T12` — Consent inheritance

Trigger when either:

```text
proposed_use.consent_transfer == True
authority_exclusions.consent_authority == True
```

If multiple threats trigger, preserve all of them in ascending threat-ID order.
The primary rejection reason is the lowest triggered threat ID.

---

## 12. 🚦 Exact result and reason contract

Exact primary reason vocabulary:

```python
class NonProjectionReason(StrEnum):
    PASS_ATTRIBUTED = "PASS_ATTRIBUTED"

    NPG_T01 = "NPG-T01"
    NPG_T02 = "NPG-T02"
    NPG_T03 = "NPG-T03"
    NPG_T04 = "NPG-T04"
    NPG_T05 = "NPG-T05"
    NPG_T06 = "NPG-T06"
    NPG_T07 = "NPG-T07"
    NPG_T08 = "NPG-T08"
    NPG_T09 = "NPG-T09"
    NPG_T10 = "NPG-T10"
    NPG_T11 = "NPG-T11"
    NPG_T12 = "NPG-T12"

    BUDGET_EXHAUSTED = "BUDGET_EXHAUSTED"
    SUBJECT_RELATION_UNKNOWN = "SUBJECT_RELATION_UNKNOWN"
    SELF_EVIDENCE_BINDING_UNSUPPORTED = "SELF_EVIDENCE_BINDING_UNSUPPORTED"
    PROVENANCE_UNKNOWN = "PROVENANCE_UNKNOWN"
    SOURCE_CLASS_UNKNOWN = "SOURCE_CLASS_UNKNOWN"
    SOURCE_ORIGIN_UNKNOWN = "SOURCE_ORIGIN_UNKNOWN"
    CONTEXT_DISTANCE_UNKNOWN = "CONTEXT_DISTANCE_UNKNOWN"
    SCOPE_UNRESOLVED = "SCOPE_UNRESOLVED"

    PROVENANCE_CONFLICTING = "PROVENANCE_CONFLICTING"
    INTERPRETATION_CONTESTED = "INTERPRETATION_CONTESTED"

    PROVENANCE_PARTIAL = "PROVENANCE_PARTIAL"
    ATTRIBUTION_REPAIR_REQUIRED = "ATTRIBUTION_REPAIR_REQUIRED"
    CONTEXT_ACKNOWLEDGEMENT_REQUIRED = "CONTEXT_ACKNOWLEDGEMENT_REQUIRED"
```

Exact result shape:

```python
@dataclass(frozen=True, slots=True)
class NonProjectionResult:
    decision: NonProjectionDecision
    primary_reason: NonProjectionReason
    reasons: tuple[NonProjectionReason, ...]
    triggered_threats: tuple[ProjectionThreat, ...]
    effective_independent_review_count: int
    envelope_fingerprint: str | None
    classification_fingerprint: str | None
    contract_version: str = "NPG-v0.1"
    envelope_version: str = "AIE-v0.1"
    canonical_profile: str = "MENTAURY_CANONICAL_JSON_V1"
```

No result contains raw source text, a credential, token, tool handle, callback,
storage locator, mutation command, capability lease, identity object,
relationship object, M2/M3 mutation object or reusable permission.

---

## 13. 🧭 Exact fail-closed decision precedence

The frozen decision precedence is:

```text
REJECT
> DEFER
> CONTESTED
> REVISE_REQUIRED
> PASS_ATTRIBUTED
```

Normative evaluation order:

```text
strict contract admission
→ derive effective reviewer independence
→ derive all NPG-T01…NPG-T12 threats
→ derive DEFER conditions
→ derive CONTESTED conditions
→ derive REVISE_REQUIRED conditions
→ canonicalize/fingerprint admitted envelope
→ add local-budget DEFER condition when applicable
→ choose highest-precedence decision
→ sort complete reason set by fixed reason priority
→ construct result
→ canonicalize/fingerprint classification evidence
```

A verified threat remains `REJECT` even when lower-precedence uncertainty,
conflict, revision or local-budget conditions are also present.

### 13.1 DEFER conditions

Add these deterministic defer reasons when applicable:

```text
actual input complexity > caller local budget      → BUDGET_EXHAUSTED
subject_relation == UNKNOWN                        → SUBJECT_RELATION_UNKNOWN
subject_relation == VERIFIED_SELF                  → SELF_EVIDENCE_BINDING_UNSUPPORTED
provenance_state == UNKNOWN                        → PROVENANCE_UNKNOWN
source_class == UNKNOWN_SOURCE                     → SOURCE_CLASS_UNKNOWN
source_origin == UNKNOWN                           → SOURCE_ORIGIN_UNKNOWN
any context distance/risk == UNKNOWN               → CONTEXT_DISTANCE_UNKNOWN
proposed scope intersects scope.unknowns            → SCOPE_UNRESOLVED
```

### 13.2 CONTESTED conditions

```text
provenance_state == CONFLICTING                     → PROVENANCE_CONFLICTING
interpretation.contested == True                   → INTERPRETATION_CONTESTED
```

### 13.3 REVISE_REQUIRED conditions

```text
provenance_state == PARTIAL                        → PROVENANCE_PARTIAL
claim in AUTOBIOGRAPHICAL_TESTIMONY /
         RELATIONSHIP_TESTIMONY /
         CONSENT_STATEMENT
and source_actor_ref is None                       → ATTRIBUTION_REPAIR_REQUIRED
required context acknowledgement missing           → CONTEXT_ACKNOWLEDGEMENT_REQUIRED
```

### 13.4 PASS condition

`PASS_ATTRIBUTED` is returned only when:

- no threat is triggered;
- no DEFER reason exists;
- no CONTESTED reason exists;
- no REVISE_REQUIRED reason exists;
- all authority-establishment booleans are `False`;
- the proposed scope is inside the admitted scope;
- the envelope and result fingerprints are derived successfully.

---

## 14. 🧾 Fixed reason ordering

Complete reasons are never emitted in incidental discovery order.

Fixed priority:

```text
NPG-T01 … NPG-T12
BUDGET_EXHAUSTED
SUBJECT_RELATION_UNKNOWN
SELF_EVIDENCE_BINDING_UNSUPPORTED
PROVENANCE_UNKNOWN
SOURCE_CLASS_UNKNOWN
SOURCE_ORIGIN_UNKNOWN
CONTEXT_DISTANCE_UNKNOWN
SCOPE_UNRESOLVED
PROVENANCE_CONFLICTING
INTERPRETATION_CONTESTED
PROVENANCE_PARTIAL
ATTRIBUTION_REPAIR_REQUIRED
CONTEXT_ACKNOWLEDGEMENT_REQUIRED
PASS_ATTRIBUTED
```

`primary_reason` is the first reason belonging to the selected highest-precedence
decision. `PASS_ATTRIBUTED` is the only reason in a positive result.

---

## 15. 🔐 Exact canonical fingerprints

### 15.1 Envelope fingerprint

Fingerprint SHA-256 over canonical JSON bytes of exactly:

```json
{
  "domain": "MENTAURY_NPG_ENVELOPE_V1",
  "contract_version": "NPG-v0.1",
  "envelope_version": "AIE-v0.1",
  "canonical_profile": "MENTAURY_CANONICAL_JSON_V1",
  "envelope": "<AttributedInterpretationEnvelope.to_value()>"
}
```

The placeholder above denotes the native canonical value, not a literal string.

Normative algorithm:

```text
strict admission
→ exact to_value projection
→ canonical_json_bytes(...)
→ enforce HARD_MAX_ENVELOPE_BYTES
→ hashlib.sha256(bytes).hexdigest()
```

### 15.2 Classification fingerprint

Fingerprint SHA-256 over canonical JSON bytes of exactly:

```text
domain = MENTAURY_NPG_CLASSIFICATION_V1
contract_version
canonical_profile
envelope_fingerprint
budget.to_value()
decision
primary_reason
reasons in fixed order
triggered_threats in ascending NPG-T order
effective_independent_review_count
```

When present, fingerprints are lowercase 64-character SHA-256 hex strings.
Fingerprints are derived evidence only and grant no authority.

A valid input that exceeds only the caller local budget may carry an envelope
fingerprint if canonicalization succeeded; its classification remains `DEFER`.
A hard-cap or malformed-contract violation raises `NonProjectionContractError`
and produces no result/fingerprint.

---

## 16. 🧪 Frozen inherited scenario matrix

The implementation contract preserves the exact readiness outcomes:

| ID | Exact decision | Required primary threat/reason |
|---|---|---|
| `NPG-SC-001` | `PASS_ATTRIBUTED` | `PASS_ATTRIBUTED` |
| `NPG-SC-002` | `PASS_ATTRIBUTED` | `PASS_ATTRIBUTED` |
| `NPG-SC-003` | `REJECT` | `NPG-T07` |
| `NPG-SC-004` | `REJECT` | `NPG-T03` |
| `NPG-SC-005` | `REJECT` | `NPG-T04` |
| `NPG-SC-006` | `REJECT` | `NPG-T01` |
| `NPG-SC-007` | `PASS_ATTRIBUTED` | `PASS_ATTRIBUTED` |
| `NPG-SC-008` | `REVISE_REQUIRED` | `CONTEXT_ACKNOWLEDGEMENT_REQUIRED` or scope-repair equivalent encoded by the exact fixture |
| `NPG-SC-009` | `REJECT` | `NPG-T09` |
| `NPG-SC-010` | `REJECT` | `NPG-T05` |
| `NPG-SC-011` | `DEFER` | `PROVENANCE_UNKNOWN` or `SOURCE_CLASS_UNKNOWN` according to the exact fixture |
| `NPG-SC-012` | `REJECT` | `NPG-T02` |

For `NPG-SC-008`, the frozen fixture must encode missing context acknowledgement
without setting deliberate `context_collapsed=True`; otherwise it would become a
higher-precedence `NPG-T08` rejection and would no longer represent the readiness
scenario.

For `NPG-SC-012`, attempting to use a positive result as Action Gate/retrieval/tool
authority is encoded by at least one of the `AuthorityExclusions` capability/action/
retrieval/tool booleans being `True`; the lowest applicable threat remains
`NPG-T02`.

### 16.1 Required contested fixture

```text
NPG-SC-CONTESTED-001
provenance_state = VERIFIED
interpretation.contested = True
alternatives != ()
disconfirming_refs != ()
no higher-precedence threat/defer
→ CONTESTED · INTERPRETATION_CONTESTED
```

---

## 17. 🔁 Frozen executable matrix families

A later bounded implementation must satisfy all of these exact families:

```text
NPG-ADM-001…NPG-ADM-020
NPG-THR-001…NPG-THR-012
NPG-SC-001…NPG-SC-012
NPG-SC-CONTESTED-001
NPG-DEC-001…NPG-DEC-012
NPG-FP-001…NPG-FP-008
MT-NPG-001…MT-NPG-008
NPG-PURE-001…NPG-PURE-010
```

### 17.1 Admission family

At minimum freezes tests for exact version, immutable types, non-empty/unpadded
refs, sorted/unique tuples, review ordering/uniqueness, exact booleans/integers,
consensus count consistency, self-basis consistency, contested fixture shape,
hard caps, local budget shape, no hidden normalization and contract-error behavior.

### 17.2 Threat family

`NPG-THR-001…012` maps one-to-one to `NPG-T01…12`; each fixture triggers exactly
its intended threat while all unrelated threat inputs remain false/safe.

### 17.3 Decision family

Must include:

- `REJECT > DEFER`;
- `DEFER > CONTESTED`;
- `CONTESTED > REVISE_REQUIRED`;
- `REVISE_REQUIRED > PASS_ATTRIBUTED`;
- deterministic lowest-threat primary reason;
- complete sorted reason preservation;
- `VERIFIED_SELF → DEFER` in v0.1;
- local budget exhaustion without truncation;
- partial provenance revision;
- unknown provenance defer;
- conflicting provenance contested;
- positive ceiling invariants.

### 17.4 Fingerprint family

Must include exact canonical domains, same-input stability, one-field sensitivity,
order rejection rather than hidden sorting, caller-fingerprint rejection,
budget-sensitive classification fingerprint, lowercase SHA-256 format and no
ambient timestamp/environment contribution.

---

## 18. 🔁 Frozen metamorphic properties

The implementation must execute the inherited properties exactly:

```text
MT-NPG-001 Attribution preservation
presentation style change only
→ source/speaker/subject attribution cannot change.

MT-NPG-002 Prestige non-escalation
source fame/status change only
→ truth/self/relationship/authority cannot increase.

MT-NPG-003 Repetition non-escalation
repeat correlated reviews
→ effective independence cannot increase.

MT-NPG-004 Context monotonicity
remove required provenance/context/scope evidence
→ result cannot become more permissive.

MT-NPG-005 Self/non-self invalidation
substitute source/subject/branch identity evidence
→ prior self attribution cannot remain valid without re-evaluation;
  in v0.1 VERIFIED_SELF still defers.

MT-NPG-006 No M3 amplification
change interpretation/voice metadata only
→ M3 nomination/write authority remains NONE.

MT-NPG-007 No relationship amplification
increase narrative similarity/shared-history references only
→ relationship/commitment/consent authority remains NONE.

MT-NPG-008 Determinism
same admitted envelope + same budget + NPG-v0.1
→ same decision, primary reason, reason set, threat set and fingerprints.
```

---

## 19. 🧪 Purity and no-hidden-I/O proof strategy

`NPG-PURE-001…010` must prove at least:

```text
NPG-PURE-001  no network access
NPG-PURE-002  no filesystem access
NPG-PURE-003  no database / vector / graph access
NPG-PURE-004  no model / LLM call
NPG-PURE-005  no retrieval / Atlas lookup
NPG-PURE-006  no persistence / event append / M2/M3 mutation
NPG-PURE-007  no identity / relationship registry lookup
NPG-PURE-008  no Action Gate / capability / tool invocation
NPG-PURE-009  no ambient clock / random / environment dependency
NPG-PURE-010  import has no side effects and same input is deterministic
```

The implementation test strategy should combine source/import inspection with
monkeypatch sentinels for forbidden I/O surfaces where practical. Green unit tests
alone do not waive the semantic purity requirement.

---

## 20. 🧱 Character, P1 and Canon compatibility

The contract changes none of:

```text
P1-001 contract = unchanged
P1-002 contract = unchanged
P1-003 contract = unchanged
MENTAURY_CANON_V0.1 = unchanged
```

The P1-003 composer remains exactly its current same-attempt P1-001/P1-002
composition. `NonProjectionResult` is not an implicit new composer input.

```text
P1_003_ELIGIBLE_FOR_NEXT_GATE
+ PASS_ATTRIBUTED
≠ Action Gate PASS
```

Any future cross-gate composition involving `NonProjectionResult` requires a
separate explicit docs-only binding decision.

Character remains downstream presentation only:

```text
Non-Projection classification
→ then Character presentation

Character presentation
→ cannot change envelope provenance
→ cannot change reviewer independence
→ cannot change threat set
→ cannot change decision or reasons
```

---

## 21. ⛔ Exact non-goals and forbidden authority surface

`NPG-v0.1` does not include or authorize:

- raw source ingestion;
- web/file/database/vector/graph retrieval;
- Creator Atlas or Human Paths Atlas runtime;
- model/LLM interpretation;
- identity/continuation lookup or verification;
- relationship/commitment reconciliation;
- consent authority verification beyond rejecting transfer/inheritance;
- belief/truth mutation;
- M2 persistence or promotion;
- M3 nomination or write;
- Character runtime activation;
- P1-003 modification;
- Action Gate implementation or invocation;
- capability acquisition;
- tool invocation;
- persistence or event append;
- backend selection/migration;
- network/filesystem/database I/O;
- deployment/runtime activation;
- P1-004 assignment.

---

## 22. ⛔ Compatibility stop

Stop promotion if implementation would require any of:

- changing frozen readiness `NPG-T01…T12`, `NPG-SC-001…012` or
  `MT-NPG-001…008` semantics;
- changing this exact package/API/schema/result/reason contract;
- making `VERIFIED_SELF` positive without a separately frozen identity binding;
- hidden retrieval, persistence, model, filesystem, network, database, graph or
  vector access;
- using Character to change evidence/result;
- using source prestige or reviewer quantity to amplify authority;
- changing P1-001/P1-002/P1-003 or Canon v0.1;
- direct or indirect M2/M3 write;
- relationship/commitment/consent inheritance;
- `PASS_ATTRIBUTED` becoming Action Gate/retrieval/tool/execution authority;
- deployment/runtime activation.

Required response:

```text
STOP_CURRENT_PROMOTION
→ new docs-only compatibility decision
→ Tier A review
→ explicit Owner decision if authority changes
```

---

## 23. 🔐 Required authority ladder after this freeze

After this contract is merged and verified, the next possible authority step is
**not implementation**. It is a separate explicit bounded Owner decision.

```text
CANDIDATE_SELECTED_DOCS_ONLY
→ NON_PROJECTION_IMPLEMENTATION_CONTRACT_FROZEN_DOCS_ONLY
→ explicit separate NON_PROJECTION_OWNER_GO_AUTHORIZED_BOUNDED
→ clean Tier A implementation PR
→ exact-head correctness + adversarial review
→ protected merge
→ green resulting-main CI
→ separate completion/status reconciliation
```

Current state after this contract freeze, if merged successfully:

```text
NON_PROJECTION_CANDIDATE_SELECTION = SELECTED
NON_PROJECTION_CANDIDATE = PURE_NON_PROJECTION_CLASSIFIER
NON_PROJECTION_IMPLEMENTATION_CONTRACT = FROZEN_DOCS
NON_PROJECTION_CONTRACT_VERSION = NPG-v0.1
P1_004 = NOT_ASSIGNED
NON_PROJECTION_OWNER_GO = NOT_GRANTED
IMPLEMENTATION_AUTHORIZATION = NONE
NON_PROJECTION_RUNTIME = NOT_AUTHORIZED
```

No later state follows automatically.

---

## 24. ✅ Contract-freeze exit criteria

```text
[x] exact package path frozen
[x] exact public API frozen
[x] exact contract/envelope versions frozen
[x] canonical domains and hard caps frozen
[x] exact immutable enums frozen
[x] exact immutable envelope schema frozen
[x] exact local budget frozen
[x] malformed-input exception policy frozen
[x] no-hidden-normalization rule frozen
[x] VERIFIED_SELF fail-closed behavior frozen
[x] reviewer-correlation algorithm frozen
[x] context/scope behavior frozen
[x] NPG-T01…T12 executable mapping frozen
[x] exact result/reason schema frozen
[x] decision precedence and reason ordering frozen
[x] canonical fingerprint algorithms frozen
[x] NPG-SC-001…012 exact outcomes retained
[x] contested fixture frozen
[x] executable matrix families frozen
[x] MT-NPG-001…008 retained
[x] NPG-PURE-001…010 purity proof frozen
[x] Character/P1/Canon compatibility retained
[x] non-goals and compatibility stop explicit
[x] P1-004 remains unassigned
[x] Owner GO remains separate
[x] implementation remains unauthorized
```

---

## 25. 🏁 Final formula

```text
P1-003 IMPLEMENTED_BOUNDED
+ Non-Projection readiness READY
+ ATTRIBUTED_INTERPRETATION_ENVELOPE readiness model frozen
+ PURE_NON_PROJECTION_CLASSIFIER selected
+ NPG-v0.1 implementation contract frozen docs-only

→ contract-ready for a later explicit Owner GO decision

≠ P1-004 assigned
≠ Owner GO
≠ implementation authorization
≠ implementation
≠ runtime activation
≠ factual truth proof
≠ identity / relationship / consent authority
≠ M2/M3 mutation
≠ Action Gate / retrieval / tool authority
≠ deployment authority
```
