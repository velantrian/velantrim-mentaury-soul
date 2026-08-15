"""Executable ATR-v0.1 contract, threat, metamorphic and purity coverage."""

from __future__ import annotations

import inspect
from dataclasses import FrozenInstanceError, replace
from hashlib import sha256
from pathlib import Path

import pytest

from mentaury.contracts import canonical_json
from mentaury.relations import (
    CANONICAL_PROFILE,
    HARD_MAX_CANONICAL_INPUT_BYTES,
    HARD_MAX_STRING_BYTES,
    HARD_MAX_TUPLE_ITEMS,
    INPUT_FINGERPRINT_DOMAIN,
    TYPED_RELATION_CONTRACT_VERSION,
    AnchoredTypedRelationRecord,
    ClaimAnchor,
    RelationEndpoints,
    RelationOrientation,
    RelationOrigin,
    RelationProvenance,
    RelationRepresentationBudget,
    RelationScope,
    RelationSemantics,
    RelationType,
    ScopeReference,
    ScopeReferenceKind,
    TypedRelationBudgetExceeded,
    TypedRelationContractError,
    represent_typed_relation,
)

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "src" / "mentaury" / "relations"


def fp(number: int) -> str:
    return f"{number:064x}"


def anchor(name: str, number: int) -> ClaimAnchor:
    return ClaimAnchor(f"claim:{name}", fp(number))


def make_endpoints(**changes: object) -> RelationEndpoints:
    values: dict[str, object] = {
        "left_anchor": anchor("alpha", 1),
        "right_anchor": anchor("beta", 2),
    }
    values.update(changes)
    return RelationEndpoints(**values)  # type: ignore[arg-type]


def make_semantics(**changes: object) -> RelationSemantics:
    values: dict[str, object] = {
        "relation_type": RelationType.CAUSAL,
        "orientation": RelationOrientation.DIRECTED,
    }
    values.update(changes)
    return RelationSemantics(**values)  # type: ignore[arg-type]


def make_provenance(**changes: object) -> RelationProvenance:
    values: dict[str, object] = {
        "origin": RelationOrigin.MENTAURY_DERIVED,
        "origin_actor_ref": "actor:mentaury",
        "source_assertion_anchor": None,
        "basis_anchors": (anchor("basis", 3),),
    }
    values.update(changes)
    return RelationProvenance(**values)  # type: ignore[arg-type]


def context_ref(name: str) -> ScopeReference:
    return ScopeReference(ScopeReferenceKind.CONTEXT_REF, f"context:{name}", None)


def claim_ref(name: str, number: int) -> ScopeReference:
    return ScopeReference(ScopeReferenceKind.CLAIM_ANCHOR, f"claim:{name}", fp(number))


def make_scope(**changes: object) -> RelationScope:
    values: dict[str, object] = {
        "conditions": (context_ref("condition"),),
        "moderators": (),
        "exceptions": (),
        "unknowns": (context_ref("unknown"),),
        "transfer_limits": (context_ref("transfer"),),
    }
    values.update(changes)
    return RelationScope(**values)  # type: ignore[arg-type]


def make_budget(**changes: object) -> RelationRepresentationBudget:
    values: dict[str, object] = {
        "max_string_bytes": HARD_MAX_STRING_BYTES,
        "max_tuple_items": HARD_MAX_TUPLE_ITEMS,
        "max_canonical_input_bytes": HARD_MAX_CANONICAL_INPUT_BYTES,
    }
    values.update(changes)
    return RelationRepresentationBudget(**values)  # type: ignore[arg-type]


def make_record(
    *,
    endpoints: RelationEndpoints | None = None,
    semantics: RelationSemantics | None = None,
    provenance: RelationProvenance | None = None,
    scope: RelationScope | None = None,
    budget: RelationRepresentationBudget | None = None,
) -> AnchoredTypedRelationRecord:
    return represent_typed_relation(
        endpoints=endpoints or make_endpoints(),
        semantics=semantics or make_semantics(),
        provenance=provenance or make_provenance(),
        scope=scope or make_scope(),
        budget=budget or make_budget(),
    )


