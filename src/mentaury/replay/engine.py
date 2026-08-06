"""P0-013 R1 full-replay and snapshot-tail equivalence verification."""

from __future__ import annotations

import hashlib
import json
from contextlib import contextmanager
from collections.abc import Iterator
from collections.abc import Mapping
from dataclasses import dataclass

from mentaury.contracts import (
    CanonicalJSONError,
    EventEnvelope,
    canonical_json_bytes,
)
from mentaury.contracts.primitives import FrozenPayload, freeze_payload
from mentaury.storage import (
    R0IntegrityVerifier,
    ResourceBudgetExceeded,
    SQLiteEventPayloadStore,
    VerificationBudget,
    compute_payload_digest,
)
from mentaury.storage.stream_meta import GENESIS_HASH
from mentaury.validation import SchemaRegistry

from .contracts import (
    R1ReplayReport,
    ReplayFailure,
    ReplayFailureCode,
    ReplayReducer,
    ReplaySnapshot,
    ReplayStateBudget,
)


@dataclass(frozen=True, slots=True)
class _NormalizedState:
    value: FrozenPayload
    canonical_bytes: bytes
    state_hash: str


@dataclass(frozen=True, slots=True)
class _ReplayRun:
    state: _NormalizedState
    checked_events: int
    applied_events: int
    checkpoint_state: _NormalizedState | None


class _ReplayAborted(RuntimeError):
    def __init__(self, failure: ReplayFailure) -> None:
        self.failure = failure
        super().__init__(failure.message)


def compute_replay_state_hash(state: Mapping[str, object]) -> str:
    """Hash one canonical projection state under an explicit R1 domain tag."""

    canonical = canonical_json_bytes(state)
    digest = hashlib.sha256(b"MENTAURY_R1_STATE_V1\x00" + canonical).hexdigest()
    return f"sha256:{digest}"


def make_replay_snapshot(
    *,
    reducer_id: str,
    reducer_version: str,
    stream_id: str,
    through_stream_version: int,
    through_event_hash: str,
    state: Mapping[str, object],
) -> ReplaySnapshot:
    """Create a self-consistent checkpoint without declaring it trustworthy."""

    normalized = _normalize_state(state, "snapshot state")
    return ReplaySnapshot(
        reducer_id=reducer_id,
        reducer_version=reducer_version,
        stream_id=stream_id,
        through_stream_version=through_stream_version,
        through_event_hash=through_event_hash,
        state=normalized.value,
        state_hash=normalized.state_hash,
    )


