"""Frozen EPR-v0.1 routing table, adversarial and metamorphic requirements."""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

from mentaury.beliefs import BeliefStatus
from mentaury.claims import (
    ClaimRepresentation,
    ClaimScope,
    EpistemicRole,
    ProvenanceSource,
    RepresentationBudget,
    represent_provenance_claim,
)
from mentaury.epistemic_change import (
    EPISTEMIC_CHANGE_CONTRACT_VERSION,
    HARD_MAX_CANONICAL_INPUT_BYTES,
    HARD_MAX_STRING_BYTES,
    HARD_MAX_TUPLE_ITEMS,
    BeliefBinding,
    EpistemicChangeBindingError,
    EpistemicChangeBudget,
    EpistemicChangeBudgetExceeded,
    EpistemicChangeContractError,
    EpistemicChangeRequest,
    EpistemicIntent,
    EpistemicOwner,
    EpistemicRoute,
    EpistemicRouteReason,
    route_epistemic_change,
)
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
PACKAGE = ROOT / "src" / "mentaury" / "epistemic_change"


def _record(*, statement_ref: str = "statement:epr:001", claim_type: ClaimType = ClaimType.CONTEXTUAL):
    return represent_provenance_claim(
        source=ProvenanceSource(
            source_ref="source:epr:001",
            source_actor_ref="actor:researcher",
            source_class=SourceClass.RESEARCH_PRIMARY,
            source_origin=SourceOrigin.PRIMARY,
            provenance_state=ProvenanceState.VERIFIED,
            publication_or_capture_context_ref="context:epr",
            sensitivity=Sensitivity.NORMAL,
            usage_boundary_ref="usage:research",
            material_gaps=(),
            derivation_refs=(),
        ),
        claim=ClaimRepresentation(
            claim_id="claim:epr:001",
            statement_ref=statement_ref,
            claim_class=ClaimClass.FACTUAL,
            claim_type=claim_type,
            epistemic_role=EpistemicRole.TESTIMONY,
            directly_stated=True,
            speaker_ref="actor:researcher",
            subject_ref="subject:world",
            subject_relation=SubjectRelation.NON_SELF,
            basis_refs=(),
            evidence_refs=("evidence:candidate:001",),
        ),
        scope=ClaimScope(
            applies_to=("scope:epr",),
            may_support=("question:epr",),
            does_not_establish=("truth:universal",),
            unknowns=("unknown:epr",),
            transfer_limits=("no:auto-belief",),
        ),
        budget=RepresentationBudget(4096, 512, 262144),
    )


def _budget(**changes: int) -> EpistemicChangeBudget:
    values = {
        "max_string_bytes": HARD_MAX_STRING_BYTES,
        "max_tuple_items": HARD_MAX_TUPLE_ITEMS,
        "max_canonical_input_bytes": HARD_MAX_CANONICAL_INPUT_BYTES,
    }
    values.update(changes)
    return EpistemicChangeBudget(**values)


def _request(intent: EpistemicIntent, *, reason_refs: tuple[str, ...] = ()) -> EpistemicChangeRequest:
    return EpistemicChangeRequest(
        request_id=f"request:{intent.value}",
        intent=intent,
        reason_refs=reason_refs,
    )


def _belief(
    record,
    *,
    status: BeliefStatus = BeliefStatus.HYPOTHESIS,
    revision: int = 1,
    claim_id: str | None = None,
    claim_type: ClaimType | None = None,
    fingerprint: str | None = None,
) -> BeliefBinding:
    return BeliefBinding(
        belief_id="belief:epr:001",
        belief_revision=revision,
        belief_status=status,
        belief_claim_type=claim_type or record.claim.claim_type,
        claim_id=claim_id or record.claim.claim_id,
        claim_record_fingerprint=fingerprint or record.input_fingerprint,
    )


