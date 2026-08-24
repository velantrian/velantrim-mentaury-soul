"""Pure deterministic EPR-v0.1 epistemic change router."""

from __future__ import annotations

from hashlib import sha256

from mentaury.beliefs.contracts import belief_status_transition_allowed
from mentaury.claims import ProvenanceClaimRecord
from mentaury.contracts import canonical_json

from .contracts import (
    CANONICAL_PROFILE,
    EPISTEMIC_CHANGE_CONTRACT_VERSION,
    HARD_MAX_CANONICAL_INPUT_BYTES,
    INPUT_FINGERPRINT_DOMAIN,
    BeliefBinding,
    EpistemicChangeBindingError,
    EpistemicChangeBudget,
    EpistemicChangeBudgetExceeded,
    EpistemicChangeContractError,
    EpistemicChangePlan,
    EpistemicChangeRequest,
    EpistemicIntent,
    EpistemicOwner,
    EpistemicRoute,
    EpistemicRouteReason,
)


def route_epistemic_change(
    *,
    record: ProvenanceClaimRecord,
    belief: BeliefBinding | None,
    request: EpistemicChangeRequest,
    budget: EpistemicChangeBudget,
) -> EpistemicChangePlan:
    """Return the next owner/prerequisite without performing the route."""

    if type(record) is not ProvenanceClaimRecord:
        raise TypeError("record must be exact ProvenanceClaimRecord")
    if belief is not None and type(belief) is not BeliefBinding:
        raise TypeError("belief must be exact BeliefBinding or None")
    if type(request) is not EpistemicChangeRequest:
        raise TypeError("request must be exact EpistemicChangeRequest")
    if type(budget) is not EpistemicChangeBudget:
        raise TypeError("budget must be exact EpistemicChangeBudget")

    if belief is not None:
        _verify_binding(record, belief)

    canonical_input = {
        "contract_version": EPISTEMIC_CHANGE_CONTRACT_VERSION,
        "record": record.to_value(),
        "belief": belief.to_value() if belief is not None else None,
        "request": request.to_value(),
        "budget": budget.to_value(),
    }
    _check_local_budget(canonical_input, budget)
    fingerprint = _routing_fingerprint(canonical_input, budget)
    route, owner, reason = _route(belief, request.intent)
    return EpistemicChangePlan(
        contract_version=EPISTEMIC_CHANGE_CONTRACT_VERSION,
        request_id=request.request_id,
        route=route,
        next_owner=owner,
        reason=reason,
        record_fingerprint=record.input_fingerprint,
        belief_id=belief.belief_id if belief is not None else None,
        belief_revision=belief.belief_revision if belief is not None else None,
        routing_input_fingerprint=fingerprint,
    )


def _verify_binding(record: ProvenanceClaimRecord, belief: BeliefBinding) -> None:
    if belief.claim_id != record.claim.claim_id:
        raise EpistemicChangeBindingError(
            "belief claim_id does not match exact PCR record"
        )
    if belief.belief_claim_type is not record.claim.claim_type:
        raise EpistemicChangeBindingError(
            "belief ClaimType does not match exact PCR record"
        )
    if belief.claim_record_fingerprint != record.input_fingerprint:
        raise EpistemicChangeBindingError(
            "belief claim_record_fingerprint does not match exact PCR record"
        )


def _route(
    belief: BeliefBinding | None,
    intent: EpistemicIntent,
) -> tuple[EpistemicRoute, EpistemicOwner, EpistemicRouteReason]:
    if belief is None:
        return _route_without_belief(intent)
    if _terminal(belief):
        return _route_terminal(intent)
    return _route_non_terminal(intent)


def _terminal(belief: BeliefBinding) -> bool:
    status = belief.belief_status
    return not belief_status_transition_allowed(status, status)


def _route_without_belief(
    intent: EpistemicIntent,
) -> tuple[EpistemicRoute, EpistemicOwner, EpistemicRouteReason]:
    if intent is EpistemicIntent.RETAIN_CLAIM:
        return (
            EpistemicRoute.RETAIN_CLAIM_ONLY,
            EpistemicOwner.PCR_V0_1,
            EpistemicRouteReason.CALLER_RETAINED_CLAIM,
        )
    if intent in {
        EpistemicIntent.CREATE_BELIEF_FROM_CLAIM,
        EpistemicIntent.SEEK_EVIDENCE_GATE_DECISION,
    }:
        return (
            EpistemicRoute.CLAIM_TO_BELIEF_BINDING_REQUIRED,
            EpistemicOwner.FUTURE_CLAIM_TO_BELIEF_BINDING,
            EpistemicRouteReason.CLAIM_BINDING_PREREQUISITE,
        )
    if intent is EpistemicIntent.DEFER:
        return (
            EpistemicRoute.DEFER,
            EpistemicOwner.NONE,
            EpistemicRouteReason.CALLER_DEFERRED,
        )
    return (
        EpistemicRoute.DEFER,
        EpistemicOwner.NONE,
        EpistemicRouteReason.INTENT_PRECONDITION_UNMET,
    )


