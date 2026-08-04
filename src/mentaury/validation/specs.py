"""Immutable structural value specifications for P0-005."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Final, TypeAlias


@dataclass(frozen=True, slots=True)
class StringSpec:
    min_length: int = 0

    def __post_init__(self) -> None:
        if isinstance(self.min_length, bool) or self.min_length < 0:
            raise ValueError("min_length must be a non-negative integer")


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
