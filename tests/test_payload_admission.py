"""Stage 04B.1: bounded payload freeze (explicit, per-call admission budget).

Small explicit test budgets only; these numbers are not Canon or production
defaults. The bounded path limits visited nodes/depth/lengths; it makes no
wall-clock or memory guarantee and cannot interrupt a blocking next().
"""

from __future__ import annotations

import copy
import itertools
import math
from collections.abc import Mapping, Sequence
from types import MappingProxyType

import pytest

from mentaury.contracts import (
    PayloadAdmissionBudget,
    PayloadAdmissionExceeded,
    canonical_json_bytes,
)
from mentaury.contracts.primitives import freeze_payload, freeze_payload_value


def budget(depth=8, nodes=100, string=16, key=16) -> PayloadAdmissionBudget:
    return PayloadAdmissionBudget(depth, nodes, string, key)


def exceeded(value, b: PayloadAdmissionBudget) -> PayloadAdmissionExceeded:
    with pytest.raises(PayloadAdmissionExceeded) as captured:
        freeze_payload_value(value, b)
    return captured.value


def nested_lists(levels: int):
    value: object = 1
    for _ in range(levels):
        value = [value]
    return value


# --- budget object ------------------------------------------------------------

def test_budget_is_immutable_and_validated() -> None:
    b = budget()
    with pytest.raises(AttributeError):
        b.max_depth = 99  # type: ignore[misc]
    for bad in (0, -1, True, 1.5, "3"):
        with pytest.raises(ValueError):
            PayloadAdmissionBudget(bad, 1, 1, 1)  # type: ignore[arg-type]
        with pytest.raises(ValueError):
            PayloadAdmissionBudget(1, 1, 1, bad)  # type: ignore[arg-type]


def test_exceeded_is_not_a_value_error_and_carries_structured_data() -> None:
    err = exceeded(nested_lists(5), budget(depth=3))
    assert not isinstance(err, ValueError)  # never mistaken for invalid input
    assert (err.dimension, err.limit, err.observed) == ("depth", 3, 4)


def test_error_message_never_contains_payload_content() -> None:
    secret = "TOP-SECRET-CONTENT"
    err = exceeded({"k": [secret * 5]}, budget(string=10))
    text = str(err) + repr(err) + repr(err.args)
    assert secret not in text
    assert err.dimension == "string_length"


# --- depth ----------------------------------------------------------------------

@pytest.mark.parametrize("make", [lambda v: [v], lambda v: {"k": v}], ids=["seq", "map"])
def test_depth_boundary_is_inclusive_and_one_more_level_fails(make) -> None:
    def build(levels):
        value: object = 1
        for _ in range(levels):
            value = make(value)
        return value

    freeze_payload_value(build(3), budget(depth=3))  # exactly at the limit
    err = exceeded(build(4), budget(depth=3))
    assert (err.dimension, err.limit, err.observed) == ("depth", 3, 4)


def test_root_container_has_depth_one_and_scalars_add_no_depth() -> None:
    freeze_payload_value([1, 2, "x"], budget(depth=1))
    freeze_payload_value({"a": 1}, budget(depth=1))
    assert exceeded([[1]], budget(depth=1)).dimension == "depth"


def test_iterative_path_survives_depth_beyond_python_recursion_limit() -> None:
    deep = nested_lists(5_000)
    with pytest.raises(RecursionError):
        freeze_payload_value(deep)  # original unbounded recursive path
    frozen = freeze_payload_value(deep, budget(depth=6_000, nodes=10_000))
    for _ in range(5_000):
        assert isinstance(frozen, tuple)
        frozen = frozen[0]
    assert frozen == 1
    assert exceeded(deep, budget(depth=100, nodes=10_000)).dimension == "depth"


# --- node accounting ------------------------------------------------------------

def test_node_counting_rules_and_inclusive_boundary() -> None:
    # sequence: root + 10 scalars = 11 visits
    wide = list(range(10))
    freeze_payload_value(wide, budget(nodes=11))
    err = exceeded(wide, budget(nodes=10))
    assert (err.dimension, err.limit) == ("nodes", 10)
    # mapping entry costs key + value visit: root + (key + value) = 3
    freeze_payload_value({"a": 1}, budget(nodes=3))
    assert exceeded({"a": 1}, budget(nodes=2)).dimension == "nodes"
    # a scalar root is one visit
    freeze_payload_value(5, budget(nodes=1))


def test_wide_tree_is_bounded() -> None:
    wide = {f"k{i}": [i, i] for i in range(50)}
    assert exceeded(wide, budget(nodes=100)).dimension == "nodes"
    freeze_payload_value(wide, budget(nodes=1 + 50 * (1 + 1 + 2)))


