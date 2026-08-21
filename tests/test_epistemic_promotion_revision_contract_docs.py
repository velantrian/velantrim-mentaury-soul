"""Structural guards for the EPR-v0.1 freeze and later bounded implementation."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
READINESS = (
    ROOT / "docs" / "research" / "EPISTEMIC_PROMOTION_REVISION_READINESS.md"
).read_text(encoding="utf-8")
SELECTION = (
    ROOT
    / "docs"
    / "research"
    / "EPISTEMIC_PROMOTION_REVISION_CANDIDATE_SELECTION.md"
).read_text(encoding="utf-8")
CONTRACT = (
    ROOT / "docs" / "research" / "EPISTEMIC_PROMOTION_REVISION_CONTRACT_V0_1.md"
).read_text(encoding="utf-8")
OWNER_GO = (
    ROOT / "docs" / "research" / "EPISTEMIC_PROMOTION_REVISION_OWNER_GO_DECISION.md"
).read_text(encoding="utf-8")
IMPLEMENTATION = (
    ROOT / "docs" / "research" / "EPISTEMIC_PROMOTION_REVISION_IMPLEMENTATION_V0_1.md"
).read_text(encoding="utf-8")
BELIEF_CONTRACTS = (
    ROOT / "src" / "mentaury" / "beliefs" / "contracts.py"
).read_text(encoding="utf-8")
BELIEF_LIFECYCLE = (
    ROOT / "src" / "mentaury" / "beliefs" / "lifecycle.py"
).read_text(encoding="utf-8")
EVIDENCE_GATE = (
    ROOT / "src" / "mentaury" / "beliefs" / "evidence_gate.py"
).read_text(encoding="utf-8")
PCR_CONTRACT = (
    ROOT
    / "docs"
    / "research"
    / "PROVENANCE_CLAIM_REPRESENTATION_CONTRACT_V0_1.md"
).read_text(encoding="utf-8")


def test_phase4_readiness_and_candidate_are_historically_docs_only() -> None:
    assert "READINESS_READY · DOCS_ONLY" in READINESS
    assert "CANDIDATE_SELECTED · DOCS_ONLY" in SELECTION
    assert "PURE_EPISTEMIC_CHANGE_ROUTER" in SELECTION
    assert "Implementation:                      NOT_STARTED" in CONTRACT
    assert "Owner GO:                            NOT_GRANTED" in CONTRACT
    assert "Runtime activation:                  NOT_AUTHORIZED" in CONTRACT


def test_epr_contract_freezes_exact_candidate_and_version() -> None:
    for marker in (
        'Contract version:                    EPR-v0.1',
        'Candidate:                           PURE_EPISTEMIC_CHANGE_ROUTER',
        'EPISTEMIC_CHANGE_CONTRACT_VERSION = "EPR-v0.1"',
        'INPUT_FINGERPRINT_DOMAIN          = "MENTAURY_EPISTEMIC_CHANGE_INPUT_V1"',
        'def route_epistemic_change(',
        'src/mentaury/epistemic_change/__init__.py',
        'src/mentaury/epistemic_change/contracts.py',
        'src/mentaury/epistemic_change/router.py',
    ):
        assert marker in CONTRACT


def test_router_has_no_terminal_status_input_or_decision_authority() -> None:
    for marker in (
        "requested BeliefStatus",
        "target_status",
        "EvidenceGateOutcome",
        "EvidenceGateReceipt as permission",
        "No intent specifies a target belief status.",
        "VALID ROUTE",
        "≠ EvidenceGateOutcome",
        "≠ SUPPORTED / CONTRADICTED",
    ):
        assert marker in CONTRACT


def test_selected_routes_preserve_owner_boundaries() -> None:
    for marker in (
        "RETAIN_CLAIM_ONLY",
        "CLAIM_TO_BELIEF_BINDING_REQUIRED",
        "P0_014_NON_TERMINAL_REVISION_REQUIRED",
        "P0_015_EVIDENCE_GATE_REQUIRED",
        "TERMINAL_RECONSIDERATION_LINEAGE_REQUIRED",
        "DEFER",
        "FUTURE_CLAIM_TO_BELIEF_BINDING",
        "P0_014_BELIEF_LIFECYCLE",
        "P0_015_EVIDENCE_GATE",
        "FUTURE_TERMINAL_RECONSIDERATION_LINEAGE",
    ):
        assert marker in CONTRACT
        assert marker in SELECTION


def test_live_p0_owner_semantics_are_not_redefined() -> None:
    assert "belief_status_requires_evidence_gate" in BELIEF_CONTRACTS
    assert "BeliefStatus.SUPPORTED" in BELIEF_CONTRACTS
    assert "BeliefStatus.CONTRADICTED" in BELIEF_CONTRACTS
    assert "BeliefStatus.SUPERSEDED" in BELIEF_CONTRACTS
    assert "EvidenceGateRejectionCode.TERMINAL_BELIEF" in EVIDENCE_GATE
    assert "BeliefRejectionCode.EVIDENCE_GATE_REQUIRED" in BELIEF_LIFECYCLE
    assert "belief_status_transition_allowed" in CONTRACT
    assert "EPR-v0.1 does not change that set." in CONTRACT


def test_pcr_to_belief_loss_is_not_hidden() -> None:
    assert "BeliefStatus / promotion decision" in PCR_CONTRACT
    assert "Belief promotion/revision authority: NONE" in PCR_CONTRACT
    assert "CLAIM_TO_BELIEF_BINDING_REQUIRED" in READINESS
    assert "CLAIM_TO_BELIEF_BINDING_REQUIRED" in SELECTION
    assert "CLAIM_TO_BELIEF_BINDING_REQUIRED" in CONTRACT
    assert "The router does not skip the missing claim→belief bridge." in SELECTION


def test_binding_mismatch_is_fail_closed_and_non_authoritative() -> None:
    for marker in (
        "belief.claim_id == record.claim.claim_id",
        "belief.belief_claim_type is record.claim.claim_type",
        "belief.claim_record_fingerprint == record.input_fingerprint",
        "EpistemicChangeBindingError",
        "does not prove:",
        "live belief revision",
        "mutation permission",
    ):
        assert marker in CONTRACT


def test_terminal_reconsideration_is_not_implemented_by_route() -> None:
    assert "Terminal reconsideration lineage:    NOT_IMPLEMENTED" in CONTRACT
    assert "TERMINAL_RECONSIDERATION_LINEAGE_REQUIRED" in CONTRACT
    assert "This result grants no authority to create a successor" in CONTRACT
    assert "TERMINAL_RECONSIDERATION_LINEAGE = NOT_IMPLEMENTED" in CONTRACT


def test_epr_threat_metamorphic_and_purity_families_are_complete() -> None:
    for number in range(1, 13):
        assert f"EPR-T{number:02d}" in CONTRACT
    for number in range(1, 11):
        assert f"EPR-M{number:02d}" in CONTRACT
    for number in range(1, 9):
        assert f"EPR-P{number:02d}" in CONTRACT


def test_phase4_source_package_exists_only_after_separate_bounded_owner_go() -> None:
    assert (ROOT / "src" / "mentaury" / "epistemic_change").exists()
    assert "Owner GO:                          GRANTED" in OWNER_GO
    assert "Owner GO scope:                    EPR-v0.1_ONLY" in OWNER_GO
    assert "Runtime GO:                        NOT_GRANTED" in OWNER_GO
    assert "PURE_EPISTEMIC_CHANGE_ROUTER" in IMPLEMENTATION
    assert "Runtime activation: NONE" in IMPLEMENTATION


def test_contract_preserves_negative_authority_boundaries() -> None:
    for marker in (
        "Belief mutation authority:           NONE",
        "P0-014 authority:                    UNCHANGED",
        "P0-015 Evidence Gate authority:      UNCHANGED",
        "Source admission authority:          NONE",
        "Retrieval / Atlas authority:         NONE",
        "Identity / relationship authority:   NONE",
        "Direct or indirect M3 write:         FORBIDDEN",
        "Persistence authority:               NONE",
        "Tool / Action Gate authority:        NONE",
        "Deployment authority:                NONE",
        "PHASE_4_OWNER_GO = NOT_GRANTED",
        "PHASE_4_RUNTIME = NOT_AUTHORIZED",
    ):
        assert marker in CONTRACT
    assert "OWNER GO FOR EPR IMPLEMENTATION != RUNTIME GO" in OWNER_GO