@pytest.mark.parametrize(
    ("intent", "route", "owner", "reason"),
    [
        (EpistemicIntent.RETAIN_CLAIM, EpistemicRoute.RETAIN_CLAIM_ONLY, EpistemicOwner.PCR_V0_1, EpistemicRouteReason.CALLER_RETAINED_CLAIM),
        (EpistemicIntent.CREATE_BELIEF_FROM_CLAIM, EpistemicRoute.CLAIM_TO_BELIEF_BINDING_REQUIRED, EpistemicOwner.FUTURE_CLAIM_TO_BELIEF_BINDING, EpistemicRouteReason.CLAIM_BINDING_PREREQUISITE),
        (EpistemicIntent.SEEK_EVIDENCE_GATE_DECISION, EpistemicRoute.CLAIM_TO_BELIEF_BINDING_REQUIRED, EpistemicOwner.FUTURE_CLAIM_TO_BELIEF_BINDING, EpistemicRouteReason.CLAIM_BINDING_PREREQUISITE),
        (EpistemicIntent.REVISE_EXISTING_BELIEF, EpistemicRoute.DEFER, EpistemicOwner.NONE, EpistemicRouteReason.INTENT_PRECONDITION_UNMET),
        (EpistemicIntent.RECONSIDER_TERMINAL_BELIEF, EpistemicRoute.DEFER, EpistemicOwner.NONE, EpistemicRouteReason.INTENT_PRECONDITION_UNMET),
        (EpistemicIntent.DEFER, EpistemicRoute.DEFER, EpistemicOwner.NONE, EpistemicRouteReason.CALLER_DEFERRED),
    ],
)
def test_epr_routing_table_without_belief(intent, route, owner, reason) -> None:
    plan = route_epistemic_change(
        record=_record(), belief=None, request=_request(intent), budget=_budget()
    )
    assert (plan.route, plan.next_owner, plan.reason) == (route, owner, reason)


@pytest.mark.parametrize(
    ("intent", "route", "owner", "reason"),
    [
        (EpistemicIntent.RETAIN_CLAIM, EpistemicRoute.RETAIN_CLAIM_ONLY, EpistemicOwner.PCR_V0_1, EpistemicRouteReason.CALLER_RETAINED_CLAIM),
        (EpistemicIntent.CREATE_BELIEF_FROM_CLAIM, EpistemicRoute.DEFER, EpistemicOwner.NONE, EpistemicRouteReason.INTENT_PRECONDITION_UNMET),
        (EpistemicIntent.REVISE_EXISTING_BELIEF, EpistemicRoute.P0_014_NON_TERMINAL_REVISION_REQUIRED, EpistemicOwner.P0_014_BELIEF_LIFECYCLE, EpistemicRouteReason.NON_TERMINAL_REVISION_OWNER),
        (EpistemicIntent.SEEK_EVIDENCE_GATE_DECISION, EpistemicRoute.P0_015_EVIDENCE_GATE_REQUIRED, EpistemicOwner.P0_015_EVIDENCE_GATE, EpistemicRouteReason.EVIDENCE_GATE_OWNER),
        (EpistemicIntent.RECONSIDER_TERMINAL_BELIEF, EpistemicRoute.DEFER, EpistemicOwner.NONE, EpistemicRouteReason.INTENT_PRECONDITION_UNMET),
        (EpistemicIntent.DEFER, EpistemicRoute.DEFER, EpistemicOwner.NONE, EpistemicRouteReason.CALLER_DEFERRED),
    ],
)
def test_epr_routing_table_non_terminal_belief(intent, route, owner, reason) -> None:
    record = _record()
    plan = route_epistemic_change(
        record=record,
        belief=_belief(record),
        request=_request(intent),
        budget=_budget(),
    )
    assert (plan.route, plan.next_owner, plan.reason) == (route, owner, reason)


@pytest.mark.parametrize(
    "status",
    [BeliefStatus.SUPPORTED, BeliefStatus.CONTRADICTED, BeliefStatus.SUPERSEDED],
)
@pytest.mark.parametrize(
    "intent",
    [
        EpistemicIntent.CREATE_BELIEF_FROM_CLAIM,
        EpistemicIntent.REVISE_EXISTING_BELIEF,
        EpistemicIntent.SEEK_EVIDENCE_GATE_DECISION,
        EpistemicIntent.RECONSIDER_TERMINAL_BELIEF,
    ],
)
def test_epr_terminal_belief_always_routes_to_future_lineage(status, intent) -> None:
    record = _record()
    plan = route_epistemic_change(
        record=record,
        belief=_belief(record, status=status),
        request=_request(intent),
        budget=_budget(),
    )
    assert plan.route is EpistemicRoute.TERMINAL_RECONSIDERATION_LINEAGE_REQUIRED
    assert plan.next_owner is EpistemicOwner.FUTURE_TERMINAL_RECONSIDERATION_LINEAGE
    assert plan.reason is EpistemicRouteReason.TERMINAL_LINEAGE_PREREQUISITE


