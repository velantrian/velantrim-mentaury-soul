"""Bounded pure composition contracts.

P1-003 exposes deterministic in-memory constraint composition only. This package
grants no Action Gate, retrieval, tool, identity, relationship, M3, persistence,
I/O, or deployment authority.
"""

from .governed_constraints import (
    BINDING_CONTRACT_VERSION,
    CANONICAL_PROFILE,
    COMMON_REQUEST_DOMAIN,
    COMPOSER_CONTRACT_VERSION,
    EVALUATION_EVIDENCE_DOMAIN,
    P1_001_EXPECTED_VERSION,
    P1_002_EXPECTED_VERSION,
    SOURCE_PROVENANCE_SCOPE,
    CompositionBudget,
    CrossGateEvaluationContext,
    GovernedConstraintContractError,
    GovernedConstraintDecision,
    GovernedConstraintReason,
    GovernedConstraintResult,
    compose_governed_constraints,
)

__all__ = [
    "BINDING_CONTRACT_VERSION",
    "CANONICAL_PROFILE",
    "COMMON_REQUEST_DOMAIN",
    "COMPOSER_CONTRACT_VERSION",
    "EVALUATION_EVIDENCE_DOMAIN",
    "P1_001_EXPECTED_VERSION",
    "P1_002_EXPECTED_VERSION",
    "SOURCE_PROVENANCE_SCOPE",
    "CompositionBudget",
    "CrossGateEvaluationContext",
    "GovernedConstraintContractError",
    "GovernedConstraintDecision",
    "GovernedConstraintReason",
    "GovernedConstraintResult",
    "compose_governed_constraints",
]
