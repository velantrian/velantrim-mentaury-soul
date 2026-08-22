"""V1 Stage 3 offline epistemic end-to-end acceptance flow.

This file deliberately composes only already-merged bounded owners. It adds no
new runtime, retrieval, identity, action, or deployment authority.
"""

from __future__ import annotations

import hashlib
from dataclasses import replace

import pytest

from mentaury.beliefs import (
    ATTACH_EVIDENCE,
    BeliefLifecycle,
    BeliefRejectionCode,
    BeliefStatus,
    EvidenceGatedBeliefLifecycle,
    EvidenceSide,
    belief_stream_id,
)
from mentaury.claim_belief_binding import (
    CREATE_BELIEF_FROM_CLAIM,
    CREATE_BELIEF_FROM_CLAIM_SCHEMA,
    ClaimBeliefBindingBudget,
    ClaimBoundBeliefLifecycle,
    ClaimBoundBeliefReducer,
)
from mentaury.claims import (
    ClaimRepresentation,
    ClaimScope,
    EpistemicRole,
    ProvenanceSource,
    RepresentationBudget,
    represent_provenance_claim,
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
from mentaury.epistemic_change import (
    BeliefBinding,
    EpistemicChangeBindingError,
    EpistemicChangeBudget,
    EpistemicChangeRequest,
    EpistemicIntent,
    EpistemicOwner,
    EpistemicRoute,
    route_epistemic_change,
)
from mentaury.epistemic_types import ClaimType
from mentaury.evidence import (
    APPLY_EVIDENCE_GATE,
    P0_015_CONTEXTUAL_POLICY,
    EvidenceGateOutcome,
    EvidenceGateRejectionCode,
    EvidenceRecord,
)
from mentaury.non_projection import (
    ClaimClass,
    ProvenanceState,
    Sensitivity,
    SourceClass,
    SourceOrigin,
    SubjectRelation,
)

BELIEF_ID = "belief:v1:e2e:001"
STREAM_ID = belief_stream_id(BELIEF_ID)
NOW = "2026-08-22T08:00:00Z"
OBSERVED_AT = "2026-08-22T07:00:00Z"


def _record():
    return represent_provenance_claim(
        source=ProvenanceSource(
            source_ref="source:v1:e2e",
            source_actor_ref="actor:researcher",
            source_class=SourceClass.RESEARCH_PRIMARY,
            source_origin=SourceOrigin.PRIMARY,
            provenance_state=ProvenanceState.VERIFIED,
            publication_or_capture_context_ref="context:v1:e2e",
            sensitivity=Sensitivity.NORMAL,
            usage_boundary_ref="usage:v1:e2e",
            material_gaps=(),
            derivation_refs=(),
        ),
        claim=ClaimRepresentation(
            claim_id="claim:v1:e2e:001",
            statement_ref="statement:v1:e2e:001",
            claim_class=ClaimClass.FACTUAL,
            claim_type=ClaimType.CONTEXTUAL,
            epistemic_role=EpistemicRole.TESTIMONY,
            directly_stated=True,
            speaker_ref="actor:researcher",
            subject_ref="subject:world",
            subject_relation=SubjectRelation.NON_SELF,
            basis_refs=(),
            evidence_refs=(),
        ),
        scope=ClaimScope(
            applies_to=("scope:v1:e2e",),
            may_support=("question:v1:e2e",),
            does_not_establish=("truth:universal",),
            unknowns=("unknown:independent-evidence",),
            transfer_limits=("no:auto-belief",),
        ),
        budget=RepresentationBudget(4096, 512, 262144),
    )


def _command(
    command_id: str,
    command_type: str,
    command_schema: str,
    payload: dict[str, object],
    *,
    expected_stream_version: int,
) -> CommandEnvelope:
    return CommandEnvelope(
        command_id=command_id,
        command_type=command_type,
        command_schema=command_schema,
        target_stream=STREAM_ID,
        expected_stream_version=expected_stream_version,
        issued_at=NOW,
        issuer=ActorRef("operator", "operator:primary"),
        authority=AuthorityRef("CAP-V1-E2E", 1),
        correlation_id="CORR-V1-E2E",
        idempotency_key=f"IDEMP-{command_id}",
        payload=payload,
    )


def _event(pending: PendingEvent, version: int) -> EventEnvelope:
    return EventEnvelope(
        event_id=f"EVT-V1-E2E-{version}",
        event_type=pending.event_type,
        envelope_schema_version=1,
        payload_schema=pending.payload_schema,
        stream_id=STREAM_ID,
        stream_version=version,
        batch_id=f"BATCH-V1-E2E-{version}",
        batch_index=0,
        batch_size=1,
        occurred_at=NOW,
        recorded_at=NOW,
        producer=ProducerRef("v1-e2e-test", "1.0.0"),
        initiator=ActorRef("operator", "operator:primary"),
        authority=AuthorityRef("CAP-V1-E2E", 1),
        causation_id=f"CMD-V1-E2E-{version}",
        correlation_id="CORR-V1-E2E",
        affects_domain_state=pending.affects_domain_state,
        payload_digest="sha256:untrusted-test-payload",
        payload_ref=f"PAYLOAD-V1-E2E-{version}",
        previous_hash="sha256:untrusted-test-previous",
        event_hash="sha256:untrusted-test-event",
    )


def _apply(reducer, state, pending: PendingEvent, version: int):
    return freeze_payload(
        reducer.apply(state, _event(pending, version), pending.payload)
    )


def _evidence_record(ref: str, group: str) -> EvidenceRecord:
    return EvidenceRecord(
        evidence_ref=ref,
        side=EvidenceSide.FOR,
        source_group=group,
        provenance_ref=f"provenance:{group}",
        content_digest="sha256:" + hashlib.sha256(ref.encode("utf-8")).hexdigest(),
        observed_at=OBSERVED_AT,
        reliability_milli=900,
        relevance_milli=900,
        revoked=False,
    )


def _belief_binding(record, state) -> BeliefBinding:
    binding = state["claim_binding"]
    return BeliefBinding(
        belief_id=BELIEF_ID,
        belief_revision=state["revision"],
        belief_status=BeliefStatus(state["status"]),
        belief_claim_type=record.claim.claim_type,
        claim_id=binding["claim_id"],
        claim_record_fingerprint=binding["claim_record_fingerprint"],
    )


def test_v1_e2e_claim_to_bound_belief_to_supported_terminal_route() -> None:
    """Primary V1 flow reaches a gated terminal belief with provenance intact."""

    record = _record()
    epr_budget = EpistemicChangeBudget(4096, 512, 262144)

    # EPR first proves that a raw PCR claim cannot silently become a belief.
    create_route = route_epistemic_change(
        record=record,
        belief=None,
        request=EpistemicChangeRequest(
            "request:v1:e2e:create",
            EpistemicIntent.CREATE_BELIEF_FROM_CLAIM,
            (),
        ),
        budget=epr_budget,
    )
    assert create_route.route is EpistemicRoute.CLAIM_TO_BELIEF_BINDING_REQUIRED

    reducer = ClaimBoundBeliefReducer()
    state = freeze_payload(reducer.initial_state())
    create = _command(
        "CMD-V1-E2E-CREATE",
        CREATE_BELIEF_FROM_CLAIM,
        CREATE_BELIEF_FROM_CLAIM_SCHEMA,
        {
            "belief_id": BELIEF_ID,
            "statement": "The bounded V1 claim is supported by independent evidence.",
            "claim_id": record.claim.claim_id,
            "claim_record_fingerprint": record.input_fingerprint,
            "claim_type": record.claim.claim_type.value,
        },
        expected_stream_version=0,
    )
    decision = ClaimBoundBeliefLifecycle().decide(
        create,
        state,
        record=record,
        budget=ClaimBeliefBindingBudget(4096, 512, 262144),
    )
    assert decision.accepted
    for version, pending in enumerate(decision.domain_events, start=1):
        state = _apply(reducer, state, pending, version)

    assert state["status"] == BeliefStatus.HYPOTHESIS.value
    assert state["claim_binding"]["claim_id"] == record.claim.claim_id
    assert state["claim_binding"]["claim_record_fingerprint"] == record.input_fingerprint

    # The now-bound belief can be routed to the existing Evidence Gate owner.
    gate_route = route_epistemic_change(
        record=record,
        belief=_belief_binding(record, state),
        request=EpistemicChangeRequest(
            "request:v1:e2e:gate",
            EpistemicIntent.SEEK_EVIDENCE_GATE_DECISION,
            (),
        ),
        budget=epr_budget,
    )
    assert gate_route.route is EpistemicRoute.P0_015_EVIDENCE_GATE_REQUIRED
    assert gate_route.next_owner is EpistemicOwner.P0_015_EVIDENCE_GATE

    # Attach the exact candidate evidence through the existing belief owner.
    records = (
        _evidence_record("evidence:v1:e2e:1", "source-group:a"),
        _evidence_record("evidence:v1:e2e:2", "source-group:b"),
    )
    version = 3
    for evidence in records:
        attach = _command(
            f"CMD-V1-E2E-ATTACH-{version}",
            ATTACH_EVIDENCE,
            "attach-evidence/v1",
            {
                "belief_id": BELIEF_ID,
                "evidence_ref": evidence.evidence_ref,
                "side": EvidenceSide.FOR.value,
            },
            expected_stream_version=version - 1,
        )
        attach_decision = BeliefLifecycle().decide(attach, state)
        assert attach_decision.accepted
        state = _apply(reducer, state, attach_decision.domain_events[0], version)
        version += 1

    gate = _command(
        "CMD-V1-E2E-GATE",
        APPLY_EVIDENCE_GATE,
        "apply-evidence-gate/v1",
        {
            "belief_id": BELIEF_ID,
            "expected_revision": state["revision"],
            "policy_id": P0_015_CONTEXTUAL_POLICY.policy_id,
            "records": [item.to_value() for item in records],
        },
        expected_stream_version=version - 1,
    )
    gate_decision = EvidenceGatedBeliefLifecycle().decide(gate, state)
    assert gate_decision.accepted
    assert gate_decision.receipt is not None
    assert gate_decision.receipt.outcome is EvidenceGateOutcome.SUPPORTED
    state = _apply(reducer, state, gate_decision.domain_events[0], version)

    # Provenance binding survives promotion, while the terminal result remains
    # owned by P0-015 rather than by PCR, CBP, or EPR.
    assert state["status"] == BeliefStatus.SUPPORTED.value
    assert state["claim_binding"]["claim_id"] == record.claim.claim_id
    assert state["claim_binding"]["claim_record_fingerprint"] == record.input_fingerprint

    terminal_route = route_epistemic_change(
        record=record,
        belief=_belief_binding(record, state),
        request=EpistemicChangeRequest(
            "request:v1:e2e:terminal",
            EpistemicIntent.REVISE_EXISTING_BELIEF,
            (),
        ),
        budget=epr_budget,
    )
    assert terminal_route.route is EpistemicRoute.TERMINAL_RECONSIDERATION_LINEAGE_REQUIRED
    assert terminal_route.next_owner is EpistemicOwner.FUTURE_TERMINAL_RECONSIDERATION_LINEAGE


def test_v1_e2e_negative_boundaries_fail_closed() -> None:
    """Core V1 negative cases cannot silently repair provenance or freshness."""

    record = _record()
    reducer = ClaimBoundBeliefReducer()
    state = freeze_payload(reducer.initial_state())

    bad_create = _command(
        "CMD-V1-E2E-BAD-CREATE",
        CREATE_BELIEF_FROM_CLAIM,
        CREATE_BELIEF_FROM_CLAIM_SCHEMA,
        {
            "belief_id": BELIEF_ID,
            "statement": "A mismatched provenance attempt.",
            "claim_id": "claim:wrong",
            "claim_record_fingerprint": record.input_fingerprint,
            "claim_type": record.claim.claim_type.value,
        },
        expected_stream_version=0,
    )
    rejected = ClaimBoundBeliefLifecycle().decide(
        bad_create,
        state,
        record=record,
        budget=ClaimBeliefBindingBudget(4096, 512, 262144),
    )
    assert not rejected.accepted
    assert rejected.rejection_code is BeliefRejectionCode.INVALID_COMMAND
    assert rejected.domain_events == ()

    create = replace(
        bad_create,
        command_id="CMD-V1-E2E-GOOD-CREATE",
        payload={
            "belief_id": BELIEF_ID,
            "statement": "A correctly bound belief.",
            "claim_id": record.claim.claim_id,
            "claim_record_fingerprint": record.input_fingerprint,
            "claim_type": record.claim.claim_type.value,
        },
    )
    accepted = ClaimBoundBeliefLifecycle().decide(
        create,
        state,
        record=record,
        budget=ClaimBeliefBindingBudget(4096, 512, 262144),
    )
    assert accepted.accepted
    for version, pending in enumerate(accepted.domain_events, start=1):
        state = _apply(reducer, state, pending, version)

    with pytest.raises(EpistemicChangeBindingError):
        route_epistemic_change(
            record=record,
            belief=replace(_belief_binding(record, state), claim_id="claim:wrong"),
            request=EpistemicChangeRequest(
                "request:v1:e2e:mismatch",
                EpistemicIntent.SEEK_EVIDENCE_GATE_DECISION,
                (),
            ),
            budget=EpistemicChangeBudget(4096, 512, 262144),
        )

    stale_gate = _command(
        "CMD-V1-E2E-STALE-GATE",
        APPLY_EVIDENCE_GATE,
        "apply-evidence-gate/v1",
        {
            "belief_id": BELIEF_ID,
            "expected_revision": state["revision"] + 1,
            "policy_id": P0_015_CONTEXTUAL_POLICY.policy_id,
            "records": [],
        },
        expected_stream_version=2,
    )
    stale = EvidenceGatedBeliefLifecycle().decide(stale_gate, state)
    assert not stale.accepted
    assert stale.rejection_code is EvidenceGateRejectionCode.REVISION_CONFLICT
    assert stale.domain_events == ()
