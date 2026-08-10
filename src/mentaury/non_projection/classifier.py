"""Pure deterministic NPG-v0.1 Non-Projection classification."""

from __future__ import annotations

from collections import Counter
from dataclasses import fields, is_dataclass
from enum import StrEnum
import hashlib
from typing import Final

import mentaury.contracts.canonical_json as canonical_json_contract

from .contracts import (
    ATTRIBUTED_INTERPRETATION_ENVELOPE_VERSION,
    CANONICAL_PROFILE,
    HARD_MAX_CANONICAL_INPUT_BYTES,
    INPUT_FINGERPRINT_DOMAIN,
    NON_PROJECTION_CONTRACT_VERSION,
    SOURCE_PROVENANCE_SCOPE,
    AnachronismRisk,
    AttributedInterpretationEnvelope,
    ClaimClass,
    ContextDistanceLevel,
    InterpretationState,
    NonProjectionBudget,
    NonProjectionContractError,
    NonProjectionDecision,
    NonProjectionReason,
    NonProjectionResult,
    NonProjectionThreatId,
    ProvenanceState,
    ReviewerIndependence,
    SourceClass,
    SourceOrigin,
    SubjectRelation,
)

_THREAT_REASON: Final[dict[NonProjectionThreatId, NonProjectionReason]] = {
    NonProjectionThreatId.NPG_T01: NonProjectionReason.AUTOBIOGRAPHY_LAUNDERING,
    NonProjectionThreatId.NPG_T02: NonProjectionReason.AUTHORITY_INHERITANCE,
    NonProjectionThreatId.NPG_T03: NonProjectionReason.TRUTH_ESCALATION,
    NonProjectionThreatId.NPG_T04: NonProjectionReason.EMOTION_TO_DRIVE_PROJECTION,
    NonProjectionThreatId.NPG_T05: NonProjectionReason.STYLE_TO_BELIEF_PROJECTION,
    NonProjectionThreatId.NPG_T06: NonProjectionReason.HISTORICAL_LAW_PROJECTION,
    NonProjectionThreatId.NPG_T07: NonProjectionReason.CORRELATED_CONSENSUS_LAUNDERING,
    NonProjectionThreatId.NPG_T08: NonProjectionReason.CONTEXT_COLLAPSE,
    NonProjectionThreatId.NPG_T09: NonProjectionReason.RELATIONSHIP_PROJECTION,
    NonProjectionThreatId.NPG_T10: NonProjectionReason.IDENTITY_TRAIT_PROJECTION,
    NonProjectionThreatId.NPG_T11: NonProjectionReason.INTERPRETATION_LAUNDERING,
    NonProjectionThreatId.NPG_T12: NonProjectionReason.CONSENT_INHERITANCE,
}

_DEFER_ORDER: Final[tuple[NonProjectionReason, ...]] = (
    NonProjectionReason.ENVELOPE_VERSION_UNVERIFIED,
    NonProjectionReason.BUDGET_EXHAUSTED,
    NonProjectionReason.CANONICALIZATION_FAILED,
    NonProjectionReason.SOURCE_CLASS_UNKNOWN,
    NonProjectionReason.SOURCE_ORIGIN_UNKNOWN,
    NonProjectionReason.PROVENANCE_UNKNOWN,
    NonProjectionReason.PROVENANCE_MATERIAL_GAP,
    NonProjectionReason.SUBJECT_RELATION_UNKNOWN,
    NonProjectionReason.SELF_BASIS_UNVERIFIED,
    NonProjectionReason.INTERPRETATION_UNKNOWN,
    NonProjectionReason.CONTEXT_UNKNOWN,
    NonProjectionReason.SCOPE_UNKNOWN,
)
_CONTESTED_ORDER: Final[tuple[NonProjectionReason, ...]] = (
    NonProjectionReason.PROVENANCE_CONFLICTING,
    NonProjectionReason.INTERPRETATION_CONTESTED,
)
_REVISE_ORDER: Final[tuple[NonProjectionReason, ...]] = (
    NonProjectionReason.ATTRIBUTION_REPAIR_REQUIRED,
    NonProjectionReason.CONTEXT_SCOPE_REPAIR_REQUIRED,
)


