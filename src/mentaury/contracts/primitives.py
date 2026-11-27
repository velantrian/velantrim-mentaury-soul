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

from .admission import PayloadAdmissionBudget, PayloadAdmissionState

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


def freeze_payload_value(
    value: object,
    budget: PayloadAdmissionBudget | None = None,
) -> FrozenPayloadValue:
    """Create a recursively immutable, detached payload snapshot.

    Floats are accepted at P0-002 because canonical numeric policy belongs to
    P0-003. Bytes and non-string object keys are rejected because they are not
    portable payload-tree values. Cyclic containers fail closed instead of
    escaping as an uncontrolled recursion error.

    Without ``budget`` the traversal is the original unbounded one (existing
    callers are unchanged). With an explicit ``PayloadAdmissionBudget`` the
    traversal is iterative and stops at the first exceeded dimension with
    ``PayloadAdmissionExceeded``; the spend state is created per call.
    """

    if budget is None:
        return _freeze_payload_value(value, set())
    return _freeze_payload_value_bounded(value, PayloadAdmissionState(budget))


class _Frame:
    __slots__ = ("container", "iterator", "is_mapping", "out", "identity", "key")

    def __init__(
        self,
        container: object,
        iterator: object,
        is_mapping: bool,
        out: dict[str, FrozenPayloadValue] | list[FrozenPayloadValue],
        identity: int,
    ) -> None:
        # Strong reference: keeps the container alive for the whole frame so
        # its id() cannot be reused by another object while it is "active".
        self.container = container
        self.iterator = iterator
        self.is_mapping = is_mapping
        self.out = out
        self.identity = identity
        self.key: str = ""


def _advance(
    frame: _Frame,
    state: PayloadAdmissionState,
) -> tuple[bool, object]:
    """Pull the next child of ``frame`` as ``(has_child, child)``.

    Exhaustion is signalled by the boolean, never by an in-band value, so no
    payload value can be mistaken for the end of iteration.
    """

    try:
        item = next(frame.iterator)  # type: ignore[call-overload]
    except StopIteration:
        return False, None
    if frame.is_mapping:
        key, child = item
        if not isinstance(key, str):
            raise TypeError("payload object keys must be strings")
        state.charge_node()
        state.check_key(key)
        frame.key = key
        return True, child
    return True, item


def _freeze_payload_value_bounded(
    value: object,
    state: PayloadAdmissionState,
) -> FrozenPayloadValue:
    active: set[int] = set()
    stack: list[_Frame] = []
    to_visit: object = value
    while True:
        state.charge_node()
        produced: FrozenPayloadValue
        if to_visit is None or isinstance(to_visit, (str, int, float, bool)):
            if isinstance(to_visit, str):
                state.check_string(to_visit)
            produced = to_visit
        elif isinstance(to_visit, Mapping) or (
            isinstance(to_visit, Sequence)
            and not isinstance(to_visit, (str, bytes, bytearray, memoryview))
        ):
            state.check_depth(len(stack) + 1)
            identity = id(to_visit)
            if identity in active:
                raise TypeError("cyclic payload container is forbidden")
            active.add(identity)
            is_mapping = isinstance(to_visit, Mapping)
            if isinstance(to_visit, Mapping):
                frame = _Frame(to_visit, iter(to_visit.items()), True, {}, identity)
            else:
                frame = _Frame(to_visit, iter(to_visit), False, [], identity)
            stack.append(frame)
            has_child, child = _advance(frame, state)
            if has_child:
                to_visit = child
                continue
            stack.pop()
            active.discard(frame.identity)
            produced = (
                MappingProxyType(frame.out)  # type: ignore[arg-type]
                if is_mapping
                else tuple(frame.out)
            )
        else:
            raise TypeError(f"unsupported payload value type: {type(to_visit).__name__}")

        # Deliver ``produced`` upward until a further child must be visited.
        while True:
            if not stack:
                return produced
            frame = stack[-1]
            if frame.is_mapping:
                frame.out[frame.key] = produced  # type: ignore[call-overload]
            else:
                frame.out.append(produced)  # type: ignore[union-attr]
            has_child, child = _advance(frame, state)
            if not has_child:
                stack.pop()
                active.discard(frame.identity)
                produced = (
                    MappingProxyType(frame.out)  # type: ignore[arg-type]
                    if frame.is_mapping
                    else tuple(frame.out)
                )
                continue
            to_visit = child
            break


def _freeze_payload_value(
    value: object,
    active: set[int],
) -> FrozenPayloadValue:
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, Mapping):
        identity = id(value)
        if identity in active:
            raise TypeError("cyclic payload container is forbidden")
        active.add(identity)
        try:
            frozen: dict[str, FrozenPayloadValue] = {}
            for key, item in value.items():
                if not isinstance(key, str):
                    raise TypeError("payload object keys must be strings")
                frozen[key] = _freeze_payload_value(item, active)
            return MappingProxyType(frozen)
        finally:
            active.remove(identity)
    if isinstance(value, Sequence) and not isinstance(
        value, (str, bytes, bytearray, memoryview)
    ):
        identity = id(value)
        if identity in active:
            raise TypeError("cyclic payload container is forbidden")
        active.add(identity)
        try:
            return tuple(_freeze_payload_value(item, active) for item in value)
        finally:
            active.remove(identity)
    raise TypeError(f"unsupported payload value type: {type(value).__name__}")


def freeze_payload(
    payload: Mapping[str, object],
    budget: PayloadAdmissionBudget | None = None,
) -> FrozenPayload:
    """Freeze a payload mapping and return a detached read-only snapshot.

    With an explicit ``budget`` a non-mapping root is refused before any
    traversal, and the bounded iterative path is used.
    """

    if budget is not None and not isinstance(payload, Mapping):
        raise TypeError("payload must be a mapping")
    frozen = freeze_payload_value(payload, budget)
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
