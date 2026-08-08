"""P0-015 deterministic Evidence Gate, lifecycle, reducer and R1 integration."""

from __future__ import annotations

from dataclasses import replace
import hashlib

import pytest

from mentaury.beliefs import (
    ATTACH_EVIDENCE,
    CREATE_BELIEF,
    REGISTER_CONTRADICTION,
    BeliefLifecycle,
    BeliefReducer,
    BeliefReducerError,
    BeliefStatus,
    ClaimType,
    EvidenceGatedBeliefLifecycle,
    EvidenceGatedBeliefReducer,
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
from mentaury.evidence import (
    APPLY_EVIDENCE_GATE,
    BELIEF_EVIDENCE_GATED,
    EVIDENCE_GATE_REJECTED,
    MAX_EVIDENCE_RECORDS,
    EvidenceGate,
    EvidenceGateError,
    EvidenceGateOutcome,
    DEFAULT_EVIDENCE_GATE_POLICIES,
    P0_015_CONTEXTUAL_POLICY,
    EvidenceGatePolicy,
    EvidenceGatePolicyRegistry,
    EvidenceGateRejectionCode,
    EvidenceRecord,
    evidence_gate_schema_definitions,
)
from mentaury.replay import (
    R1ReplayVerifier,
    ReplayStateBudget,
    make_replay_snapshot,
)
from mentaury.storage import SQLiteEventPayloadStore, VerificationBudget
from mentaury.validation import SchemaRegistry, ValidationCode

BELIEF_ID = "belief-gate-001"
STREAM_ID = belief_stream_id(BELIEF_ID)
EVALUATED_AT = "2026-08-06T12:00:00Z"
OBSERVED_AT = "2026-08-06T10:00:00Z"


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
        issued_at=EVALUATED_AT,
        issuer=ActorRef("operator", "operator:primary"),
        authority=AuthorityRef("CAP-EVIDENCE-GATE", 1),
        correlation_id="CORR-EVIDENCE-GATE",
        idempotency_key=f"IDEMP-{command_id or command_type}",
        payload=payload,
    )


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
        occurred_at=EVALUATED_AT,
        recorded_at=EVALUATED_AT,
        producer=ProducerRef("evidence-gate-test", "0.1.0"),
        initiator=ActorRef("operator", "operator:primary"),
        authority=AuthorityRef("CAP-EVIDENCE-GATE", 1),
        causation_id=f"CMD-{event_id}",
        correlation_id="CORR-EVIDENCE-GATE",
        affects_domain_state=pending.affects_domain_state,
        payload_digest="sha256:untrusted",
        payload_ref=f"PAYLOAD-{event_id}",
        previous_hash="sha256:untrusted",
        event_hash="sha256:untrusted",
    )


def _apply(reducer, state, pending: PendingEvent, version: int, event_id: str):
    return freeze_payload(
        reducer.apply(state, _event(pending, version, event_id), pending.payload)
    )


def _policy(**changes: int) -> EvidenceGatePolicy:
    values: dict[str, object] = {
        "allowed_claim_types": (ClaimType.CONTEXTUAL,),
        "minimum_source_groups_for": 2,
        "minimum_source_groups_against": 2,
        "minimum_reliability_milli": 800,
        "minimum_relevance_milli": 800,
        "maximum_age_seconds": 86_400,
    }
    values.update(changes)
    return EvidenceGatePolicy("mentaury-evidence-contextual-v1", **values)


def _record(
    evidence_ref: str,
    side: EvidenceSide,
    source_group: str,
    *,
    reliability_milli: int = 900,
    relevance_milli: int = 900,
    observed_at: str = OBSERVED_AT,
    revoked: bool = False,
) -> EvidenceRecord:
    suffix = evidence_ref.replace(":", "-")
    return EvidenceRecord(
        evidence_ref=evidence_ref,
        side=side,
        source_group=source_group,
        provenance_ref=f"provenance:{suffix}",
        content_digest="sha256:" + hashlib.sha256(evidence_ref.encode("utf-8")).hexdigest(),
        observed_at=observed_at,
        reliability_milli=reliability_milli,
        relevance_milli=relevance_milli,
        revoked=revoked,
    )


def _empty_state():
    return freeze_payload(BeliefReducer().initial_state())


