"""Neutral Mentaury package boundary.

P0-002 exposes typed envelope contracts only. It still provides no identity,
relationship, cognition, tool, persistence, or autonomous runtime.
"""

from typing import Final

__all__ = ["__version__", "SKELETON_STATUS", "IMPLEMENTATION_STATUS"]

__version__: Final[str] = "0.0.0"
SKELETON_STATUS: Final[str] = "P0-001_NEUTRAL_SKELETON"
IMPLEMENTATION_STATUS: Final[str] = "P0-002_ENVELOPE_CONTRACTS"
