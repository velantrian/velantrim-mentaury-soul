"""P0-009 R0 integrity computation and first-failure diagnostics."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, replace
from enum import StrEnum

from mentaury.contracts import (
    EventEnvelope,
    canonical_event_hash_input_bytes,
    canonical_json_bytes,
    canonical_timestamp,
)
from mentaury.validation import SchemaRegistry

from .sqlite_store import SQLiteEventPayloadStore
from .stream_meta import GENESIS_HASH, read_stream_meta


class IntegrityCode(StrEnum):
    STREAM_VERSION_GAP = "STREAM_VERSION_GAP"
    BATCH_INCOMPLETE = "BATCH_INCOMPLETE"
    BATCH_ORDER_MISMATCH = "BATCH_ORDER_MISMATCH"
    SCHEMA_INVALID = "SCHEMA_INVALID"
    PAYLOAD_MISSING = "PAYLOAD_MISSING"
    PAYLOAD_DECODE_ERROR = "PAYLOAD_DECODE_ERROR"
    PAYLOAD_DIGEST_MISMATCH = "PAYLOAD_DIGEST_MISMATCH"
    PREVIOUS_HASH_MISMATCH = "PREVIOUS_HASH_MISMATCH"
    EVENT_HASH_MISMATCH = "EVENT_HASH_MISMATCH"
    STREAM_META_VERSION_MISMATCH = "STREAM_META_VERSION_MISMATCH"
    STREAM_META_HASH_MISMATCH = "STREAM_META_HASH_MISMATCH"
    STREAM_META_COUNT_MISMATCH = "STREAM_META_COUNT_MISMATCH"


@dataclass(frozen=True, slots=True)
class IntegrityFailure:
    code: IntegrityCode
    stream_id: str
    message: str
    event_id: str | None = None
    stream_version: int | None = None


@dataclass(frozen=True, slots=True)
class R0IntegrityReport:
    stream_id: str
    ok: bool
    checked_events: int
    failure: IntegrityFailure | None


def compute_payload_digest(payload_bytes: bytes) -> str:
    if not isinstance(payload_bytes, bytes):
        raise TypeError("payload_bytes must be bytes")
    return f"sha256:{hashlib.sha256(payload_bytes).hexdigest()}"


def compute_event_hash(event: EventEnvelope) -> str:
    if not isinstance(event, EventEnvelope):
        raise TypeError("event must be an EventEnvelope")
    digest = hashlib.sha256(canonical_event_hash_input_bytes(event)).hexdigest()
    return f"sha256:{digest}"


def seal_event(
    event: EventEnvelope,
    payload: object,
    *,
    previous_hash: str | None = None,
) -> EventEnvelope:
    """Return a canonical-timestamp event with recomputed digest and event hash."""

    payload_bytes = canonical_json_bytes(payload)
    provisional = replace(
        event,
        occurred_at=canonical_timestamp(event.occurred_at),
        recorded_at=canonical_timestamp(event.recorded_at),
        payload_digest=compute_payload_digest(payload_bytes),
        previous_hash=event.previous_hash if previous_hash is None else previous_hash,
        event_hash="sha256:pending",
    )
    return replace(provisional, event_hash=compute_event_hash(provisional))


class R0IntegrityVerifier:
    """Verify one stream and return only the first actionable integrity failure."""

    def __init__(self, store: SQLiteEventPayloadStore, registry: SchemaRegistry) -> None:
        if not isinstance(store, SQLiteEventPayloadStore):
            raise TypeError("store must be a SQLiteEventPayloadStore")
        if not isinstance(registry, SchemaRegistry):
            raise TypeError("registry must be a SchemaRegistry")
        self._store = store
        self._registry = registry

    def verify_stream(self, stream_id: str) -> R0IntegrityReport:
        self._store._require_initialized()
        events = self._store.list_stream(stream_id)
        meta = read_stream_meta(self._store._connection, stream_id)
        if not events:
            if meta.current_version != 0:
                return self._fail(
                    stream_id,
                    0,
                    IntegrityCode.STREAM_META_VERSION_MISMATCH,
                    "empty stream must have current_version 0",
                )
            if meta.last_event_hash != GENESIS_HASH:
                return self._fail(
                    stream_id,
                    0,
                    IntegrityCode.STREAM_META_HASH_MISMATCH,
                    "empty stream must use GENESIS_HASH",
                )
            if meta.event_count != 0:
                return self._fail(
                    stream_id,
                    0,
                    IntegrityCode.STREAM_META_COUNT_MISMATCH,
                    "empty stream must have event_count 0",
                )
            return R0IntegrityReport(stream_id, True, 0, None)

        expected_previous_hash = GENESIS_HASH
        checked = 0
        batch_start = 0
        for index, event in enumerate(events):
            expected_version = index + 1
            if event.stream_version != expected_version:
                return self._event_fail(
                    event,
                    checked,
                    IntegrityCode.STREAM_VERSION_GAP,
                    f"expected stream version {expected_version}",
                )

            if index == batch_start:
                if event.batch_index != 0:
                    return self._event_fail(
                        event,
                        checked,
                        IntegrityCode.BATCH_ORDER_MISMATCH,
                        "batch must start at index 0",
                    )
                batch_end = batch_start + event.batch_size
                if batch_end > len(events):
                    return self._event_fail(
                        event,
                        checked,
                        IntegrityCode.BATCH_INCOMPLETE,
                        "batch extends beyond available stream events",
                    )
                for expected_index, member in enumerate(events[batch_start:batch_end]):
                    if (
                        member.batch_id != event.batch_id
                        or member.batch_size != event.batch_size
                        or member.batch_index != expected_index
                    ):
                        return self._event_fail(
                            member,
                            checked,
                            IntegrityCode.BATCH_ORDER_MISMATCH,
                            "batch identifiers, size, or order are inconsistent",
                        )
                batch_start = batch_end

            envelope_issues = self._registry.validate_event_envelope(event)
            if envelope_issues:
                return self._event_fail(
                    event,
                    checked,
                    IntegrityCode.SCHEMA_INVALID,
                    str(envelope_issues[0]),
                )

            payload = self._store.load_payload(event.payload_ref)
            if payload is None:
                return self._event_fail(
                    event,
                    checked,
                    IntegrityCode.PAYLOAD_MISSING,
                    "payload material is missing",
                )
            try:
                decoded = json.loads(payload.payload_bytes.decode("utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError) as exc:
                return self._event_fail(
                    event,
                    checked,
                    IntegrityCode.PAYLOAD_DECODE_ERROR,
                    f"payload cannot be decoded: {exc}",
                )
            payload_issues = self._registry.validate_event_payload(event, decoded)
            if payload_issues:
                return self._event_fail(
                    event,
                    checked,
                    IntegrityCode.SCHEMA_INVALID,
                    str(payload_issues[0]),
                )
            recomputed_payload_digest = compute_payload_digest(payload.payload_bytes)
            if event.payload_digest != recomputed_payload_digest:
                return self._event_fail(
                    event,
                    checked,
                    IntegrityCode.PAYLOAD_DIGEST_MISMATCH,
                    "stored payload digest differs from recomputed digest",
                )
            if event.previous_hash != expected_previous_hash:
                return self._event_fail(
                    event,
                    checked,
                    IntegrityCode.PREVIOUS_HASH_MISMATCH,
                    "previous_hash does not match the prior event hash",
                )
            recomputed_event_hash = compute_event_hash(event)
            if event.event_hash != recomputed_event_hash:
                return self._event_fail(
                    event,
                    checked,
                    IntegrityCode.EVENT_HASH_MISMATCH,
                    "stored event hash differs from recomputed hash",
                )
            expected_previous_hash = event.event_hash
            checked += 1

        tail = events[-1]
        if meta.current_version != tail.stream_version:
            return self._fail(
                stream_id,
                checked,
                IntegrityCode.STREAM_META_VERSION_MISMATCH,
                "stream_meta current_version differs from ledger tail",
            )
        if meta.last_event_hash != tail.event_hash:
            return self._fail(
                stream_id,
                checked,
                IntegrityCode.STREAM_META_HASH_MISMATCH,
                "stream_meta last_event_hash differs from ledger tail",
            )
        if meta.event_count != len(events):
            return self._fail(
                stream_id,
                checked,
                IntegrityCode.STREAM_META_COUNT_MISMATCH,
                "stream_meta event_count differs from ledger count",
            )
        return R0IntegrityReport(stream_id, True, checked, None)

    @staticmethod
    def _event_fail(
        event: EventEnvelope,
        checked: int,
        code: IntegrityCode,
        message: str,
    ) -> R0IntegrityReport:
        return R0IntegrityReport(
            event.stream_id,
            False,
            checked,
            IntegrityFailure(
                code,
                event.stream_id,
                message,
                event.event_id,
                event.stream_version,
            ),
        )

    @staticmethod
    def _fail(
        stream_id: str,
        checked: int,
        code: IntegrityCode,
        message: str,
    ) -> R0IntegrityReport:
        return R0IntegrityReport(
            stream_id,
            False,
            checked,
            IntegrityFailure(code, stream_id, message),
        )
