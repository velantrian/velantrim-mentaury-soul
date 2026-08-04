"""Primitive immutable values shared by P0 envelope contracts.

This module freezes caller-provided payload containers so an envelope records a
stable local snapshot. It deliberately does not define canonical JSON,
cryptographic hashing, schema registry behavior, or persistence semantics.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from types import MappingProxyType
from typing import TypeAlias

PayloadScalar: TypeAlias = str | int | float | bool | None
FrozenPayloadValue: TypeAlias = (
    PayloadScalar
    | tuple["FrozenPayloadValue", ...]
    | Mapping[str, "FrozenPayloadValue"]
)
FrozenPayload: TypeAlias = Mapping[str, FrozenPayloadValue]


def require_non_empty(value: str, field_name: str) -> None:
    """Reject absent identifiers without imposing future format policy."""

    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")


def require_non_negative(value: int, field_name: str) -> None:
    """Reject negative counters while deferring upper bounds to later gates."""

    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ValueError(f"{field_name} must be a non-negative integer")


def require_positive(value: int, field_name: str) -> None:
    """Reject zero/negative sequence positions where one-based values apply."""

    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        raise ValueError(f"{field_name} must be a positive integer")


def freeze_payload_value(value: object) -> FrozenPayloadValue:
    """Create a recursively immutable, detached payload snapshot.

    Floats are accepted at P0-002 because canonical numeric policy belongs to
    P0-003. Bytes and non-string object keys are rejected because they are not
    portable payload-tree values.
    """

    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, Mapping):
        frozen: dict[str, FrozenPayloadValue] = {}
        for key, item in value.items():
            if not isinstance(key, str):
                raise TypeError("payload object keys must be strings")
            frozen[key] = freeze_payload_value(item)
        return MappingProxyType(frozen)
    if isinstance(value, Sequence) and not isinstance(
        value, (str, bytes, bytearray, memoryview)
    ):
        return tuple(freeze_payload_value(item) for item in value)
    raise TypeError(f"unsupported payload value type: {type(value).__name__}")


def freeze_payload(payload: Mapping[str, object]) -> FrozenPayload:
    """Freeze a payload mapping and return a detached read-only snapshot."""

    frozen = freeze_payload_value(payload)
    if not isinstance(frozen, Mapping):  # pragma: no cover - type contract guard
        raise TypeError("payload must be a mapping")
    return frozen


@dataclass(frozen=True, slots=True)
class ActorRef:
    """Attributable actor reference without embedded permissions."""

    actor_type: str
    actor_id: str

    def __post_init__(self) -> None:
        require_non_empty(self.actor_type, "actor_type")
        require_non_empty(self.actor_id, "actor_id")


@dataclass(frozen=True, slots=True)
class AuthorityRef:
    """Reference to an external authority record, never a permission copy."""

    capability_lease_id: str
    capability_revision: int

    def __post_init__(self) -> None:
        require_non_empty(self.capability_lease_id, "capability_lease_id")
        require_non_negative(self.capability_revision, "capability_revision")


@dataclass(frozen=True, slots=True)
class ProducerRef:
    """Versioned infrastructure component that produced an event envelope."""

    component: str
    version: str

    def __post_init__(self) -> None:
        require_non_empty(self.component, "component")
        require_non_empty(self.version, "version")
