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
    '''from mentaury.contracts.primitives import (
    FrozenPayload,
    freeze_payload,
    require_non_empty,
    require_non_negative,
)
''',
    '''from mentaury.contracts.primitives import (
    FrozenPayload,
    freeze_payload,
    require_non_empty,
    require_non_negative,
)
from mentaury.storage.budget import ResourceBudgetExceeded
''',
)
replace_once(
    contracts,
    '''

@dataclass(frozen=True, slots=True)
class ReplaySnapshot:
''',
    '''

@dataclass(frozen=True, slots=True)
class ReplayStateBudget:
    """Caller-supplied canonical state-size limits for each replay path."""

    max_state_bytes: int
    max_total_state_bytes: int

    def __post_init__(self) -> None:
        for field_name in ("max_state_bytes", "max_total_state_bytes"):
            value = getattr(self, field_name)
            if isinstance(value, bool) or not isinstance(value, int) or value < 1:
                raise ValueError(f"{field_name} must be a positive integer")
        if self.max_total_state_bytes < self.max_state_bytes:
            raise ValueError(
                "max_total_state_bytes must be >= max_state_bytes"
            )

    def require_state_size(self, observed: int) -> None:
        if observed > self.max_state_bytes:
            raise ResourceBudgetExceeded(
                "replay_state_bytes",
                self.max_state_bytes,
                observed,
            )

    def require_total_state_size(self, observed: int) -> None:
        if observed > self.max_total_state_bytes:
            raise ResourceBudgetExceeded(
                "replay_total_state_bytes",
                self.max_total_state_bytes,
                observed,
            )


@dataclass(frozen=True, slots=True)
class ReplaySnapshot:
''',
)
replace_once(
    contracts,
    '''    PAYLOAD_DECODE_ERROR = "PAYLOAD_DECODE_ERROR"
    PAYLOAD_NOT_CANONICAL = "PAYLOAD_NOT_CANONICAL"
''',
    '''    PAYLOAD_DECODE_ERROR = "PAYLOAD_DECODE_ERROR"
    PAYLOAD_NOT_CANONICAL = "PAYLOAD_NOT_CANONICAL"
    PAYLOAD_DIGEST_MISMATCH = "PAYLOAD_DIGEST_MISMATCH"
    STREAM_CHANGED_DURING_VERIFICATION = "STREAM_CHANGED_DURING_VERIFICATION"
''',
)

replay_init = Path("src/mentaury/replay/__init__.py")
replace_once(
    replay_init,
    '''    ReplayReducer,
    ReplaySnapshot,
)
''',
    '''    ReplayReducer,
    ReplaySnapshot,
    ReplayStateBudget,
)
''',
)
replace_once(
    replay_init,
    '''    "ReplayReducer",
    "ReplaySnapshot",
''',
    '''    "ReplayReducer",
    "ReplaySnapshot",
    "ReplayStateBudget",
''',
)

