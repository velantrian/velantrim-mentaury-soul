"""Neutral Mentaury package boundary.

P0-003 exposes typed envelope contracts and deterministic canonical JSON only.
It still provides no identity, relationship, cognition, tool, persistence, or
autonomous runtime.
"""

from typing import Final

__all__ = ["__version__", "SKELETON_STATUS", "IMPLEMENTATION_STATUS"]

__version__: Final[str] = "0.0.0"
SKELETON_STATUS: Final[str] = "P0-001_NEUTRAL_SKELETON"
IMPLEMENTATION_STATUS: Final[str] = "P0-003_CANONICAL_JSON_V1"
