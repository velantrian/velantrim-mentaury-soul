"""P0-014 minimal belief lifecycle decisions, projection and R1 integration."""

from __future__ import annotations

from dataclasses import replace

import pytest

from mentaury.beliefs import (
    ATTACH_EVIDENCE,
    BELIEF_REVISION_REJECTED,
    CREATE_BELIEF,
    REGISTER_CONTRADICTION,
    REVISE_BELIEF,
    BeliefLifecycle,
    BeliefReducer,
    BeliefReducerError,
    BeliefRejectionCode,
    BeliefStatus,
    ClaimType,
    EvidenceSide,
    belief_schema_definitions,
    belief_stream_id,
)
from mentaury.contracts import (
    ActorRef,
    AuthorityRef,
    CommandEnvelope,
    EventEnvelope,
    PendingEvent,
    ProducerRef,
)
from mentaury.contracts.primitives import freeze_payload
from mentaury.replay import (
    R1ReplayVerifier,
    ReplayStateBudget,
    make_replay_snapshot,
)
from mentaury.storage import SQLiteEventPayloadStore, VerificationBudget
from mentaury.validation import SchemaRegistry


BELIEF_ID = "belief-001"
STREAM_ID = belief_stream_id(BELIEF_ID)


def _command(
    command_type: str,
    payload: dict[str, object],
    *,
    expected_stream_version: int = 0,
    command_id: str | None = None,
    target_stream: str = STREAM_ID,
) -> CommandEnvelope:
    return CommandEnvelope(
        command_id=command_id or f"CMD-{command_type}",
        command_type=command_type,
        command_schema=f"{command_type.lower().replace('_', '-')}/v1",
        target_stream=target_stream,
        expected_stream_version=expected_stream_version,
        issued_at="2026-08-06T00:00:00Z",
        issuer=ActorRef("operator", "operator:primary"),
        authority=AuthorityRef("CAP-BELIEF", 1),
        correlation_id="CORR-BELIEF",
        idempotency_key=f"IDEMP-{command_id or command_type}",
        payload=payload,
    )


def _create_command() -> CommandEnvelope:
    return _command(
        CREATE_BELIEF,
        {
            "belief_id": BELIEF_ID,
            "statement": "Water boils near 100°C at standard pressure.",
            "claim_type": ClaimType.CONTEXTUAL.value,
        },
    )


def _empty_state():
    return freeze_payload(BeliefReducer().initial_state())


def _event(
    pending: PendingEvent,
    version: int,
    event_id: str,
) -> EventEnvelope:
    return EventEnvelope(
        event_id=event_id,
        event_type=pending.event_type,
        envelope_schema_version=1,
        payload_schema=pending.payload_schema,
        stream_id=STREAM_ID,
        stream_version=version,
        batch_id=f"BATCH-{event_id}",
        batch_index=0,
        batch_size=1,
        occurred_at="2026-08-06T00:00:00Z",
        recorded_at="2026-08-06T00:00:00Z",
        producer=ProducerRef("belief-test", "0.1.0"),
        initiator=ActorRef("operator", "operator:primary"),
        authority=AuthorityRef("CAP-BELIEF", 1),
        causation_id=f"CMD-{event_id}",
        correlation_id="CORR-BELIEF",
        affects_domain_state=pending.affects_domain_state,
        payload_digest="sha256:untrusted",
        payload_ref=f"PAYLOAD-{event_id}",
        previous_hash="sha256:untrusted",
        event_hash="sha256:untrusted",
    )


def _apply(state, pending: PendingEvent, version: int, event_id: str):
    return freeze_payload(
        BeliefReducer().apply(
            state,
            _event(pending, version, event_id),
            pending.payload,
        )
    )


def _created_state():
    decision = BeliefLifecycle().decide(_create_command(), _empty_state())
    assert decision.accepted
    return _apply(_empty_state(), decision.domain_events[0], 1, "EVT-CREATED")


def _attach_command(
    evidence_ref: str,
    side: EvidenceSide = EvidenceSide.FOR,
    *,
    version: int = 1,
) -> CommandEnvelope:
    return _command(
        ATTACH_EVIDENCE,
        {
            "belief_id": BELIEF_ID,
            "evidence_ref": evidence_ref,
            "side": side.value,
            "note": "structural reference only",
        },
        expected_stream_version=version,
        command_id=f"CMD-ATTACH-{evidence_ref}",
    )


