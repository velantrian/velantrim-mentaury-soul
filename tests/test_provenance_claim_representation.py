"""Executable PCR-v0.1 threat, metamorphic, budget and purity coverage."""

from __future__ import annotations

import inspect
from dataclasses import FrozenInstanceError, replace
from hashlib import sha256
from pathlib import Path

import pytest

from mentaury import epistemic_types
from mentaury.claims import (
    CANONICAL_PROFILE,
    HARD_MAX_CANONICAL_INPUT_BYTES,
    HARD_MAX_STRING_BYTES,
    HARD_MAX_TUPLE_ITEMS,
    INPUT_FINGERPRINT_DOMAIN,
    PROVENANCE_CLAIM_CONTRACT_VERSION,
    SOURCE_SCOPE,
    ClaimRepresentation,
    ClaimScope,
    EpistemicRole,
    ProvenanceClaimBudgetExceeded,
    ProvenanceClaimContractError,
    ProvenanceClaimRecord,
    ProvenanceSource,
    RepresentationBudget,
    represent_provenance_claim,
)
from mentaury.contracts import canonical_json
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
PACKAGE = ROOT / "src" / "mentaury" / "claims"


def make_source(**changes: object) -> ProvenanceSource:
    values: dict[str, object] = {
        "source_ref": "source:alpha",
        "source_actor_ref": "actor:author",
        "source_class": SourceClass.RESEARCH_PRIMARY,
        "source_origin": SourceOrigin.PRIMARY,
        "provenance_state": ProvenanceState.VERIFIED,
        "publication_or_capture_context_ref": "context:publication",
        "sensitivity": Sensitivity.NORMAL,
        "usage_boundary_ref": "usage:research",
        "material_gaps": (),
        "derivation_refs": (),
    }
    values.update(changes)
    return ProvenanceSource(**values)  # type: ignore[arg-type]


def make_claim(**changes: object) -> ClaimRepresentation:
    values: dict[str, object] = {
        "claim_id": "claim:alpha",
        "statement_ref": "statement:alpha",
        "claim_class": ClaimClass.FACTUAL,
        "claim_type": ClaimType.CONTEXTUAL,
        "epistemic_role": EpistemicRole.OBSERVATION,
        "directly_stated": True,
        "speaker_ref": "actor:author",
        "subject_ref": "subject:world",
        "subject_relation": SubjectRelation.NON_SELF,
        "basis_refs": (),
        "evidence_refs": (),
    }
    values.update(changes)
    return ClaimRepresentation(**values)  # type: ignore[arg-type]


def make_scope(**changes: object) -> ClaimScope:
    values: dict[str, object] = {
        "applies_to": ("context:publication",),
        "may_support": ("question:alpha",),
        "does_not_establish": ("truth:universal",),
        "unknowns": (),
        "transfer_limits": ("no-cross-context-transfer",),
    }
    values.update(changes)
    return ClaimScope(**values)  # type: ignore[arg-type]


def make_budget(**changes: object) -> RepresentationBudget:
    values: dict[str, object] = {
        "max_string_bytes": HARD_MAX_STRING_BYTES,
        "max_tuple_items": HARD_MAX_TUPLE_ITEMS,
        "max_canonical_input_bytes": HARD_MAX_CANONICAL_INPUT_BYTES,
    }
    values.update(changes)
    return RepresentationBudget(**values)  # type: ignore[arg-type]


def make_record(
    *,
    source: ProvenanceSource | None = None,
    claim: ClaimRepresentation | None = None,
    scope: ClaimScope | None = None,
    budget: RepresentationBudget | None = None,
) -> ProvenanceClaimRecord:
    return represent_provenance_claim(
        source=source or make_source(),
        claim=claim or make_claim(),
        scope=scope or make_scope(),
        budget=budget or make_budget(),
    )


