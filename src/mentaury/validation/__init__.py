"""Fail-closed P0 structural validation contracts."""

from .issues import SchemaValidationError, ValidationCode, ValidationIssue
from .registry import EventSchemaDefinition, SchemaRegistry
from .specs import (
    SHA256_DIGEST_PATTERN,
    ArraySpec,
    BooleanSpec,
    IntegerSpec,
    NullSpec,
    ObjectSpec,
    OneOfSpec,
    StringSpec,
    sha256_digest_spec,
)

__all__ = [
    "SHA256_DIGEST_PATTERN",
    "ArraySpec",
    "BooleanSpec",
    "EventSchemaDefinition",
    "IntegerSpec",
    "NullSpec",
    "ObjectSpec",
    "OneOfSpec",
    "SchemaRegistry",
    "SchemaValidationError",
    "StringSpec",
    "ValidationCode",
    "ValidationIssue",
    "sha256_digest_spec",
]
