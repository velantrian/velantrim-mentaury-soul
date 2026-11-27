"""Stage 04B.3: operation-level admission wired into batch and ingress paths.

Small explicit test budgets only (not Canon, not production defaults). Admission
is opt-in per call (``admission=`` / ``.admitted(...)``); every legacy call is
unchanged. Bounds limit visited nodes/bytes/entries; no wall-clock or RSS claim.
"""

from __future__ import annotations

import itertools
import sqlite3
from collections.abc import Sequence
from dataclasses import replace

import pytest

import mentaury.contracts.canonical_json as canonical_module
import mentaury.contracts.primitives as primitives_module
import test_atomic_batch as atomic
import test_idempotency as idem
from mentaury.contracts import (
    CommandEnvelope,
    OperationAdmissionBudget,
    OperationAdmissionState,
    PayloadAdmissionBudget,
    PayloadAdmissionExceeded,
    PendingEvent,
    canonical_json_bytes,
    snapshot_pending_batch,
)
from mentaury.storage import (
    BatchEntry,
    IdempotencyStatus,
    SQLiteAtomicBatchAppender,
    SQLiteEventPayloadStore,
    SQLiteIdempotentBatchAppender,
    TransactionOwnershipError,
)
from mentaury.storage.idempotency import IdempotentBatchRequest, idempotency_fingerprint
from mentaury.storage.sealing import seal_event, validate_event_for_commit
from mentaury.validation import SchemaValidationError


def budget(
    entries=4, depth=8, nodes=50, string=64, key=32, payload_bytes=400,
    total_nodes=2_000, total_bytes=8_000,
) -> OperationAdmissionBudget:
    return OperationAdmissionBudget(
        entries, PayloadAdmissionBudget(depth, nodes, string, key),
        payload_bytes, total_nodes, total_bytes,
    )


def state(**kw) -> OperationAdmissionState:
    return OperationAdmissionState(budget(**kw))


def raises_exceeded(fn) -> PayloadAdmissionExceeded:
    with pytest.raises(PayloadAdmissionExceeded) as captured:
        fn()
    return captured.value


# --- budget & state objects ---------------------------------------------------------------

def test_budget_is_immutable_validated_and_has_no_defaults() -> None:
    b = budget()
    with pytest.raises(AttributeError):
        b.max_total_nodes = 1  # type: ignore[misc]
    for bad in (0, -1, True, 1.5):
        with pytest.raises(ValueError):
            budget(entries=bad)
        with pytest.raises(ValueError):
            budget(total_nodes=bad)
        with pytest.raises(ValueError):
            budget(total_bytes=bad)
        with pytest.raises(ValueError):
            budget(payload_bytes=bad)
    with pytest.raises(TypeError):
        OperationAdmissionBudget(4, object(), 1, 1, 1)  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        OperationAdmissionState(object())  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        OperationAdmissionBudget()  # type: ignore[call-arg]  # nothing is defaulted


# --- batch entry count: exact boundary, lying len, endless iterables ------------------------------

def test_entry_count_boundary_is_inclusive_and_one_more_fails() -> None:
    assert len(state(entries=3).take_entries([1, 2, 3])) == 3
    err = raises_exceeded(lambda: state(entries=3).take_entries([1, 2, 3, 4]))
    assert (err.dimension, err.limit, err.observed) == ("batch_entries", 3, 4)


def test_endless_iterable_is_stopped_after_limit_plus_one_items() -> None:
    pulled = 0

    def endless():
        nonlocal pulled
        for i in itertools.count():
            pulled += 1
            if pulled > 10_000:
                raise RuntimeError("runaway")
            yield i

    err = raises_exceeded(lambda: state(entries=5).take_entries(endless()))
    assert err.dimension == "batch_entries" and pulled == 6


def test_subclass_with_lying_len_cannot_bypass_the_entry_limit() -> None:
    class Liar(list):
        def __len__(self):
            return 1

        def __iter__(self):
            return iter(range(100))

    err = raises_exceeded(lambda: state(entries=5).take_entries(Liar([0])))
    assert err.dimension == "batch_entries"


