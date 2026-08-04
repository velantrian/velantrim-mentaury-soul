"""MENTAURY_CANONICAL_JSON_V1 deterministic serialization profile.

This is a deliberately restricted profile, not a claim of RFC 8785 support.
It creates deterministic UTF-8 JSON bytes for portable value trees and typed
P0 envelopes. Cryptographic hashing and persistence are owned by later P0
milestones.
"""

from __future__ import annotations

import json
import re
from collections.abc import Iterable, Mapping, Sequence
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from typing import Final, TypeAlias

from .envelopes import CommandEnvelope, EventEnvelope, PendingEvent, snapshot_pending_batch
from .primitives import ActorRef, AuthorityRef, ProducerRef

PROFILE_NAME: Final[str] = "MENTAURY_CANONICAL_JSON_V1"
SAFE_INTEGER_MAX: Final[int] = (1 << 53) - 1
SAFE_INTEGER_MIN: Final[int] = -SAFE_INTEGER_MAX
_TIMESTAMP_RE: Final[re.Pattern[str]] = re.compile(
    r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}"
    r"(?:\.\d{1,6})?(?:Z|[+-]\d{2}:\d{2})$"
)

CanonicalScalar: TypeAlias = str | int | bool | None
CanonicalValue: TypeAlias = (
    CanonicalScalar | list["CanonicalValue"] | dict[str, "CanonicalValue"]
)


class CanonicalJSONError(ValueError):
    """Raised when a value cannot enter MENTAURY_CANONICAL_JSON_V1."""


def _validate_unicode_scalar_text(value: str, path: str) -> str:
    for character in value:
        code_point = ord(character)
        if 0xD800 <= code_point <= 0xDFFF:
            raise CanonicalJSONError(f"lone surrogate is forbidden at {path}")
    return value


def _prepare(value: object, path: str, active: set[int]) -> CanonicalValue:
    if value is None or isinstance(value, bool):
        return value
    if isinstance(value, int):
        if value < SAFE_INTEGER_MIN or value > SAFE_INTEGER_MAX:
            raise CanonicalJSONError(
                f"integer outside safe range at {path}: {value}"
            )
        return value
    if isinstance(value, float):
        raise CanonicalJSONError(f"float is forbidden at {path}")
    if isinstance(value, Decimal):
        raise CanonicalJSONError(
            f"Decimal is forbidden at {path}; encode it explicitly as a canonical string"
        )
    if isinstance(value, str):
        return _validate_unicode_scalar_text(value, path)
    if isinstance(value, Mapping):
        identity = id(value)
        if identity in active:
            raise CanonicalJSONError(f"cyclic mapping is forbidden at {path}")
        active.add(identity)
        try:
            prepared: dict[str, CanonicalValue] = {}
            for key, item in value.items():
                if not isinstance(key, str):
                    raise CanonicalJSONError(
                        f"object key must be a string at {path}"
                    )
                safe_key = _validate_unicode_scalar_text(key, f"{path}.<key>")
                if safe_key in prepared:
                    raise CanonicalJSONError(f"duplicate object key at {path}: {safe_key}")
                prepared[safe_key] = _prepare(item, f"{path}.{safe_key}", active)
            return prepared
        finally:
            active.remove(identity)
    if isinstance(value, Sequence) and not isinstance(
        value, (str, bytes, bytearray, memoryview)
    ):
        identity = id(value)
        if identity in active:
            raise CanonicalJSONError(f"cyclic sequence is forbidden at {path}")
        active.add(identity)
        try:
            return [
                _prepare(item, f"{path}[{index}]", active)
                for index, item in enumerate(value)
            ]
        finally:
            active.remove(identity)
    raise CanonicalJSONError(
        f"unsupported canonical JSON type at {path}: {type(value).__name__}"
    )


def canonical_json_text(value: object) -> str:
    """Serialize one portable value tree without insignificant whitespace."""

    prepared = _prepare(value, "$", set())
    return json.dumps(
        prepared,
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    )


def canonical_json_bytes(value: object) -> bytes:
    """Return the canonical UTF-8 byte representation."""

    return canonical_json_text(value).encode("utf-8")


def canonical_decimal_string(value: Decimal | str) -> str:
    """Normalize a finite decimal to a schema-controlled JSON string value.

    Decimal objects are never serialized implicitly because JSON numbers cannot
    preserve decimal intent across runtimes. Callers must store the returned
    string in a field whose schema declares decimal-string semantics.
    """

    if isinstance(value, str):
        if not value or value != value.strip():
            raise CanonicalJSONError("decimal text must be non-empty and unpadded")
        try:
            decimal_value = Decimal(value)
        except InvalidOperation as exc:
            raise CanonicalJSONError("invalid decimal text") from exc
    elif isinstance(value, Decimal):
        decimal_value = value
    else:
        raise TypeError("value must be Decimal or str")

    if not decimal_value.is_finite():
        raise CanonicalJSONError("decimal must be finite")
    if decimal_value.is_zero():
        return "0"

    rendered = format(decimal_value, "f")
    if "." in rendered:
        rendered = rendered.rstrip("0").rstrip(".")
    if rendered.startswith("."):
        rendered = f"0{rendered}"
    elif rendered.startswith("-."):
        rendered = rendered.replace("-.", "-0.", 1)
    return rendered


