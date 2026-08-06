from __future__ import annotations

from pathlib import Path


def replace_once(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{path}: expected one marker, found {count}: {old!r}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


contracts = Path("src/mentaury/beliefs/contracts.py")
replace_once(
    contracts,
    '''    INVALID_STATUS_TRANSITION = "INVALID_STATUS_TRANSITION"
    NO_EFFECT = "NO_EFFECT"
''',
    '''    INVALID_STATUS_TRANSITION = "INVALID_STATUS_TRANSITION"
    EVIDENCE_GATE_REQUIRED = "EVIDENCE_GATE_REQUIRED"
    NO_EFFECT = "NO_EFFECT"
''',
)

schemas = Path("src/mentaury/beliefs/schemas.py")
replace_once(
    schemas,
    '''                        "expected_revision": IntegerSpec(minimum=0),
                        "current_revision": IntegerSpec(minimum=0),
''',
    '''                        "expected_stream_version": IntegerSpec(minimum=0),
                        "current_belief_revision": IntegerSpec(minimum=0),
                        "requested_belief_revision": IntegerSpec(minimum=0),
''',
)
replace_once(
    schemas,
    '''                            "expected_revision",
                            "current_revision",
''',
    '''                            "expected_stream_version",
                            "current_belief_revision",
                            "requested_belief_revision",
''',
)

lifecycle = Path("src/mentaury/beliefs/lifecycle.py")
replace_once(
    lifecycle,
    '''        current_status = _status(state)
        if new_status != current_status and new_status not in _ALLOWED_TRANSITIONS[current_status]:
''',
    '''        current_status = _status(state)
        if new_status is BeliefStatus.SUPPORTED:
            return self._reject(
                command,
                belief_id,
                state,
                BeliefRejectionCode.EVIDENCE_GATE_REQUIRED,
                "supported status requires the separately reviewed P0-015 Evidence Gate",
            )
        if new_status != current_status and new_status not in _ALLOWED_TRANSITIONS[current_status]:
''',
)
replace_once(
    lifecycle,
    '''        current_revision = _revision(state)
        event_type = (
''',
    '''        current_revision = _revision(state)
        requested_revision = command.payload.get("expected_revision", 0)
        if isinstance(requested_revision, bool) or not isinstance(
            requested_revision,
            int,
        ) or requested_revision < 0:
            requested_revision = 0
        event_type = (
''',
)
replace_once(
    lifecycle,
    '''                "expected_revision": command.expected_stream_version,
                "current_revision": current_revision,
''',
    '''                "expected_stream_version": command.expected_stream_version,
                "current_belief_revision": current_revision,
                "requested_belief_revision": requested_revision,
''',
)

reducer = Path("src/mentaury/beliefs/reducer.py")
replace_once(
    reducer,
    '''        new_statement = _string(payload, "new_statement")
        new_status = _enum_value(BeliefStatus, payload, "new_status")
        history = [dict(item) for item in _objects(state, "history")]
''',
    '''        new_statement = _string(payload, "new_statement")
        new_status = _enum_value(BeliefStatus, payload, "new_status")
        if new_status is BeliefStatus.SUPPORTED:
            raise BeliefReducerError(
                "supported status requires a future Evidence Gate receipt"
            )
        history = [dict(item) for item in _objects(state, "history")]
''',
)

tests = Path("tests/test_belief_lifecycle.py")
text = tests.read_text(encoding="utf-8")
text = text.replace(
    '"new_status": BeliefStatus.SUPPORTED.value,\n                "reason": "scope clarified",',
    '"new_status": BeliefStatus.PROVISIONAL.value,\n                "reason": "scope clarified",',
    1,
)
text = text.replace(
    'assert projected["status"] == BeliefStatus.SUPPORTED.value',
    'assert projected["status"] == BeliefStatus.PROVISIONAL.value',
    1,
)
append = '''


def test_supported_status_requires_future_evidence_gate() -> None:
    state = _state_with_evidence()
    decision = BeliefLifecycle().decide(
        _command(
            REVISE_BELIEF,
            {
                "belief_id": BELIEF_ID,
                "expected_revision": 1,
                "new_statement": "Structurally supported claim.",
                "new_status": BeliefStatus.SUPPORTED.value,
                "reason": "attached reference is not yet governed evidence",
                "evidence_refs": ["evidence:for:1"],
                "addressed_contradiction_ids": [],
            },
            expected_stream_version=2,
        ),
        state,
    )

    assert not decision.accepted
    assert decision.rejection_code is BeliefRejectionCode.EVIDENCE_GATE_REQUIRED
    assert decision.audit_event is not None
    assert not decision.audit_event.affects_domain_state


def test_reducer_rejects_supported_revision_without_gate_receipt() -> None:
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
            "new_statement": "Unsupported direct committed revision.",
            "previous_status": state["status"],
            "new_status": BeliefStatus.SUPPORTED.value,
            "reason": "forged direct event",
            "evidence_refs": ["evidence:for:1"],
            "addressed_contradiction_ids": [],
        },
    )

    with pytest.raises(
        Exception,
        match="Evidence Gate",
    ):
        _apply(state, pending, 3, "EVT-FORGED-SUPPORTED")


def test_rejection_audit_distinguishes_stream_and_belief_revisions() -> None:
    state = _state_with_evidence()
    decision = BeliefLifecycle().decide(
        _command(
            REVISE_BELIEF,
            {
                "belief_id": BELIEF_ID,
                "expected_revision": 99,
                "new_statement": "Revised claim",
                "new_status": BeliefStatus.PROVISIONAL.value,
                "reason": "stale belief revision",
                "evidence_refs": ["evidence:for:1"],
                "addressed_contradiction_ids": [],
            },
            expected_stream_version=17,
            command_id="CMD-REVISION-AUDIT-FIELDS",
        ),
        state,
    )

    assert not decision.accepted
    assert decision.audit_event is not None
    payload = decision.audit_event.payload
    assert payload["expected_stream_version"] == 17
    assert payload["current_belief_revision"] == 1
    assert payload["requested_belief_revision"] == 99
'''
if "test_supported_status_requires_future_evidence_gate" in text:
    raise RuntimeError("P0-014 evidence boundary tests already present")
tests.write_text(text + append, encoding="utf-8")

doc = Path("docs/P0_014_MINIMAL_BELIEF_LIFECYCLE.md")
replace_once(
    doc,
    '''`superseded` is terminal for this minimal lifecycle. A later lifecycle may add a
separate reactivation event only through a new reviewed specification.
''',
    '''`supported` exists in the shared status vocabulary but is deliberately unreachable
in P0-014. Both the lifecycle decision and reducer reject a direct transition to
`supported` until P0-015 defines a governed Evidence Gate receipt and event contract.

`superseded` is terminal for this minimal lifecycle. A later lifecycle may add a
separate reactivation event only through a new reviewed specification.
''',
)
replace_once(
    doc,
    '''- whether a belief deserves `supported` status.

Those controls belong to **P0-015 Evidence Gate**. Therefore:
''',
    '''- whether a belief deserves `supported` status.

P0-014 therefore rejects `supported` through `EVIDENCE_GATE_REQUIRED`; a caller
cannot bypass this by appending a direct `BELIEF_REVISED` event because the v1
reducer rejects the same transition without a future gate receipt.

Those controls belong to **P0-015 Evidence Gate**. Therefore:
''',
)
replace_once(
    doc,
    '''The pure lifecycle does not persist audit events automatically. The caller must
make a separate explicit append decision. Therefore a rejected command cannot
silently mutate domain state.
''',
    '''The pure lifecycle does not persist audit events automatically. The caller must
make a separate explicit append decision. Therefore a rejected command cannot
silently mutate domain state.

Audit payloads distinguish three concurrency concepts rather than conflating
them: `expected_stream_version` from the storage CAS envelope,
`current_belief_revision` from the projection and
`requested_belief_revision` from a revision command payload.
''',
)
