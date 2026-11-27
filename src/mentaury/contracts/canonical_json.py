"""MENTAURY_CANONICAL_JSON_V1 deterministic serialization profile.

This is a deliberately restricted profile, not a claim of RFC 8785 support.
It creates deterministic UTF-8 JSON bytes for portable value trees and typed
P0 envelopes. Cryptographic hashing and persistence are owned by later P0
milestones.
"""

from __future__ import annotations

import json
import re
from collections.abc import Iterable, Mapping, Sequence
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from typing import TYPE_CHECKING, Final, TypeAlias

from .admission import (
    CanonicalAdmissionBudget,
    PayloadAdmissionExceeded,
    PayloadAdmissionState,
)
from .envelopes import CommandEnvelope, EventEnvelope, PendingEvent, snapshot_pending_batch
from .primitives import ActorRef, AuthorityRef, ProducerRef

if TYPE_CHECKING:
    from .operation_admission import OperationAdmissionState

PROFILE_NAME: Final[str] = "MENTAURY_CANONICAL_JSON_V1"
SAFE_INTEGER_MAX: Final[int] = (1 << 53) - 1
SAFE_INTEGER_MIN: Final[int] = -SAFE_INTEGER_MAX
_TIMESTAMP_RE: Final[re.Pattern[str]] = re.compile(
    r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}"
    r"(?:\.\d{1,6})?(?:Z|[+-]\d{2}:\d{2})$"
)

CanonicalScalar: TypeAlias = str | int | bool | None
CanonicalValue: TypeAlias = (
    CanonicalScalar | list["CanonicalValue"] | dict[str, "CanonicalValue"]
)


class CanonicalJSONError(ValueError):
    """Raised when a value cannot enter MENTAURY_CANONICAL_JSON_V1."""


def _unsafe_integer_error(path: str, value: int) -> CanonicalJSONError:
    """Error for an out-of-range integer without ever formatting a huge value.

    ``str(int)`` raises ``ValueError`` beyond Python's digit-conversion limit,
    which would escape as an uncontrolled error. Values that fit in 64 bits keep
    the historical message; larger ones omit the value.
    """

    if value.bit_length() <= 64:
        return CanonicalJSONError(f"integer outside safe range at {path}: {value}")
    return CanonicalJSONError(f"integer outside safe range at {path}")


def _validate_unicode_scalar_text(value: str, path: str) -> str:
    for character in value:
        code_point = ord(character)
        if 0xD800 <= code_point <= 0xDFFF:
            raise CanonicalJSONError(f"lone surrogate is forbidden at {path}")
    return value


def _prepare(value: object, path: str, active: set[int]) -> CanonicalValue:
    if value is None or isinstance(value, bool):
        return value
    if isinstance(value, int):
        if value < SAFE_INTEGER_MIN or value > SAFE_INTEGER_MAX:
            raise _unsafe_integer_error(path, value)
        return value
    if isinstance(value, float):
        raise CanonicalJSONError(f"float is forbidden at {path}")
    if isinstance(value, Decimal):
        raise CanonicalJSONError(
            f"Decimal is forbidden at {path}; encode it explicitly as a canonical string"
        )
    if isinstance(value, str):
        return _validate_unicode_scalar_text(value, path)
    if isinstance(value, Mapping):
        identity = id(value)
        if identity in active:
            raise CanonicalJSONError(f"cyclic mapping is forbidden at {path}")
        active.add(identity)
        try:
            prepared: dict[str, CanonicalValue] = {}
            for key, item in value.items():
                if not isinstance(key, str):
                    raise CanonicalJSONError(
                        f"object key must be a string at {path}"
                    )
                safe_key = _validate_unicode_scalar_text(key, f"{path}.<key>")
                if safe_key in prepared:
                    raise CanonicalJSONError(f"duplicate object key at {path}: {safe_key}")
                prepared[safe_key] = _prepare(item, f"{path}.{safe_key}", active)
            return prepared
        finally:
            active.remove(identity)
    if isinstance(value, Sequence) and not isinstance(
        value, (str, bytes, bytearray, memoryview)
    ):
        identity = id(value)
        if identity in active:
            raise CanonicalJSONError(f"cyclic sequence is forbidden at {path}")
        active.add(identity)
        try:
            return [
                _prepare(item, f"{path}[{index}]", active)
                for index, item in enumerate(value)
            ]
        finally:
            active.remove(identity)
    raise CanonicalJSONError(
        f"unsupported canonical JSON type at {path}: {type(value).__name__}"
    )


