"""Pure deterministic P1-003 governed constraint composition."""

from __future__ import annotations

import hashlib
from enum import StrEnum
from typing import Final

from mentaury.capabilities import (
    RESOLVER_CONTRACT_VERSION,
    ActionIntent,
    LeaseStatus,
    ResolutionDecision,
    ResolutionReason,
    ResolutionResult,
    resolve_capability_lease,
)
from mentaury.contracts import PROFILE_NAME, CanonicalJSONError, canonical_json_bytes
from mentaury.privacy.reconciliation import (
    CLASSIFIER_CONTRACT_VERSION,
    PrivacyAccessIntent,
    PrivacyContractError,
    PrivacyDecision,
    PrivacyReason,
    PrivacyReconciliationResult,
    classify_privacy_reconciliation,
)

from .contracts import (
    BINDING_CONTRACT_VERSION,
    CANONICAL_PROFILE,
    COMMON_REQUEST_DOMAIN,
    COMPOSER_CONTRACT_VERSION,
    EVALUATION_EVIDENCE_DOMAIN,
    P1_001_EXPECTED_VERSION,
    P1_002_EXPECTED_VERSION,
    SOURCE_PROVENANCE_SCOPE,
    CrossGateEvaluationContext,
    GovernedConstraintContractError,
    GovernedConstraintDecision,
    GovernedConstraintReason,
    GovernedConstraintResult,
)


class _Disposition(StrEnum):
    POSITIVE = "POSITIVE"
    BLOCKER = "BLOCKER"
    DEFER = "DEFER"


_CAPABILITY_DEFER_REASONS: Final[frozenset[ResolutionReason]] = frozenset(
    {
        ResolutionReason.REQUEST_INVALID,
        ResolutionReason.BUDGET_MISSING,
        ResolutionReason.BUDGET_EXHAUSTED,
        ResolutionReason.REGISTRY_UNAVAILABLE,
        ResolutionReason.REGISTRY_CONTRACT_VIOLATION,
        ResolutionReason.UNKNOWN_LEASE,
        ResolutionReason.LEASE_CONTRACT_VIOLATION,
    }
)
_CAPABILITY_BLOCK_REASONS: Final[frozenset[ResolutionReason]] = frozenset(
    {
        ResolutionReason.REVISION_MISMATCH,
        ResolutionReason.LEASE_DIGEST_MISMATCH,
        ResolutionReason.LEASE_REVOKED,
        ResolutionReason.LEASE_EXPIRED,
        ResolutionReason.NOT_YET_VALID,
        ResolutionReason.PURPOSE_MISMATCH,
        ResolutionReason.OPERATION_NOT_ALLOWED,
        ResolutionReason.DATA_SCOPE_VIOLATION,
        ResolutionReason.SIDE_EFFECT_NOT_ALLOWED,
    }
)
_PRIVACY_BLOCK_REASONS: Final[frozenset[PrivacyReason]] = frozenset(
    {
        PrivacyReason.COPY_ABSENT,
        PrivacyReason.COPY_ALREADY_QUARANTINED,
        PrivacyReason.DELETED_OR_REDACTED_MATERIAL,
        PrivacyReason.THIRD_PARTY_PERMISSION_MISSING,
        PrivacyReason.PURPOSE_WITHDRAWN,
        PrivacyReason.PURPOSE_NOT_PERMITTED,
        PrivacyReason.BRANCH_NOT_PERMITTED,
        PrivacyReason.STALE_POLICY_REVISION,
    }
)


