"""Trusted P0-009 event validation and canonical sealing primitives."""

from __future__ import annotations

import hashlib
from collections.abc import Mapping
from dataclasses import replace

from mentaury.contracts import (
    EventEnvelope,
    canonical_event_hash_input_bytes,
    canonical_json_bytes,
    canonical_timestamp,
)
from mentaury.validation import SchemaRegistry


class CommitValidationError(ValueError):
    """Raised before persistence when a proposed event cannot be committed safely."""


def compute_payload_digest(payload_bytes: bytes) -> str:
    if not isinstance(payload_bytes, bytes):
        raise TypeError("payload_bytes must be bytes")
    return f"sha256:{hashlib.sha256(payload_bytes).hexdigest()}"


def compute_event_hash(event: EventEnvelope) -> str:
    if not isinstance(event, EventEnvelope):
        raise TypeError("event must be an EventEnvelope")
    digest = hashlib.sha256(canonical_event_hash_input_bytes(event)).hexdigest()
    return f"sha256:{digest}"


def seal_event_bytes(
    event: EventEnvelope,
    payload_bytes: bytes,
    *,
    previous_hash: str,
) -> EventEnvelope:
    """Allocate canonical timestamps, digest, chain link, and event hash.

    Caller-supplied hash and digest fields are never trusted. The returned event
    is the only envelope that may cross the immutable commit boundary.
    """

    if not isinstance(event, EventEnvelope):
        raise TypeError("event must be an EventEnvelope")
    if not isinstance(payload_bytes, bytes):
        raise TypeError("payload_bytes must be bytes")
    if not isinstance(previous_hash, str) or not previous_hash.strip():
        raise ValueError("previous_hash must be a non-blank string")

    provisional = replace(
        event,
        occurred_at=canonical_timestamp(event.occurred_at),
        recorded_at=canonical_timestamp(event.recorded_at),
        payload_digest=compute_payload_digest(payload_bytes),
        previous_hash=previous_hash,
        event_hash="sha256:pending",
    )
    return replace(provisional, event_hash=compute_event_hash(provisional))


def seal_event(
    event: EventEnvelope,
    payload: object,
    *,
    previous_hash: str | None = None,
) -> EventEnvelope:
    """Return a deterministically sealed event without persisting it."""

    selected_previous_hash = (
        event.previous_hash if previous_hash is None else previous_hash
    )
    return seal_event_bytes(
        event,
        canonical_json_bytes(payload),
        previous_hash=selected_previous_hash,
    )


def validate_event_for_commit(
    event: EventEnvelope,
    payload: Mapping[str, object],
    registry: SchemaRegistry,
) -> bytes:
    """Fail closed on event/schema identity, payload structure, and encoding.

    The returned bytes are the exact canonical payload bytes used for both the
    payload digest and immutable persistence.
    """

    if not isinstance(event, EventEnvelope):
        raise TypeError("event must be an EventEnvelope")
    if not isinstance(payload, Mapping):
        raise TypeError("payload must be a mapping")
    if not isinstance(registry, SchemaRegistry):
        raise TypeError("registry must be a SchemaRegistry")

    registry.require_event_envelope(event)
    registry.require_event_payload(event, payload)
    return canonical_json_bytes(payload)
