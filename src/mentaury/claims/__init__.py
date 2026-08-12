"""Bounded pure PCR-v0.1 provenance-claim representation API."""

from .contracts import (
    CANONICAL_PROFILE,
    HARD_MAX_CANONICAL_INPUT_BYTES,
    HARD_MAX_STRING_BYTES,
    HARD_MAX_TUPLE_ITEMS,
    INPUT_FINGERPRINT_DOMAIN,
    PROVENANCE_CLAIM_CONTRACT_VERSION,
    SOURCE_SCOPE,
    ClaimRepresentation,
    ClaimScope,
    EpistemicRole,
    ProvenanceClaimBudgetExceeded,
    ProvenanceClaimContractError,
    ProvenanceClaimRecord,
    ProvenanceSource,
    RepresentationBudget,
)
from .representation import represent_provenance_claim

__all__ = [
    "CANONICAL_PROFILE",
    "HARD_MAX_CANONICAL_INPUT_BYTES",
    "HARD_MAX_STRING_BYTES",
    "HARD_MAX_TUPLE_ITEMS",
    "INPUT_FINGERPRINT_DOMAIN",
    "PROVENANCE_CLAIM_CONTRACT_VERSION",
    "SOURCE_SCOPE",
    "ClaimRepresentation",
    "ClaimScope",
    "EpistemicRole",
    "ProvenanceClaimBudgetExceeded",
    "ProvenanceClaimContractError",
    "ProvenanceClaimRecord",
    "ProvenanceSource",
    "RepresentationBudget",
    "represent_provenance_claim",
]