def compose_governed_constraints(
    *,
    context: CrossGateEvaluationContext,
) -> GovernedConstraintResult:
    """Return bounded next-gate eligibility from one immutable same-attempt context."""

    if type(context) is not CrossGateEvaluationContext:
        raise GovernedConstraintContractError(
            "context must be exact CrossGateEvaluationContext"
        )

    if (
        len(context.data_scope) > context.composition_budget.max_scope_items
        or len(context.requested_side_effects)
        > context.composition_budget.max_side_effects
    ):
        return _result(
            GovernedConstraintDecision.DEFER,
            GovernedConstraintReason.COMPOSITION_BUDGET_EXHAUSTED,
        )

    try:
        common_bytes = canonical_json_bytes(_common_request_value(context))
    except (CanonicalJSONError, TypeError, ValueError, UnicodeEncodeError):
        return _result(
            GovernedConstraintDecision.NOT_ELIGIBLE,
            GovernedConstraintReason.BINDING_CANONICALIZATION_FAILED,
        )

    if len(common_bytes) > context.composition_budget.max_common_request_bytes:
        return _result(
            GovernedConstraintDecision.DEFER,
            GovernedConstraintReason.COMPOSITION_BUDGET_EXHAUSTED,
        )

    common_fingerprint = hashlib.sha256(common_bytes).hexdigest()

    if not _live_versions_verified():
        return _result(
            GovernedConstraintDecision.DEFER,
            GovernedConstraintReason.GATE_VERSION_UNVERIFIED,
            common_request_fingerprint=common_fingerprint,
        )

    try:
        action_intent = ActionIntent(
            purpose_id=context.purpose_id,
            operation_id=context.operation_id,
            data_scope=context.data_scope,
            requested_side_effects=context.requested_side_effects,
        )
        privacy_intent = PrivacyAccessIntent(
            copy_id=context.privacy_copy.copy_id,
            branch_id=context.branch_id,
            purpose=context.purpose_id,
        )
    except (TypeError, ValueError, PrivacyContractError):
        return _result(
            GovernedConstraintDecision.DEFER,
            GovernedConstraintReason.GATE_CONTRACT_UNVERIFIED,
            common_request_fingerprint=common_fingerprint,
        )

    try:
        capability_result = resolve_capability_lease(
            registry_snapshot=context.registry_snapshot,
            authority_ref=context.authority_ref,
            action_intent=action_intent,
            evaluated_at=context.evaluated_at,
            resolution_budget=context.capability_budget,
        )
    except Exception:
        return _result(
            GovernedConstraintDecision.DEFER,
            GovernedConstraintReason.GATE_CONTRACT_UNVERIFIED,
            common_request_fingerprint=common_fingerprint,
        )

    try:
        privacy_result = classify_privacy_reconciliation(
            context.privacy_material,
            context.privacy_copy,
            privacy_intent,
            context.privacy_budget,
        )
    except PrivacyContractError:
        return _result(
            GovernedConstraintDecision.DEFER,
            GovernedConstraintReason.GATE_CONTRACT_UNVERIFIED,
            common_request_fingerprint=common_fingerprint,
            capability_result=(
                capability_result
                if type(capability_result) is ResolutionResult
                else None
            ),
        )
    except Exception:
        return _result(
            GovernedConstraintDecision.DEFER,
            GovernedConstraintReason.GATE_CONTRACT_UNVERIFIED,
            common_request_fingerprint=common_fingerprint,
            capability_result=(
                capability_result
                if type(capability_result) is ResolutionResult
                else None
            ),
        )

    if type(capability_result) is not ResolutionResult or type(
        privacy_result
    ) is not PrivacyReconciliationResult:
        return _result(
            GovernedConstraintDecision.DEFER,
            GovernedConstraintReason.GATE_CONTRACT_UNVERIFIED,
            common_request_fingerprint=common_fingerprint,
        )

    if capability_result.resolver_contract_version != P1_001_EXPECTED_VERSION:
        return _result(
            GovernedConstraintDecision.DEFER,
            GovernedConstraintReason.GATE_VERSION_UNVERIFIED,
            common_request_fingerprint=common_fingerprint,
            capability_result=capability_result,
            privacy_result=privacy_result,
        )

    if not _common_binding_matches(context, capability_result):
        return _result(
            GovernedConstraintDecision.NOT_ELIGIBLE,
            GovernedConstraintReason.COMMON_BINDING_MISMATCH,
            common_request_fingerprint=common_fingerprint,
            capability_result=capability_result,
            privacy_result=privacy_result,
        )

    try:
        evidence_bytes = canonical_json_bytes(
            _evaluation_evidence_value(
                context=context,
                common_request_fingerprint=common_fingerprint,
                privacy_intent=privacy_intent,
                capability_result=capability_result,
                privacy_result=privacy_result,
            )
        )
    except (CanonicalJSONError, TypeError, ValueError, UnicodeEncodeError):
        return _result(
            GovernedConstraintDecision.NOT_ELIGIBLE,
            GovernedConstraintReason.EVIDENCE_CANONICALIZATION_FAILED,
            common_request_fingerprint=common_fingerprint,
            capability_result=capability_result,
            privacy_result=privacy_result,
        )

    if len(evidence_bytes) > context.composition_budget.max_evidence_bytes:
        return _result(
            GovernedConstraintDecision.DEFER,
            GovernedConstraintReason.COMPOSITION_BUDGET_EXHAUSTED,
            common_request_fingerprint=common_fingerprint,
            capability_result=capability_result,
            privacy_result=privacy_result,
        )

    evidence_fingerprint = hashlib.sha256(evidence_bytes).hexdigest()
    capability_disposition = _capability_disposition(capability_result)
    privacy_disposition = _privacy_disposition(privacy_result)

    if capability_disposition is None or privacy_disposition is None:
        return _result(
            GovernedConstraintDecision.DEFER,
            GovernedConstraintReason.GATE_CONTRACT_UNVERIFIED,
            common_request_fingerprint=common_fingerprint,
            evaluation_evidence_fingerprint=evidence_fingerprint,
            capability_result=capability_result,
            privacy_result=privacy_result,
        )

    decision, reason = _compose_dispositions(
        capability_disposition,
        privacy_disposition,
    )
    return _result(
        decision,
        reason,
        common_request_fingerprint=common_fingerprint,
        evaluation_evidence_fingerprint=evidence_fingerprint,
        capability_result=capability_result,
        privacy_result=privacy_result,
    )