def _created_state(claim_type: ClaimType = ClaimType.CONTEXTUAL):
    lifecycle = BeliefLifecycle()
    command = _command(
        CREATE_BELIEF,
        {
            "belief_id": BELIEF_ID,
            "statement": "The governed claim is supported by independent evidence.",
            "claim_type": claim_type.value,
        },
    )
    decision = lifecycle.decide(command, _empty_state())
    assert decision.accepted
    return _apply(BeliefReducer(), _empty_state(), decision.domain_events[0], 1, "EVT-CREATE")


def _attach(state, evidence_ref: str, side: EvidenceSide, version: int):
    decision = BeliefLifecycle().decide(
        _command(
            ATTACH_EVIDENCE,
            {
                "belief_id": BELIEF_ID,
                "evidence_ref": evidence_ref,
                "side": side.value,
            },
            expected_stream_version=version - 1,
            command_id=f"CMD-ATTACH-{version}",
        ),
        state,
    )
    assert decision.accepted
    return _apply(
        BeliefReducer(),
        state,
        decision.domain_events[0],
        version,
        f"EVT-ATTACH-{version}",
    ), decision.domain_events[0]


def _support_state(claim_type: ClaimType = ClaimType.CONTEXTUAL):
    state = _created_state(claim_type)
    state, _ = _attach(state, "evidence:for:1", EvidenceSide.FOR, 2)
    state, _ = _attach(state, "evidence:for:2", EvidenceSide.FOR, 3)
    return state


def _contradicted_candidate_state():
    state = _created_state()
    state, _ = _attach(state, "evidence:against:1", EvidenceSide.AGAINST, 2)
    state, _ = _attach(state, "evidence:against:2", EvidenceSide.AGAINST, 3)
    decision = BeliefLifecycle().decide(
        _command(
            REGISTER_CONTRADICTION,
            {
                "belief_id": BELIEF_ID,
                "contradiction_id": "contradiction:gate:1",
                "statement": "Independent evidence contradicts the claim.",
                "evidence_refs": ["evidence:against:1"],
            },
            expected_stream_version=3,
            command_id="CMD-CONTRADICTION",
        ),
        state,
    )
    assert decision.accepted
    return _apply(
        BeliefReducer(), state, decision.domain_events[0], 4, "EVT-CONTRADICTION"
    )


def _gate_command(
    state,
    records,
    *,
    policy_id: str = P0_015_CONTEXTUAL_POLICY.policy_id,
    expected_stream_version: int = 3,
    issued_at: str = EVALUATED_AT,
    extra_payload: dict[str, object] | None = None,
):
    payload: dict[str, object] = {
        "belief_id": BELIEF_ID,
        "expected_revision": state["revision"],
        "policy_id": policy_id,
        "records": [record.to_value() for record in records],
    }
    if extra_payload:
        payload.update(extra_payload)
    command = _command(
        APPLY_EVIDENCE_GATE,
        payload,
        expected_stream_version=expected_stream_version,
        command_id="CMD-APPLY-EVIDENCE-GATE",
    )
    return replace(command, issued_at=issued_at)


def test_gate_receipt_is_order_independent_and_content_addressed() -> None:
    records = (
        _record("evidence:for:1", EvidenceSide.FOR, "source:a"),
        _record("evidence:for:2", EvidenceSide.FOR, "source:b"),
    )
    kwargs = {
        "belief_id": BELIEF_ID,
        "belief_revision": 1,
        "claim_type": ClaimType.CONTEXTUAL,
        "statement": "claim",
        "evidence_for": ["evidence:for:1", "evidence:for:2"],
        "evidence_against": [],
        "policy": _policy(),
        "evaluated_at": EVALUATED_AT,
    }

    first = EvidenceGate().evaluate(records=records, **kwargs)
    second = EvidenceGate().evaluate(records=reversed(records), **kwargs)

    assert first.outcome is EvidenceGateOutcome.SUPPORTED
    assert first == second
    assert first.receipt_digest.startswith("sha256:")


def test_gate_requires_complete_exact_evidence_set() -> None:
    with pytest.raises(EvidenceGateError, match="exactly match"):
        EvidenceGate().evaluate(
            belief_id=BELIEF_ID,
            belief_revision=1,
            claim_type=ClaimType.CONTEXTUAL,
            statement="claim",
            evidence_for=["evidence:for:1", "evidence:for:2"],
            evidence_against=[],
            records=[_record("evidence:for:1", EvidenceSide.FOR, "source:a")],
            policy=_policy(),
            evaluated_at=EVALUATED_AT,
        )