def test_snapshot_pending_batch_uses_the_operation_budget_only_when_asked() -> None:
    pending = idem.pending_batch()
    assert snapshot_pending_batch(pending) == pending  # legacy untouched
    assert snapshot_pending_batch(pending, state(entries=2)) == pending
    assert raises_exceeded(lambda: snapshot_pending_batch(pending, state(entries=1))).dimension == "batch_entries"


# --- envelope factories ---------------------------------------------------------------------------

COMMAND_FIELDS = dict(
    command_id="CMD-1", command_type="CREATE_BELIEF", command_schema="create-belief/v1",
    target_stream="belief:B-204", expected_stream_version=0, issued_at="2026-08-05T00:00:00Z",
    issuer=idem.command().issuer, authority=idem.command().authority,
    correlation_id="CORR-1", idempotency_key="IDEMP-1",
)


def test_admitted_command_equals_the_normally_constructed_envelope() -> None:
    payload = {"statement": "alpha", "n": [1, {"k": None}]}
    normal = CommandEnvelope(**COMMAND_FIELDS, payload=payload)
    admitted = CommandEnvelope.admitted(state(), **COMMAND_FIELDS, payload=payload)
    assert admitted == normal
    assert canonical_json_bytes(admitted.payload) == canonical_json_bytes(normal.payload)
    assert type(admitted.payload) is type(normal.payload)


def test_admitted_pending_event_and_batch_entry_equal_normal_construction() -> None:
    payload = {"a": [1, 2], "b": {"c": "x"}}
    fields = dict(event_type="BELIEF_CREATED", payload_schema="belief-created/v1", affects_domain_state=True)
    assert PendingEvent.admitted(state(), **fields, payload=payload) == PendingEvent(**fields, payload=payload)
    event = atomic.event(0, batch_size=1)
    assert BatchEntry.admitted(state(), event, payload) == BatchEntry(event, payload)


def test_factories_keep_normal_field_validation() -> None:
    with pytest.raises(ValueError, match="command_id"):
        CommandEnvelope.admitted(state(), **{**COMMAND_FIELDS, "command_id": ""}, payload={})
    with pytest.raises(TypeError, match="payload is required"):
        CommandEnvelope.admitted(state(), **COMMAND_FIELDS)
    with pytest.raises(TypeError, match="mapping"):
        PendingEvent.admitted(state(), event_type="E", payload_schema="s/v1", affects_domain_state=True, payload=[1])
    with pytest.raises(TypeError):
        BatchEntry.admitted(state(), object(), {})  # type: ignore[arg-type]


def test_each_payload_limit_has_an_exact_inclusive_boundary() -> None:
    mk = lambda s, payload: PendingEvent.admitted(  # noqa: E731
        s, event_type="E", payload_schema="s/v1", affects_domain_state=True, payload=payload
    )
    # nodes: root + key + value = 3
    mk(state(nodes=3), {"k": 1})
    assert raises_exceeded(lambda: mk(state(nodes=2), {"k": 1})).dimension == "nodes"
    # depth: {"k": {"j": 1}} has depth 2
    mk(state(depth=2), {"k": {"j": 1}})
    assert raises_exceeded(lambda: mk(state(depth=1), {"k": {"j": 1}})).dimension == "depth"
    mk(state(string=5), {"k": "v" * 5})
    assert raises_exceeded(lambda: mk(state(string=5), {"k": "v" * 6})).dimension == "string_length"
    mk(state(key=5), {"k" * 5: 1})
    assert raises_exceeded(lambda: mk(state(key=5), {"k" * 6: 1})).dimension == "key_length"


