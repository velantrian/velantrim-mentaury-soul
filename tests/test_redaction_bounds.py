"""Stage 04C: bounded redaction-evidence loading (AUD-04-F3).

The bound is on *Python-side materialization* of ``redactions`` metadata: row
count, per-record bytes and total bytes are measured by SQLite aggregates before
any row value is fetched. It makes no claim about SQLite's own resource use.
Budgets below are small explicit test profiles, not Canon or production values.
"""

from __future__ import annotations

import sqlite3
from pathlib import Path

import pytest

import test_r1_replay as r1
import test_redaction as red
from mentaury.storage import (
    IntegrityCode,
    R0IntegrityVerifier,
    ResourceBudgetExceeded,
    SQLiteEventPayloadStore,
    VerificationBudget,
    redacted_targets_for_stream,
)

STREAM = "test:stream"
SECRET = "SECRET-REASON-MUST-NEVER-LEAK"
FETCH_PREFIX = "SELECT target_event_id, target_stream_id"  # the full evidence fetch
HELPER_FETCH_PREFIX = "SELECT target_event_id, target_payload_ref"


def budget(**kw) -> VerificationBudget:
    values = dict(max_events=10, max_payload_bytes=1_000, max_total_payload_bytes=5_000)
    values.update(kw)
    return VerificationBudget(**values)


def r0(store, **kw) -> R0IntegrityVerifier:
    return R0IntegrityVerifier(store, red.registry(), budget(**kw))


def forge(store, count: int, *, reason: str = "r", start: int = 0, stream: str = STREAM,
          target: str | None = None, payload_ref: str | None = None, audit: str | None = None) -> None:
    connection = store.raw_connection_for_tests()
    for index in range(start, start + count):
        connection.execute(
            """
            INSERT INTO redactions(
                target_event_id, idempotency_key, fingerprint, target_stream_id,
                target_payload_ref, audit_event_id, reason, capability_lease_id,
                capability_revision, redacted_at
            ) VALUES (?, ?, 'sha256:f', ?, ?, ?, ?, 'CAP-1', 1, '2026-08-05T01:00:00Z')
            """,
            (target or f"FORGED-{index}", f"KEY-{index}", stream, payload_ref or f"PAYLOAD-F-{index}",
             audit or f"AUDIT-F-{index}", reason),
        )


def two_redactions(store) -> None:
    red.append_target(store, event_id="EVT-1", version=1)
    red.executor(store).redact(red.redaction_request())
    red.append_target(store, event_id="EVT-3", version=3, n=3)
    red.executor(store).redact(red.redaction_request(
        idempotency_key="REDACT-2", command_id="CMD-2", target_event_id="EVT-3",
        expected_stream_version=3, audit_event_id="AUDIT-2", correlation_id="CORR-2"))


def traced(store) -> list[str]:
    statements: list[str] = []
    store.raw_connection_for_tests().set_trace_callback(statements.append)
    return statements


def untrace(store) -> None:
    store.raw_connection_for_tests().set_trace_callback(None)


def refused(report) -> ResourceBudgetExceeded | None:
    assert not report.ok and report.failure is not None
    assert report.failure.code is IntegrityCode.RESOURCE_BUDGET_EXCEEDED
    return None


def fresh() -> SQLiteEventPayloadStore:
    store = SQLiteEventPayloadStore.in_memory()
    store.initialize_schema()
    red.append_target(store)
    return store


# --- budget object ---------------------------------------------------------------------------------------------------

def test_new_budget_parameters_are_optional_validated_and_derive_from_existing_limits() -> None:
    plain = VerificationBudget(10, 1_000, 5_000)  # existing three-argument calls still work
    assert (plain.effective_redaction_rows, plain.effective_redaction_record_bytes,
            plain.effective_total_redaction_bytes) == (10, 1_000, 5_000)
    tuned = VerificationBudget(10, 1_000, 5_000, max_redaction_rows=2,
                               max_redaction_record_bytes=300, max_total_redaction_bytes=400)
    assert (tuned.effective_redaction_rows, tuned.effective_redaction_record_bytes,
            tuned.effective_total_redaction_bytes) == (2, 300, 400)
    for bad in (0, -1, True, 1.5):
        for name in ("max_redaction_rows", "max_redaction_record_bytes", "max_total_redaction_bytes"):
            with pytest.raises(ValueError):
                VerificationBudget(10, 1_000, 5_000, **{name: bad})
    with pytest.raises(ValueError):
        VerificationBudget(10, 1_000, 5_000, max_redaction_record_bytes=500, max_total_redaction_bytes=400)


# --- R0: row count --------------------------------------------------------------------------------------------------

