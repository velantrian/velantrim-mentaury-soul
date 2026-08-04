from __future__ import annotations

import threading
from pathlib import Path
from queue import Queue

import pytest

from mentaury.storage import (
    BusyRetryPolicy,
    IdempotencyConflictError,
    IdempotencyStatus,
    SQLiteEventPayloadStore,
    SQLiteIdempotentBatchAppender,
    StoreBusyError,
    VersionConflictError,
)
from test_idempotency import command, pending_batch, request


def test_busy_retry_exhaustion_is_controlled_and_writes_nothing(tmp_path: Path) -> None:
    database = tmp_path / "busy.sqlite3"
    policy = BusyRetryPolicy(max_attempts=2, backoff_seconds=0.001)
    with SQLiteEventPayloadStore.connect(database, busy_policy=policy) as holder:
        holder.initialize_schema()
        holder.raw_connection_for_tests().execute("BEGIN IMMEDIATE")
        try:
            with SQLiteEventPayloadStore.connect(database, busy_policy=policy) as contender:
                with pytest.raises(StoreBusyError) as captured:
                    SQLiteIdempotentBatchAppender(contender, policy).append(request())
                assert captured.value.attempts == 2
                assert contender.list_stream("belief:B-204") == ()
        finally:
            holder.raw_connection_for_tests().execute("ROLLBACK")


def _run_request(
    database: Path,
    request_value,
    barrier: threading.Barrier,
    outcomes: Queue[object],
) -> None:
    policy = BusyRetryPolicy(max_attempts=50, backoff_seconds=0.002)
    try:
        with SQLiteEventPayloadStore.connect(database, busy_policy=policy) as store:
            barrier.wait()
            result = SQLiteIdempotentBatchAppender(store, policy).append(request_value)
            outcomes.put(result.status)
    except BaseException as exc:  # captured for deterministic test assertion
        outcomes.put(exc)


def test_concurrent_same_key_same_semantics_replays_once(tmp_path: Path) -> None:
    database = tmp_path / "same.sqlite3"
    with SQLiteEventPayloadStore.connect(database) as setup:
        setup.initialize_schema()

    first = request(generation="A")
    retry_cmd = command(
        command_id="CMD-B",
        issued_at="2026-08-05T00:01:00Z",
        correlation_id="CORR-B",
    )
    second = request(retry_cmd, pending_batch(), generation="B")
    barrier = threading.Barrier(2)
    outcomes: Queue[object] = Queue()
    threads = [
        threading.Thread(target=_run_request, args=(database, first, barrier, outcomes)),
        threading.Thread(target=_run_request, args=(database, second, barrier, outcomes)),
    ]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join(timeout=5)
        assert not thread.is_alive()

    values = [outcomes.get_nowait(), outcomes.get_nowait()]
    assert sorted(str(value) for value in values) == [
        IdempotencyStatus.ALREADY_APPLIED,
        IdempotencyStatus.APPLIED,
    ]
    with SQLiteEventPayloadStore.connect(database) as check:
        assert len(check.list_stream("belief:B-204")) == 2


def test_concurrent_same_key_changed_semantics_conflicts(tmp_path: Path) -> None:
    database = tmp_path / "conflict.sqlite3"
    with SQLiteEventPayloadStore.connect(database) as setup:
        setup.initialize_schema()

    first = request(generation="A")
    changed = request(
        command(payload_value="beta"),
        pending_batch(first_payload="beta"),
        generation="B",
    )
    barrier = threading.Barrier(2)
    outcomes: Queue[object] = Queue()
    threads = [
        threading.Thread(target=_run_request, args=(database, first, barrier, outcomes)),
        threading.Thread(target=_run_request, args=(database, changed, barrier, outcomes)),
    ]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join(timeout=5)
        assert not thread.is_alive()

    values = [outcomes.get_nowait(), outcomes.get_nowait()]
    assert sum(value is IdempotencyStatus.APPLIED for value in values) == 1
    assert sum(isinstance(value, IdempotencyConflictError) for value in values) == 1


def test_concurrent_different_keys_same_version_is_controlled(tmp_path: Path) -> None:
    database = tmp_path / "version.sqlite3"
    with SQLiteEventPayloadStore.connect(database) as setup:
        setup.initialize_schema()

    first = request(command(idempotency_key="KEY-A"), generation="A")
    second = request(command(idempotency_key="KEY-B"), generation="B")
    barrier = threading.Barrier(2)
    outcomes: Queue[object] = Queue()
    threads = [
        threading.Thread(target=_run_request, args=(database, first, barrier, outcomes)),
        threading.Thread(target=_run_request, args=(database, second, barrier, outcomes)),
    ]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join(timeout=5)
        assert not thread.is_alive()

    values = [outcomes.get_nowait(), outcomes.get_nowait()]
    assert sum(value is IdempotencyStatus.APPLIED for value in values) == 1
    assert sum(isinstance(value, VersionConflictError) for value in values) == 1
    with SQLiteEventPayloadStore.connect(database) as check:
        assert len(check.list_stream("belief:B-204")) == 2


def test_busy_policy_validation() -> None:
    with pytest.raises(ValueError):
        BusyRetryPolicy(max_attempts=0)
    with pytest.raises(ValueError):
        BusyRetryPolicy(backoff_seconds=-1)


def test_sqlite_runtime_gate_and_busy_timeout(tmp_path: Path) -> None:
    from mentaury.storage import (
        MINIMUM_SQLITE_VERSION,
        StorageError,
        ensure_supported_sqlite_runtime,
    )

    ensure_supported_sqlite_runtime(MINIMUM_SQLITE_VERSION)
    with pytest.raises(StorageError, match="unsupported SQLite"):
        ensure_supported_sqlite_runtime((3, 36, 0))

    database = tmp_path / "timeout.sqlite3"
    with SQLiteEventPayloadStore.connect(database, busy_timeout_ms=17) as store:
        value = store.raw_connection_for_tests().execute(
            "PRAGMA busy_timeout"
        ).fetchone()[0]
        assert value == 17
