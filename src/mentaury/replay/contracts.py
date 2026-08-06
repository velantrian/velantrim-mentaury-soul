"""P0-013 immutable contracts for deterministic R1 state replay."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from enum import StrEnum
from typing import Protocol, runtime_checkable

from mentaury.contracts import EventEnvelope
from mentaury.contracts.primitives import (
    FrozenPayload,
    freeze_payload,
    require_non_empty,
    require_non_negative,
)


@runtime_checkable
class ReplayReducer(Protocol):
    """Pure, versioned reducer boundary owned by one projection.

    The engine supplies recursively immutable canonical mappings. Reducers must
    return a new mapping and must not use clocks, networks or unrecorded
    randomness. The engine executes each state transition twice and compares
    canonical outputs, but this remains a deterministic-behavior check rather
    than a complete side-effect sandbox.
    """

    reducer_id: str
    reducer_version: str
    supported_event_schemas: frozenset[tuple[str, str]]

    def initial_state(self) -> Mapping[str, object]:
        """Return a fresh canonicalizable initial state mapping."""

    def apply(
        self,
        state: FrozenPayload,
        event: EventEnvelope,
        payload: FrozenPayload,
    ) -> Mapping[str, object]:
        """Return the next state without mutating the immutable inputs."""


@dataclass(frozen=True, slots=True)
class ReplayStateBudget:
    """Caller-supplied canonical state-size limits for each replay path."""

    max_state_bytes: int
    max_total_state_bytes: int

    def __post_init__(self) -> None:
        for field_name in ("max_state_bytes", "max_total_state_bytes"):
            value = getattr(self, field_name)
            if isinstance(value, bool) or not isinstance(value, int) or value < 1:
                raise ValueError(f"{field_name} must be a positive integer")
        if self.max_total_state_bytes < self.max_state_bytes:
            raise ValueError(
                "max_total_state_bytes must be >= max_state_bytes"
            )


@dataclass(frozen=True, slots=True)
class ReplaySnapshot:
    """Externally supplied projection checkpoint; never a source of truth."""

    reducer_id: str
    reducer_version: str
    stream_id: str
    through_stream_version: int
    through_event_hash: str
    state: FrozenPayload = field(repr=False)
    state_hash: str

    def __post_init__(self) -> None:
        for field_name in (
            "reducer_id",
            "reducer_version",
            "stream_id",
            "through_event_hash",
            "state_hash",
        ):
            require_non_empty(getattr(self, field_name), field_name)
        require_non_negative(
            self.through_stream_version,
            "through_stream_version",
        )
        if not isinstance(self.state, Mapping):
            raise TypeError("state must be a mapping")
        object.__setattr__(self, "state", freeze_payload(self.state))


class ReplayFailureCode(StrEnum):
    """First actionable R1 replay failure."""

    R0_PREREQUISITE_FAILED = "R0_PREREQUISITE_FAILED"
    INVALID_REDUCER = "INVALID_REDUCER"
    INVALID_INITIAL_STATE = "INVALID_INITIAL_STATE"
    RESOURCE_BUDGET_EXCEEDED = "RESOURCE_BUDGET_EXCEEDED"
    UNKNOWN_EVENT_SCHEMA = "UNKNOWN_EVENT_SCHEMA"
    PAYLOAD_UNAVAILABLE = "PAYLOAD_UNAVAILABLE"
    PAYLOAD_DECODE_ERROR = "PAYLOAD_DECODE_ERROR"
    PAYLOAD_NOT_CANONICAL = "PAYLOAD_NOT_CANONICAL"
    PAYLOAD_DIGEST_MISMATCH = "PAYLOAD_DIGEST_MISMATCH"
    STREAM_CHANGED_DURING_VERIFICATION = "STREAM_CHANGED_DURING_VERIFICATION"
    ACTIVE_TRANSACTION = "ACTIVE_TRANSACTION"
    REDUCER_ERROR = "REDUCER_ERROR"
    REDUCER_REUSED_INPUT = "REDUCER_REUSED_INPUT"
    REDUCER_NONDETERMINISTIC = "REDUCER_NONDETERMINISTIC"
    INVALID_REDUCER_STATE = "INVALID_REDUCER_STATE"
    SNAPSHOT_REDUCER_MISMATCH = "SNAPSHOT_REDUCER_MISMATCH"
    SNAPSHOT_STREAM_MISMATCH = "SNAPSHOT_STREAM_MISMATCH"
    SNAPSHOT_VERSION_OUT_OF_RANGE = "SNAPSHOT_VERSION_OUT_OF_RANGE"
    SNAPSHOT_ANCHOR_MISMATCH = "SNAPSHOT_ANCHOR_MISMATCH"
    SNAPSHOT_STATE_HASH_MISMATCH = "SNAPSHOT_STATE_HASH_MISMATCH"
    SNAPSHOT_STATE_MISMATCH = "SNAPSHOT_STATE_MISMATCH"
    FINAL_STATE_MISMATCH = "FINAL_STATE_MISMATCH"


@dataclass(frozen=True, slots=True)
class ReplayFailure:
    code: ReplayFailureCode
    stream_id: str
    message: str
    event_id: str | None = None
    stream_version: int | None = None


@dataclass(frozen=True, slots=True)
class R1ReplayReport:
    """Result of full replay versus independently checked snapshot + tail."""

    stream_id: str
    reducer_id: str
    reducer_version: str
    ok: bool
    checked_events: int
    applied_events: int
    snapshot_through_version: int
    full_state_hash: str | None
    snapshot_state_hash: str | None
    tail_state_hash: str | None
    failure: ReplayFailure | None
    verified_through_stream_version: int = 0
    verified_through_event_hash: str | None = None