def canonical_json_text(
    value: object,
    budget: CanonicalAdmissionBudget | None = None,
) -> str:
    """Serialize one portable value tree without insignificant whitespace.

    Without ``budget`` the original unbounded path runs (unchanged). With an
    explicit ``CanonicalAdmissionBudget`` the bounded iterative path runs; its
    output is byte-identical to the unbounded path for every value both accept.
    """

    if budget is not None:
        return _canonical_text_bounded(value, budget)
    prepared = _prepare(value, "$", set())
    return json.dumps(
        prepared,
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    )


def canonical_json_bytes(
    value: object,
    budget: CanonicalAdmissionBudget | None = None,
) -> bytes:
    """Return the canonical UTF-8 byte representation."""

    return canonical_json_text(value, budget).encode("utf-8")


class _CFrame:
    __slots__ = ("container", "iterator", "is_mapping", "out", "identity", "key", "seen")

    def __init__(
        self,
        container: object,
        iterator: object,
        is_mapping: bool,
        identity: int,
    ) -> None:
        # Strong reference keeps ``container`` (and so its id()) alive until
        # the frame completes.
        self.container = container
        self.iterator = iterator
        self.is_mapping = is_mapping
        self.out: dict[str, CanonicalValue] | list[CanonicalValue] = (
            {} if is_mapping else []
        )
        self.identity = identity
        self.key = ""
        self.seen = 0


def _path_of(stack: Sequence[_CFrame]) -> str:
    path = "$"
    for frame in stack:
        path += f".{frame.key}" if frame.is_mapping else f"[{len(frame.out)}]"
    return path


def _scalar_text(value: CanonicalValue) -> str:
    if value is None:
        return "null"
    if value is True:
        return "true"
    if value is False:
        return "false"
    if isinstance(value, int):
        return str(value)
    return json.dumps(value, ensure_ascii=False)


def _exact_str(value: str) -> str:
    """Exact ``str`` copy so subclass overrides cannot influence content."""

    return str.__getitem__(value, slice(None))


_STRING_CHUNK: Final[int] = 256  # implementation chunk size for metering, not a limit


def _meter_json_string(text: str, path: str, meter: "_ByteMeter") -> None:
    """Validate ``text`` and meter its exact JSON size incrementally.

    ``text`` must already be an exact ``str``. The size covers the two quotes
    plus every escape and UTF-8 byte. It is accumulated chunk by chunk, so a
    value that exceeds the output budget is rejected after at most one chunk
    beyond the limit and is never serialized or encoded as a whole.
    """

    meter.add(2)  # opening and closing quote
    for start in range(0, str.__len__(text), _STRING_CHUNK):
        chunk = text[start : start + _STRING_CHUNK]
        _validate_unicode_scalar_text(chunk, path)
        meter.add(len(json.dumps(chunk, ensure_ascii=False).encode("utf-8")) - 2)


class _ByteMeter:
    __slots__ = ("limit", "total")

    def __init__(self, limit: int) -> None:
        self.limit = limit
        self.total = 0

    def add(self, size: int) -> None:
        # ``total`` is only ever bytes that were admitted; a refused increment
        # is reported through ``observed`` but never counted as spend.
        if self.total + size > self.limit:
            raise PayloadAdmissionExceeded(
                "output_bytes", self.limit, self.total + size
            )
        self.total += size


def _canonical_text_bounded(
    value: object,
    budget: CanonicalAdmissionBudget,
) -> str:
    return _canonical_bounded(value, budget)[0]


def _canonical_bounded(
    value: object,
    budget: CanonicalAdmissionBudget,
    state: PayloadAdmissionState | None = None,
    meter: _ByteMeter | None = None,
) -> tuple[str, int, CanonicalValue]:
    """Bounded canonical text, nodes visited and the trusted prepared snapshot.

    The prepared snapshot is the detached, validated copy (exact ``str``/``int``,
    plain ``dict``/``list``, duplicate keys rejected) from which the text is
    rendered, so anything validated afterwards is exactly what is serialized.
    A caller that needs the spend even when the call fails passes its own
    ``state``/``meter``; otherwise fresh per-call ones are used.
    """

    if not isinstance(budget, CanonicalAdmissionBudget):
        raise TypeError("budget must be a CanonicalAdmissionBudget")
    spend = state if state is not None else PayloadAdmissionState(budget.payload)
    used = meter if meter is not None else _ByteMeter(budget.max_output_bytes)
    prepared = _prepare_bounded(value, spend, used)
    return _emit_bounded(prepared), spend.nodes_visited, prepared


