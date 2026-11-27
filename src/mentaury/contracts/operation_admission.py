"""Operation-level admission: one budget shared by every step of one operation.

Stage 04B.3. ``OperationAdmissionBudget`` is an immutable, caller-supplied
profile (no defaults, not Canon, not a production limit). Each operation creates
its own ``OperationAdmissionState``; passing that same state through the
envelope, batch, fingerprint, validation and sealing steps means the aggregate
spend is never reset between functions.

Accounting is *work based*: every bounded traversal (freeze, canonical
serialization, the schema-validation walk) charges the nodes it visited, and
every canonical serialization charges the bytes it produced. A payload that is
processed three times therefore costs three times; repeated processing is
visible and bounded instead of free. ``max_batch_entries`` bounds each
materialized collection (pending events, entries), not a running total.
"""

from __future__ import annotations

import itertools
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from typing import TypeVar

from .admission import (
    CanonicalAdmissionBudget,
    PayloadAdmissionBudget,
    PayloadAdmissionExceeded,
    PayloadAdmissionState,
)
from .canonical_json import _canonical_bounded
from .primitives import FrozenPayload, _freeze_payload_value_bounded

_T = TypeVar("_T")

# Structural levels a whole-operation document (fingerprint) adds around a payload.
_WRAPPER_DEPTH = 4


@dataclass(frozen=True, slots=True)
class OperationAdmissionBudget:
    """Immutable limits for one operation; all bounds are inclusive."""

    max_batch_entries: int
    payload: PayloadAdmissionBudget
    max_payload_output_bytes: int
    max_total_nodes: int
    max_total_output_bytes: int

    def __post_init__(self) -> None:
        if not isinstance(self.payload, PayloadAdmissionBudget):
            raise TypeError("payload must be a PayloadAdmissionBudget")
        for name in (
            "max_batch_entries",
            "max_payload_output_bytes",
            "max_total_nodes",
            "max_total_output_bytes",
        ):
            value = getattr(self, name)
            if isinstance(value, bool) or not isinstance(value, int) or value < 1:
                raise ValueError(f"{name} must be a positive integer")