def _walk_input(value: object):
    if isinstance(value, StrEnum):
        yield ("string", value.value)
        return
    if type(value) is str:
        yield ("string", value)
        return
    if type(value) is tuple:
        yield ("tuple", len(value))
        for item in value:
            yield from _walk_input(item)
        return
    if is_dataclass(value):
        for field in fields(value):
            yield from _walk_input(getattr(value, field.name))
        return
    if value is None or type(value) in {bool, int}:
        return
    raise NonProjectionContractError(
        f"unexpected admitted runtime value type: {type(value).__name__}"
    )


def _local_complexity_exhausted(
    envelope: AttributedInterpretationEnvelope, budget: NonProjectionBudget
) -> bool:
    for kind, item in _walk_input(envelope):
        if kind == "string" and len(item.encode("utf-8")) > budget.max_string_bytes:
            return True
        if kind == "tuple" and item > budget.max_tuple_items:
            return True
    if len(envelope.review_provenance.reviews) > budget.max_review_records:
        return True
    return False


def _effective_independent_review_count(
    envelope: AttributedInterpretationEnvelope,
) -> int:
    reviews = envelope.review_provenance.reviews
    reviewer_counts = Counter(review.reviewer_ref for review in reviews)
    provider_counts = Counter(
        review.provider_ref for review in reviews if review.provider_ref is not None
    )
    prompt_counts = Counter(
        review.prompt_family_ref
        for review in reviews
        if review.prompt_family_ref is not None
    )
    context_counts = Counter(
        review.context_snapshot_ref
        for review in reviews
        if review.context_snapshot_ref is not None
    )

    count = 0
    for review in reviews:
        if review.independence is not ReviewerIndependence.INDEPENDENT:
            continue
        if review.saw_prior_output:
            continue
        if review.provider_ref is None or review.prompt_family_ref is None or review.context_snapshot_ref is None:
            continue
        if reviewer_counts[review.reviewer_ref] != 1:
            continue
        if provider_counts[review.provider_ref] != 1:
            continue
        if prompt_counts[review.prompt_family_ref] != 1:
            continue
        if context_counts[review.context_snapshot_ref] != 1:
            continue
        count += 1
    return count


def _triggered_threats(
    envelope: AttributedInterpretationEnvelope,
    effective_independent_review_count: int,
) -> tuple[NonProjectionThreatId, ...]:
    intent = envelope.projection_intent
    exclusions = envelope.authority_exclusions
    scope = envelope.scope
    triggered: list[NonProjectionThreatId] = []

    if intent.adopt_as_self_experience:
        triggered.append(NonProjectionThreatId.NPG_T01)
    if intent.inherit_source_authority or any((exclusions.capability_authority, exclusions.action_gate_authority, exclusions.retrieval_authority, exclusions.tool_execution_authority)):
        triggered.append(NonProjectionThreatId.NPG_T02)
    if intent.assert_as_objective_truth or exclusions.factual_truth_proof:
        triggered.append(NonProjectionThreatId.NPG_T03)
    if intent.adopt_source_emotion_as_drive:
        triggered.append(NonProjectionThreatId.NPG_T04)
    if intent.style_changes_evidence_status:
        triggered.append(NonProjectionThreatId.NPG_T05)
    if intent.generalize_beyond_scope or not set(intent.proposed_applies_to).issubset(scope.applies_to):
        triggered.append(NonProjectionThreatId.NPG_T06)
    if intent.claimed_independent_review_count > effective_independent_review_count:
        triggered.append(NonProjectionThreatId.NPG_T07)
    if intent.discard_relevant_context:
        triggered.append(NonProjectionThreatId.NPG_T08)
    if intent.inherit_relationship_or_commitment or exclusions.relationship_authority:
        triggered.append(NonProjectionThreatId.NPG_T09)
    if intent.promote_to_stable_identity_trait or exclusions.identity_authority or exclusions.m3_nomination_or_write:
        triggered.append(NonProjectionThreatId.NPG_T10)
    if intent.present_interpretation_as_direct_testimony:
        triggered.append(NonProjectionThreatId.NPG_T11)
    if intent.inherit_consent or exclusions.consent_authority:
        triggered.append(NonProjectionThreatId.NPG_T12)

    return tuple(triggered)