def test_gate_rejects_side_mismatch_and_future_evidence() -> None:
    with pytest.raises(EvidenceGateError, match="side mismatch"):
        EvidenceGate().evaluate(
            belief_id=BELIEF_ID,
            belief_revision=1,
            claim_type=ClaimType.CONTEXTUAL,
            statement="claim",
            evidence_for=["evidence:for:1"],
            evidence_against=[],
            records=[
                _record("evidence:for:1", EvidenceSide.AGAINST, "source:a")
            ],
            policy=_policy(minimum_source_groups_for=1),
            evaluated_at=EVALUATED_AT,
        )
    with pytest.raises(EvidenceGateError, match="after evaluated_at"):
        EvidenceGate().evaluate(
            belief_id=BELIEF_ID,
            belief_revision=1,
            claim_type=ClaimType.CONTEXTUAL,
            statement="claim",
            evidence_for=["evidence:for:1"],
            evidence_against=[],
            records=[
                _record(
                    "evidence:for:1",
                    EvidenceSide.FOR,
                    "source:a",
                    observed_at="2026-08-07T00:00:00Z",
                )
            ],
            policy=_policy(minimum_source_groups_for=1),
            evaluated_at=EVALUATED_AT,
        )


def test_duplicate_material_and_cross_side_source_group_are_rejected() -> None:
    first = _record("evidence:for:1", EvidenceSide.FOR, "source:a")
    duplicate_content = replace(
        _record("evidence:for:2", EvidenceSide.FOR, "source:b"),
        content_digest=first.content_digest,
    )
    with pytest.raises(EvidenceGateError, match="duplicate content_digest"):
        EvidenceGate().evaluate(
            belief_id=BELIEF_ID,
            belief_revision=1,
            claim_type=ClaimType.CONTEXTUAL,
            statement="claim",
            evidence_for=["evidence:for:1", "evidence:for:2"],
            evidence_against=[],
            records=[first, duplicate_content],
            policy=_policy(),
            evaluated_at=EVALUATED_AT,
        )

    duplicate_provenance = replace(
        _record("evidence:for:2", EvidenceSide.FOR, "source:b"),
        provenance_ref=first.provenance_ref,
    )
    with pytest.raises(EvidenceGateError, match="duplicate provenance_ref"):
        EvidenceGate().evaluate(
            belief_id=BELIEF_ID,
            belief_revision=1,
            claim_type=ClaimType.CONTEXTUAL,
            statement="claim",
            evidence_for=["evidence:for:1", "evidence:for:2"],
            evidence_against=[],
            records=[first, duplicate_provenance],
            policy=_policy(),
            evaluated_at=EVALUATED_AT,
        )

    with pytest.raises(EvidenceGateError, match="both evidence sides"):
        EvidenceGate().evaluate(
            belief_id=BELIEF_ID,
            belief_revision=1,
            claim_type=ClaimType.CONTEXTUAL,
            statement="claim",
            evidence_for=["evidence:for:1"],
            evidence_against=["evidence:against:1"],
            records=[
                first,
                _record(
                    "evidence:against:1",
                    EvidenceSide.AGAINST,
                    "source:a",
                ),
            ],
            policy=_policy(
                minimum_source_groups_for=1,
                minimum_source_groups_against=1,
            ),
            evaluated_at=EVALUATED_AT,
        )


def test_low_quality_stale_and_revoked_records_do_not_count() -> None:
    receipt = EvidenceGate().evaluate(
        belief_id=BELIEF_ID,
        belief_revision=1,
        claim_type=ClaimType.CONTEXTUAL,
        statement="claim",
        evidence_for=["evidence:for:1", "evidence:for:2", "evidence:for:3"],
        evidence_against=[],
        records=[
            _record(
                "evidence:for:1",
                EvidenceSide.FOR,
                "source:a",
                reliability_milli=100,
            ),
            _record(
                "evidence:for:2",
                EvidenceSide.FOR,
                "source:b",
                observed_at="2026-07-01T00:00:00Z",
            ),
            _record(
                "evidence:for:3",
                EvidenceSide.FOR,
                "source:c",
                revoked=True,
            ),
        ],
        policy=_policy(),
        evaluated_at=EVALUATED_AT,
    )

    assert receipt.outcome is EvidenceGateOutcome.INCONCLUSIVE
    assert receipt.rejected_refs == (
        "evidence:for:1",
        "evidence:for:2",
        "evidence:for:3",
    )