def test_oversized_payload_is_stopped_before_it_is_fully_copied() -> None:
    class Endless(Sequence):
        calls = 0

        def __len__(self):
            return 1

        def __getitem__(self, i):  # pragma: no cover
            raise IndexError

        def __iter__(self):
            return self

        def __next__(self):
            type(self).calls += 1
            if type(self).calls > 50_000:
                raise RuntimeError("runaway")
            return 1

    err = raises_exceeded(lambda: CommandEnvelope.admitted(
        state(nodes=20), **COMMAND_FIELDS, payload={"items": Endless()}))
    assert err.dimension == "nodes" and Endless.calls <= 21


def test_admitted_snapshot_is_detached_from_the_source_object() -> None:
    source = {"a": [1, 2]}
    pending = PendingEvent.admitted(state(), event_type="E", payload_schema="s/v1", affects_domain_state=True, payload=source)
    source["a"].append(3)
    assert canonical_json_bytes(pending.payload) == b'{"a":[1,2]}'


def test_errors_never_contain_payload_content() -> None:
    secret = "TOP-SECRET-PAYLOAD"
    err = raises_exceeded(lambda: PendingEvent.admitted(
        state(string=10), event_type="E", payload_schema="s/v1", affects_domain_state=True,
        payload={"k": secret}))
    assert secret not in str(err) + repr(err)
    assert not isinstance(err, ValueError)


# --- aggregate budget -----------------------------------------------------------------------------------

def test_work_based_accounting_is_exact_for_freeze_canonical_and_validation() -> None:
    payload = {"a": [1, 2]}  # root + key + list + 2 scalars = 5 nodes, 11 bytes
    event = atomic.event(0, batch_size=1)
    reg = atomic.registry()
    s = state(total_nodes=15, total_bytes=11)
    frozen = s.freeze_payload(payload)
    assert s.nodes == 5
    out = validate_event_for_commit(event, frozen, reg, s)
    assert out == b'{"a":[1,2]}'
    assert (s.nodes, s.output_bytes) == (15, 11)  # freeze + canonical + validation walk
    # one node / one byte less is refused with the *aggregate* dimension
    s2 = state(total_nodes=14, total_bytes=11)
    f2 = s2.freeze_payload(payload)
    assert raises_exceeded(lambda: validate_event_for_commit(event, f2, reg, s2)).dimension == "total_nodes"
    s3 = state(total_nodes=15, total_bytes=10)
    f3 = s3.freeze_payload(payload)
    err = raises_exceeded(lambda: validate_event_for_commit(event, f3, reg, s3))
    assert err.dimension == "total_output_bytes"


def test_aggregate_exceedance_is_reported_with_the_aggregate_dimension() -> None:
    s = state(nodes=10, total_nodes=7)
    s.freeze_payload({"k": 1})  # 3
    s.freeze_payload({"k": 2})  # 6
    err = raises_exceeded(lambda: s.freeze_payload({"k": 3}))  # needs 3, only 1 left
    assert (err.dimension, err.limit) == ("total_nodes", 7)


def test_the_same_state_carries_the_spend_across_functions_a_new_one_resets() -> None:
    pending = idem.pending_batch()
    s = state()
    snapshot_pending_batch(pending, s)
    PendingEvent.admitted(s, event_type="E", payload_schema="s/v1", affects_domain_state=True, payload={"a": 1})
    spent = s.nodes
    assert spent > 0
    s.freeze_payload({"b": 2})
    assert s.nodes > spent  # monotonic across components: no reset
    assert state().nodes == 0  # a fresh operation state starts empty (explicit choice)


def test_whole_operation_depth_allowance_covers_only_the_fingerprint_wrapper() -> None:
    cmd, pending = idem.command(), idem.pending_batch()
    idempotency_fingerprint(cmd, pending, state(depth=1))  # payloads are depth-1 dicts


# --- fingerprint & sealing compatibility -----------------------------------------------------------------

def test_fingerprint_is_identical_bounded_and_unbounded() -> None:
    cmd, pending = idem.command(), idem.pending_batch()
    assert idempotency_fingerprint(cmd, pending, state()) == idempotency_fingerprint(cmd, pending)
    assert idempotency_fingerprint(cmd, list(pending), state()) == idempotency_fingerprint(cmd, pending)


