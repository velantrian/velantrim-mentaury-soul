"""Neutral Mentaury package boundary.

P0-001 intentionally exposes no identity, relationship, cognition, tool, or
persistence runtime. Later P0 commits may add infrastructure only through the
approved sequential implementation plan.
"""

from typing import Final

__all__ = ["__version__", "SKELETON_STATUS"]

__version__: Final[str] = "0.0.0"
SKELETON_STATUS: Final[str] = "P0-001_NEUTRAL_SKELETON"
