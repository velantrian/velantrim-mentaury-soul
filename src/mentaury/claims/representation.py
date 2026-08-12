"""Pure deterministic PCR-v0.1 provenance-claim representation."""

from __future__ import annotations

from hashlib import sha256

from mentaury.contracts import canonical_json

from .contracts import (
    CANONICAL_PROFILE,
    HARD_MAX_CANONICAL_INPUT_BYTES,
    INPUT_FINGERPRINT_DOMAIN,
    PROVENANCE_CLAIM_CONTRACT_VERSION,
    ClaimRepresentation,
    ClaimScope,
    ProvenanceClaimBudgetExceeded,
    ProvenanceClaimContractError,
    ProvenanceClaimRecord,
    ProvenanceSource,
    RepresentationBudget,
)


def _require_exact(value: object, expected: type[object], name: str) -> None:
    if type(value) is not expected:
        raise ProvenanceClaimContractError(
            f"{name} must be exact {expected.__name__}"
        )


def _check_string_budget(
    value: str | None, *, name: str, budget: RepresentationBudget
) -> None:
    if value is None:
        return
    if len(value.encode("utf-8")) > budget.max_string_bytes:
        raise ProvenanceClaimBudgetExceeded(
            f"{name} exceeds local max_string_bytes"
        )


def _check_tuple_budget(
    value: tuple[str, ...], *, name: str, budget: RepresentationBudget
) -> None:
    if len(value) > budget.max_tuple_items:
        raise ProvenanceClaimBudgetExceeded(
            f"{name} exceeds local max_tuple_items"
        )
    for index, item in enumerate(value):
        _check_string_budget(
            item,
            name=f"{name}[{index}]",
            budget=budget,
        )


def _check_local_budget(
    *,
    source: ProvenanceSource,
    claim: ClaimRepresentation,
    scope: ClaimScope,
    budget: RepresentationBudget,
) -> None:
    for name in (
        "source_ref",
        "source_actor_ref",
        "publication_or_capture_context_ref",
        "usage_boundary_ref",
    ):
        _check_string_budget(
            getattr(source, name), name=f"source.{name}", budget=budget
        )
    for name in ("material_gaps", "derivation_refs"):
        _check_tuple_budget(
            getattr(source, name), name=f"source.{name}", budget=budget
        )

    for name in (
        "claim_id",
        "statement_ref",
        "speaker_ref",
        "subject_ref",
    ):
        _check_string_budget(
            getattr(claim, name), name=f"claim.{name}", budget=budget
        )
    for name in ("basis_refs", "evidence_refs"):
        _check_tuple_budget(
            getattr(claim, name), name=f"claim.{name}", budget=budget
        )

    for name in (
        "applies_to",
        "may_support",
        "does_not_establish",
        "unknowns",
        "transfer_limits",
    ):
        _check_tuple_budget(
            getattr(scope, name), name=f"scope.{name}", budget=budget
        )


def _canonical_input_bytes(
    *,
    source: ProvenanceSource,
    claim: ClaimRepresentation,
    scope: ClaimScope,
    budget: RepresentationBudget,
) -> bytes:
    if canonical_json.PROFILE_NAME != CANONICAL_PROFILE:
        raise ProvenanceClaimContractError(
            "STOP_AND_RECONCILE: canonical JSON profile drift"
        )
    try:
        encoded = canonical_json.canonical_json_bytes(
            {
                "contract_version": PROVENANCE_CLAIM_CONTRACT_VERSION,
                "source": source.to_value(),
                "claim": claim.to_value(),
                "scope": scope.to_value(),
                "budget": budget.to_value(),
            }
        )
    except (TypeError, ValueError) as exc:
        raise ProvenanceClaimContractError(
            "canonicalization failed for admitted PCR-v0.1 input"
        ) from exc

    if len(encoded) > HARD_MAX_CANONICAL_INPUT_BYTES:
        raise ProvenanceClaimContractError(
            "canonical input exceeds HARD_MAX_CANONICAL_INPUT_BYTES"
        )
    if len(encoded) > budget.max_canonical_input_bytes:
        raise ProvenanceClaimBudgetExceeded(
            "canonical input exceeds local max_canonical_input_bytes"
        )
    return encoded


def represent_provenance_claim(
    *,
    source: ProvenanceSource,
    claim: ClaimRepresentation,
    scope: ClaimScope,
    budget: RepresentationBudget,
) -> ProvenanceClaimRecord:
    """Return one immutable deterministic record for exact caller-supplied input.

    This function performs representation only. It does not admit sources,
    evaluate evidence, promote beliefs, call NPG, retrieve data, store state,
    invoke tools, mutate identity, or grant runtime/action authority.
    """

    _require_exact(source, ProvenanceSource, "source")
    _require_exact(claim, ClaimRepresentation, "claim")
    _require_exact(scope, ClaimScope, "scope")
    _require_exact(budget, RepresentationBudget, "budget")

    _check_local_budget(
        source=source,
        claim=claim,
        scope=scope,
        budget=budget,
    )
    encoded = _canonical_input_bytes(
        source=source,
        claim=claim,
        scope=scope,
        budget=budget,
    )
    fingerprint = sha256(
        INPUT_FINGERPRINT_DOMAIN.encode("ascii") + b"\x00" + encoded
    ).hexdigest()

    return ProvenanceClaimRecord(
        contract_version=PROVENANCE_CLAIM_CONTRACT_VERSION,
        source=source,
        claim=claim,
        scope=scope,
        input_fingerprint=fingerprint,
    )