def test_fingerprint_respects_entry_and_aggregate_limits() -> None:
    cmd, pending = idem.command(), idem.pending_batch()
    assert raises_exceeded(lambda: idempotency_fingerprint(cmd, pending, state(entries=1))).dimension == "batch_entries"
    err = raises_exceeded(lambda: idempotency_fingerprint(cmd, pending, state(total_bytes=20)))
    assert err.dimension == "total_output_bytes"
    err = raises_exceeded(lambda: idempotency_fingerprint(cmd, pending, state(total_nodes=5)))
    assert err.dimension == "total_nodes"


def test_seal_event_bounded_equals_legacy_and_is_charged() -> None:
    event = atomic.event(0, batch_size=1)
    payload = {"a": [1, 2]}
    s = state()
    assert seal_event(event, payload, admission=s) == seal_event(event, payload)
    assert s.output_bytes == len(b'{"a":[1,2]}') and s.nodes == 5
    assert raises_exceeded(lambda: seal_event(event, payload, admission=state(payload_bytes=10))).dimension == "output_bytes"


def test_resource_admission_runs_before_schema_validation(monkeypatch) -> None:
    event, reg = atomic.event(0, batch_size=1), atomic.registry()
    calls = []
    monkeypatch.setattr(reg, "require_event_payload", lambda *a, **k: calls.append(1))
    raises_exceeded(lambda: validate_event_for_commit(event, {"k": "v" * 100}, reg, state(string=5)))
    assert calls == []  # the validator never saw the oversized payload
    validate_event_for_commit(event, {"k": "v"}, reg, state(string=5))
    assert calls == [1]


def test_schema_semantics_are_unchanged_for_admitted_payloads() -> None:
    from mentaury.validation import EventSchemaDefinition, IntegerSpec, ObjectSpec, SchemaRegistry

    reg = SchemaRegistry([EventSchemaDefinition(
        event_type="BELIEF_EVENT", payload_schema="belief-event/v1", affects_domain_state=True,
        payload=ObjectSpec({"n": IntegerSpec(minimum=0)}, required=frozenset({"n"})))])
    event = atomic.event(0, batch_size=1)
    assert validate_event_for_commit(event, {"n": 3}, reg, state()) == b'{"n":3}'
    with pytest.raises(SchemaValidationError):
        validate_event_for_commit(event, {"n": -1}, reg, state())
    with pytest.raises(SchemaValidationError):
        validate_event_for_commit(event, {"n": -1}, reg)  # same outcome without admission


# --- atomic batch appender --------------------------------------------------------------------------------------

def _rows(store) -> dict:
    c = store.raw_connection_for_tests()
    return {t: [tuple(r) for r in c.execute(f"SELECT * FROM {t} ORDER BY 1").fetchall()]
            for t in ("events", "event_payloads", "stream_meta", "idempotency_records")}


def test_admitted_append_is_byte_identical_to_the_legacy_append() -> None:
    with SQLiteEventPayloadStore.in_memory() as legacy, SQLiteEventPayloadStore.in_memory() as bounded:
        for s in (legacy, bounded):
            s.initialize_schema()
        entries = atomic.entries(3)
        r1 = SQLiteAtomicBatchAppender(legacy, atomic.registry()).append(entries)
        op = state()
        r2 = SQLiteAtomicBatchAppender(bounded, atomic.registry()).append(iter(entries), admission=op)
        assert r1 == r2
        assert _rows(legacy) == _rows(bounded)  # digests, hashes, payload bytes, stream meta
        assert op.nodes > 0 and op.output_bytes > 0


def test_oversized_batch_is_refused_with_no_partial_writes() -> None:
    with SQLiteEventPayloadStore.in_memory() as store:
        store.initialize_schema()
        before = _rows(store)
        err = raises_exceeded(lambda: SQLiteAtomicBatchAppender(store, atomic.registry()).append(
            atomic.entries(3), admission=state(entries=2)))
        assert err.dimension == "batch_entries"
        assert _rows(store) == before
        assert not store.raw_connection_for_tests().in_transaction


