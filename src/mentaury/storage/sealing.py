"""Trusted P0-009 event validation and canonical sealing primitives."""

from __future__ import annotations

import hashlib
from collections.abc import Mapping
from dataclasses import replace
from typing import TYPE_CHECKING

from mentaury.contracts import (
    EventEnvelope,
    canonical_event_hash_input_bytes,
    canonical_json_bytes,
    canonical_timestamp,
)
from mentaury.validation import SchemaRegistry

if TYPE_CHECKING:
    from mentaury.contracts import OperationAdmissionState


def compute_payload_digest(payload_bytes: bytes) -> str:
    if not isinstance(payload_bytes, bytes):
        raise TypeError("payload_bytes must be bytes")
    return f"sha256:{hashlib.sha256(payload_bytes).hexdigest()}"


def compute_event_hash(
    event: EventEnvelope,
    admission: OperationAdmissionState | None = None,
) -> str:
    """Event hash; with ``admission`` the hash projection is bounded and charged."""

    if not isinstance(event, EventEnvelope):
        raise TypeError("event must be an EventEnvelope")
    digest = hashlib.sha256(
        canonical_event_hash_input_bytes(event, admission)
    ).hexdigest()
    return f"sha256:{digest}"


def seal_event_bytes(
    event: EventEnvelope,
    payload_bytes: bytes,
    *,
    previous_hash: str,
    admission: OperationAdmissionState | None = None,
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
    return replace(
        provisional, event_hash=compute_event_hash(provisional, admission)
    )


def seal_event(
    event: EventEnvelope,
    payload: object,
    *,
    previous_hash: str | None = None,
    admission: OperationAdmissionState | None = None,
) -> EventEnvelope:
    """Return a deterministically sealed event without persisting it.

    With an explicit ``admission`` the payload is serialized through the bounded
    canonical path (same bytes, charged to the operation budget).
    """

    selected_previous_hash = (
        event.previous_hash if previous_hash is None else previous_hash
    )
    payload_bytes = (
        canonical_json_bytes(payload)
        if admission is None
        else admission.canonical_payload(payload)[0]
    )
    return seal_event_bytes(
        event,
        payload_bytes,
        previous_hash=selected_previous_hash,
        admission=admission,
    )


def validate_event_for_commit(
    event: EventEnvelope,
    payload: Mapping[str, object],
    registry: SchemaRegistry,
    admission: OperationAdmissionState | None = None,
) -> bytes:
    """Fail closed on event/schema identity, payload structure, and encoding.

    The returned bytes are the exact canonical payload bytes used for both the
    payload digest and immutable persistence.

    With an explicit ``admission`` the resource admission runs first: the
    payload is admitted through the bounded canonical path (depth, nodes,
    lengths, bytes, aggregate budget) *before* the schema validator walks it,
    and every validator step (including each ``OneOfSpec`` alternative) is
    charged to the operation as well. The bytes come from the same trusted
    snapshot that is validated. Canonical failures (floats, duplicate keys,
    lone surrogates) surface as ``CanonicalJSONError`` here, ahead of the schema
    issues the legacy order would report for the same input.
    """

    if not isinstance(event, EventEnvelope):
        raise TypeError("event must be an EventEnvelope")
    if not isinstance(payload, Mapping):
        raise TypeError("payload must be a mapping")
    if not isinstance(registry, SchemaRegistry):
        raise TypeError("registry must be a SchemaRegistry")

    if admission is None:
        registry.require_event_envelope(event)
        registry.require_event_payload(event, payload)
        return canonical_json_bytes(payload)
    # One trusted, detached representation: the bytes are rendered from the
    # snapshot and the schema validator walks that same snapshot, so what is
    # validated is exactly what is digested and persisted (a mapping that
    # reports different content on a second read cannot split the two).
    payload_bytes, snapshot = admission.admit_payload(payload)
    registry.require_event_envelope(event)
    registry.require_event_payload(
        event,
        snapshot,  # type: ignore[arg-type]
        admission.validation_visit,
    )
    return payload_bytes