def test_contract_constants_and_exact_public_signature() -> None:
    assert PROVENANCE_CLAIM_CONTRACT_VERSION == "PCR-v0.1"
    assert CANONICAL_PROFILE == "MENTAURY_CANONICAL_JSON_V1"
    assert INPUT_FINGERPRINT_DOMAIN == "MENTAURY_PROVENANCE_CLAIM_INPUT_V1"
    assert SOURCE_SCOPE == "CALLER_SUPPLIED_REFERENCES_ONLY"
    assert HARD_MAX_STRING_BYTES == 4096
    assert HARD_MAX_TUPLE_ITEMS == 512
    assert HARD_MAX_CANONICAL_INPUT_BYTES == 262144

    signature = inspect.signature(represent_provenance_claim)
    assert tuple(signature.parameters) == ("source", "claim", "scope", "budget")
    assert all(
        parameter.kind is inspect.Parameter.KEYWORD_ONLY
        for parameter in signature.parameters.values()
    )


def test_reused_enum_class_identities_are_exact() -> None:
    from mentaury.claims import contracts as pcr_contracts

    assert pcr_contracts.ClaimClass is ClaimClass
    assert pcr_contracts.ProvenanceState is ProvenanceState
    assert pcr_contracts.Sensitivity is Sensitivity
    assert pcr_contracts.SourceClass is SourceClass
    assert pcr_contracts.SourceOrigin is SourceOrigin
    assert pcr_contracts.SubjectRelation is SubjectRelation
    assert pcr_contracts.ClaimType is epistemic_types.ClaimType


def test_immutable_contracts_and_value_projection() -> None:
    record = make_record()
    with pytest.raises(FrozenInstanceError):
        record.claim = make_claim()  # type: ignore[misc]
    assert record.to_value()["contract_version"] == "PCR-v0.1"
    assert record.source.to_value()["source_class"] == "RESEARCH_PRIMARY"
    assert record.claim.to_value()["claim_type"] == "contextual"
    assert record.scope.to_value()["transfer_limits"] == ["no-cross-context-transfer"]


def test_exact_fingerprint_formula_is_independently_reproduced() -> None:
    source = make_source()
    claim = make_claim()
    scope = make_scope()
    budget = make_budget()
    record = make_record(source=source, claim=claim, scope=scope, budget=budget)
    encoded = canonical_json.canonical_json_bytes(
        {
            "contract_version": "PCR-v0.1",
            "source": source.to_value(),
            "claim": claim.to_value(),
            "scope": scope.to_value(),
            "budget": budget.to_value(),
        }
    )
    expected = sha256(
        b"MENTAURY_PROVENANCE_CLAIM_INPUT_V1\x00" + encoded
    ).hexdigest()
    assert record.input_fingerprint == expected


def test_local_string_budget_is_distinct_from_hard_cap() -> None:
    source = make_source(source_ref="abcd")
    with pytest.raises(ProvenanceClaimBudgetExceeded):
        make_record(source=source, budget=make_budget(max_string_bytes=3))
    with pytest.raises(ProvenanceClaimContractError):
        make_source(source_ref="x" * (HARD_MAX_STRING_BYTES + 1))


def test_local_tuple_budget_is_distinct_from_hard_cap() -> None:
    source = make_source(material_gaps=("gap:a", "gap:b"))
    with pytest.raises(ProvenanceClaimBudgetExceeded):
        make_record(source=source, budget=make_budget(max_tuple_items=1))
    too_many = tuple(f"gap:{index:04d}" for index in range(HARD_MAX_TUPLE_ITEMS + 1))
    with pytest.raises(ProvenanceClaimContractError):
        make_source(material_gaps=too_many)


def test_local_canonical_budget_fails_without_truncation() -> None:
    source = make_source(source_ref="source:" + "x" * 200)
    with pytest.raises(ProvenanceClaimBudgetExceeded):
        make_record(source=source, budget=make_budget(max_canonical_input_bytes=64))


def test_budget_values_require_exact_positive_int_and_hard_cap() -> None:
    for value in (0, -1, True, 1.0):
        with pytest.raises(ProvenanceClaimContractError):
            make_budget(max_string_bytes=value)
    with pytest.raises(ProvenanceClaimContractError):
        make_budget(max_tuple_items=HARD_MAX_TUPLE_ITEMS + 1)
    with pytest.raises(ProvenanceClaimContractError):
        make_budget(max_canonical_input_bytes=HARD_MAX_CANONICAL_INPUT_BYTES + 1)


