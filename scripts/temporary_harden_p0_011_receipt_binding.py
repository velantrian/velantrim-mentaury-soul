from __future__ import annotations

from pathlib import Path


def replace_once(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{path}: expected one marker, found {count}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


path = Path("src/mentaury/storage/idempotency.py")
replace_once(
    path,
    'from .sqlite_store import SQLiteEventPayloadStore\n',
    'from .sealing import compute_payload_digest\nfrom .sqlite_store import SQLiteEventPayloadStore\n',
)
replace_once(
    path,
    '''class IdempotencyReceiptIntegrityError(RuntimeError):
    "Raised when a stored ALREADY_APPLIED receipt is not ledger-backed."
''',
    '''class IdempotencyReceiptIntegrityError(RuntimeError):
    """Raised when a stored ALREADY_APPLIED receipt is not ledger-backed."""
''',
)
replace_once(
    path,
    '''                _verify_stored_receipt(
                    connection,
                    receipt,
                    request.command.idempotency_key,
                )
''',
    '''                _verify_stored_receipt(
                    connection,
                    receipt,
                    request,
                )
''',
)
old_function = '''def _verify_stored_receipt(
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
new_function = '''def _verify_stored_receipt(
    connection: sqlite3.Connection,
    receipt: BatchAppendReceipt,
    request: IdempotentBatchRequest,
) -> None:
    idempotency_key = request.command.idempotency_key
    expected_first_version = request.command.expected_stream_version + 1
    if receipt.stream_id != request.command.target_stream:
        raise IdempotencyReceiptIntegrityError(
            idempotency_key,
            "stored stream_id does not match command target_stream",
        )
    if receipt.first_stream_version != expected_first_version:
        raise IdempotencyReceiptIntegrityError(
            idempotency_key,
            "stored first_stream_version does not follow the command expectation",
        )
    if len(receipt.event_ids) != len(request.pending_events):
        raise IdempotencyReceiptIntegrityError(
            idempotency_key,
            "stored event count does not match the fingerprinted pending batch",
        )

    expected_batch_size = len(receipt.event_ids)
    for offset, (event_id, proposed) in enumerate(
        zip(receipt.event_ids, request.pending_events, strict=True)
    ):
        row = connection.execute(
            """
            SELECT event_id, batch_id, batch_index, batch_size,
                   stream_id, stream_version, event_type, payload_schema,
                   affects_domain_state, payload_digest,
                   initiator_type, initiator_id,
                   capability_lease_id, capability_revision
            FROM events
            WHERE event_id = ?
            """,
            (event_id,),
        ).fetchone()
        if row is None:
            raise IdempotencyReceiptIntegrityError(
                idempotency_key,
                f"referenced event {event_id} does not exist",
            )

        expected_version = receipt.first_stream_version + offset
        checks = (
            (row["batch_id"] == receipt.batch_id, "batch_id"),
            (row["batch_index"] == offset, "batch_index"),
            (row["batch_size"] == expected_batch_size, "batch_size"),
            (row["stream_id"] == receipt.stream_id, "stream_id"),
            (row["stream_version"] == expected_version, "stream_version"),
            (row["event_type"] == proposed.event_type, "event_type"),
            (row["payload_schema"] == proposed.payload_schema, "payload_schema"),
            (
                bool(row["affects_domain_state"])
                is proposed.affects_domain_state,
                "affects_domain_state",
            ),
            (
                row["payload_digest"]
                == compute_payload_digest(canonical_json_bytes(proposed.payload)),
                "payload_digest",
            ),
            (
                row["initiator_type"] == request.command.issuer.type
                and row["initiator_id"] == request.command.issuer.id,
                "initiator",
            ),
            (
                row["capability_lease_id"]
                == request.command.authority.capability_lease_id
                and row["capability_revision"]
                == request.command.authority.capability_revision,
                "authority",
            ),
        )
        for matches, field in checks:
            if not matches:
                raise IdempotencyReceiptIntegrityError(
                    idempotency_key,
                    f"event {event_id} {field} does not match the fingerprinted request",
                )
'''
replace_once(path, old_function, new_function)

tests = Path("tests/test_adversarial_integrity_suite.py")
append = '''


def test_stored_receipt_cannot_redirect_to_another_stream() -> None:
    with SQLiteEventPayloadStore.in_memory() as store:
        store.initialize_schema()
        appender = SQLiteIdempotentBatchAppender(store, _registry())
        request = _idempotent_request()
        appender.append(request)
        _corrupt_idempotency_record(store, "stream_id = 'other:stream'")

        with pytest.raises(
            IdempotencyReceiptIntegrityError,
            match="target_stream",
        ):
            appender.append(request)


def test_stored_receipt_must_start_after_expected_version() -> None:
    with SQLiteEventPayloadStore.in_memory() as store:
        store.initialize_schema()
        appender = SQLiteIdempotentBatchAppender(store, _registry())
        request = _idempotent_request()
        appender.append(request)
        _corrupt_idempotency_record(
            store,
            "first_stream_version = 2, last_stream_version = 3",
        )

        with pytest.raises(
            IdempotencyReceiptIntegrityError,
            match="command expectation",
        ):
            appender.append(request)


def test_stored_receipt_verifies_full_batch_shape() -> None:
    with SQLiteEventPayloadStore.in_memory() as store:
        store.initialize_schema()
        appender = SQLiteIdempotentBatchAppender(store, _registry())
        request = _idempotent_request()
        appender.append(request)
        connection = store.raw_connection_for_tests()
        connection.execute("DROP TRIGGER events_are_immutable_on_update")
        connection.execute(
            "UPDATE events SET batch_size = 3 WHERE event_id = 'IDEMP-EVT-1'"
        )

        with pytest.raises(
            IdempotencyReceiptIntegrityError,
            match="batch_size",
        ):
            appender.append(request)


def test_stored_receipt_verifies_fingerprinted_event_semantics() -> None:
    with SQLiteEventPayloadStore.in_memory() as store:
        store.initialize_schema()
        appender = SQLiteIdempotentBatchAppender(store, _registry())
        request = _idempotent_request()
        appender.append(request)
        connection = store.raw_connection_for_tests()
        connection.execute("DROP TRIGGER events_are_immutable_on_update")
        connection.execute(
            "UPDATE events SET payload_digest = 'sha256:forged' "
            "WHERE event_id = 'IDEMP-EVT-1'"
        )

        with pytest.raises(
            IdempotencyReceiptIntegrityError,
            match="payload_digest",
        ):
            appender.append(request)
'''
text = tests.read_text(encoding="utf-8")
if "test_stored_receipt_cannot_redirect_to_another_stream" in text:
    raise RuntimeError("request-binding tests already present")
tests.write_text(text + append, encoding="utf-8")


doc = Path("docs/P0_011_ADVERSARIAL_INTEGRITY_SUITE.md")
replace_once(
    doc,
    '''each referenced event
├── exists
├── batch_id matches
├── stream_id matches
└── stream_version matches receipt order
''',
    '''receipt ↔ fingerprinted request
├── stream matches command target
├── first version follows expected version
└── event count matches pending batch

each referenced event
├── exists
├── batch ID, index and size match
├── stream and version order match
├── type, schema and state-affecting flag match
├── payload digest matches canonical proposed payload
└── initiator and authority match the command
''',
)