def test_endless_entry_iterable_is_not_materialized_by_the_appender() -> None:
    pulled = 0

    def endless():
        nonlocal pulled
        proto = atomic.entries(1)[0]
        for _ in range(100_000):
            pulled += 1
            yield proto

    with SQLiteEventPayloadStore.in_memory() as store:
        store.initialize_schema()
        err = raises_exceeded(lambda: SQLiteAtomicBatchAppender(store, atomic.registry()).append(
            endless(), admission=state(entries=4)))
        assert err.dimension == "batch_entries" and pulled == 5
        assert _rows(store)["events"] == []


def test_one_bad_payload_in_a_batch_leaves_nothing_behind() -> None:
    entries = list(atomic.entries(3))
    entries[2] = replace(entries[2], payload={"k": "v" * 100})
    with SQLiteEventPayloadStore.in_memory() as store:
        store.initialize_schema()
        err = raises_exceeded(lambda: SQLiteAtomicBatchAppender(store, atomic.registry()).append(
            entries, admission=state(string=10)))
        assert err.dimension == "string_length"
        assert _rows(store) == {"events": [], "event_payloads": [], "stream_meta": [], "idempotency_records": []}


def test_aggregate_budget_stops_a_batch_of_individually_valid_payloads() -> None:
    with SQLiteEventPayloadStore.in_memory() as store:
        store.initialize_schema()
        # each payload alone is well inside every per-payload limit
        err = raises_exceeded(lambda: SQLiteAtomicBatchAppender(store, atomic.registry()).append(
            atomic.entries(3), admission=state(total_nodes=12)))
        assert err.dimension == "total_nodes"
        assert _rows(store)["events"] == []


def test_foreign_transaction_is_preserved_for_both_refusal_kinds() -> None:
    with SQLiteEventPayloadStore.in_memory() as store:
        store.initialize_schema()
        c = store.raw_connection_for_tests()
        c.execute("CREATE TABLE sentinel(x)")
        c.execute("BEGIN")
        c.execute("INSERT INTO sentinel VALUES (1)")
        appender = SQLiteAtomicBatchAppender(store, atomic.registry())
        raises_exceeded(lambda: appender.append(atomic.entries(3), admission=state(entries=1)))
        assert c.in_transaction and c.execute("SELECT COUNT(*) FROM sentinel").fetchone()[0] == 1
        with pytest.raises(TransactionOwnershipError):
            appender.append(atomic.entries(2), admission=state())
        assert c.in_transaction and c.execute("SELECT COUNT(*) FROM sentinel").fetchone()[0] == 1
        c.execute("ROLLBACK")


# --- idempotent appender -----------------------------------------------------------------------------------------

def test_admitted_request_and_append_match_legacy_results_and_replay() -> None:
    cmd, pending = idem.command(), idem.pending_batch()
    entries = idem.entries_for(cmd, pending)
    with SQLiteEventPayloadStore.in_memory() as legacy, SQLiteEventPayloadStore.in_memory() as bounded:
        for s in (legacy, bounded):
            s.initialize_schema()
        legacy_result = SQLiteIdempotentBatchAppender(legacy, idem.registry()).append(
            IdempotentBatchRequest(cmd, pending, entries))
        op = state()
        request = IdempotentBatchRequest.admitted(op, cmd, iter(pending), iter(entries))
        bounded_result = SQLiteIdempotentBatchAppender(bounded, idem.registry()).append(request, admission=op)
        assert bounded_result == legacy_result and bounded_result.status is IdempotencyStatus.APPLIED
        assert _rows(legacy) == _rows(bounded)
        # a successful retry (fresh operation state) still replays the original receipt
        retry_op = state()
        retry = IdempotentBatchRequest.admitted(retry_op, cmd, pending, idem.entries_for(cmd, pending, generation="B"))
        again = SQLiteIdempotentBatchAppender(bounded, idem.registry()).append(retry, admission=retry_op)
        assert again.status is IdempotencyStatus.ALREADY_APPLIED
        assert again.receipt == bounded_result.receipt and again.fingerprint == bounded_result.fingerprint
        assert _rows(legacy) == _rows(bounded)


