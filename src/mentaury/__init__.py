"""Neutral Mentaury package boundary.

P0-005 exposes typed contracts, canonical serialization, explicit storage
primitives, and fail-closed structural schema validation only. It provides no
identity, relationship, cognition, tool, or autonomous domain runtime.
"""

from typing import Final

__all__ = ["__version__", "SKELETON_STATUS", "IMPLEMENTATION_STATUS"]

__version__: Final[str] = "0.0.0"
SKELETON_STATUS: Final[str] = "P0-001_NEUTRAL_SKELETON"
IMPLEMENTATION_STATUS: Final[str] = "P0-005_STRUCTURAL_SCHEMA_VALIDATION"