def _prepare_bounded(
    value: object,
    state: PayloadAdmissionState,
    meter: _ByteMeter,
) -> CanonicalValue:
    """Validate, account and copy ``value`` iteratively (no recursion)."""

    active: set[int] = set()
    stack: list[_CFrame] = []
    to_visit: object = value
    while True:
        state.charge_node()
        path = _path_of(stack)
        produced: CanonicalValue
        scalar = True
        if to_visit is None or isinstance(to_visit, bool):
            produced = to_visit
        elif isinstance(to_visit, int):
            number = int.__index__(to_visit)
            if number < SAFE_INTEGER_MIN or number > SAFE_INTEGER_MAX:
                raise _unsafe_integer_error(path, number)
            produced = number
        elif isinstance(to_visit, float):
            raise CanonicalJSONError(f"float is forbidden at {path}")
        elif isinstance(to_visit, Decimal):
            raise CanonicalJSONError(
                f"Decimal is forbidden at {path}; encode it explicitly as a canonical string"
            )
        elif isinstance(to_visit, str):
            state.check_string(to_visit)
            produced = _exact_str(to_visit)
            _meter_json_string(produced, path, meter)  # validates + meters in chunks
        elif isinstance(to_visit, Mapping) or (
            isinstance(to_visit, Sequence)
            and not isinstance(to_visit, (bytes, bytearray, memoryview))
        ):
            scalar = False
        else:
            raise CanonicalJSONError(
                f"unsupported canonical JSON type at {path}: {type(to_visit).__name__}"
            )

        if scalar:
            if not isinstance(produced, str):  # strings were metered incrementally
                meter.add(len(_scalar_text(produced).encode("utf-8")))
            # a child of an open container: separators are metered on delivery
        else:
            state.check_depth(len(stack) + 1)
            identity = id(to_visit)
            kind = "mapping" if isinstance(to_visit, Mapping) else "sequence"
            if identity in active:
                raise CanonicalJSONError(f"cyclic {kind} is forbidden at {path}")
            active.add(identity)
            if isinstance(to_visit, Mapping):
                frame = _CFrame(to_visit, iter(to_visit.items()), True, identity)
            else:
                assert isinstance(to_visit, Sequence)  # narrowed by the branch above
                frame = _CFrame(to_visit, iter(to_visit), False, identity)
            stack.append(frame)
            meter.add(2)  # "{}" or "[]"
            has_child, child = _advance_bounded(frame, state, meter, stack)
            if has_child:
                to_visit = child
                continue
            stack.pop()
            active.discard(frame.identity)
            produced = frame.out

        while True:
            if not stack:
                return produced
            frame = stack[-1]
            if frame.is_mapping:
                assert isinstance(frame.out, dict)
                frame.out[frame.key] = produced
            else:
                assert isinstance(frame.out, list)
                frame.out.append(produced)
            has_child, child = _advance_bounded(frame, state, meter, stack)
            if not has_child:
                stack.pop()
                active.discard(frame.identity)
                produced = frame.out
                continue
            to_visit = child
            break


def _advance_bounded(
    frame: _CFrame,
    state: PayloadAdmissionState,
    meter: _ByteMeter,
    stack: list[_CFrame],
) -> tuple[bool, object]:
    """Next child as ``(has_child, child)``; meters separators and keys."""

    try:
        item = next(frame.iterator)  # type: ignore[call-overload]
    except StopIteration:
        return False, None
    if frame.seen:
        meter.add(1)  # comma
    frame.seen += 1
    if frame.is_mapping:
        key, child = item
        path = _path_of(stack[:-1])  # the mapping's own path, as in the original
        if not isinstance(key, str):
            raise CanonicalJSONError(f"object key must be a string at {path}")
        state.charge_node()
        state.check_key(key)
        safe_key = _exact_str(key)
        _meter_json_string(safe_key, f"{path}.<key>", meter)  # validates + meters
        assert isinstance(frame.out, dict)
        if safe_key in frame.out:
            raise CanonicalJSONError(f"duplicate object key at {path}: {safe_key}")
        frame.key = safe_key
        meter.add(1)  # colon
        return True, child
    return True, item