def test_request_admission_bounds_both_collections_and_alignment_work() -> None:
    cmd, pending = idem.command(), idem.pending_batch()
    entries = idem.entries_for(cmd, pending)
    assert raises_exceeded(lambda: IdempotentBatchRequest.admitted(state(entries=1), cmd, pending, entries)).dimension == "batch_entries"
    assert raises_exceeded(lambda: IdempotentBatchRequest.admitted(state(total_nodes=6), cmd, pending, entries)).dimension == "total_nodes"
    with pytest.raises(TypeError):
        IdempotentBatchRequest.admitted(state(), cmd, pending, [object(), object()])  # type: ignore[list-item]


def test_refused_idempotent_apply_writes_no_record_and_a_proper_retry_succeeds() -> None:
    cmd, pending = idem.command(), idem.pending_batch()
    entries = idem.entries_for(cmd, pending)
    with SQLiteEventPayloadStore.in_memory() as store:
        store.initialize_schema()
        before = _rows(store)
        tight = state(total_nodes=20)
        request = IdempotentBatchRequest.admitted(state(), cmd, pending, entries)
        err = raises_exceeded(lambda: SQLiteIdempotentBatchAppender(store, idem.registry()).append(request, admission=tight))
        assert err.dimension in {"total_nodes", "total_output_bytes"}
        assert _rows(store) == before and not store.raw_connection_for_tests().in_transaction
        ok = SQLiteIdempotentBatchAppender(store, idem.registry()).append(request, admission=state())
        assert ok.status is IdempotencyStatus.APPLIED  # no false receipt was left behind


def test_replay_verification_is_budgeted_and_rolls_back_cleanly() -> None:
    cmd, pending = idem.command(), idem.pending_batch()
    request = IdempotentBatchRequest(cmd, pending, idem.entries_for(cmd, pending))
    with SQLiteEventPayloadStore.in_memory() as store:
        store.initialize_schema()
        appender = SQLiteIdempotentBatchAppender(store, idem.registry())
        first = appender.append(request)
        before = _rows(store)
        # fingerprint fits, replay verification (payload digests) does not
        fingerprint_cost = state()
        idempotency_fingerprint(cmd, pending, fingerprint_cost)
        tight = state(total_nodes=fingerprint_cost.nodes + 1, total_bytes=10_000)
        err = raises_exceeded(lambda: appender.append(request, admission=tight))
        assert err.dimension == "total_nodes"
        assert _rows(store) == before and not store.raw_connection_for_tests().in_transaction
        assert appender.append(request, admission=state()).receipt == first.receipt


def test_idempotent_append_keeps_foreign_transactions_untouched() -> None:
    cmd, pending = idem.command(), idem.pending_batch()
    request = IdempotentBatchRequest.admitted(state(), cmd, pending, idem.entries_for(cmd, pending))
    with SQLiteEventPayloadStore.in_memory() as store:
        store.initialize_schema()
        c = store.raw_connection_for_tests()
        c.execute("CREATE TABLE sentinel(x)")
        c.execute("BEGIN")
        c.execute("INSERT INTO sentinel VALUES (1)")
        with pytest.raises(TransactionOwnershipError):
            SQLiteIdempotentBatchAppender(store, idem.registry()).append(request, admission=state())
        assert c.in_transaction and c.execute("SELECT COUNT(*) FROM sentinel").fetchone()[0] == 1
        c.execute("ROLLBACK")


# --- no bypass inside an explicitly bounded operation ------------------------------------------------------------------