def _state_with_evidence():
    state = _created_state()
    decision = BeliefLifecycle().decide(_attach_command("evidence:for:1"), state)
    assert decision.accepted
    return _apply(state, decision.domain_events[0], 2, "EVT-EVIDENCE-FOR")


def _state_with_status(status: BeliefStatus):
    """Build a belief projection pinned at an arbitrary status.

    This does not go through the real P0-015 Evidence Gate; it directly
    overrides the projected status the way a hand-built forged event would,
    which is the same pattern already used by the reducer-level tests below
    (e.g. ``test_reducer_rejects_supported_revision_without_gate_receipt``).
    It lets lifecycle-boundary tests exercise every ``BeliefStatus`` without
    needing the evidence-gate machinery.
    """

    state = _state_with_evidence()
    plain = dict(state)
    plain["status"] = status.value
    return freeze_payload(plain)


def test_create_belief_starts_at_hypothesis_revision_one() -> None:
    decision = BeliefLifecycle().decide(_create_command(), _empty_state())

    assert decision.accepted
    event = decision.domain_events[0]
    assert event.payload["status"] == BeliefStatus.HYPOTHESIS.value
    assert event.payload["revision"] == 1
    assert event.affects_domain_state


def test_target_stream_mismatch_is_audited_without_domain_mutation() -> None:
    decision = BeliefLifecycle().decide(
        _command(
            CREATE_BELIEF,
            {
                "belief_id": BELIEF_ID,
                "statement": "claim",
                "claim_type": ClaimType.UNSPECIFIED.value,
            },
            target_stream="belief:wrong",
        ),
        _empty_state(),
    )

    assert not decision.accepted
    assert decision.domain_events == ()
    assert decision.rejection_code is BeliefRejectionCode.TARGET_STREAM_MISMATCH
    assert decision.audit_event is not None
    assert not decision.audit_event.affects_domain_state


def test_duplicate_create_is_rejected() -> None:
    decision = BeliefLifecycle().decide(_create_command(), _created_state())

    assert not decision.accepted
    assert decision.rejection_code is BeliefRejectionCode.BELIEF_ALREADY_EXISTS


def test_attach_evidence_is_explicit_and_side_aware() -> None:
    decision = BeliefLifecycle().decide(
        _attach_command("evidence:against:1", EvidenceSide.AGAINST),
        _created_state(),
    )

    assert decision.accepted
    assert decision.domain_events[0].payload["side"] == EvidenceSide.AGAINST.value


def test_duplicate_evidence_is_rejected_across_sides() -> None:
    state = _state_with_evidence()
    decision = BeliefLifecycle().decide(
        _attach_command("evidence:for:1", EvidenceSide.AGAINST, version=2),
        state,
    )

    assert not decision.accepted
    assert decision.rejection_code is BeliefRejectionCode.DUPLICATE_EVIDENCE


def test_contradiction_requires_attached_evidence() -> None:
    decision = BeliefLifecycle().decide(
        _command(
            REGISTER_CONTRADICTION,
            {
                "belief_id": BELIEF_ID,
                "contradiction_id": "contradiction:1",
                "statement": "Pressure differs from the assumed context.",
                "evidence_refs": ["evidence:missing"],
            },
            expected_stream_version=1,
        ),
        _created_state(),
    )

    assert not decision.accepted
    assert decision.rejection_code is BeliefRejectionCode.UNKNOWN_EVIDENCE_REF


def test_registered_contradiction_moves_projection_to_contested() -> None:
    state = _state_with_evidence()
    command = _command(
        REGISTER_CONTRADICTION,
        {
            "belief_id": BELIEF_ID,
            "contradiction_id": "contradiction:1",
            "statement": "Boiling point depends on atmospheric pressure.",
            "evidence_refs": ["evidence:for:1"],
        },
        expected_stream_version=2,
    )
    decision = BeliefLifecycle().decide(command, state)
    assert decision.accepted

    projected = _apply(state, decision.domain_events[0], 3, "EVT-CONTRADICTION")

    assert projected["status"] == BeliefStatus.CONTESTED.value
    assert projected["revision"] == 1
    assert projected["contradictions"][0]["addressed_in_revision"] is None


