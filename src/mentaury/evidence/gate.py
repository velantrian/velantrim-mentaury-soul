"""Deterministic P0-015 evidence evaluation and receipt verification."""

from __future__ import annotations

import hashlib
from collections.abc import Iterable, Mapping, Sequence
from datetime import datetime, timezone

from mentaury.beliefs.contracts import ClaimType, EvidenceSide
from mentaury.contracts import canonical_json_bytes, canonical_timestamp

from .contracts import (
    EVIDENCE_GATE_PROFILE,
    EvidenceGateOutcome,
    EvidenceGatePolicy,
    EvidenceGateReceipt,
    EvidenceRecord,
)


class EvidenceGateError(ValueError):
    """Raised when gate inputs are structurally invalid or incomplete."""


class EvidenceGate:
    """Evaluate a complete immutable evidence set without external authority."""

    def evaluate(
        self,
        *,
        belief_id: str,
        belief_revision: int,
        claim_type: ClaimType,
        statement: str,
        evidence_for: Sequence[str],
        evidence_against: Sequence[str],
        records: Iterable[EvidenceRecord],
        policy: EvidenceGatePolicy,
        evaluated_at: str,
    ) -> EvidenceGateReceipt:
        if not isinstance(belief_id, str) or not belief_id.strip():
            raise EvidenceGateError("belief_id must be a non-empty string")
        if (
            isinstance(belief_revision, bool)
            or not isinstance(belief_revision, int)
            or belief_revision <= 0
        ):
            raise EvidenceGateError("belief_revision must be positive")
        if not isinstance(claim_type, ClaimType):
            raise TypeError("claim_type must be a ClaimType")
        if not isinstance(statement, str) or not statement.strip():
            raise EvidenceGateError("statement must be a non-empty string")
        if not isinstance(policy, EvidenceGatePolicy):
            raise TypeError("policy must be an EvidenceGatePolicy")
        if claim_type not in policy.allowed_claim_types:
            raise EvidenceGateError(
                f"policy {policy.policy_id} does not allow claim type {claim_type.value}"
            )

        for_refs = _unique_refs(evidence_for, "evidence_for")
        against_refs = _unique_refs(evidence_against, "evidence_against")
        overlap = set(for_refs).intersection(against_refs)
        if overlap:
            raise EvidenceGateError(
                f"evidence references cannot appear on both sides: {sorted(overlap)!r}"
            )
        expected_refs = set(for_refs).union(against_refs)
        if not expected_refs:
            raise EvidenceGateError("evidence gate requires attached evidence")

        snapshotted = tuple(records)
        if not snapshotted or any(
            not isinstance(record, EvidenceRecord) for record in snapshotted
        ):
            raise TypeError("records must contain EvidenceRecord values")
        by_ref: dict[str, EvidenceRecord] = {}
        content_digests: set[str] = set()
        provenance_refs: set[str] = set()
        source_sides: dict[str, EvidenceSide] = {}
        for record in snapshotted:
            if record.evidence_ref in by_ref:
                raise EvidenceGateError("evidence records must have unique references")
            if record.content_digest in content_digests:
                raise EvidenceGateError(
                    "duplicate content_digest cannot manufacture independent evidence"
                )
            if record.provenance_ref in provenance_refs:
                raise EvidenceGateError(
                    "duplicate provenance_ref cannot manufacture independent evidence"
                )
            prior_side = source_sides.get(record.source_group)
            if prior_side is not None and prior_side is not record.side:
                raise EvidenceGateError(
                    "one source_group cannot be counted on both evidence sides"
                )
            by_ref[record.evidence_ref] = record
            content_digests.add(record.content_digest)
            provenance_refs.add(record.provenance_ref)
            source_sides[record.source_group] = record.side
        actual_refs = set(by_ref)
        if actual_refs != expected_refs:
            missing = sorted(expected_refs.difference(actual_refs))
            extra = sorted(actual_refs.difference(expected_refs))
            raise EvidenceGateError(
                "records must exactly match attached evidence; "
                f"missing={missing!r}, extra={extra!r}"
            )
        for ref in for_refs:
            if by_ref[ref].side is not EvidenceSide.FOR:
                raise EvidenceGateError(f"record side mismatch for {ref}")
        for ref in against_refs:
            if by_ref[ref].side is not EvidenceSide.AGAINST:
                raise EvidenceGateError(f"record side mismatch for {ref}")

        evaluated = _parse_timestamp(evaluated_at, "evaluated_at")
        canonical_evaluated_at = canonical_timestamp(evaluated_at)
        qualified_for: list[EvidenceRecord] = []
        qualified_against: list[EvidenceRecord] = []
        rejected_refs: list[str] = []
        for record in snapshotted:
            observed = _parse_timestamp(record.observed_at, "observed_at")
            age_seconds = (evaluated - observed).total_seconds()
            if age_seconds < 0:
                raise EvidenceGateError(
                    f"evidence {record.evidence_ref} is observed after evaluated_at"
                )
            qualifies = (
                not record.revoked
                and age_seconds <= policy.maximum_age_seconds
                and record.reliability_milli >= policy.minimum_reliability_milli
                and record.relevance_milli >= policy.minimum_relevance_milli
            )
            if not qualifies:
                rejected_refs.append(record.evidence_ref)
                continue
            if record.side is EvidenceSide.FOR:
                qualified_for.append(record)
            else:
                qualified_against.append(record)

        groups_for = sorted({record.source_group for record in qualified_for})
        groups_against = sorted({record.source_group for record in qualified_against})
        passes_for = len(groups_for) >= policy.minimum_source_groups_for
        passes_against = len(groups_against) >= policy.minimum_source_groups_against
        if passes_for and passes_against:
            outcome = EvidenceGateOutcome.CONFLICT
        elif passes_for:
            outcome = EvidenceGateOutcome.SUPPORTED
        elif passes_against:
            outcome = EvidenceGateOutcome.CONTRADICTED
        else:
            outcome = EvidenceGateOutcome.INCONCLUSIVE

        statement_digest = _digest(
            {"claim_type": claim_type.value, "statement": statement}
        )
        policy_digest = _digest(policy.to_value())
        records_value = [
            record.to_value()
            for record in sorted(snapshotted, key=lambda item: item.evidence_ref)
        ]
        evidence_set_digest = _digest({"records": records_value})
        body = {
            "profile": EVIDENCE_GATE_PROFILE,
            "belief_id": belief_id,
            "belief_revision": belief_revision,
            "claim_type": claim_type.value,
            "statement_digest": statement_digest,
            "evaluated_at": canonical_evaluated_at,
            "policy_id": policy.policy_id,
            "policy_digest": policy_digest,
            "evidence_set_digest": evidence_set_digest,
            "outcome": outcome.value,
            "qualifying_for_refs": sorted(
                record.evidence_ref for record in qualified_for
            ),
            "qualifying_against_refs": sorted(
                record.evidence_ref for record in qualified_against
            ),
            "source_groups_for": groups_for,
            "source_groups_against": groups_against,
            "rejected_refs": sorted(rejected_refs),
        }
        return EvidenceGateReceipt(
            profile=EVIDENCE_GATE_PROFILE,
            belief_id=belief_id,
            belief_revision=belief_revision,
            claim_type=claim_type,
            statement_digest=statement_digest,
            evaluated_at=canonical_evaluated_at,
            policy_id=policy.policy_id,
            policy_digest=policy_digest,
            evidence_set_digest=evidence_set_digest,
            outcome=outcome,
            qualifying_for_refs=tuple(body["qualifying_for_refs"]),
            qualifying_against_refs=tuple(body["qualifying_against_refs"]),
            source_groups_for=tuple(groups_for),
            source_groups_against=tuple(groups_against),
            rejected_refs=tuple(body["rejected_refs"]),
            receipt_digest=_digest(body),
        )

    def verify_receipt(
        self,
        receipt_value: Mapping[str, object],
        **evaluation_inputs: object,
    ) -> EvidenceGateReceipt:
        if not isinstance(receipt_value, Mapping):
            raise EvidenceGateError("receipt must be an object")
        computed = self.evaluate(**evaluation_inputs)
        if canonical_json_bytes(dict(receipt_value)) != canonical_json_bytes(
            computed.to_value()
        ):
            raise EvidenceGateError("evidence-gate receipt does not match recomputation")
        return computed