def _emit_bounded(prepared: CanonicalValue) -> str:
    """Iteratively render a prepared tree exactly like ``json.dumps``."""

    pieces: list[str] = []
    stack: list[tuple[object, object, bool]] = []  # (iterator, source, is_dict)
    firsts: list[bool] = []
    to_emit: CanonicalValue = prepared
    while True:
        if isinstance(to_emit, dict):
            pieces.append("{")
            stack.append((iter(sorted(to_emit)), to_emit, True))
            firsts.append(True)
        elif isinstance(to_emit, list):
            pieces.append("[")
            stack.append((iter(to_emit), to_emit, False))
            firsts.append(True)
        else:
            pieces.append(_scalar_text(to_emit))
        while True:
            if not stack:
                return "".join(pieces)
            iterator, source, is_dict = stack[-1]
            try:
                nxt = next(iterator)  # type: ignore[call-overload]
            except StopIteration:
                pieces.append("}" if is_dict else "]")
                stack.pop()
                firsts.pop()
                continue
            if not firsts[-1]:
                pieces.append(",")
            firsts[-1] = False
            if is_dict:
                pieces.append(json.dumps(nxt, ensure_ascii=False) + ":")
                to_emit = source[nxt]  # type: ignore[index]
            else:
                to_emit = nxt
            break


def _plain_notation_length(value: Decimal) -> int:
    """Exact length of ``format(value, "f")`` for a finite non-zero Decimal.

    Computed from sign, digit count and exponent only, so no large string is
    built. With ``n`` coefficient digits and exponent ``e``:

    * ``e >= 0``: ``n + e`` characters (digits followed by ``e`` zeros);
    * ``e < 0``: integer part ``max(n + e, 1)`` characters ("0" when the value
      is below one), a decimal point, and ``-e`` fractional digits.

    A leading ``-`` adds one character; a positive value has no sign.
    """

    sign, digits, exponent = value.as_tuple()
    assert isinstance(exponent, int)  # finite
    count = len(digits)
    if exponent >= 0:
        length = count + exponent
    else:
        length = max(count + exponent, 1) + 1 + (-exponent)
    return length + (1 if sign else 0)


def canonical_decimal_string(
    value: Decimal | str,
    max_rendered_chars: int | None = None,
) -> str:
    """Normalize a finite decimal to a schema-controlled JSON string value.

    Decimal objects are never serialized implicitly because JSON numbers cannot
    preserve decimal intent across runtimes. Callers must store the returned
    string in a field whose schema declares decimal-string semantics.

    ``max_rendered_chars`` is an explicit, opt-in admission bound (no default).
    It limits the input text length and the exact *pre-normalization*
    plain-notation length (sign, integer and fractional digits, point; i.e.
    ``len(format(value, "f"))``), which is computed arithmetically before the
    potentially huge ``format(..., "f")`` string is built. Exceeding it raises
    ``PayloadAdmissionExceeded("decimal_chars", ...)``.
    """

    if max_rendered_chars is not None and (
        isinstance(max_rendered_chars, bool)
        or not isinstance(max_rendered_chars, int)
        or max_rendered_chars < 1
    ):
        raise ValueError("max_rendered_chars must be a positive integer")
    if max_rendered_chars is not None:
        # Trusted representation: subclasses may override as_tuple(),
        # is_finite(), is_zero(), __format__() or str methods. Decimal(x) copies
        # the numeric value of any Decimal exactly without calling them, and an
        # exact str copy cannot change behavior either.
        if isinstance(value, Decimal):
            value = Decimal(value)
        elif isinstance(value, str):
            value = _exact_str(value)
    if isinstance(value, str):
        if max_rendered_chars is not None and str.__len__(value) > max_rendered_chars:
            raise PayloadAdmissionExceeded(
                "decimal_chars", max_rendered_chars, str.__len__(value)
            )
        if not value or value != value.strip():
            raise CanonicalJSONError("decimal text must be non-empty and unpadded")
        try:
            decimal_value = Decimal(value)
        except InvalidOperation as exc:
            raise CanonicalJSONError("invalid decimal text") from exc
    elif isinstance(value, Decimal):
        decimal_value = value
    else:
        raise TypeError("value must be Decimal or str")

    if not decimal_value.is_finite():
        raise CanonicalJSONError("decimal must be finite")
    if decimal_value.is_zero():
        return "0"
    if max_rendered_chars is not None:
        plain_length = _plain_notation_length(decimal_value)
        if plain_length > max_rendered_chars:
            raise PayloadAdmissionExceeded(
                "decimal_chars", max_rendered_chars, plain_length
            )

    rendered = format(decimal_value, "f")
    if "." in rendered:
        rendered = rendered.rstrip("0").rstrip(".")
    if rendered.startswith("."):
        rendered = f"0{rendered}"
    elif rendered.startswith("-."):
        rendered = rendered.replace("-.", "-0.", 1)
    return rendered