engine = Path("src/mentaury/replay/engine.py")
replace_once(
    engine,
    '''    R0IntegrityVerifier,
    ResourceBudgetExceeded,
    SQLiteEventPayloadStore,
    VerificationBudget,
)
''',
    '''    R0IntegrityVerifier,
    ResourceBudgetExceeded,
    SQLiteEventPayloadStore,
    VerificationBudget,
    compute_payload_digest,
)
''',
)
replace_once(
    engine,
    '''    ReplayReducer,
    ReplaySnapshot,
)
''',
    '''    ReplayReducer,
    ReplaySnapshot,
    ReplayStateBudget,
)
''',
)
replace_once(
    engine,
    '''        budget: VerificationBudget,
        reducer: ReplayReducer,
    ) -> None:
''',
    '''        budget: VerificationBudget,
        state_budget: ReplayStateBudget,
        reducer: ReplayReducer,
    ) -> None:
''',
)
replace_once(
    engine,
    '''        if not isinstance(budget, VerificationBudget):
            raise TypeError("budget must be a VerificationBudget")
        self._store = store
        self._registry = registry
        self._budget = budget
        self._reducer = reducer
''',
    '''        if not isinstance(budget, VerificationBudget):
            raise TypeError("budget must be a VerificationBudget")
        if not isinstance(state_budget, ReplayStateBudget):
            raise TypeError("state_budget must be a ReplayStateBudget")
        self._store = store
        self._registry = registry
        self._budget = budget
        self._state_budget = state_budget
        self._reducer = reducer
''',
)
replace_once(
    engine,
    '''        events = self._store.list_stream(stream_id)
        metadata_failure = self._validate_snapshot_metadata(
''',
    '''        events = self._store.list_stream(stream_id)
        stream_meta = self._store.load_stream_meta(stream_id)
        expected_tail_hash = events[-1].event_hash if events else GENESIS_HASH
        if (
            len(events) != r0_report.checked_events
            or stream_meta.event_count != len(events)
            or stream_meta.current_version != len(events)
            or stream_meta.last_event_hash != expected_tail_hash
        ):
            return self._failed_report(
                stream_id,
                reducer_id,
                reducer_version,
                snapshot.through_stream_version,
                ReplayFailure(
                    ReplayFailureCode.STREAM_CHANGED_DURING_VERIFICATION,
                    stream_id,
                    "stream changed between R0 verification and replay capture",
                ),
                checked_events=r0_report.checked_events,
            )

        metadata_failure = self._validate_snapshot_metadata(
''',
)
replace_once(
    engine,
    '''        if snapshot_state.state_hash != snapshot.state_hash:
''',
    '''        snapshot_budget_failure = self._state_budget_failure(
            stream_id,
            snapshot_state,
            len(snapshot_state.canonical_bytes),
        )
        if snapshot_budget_failure is not None:
            return self._failed_report(
                stream_id,
                reducer_id,
                reducer_version,
                snapshot.through_stream_version,
                snapshot_budget_failure,
                snapshot_state_hash=snapshot_state.state_hash,
            )
        if snapshot_state.state_hash != snapshot.state_hash:
''',
)
replace_once(
    engine,
    '''        try:
            full = self._run(
''',
    '''        initial_budget_failure = self._state_budget_failure(
            stream_id,
            initial_state,
            len(initial_state.canonical_bytes),
        )
        if initial_budget_failure is not None:
            return self._failed_report(
                stream_id,
                reducer_id,
                reducer_version,
                snapshot.through_stream_version,
                initial_budget_failure,
            )

        try:
            full = self._run(
''',
)
replace_once(
    engine,
    '''        total_payload_bytes = 0
        checkpoint = state if checkpoint_version == 0 else None

        try:
''',
    '''        total_payload_bytes = 0
        total_state_bytes = len(state.canonical_bytes)
        checkpoint = state if checkpoint_version == 0 else None

        try:
            self._state_budget.require_state_size(len(state.canonical_bytes))
            self._state_budget.require_total_state_size(total_state_bytes)
''',
)
replace_once(
    engine,
    '''                payload = _decode_payload(stream_id, event, payload_bytes)
                state = self._apply_twice(stream_id, state, event, payload)
                applied += 1
''',
    '''                payload = _decode_payload(stream_id, event, payload_bytes)
                state = self._apply_twice(stream_id, state, event, payload)
                try:
                    self._state_budget.require_state_size(
                        len(state.canonical_bytes)
                    )
                    total_state_bytes += len(state.canonical_bytes)
                    self._state_budget.require_total_state_size(
                        total_state_bytes
                    )
                except ResourceBudgetExceeded as exc:
                    raise _ReplayAborted(
                        ReplayFailure(
                            ReplayFailureCode.RESOURCE_BUDGET_EXCEEDED,
                            stream_id,
                            str(exc),
                            event.event_id,
                            event.stream_version,
                        )
                    ) from exc
                applied += 1
''',
)
replace_once(
    engine,
    '''    @staticmethod
    def _failed_report(
''',
    '''    def _state_budget_failure(
        self,
        stream_id: str,
        state: _NormalizedState,
        total_state_bytes: int,
    ) -> ReplayFailure | None:
        try:
            self._state_budget.require_state_size(len(state.canonical_bytes))
            self._state_budget.require_total_state_size(total_state_bytes)
        except ResourceBudgetExceeded as exc:
            return ReplayFailure(
                ReplayFailureCode.RESOURCE_BUDGET_EXCEEDED,
                stream_id,
                str(exc),
            )
        return None

    @staticmethod
    def _failed_report(
''',
)
replace_once(
    engine,
    '''    if canonical != payload_bytes:
        raise _ReplayAborted(
            ReplayFailure(
                ReplayFailureCode.PAYLOAD_NOT_CANONICAL,
                stream_id,
                "payload bytes do not use canonical JSON encoding",
                event.event_id,
                event.stream_version,
            )
        )
    return freeze_payload(decoded)
''',
    '''    if canonical != payload_bytes:
        raise _ReplayAborted(
            ReplayFailure(
                ReplayFailureCode.PAYLOAD_NOT_CANONICAL,
                stream_id,
                "payload bytes do not use canonical JSON encoding",
                event.event_id,
                event.stream_version,
            )
        )
    if compute_payload_digest(payload_bytes) != event.payload_digest:
        raise _ReplayAborted(
            ReplayFailure(
                ReplayFailureCode.PAYLOAD_DIGEST_MISMATCH,
                stream_id,
                "payload digest changed after R0 verification",
                event.event_id,
                event.stream_version,
            )
        )
    return freeze_payload(decoded)
''',
)