MARK = "UNIQUE-PAYLOAD-MARKER-7f3a"


def _spy_unbounded_walks(monkeypatch) -> list[str]:
    seen: list[str] = []
    real_prepare, real_freeze = canonical_module._prepare, primitives_module._freeze_payload_value

    def prepare(value, path, active):
        if path == "$" and MARK in repr(value):
            seen.append("canonical._prepare")
        return real_prepare(value, path, active)

    def freeze(value, active):
        if MARK in repr(value):
            seen.append("primitives._freeze_payload_value")
        return real_freeze(value, active)

    monkeypatch.setattr(canonical_module, "_prepare", prepare)
    monkeypatch.setattr(primitives_module, "_freeze_payload_value", freeze)
    return seen


def _events_for(cmd, pending):
    """Committed-event envelopes only (no payloads), so nothing legacy touches them."""

    from mentaury.contracts import EventEnvelope, ProducerRef

    return tuple(
        EventEnvelope(
            event_id=f"EVT-A-{i}", event_type=p.event_type, envelope_schema_version=1,
            payload_schema=p.payload_schema, stream_id=cmd.target_stream,
            stream_version=cmd.expected_stream_version + i + 1, batch_id="BATCH-A",
            batch_index=i, batch_size=len(pending), occurred_at="2026-08-05T00:00:00Z",
            recorded_at="2026-08-05T00:00:00Z", producer=ProducerRef("t", "0.1.0"),
            initiator=cmd.issuer, authority=cmd.authority, causation_id=cmd.command_id,
            correlation_id=cmd.correlation_id, affects_domain_state=p.affects_domain_state,
            payload_digest="sha256:x", payload_ref=f"PAYLOAD-A-{i}",
            previous_hash="sha256:x", event_hash="sha256:x",
        )
        for i, p in enumerate(pending)
    )


def _full_flow(op, store_registry, *, marker: str):
    cmd = CommandEnvelope.admitted(
        op, **{**COMMAND_FIELDS, "target_stream": "belief:B-204"}, payload={"statement": marker})
    pending = tuple(
        PendingEvent.admitted(op, event_type=t, payload_schema=sch, affects_domain_state=True,
                              payload={"value": marker})
        for t, sch in (("BELIEF_CREATED", "belief-created/v1"), ("EVIDENCE_ATTACHED", "evidence-attached/v1")))
    entries = tuple(
        BatchEntry.admitted(op, event, proposed.payload)
        for event, proposed in zip(_events_for(cmd, pending), pending, strict=True)
    )
    request = IdempotentBatchRequest.admitted(op, cmd, pending, entries)
    with SQLiteEventPayloadStore.in_memory() as store:
        store.initialize_schema()
        return SQLiteIdempotentBatchAppender(store, store_registry).append(request, admission=op)


def test_no_unbounded_payload_traversal_inside_a_fully_admitted_operation(monkeypatch) -> None:
    seen = _spy_unbounded_walks(monkeypatch)
    result = _full_flow(state(), idem.registry(), marker=MARK)
    assert result.status is IdempotencyStatus.APPLIED
    assert seen == []  # no legacy walk ever saw the payload
    # control: the legacy path does hit the spies, so the instrumentation is live
    cmd = idem.command(payload_value=MARK)
    idempotency_fingerprint(cmd, idem.pending_batch(first_payload=MARK))
    CommandEnvelope(**COMMAND_FIELDS, payload={"x": MARK})
    assert "canonical._prepare" in seen and "primitives._freeze_payload_value" in seen


def test_legacy_calls_remain_unbounded_and_unchanged() -> None:
    big = {"items": list(range(5_000))}
    assert len(CommandEnvelope(**COMMAND_FIELDS, payload=big).payload["items"]) == 5_000
    with SQLiteEventPayloadStore.in_memory() as store:
        store.initialize_schema()
        SQLiteAtomicBatchAppender(store, atomic.registry()).append(atomic.entries(3))
        assert len(_rows(store)["events"]) == 3
