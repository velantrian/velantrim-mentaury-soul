"""Explicit, caller-supplied payload admission budgets (Stage 04B.1).

A budget bounds how much of an *untrusted payload tree* a freeze operation is
willing to traverse. It is a non-Canonical implementation profile: Mentaury
defines no default numeric limits here, every caller must pass its own.

Accounting rules (the contract of ``freeze_payload_value(..., budget=...)``):

* depth   - the root container has depth 1; each nested container adds 1.
            Scalars do not add depth. The limit is inclusive.
* nodes   - every *visit* costs 1: the root, every container, every scalar
            value and every mapping key. A mapping entry therefore costs
            1 (key) + the visit of its value; nothing is counted twice for one
            visit. A shared object (alias / DAG) is charged on every visit.
* string_length / key_length - length in Unicode code points (``len(str)``),
            no normalization; applied to string values and mapping keys.
            The limit is inclusive.

Traversal stops at the first exceeded dimension; only the one item needed to
detect the excess is pulled (look-ahead). Declared ``len()`` of a collection is
never used as evidence of its real size. The budget bounds visited nodes; it is
not a wall-clock or memory guarantee and cannot interrupt a blocking ``next()``.
"""

from __future__ import annotations

from dataclasses import dataclass


class PayloadAdmissionExceeded(RuntimeError):
    """A payload tree exceeded its admission budget.

    This is a resource-admission outcome only. It is NOT evidence of
    corruption, schema invalidity or falsity of the data, and it deliberately
    does not derive from ``ValueError`` so that it is never mistaken for
    invalid input. The message never contains payload content.

    ``observed`` is the value at the moment of detection: exact for depth and
    string/key lengths, and ``limit + 1`` (a lower bound) for ``nodes``.
    """

    def __init__(self, dimension: str, limit: int, observed: int | None) -> None:
        self.dimension = dimension
        self.limit = limit
        self.observed = observed
        seen = "unknown" if observed is None else str(observed)
        super().__init__(
            f"PAYLOAD_ADMISSION_EXCEEDED: {dimension} limit {limit}, observed {seen}"
        )


@dataclass(frozen=True, slots=True)
class PayloadAdmissionBudget:
    """Immutable limits for one freeze operation; all bounds are inclusive."""

    max_depth: int
    max_nodes: int
    max_string_length: int
    max_key_length: int

    def __post_init__(self) -> None:
        for name in ("max_depth", "max_nodes", "max_string_length", "max_key_length"):
            value = getattr(self, name)
            if isinstance(value, bool) or not isinstance(value, int) or value < 1:
                raise ValueError(f"{name} must be a positive integer")


@dataclass(frozen=True, slots=True)
class CanonicalAdmissionBudget:
    """Limits for one bounded canonical serialization (Stage 04B.2).

    ``payload`` bounds the traversal exactly like the bounded freeze;
    ``max_output_bytes`` bounds the exact UTF-8 size of the canonical output and
    is enforced incrementally, before the output text is materialized.
    Caller-supplied, inclusive, no defaults.
    """

    payload: PayloadAdmissionBudget
    max_output_bytes: int

    def __post_init__(self) -> None:
        if not isinstance(self.payload, PayloadAdmissionBudget):
            raise TypeError("payload must be a PayloadAdmissionBudget")
        value = self.max_output_bytes
        if isinstance(value, bool) or not isinstance(value, int) or value < 1:
            raise ValueError("max_output_bytes must be a positive integer")


class PayloadAdmissionState:
    """Mutable spend tracker for exactly one operation (never shared)."""

    __slots__ = ("_budget", "_nodes")

    def __init__(self, budget: PayloadAdmissionBudget) -> None:
        if not isinstance(budget, PayloadAdmissionBudget):
            raise TypeError("budget must be a PayloadAdmissionBudget")
        self._budget = budget
        self._nodes = 0

    def charge_node(self) -> None:
        self._nodes += 1
        if self._nodes > self._budget.max_nodes:
            raise PayloadAdmissionExceeded(
                "nodes", self._budget.max_nodes, self._nodes
            )

    def check_depth(self, depth: int) -> None:
        if depth > self._budget.max_depth:
            raise PayloadAdmissionExceeded("depth", self._budget.max_depth, depth)

    def check_string(self, value: str) -> None:
        # str.__len__ measures the real code points even for str subclasses
        # that override __len__ with an untrustworthy value.
        length = str.__len__(value)
        if length > self._budget.max_string_length:
            raise PayloadAdmissionExceeded(
                "string_length", self._budget.max_string_length, length
            )

    def check_key(self, key: str) -> None:
        length = str.__len__(key)
        if length > self._budget.max_key_length:
            raise PayloadAdmissionExceeded(
                "key_length", self._budget.max_key_length, length
            )
