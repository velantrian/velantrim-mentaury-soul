from __future__ import annotations

from pathlib import Path


def replace_once(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{path}: expected one marker, found {count}: {old!r}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


contracts = Path("src/mentaury/replay/contracts.py")
replace_once(
    contracts,
    '''    STREAM_CHANGED_DURING_VERIFICATION = "STREAM_CHANGED_DURING_VERIFICATION"
    REDUCER_ERROR = "REDUCER_ERROR"
''',
    '''    STREAM_CHANGED_DURING_VERIFICATION = "STREAM_CHANGED_DURING_VERIFICATION"
    ACTIVE_TRANSACTION = "ACTIVE_TRANSACTION"
    REDUCER_ERROR = "REDUCER_ERROR"
''',
)

engine = Path("src/mentaury/replay/engine.py")
text = engine.read_text(encoding="utf-8")
text = text.replace(
    '''from contextlib import contextmanager
from collections.abc import Iterator
from collections.abc import Mapping
''',
    '''from collections.abc import Iterator, Mapping
from contextlib import contextmanager
''',
    1,
)
old_wrapper = '''        if not isinstance(snapshot, ReplaySnapshot):
            raise TypeError("snapshot must be a ReplaySnapshot")

        with _sqlite_read_snapshot(self._store):
            return self._verify_stream_in_snapshot(stream_id, snapshot)
'''
new_wrapper = '''        if not isinstance(snapshot, ReplaySnapshot):
            raise TypeError("snapshot must be a ReplaySnapshot")
        if self._store._connection.in_transaction:
            reducer_id = getattr(self._reducer, "reducer_id", "<invalid>")
            reducer_version = getattr(
                self._reducer,
                "reducer_version",
                "<invalid>",
            )
            return self._failed_report(
                stream_id,
                str(reducer_id),
                str(reducer_version),
                snapshot.through_stream_version,
                ReplayFailure(
                    ReplayFailureCode.ACTIVE_TRANSACTION,
                    stream_id,
                    "R1 verification requires an autocommit connection; "
                    "uncommitted state cannot be certified",
                ),
            )

        with _sqlite_read_snapshot(self._store):
            return self._verify_stream_in_snapshot(stream_id, snapshot)
'''
if text.count(old_wrapper) != 1:
    raise RuntimeError("verify wrapper marker mismatch")
text = text.replace(old_wrapper, new_wrapper, 1)

method_start = text.index("    def _verify_stream_in_snapshot(\n")
body_start = text.index("        reducer_error =", method_start)
method_end = text.index("    def _run(\n", body_start)
body = text[body_start:method_end]
lines = body.splitlines(keepends=True)
for line in lines:
    if line.strip() and not line.startswith("            "):
        raise RuntimeError(f"unexpected private-method indentation: {line!r}")
normalized = "".join(
    line[4:] if line.strip() else line
    for line in lines
)
text = text[:body_start] + normalized + text[method_end:]
engine.write_text(text, encoding="utf-8")


tests = Path("tests/test_r1_replay.py")
test_text = tests.read_text(encoding="utf-8")
append = '''


def test_r1_refuses_uncommitted_connection_state() -> None:
    with SQLiteEventPayloadStore.in_memory() as store:
        store.initialize_schema()
        snapshot = make_replay_snapshot(
            reducer_id=CounterReducer.reducer_id,
            reducer_version=CounterReducer.reducer_version,
            stream_id=STREAM_ID,
            through_stream_version=0,
            through_event_hash=GENESIS_HASH,
            state={"total": 0, "event_ids": []},
        )
        connection = store.raw_connection_for_tests()
        connection.execute("BEGIN IMMEDIATE")
        try:
            report = _verifier(store).verify_stream(STREAM_ID, snapshot)
        finally:
            connection.execute("ROLLBACK")

        assert _failure_code(report) is ReplayFailureCode.ACTIVE_TRANSACTION
'''
if "test_r1_refuses_uncommitted_connection_state" in test_text:
    raise RuntimeError("active transaction test already present")
tests.write_text(test_text + append, encoding="utf-8")


doc = Path("docs/P0_013_R1_DETERMINISTIC_REPLAY.md")
replace_once(
    doc,
    '''The P0-013 suite contains **22 replay tests** covering:
''',
    '''The P0-013 suite contains **23 replay tests** covering:
''',
)
replace_once(
    doc,
    '''- concurrent append semantics with an explicitly reported verified prefix;
''',
    '''- concurrent append semantics with an explicitly reported verified prefix;
- refusal to certify an outer uncommitted transaction;
''',
)
replace_once(
    doc,
    '''All R0, event, metadata and payload reads occur under one SQLite read snapshot.
''',
    '''R1 refuses to start while the store connection is already inside an outer
transaction: uncommitted state may later roll back and cannot receive a durable
verification report.

All R0, event, metadata and payload reads occur under one SQLite read snapshot.
''',
)
