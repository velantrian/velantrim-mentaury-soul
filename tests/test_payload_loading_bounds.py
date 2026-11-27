"""Stage 04D: bounded payload (BLOB) loading, AUD-04-F4.

Pattern under test: probe (exists / typeof / length) -> admit against the budget
-> only then fetch. The instrument is SQLite's own statement trace: a *full
load* is any ``SELECT [payload_ref,] payload_bytes ...`` statement. The claims
are about what Python materializes, not about SQLite page reads or process
memory. Budgets are small explicit test profiles, not production values.
"""

from __future__ import annotations

import re
import sqlite3
from pathlib import Path

import pytest

import test_atomic_batch as atomic
import test_integrity as ti
import test_r1_replay as r1
import test_redaction as red
from dataclasses import replace

from mentaury.contracts import canonical_json_bytes
from mentaury.storage import (
    IntegrityCode,
    PayloadChangedError,
    PayloadStorageTypeError,
    R0IntegrityReport,
    R0IntegrityVerifier,
    ResourceBudgetExceeded,
    SQLiteEventPayloadStore,
    StorageError,
    TargetPayloadMissingError,
    TransactionOwnershipError,
    VerificationBudget,
)
from mentaury.storage._bounded_read import fetch_probed
import mentaury.storage.integrity as integrity_module

FULL = re.compile(r"^\s*SELECT\s+(payload_ref,\s*)?payload_bytes\b", re.I)
SECRET = b"SECRET-BLOB-CONTENT-MUST-NEVER-LEAK"
STREAM = "test:stream"  # redaction fixtures
ATOMIC_STREAM = "belief:B-204"  # padded_stream fixtures


def trace(store) -> list[str]:
    statements: list[str] = []
    store.raw_connection_for_tests().set_trace_callback(statements.append)
    return statements


def untrace(store) -> None:
    store.raw_connection_for_tests().set_trace_callback(None)


def full_loads(statements: list[str], ref: str | None = None) -> int:
    return sum(1 for s in statements if FULL.match(s) and (ref is None or ref in s))


