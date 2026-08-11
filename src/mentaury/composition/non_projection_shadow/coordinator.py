"""Pure same-attempt NPG-v0.1 shadow composition."""

from __future__ import annotations

from mentaury.non_projection import NonProjectionContractError, classify_non_projection

from .contracts import (
    NonProjectionShadowContext,
    NonProjectionShadowObservation,
    assert_frozen_compatibility,
)


def evaluate_non_projection_shadow(
    *,
    context: NonProjectionShadowContext,
) -> NonProjectionShadowObservation:
    """Evaluate exactly one admitted shadow attempt without side effects."""

    if type(context) is not NonProjectionShadowContext:
        raise NonProjectionContractError(
            "context must be exact NonProjectionShadowContext"
        )

    assert_frozen_compatibility()

    result = classify_non_projection(
        envelope=context.envelope,
        budget=context.budget,
    )

    return NonProjectionShadowObservation(
        evaluation_id=context.evaluation_id,
        proposal_ref=context.proposal_ref,
        result=result,
    )
