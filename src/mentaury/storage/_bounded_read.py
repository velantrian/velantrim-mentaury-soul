"""Internal bounded read primitives for stored payload material (Stage 04D).

The pattern is *probe, admit, then load*. A probe asks SQLite for the record's
existence, ``typeof(payload_bytes)`` and ``length(payload_bytes)`` and returns
three scalars, never the BLOB. The caller's budget decides on the measured size;
only an admitted record is then fetched, and the fetched size must equal the
measured one. This bounds how much payload material Python materializes; it
makes no claim about SQLite's own page reads or the process's total memory.

Probe and fetch must observe one version of the data: callers run inside an
existing read snapshot (R0/R1), an existing write transaction (migration), or
``consistent_read`` (public bounded load). Nothing here opens, commits or rolls
back a transaction it does not own.
"""

from __future__ import annotations

import sqlite3
from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import dataclass

from .budget import VerificationBudget
from .concurrency import rollback_after_failure


class PayloadStorageError(RuntimeError):
    """Base for controlled stored-payload read failures (never carries content)."""


class PayloadStorageTypeError(PayloadStorageError):
    """The stored value is not a BLOB, so it is never converted to bytes."""

    def __init__(self, stored_type: str) -> None:
        self.stored_type = stored_type
        super().__init__(f"stored payload value has SQLite type {stored_type}, expected blob")


class PayloadChangedError(PayloadStorageError):
    """The fetched payload differs from what the preflight measured."""

    def __init__(self, expected: int, observed: int | None) -> None:
        self.expected = expected
        self.observed = observed
        super().__init__("stored payload changed between the size preflight and the load")


@dataclass(frozen=True, slots=True)
class LoadedPayload:
    payload_bytes: bytes
    size: int


@contextmanager
def consistent_read(connection: sqlite3.Connection) -> Iterator[None]:
    """One read snapshot for probe + fetch without touching a caller's work.

    A connection already inside a caller-owned transaction is used as is (that
    transaction is the snapshot and is never committed or rolled back here);
    otherwise a savepoint opens and releases this call's own snapshot.
    """

    if connection.in_transaction:
        yield
        return
    connection.execute("SAVEPOINT mentaury_bounded_read")
    try:
        yield
        connection.execute("RELEASE mentaury_bounded_read")
    except BaseException as exc:
        rollback_after_failure(connection, exc)
        raise


def payload_exists(connection: sqlite3.Connection, payload_ref: str) -> bool:
    """Existence only: no payload content (not even its size) is read."""

    return (
        connection.execute(
            "SELECT 1 FROM event_payloads WHERE payload_ref = ?", (payload_ref,)
        ).fetchone()
        is not None
    )


def probe_payload(connection: sqlite3.Connection, payload_ref: str) -> int | None:
    """Return the stored BLOB size, ``None`` if absent; refuse non-BLOB values."""

    row = connection.execute(
        "SELECT typeof(payload_bytes), length(payload_bytes) "
        "FROM event_payloads WHERE payload_ref = ?",
        (payload_ref,),
    ).fetchone()
    if row is None:
        return None
    stored_type, size = row[0], row[1]
    if stored_type != "blob":
        raise PayloadStorageTypeError(str(stored_type))
    return int(size)


def fetch_probed(
    connection: sqlite3.Connection,
    payload_ref: str,
    expected_size: int,
) -> bytes:
    """Fetch an already-admitted payload and verify type and size."""

    row = connection.execute(
        "SELECT payload_bytes FROM event_payloads WHERE payload_ref = ?",
        (payload_ref,),
    ).fetchone()
    if row is None:
        raise PayloadChangedError(expected_size, None)
    value = row[0]
    if not isinstance(value, bytes):
        raise PayloadStorageTypeError(type(value).__name__)
    if len(value) != expected_size:
        raise PayloadChangedError(expected_size, len(value))
    return value


def admit_and_load(
    connection: sqlite3.Connection,
    payload_ref: str,
    budget: VerificationBudget,
    total_so_far: int,
    *,
    charge_total: bool = True,
) -> LoadedPayload | None:
    """Probe, admit against ``budget``, then load; ``None`` when absent.

    ``ResourceBudgetExceeded`` is raised *before* any BLOB is fetched: first the
    individual limit, then (when ``charge_total``) ``total_so_far + size`` against
    the aggregate limit. ``charge_total=False`` is for a payload that is checked
    on its own but accounted elsewhere (the redaction audit payload, which the
    logical total counts once, when it is verified as an event).
    """

    size = probe_payload(connection, payload_ref)
    if size is None:
        return None
    budget.require_payload_size(size)
    if charge_total:
        budget.require_total_payload_size(total_so_far + size)
    return LoadedPayload(fetch_probed(connection, payload_ref, size), size)
