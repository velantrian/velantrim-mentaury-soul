"""Stage 04B.2: opt-in bounded canonical serialization and decimal admission.

Small explicit test budgets only (not Canon, not production defaults). The
bounded path bounds visited nodes/depth/lengths and exact output bytes; it makes
no wall-clock or memory guarantee and cannot interrupt a blocking next().
"""

from __future__ import annotations

import gc
import json
import weakref
from collections.abc import Mapping, Sequence
from decimal import Decimal
from pathlib import Path

import pytest

from mentaury.contracts import (
    SAFE_INTEGER_MAX,
    CanonicalAdmissionBudget,
    CanonicalJSONError,
    PayloadAdmissionBudget,
    PayloadAdmissionExceeded,
    canonical_decimal_string,
    canonical_json_bytes,
    canonical_json_text,
)

FIXTURES = Path(__file__).parent / "fixtures" / "canonical_json_v1_vectors.json"


def cb(depth=16, nodes=1_000, string=64, key=64, out=10_000) -> CanonicalAdmissionBudget:
    return CanonicalAdmissionBudget(PayloadAdmissionBudget(depth, nodes, string, key), out)


def exceeded(value, budget) -> PayloadAdmissionExceeded:
    with pytest.raises(PayloadAdmissionExceeded) as captured:
        canonical_json_bytes(value, budget)
    return captured.value


# --- budget object -----------------------------------------------------------------

def test_budget_is_immutable_validated_and_has_no_defaults() -> None:
    budget = cb()
    with pytest.raises(AttributeError):
        budget.max_output_bytes = 1  # type: ignore[misc]
    for bad in (0, -1, True, 1.5):
        with pytest.raises(ValueError):
            CanonicalAdmissionBudget(PayloadAdmissionBudget(1, 1, 1, 1), bad)  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        CanonicalAdmissionBudget(object(), 10)  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        canonical_json_bytes({}, object())  # type: ignore[arg-type]


# --- compatibility vectors ------------------------------------------------------------

def test_bounded_output_matches_every_conformance_vector_byte_for_byte() -> None:
    vectors = json.loads(FIXTURES.read_text(encoding="utf-8"))
    for vector in vectors["canonical_values"]:
        bounded = canonical_json_bytes(vector["value"], cb())
        assert bounded == canonical_json_bytes(vector["value"]), vector["name"]
        assert bounded.decode("utf-8") == vector["canonical"], vector["name"]
        assert bounded.hex() == vector["utf8_hex"], vector["name"]
    for vector in vectors["decimal_strings"]:
        assert canonical_decimal_string(vector["input"], 100) == vector["canonical"]


PARITY = [
    None, True, False, 0, -7, SAFE_INTEGER_MAX, -SAFE_INTEGER_MAX, "", "plain",
    "line\n\"q\"\\ \t \u0000 \u001f", "é", "é", "\U0001F600   \u007f",
    [], {}, [[], {}], {"": 1}, {"z": 1, "a": [1, {"b": None}], "m": {"k": "v"}},
    {"\U0001F600": 1, "￿": 2, "a": 3, "é": 4, "z": 5},  # code-point key order
    [1, [2, [3, [4, [5]]]]], {"a": {"b": {"c": {"d": []}}}},
    (1, 2, (3, "x")),  # tuples are sequences
]


@pytest.mark.parametrize("value", PARITY)
def test_bounded_equals_unbounded_text_bytes_and_exact_byte_count(value) -> None:
    expected = canonical_json_bytes(value)
    assert canonical_json_bytes(value, cb()) == expected
    assert canonical_json_text(value, cb()) == expected.decode("utf-8")
    canonical_json_bytes(value, cb(out=len(expected)))  # inclusive, exact
    if len(expected) > 1:
        err = exceeded(value, cb(out=len(expected) - 1))
        assert err.dimension == "output_bytes"
        assert err.limit == len(expected) - 1


# --- error parity (canonical failures stay CanonicalJSONError, same message) -------------