def test_epr_t01_t03_record_evidence_or_caller_intent_cannot_promote_belief() -> None:
    record = _record()
    plan = route_epistemic_change(
        record=record,
        belief=None,
        request=_request(EpistemicIntent.SEEK_EVIDENCE_GATE_DECISION),
        budget=_budget(),
    )
    assert plan.route is EpistemicRoute.CLAIM_TO_BELIEF_BINDING_REQUIRED
    assert "status" not in plan.to_value()
    assert "evidence" not in plan.to_value()
    with pytest.raises(TypeError):
        EpistemicChangeRequest(
            request_id="bad", intent=EpistemicIntent.RETAIN_CLAIM, reason_refs=(), target_status="supported"  # type: ignore[call-arg]
        )


def test_epr_t04_router_does_not_import_or_duplicate_evidence_gate_logic() -> None:
    source = (PACKAGE / "router.py").read_text(encoding="utf-8")
    assert "EvidenceGate" not in source
    assert "threshold" not in source.lower()
    assert "policy" not in source.lower()


@pytest.mark.parametrize(
    "changes",
    [
        {"claim_id": "claim:wrong"},
        {"claim_type": ClaimType.UNIVERSAL},
        {"fingerprint": "0" * 64},
    ],
)
def test_epr_t06_binding_mismatch_fails_closed(changes) -> None:
    record = _record()
    with pytest.raises(EpistemicChangeBindingError):
        route_epistemic_change(
            record=record,
            belief=_belief(record, **changes),
            request=_request(EpistemicIntent.REVISE_EXISTING_BELIEF),
            budget=_budget(),
        )


def test_epr_t07_belief_revision_is_routing_data_not_execution_authority() -> None:
    record = _record()
    one = route_epistemic_change(
        record=record,
        belief=_belief(record, revision=1),
        request=_request(EpistemicIntent.REVISE_EXISTING_BELIEF),
        budget=_budget(),
    )
    two = route_epistemic_change(
        record=record,
        belief=_belief(record, revision=2),
        request=_request(EpistemicIntent.REVISE_EXISTING_BELIEF),
        budget=_budget(),
    )
    assert one.route is two.route is EpistemicRoute.P0_014_NON_TERMINAL_REVISION_REQUIRED
    assert one.routing_input_fingerprint != two.routing_input_fingerprint


def test_epr_t08_t09_terminal_route_never_constructs_successor_or_mutation() -> None:
    record = _record()
    plan = route_epistemic_change(
        record=record,
        belief=_belief(record, status=BeliefStatus.SUPPORTED),
        request=_request(EpistemicIntent.RECONSIDER_TERMINAL_BELIEF),
        budget=_budget(),
    )
    assert plan.route is EpistemicRoute.TERMINAL_RECONSIDERATION_LINEAGE_REQUIRED
    assert set(plan.to_value()) == {
        "contract_version",
        "request_id",
        "route",
        "next_owner",
        "reason",
        "record_fingerprint",
        "belief_id",
        "belief_revision",
        "routing_input_fingerprint",
    }


def test_epr_t10_owner_types_remain_distinct() -> None:
    assert ClaimType is not BeliefStatus
    assert EpistemicRoute is not EpistemicIntent
    assert EpistemicOwner is not EpistemicRoute


def test_epr_t11_t12_plan_contains_no_capability_action_identity_or_runtime_handle() -> None:
    plan = route_epistemic_change(
        record=_record(),
        belief=None,
        request=_request(EpistemicIntent.RETAIN_CLAIM),
        budget=_budget(),
    )
    forbidden = {
        "permission",
        "capability",
        "action",
        "identity",
        "relationship",
        "m3",
        "command",
        "event",
        "receipt",
        "target_status",
    }
    assert not (set(plan.to_value()) & forbidden)