def test_independent_source_groups_are_counted_not_record_count() -> None:
    receipt = EvidenceGate().evaluate(
        belief_id=BELIEF_ID,
        belief_revision=1,
        claim_type=ClaimType.CONTEXTUAL,
        statement="claim",
        evidence_for=["evidence:for:1", "evidence:for:2"],
        evidence_against=[],
        records=[
            _record("evidence:for:1", EvidenceSide.FOR, "source:same"),
            _record("evidence:for:2", EvidenceSide.FOR, "source:same"),
        ],
        policy=_policy(),
        evaluated_at=EVALUATED_AT,
    )

    assert receipt.outcome is EvidenceGateOutcome.INCONCLUSIVE
    assert receipt.source_groups_for == ("source:same",)


def test_both_sides_passing_is_conflict_not_arbitrary_winner() -> None:
    receipt = EvidenceGate().evaluate(
        belief_id=BELIEF_ID,
        belief_revision=1,
        claim_type=ClaimType.CONTEXTUAL,
        statement="claim",
        evidence_for=["evidence:for:1"],
        evidence_against=["evidence:against:1"],
        records=[
            _record("evidence:for:1", EvidenceSide.FOR, "source:for"),
            _record(
                "evidence:against:1", EvidenceSide.AGAINST, "source:against"
            ),
        ],
        policy=_policy(
            minimum_source_groups_for=1,
            minimum_source_groups_against=1,
        ),
        evaluated_at=EVALUATED_AT,
    )

    assert receipt.outcome is EvidenceGateOutcome.CONFLICT


def test_lifecycle_rejects_unapproved_policy_and_unsupported_claim_type() -> None:
    state = _support_state()
    records = (
        _record("evidence:for:1", EvidenceSide.FOR, "source:a"),
        _record("evidence:for:2", EvidenceSide.FOR, "source:b"),
    )
    unapproved = EvidenceGatedBeliefLifecycle().decide(
        _gate_command(state, records, policy_id="policy:attacker:lenient"),
        state,
    )
    assert not unapproved.accepted
    assert unapproved.rejection_code is EvidenceGateRejectionCode.POLICY_NOT_APPROVED

    causal_state = _support_state(ClaimType.CAUSAL)
    unsupported = EvidenceGatedBeliefLifecycle().decide(
        _gate_command(causal_state, records),
        causal_state,
    )
    assert not unsupported.accepted
    assert (
        unsupported.rejection_code
        is EvidenceGateRejectionCode.CLAIM_TYPE_NOT_ALLOWED
    )


def test_lifecycle_rejects_hidden_command_fields() -> None:
    state = _support_state()
    records = (
        _record("evidence:for:1", EvidenceSide.FOR, "source:a"),
        _record("evidence:for:2", EvidenceSide.FOR, "source:b"),
    )
    decision = EvidenceGatedBeliefLifecycle().decide(
        _gate_command(state, records, extra_payload={"minimum_sources": 1}),
        state,
    )
    assert not decision.accepted
    assert decision.rejection_code is EvidenceGateRejectionCode.INVALID_COMMAND


def test_lifecycle_accepts_supported_gate_and_emits_strict_event() -> None:
    state = _support_state()
    records = (
        _record("evidence:for:1", EvidenceSide.FOR, "source:a"),
        _record("evidence:for:2", EvidenceSide.FOR, "source:b"),
    )

    decision = EvidenceGatedBeliefLifecycle().decide(
        _gate_command(state, records), state
    )

    assert decision.accepted
    assert decision.receipt is not None
    assert decision.receipt.outcome is EvidenceGateOutcome.SUPPORTED
    assert decision.domain_events[0].event_type == BELIEF_EVIDENCE_GATED
    assert decision.domain_events[0].payload["new_status"] == "supported"


def test_lifecycle_rejections_are_non_state_audits() -> None:
    state = _support_state()
    records = (
        _record(
            "evidence:for:1",
            EvidenceSide.FOR,
            "source:a",
            reliability_milli=1,
        ),
        _record(
            "evidence:for:2",
            EvidenceSide.FOR,
            "source:b",
            reliability_milli=1,
        ),
    )

    decision = EvidenceGatedBeliefLifecycle().decide(
        _gate_command(state, records), state
    )

    assert not decision.accepted
    assert decision.rejection_code is EvidenceGateRejectionCode.INCONCLUSIVE
    assert decision.audit_event is not None
    assert decision.audit_event.event_type == EVIDENCE_GATE_REJECTED
    assert not decision.audit_event.affects_domain_state
    assert decision.receipt is not None
    assert decision.audit_event.payload["receipt"]["outcome"] == "inconclusive"