def test_excess_redaction_rows_are_refused_before_any_row_is_fetched() -> None:
    with fresh() as store:
        forge(store, 50)  # one event, fifty forged rows, limit 10
        statements = traced(store)
        report = r0(store).verify_stream(STREAM)
        untrace(store)
        refused(report)
        assert "redaction_rows" in report.failure.message and "limit 10" in report.failure.message
        assert not any(s.strip().startswith(FETCH_PREFIX) for s in statements)  # values never fetched
        assert not store.raw_connection_for_tests().in_transaction  # own snapshot released


def test_row_limit_boundary_is_exact_for_legitimate_redactions() -> None:
    with SQLiteEventPayloadStore.in_memory() as store:
        store.initialize_schema()
        two_redactions(store)
        statements = traced(store)
        assert r0(store, max_events=100, max_redaction_rows=2).verify_stream(STREAM).ok
        untrace(store)
        # positive control: an admitted verification does run the bounded fetch (so the
        # "never fetched" assertions elsewhere are not vacuous) after the SQL preflight
        order = [s.strip().split("\n")[0][:60] for s in statements]
        assert any(s.strip().startswith(FETCH_PREFIX) for s in statements)
        assert any("LENGTH(CAST" in s for s in statements)
        report = r0(store, max_events=100, max_redaction_rows=1).verify_stream(STREAM)
        refused(report)
        assert "redaction_rows limit 1, observed 2" in report.failure.message


def test_legitimate_governed_redaction_passes_with_only_the_existing_three_limits() -> None:
    with SQLiteEventPayloadStore.in_memory() as store:
        store.initialize_schema()
        two_redactions(store)
        report = R0IntegrityVerifier(store, red.registry(), VerificationBudget(4, 10_000, 100_000)).verify_stream(STREAM)
        assert report.ok and report.checked_events == 4


# --- R0: record and total bytes -----------------------------------------------------------------------------------

def test_one_record_with_a_huge_reason_is_refused_without_fetching_it() -> None:
    with fresh() as store:
        forge(store, 1, reason=SECRET * 400)  # ~11 kB reason, payload limit 1 kB
        statements = traced(store)
        report = r0(store).verify_stream(STREAM)
        untrace(store)
        refused(report)
        assert "redaction_record_bytes" in report.failure.message
        assert not any(s.strip().startswith(FETCH_PREFIX) for s in statements)
        assert SECRET not in repr(report) and SECRET not in report.failure.message


def test_aggregate_metadata_size_over_the_budget_is_refused() -> None:
    with fresh() as store:
        forge(store, 30, reason="x" * 100)  # each ~150 B (< 1000), total ~4.5 kB > 3000
        report = r0(store, max_events=100, max_total_payload_bytes=3_000).verify_stream(STREAM)
        refused(report)
        assert "redaction_total_bytes" in report.failure.message


def test_record_and_total_byte_boundaries_are_exact() -> None:
    cols = ("target_event_id", "target_stream_id", "target_payload_ref", "reason", "capability_lease_id")
    expr = " + ".join(f"LENGTH(CAST({c} AS BLOB))" for c in cols)
    with SQLiteEventPayloadStore.in_memory() as store:
        store.initialize_schema()
        two_redactions(store)
        sizes = [r[0] for r in store.raw_connection_for_tests().execute(
            f"SELECT {expr} FROM redactions ORDER BY 1").fetchall()]
        biggest, total = max(sizes), sum(sizes)
        ok = dict(max_events=100, max_payload_bytes=10_000, max_total_payload_bytes=100_000)
        assert R0IntegrityVerifier(store, red.registry(), VerificationBudget(
            **ok, max_redaction_record_bytes=biggest, max_total_redaction_bytes=total)).verify_stream(STREAM).ok
        rec = R0IntegrityVerifier(store, red.registry(), VerificationBudget(
            **ok, max_redaction_record_bytes=biggest - 1, max_total_redaction_bytes=total)).verify_stream(STREAM)
        refused(rec)
        assert f"redaction_record_bytes limit {biggest - 1}, observed {biggest}" in rec.failure.message
        tot = R0IntegrityVerifier(store, red.registry(), VerificationBudget(
            **ok, max_redaction_record_bytes=biggest, max_total_redaction_bytes=total - 1)).verify_stream(STREAM)
        refused(tot)
        assert f"redaction_total_bytes limit {total - 1}, observed {total}" in tot.failure.message