def test_repeated_aliases_and_shared_dag_are_counted_per_visit() -> None:
    shared = [1, 2]
    payload = {"a": shared, "b": shared}
    # root 1 + 2 keys + 2 * (container 1 + 2 scalars) = 9
    frozen = freeze_payload_value(payload, budget(nodes=9))
    assert frozen == {"a": (1, 2), "b": (1, 2)}
    assert exceeded(payload, budget(nodes=8)).dimension == "nodes"
    # a DAG is not a cycle
    diamond = [shared, [shared]]
    freeze_payload_value(diamond, budget(nodes=100))


# --- string / key length (code points, no normalization) -------------------------

def test_string_and_key_limits_are_inclusive_in_code_points() -> None:
    freeze_payload_value({"k" * 5: "v" * 5}, budget(string=5, key=5))
    err = exceeded({"k": "v" * 6}, budget(string=5, key=5))
    assert (err.dimension, err.limit, err.observed) == ("string_length", 5, 6)
    err = exceeded({"k" * 6: 1}, budget(string=5, key=5))
    assert (err.dimension, err.limit, err.observed) == ("key_length", 5, 6)


def test_unicode_is_measured_in_code_points_without_normalization() -> None:
    decomposed = "é" * 3  # 6 code points; NFC would be 3
    assert exceeded([decomposed], budget(string=5)).observed == 6
    astral = "\U0001F600" * 5  # 5 code points (10 UTF-16 units, 20 UTF-8 bytes)
    frozen = freeze_payload_value({astral: astral}, budget(string=5, key=5))
    assert frozen == {astral: astral}
    assert next(iter(frozen)) == astral  # text unchanged, not normalized
    assert list(freeze_payload_value([decomposed], budget(string=6))) == [decomposed]


# --- cycles ----------------------------------------------------------------------

def test_cycles_still_fail_closed_with_type_error() -> None:
    loop: list[object] = []
    loop.append(loop)
    with pytest.raises(TypeError, match="cyclic"):
        freeze_payload_value(loop, budget(depth=50, nodes=1_000))
    mapping: dict[str, object] = {}
    mapping["self"] = mapping
    with pytest.raises(TypeError, match="cyclic"):
        freeze_payload_value(mapping, budget(depth=50, nodes=1_000))
    indirect: dict[str, object] = {"a": []}
    indirect["a"].append(indirect)  # type: ignore[union-attr]
    with pytest.raises(TypeError, match="cyclic"):
        freeze_payload_value(indirect, budget(depth=50, nodes=1_000))


# --- counted sequences with untrustworthy len() -------------------------------------

class _CountedSequence(Sequence):
    """len() claims 1; iteration is endless; counts next() calls."""

    def __init__(self) -> None:
        self.next_calls = 0

    def __len__(self) -> int:
        return 1

    def __getitem__(self, index):  # pragma: no cover - iteration is overridden
        raise IndexError

    def __iter__(self):
        return self

    def __next__(self):
        self.next_calls += 1
        if self.next_calls > 50_000:
            raise RuntimeError("runaway consumption")
        return 1


class _CountedMapping(Mapping):
    def __init__(self) -> None:
        self.next_calls = 0

    def __len__(self) -> int:
        return 1

    def __getitem__(self, key):  # pragma: no cover
        raise KeyError(key)

    def __iter__(self):
        return self

    def items(self):
        return self

    def __next__(self):
        self.next_calls += 1
        if self.next_calls > 50_000:
            raise RuntimeError("runaway consumption")
        return (f"k{self.next_calls}", 1)


def test_lying_len_sequence_traversal_stops_at_the_node_limit() -> None:
    seq = _CountedSequence()
    err = exceeded(seq, budget(nodes=6))
    assert err.dimension == "nodes"
    # root = 1 visit; 5 admitted items; the 6th pulled item is the look-ahead.
    assert seq.next_calls == 6


def test_lying_len_mapping_traversal_stops_without_draining() -> None:
    mapping = _CountedMapping()
    err = exceeded(mapping, budget(nodes=7))
    assert err.dimension == "nodes"
    assert mapping.next_calls <= 7  # nowhere near the 50k runaway cap


def test_remaining_elements_are_not_consumed_after_rejection() -> None:
    consumed = 0

    def producer():
        nonlocal consumed
        for i in range(10_000):
            consumed += 1
            yield i

    class Source(Sequence):
        def __len__(self):
            return 10_000

        def __getitem__(self, i):  # pragma: no cover
            raise IndexError

        def __iter__(self):
            return producer()

    exceeded(Source(), budget(nodes=10))
    assert consumed <= 10


