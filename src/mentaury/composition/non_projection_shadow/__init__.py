"""Bounded NPG-COMP-v0.1 same-attempt shadow composition API."""

from .contracts import (
    AUTHORITY_CEILING,
    CALLER_ROLE,
    COMPOSITION_CONTRACT_VERSION,
    EXPECTED_ENVELOPE_VERSION,
    EXPECTED_NPG_CONTRACT_VERSION,
    OUTPUT_ROLE,
    NonProjectionShadowContext,
    NonProjectionShadowObservation,
)
from .coordinator import evaluate_non_projection_shadow

__all__ = [
    "AUTHORITY_CEILING",
    "CALLER_ROLE",
    "COMPOSITION_CONTRACT_VERSION",
    "EXPECTED_ENVELOPE_VERSION",
    "EXPECTED_NPG_CONTRACT_VERSION",
    "OUTPUT_ROLE",
    "NonProjectionShadowContext",
    "NonProjectionShadowObservation",
    "evaluate_non_projection_shadow",
]
