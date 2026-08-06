"""P0-013 deterministic full-replay versus snapshot-tail verification."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import replace
from pathlib import Path

import pytest

from mentaury.contracts import (
    ActorRef,
    AuthorityRef,
    EventEnvelope,
    ProducerRef,
)
from mentaury.replay import (
    R1ReplayVerifier,
    ReplayFailureCode,
    ReplaySnapshot,
    ReplayStateBudget,
    compute_replay_state_hash,
    make_replay_snapshot,
)
from mentaury.storage import (
    GENESIS_HASH,
    REDACTION_EVENT_TYPE,
    REDACTION_PAYLOAD_SCHEMA,
    RedactionRequest,
    SQLiteEventPayloadStore,
    SQLiteRedactionExecutor,
    VerificationBudget,
)
from mentaury.validation import (
    EventSchemaDefinition,
    IntegerSpec,
    ObjectSpec,
    SchemaRegistry,
    StringSpec,
)


STREAM_ID = "counter:primary"
COUNTER_EVENT = "COUNTER_INCREMENTED"
COUNTER_SCHEMA = "counter-incremented/v1"
NOTE_EVENT = "NOTE_RECORDED"
NOTE_SCHEMA = "note-recorded/v1"
UNKNOWN_EVENT = "UNKNOWN_DOMAIN_EVENT"
UNKNOWN_SCHEMA = "unknown-domain-event/v1"


class CounterReducer:
    reducer_id = "counter-projection"
    reducer_version = "1"
    supported_event_schemas = frozenset({(COUNTER_EVENT, COUNTER_SCHEMA)})

    def initial_state(self) -> Mapping[str, object]:
        return {"total": 0, "event_ids": []}

    def apply(self, state, event, payload) -> Mapping[str, object]:
        total = state["total"]
        event_ids = state["event_ids"]
        delta = payload["delta"]
        assert isinstance(total, int)
        assert isinstance(event_ids, tuple)
        assert isinstance(delta, int)
        return {
            "total": total + delta,
            "event_ids": [*event_ids, event.event_id],
        }


class NondeterministicReducer(CounterReducer):
    def __init__(self) -> None:
        self.calls = 0

    def apply(self, state, event, payload) -> Mapping[str, object]:
        self.calls += 1
        return {"total": self.calls, "event_ids": [event.event_id]}


class ReusingReducer(CounterReducer):
    def apply(self, state, event, payload) -> Mapping[str, object]:
        return state


class MutatingReducer(CounterReducer):
    def apply(self, state, event, payload) -> Mapping[str, object]:
        state["total"] = 99  # type: ignore[index]
        return state


class InvalidInitialReducer(CounterReducer):
    def initial_state(self) -> Mapping[str, object]:
        return {"total": 1.5, "event_ids": []}


class InvalidContractReducer(CounterReducer):
    supported_event_schemas = {(COUNTER_EVENT, COUNTER_SCHEMA)}


def _registry() -> SchemaRegistry:
    return SchemaRegistry(
        [
            EventSchemaDefinition(
                event_type=COUNTER_EVENT,
                payload_schema=COUNTER_SCHEMA,
                affects_domain_state=True,
                payload=ObjectSpec(
                    {"delta": IntegerSpec(minimum=0)},
                    required=frozenset({"delta"}),
                ),
            ),
            EventSchemaDefinition(
                event_type=NOTE_EVENT,
                payload_schema=NOTE_SCHEMA,
                affects_domain_state=False,
                payload=ObjectSpec(
                    {"message": StringSpec(min_length=1)},
                    required=frozenset({"message"}),
                ),
            ),
            EventSchemaDefinition(
                event_type=UNKNOWN_EVENT,
                payload_schema=UNKNOWN_SCHEMA,
                affects_domain_state=True,
                payload=ObjectSpec(
                    {"value": IntegerSpec(minimum=0)},
                    required=frozenset({"value"}),
                ),
            ),
            EventSchemaDefinition(
                event_type=REDACTION_EVENT_TYPE,
                payload_schema=REDACTION_PAYLOAD_SCHEMA,
                affects_domain_state=True,
                payload=ObjectSpec(
                    {
                        "target_event_id": StringSpec(min_length=1),
                        "target_stream_id": StringSpec(min_length=1),
                        "target_payload_ref": StringSpec(min_length=1),
                        "reason": StringSpec(min_length=1),
                        "authority": ObjectSpec(
                            {
                                "capability_lease_id": StringSpec(min_length=1),
                                "capability_revision": IntegerSpec(minimum=0),
                            },
                            required=frozenset(
                                {"capability_lease_id", "capability_revision"}
                            ),
                        ),
                    },
                    required=frozenset(
                        {
                            "target_event_id",
                            "target_stream_id",
                            "target_payload_ref",
                            "reason",
                            "authority",
                        }
                    ),
                ),
            ),
        ]
    )


def _budget(
    *,
    max_events: int = 100,
    max_payload_bytes: int = 10_000,
    max_total_payload_bytes: int = 100_000,
) -> VerificationBudget:
    return VerificationBudget(
        max_events=max_events,
        max_payload_bytes=max_payload_bytes,
        max_total_payload_bytes=max_total_payload_bytes,
    )


def _raw_event(
    *,
    event_id: str,
    stream_version: int,
    event_type: str,
    payload_schema: str,
    affects_domain_state: bool,
) -> EventEnvelope:
    return EventEnvelope(
        event_id=event_id,
        event_type=event_type,
        envelope_schema_version=1,
        payload_schema=payload_schema,
        stream_id=STREAM_ID,
        stream_version=stream_version,
        batch_id=f"BATCH-{event_id}",
        batch_index=0,
        batch_size=1,
        occurred_at="2026-08-06T00:00:00Z",
        recorded_at="2026-08-06T00:00:00Z",
        producer=ProducerRef("p0-013-test", "0.1.0"),
        initiator=ActorRef("operator", "operator:primary"),
        authority=AuthorityRef("CAP-P0-013", 1),
        causation_id=f"CMD-{event_id}",
        correlation_id="CORR-P0-013",
        affects_domain_state=affects_domain_state,
        payload_digest="sha256:untrusted",
        payload_ref=f"PAYLOAD-{event_id}",
        previous_hash="sha256:untrusted",
        event_hash="sha256:untrusted",
    )


def _append_counter(
    store: SQLiteEventPayloadStore,
    event_id: str,
    version: int,
    delta: int,
) -> EventEnvelope:
    return store.append_one(
        _raw_event(
            event_id=event_id,
            stream_version=version,
            event_type=COUNTER_EVENT,
            payload_schema=COUNTER_SCHEMA,
            affects_domain_state=True,
        ),
        {"delta": delta},
        registry=_registry(),
    )


def _append_note(
    store: SQLiteEventPayloadStore,
    event_id: str,
    version: int,
) -> EventEnvelope:
    return store.append_one(
        _raw_event(
            event_id=event_id,
            stream_version=version,
            event_type=NOTE_EVENT,
            payload_schema=NOTE_SCHEMA,
            affects_domain_state=False,
        ),
        {"message": "diagnostic only"},
        registry=_registry(),
    )


def _append_unknown_domain(
    store: SQLiteEventPayloadStore,
    event_id: str,
    version: int,
) -> EventEnvelope:
    return store.append_one(
        _raw_event(
            event_id=event_id,
            stream_version=version,
            event_type=UNKNOWN_EVENT,
            payload_schema=UNKNOWN_SCHEMA,
            affects_domain_state=True,
        ),
        {"value": 1},
        registry=_registry(),
    )


def _state_budget(
    *,
    max_state_bytes: int = 10_000,
    max_total_state_bytes: int = 100_000,
) -> ReplayStateBudget:
    return ReplayStateBudget(
        max_state_bytes=max_state_bytes,
        max_total_state_bytes=max_total_state_bytes,
    )


def _verifier(
    store: SQLiteEventPayloadStore,
    reducer=None,
    *,
    budget: VerificationBudget | None = None,
    state_budget: ReplayStateBudget | None = None,
) -> R1ReplayVerifier:
    return R1ReplayVerifier(
        store,
        _registry(),
        budget or _budget(),
        state_budget or _state_budget(),
        reducer or CounterReducer(),
    )


def _snapshot_after_first(event: EventEnvelope) -> ReplaySnapshot:
    return make_replay_snapshot(
        reducer_id=CounterReducer.reducer_id,
        reducer_version=CounterReducer.reducer_version,
        stream_id=STREAM_ID,
        through_stream_version=1,
        through_event_hash=event.event_hash,
        state={"total": 2, "event_ids": [event.event_id]},
    )


def _failure_code(report) -> ReplayFailureCode:
    assert not report.ok
    assert report.failure is not None
    return report.failure.code


def test_full_replay_equals_snapshot_plus_tail() -> None:
    with SQLiteEventPayloadStore.in_memory() as store:
        store.initialize_schema()
        first = _append_counter(store, "EVT-1", 1, 2)
        _append_note(store, "EVT-2", 2)
        _append_counter(store, "EVT-3", 3, 5)

        report = _verifier(store).verify_stream(
            STREAM_ID,
            _snapshot_after_first(first),
        )

        expected_hash = compute_replay_state_hash(
            {"total": 7, "event_ids": ["EVT-1", "EVT-3"]}
        )
        assert report.ok
        assert report.checked_events == 3
        assert report.applied_events == 2
        assert report.full_state_hash == expected_hash
        assert report.tail_state_hash == expected_hash
        assert report.verified_through_stream_version == 3
        assert report.verified_through_event_hash == store.list_stream(STREAM_ID)[-1].event_hash
        assert report.failure is None


def test_genesis_snapshot_replays_complete_stream() -> None:
    with SQLiteEventPayloadStore.in_memory() as store:
        store.initialize_schema()
        _append_counter(store, "EVT-1", 1, 3)
        snapshot = make_replay_snapshot(
            reducer_id=CounterReducer.reducer_id,
            reducer_version=CounterReducer.reducer_version,
            stream_id=STREAM_ID,
            through_stream_version=0,
            through_event_hash=GENESIS_HASH,
            state={"total": 0, "event_ids": []},
        )

        report = _verifier(store).verify_stream(STREAM_ID, snapshot)

        assert report.ok
        assert report.full_state_hash == report.tail_state_hash


def test_empty_stream_accepts_genesis_snapshot() -> None:
    with SQLiteEventPayloadStore.in_memory() as store:
        store.initialize_schema()
        snapshot = make_replay_snapshot(
            reducer_id=CounterReducer.reducer_id,
            reducer_version=CounterReducer.reducer_version,
            stream_id=STREAM_ID,
            through_stream_version=0,
            through_event_hash=GENESIS_HASH,
            state={"total": 0, "event_ids": []},
        )

        report = _verifier(store).verify_stream(STREAM_ID, snapshot)

        assert report.ok
        assert report.checked_events == 0
        assert report.applied_events == 0


def test_non_state_event_can_be_snapshot_anchor() -> None:
    with SQLiteEventPayloadStore.in_memory() as store:
        store.initialize_schema()
        first = _append_counter(store, "EVT-1", 1, 2)
        note = _append_note(store, "EVT-2", 2)
        _append_counter(store, "EVT-3", 3, 1)
        snapshot = make_replay_snapshot(
            reducer_id=CounterReducer.reducer_id,
            reducer_version=CounterReducer.reducer_version,
            stream_id=STREAM_ID,
            through_stream_version=2,
            through_event_hash=note.event_hash,
            state={"total": 2, "event_ids": [first.event_id]},
        )

        report = _verifier(store).verify_stream(STREAM_ID, snapshot)

        assert report.ok
        assert report.applied_events == 2


def test_snapshot_reducer_version_mismatch_fails_closed() -> None:
    with SQLiteEventPayloadStore.in_memory() as store:
        store.initialize_schema()
        first = _append_counter(store, "EVT-1", 1, 2)
        snapshot = replace(_snapshot_after_first(first), reducer_version="2")

        report = _verifier(store).verify_stream(STREAM_ID, snapshot)

        assert _failure_code(report) is ReplayFailureCode.SNAPSHOT_REDUCER_MISMATCH


def test_snapshot_stream_mismatch_fails_closed() -> None:
    with SQLiteEventPayloadStore.in_memory() as store:
        store.initialize_schema()
        first = _append_counter(store, "EVT-1", 1, 2)
        snapshot = replace(_snapshot_after_first(first), stream_id="counter:other")

        report = _verifier(store).verify_stream(STREAM_ID, snapshot)

        assert _failure_code(report) is ReplayFailureCode.SNAPSHOT_STREAM_MISMATCH


def test_snapshot_version_beyond_tail_fails_closed() -> None:
    with SQLiteEventPayloadStore.in_memory() as store:
        store.initialize_schema()
        first = _append_counter(store, "EVT-1", 1, 2)
        snapshot = replace(
            _snapshot_after_first(first),
            through_stream_version=2,
        )

        report = _verifier(store).verify_stream(STREAM_ID, snapshot)

        assert _failure_code(report) is ReplayFailureCode.SNAPSHOT_VERSION_OUT_OF_RANGE


def test_snapshot_anchor_mismatch_fails_closed() -> None:
    with SQLiteEventPayloadStore.in_memory() as store:
        store.initialize_schema()
        first = _append_counter(store, "EVT-1", 1, 2)
        snapshot = replace(
            _snapshot_after_first(first),
            through_event_hash="sha256:wrong-anchor",
        )

        report = _verifier(store).verify_stream(STREAM_ID, snapshot)

        assert _failure_code(report) is ReplayFailureCode.SNAPSHOT_ANCHOR_MISMATCH


def test_snapshot_state_hash_tampering_is_detected() -> None:
    with SQLiteEventPayloadStore.in_memory() as store:
        store.initialize_schema()
        first = _append_counter(store, "EVT-1", 1, 2)
        snapshot = replace(
            _snapshot_after_first(first),
            state_hash="sha256:tampered",
        )

        report = _verifier(store).verify_stream(STREAM_ID, snapshot)

        assert _failure_code(report) is ReplayFailureCode.SNAPSHOT_STATE_HASH_MISMATCH


def test_self_consistent_but_wrong_snapshot_state_is_rejected() -> None:
    with SQLiteEventPayloadStore.in_memory() as store:
        store.initialize_schema()
        first = _append_counter(store, "EVT-1", 1, 2)
        snapshot = make_replay_snapshot(
            reducer_id=CounterReducer.reducer_id,
            reducer_version=CounterReducer.reducer_version,
            stream_id=STREAM_ID,
            through_stream_version=1,
            through_event_hash=first.event_hash,
            state={"total": 999, "event_ids": [first.event_id]},
        )

        report = _verifier(store).verify_stream(STREAM_ID, snapshot)

        assert _failure_code(report) is ReplayFailureCode.SNAPSHOT_STATE_MISMATCH


def test_unknown_state_affecting_schema_fails_closed() -> None:
    with SQLiteEventPayloadStore.in_memory() as store:
        store.initialize_schema()
        _append_unknown_domain(store, "EVT-1", 1)
        snapshot = make_replay_snapshot(
            reducer_id=CounterReducer.reducer_id,
            reducer_version=CounterReducer.reducer_version,
            stream_id=STREAM_ID,
            through_stream_version=0,
            through_event_hash=GENESIS_HASH,
            state={"total": 0, "event_ids": []},
        )

        report = _verifier(store).verify_stream(STREAM_ID, snapshot)

        assert _failure_code(report) is ReplayFailureCode.UNKNOWN_EVENT_SCHEMA


def test_nondeterministic_reducer_is_detected() -> None:
    with SQLiteEventPayloadStore.in_memory() as store:
        store.initialize_schema()
        _append_counter(store, "EVT-1", 1, 1)
        snapshot = make_replay_snapshot(
            reducer_id=CounterReducer.reducer_id,
            reducer_version=CounterReducer.reducer_version,
            stream_id=STREAM_ID,
            through_stream_version=0,
            through_event_hash=GENESIS_HASH,
            state={"total": 0, "event_ids": []},
        )

        report = _verifier(store, NondeterministicReducer()).verify_stream(
            STREAM_ID,
            snapshot,
        )

        assert _failure_code(report) is ReplayFailureCode.REDUCER_NONDETERMINISTIC


def test_reducer_cannot_reuse_input_state() -> None:
    with SQLiteEventPayloadStore.in_memory() as store:
        store.initialize_schema()
        _append_counter(store, "EVT-1", 1, 1)
        snapshot = make_replay_snapshot(
            reducer_id=CounterReducer.reducer_id,
            reducer_version=CounterReducer.reducer_version,
            stream_id=STREAM_ID,
            through_stream_version=0,
            through_event_hash=GENESIS_HASH,
            state={"total": 0, "event_ids": []},
        )

        report = _verifier(store, ReusingReducer()).verify_stream(STREAM_ID, snapshot)

        assert _failure_code(report) is ReplayFailureCode.REDUCER_REUSED_INPUT


def test_reducer_inputs_are_immutable() -> None:
    with SQLiteEventPayloadStore.in_memory() as store:
        store.initialize_schema()
        _append_counter(store, "EVT-1", 1, 1)
        snapshot = make_replay_snapshot(
            reducer_id=CounterReducer.reducer_id,
            reducer_version=CounterReducer.reducer_version,
            stream_id=STREAM_ID,
            through_stream_version=0,
            through_event_hash=GENESIS_HASH,
            state={"total": 0, "event_ids": []},
        )

        report = _verifier(store, MutatingReducer()).verify_stream(STREAM_ID, snapshot)

        assert _failure_code(report) is ReplayFailureCode.REDUCER_ERROR
        assert report.failure is not None
        assert "TypeError" in report.failure.message


def test_invalid_initial_state_fails_closed() -> None:
    with SQLiteEventPayloadStore.in_memory() as store:
        store.initialize_schema()
        snapshot = ReplaySnapshot(
            reducer_id=CounterReducer.reducer_id,
            reducer_version=CounterReducer.reducer_version,
            stream_id=STREAM_ID,
            through_stream_version=0,
            through_event_hash=GENESIS_HASH,
            state={"total": 0, "event_ids": []},
            state_hash=compute_replay_state_hash({"total": 0, "event_ids": []}),
        )

        report = _verifier(store, InvalidInitialReducer()).verify_stream(
            STREAM_ID,
            snapshot,
        )

        assert _failure_code(report) is ReplayFailureCode.INVALID_INITIAL_STATE


def test_invalid_reducer_contract_fails_closed() -> None:
    with SQLiteEventPayloadStore.in_memory() as store:
        store.initialize_schema()
        snapshot = make_replay_snapshot(
            reducer_id=CounterReducer.reducer_id,
            reducer_version=CounterReducer.reducer_version,
            stream_id=STREAM_ID,
            through_stream_version=0,
            through_event_hash=GENESIS_HASH,
            state={"total": 0, "event_ids": []},
        )

        report = _verifier(store, InvalidContractReducer()).verify_stream(
            STREAM_ID,
            snapshot,
        )

        assert _failure_code(report) is ReplayFailureCode.INVALID_REDUCER


def test_r0_failure_prevents_replay() -> None:
    with SQLiteEventPayloadStore.in_memory() as store:
        store.initialize_schema()
        _append_counter(store, "EVT-1", 1, 1)
        connection = store.raw_connection_for_tests()
        connection.execute("DROP TRIGGER events_are_immutable_on_update")
        connection.execute(
            "UPDATE events SET event_hash = 'sha256:tampered' "
            "WHERE event_id = 'EVT-1'"
        )
        snapshot = make_replay_snapshot(
            reducer_id=CounterReducer.reducer_id,
            reducer_version=CounterReducer.reducer_version,
            stream_id=STREAM_ID,
            through_stream_version=0,
            through_event_hash=GENESIS_HASH,
            state={"total": 0, "event_ids": []},
        )

        report = _verifier(store).verify_stream(STREAM_ID, snapshot)

        assert _failure_code(report) is ReplayFailureCode.R0_PREREQUISITE_FAILED


def test_governed_redaction_cannot_be_hidden_by_snapshot() -> None:
    with SQLiteEventPayloadStore.in_memory() as store:
        store.initialize_schema()
        _append_counter(store, "EVT-1", 1, 4)
        SQLiteRedactionExecutor(store, _registry()).redact(
            RedactionRequest(
                idempotency_key="REDACT-R1",
                command_id="CMD-REDACT-R1",
                target_event_id="EVT-1",
                target_stream=STREAM_ID,
                expected_stream_version=1,
                reason="remove state material",
                issuer=ActorRef("operator", "operator:primary"),
                authority=AuthorityRef("CAP-P0-013", 1),
                correlation_id="CORR-REDACT-R1",
                audit_event_id="AUDIT-1",
                producer=ProducerRef("p0-013-test", "0.1.0"),
                occurred_at="2026-08-06T01:00:00Z",
                recorded_at="2026-08-06T01:00:00Z",
            )
        )
        snapshot = make_replay_snapshot(
            reducer_id=CounterReducer.reducer_id,
            reducer_version=CounterReducer.reducer_version,
            stream_id=STREAM_ID,
            through_stream_version=2,
            through_event_hash=store.list_stream(STREAM_ID)[1].event_hash,
            state={"total": 4, "event_ids": ["EVT-1"]},
        )

        report = _verifier(store).verify_stream(STREAM_ID, snapshot)

        assert _failure_code(report) is ReplayFailureCode.PAYLOAD_UNAVAILABLE


def test_r0_resource_budget_failure_prevents_replay() -> None:
    with SQLiteEventPayloadStore.in_memory() as store:
        store.initialize_schema()
        first = _append_counter(store, "EVT-1", 1, 1)
        _append_counter(store, "EVT-2", 2, 1)

        report = _verifier(
            store,
            budget=_budget(max_events=1),
        ).verify_stream(STREAM_ID, _snapshot_after_first(first))

        assert _failure_code(report) is ReplayFailureCode.R0_PREREQUISITE_FAILED


class ExpandingReducer(CounterReducer):
    def apply(self, state, event, payload) -> Mapping[str, object]:
        return {
            "total": state["total"],
            "event_ids": list(state["event_ids"]),
            "padding": "x" * 1_000,
        }


def test_reducer_state_size_budget_is_enforced() -> None:
    with SQLiteEventPayloadStore.in_memory() as store:
        store.initialize_schema()
        _append_counter(store, "EVT-1", 1, 1)
        snapshot = make_replay_snapshot(
            reducer_id=CounterReducer.reducer_id,
            reducer_version=CounterReducer.reducer_version,
            stream_id=STREAM_ID,
            through_stream_version=0,
            through_event_hash=GENESIS_HASH,
            state={"total": 0, "event_ids": []},
        )

        report = _verifier(
            store,
            ExpandingReducer(),
            state_budget=_state_budget(max_state_bytes=200),
        ).verify_stream(STREAM_ID, snapshot)

        assert _failure_code(report) is ReplayFailureCode.RESOURCE_BUDGET_EXCEEDED


def test_snapshot_state_size_budget_is_enforced_before_replay() -> None:
    with SQLiteEventPayloadStore.in_memory() as store:
        store.initialize_schema()
        snapshot = make_replay_snapshot(
            reducer_id=CounterReducer.reducer_id,
            reducer_version=CounterReducer.reducer_version,
            stream_id=STREAM_ID,
            through_stream_version=0,
            through_event_hash=GENESIS_HASH,
            state={"total": 0, "event_ids": [], "padding": "x" * 1_000},
        )

        report = _verifier(
            store,
            state_budget=_state_budget(max_state_bytes=200),
        ).verify_stream(STREAM_ID, snapshot)

        assert _failure_code(report) is ReplayFailureCode.RESOURCE_BUDGET_EXCEEDED



def test_r1_uses_one_sqlite_read_snapshot_for_concurrent_append(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    database = tmp_path / "r1-read-snapshot.sqlite3"
    with SQLiteEventPayloadStore.connect(database) as setup:
        setup.raw_connection_for_tests().execute("PRAGMA journal_mode = WAL")
        setup.initialize_schema()
        first = _append_counter(setup, "EVT-1", 1, 2)

    with (
        SQLiteEventPayloadStore.connect(database) as reader,
        SQLiteEventPayloadStore.connect(database) as writer,
    ):
        reader.raw_connection_for_tests().execute("PRAGMA journal_mode = WAL")
        writer.raw_connection_for_tests().execute("PRAGMA journal_mode = WAL")
        original_list_stream = reader.list_stream
        calls = 0

        def append_between_r0_count_and_event_capture(stream_id: str):
            nonlocal calls
            calls += 1
            if calls == 1:
                _append_counter(writer, "EVT-2", 2, 5)
            return original_list_stream(stream_id)

        monkeypatch.setattr(
            reader,
            "list_stream",
            append_between_r0_count_and_event_capture,
        )
        report = _verifier(reader).verify_stream(
            STREAM_ID,
            _snapshot_after_first(first),
        )

        assert report.ok
        assert report.verified_through_stream_version == 1
        assert report.verified_through_event_hash == first.event_hash
        assert len(original_list_stream(STREAM_ID)) == 2



def test_r1_refuses_uncommitted_connection_state() -> None:
    with SQLiteEventPayloadStore.in_memory() as store:
        store.initialize_schema()
        snapshot = make_replay_snapshot(
            reducer_id=CounterReducer.reducer_id,
            reducer_version=CounterReducer.reducer_version,
            stream_id=STREAM_ID,
            through_stream_version=0,
            through_event_hash=GENESIS_HASH,
            state={"total": 0, "event_ids": []},
        )
        connection = store.raw_connection_for_tests()
        connection.execute("BEGIN IMMEDIATE")
        try:
            report = _verifier(store).verify_stream(STREAM_ID, snapshot)
        finally:
            connection.execute("ROLLBACK")

        assert _failure_code(report) is ReplayFailureCode.ACTIVE_TRANSACTION
