"""Focused static check for the CBP adapter/subtype boundary."""

from collections.abc import Mapping

from mentaury.beliefs import BeliefLifecycle
from mentaury.claim_belief_binding import ClaimBoundBeliefLifecycle
from mentaury.contracts import CommandEnvelope


def accepts_base_lifecycle(
    lifecycle: BeliefLifecycle,
    command: CommandEnvelope,
    state: Mapping[str, object],
) -> None:
    lifecycle.decide(command, state)


base: BeliefLifecycle = BeliefLifecycle()
adapter: ClaimBoundBeliefLifecycle = ClaimBoundBeliefLifecycle(base)
accepts_base_lifecycle(base, None, {})  # type: ignore[arg-type]
# Deliberately no assignment of adapter to BeliefLifecycle: it is not substitutable.
