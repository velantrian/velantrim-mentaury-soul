"""Pure fail-closed P1-002 privacy reconciliation classification."""

from __future__ import annotations

from typing import Final

from mentaury.contracts import CanonicalJSONError, canonical_json_bytes

from .contracts import (
    CopyState,
    MaterialState,
    PrivacyAccessIntent,
    PrivacyClass,
    PrivacyContractError,
    PrivacyCopy,
    PrivacyDecision,
    PrivacyMaterial,
    PrivacyReason,
    PrivacyReconciliationBudget,
    PrivacyReconciliationResult,
    SurfaceKind,
)

_DERIVED_SURFACES: Final[frozenset[SurfaceKind]] = frozenset(
    {
        SurfaceKind.INDEX,
        SurfaceKind.EMBEDDING,
        SurfaceKind.GRAPH_EDGE,
        SurfaceKind.CACHE,
        SurfaceKind.DERIVED_SUMMARY,
    }
)
_BRANCH_SURFACES: Final[frozenset[SurfaceKind]] = frozenset(
    {SurfaceKind.BACKUP, SurfaceKind.FORK}
)


def _result(
    decision: PrivacyDecision, reason: PrivacyReason
) -> PrivacyReconciliationResult:
    return PrivacyReconciliationResult(decision=decision, reason=reason)


def _surface_result(
    surface: SurfaceKind, reason: PrivacyReason
) -> PrivacyReconciliationResult:
    if surface in _BRANCH_SURFACES:
        return _result(PrivacyDecision.QUARANTINE_REQUIRED, reason)
    if surface in _DERIVED_SURFACES:
        return _result(PrivacyDecision.REBUILD_REQUIRED, reason)
    return _result(PrivacyDecision.DENY_RETRIEVAL, reason)


def classify_privacy_reconciliation(
    material: PrivacyMaterial | object,
    copy: PrivacyCopy | object,
    intent: PrivacyAccessIntent | object,
    budget: PrivacyReconciliationBudget | object,
) -> PrivacyReconciliationResult:
    """Classify one caller-supplied privacy copy without performing any action.

    Strict admission exceptions represent ``INPUT_CONTRACT_VIOLATION`` from the
    frozen contract. Empty purpose and branch allowlists grant nothing; they
    are never interpreted as wildcard authority.
    """

    admitted_material = PrivacyMaterial.from_value(material)
    admitted_copy = PrivacyCopy.from_value(copy)
    admitted_intent = PrivacyAccessIntent.from_value(intent)
    admitted_budget = PrivacyReconciliationBudget.from_value(budget)

    if admitted_copy.material_id != admitted_material.material_id:
        raise PrivacyContractError("copy.material_id must equal material.material_id")
    if admitted_intent.copy_id != admitted_copy.copy_id:
        raise PrivacyContractError("intent.copy_id must equal copy.copy_id")
    if admitted_intent.branch_id != admitted_copy.branch_id:
        raise PrivacyContractError("intent.branch_id must equal copy.branch_id")
    if admitted_copy.policy_revision > admitted_material.policy_revision:
        raise PrivacyContractError(
            "copy.policy_revision cannot be ahead of material.policy_revision"
        )

    canonical_input = {
        "material": admitted_material.to_value(),
        "copy": admitted_copy.to_value(),
        "intent": admitted_intent.to_value(),
    }
    try:
        serialized_size = len(canonical_json_bytes(canonical_input))
    except (CanonicalJSONError, UnicodeEncodeError) as exc:
        raise PrivacyContractError(
            "material, copy, and intent must be canonical JSON values"
        ) from exc

    purpose_count = len(admitted_material.permitted_purposes) + len(
        admitted_material.withdrawn_purposes
    )
    branch_count = len(admitted_material.permitted_branches)
    if (
        serialized_size > admitted_budget.max_serialized_bytes
        or purpose_count > admitted_budget.max_purposes
        or branch_count > admitted_budget.max_branches
    ):
        return _result(
            PrivacyDecision.DENY_RETRIEVAL, PrivacyReason.BUDGET_EXHAUSTED
        )

    if admitted_copy.state is CopyState.ABSENT:
        return _result(PrivacyDecision.DENY_RETRIEVAL, PrivacyReason.COPY_ABSENT)

    if admitted_copy.state is CopyState.QUARANTINED:
        return _result(
            PrivacyDecision.QUARANTINE_REQUIRED,
            PrivacyReason.COPY_ALREADY_QUARANTINED,
        )

    if (
        admitted_material.state in {MaterialState.DELETED, MaterialState.REDACTED}
        or admitted_material.privacy_class is PrivacyClass.REDACTED
    ):
        return _surface_result(
            admitted_copy.surface, PrivacyReason.DELETED_OR_REDACTED_MATERIAL
        )

    if (
        admitted_material.privacy_class is PrivacyClass.THIRD_PARTY
        and not admitted_material.third_party_permission
    ):
        return _surface_result(
            admitted_copy.surface, PrivacyReason.THIRD_PARTY_PERMISSION_MISSING
        )

    if admitted_intent.purpose in admitted_material.withdrawn_purposes:
        return _surface_result(admitted_copy.surface, PrivacyReason.PURPOSE_WITHDRAWN)

    if admitted_intent.purpose not in admitted_material.permitted_purposes:
        return _surface_result(
            admitted_copy.surface, PrivacyReason.PURPOSE_NOT_PERMITTED
        )

    if admitted_intent.branch_id not in admitted_material.permitted_branches:
        return _surface_result(
            admitted_copy.surface, PrivacyReason.BRANCH_NOT_PERMITTED
        )

    if admitted_copy.policy_revision < admitted_material.policy_revision:
        return _surface_result(
            admitted_copy.surface, PrivacyReason.STALE_POLICY_REVISION
        )

    return _result(
        PrivacyDecision.ALLOW_REFERENCE, PrivacyReason.ALLOW_REFERENCE
    )
