"""Pure deterministic ATR-v0.1 typed-relation representation."""

from __future__ import annotations

from hashlib import sha256

from mentaury.contracts import canonical_json

from .contracts import (
    CANONICAL_PROFILE,
    HARD_MAX_CANONICAL_INPUT_BYTES,
    INPUT_FINGERPRINT_DOMAIN,
    TYPED_RELATION_CONTRACT_VERSION,
    AnchoredTypedRelationRecord,
    ClaimAnchor,
    RelationEndpoints,
    RelationOrientation,
    RelationProvenance,
    RelationRepresentationBudget,
    RelationScope,
    RelationSemantics,
    ScopeReference,
    TypedRelationBudgetExceeded,
    TypedRelationContractError,
)


def _require_exact(value: object, expected: type[object], name: str) -> None:
    if type(value) is not expected:
        raise TypedRelationContractError(
            f"{name} must be exact {expected.__name__}"
        )


def _anchor_key(anchor: ClaimAnchor) -> tuple[str, str]:
    return (anchor.claim_id, anchor.claim_input_fingerprint)


def _check_cross_input_invariants(
    *,
    endpoints: RelationEndpoints,
    semantics: RelationSemantics,
    provenance: RelationProvenance,
) -> None:
    if semantics.orientation is RelationOrientation.SYMMETRIC:
        if _anchor_key(endpoints.left_anchor) > _anchor_key(endpoints.right_anchor):
            raise TypedRelationContractError(
                "symmetric endpoints must already be canonically sorted"
            )

    source_anchor = provenance.source_assertion_anchor
    if source_anchor is not None and source_anchor in (
        endpoints.left_anchor,
        endpoints.right_anchor,
    ):
        raise TypedRelationContractError(
            "source_assertion_anchor must be distinct from both endpoints"
        )


def _check_string_budget(
    value: str | None, *, name: str, budget: RelationRepresentationBudget
) -> None:
    if value is None:
        return
    if len(value.encode("utf-8")) > budget.max_string_bytes:
        raise TypedRelationBudgetExceeded(
            f"{name} exceeds local max_string_bytes"
        )


def _check_anchor_budget(
    anchor: ClaimAnchor, *, name: str, budget: RelationRepresentationBudget
) -> None:
    _check_string_budget(anchor.claim_id, name=f"{name}.claim_id", budget=budget)
    _check_string_budget(
        anchor.claim_input_fingerprint,
        name=f"{name}.claim_input_fingerprint",
        budget=budget,
    )


def _check_anchor_tuple_budget(
    anchors: tuple[ClaimAnchor, ...],
    *,
    name: str,
    budget: RelationRepresentationBudget,
) -> None:
    if len(anchors) > budget.max_tuple_items:
        raise TypedRelationBudgetExceeded(
            f"{name} exceeds local max_tuple_items"
        )
    for index, anchor in enumerate(anchors):
        _check_anchor_budget(anchor, name=f"{name}[{index}]", budget=budget)


def _check_scope_reference_budget(
    reference: ScopeReference,
    *,
    name: str,
    budget: RelationRepresentationBudget,
) -> None:
    _check_string_budget(reference.kind.value, name=f"{name}.kind", budget=budget)
    _check_string_budget(
        reference.reference_id, name=f"{name}.reference_id", budget=budget
    )
    _check_string_budget(
        reference.claim_input_fingerprint,
        name=f"{name}.claim_input_fingerprint",
        budget=budget,
    )


def _check_scope_tuple_budget(
    references: tuple[ScopeReference, ...],
    *,
    name: str,
    budget: RelationRepresentationBudget,
) -> None:
    if len(references) > budget.max_tuple_items:
        raise TypedRelationBudgetExceeded(
            f"{name} exceeds local max_tuple_items"
        )
    for index, reference in enumerate(references):
        _check_scope_reference_budget(
            reference,
            name=f"{name}[{index}]",
            budget=budget,
        )


