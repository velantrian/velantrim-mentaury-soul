"""Stage 01 remediation: writers may commit/roll back only their own transaction.

Contract under test: public writers and ``initialize_schema`` require an idle
connection. An already-active transaction is foreign; the operation refuses with
``TransactionOwnershipError`` and neither commits, rolls back, nor mutates it.
"""

from __future__ import annotations

import sqlite3
from collections.abc import Callable
from pathlib import Path

import pytest

import test_atomic_batch as atomic
import test_idempotency as idem
import test_redaction as redact
import test_sqlite_store as plain
from mentaury.storage import (
    SCHEMA_VERSION,
    SQLiteAtomicBatchAppender,
    SQLiteEventPayloadStore,
    SQLiteIdempotentBatchAppender,
    SQLiteRedactionExecutor,
    StorageError,
    TransactionOwnershipError,
)
from mentaury.storage.concurrency import begin_immediate
from test_integrity import (
    _downgrade_database_to_v2,
    append_valid_stream,
    registry as integrity_registry,
    verification_budget,
)

Writer = Callable[[SQLiteEventPayloadStore], object]


def _sentinel_count(connection: sqlite3.Connection) -> int:
    return connection.execute("SELECT COUNT(*) FROM sentinel").fetchone()[0]


def _open_external(connection: sqlite3.Connection) -> None:
    connection.execute("CREATE TABLE IF NOT EXISTS sentinel(x)")
    connection.execute("BEGIN")
    connection.execute("INSERT INTO sentinel VALUES (1)")


def _ready_store() -> SQLiteEventPayloadStore:
    store = SQLiteEventPayloadStore.in_memory()
    store.initialize_schema()
    store.raw_connection_for_tests().execute("CREATE TABLE sentinel(x)")
    return store


def _row_counts(connection: sqlite3.Connection) -> dict[str, int]:
    return {
        table: connection.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        for table in (
            "events",
            "event_payloads",
            "stream_meta",
            "idempotency_records",
            "redactions",
        )
    }


# --- writers -----------------------------------------------------------------

def _w_append_one(store: SQLiteEventPayloadStore) -> object:
    return store.append_one(plain.event(), {"a": 1}, registry=plain.registry())


def _w_atomic(store: SQLiteEventPayloadStore) -> object:
    return SQLiteAtomicBatchAppender(store, atomic.registry()).append(atomic.entries())


def _w_idempotent(store: SQLiteEventPayloadStore) -> object:
    return SQLiteIdempotentBatchAppender(store, idem.registry()).append(
        idem.request()
    )


def _w_redact(store: SQLiteEventPayloadStore) -> object:
    return SQLiteRedactionExecutor(store, redact.registry()).redact(
        redact.redaction_request()
    )


def _prepare_redact(store: SQLiteEventPayloadStore) -> None:
    redact.append_target(store)


WRITERS = [
    pytest.param(_w_append_one, None, id="append_one"),
    pytest.param(_w_atomic, None, id="atomic_batch"),
    pytest.param(_w_idempotent, None, id="idempotent_append"),
    pytest.param(_w_redact, _prepare_redact, id="redact"),
]


# T01 -------------------------------------------------------------------------

def test_begin_immediate_refuses_external_transaction_without_touching_it() -> None:
    with _ready_store() as store:
        connection = store.raw_connection_for_tests()
        _open_external(connection)
        with pytest.raises(TransactionOwnershipError):
            begin_immediate(connection)
        assert connection.in_transaction
        assert _sentinel_count(connection) == 1
        connection.execute("ROLLBACK")
        assert _sentinel_count(connection) == 0


def test_ownership_error_is_not_a_busy_error_and_not_retried() -> None:
    from mentaury.storage import BusyRetryPolicy, StoreBusyError

    slow = BusyRetryPolicy(max_attempts=50, backoff_seconds=1.0)
    with _ready_store() as store:
        connection = store.raw_connection_for_tests()
        _open_external(connection)
        with pytest.raises(TransactionOwnershipError) as captured:
            begin_immediate(connection, slow)  # would take ~50s if it retried
        assert not isinstance(captured.value, StoreBusyError)
        assert captured.value.operation == "begin_immediate"
        connection.execute("ROLLBACK")


