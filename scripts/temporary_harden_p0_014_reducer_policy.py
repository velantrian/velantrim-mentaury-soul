from __future__ import annotations

from pathlib import Path


def replace_once(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{path}: expected one marker, found {count}: {old!r}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


contracts = Path("src/mentaury/beliefs/contracts.py")
insert = '''

_P0_014_ALLOWED_TRANSITIONS: dict[BeliefStatus, frozenset[BeliefStatus]] = {
    BeliefStatus.HYPOTHESIS: frozenset(
        {
            BeliefStatus.PROVISIONAL,
            BeliefStatus.CONTESTED,
            BeliefStatus.UNRESOLVED,
            BeliefStatus.SUPERSEDED,
        }
    ),
    BeliefStatus.PROVISIONAL: frozenset(
        {
            BeliefStatus.CONTESTED,
            BeliefStatus.UNRESOLVED,
            BeliefStatus.SUPERSEDED,
        }
    ),
    BeliefStatus.CONTESTED: frozenset(
        {
            BeliefStatus.PROVISIONAL,
            BeliefStatus.UNRESOLVED,
            BeliefStatus.SUPERSEDED,
        }
    ),
    BeliefStatus.UNRESOLVED: frozenset(
        {
            BeliefStatus.HYPOTHESIS,
            BeliefStatus.PROVISIONAL,
            BeliefStatus.CONTESTED,
            BeliefStatus.SUPERSEDED,
        }
    ),
    BeliefStatus.SUPPORTED: frozenset(),
    BeliefStatus.CONTRADICTED: frozenset(),
    BeliefStatus.SUPERSEDED: frozenset(),
}


def belief_status_requires_evidence_gate(status: BeliefStatus) -> bool:
    return status in {BeliefStatus.SUPPORTED, BeliefStatus.CONTRADICTED}


def belief_status_transition_allowed(
    current: BeliefStatus,
    requested: BeliefStatus,
) -> bool:
    if current in {
        BeliefStatus.SUPPORTED,
        BeliefStatus.CONTRADICTED,
        BeliefStatus.SUPERSEDED,
    }:
        return False
    return requested is current or requested in _P0_014_ALLOWED_TRANSITIONS[current]
'''
replace_once(
    contracts,
    '''class EvidenceSide(StrEnum):
    FOR = "for"
    AGAINST = "against"


class BeliefRejectionCode(StrEnum):
''',
    '''class EvidenceSide(StrEnum):
    FOR = "for"
    AGAINST = "against"
''' + insert + '''

class BeliefRejectionCode(StrEnum):
''',
)

lifecycle = Path("src/mentaury/beliefs/lifecycle.py")
text = lifecycle.read_text(encoding="utf-8")
start = text.index("_ALLOWED_TRANSITIONS: dict[BeliefStatus")
end = text.index("\n\n\nclass BeliefLifecycle:", start)
text = text[:start] + text[end + 2 :]
text = text.replace(
    '''    EvidenceSide,
    belief_stream_id,
)
''',
    '''    EvidenceSide,
    belief_status_requires_evidence_gate,
    belief_status_transition_allowed,
    belief_stream_id,
)
''',
    1,
)
text = text.replace(
    '''        if new_status is BeliefStatus.SUPPORTED:
            return self._reject(
                command,
                belief_id,
                state,
                BeliefRejectionCode.EVIDENCE_GATE_REQUIRED,
                "supported status requires the separately reviewed P0-015 Evidence Gate",
            )
        if new_status != current_status and new_status not in _ALLOWED_TRANSITIONS[current_status]:
''',
    '''        if belief_status_requires_evidence_gate(new_status):
            return self._reject(
                command,
                belief_id,
                state,
                BeliefRejectionCode.EVIDENCE_GATE_REQUIRED,
                f"{new_status.value} status requires the separately reviewed "
                "P0-015 Evidence Gate",
            )
        if not belief_status_transition_allowed(current_status, new_status):
''',
    1,
)
old_known = '''        known_contradictions = {
            str(item["contradiction_id"])
            for item in _object_sequence(state.get("contradictions"))
        }
'''
new_known = '''        contradiction_objects = _object_sequence(state.get("contradictions"))
        known_contradictions = {
            str(item["contradiction_id"])
            for item in contradiction_objects
        }
        open_contradictions = {
            str(item["contradiction_id"])
            for item in contradiction_objects
            if item.get("addressed_in_revision") is None
        }
'''
if text.count(old_known) != 1:
    raise RuntimeError("lifecycle contradiction marker mismatch")
text = text.replace(old_known, new_known, 1)
transition_marker = '''        if not belief_status_transition_allowed(current_status, new_status):
            return self._reject(
                command,
                belief_id,
                state,
                BeliefRejectionCode.INVALID_STATUS_TRANSITION,
                f"transition {current_status.value} → {new_status.value} is not allowed",
            )
'''
transition_new = transition_marker + '''        if (
            current_status is BeliefStatus.CONTESTED
            and new_status not in {BeliefStatus.CONTESTED, BeliefStatus.UNRESOLVED}
            and not open_contradictions.issubset(set(contradiction_ids))
        ):
            return self._reject(
                command,
                belief_id,
                state,
                BeliefRejectionCode.UNKNOWN_CONTRADICTION,
                "leaving contested status requires addressing every open contradiction",
            )
'''
if text.count(transition_marker) != 1:
    raise RuntimeError("lifecycle transition marker mismatch")
text = text.replace(transition_marker, transition_new, 1)
lifecycle.write_text(text, encoding="utf-8")

reducer = Path("src/mentaury/beliefs/reducer.py")
text = reducer.read_text(encoding="utf-8")
text = text.replace(
    '''    EvidenceSide,
)
''',
    '''    EvidenceSide,
    belief_status_requires_evidence_gate,
    belief_status_transition_allowed,
)
''',
    1,
)
text = text.replace(
    '''        _require_existing(state, payload)
        evidence_ref = _string(payload, "evidence_ref")
''',
    '''        _require_existing(state, payload)
        _require_non_terminal(state)
        evidence_ref = _string(payload, "evidence_ref")
''',
    1,
)
text = text.replace(
    '''        _require_existing(state, payload)
        contradiction_id = _string(payload, "contradiction_id")
''',
    '''        _require_existing(state, payload)
        _require_non_terminal(state)
        contradiction_id = _string(payload, "contradiction_id")
''',
    1,
)
text = text.replace(
    '''        if previous_status.value != _string(state, "status"):
            raise BeliefReducerError("previous_status does not match projection")

        evidence_refs = list(_strings(payload, "evidence_refs"))
''',
    '''        if previous_status.value != _string(state, "status"):
            raise BeliefReducerError("previous_status does not match projection")
        _require_non_terminal(state)

        evidence_refs = list(_strings(payload, "evidence_refs"))
''',
    1,
)
text = text.replace(
    '''        known = {str(item["contradiction_id"]) for item in contradictions}
        if not addressed.issubset(known):
            raise BeliefReducerError("revision references unknown contradiction")
''',
    '''        known = {str(item["contradiction_id"]) for item in contradictions}
        open_contradictions = {
            str(item["contradiction_id"])
            for item in contradictions
            if item["addressed_in_revision"] is None
        }
        if not addressed.issubset(known):
            raise BeliefReducerError("revision references unknown contradiction")
''',
    1,
)
text = text.replace(
    '''        if new_status is BeliefStatus.SUPPORTED:
            raise BeliefReducerError(
                "supported status requires a future Evidence Gate receipt"
            )
        history = [dict(item) for item in _objects(state, "history")]
''',
    '''        if belief_status_requires_evidence_gate(new_status):
            raise BeliefReducerError(
                f"{new_status.value} status requires a future Evidence Gate receipt"
            )
        if not belief_status_transition_allowed(previous_status, new_status):
            raise BeliefReducerError(
                f"transition {previous_status.value} → {new_status.value} is not allowed"
            )
        if (
            previous_status is BeliefStatus.CONTESTED
            and new_status not in {BeliefStatus.CONTESTED, BeliefStatus.UNRESOLVED}
            and not open_contradictions.issubset(addressed)
        ):
            raise BeliefReducerError(
                "leaving contested status requires addressing every open contradiction"
            )
        if (
            new_statement == previous_statement
            and new_status is previous_status
            and not addressed
        ):
            raise BeliefReducerError("belief revision has no effect")
        history = [dict(item) for item in _objects(state, "history")]
''',
    1,
)
helper_marker = '''
def _require_existing(state: FrozenPayload, payload: FrozenPayload) -> None:
'''
helper = '''
def _require_non_terminal(state: FrozenPayload) -> None:
    status = BeliefStatus(_string(state, "status"))
    if status is BeliefStatus.SUPERSEDED:
        raise BeliefReducerError("superseded belief is terminal")
    if belief_status_requires_evidence_gate(status):
        raise BeliefReducerError(
            "P0-014 cannot continue from an Evidence Gate-owned status"
        )


def _require_existing(state: FrozenPayload, payload: FrozenPayload) -> None:
'''
if text.count(helper_marker) != 1:
    raise RuntimeError("reducer helper marker mismatch")
text = text.replace(helper_marker, helper, 1)
reducer.write_text(text, encoding="utf-8")

tests = Path("tests/test_belief_lifecycle.py")
text = tests.read_text(encoding="utf-8")
text = text.replace(
    '''    BeliefReducer,
    BeliefRejectionCode,
''',
    '''    BeliefReducer,
    BeliefReducerError,
    BeliefRejectionCode,
''',
    1,
)
text = text.replace(
    '''    with pytest.raises(
        Exception,
        match="Evidence Gate",
    ):
''',
    '''    with pytest.raises(
        BeliefReducerError,
        match="Evidence Gate",
    ):
''',
    1,
)
append = '''


def test_contradicted_status_requires_future_evidence_gate() -> None:
    state = _state_with_evidence()
    decision = BeliefLifecycle().decide(
        _command(
            REVISE_BELIEF,
            {
                "belief_id": BELIEF_ID,
                "expected_revision": 1,
                "new_statement": "Claim rejected by stronger evidence.",
                "new_status": BeliefStatus.CONTRADICTED.value,
                "reason": "epistemic status requires gate",
                "evidence_refs": ["evidence:for:1"],
                "addressed_contradiction_ids": [],
            },
            expected_stream_version=2,
        ),
        state,
    )

    assert not decision.accepted
    assert decision.rejection_code is BeliefRejectionCode.EVIDENCE_GATE_REQUIRED


def test_leaving_contested_requires_addressing_all_open_contradictions() -> None:
    state = _state_with_evidence()
    contradiction = BeliefLifecycle().decide(
        _command(
            REGISTER_CONTRADICTION,
            {
                "belief_id": BELIEF_ID,
                "contradiction_id": "contradiction:open",
                "statement": "Context remains disputed.",
                "evidence_refs": ["evidence:for:1"],
            },
            expected_stream_version=2,
        ),
        state,
    )
    assert contradiction.accepted
    state = _apply(state, contradiction.domain_events[0], 3, "EVT-OPEN-CONTRADICTION")

    decision = BeliefLifecycle().decide(
        _command(
            REVISE_BELIEF,
            {
                "belief_id": BELIEF_ID,
                "expected_revision": 1,
                "new_statement": "Prematurely cleared claim.",
                "new_status": BeliefStatus.PROVISIONAL.value,
                "reason": "attempted contradiction bypass",
                "evidence_refs": ["evidence:for:1"],
                "addressed_contradiction_ids": [],
            },
            expected_stream_version=3,
        ),
        state,
    )

    assert not decision.accepted
    assert decision.rejection_code is BeliefRejectionCode.UNKNOWN_CONTRADICTION


def test_reducer_enforces_terminal_and_transition_policy_on_direct_events() -> None:
    state = _state_with_evidence()
    supersede = BeliefLifecycle().decide(
        _command(
            REVISE_BELIEF,
            {
                "belief_id": BELIEF_ID,
                "expected_revision": 1,
                "new_statement": "Terminal replacement.",
                "new_status": BeliefStatus.SUPERSEDED.value,
                "reason": "replacement",
                "evidence_refs": ["evidence:for:1"],
                "addressed_contradiction_ids": [],
            },
            expected_stream_version=2,
        ),
        state,
    )
    assert supersede.accepted
    state = _apply(state, supersede.domain_events[0], 3, "EVT-DIRECT-TERMINAL")
    direct_evidence = PendingEvent(
        "EVIDENCE_ATTACHED",
        "evidence-attached/v1",
        True,
        {
            "belief_id": BELIEF_ID,
            "evidence_ref": "evidence:after-terminal",
            "side": EvidenceSide.FOR.value,
        },
    )

    with pytest.raises(BeliefReducerError, match="terminal"):
        _apply(state, direct_evidence, 4, "EVT-AFTER-TERMINAL")


def test_reducer_rejects_direct_no_effect_revision() -> None:
    state = _state_with_evidence()
    pending = PendingEvent(
        "BELIEF_REVISED",
        "belief-revised/v1",
        True,
        {
            "belief_id": BELIEF_ID,
            "previous_revision": 1,
            "new_revision": 2,
            "previous_statement": state["statement"],
            "new_statement": state["statement"],
            "previous_status": state["status"],
            "new_status": state["status"],
            "reason": "direct no-op",
            "evidence_refs": ["evidence:for:1"],
            "addressed_contradiction_ids": [],
        },
    )

    with pytest.raises(BeliefReducerError, match="no effect"):
        _apply(state, pending, 3, "EVT-DIRECT-NOOP")
'''
if "test_contradicted_status_requires_future_evidence_gate" in text:
    raise RuntimeError("reducer-policy tests already present")
tests.write_text(text + append, encoding="utf-8")

doc = Path("docs/P0_014_MINIMAL_BELIEF_LIFECYCLE.md")
replace_once(
    doc,
    '''`supported` exists in the shared status vocabulary but is deliberately unreachable
in P0-014. Both the lifecycle decision and reducer reject a direct transition to
`supported` until P0-015 defines a governed Evidence Gate receipt and event contract.
''',
    '''`supported` and `contradicted` exist in the shared status vocabulary but are
deliberately unreachable in P0-014. Both the lifecycle decision and reducer reject
a direct transition to either status until P0-015 defines a governed Evidence
Gate receipt and event contract.
''',
)
replace_once(
    doc,
    '''Revisions never erase earlier statement/status history. Addressed
contradictions remain visible with the revision that addressed them.
''',
    '''Revisions never erase earlier statement/status history. Addressed
contradictions remain visible with the revision that addressed them. Leaving
`contested` for a non-contested/non-unresolved status requires every open
contradiction to be explicitly addressed by that revision.
''',
)
replace_once(
    doc,
    '''P0-014 therefore rejects `supported` through `EVIDENCE_GATE_REQUIRED`; a caller
cannot bypass this by appending a direct `BELIEF_REVISED` event because the v1
reducer rejects the same transition without a future gate receipt.
''',
    '''P0-014 therefore rejects `supported` and `contradicted` through
`EVIDENCE_GATE_REQUIRED`; a caller cannot bypass this by appending a direct
`BELIEF_REVISED` event because the v1 reducer enforces the same status, terminal,
open-contradiction and no-effect policy.
''',
)
