"""Operation-level admission: one budget shared by every step of one operation.

Stage 04B.3. ``OperationAdmissionBudget`` is an immutable, caller-supplied
profile (no defaults, not Canon, not a production limit). Each operation creates
its own ``OperationAdmissionState``; passing that same state through the
envelope, batch, fingerprint, validation and sealing steps means the aggregate
spend is never reset between functions.

Accounting is *work based*: every bounded traversal (freeze, canonical
serialization, every step the schema validator actually takes -- including each
``OneOfSpec`` alternative that re-walks a value) charges the nodes it visited,
and every canonical serialization charges the bytes it produced. A payload that
is processed three times therefore costs three times; repeated processing is
visible and bounded instead of free. ``max_batch_entries`` bounds each
materialized collection (pending events, entries), not a running total.

Per-payload limits (depth, nodes, string/key length, output bytes) and the
aggregate limits (total nodes, total output bytes) always apply *together*: the
effective cap of any single traversal is the tighter of the two. A document that
embeds payloads (the fingerprint, the envelope serializers) first admits every
payload individually and only then runs the whole-document pass.

Refusal is terminal. Once a state has refused an operation it keeps refusing
every later request with the same dimension and limit and its recorded spend is
never reset, so a refused state cannot be reused to start over. A caller error
(for example a non-mapping payload) is not a resource refusal and does not
poison the state.
"""

from __future__ import annotations

import itertools
from collections.abc import Callable, Iterable, Mapping
from dataclasses import dataclass
from typing import TypeVar