def policy_from_value(value: object) -> EvidenceGatePolicy:
    if not isinstance(value, Mapping):
        raise EvidenceGateError("policy must be an object")
    _require_exact_keys(
        value,
        {
            "policy_id",
            "allowed_claim_types",
            "minimum_source_groups_for",
            "minimum_source_groups_against",
            "minimum_reliability_milli",
            "minimum_relevance_milli",
            "maximum_age_seconds",
        },
        "policy",
    )
    try:
        allowed_value = value["allowed_claim_types"]
        if not isinstance(allowed_value, (tuple, list)):
            raise TypeError("allowed_claim_types must be an array")
        allowed_claim_types = tuple(ClaimType(_raw_string(item)) for item in allowed_value)
        return EvidenceGatePolicy(
            policy_id=_string(value, "policy_id"),
            allowed_claim_types=allowed_claim_types,
            minimum_source_groups_for=_integer(
                value, "minimum_source_groups_for"
            ),
            minimum_source_groups_against=_integer(
                value, "minimum_source_groups_against"
            ),
            minimum_reliability_milli=_integer(
                value, "minimum_reliability_milli"
            ),
            minimum_relevance_milli=_integer(value, "minimum_relevance_milli"),
            maximum_age_seconds=_integer(value, "maximum_age_seconds"),
        )
    except (KeyError, TypeError, ValueError) as exc:
        raise EvidenceGateError("invalid evidence-gate policy") from exc