def test_duplicate_contradiction_id_is_rejected() -> None:
    state = _state_with_evidence()
    command = _command(
        REGISTER_CONTRADICTION,
        {
            "belief_id": BELIEF_ID,
            "contradiction_id": "contradiction:1",
            "statement": "Pressure context differs.",
            "evidence_refs": ["evidence:for:1"],
        },
        expected_stream_version=2,
    )
    first = BeliefLifecycle().decide(command, state)
    assert first.accepted
    state = _apply(state, first.domain_events[0], 3, "EVT-CONTRADICTION")

    duplicate = BeliefLifecycle().decide(
        replace(command, command_id="CMD-CONTRADICTION-2", expected_stream_version=3),
        state,
    )

    assert not duplicate.accepted
    assert duplicate.rejection_code is BeliefRejectionCode.DUPLICATE_CONTRADICTION


def test_revision_conflict_is_audited_as_revision_rejection() -> None:
    state = _state_with_evidence()
    decision = BeliefLifecycle().decide(
        _command(
            REVISE_BELIEF,
            {
                "belief_id": BELIEF_ID,
                "expected_revision": 99,
                "new_statement": "Revised claim",
                "new_status": BeliefStatus.PROVISIONAL.value,
                "reason": "new evidence",
                "evidence_refs": ["evidence:for:1"],
                "addressed_contradiction_ids": [],
            },
            expected_stream_version=2,
        ),
        state,
    )

    assert not decision.accepted
    assert decision.rejection_code is BeliefRejectionCode.REVISION_CONFLICT
    assert decision.audit_event is not None
    assert decision.audit_event.event_type == BELIEF_REVISION_REJECTED


def test_revision_requires_attached_evidence() -> None:
    state = _state_with_evidence()
    decision = BeliefLifecycle().decide(
        _command(
            REVISE_BELIEF,
            {
                "belief_id": BELIEF_ID,
                "expected_revision": 1,
                "new_statement": "Revised claim",
                "new_status": BeliefStatus.PROVISIONAL.value,
                "reason": "missing source",
                "evidence_refs": ["evidence:missing"],
                "addressed_contradiction_ids": [],
            },
            expected_stream_version=2,
        ),
        state,
    )

    assert not decision.accepted
    assert decision.rejection_code is BeliefRejectionCode.UNKNOWN_EVIDENCE_REF


def test_no_effect_revision_is_rejected() -> None:
    state = _state_with_evidence()
    decision = BeliefLifecycle().decide(
        _command(
            REVISE_BELIEF,
            {
                "belief_id": BELIEF_ID,
                "expected_revision": 1,
                "new_statement": state["statement"],
                "new_status": state["status"],
                "reason": "no change",
                "evidence_refs": ["evidence:for:1"],
                "addressed_contradiction_ids": [],
            },
            expected_stream_version=2,
        ),
        state,
    )

    assert not decision.accepted
    assert decision.rejection_code is BeliefRejectionCode.NO_EFFECT


def test_revision_preserves_history_and_marks_contradiction_addressed() -> None:
    state = _state_with_evidence()
    contradiction = BeliefLifecycle().decide(
        _command(
            REGISTER_CONTRADICTION,
            {
                "belief_id": BELIEF_ID,
                "contradiction_id": "contradiction:1",
                "statement": "Pressure varies.",
                "evidence_refs": ["evidence:for:1"],
            },
            expected_stream_version=2,
        ),
        state,
    )
    assert contradiction.accepted
    state = _apply(state, contradiction.domain_events[0], 3, "EVT-CONTRADICTION")
    revision = BeliefLifecycle().decide(
        _command(
            REVISE_BELIEF,
            {
                "belief_id": BELIEF_ID,
                "expected_revision": 1,
                "new_statement": "At standard pressure, pure water boils near 100°C.",
                "new_status": BeliefStatus.PROVISIONAL.value,
                "reason": "scope clarified",
                "evidence_refs": ["evidence:for:1"],
                "addressed_contradiction_ids": ["contradiction:1"],
            },
            expected_stream_version=3,
        ),
        state,
    )
    assert revision.accepted

    projected = _apply(state, revision.domain_events[0], 4, "EVT-REVISED")

    assert projected["revision"] == 2
    assert projected["status"] == BeliefStatus.PROVISIONAL.value
    assert len(projected["history"]) == 2
    assert projected["contradictions"][0]["addressed_in_revision"] == 2