def test_supported_gate_rejects_open_contradictions() -> None:
    state = _support_state()
    contradiction = BeliefLifecycle().decide(
        _command(
            REGISTER_CONTRADICTION,
            {
                "belief_id": BELIEF_ID,
                "contradiction_id": "contradiction:open",
                "statement": "An unresolved exception remains.",
                "evidence_refs": ["evidence:for:1"],
            },
            expected_stream_version=3,
            command_id="CMD-OPEN-CONTRADICTION",
        ),
        state,
    )
    assert contradiction.accepted
    state = _apply(
        BeliefReducer(), state, contradiction.domain_events[0], 4, "EVT-OPEN"
    )
    records = (
        _record("evidence:for:1", EvidenceSide.FOR, "source:a"),
        _record("evidence:for:2", EvidenceSide.FOR, "source:b"),
    )

    decision = EvidenceGatedBeliefLifecycle().decide(
        _gate_command(state, records, expected_stream_version=4), state
    )

    assert not decision.accepted
    assert decision.rejection_code is EvidenceGateRejectionCode.OPEN_CONTRADICTIONS


def test_contradicted_gate_requires_open_registered_contradiction() -> None:
    state = _created_state()
    state, _ = _attach(state, "evidence:against:1", EvidenceSide.AGAINST, 2)
    state, _ = _attach(state, "evidence:against:2", EvidenceSide.AGAINST, 3)
    records = (
        _record("evidence:against:1", EvidenceSide.AGAINST, "source:a"),
        _record("evidence:against:2", EvidenceSide.AGAINST, "source:b"),
    )

    decision = EvidenceGatedBeliefLifecycle().decide(
        _gate_command(state, records), state
    )

    assert not decision.accepted
    assert decision.rejection_code is EvidenceGateRejectionCode.CONTRADICTION_REQUIRED


def test_reducer_recomputes_receipt_and_rejects_tampering() -> None:
    state = _support_state()
    records = (
        _record("evidence:for:1", EvidenceSide.FOR, "source:a"),
        _record("evidence:for:2", EvidenceSide.FOR, "source:b"),
    )
    decision = EvidenceGatedBeliefLifecycle().decide(
        _gate_command(state, records), state
    )
    assert decision.accepted
    event = decision.domain_events[0]
    projected = _apply(
        EvidenceGatedBeliefReducer(), state, event, 4, "EVT-GATED"
    )
    assert projected["status"] == BeliefStatus.SUPPORTED.value
    assert projected["revision"] == 2
    assert projected["history"][-1]["gate_receipt_digest"].startswith("sha256:")

    tampered_payload = dict(event.payload)
    tampered_receipt = dict(tampered_payload["receipt"])
    tampered_receipt["outcome"] = EvidenceGateOutcome.CONTRADICTED.value
    tampered_payload["receipt"] = tampered_receipt
    tampered = PendingEvent(
        event.event_type,
        event.payload_schema,
        True,
        tampered_payload,
    )
    with pytest.raises(BeliefReducerError, match="receipt"):
        _apply(
            EvidenceGatedBeliefReducer(), state, tampered, 4, "EVT-TAMPERED"
        )


def test_reducer_rejects_unapproved_policy_tampering_and_time_rebinding() -> None:
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

    policy_payload = dict(pending.payload)
    forged_policy = dict(policy_payload["policy"])
    forged_policy["minimum_source_groups_for"] = 1
    policy_payload["policy"] = forged_policy
    with pytest.raises(BeliefReducerError, match="approved policy"):
        _apply(
            EvidenceGatedBeliefReducer(),
            state,
            PendingEvent(
                pending.event_type,
                pending.payload_schema,
                True,
                policy_payload,
            ),
            4,
            "EVT-FORGED-POLICY",
        )

    rebound_event = replace(
        _event(pending, 4, "EVT-TIME-REBOUND"),
        occurred_at="2026-08-06T13:00:00Z",
    )
    with pytest.raises(BeliefReducerError, match="occurred_at"):
        EvidenceGatedBeliefReducer().apply(state, rebound_event, pending.payload)