def canonical_timestamp(value: datetime | str) -> str:
    """Normalize an RFC 3339 timestamp to UTC with millisecond precision.

    Canonical output has either no fractional part or exactly three digits.
    Inputs carrying sub-millisecond precision are rejected rather than rounded.
    """

    if isinstance(value, str):
        _validate_unicode_scalar_text(value, "timestamp")
        if not _TIMESTAMP_RE.fullmatch(value):
            raise CanonicalJSONError("timestamp must be strict RFC 3339")
        if value.endswith("-00:00"):
            raise CanonicalJSONError("timestamp offset -00:00 is ambiguous")
        parse_value = value[:-1] + "+00:00" if value.endswith("Z") else value
        try:
            parsed = datetime.fromisoformat(parse_value)
        except ValueError as exc:
            raise CanonicalJSONError("timestamp is not a valid calendar instant") from exc
    elif isinstance(value, datetime):
        parsed = value
    else:
        raise TypeError("timestamp must be datetime or str")

    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise CanonicalJSONError("timestamp must include a UTC offset")
    offset = parsed.utcoffset()
    assert offset is not None
    if offset.total_seconds() % 60:
        raise CanonicalJSONError("timestamp offset must use whole minutes")

    utc_value = parsed.astimezone(timezone.utc)
    if utc_value.microsecond % 1000:
        raise CanonicalJSONError("timestamp precision finer than milliseconds is forbidden")

    prefix = (
        f"{utc_value.year:04d}-{utc_value.month:02d}-{utc_value.day:02d}T"
        f"{utc_value.hour:02d}:{utc_value.minute:02d}:{utc_value.second:02d}"
    )
    if utc_value.microsecond:
        return f"{prefix}.{utc_value.microsecond // 1000:03d}Z"
    return f"{prefix}Z"


def actor_ref_value(value: ActorRef) -> dict[str, CanonicalValue]:
    if not isinstance(value, ActorRef):
        raise TypeError("value must be an ActorRef")
    return {"type": value.actor_type, "id": value.actor_id}


def authority_ref_value(value: AuthorityRef) -> dict[str, CanonicalValue]:
    if not isinstance(value, AuthorityRef):
        raise TypeError("value must be an AuthorityRef")
    return {
        "capability_lease_id": value.capability_lease_id,
        "capability_revision": value.capability_revision,
    }


def producer_ref_value(value: ProducerRef) -> dict[str, CanonicalValue]:
    if not isinstance(value, ProducerRef):
        raise TypeError("value must be a ProducerRef")
    return {"component": value.component, "version": value.version}


def command_envelope_value(command: CommandEnvelope) -> dict[str, CanonicalValue]:
    if not isinstance(command, CommandEnvelope):
        raise TypeError("command must be a CommandEnvelope")
    return {
        "command_id": command.command_id,
        "command_type": command.command_type,
        "command_schema": command.command_schema,
        "target_stream": command.target_stream,
        "expected_stream_version": command.expected_stream_version,
        "issued_at": canonical_timestamp(command.issued_at),
        "issuer": actor_ref_value(command.issuer),
        "authority": authority_ref_value(command.authority),
        "correlation_id": command.correlation_id,
        "idempotency_key": command.idempotency_key,
        "payload": _prepare(command.payload, "$.payload", set()),
    }


def pending_event_value(event: PendingEvent) -> dict[str, CanonicalValue]:
    if not isinstance(event, PendingEvent):
        raise TypeError("event must be a PendingEvent")
    return {
        "event_type": event.event_type,
        "payload_schema": event.payload_schema,
        "affects_domain_state": event.affects_domain_state,
        "payload": _prepare(event.payload, "$.payload", set()),
    }


def pending_batch_value(events: Iterable[PendingEvent]) -> list[CanonicalValue]:
    return [pending_event_value(event) for event in snapshot_pending_batch(events)]


def event_envelope_value(
    event: EventEnvelope, *, include_event_hash: bool = True
) -> dict[str, CanonicalValue]:
    if not isinstance(event, EventEnvelope):
        raise TypeError("event must be an EventEnvelope")
    value: dict[str, CanonicalValue] = {
        "event_id": event.event_id,
        "event_type": event.event_type,
        "envelope_schema_version": event.envelope_schema_version,
        "payload_schema": event.payload_schema,
        "stream_id": event.stream_id,
        "stream_version": event.stream_version,
        "batch_id": event.batch_id,
        "batch_index": event.batch_index,
        "batch_size": event.batch_size,
        "occurred_at": canonical_timestamp(event.occurred_at),
        "recorded_at": canonical_timestamp(event.recorded_at),
        "producer": producer_ref_value(event.producer),
        "initiator": actor_ref_value(event.initiator),
        "authority": authority_ref_value(event.authority),
        "causation_id": event.causation_id,
        "correlation_id": event.correlation_id,
        "affects_domain_state": event.affects_domain_state,
        "payload_digest": event.payload_digest,
        "payload_ref": event.payload_ref,
        "previous_hash": event.previous_hash,
    }
    if include_event_hash:
        value["event_hash"] = event.event_hash
    return value


def event_hash_input_value(event: EventEnvelope) -> dict[str, CanonicalValue]:
    """Return hash-input metadata: previous_hash included, event_hash excluded."""

    value = event_envelope_value(event, include_event_hash=False)
    if "previous_hash" not in value:  # pragma: no cover - invariant guard
        raise AssertionError("previous_hash must be part of event hash input")
    return value


def canonical_command_bytes(command: CommandEnvelope) -> bytes:
    return canonical_json_bytes(command_envelope_value(command))


def canonical_pending_batch_bytes(events: Iterable[PendingEvent]) -> bytes:
    return canonical_json_bytes(pending_batch_value(events))


def canonical_event_bytes(event: EventEnvelope) -> bytes:
    return canonical_json_bytes(event_envelope_value(event))


def canonical_event_hash_input_bytes(event: EventEnvelope) -> bytes:
    return canonical_json_bytes(event_hash_input_value(event))
