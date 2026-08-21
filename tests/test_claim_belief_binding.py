"""CBP-v0.1 claim-to-belief provenance binding acceptance and adversarial coverage."""

from __future__ import annotations

import ast
from dataclasses import replace
from pathlib import Path

import pytest

from mentaury.beliefs import (
    ATTACH_EVIDENCE,
    CREATE_BELIEF,
    BeliefLifecycle,
    BeliefReducerError,
    BeliefRejectionCode,
    BeliefStatus,
    EvidenceSide,
    belief_stream_id,
)
from mentaury.claim_belief_binding import (
    BELIEF_CLAIM_BOUND,
    CLAIM_BELIEF_BINDING_CONTRACT_VERSION,
    CREATE_BELIEF_FROM_CLAIM,
    CREATE_BELIEF_FROM_CLAIM_SCHEMA,
    HARD_MAX_CANONICAL_INPUT_BYTES,
    HARD_MAX_STRING_BYTES,
    HARD_MAX_TUPLE_ITEMS,
    ClaimBeliefBindingBudget,
    ClaimBeliefBindingBudgetExceeded,
    ClaimBoundBeliefLifecycle,
    ClaimBoundBeliefReducer,
    StatementEquivalence,
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
from mentaury.epistemic_types import ClaimType
from mentaury.non_projection import (
    ClaimClass,
    ProvenanceState,
    Sensitivity,
    SourceClass,
    SourceOrigin,
    SubjectRelation,
)

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "src" / "mentaury" / "claim_belief_binding"
BELIEF_ID = "belief:cbp:001"
STREAM_ID = belief_stream_id(BELIEF_ID)


def _record(*, claim_type: ClaimType = ClaimType.CONTEXTUAL):
    source = ProvenanceSource(
        source_ref="source:cbp:001",
        source_actor_ref="actor:researcher",
        source_class=SourceClass.RESEARCH_PRIMARY,
        source_origin=SourceOrigin.PRIMARY,
        provenance_state=ProvenanceState.VERIFIED,
        publication_or_capture_context_ref="context:cbp",
        sensitivity=Sensitivity.NORMAL,
        usage_boundary_ref="usage:research",
        material_gaps=(),
        derivation_refs=(),
    )
    claim = ClaimRepresentation(
        claim_id="claim:cbp:001",
        statement_ref="statement:opaque-ref:001",
        claim_class=ClaimClass.FACTUAL,
        claim_type=claim_type,
        epistemic_role=EpistemicRole.TESTIMONY,
        directly_stated=True,
        speaker_ref="actor:researcher",
        subject_ref="subject:world",
        subject_relation=SubjectRelation.NON_SELF,
        basis_refs=(),
        evidence_refs=("evidence:candidate:001",),
    )
    scope = ClaimScope(
        applies_to=("scope:cbp",),
        may_support=("question:cbp",),
        does_not_establish=("truth:universal",),
        unknowns=("unknown:statement-byte-equivalence",),
        transfer_limits=("no:auto-belief",),
    )
    return represent_provenance_claim(
        source=source,
        claim=claim,
        scope=scope,
        budget=RepresentationBudget(4096, 512, 262144),
    )


def _budget(**changes: int) -> ClaimBeliefBindingBudget:
    values = {
        "max_string_bytes": HARD_MAX_STRING_BYTES,
        "max_tuple_items": HARD_MAX_TUPLE_ITEMS,
        "max_canonical_input_bytes": HARD_MAX_CANONICAL_INPUT_BYTES,
    }
    values.update(changes)
    return ClaimBeliefBindingBudget(**values)


def _command(record=None, **payload_changes: object) -> CommandEnvelope:
    record = record or _record()
    payload: dict[str, object] = {
        "belief_id": BELIEF_ID,
        "statement": "A bounded belief statement whose byte equality is not inferred.",
        "claim_id": record.claim.claim_id,
        "claim_record_fingerprint": record.input_fingerprint,
        "claim_type": record.claim.claim_type.value,
    }
    payload.update(payload_changes)
    return CommandEnvelope(
        command_id="CMD-CBP-001",
        command_type=CREATE_BELIEF_FROM_CLAIM,
        command_schema=CREATE_BELIEF_FROM_CLAIM_SCHEMA,
        target_stream=STREAM_ID,
        expected_stream_version=0,
        issued_at="2026-08-21T00:00:00Z",
        issuer=ActorRef("operator", "operator:primary"),
        authority=AuthorityRef("CAP-BELIEF", 1),
        correlation_id="CORR-CBP",
        idempotency_key="IDEMP-CBP-001",
        payload=payload,
    )


def _base_create_command(record=None) -> CommandEnvelope:
    record = record or _record()
    return CommandEnvelope(
        command_id="CMD-CBP-001",
        command_type=CREATE_BELIEF,
        command_schema="create-belief/v1",
        target_stream=STREAM_ID,
        expected_stream_version=0,
        issued_at="2026-08-21T00:00:00Z",
        issuer=ActorRef("operator", "operator:primary"),
        authority=AuthorityRef("CAP-BELIEF", 1),
        correlation_id="CORR-CBP",
        idempotency_key="IDEMP-CBP-001",
        payload={
            "belief_id": BELIEF_ID,
            "statement": "A bounded belief statement whose byte equality is not inferred.",
            "claim_type": record.claim.claim_type.value,
        },
    )


def _event(
    pending: PendingEvent,
    *,
    stream_version: int,
    batch_index: int,
    batch_size: int = 2,
) -> EventEnvelope:
    return EventEnvelope(
        event_id=f"EVT-CBP-{stream_version}",
        event_type=pending.event_type,
        envelope_schema_version=1,
        payload_schema=pending.payload_schema,
        stream_id=STREAM_ID,
        stream_version=stream_version,
        batch_id="BATCH-CBP-001",
        batch_index=batch_index,
        batch_size=batch_size,
        occurred_at="2026-08-21T00:00:00Z",
        recorded_at="2026-08-21T00:00:00Z",
        producer=ProducerRef("cbp-test", "0.1.0"),
        initiator=ActorRef("operator", "operator:primary"),
        authority=AuthorityRef("CAP-BELIEF", 1),
        causation_id="CMD-CBP-001",
        correlation_id="CORR-CBP",
        affects_domain_state=pending.affects_domain_state,
        payload_digest="sha256:untrusted",
        payload_ref=f"PAYLOAD-CBP-{stream_version}",
        previous_hash="sha256:untrusted",
        event_hash="sha256:untrusted",
    )


def _bound_state():
    record = _record()
    reducer = ClaimBoundBeliefReducer()
    state = freeze_payload(reducer.initial_state())
    decision = ClaimBoundBeliefLifecycle().decide(
        _command(record),
        state,
        record=record,
        budget=_budget(),
    )
    assert decision.accepted
    for index, pending in enumerate(decision.domain_events):
        state = freeze_payload(
            reducer.apply(
                state,
                _event(pending, stream_version=index + 1, batch_index=index),
                pending.payload,
            )
        )
    return state


def test_cbp_t01_delegates_genesis_to_p0_014_and_emits_ordered_binding() -> None:
    record = _record()
    state = freeze_payload(ClaimBoundBeliefReducer().initial_state())
    decision = ClaimBoundBeliefLifecycle().decide(
        _command(record), state, record=record, budget=_budget()
    )
    assert decision.accepted
    assert len(decision.domain_events) == 2
    assert decision.domain_events[0] == BeliefLifecycle().decide(
        _base_create_command(record), state
    ).domain_events[0]
    assert decision.domain_events[1].event_type == BELIEF_CLAIM_BOUND
    assert (
        decision.domain_events[1].payload["contract_version"]
        == CLAIM_BELIEF_BINDING_CONTRACT_VERSION
    )


def test_cbp_t02_bound_projection_preserves_exact_pcr_identity() -> None:
    record = _record()
    state = _bound_state()
    binding = state["claim_binding"]
    assert binding["claim_id"] == record.claim.claim_id
    assert binding["claim_record_fingerprint"] == record.input_fingerprint
    assert binding["claim_type"] == record.claim.claim_type.value
    assert binding["statement_ref"] == record.claim.statement_ref
    assert binding["belief_revision"] == 1


def test_cbp_t03_statement_ref_never_claims_concrete_statement_equivalence() -> None:
    state = _bound_state()
    binding = state["claim_binding"]
    assert binding["statement_equivalence"] == StatementEquivalence.NOT_ESTABLISHED.value
    assert binding["statement_ref"] != state["statement"]


def test_cbp_t04_wrong_claim_id_fingerprint_or_claim_type_fails_closed() -> None:
    record = _record()
    state = freeze_payload(ClaimBoundBeliefReducer().initial_state())
    cases = (
        {"claim_id": "claim:wrong"},
        {"claim_record_fingerprint": "0" * 64},
        {"claim_type": ClaimType.UNIVERSAL.value},
    )
    for changes in cases:
        decision = ClaimBoundBeliefLifecycle().decide(
            _command(record, **changes),
            state,
            record=record,
            budget=_budget(),
        )
        assert not decision.accepted
        assert decision.rejection_code is BeliefRejectionCode.INVALID_COMMAND
        assert decision.domain_events == ()


def test_cbp_t05_command_payload_is_exact_and_cannot_smuggle_target_status() -> None:
    record = _record()
    state = freeze_payload(ClaimBoundBeliefReducer().initial_state())
    decision = ClaimBoundBeliefLifecycle().decide(
        _command(record, target_status=BeliefStatus.SUPPORTED.value),
        state,
        record=record,
        budget=_budget(),
    )
    assert not decision.accepted
    assert decision.rejection_code is BeliefRejectionCode.INVALID_COMMAND


def test_cbp_t06_pcr_evidence_refs_do_not_promote_belief_status() -> None:
    state = _bound_state()
    assert state["status"] == BeliefStatus.HYPOTHESIS.value
    assert state["evidence_for"] == ()
    assert state["evidence_against"] == ()


def test_cbp_t07_binding_event_cannot_exist_before_belief_genesis() -> None:
    record = _record()
    reducer = ClaimBoundBeliefReducer()
    state = freeze_payload(reducer.initial_state())
    decision = ClaimBoundBeliefLifecycle().decide(
        _command(record), state, record=record, budget=_budget()
    )
    binding_event = decision.domain_events[1]
    with pytest.raises(BeliefReducerError):
        reducer.apply(
            state,
            _event(binding_event, stream_version=1, batch_index=0, batch_size=1),
            binding_event.payload,
        )


def test_cbp_t08_duplicate_or_late_binding_fails_closed() -> None:
    state = _bound_state()
    binding = dict(state["claim_binding"])
    binding.pop("binding_event_id")
    pending = PendingEvent(BELIEF_CLAIM_BOUND, "belief-claim-bound/v1", True, binding)
    reducer = ClaimBoundBeliefReducer()
    with pytest.raises(BeliefReducerError, match="already has a claim binding"):
        reducer.apply(
            state,
            _event(pending, stream_version=3, batch_index=0, batch_size=1),
            pending.payload,
        )
    late = dict(state)
    late["claim_binding"] = None
    late["revision"] = 2
    with pytest.raises(BeliefReducerError, match="genesis revision 1"):
        reducer.apply(
            freeze_payload(late),
            _event(pending, stream_version=3, batch_index=0, batch_size=1),
            pending.payload,
        )


def test_cbp_t09_binding_survives_later_p0_014_events_without_taking_authority() -> None:
    state = _bound_state()
    binding_before = state["claim_binding"]
    attach = CommandEnvelope(
        command_id="CMD-ATTACH-CBP",
        command_type=ATTACH_EVIDENCE,
        command_schema="attach-evidence/v1",
        target_stream=STREAM_ID,
        expected_stream_version=2,
        issued_at="2026-08-21T00:01:00Z",
        issuer=ActorRef("operator", "operator:primary"),
        authority=AuthorityRef("CAP-BELIEF", 1),
        correlation_id="CORR-CBP",
        idempotency_key="IDEMP-ATTACH-CBP",
        payload={
            "belief_id": BELIEF_ID,
            "evidence_ref": "evidence:later:1",
            "side": EvidenceSide.FOR.value,
        },
    )
    decision = BeliefLifecycle().decide(attach, state)
    assert decision.accepted
    pending = decision.domain_events[0]
    state = freeze_payload(
        ClaimBoundBeliefReducer().apply(
            state,
            _event(pending, stream_version=3, batch_index=0, batch_size=1),
            pending.payload,
        )
    )
    assert state["claim_binding"] == binding_before
    assert state["status"] == BeliefStatus.HYPOTHESIS.value


def test_cbp_t10_binding_output_contains_no_truth_evidence_identity_or_action_authority() -> None:
    record = _record()
    state = freeze_payload(ClaimBoundBeliefReducer().initial_state())
    decision = ClaimBoundBeliefLifecycle().decide(
        _command(record), state, record=record, budget=_budget()
    )
    payload = decision.domain_events[1].payload
    forbidden = {
        "supported",
        "contradicted",
        "truth",
        "confidence",
        "identity",
        "relationship",
        "m3",
        "permission",
        "capability",
        "action",
        "target_status",
    }
    assert not ({key.lower() for key in payload} & forbidden)
    assert StatementEquivalence.NOT_ESTABLISHED.value in repr(dict(payload))


def test_cbp_t11_binding_fingerprint_is_deterministic_and_input_sensitive() -> None:
    record = _record()
    state = freeze_payload(ClaimBoundBeliefReducer().initial_state())
    lifecycle = ClaimBoundBeliefLifecycle()
    a = lifecycle.decide(_command(record), state, record=record, budget=_budget())
    b = lifecycle.decide(_command(record), state, record=record, budget=_budget())
    changed = lifecycle.decide(
        _command(record, statement="A different bounded statement."),
        state,
        record=record,
        budget=_budget(),
    )
    assert (
        a.domain_events[1].payload["binding_input_fingerprint"]
        == b.domain_events[1].payload["binding_input_fingerprint"]
    )
    assert (
        a.domain_events[1].payload["binding_input_fingerprint"]
        != changed.domain_events[1].payload["binding_input_fingerprint"]
    )


def test_cbp_t12_local_budget_fails_without_truncation_or_repair() -> None:
    record = _record()
    state = freeze_payload(ClaimBoundBeliefReducer().initial_state())
    with pytest.raises(ClaimBeliefBindingBudgetExceeded):
        ClaimBoundBeliefLifecycle().decide(
            _command(record),
            state,
            record=record,
            budget=_budget(max_string_bytes=8),
        )


def test_cbp_t13_no_hidden_io_runtime_or_evidence_gate_ownership_imports() -> None:
    forbidden = (
        "requests",
        "httpx",
        "urllib",
        "socket",
        "subprocess",
        "sqlite",
        "sqlalchemy",
        "openai",
        "retrieval",
        "scheduler",
        "identity",
        "relationship",
        "action",
    )
    for path in PACKAGE.glob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        imports: list[str] = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.extend(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imports.append(node.module)
        for imported in imports:
            assert not any(token in imported.lower() for token in forbidden)


def test_cbp_t14_wrong_command_schema_fails_closed() -> None:
    record = _record()
    state = freeze_payload(ClaimBoundBeliefReducer().initial_state())
    command = replace(_command(record), command_schema="create-belief-from-claim/v2")
    decision = ClaimBoundBeliefLifecycle().decide(
        command, state, record=record, budget=_budget()
    )
    assert not decision.accepted
    assert decision.rejection_code is BeliefRejectionCode.INVALID_COMMAND
