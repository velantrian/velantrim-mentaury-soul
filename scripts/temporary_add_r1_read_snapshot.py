from __future__ import annotations

from pathlib import Path


def replace_once(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{path}: expected one marker, found {count}: {old!r}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


engine = Path("src/mentaury/replay/engine.py")
text = engine.read_text(encoding="utf-8")
text = text.replace(
    "import hashlib\nimport json\n",
    "import hashlib\nimport json\nfrom contextlib import contextmanager\nfrom collections.abc import Iterator\n",
    1,
)
start_marker = '''        reducer_error = _validate_reducer(self._reducer)
'''
end_marker = '''    def _run(
'''
start = text.index(start_marker)
end = text.index(end_marker, start)
body = text[start:end]
indented_body = "".join(
    "    " + line if line.strip() else line
    for line in body.splitlines(keepends=True)
)
replacement = '''        with _sqlite_read_snapshot(self._store):
            return self._verify_stream_in_snapshot(stream_id, snapshot)

    def _verify_stream_in_snapshot(
        self,
        stream_id: str,
        snapshot: ReplaySnapshot,
    ) -> R1ReplayReport:
''' + indented_body
text = text[:start] + replacement + text[end:]
helper_marker = '''
def _require_state_budget(
'''
helper = '''
@contextmanager
def _sqlite_read_snapshot(
    store: SQLiteEventPayloadStore,
) -> Iterator[None]:
    """Hold one SQLite snapshot across R0, capture and replay reads."""

    connection = store._connection
    savepoint = "mentaury_r1_read_snapshot"
    connection.execute(f"SAVEPOINT {savepoint}")
    try:
        yield
    except BaseException:
        connection.execute(f"ROLLBACK TO {savepoint}")
        connection.execute(f"RELEASE {savepoint}")
        raise
    else:
        connection.execute(f"RELEASE {savepoint}")


def _require_state_budget(
'''
if text.count(helper_marker) != 1:
    raise RuntimeError("state-budget helper marker mismatch")
text = text.replace(helper_marker, helper, 1)
engine.write_text(text, encoding="utf-8")


tests = Path("tests/test_r1_replay.py")
test_text = tests.read_text(encoding="utf-8")
test_text = test_text.replace(
    "from collections.abc import Mapping\nfrom dataclasses import replace\n",
    "from collections.abc import Mapping\nfrom dataclasses import replace\nfrom pathlib import Path\n",
    1,
)
append = '''


def test_r1_uses_one_sqlite_read_snapshot_for_concurrent_append(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    database = tmp_path / "r1-read-snapshot.sqlite3"
    with SQLiteEventPayloadStore.connect(database) as setup:
        setup.raw_connection_for_tests().execute("PRAGMA journal_mode = WAL")
        setup.initialize_schema()
        first = _append_counter(setup, "EVT-1", 1, 2)

    with (
        SQLiteEventPayloadStore.connect(database) as reader,
        SQLiteEventPayloadStore.connect(database) as writer,
    ):
        reader.raw_connection_for_tests().execute("PRAGMA journal_mode = WAL")
        writer.raw_connection_for_tests().execute("PRAGMA journal_mode = WAL")
        original_list_stream = reader.list_stream
        calls = 0

        def append_between_r0_count_and_event_capture(stream_id: str):
            nonlocal calls
            calls += 1
            if calls == 1:
                _append_counter(writer, "EVT-2", 2, 5)
            return original_list_stream(stream_id)

        monkeypatch.setattr(
            reader,
            "list_stream",
            append_between_r0_count_and_event_capture,
        )
        report = _verifier(reader).verify_stream(
            STREAM_ID,
            _snapshot_after_first(first),
        )

        assert report.ok
        assert report.verified_through_stream_version == 1
        assert report.verified_through_event_hash == first.event_hash
        assert len(original_list_stream(STREAM_ID)) == 2
'''
if "test_r1_uses_one_sqlite_read_snapshot_for_concurrent_append" in test_text:
    raise RuntimeError("read snapshot test already present")
tests.write_text(test_text + append, encoding="utf-8")


doc = Path("docs/P0_013_R1_DETERMINISTIC_REPLAY.md")
replace_once(
    doc,
    '''2. run bounded R0 verification on the complete stream;
3. capture the same verified event count/tail metadata before replay;
''',
    '''2. open one SQLite read snapshot for all verification reads;
3. run bounded R0 verification on the complete stream inside that snapshot;
4. capture the same verified event count/tail metadata before replay;
''',
)
replace_once(
    doc,
    '''4. verify snapshot reducer, stream, version and event-hash anchor;
5. recompute the snapshot state hash and apply state-size bounds;
6. replay the complete stream from a canonical bounded initial state;
7. recheck each replayed payload digest against its immutable envelope;
8. compare the supplied snapshot state with the full-replay checkpoint state;
9. replay the tail from the supplied snapshot;
10. compare canonical final bytes and state hashes.
''',
    '''5. verify snapshot reducer, stream, version and event-hash anchor;
6. recompute the snapshot state hash and apply state-size bounds;
7. replay the complete stream from a canonical bounded initial state;
8. recheck each replayed payload digest against its immutable envelope;
9. compare the supplied snapshot state with the full-replay checkpoint state;
10. replay the tail from the supplied snapshot;
11. compare canonical final bytes and state hashes.
''',
)
replace_once(
    doc,
    '''The P0-013 suite contains **21 replay tests** covering:
''',
    '''The P0-013 suite contains **22 replay tests** covering:
''',
)
replace_once(
    doc,
    '''- stream-stability capture after R0;
''',
    '''- one SQLite read snapshot across R0, event capture and payload replay;
- concurrent append semantics with an explicitly reported verified prefix;
- stream-stability capture after R0;
''',
)
replace_once(
    doc,
    '''A successful report records the exact captured stream version and tail event
hash so callers do not confuse a verified immutable prefix with an open-ended
claim about future appends.
''',
    '''All R0, event, metadata and payload reads occur under one SQLite read snapshot.
A concurrent append after that snapshot may complete in WAL mode, but it is not
silently included. A successful report records the exact captured stream version
and tail event hash so callers do not confuse a verified immutable prefix with an
open-ended claim about future appends.
''',
)