# T02 / T05 -------------------------------------------------------------------

@pytest.mark.parametrize("writer, prepare", WRITERS)
@pytest.mark.parametrize("owner_action", ["COMMIT", "ROLLBACK"])
def test_public_writers_refuse_external_transaction_and_owner_stays_usable(
    writer: Writer,
    prepare: Callable[[SQLiteEventPayloadStore], None] | None,
    owner_action: str,
) -> None:
    with _ready_store() as store:
        if prepare:
            prepare(store)
        connection = store.raw_connection_for_tests()
        before = _row_counts(connection)
        _open_external(connection)

        with pytest.raises(TransactionOwnershipError):
            writer(store)

        assert connection.in_transaction
        assert _sentinel_count(connection) == 1
        assert _row_counts(connection) == before
        connection.execute(owner_action)  # owner's transaction is still usable
        assert not connection.in_transaction
        assert _sentinel_count(connection) == (1 if owner_action == "COMMIT" else 0)
        assert _row_counts(connection) == before


def test_idempotency_replay_is_also_refused_inside_external_transaction() -> None:
    with _ready_store() as store:
        connection = store.raw_connection_for_tests()
        _w_idempotent(store)  # first apply, own transaction
        before = _row_counts(connection)
        _open_external(connection)
        with pytest.raises(TransactionOwnershipError):
            _w_idempotent(store)  # would be ALREADY_APPLIED when idle
        assert connection.in_transaction
        assert _sentinel_count(connection) == 1
        connection.execute("ROLLBACK")
        assert _row_counts(connection) == before
        # Idle replay still works and reports ALREADY_APPLIED.
        assert _w_idempotent(store).status.name == "ALREADY_APPLIED"  # type: ignore[attr-defined]


def test_redaction_replay_is_also_refused_inside_external_transaction() -> None:
    with _ready_store() as store:
        connection = store.raw_connection_for_tests()
        _prepare_redact(store)
        _w_redact(store)
        before = _row_counts(connection)
        _open_external(connection)
        with pytest.raises(TransactionOwnershipError):
            _w_redact(store)  # would be ALREADY_REDACTED when idle
        assert connection.in_transaction
        assert _sentinel_count(connection) == 1
        connection.execute("ROLLBACK")
        assert _row_counts(connection) == before
        assert _w_redact(store).status.name == "ALREADY_REDACTED"  # type: ignore[attr-defined]


@pytest.mark.parametrize("writer, prepare", WRITERS)
def test_writer_succeeds_after_external_transaction_is_finished(
    writer: Writer,
    prepare: Callable[[SQLiteEventPayloadStore], None] | None,
) -> None:
    with _ready_store() as store:
        if prepare:
            prepare(store)
        connection = store.raw_connection_for_tests()
        _open_external(connection)
        with pytest.raises(TransactionOwnershipError):
            writer(store)
        connection.execute("COMMIT")
        writer(store)
        assert not connection.in_transaction


# T03 -------------------------------------------------------------------------

def _schema_snapshot(connection: sqlite3.Connection) -> list[tuple[object, ...]]:
    return connection.execute(
        "SELECT type, name, sql FROM sqlite_master ORDER BY type, name"
    ).fetchall()


def test_initialize_schema_refuses_external_transaction_on_fresh_database() -> None:
    connection = sqlite3.connect(":memory:", isolation_level=None)
    store = SQLiteEventPayloadStore(connection)
    _open_external(connection)
    snapshot = _schema_snapshot(connection)

    with pytest.raises(TransactionOwnershipError) as captured:
        store.initialize_schema()

    assert captured.value.operation == "initialize_schema"
    assert connection.in_transaction  # not implicitly committed
    assert _schema_snapshot(connection) == snapshot  # no DDL ran
    connection.execute("ROLLBACK")  # owner can still discard its work
    assert _sentinel_count(connection) == 0
    store.close()