def test_superseded_belief_is_terminal() -> None:
    state = _state_with_evidence()
    revision = BeliefLifecycle().decide(
        _command(
            REVISE_BELIEF,
            {
                "belief_id": BELIEF_ID,
                "expected_revision": 1,
                "new_statement": "Superseded by a more precise belief.",
                "new_status": BeliefStatus.SUPERSEDED.value,
                "reason": "replacement belief created elsewhere",
                "evidence_refs": ["evidence:for:1"],
                "addressed_contradiction_ids": [],
            },
            expected_stream_version=2,
        ),
        state,
    )
    assert revision.accepted
    state = _apply(state, revision.domain_events[0], 3, "EVT-SUPERSEDED")

    decision = BeliefLifecycle().decide(
        _attach_command("evidence:later", version=3),
        state,
    )

    assert not decision.accepted
    assert decision.rejection_code is BeliefRejectionCode.TERMINAL_BELIEF


@pytest.mark.parametrize("status", [BeliefStatus.SUPPORTED, BeliefStatus.CONTRADICTED])
def test_attach_evidence_rejected_when_belief_is_evidence_gate_owned(
    status: BeliefStatus,
) -> None:
    """Regression guard: decide() must mirror the reducer's terminal check.

    Before this fix, ``BeliefLifecycle._require_mutable`` only rejected
    ``superseded`` beliefs, so ``ATTACH_EVIDENCE`` against an already
    ``supported``/``contradicted`` (Evidence Gate-owned) belief was wrongly
    accepted and produced a ``PendingEvent`` that ``BeliefReducer.apply()``
    would later refuse to project.
    """

    state = _state_with_status(status)
    decision = BeliefLifecycle().decide(
        _attach_command("evidence:after-gate", version=3),
        state,
    )

    assert not decision.accepted
    assert decision.rejection_code is BeliefRejectionCode.EVIDENCE_GATE_OWNED_BELIEF
    assert decision.audit_event is not None
    assert not decision.audit_event.affects_domain_state


@pytest.mark.parametrize("status", [BeliefStatus.SUPPORTED, BeliefStatus.CONTRADICTED])
def test_register_contradiction_rejected_when_belief_is_evidence_gate_owned(
    status: BeliefStatus,
) -> None:
    state = _state_with_status(status)
    decision = BeliefLifecycle().decide(
        _command(
            REGISTER_CONTRADICTION,
            {
                "belief_id": BELIEF_ID,
                "contradiction_id": "contradiction:after-gate",
                "statement": "Attempted contradiction after the gate decided.",
                "evidence_refs": ["evidence:for:1"],
            },
            expected_stream_version=3,
        ),
        state,
    )

    assert not decision.accepted
    assert decision.rejection_code is BeliefRejectionCode.EVIDENCE_GATE_OWNED_BELIEF


@pytest.mark.parametrize("status", [BeliefStatus.SUPPORTED, BeliefStatus.CONTRADICTED])
def test_revise_belief_rejected_when_belief_is_evidence_gate_owned(
    status: BeliefStatus,
) -> None:
    state = _state_with_status(status)
    decision = BeliefLifecycle().decide(
        _command(
            REVISE_BELIEF,
            {
                "belief_id": BELIEF_ID,
                "expected_revision": 1,
                "new_statement": "Attempted revision after the gate decided.",
                "new_status": BeliefStatus.PROVISIONAL.value,
                "reason": "attempted bypass of evidence-gate ownership",
                "evidence_refs": ["evidence:for:1"],
                "addressed_contradiction_ids": [],
            },
            expected_stream_version=3,
        ),
        state,
    )

    assert not decision.accepted
    assert decision.rejection_code is BeliefRejectionCode.EVIDENCE_GATE_OWNED_BELIEF


