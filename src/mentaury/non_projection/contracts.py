"""Immutable contracts for the bounded NPG-v0.1 Non-Projection classifier."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Final

NON_PROJECTION_CONTRACT_VERSION: Final[str] = "NPG-v0.1"
ATTRIBUTED_INTERPRETATION_ENVELOPE_VERSION: Final[str] = "AIE-v0.1"
CANONICAL_PROFILE: Final[str] = "MENTAURY_CANONICAL_JSON_V1"
INPUT_FINGERPRINT_DOMAIN: Final[str] = "MENTAURY_NPG_INPUT_V1"
SOURCE_PROVENANCE_SCOPE: Final[str] = "CALLER_SUPPLIED_ATTRIBUTED_VALUES_ONLY"

HARD_MAX_STRING_BYTES: Final[int] = 4096
HARD_MAX_TUPLE_ITEMS: Final[int] = 512
HARD_MAX_REVIEW_RECORDS: Final[int] = 64
HARD_MAX_CANONICAL_INPUT_BYTES: Final[int] = 262144


class NonProjectionContractError(ValueError):
    """Raised when caller-supplied values violate the frozen NPG-v0.1 contract."""


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


class InterpretationState(StrEnum):
    SUPPORTED = "SUPPORTED"
    CONTESTED = "CONTESTED"
    UNKNOWN = "UNKNOWN"


class ContextDistanceLevel(StrEnum):
    SAME_CONTEXT = "SAME_CONTEXT"
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


class NonProjectionDecision(StrEnum):
    PASS_ATTRIBUTED = "PASS_ATTRIBUTED"
    REVISE_REQUIRED = "REVISE_REQUIRED"
    CONTESTED = "CONTESTED"
    DEFER = "DEFER"
    REJECT = "REJECT"


class NonProjectionReason(StrEnum):
    PASS_ATTRIBUTED = "PASS_ATTRIBUTED"
    ATTRIBUTION_REPAIR_REQUIRED = "ATTRIBUTION_REPAIR_REQUIRED"
    CONTEXT_SCOPE_REPAIR_REQUIRED = "CONTEXT_SCOPE_REPAIR_REQUIRED"
    PROVENANCE_CONFLICTING = "PROVENANCE_CONFLICTING"
    INTERPRETATION_CONTESTED = "INTERPRETATION_CONTESTED"
    ENVELOPE_VERSION_UNVERIFIED = "ENVELOPE_VERSION_UNVERIFIED"
    BUDGET_EXHAUSTED = "BUDGET_EXHAUSTED"
    CANONICALIZATION_FAILED = "CANONICALIZATION_FAILED"
    SOURCE_CLASS_UNKNOWN = "SOURCE_CLASS_UNKNOWN"
    SOURCE_ORIGIN_UNKNOWN = "SOURCE_ORIGIN_UNKNOWN"
    PROVENANCE_UNKNOWN = "PROVENANCE_UNKNOWN"
    PROVENANCE_MATERIAL_GAP = "PROVENANCE_MATERIAL_GAP"
    SUBJECT_RELATION_UNKNOWN = "SUBJECT_RELATION_UNKNOWN"
    SELF_BASIS_UNVERIFIED = "SELF_BASIS_UNVERIFIED"
    INTERPRETATION_UNKNOWN = "INTERPRETATION_UNKNOWN"
    CONTEXT_UNKNOWN = "CONTEXT_UNKNOWN"
    SCOPE_UNKNOWN = "SCOPE_UNKNOWN"
    AUTOBIOGRAPHY_LAUNDERING = "AUTOBIOGRAPHY_LAUNDERING"
    AUTHORITY_INHERITANCE = "AUTHORITY_INHERITANCE"
    TRUTH_ESCALATION = "TRUTH_ESCALATION"
    EMOTION_TO_DRIVE_PROJECTION = "EMOTION_TO_DRIVE_PROJECTION"
    STYLE_TO_BELIEF_PROJECTION = "STYLE_TO_BELIEF_PROJECTION"
    HISTORICAL_LAW_PROJECTION = "HISTORICAL_LAW_PROJECTION"
    CORRELATED_CONSENSUS_LAUNDERING = "CORRELATED_CONSENSUS_LAUNDERING"
    CONTEXT_COLLAPSE = "CONTEXT_COLLAPSE"
    RELATIONSHIP_PROJECTION = "RELATIONSHIP_PROJECTION"
    IDENTITY_TRAIT_PROJECTION = "IDENTITY_TRAIT_PROJECTION"
    INTERPRETATION_LAUNDERING = "INTERPRETATION_LAUNDERING"
    CONSENT_INHERITANCE = "CONSENT_INHERITANCE"


class NonProjectionThreatId(StrEnum):
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


def _require_exact_type(value: object, expected: type[object], name: str) -> None:
    if type(value) is not expected:
        raise NonProjectionContractError(f"{name} must be exact {expected.__name__}")


def _require_exact_enum(value: object, expected: type[StrEnum], name: str) -> None:
    if type(value) is not expected:
        raise NonProjectionContractError(f"{name} must be exact {expected.__name__} member")


def _require_string(value: object, name: str, *, optional: bool = False) -> str | None:
    if optional and value is None:
        return None
    if type(value) is not str or not value or value != value.strip():
        raise NonProjectionContractError(f"{name} must be a non-empty unpadded string")
    try:
        encoded = value.encode("utf-8")
    except UnicodeEncodeError as exc:
        raise NonProjectionContractError(f"{name} must be valid UTF-8") from exc
    if len(encoded) > HARD_MAX_STRING_BYTES:
        raise NonProjectionContractError(f"{name} exceeds HARD_MAX_STRING_BYTES")
    return value


def _require_bool(value: object, name: str) -> bool:
    if type(value) is not bool:
        raise NonProjectionContractError(f"{name} must be exact bool")
    return value


def _require_non_negative_int(value: object, name: str) -> int:
    if type(value) is not int or value < 0:
        raise NonProjectionContractError(f"{name} must be a non-negative integer")
    return value


def _require_positive_int(value: object, name: str, hard_cap: int) -> int:
    if type(value) is not int or value <= 0:
        raise NonProjectionContractError(f"{name} must be a positive integer")
    if value > hard_cap:
        raise NonProjectionContractError(f"{name} exceeds frozen hard cap")
    return value


def _require_string_tuple(value: object, name: str, *, non_empty: bool = False) -> tuple[str, ...]:
    if type(value) is not tuple:
        raise NonProjectionContractError(f"{name} must be exact tuple")
    if len(value) > HARD_MAX_TUPLE_ITEMS:
        raise NonProjectionContractError(f"{name} exceeds HARD_MAX_TUPLE_ITEMS")
    if non_empty and not value:
        raise NonProjectionContractError(f"{name} must be non-empty")
    checked = tuple(_require_string(item, f"{name}[{index}]") for index, item in enumerate(value))
    if tuple(sorted(checked)) != checked:
        raise NonProjectionContractError(f"{name} must already be lexicographically sorted")
    if len(set(checked)) != len(checked):
        raise NonProjectionContractError(f"{name} must be unique")
    return checked


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

    def __post_init__(self) -> None:
        _require_string(self.source_ref, "source_ref")
        _require_string(self.source_actor_ref, "source_actor_ref", optional=True)
        _require_exact_enum(self.source_class, SourceClass, "source_class")
        _require_exact_enum(self.source_origin, SourceOrigin, "source_origin")
        _require_exact_enum(self.provenance_state, ProvenanceState, "provenance_state")
        _require_string(self.publication_or_capture_context_ref, "publication_or_capture_context_ref", optional=True)
        _require_exact_enum(self.sensitivity, Sensitivity, "sensitivity")
        _require_string(self.usage_boundary_ref, "usage_boundary_ref")
        _require_string_tuple(self.material_gaps, "material_gaps")

    def to_value(self) -> dict[str, object]:
        return {"source_ref": self.source_ref, "source_actor_ref": self.source_actor_ref, "source_class": self.source_class.value, "source_origin": self.source_origin.value, "provenance_state": self.provenance_state.value, "publication_or_capture_context_ref": self.publication_or_capture_context_ref, "sensitivity": self.sensitivity.value, "usage_boundary_ref": self.usage_boundary_ref, "material_gaps": list(self.material_gaps)}


@dataclass(frozen=True, slots=True)
class Attribution:
    speaker_ref: str
    subject_ref: str
    subject_relation: SubjectRelation
    self_basis_ref: str | None
    attribution_basis_refs: tuple[str, ...]

    def __post_init__(self) -> None:
        _require_string(self.speaker_ref, "speaker_ref")
        _require_string(self.subject_ref, "subject_ref")
        _require_exact_enum(self.subject_relation, SubjectRelation, "subject_relation")
        _require_string(self.self_basis_ref, "self_basis_ref", optional=True)
        _require_string_tuple(self.attribution_basis_refs, "attribution_basis_refs")
        if self.subject_relation in {SubjectRelation.NON_SELF, SubjectRelation.UNKNOWN} and self.self_basis_ref is not None:
            raise NonProjectionContractError("NON_SELF/UNKNOWN requires self_basis_ref is None")
        if self.subject_relation is SubjectRelation.VERIFIED_SELF and self.self_basis_ref is None:
            raise NonProjectionContractError("VERIFIED_SELF requires self_basis_ref")

    def to_value(self) -> dict[str, object]:
        return {"speaker_ref": self.speaker_ref, "subject_ref": self.subject_ref, "subject_relation": self.subject_relation.value, "self_basis_ref": self.self_basis_ref, "attribution_basis_refs": list(self.attribution_basis_refs)}


@dataclass(frozen=True, slots=True)
class Claim:
    claim_id: str
    claim_class: ClaimClass
    statement_ref: str
    directly_stated: bool

    def __post_init__(self) -> None:
        _require_string(self.claim_id, "claim_id")
        _require_exact_enum(self.claim_class, ClaimClass, "claim_class")
        _require_string(self.statement_ref, "statement_ref")
        _require_bool(self.directly_stated, "directly_stated")

    def to_value(self) -> dict[str, object]:
        return {"claim_id": self.claim_id, "claim_class": self.claim_class.value, "statement_ref": self.statement_ref, "directly_stated": self.directly_stated}


@dataclass(frozen=True, slots=True)
class Interpretation:
    interpretation_ref: str | None
    interpreter_ref: str | None
    state: InterpretationState
    alternatives: tuple[str, ...]
    disconfirming_refs: tuple[str, ...]

    def __post_init__(self) -> None:
        _require_string(self.interpretation_ref, "interpretation_ref", optional=True)
        _require_string(self.interpreter_ref, "interpreter_ref", optional=True)
        _require_exact_enum(self.state, InterpretationState, "interpretation_state")
        _require_string_tuple(self.alternatives, "alternatives")
        _require_string_tuple(self.disconfirming_refs, "disconfirming_refs")
        if self.state is InterpretationState.CONTESTED:
            if len(self.alternatives) < 2:
                raise NonProjectionContractError("CONTESTED requires at least two alternatives")
            if not self.disconfirming_refs:
                raise NonProjectionContractError("CONTESTED requires disconfirming_refs")

    def to_value(self) -> dict[str, object]:
        return {"interpretation_ref": self.interpretation_ref, "interpreter_ref": self.interpreter_ref, "state": self.state.value, "alternatives": list(self.alternatives), "disconfirming_refs": list(self.disconfirming_refs)}


@dataclass(frozen=True, slots=True)
class ContextualDistance:
    historical: ContextDistanceLevel
    cultural: ContextDistanceLevel
    terminology: ContextDistanceLevel
    translation_or_paraphrase: ContextDistanceLevel
    source_distance: ContextDistanceLevel
    anachronism_risk: AnachronismRisk

    def __post_init__(self) -> None:
        for name in ("historical", "cultural", "terminology", "translation_or_paraphrase", "source_distance"):
            _require_exact_enum(getattr(self, name), ContextDistanceLevel, name)
        _require_exact_enum(self.anachronism_risk, AnachronismRisk, "anachronism_risk")

    def to_value(self) -> dict[str, object]:
        return {"historical": self.historical.value, "cultural": self.cultural.value, "terminology": self.terminology.value, "translation_or_paraphrase": self.translation_or_paraphrase.value, "source_distance": self.source_distance.value, "anachronism_risk": self.anachronism_risk.value}


@dataclass(frozen=True, slots=True)
class ReviewRecord:
    review_ref: str
    reviewer_ref: str
    independence: ReviewerIndependence
    provider_ref: str | None
    prompt_family_ref: str | None
    context_snapshot_ref: str | None
    saw_prior_output: bool

    def __post_init__(self) -> None:
        _require_string(self.review_ref, "review_ref")
        _require_string(self.reviewer_ref, "reviewer_ref")
        _require_exact_enum(self.independence, ReviewerIndependence, "independence")
        _require_string(self.provider_ref, "provider_ref", optional=True)
        _require_string(self.prompt_family_ref, "prompt_family_ref", optional=True)
        _require_string(self.context_snapshot_ref, "context_snapshot_ref", optional=True)
        _require_bool(self.saw_prior_output, "saw_prior_output")

    def to_value(self) -> dict[str, object]:
        return {"review_ref": self.review_ref, "reviewer_ref": self.reviewer_ref, "independence": self.independence.value, "provider_ref": self.provider_ref, "prompt_family_ref": self.prompt_family_ref, "context_snapshot_ref": self.context_snapshot_ref, "saw_prior_output": self.saw_prior_output}


@dataclass(frozen=True, slots=True)
class ReviewProvenance:
    reviews: tuple[ReviewRecord, ...]

    def __post_init__(self) -> None:
        if type(self.reviews) is not tuple:
            raise NonProjectionContractError("reviews must be exact tuple")
        if len(self.reviews) > HARD_MAX_REVIEW_RECORDS:
            raise NonProjectionContractError("reviews exceeds HARD_MAX_REVIEW_RECORDS")
        if len(self.reviews) > HARD_MAX_TUPLE_ITEMS:
            raise NonProjectionContractError("reviews exceeds HARD_MAX_TUPLE_ITEMS")
        for index, review in enumerate(self.reviews):
            _require_exact_type(review, ReviewRecord, f"reviews[{index}]")
        refs = tuple(review.review_ref for review in self.reviews)
        if tuple(sorted(refs)) != refs:
            raise NonProjectionContractError("reviews must already be sorted by review_ref")
        if len(set(refs)) != len(refs):
            raise NonProjectionContractError("review_ref must be unique")

    def to_value(self) -> dict[str, object]:
        return {"reviews": [review.to_value() for review in self.reviews]}


@dataclass(frozen=True, slots=True)
class ScopeBoundary:
    applies_to: tuple[str, ...]
    may_support: tuple[str, ...]
    does_not_establish: tuple[str, ...]
    unknowns: tuple[str, ...]
    transfer_limits: tuple[str, ...]

    def __post_init__(self) -> None:
        for name in ("applies_to", "may_support", "does_not_establish", "unknowns", "transfer_limits"):
            _require_string_tuple(getattr(self, name), name)

    def to_value(self) -> dict[str, object]:
        return {name: list(getattr(self, name)) for name in ("applies_to", "may_support", "does_not_establish", "unknowns", "transfer_limits")}


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

    def __post_init__(self) -> None:
        for name in ("factual_truth_proof", "identity_authority", "relationship_authority", "consent_authority", "capability_authority", "action_gate_authority", "retrieval_authority", "tool_execution_authority", "m3_nomination_or_write"):
            _require_bool(getattr(self, name), name)

    def to_value(self) -> dict[str, object]:
        return {name: getattr(self, name) for name in ("factual_truth_proof", "identity_authority", "relationship_authority", "consent_authority", "capability_authority", "action_gate_authority", "retrieval_authority", "tool_execution_authority", "m3_nomination_or_write")}


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

    def __post_init__(self) -> None:
        _require_string_tuple(self.proposed_applies_to, "proposed_applies_to", non_empty=True)
        for name in ("adopt_as_self_experience", "inherit_source_authority", "assert_as_objective_truth", "adopt_source_emotion_as_drive", "style_changes_evidence_status", "generalize_beyond_scope", "discard_relevant_context", "inherit_relationship_or_commitment", "promote_to_stable_identity_trait", "present_interpretation_as_direct_testimony", "inherit_consent"):
            _require_bool(getattr(self, name), name)
        _require_non_negative_int(self.claimed_independent_review_count, "claimed_independent_review_count")

    def to_value(self) -> dict[str, object]:
        return {"proposed_applies_to": list(self.proposed_applies_to), "adopt_as_self_experience": self.adopt_as_self_experience, "inherit_source_authority": self.inherit_source_authority, "assert_as_objective_truth": self.assert_as_objective_truth, "adopt_source_emotion_as_drive": self.adopt_source_emotion_as_drive, "style_changes_evidence_status": self.style_changes_evidence_status, "generalize_beyond_scope": self.generalize_beyond_scope, "claimed_independent_review_count": self.claimed_independent_review_count, "discard_relevant_context": self.discard_relevant_context, "inherit_relationship_or_commitment": self.inherit_relationship_or_commitment, "promote_to_stable_identity_trait": self.promote_to_stable_identity_trait, "present_interpretation_as_direct_testimony": self.present_interpretation_as_direct_testimony, "inherit_consent": self.inherit_consent}


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

    def __post_init__(self) -> None:
        _require_string(self.envelope_version, "envelope_version")
        for name, expected in (("source_provenance", SourceProvenance), ("attribution", Attribution), ("claim", Claim), ("interpretation", Interpretation), ("contextual_distance", ContextualDistance), ("review_provenance", ReviewProvenance), ("scope", ScopeBoundary), ("authority_exclusions", AuthorityExclusions), ("projection_intent", ProjectionIntent)):
            _require_exact_type(getattr(self, name), expected, name)

    def to_value(self) -> dict[str, object]:
        return {"envelope_version": self.envelope_version, "source_provenance": self.source_provenance.to_value(), "attribution": self.attribution.to_value(), "claim": self.claim.to_value(), "interpretation": self.interpretation.to_value(), "contextual_distance": self.contextual_distance.to_value(), "review_provenance": self.review_provenance.to_value(), "scope": self.scope.to_value(), "authority_exclusions": self.authority_exclusions.to_value(), "projection_intent": self.projection_intent.to_value()}


@dataclass(frozen=True, slots=True)
class NonProjectionBudget:
    max_string_bytes: int
    max_tuple_items: int
    max_review_records: int
    max_canonical_input_bytes: int

    def __post_init__(self) -> None:
        _require_positive_int(self.max_string_bytes, "max_string_bytes", HARD_MAX_STRING_BYTES)
        _require_positive_int(self.max_tuple_items, "max_tuple_items", HARD_MAX_TUPLE_ITEMS)
        _require_positive_int(self.max_review_records, "max_review_records", HARD_MAX_REVIEW_RECORDS)
        _require_positive_int(self.max_canonical_input_bytes, "max_canonical_input_bytes", HARD_MAX_CANONICAL_INPUT_BYTES)

    def to_value(self) -> dict[str, object]:
        return {"max_string_bytes": self.max_string_bytes, "max_tuple_items": self.max_tuple_items, "max_review_records": self.max_review_records, "max_canonical_input_bytes": self.max_canonical_input_bytes}


@dataclass(frozen=True, slots=True)
class NonProjectionResult:
    decision: NonProjectionDecision
    primary_reason: NonProjectionReason
    reasons: tuple[NonProjectionReason, ...]
    triggered_threat_ids: tuple[NonProjectionThreatId, ...]
    effective_independent_review_count: int
    input_fingerprint: str | None
    contract_version: str = NON_PROJECTION_CONTRACT_VERSION
    envelope_version: str = ATTRIBUTED_INTERPRETATION_ENVELOPE_VERSION
    canonical_profile: str = CANONICAL_PROFILE
    source_provenance_scope: str = SOURCE_PROVENANCE_SCOPE

    def __post_init__(self) -> None:
        _require_exact_enum(self.decision, NonProjectionDecision, "decision")
        _require_exact_enum(self.primary_reason, NonProjectionReason, "primary_reason")
        if type(self.reasons) is not tuple or not self.reasons:
            raise NonProjectionContractError("reasons must be a non-empty exact tuple")
        for reason in self.reasons:
            _require_exact_enum(reason, NonProjectionReason, "reason")
        if self.primary_reason is not self.reasons[0]:
            raise NonProjectionContractError("primary_reason must equal first ordered reason")
        if len(set(self.reasons)) != len(self.reasons):
            raise NonProjectionContractError("reasons must be unique")
        if type(self.triggered_threat_ids) is not tuple:
            raise NonProjectionContractError("triggered_threat_ids must be exact tuple")
        for threat in self.triggered_threat_ids:
            _require_exact_enum(threat, NonProjectionThreatId, "threat")
        if tuple(sorted(self.triggered_threat_ids, key=lambda item: item.value)) != self.triggered_threat_ids:
            raise NonProjectionContractError("triggered_threat_ids must be ordered")
        if len(set(self.triggered_threat_ids)) != len(self.triggered_threat_ids):
            raise NonProjectionContractError("triggered_threat_ids must be unique")
        _require_non_negative_int(self.effective_independent_review_count, "effective_independent_review_count")
        if self.input_fingerprint is not None:
            if type(self.input_fingerprint) is not str or len(self.input_fingerprint) != 64:
                raise NonProjectionContractError("input_fingerprint must be lowercase SHA-256 hex or None")
            if any(character not in "0123456789abcdef" for character in self.input_fingerprint):
                raise NonProjectionContractError("input_fingerprint must be lowercase SHA-256 hex")
        if self.contract_version != NON_PROJECTION_CONTRACT_VERSION:
            raise NonProjectionContractError("contract_version is frozen")
        if self.envelope_version != ATTRIBUTED_INTERPRETATION_ENVELOPE_VERSION:
            raise NonProjectionContractError("result envelope_version is frozen")
        if self.canonical_profile != CANONICAL_PROFILE:
            raise NonProjectionContractError("canonical_profile is frozen")
        if self.source_provenance_scope != SOURCE_PROVENANCE_SCOPE:
            raise NonProjectionContractError("source_provenance_scope is frozen")
        if self.decision is NonProjectionDecision.PASS_ATTRIBUTED:
            if self.primary_reason is not NonProjectionReason.PASS_ATTRIBUTED or self.reasons != (NonProjectionReason.PASS_ATTRIBUTED,) or self.triggered_threat_ids or self.input_fingerprint is None:
                raise NonProjectionContractError("invalid PASS_ATTRIBUTED result invariant")
        elif self.primary_reason is NonProjectionReason.PASS_ATTRIBUTED or NonProjectionReason.PASS_ATTRIBUTED in self.reasons:
            raise NonProjectionContractError("non-positive result cannot contain PASS_ATTRIBUTED reason")

    def to_value(self) -> dict[str, object]:
        return {"decision": self.decision.value, "primary_reason": self.primary_reason.value, "reasons": [reason.value for reason in self.reasons], "triggered_threat_ids": [threat.value for threat in self.triggered_threat_ids], "effective_independent_review_count": self.effective_independent_review_count, "input_fingerprint": self.input_fingerprint, "contract_version": self.contract_version, "envelope_version": self.envelope_version, "canonical_profile": self.canonical_profile, "source_provenance_scope": self.source_provenance_scope}