def _result(
    decision: GovernedConstraintDecision,
    reason: GovernedConstraintReason,
    *,
    common_request_fingerprint: str | None = None,
    evaluation_evidence_fingerprint: str | None = None,
    capability_result: ResolutionResult | None = None,
    privacy_result: PrivacyReconciliationResult | None = None,
) -> GovernedConstraintResult:
    return GovernedConstraintResult(
        decision=decision,
        primary_reason=reason,
        common_request_fingerprint=common_request_fingerprint,
        evaluation_evidence_fingerprint=evaluation_evidence_fingerprint,
        capability_result=capability_result,
        privacy_result=privacy_result,
    )


def _live_versions_verified() -> bool:
    return (
        RESOLVER_CONTRACT_VERSION == P1_001_EXPECTED_VERSION
        and CLASSIFIER_CONTRACT_VERSION == P1_002_EXPECTED_VERSION
        and PROFILE_NAME == CANONICAL_PROFILE
    )


def _common_request_value(context: CrossGateEvaluationContext) -> dict[str, object]:
    return {
        "domain": COMMON_REQUEST_DOMAIN,
        "composer_contract_version": COMPOSER_CONTRACT_VERSION,
        "binding_contract_version": BINDING_CONTRACT_VERSION,
        "canonical_profile": CANONICAL_PROFILE,
        "request_id": context.request_id,
        "purpose_id": context.purpose_id,
        "operation_id": context.operation_id,
        "data_scope": [item.to_value() for item in context.data_scope],
        "requested_side_effects": list(context.requested_side_effects),
        "branch_id": context.branch_id,
        "material_id": context.privacy_material.material_id,
        "copy_id": context.privacy_copy.copy_id,
        "capability_lease_id": context.authority_ref.capability_lease_id,
        "capability_revision": context.authority_ref.capability_revision,
    }


def _targeted_capability_source(
    context: CrossGateEvaluationContext,
) -> dict[str, object]:
    snapshot = context.registry_snapshot
    lease_id = context.authority_ref.capability_lease_id
    revision = context.authority_ref.capability_revision
    return {
        "registry_availability": snapshot.availability.value,
        "registry_unavailable_reason": snapshot.unavailable_reason,
        "registry_schema_version": snapshot.registry_schema_version,
        "requested_capability_lease_id": lease_id,
        "requested_capability_revision": revision,
        "observed_live_revision": snapshot.live_heads.get(lease_id),
        "requested_record": snapshot.record_for(lease_id, revision),
    }


def _privacy_source(
    context: CrossGateEvaluationContext,
    privacy_intent: PrivacyAccessIntent,
) -> dict[str, object]:
    return {
        "privacy_material": context.privacy_material.to_value(),
        "privacy_copy": context.privacy_copy.to_value(),
        "privacy_intent": privacy_intent.to_value(),
        "privacy_budget": context.privacy_budget.to_value(),
    }