def test_epr_m01_record_semantic_change_changes_fingerprint() -> None:
    a = route_epistemic_change(
        record=_record(statement_ref="statement:epr:a"),
        belief=None,
        request=_request(EpistemicIntent.RETAIN_CLAIM),
        budget=_budget(),
    )
    b = route_epistemic_change(
        record=_record(statement_ref="statement:epr:b"),
        belief=None,
        request=_request(EpistemicIntent.RETAIN_CLAIM),
        budget=_budget(),
    )
    assert a.routing_input_fingerprint != b.routing_input_fingerprint


def test_epr_m02_intent_changes_route_and_fingerprint() -> None:
    record = _record()
    retain = route_epistemic_change(
        record=record,
        belief=None,
        request=_request(EpistemicIntent.RETAIN_CLAIM),
        budget=_budget(),
    )
    create = route_epistemic_change(
        record=record,
        belief=None,
        request=_request(EpistemicIntent.CREATE_BELIEF_FROM_CLAIM),
        budget=_budget(),
    )
    assert retain.route is not create.route
    assert retain.routing_input_fingerprint != create.routing_input_fingerprint


def test_epr_m08_terminal_vs_non_terminal_changes_owner_route() -> None:
    record = _record()
    request = _request(EpistemicIntent.REVISE_EXISTING_BELIEF)
    non_terminal = route_epistemic_change(
        record=record, belief=_belief(record), request=request, budget=_budget()
    )
    terminal = route_epistemic_change(
        record=record,
        belief=_belief(record, status=BeliefStatus.SUPPORTED),
        request=request,
        budget=_budget(),
    )
    assert non_terminal.next_owner is EpistemicOwner.P0_014_BELIEF_LIFECYCLE
    assert terminal.next_owner is EpistemicOwner.FUTURE_TERMINAL_RECONSIDERATION_LINEAGE


def test_epr_m09_reason_refs_change_identity_not_support_or_permission() -> None:
    record = _record()
    a = route_epistemic_change(
        record=record,
        belief=None,
        request=_request(EpistemicIntent.RETAIN_CLAIM),
        budget=_budget(),
    )
    b = route_epistemic_change(
        record=record,
        belief=None,
        request=_request(EpistemicIntent.RETAIN_CLAIM, reason_refs=("reason:a",)),
        budget=_budget(),
    )
    assert a.route is b.route is EpistemicRoute.RETAIN_CLAIM_ONLY
    assert a.routing_input_fingerprint != b.routing_input_fingerprint


def test_epr_m10_duplicate_or_unsorted_reason_refs_fail_closed() -> None:
    with pytest.raises(EpistemicChangeContractError):
        EpistemicChangeRequest(
            "request:dup", EpistemicIntent.DEFER, ("reason:a", "reason:a")
        )
    with pytest.raises(EpistemicChangeContractError):
        EpistemicChangeRequest(
            "request:sort", EpistemicIntent.DEFER, ("reason:b", "reason:a")
        )


def test_epr_local_budget_fails_without_truncation_or_repair() -> None:
    with pytest.raises(EpistemicChangeBudgetExceeded):
        route_epistemic_change(
            record=_record(),
            belief=None,
            request=_request(EpistemicIntent.RETAIN_CLAIM),
            budget=_budget(max_string_bytes=8),
        )


def test_epr_exact_frozen_contract_version_and_determinism() -> None:
    record = _record()
    request = _request(EpistemicIntent.RETAIN_CLAIM)
    first = route_epistemic_change(
        record=record, belief=None, request=request, budget=_budget()
    )
    second = route_epistemic_change(
        record=record, belief=None, request=request, budget=_budget()
    )
    assert first.contract_version == EPISTEMIC_CHANGE_CONTRACT_VERSION == "EPR-v0.1"
    assert first == second


def test_epr_no_hidden_io_execution_or_owner_invocation_imports() -> None:
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
        "storage",
        "lifecycle",
        "evidence_gate",
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
