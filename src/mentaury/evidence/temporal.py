"""Write-boundary check of the Evidence Gate time contract (ARCH-001).

``docs/P0_015_EVIDENCE_GATE.md``: the lifecycle uses canonical
``CommandEnvelope.issued_at`` as ``evaluated_at`` and the committed gated event
must carry the same moment as immutable ``EventEnvelope.occurred_at``; the
reducer rejects time rebinding during replay. This module enforces the same
equality *before* such an event is persisted, so a journal cannot contain a gate
decision that its own reducer will refuse to replay.

Moments are compared as canonical UTC instants (``canonical_timestamp``), never
as raw text, so equivalent zone spellings agree. Nothing here rewrites a
timestamp, and agreement does not prove the issuer's clock or the evidence is
honest; trusted-clock validation remains an outer authority concern.
"""

from __future__ import annotations

from collections.abc import Mapping

from mentaury.contracts import EventEnvelope, canonical_timestamp

from .gate import EvidenceGateError


class EvidenceGateTemporalError(EvidenceGateError):
    """A gate decision's timestamps violate the P0-015 time contract."""


def _moment(value: object, name: str) -> str:
    if not isinstance(value, str):
        raise EvidenceGateTemporalError(f"{name} must be a timestamp string")
    try:
        return canonical_timestamp(value)
    except (TypeError, ValueError) as exc:
        raise EvidenceGateTemporalError(f"{name} is not a valid canonical timestamp") from exc


def require_gate_time_consistency(
    event: EventEnvelope,
    payload: Mapping[str, object],
    *,
    command_issued_at: str | None = None,
) -> None:
    """Require occurred_at == payload.evaluated_at == receipt.evaluated_at
    (== command.issued_at when the originating command is available), with the
    receipt's own time in exact canonical form.

    ``payload`` must be the exact representation that is about to be stored (the
    caller passes the decoded persisted bytes, never a mutable object that could
    report different content on another read).
    """

    occurred_at = _moment(event.occurred_at, "event occurred_at")
    evaluated_at = _moment(payload.get("evaluated_at"), "payload evaluated_at")
    receipt = payload.get("receipt")
    if not isinstance(receipt, Mapping):
        raise EvidenceGateTemporalError("payload receipt must be an object")
    receipt_raw = receipt.get("evaluated_at")
    receipt_evaluated_at = _moment(receipt_raw, "receipt evaluated_at")
    if evaluated_at != occurred_at:
        raise EvidenceGateTemporalError(
            "gate evaluated_at must equal immutable event occurred_at"
        )
    if receipt_evaluated_at != evaluated_at:
        raise EvidenceGateTemporalError(
            "gate receipt evaluated_at must equal payload evaluated_at"
        )
    # The receipt is content-addressed and ``EvidenceGate.verify_receipt`` compares
    # the *full canonical* receipt with the recomputed one, so its time must be the
    # exact canonical spelling, not merely an equivalent instant. (The other time
    # fields only need to denote the same instant, as the reducer canonicalizes
    # them.) The stored receipt is never normalized or re-digested here.
    if receipt_raw != receipt_evaluated_at:
        raise EvidenceGateTemporalError(
            "gate receipt evaluated_at must use the exact canonical timestamp representation"
        )
    if command_issued_at is not None:
        issued_at = _moment(command_issued_at, "command issued_at")
        if issued_at != occurred_at:
            raise EvidenceGateTemporalError(
                "gate command issued_at must equal immutable event occurred_at"
            )
