"""Recursive portable-value and structural validation."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from decimal import Decimal

from mentaury.contracts import SAFE_INTEGER_MAX, SAFE_INTEGER_MIN

from .issues import ValidationCode, ValidationIssue
from .specs import (
    ArraySpec,
    BooleanSpec,
    IntegerSpec,
    NullSpec,
    ObjectSpec,
    OneOfSpec,
    StringSpec,
    ValueSpec,
)


def validate_value(
    value: object, spec: ValueSpec, path: str = "$"
) -> tuple[ValidationIssue, ...]:
    return tuple(_validate(value, spec, path, set()))


def _validate(
    value: object,
    spec: ValueSpec,
    path: str,
    active: set[int],
) -> list[ValidationIssue]:
    portability_issue = _portable_issue(value, path)
    if portability_issue is not None:
        return [portability_issue]

    if isinstance(spec, OneOfSpec):
        options = [
            _validate(value, option, path, set(active))
            for option in spec.options
        ]
        matches = sum(not result for result in options)
        if matches == 1:
            return []
        message = (
            "value matches no allowed option"
            if matches == 0
            else "value matches more than one allowed option"
        )
        return [
            _issue(
                ValidationCode.TYPE_MISMATCH,
                path,
                message,
            )
        ]

    if isinstance(spec, StringSpec):
        if not isinstance(value, str):
            return [_type_issue(path, "string", value)]
        if len(value) < spec.min_length:
            return [
                _issue(
                    ValidationCode.STRING_TOO_SHORT,
                    path,
                    f"minimum length is {spec.min_length}",
                )
            ]
        return []

    if isinstance(spec, IntegerSpec):
        if isinstance(value, bool) or not isinstance(value, int):
            return [_type_issue(path, "integer", value)]
        issues: list[ValidationIssue] = []
        if spec.minimum is not None and value < spec.minimum:
            issues.append(
                _issue(
                    ValidationCode.TYPE_MISMATCH,
                    path,
                    f"integer must be >= {spec.minimum}",
                )
            )
        if spec.maximum is not None and value > spec.maximum:
            issues.append(
                _issue(
                    ValidationCode.TYPE_MISMATCH,
                    path,
                    f"integer must be <= {spec.maximum}",
                )
            )
        return issues

    if isinstance(spec, BooleanSpec):
        return (
            []
            if isinstance(value, bool)
            else [_type_issue(path, "boolean", value)]
        )

    if isinstance(spec, NullSpec):
        return [] if value is None else [_type_issue(path, "null", value)]

    if isinstance(spec, ArraySpec):
        if not isinstance(value, Sequence) or isinstance(
            value, (str, bytes, bytearray, memoryview)
        ):
            return [_type_issue(path, "array", value)]
        identity = id(value)
        if identity in active:
            return [
                _issue(
                    ValidationCode.CYCLIC_VALUE,
                    path,
                    "cyclic array is forbidden",
                )
            ]
        active.add(identity)
        try:
            issues: list[ValidationIssue] = []
            if len(value) < spec.min_items:
                issues.append(
                    _issue(
                        ValidationCode.ARRAY_TOO_SHORT,
                        path,
                        f"minimum item count is {spec.min_items}",
                    )
                )
            for index, item in enumerate(value):
                issues.extend(
                    _validate(item, spec.items, f"{path}[{index}]", active)
                )
            return issues
        finally:
            active.remove(identity)

    if isinstance(spec, ObjectSpec):
        if not isinstance(value, Mapping):
            return [_type_issue(path, "object", value)]
        identity = id(value)
        if identity in active:
            return [
                _issue(
                    ValidationCode.CYCLIC_VALUE,
                    path,
                    "cyclic object is forbidden",
                )
            ]
        active.add(identity)
        try:
            issues: list[ValidationIssue] = []
            string_keys = {key for key in value if isinstance(key, str)}
            for key in value:
                if not isinstance(key, str):
                    issues.append(
                        _issue(
                            ValidationCode.NON_STRING_OBJECT_KEY,
                            f"{path}.<key>",
                            "object keys must be strings",
                        )
                    )
            for required in sorted(spec.required.difference(string_keys)):
                issues.append(
                    _issue(
                        ValidationCode.MISSING_REQUIRED_FIELD,
                        f"{path}.{required}",
                        "required field is missing",
                    )
                )
            for key, item in value.items():
                if not isinstance(key, str):
                    continue
                child_spec = spec.properties.get(key)
                if child_spec is None:
                    if not spec.additional_properties:
                        issues.append(
                            _issue(
                                ValidationCode.FORBIDDEN_FIELD,
                                f"{path}.{key}",
                                "field is not declared by the strict schema",
                            )
                        )
                    continue
                issues.extend(
                    _validate(item, child_spec, f"{path}.{key}", active)
                )
            return issues
        finally:
            active.remove(identity)

    raise AssertionError(f"unhandled spec type: {type(spec).__name__}")


def _portable_issue(value: object, path: str) -> ValidationIssue | None:
    if isinstance(value, (float, Decimal)):
        return _issue(
            ValidationCode.UNSUPPORTED_NUMERIC,
            path,
            f"unsupported numeric type: {type(value).__name__}",
        )
    if isinstance(value, int) and not isinstance(value, bool):
        if value < SAFE_INTEGER_MIN or value > SAFE_INTEGER_MAX:
            return _issue(
                ValidationCode.UNSUPPORTED_NUMERIC,
                path,
                "integer is outside the canonical safe range",
            )
    if isinstance(value, str) and any(
        0xD800 <= ord(character) <= 0xDFFF for character in value
    ):
        return _issue(
            ValidationCode.INVALID_UNICODE,
            path,
            "lone surrogate is forbidden",
        )
    if isinstance(value, (bytes, bytearray, memoryview, set, frozenset)):
        return _issue(
            ValidationCode.UNSUPPORTED_VALUE,
            path,
            f"unsupported portable value type: {type(value).__name__}",
        )
    return None


def _issue(
    code: ValidationCode, path: str, message: str
) -> ValidationIssue:
    return ValidationIssue(code, path, message)


def _type_issue(
    path: str, expected: str, value: object
) -> ValidationIssue:
    return _issue(
        ValidationCode.TYPE_MISMATCH,
        path,
        f"expected {expected}, got {type(value).__name__}",
    )