class R1ReplayVerifier:
    """Verify R0 first, then compare full replay with snapshot + tail replay."""

    def __init__(
        self,
        store: SQLiteEventPayloadStore,
        registry: SchemaRegistry,
        budget: VerificationBudget,
        state_budget: ReplayStateBudget,
        reducer: ReplayReducer,
    ) -> None:
        if not isinstance(store, SQLiteEventPayloadStore):
            raise TypeError("store must be a SQLiteEventPayloadStore")
        if not isinstance(registry, SchemaRegistry):
            raise TypeError("registry must be a SchemaRegistry")
        if not isinstance(budget, VerificationBudget):
            raise TypeError("budget must be a VerificationBudget")
        if not isinstance(state_budget, ReplayStateBudget):
            raise TypeError("state_budget must be a ReplayStateBudget")
        self._store = store
        self._registry = registry
        self._budget = budget
        self._state_budget = state_budget
        self._reducer = reducer

    def verify_stream(
        self,
        stream_id: str,
        snapshot: ReplaySnapshot,
    ) -> R1ReplayReport:
        if not isinstance(stream_id, str) or not stream_id.strip():
            raise ValueError("stream_id must be a non-empty string")
        if not isinstance(snapshot, ReplaySnapshot):
            raise TypeError("snapshot must be a ReplaySnapshot")

        with _sqlite_read_snapshot(self._store):
            return self._verify_stream_in_snapshot(stream_id, snapshot)

    def _verify_stream_in_snapshot(
        self,
        stream_id: str,
        snapshot: ReplaySnapshot,
    ) -> R1ReplayReport:
            reducer_error = _validate_reducer(self._reducer)
            reducer_id = getattr(self._reducer, "reducer_id", "<invalid>")
            reducer_version = getattr(self._reducer, "reducer_version", "<invalid>")
            if reducer_error is not None:
                return self._failed_report(
                    stream_id,
                    reducer_id,
                    reducer_version,
                    snapshot.through_stream_version,
                    ReplayFailure(
                        ReplayFailureCode.INVALID_REDUCER,
                        stream_id,
                        reducer_error,
                    ),
                )

            r0_report = R0IntegrityVerifier(
                self._store,
                self._registry,
                self._budget,
            ).verify_stream(stream_id)
            if not r0_report.ok:
                assert r0_report.failure is not None
                return self._failed_report(
                    stream_id,
                    reducer_id,
                    reducer_version,
                    snapshot.through_stream_version,
                    ReplayFailure(
                        ReplayFailureCode.R0_PREREQUISITE_FAILED,
                        stream_id,
                        "R0 prerequisite failed: "
                        f"{r0_report.failure.code}: {r0_report.failure.message}",
                        r0_report.failure.event_id,
                        r0_report.failure.stream_version,
                    ),
                    checked_events=r0_report.checked_events,
                )

            events = self._store.list_stream(stream_id)
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
                stream_id,
                snapshot,
                events,
                reducer_id,
                reducer_version,
            )
            if metadata_failure is not None:
                return self._failed_report(
                    stream_id,
                    reducer_id,
                    reducer_version,
                    snapshot.through_stream_version,
                    metadata_failure,
                )

            try:
                snapshot_state = _normalize_state(snapshot.state, "snapshot state")
            except (CanonicalJSONError, TypeError, ValueError) as exc:
                return self._failed_report(
                    stream_id,
                    reducer_id,
                    reducer_version,
                    snapshot.through_stream_version,
                    ReplayFailure(
                        ReplayFailureCode.SNAPSHOT_STATE_HASH_MISMATCH,
                        stream_id,
                        f"snapshot state is not canonical: {exc}",
                    ),
                )
            snapshot_budget_failure = self._state_budget_failure(
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
                return self._failed_report(
                    stream_id,
                    reducer_id,
                    reducer_version,
                    snapshot.through_stream_version,
                    ReplayFailure(
                        ReplayFailureCode.SNAPSHOT_STATE_HASH_MISMATCH,
                        stream_id,
                        "snapshot state_hash does not match canonical state",
                    ),
                    snapshot_state_hash=snapshot_state.state_hash,
                )

            try:
                initial_state = _normalize_state(
                    self._reducer.initial_state(),
                    "initial reducer state",
                )
            except Exception as exc:
                return self._failed_report(
                    stream_id,
                    reducer_id,
                    reducer_version,
                    snapshot.through_stream_version,
                    ReplayFailure(
                        ReplayFailureCode.INVALID_INITIAL_STATE,
                        stream_id,
                        f"invalid initial reducer state: {exc}",
                    ),
                )

            initial_budget_failure = self._state_budget_failure(
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
                    stream_id,
                    events,
                    initial_state,
                    checkpoint_version=snapshot.through_stream_version,
                )
            except _ReplayAborted as exc:
                return self._failed_report(
                    stream_id,
                    reducer_id,
                    reducer_version,
                    snapshot.through_stream_version,
                    exc.failure,
                )

            assert full.checkpoint_state is not None
            if (
                full.checkpoint_state.state_hash != snapshot.state_hash
                or full.checkpoint_state.canonical_bytes
                != snapshot_state.canonical_bytes
            ):
                return self._failed_report(
                    stream_id,
                    reducer_id,
                    reducer_version,
                    snapshot.through_stream_version,
                    ReplayFailure(
                        ReplayFailureCode.SNAPSHOT_STATE_MISMATCH,
                        stream_id,
                        "snapshot state does not equal full replay at its checkpoint",
                    ),
                    checked_events=full.checked_events,
                    applied_events=full.applied_events,
                    full_state_hash=full.state.state_hash,
                    snapshot_state_hash=snapshot_state.state_hash,
                )

            tail_events = events[snapshot.through_stream_version :]
            try:
                tail = self._run(
                    stream_id,
                    tail_events,
                    snapshot_state,
                    checkpoint_version=None,
                )
            except _ReplayAborted as exc:
                return self._failed_report(
                    stream_id,
                    reducer_id,
                    reducer_version,
                    snapshot.through_stream_version,
                    exc.failure,
                    checked_events=full.checked_events,
                    applied_events=full.applied_events,
                    full_state_hash=full.state.state_hash,
                    snapshot_state_hash=snapshot_state.state_hash,
                )

            if (
                tail.state.state_hash != full.state.state_hash
                or tail.state.canonical_bytes != full.state.canonical_bytes
            ):
                return self._failed_report(
                    stream_id,
                    reducer_id,
                    reducer_version,
                    snapshot.through_stream_version,
                    ReplayFailure(
                        ReplayFailureCode.FINAL_STATE_MISMATCH,
                        stream_id,
                        "snapshot + tail state does not equal full replay state",
                    ),
                    checked_events=full.checked_events,
                    applied_events=full.applied_events,
                    full_state_hash=full.state.state_hash,
                    snapshot_state_hash=snapshot_state.state_hash,
                    tail_state_hash=tail.state.state_hash,
                )

            return R1ReplayReport(
                stream_id=stream_id,
                reducer_id=reducer_id,
                reducer_version=reducer_version,
                ok=True,
                checked_events=full.checked_events,
                applied_events=full.applied_events,
                snapshot_through_version=snapshot.through_stream_version,
                full_state_hash=full.state.state_hash,
                snapshot_state_hash=snapshot_state.state_hash,
                tail_state_hash=tail.state.state_hash,
                failure=None,
                verified_through_stream_version=len(events),
                verified_through_event_hash=expected_tail_hash,
            )

    def _run(
        self,
        stream_id: str,
        events: tuple[EventEnvelope, ...],
        starting_state: _NormalizedState,
        *,
        checkpoint_version: int | None,
    ) -> _ReplayRun:
        state = starting_state
        checked = 0
        applied = 0
        total_payload_bytes = 0
        total_state_bytes = len(state.canonical_bytes)
        checkpoint = state if checkpoint_version == 0 else None

        try:
            _require_state_budget(
                self._state_budget,
                len(state.canonical_bytes),
                total_state_bytes,
            )
            self._budget.require_event_count(len(events))
        except ResourceBudgetExceeded as exc:
            raise _ReplayAborted(
                ReplayFailure(
                    ReplayFailureCode.RESOURCE_BUDGET_EXCEEDED,
                    stream_id,
                    str(exc),
                )
            ) from exc

        for event in events:
            checked += 1
            if event.affects_domain_state:
                pair = (event.event_type, event.payload_schema)
                if pair not in self._reducer.supported_event_schemas:
                    raise _ReplayAborted(
                        ReplayFailure(
                            ReplayFailureCode.UNKNOWN_EVENT_SCHEMA,
                            stream_id,
                            "state-affecting event/schema is not supported by reducer: "
                            f"{pair!r}",
                            event.event_id,
                            event.stream_version,
                        )
                    )

                stored_payload = self._store.load_payload(event.payload_ref)
                if stored_payload is None:
                    raise _ReplayAborted(
                        ReplayFailure(
                            ReplayFailureCode.PAYLOAD_UNAVAILABLE,
                            stream_id,
                            "state-affecting payload material is unavailable; "
                            "snapshot cannot replace missing history",
                            event.event_id,
                            event.stream_version,
                        )
                    )
                payload_bytes = stored_payload.payload_bytes
                try:
                    self._budget.require_payload_size(len(payload_bytes))
                    total_payload_bytes += len(payload_bytes)
                    self._budget.require_total_payload_size(total_payload_bytes)
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

                payload = _decode_payload(stream_id, event, payload_bytes)
                state = self._apply_twice(stream_id, state, event, payload)
                try:
                    total_state_bytes += len(state.canonical_bytes)
                    _require_state_budget(
                        self._state_budget,
                        len(state.canonical_bytes),
                        total_state_bytes,
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

            if checkpoint_version == event.stream_version:
                checkpoint = state

        return _ReplayRun(state, checked, applied, checkpoint)

    def _apply_twice(
        self,
        stream_id: str,
        state: _NormalizedState,
        event: EventEnvelope,
        payload: FrozenPayload,
    ) -> _NormalizedState:
        first_input = _clone_frozen(state.value)
        second_input = _clone_frozen(state.value)
        first_payload = _clone_frozen(payload)
        second_payload = _clone_frozen(payload)
        try:
            first_output = self._reducer.apply(first_input, event, first_payload)
            second_output = self._reducer.apply(second_input, event, second_payload)
        except Exception as exc:
            raise _ReplayAborted(
                ReplayFailure(
                    ReplayFailureCode.REDUCER_ERROR,
                    stream_id,
                    f"reducer raised {type(exc).__name__}: {exc}",
                    event.event_id,
                    event.stream_version,
                )
            ) from exc

        if first_output is first_input or second_output is second_input:
            raise _ReplayAborted(
                ReplayFailure(
                    ReplayFailureCode.REDUCER_REUSED_INPUT,
                    stream_id,
                    "reducer must return a new state mapping",
                    event.event_id,
                    event.stream_version,
                )
            )

        try:
            first = _normalize_state(first_output, "reducer output")
            second = _normalize_state(second_output, "reducer output")
        except (CanonicalJSONError, TypeError, ValueError) as exc:
            raise _ReplayAborted(
                ReplayFailure(
                    ReplayFailureCode.INVALID_REDUCER_STATE,
                    stream_id,
                    f"reducer returned invalid canonical state: {exc}",
                    event.event_id,
                    event.stream_version,
                )
            ) from exc

        if (
            first.state_hash != second.state_hash
            or first.canonical_bytes != second.canonical_bytes
        ):
            raise _ReplayAborted(
                ReplayFailure(
                    ReplayFailureCode.REDUCER_NONDETERMINISTIC,
                    stream_id,
                    "reducer produced different canonical outputs for identical inputs",
                    event.event_id,
                    event.stream_version,
                )
            )
        return first

    def _validate_snapshot_metadata(
        self,
        stream_id: str,
        snapshot: ReplaySnapshot,
        events: tuple[EventEnvelope, ...],
        reducer_id: str,
        reducer_version: str,
    ) -> ReplayFailure | None:
        if (
            snapshot.reducer_id != reducer_id
            or snapshot.reducer_version != reducer_version
        ):
            return ReplayFailure(
                ReplayFailureCode.SNAPSHOT_REDUCER_MISMATCH,
                stream_id,
                "snapshot reducer identity/version does not match verifier",
            )
        if snapshot.stream_id != stream_id:
            return ReplayFailure(
                ReplayFailureCode.SNAPSHOT_STREAM_MISMATCH,
                stream_id,
                "snapshot stream_id does not match requested stream",
            )
        if snapshot.through_stream_version > len(events):
            return ReplayFailure(
                ReplayFailureCode.SNAPSHOT_VERSION_OUT_OF_RANGE,
                stream_id,
                "snapshot checkpoint is beyond the verified stream tail",
            )
        expected_anchor = (
            GENESIS_HASH
            if snapshot.through_stream_version == 0
            else events[snapshot.through_stream_version - 1].event_hash
        )
        if snapshot.through_event_hash != expected_anchor:
            return ReplayFailure(
                ReplayFailureCode.SNAPSHOT_ANCHOR_MISMATCH,
                stream_id,
                "snapshot event-hash anchor does not match verified history",
            )
        return None

    def _state_budget_failure(
        self,
        stream_id: str,
        state: _NormalizedState,
        total_state_bytes: int,
    ) -> ReplayFailure | None:
        try:
            _require_state_budget(
                self._state_budget,
                len(state.canonical_bytes),
                total_state_bytes,
            )
        except ResourceBudgetExceeded as exc:
            return ReplayFailure(
                ReplayFailureCode.RESOURCE_BUDGET_EXCEEDED,
                stream_id,
                str(exc),
            )
        return None

    @staticmethod
    def _failed_report(
        stream_id: str,
        reducer_id: str,
        reducer_version: str,
        snapshot_version: int,
        failure: ReplayFailure,
        *,
        checked_events: int = 0,
        applied_events: int = 0,
        full_state_hash: str | None = None,
        snapshot_state_hash: str | None = None,
        tail_state_hash: str | None = None,
    ) -> R1ReplayReport:
        return R1ReplayReport(
            stream_id=stream_id,
            reducer_id=str(reducer_id),
            reducer_version=str(reducer_version),
            ok=False,
            checked_events=checked_events,
            applied_events=applied_events,
            snapshot_through_version=snapshot_version,
            full_state_hash=full_state_hash,
            snapshot_state_hash=snapshot_state_hash,
            tail_state_hash=tail_state_hash,
            failure=failure,
        )


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
    budget: ReplayStateBudget,
    state_bytes: int,
    total_state_bytes: int,
) -> None:
    if state_bytes > budget.max_state_bytes:
        raise ResourceBudgetExceeded(
            "replay_state_bytes",
            budget.max_state_bytes,
            state_bytes,
        )
    if total_state_bytes > budget.max_total_state_bytes:
        raise ResourceBudgetExceeded(
            "replay_total_state_bytes",
            budget.max_total_state_bytes,
            total_state_bytes,
        )


def _validate_reducer(reducer: object) -> str | None:
    reducer_id = getattr(reducer, "reducer_id", None)
    reducer_version = getattr(reducer, "reducer_version", None)
    supported = getattr(reducer, "supported_event_schemas", None)
    if not isinstance(reducer_id, str) or not reducer_id.strip():
        return "reducer_id must be a non-empty string"
    if not isinstance(reducer_version, str) or not reducer_version.strip():
        return "reducer_version must be a non-empty string"
    if not isinstance(supported, frozenset) or not supported:
        return "supported_event_schemas must be a non-empty frozenset"
    for pair in supported:
        if (
            not isinstance(pair, tuple)
            or len(pair) != 2
            or any(not isinstance(value, str) or not value for value in pair)
        ):
            return "supported_event_schemas must contain non-empty string pairs"
    if not callable(getattr(reducer, "initial_state", None)):
        return "reducer must define initial_state()"
    if not callable(getattr(reducer, "apply", None)):
        return "reducer must define apply()"
    return None


def _normalize_state(
    value: Mapping[str, object],
    context: str,
) -> _NormalizedState:
    if not isinstance(value, Mapping):
        raise TypeError(f"{context} must be a mapping")
    canonical = canonical_json_bytes(value)
    decoded = json.loads(canonical.decode("utf-8"))
    if not isinstance(decoded, dict):  # pragma: no cover - Mapping contract guard
        raise TypeError(f"{context} must encode as an object")
    frozen = freeze_payload(decoded)
    return _NormalizedState(
        frozen,
        canonical,
        compute_replay_state_hash(decoded),
    )


def _clone_frozen(value: FrozenPayload) -> FrozenPayload:
    decoded = json.loads(canonical_json_bytes(value).decode("utf-8"))
    if not isinstance(decoded, dict):  # pragma: no cover - FrozenPayload contract
        raise TypeError("frozen replay value must encode as an object")
    return freeze_payload(decoded)


def _decode_payload(
    stream_id: str,
    event: EventEnvelope,
    payload_bytes: bytes,
) -> FrozenPayload:
    try:
        decoded = json.loads(payload_bytes.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise _ReplayAborted(
            ReplayFailure(
                ReplayFailureCode.PAYLOAD_DECODE_ERROR,
                stream_id,
                f"payload decode failed: {exc}",
                event.event_id,
                event.stream_version,
            )
        ) from exc
    if not isinstance(decoded, dict):
        raise _ReplayAborted(
            ReplayFailure(
                ReplayFailureCode.PAYLOAD_DECODE_ERROR,
                stream_id,
                "state-affecting payload must be an object",
                event.event_id,
                event.stream_version,
            )
        )
    try:
        canonical = canonical_json_bytes(decoded)
    except (CanonicalJSONError, TypeError, ValueError) as exc:
        raise _ReplayAborted(
            ReplayFailure(
                ReplayFailureCode.PAYLOAD_NOT_CANONICAL,
                stream_id,
                f"payload is not canonicalizable: {exc}",
                event.event_id,
                event.stream_version,
            )
        ) from exc
    if canonical != payload_bytes:
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