class _Weird:
    pass


@pytest.mark.parametrize(
    "value, match",
    [
        ({"n": 1.0}, "float is forbidden at \\$\\.n"),
        ([Decimal("1")], "Decimal is forbidden at \\$\\[0\\]"),
        ({"a": [b"x"]}, "unsupported canonical JSON type at \\$\\.a\\[0\\]: bytes"),
        ({"a": _Weird()}, "unsupported canonical JSON type at \\$\\.a: _Weird"),
        ({"bad": "\ud800"}, "lone surrogate is forbidden at \\$\\.bad"),
        ({"\ud800": 1}, "lone surrogate is forbidden at \\$\\.<key>"),
        ({1: "x"}, "object key must be a string at \\$"),
        ({"n": SAFE_INTEGER_MAX + 1}, "integer outside safe range at \\$\\.n"),
        ([[-SAFE_INTEGER_MAX - 1]], "integer outside safe range at \\$\\[0\\]\\[0\\]"),
    ],
)
def test_canonical_errors_match_the_unbounded_path(value, match) -> None:
    with pytest.raises(CanonicalJSONError, match=match) as unbounded:
        canonical_json_bytes(value)
    with pytest.raises(CanonicalJSONError, match=match) as bounded:
        canonical_json_bytes(value, cb())
    assert str(bounded.value) == str(unbounded.value)


def test_cycles_are_canonical_errors_with_the_same_wording() -> None:
    loop: list[object] = []
    loop.append(loop)
    with pytest.raises(CanonicalJSONError, match="cyclic sequence is forbidden at \\$"):
        canonical_json_bytes(loop, cb())
    mapping: dict[str, object] = {}
    mapping["m"] = mapping
    with pytest.raises(CanonicalJSONError, match="cyclic mapping is forbidden at \\$\\.m"):
        canonical_json_bytes(mapping, cb())


def test_duplicate_keys_from_a_custom_mapping_are_rejected() -> None:
    class Dup(Mapping):
        def __len__(self):
            return 2

        def __getitem__(self, key):  # pragma: no cover
            raise KeyError(key)

        def __iter__(self):  # pragma: no cover
            return iter(())

        def items(self):
            return iter([("k", 1), ("k", 2)])

    with pytest.raises(CanonicalJSONError, match="duplicate object key at \\$: k"):
        canonical_json_bytes(Dup())
    with pytest.raises(CanonicalJSONError, match="duplicate object key at \\$: k"):
        canonical_json_bytes(Dup(), cb())


# --- depth: RecursionError at ~1500 on the unbounded path --------------------------------

def test_depth_1500_is_handled_iteratively_and_exact() -> None:
    value: object = 1
    for _ in range(1_500):
        value = [value]
    with pytest.raises(RecursionError):
        canonical_json_bytes(value)  # baseline behaviour, unchanged
    out = canonical_json_bytes(value, cb(depth=1_500, nodes=2_000, out=4_000))
    assert out == b"[" * 1_500 + b"1" + b"]" * 1_500
    assert exceeded(value, cb(depth=1_499, nodes=2_000, out=4_000)).dimension == "depth"


def test_deep_mappings_are_also_iterative() -> None:
    value: object = 0
    for _ in range(1_200):
        value = {"k": value}
    out = canonical_json_text(value, cb(depth=1_200, nodes=3_000, out=20_000))
    assert out == '{"k":' * 1_200 + "0" + "}" * 1_200


# --- huge integers: controlled error, no value in the message -----------------------------

def test_huge_integer_is_a_controlled_canonical_error_on_both_paths() -> None:
    huge = 10**5_000  # str(huge) raises ValueError on CPython's digit limit
    for budget in (None, cb()):
        with pytest.raises(CanonicalJSONError) as captured:
            canonical_json_bytes({"n": huge}, budget)
        assert type(captured.value) is CanonicalJSONError  # not a stray ValueError
        assert "safe range" in str(captured.value)
        assert len(str(captured.value)) < 100  # value not embedded