class OperationAdmissionState:
    """Mutable aggregate spend of exactly one operation (never shared)."""

    __slots__ = ("_budget", "_nodes", "_bytes")

    def __init__(self, budget: OperationAdmissionBudget) -> None:
        if not isinstance(budget, OperationAdmissionBudget):
            raise TypeError("budget must be an OperationAdmissionBudget")
        self._budget = budget
        self._nodes = 0
        self._bytes = 0

    @property
    def nodes(self) -> int:
        return self._nodes

    @property
    def output_bytes(self) -> int:
        return self._bytes

    # -- collections -------------------------------------------------------------------

    def take_entries(self, items: Iterable[_T]) -> tuple[_T, ...]:
        """Materialize ``items`` consuming at most ``max_batch_entries + 1`` items.

        Only exact built-in list/tuple use the copy fast path; any other
        iterable (including subclasses with an untrustworthy ``len``) is drawn
        through ``islice``. Declared length is never the only evidence.
        """

        limit = self._budget.max_batch_entries
        if type(items) in (list, tuple):
            if len(items) > limit:  # type: ignore[arg-type]
                raise PayloadAdmissionExceeded("batch_entries", limit, len(items))  # type: ignore[arg-type]
            return tuple(items)
        taken = tuple(itertools.islice(iter(items), limit + 1))
        if len(taken) > limit:
            raise PayloadAdmissionExceeded("batch_entries", limit, len(taken))
        return taken

    # -- payload steps -------------------------------------------------------------------

    def freeze_payload(self, payload: object) -> FrozenPayload:
        """Bounded detached snapshot; charges the nodes visited."""

        if not isinstance(payload, Mapping):
            raise TypeError("payload must be a mapping")
        remaining = self._remaining_nodes()
        budget = self._budget.payload
        effective = PayloadAdmissionBudget(
            budget.max_depth,
            min(budget.max_nodes, remaining),
            budget.max_string_length,
            budget.max_key_length,
        )
        spend = PayloadAdmissionState(effective)
        try:
            frozen = _freeze_payload_value_bounded(payload, spend)
        except PayloadAdmissionExceeded as exc:
            self._nodes += spend.nodes_visited
            raise self._remap_nodes(exc, remaining) from None
        self._nodes += spend.nodes_visited
        assert isinstance(frozen, Mapping)
        return frozen

    def canonical_payload(
        self,
        value: object,
        *,
        whole_operation: bool = False,
    ) -> tuple[bytes, int]:
        """Bounded canonical bytes; returns ``(bytes, nodes_visited)``.

        Charges nodes and bytes to the aggregate. ``whole_operation`` is for a
        document spanning several payloads (the fingerprint): the per-payload
        node/byte caps then yield to the remaining aggregate budget.
        """

        remaining_nodes = self._remaining_nodes()
        remaining_bytes = self._budget.max_total_output_bytes - self._bytes
        if remaining_bytes < 1:
            raise PayloadAdmissionExceeded(
                "total_output_bytes",
                self._budget.max_total_output_bytes,
                self._bytes + 1,
            )
        payload = self._budget.payload
        if whole_operation:
            node_cap = remaining_nodes
            byte_cap = remaining_bytes
            depth = payload.max_depth + _WRAPPER_DEPTH
        else:
            node_cap = min(payload.max_nodes, remaining_nodes)
            byte_cap = min(self._budget.max_payload_output_bytes, remaining_bytes)
            depth = payload.max_depth
        budget = CanonicalAdmissionBudget(
            PayloadAdmissionBudget(
                depth, node_cap, payload.max_string_length, payload.max_key_length
            ),
            byte_cap,
        )
        spend = PayloadAdmissionState(budget.payload)
        try:
            text, nodes = _canonical_bounded(value, budget, spend)
        except PayloadAdmissionExceeded as exc:
            self._nodes += spend.nodes_visited
            raise self._remap(exc, node_cap, remaining_nodes, byte_cap, remaining_bytes) from None
        encoded = text.encode("utf-8")
        self._nodes += nodes
        self._bytes += len(encoded)
        return encoded, nodes

    def charge_validation_pass(self, nodes: int) -> None:
        """Charge the node visits of a schema-validation walk over ``nodes``."""

        remaining = self._remaining_nodes()
        if nodes > remaining:
            raise PayloadAdmissionExceeded(
                "total_nodes", self._budget.max_total_nodes, self._nodes + nodes
            )
        self._nodes += nodes

    # -- internals --------------------------------------------------------------------------

    def _remaining_nodes(self) -> int:
        remaining = self._budget.max_total_nodes - self._nodes
        if remaining < 1:
            raise PayloadAdmissionExceeded(
                "total_nodes", self._budget.max_total_nodes, self._nodes + 1
            )
        return remaining

    def _remap_nodes(
        self, exc: PayloadAdmissionExceeded, remaining: int
    ) -> PayloadAdmissionExceeded:
        if exc.dimension == "nodes" and remaining < self._budget.payload.max_nodes:
            return PayloadAdmissionExceeded(
                "total_nodes", self._budget.max_total_nodes, self._nodes + 1
            )
        return exc

    def _remap(
        self,
        exc: PayloadAdmissionExceeded,
        node_cap: int,
        remaining_nodes: int,
        byte_cap: int,
        remaining_bytes: int,
    ) -> PayloadAdmissionExceeded:
        if exc.dimension == "nodes" and node_cap == remaining_nodes:
            return PayloadAdmissionExceeded(
                "total_nodes", self._budget.max_total_nodes, self._nodes + 1
            )
        if exc.dimension == "output_bytes" and byte_cap == remaining_bytes:
            return PayloadAdmissionExceeded(
                "total_output_bytes",
                self._budget.max_total_output_bytes,
                self._bytes + (exc.observed or byte_cap + 1),
            )
        return exc
