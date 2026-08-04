"""P0-002 immutable command, pending-event, and committed-event envelopes."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass, field

from .primitives import (
    ActorRef,
    AuthorityRef,
    FrozenPayload,
    ProducerRef,
    freeze_payload,
    require_non_empty,
    require_non_negative,
    require_positive,
)


@dataclass(frozen=True, slots=True)
class CommandEnvelope:
    """A versioned intent submitted for validation and decision.

    This contract records authority by reference. Constructing a command does
    not prove that the referenced lease exists or grants the requested action.
    """

    command_id: str
    command_type: str
    command_schema: str
    target_stream: str
    expected_stream_version: int
    issued_at: str
    issuer: ActorRef
    authority: AuthorityRef
    correlation_id: str
    idempotency_key: str
    payload: FrozenPayload = field(repr=False)

    def __post_init__(self) -> None:
        for field_name in (
            "command_id",
            "command_type",
            "command_schema",
            "target_stream",
            "issued_at",
            "correlation_id",
            "idempotency_key",
        ):
            require_non_empty(getattr(self, field_name), field_name)
        require_non_negative(
            self.expected_stream_version, "expected_stream_version"
        )
        if not isinstance(self.issuer, ActorRef):
            raise TypeError("issuer must be an ActorRef")
        if not isinstance(self.authority, AuthorityRef):
            raise TypeError("authority must be an AuthorityRef")
        object.__setattr__(self, "payload", freeze_payload(self.payload))


@dataclass(frozen=True, slots=True)
class PendingEvent:
    """An ordered proposed fact that has not yet been committed."""

    event_type: str
    payload_schema: str
    affects_domain_state: bool
    payload: FrozenPayload = field(repr=False)

    def __post_init__(self) -> None:
        require_non_empty(self.event_type, "event_type")
        require_non_empty(self.payload_schema, "payload_schema")
        if not isinstance(self.affects_domain_state, bool):
            raise ValueError("affects_domain_state must be a boolean")
        object.__setattr__(self, "payload", freeze_payload(self.payload))


@dataclass(frozen=True, slots=True)
class EventEnvelope:
    """Immutable metadata for one committed event and its external payload."""

    event_id: str
    event_type: str
    envelope_schema_version: int
    payload_schema: str
    stream_id: str
    stream_version: int
    batch_id: str
    batch_index: int
    batch_size: int
    occurred_at: str
    recorded_at: str
    producer: ProducerRef
    initiator: ActorRef
    authority: AuthorityRef
    causation_id: str
    correlation_id: str
    affects_domain_state: bool
    payload_digest: str
    payload_ref: str
    previous_hash: str
    event_hash: str

    def __post_init__(self) -> None:
        for field_name in (
            "event_id",
            "event_type",
            "payload_schema",
            "stream_id",
            "batch_id",
            "occurred_at",
            "recorded_at",
            "causation_id",
            "correlation_id",
            "payload_digest",
            "payload_ref",
            "previous_hash",
            "event_hash",
        ):
            require_non_empty(getattr(self, field_name), field_name)
        require_positive(self.envelope_schema_version, "envelope_schema_version")
        require_positive(self.stream_version, "stream_version")
        require_non_negative(self.batch_index, "batch_index")
        require_positive(self.batch_size, "batch_size")
        if self.batch_index >= self.batch_size:
            raise ValueError("batch_index must be lower than batch_size")
        if not isinstance(self.affects_domain_state, bool):
            raise ValueError("affects_domain_state must be a boolean")
        if not isinstance(self.producer, ProducerRef):
            raise TypeError("producer must be a ProducerRef")
        if not isinstance(self.initiator, ActorRef):
            raise TypeError("initiator must be an ActorRef")
        if not isinstance(self.authority, AuthorityRef):
            raise TypeError("authority must be an AuthorityRef")


def snapshot_pending_batch(
    pending_events: Iterable[PendingEvent],
) -> tuple[PendingEvent, ...]:
    """Return an immutable ordered batch without assigning versions or hashes."""

    batch = tuple(pending_events)
    if not batch:
        raise ValueError("pending event batch must not be empty")
    if any(not isinstance(item, PendingEvent) for item in batch):
        raise TypeError("pending event batch may contain only PendingEvent values")
    return batch