def test_reducer_requires_canonical_record_order() -> None:
    state = _support_state()
    records = (
        _record("evidence:for:2", EvidenceSide.FOR, "source:b"),
        _record("evidence:for:1", EvidenceSide.FOR, "source:a"),
    )
    decision = EvidenceGatedBeliefLifecycle().decide(
        _gate_command(state, records), state
    )
    assert decision.accepted
    pending = decision.domain_events[0]
    assert [item["evidence_ref"] for item in pending.payload["records"]] == [
        "evidence:for:1",
        "evidence:for:2",
    ]

    reordered_payload = dict(pending.payload)
    reordered_payload["records"] = list(reversed(reordered_payload["records"]))
    with pytest.raises(BeliefReducerError, match="sorted"):
        _apply(
            EvidenceGatedBeliefReducer(),
            state,
            PendingEvent(
                pending.event_type,
                pending.payload_schema,
                True,
                reordered_payload,
            ),
            4,
            "EVT-REORDERED",
        )


def test_reducer_rejects_incomplete_records_and_wrong_new_status() -> None:
    state = _support_state()
    records = (
        _record("evidence:for:1", EvidenceSide.FOR, "source:a"),
        _record("evidence:for:2", EvidenceSide.FOR, "source:b"),
    )
    decision = EvidenceGatedBeliefLifecycle().decide(
        _gate_command(state, records), state
    )
    assert decision.accepted
    event = decision.domain_events[0]

    missing_payload = dict(event.payload)
    missing_payload["records"] = list(missing_payload["records"][:-1])
    missing = PendingEvent(event.event_type, event.payload_schema, True, missing_payload)
    with pytest.raises(BeliefReducerError, match="receipt"):
        _apply(EvidenceGatedBeliefReducer(), state, missing, 4, "EVT-MISSING")

    wrong_status_payload = dict(event.payload)
    wrong_status_payload["new_status"] = BeliefStatus.CONTRADICTED.value
    wrong_status = PendingEvent(
        event.event_type,
        event.payload_schema,
        True,
        wrong_status_payload,
    )
    with pytest.raises(BeliefReducerError, match="new_status"):
        _apply(
            EvidenceGatedBeliefReducer(), state, wrong_status, 4, "EVT-WRONG-STATUS"
        )


def test_contradicted_gate_is_replayable_with_open_contradiction() -> None:
    state = _contradicted_candidate_state()
    records = (
        _record("evidence:against:1", EvidenceSide.AGAINST, "source:a"),
        _record("evidence:against:2", EvidenceSide.AGAINST, "source:b"),
    )
    decision = EvidenceGatedBeliefLifecycle().decide(
        _gate_command(state, records, expected_stream_version=4), state
    )
    assert decision.accepted
    projected = _apply(
        EvidenceGatedBeliefReducer(), state, decision.domain_events[0], 5, "EVT-CONTRADICTED"
    )
    assert projected["status"] == BeliefStatus.CONTRADICTED.value


def test_gate_schemas_are_strict_and_registered() -> None:
    registry = SchemaRegistry(
        (*belief_schema_definitions(), *evidence_gate_schema_definitions())
    )
    state = _support_state()
    records = (
        _record("evidence:for:1", EvidenceSide.FOR, "source:a"),
        _record("evidence:for:2", EvidenceSide.FOR, "source:b"),
    )
    accepted = EvidenceGatedBeliefLifecycle().decide(
        _gate_command(state, records), state
    )
    rejected = EvidenceGatedBeliefLifecycle().decide(
        _gate_command(
            state,
            (
                replace(records[0], reliability_milli=1),
                replace(records[1], reliability_milli=1),
            ),
        ),
        state,
    )
    assert accepted.accepted
    registry.validate_pending_event(accepted.domain_events[0])
    assert rejected.audit_event is not None
    registry.validate_pending_event(rejected.audit_event)


def _gate_registry() -> SchemaRegistry:
    return SchemaRegistry(
        (*belief_schema_definitions(), *evidence_gate_schema_definitions())
    )


def _gated_event_payload() -> dict[str, object]:
    """A real BELIEF_EVIDENCE_GATED payload produced by the actual P0-015
    decision path (not a hand-built synthetic payload), used to prove that
    the sha256 pattern check in evidence_gate_schema_definitions() is wired
    to the fields real callers actually populate.
    """

    state = _support_state()
    records = (
        _record("evidence:for:1", EvidenceSide.FOR, "source:a"),
        _record("evidence:for:2", EvidenceSide.FOR, "source:b"),
    )
    decision = EvidenceGatedBeliefLifecycle().decide(
        _gate_command(state, records), state
    )
    assert decision.accepted
    return dict(decision.domain_events[0].payload)


