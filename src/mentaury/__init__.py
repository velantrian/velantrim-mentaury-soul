"""Neutral Mentaury package boundary.

P0-009 exposes typed contracts, canonical serialization, explicit storage,
fail-closed validation, atomic batches, idempotency, concurrency, and R0
integrity verification only. It provides no identity, relationship, cognition,
tool, or autonomous runtime.
"""

from typing import Final

__all__ = ["__version__", "SKELETON_STATUS", "IMPLEMENTATION_STATUS"]

__version__: Final[str] = "0.0.0"
SKELETON_STATUS: Final[str] = "P0-001_NEUTRAL_SKELETON"
IMPLEMENTATION_STATUS: Final[str] = "P0-009_FULL_R0_INTEGRITY"
