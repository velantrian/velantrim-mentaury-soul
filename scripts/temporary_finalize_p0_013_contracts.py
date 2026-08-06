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
    "from mentaury.storage.budget import ResourceBudgetExceeded\n",
    "",
)
old_methods = '''
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
'''
replace_once(contracts, old_methods, "")
replace_once(
    contracts,
    '''    tail_state_hash: str | None
    failure: ReplayFailure | None
''',
    '''    tail_state_hash: str | None
    failure: ReplayFailure | None
    verified_through_stream_version: int = 0
    verified_through_event_hash: str | None = None
''',
)

engine = Path("src/mentaury/replay/engine.py")
replace_once(
    engine,
    '''            tail_state_hash=tail.state.state_hash,
            failure=None,
        )
''',
    '''            tail_state_hash=tail.state.state_hash,
            failure=None,
            verified_through_stream_version=len(events),
            verified_through_event_hash=expected_tail_hash,
        )
''',
)
replace_once(
    engine,
    '''            self._state_budget.require_state_size(len(state.canonical_bytes))
            self._state_budget.require_total_state_size(total_state_bytes)
            self._budget.require_event_count(len(events))
''',
    '''            _require_state_budget(
                self._state_budget,
                len(state.canonical_bytes),
                total_state_bytes,
            )
            self._budget.require_event_count(len(events))
''',
)
replace_once(
    engine,
    '''                    self._state_budget.require_state_size(
                        len(state.canonical_bytes)
                    )
                    total_state_bytes += len(state.canonical_bytes)
                    self._state_budget.require_total_state_size(
                        total_state_bytes
                    )
''',
    '''                    total_state_bytes += len(state.canonical_bytes)
                    _require_state_budget(
                        self._state_budget,
                        len(state.canonical_bytes),
                        total_state_bytes,
                    )
''',
)
replace_once(
    engine,
    '''        try:
            self._state_budget.require_state_size(len(state.canonical_bytes))
            self._state_budget.require_total_state_size(total_state_bytes)
        except ResourceBudgetExceeded as exc:
''',
    '''        try:
            _require_state_budget(
                self._state_budget,
                len(state.canonical_bytes),
                total_state_bytes,
            )
        except ResourceBudgetExceeded as exc:
''',
)
insert_marker = '''
def _validate_reducer(reducer: object) -> str | None:
'''
helper = '''
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
'''
replace_once(engine, insert_marker, helper)

tests = Path("tests/test_r1_replay.py")
replace_once(
    tests,
    '''        assert report.tail_state_hash == expected_hash
        assert report.failure is None
''',
    '''        assert report.tail_state_hash == expected_hash
        assert report.verified_through_stream_version == 3
        assert report.verified_through_event_hash == store.list_stream(STREAM_ID)[-1].event_hash
        assert report.failure is None
''',
)

doc = Path("docs/P0_013_R1_DETERMINISTIC_REPLAY.md")
replace_once(
    doc,
    '''The P0-013 tests cover:
''',
    '''The P0-013 suite contains **21 replay tests** covering:
''',
)
replace_once(
    doc,
    '''R1 verifies deterministic state reconstruction for one declared reducer and one
R0-verified stream. It does not establish cross-stream transaction semantics,
''',
    '''A successful report records the exact captured stream version and tail event
hash so callers do not confuse a verified immutable prefix with an open-ended
claim about future appends.

R1 verifies deterministic state reconstruction for one declared reducer and one
R0-verified stream. It does not establish cross-stream transaction semantics,
''',
)