tests = Path("tests/test_r1_replay.py")
replace_once(
    tests,
    '''    ReplaySnapshot,
    compute_replay_state_hash,
''',
    '''    ReplaySnapshot,
    ReplayStateBudget,
    compute_replay_state_hash,
''',
)
replace_once(
    tests,
    '''def _verifier(
    store: SQLiteEventPayloadStore,
    reducer=None,
    *,
    budget: VerificationBudget | None = None,
) -> R1ReplayVerifier:
    return R1ReplayVerifier(
        store,
        _registry(),
        budget or _budget(),
        reducer or CounterReducer(),
    )
''',
    '''def _state_budget(
    *,
    max_state_bytes: int = 10_000,
    max_total_state_bytes: int = 100_000,
) -> ReplayStateBudget:
    return ReplayStateBudget(
        max_state_bytes=max_state_bytes,
        max_total_state_bytes=max_total_state_bytes,
    )


def _verifier(
    store: SQLiteEventPayloadStore,
    reducer=None,
    *,
    budget: VerificationBudget | None = None,
    state_budget: ReplayStateBudget | None = None,
) -> R1ReplayVerifier:
    return R1ReplayVerifier(
        store,
        _registry(),
        budget or _budget(),
        state_budget or _state_budget(),
        reducer or CounterReducer(),
    )
''',
)
append_tests = '''

class ExpandingReducer(CounterReducer):
    def apply(self, state, event, payload) -> Mapping[str, object]:
        return {
            "total": state["total"],
            "event_ids": list(state["event_ids"]),
            "padding": "x" * 1_000,
        }


def test_reducer_state_size_budget_is_enforced() -> None:
    with SQLiteEventPayloadStore.in_memory() as store:
        store.initialize_schema()
        _append_counter(store, "EVT-1", 1, 1)
        snapshot = make_replay_snapshot(
            reducer_id=CounterReducer.reducer_id,
            reducer_version=CounterReducer.reducer_version,
            stream_id=STREAM_ID,
            through_stream_version=0,
            through_event_hash=GENESIS_HASH,
            state={"total": 0, "event_ids": []},
        )

        report = _verifier(
            store,
            ExpandingReducer(),
            state_budget=_state_budget(max_state_bytes=200),
        ).verify_stream(STREAM_ID, snapshot)

        assert _failure_code(report) is ReplayFailureCode.RESOURCE_BUDGET_EXCEEDED


def test_snapshot_state_size_budget_is_enforced_before_replay() -> None:
    with SQLiteEventPayloadStore.in_memory() as store:
        store.initialize_schema()
        snapshot = make_replay_snapshot(
            reducer_id=CounterReducer.reducer_id,
            reducer_version=CounterReducer.reducer_version,
            stream_id=STREAM_ID,
            through_stream_version=0,
            through_event_hash=GENESIS_HASH,
            state={"total": 0, "event_ids": [], "padding": "x" * 1_000},
        )

        report = _verifier(
            store,
            state_budget=_state_budget(max_state_bytes=200),
        ).verify_stream(STREAM_ID, snapshot)

        assert _failure_code(report) is ReplayFailureCode.RESOURCE_BUDGET_EXCEEDED
'''
text = tests.read_text(encoding="utf-8")
if "test_reducer_state_size_budget_is_enforced" in text:
    raise RuntimeError("state budget tests already present")
tests.write_text(text + append_tests, encoding="utf-8")

doc = Path("docs/P0_013_R1_DETERMINISTIC_REPLAY.md")
replace_once(
    doc,
    '''The caller supplies `VerificationBudget` limits for:

- event count;
- one payload size;
- total payload material per replay path.

Full replay and snapshot-tail replay each operate under the declared bound.
''',
    '''The caller supplies `VerificationBudget` limits for:

- event count;
- one payload size;
- total payload material per replay path.

The caller also supplies `ReplayStateBudget` limits for:

- one canonical projection state;
- cumulative canonical state material produced per replay path.

Full replay and snapshot-tail replay each operate under the declared bounds.
''',
)
replace_once(
    doc,
    '''- explicit resource-budget failure.
''',
    '''- explicit event/payload and reducer-state resource-budget failure;
- stream-stability capture after R0;
- replay-time payload digest verification.
''',
)
replace_once(
    doc,
    '''2. run bounded R0 verification on the complete stream;
3. verify snapshot reducer, stream, version and event-hash anchor;
''',
    '''2. run bounded R0 verification on the complete stream;
3. capture the same verified event count/tail metadata before replay;
4. verify snapshot reducer, stream, version and event-hash anchor;
''',
)
replace_once(
    doc,
    '''4. recompute the snapshot state hash;
5. replay the complete stream from a canonical initial state;
6. compare the supplied snapshot state with the full-replay checkpoint state;
7. replay the tail from the supplied snapshot;
8. compare canonical final bytes and state hashes.
''',
    '''5. recompute the snapshot state hash and apply state-size bounds;
6. replay the complete stream from a canonical bounded initial state;
7. recheck each replayed payload digest against its immutable envelope;
8. compare the supplied snapshot state with the full-replay checkpoint state;
9. replay the tail from the supplied snapshot;
10. compare canonical final bytes and state hashes.
''',
)