def test_contract_constants_signature_and_closed_enums() -> None:
    assert TYPED_RELATION_CONTRACT_VERSION == "ATR-v0.1"
    assert CANONICAL_PROFILE == "MENTAURY_CANONICAL_JSON_V1"
    assert INPUT_FINGERPRINT_DOMAIN == "MENTAURY_ANCHORED_TYPED_RELATION_INPUT_V1"
    assert HARD_MAX_STRING_BYTES == 4096
    assert HARD_MAX_TUPLE_ITEMS == 512
    assert HARD_MAX_CANONICAL_INPUT_BYTES == 262144

    signature = inspect.signature(represent_typed_relation)
    assert tuple(signature.parameters) == (
        "endpoints",
        "semantics",
        "provenance",
        "scope",
        "budget",
    )
    assert all(
        parameter.kind is inspect.Parameter.KEYWORD_ONLY
        for parameter in signature.parameters.values()
    )
    assert {item.value for item in RelationType} == {
        "CAUSAL",
        "CORRELATIONAL",
        "TEMPORAL",
        "ANALOGICAL",
        "TAXONOMIC",
        "MECHANISTIC",
        "EVIDENTIAL",
        "CONTRADICTORY",
        "UNKNOWN",
    }


def test_contracts_are_immutable_and_project_exact_values() -> None:
    record = make_record()
    with pytest.raises(FrozenInstanceError):
        record.scope = make_scope()  # type: ignore[misc]
    assert record.contract_version == "ATR-v0.1"
    assert record.endpoints.to_value()["left_anchor"] == anchor("alpha", 1).to_value()
    assert record.semantics.to_value() == {
        "relation_type": "CAUSAL",
        "orientation": "DIRECTED",
    }
    assert set(record.scope.to_value()) == {
        "conditions",
        "moderators",
        "exceptions",
        "unknowns",
        "transfer_limits",
    }


def test_claim_anchor_validation_is_shape_only_and_fail_closed() -> None:
    assert anchor("alpha", 1).claim_input_fingerprint == fp(1)
    for bad_id in ("", " padded", "padded ", "\ud800"):
        with pytest.raises(TypedRelationContractError):
            ClaimAnchor(bad_id, fp(1))
    for bad_fp in ("a" * 63, "A" * 64, "g" * 64, 1):
        with pytest.raises(TypedRelationContractError):
            ClaimAnchor("claim:alpha", bad_fp)  # type: ignore[arg-type]
    with pytest.raises(TypedRelationContractError):
        ClaimAnchor("x" * (HARD_MAX_STRING_BYTES + 1), fp(1))


def test_endpoint_self_link_and_exact_types_fail_closed() -> None:
    same = anchor("same", 1)
    with pytest.raises(TypedRelationContractError):
        RelationEndpoints(same, same)
    with pytest.raises(TypedRelationContractError):
        RelationEndpoints(object(), anchor("beta", 2))  # type: ignore[arg-type]


@pytest.mark.parametrize(
    ("relation_type", "orientation"),
    [
        (RelationType.CAUSAL, RelationOrientation.DIRECTED),
        (RelationType.CORRELATIONAL, RelationOrientation.SYMMETRIC),
        (RelationType.TEMPORAL, RelationOrientation.DIRECTED),
        (RelationType.ANALOGICAL, RelationOrientation.SYMMETRIC),
        (RelationType.TAXONOMIC, RelationOrientation.DIRECTED),
        (RelationType.MECHANISTIC, RelationOrientation.DIRECTED),
        (RelationType.EVIDENTIAL, RelationOrientation.DIRECTED),
        (RelationType.CONTRADICTORY, RelationOrientation.SYMMETRIC),
        (RelationType.UNKNOWN, RelationOrientation.UNKNOWN),
        (RelationType.UNKNOWN, RelationOrientation.DIRECTED),
        (RelationType.UNKNOWN, RelationOrientation.SYMMETRIC),
    ],
)
def test_relation_orientation_compatibility_positive(
    relation_type: RelationType, orientation: RelationOrientation
) -> None:
    assert RelationSemantics(relation_type, orientation).orientation is orientation


@pytest.mark.parametrize(
    ("relation_type", "orientation"),
    [
        (RelationType.CAUSAL, RelationOrientation.SYMMETRIC),
        (RelationType.CORRELATIONAL, RelationOrientation.DIRECTED),
        (RelationType.TEMPORAL, RelationOrientation.SYMMETRIC),
        (RelationType.ANALOGICAL, RelationOrientation.DIRECTED),
        (RelationType.TAXONOMIC, RelationOrientation.SYMMETRIC),
        (RelationType.MECHANISTIC, RelationOrientation.SYMMETRIC),
        (RelationType.EVIDENTIAL, RelationOrientation.SYMMETRIC),
        (RelationType.CONTRADICTORY, RelationOrientation.DIRECTED),
    ],
)
def test_relation_orientation_incompatibility_fails_closed(
    relation_type: RelationType, orientation: RelationOrientation
) -> None:
    with pytest.raises(TypedRelationContractError):
        RelationSemantics(relation_type, orientation)