def test_refusal_is_resource_exceeded_not_corruption_and_never_a_false_success() -> None:
    with fresh() as store:
        forge(store, 50)
        report = r0(store).verify_stream(STREAM)
        assert report.ok is False
        assert report.failure.code is IntegrityCode.RESOURCE_BUDGET_EXCEEDED
        assert report.failure.code not in {
            IntegrityCode.REDACTION_TARGET_EVENT_MISSING, IntegrityCode.REDACTION_AUDIT_EVENT_MISSING,
            IntegrityCode.PAYLOAD_MISSING, IntegrityCode.REDACTED_PAYLOAD_STILL_PRESENT}
        assert store.load_payload("PAYLOAD-EVT-1") is not None  # nothing was removed or altered


# --- linkage checks are untouched ---------------------------------------------------------------------------------

def test_dangling_audit_link_is_still_reported_with_its_specific_code_inside_budget() -> None:
    with fresh() as store:
        store.raw_connection_for_tests().execute("DELETE FROM event_payloads WHERE payload_ref = 'PAYLOAD-EVT-1'")
        forge(store, 1, target="EVT-1", payload_ref="PAYLOAD-EVT-1", audit="AUDIT-GHOST")
        report = r0(store).verify_stream(STREAM)
        assert not report.ok and report.failure.code is IntegrityCode.REDACTION_AUDIT_EVENT_MISSING


def test_orphan_rows_inside_budget_keep_their_existing_diagnostic() -> None:
    with fresh() as store:
        forge(store, 2)  # targets do not exist in the stream
        report = r0(store).verify_stream(STREAM)
        assert not report.ok and report.failure.code is IntegrityCode.REDACTION_TARGET_EVENT_MISSING


# --- R1 and foreign transactions ----------------------------------------------------------------------------------

def test_r1_does_not_continue_when_r0_refuses_on_redaction_bounds() -> None:
    applied = []

    class Spy(r1.CounterReducer):
        def apply(self, state, event, payload):
            applied.append(event.event_id)
            return super().apply(state, event, payload)

    with SQLiteEventPayloadStore.in_memory() as store:
        store.initialize_schema()
        first = r1._append_counter(store, "EVT-1", 1, 2)
        forge(store, 50, stream=r1.STREAM_ID)
        report = r1._verifier(store, Spy(), budget=r1._budget(max_events=10)).verify_stream(
            r1.STREAM_ID, r1._snapshot_after_first(first))
        assert not report.ok
        assert "RESOURCE_BUDGET_EXCEEDED" in report.failure.message
        assert applied == []  # replay never started
        assert not store.raw_connection_for_tests().in_transaction


def test_external_transaction_is_refused_and_left_untouched() -> None:
    with fresh() as store:
        forge(store, 50)
        c = store.raw_connection_for_tests()
        c.execute("CREATE TABLE sentinel(x)")
        c.execute("BEGIN")
        c.execute("INSERT INTO sentinel VALUES (1)")
        report = r0(store).verify_stream(STREAM)
        assert report.failure.code is IntegrityCode.ACTIVE_TRANSACTION
        assert c.in_transaction and c.execute("SELECT COUNT(*) FROM sentinel").fetchone()[0] == 1
        c.execute("ROLLBACK")


# --- concurrency -----------------------------------------------------------------------------------------------------

def test_preflight_and_fetch_share_one_snapshot_under_a_concurrent_writer(tmp_path: Path) -> None:
    database = tmp_path / "bounds.sqlite3"
    with SQLiteEventPayloadStore.connect(database) as setup:
        setup.initialize_schema()
        two_redactions(setup)
    reader = SQLiteEventPayloadStore.connect(database)
    writer = SQLiteEventPayloadStore.connect(database)
    with reader, writer:
        fired = []

        def trace(statement: str) -> None:
            if statement.strip().startswith(FETCH_PREFIX) and not fired:
                fired.append(1)  # another connection commits 50 rows between preflight and fetch
                forge(writer, 50, start=100)

        reader.raw_connection_for_tests().set_trace_callback(trace)
        report = R0IntegrityVerifier(reader, red.registry(), budget(max_events=100)).verify_stream(STREAM)
        reader.raw_connection_for_tests().set_trace_callback(None)
        assert fired and report.ok, report.failure  # the snapshot predates the writer: no mixed view
        later = R0IntegrityVerifier(reader, red.registry(), budget(max_events=10)).verify_stream(STREAM)
        refused(later)  # after the snapshot ends the new rows are visible and bounded
        assert "redaction_rows" in later.failure.message


# --- exported helper ----------------------------------------------------------------------------------------------------