def _gated_pending(payload: dict[str, object]) -> PendingEvent:
    return PendingEvent(BELIEF_EVIDENCE_GATED, "belief-evidence-gated/v1", True, payload)


def test_real_gated_event_payload_passes_schema_admission() -> None:
    payload = _gated_event_payload()
    assert _gate_registry().validate_pending_event(_gated_pending(payload)) == ()


# (label, malformed digest value, expected validation code). Length is
# checked before pattern in mentaury.validation.validator, so a too-short
# digest fails on STRING_TOO_SHORT rather than STRING_PATTERN_MISMATCH; every
# other malformation preserves the required length but violates the sha256
# shape, so it must fail on STRING_PATTERN_MISMATCH.
_MALFORMED_DIGEST_VARIANTS = (
    ("uppercase_hex", "sha256:" + "F" * 64, ValidationCode.STRING_PATTERN_MISMATCH),
    ("wrong_prefix", "sha512:" + "a" * 64, ValidationCode.STRING_PATTERN_MISMATCH),
    ("non_hex_characters", "sha256:" + "g" * 64, ValidationCode.STRING_PATTERN_MISMATCH),
    ("too_short_63_hex_chars", "sha256:" + "a" * 63, ValidationCode.STRING_TOO_SHORT),
    ("too_long_65_hex_chars", "sha256:" + "a" * 65, ValidationCode.STRING_PATTERN_MISMATCH),
    ("trailing_newline", "sha256:" + "a" * 64 + "\n", ValidationCode.STRING_PATTERN_MISMATCH),
    ("trailing_whitespace", "sha256:" + "a" * 64 + " ", ValidationCode.STRING_PATTERN_MISMATCH),
    ("extra_suffix", "sha256:" + "a" * 64 + "-extra", ValidationCode.STRING_PATTERN_MISMATCH),
)


@pytest.mark.parametrize("label,malformed,expected_code", _MALFORMED_DIGEST_VARIANTS)
def test_belief_evidence_gated_schema_rejects_malformed_record_content_digest(
    label: str, malformed: str, expected_code: ValidationCode
) -> None:
    payload = _gated_event_payload()
    records = [dict(record) for record in payload["records"]]
    records[0] = {**records[0], "content_digest": malformed}
    payload["records"] = records

    issues = _gate_registry().validate_pending_event(_gated_pending(payload))

    assert {issue.code for issue in issues} == {expected_code}, label
    assert issues[0].path == "$.records[0].content_digest"


@pytest.mark.parametrize(
    "receipt_digest_field",
    ["statement_digest", "policy_digest", "evidence_set_digest", "receipt_digest"],
)
def test_belief_evidence_gated_schema_rejects_malformed_receipt_digest_fields(
    receipt_digest_field: str,
) -> None:
    payload = _gated_event_payload()
    receipt = dict(payload["receipt"])
    receipt[receipt_digest_field] = "sha256:" + "F" * 64
    payload["receipt"] = receipt

    issues = _gate_registry().validate_pending_event(_gated_pending(payload))

    assert {issue.code for issue in issues} == {ValidationCode.STRING_PATTERN_MISMATCH}
    assert issues[0].path == f"$.receipt.{receipt_digest_field}"