class _Boom(Sequence):
    def __len__(self):
        return 3

    def __getitem__(self, i):  # pragma: no cover
        raise IndexError

    def __iter__(self):
        yield 1
        raise RuntimeError("user iterator failed")


def test_user_iterator_exception_propagates_unchanged_and_state_is_not_reused() -> None:
    b = budget(nodes=10)
    with pytest.raises(RuntimeError, match="user iterator failed"):
        freeze_payload_value([_Boom()], b)
    # a fresh call gets a fresh spend state from the same immutable budget
    assert freeze_payload_value([1, 2, 3], b) == (1, 2, 3)


# --- per-call state & source immutability -------------------------------------------

def test_every_call_gets_its_own_budget_state() -> None:
    b = budget(nodes=4)
    payload = [1, 2, 3]  # exactly 4 visits
    for _ in range(5):  # would fail on the 2nd call if spend leaked between calls
        assert freeze_payload_value(payload, b) == (1, 2, 3)


def test_source_object_is_unchanged_after_rejection() -> None:
    source = {"a": [1, {"b": "x" * 20}], "c": [3, 4]}
    snapshot = copy.deepcopy(source)
    with pytest.raises(PayloadAdmissionExceeded):
        freeze_payload_value(source, budget(string=10))
    assert source == snapshot
    assert isinstance(source["a"], list) and isinstance(source, dict)


# --- compatibility with the unbudgeted path ------------------------------------------

VALID_VALUES = [
    None,
    True,
    7,
    "text",
    1.5,
    [],
    {},
    [1, [2, [3, []]], {"a": None}],
    {"z": 1, "a": [1, 2, {"m": "é", "n": [True, False]}], "k": {}},
    {"nested": {"deeper": {"deepest": [125, "x", None]}}},
]


@pytest.mark.parametrize("value", VALID_VALUES)
def test_bounded_result_matches_unbounded_and_canonical_bytes(value) -> None:
    unbounded = freeze_payload_value(value)
    bounded = freeze_payload_value(value, budget(depth=20, nodes=1_000))
    assert bounded == unbounded
    assert type(bounded) is type(unbounded)
    if isinstance(value, dict):
        assert isinstance(bounded, MappingProxyType)
        assert list(bounded) == list(unbounded) == list(value)  # key order kept
        assert canonical_json_bytes(bounded) == canonical_json_bytes(unbounded)
        assert canonical_json_bytes(bounded) == canonical_json_bytes(value)
    if isinstance(value, list):
        assert isinstance(bounded, tuple)


def test_snapshot_is_detached_immutable_and_ordered() -> None:
    source = {"b": [1, 2], "a": {"x": [3]}}
    frozen = freeze_payload(source, budget())
    source["b"].append(99)  # type: ignore[union-attr]
    source["a"]["x"].append(4)  # type: ignore[index]
    assert frozen == {"b": (1, 2), "a": {"x": (3,)}}
    assert list(frozen) == ["b", "a"]
    with pytest.raises(TypeError):
        frozen["new"] = 1  # type: ignore[index]
    assert isinstance(frozen["a"], MappingProxyType)
    assert isinstance(frozen["b"], tuple)


def test_float_behavior_stays_at_freeze_level() -> None:
    frozen = freeze_payload_value([math.inf, -0.0, 0.1], budget())
    assert frozen[0] == math.inf and math.isnan(freeze_payload_value(math.nan, budget()))  # type: ignore[arg-type,index]
    assert freeze_payload_value([math.inf]) == freeze_payload_value([math.inf], budget())


def test_type_rejections_match_the_unbounded_path() -> None:
    for bad in (b"bytes", bytearray(b"x"), {1, 2}, object(), {1: "non-string key"}):
        with pytest.raises(TypeError):
            freeze_payload_value(bad)
        with pytest.raises(TypeError):
            freeze_payload_value(bad, budget())
    with pytest.raises(TypeError, match="keys must be strings"):
        freeze_payload_value({1: "x"}, budget())


def test_bounded_freeze_payload_refuses_non_mapping_root_before_traversal() -> None:
    seq = _CountedSequence()
    with pytest.raises(TypeError, match="mapping"):
        freeze_payload(seq, budget())  # type: ignore[arg-type]
    assert seq.next_calls == 0


def test_no_hidden_defaults_unbudgeted_calls_and_constructors_are_unchanged() -> None:
    from mentaury.contracts import PendingEvent

    big = {"items": list(range(5_000))}  # far above any test budget
    assert len(freeze_payload(big)["items"]) == 5_000
    pending = PendingEvent("TEST_EVENT", "test-event/v1", True, big)
    assert len(pending.payload["items"]) == 5_000  # constructors are not budgeted