def test_raw_enum_strings_and_non_bool_are_not_coerced() -> None:
    with pytest.raises(ProvenanceClaimContractError):
        make_claim(claim_class="FACTUAL")
    with pytest.raises(ProvenanceClaimContractError):
        make_claim(claim_type="contextual")
    with pytest.raises(ProvenanceClaimContractError):
        make_claim(epistemic_role="OBSERVATION")
    with pytest.raises(ProvenanceClaimContractError):
        make_claim(directly_stated=1)


def test_strings_require_nonempty_unpadded_utf8() -> None:
    for value in ("", " padded", "padded "):
        with pytest.raises(ProvenanceClaimContractError):
            make_source(source_ref=value)
    with pytest.raises(ProvenanceClaimContractError):
        make_source(source_ref="\ud800")


def test_inference_requires_nonempty_caller_basis_refs() -> None:
    with pytest.raises(ProvenanceClaimContractError):
        make_claim(epistemic_role=EpistemicRole.INFERENCE, basis_refs=())
    claim = make_claim(
        epistemic_role=EpistemicRole.INFERENCE,
        basis_refs=("basis:a",),
        directly_stated=False,
    )
    assert make_record(claim=claim).claim.basis_refs == ("basis:a",)


def test_unsorted_or_duplicate_tuple_fails_closed() -> None:
    with pytest.raises(ProvenanceClaimContractError):
        make_claim(evidence_refs=("evidence:b", "evidence:a"))
    with pytest.raises(ProvenanceClaimContractError):
        make_claim(evidence_refs=("evidence:a", "evidence:a"))


def test_exact_top_level_types_are_required() -> None:
    with pytest.raises(ProvenanceClaimContractError):
        represent_provenance_claim(
            source=object(),  # type: ignore[arg-type]
            claim=make_claim(),
            scope=make_scope(),
            budget=make_budget(),
        )