from .admission import (
    CanonicalAdmissionBudget,
    PayloadAdmissionBudget,
    PayloadAdmissionExceeded,
    PayloadAdmissionState,
)
from .canonical_json import CanonicalValue, _ByteMeter, _canonical_bounded
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

    __slots__ = ("_budget", "_nodes", "_bytes", "_refusal")

    def __init__(self, budget: OperationAdmissionBudget) -> None:
        if not isinstance(budget, OperationAdmissionBudget):
            raise TypeError("budget must be an OperationAdmissionBudget")
        self._budget = budget
        self._nodes = 0
        self._bytes = 0
        self._refusal: PayloadAdmissionExceeded | None = None

    @property
    def nodes(self) -> int:
        return self._nodes

    @property
    def output_bytes(self) -> int:
        return self._bytes

    @property
    def refused(self) -> bool:
        return self._refusal is not None

    # -- terminal refusal ------------------------------------------------------------------

    def _guard(self) -> None:
        refusal = self._refusal
        if refusal is not None:
            raise PayloadAdmissionExceeded(
                refusal.dimension, refusal.limit, refusal.observed
            )

    def _refuse(self, exc: PayloadAdmissionExceeded) -> PayloadAdmissionExceeded:
        if self._refusal is None:
            self._refusal = exc
        return exc

    # -- collections -------------------------------------------------------------------

    def take_entries(self, items: Iterable[_T]) -> tuple[_T, ...]:
        """Materialize ``items`` consuming at most ``max_batch_entries + 1`` items.

        Only exact built-in list/tuple use the copy fast path; any other
        iterable (including subclasses with an untrustworthy ``len``) is drawn
        through ``islice``. Declared length is never the only evidence.
        """

        self._guard()
        limit = self._budget.max_batch_entries
        if type(items) in (list, tuple):
            if len(items) > limit:  # type: ignore[arg-type]
                raise self._refuse(
                    PayloadAdmissionExceeded("batch_entries", limit, len(items))  # type: ignore[arg-type]
                )
            return tuple(items)
        taken = tuple(itertools.islice(iter(items), limit + 1))
        if len(taken) > limit:
            raise self._refuse(
                PayloadAdmissionExceeded("batch_entries", limit, len(taken))
            )
        return taken

    # -- payload steps -------------------------------------------------------------------

    def freeze_payload(self, payload: object) -> FrozenPayload:
        """Bounded detached snapshot; charges the nodes visited."""

        self._guard()
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
        nodes_before = self._nodes
        try:
            frozen = _freeze_payload_value_bounded(payload, spend)
        except PayloadAdmissionExceeded as exc:
            raise self._refuse(
                self._remap(
                    exc,
                    node_aggregate=remaining < budget.max_nodes,
                    nodes_before=nodes_before,
                )
            ) from None
        finally:
            # whatever happened after the traversal began (success, refusal,
            # TypeError, ...), the visits actually performed stay charged
            self._nodes += spend.nodes_visited
        assert isinstance(frozen, Mapping)
        return frozen

    def admit_payload(self, value: object) -> tuple[bytes, CanonicalValue]:
        """Admit one payload under the per-payload AND aggregate limits.

        Returns ``(canonical_bytes, snapshot)``. The snapshot is the single
        trusted, detached copy the bytes were rendered from (duplicate keys
        rejected, canonical value semantics applied); callers must validate and
        persist *that*, never re-read the original object.
        """

        text, _, snapshot = self._canonical(value, whole_document=False)
        return text.encode("utf-8"), snapshot

    def canonical_payload(self, value: object) -> tuple[bytes, int]:
        """Like ``admit_payload`` but returns ``(bytes, nodes_visited)``."""

        before = self._nodes
        encoded, _ = self.admit_payload(value)
        return encoded, self._nodes - before

    def canonical_document(self, document: object) -> bytes:
        """Canonical bytes of a *metadata-only* document, aggregate limits only.

        Contract: ``document`` must not embed caller-controlled payload trees.
        It is meant for documents the operation built itself from already
        validated scalar fields (event metadata, the hash projection, receipt id
        lists). A document that embeds payloads must use
        ``canonical_document_with_payloads`` so every payload is admitted under
        the per-payload limits and rendered from one trusted snapshot.
        """

        text, _, _ = self._canonical(document, whole_document=True)
        return text.encode("utf-8")

    def canonical_document_with_payloads(
        self,
        build: Callable[[tuple[CanonicalValue, ...]], object],
        payloads: Iterable[object],
    ) -> bytes:
        """Canonical bytes of a document that embeds payloads.

        Every payload is admitted once under the per-payload AND aggregate
        limits; ``build`` receives the resulting trusted snapshots (in order)
        and must construct the document from *those*, never from the original
        objects. The whole-document pass then reads only snapshots, so the
        admitted payload and the serialized payload are the same data even if
        the original is a mapping that reports different content per read.
        """

        snapshots = tuple(self.admit_payload(payload)[1] for payload in payloads)
        text, _, _ = self._canonical(build(snapshots), whole_document=True)
        return text.encode("utf-8")

    def validation_visit(self) -> None:
        """Work meter for the schema validator: one unit per validator step."""

        self._guard()
        if self._nodes + 1 > self._budget.max_total_nodes:
            raise self._refuse(
                PayloadAdmissionExceeded(
                    "total_nodes", self._budget.max_total_nodes, self._nodes + 1
                )
            )
        self._nodes += 1

    # -- internals --------------------------------------------------------------------------

    def _canonical(
        self,
        value: object,
        *,
        whole_document: bool,
    ) -> tuple[str, int, CanonicalValue]:
        self._guard()
        remaining_nodes = self._remaining_nodes()
        remaining_bytes = self._budget.max_total_output_bytes - self._bytes
        if remaining_bytes < 1:
            raise self._refuse(
                PayloadAdmissionExceeded(
                    "total_output_bytes",
                    self._budget.max_total_output_bytes,
                    self._bytes + 1,
                )
            )
        payload = self._budget.payload
        if whole_document:
            node_cap, byte_cap = remaining_nodes, remaining_bytes
            depth = payload.max_depth + _WRAPPER_DEPTH
            text_cap = remaining_bytes  # payload strings were already limited per payload
            string_cap, key_cap = text_cap, text_cap
            node_aggregate = byte_aggregate = True
        else:
            node_cap = min(payload.max_nodes, remaining_nodes)
            byte_cap = min(self._budget.max_payload_output_bytes, remaining_bytes)
            depth = payload.max_depth
            string_cap, key_cap = payload.max_string_length, payload.max_key_length
            node_aggregate = remaining_nodes < payload.max_nodes
            byte_aggregate = remaining_bytes < self._budget.max_payload_output_bytes
        budget = CanonicalAdmissionBudget(
            PayloadAdmissionBudget(depth, node_cap, string_cap, key_cap), byte_cap
        )
        spend = PayloadAdmissionState(budget.payload)
        meter = _ByteMeter(byte_cap)
        nodes_before, bytes_before = self._nodes, self._bytes
        try:
            text, nodes, prepared = _canonical_bounded(value, budget, spend, meter)
        except PayloadAdmissionExceeded as exc:
            raise self._refuse(
                self._remap(
                    exc,
                    node_aggregate=node_aggregate,
                    byte_aggregate=byte_aggregate,
                    nodes_before=nodes_before,
                    bytes_before=bytes_before,
                )
            ) from None
        finally:
            # visits and bytes actually performed/admitted stay charged on every
            # outcome after the traversal began (success, refusal, CanonicalJSONError, ...)
            self._nodes += spend.nodes_visited
            self._bytes += meter.total
        return text, nodes, prepared

    def _remaining_nodes(self) -> int:
        remaining = self._budget.max_total_nodes - self._nodes
        if remaining < 1:
            raise self._refuse(
                PayloadAdmissionExceeded(
                    "total_nodes", self._budget.max_total_nodes, self._nodes + 1
                )
            )
        return remaining

    def _remap(
        self,
        exc: PayloadAdmissionExceeded,
        *,
        node_aggregate: bool = False,
        byte_aggregate: bool = False,
        nodes_before: int = 0,
        bytes_before: int = 0,
    ) -> PayloadAdmissionExceeded:
        """Re-express a pass-local refusal as an aggregate one.

        ``exc.observed`` is the pass-local count that would have been reached;
        the aggregate observed value is the spend *before* the pass plus that
        count, so no unit is counted twice and the refused unit is counted once.
        """

        if exc.dimension == "nodes" and node_aggregate:
            return PayloadAdmissionExceeded(
                "total_nodes",
                self._budget.max_total_nodes,
                nodes_before + (exc.observed or 0),
            )
        if exc.dimension == "output_bytes" and byte_aggregate:
            return PayloadAdmissionExceeded(
                "total_output_bytes",
                self._budget.max_total_output_bytes,
                bytes_before + (exc.observed or 0),
            )
        return exc
