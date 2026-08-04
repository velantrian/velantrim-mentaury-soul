from __future__ import annotations

import json
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path

import pytest

from mentaury.contracts import (
    SAFE_INTEGER_MAX,
    ActorRef,
    AuthorityRef,
    CanonicalJSONError,
    CommandEnvelope,
    EventEnvelope,
    PendingEvent,
    ProducerRef,
    canonical_command_bytes,
    canonical_decimal_string,
    canonical_event_bytes,
    canonical_event_hash_input_bytes,
    canonical_json_bytes,
    canonical_json_text,
    canonical_pending_batch_bytes,
    canonical_timestamp,
    event_hash_input_value,
)

FIXTURES = Path(__file__).parent / "fixtures" / "canonical_json_v1_vectors.json"


def actor() -> ActorRef:
    return ActorRef("operator", "operator:primary")


def authority() -> AuthorityRef:
    return AuthorityRef("CAP-81", 2)


def event() -> EventEnvelope:
    return EventEnvelope(
        event_id="EVT-1",
        event_type="BELIEF_CREATED",
        envelope_schema_version=1,
        payload_schema="belief-created/v1",
        stream_id="belief:B-204",
        stream_version=1,
        batch_id="BATCH-1",
        batch_index=0,
        batch_size=1,
        occurred_at="2026-08-05T00:00:00+02:00",
        recorded_at="2026-08-04T22:00:00.12Z",
        producer=ProducerRef("belief-command-handler", "0.1.0"),
        initiator=actor(),
        authority=authority(),
        causation_id="CMD-1",
        correlation_id="CORR-12",
        affects_domain_state=True,
        payload_digest="sha256:payload",
        payload_ref="PAYLOAD-1",
        previous_hash="sha256:genesis",
        event_hash="sha256:event",
    )


def test_language_neutral_conformance_vectors() -> None:
    vectors = json.loads(FIXTURES.read_text(encoding="utf-8"))
    assert vectors["profile"] == "MENTAURY_CANONICAL_JSON_V1"
    assert vectors["safe_integer_max"] == SAFE_INTEGER_MAX

    for vector in vectors["canonical_values"]:
        canonical = canonical_json_bytes(vector["value"])
        assert canonical.decode("utf-8") == vector["canonical"], vector["name"]
        assert canonical.hex() == vector["utf8_hex"], vector["name"]

    for vector in vectors["timestamps"]:
        assert canonical_timestamp(vector["input"]) == vector["canonical"]

    for vector in vectors["decimal_strings"]:
        assert canonical_decimal_string(vector["input"]) == vector["canonical"]


def test_object_order_whitespace_and_unicode_policy() -> None:
    decomposed = "e\u0301"
    composed = "é"
    text = canonical_json_text({"z": decomposed, "a": composed})

    assert text == '{"a":"é","z":"é"}'
    assert " " not in text
    assert decomposed in text
    assert composed in text


def test_float_decimal_and_unsafe_integer_are_rejected() -> None:
    with pytest.raises(CanonicalJSONError, match="float"):
        canonical_json_bytes({"n": 1.0})
    with pytest.raises(CanonicalJSONError, match="Decimal"):
        canonical_json_bytes({"n": Decimal("1.0")})
    with pytest.raises(CanonicalJSONError, match="safe range"):
        canonical_json_bytes({"n": SAFE_INTEGER_MAX + 1})


def test_lone_surrogates_and_cycles_are_rejected() -> None:
    with pytest.raises(CanonicalJSONError, match="lone surrogate"):
        canonical_json_text({"bad": "\ud800"})

    cyclic: list[object] = []
    cyclic.append(cyclic)
    with pytest.raises(CanonicalJSONError, match="cyclic sequence"):
        canonical_json_text(cyclic)


def test_timestamp_is_utc_and_millisecond_exact() -> None:
    assert canonical_timestamp("2026-08-04T22:00:00.12Z") == "2026-08-04T22:00:00.120Z"
    assert canonical_timestamp("2026-08-05T00:00:00+02:00") == "2026-08-04T22:00:00Z"
    assert canonical_timestamp(datetime(2026, 8, 4, 22, tzinfo=timezone.utc)) == "2026-08-04T22:00:00Z"

    with pytest.raises(CanonicalJSONError, match="milliseconds"):
        canonical_timestamp("2026-08-04T22:00:00.123456Z")
    with pytest.raises(CanonicalJSONError, match="UTC offset"):
        canonical_timestamp(datetime(2026, 8, 4, 22))
    with pytest.raises(CanonicalJSONError, match="strict RFC 3339"):
        canonical_timestamp("2026-08-04 22:00:00Z")
    with pytest.raises(CanonicalJSONError, match="ambiguous"):
        canonical_timestamp("2026-08-04T22:00:00-00:00")


def test_decimal_encoding_is_explicit_and_canonical() -> None:
    assert canonical_decimal_string(Decimal("1.2300")) == "1.23"
    assert canonical_decimal_string(Decimal("-0")) == "0"
    assert canonical_decimal_string("1E+3") == "1000"
    with pytest.raises(CanonicalJSONError, match="finite"):
        canonical_decimal_string("NaN")


def test_command_and_pending_batch_serialization() -> None:
    command = CommandEnvelope(
        command_id="CMD-1",
        command_type="CREATE_BELIEF",
        command_schema="create-belief/v1",
        target_stream="belief:B-204",
        expected_stream_version=0,
        issued_at="2026-08-05T00:00:00+02:00",
        issuer=actor(),
        authority=authority(),
        correlation_id="CORR-12",
        idempotency_key="request-1",
        payload={"statement": "alpha", "count": 1},
    )
    encoded = canonical_command_bytes(command).decode("utf-8")
    assert '"issued_at":"2026-08-04T22:00:00Z"' in encoded
    assert '"issuer":{"id":"operator:primary","type":"operator"}' in encoded

    batch = canonical_pending_batch_bytes(
        [
            PendingEvent("FIRST", "first/v1", True, {"n": 1}),
            PendingEvent("SECOND", "second/v1", False, {"n": 2}),
        ]
    ).decode("utf-8")
    assert batch.index('"event_type":"FIRST"') < batch.index('"event_type":"SECOND"')


def test_event_hash_input_excludes_event_hash_but_includes_previous_hash() -> None:
    value = event_hash_input_value(event())
    assert "event_hash" not in value
    assert value["previous_hash"] == "sha256:genesis"

    hash_input = canonical_event_hash_input_bytes(event()).decode("utf-8")
    complete = canonical_event_bytes(event()).decode("utf-8")
    assert '"event_hash"' not in hash_input
    assert '"previous_hash":"sha256:genesis"' in hash_input
    assert '"event_hash":"sha256:event"' in complete
    assert '"recorded_at":"2026-08-04T22:00:00.120Z"' in complete