def test_helper_without_a_budget_is_unchanged_and_with_one_is_bounded() -> None:
    with SQLiteEventPayloadStore.in_memory() as store:
        store.initialize_schema()
        two_redactions(store)
        c = store.raw_connection_for_tests()
        legacy = redacted_targets_for_stream(c, STREAM)
        assert legacy == {"EVT-1": "PAYLOAD-EVT-1", "EVT-3": "PAYLOAD-EVT-3"}
        assert redacted_targets_for_stream(c, STREAM, budget(max_events=100, max_redaction_rows=2)) == legacy
        with pytest.raises(ResourceBudgetExceeded) as captured:
            redacted_targets_for_stream(c, STREAM, budget(max_events=100, max_redaction_rows=1))
        assert (captured.value.dimension, captured.value.limit, captured.value.observed) == ("redaction_rows", 1, 2)
        assert not c.in_transaction  # its own snapshot is released


def test_helper_never_returns_a_partial_selection_and_refuses_before_fetching() -> None:
    with fresh() as store:
        forge(store, 40)
        c = store.raw_connection_for_tests()
        statements = traced(store)
        with pytest.raises(ResourceBudgetExceeded):
            redacted_targets_for_stream(c, STREAM, budget(max_events=10))
        untrace(store)
        assert not any(s.strip().startswith(HELPER_FETCH_PREFIX) for s in statements)
        # exact boundary: 40 rows pass at limit 40, fail at 39 (no truncated dict in either case)
        assert len(redacted_targets_for_stream(c, STREAM, budget(max_events=100, max_redaction_rows=40))) == 40
        with pytest.raises(ResourceBudgetExceeded):
            redacted_targets_for_stream(c, STREAM, budget(max_events=100, max_redaction_rows=39))


def test_helper_measures_only_the_columns_it_loads_for_record_and_total_bytes() -> None:
    with fresh() as store:
        forge(store, 1, reason="huge-reason-is-not-loaded-by-the-helper" * 100)
        c = store.raw_connection_for_tests()
        assert len(redacted_targets_for_stream(c, STREAM, budget(max_events=10))) == 1  # reason is not loaded here
    with fresh() as store:
        forge(store, 1)
        c = store.raw_connection_for_tests()
        # the helper's loaded columns are tiny; shrinking the record limit below them refuses
        size = len("FORGED-0") + len("PAYLOAD-F-0")
        assert len(redacted_targets_for_stream(c, STREAM, budget(max_redaction_record_bytes=size))) == 1
        with pytest.raises(ResourceBudgetExceeded) as record:
            redacted_targets_for_stream(c, STREAM, budget(max_redaction_record_bytes=size - 1))
        assert record.value.dimension == "redaction_record_bytes" and record.value.observed == size
        with pytest.raises(ResourceBudgetExceeded) as total:
            redacted_targets_for_stream(c, STREAM, budget(max_total_redaction_bytes=size - 1))
        assert total.value.dimension == "redaction_total_bytes"


def test_helper_preserves_a_callers_transaction_and_snapshot() -> None:
    with fresh() as store:
        forge(store, 3)
        c = store.raw_connection_for_tests()
        c.execute("CREATE TABLE sentinel(x)")
        c.execute("BEGIN")
        c.execute("INSERT INTO sentinel VALUES (1)")
        assert len(redacted_targets_for_stream(c, STREAM, budget(max_events=10))) == 3
        with pytest.raises(ResourceBudgetExceeded):
            redacted_targets_for_stream(c, STREAM, budget(max_events=2))
        assert c.in_transaction and c.execute("SELECT COUNT(*) FROM sentinel").fetchone()[0] == 1
        c.execute("ROLLBACK")
        assert c.execute("SELECT COUNT(*) FROM sentinel").fetchone()[0] == 0


def test_helper_errors_never_contain_reason_or_payload_content() -> None:
    with fresh() as store:
        forge(store, 1, reason=SECRET * 50)
        c = store.raw_connection_for_tests()
        with pytest.raises(ResourceBudgetExceeded) as captured:
            redacted_targets_for_stream(c, STREAM, budget(max_redaction_record_bytes=5))
        text = str(captured.value) + repr(captured.value) + repr(captured.value.args)
        assert SECRET not in text and "FORGED-0" not in text and "PAYLOAD-F-0" not in text


def test_infeasible_three_limit_profile_is_still_a_resource_refusal_never_a_success() -> None:
    """A profile smaller than the stream's own audit payload (1-byte limits) is
    refused at the redaction metadata preflight before any payload is decoded;
    only the diagnostic dimension differs from the payload-budget refusal that
    explicit redaction bounds still reach (see the linkage test)."""

    with SQLiteEventPayloadStore.in_memory() as store:
        store.initialize_schema()
        red.append_target(store)
        red.executor(store).redact(red.redaction_request())
        report = R0IntegrityVerifier(store, red.registry(), VerificationBudget(100, 1, 1)).verify_stream(STREAM)
        assert not report.ok and report.failure.code is IntegrityCode.RESOURCE_BUDGET_EXCEEDED
        assert "redaction_record_bytes" in report.failure.message