@pytest.mark.parametrize("status", list(BeliefStatus))
def test_decide_acceptance_never_breaks_reducer_projection(
    status: BeliefStatus,
) -> None:
    """Whole-lattice invariant: decide()-accepted events must always project.

    For every ``BeliefStatus`` in the lattice, an ``ATTACH_EVIDENCE`` or
    ``REGISTER_CONTRADICTION`` command that ``BeliefLifecycle.decide()``
    accepts must be safely projectable by ``BeliefReducer.apply()`` without
    raising. This is the general form of the P0-014/P0-015 boundary bug found
    during audit (terminal statuses were checked in the reducer but not in
    the lifecycle decision layer for two of the three mutating command
    types). Keeping this matrix test alive prevents a future status or
    command addition from silently reopening the same lifecycle/reducer gap.
    """

    state = _state_with_status(status)

    attach_decision = BeliefLifecycle().decide(
        _attach_command("evidence:matrix:attach", version=5),
        state,
    )
    if attach_decision.accepted:
        _apply(
            state,
            attach_decision.domain_events[0],
            6,
            f"EVT-MATRIX-ATTACH-{status.value}",
        )

    contradiction_decision = BeliefLifecycle().decide(
        _command(
            REGISTER_CONTRADICTION,
            {
                "belief_id": BELIEF_ID,
                "contradiction_id": f"contradiction:matrix:{status.value}",
                "statement": "Matrix-generated contradiction candidate.",
                "evidence_refs": ["evidence:for:1"],
            },
            expected_stream_version=5,
        ),
        state,
    )
    if contradiction_decision.accepted:
        _apply(
            state,
            contradiction_decision.domain_events[0],
            6,
            f"EVT-MATRIX-CONTRADICTION-{status.value}",
        )


def test_schema_registry_accepts_domain_and_audit_events() -> None:
    registry = SchemaRegistry(belief_schema_definitions())
    lifecycle = BeliefLifecycle()
    accepted = lifecycle.decide(_create_command(), _empty_state())
    rejected = lifecycle.decide(_create_command(), _created_state())

    registry.validate_pending_event(accepted.domain_events[0])
    assert rejected.audit_event is not None
    registry.validate_pending_event(rejected.audit_event)


def test_belief_projection_is_r1_compatible_and_skips_rejection_audit() -> None:
    registry = SchemaRegistry(belief_schema_definitions())
    reducer = BeliefReducer()
    lifecycle = BeliefLifecycle()
    state = _empty_state()
    create = lifecycle.decide(_create_command(), state)
    assert create.accepted
    state_after_create = _apply(state, create.domain_events[0], 1, "EVT-CREATED")
    rejected = lifecycle.decide(_create_command(), state_after_create)
    assert rejected.audit_event is not None
    attach = lifecycle.decide(_attach_command("evidence:for:1", version=2), state_after_create)
    assert attach.accepted

    with SQLiteEventPayloadStore.in_memory() as store:
        store.initialize_schema()
        committed_create = store.append_one(
            _event(create.domain_events[0], 1, "EVT-CREATED"),
            create.domain_events[0].payload,
            registry=registry,
        )
        store.append_one(
            _event(rejected.audit_event, 2, "EVT-REJECTED"),
            rejected.audit_event.payload,
            registry=registry,
        )
        store.append_one(
            _event(attach.domain_events[0], 3, "EVT-EVIDENCE"),
            attach.domain_events[0].payload,
            registry=registry,
        )
        snapshot = make_replay_snapshot(
            reducer_id=reducer.reducer_id,
            reducer_version=reducer.reducer_version,
            stream_id=STREAM_ID,
            through_stream_version=1,
            through_event_hash=committed_create.event_hash,
            state=state_after_create,
        )
        report = R1ReplayVerifier(
            store,
            registry,
            VerificationBudget(100, 10_000, 100_000),
            ReplayStateBudget(50_000, 500_000),
            reducer,
        ).verify_stream(STREAM_ID, snapshot)

        assert report.ok
        assert report.checked_events == 3
        assert report.applied_events == 2
        assert report.verified_through_stream_version == 3



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
        BeliefReducerError,
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