def canonical_timestamp(value: datetime | str) -> str:
    """Normalize an RFC 3339 timestamp to UTC with millisecond precision.

    Canonical output has either no fractional part or exactly three digits.
    Inputs carrying sub-millisecond precision are rejected rather than rounded.
    """

    if isinstance(value, str):
        _validate_unicode_scalar_text(value, "timestamp")
        if not _TIMESTAMP_RE.fullmatch(value):
            raise CanonicalJSONError("timestamp must be strict RFC 3339")
        if value.endswith("-00:00"):
            raise CanonicalJSONError("timestamp offset -00:00 is ambiguous")
        parse_value = value[:-1] + "+00:00" if value.endswith("Z") else value
        try:
            parsed = datetime.fromisoformat(parse_value)
        except ValueError as exc:
            raise CanonicalJSONError("timestamp is not a valid calendar instant") from exc
    elif isinstance(value, datetime):
        parsed = value
    else:
        raise TypeError("timestamp must be datetime or str")

    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise CanonicalJSONError("timestamp must include a UTC offset")
    offset = parsed.utcoffset()
    assert offset is not None
    if offset.total_seconds() % 60:
        raise CanonicalJSONError("timestamp offset must use whole minutes")

    utc_value = parsed.astimezone(timezone.utc)
    if utc_value.microsecond % 1000:
        raise CanonicalJSONError("timestamp precision finer than milliseconds is forbidden")

    prefix = (
        f"{utc_value.year:04d}-{utc_value.month:02d}-{utc_value.day:02d}T"
        f"{utc_value.hour:02d}:{utc_value.minute:02d}:{utc_value.second:02d}"
    )
    if utc_value.microsecond:
        return f"{prefix}.{utc_value.microsecond // 1000:03d}Z"
    return f"{prefix}Z"


def actor_ref_value(value: ActorRef) -> dict[str, CanonicalValue]:
    if not isinstance(value, ActorRef):
        raise TypeError("value must be an ActorRef")
    return {"type": value.actor_type, "id": value.actor_id}


def authority_ref_value(value: AuthorityRef) -> dict[str, CanonicalValue]:
    if not isinstance(value, AuthorityRef):
        raise TypeError("value must be an AuthorityRef")
    return {
        "capability_lease_id": value.capability_lease_id,
        "capability_revision": value.capability_revision,
    }


def producer_ref_value(value: ProducerRef) -> dict[str, CanonicalValue]:
    if not isinstance(value, ProducerRef):
        raise TypeError("value must be a ProducerRef")
    return {"component": value.component, "version": value.version}


def _command_document(command: CommandEnvelope, payload: object) -> dict[str, object]:
    return {
        "command_id": command.command_id,
        "command_type": command.command_type,
        "command_schema": command.command_schema,
        "target_stream": command.target_stream,
        "expected_stream_version": command.expected_stream_version,
        "issued_at": canonical_timestamp(command.issued_at),
        "issuer": actor_ref_value(command.issuer),
        "authority": authority_ref_value(command.authority),
        "correlation_id": command.correlation_id,
        "idempotency_key": command.idempotency_key,
        "payload": payload,
    }


def command_envelope_value(command: CommandEnvelope) -> dict[str, CanonicalValue]:
    if not isinstance(command, CommandEnvelope):
        raise TypeError("command must be a CommandEnvelope")
    return _command_document(  # type: ignore[return-value]
        command, _prepare(command.payload, "$.payload", set())
    )