def _make_legacy(database: Path, version: int) -> None:
    with SQLiteEventPayloadStore.connect(database) as store:
        store.initialize_schema()
    connection = sqlite3.connect(database, isolation_level=None)
    if version <= 3:
        connection.execute("DROP TABLE redactions")
    if version <= 2:
        connection.execute("DROP TABLE stream_meta")
    if version <= 1:
        connection.execute("DROP TABLE idempotency_records")
    connection.execute(
        "UPDATE p0_schema_meta SET schema_version = ? WHERE singleton = 1",
        (version,),
    )
    connection.close()


# T03 / T07 -------------------------------------------------------------------

@pytest.mark.parametrize("version", [1, 2, 3])
def test_migration_refused_in_external_transaction_then_succeeds_when_idle(
    tmp_path: Path, version: int
) -> None:
    database = tmp_path / f"legacy-v{version}.sqlite3"
    _make_legacy(database, version)
    with SQLiteEventPayloadStore.connect(database) as store:
        connection = store.raw_connection_for_tests()
        _open_external(connection)
        snapshot = _schema_snapshot(connection)

        with pytest.raises(TransactionOwnershipError):
            store.initialize_schema()

        assert connection.in_transaction
        assert _schema_snapshot(connection) == snapshot
        assert (
            connection.execute("SELECT schema_version FROM p0_schema_meta").fetchone()[0]
            == version
        )
        connection.execute("ROLLBACK")
        assert _sentinel_count(connection) == 0

        store.initialize_schema()  # idle: each supported transition completes
        assert (
            connection.execute("SELECT schema_version FROM p0_schema_meta").fetchone()[0]
            == SCHEMA_VERSION
        )


def test_populated_v2_migration_refused_in_external_transaction(tmp_path: Path) -> None:
    database = tmp_path / "populated-v2.sqlite3"
    with SQLiteEventPayloadStore.connect(database) as store:
        store.initialize_schema()
        append_valid_stream(store, 2)
    _downgrade_database_to_v2(database, tamper=False)
    with SQLiteEventPayloadStore.connect(database) as store:
        connection = store.raw_connection_for_tests()
        _open_external(connection)
        with pytest.raises(TransactionOwnershipError):
            store.initialize_schema(
                migration_registry=integrity_registry(),
                migration_budget=verification_budget(),
            )
        assert connection.in_transaction
        connection.execute("ROLLBACK")
        assert (
            connection.execute("SELECT schema_version FROM p0_schema_meta").fetchone()[0]
            == 2
        )


def test_corrupted_legacy_ledger_still_fails_closed_when_idle(tmp_path: Path) -> None:
    database = tmp_path / "corrupted-v2.sqlite3"
    with SQLiteEventPayloadStore.connect(database) as store:
        store.initialize_schema()
        append_valid_stream(store, 1)
    _downgrade_database_to_v2(database, tamper=True)
    with SQLiteEventPayloadStore.connect(database) as store:
        connection = store.raw_connection_for_tests()
        with pytest.raises(StorageError, match="event hash mismatch"):
            store.initialize_schema(
                migration_registry=integrity_registry(),
                migration_budget=verification_budget(),
            )
        assert not connection.in_transaction  # own transaction rolled back
        assert (
            connection.execute("SELECT schema_version FROM p0_schema_meta").fetchone()[0]
            == 2
        )


def test_unsupported_schema_version_is_refused_for_both_causes(tmp_path: Path) -> None:
    database = tmp_path / "future.sqlite3"
    with SQLiteEventPayloadStore.connect(database) as store:
        store.initialize_schema()
        connection = store.raw_connection_for_tests()
        connection.execute("UPDATE p0_schema_meta SET schema_version = 99")
        with pytest.raises(StorageError, match="unsupported"):
            store.initialize_schema()
        _open_external(connection)
        with pytest.raises(TransactionOwnershipError):
            store.initialize_schema()
        assert connection.in_transaction
        connection.execute("ROLLBACK")


# T04 -------------------------------------------------------------------------

def _fail_trigger(connection: sqlite3.Connection, table: str, when: str = "1") -> None:
    connection.execute(
        f"""
        CREATE TRIGGER fail_{table} BEFORE INSERT ON {table}
        WHEN {when}
        BEGIN SELECT RAISE(ABORT, 'forced failure'); END
        """
    )


