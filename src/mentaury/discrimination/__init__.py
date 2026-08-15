"""Bounded pure HDE-v0.1 hypothesis-discrimination evaluation API."""

from .contracts import (
    CANONICAL_PROFILE,
    HARD_MAX_CANONICAL_INPUT_BYTES,
    HARD_MAX_STRING_BYTES,
    HARD_MAX_TUPLE_ITEMS,
    HYPOTHESIS_DISCRIMINATION_CONTRACT_VERSION,
    INPUT_FINGERPRINT_DOMAIN,
    DiscriminationClass,
    DiscriminationEvaluation,
    DiscriminationEvaluationBudget,
    DiscriminationProposal,
    HypothesisDiscriminationContractError,
    OutcomePrediction,
    PredictionState,
)
from .evaluator import evaluate_hypothesis_discrimination

__all__ = [
    "CANONICAL_PROFILE",
    "HARD_MAX_CANONICAL_INPUT_BYTES",
    "HARD_MAX_STRING_BYTES",
    "HARD_MAX_TUPLE_ITEMS",
    "HYPOTHESIS_DISCRIMINATION_CONTRACT_VERSION",
    "INPUT_FINGERPRINT_DOMAIN",
    "DiscriminationClass",
    "DiscriminationEvaluation",
    "DiscriminationEvaluationBudget",
    "DiscriminationProposal",
    "HypothesisDiscriminationContractError",
    "OutcomePrediction",
    "PredictionState",
    "evaluate_hypothesis_discrimination",
]