def test_evidence_gate_event_is_r1_replay_compatible() -> None:
    registry = SchemaRegistry(
        (*belief_schema_definitions(), *evidence_gate_schema_definitions())
    )
    base_reducer = BeliefReducer()
    gated_reducer = EvidenceGatedBeliefReducer()
    lifecycle = BeliefLifecycle()
    state = freeze_payload(base_reducer.initial_state())

    create = lifecycle.decide(
        _command(
            CREATE_BELIEF,
            {
                "belief_id": BELIEF_ID,
                "statement": "The governed claim is supported by independent evidence.",
                "claim_type": ClaimType.CONTEXTUAL.value,
            },
        ),
        state,
    )
    assert create.accepted
    state = _apply(base_reducer, state, create.domain_events[0], 1, "EVT-R1-CREATE")
    snapshot_state = state
    attach_one = lifecycle.decide(
        _command(
            ATTACH_EVIDENCE,
            {
                "belief_id": BELIEF_ID,
                "evidence_ref": "evidence:for:1",
                "side": EvidenceSide.FOR.value,
            },
            expected_stream_version=1,
            command_id="CMD-R1-ATTACH-1",
        ),
        state,
    )
    assert attach_one.accepted
    state = _apply(base_reducer, state, attach_one.domain_events[0], 2, "EVT-R1-ATTACH-1")
    attach_two = lifecycle.decide(
        _command(
            ATTACH_EVIDENCE,
            {
                "belief_id": BELIEF_ID,
                "evidence_ref": "evidence:for:2",
                "side": EvidenceSide.FOR.value,
            },
            expected_stream_version=2,
            command_id="CMD-R1-ATTACH-2",
        ),
        state,
    )
    assert attach_two.accepted
    state = _apply(base_reducer, state, attach_two.domain_events[0], 3, "EVT-R1-ATTACH-2")
    records = (
        _record("evidence:for:1", EvidenceSide.FOR, "source:a"),
        _record("evidence:for:2", EvidenceSide.FOR, "source:b"),
    )
    gated = EvidenceGatedBeliefLifecycle().decide(
        _gate_command(state, records), state
    )
    assert gated.accepted

    with SQLiteEventPayloadStore.in_memory() as store:
        store.initialize_schema()
        committed_create = None
        for version, event_id, pending in (
            (1, "EVT-R1-CREATE", create.domain_events[0]),
            (2, "EVT-R1-ATTACH-1", attach_one.domain_events[0]),
            (3, "EVT-R1-ATTACH-2", attach_two.domain_events[0]),
            (4, "EVT-R1-GATED", gated.domain_events[0]),
        ):
            committed = store.append_one(
                _event(pending, version, event_id),
                pending.payload,
                registry=registry,
            )
            if version == 1:
                committed_create = committed
        assert committed_create is not None
        snapshot = make_replay_snapshot(
            reducer_id=gated_reducer.reducer_id,
            reducer_version=gated_reducer.reducer_version,
            stream_id=STREAM_ID,
            through_stream_version=1,
            through_event_hash=committed_create.event_hash,
            state=snapshot_state,
        )
        report = R1ReplayVerifier(
            store,
            registry,
            VerificationBudget(100, 100_000, 1_000_000),
            ReplayStateBudget(100_000, 1_000_000),
            gated_reducer,
        ).verify_stream(STREAM_ID, snapshot)

        assert report.ok
        assert report.checked_events == 4
        assert report.applied_events == 4
        assert report.verified_through_stream_version == 4
        assert report.full_state_hash is not None



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


def test_lifecycle_conflict_uses_qualifying_evidence_fail_closed_message() -> None:
    """CONFLICT возникает при qualifying groups на обеих сторонах.

    Даже если threshold полностью не достигнут с одной стороны, наличие
    qualifying evidence на обеих сторонах остаётся fail-closed CONFLICT.
    Сообщение не должно утверждать, что обе стороны «satisfy the approved
    policy».
    """

    state = _created_state()
    state, _ = _attach(state, "evidence:for:1", EvidenceSide.FOR, 2)
    state, _ = _attach(state, "evidence:against:1", EvidenceSide.AGAINST, 3)
    records = (
        _record("evidence:for:1", EvidenceSide.FOR, "source:for"),
        _record("evidence:against:1", EvidenceSide.AGAINST, "source:against"),
    )
    # minimum_source_groups_against=2: against не достигает threshold,
    # но qualifying group на against всё равно существует → CONFLICT.
    policy = EvidenceGatePolicy(
        policy_id=P0_015_CONTEXTUAL_POLICY.policy_id,
        allowed_claim_types=P0_015_CONTEXTUAL_POLICY.allowed_claim_types,
        minimum_source_groups_for=1,
        minimum_source_groups_against=2,
        minimum_reliability_milli=P0_015_CONTEXTUAL_POLICY.minimum_reliability_milli,
        minimum_relevance_milli=P0_015_CONTEXTUAL_POLICY.minimum_relevance_milli,
        maximum_age_seconds=P0_015_CONTEXTUAL_POLICY.maximum_age_seconds,
    )
    registry = EvidenceGatePolicyRegistry((policy,))
    decision = EvidenceGatedBeliefLifecycle(policies=registry).decide(
        _gate_command(state, records, policy_id=policy.policy_id),
        state,
    )

    assert not decision.accepted
    assert decision.rejection_code is EvidenceGateRejectionCode.CONFLICT
    assert decision.message == (
        "qualifying evidence exists on both sides; fail-closed conflict"
    )
    assert decision.receipt is not None
    assert decision.receipt.outcome is EvidenceGateOutcome.CONFLICT
    assert "satisfy the approved policy" not in (decision.message or "")