def test_historical_message_for_moderately_large_integers_is_unchanged() -> None:
    with pytest.raises(CanonicalJSONError, match=str(SAFE_INTEGER_MAX + 1)):
        canonical_json_bytes([SAFE_INTEGER_MAX + 1])


# --- traversal budgets -----------------------------------------------------------------------

def test_node_string_and_key_limits_are_enforced_and_inclusive() -> None:
    canonical_json_bytes([1, 2, 3], cb(nodes=4))
    assert exceeded([1, 2, 3], cb(nodes=3)).dimension == "nodes"
    canonical_json_bytes({"k" * 5: "v" * 5}, cb(string=5, key=5))
    assert exceeded({"k": "v" * 6}, cb(string=5, key=5)).dimension == "string_length"
    assert exceeded({"k" * 6: 1}, cb(string=5, key=5)).dimension == "key_length"


def test_lying_str_subclasses_are_measured_and_serialized_by_real_content() -> None:
    class Liar(str):
        def __len__(self) -> int:
            return 0

        def encode(self, *args, **kwargs):  # pragma: no cover - must not be used
            return b""

    assert exceeded([Liar("x" * 40)], cb(string=5)).observed == 40
    out = canonical_json_bytes({Liar("k"): Liar("v")}, cb())
    assert out == b'{"k":"v"}'


def test_int_subclass_is_serialized_by_real_value() -> None:
    class Liar(int):
        def __str__(self) -> str:  # pragma: no cover - must not be used
            return "999"

    assert canonical_json_bytes([Liar(7)], cb()) == b"[7]"


class _Endless(Sequence):
    """len() claims 1; iteration never ends; counts next() calls."""

    def __init__(self) -> None:
        self.next_calls = 0

    def __len__(self) -> int:
        return 1

    def __getitem__(self, index):  # pragma: no cover
        raise IndexError

    def __iter__(self):
        return self

    def __next__(self):
        self.next_calls += 1
        if self.next_calls > 50_000:
            raise RuntimeError("runaway consumption")
        return 1


def test_misleading_len_traversal_stops_at_the_node_limit() -> None:
    seq = _Endless()
    err = exceeded(seq, cb(nodes=6, out=10_000))
    assert err.dimension in {"nodes", "output_bytes"}
    assert seq.next_calls <= 6  # nowhere near the 10,000-visit baseline


def test_output_bytes_are_enforced_before_the_text_is_materialized() -> None:
    seq = _Endless()
    err = exceeded(seq, cb(nodes=10_000, out=11))
    assert err.dimension == "output_bytes"
    assert seq.next_calls <= 12  # stopped by bytes long before nodes ran out


def test_per_call_state_source_unchanged_and_no_payload_in_error() -> None:
    budget = cb(out=20)
    payload = {"secret": ["TOP-SECRET-" * 3, 1]}
    snapshot = json.dumps(payload, sort_keys=True)
    err = exceeded(payload, budget)
    assert json.dumps(payload, sort_keys=True) == snapshot
    assert "TOP-SECRET" not in str(err) + repr(err)
    assert not isinstance(err, ValueError)
    for _ in range(3):  # fresh spend state per call from one immutable budget
        assert canonical_json_bytes([1, 2], cb(nodes=3, out=5)) == b"[1,2]"


class _Dyn(Sequence):
    registry: list = []
    alive: list = []
    limit = 0

    def __init__(self, depth: int) -> None:
        self.depth = depth
        type(self).registry.append(weakref.ref(self))

    def __len__(self) -> int:
        return 1

    def __getitem__(self, index):  # pragma: no cover
        raise IndexError

    def __iter__(self):
        return _children(self.depth)


def _children(depth: int):
    if depth >= _Dyn.limit:
        gc.collect()
        _Dyn.alive = [ref() is not None for ref in _Dyn.registry]
        yield 1
        return
    yield _Dyn(depth + 1)


