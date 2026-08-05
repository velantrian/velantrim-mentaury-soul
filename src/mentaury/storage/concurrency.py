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


def begin_immediate(
    connection: sqlite3.Connection,
    policy: BusyRetryPolicy = DEFAULT_BUSY_RETRY_POLICY,
) -> int:
    """Acquire SQLite's reserved write lock using a bounded retry policy."""

    if not isinstance(policy, BusyRetryPolicy):
        raise TypeError("policy must be a BusyRetryPolicy")
    last_error: sqlite3.OperationalError | None = None
    for attempt in range(1, policy.max_attempts + 1):
        try:
            connection.execute("BEGIN IMMEDIATE")
            return attempt
        except sqlite3.OperationalError as exc:
            if not is_busy_error(exc):
                _rollback_if_active(connection)
                raise
            last_error = exc
            _rollback_if_active(connection)
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
    """Complete an active transaction with bounded retries and fail-closed rollback."""

    if not isinstance(policy, BusyRetryPolicy):
        raise TypeError("policy must be a BusyRetryPolicy")
    last_error: sqlite3.OperationalError | None = None
    for attempt in range(1, policy.max_attempts + 1):
        try:
            connection.execute("COMMIT")
            return attempt
        except sqlite3.OperationalError as exc:
            if not is_busy_error(exc):
                _rollback_if_active(connection)
                raise
            last_error = exc
            if attempt < policy.max_attempts and policy.backoff_seconds:
                time.sleep(policy.backoff_seconds)
    assert last_error is not None
    _rollback_if_active(connection)
    raise StoreBusyError(policy.max_attempts, last_error)


def _rollback_if_active(connection: sqlite3.Connection) -> None:
    if connection.in_transaction:
        connection.execute("ROLLBACK")
