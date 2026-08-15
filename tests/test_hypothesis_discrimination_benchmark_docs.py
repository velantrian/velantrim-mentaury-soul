"""Structural guards for Phase 6 hypothesis-discrimination benchmark preparation."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BENCHMARK = (
    ROOT
    / "docs"
    / "research"
    / "INFERENCE_BRIDGE_HYPOTHESIS_DISCRIMINATION_BENCHMARK.md"
).read_text(encoding="utf-8")
STATUS = (ROOT / "docs" / "CURRENT_STATUS.md").read_text(encoding="utf-8")
PCR = (ROOT / "src" / "mentaury" / "claims" / "contracts.py").read_text(
    encoding="utf-8"
)
ATR = (ROOT / "src" / "mentaury" / "relations" / "contracts.py").read_text(
    encoding="utf-8"
)
BELIEFS = (ROOT / "src" / "mentaury" / "beliefs" / "contracts.py").read_text(
    encoding="utf-8"
)


def test_phase6_is_docs_tests_only_and_non_runtime() -> None:
    for marker in (
        "Status:                         PREPARED · DOCS_TESTS_ONLY · NON_RUNTIME",
        "Phase 5 ATR-v0.1:               IMPLEMENTED_BOUNDED",
        "Phase 6 research preparation:   AUTHORIZED_DOCS_TESTS_ONLY",
        "Phase 6 implementation:         NOT_AUTHORIZED",
        "Phase 6 runtime:                NOT_AUTHORIZED",
        "Autonomous cognition:           NOT_AUTHORIZED",
        "Retrieval / tools:              NOT_AUTHORIZED",
        "Evidence Gate authority:        UNCHANGED · P0-015",
        "BENCHMARK PREPARATION ≠ IMPLEMENTATION AUTHORITY",
    ):
        assert marker in BENCHMARK


def test_audit_reuses_existing_owners_instead_of_duplication() -> None:
    assert 'HYPOTHESIS = "HYPOTHESIS"' in PCR
    assert 'INFERENCE = "INFERENCE"' in PCR
    assert 'CAUSAL = "CAUSAL"' in ATR
    assert 'CORRELATIONAL = "CORRELATIONAL"' in ATR
    assert 'ANALOGICAL = "ANALOGICAL"' in ATR
    assert 'HYPOTHESIS = "hypothesis"' in BELIEFS
    assert 'UNRESOLVED = "unresolved"' in BELIEFS
    for marker in (
        "HypothesisRecord        # PCR claim already owns representation",
        "InferenceRecord         # PCR EpistemicRole.INFERENCE already exists",
        "RelationRecord          # ATR-v0.1 already owns it",
        "EvidenceVerdict         # P0-015 already owns it",
        "BeliefRevisionOwner     # P0-014 / P0-015 ownership already exists",
    ):
        assert marker in BENCHMARK


def test_missing_failure_mode_is_explicit_and_not_schema_restating() -> None:
    for marker in (
        "NON_DISCRIMINATING_EVIDENCE_COLLECTION",
        "whose outcomes do not actually distinguish H1 from H2",
        "A benchmark that merely restates PCR/ATR schema validity is not progress",
        "well-formed representation",
        "actually discriminating inquiry",
    ):
        assert marker in BENCHMARK


def test_all_required_hd_cases_are_present_and_behavioral() -> None:
    required = {
        "HD-01": "Alternative generation",
        "HD-02": "Discriminating observation",
        "HD-03": "Falsification preference",
        "HD-04": "Confirmation-bias resistance",
        "HD-05": "Relation ≠ causation",
        "HD-06": "Evidence ownership",
        "HD-07": "Inconclusive outcome",
        "HD-08": "Revision without history deletion",
        "HD-09": "Provenance preservation",
        "HD-10": "No pseudo-confidence",
    }
    for case_id, title in required.items():
        assert f"### {case_id} — {title}" in BENCHMARK
    assert BENCHMARK.count("**PASS:") >= 8
    assert BENCHMARK.count("**FAIL:") >= 8


def test_discrimination_requires_different_outcome_patterns() -> None:
    for marker in (
        "OUTCOME PATTERN EXPECTED MORE UNDER H1",
        "OUTCOME PATTERN EXPECTED MORE UNDER H2",
        "WHY THIS SEPARATES THEM",
        "any result\nthat H1 and H2 predict equally",
        "predicted by both H1 and H2",
    ):
        assert marker in BENCHMARK


def test_confirmation_relation_and_causal_laundering_are_rejected() -> None:
    for marker in (
        "CONFIRMING SOURCES ≠ HYPOTHESIS DISCRIMINATION",
        "REPETITION ≠ TRUTH",
        "SOURCE COUNT ≠ TRUTH",
        "A CORRELATES_WITH B\n→ A CAUSES B",
        "graph adjacency/path/count as causal evidence",
        "Relation laundering",
        "Causal escalation",
    ):
        assert marker in BENCHMARK


def test_evidence_gate_ownership_is_preserved() -> None:
    for marker in (
        "P0-015 Evidence Gate",
        "EXCLUSIVE OWNER",
        "EvidenceGateOutcome.SUPPORTED",
        "EvidenceGateOutcome.CONTRADICTED",
        "BENCHMARK RESULT ≠ EVIDENCE GATE VERDICT",
        "create a new Evidence Gate",
        "create a new belief/evidence owner",
    ):
        assert marker in BENCHMARK


def test_wait_defer_and_revision_history_are_first_class_benchmark_outcomes() -> None:
    for marker in (
        "RETAIN / REVISE / DEFER / WAIT",
        "WAIT = VALID COGNITIVE OUTCOME",
        "DEFER = VALID COGNITIVE OUTCOME",
        "INCONCLUSIVE ≠ FAILURE TO THINK",
        "REVISION ≠ HISTORY REWRITE",
        "benchmark labels, not new domain-state values",
    ):
        assert marker in BENCHMARK


def test_pseudo_confidence_and_authority_fields_are_forbidden() -> None:
    for marker in (
        "confidence: 0.78",
        "probability: 82%",
        "truth_score",
        "relation_weight",
        "DETERMINISTIC NUMBER ≠ VALIDATED CONFIDENCE",
        "BENCHMARK PASS ≠ AUTONOMY AUTHORITY",
    ):
        assert marker in BENCHMARK


def test_understanding_gist_remains_direction_not_module() -> None:
    for marker in (
        "Understanding / gist remains a benchmark direction, not a module",
        "No `FastGist`, `GistEngine`, `ConsequenceSketch`, `SemanticCompressionModule` or",
        "`SlowModeVerifier` is selected or authorized",
        "DETAILS SERVE MEANING",
        "FAST UNDERSTANDING ≠ PROVEN CORRECTNESS",
    ):
        assert marker in BENCHMARK


def test_no_phase6_runtime_source_package_exists() -> None:
    for path in (
        ROOT / "src" / "mentaury" / "inference_bridge",
        ROOT / "src" / "mentaury" / "hypothesis_discrimination",
        ROOT / "src" / "mentaury" / "inquiry",
        ROOT / "src" / "mentaury" / "fast_gist",
        ROOT / "src" / "mentaury" / "gist",
        ROOT / "src" / "mentaury" / "scheduler",
    ):
        assert not path.exists()


def test_phase6_requires_new_owner_decision_before_any_implementation() -> None:
    for marker in (
        "PHASE_6_IMPLEMENTATION_MILESTONE = NOT_SELECTED",
        "PHASE_6_OWNER_GO_FOR_IMPLEMENTATION = NOT_GRANTED",
        "PHASE_6_RUNTIME = NOT_AUTHORIZED",
        "A future Owner decision may choose one of these outcomes",
        "SELECT_BOUNDED_NON_AUTONOMOUS_IMPLEMENTATION_READINESS",
        "not implementation or runtime by itself",
    ):
        assert marker in BENCHMARK
    assert "PHASE_6_RUNTIME_NOT_AUTHORIZED" in STATUS