def test_raw_enum_strings_are_not_coerced() -> None:
    with pytest.raises(TypedRelationContractError):
        RelationSemantics("CAUSAL", RelationOrientation.DIRECTED)  # type: ignore[arg-type]
    with pytest.raises(TypedRelationContractError):
        ScopeReference("CONTEXT_REF", "context:x", None)  # type: ignore[arg-type]


def test_scope_reference_tagged_union_and_tuple_canonicality() -> None:
    assert claim_ref("alpha", 1).claim_input_fingerprint == fp(1)
    assert context_ref("alpha").claim_input_fingerprint is None
    with pytest.raises(TypedRelationContractError):
        ScopeReference(ScopeReferenceKind.CLAIM_ANCHOR, "claim:x", None)
    with pytest.raises(TypedRelationContractError):
        ScopeReference(ScopeReferenceKind.CONTEXT_REF, "context:x", fp(1))
    a = context_ref("a")
    b = context_ref("b")
    with pytest.raises(TypedRelationContractError):
        make_scope(conditions=(b, a))
    with pytest.raises(TypedRelationContractError):
        make_scope(conditions=(a, a))
    with pytest.raises(TypedRelationContractError):
        make_scope(conditions=[a])  # type: ignore[arg-type]


def test_provenance_modes_are_exact() -> None:
    source_anchor = anchor("source-assertion", 9)
    source = RelationProvenance(
        RelationOrigin.SOURCE_ASSERTED,
        "actor:source",
        source_anchor,
        (),
    )
    assert source.source_assertion_anchor == source_anchor

    for origin in (RelationOrigin.MENTAURY_DERIVED, RelationOrigin.EXTERNAL_DERIVED):
        derived = RelationProvenance(
            origin,
            "actor:derived",
            None,
            (anchor("basis", 3),),
        )
        assert derived.basis_anchors
        with pytest.raises(TypedRelationContractError):
            RelationProvenance(origin, "actor:derived", None, ())
        with pytest.raises(TypedRelationContractError):
            RelationProvenance(origin, "actor:derived", source_anchor, (anchor("basis", 3),))

    unknown = RelationProvenance(RelationOrigin.UNKNOWN, None, None, ())
    assert unknown.origin_actor_ref is None
    with pytest.raises(TypedRelationContractError):
        RelationProvenance(RelationOrigin.UNKNOWN, "actor:x", None, ())


def test_provenance_basis_is_exact_sorted_unique_claim_anchors() -> None:
    a = anchor("a", 1)
    b = anchor("b", 2)
    assert make_provenance(basis_anchors=(a, b)).basis_anchors == (a, b)
    with pytest.raises(TypedRelationContractError):
        make_provenance(basis_anchors=(b, a))
    with pytest.raises(TypedRelationContractError):
        make_provenance(basis_anchors=(a, a))
    with pytest.raises(TypedRelationContractError):
        make_provenance(basis_anchors=(object(),))


def test_source_assertion_anchor_must_be_distinct_from_endpoints() -> None:
    endpoints = make_endpoints()
    provenance = RelationProvenance(
        RelationOrigin.SOURCE_ASSERTED,
        "actor:source",
        endpoints.left_anchor,
        (),
    )
    with pytest.raises(TypedRelationContractError):
        make_record(endpoints=endpoints, provenance=provenance)


def test_symmetric_endpoint_input_must_arrive_canonically_sorted() -> None:
    semantics = RelationSemantics(RelationType.CORRELATIONAL, RelationOrientation.SYMMETRIC)
    sorted_endpoints = RelationEndpoints(anchor("alpha", 1), anchor("beta", 2))
    assert make_record(endpoints=sorted_endpoints, semantics=semantics)
    reversed_endpoints = RelationEndpoints(anchor("beta", 2), anchor("alpha", 1))
    with pytest.raises(TypedRelationContractError):
        make_record(endpoints=reversed_endpoints, semantics=semantics)


