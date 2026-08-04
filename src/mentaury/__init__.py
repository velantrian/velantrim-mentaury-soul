"""Neutral Mentaury package boundary.

P0-008 exposes typed contracts, canonical serialization, explicit storage,
fail-closed validation, atomic batches, idempotency, and controlled SQLite write
concurrency only. It provides no identity, relationship, cognition, tool, or
autonomous runtime.
"""

from typing import Final

__all__ = ["__version__", "SKELETON_STATUS", "IMPLEMENTATION_STATUS"]

__version__: Final[str] = "0.0.0"
SKELETON_STATUS: Final[str] = "P0-001_NEUTRAL_SKELETON"
IMPLEMENTATION_STATUS: Final[str] = "P0-008_TRANSACTIONAL_CONCURRENCY"