def test_active_containers_stay_alive_so_dynamic_children_cannot_fake_a_cycle() -> None:
    _Dyn.registry, _Dyn.alive, _Dyn.limit = [], [], 20
    out = canonical_json_bytes(_Dyn(0), cb(depth=50, nodes=200, out=200))
    assert out == b"[" * 21 + b"1" + b"]" * 21
    assert _Dyn.alive and all(_Dyn.alive)
    gc.collect()
    assert all(ref() is None for ref in _Dyn.registry)


# --- decimal admission --------------------------------------------------------------------------

@pytest.mark.parametrize("text", ["1E+100000", "1E-100000", "-1E+100000", "123456789E-100000"])
def test_decimal_with_huge_exponent_is_refused_before_formatting(text) -> None:
    for candidate in (text, Decimal(text)):
        with pytest.raises(PayloadAdmissionExceeded) as captured:
            canonical_decimal_string(candidate, 100)
        assert captured.value.dimension == "decimal_chars"
        assert captured.value.limit == 100
        assert captured.value.observed is not None and captured.value.observed > 100


def test_decimal_input_text_length_is_bounded_before_parsing() -> None:
    with pytest.raises(PayloadAdmissionExceeded) as captured:
        canonical_decimal_string("1" * 500, 100)
    assert captured.value.observed == 500


def test_decimal_unbounded_default_and_valid_results_are_unchanged() -> None:
    cases = ["1.2300", "-0", "0", "1E+3", "0.000123", "-12.5", "100", "1E-6", "5E-1"]
    for text in cases:
        assert canonical_decimal_string(text, 1_000) == canonical_decimal_string(text)
        assert canonical_decimal_string(Decimal(text), 1_000) == canonical_decimal_string(Decimal(text))
    assert len(canonical_decimal_string("1E+3000")) == 3001  # default path unchanged


def test_decimal_boundary_and_other_failures_keep_their_errors() -> None:
    assert canonical_decimal_string("1E+3", 5) == "1000"
    with pytest.raises(CanonicalJSONError, match="finite"):
        canonical_decimal_string("NaN", 10)
    with pytest.raises(CanonicalJSONError, match="invalid decimal"):
        canonical_decimal_string("not-a-number", 20)
    with pytest.raises(CanonicalJSONError, match="unpadded"):
        canonical_decimal_string(" 1", 10)
    for bad in (0, -1, True, 1.5):
        with pytest.raises(ValueError):
            canonical_decimal_string("1", bad)  # type: ignore[arg-type]
    assert canonical_decimal_string("0E+100000", 10) == "0"  # zero is never expanded


def test_unbudgeted_callers_and_envelope_serializers_are_untouched() -> None:
    big = {"items": list(range(5_000))}
    assert canonical_json_bytes(big).startswith(b'{"items":[0,1,2')
    assert canonical_json_bytes([]) == b"[]"


# --- decimal pre-estimate must equal the real plain-notation length ---------------------------

@pytest.mark.parametrize(
    "text, actual",
    [("-0.01", 5), ("1", 1), ("-1", 2), ("0.5", 3), ("-0.5", 4), ("10", 2), ("-10", 3),
     ("123.456", 7), ("-123.456", 8), ("0.00100", 7), ("1E+3", 4), ("-1E+3", 5),
     ("1E-3", 5), ("-1E-3", 6), ("12E-1", 3), ("-12E-1", 4), ("120E-1", 4)],
)
def test_decimal_limit_is_exact_at_the_boundary_for_both_signs(text, actual) -> None:
    value = Decimal(text)
    assert len(format(value, "f")) == actual  # the table itself is real
    expected = canonical_decimal_string(value)
    assert canonical_decimal_string(value, actual) == expected  # limit == length: ok
    assert canonical_decimal_string(value, actual + 1) == expected
    if actual > 1:
        with pytest.raises(PayloadAdmissionExceeded) as captured:
            canonical_decimal_string(value, actual - 1)  # one below: refused
        assert (captured.value.dimension, captured.value.limit) == ("decimal_chars", actual - 1)
        assert captured.value.observed == actual  # reported value is the exact length


