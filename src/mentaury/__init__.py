"""Mentaury Soul bounded research package metadata.

The root package intentionally exposes only a version marker. Public bounded
primitives live in their owning subpackages; current engineering status is
resolved from live GitHub plus ``docs/CURRENT_STATUS.md``, not package-level
milestone literals.
"""

from typing import Final

__all__ = ["__version__"]

__version__: Final[str] = "1.0.0"
