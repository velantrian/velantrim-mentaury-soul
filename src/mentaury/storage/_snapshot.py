"""Private SQLite read-snapshot helper shared by R0 and R1 verification."""

from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager

from .concurrency import require_idle_connection, rollback_after_failure
from .sqlite_store import SQLiteEventPayloadStore

_SNAPSHOT_SAVEPOINT = "mentaury_read_snapshot"


@contextmanager
def sqlite_read_snapshot(
    store: SQLiteEventPayloadStore,
    operation: str,
) -> Iterator[None]:
    """Hold one SQLite read snapshot across every read made inside the block.

    The connection must be idle: the snapshot is the *caller's own* transaction,
    opened here and ended here, so an externally owned transaction is refused
    (``TransactionOwnershipError``) before anything is executed. In WAL mode the
    snapshot is fixed by the first read inside the block, so later concurrent
    commits from other connections are not observed until the block ends.
    The snapshot is released on success, controlled early return and exception.
    """

    connection = store._connection
    require_idle_connection(connection, operation)
    connection.execute(f"SAVEPOINT {_SNAPSHOT_SAVEPOINT}")
    try:
        yield
        connection.execute(f"RELEASE {_SNAPSHOT_SAVEPOINT}")
    except BaseException as exc:
        rollback_after_failure(connection, exc)
        raise
