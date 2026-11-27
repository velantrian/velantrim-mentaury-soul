"""Explicit caller-supplied resource budgets for P0 integrity operations."""

from __future__ import annotations

from dataclasses import dataclass


class ResourceBudgetExceeded(RuntimeError):
    """Raised when an operation would exceed its declared resource envelope."""

    def __init__(self, dimension: str, limit: int, observed: int) -> None:
        self.dimension = dimension
        self.limit = limit
        self.observed = observed
        super().__init__(
            f"RESOURCE_BUDGET_EXCEEDED: {dimension} limit {limit}, observed {observed}"
        )


@dataclass(frozen=True, slots=True)
class VerificationBudget:
    """Non-Canonical implementation profile supplied by the caller.

    Mentaury does not choose universal numeric thresholds here. Each deployment
    or test profile must explicitly declare its own event and payload limits.
    """

    max_events: int
    max_payload_bytes: int
    max_total_payload_bytes: int
    # Optional explicit redaction-metadata bounds (Stage 04C). When unset they
    # are derived from the three limits above, with no new numeric choice: a
    # governed redaction row is backed by a same-stream target event and a
    # same-stream audit event (both counted by ``max_events``) and its text
    # columns are copied from the audit payload (bounded by the payload limits),
    # so a legitimate stream can never exceed the derived values.
    max_redaction_rows: int | None = None
    max_redaction_record_bytes: int | None = None
    max_total_redaction_bytes: int | None = None

    def __post_init__(self) -> None:
        for name in (
            "max_events",
            "max_payload_bytes",
            "max_total_payload_bytes",
        ):
            value = getattr(self, name)
            if isinstance(value, bool) or not isinstance(value, int) or value < 1:
                raise ValueError(f"{name} must be a positive integer")
        if self.max_total_payload_bytes < self.max_payload_bytes:
            raise ValueError(
                "max_total_payload_bytes must be >= max_payload_bytes"
            )
        for name in (
            "max_redaction_rows",
            "max_redaction_record_bytes",
            "max_total_redaction_bytes",
        ):
            value = getattr(self, name)
            if value is not None and (
                isinstance(value, bool) or not isinstance(value, int) or value < 1
            ):
                raise ValueError(f"{name} must be a positive integer or None")
        if (
            self.max_redaction_record_bytes is not None
            and self.max_total_redaction_bytes is not None
            and self.max_total_redaction_bytes < self.max_redaction_record_bytes
        ):
            raise ValueError(
                "max_total_redaction_bytes must be >= max_redaction_record_bytes"
            )

    @property
    def effective_redaction_rows(self) -> int:
        return self.max_events if self.max_redaction_rows is None else self.max_redaction_rows

    @property
    def effective_redaction_record_bytes(self) -> int:
        return (
            self.max_payload_bytes
            if self.max_redaction_record_bytes is None
            else self.max_redaction_record_bytes
        )

    @property
    def effective_total_redaction_bytes(self) -> int:
        return (
            self.max_total_payload_bytes
            if self.max_total_redaction_bytes is None
            else self.max_total_redaction_bytes
        )

    def require_redaction_rows(self, observed: int) -> None:
        limit = self.effective_redaction_rows
        if observed > limit:
            raise ResourceBudgetExceeded("redaction_rows", limit, observed)

    def require_redaction_record_size(self, observed: int) -> None:
        limit = self.effective_redaction_record_bytes
        if observed > limit:
            raise ResourceBudgetExceeded("redaction_record_bytes", limit, observed)

    def require_total_redaction_size(self, observed: int) -> None:
        limit = self.effective_total_redaction_bytes
        if observed > limit:
            raise ResourceBudgetExceeded("redaction_total_bytes", limit, observed)

    def require_event_count(self, observed: int) -> None:
        if observed > self.max_events:
            raise ResourceBudgetExceeded("event_count", self.max_events, observed)

    def require_payload_size(self, observed: int) -> None:
        if observed > self.max_payload_bytes:
            raise ResourceBudgetExceeded(
                "payload_bytes", self.max_payload_bytes, observed
            )

    def require_total_payload_size(self, observed: int) -> None:
        if observed > self.max_total_payload_bytes:
            raise ResourceBudgetExceeded(
                "total_payload_bytes",
                self.max_total_payload_bytes,
                observed,
            )