def _context_is_unknown(envelope: AttributedInterpretationEnvelope) -> bool:
    context = envelope.contextual_distance
    return any(level is ContextDistanceLevel.UNKNOWN for level in (context.historical, context.cultural, context.terminology, context.translation_or_paraphrase, context.source_distance)) or context.anachronism_risk is AnachronismRisk.UNKNOWN


def _needs_context_scope_repair(envelope: AttributedInterpretationEnvelope) -> bool:
    if envelope.scope.transfer_limits:
        return False
    context = envelope.contextual_distance
    return (
        envelope.source_provenance.source_class in {SourceClass.HISTORICAL_PRIMARY, SourceClass.HISTORICAL_SECONDARY}
        or any(level is ContextDistanceLevel.HIGH for level in (context.historical, context.cultural, context.terminology, context.translation_or_paraphrase, context.source_distance))
        or context.anachronism_risk is AnachronismRisk.HIGH
    )


def _ordered_present(order: tuple[NonProjectionReason, ...], present: set[NonProjectionReason]) -> tuple[NonProjectionReason, ...]:
    return tuple(reason for reason in order if reason in present)


def classify_non_projection(
    *,
    envelope: AttributedInterpretationEnvelope,
    budget: NonProjectionBudget,
) -> NonProjectionResult:
    """Classify one admitted attributed interpretation without side effects."""

    if type(envelope) is not AttributedInterpretationEnvelope:
        raise NonProjectionContractError("envelope must be exact AttributedInterpretationEnvelope")
    if type(budget) is not NonProjectionBudget:
        raise NonProjectionContractError("budget must be exact NonProjectionBudget")

    effective_count = _effective_independent_review_count(envelope)
    threats = _triggered_threats(envelope, effective_count)

    defer: set[NonProjectionReason] = set()
    contested: set[NonProjectionReason] = set()
    revise: set[NonProjectionReason] = set()

    if envelope.envelope_version != ATTRIBUTED_INTERPRETATION_ENVELOPE_VERSION:
        defer.add(NonProjectionReason.ENVELOPE_VERSION_UNVERIFIED)
    if _local_complexity_exhausted(envelope, budget):
        defer.add(NonProjectionReason.BUDGET_EXHAUSTED)

    provenance = envelope.source_provenance
    if provenance.source_class is SourceClass.UNKNOWN_SOURCE:
        defer.add(NonProjectionReason.SOURCE_CLASS_UNKNOWN)
    if provenance.source_origin is SourceOrigin.UNKNOWN:
        defer.add(NonProjectionReason.SOURCE_ORIGIN_UNKNOWN)
    if provenance.provenance_state is ProvenanceState.UNKNOWN:
        defer.add(NonProjectionReason.PROVENANCE_UNKNOWN)
    elif provenance.provenance_state is ProvenanceState.PARTIAL and provenance.material_gaps:
        defer.add(NonProjectionReason.PROVENANCE_MATERIAL_GAP)

    relation = envelope.attribution.subject_relation
    if relation is SubjectRelation.UNKNOWN:
        defer.add(NonProjectionReason.SUBJECT_RELATION_UNKNOWN)
    elif relation is SubjectRelation.VERIFIED_SELF:
        defer.add(NonProjectionReason.SELF_BASIS_UNVERIFIED)

    if envelope.interpretation.state is InterpretationState.UNKNOWN:
        defer.add(NonProjectionReason.INTERPRETATION_UNKNOWN)
    if _context_is_unknown(envelope):
        defer.add(NonProjectionReason.CONTEXT_UNKNOWN)
    if set(envelope.projection_intent.proposed_applies_to) & set(envelope.scope.unknowns):
        defer.add(NonProjectionReason.SCOPE_UNKNOWN)

    if provenance.provenance_state is ProvenanceState.CONFLICTING:
        contested.add(NonProjectionReason.PROVENANCE_CONFLICTING)
    if envelope.interpretation.state is InterpretationState.CONTESTED:
        contested.add(NonProjectionReason.INTERPRETATION_CONTESTED)

    if envelope.claim.claim_class in {ClaimClass.AUTOBIOGRAPHICAL_TESTIMONY, ClaimClass.RELATIONSHIP_TESTIMONY, ClaimClass.CONSENT_STATEMENT} and provenance.source_actor_ref is None:
        revise.add(NonProjectionReason.ATTRIBUTION_REPAIR_REQUIRED)
    if _needs_context_scope_repair(envelope):
        revise.add(NonProjectionReason.CONTEXT_SCOPE_REPAIR_REQUIRED)

    fingerprint: str | None = None
    if canonical_json_contract.PROFILE_NAME != CANONICAL_PROFILE:
        defer.add(NonProjectionReason.CANONICALIZATION_FAILED)
    else:
        canonical_input = {
            "domain": INPUT_FINGERPRINT_DOMAIN,
            "non_projection_contract_version": NON_PROJECTION_CONTRACT_VERSION,
            "envelope_version": envelope.envelope_version,
            "canonical_profile": CANONICAL_PROFILE,
            "source_provenance_scope": SOURCE_PROVENANCE_SCOPE,
            "envelope": envelope.to_value(),
            "budget": budget.to_value(),
        }
        try:
            canonical_bytes = canonical_json_contract.canonical_json_bytes(canonical_input)
        except (canonical_json_contract.CanonicalJSONError, UnicodeEncodeError):
            defer.add(NonProjectionReason.CANONICALIZATION_FAILED)
        else:
            if len(canonical_bytes) > HARD_MAX_CANONICAL_INPUT_BYTES:
                raise NonProjectionContractError("canonical input exceeds HARD_MAX_CANONICAL_INPUT_BYTES")
            if len(canonical_bytes) > budget.max_canonical_input_bytes:
                defer.add(NonProjectionReason.BUDGET_EXHAUSTED)
            else:
                fingerprint = hashlib.sha256(canonical_bytes).hexdigest()

    reject_reasons = tuple(_THREAT_REASON[threat] for threat in threats)
    defer_reasons = _ordered_present(_DEFER_ORDER, defer)
    contested_reasons = _ordered_present(_CONTESTED_ORDER, contested)
    revise_reasons = _ordered_present(_REVISE_ORDER, revise)

    if reject_reasons:
        decision = NonProjectionDecision.REJECT
        reasons = reject_reasons + defer_reasons + contested_reasons + revise_reasons
    elif defer_reasons:
        decision = NonProjectionDecision.DEFER
        reasons = defer_reasons + contested_reasons + revise_reasons
    elif contested_reasons:
        decision = NonProjectionDecision.CONTESTED
        reasons = contested_reasons + revise_reasons
    elif revise_reasons:
        decision = NonProjectionDecision.REVISE_REQUIRED
        reasons = revise_reasons
    else:
        if fingerprint is None:
            return NonProjectionResult(decision=NonProjectionDecision.DEFER, primary_reason=NonProjectionReason.CANONICALIZATION_FAILED, reasons=(NonProjectionReason.CANONICALIZATION_FAILED,), triggered_threat_ids=(), effective_independent_review_count=effective_count, input_fingerprint=None)
        decision = NonProjectionDecision.PASS_ATTRIBUTED
        reasons = (NonProjectionReason.PASS_ATTRIBUTED,)

    return NonProjectionResult(
        decision=decision,
        primary_reason=reasons[0],
        reasons=reasons,
        triggered_threat_ids=threats,
        effective_independent_review_count=effective_count,
        input_fingerprint=fingerprint,
    )
