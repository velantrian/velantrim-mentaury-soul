"""Structural guards for the post-Phase-4 cognitive milestone discrimination."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DECISION = (
    ROOT
    / "docs"
    / "research"
    / "POST_PHASE4_COGNITIVE_MILESTONE_DISCRIMINATION.md"
).read_text(encoding="utf-8")
STATUS = (ROOT / "docs" / "CURRENT_STATUS.md").read_text(encoding="utf-8")
EPR = (
    ROOT / "docs" / "research" / "EPISTEMIC_PROMOTION_REVISION_CONTRACT_V0_1.md"
).read_text(encoding="utf-8")


def test_discrimination_selects_readiness_not_implementation() -> None:
    assert "POST_PHASE_4_COGNITIVE_MILESTONE_DISCRIMINATION = COMPLETE" in DECISION
    assert (
        "NEXT_BOUNDED_READINESS_MILESTONE = "
        "PHASE_5_TYPED_RELATIONS_CONTRACT_READINESS"
    ) in DECISION
    assert "NEXT_IMPLEMENTATION_MILESTONE = NOT_SELECTED" in DECISION
    assert "PHASE_5_TYPED_RELATIONS_IMPLEMENTATION = NOT_STARTED" in DECISION
    assert "PHASE_5_OWNER_GO = NOT_GRANTED" in DECISION


def test_probe_is_not_roadmap_preference_laundering() -> None:
    for marker in (
        "Probe P4-DISC-01 — Discovery",
        "Probe P4-DISC-02 — Restraint",
        "Probe P4-DISC-03 — False Bridge",
        "first missing bounded primitive",
        "Discrimination matrix",
    ):
        assert marker in DECISION
    assert "Typed Relations" in DECISION
    assert "Inference Bridge Audit" in DECISION
    assert "Hypothesis Discrimination" in DECISION
    assert "ACI-X0.0" in DECISION


def test_relation_semantics_do_not_escalate_authority() -> None:
    for invariant in (
        "RELATION ≠ TRUTH",
        "RELATION TYPE ≠ CONFIDENCE",
        "CORRELATION ≠ CAUSATION",
        "ANALOGY ≠ MECHANISM",
        "GRAPH LINK ≠ CONFIDENCE PROPAGATION",
        "CANDIDATE RELATION ≠ EVIDENCE FOR ITSELF",
        "GENERATED HYPOTHESIS ≠ INDEPENDENT EVIDENCE",
    ):
        assert invariant in DECISION


def test_epr_implementation_remains_unauthorized() -> None:
    assert "PHASE_4_IMPLEMENTATION_NOT_STARTED" in STATUS
    assert "PHASE_4_OWNER_GO_NOT_GRANTED" in STATUS
    assert "PHASE_4_RUNTIME_NOT_AUTHORIZED" in STATUS
    assert "Owner GO:                            NOT_GRANTED" in EPR
    assert "Implementation:                      NOT_STARTED" in EPR
    assert not (ROOT / "src" / "mentaury" / "epistemic_change").exists()


def test_typed_relations_are_selected_only_for_readiness() -> None:
    assert "SELECTION OF READINESS ≠ IMPLEMENTATION AUTHORITY" in DECISION
    assert "This selection does **not** freeze a Typed Relations implementation contract" in DECISION
    assert "Do not automatically implement EPR or Typed Relations" in DECISION
    assert not (ROOT / "src" / "mentaury" / "relations").exists()


def test_no_runtime_or_downstream_authority_is_granted() -> None:
    for marker in (
        "ACTION_GATE_NOT_AUTHORIZED",
        "RETRIEVAL_EXECUTION_NOT_AUTHORIZED",
        "TOOL_EXECUTION_NOT_AUTHORIZED",
        "DIRECT_OR_INDIRECT_M3_WRITE_FORBIDDEN",
        "RUNTIME_DEPLOYMENT_NOT_AUTHORIZED",
    ):
        assert marker in STATUS
    for forbidden in (
        "implement EPR-v0.1",
        "implement Typed Relations",
        "persist or retrieve",
        "pass Action Gate",
        "mutate identity/relationship/M3",
        "start autonomous/background cognition",
        "activate runtime",
        "deploy",
    ):
        assert forbidden in DECISION