def _evaluation_evidence_value(
    *,
    context: CrossGateEvaluationContext,
    common_request_fingerprint: str,
    privacy_intent: PrivacyAccessIntent,
    capability_result: ResolutionResult,
    privacy_result: PrivacyReconciliationResult,
) -> dict[str, object]:
    return {
        "domain": EVALUATION_EVIDENCE_DOMAIN,
        "composer_contract_version": COMPOSER_CONTRACT_VERSION,
        "binding_contract_version": BINDING_CONTRACT_VERSION,
        "canonical_profile": CANONICAL_PROFILE,
        "source_provenance_scope": SOURCE_PROVENANCE_SCOPE,
        "common_request_fingerprint": common_request_fingerprint,
        "evaluated_at": context.evaluated_at,
        "p1_001_contract_version": RESOLVER_CONTRACT_VERSION,
        "p1_002_contract_version": CLASSIFIER_CONTRACT_VERSION,
        "capability_budget": context.capability_budget.to_value(),
        "privacy_budget": context.privacy_budget.to_value(),
        "composition_budget": context.composition_budget.to_value(),
        "targeted_capability_source": _targeted_capability_source(context),
        "privacy_source": _privacy_source(context, privacy_intent),
        "capability_result": capability_result.to_value(),
        "privacy_result": privacy_result.to_value(),
    }


def _common_binding_matches(
    context: CrossGateEvaluationContext,
    capability_result: ResolutionResult,
) -> bool:
    return (
        capability_result.lease_id == context.authority_ref.capability_lease_id
        and capability_result.requested_revision
        == context.authority_ref.capability_revision
        and capability_result.evaluated_at == context.evaluated_at
    )


def _capability_disposition(result: ResolutionResult) -> _Disposition | None:
    if (
        result.decision is ResolutionDecision.ALLOW
        and result.primary_reason is ResolutionReason.ALLOW
    ):
        return _Disposition.POSITIVE
    if result.primary_reason in _CAPABILITY_DEFER_REASONS:
        return _Disposition.DEFER
    if result.primary_reason is ResolutionReason.LEASE_NOT_ACTIVE:
        return (
            _Disposition.DEFER
            if result.observed_status is LeaseStatus.UNVERIFIED
            else _Disposition.BLOCKER
        )
    if result.primary_reason in _CAPABILITY_BLOCK_REASONS:
        return _Disposition.BLOCKER
    return None


def _privacy_disposition(
    result: PrivacyReconciliationResult,
) -> _Disposition | None:
    if (
        result.decision is PrivacyDecision.ALLOW_REFERENCE
        and result.reason is PrivacyReason.ALLOW_REFERENCE
    ):
        return _Disposition.POSITIVE
    if result.reason is PrivacyReason.BUDGET_EXHAUSTED:
        return _Disposition.DEFER
    if result.reason in _PRIVACY_BLOCK_REASONS:
        return _Disposition.BLOCKER
    return None


def _compose_dispositions(
    capability: _Disposition,
    privacy: _Disposition,
) -> tuple[GovernedConstraintDecision, GovernedConstraintReason]:
    if capability is _Disposition.BLOCKER and privacy is _Disposition.BLOCKER:
        return (
            GovernedConstraintDecision.NOT_ELIGIBLE,
            GovernedConstraintReason.CAPABILITY_AND_PRIVACY_BLOCKED,
        )
    if capability is _Disposition.BLOCKER:
        return (
            GovernedConstraintDecision.NOT_ELIGIBLE,
            GovernedConstraintReason.CAPABILITY_BLOCKED,
        )
    if privacy is _Disposition.BLOCKER:
        return (
            GovernedConstraintDecision.NOT_ELIGIBLE,
            GovernedConstraintReason.PRIVACY_BLOCKED,
        )
    if capability is _Disposition.DEFER and privacy is _Disposition.DEFER:
        return (
            GovernedConstraintDecision.DEFER,
            GovernedConstraintReason.CAPABILITY_AND_PRIVACY_DEFERRED,
        )
    if capability is _Disposition.DEFER:
        return (
            GovernedConstraintDecision.DEFER,
            GovernedConstraintReason.CAPABILITY_DEFERRED,
        )
    if privacy is _Disposition.DEFER:
        return (
            GovernedConstraintDecision.DEFER,
            GovernedConstraintReason.PRIVACY_DEFERRED,
        )
    return (
        GovernedConstraintDecision.ELIGIBLE_FOR_NEXT_GATE,
        GovernedConstraintReason.ELIGIBLE_FOR_NEXT_GATE,
    )


__all__ = ["compose_governed_constraints"]