def test_decimal_estimate_equals_real_length_over_a_grid() -> None:
    from mentaury.contracts.canonical_json import _plain_notation_length

    for sign in ("", "-"):
        for digits in ("1", "7", "10", "12", "105", "9999", "100000"):
            for exponent in range(-8, 9):
                value = Decimal(f"{sign}{digits}E{exponent:+d}")
                assert _plain_notation_length(value) == len(format(value, "f")), value


@pytest.mark.parametrize("sign", ["", "-"])
def test_decimal_huge_exponents_are_exact_and_refused_without_formatting(sign) -> None:
    from mentaury.contracts.canonical_json import _plain_notation_length

    for text, length in ((f"{sign}1E+100000", 100_001), (f"{sign}1E-100000", 100_002)):
        value = Decimal(text)
        expected = length + (1 if sign else 0)
        assert _plain_notation_length(value) == expected
        with pytest.raises(PayloadAdmissionExceeded) as captured:
            canonical_decimal_string(value, expected - 1)
        assert captured.value.observed == expected
    # exactly at the limit the (large but admitted) value still normalizes
    assert len(canonical_decimal_string(Decimal(f"{sign}1E+2000"), 2_001 + (1 if sign else 0))) == (
        2_001 + (1 if sign else 0)
    )


def test_decimal_zero_is_never_expanded_whatever_its_exponent_or_sign() -> None:
    for text in ("0", "-0", "0E+100000", "-0E-100000", "0.000"):
        assert canonical_decimal_string(Decimal(text), 1) == "0"


# --- final resource boundaries (review findings F1, F2) ----------------------------------------

import mentaury.contracts.canonical_json as _cj  # noqa: E402
from decimal import DecimalTuple  # noqa: E402


class _DumpsSpy:
    """Records the size of every str handed to json.dumps (instrumentation)."""

    def __init__(self, real) -> None:
        self.real = real
        self.largest = 0

    def __call__(self, obj, *args, **kwargs):
        if isinstance(obj, str):
            self.largest = max(self.largest, len(obj))
        return self.real(obj, *args, **kwargs)


def _spy(monkeypatch) -> _DumpsSpy:
    spy = _DumpsSpy(_cj.json.dumps)
    monkeypatch.setattr(_cj.json, "dumps", spy)
    return spy


def test_f1_rejected_string_value_is_never_fully_materialized(monkeypatch) -> None:
    spy = _spy(monkeypatch)
    big = "é" * 50_000  # 100,000 UTF-8 bytes; string budget is far larger than output
    err = exceeded([big], cb(string=100_000, nodes=10, out=100))
    assert (err.dimension, err.limit) == ("output_bytes", 100)
    assert err.observed is not None and err.observed < 100 + 4 * _cj._STRING_CHUNK
    assert spy.largest <= _cj._STRING_CHUNK  # no full-string json.dumps / encode


def test_f1_rejected_key_is_never_fully_materialized(monkeypatch) -> None:
    spy = _spy(monkeypatch)
    err = exceeded({"k" * 50_000: 1}, cb(key=100_000, string=100_000, nodes=10, out=100))
    assert err.dimension == "output_bytes"
    assert spy.largest <= _cj._STRING_CHUNK


def test_f1_escape_heavy_input_is_rejected_incrementally(monkeypatch) -> None:
    spy = _spy(monkeypatch)
    # 20,000 code points but 6 bytes each once escaped (\u0000): ~120 kB
    err = exceeded(["\u0000" * 20_000], cb(string=100_000, nodes=10, out=500))
    assert err.dimension == "output_bytes"
    assert spy.largest <= _cj._STRING_CHUNK


