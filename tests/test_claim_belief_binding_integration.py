"""Storage/replay integration for CBP-v0.1 genesis binding."""

from __future__ import annotations

from mentaury.beliefs import belief_schema_definitions, belief_stream_id
from mentaury.claim_belief_binding import (
    CREATE_BELIEF_FROM_CLAIM,
    CREATE_BELIEF_FROM_CLAIM_SCHEMA,
    ClaimBeliefBindingBudget,
    ClaimBoundBeliefLifecycle,
    ClaimBoundBeliefReducer,
    claim_belief_binding_schema_definitions,
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
    ProducerRef,
)
from mentaury.contracts.primitives import freeze_payload
from mentaury.epistemic_types import ClaimType
from mentaury.non_projection import (
    ClaimClass,
    ProvenanceState,
    Sensitivity,
    SourceClass,
    SourceOrigin,
    SubjectRelation,
)
from mentaury.storage import BatchEntry, SQLiteAtomicBatchAppender, SQLiteEventPayloadStore
from mentaury.validation import SchemaRegistry

BELIEF_ID = "belief:cbp:integration"
STREAM_ID = belief_stream_id(BELIEF_ID)


def _record():
    return represent_provenance_claim(
        source=ProvenanceSource(
            source_ref="source:cbp:integration",
            source_actor_ref="actor:researcher",
            source_class=SourceClass.RESEARCH_PRIMARY,
            source_origin=SourceOrigin.PRIMARY,
            provenance_state=ProvenanceState.VERIFIED,
            publication_or_capture_context_ref="context:cbp:integration",
            sensitivity=Sensitivity.NORMAL,
            usage_boundary_ref="usage:research",
            material_gaps=(),
            derivation_refs=(),
        ),
        claim=ClaimRepresentation(
            claim_id="claim:cbp:integration",
            statement_ref="statement:cbp:integration",
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
            applies_to=("scope:cbp:integration",),
            may_support=(),
            does_not_establish=("truth:universal",),
            unknowns=("unknown:statement-equivalence",),
            transfer_limits=("no:auto-belief",),
        ),
        budget=RepresentationBudget(4096, 512, 262144),
    )


def _command(record) -> CommandEnvelope:
    return CommandEnvelope(
        command_id="CMD-CBP-INTEGRATION",
        command_type=CREATE_BELIEF_FROM_CLAIM,
        command_schema=CREATE_BELIEF_FROM_CLAIM_SCHEMA,
        target_stream=STREAM_ID,
        expected_stream_version=0,
        issued_at="2026-08-21T00:00:00Z",
        issuer=ActorRef("operator", "operator:primary"),
        authority=AuthorityRef("CAP-BELIEF", 1),
        correlation_id="CORR-CBP-INTEGRATION",
        idempotency_key="IDEMP-CBP-INTEGRATION",
        payload={
            "belief_id": BELIEF_ID,
            "statement": "Integration-bound belief statement.",
            "claim_id": record.claim.claim_id,
            "claim_record_fingerprint": record.input_fingerprint,
            "claim_type": record.claim.claim_type.value,
        },
    )


def _event(pending, index: int) -> EventEnvelope:
    return EventEnvelope(
        event_id=f"EVT-CBP-INTEGRATION-{index + 1}",
        event_type=pending.event_type,
        envelope_schema_version=1,
        payload_schema=pending.payload_schema,
        stream_id=STREAM_ID,
        stream_version=index + 1,
        batch_id="BATCH-CBP-INTEGRATION",
        batch_index=index,
        batch_size=2,
        occurred_at="2026-08-21T00:00:00Z",
        recorded_at="2026-08-21T00:00:00Z",
        producer=ProducerRef("cbp-integration-test", "0.1.0"),
        initiator=ActorRef("operator", "operator:primary"),
        authority=AuthorityRef("CAP-BELIEF", 1),
        causation_id="CMD-CBP-INTEGRATION",
        correlation_id="CORR-CBP-INTEGRATION",
        affects_domain_state=pending.affects_domain_state,
        payload_digest=f"sha256:untrusted-payload-{index}",
        payload_ref=f"PAYLOAD-CBP-INTEGRATION-{index + 1}",
        previous_hash=f"sha256:untrusted-previous-{index}",
        event_hash=f"sha256:untrusted-event-{index}",
    )


def test_cbp_genesis_binding_commits_atomically_and_replays() -> None:
    record = _record()
    reducer = ClaimBoundBeliefReducer()
    state = freeze_payload(reducer.initial_state())
    decision = ClaimBoundBeliefLifecycle().decide(
        _command(record),
        state,
        record=record,
        budget=ClaimBeliefBindingBudget(4096, 512, 262144),
    )
    assert decision.accepted
    assert len(decision.domain_events) == 2

    registry = SchemaRegistry(
        [
            *belief_schema_definitions(),
            *claim_belief_binding_schema_definitions(),
        ]
    )
    entries = tuple(
        BatchEntry(_event(pending, index), pending.payload)
        for index, pending in enumerate(decision.domain_events)
    )

    with SQLiteEventPayloadStore.in_memory() as store:
        store.initialize_schema()
        receipt = SQLiteAtomicBatchAppender(store, registry).append(entries)
        assert receipt.first_stream_version == 1
        assert receipt.last_stream_version == 2
        committed = store.list_stream(STREAM_ID)
        assert [event.event_type for event in committed] == [
            "BELIEF_CREATED",
            "BELIEF_CLAIM_BOUND",
        ]

        replay_state = freeze_payload(reducer.initial_state())
        for event in committed:
            payload = store.load_payload(event.payload_ref)
            assert payload is not None
            replay_state = freeze_payload(reducer.apply(replay_state, event, payload))

        binding = replay_state["claim_binding"]
        assert binding["claim_id"] == record.claim.claim_id
        assert binding["claim_record_fingerprint"] == record.input_fingerprint
        assert binding["belief_revision"] == 1
