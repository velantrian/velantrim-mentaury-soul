"""Fail-closed P0 structural validation contracts."""

from .issues import SchemaValidationError, ValidationCode, ValidationIssue
from .registry import EventSchemaDefinition, SchemaRegistry
from .specs import (
    ArraySpec,
    BooleanSpec,
    IntegerSpec,
    NullSpec,
    ObjectSpec,
    OneOfSpec,
    StringSpec,
)

__all__ = [
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
]
