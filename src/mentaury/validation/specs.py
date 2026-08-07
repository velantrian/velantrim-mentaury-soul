"""Immutable structural value specifications for P0-005."""

from __future__ import annotations

import re
from collections.abc import Mapping
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Final, TypeAlias

#: Canonical lowercase sha256 content-address pattern, e.g. ``sha256:<64 hex>``.
#: Shared with ``mentaury.evidence.contracts`` so the schema-admission
#: boundary and the domain-object construction boundary cannot drift apart.
SHA256_DIGEST_PATTERN: Final[str] = r"sha256:[0-9a-f]{64}"


@dataclass(frozen=True, slots=True)
class StringSpec:
    min_length: int = 0
    pattern: str | None = None

    def __post_init__(self) -> None:
        if isinstance(self.min_length, bool) or self.min_length < 0:
            raise ValueError("min_length must be a non-negative integer")
        if self.pattern is not None:
            if not isinstance(self.pattern, str) or not self.pattern:
                raise ValueError("pattern must be a non-empty string")
            try:
                re.compile(self.pattern)
            except re.error as exc:
                raise ValueError(
                    f"pattern is not a valid regular expression: {exc}"
                ) from exc


def sha256_digest_spec() -> StringSpec:
    """Structural spec for a canonical lowercase sha256 digest string.

    ``min_length`` is not configurable: the pattern already fixes the exact
    shape (``sha256:`` plus 64 lowercase hex characters), so a caller-supplied
    ``min_length`` could only ever create an internally inconsistent spec
    (e.g. a length bound the pattern could never satisfy). The fixed length
    check still runs before the pattern check purely as a cheap fail-fast
    path, not as an independently tunable constraint.
    """

    return StringSpec(min_length=len("sha256:") + 64, pattern=SHA256_DIGEST_PATTERN)


@dataclass(frozen=True, slots=True)
class IntegerSpec:
    minimum: int | None = None
    maximum: int | None = None

    def __post_init__(self) -> None:
        for name, value in (("minimum", self.minimum), ("maximum", self.maximum)):
            if value is not None and (
                isinstance(value, bool) or not isinstance(value, int)
            ):
                raise TypeError(f"{name} must be an integer or None")
        if self.minimum is not None and self.maximum is not None:
            if self.minimum > self.maximum:
                raise ValueError("integer minimum cannot exceed maximum")


@dataclass(frozen=True, slots=True)
class BooleanSpec:
    pass


@dataclass(frozen=True, slots=True)
class NullSpec:
    pass


@dataclass(frozen=True, slots=True)
class ArraySpec:
    items: ValueSpec
    min_items: int = 0

    def __post_init__(self) -> None:
        if isinstance(self.min_items, bool) or self.min_items < 0:
            raise ValueError("min_items must be a non-negative integer")
        require_spec(self.items)


@dataclass(frozen=True, slots=True)
class ObjectSpec:
    properties: Mapping[str, ValueSpec]
    required: frozenset[str] = field(default_factory=frozenset)
    additional_properties: bool = False

    def __post_init__(self) -> None:
        copied: dict[str, ValueSpec] = {}
        for name, spec in self.properties.items():
            if not isinstance(name, str) or not name.strip():
                raise ValueError("schema property names must be non-blank strings")
            require_spec(spec)
            copied[name] = spec
        required = frozenset(self.required)
        missing = required.difference(copied)
        if missing:
            raise ValueError(
                f"required fields are not declared: {sorted(missing)!r}"
            )
        if not isinstance(self.additional_properties, bool):
            raise TypeError("additional_properties must be boolean")
        object.__setattr__(self, "properties", MappingProxyType(copied))
        object.__setattr__(self, "required", required)


@dataclass(frozen=True, slots=True)
class OneOfSpec:
    options: tuple[ValueSpec, ...]

    def __post_init__(self) -> None:
        options = tuple(self.options)
        if not options:
            raise ValueError("one-of spec requires at least one option")
        for option in options:
            require_spec(option)
        object.__setattr__(self, "options", options)


ValueSpec: TypeAlias = (
    StringSpec
    | IntegerSpec
    | BooleanSpec
    | NullSpec
    | ArraySpec
    | ObjectSpec
    | OneOfSpec
)
_SPEC_TYPES: Final[tuple[type[object], ...]] = (
    StringSpec,
    IntegerSpec,
    BooleanSpec,
    NullSpec,
    ArraySpec,
    ObjectSpec,
    OneOfSpec,
)


def require_spec(value: object) -> None:
    if not isinstance(value, _SPEC_TYPES):
        raise TypeError(f"unsupported value spec: {type(value).__name__}")
