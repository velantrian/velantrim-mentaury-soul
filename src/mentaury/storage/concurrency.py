"""P0-008 controlled SQLite write concurrency and busy handling."""

from __future__ import annotations

import sqlite3
import time
from dataclasses import dataclass


class StoreBusyError(RuntimeError):
    """Raised when a bounded write-lock acquisition policy is exhausted."""

    def __init__(self, attempts: int, last_error: sqlite3.OperationalError) -> None:
        self.attempts = attempts
        self.last_error = last_error
        super().__init__(f"STORE_BUSY after {attempts} attempts: {last_error}")


class TransactionOwnershipError(RuntimeError):
    """Raised when a write operation finds a transaction it does not own.

    Public writers require an idle connection. An already-active transaction
    belongs to the caller, so the operation refuses without committing,
    rolling back, or otherwise touching it.
    """

    def __init__(self, operation: str) -> None:
        self.operation = operation
        super().__init__(
            f"TRANSACTION_OWNERSHIP: {operation} requires an idle connection; "
            "an externally owned transaction is active and was left untouched"
        )


class VersionConflictError(RuntimeError):
    """Raised when a stream/version pair was already committed."""

    def __init__(self, stream_id: str, first_stream_version: int) -> None:
        self.stream_id = stream_id
        self.first_stream_version = first_stream_version
        super().__init__(
            f"VERSION_CONFLICT for {stream_id} at version {first_stream_version}"
        )


@dataclass(frozen=True, slots=True)
class BusyRetryPolicy:
    max_attempts: int = 3
    backoff_seconds: float = 0.01

    def __post_init__(self) -> None:
        if isinstance(self.max_attempts, bool) or self.max_attempts < 1:
            raise ValueError("max_attempts must be a positive integer")
        if isinstance(self.backoff_seconds, bool) or not isinstance(
            self.backoff_seconds, (int, float)
        ):
            raise TypeError("backoff_seconds must be numeric")
        if self.backoff_seconds < 0:
            raise ValueError("backoff_seconds must be non-negative")


DEFAULT_BUSY_RETRY_POLICY = BusyRetryPolicy()


def require_idle_connection(
    connection: sqlite3.Connection,
    operation: str,
) -> None:
    """Refuse, without side effects, when the caller already owns a transaction.

    Invariant: an operation may commit or roll back only its own transaction.
    Ownership can be claimed only after a successful ``BEGIN``; therefore any
    transaction visible beforehand is foreign and must not be touched.
    """

    if connection.in_transaction:
        raise TransactionOwnershipError(operation)


def begin_immediate(
    connection: sqlite3.Connection,
    policy: BusyRetryPolicy = DEFAULT_BUSY_RETRY_POLICY,
) -> int:
    """Acquire SQLite's reserved write lock using a bounded retry policy.

    Fails closed with ``TransactionOwnershipError`` before any BEGIN or retry
    when the connection already has an active (externally owned) transaction.
    Rollbacks below only ever undo a transaction this call itself opened.
    """

    if not isinstance(policy, BusyRetryPolicy):
        raise TypeError("policy must be a BusyRetryPolicy")
    require_idle_connection(connection, "begin_immediate")
    last_error: sqlite3.OperationalError | None = None
    for attempt in range(1, policy.max_attempts + 1):
        try:
            connection.execute("BEGIN IMMEDIATE")
            return attempt
        except sqlite3.OperationalError as exc:
            # A failed BEGIN opened nothing, so ownership was never established
            # and there is nothing of ours to roll back.
            if not is_busy_error(exc):
                raise
            last_error = exc
            if attempt < policy.max_attempts and policy.backoff_seconds:
                time.sleep(policy.backoff_seconds)
    assert last_error is not None
    raise StoreBusyError(policy.max_attempts, last_error)


def is_busy_error(error: sqlite3.OperationalError) -> bool:
    code = getattr(error, "sqlite_errorcode", None)
    if code in {sqlite3.SQLITE_BUSY, sqlite3.SQLITE_LOCKED}:
        return True
    message = str(error).lower()
    return "database is locked" in message or "database table is locked" in message


def is_stream_version_conflict(error: sqlite3.IntegrityError) -> bool:
    message = str(error)
    return (
        "events.stream_id, events.stream_version" in message
        or "UNIQUE constraint failed: events.stream_id, events.stream_version" in message
    )


def commit_with_retry(
    connection: sqlite3.Connection,
    policy: BusyRetryPolicy = DEFAULT_BUSY_RETRY_POLICY,
) -> int:
    """Complete the caller's *own* active transaction, fail-closed.

    Must only be called after a successful ``begin_immediate`` by the same
    operation. Busy contention is retried under ``policy``. Any other
    ``sqlite3.Error`` (for example a deferred foreign-key ``IntegrityError`` or
    an authorizer denial) can leave the transaction open, so it is rolled back
    and the original error is re-raised unchanged.
    """

    if not isinstance(policy, BusyRetryPolicy):
        raise TypeError("policy must be a BusyRetryPolicy")
    last_error: sqlite3.OperationalError | None = None
    for attempt in range(1, policy.max_attempts + 1):
        try:
            connection.execute("COMMIT")
            return attempt
        except sqlite3.OperationalError as exc:
            if not is_busy_error(exc):
                rollback_after_failure(connection, exc)
                raise
            last_error = exc
            if attempt < policy.max_attempts and policy.backoff_seconds:
                time.sleep(policy.backoff_seconds)
        except sqlite3.Error as exc:
            rollback_after_failure(connection, exc)
            raise
    assert last_error is not None
    rollback_after_failure(connection, last_error)
    raise StoreBusyError(policy.max_attempts, last_error)


def rollback_after_failure(
    connection: sqlite3.Connection,
    original: BaseException,
) -> None:
    """Roll back our own transaction after ``original`` without masking it.

    A failing ROLLBACK is attached to ``original`` as a note instead of
    replacing it. Success is claimed only if the connection is verifiably idle
    afterwards; otherwise the note says the rollback is unconfirmed.
    """

    if not connection.in_transaction:
        return
    try:
        connection.execute("ROLLBACK")
    except sqlite3.Error as rollback_error:
        original.add_note(f"rollback failed: {rollback_error!r}")
    if connection.in_transaction:
        original.add_note(
            "rollback unconfirmed: connection is still inside a transaction"
        )