def inflate(store, ref: str, size: int) -> None:
    """Make a stored payload ``size`` bytes (content is a recognizable marker)."""

    c = store.raw_connection_for_tests()
    c.execute("DROP TRIGGER IF EXISTS payload_material_cannot_be_rewritten")
    c.execute("UPDATE event_payloads SET payload_bytes = ? WHERE payload_ref = ?",
              ((SECRET * (size // len(SECRET) + 1))[:size], ref))


def poison_type(store, ref: str, value) -> None:
    """Replace the table with a non-STRICT copy holding a mistyped value (test fixture only)."""

    c = store.raw_connection_for_tests()
    rows = c.execute("SELECT payload_ref, payload_bytes, created_at FROM event_payloads").fetchall()
    c.execute("DROP TABLE event_payloads")
    c.execute("CREATE TABLE event_payloads(payload_ref TEXT PRIMARY KEY NOT NULL, "
              "payload_bytes BLOB NOT NULL, created_at TEXT NOT NULL)")
    for row in rows:
        c.execute("INSERT INTO event_payloads VALUES (?, ?, ?)",
                  (row[0], value if row[0] == ref else row[1], row[2]))


def budget(payload=1_000, total=5_000, events=100) -> VerificationBudget:
    return VerificationBudget(events, payload, total)


def r0(store, **kw) -> R0IntegrityVerifier:
    return R0IntegrityVerifier(store, atomic.registry(), budget(**kw))


def padded_stream(store, sizes: list[int]) -> list[str]:
    """Valid stream whose canonical payloads have exactly the given byte sizes."""

    refs = []
    for index, size in enumerate(sizes):
        overhead = len(canonical_json_bytes({"p": ""}))
        payload = {"p": "x" * (size - overhead)}
        assert len(canonical_json_bytes(payload)) == size
        event = replace(
            atomic.event(0, batch_size=1, batch_id=f"B-{index}"),
            event_id=f"EVT-{index + 1}", stream_version=index + 1, payload_ref=f"PAYLOAD-{index + 1}",
        )
        store.append_one(event, payload, registry=atomic.registry())
        refs.append(event.payload_ref)
    return refs


def one_event_store(tmp_path: Path | None = None) -> SQLiteEventPayloadStore:
    store = (SQLiteEventPayloadStore.connect(tmp_path / "p.sqlite3") if tmp_path
             else SQLiteEventPayloadStore.in_memory())
    store.initialize_schema()
    return store


def redacted_store() -> SQLiteEventPayloadStore:
    store = SQLiteEventPayloadStore.in_memory()
    store.initialize_schema()
    red.append_target(store)
    red.executor(store).redact(red.redaction_request())
    return store


def red_r0(store, **kw) -> R0IntegrityVerifier:
    return R0IntegrityVerifier(store, red.registry(), budget(**kw))


def refused(report) -> None:
    assert not report.ok and report.failure is not None
    assert report.failure.code is IntegrityCode.RESOURCE_BUDGET_EXCEEDED


# --- R0: normal payload ----------------------------------------------------------------------------------------------

def test_oversized_blob_is_refused_before_it_is_loaded_with_a_live_instrument() -> None:
    with one_event_store() as store:
        refs = padded_stream(store, [100])
        inflate(store, refs[0], 2_000_000)
        statements = trace(store)
        report = r0(store).verify_stream(ATOMIC_STREAM)
        untrace(store)
        refused(report)
        assert report.failure.event_id == "EVT-1"
        assert "payload_bytes limit 1000, observed 2000000" in report.failure.message
        assert full_loads(statements) == 0  # the rejected BLOB was never fetched
        assert any("typeof(payload_bytes)" in s for s in statements)  # the probe did run
        # positive control: with a budget that admits it, the same instrument sees the load
        statements = trace(store)
        r0(store, payload=3_000_000, total=3_000_000).verify_stream(ATOMIC_STREAM)
        untrace(store)
        assert full_loads(statements, refs[0]) == 1


def test_individual_boundary_is_exact_and_one_byte_over_is_refused() -> None:
    with one_event_store() as store:
        padded_stream(store, [300])
        assert r0(store, payload=300, total=300).verify_stream(ATOMIC_STREAM).ok
        report = r0(store, payload=299, total=300).verify_stream(ATOMIC_STREAM)
        refused(report)
        assert "payload_bytes limit 299, observed 300" in report.failure.message


def test_aggregate_over_budget_with_individually_valid_blobs_stops_before_the_load() -> None:
    with one_event_store() as store:
        refs = padded_stream(store, [300, 300, 300])
        statements = trace(store)
        report = r0(store, payload=350, total=700).verify_stream(ATOMIC_STREAM)
        untrace(store)
        refused(report)
        assert "total_payload_bytes limit 700, observed 900" in report.failure.message
        assert report.failure.event_id == "EVT-3"
        assert full_loads(statements, refs[2]) == 0 and full_loads(statements, refs[1]) == 1
        # exact aggregate boundary
        assert r0(store, payload=350, total=900).verify_stream(ATOMIC_STREAM).ok
        refused(r0(store, payload=350, total=899).verify_stream(ATOMIC_STREAM))


def test_missing_payload_keeps_its_diagnostic() -> None:
    with one_event_store() as store:
        refs = padded_stream(store, [100])
        store.raw_connection_for_tests().execute("DELETE FROM event_payloads WHERE payload_ref = ?", (refs[0],))
        report = r0(store).verify_stream(ATOMIC_STREAM)
        assert not report.ok and report.failure.code is IntegrityCode.PAYLOAD_MISSING


@pytest.mark.parametrize("value", ["not-bytes-text", 5, 1.5])
def test_mistyped_stored_value_is_refused_without_conversion_to_bytes(value) -> None:
    with one_event_store() as store:
        refs = padded_stream(store, [100])
        poison_type(store, refs[0], value)
        statements = trace(store)
        report = r0(store).verify_stream(ATOMIC_STREAM)
        untrace(store)
        assert not report.ok
        assert report.failure.code is IntegrityCode.PAYLOAD_STORAGE_TYPE_INVALID
        assert full_loads(statements) == 0  # nothing was fetched, let alone bytes()-converted
        assert "bytes(" not in report.failure.message


# --- R0: linked audit payload, existence-only, accounting ---------------------------------------------------------------

def test_linked_audit_payload_is_probed_and_refused_before_it_is_loaded() -> None:
    with redacted_store() as store:
        inflate(store, "PAYLOAD-REDACTION-AUDIT-1", 2_000_000)
        statements = trace(store)
        report = red_r0(store).verify_stream(STREAM)
        untrace(store)
        refused(report)
        assert report.failure.event_id == "EVT-1"  # reported on the redaction target, as before
        assert full_loads(statements, "PAYLOAD-REDACTION-AUDIT-1") == 0


def test_missing_and_mistyped_audit_payload_keep_distinct_diagnostics() -> None:
    with redacted_store() as store:
        store.raw_connection_for_tests().execute("DELETE FROM event_payloads WHERE payload_ref = 'PAYLOAD-REDACTION-AUDIT-1'")
        report = red_r0(store).verify_stream(STREAM)
        assert report.failure.code is IntegrityCode.REDACTION_AUDIT_PAYLOAD_MISSING
    with redacted_store() as store:
        poison_type(store, "PAYLOAD-REDACTION-AUDIT-1", "text")
        report = red_r0(store).verify_stream(STREAM)
        assert report.failure.code is IntegrityCode.PAYLOAD_STORAGE_TYPE_INVALID
        assert "audit payload" in report.failure.message


def test_redacted_payload_existence_is_checked_without_reading_its_content() -> None:
    with redacted_store() as store:
        c = store.raw_connection_for_tests()
        c.execute("INSERT INTO event_payloads VALUES ('PAYLOAD-EVT-1', ?, '2026-08-05T00:00:00Z')", (SECRET * 100_000,))
        statements = trace(store)
        report = red_r0(store, payload=10**7, total=10**8).verify_stream(STREAM)
        untrace(store)
        assert not report.ok and report.failure.code is IntegrityCode.REDACTED_PAYLOAD_STILL_PRESENT
        assert full_loads(statements, "PAYLOAD-EVT-1") == 0
        assert not any("typeof(payload_bytes)" in s and "PAYLOAD-EVT-1" in s for s in statements)
        # even over the budget it is still "still present", not a resource refusal: no size was read
        assert red_r0(store).verify_stream(STREAM).failure.code is IntegrityCode.REDACTED_PAYLOAD_STILL_PRESENT


def test_redaction_checks_target_existence_without_loading_the_payload_it_deletes() -> None:
    with SQLiteEventPayloadStore.in_memory() as store:
        store.initialize_schema()
        red.append_target(store)
        inflate(store, "PAYLOAD-EVT-1", 2_000_000)
        statements = trace(store)
        result = red.executor(store).redact(red.redaction_request())
        untrace(store)
        assert result.status.value == "REDACTED"
        assert full_loads(statements, "PAYLOAD-EVT-1") == 0
        assert store.load_payload("PAYLOAD-EVT-1") is None
    with SQLiteEventPayloadStore.in_memory() as store:
        store.initialize_schema()
        red.append_target(store)
        store.raw_connection_for_tests().execute("DELETE FROM event_payloads WHERE payload_ref = 'PAYLOAD-EVT-1'")
        with pytest.raises(TargetPayloadMissingError):
            red.executor(store).redact(red.redaction_request())


def test_audit_payload_is_counted_once_logically_and_loaded_twice_physically() -> None:
    with redacted_store() as store:
        audit_size = len(store.load_payload("PAYLOAD-REDACTION-AUDIT-1").payload_bytes)
        statements = trace(store)
        # the only payload that counts is the audit event's own, once: total == its size passes
        assert red_r0(store, payload=audit_size, total=audit_size).verify_stream(STREAM).ok
        untrace(store)
        # reported physical loads: once as redaction evidence, once as the stream's own event
        assert full_loads(statements, "PAYLOAD-REDACTION-AUDIT-1") == 2
        # not double counted logically; one byte less than the single charge is refused
        refused(red_r0(store, payload=audit_size - 1, total=audit_size - 1).verify_stream(STREAM))


def test_logical_total_with_a_redaction_equals_only_the_payloads_actually_present() -> None:
    with SQLiteEventPayloadStore.in_memory() as store:
        store.initialize_schema()
        red.append_target(store, event_id="EVT-1", version=1)
        red.append_target(store, event_id="EVT-2", version=2, n=2)
        red.executor(store).redact(red.redaction_request(expected_stream_version=2))  # redacts EVT-1
        present = sum(len(store.load_payload(f"PAYLOAD-{e}").payload_bytes)
                      for e in ("EVT-2", "REDACTION-AUDIT-1"))
        top = max(len(store.load_payload(f"PAYLOAD-{e}").payload_bytes) for e in ("EVT-2", "REDACTION-AUDIT-1"))
        assert red_r0(store, payload=top, total=present).verify_stream(STREAM).ok
        report = red_r0(store, payload=top, total=present - 1).verify_stream(STREAM)
        refused(report)
        assert f"observed {present}" in report.failure.message  # counted once each, no double charge


# --- R1 ------------------------------------------------------------------------------------------------------------------

def test_r1_refuses_an_oversized_payload_before_loading_it(monkeypatch) -> None:
    with SQLiteEventPayloadStore.in_memory() as store:
        store.initialize_schema()
        first = r1._append_counter(store, "EVT-1", 1, 2)
        inflate(store, first.payload_ref, 2_000_000)
        # R0 (same budget) would reject this first; stub it to reach R1's own admission
        monkeypatch.setattr(R0IntegrityVerifier, "_verify_stream_in_snapshot",
                            lambda self, stream_id: R0IntegrityReport(stream_id, True, 1, None))
        statements = trace(store)
        report = r1._verifier(store, budget=r1._budget(max_payload_bytes=1_000)).verify_stream(
            r1.STREAM_ID, r1._snapshot_after_first_for_empty())
        untrace(store)
        assert not report.ok and report.failure.code.value == "RESOURCE_BUDGET_EXCEEDED"
        assert full_loads(statements) == 0
        assert not store.raw_connection_for_tests().in_transaction


def test_r1_normal_replay_still_loads_once_per_state_affecting_event() -> None:
    with SQLiteEventPayloadStore.in_memory() as store:
        store.initialize_schema()
        first = r1._append_counter(store, "EVT-1", 1, 2)
        statements = trace(store)
        report = r1._verifier(store).verify_stream(r1.STREAM_ID, r1._snapshot_after_first(first))
        untrace(store)
        assert report.ok
        assert full_loads(statements, first.payload_ref) >= 1  # positive control for the R1 path


# --- migration v2 -> v3 -----------------------------------------------------------------------------------------------------

def v2_database(tmp_path: Path, events: int = 2) -> Path:
    database = tmp_path / "legacy.sqlite3"
    with SQLiteEventPayloadStore.connect(database) as store:
        store.initialize_schema()
        ti.append_valid_stream(store, events)
    ti._downgrade_database_to_v2(database, tamper=False)
    return database


def schema_version(store) -> int:
    return store.raw_connection_for_tests().execute("SELECT schema_version FROM p0_schema_meta").fetchone()[0]


def has_table(store, name: str) -> bool:
    return store.raw_connection_for_tests().execute(
        "SELECT 1 FROM sqlite_master WHERE name = ?", (name,)).fetchone() is not None


def test_migration_refuses_an_oversized_payload_before_loading_it_and_leaves_no_partial_state(tmp_path) -> None:
    database = v2_database(tmp_path)
    with SQLiteEventPayloadStore.connect(database) as store:
        inflate(store, "PAYLOAD-1", 2_000_000)
        statements = trace(store)
        with pytest.raises(ResourceBudgetExceeded) as captured:
            store.initialize_schema(migration_registry=ti.registry(),
                                    migration_budget=ti.verification_budget(max_payload_bytes=1_000))
        untrace(store)
        assert captured.value.dimension == "payload_bytes"
        assert full_loads(statements, "PAYLOAD-1") == 0
        assert schema_version(store) == 2 and not has_table(store, "stream_meta")
        assert not store.raw_connection_for_tests().in_transaction
        assert SECRET.decode() not in str(captured.value)


def test_migration_aggregate_is_checked_before_the_second_load(tmp_path) -> None:
    database = v2_database(tmp_path)
    with SQLiteEventPayloadStore.connect(database) as store:
        size = store.raw_connection_for_tests().execute(
            "SELECT length(payload_bytes) FROM event_payloads WHERE payload_ref = 'PAYLOAD-1'").fetchone()[0]
        statements = trace(store)
        with pytest.raises(ResourceBudgetExceeded) as captured:
            store.initialize_schema(migration_registry=ti.registry(), migration_budget=
                                    ti.verification_budget(max_payload_bytes=size, max_total_payload_bytes=size))
        untrace(store)
        assert captured.value.dimension == "total_payload_bytes" and captured.value.observed == 2 * size
        assert full_loads(statements, "PAYLOAD-1") == 1 and full_loads(statements, "PAYLOAD-2") == 0
        assert schema_version(store) == 2 and not has_table(store, "stream_meta")
        # exact boundary then succeeds, once, with the physical loads visible
        statements = trace(store)
        store.initialize_schema(migration_registry=ti.registry(), migration_budget=
                                ti.verification_budget(max_payload_bytes=size, max_total_payload_bytes=2 * size))
        untrace(store)
        assert schema_version(store) == 4 and full_loads(statements) == 2


def test_migration_refuses_mistyped_and_missing_payloads_with_controlled_errors(tmp_path) -> None:
    (tmp_path / "typed").mkdir()
    (tmp_path / "missing").mkdir()
    with SQLiteEventPayloadStore.connect(v2_database(tmp_path / "typed")) as store:
        poison_type(store, "PAYLOAD-1", "text")
        with pytest.raises(StorageError, match="payload storage invalid"):
            store.initialize_schema(migration_registry=ti.registry(), migration_budget=ti.verification_budget())
        assert schema_version(store) == 2 and not has_table(store, "stream_meta")
    with SQLiteEventPayloadStore.connect(v2_database(tmp_path / "missing")) as store:
        store.raw_connection_for_tests().execute("DELETE FROM event_payloads WHERE payload_ref = 'PAYLOAD-1'")
        with pytest.raises(StorageError, match="payload missing"):
            store.initialize_schema(migration_registry=ti.registry(), migration_budget=ti.verification_budget())


def test_migration_inside_a_foreign_transaction_is_still_refused_untouched(tmp_path) -> None:
    database = v2_database(tmp_path)
    with SQLiteEventPayloadStore.connect(database) as store:
        c = store.raw_connection_for_tests()
        c.execute("CREATE TABLE sentinel(x)")
        c.execute("BEGIN")
        c.execute("INSERT INTO sentinel VALUES (1)")
        with pytest.raises(TransactionOwnershipError):
            store.initialize_schema(migration_registry=ti.registry(), migration_budget=ti.verification_budget())
        assert c.in_transaction and c.execute("SELECT COUNT(*) FROM sentinel").fetchone()[0] == 1
        c.execute("ROLLBACK")


# --- public bounded load_payload ---------------------------------------------------------------------------------------------

def test_bounded_load_payload_boundaries_and_early_refusal() -> None:
    with one_event_store() as store:
        refs = padded_stream(store, [300])
        assert store.load_payload(refs[0], budget(payload=300, total=300)).payload_bytes
        with pytest.raises(ResourceBudgetExceeded) as individual:
            store.load_payload(refs[0], budget(payload=299, total=300))
        assert (individual.value.dimension, individual.value.limit, individual.value.observed) == ("payload_bytes", 299, 300)
        with pytest.raises(ResourceBudgetExceeded) as aggregate:  # caller already loaded 500 bytes
            store.load_payload(refs[0], budget(payload=400, total=700), total_loaded_bytes=500)
        assert (aggregate.value.dimension, aggregate.value.observed) == ("total_payload_bytes", 800)
        assert store.load_payload("ABSENT", budget()) is None
        inflate(store, refs[0], 2_000_000)
        statements = trace(store)
        with pytest.raises(ResourceBudgetExceeded):
            store.load_payload(refs[0], budget())
        untrace(store)
        assert full_loads(statements) == 0
        assert not store.raw_connection_for_tests().in_transaction  # own snapshot released


def test_bounded_load_payload_refuses_a_mistyped_value_and_keeps_errors_content_free() -> None:
    with one_event_store() as store:
        refs = padded_stream(store, [100])
        poison_type(store, refs[0], 5)
        with pytest.raises(PayloadStorageTypeError) as captured:
            store.load_payload(refs[0], budget())
        assert "integer" in str(captured.value) and "bytes(" not in str(captured.value)
    with one_event_store() as store:
        refs = padded_stream(store, [100])
        inflate(store, refs[0], 50_000)
        with pytest.raises(ResourceBudgetExceeded) as captured:
            store.load_payload(refs[0], budget())
        assert SECRET.decode() not in str(captured.value) + repr(captured.value) + repr(captured.value.args)


def test_legacy_load_payload_and_existence_method_are_unchanged() -> None:
    with one_event_store() as store:
        refs = padded_stream(store, [200])
        assert len(store.load_payload(refs[0]).payload_bytes) == 200  # no budget: legacy read
        assert store.payload_exists(refs[0]) and not store.payload_exists("ABSENT")


def test_bounded_load_preserves_a_callers_transaction() -> None:
    with one_event_store() as store:
        refs = padded_stream(store, [100])
        c = store.raw_connection_for_tests()
        c.execute("CREATE TABLE sentinel(x)")
        c.execute("BEGIN")
        c.execute("INSERT INTO sentinel VALUES (1)")
        assert store.load_payload(refs[0], budget()) is not None
        with pytest.raises(ResourceBudgetExceeded):
            store.load_payload(refs[0], budget(payload=10, total=10))
        assert c.in_transaction and c.execute("SELECT COUNT(*) FROM sentinel").fetchone()[0] == 1
        c.execute("ROLLBACK")


# --- concurrency and the change-detection guard ------------------------------------------------------------------------------

def test_probe_and_load_share_one_snapshot_under_a_concurrent_writer(tmp_path) -> None:
    database = tmp_path / "c.sqlite3"
    with SQLiteEventPayloadStore.connect(database) as setup:
        setup.initialize_schema()
        refs = padded_stream(setup, [300])
    reader, writer = SQLiteEventPayloadStore.connect(database), SQLiteEventPayloadStore.connect(database)
    with reader, writer:
        fired: list[int] = []

        def hook(statement: str) -> None:
            if FULL.match(statement) and not fired:
                fired.append(1)  # another connection swaps the payload for a 2 MB blob, committed
                writer.raw_connection_for_tests().execute("DELETE FROM event_payloads WHERE payload_ref = ?", (refs[0],))
                writer.raw_connection_for_tests().execute(
                    "INSERT INTO event_payloads VALUES (?, ?, '2026-08-05T00:00:00Z')", (refs[0], SECRET * 60_000))

        reader.raw_connection_for_tests().set_trace_callback(hook)
        report = R0IntegrityVerifier(reader, atomic.registry(), budget(payload=350, total=350)).verify_stream(ATOMIC_STREAM)
        reader.raw_connection_for_tests().set_trace_callback(None)
        assert fired and report.ok, report.failure  # probe and fetch saw the same (old) version
        later = R0IntegrityVerifier(reader, atomic.registry(), budget(payload=350, total=350)).verify_stream(ATOMIC_STREAM)
        refused(later)  # after the snapshot the swapped-in blob is visible and bounded


def test_size_mismatch_between_probe_and_fetch_is_detected_not_trusted() -> None:
    with one_event_store() as store:
        refs = padded_stream(store, [100])
        with pytest.raises(PayloadChangedError):
            fetch_probed(store.raw_connection_for_tests(), refs[0], 99)
        with pytest.raises(PayloadChangedError):
            fetch_probed(store.raw_connection_for_tests(), "ABSENT", 1)


def test_r0_reports_an_incoherent_snapshot_if_the_guard_trips(monkeypatch) -> None:
    def tripped(*args, **kwargs):
        raise PayloadChangedError(1, 2)

    with one_event_store() as store:
        padded_stream(store, [100])
        monkeypatch.setattr(integrity_module, "admit_and_load", tripped)
        report = r0(store).verify_stream(ATOMIC_STREAM)
        assert not report.ok and report.failure.code is IntegrityCode.SNAPSHOT_INCOHERENT


def test_external_transaction_is_still_refused_by_r0_and_left_untouched() -> None:
    with one_event_store() as store:
        padded_stream(store, [100])
        c = store.raw_connection_for_tests()
        c.execute("CREATE TABLE sentinel(x)")
        c.execute("BEGIN")
        c.execute("INSERT INTO sentinel VALUES (1)")
        assert r0(store).verify_stream(ATOMIC_STREAM).failure.code is IntegrityCode.ACTIVE_TRANSACTION
        assert c.in_transaction and c.execute("SELECT COUNT(*) FROM sentinel").fetchone()[0] == 1
        c.execute("ROLLBACK")
