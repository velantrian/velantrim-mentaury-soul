from __future__ import annotations

from pathlib import Path


def replace_once(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{path}: expected one marker, found {count}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


idempotency = Path("src/mentaury/storage/idempotency.py")
text = idempotency.read_text(encoding="utf-8")

marker = "\n\n@dataclass(frozen=True, slots=True)\nclass IdempotentBatchRequest:"
if text.count(marker) != 1:
    raise RuntimeError("idempotency request marker not found exactly once")
text = text.replace(
    marker,
    '''

class IdempotencyReceiptIntegrityError(RuntimeError):
    "Raised when a stored ALREADY_APPLIED receipt is not ledger-backed."

    def __init__(self, idempotency_key: str, detail: str) -> None:
        self.idempotency_key = idempotency_key
        self.detail = detail
        super().__init__(
            f"invalid stored idempotency receipt for key "
            f"{idempotency_key}: {detail}"
        )


@dataclass(frozen=True, slots=True)
class IdempotentBatchRequest:''',
    1,
)

old_replay = '''                receipt = _receipt_from_row(existing)
                commit_with_retry(connection, self._busy_policy)
'''
new_replay = '''                receipt = _receipt_from_row(
                    existing,
                    request.command.idempotency_key,
                )
                _verify_stored_receipt(
                    connection,
                    receipt,
                    request.command.idempotency_key,
                )
                commit_with_retry(connection, self._busy_policy)
'''
if text.count(old_replay) != 1:
    raise RuntimeError("existing-receipt replay marker not found exactly once")
text = text.replace(old_replay, new_replay, 1)

tail_marker = "def _receipt_from_row(row: sqlite3.Row) -> BatchAppendReceipt:\n"
prefix, separator, _ = text.partition(tail_marker)
if not separator:
    raise RuntimeError("receipt helper marker not found")

new_tail = r'''def _receipt_from_row(
    row: sqlite3.Row,
    idempotency_key: str,
) -> BatchAppendReceipt:
    try:
        encoded_event_ids = bytes(row["event_ids_json"])
        decoded_event_ids = json.loads(encoded_event_ids.decode("utf-8"))
    except (TypeError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise IdempotencyReceiptIntegrityError(
            idempotency_key,
            "event_ids_json is not valid UTF-8 JSON",
        ) from exc

    if not isinstance(decoded_event_ids, list) or not decoded_event_ids:
        raise IdempotencyReceiptIntegrityError(
            idempotency_key,
            "event_ids_json must be a non-empty list",
        )
    if any(
        not isinstance(event_id, str) or not event_id
        for event_id in decoded_event_ids
    ):
        raise IdempotencyReceiptIntegrityError(
            idempotency_key,
            "event_ids_json must contain non-empty strings",
        )
    if len(set(decoded_event_ids)) != len(decoded_event_ids):
        raise IdempotencyReceiptIntegrityError(
            idempotency_key,
            "event_ids_json must not contain duplicate event IDs",
        )
    if canonical_json_bytes(decoded_event_ids) != encoded_event_ids:
        raise IdempotencyReceiptIntegrityError(
            idempotency_key,
            "event_ids_json must use canonical JSON encoding",
        )

    batch_id = row["batch_id"]
    stream_id = row["stream_id"]
    first_stream_version = row["first_stream_version"]
    last_stream_version = row["last_stream_version"]
    if not isinstance(batch_id, str) or not batch_id:
        raise IdempotencyReceiptIntegrityError(
            idempotency_key,
            "batch_id must be a non-empty string",
        )
    if not isinstance(stream_id, str) or not stream_id:
        raise IdempotencyReceiptIntegrityError(
            idempotency_key,
            "stream_id must be a non-empty string",
        )
    if (
        isinstance(first_stream_version, bool)
        or not isinstance(first_stream_version, int)
        or first_stream_version <= 0
    ):
        raise IdempotencyReceiptIntegrityError(
            idempotency_key,
            "first_stream_version must be a positive integer",
        )
    if (
        isinstance(last_stream_version, bool)
        or not isinstance(last_stream_version, int)
        or last_stream_version < first_stream_version
    ):
        raise IdempotencyReceiptIntegrityError(
            idempotency_key,
            "last_stream_version must not precede first_stream_version",
        )

    receipt = BatchAppendReceipt(
        batch_id=batch_id,
        stream_id=stream_id,
        event_ids=tuple(decoded_event_ids),
        first_stream_version=first_stream_version,
        last_stream_version=last_stream_version,
    )
    expected_count = (
        receipt.last_stream_version - receipt.first_stream_version + 1
    )
    if len(receipt.event_ids) != expected_count:
        raise IdempotencyReceiptIntegrityError(
            idempotency_key,
            "event ID count does not match the stored version span",
        )
    return receipt


def _verify_stored_receipt(
    connection: sqlite3.Connection,
    receipt: BatchAppendReceipt,
    idempotency_key: str,
) -> None:
    for offset, event_id in enumerate(receipt.event_ids):
        row = connection.execute(
            "SELECT event_id, batch_id, stream_id, stream_version "
            "FROM events WHERE event_id = ?",
            (event_id,),
        ).fetchone()
        if row is None:
            raise IdempotencyReceiptIntegrityError(
                idempotency_key,
                f"referenced event {event_id} does not exist",
            )

        expected_version = receipt.first_stream_version + offset
        if row["batch_id"] != receipt.batch_id:
            raise IdempotencyReceiptIntegrityError(
                idempotency_key,
                f"event {event_id} batch_id does not match the stored receipt",
            )
        if row["stream_id"] != receipt.stream_id:
            raise IdempotencyReceiptIntegrityError(
                idempotency_key,
                f"event {event_id} stream_id does not match the stored receipt",
            )
        if row["stream_version"] != expected_version:
            raise IdempotencyReceiptIntegrityError(
                idempotency_key,
                f"event {event_id} stream_version does not match receipt order",
            )
'''
idempotency.write_text(prefix + new_tail, encoding="utf-8")

storage_init = Path("src/mentaury/storage/__init__.py")
replace_once(
    storage_init,
    '''    IdempotencyConflictError,
    IdempotencyInvariantError,
''',
    '''    IdempotencyConflictError,
    IdempotencyInvariantError,
    IdempotencyReceiptIntegrityError,
''',
)
replace_once(
    storage_init,
    '''    "IdempotencyConflictError",
    "IdempotencyInvariantError",
''',
    '''    "IdempotencyConflictError",
    "IdempotencyInvariantError",
    "IdempotencyReceiptIntegrityError",
''',
)