@pytest.mark.parametrize(
    "writer, prepare, table, when",
    [
        pytest.param(_w_append_one, None, "stream_meta", "1", id="append_one"),
        pytest.param(
            _w_atomic, None, "events", "NEW.event_id = 'EVT-3'", id="atomic_batch"
        ),
        pytest.param(
            _w_idempotent, None, "idempotency_records", "1", id="idempotent"
        ),
        pytest.param(_w_redact, _prepare_redact, "redactions", "1", id="redact"),
    ],
)
def test_failure_after_own_begin_rolls_back_only_own_work(
    writer: Writer,
    prepare: Callable[[SQLiteEventPayloadStore], None] | None,
    table: str,
    when: str,
) -> None:
    with _ready_store() as store:
        if prepare:
            prepare(store)
        connection = store.raw_connection_for_tests()
        before = _row_counts(connection)
        _fail_trigger(connection, table, when)

        with pytest.raises(sqlite3.IntegrityError, match="forced failure"):
            writer(store)

        assert not connection.in_transaction  # own transaction was completed
        assert _row_counts(connection) == before  # no partial events/payloads/
        # stream metadata/idempotency/redaction records survive


def test_failure_in_one_writer_does_not_poison_the_next_idle_call() -> None:
    with _ready_store() as store:
        connection = store.raw_connection_for_tests()
        _fail_trigger(connection, "stream_meta")
        with pytest.raises(sqlite3.IntegrityError):
            _w_append_one(store)
        connection.execute("DROP TRIGGER fail_stream_meta")
        _w_append_one(store)
        assert _row_counts(connection)["events"] == 1


# Connection semantics (Python 3.13 transaction-control modes) -------------------

def test_legacy_default_isolation_level_idle_works_and_implicit_begin_is_foreign() -> None:
    connection = sqlite3.connect(":memory:")  # isolation_level == "" (legacy implicit BEGIN)
    store = SQLiteEventPayloadStore(connection)
    store.initialize_schema()
    connection.execute("CREATE TABLE sentinel(x)")
    connection.commit()
    _w_append_one(store)  # idle: allowed
    assert not connection.in_transaction

    connection.execute("INSERT INTO sentinel VALUES (1)")  # driver opens BEGIN implicitly
    assert connection.in_transaction
    with pytest.raises(TransactionOwnershipError):
        _w_append_one(store)
    assert connection.in_transaction
    connection.rollback()
    assert _sentinel_count(connection) == 0
    store.close()


def test_autocommit_false_connection_is_always_foreign_and_fails_closed() -> None:
    connection = sqlite3.connect(":memory:", autocommit=False)
    store = SQLiteEventPayloadStore(connection)
    with pytest.raises(TransactionOwnershipError):
        store.initialize_schema()
    assert connection.in_transaction
    store.close()


def test_autocommit_true_connection_behaves_like_idle_connection() -> None:
    connection = sqlite3.connect(":memory:", autocommit=True)
    store = SQLiteEventPayloadStore(connection)
    store.initialize_schema()
    _w_append_one(store)
    assert not connection.in_transaction
    store.close()


# COMMIT-failure handling (follow-up) ---------------------------------------------

def _deny(*, commit: bool = False, rollback: bool = False, begin: bool = False,
          seen: list[str] | None = None) -> Callable[..., int]:
    denied = {
        name
        for name, flag in (("COMMIT", commit), ("ROLLBACK", rollback), ("BEGIN", begin))
        if flag
    }

    def authorizer(action: int, arg1: object, *_: object) -> int:
        if action == sqlite3.SQLITE_TRANSACTION:
            if seen is not None:
                seen.append(str(arg1))
            if arg1 in denied:
                return sqlite3.SQLITE_DENY
        return sqlite3.SQLITE_OK

    return authorizer


def _arm_deferred_fk_failure(connection: sqlite3.Connection) -> None:
    """Every events insert also writes a child row whose FK only fails at COMMIT."""

    connection.execute("CREATE TABLE fk_parent(id INTEGER PRIMARY KEY)")
    connection.execute(
        "CREATE TABLE fk_child(parent_id INTEGER REFERENCES fk_parent(id) "
        "DEFERRABLE INITIALLY DEFERRED)"
    )
    connection.execute(
        "CREATE TRIGGER fk_probe AFTER INSERT ON events "
        "BEGIN INSERT INTO fk_child VALUES (424242); END"
    )


