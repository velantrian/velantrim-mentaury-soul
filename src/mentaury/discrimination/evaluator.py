"""Pure deterministic HDE-v0.1 hypothesis-discrimination evaluation."""

from __future__ import annotations

from hashlib import sha256

from mentaury.contracts import canonical_json

from .contracts import (
    CANONICAL_PROFILE,
    HARD_MAX_CANONICAL_INPUT_BYTES,
    HYPOTHESIS_DISCRIMINATION_CONTRACT_VERSION,
    INPUT_FINGERPRINT_DOMAIN,
    DiscriminationClass,
    DiscriminationEvaluation,
    DiscriminationEvaluationBudget,
    DiscriminationProposal,
    HypothesisDiscriminationContractError,
    PredictionState,
)


def _require_exact(value: object, expected: type[object], name: str) -> None:
    if type(value) is not expected:
        raise HypothesisDiscriminationContractError(
            f"{name} must be exact {expected.__name__}"
        )


def _check_string_budget(
    value: str,
    *,
    name: str,
    budget: DiscriminationEvaluationBudget,
) -> None:
    if len(value.encode("utf-8")) > budget.max_string_bytes:
        raise HypothesisDiscriminationContractError(
            f"{name} exceeds local max_string_bytes"
        )


def _check_string_tuple_budget(
    value: tuple[str, ...],
    *,
    name: str,
    budget: DiscriminationEvaluationBudget,
) -> None:
    if len(value) > budget.max_tuple_items:
        raise HypothesisDiscriminationContractError(
            f"{name} exceeds local max_tuple_items"
        )
    for index, item in enumerate(value):
        _check_string_budget(
            item,
            name=f"{name}[{index}]",
            budget=budget,
        )


def _check_local_budget(
    proposal: DiscriminationProposal,
    budget: DiscriminationEvaluationBudget,
) -> None:
    for name in (
        "proposed_observation_ref",
        "design_origin_ref",
        "partition_scope_ref",
    ):
        _check_string_budget(
            getattr(proposal, name),
            name=name,
            budget=budget,
        )
    _check_string_tuple_budget(
        proposal.design_basis_refs,
        name="design_basis_refs",
        budget=budget,
    )
    if len(proposal.outcomes) > budget.max_tuple_items:
        raise HypothesisDiscriminationContractError(
            "outcomes exceeds local max_tuple_items"
        )
    for index, outcome in enumerate(proposal.outcomes):
        _check_string_budget(
            outcome.outcome_ref,
            name=f"outcomes[{index}].outcome_ref",
            budget=budget,
        )
        _check_string_tuple_budget(
            outcome.expectation_basis_refs,
            name=f"outcomes[{index}].expectation_basis_refs",
            budget=budget,
        )


def _canonical_input_bytes(
    proposal: DiscriminationProposal,
    budget: DiscriminationEvaluationBudget,
) -> bytes:
    if canonical_json.PROFILE_NAME != CANONICAL_PROFILE:
        raise HypothesisDiscriminationContractError(
            "STOP_AND_RECONCILE: canonical JSON profile drift"
        )
    try:
        encoded = canonical_json.canonical_json_bytes(
            {
                "contract_version": HYPOTHESIS_DISCRIMINATION_CONTRACT_VERSION,
                "proposal": proposal.to_value(),
                "budget": budget.to_value(),
            }
        )
    except (TypeError, ValueError) as exc:
        raise HypothesisDiscriminationContractError(
            "canonicalization failed for admitted HDE-v0.1 input"
        ) from exc

    if len(encoded) > HARD_MAX_CANONICAL_INPUT_BYTES:
        raise HypothesisDiscriminationContractError(
            "canonical input exceeds HARD_MAX_CANONICAL_INPUT_BYTES"
        )
    if len(encoded) > budget.max_canonical_input_bytes:
        raise HypothesisDiscriminationContractError(
            "canonical input exceeds local max_canonical_input_bytes"
        )
    return encoded


def evaluate_hypothesis_discrimination(
    proposal: DiscriminationProposal,
    budget: DiscriminationEvaluationBudget,
) -> DiscriminationEvaluation:
    """Evaluate only caller-supplied H1/H2 outcome-discrimination structure.

    The function performs no retrieval, observation execution, evidence
    collection, Evidence Gate call, belief mutation, confidence assignment,
    scheduling, action selection, identity/relationship/M3 change, or runtime I/O.
    """

    _require_exact(proposal, DiscriminationProposal, "proposal")
    _require_exact(budget, DiscriminationEvaluationBudget, "budget")
    _check_local_budget(proposal, budget)

    differential_refs: list[str] = []
    unknown_refs: list[str] = []

    for outcome in proposal.outcomes:
        if (
            outcome.h1_prediction is PredictionState.UNKNOWN
            or outcome.h2_prediction is PredictionState.UNKNOWN
        ):
            unknown_refs.append(outcome.outcome_ref)
        elif {
            outcome.h1_prediction,
            outcome.h2_prediction,
        } == {
            PredictionState.PREDICTED,
            PredictionState.NOT_PREDICTED,
        }:
            differential_refs.append(outcome.outcome_ref)

    if not proposal.partition_complete_for_scope or unknown_refs:
        classification = DiscriminationClass.INCONCLUSIVE_STRUCTURE
    elif differential_refs:
        classification = DiscriminationClass.DISCRIMINATING
    else:
        classification = DiscriminationClass.NON_DISCRIMINATING

    encoded = _canonical_input_bytes(proposal, budget)
    fingerprint = sha256(
        INPUT_FINGERPRINT_DOMAIN.encode("ascii") + b"\x00" + encoded
    ).hexdigest()

    return DiscriminationEvaluation(
        contract_version=HYPOTHESIS_DISCRIMINATION_CONTRACT_VERSION,
        classification=classification,
        differential_outcome_refs=tuple(differential_refs),
        unknown_outcome_refs=tuple(unknown_refs),
        input_fingerprint=fingerprint,
    )