def _pending_document(event: PendingEvent, payload: object) -> dict[str, object]:
    return {
        "event_type": event.event_type,
        "payload_schema": event.payload_schema,
        "affects_domain_state": event.affects_domain_state,
        "payload": payload,
    }


def pending_event_value(event: PendingEvent) -> dict[str, CanonicalValue]:
    if not isinstance(event, PendingEvent):
        raise TypeError("event must be a PendingEvent")
    return _pending_document(  # type: ignore[return-value]
        event, _prepare(event.payload, "$.payload", set())
    )


def pending_batch_value(events: Iterable[PendingEvent]) -> list[CanonicalValue]:
    return [pending_event_value(event) for event in snapshot_pending_batch(events)]


def event_envelope_value(
    event: EventEnvelope, *, include_event_hash: bool = True
) -> dict[str, CanonicalValue]:
    if not isinstance(event, EventEnvelope):
        raise TypeError("event must be an EventEnvelope")
    value: dict[str, CanonicalValue] = {
        "event_id": event.event_id,
        "event_type": event.event_type,
        "envelope_schema_version": event.envelope_schema_version,
        "payload_schema": event.payload_schema,
        "stream_id": event.stream_id,
        "stream_version": event.stream_version,
        "batch_id": event.batch_id,
        "batch_index": event.batch_index,
        "batch_size": event.batch_size,
        "occurred_at": canonical_timestamp(event.occurred_at),
        "recorded_at": canonical_timestamp(event.recorded_at),
        "producer": producer_ref_value(event.producer),
        "initiator": actor_ref_value(event.initiator),
        "authority": authority_ref_value(event.authority),
        "causation_id": event.causation_id,
        "correlation_id": event.correlation_id,
        "affects_domain_state": event.affects_domain_state,
        "payload_digest": event.payload_digest,
        "payload_ref": event.payload_ref,
        "previous_hash": event.previous_hash,
    }
    if include_event_hash:
        value["event_hash"] = event.event_hash
    return value


def event_hash_input_value(event: EventEnvelope) -> dict[str, CanonicalValue]:
    """Return hash-input metadata: previous_hash included, event_hash excluded."""

    value = event_envelope_value(event, include_event_hash=False)
    if "previous_hash" not in value:  # pragma: no cover - invariant guard
        raise AssertionError("previous_hash must be part of event hash input")
    return value


def canonical_command_bytes(
    command: CommandEnvelope,
    admission: OperationAdmissionState | None = None,
) -> bytes:
    """Canonical command bytes; with ``admission`` the bounded path is used.

    Bounded mode enforces the per-payload limits on the command payload and the
    aggregate limits on the whole document; the bytes are identical.
    """

    if admission is None:
        return canonical_json_bytes(command_envelope_value(command))
    if not isinstance(command, CommandEnvelope):
        raise TypeError("command must be a CommandEnvelope")
    return admission.canonical_document_with_payloads(
        lambda snapshots: _command_document(command, snapshots[0]),
        payloads=(command.payload,),
    )


def canonical_pending_batch_bytes(
    events: Iterable[PendingEvent],
    admission: OperationAdmissionState | None = None,
) -> bytes:
    if admission is None:
        return canonical_json_bytes(pending_batch_value(events))
    batch = snapshot_pending_batch(events, admission)
    return admission.canonical_document_with_payloads(
        lambda snapshots: [
            _pending_document(event, snapshot)
            for event, snapshot in zip(batch, snapshots, strict=True)
        ],
        payloads=tuple(event.payload for event in batch),
    )


def canonical_event_bytes(
    event: EventEnvelope,
    admission: OperationAdmissionState | None = None,
) -> bytes:
    if admission is None:
        return canonical_json_bytes(event_envelope_value(event))
    return admission.canonical_document(event_envelope_value(event))


def canonical_event_hash_input_bytes(
    event: EventEnvelope,
    admission: OperationAdmissionState | None = None,
) -> bytes:
    """Hash-projection bytes; with ``admission`` it is bounded and charged."""

    if admission is None:
        return canonical_json_bytes(event_hash_input_value(event))
    return admission.canonical_document(event_hash_input_value(event))
