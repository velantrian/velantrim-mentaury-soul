"""Shared leaf types for belief and evidence contracts.

This module intentionally lives outside both ``mentaury.beliefs`` and
``mentaury.evidence``. Importing a package submodule executes that package's
``__init__`` first, so placing these shared enums inside either package would
reintroduce the circular import that this leaf module removes.

The enums are re-exported from ``mentaury.beliefs.contracts`` and the public
``mentaury.beliefs`` package for compatibility while retaining one class
identity across all consumers.
"""

from __future__ import annotations

from enum import StrEnum

__all__ = ["ClaimType", "EvidenceSide"]


class ClaimType(StrEnum):
    UNIVERSAL = "universal"
    STATISTICAL = "statistical"
    CAUSAL = "causal"
    CONTEXTUAL = "contextual"
    EXISTENTIAL = "existential"
    UNSPECIFIED = "unspecified"


class EvidenceSide(StrEnum):
    FOR = "for"
    AGAINST = "against"
