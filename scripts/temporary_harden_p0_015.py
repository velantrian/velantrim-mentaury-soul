from __future__ import annotations

from pathlib import Path


def replace_once(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{path}: expected one marker, found {count}: {old!r}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


contracts = Path("src/mentaury/evidence/contracts.py")
replace_once(
    contracts,
    "allowed_claim_types=(ClaimType.CONTEXTUAL, ClaimType.UNSPECIFIED),",
    "allowed_claim_types=(ClaimType.CONTEXTUAL,),",
)

gate = Path("src/mentaury/evidence/gate.py")
replace_once(
    gate,
    "from .contracts import (\n",
    "MAX_EVIDENCE_RECORDS = 256\n\n\nfrom .contracts import (\n",
)
replace_once(
    gate,
    '''        if not snapshotted or any(
            not isinstance(record, EvidenceRecord) for record in snapshotted
        ):
            raise TypeError("records must contain EvidenceRecord values")
''',
    '''        if not snapshotted or any(
            not isinstance(record, EvidenceRecord) for record in snapshotted
        ):
            raise TypeError("records must contain EvidenceRecord values")
        if len(snapshotted) > MAX_EVIDENCE_RECORDS:
            raise EvidenceGateError(
                f"evidence gate accepts at most {MAX_EVIDENCE_RECORDS} records"
            )
''',
)
replace_once(
    gate,
    '''        passes_for = len(groups_for) >= policy.minimum_source_groups_for
        passes_against = len(groups_against) >= policy.minimum_source_groups_against
        if passes_for and passes_against:
            outcome = EvidenceGateOutcome.CONFLICT
        elif passes_for:
            outcome = EvidenceGateOutcome.SUPPORTED
        elif passes_against:
            outcome = EvidenceGateOutcome.CONTRADICTED
        else:
            outcome = EvidenceGateOutcome.INCONCLUSIVE
''',
    '''        passes_for = len(groups_for) >= policy.minimum_source_groups_for
        passes_against = len(groups_against) >= policy.minimum_source_groups_against
        has_for = bool(groups_for)
        has_against = bool(groups_against)
        if has_for and has_against:
            outcome = EvidenceGateOutcome.CONFLICT
        elif passes_for:
            outcome = EvidenceGateOutcome.SUPPORTED
        elif passes_against:
            outcome = EvidenceGateOutcome.CONTRADICTED
        else:
            outcome = EvidenceGateOutcome.INCONCLUSIVE
''',
)

exports = Path("src/mentaury/evidence/__init__.py")
replace_once(
    exports,
    "from .gate import EvidenceGate, EvidenceGateError, policy_from_value, records_from_value",
    '''from .gate import (
    MAX_EVIDENCE_RECORDS,
    EvidenceGate,
    EvidenceGateError,
    policy_from_value,
    records_from_value,
)''',
)
replace_once(exports, '    "EvidenceGate",\n', '    "MAX_EVIDENCE_RECORDS",\n    "EvidenceGate",\n')

lifecycle = Path("src/mentaury/beliefs/evidence_gate.py")
replace_once(
    lifecycle,
    '''        if not isinstance(policies, EvidenceGatePolicyRegistry):
            raise TypeError("policies must be an EvidenceGatePolicyRegistry")
        self._gate = gate or EvidenceGate()
''',
    '''        if gate is not None and not isinstance(gate, EvidenceGate):
            raise TypeError("gate must be an EvidenceGate or None")
        if not isinstance(policies, EvidenceGatePolicyRegistry):
            raise TypeError("policies must be an EvidenceGatePolicyRegistry")
        self._gate = gate or EvidenceGate()
''',
)

reducer = Path("src/mentaury/beliefs/gated_reducer.py")
replace_once(
    reducer,
    "from .contracts import BeliefStatus, ClaimType",
    "from .contracts import BeliefStatus, ClaimType, belief_stream_id",
)
replace_once(
    reducer,
    '''        if not isinstance(policies, EvidenceGatePolicyRegistry):
            raise TypeError("policies must be an EvidenceGatePolicyRegistry")
        self._gate = gate or EvidenceGate()
''',
    '''        if gate is not None and not isinstance(gate, EvidenceGate):
            raise TypeError("gate must be an EvidenceGate or None")
        if not isinstance(policies, EvidenceGatePolicyRegistry):
            raise TypeError("policies must be an EvidenceGatePolicyRegistry")
        self._gate = gate or EvidenceGate()
''',
)
replace_once(
    reducer,
    '''        belief_id = _state_string(state, "belief_id")
        if _payload_string(payload, "belief_id") != belief_id:
''',
    '''        belief_id = _state_string(state, "belief_id")
        if event.stream_id != belief_stream_id(belief_id):
            raise BeliefReducerError("gate event stream_id does not match belief")
        if not event.affects_domain_state:
            raise BeliefReducerError("gate event must affect domain state")
        if _payload_string(payload, "belief_id") != belief_id:
''',
)

tests = Path("tests/test_evidence_gate.py")
test_text = tests.read_text(encoding="utf-8")
if "test_mixed_qualifying_evidence_fails_closed_as_conflict" in test_text:
    raise RuntimeError("P0-015 hardening tests already present")
test_text = test_text.replace(
    "    EVIDENCE_GATE_REJECTED,\n",
    "    EVIDENCE_GATE_REJECTED,\n    MAX_EVIDENCE_RECORDS,\n",
    1,
)
test_text = test_text.replace(
    '"allowed_claim_types": (ClaimType.CONTEXTUAL, ClaimType.UNSPECIFIED),',
    '"allowed_claim_types": (ClaimType.CONTEXTUAL,),',
    1,
)
test_text += '''


def test_mixed_qualifying_evidence_fails_closed_as_conflict() -> None:
    records = (
        _record("evidence:for:1", EvidenceSide.FOR, "source:for-a"),
        _record("evidence:for:2", EvidenceSide.FOR, "source:for-b"),
        _record("evidence:against:1", EvidenceSide.AGAINST, "source:against-a"),
    )
    receipt = EvidenceGate().evaluate(
        belief_id=BELIEF_ID,
        belief_revision=1,
        claim_type=ClaimType.CONTEXTUAL,
        statement="A contextual claim with credible opposition.",
        evidence_for=("evidence:for:1", "evidence:for:2"),
        evidence_against=("evidence:against:1",),
        records=records,
        policy=P0_015_CONTEXTUAL_POLICY,
        evaluated_at=EVALUATED_AT,
    )

    assert receipt.outcome is EvidenceGateOutcome.CONFLICT
    assert receipt.source_groups_for == ("source:for-a", "source:for-b")
    assert receipt.source_groups_against == ("source:against-a",)


def test_unspecified_claims_require_classification_before_gate() -> None:
    state = _support_state(ClaimType.UNSPECIFIED)
    records = (
        _record("evidence:for:1", EvidenceSide.FOR, "source:a"),
        _record("evidence:for:2", EvidenceSide.FOR, "source:b"),
    )
    decision = EvidenceGatedBeliefLifecycle().decide(
        _gate_command(state, records), state
    )

    assert not decision.accepted
    assert decision.rejection_code is EvidenceGateRejectionCode.CLAIM_TYPE_NOT_ALLOWED
    assert decision.audit_event is not None
    assert not decision.audit_event.affects_domain_state


def test_gate_enforces_record_budget() -> None:
    refs = tuple(f"evidence:for:{index}" for index in range(MAX_EVIDENCE_RECORDS + 1))
    records = tuple(
        _record(ref, EvidenceSide.FOR, f"source:{index}")
        for index, ref in enumerate(refs)
    )

    with pytest.raises(EvidenceGateError, match="at most"):
        EvidenceGate().evaluate(
            belief_id=BELIEF_ID,
            belief_revision=1,
            claim_type=ClaimType.CONTEXTUAL,
            statement="Oversized evidence set.",
            evidence_for=refs,
            evidence_against=(),
            records=records,
            policy=P0_015_CONTEXTUAL_POLICY,
            evaluated_at=EVALUATED_AT,
        )


def test_reducer_binds_gate_event_to_stream_and_state_flag() -> None:
    state = _support_state()
    records = (
        _record("evidence:for:1", EvidenceSide.FOR, "source:a"),
        _record("evidence:for:2", EvidenceSide.FOR, "source:b"),
    )
    decision = EvidenceGatedBeliefLifecycle().decide(
        _gate_command(state, records), state
    )
    assert decision.accepted
    pending = decision.domain_events[0]
    event = _event(pending, 4, "EVT-GATE-BOUNDARY")
    gated_reducer = EvidenceGatedBeliefReducer()

    with pytest.raises(BeliefReducerError, match="stream_id"):
        gated_reducer.apply(
            state,
            replace(event, stream_id="belief:another-belief"),
            pending.payload,
        )
    with pytest.raises(BeliefReducerError, match="affect domain state"):
        gated_reducer.apply(
            state,
            replace(event, affects_domain_state=False),
            pending.payload,
        )
'''
tests.write_text(test_text, encoding="utf-8")

doc = Path("docs/P0_015_EVIDENCE_GATE.md")
replace_once(doc, "allowed claim types: contextual, unspecified", "allowed claim types: contextual")
replace_once(
    doc,
    '''Causal, statistical, universal and existential claims remain ungated until a
separate reviewed policy defines the necessary method-specific requirements.
''',
    '''Unspecified, causal, statistical, universal and existential claims remain ungated
until the claim is classified and a separate reviewed policy defines the
necessary method-specific requirements.
''',
)
replace_once(
    doc,
    '''maximum age: 86400 seconds
```''',
    '''maximum age: 86400 seconds
maximum records per evaluation: 256
```''',
)
replace_once(
    doc,
    '''for side passes, against does not  → supported
against side passes, for does not  → contradicted
both sides pass                     → conflict, no state mutation
neither side passes                 → inconclusive, no state mutation
''',
    '''for side passes, no qualifying against evidence     → supported
against side passes, no qualifying for evidence     → contradicted
both sides contain qualifying evidence               → conflict, no state mutation
neither side reaches its threshold                   → inconclusive, no state mutation
''',
)
replace_once(
    doc,
    "source-group deduplication\n",
    "source-group deduplication\nmixed qualifying evidence fails closed as conflict\nrecord-count budget\n",
)