def test_canonical_profile_drift_stops_and_reconciles(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(canonical_json, "PROFILE_NAME", "DRIFTED_PROFILE")
    with pytest.raises(ProvenanceClaimContractError, match="STOP_AND_RECONCILE"):
        make_record()


@pytest.mark.parametrize(
    ("threat_id", "scenario"),
    [
        ("PCR-T01", "creator_autobiography"),
        ("PCR-T02", "claim_class_to_type"),
        ("PCR-T03", "claim_type_to_class"),
        ("PCR-T04", "roles_distinct"),
        ("PCR-T05", "derived_directness"),
        ("PCR-T06", "provenance_upgrade"),
        ("PCR-T07", "evidence_support"),
        ("PCR-T08", "source_admission"),
        ("PCR-T09", "truth_support_confidence"),
        ("PCR-T10", "inference_to_causal"),
        ("PCR-T11", "numeric_pseudo_precision"),
        ("PCR-T12", "authority_laundering"),
    ],
    ids=[f"PCR-T{i:02d}" for i in range(1, 13)],
)
def test_pcr_threat_families_are_behaviorally_enforced(
    threat_id: str, scenario: str
) -> None:
    assert threat_id.startswith("PCR-T")

    if scenario == "creator_autobiography":
        record = make_record(
            source=make_source(source_class=SourceClass.CREATOR_TESTIMONY),
            claim=make_claim(
                claim_class=ClaimClass.AUTOBIOGRAPHICAL_TESTIMONY,
                epistemic_role=EpistemicRole.TESTIMONY,
                subject_relation=SubjectRelation.NON_SELF,
            ),
        )
        assert record.source.source_class is SourceClass.CREATOR_TESTIMONY
        assert record.claim.subject_relation is SubjectRelation.NON_SELF
        assert "identity" not in record.to_value()
    elif scenario == "claim_class_to_type":
        original = make_claim(claim_class=ClaimClass.CAUSAL, claim_type=ClaimType.CONTEXTUAL)
        changed = make_claim(claim_class=ClaimClass.FACTUAL, claim_type=ClaimType.CONTEXTUAL)
        assert original.claim_type is changed.claim_type is ClaimType.CONTEXTUAL
        assert original.claim_class is not changed.claim_class
    elif scenario == "claim_type_to_class":
        original = make_claim(claim_class=ClaimClass.FACTUAL, claim_type=ClaimType.CAUSAL)
        changed = make_claim(claim_class=ClaimClass.FACTUAL, claim_type=ClaimType.STATISTICAL)
        assert original.claim_class is changed.claim_class is ClaimClass.FACTUAL
        assert original.claim_type is not changed.claim_type
    elif scenario == "roles_distinct":
        roles = {role.value for role in EpistemicRole}
        assert len(roles) == 8
        assert {"OBSERVATION", "EVIDENCE_CANDIDATE", "HYPOTHESIS", "INFERENCE"} <= roles
    elif scenario == "derived_directness":
        claim = make_claim(
            epistemic_role=EpistemicRole.INTERPRETATION,
            directly_stated=False,
        )
        assert make_record(claim=claim).claim.directly_stated is False
    elif scenario == "provenance_upgrade":
        for state in (ProvenanceState.UNKNOWN, ProvenanceState.PARTIAL):
            record = make_record(source=make_source(provenance_state=state))
            assert record.source.provenance_state is state
    elif scenario == "evidence_support":
        record = make_record(claim=make_claim(evidence_refs=("evidence:a", "evidence:b")))
        assert record.claim.evidence_refs == ("evidence:a", "evidence:b")
        assert "supported" not in record.to_value()
        assert "contradicted" not in record.to_value()
    elif scenario == "source_admission":
        fields = inspect.signature(represent_provenance_claim).parameters
        assert "source_admission" not in fields
        assert "admission_result" not in fields
    elif scenario == "truth_support_confidence":
        field_names = set(ProvenanceClaimRecord.__dataclass_fields__)
        assert not {"truth", "supported", "contradicted", "confidence", "reliability"} & field_names
    elif scenario == "inference_to_causal":
        claim = make_claim(
            claim_class=ClaimClass.FACTUAL,
            claim_type=ClaimType.CONTEXTUAL,
            epistemic_role=EpistemicRole.INFERENCE,
            basis_refs=("basis:a",),
            directly_stated=False,
        )
        record = make_record(claim=claim)
        assert record.claim.claim_class is ClaimClass.FACTUAL
        assert record.claim.claim_type is ClaimType.CONTEXTUAL
    elif scenario == "numeric_pseudo_precision":
        all_fields = (
            set(ProvenanceSource.__dataclass_fields__)
            | set(ClaimRepresentation.__dataclass_fields__)
            | set(ClaimScope.__dataclass_fields__)
            | set(ProvenanceClaimRecord.__dataclass_fields__)
        )
        assert not {"confidence", "probability", "reliability", "score"} & all_fields
    elif scenario == "authority_laundering":
        value = make_record().to_value()
        assert not {
            "retrieval_permission",
            "action_gate",
            "identity_authority",
            "relationship_authority",
            "m3_authority",
            "deployment_authority",
        } & set(value)
    else:  # pragma: no cover
        raise AssertionError(scenario)


@pytest.mark.parametrize(
    "metamorphic_id",
    [f"PCR-M{i:02d}" for i in range(1, 11)],
)
def test_pcr_metamorphic_contract_families_are_behaviorally_covered(
    metamorphic_id: str,
) -> None:
    base_source = make_source()
    base_claim = make_claim()
    base_scope = make_scope()
    budget = make_budget()
    base = make_record(
        source=base_source,
        claim=base_claim,
        scope=base_scope,
        budget=budget,
    )

    if metamorphic_id == "PCR-M01":
        changed = make_record(source=replace(base_source, source_ref="source:beta"))
        assert changed.input_fingerprint != base.input_fingerprint
    elif metamorphic_id == "PCR-M02":
        changed = make_record(claim=replace(base_claim, statement_ref="statement:beta"))
        assert changed.input_fingerprint != base.input_fingerprint
    elif metamorphic_id == "PCR-M03":
        changed_claim = replace(base_claim, claim_class=ClaimClass.PREDICTIVE)
        changed = make_record(claim=changed_claim)
        assert changed.input_fingerprint != base.input_fingerprint
        assert changed.claim.claim_type is base.claim.claim_type
    elif metamorphic_id == "PCR-M04":
        changed_claim = replace(base_claim, claim_type=ClaimType.STATISTICAL)
        changed = make_record(claim=changed_claim)
        assert changed.input_fingerprint != base.input_fingerprint
        assert changed.claim.claim_class is base.claim.claim_class
    elif metamorphic_id == "PCR-M05":
        changed = make_record(claim=replace(base_claim, epistemic_role=EpistemicRole.HYPOTHESIS))
        assert changed.input_fingerprint != base.input_fingerprint
    elif metamorphic_id == "PCR-M06":
        changed = make_record(claim=replace(base_claim, directly_stated=False))
        assert changed.input_fingerprint != base.input_fingerprint
    elif metamorphic_id == "PCR-M07":
        changed = make_record(
            claim=replace(
                base_claim,
                speaker_ref="actor:other",
                subject_ref="subject:other",
                subject_relation=SubjectRelation.UNKNOWN,
            )
        )
        assert changed.input_fingerprint != base.input_fingerprint
    elif metamorphic_id == "PCR-M08":
        changed = make_record(
            scope=replace(base_scope, transfer_limits=("no-export", "no-transfer"))
        )
        assert changed.input_fingerprint != base.input_fingerprint
    elif metamorphic_id == "PCR-M09":
        changed = make_record(
            claim=replace(base_claim, evidence_refs=("evidence:a", "evidence:b"))
        )
        assert changed.input_fingerprint != base.input_fingerprint
        assert "supported" not in changed.to_value()
    elif metamorphic_id == "PCR-M10":
        with pytest.raises(ProvenanceClaimContractError):
            make_claim(basis_refs=("basis:b", "basis:a"))
        with pytest.raises(ProvenanceClaimContractError):
            make_claim(basis_refs=("basis:a", "basis:a"))
    else:  # pragma: no cover
        raise AssertionError(metamorphic_id)


@pytest.mark.parametrize("purity_id", [f"PCR-P{i:02d}" for i in range(1, 9)])
def test_pcr_purity_families_are_executable(purity_id: str) -> None:
    source_text = "\n".join(
        path.read_text(encoding="utf-8")
        for path in sorted(PACKAGE.glob("*.py"))
    ).lower()

    forbidden_by_family = {
        "PCR-P01": ("requests", "urllib", "socket", "httpx", "aiohttp"),
        "PCR-P02": ("open(", "pathlib", "os.path", "shutil"),
        "PCR-P03": ("sqlite", "postgres", "sqlalchemy", "persist", "database"),
        "PCR-P04": ("datetime.now", "time.time", "os.environ", "getenv", "random"),
        "PCR-P05": ("openai", "anthropic", "retriever", "atlas", "embedding", "graph"),
        "PCR-P06": ("action_gate", "subprocess", "plugin", "capability.invoke"),
        "PCR-P07": ("evidencegate", "promote_belief", "beliefstatus", "m3_write"),
    }
    if purity_id in forbidden_by_family:
        for token in forbidden_by_family[purity_id]:
            assert token not in source_text
    else:
        first = make_record()
        second = make_record()
        assert first == second
        assert first.input_fingerprint == second.input_fingerprint


def test_public_contract_has_no_extension_dictionary_or_forbidden_authority_inputs() -> None:
    for cls in (
        ProvenanceSource,
        ClaimRepresentation,
        ClaimScope,
        RepresentationBudget,
        ProvenanceClaimRecord,
    ):
        fields = set(cls.__dataclass_fields__)
        assert not {"extensions", "metadata", "extra", "context"} & fields
    public_inputs = set(inspect.signature(represent_provenance_claim).parameters)
    assert public_inputs == {"source", "claim", "scope", "budget"}


def test_fingerprint_change_is_identity_evidence_not_mutable_bearer_authority() -> None:
    first = make_record()
    second = make_record(source=make_source(source_ref="source:beta"))
    assert first.input_fingerprint != second.input_fingerprint
    assert not hasattr(first, "authorize")
    assert not hasattr(first, "execute")
    assert not hasattr(first, "persist")