def _disarm_deferred_fk_failure(connection: sqlite3.Connection) -> None:
    connection.execute("DROP TRIGGER fk_probe")


@pytest.mark.parametrize("writer, prepare", WRITERS)
def test_commit_denied_by_authorizer_rolls_back_own_transaction(
    writer: Writer,
    prepare: Callable[[SQLiteEventPayloadStore], None] | None,
) -> None:
    with _ready_store() as store:
        if prepare:
            prepare(store)
        connection = store.raw_connection_for_tests()
        before = _row_counts(connection)
        connection.set_authorizer(_deny(commit=True))

        with pytest.raises(sqlite3.DatabaseError, match="not authorized"):
            writer(store)

        assert not connection.in_transaction  # own transaction was ended
        connection.set_authorizer(None)
        assert _row_counts(connection) == before  # nothing partially persisted
        writer(store)  # connection is immediately reusable
        assert not connection.in_transaction


@pytest.mark.parametrize("writer, prepare", WRITERS)
def test_deferred_foreign_key_failure_at_commit_rolls_back_own_transaction(
    writer: Writer,
    prepare: Callable[[SQLiteEventPayloadStore], None] | None,
) -> None:
    with _ready_store() as store:
        if prepare:
            prepare(store)
        connection = store.raw_connection_for_tests()
        before = _row_counts(connection)
        _arm_deferred_fk_failure(connection)

        with pytest.raises(sqlite3.IntegrityError, match="FOREIGN KEY"):
            writer(store)

        assert not connection.in_transaction
        assert _row_counts(connection) == before
        assert connection.execute("SELECT COUNT(*) FROM fk_child").fetchone()[0] == 0
        _disarm_deferred_fk_failure(connection)
        writer(store)
        assert not connection.in_transaction


def test_commit_failure_does_not_touch_a_foreign_transaction() -> None:
    with _ready_store() as store:
        connection = store.raw_connection_for_tests()
        connection.set_authorizer(_deny(commit=True))
        _open_external(connection)
        with pytest.raises(TransactionOwnershipError):
            _w_append_one(store)
        connection.set_authorizer(None)
        assert connection.in_transaction
        assert _sentinel_count(connection) == 1
        connection.execute("ROLLBACK")


def test_failed_rollback_never_masks_commit_error_and_is_reported_unconfirmed() -> None:
    from mentaury.storage.concurrency import commit_with_retry

    with _ready_store() as store:
        connection = store.raw_connection_for_tests()
        connection.execute("BEGIN IMMEDIATE")
        connection.execute("INSERT INTO sentinel VALUES (1)")
        connection.set_authorizer(_deny(commit=True, rollback=True))

        with pytest.raises(sqlite3.DatabaseError) as captured:
            commit_with_retry(connection)

        assert "not authorized" in str(captured.value)  # original error preserved
        notes = " ".join(getattr(captured.value, "__notes__", []))
        assert "rollback" in notes and "unconfirmed" in notes
        assert connection.in_transaction  # honestly reported, not faked
        connection.set_authorizer(None)
        connection.execute("ROLLBACK")


def test_confirmed_rollback_after_commit_error_adds_no_unconfirmed_note() -> None:
    from mentaury.storage.concurrency import commit_with_retry

    with _ready_store() as store:
        connection = store.raw_connection_for_tests()
        connection.execute("BEGIN IMMEDIATE")
        connection.set_authorizer(_deny(commit=True))
        with pytest.raises(sqlite3.DatabaseError) as captured:
            commit_with_retry(connection)
        assert not getattr(captured.value, "__notes__", [])
        assert not connection.in_transaction


def test_failed_begin_is_never_followed_by_a_rollback() -> None:
    seen: list[str] = []
    with _ready_store() as store:
        connection = store.raw_connection_for_tests()
        connection.set_authorizer(_deny(begin=True, seen=seen))
        with pytest.raises(sqlite3.DatabaseError, match="not authorized"):
            begin_immediate(connection)
        assert "ROLLBACK" not in seen  # no ownership was ever established
        assert "BEGIN" in seen
        connection.set_authorizer(None)
