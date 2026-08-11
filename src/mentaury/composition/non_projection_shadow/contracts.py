"""Immutable contracts for bounded NPG-COMP-v0.1 shadow composition."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final

from mentaury.non_projection import (
    ATTRIBUTED_INTERPRETATION_ENVELOPE_VERSION,
    NON_PROJECTION_CONTRACT_VERSION,
    AttributedInterpretationEnvelope,
    NonProjectionBudget,
    NonProjectionContractError,
    NonProjectionResult,
)

COMPOSITION_CONTRACT_VERSION: Final[str] = "NPG-COMP-v0.1"
EXPECTED_NPG_CONTRACT_VERSION: Final[str] = "NPG-v0.1"
EXPECTED_ENVELOPE_VERSION: Final[str] = "AIE-v0.1"
CALLER_ROLE: Final[str] = "NON_PROJECTION_SHADOW_COORDINATOR"
OUTPUT_ROLE: Final[str] = "BOUND_NON_PROJECTION_SHADOW_OBSERVATION"
AUTHORITY_CEILING: Final[str] = "NONE"


def _require_ref(value: object, name: str) -> None:
    if type(value) is not str or not value:
        raise NonProjectionContractError(f"{name} must be an exact non-empty str")


def _require_exact_type(value: object, expected: type[object], name: str) -> None:
    if type(value) is not expected:
        raise NonProjectionContractError(f"{name} must be exact {expected.__name__}")


@dataclass(frozen=True, slots=True)
class NonProjectionShadowContext:
    """Exact caller-supplied input for one shadow evaluation attempt."""

    evaluation_id: str
    proposal_ref: str
    envelope: AttributedInterpretationEnvelope
    budget: NonProjectionBudget

    def __post_init__(self) -> None:
        _require_ref(self.evaluation_id, "evaluation_id")
        _require_ref(self.proposal_ref, "proposal_ref")
        _require_exact_type(
            self.envelope, AttributedInterpretationEnvelope, "envelope"
        )
        _require_exact_type(self.budget, NonProjectionBudget, "budget")


@dataclass(frozen=True, slots=True)
class NonProjectionShadowObservation:
    """Same-attempt bound observation with no execution or mutation authority."""

    evaluation_id: str
    proposal_ref: str
    result: NonProjectionResult
    composition_contract_version: str = COMPOSITION_CONTRACT_VERSION

    def __post_init__(self) -> None:
        _require_ref(self.evaluation_id, "evaluation_id")
        _require_ref(self.proposal_ref, "proposal_ref")
        _require_exact_type(self.result, NonProjectionResult, "result")
        if self.composition_contract_version != COMPOSITION_CONTRACT_VERSION:
            raise NonProjectionContractError(
                "composition_contract_version is frozen"
            )


def assert_frozen_compatibility() -> None:
    """Fail closed if the locally imported NPG/AIE contract identities drift."""

    if NON_PROJECTION_CONTRACT_VERSION != EXPECTED_NPG_CONTRACT_VERSION:
        raise NonProjectionContractError(
            "NPG contract compatibility changed; STOP_AND_RECONCILE"
        )
    if ATTRIBUTED_INTERPRETATION_ENVELOPE_VERSION != EXPECTED_ENVELOPE_VERSION:
        raise NonProjectionContractError(
            "AIE contract compatibility changed; STOP_AND_RECONCILE"
        )