def test_budget_errors_are_distinct_from_contract_errors() -> None:
    with pytest.raises(TypedRelationBudgetExceeded):
        make_record(budget=make_budget(max_string_bytes=63))
    provenance = make_provenance(
        basis_anchors=(anchor("a", 1), anchor("b", 2))
    )
    with pytest.raises(TypedRelationBudgetExceeded):
        make_record(provenance=provenance, budget=make_budget(max_tuple_items=1))
    with pytest.raises(TypedRelationBudgetExceeded):
        make_record(budget=make_budget(max_canonical_input_bytes=64))
    for value in (0, -1, True, 1.0):
        with pytest.raises(TypedRelationContractError):
            make_budget(max_string_bytes=value)
    with pytest.raises(TypedRelationContractError):
        make_budget(max_tuple_items=HARD_MAX_TUPLE_ITEMS + 1)


def test_exact_fingerprint_formula_is_independently_reproduced() -> None:
    endpoints = make_endpoints()
    semantics = make_semantics()
    provenance = make_provenance()
    scope = make_scope()
    budget = make_budget()
    record = make_record(
        endpoints=endpoints,
        semantics=semantics,
        provenance=provenance,
        scope=scope,
        budget=budget,
    )
    encoded = canonical_json.canonical_json_bytes(
        {
            "contract_version": "ATR-v0.1",
            "endpoints": endpoints.to_value(),
            "semantics": semantics.to_value(),
            "provenance": provenance.to_value(),
            "scope": scope.to_value(),
            "budget": budget.to_value(),
        }
    )
    expected = sha256(
        b"MENTAURY_ANCHORED_TYPED_RELATION_INPUT_V1\x00" + encoded
    ).hexdigest()
    assert record.input_fingerprint == expected


