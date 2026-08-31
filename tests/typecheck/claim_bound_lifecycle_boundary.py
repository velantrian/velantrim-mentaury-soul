"""Focused static check for the CBP adapter/subtype boundary."""

from mentaury.beliefs import BeliefLifecycle
from mentaury.claim_belief_binding import ClaimBoundBeliefLifecycle


base: BeliefLifecycle = BeliefLifecycle()
adapter: ClaimBoundBeliefLifecycle = ClaimBoundBeliefLifecycle(base)

# The ignore is intentionally required. With --warn-unused-ignores this check
# fails if the adapter ever becomes a BeliefLifecycle subtype again.
not_substitutable: BeliefLifecycle = adapter  # type: ignore[assignment]