# --- final boundary fixes (review findings F1-F3) -----------------------------------

import gc  # noqa: E402
import weakref  # noqa: E402

from mentaury.contracts import primitives as _primitives  # noqa: E402


class _LyingStr(str):
    """A str subclass whose len() lies; the real content length is len via str."""

    claimed = 0

    def __len__(self) -> int:
        return type(self).claimed


def test_f1_lying_str_value_cannot_bypass_string_limit() -> None:
    long_value = _LyingStr("x" * 100)  # claims len() == 0
    err = exceeded([long_value], budget(string=5))
    assert (err.dimension, err.limit, err.observed) == ("string_length", 5, 100)


def test_f1_lying_str_key_cannot_bypass_key_limit() -> None:
    long_key = _LyingStr("k" * 100)
    err = exceeded({long_key: 1}, budget(key=5))
    assert (err.dimension, err.limit, err.observed) == ("key_length", 5, 100)


def test_f1_overstated_len_does_not_reject_short_content() -> None:
    class Overstated(str):
        def __len__(self) -> int:
            return 10_000

    frozen = freeze_payload_value({Overstated("ab"): Overstated("cd")}, budget(string=5, key=5))
    assert list(frozen.items()) == [("ab", "cd")]  # real length 2 is within limits


class _Dyn(Sequence):
    """Container whose iterator is independent of ``self`` and yields fresh children."""

    registry: list = []
    alive_at_leaf: list = []
    max_depth = 0

    def __init__(self, depth: int) -> None:
        self.depth = depth
        type(self).registry.append(weakref.ref(self))

    def __len__(self) -> int:
        return 1

    def __getitem__(self, index):  # pragma: no cover
        raise IndexError

    def __iter__(self):
        return _dyn_children(self.depth)


def _dyn_children(depth: int):
    # Deliberately holds no reference to the container object itself.
    if depth >= _Dyn.max_depth:
        gc.collect()
        _Dyn.alive_at_leaf = [ref() is not None for ref in _Dyn.registry]
        yield "leaf"
        return
    yield _Dyn(depth + 1)


def test_f2_active_containers_stay_alive_so_ids_cannot_be_reused() -> None:
    _Dyn.registry = []
    _Dyn.alive_at_leaf = []
    _Dyn.max_depth = 25
    frozen = freeze_payload_value(_Dyn(0), budget(depth=100, nodes=1_000))
    for _ in range(25):
        frozen = frozen[0]  # type: ignore[index]
    assert frozen == ("leaf",)
    # every ancestor (all registered containers) was still alive at the leaf
    assert _Dyn.alive_at_leaf and all(_Dyn.alive_at_leaf)


def test_f2_containers_are_released_after_the_freeze_finishes() -> None:
    _Dyn.registry = []
    _Dyn.max_depth = 5
    freeze_payload_value(_Dyn(0), budget(depth=100, nodes=1_000))
    gc.collect()
    assert all(ref() is None for ref in _Dyn.registry)  # no lingering strong refs


def test_f2_real_cycles_and_dags_are_still_handled_with_dynamic_containers() -> None:
    class SelfYielding(Sequence):
        def __len__(self):
            return 1

        def __getitem__(self, index):  # pragma: no cover
            raise IndexError

        def __iter__(self):
            return iter([self])  # a genuine cycle via an independent iterator

    with pytest.raises(TypeError, match="cyclic"):
        freeze_payload_value(SelfYielding(), budget(depth=50, nodes=1_000))
    shared = _Dyn(0)
    _Dyn.max_depth = 1
    freeze_payload_value([shared, shared], budget(depth=10, nodes=1_000))  # DAG, no cycle


def _former_sentinel() -> object:
    return getattr(_primitives, "_END", object())


def test_f3_sentinel_as_sequence_item_is_not_silent_truncation() -> None:
    marker = _former_sentinel()
    with pytest.raises(TypeError, match="unsupported payload value"):
        freeze_payload_value([1, marker, 3], budget())


def test_f3_sentinel_as_mapping_value_is_not_silent_truncation() -> None:
    marker = _former_sentinel()
    with pytest.raises(TypeError, match="unsupported payload value"):
        freeze_payload_value({"a": 1, "b": marker, "c": 3}, budget())


def test_f3_sentinel_as_root_and_nested_is_rejected() -> None:
    marker = _former_sentinel()
    for value in (marker, [[marker]], {"k": [marker]}):
        with pytest.raises(TypeError):
            freeze_payload_value(value, budget())