@pytest.mark.parametrize("length", [0, 1, 255, 256, 257, 511, 512, 513, 1_000, 2_049])
def test_f1_incremental_size_is_exact_across_chunk_boundaries(length) -> None:
    alphabet = ['a', 'é', '€', '\U0001F600', '"', '\\', '\n', '\t', '\u0000', '\u001f', '\u007f', ' ']
    text = "".join(alphabet[i % len(alphabet)] for i in range(length))
    value = {text: text}
    expected = canonical_json_bytes(value)
    canonical_json_bytes(value, cb(string=5_000, key=5_000, out=len(expected)))
    err = exceeded(value, cb(string=5_000, key=5_000, out=len(expected) - 1))
    assert err.dimension == "output_bytes"
    assert canonical_json_bytes(value, cb(string=5_000, key=5_000, out=10**7)) == expected


def test_f1_lone_surrogate_in_a_long_string_is_still_a_canonical_error() -> None:
    value = ["a" * 700 + "\ud800" + "b" * 10]
    with pytest.raises(CanonicalJSONError, match="lone surrogate is forbidden at \\$\\[0\\]"):
        canonical_json_bytes(value, cb(string=5_000, out=10**7))


class _LiarDecimal(Decimal):
    """Overrides every inspection hook an estimate might rely on."""

    def as_tuple(self):
        return DecimalTuple(0, (1,), 0)  # always claims "1"

    def is_finite(self):
        return True

    def is_zero(self):
        return True

    def __format__(self, spec):
        return "1"


class _SmallTupleLiar(Decimal):
    def as_tuple(self):
        return DecimalTuple(0, (1,), 0)


class _ZeroLiar(Decimal):
    def is_zero(self):
        return True


class _FiniteLiar(Decimal):
    def is_finite(self):
        return True


class _FormatLiar(Decimal):
    def __format__(self, spec):
        return "999"


@pytest.mark.parametrize("liar", [_LiarDecimal, _SmallTupleLiar, _ZeroLiar])
def test_f2_decimal_subclass_cannot_bypass_the_rendered_char_limit(liar) -> None:
    with pytest.raises(PayloadAdmissionExceeded) as captured:
        canonical_decimal_string(liar("1E+100000"), 100)
    assert (captured.value.dimension, captured.value.observed) == ("decimal_chars", 100_001)
    with pytest.raises(PayloadAdmissionExceeded):
        canonical_decimal_string(liar("-1E-100000"), 100)


def test_f2_zero_flag_lie_cannot_turn_a_nonzero_value_into_zero() -> None:
    assert canonical_decimal_string(_ZeroLiar("1.50"), 100) == "1.5"
    assert canonical_decimal_string(_LiarDecimal("2.5"), 100) == "2.5"


def test_f2_finite_flag_lie_cannot_smuggle_nan_or_infinity() -> None:
    for text in ("NaN", "Infinity", "-Infinity", "sNaN"):
        with pytest.raises(CanonicalJSONError, match="finite"):
            canonical_decimal_string(_FiniteLiar(text), 100)


def test_f2_format_override_cannot_change_the_result() -> None:
    assert canonical_decimal_string(_FormatLiar("1.50"), 100) == "1.5"
    assert canonical_decimal_string(_FormatLiar("-0.01"), 5) == "-0.01"
    with pytest.raises(PayloadAdmissionExceeded):
        canonical_decimal_string(_FormatLiar("-0.01"), 4)


def test_f2_str_subclass_input_is_normalized_before_inspection() -> None:
    class StrLiar(str):
        def strip(self, *args):
            return str.__str__(self)  # pretends there is no padding

    with pytest.raises(CanonicalJSONError, match="unpadded"):
        canonical_decimal_string(StrLiar(" 1"), 10)


def test_f2_ordinary_decimals_and_the_unbudgeted_path_are_unchanged() -> None:
    for text in ("1.2300", "-0", "0", "1E+3", "-12.5", "0.000123", "1E-6"):
        assert canonical_decimal_string(Decimal(text), 1_000) == canonical_decimal_string(Decimal(text))
        assert canonical_decimal_string(text, 1_000) == canonical_decimal_string(text)