def records_from_value(value: object) -> tuple[EvidenceRecord, ...]:
    if not isinstance(value, (tuple, list)):
        raise EvidenceGateError("records must be an array")
    records: list[EvidenceRecord] = []
    try:
        for item in value:
            if not isinstance(item, Mapping):
                raise EvidenceGateError("each evidence record must be an object")
            _require_exact_keys(
                item,
                {
                    "evidence_ref",
                    "side",
                    "source_group",
                    "provenance_ref",
                    "content_digest",
                    "observed_at",
                    "reliability_milli",
                    "relevance_milli",
                    "revoked",
                },
                "evidence record",
            )
            records.append(
                EvidenceRecord(
                    evidence_ref=_string(item, "evidence_ref"),
                    side=EvidenceSide(_string(item, "side")),
                    source_group=_string(item, "source_group"),
                    provenance_ref=_string(item, "provenance_ref"),
                    content_digest=_string(item, "content_digest"),
                    observed_at=_string(item, "observed_at"),
                    reliability_milli=_integer(item, "reliability_milli"),
                    relevance_milli=_integer(item, "relevance_milli"),
                    revoked=_boolean(item, "revoked"),
                )
            )
    except (KeyError, TypeError, ValueError) as exc:
        if isinstance(exc, EvidenceGateError):
            raise
        raise EvidenceGateError("invalid evidence record") from exc
    return tuple(records)


def _unique_refs(value: Sequence[str], name: str) -> tuple[str, ...]:
    if not isinstance(value, (tuple, list)) or any(
        not isinstance(item, str) or not item for item in value
    ):
        raise EvidenceGateError(f"{name} must be a string sequence")
    result = tuple(value)
    if len(set(result)) != len(result):
        raise EvidenceGateError(f"{name} must not contain duplicates")
    return result


def _parse_timestamp(value: str, name: str) -> datetime:
    try:
        canonical = canonical_timestamp(value)
        parsed = datetime.fromisoformat(canonical.replace("Z", "+00:00"))
    except (TypeError, ValueError) as exc:
        raise EvidenceGateError(f"{name} must be a canonical timestamp") from exc
    if parsed.tzinfo is None:
        raise EvidenceGateError(f"{name} must include timezone")
    return parsed.astimezone(timezone.utc)


def _digest(value: object) -> str:
    return f"sha256:{hashlib.sha256(canonical_json_bytes(value)).hexdigest()}"


def _require_exact_keys(
    mapping: Mapping[str, object],
    expected: set[str],
    name: str,
) -> None:
    actual = set(mapping)
    if actual != expected:
        raise EvidenceGateError(
            f"{name} keys must be exact; missing={sorted(expected - actual)!r}, "
            f"extra={sorted(actual - expected)!r}"
        )


def _raw_string(value: object) -> str:
    if not isinstance(value, str) or not value:
        raise ValueError("value must be a non-empty string")
    return value


def _string(mapping: Mapping[str, object], key: str) -> str:
    return _raw_string(mapping[key])


def _integer(mapping: Mapping[str, object], key: str) -> int:
    value = mapping[key]
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{key} must be an integer")
    return value


def _boolean(mapping: Mapping[str, object], key: str) -> bool:
    value = mapping[key]
    if not isinstance(value, bool):
        raise TypeError(f"{key} must be boolean")
    return value