def test_canonical_profile_drift_stops_and_reconciles(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(canonical_json, "PROFILE_NAME", "DRIFTED_PROFILE")
    with pytest.raises(TypedRelationContractError, match="STOP_AND_RECONCILE"):
        make_record()


def test_exact_top_level_types_are_required() -> None:
    with pytest.raises(TypedRelationContractError):
        represent_typed_relation(
            endpoints=object(),  # type: ignore[arg-type]
            semantics=make_semantics(),
            provenance=make_provenance(),
            scope=make_scope(),
            budget=make_budget(),
        )


@pytest.mark.parametrize(
    ("threat_id", "scenario"),
    [
        ("TR-T01", "analogy"),
        ("TR-T02", "correlation"),
        ("TR-T03", "temporal"),
        ("TR-T04", "evidential"),
        ("TR-T05", "contradictory"),
        ("TR-T06", "source_asserted"),
        ("TR-T07", "derived"),
        ("TR-T08", "confidence"),
        ("TR-T09", "topology"),
        ("TR-T10", "endpoint_fingerprint"),
        ("TR-T11", "scope_preservation"),
        ("TR-T12", "unknown"),
        ("TR-T13", "directed_reversal"),
        ("TR-T14", "symmetric_unsorted"),
        ("TR-T15", "malformed_or_self"),
        ("TR-T16", "authority"),
    ],
    ids=[f"TR-T{i:02d}" for i in range(1, 17)],
)
def test_atr_threat_families_are_behaviorally_enforced(
    threat_id: str, scenario: str
) -> None:
    assert threat_id.startswith("TR-T")
    if scenario == "analogy":
        record = make_record(
            semantics=RelationSemantics(RelationType.ANALOGICAL, RelationOrientation.SYMMETRIC)
        )
        assert record.semantics.relation_type is RelationType.ANALOGICAL
    elif scenario == "correlation":
        record = make_record(
            semantics=RelationSemantics(RelationType.CORRELATIONAL, RelationOrientation.SYMMETRIC)
        )
        assert record.semantics.relation_type is RelationType.CORRELATIONAL
    elif scenario == "temporal":
        record = make_record(
            semantics=RelationSemantics(RelationType.TEMPORAL, RelationOrientation.DIRECTED)
        )
        assert record.semantics.relation_type is RelationType.TEMPORAL
    elif scenario == "evidential":
        value = make_record(
            semantics=RelationSemantics(RelationType.EVIDENTIAL, RelationOrientation.DIRECTED)
        ).to_value()
        assert "supported" not in repr(value).lower()
    elif scenario == "contradictory":
        value = make_record(
            semantics=RelationSemantics(RelationType.CONTRADICTORY, RelationOrientation.SYMMETRIC)
        ).to_value()
        assert "evidencegateoutcome" not in repr(value).lower()
        assert "contradicted" not in repr(value).lower()
    elif scenario == "source_asserted":
        provenance = RelationProvenance(
            RelationOrigin.SOURCE_ASSERTED,
            "actor:source",
            anchor("source", 9),
            (),
        )
        value = make_record(provenance=provenance).to_value()
        assert "truth" not in value
    elif scenario == "derived":
        record = make_record()
        assert record.provenance.origin is RelationOrigin.MENTAURY_DERIVED
        assert "evidence" not in record.provenance.to_value()
    elif scenario == "confidence":
        fields = set(AnchoredTypedRelationRecord.__dataclass_fields__)
        assert not {"confidence", "probability", "reliability", "weight", "score"} & fields
    elif scenario == "topology":
        fields = set(AnchoredTypedRelationRecord.__dataclass_fields__)
        assert not {"path", "adjacency", "centrality", "edge_count"} & fields
    elif scenario == "endpoint_fingerprint":
        base = make_record()
        changed = make_record(
            endpoints=RelationEndpoints(
                ClaimAnchor("claim:alpha", fp(99)),
                anchor("beta", 2),
            )
        )
        assert changed.input_fingerprint != base.input_fingerprint
    elif scenario == "scope_preservation":
        assert set(make_record().scope.to_value()) == {
            "conditions", "moderators", "exceptions", "unknowns", "transfer_limits"
        }
    elif scenario == "unknown":
        record = make_record(
            semantics=RelationSemantics(RelationType.UNKNOWN, RelationOrientation.UNKNOWN)
        )
        assert record.semantics.relation_type is RelationType.UNKNOWN
    elif scenario == "directed_reversal":
        base = make_record()
        endpoints = make_endpoints()
        reversed_record = make_record(
            endpoints=RelationEndpoints(endpoints.right_anchor, endpoints.left_anchor)
        )
        assert reversed_record.input_fingerprint != base.input_fingerprint
    elif scenario == "symmetric_unsorted":
        with pytest.raises(TypedRelationContractError):
            make_record(
                endpoints=RelationEndpoints(anchor("beta", 2), anchor("alpha", 1)),
                semantics=RelationSemantics(RelationType.ANALOGICAL, RelationOrientation.SYMMETRIC),
            )
    elif scenario == "malformed_or_self":
        same = anchor("same", 1)
        with pytest.raises(TypedRelationContractError):
            RelationEndpoints(same, same)
    elif scenario == "authority":
        record = make_record()
        assert not any(
            hasattr(record, name)
            for name in (
                "authorize", "execute", "persist", "retrieve", "mutate_belief",
                "mutate_identity", "mutate_relationship", "m3_write",
            )
        )
    else:  # pragma: no cover
        raise AssertionError(scenario)


@pytest.mark.parametrize("metamorphic_id", [f"TR-M{i:02d}" for i in range(1, 13)])
def test_atr_metamorphic_families_are_behaviorally_enforced(
    metamorphic_id: str,
) -> None:
    base = make_record()
    endpoints = make_endpoints()
    if metamorphic_id == "TR-M01":
        changed = make_record(
            endpoints=RelationEndpoints(ClaimAnchor("claim:alpha", fp(10)), endpoints.right_anchor)
        )
        assert changed.input_fingerprint != base.input_fingerprint
    elif metamorphic_id == "TR-M02":
        changed = make_record(
            endpoints=RelationEndpoints(ClaimAnchor("claim:aardvark", fp(1)), endpoints.right_anchor)
        )
        assert changed.input_fingerprint != base.input_fingerprint
    elif metamorphic_id == "TR-M03":
        changed = make_record(
            semantics=RelationSemantics(RelationType.TEMPORAL, RelationOrientation.DIRECTED)
        )
        assert changed.input_fingerprint != base.input_fingerprint
    elif metamorphic_id == "TR-M04":
        unknown_directed = make_record(
            semantics=RelationSemantics(RelationType.UNKNOWN, RelationOrientation.DIRECTED)
        )
        unknown_symmetric = make_record(
            semantics=RelationSemantics(RelationType.UNKNOWN, RelationOrientation.SYMMETRIC)
        )
        assert unknown_directed.input_fingerprint != unknown_symmetric.input_fingerprint
    elif metamorphic_id == "TR-M05":
        changed = make_record(
            provenance=make_provenance(origin_actor_ref="actor:mentaury-v2")
        )
        assert changed.input_fingerprint != base.input_fingerprint
    elif metamorphic_id == "TR-M06":
        first = RelationProvenance(RelationOrigin.SOURCE_ASSERTED, "actor:source", anchor("source-a", 8), ())
        second = RelationProvenance(RelationOrigin.SOURCE_ASSERTED, "actor:source", anchor("source-b", 9), ())
        assert make_record(provenance=first).input_fingerprint != make_record(provenance=second).input_fingerprint
    elif metamorphic_id == "TR-M07":
        changed = make_record(provenance=make_provenance(basis_anchors=(anchor("basis-2", 4),)))
        assert changed.input_fingerprint != base.input_fingerprint
        assert "supported" not in repr(changed.to_value()).lower()
    elif metamorphic_id == "TR-M08":
        changed = make_record(scope=make_scope(unknowns=(context_ref("different"),)))
        assert changed.input_fingerprint != base.input_fingerprint
    elif metamorphic_id == "TR-M09":
        reversed_record = make_record(
            endpoints=RelationEndpoints(endpoints.right_anchor, endpoints.left_anchor)
        )
        assert reversed_record.input_fingerprint != base.input_fingerprint
    elif metamorphic_id == "TR-M10":
        with pytest.raises(TypedRelationContractError):
            make_record(
                endpoints=RelationEndpoints(endpoints.right_anchor, endpoints.left_anchor),
                semantics=RelationSemantics(RelationType.CORRELATIONAL, RelationOrientation.SYMMETRIC),
            )
        same = anchor("same", 1)
        with pytest.raises(TypedRelationContractError):
            RelationEndpoints(same, same)
    elif metamorphic_id == "TR-M11":
        a = anchor("a", 1)
        with pytest.raises(TypedRelationContractError):
            make_provenance(basis_anchors=(a, a))
        ref = context_ref("same")
        with pytest.raises(TypedRelationContractError):
            make_scope(conditions=(ref, ref))
    elif metamorphic_id == "TR-M12":
        repeated = make_record()
        assert repeated == base
        assert repeated.input_fingerprint == base.input_fingerprint
    else:  # pragma: no cover
        raise AssertionError(metamorphic_id)


@pytest.mark.parametrize("purity_id", [f"TR-P{i:02d}" for i in range(1, 13)])
def test_atr_purity_families_are_executable(purity_id: str) -> None:
    source_text = "\n".join(
        path.read_text(encoding="utf-8") for path in sorted(PACKAGE.glob("*.py"))
    ).lower()
    forbidden_by_family = {
        "TR-P01": ("requests", "urllib", "socket", "httpx", "aiohttp"),
        "TR-P02": ("open(", "pathlib", "os.path", "shutil"),
        "TR-P03": ("sqlite", "postgres", "sqlalchemy", "database", "persist("),
        "TR-P04": ("datetime.now", "time.time", "os.environ", "getenv", "random"),
        "TR-P05": ("openai", "anthropic", "embedding", "retriever", "atlas"),
        "TR-P06": ("traverse", "discover_relation", "transitive_closure"),
        "TR-P07": ("evidencegate", "evaluate_evidence", "evidence_gate("),
        "TR-P08": ("create_belief", "revise_belief", "beliefstatus"),
        "TR-P09": ("action_gate", "subprocess", "tool.invoke", "capability.invoke"),
        "TR-P10": ("mutate_identity", "mutate_relationship", "m3_write"),
        "TR-P11": ("scheduler", "background", "while true"),
    }
    if purity_id in forbidden_by_family:
        for token in forbidden_by_family[purity_id]:
            assert token not in source_text
    else:
        first = make_record()
        second = make_record()
        assert first == second
        assert first.input_fingerprint == second.input_fingerprint


def test_static_source_surface_is_exactly_three_files() -> None:
    assert {path.name for path in PACKAGE.iterdir() if path.is_file()} == {
        "__init__.py",
        "contracts.py",
        "representation.py",
    }
    source_text = "\n".join(
        path.read_text(encoding="utf-8") for path in sorted(PACKAGE.glob("*.py"))
    )
    assert "mentaury.contracts import canonical_json" in source_text
    for forbidden_import in (
        "mentaury.evidence",
        "mentaury.beliefs",
        "mentaury.storage",
        "mentaury.replay",
        "mentaury.non_projection",
        "mentaury.capabilities",
    ):
        assert forbidden_import not in source_text


def test_public_surface_contains_no_confidence_metadata_or_authority_extensions() -> None:
    for cls in (
        ClaimAnchor,
        RelationEndpoints,
        RelationSemantics,
        ScopeReference,
        RelationProvenance,
        RelationScope,
        RelationRepresentationBudget,
        AnchoredTypedRelationRecord,
    ):
        fields = set(cls.__dataclass_fields__)
        assert not {
            "confidence", "probability", "reliability", "weight", "score",
            "supported", "contradicted", "truth", "metadata", "extensions",
            "action_permission", "retrieval_permission", "runtime_permission",
        } & fields
