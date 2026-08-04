"""Stable fail-closed validation issue contracts."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class ValidationCode(StrEnum):
    UNKNOWN_EVENT_TYPE = "UNKNOWN_EVENT_TYPE"
    EVENT_SCHEMA_MISMATCH = "EVENT_SCHEMA_MISMATCH"
    UNSUPPORTED_ENVELOPE_VERSION = "UNSUPPORTED_ENVELOPE_VERSION"
    AFFECTS_DOMAIN_STATE_MISMATCH = "AFFECTS_DOMAIN_STATE_MISMATCH"
    MISSING_REQUIRED_FIELD = "MISSING_REQUIRED_FIELD"
    FORBIDDEN_FIELD = "FORBIDDEN_FIELD"
    TYPE_MISMATCH = "TYPE_MISMATCH"
    UNSUPPORTED_NUMERIC = "UNSUPPORTED_NUMERIC"
    UNSUPPORTED_VALUE = "UNSUPPORTED_VALUE"
    INVALID_UNICODE = "INVALID_UNICODE"
    NON_STRING_OBJECT_KEY = "NON_STRING_OBJECT_KEY"
    CYCLIC_VALUE = "CYCLIC_VALUE"
    ARRAY_TOO_SHORT = "ARRAY_TOO_SHORT"
    STRING_TOO_SHORT = "STRING_TOO_SHORT"


@dataclass(frozen=True, slots=True)
class ValidationIssue:
    code: ValidationCode
    path: str
    message: str


class SchemaValidationError(ValueError):
    """Raised when fail-closed validation finds one or more issues."""

    def __init__(self, issues: tuple[ValidationIssue, ...]) -> None:
        if not issues:
            raise ValueError("SchemaValidationError requires at least one issue")
        self.issues = issues
        summary = "; ".join(
            f"{issue.code}@{issue.path}: {issue.message}" for issue in issues
        )
        super().__init__(summary)
