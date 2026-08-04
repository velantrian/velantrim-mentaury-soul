"""Neutral Mentaury package boundary.

P0-004 exposes typed contracts, canonical serialization, and explicit storage
primitives only. It provides no identity, relationship, cognition, tool, or
autonomous domain runtime.
"""

from typing import Final

__all__ = ["__version__", "SKELETON_STATUS", "IMPLEMENTATION_STATUS"]

__version__: Final[str] = "0.0.0"
SKELETON_STATUS: Final[str] = "P0-001_NEUTRAL_SKELETON"
IMPLEMENTATION_STATUS: Final[str] = "P0-004_IMMUTABLE_EVENT_PAYLOAD_STORAGE"