def _check_local_budget(
    *,
    endpoints: RelationEndpoints,
    semantics: RelationSemantics,
    provenance: RelationProvenance,
    scope: RelationScope,
    budget: RelationRepresentationBudget,
) -> None:
    _check_string_budget(
        TYPED_RELATION_CONTRACT_VERSION,
        name="contract_version",
        budget=budget,
    )
    _check_anchor_budget(
        endpoints.left_anchor, name="endpoints.left_anchor", budget=budget
    )
    _check_anchor_budget(
        endpoints.right_anchor, name="endpoints.right_anchor", budget=budget
    )
    _check_string_budget(
        semantics.relation_type.value,
        name="semantics.relation_type",
        budget=budget,
    )
    _check_string_budget(
        semantics.orientation.value,
        name="semantics.orientation",
        budget=budget,
    )
    _check_string_budget(
        provenance.origin.value, name="provenance.origin", budget=budget
    )
    _check_string_budget(
        provenance.origin_actor_ref,
        name="provenance.origin_actor_ref",
        budget=budget,
    )
    if provenance.source_assertion_anchor is not None:
        _check_anchor_budget(
            provenance.source_assertion_anchor,
            name="provenance.source_assertion_anchor",
            budget=budget,
        )
    _check_anchor_tuple_budget(
        provenance.basis_anchors,
        name="provenance.basis_anchors",
        budget=budget,
    )
    for name in (
        "conditions",
        "moderators",
        "exceptions",
        "unknowns",
        "transfer_limits",
    ):
        _check_scope_tuple_budget(
            getattr(scope, name), name=f"scope.{name}", budget=budget
        )


def _canonical_input_bytes(
    *,
    endpoints: RelationEndpoints,
    semantics: RelationSemantics,
    provenance: RelationProvenance,
    scope: RelationScope,
    budget: RelationRepresentationBudget,
) -> bytes:
    if canonical_json.PROFILE_NAME != CANONICAL_PROFILE:
        raise TypedRelationContractError(
            "STOP_AND_RECONCILE: canonical JSON profile drift"
        )
    try:
        encoded = canonical_json.canonical_json_bytes(
            {
                "contract_version": TYPED_RELATION_CONTRACT_VERSION,
                "endpoints": endpoints.to_value(),
                "semantics": semantics.to_value(),
                "provenance": provenance.to_value(),
                "scope": scope.to_value(),
                "budget": budget.to_value(),
            }
        )
    except (TypeError, ValueError) as exc:
        raise TypedRelationContractError(
            "canonicalization failed for admitted ATR-v0.1 input"
        ) from exc

    if len(encoded) > HARD_MAX_CANONICAL_INPUT_BYTES:
        raise TypedRelationContractError(
            "canonical input exceeds HARD_MAX_CANONICAL_INPUT_BYTES"
        )
    if len(encoded) > budget.max_canonical_input_bytes:
        raise TypedRelationBudgetExceeded(
            "canonical input exceeds local max_canonical_input_bytes"
        )
    return encoded


def represent_typed_relation(
    *,
    endpoints: RelationEndpoints,
    semantics: RelationSemantics,
    provenance: RelationProvenance,
    scope: RelationScope,
    budget: RelationRepresentationBudget,
) -> AnchoredTypedRelationRecord:
    """Represent one exact caller-supplied relation candidate deterministically."""

    _require_exact(endpoints, RelationEndpoints, "endpoints")
    _require_exact(semantics, RelationSemantics, "semantics")
    _require_exact(provenance, RelationProvenance, "provenance")
    _require_exact(scope, RelationScope, "scope")
    _require_exact(budget, RelationRepresentationBudget, "budget")

    _check_cross_input_invariants(
        endpoints=endpoints,
        semantics=semantics,
        provenance=provenance,
    )
    _check_local_budget(
        endpoints=endpoints,
        semantics=semantics,
        provenance=provenance,
        scope=scope,
        budget=budget,
    )
    encoded = _canonical_input_bytes(
        endpoints=endpoints,
        semantics=semantics,
        provenance=provenance,
        scope=scope,
        budget=budget,
    )
    fingerprint = sha256(
        INPUT_FINGERPRINT_DOMAIN.encode("ascii") + b"\x00" + encoded
    ).hexdigest()

    return AnchoredTypedRelationRecord(
        contract_version=TYPED_RELATION_CONTRACT_VERSION,
        endpoints=endpoints,
        semantics=semantics,
        provenance=provenance,
        scope=scope,
        input_fingerprint=fingerprint,
    )