def _route_non_terminal(
    intent: EpistemicIntent,
) -> tuple[EpistemicRoute, EpistemicOwner, EpistemicRouteReason]:
    if intent is EpistemicIntent.RETAIN_CLAIM:
        return (
            EpistemicRoute.RETAIN_CLAIM_ONLY,
            EpistemicOwner.PCR_V0_1,
            EpistemicRouteReason.CALLER_RETAINED_CLAIM,
        )
    if intent is EpistemicIntent.REVISE_EXISTING_BELIEF:
        return (
            EpistemicRoute.P0_014_NON_TERMINAL_REVISION_REQUIRED,
            EpistemicOwner.P0_014_BELIEF_LIFECYCLE,
            EpistemicRouteReason.NON_TERMINAL_REVISION_OWNER,
        )
    if intent is EpistemicIntent.SEEK_EVIDENCE_GATE_DECISION:
        return (
            EpistemicRoute.P0_015_EVIDENCE_GATE_REQUIRED,
            EpistemicOwner.P0_015_EVIDENCE_GATE,
            EpistemicRouteReason.EVIDENCE_GATE_OWNER,
        )
    if intent is EpistemicIntent.DEFER:
        return (
            EpistemicRoute.DEFER,
            EpistemicOwner.NONE,
            EpistemicRouteReason.CALLER_DEFERRED,
        )
    return (
        EpistemicRoute.DEFER,
        EpistemicOwner.NONE,
        EpistemicRouteReason.INTENT_PRECONDITION_UNMET,
    )


def _route_terminal(
    intent: EpistemicIntent,
) -> tuple[EpistemicRoute, EpistemicOwner, EpistemicRouteReason]:
    if intent is EpistemicIntent.RETAIN_CLAIM:
        return (
            EpistemicRoute.RETAIN_CLAIM_ONLY,
            EpistemicOwner.PCR_V0_1,
            EpistemicRouteReason.CALLER_RETAINED_CLAIM,
        )
    if intent is EpistemicIntent.DEFER:
        return (
            EpistemicRoute.DEFER,
            EpistemicOwner.NONE,
            EpistemicRouteReason.CALLER_DEFERRED,
        )
    return (
        EpistemicRoute.TERMINAL_RECONSIDERATION_LINEAGE_REQUIRED,
        EpistemicOwner.FUTURE_TERMINAL_RECONSIDERATION_LINEAGE,
        EpistemicRouteReason.TERMINAL_LINEAGE_PREREQUISITE,
    )


def _check_local_budget(value: object, budget: EpistemicChangeBudget) -> None:
    def walk(item: object, path: str) -> None:
        if isinstance(item, str):
            if len(item.encode("utf-8")) > budget.max_string_bytes:
                raise EpistemicChangeBudgetExceeded(
                    f"{path} exceeds local max_string_bytes"
                )
            return
        if isinstance(item, list):
            if len(item) > budget.max_tuple_items:
                raise EpistemicChangeBudgetExceeded(
                    f"{path} exceeds local max_tuple_items"
                )
            for index, child in enumerate(item):
                walk(child, f"{path}[{index}]")
            return
        if isinstance(item, dict):
            for key, child in item.items():
                walk(key, f"{path}.<key>")
                walk(child, f"{path}.{key}")
            return
        if item is None or type(item) in {bool, int}:
            return
        raise EpistemicChangeContractError(
            f"unsupported canonical input type at {path}: {type(item).__name__}"
        )

    walk(value, "input")


def _routing_fingerprint(
    canonical_input: dict[str, object],
    budget: EpistemicChangeBudget,
) -> str:
    if canonical_json.PROFILE_NAME != CANONICAL_PROFILE:
        raise EpistemicChangeContractError(
            "STOP_AND_RECONCILE: canonical JSON profile drift"
        )
    try:
        encoded = canonical_json.canonical_json_bytes(canonical_input)
    except (TypeError, ValueError) as exc:
        raise EpistemicChangeContractError(
            "canonicalization failed for admitted EPR-v0.1 input"
        ) from exc
    if len(encoded) > HARD_MAX_CANONICAL_INPUT_BYTES:
        raise EpistemicChangeContractError(
            "canonical input exceeds HARD_MAX_CANONICAL_INPUT_BYTES"
        )
    if len(encoded) > budget.max_canonical_input_bytes:
        raise EpistemicChangeBudgetExceeded(
            "canonical input exceeds local max_canonical_input_bytes"
        )
    return sha256(
        INPUT_FINGERPRINT_DOMAIN.encode("ascii") + b"\x00" + encoded
    ).hexdigest()
