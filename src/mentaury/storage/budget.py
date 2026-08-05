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
