"""Immutable fail-closed event/schema registry."""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from dataclasses import dataclass, field
from types import MappingProxyType

from mentaury.contracts import EventEnvelope, PendingEvent

from .issues import SchemaValidationError, ValidationCode, ValidationIssue
from .specs import ObjectSpec
from .validator import validate_value


@dataclass(frozen=True, slots=True)
class EventSchemaDefinition:
    event_type: str
    payload_schema: str
    payload: ObjectSpec
    affects_domain_state: bool
    envelope_versions: frozenset[int] = field(
        default_factory=lambda: frozenset({1})
    )

    def __post_init__(self) -> None:
        for field_name, value in (
            ("event_type", self.event_type),
            ("payload_schema", self.payload_schema),
        ):
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{field_name} must be a non-blank string")
        if not isinstance(self.payload, ObjectSpec):
            raise TypeError("payload must be an ObjectSpec")
        if not isinstance(self.affects_domain_state, bool):
            raise TypeError("affects_domain_state must be boolean")
        versions = frozenset(self.envelope_versions)
        if not versions or any(
            isinstance(version, bool)
            or not isinstance(version, int)
            or version < 1
            for version in versions
        ):
            raise ValueError(
                "envelope_versions must contain positive integers"
            )
        object.__setattr__(self, "envelope_versions", versions)


class SchemaRegistry:
    """Immutable event-type registry with fail-closed lookups."""

    def __init__(
        self, definitions: Iterable[EventSchemaDefinition]
    ) -> None:
        by_type: dict[str, EventSchemaDefinition] = {}
        for definition in definitions:
            if not isinstance(definition, EventSchemaDefinition):
                raise TypeError(
                    "registry entries must be EventSchemaDefinition"
                )
            if definition.event_type in by_type:
                raise ValueError(
                    f"duplicate event type: {definition.event_type}"
                )
            by_type[definition.event_type] = definition
        if not by_type:
            raise ValueError("schema registry cannot be empty")
        self._by_type = MappingProxyType(by_type)

    @property
    def event_types(self) -> frozenset[str]:
        return frozenset(self._by_type)

    def definition_for(
        self, event_type: str
    ) -> EventSchemaDefinition | None:
        return self._by_type.get(event_type)

    def validate_pending_event(
        self, event: PendingEvent
    ) -> tuple[ValidationIssue, ...]:
        if not isinstance(event, PendingEvent):
            raise TypeError("event must be a PendingEvent")
        definition, issues = self._identity_issues(
            event.event_type,
            event.payload_schema,
            event.affects_domain_state,
            None,
        )
        if definition is not None:
            issues.extend(validate_value(event.payload, definition.payload))
        return tuple(issues)

    def require_pending_event(self, event: PendingEvent) -> None:
        self._require(self.validate_pending_event(event))

    def validate_event_envelope(
        self, event: EventEnvelope
    ) -> tuple[ValidationIssue, ...]:
        if not isinstance(event, EventEnvelope):
            raise TypeError("event must be an EventEnvelope")
        _, issues = self._identity_issues(
            event.event_type,
            event.payload_schema,
            event.affects_domain_state,
            event.envelope_schema_version,
        )
        return tuple(issues)

    def require_event_envelope(self, event: EventEnvelope) -> None:
        self._require(self.validate_event_envelope(event))

    def validate_event_payload(
        self,
        event: EventEnvelope,
        payload: Mapping[str, object],
    ) -> tuple[ValidationIssue, ...]:
        if not isinstance(event, EventEnvelope):
            raise TypeError("event must be an EventEnvelope")
        definition, issues = self._identity_issues(
            event.event_type,
            event.payload_schema,
            event.affects_domain_state,
            event.envelope_schema_version,
        )
        if definition is not None:
            issues.extend(validate_value(payload, definition.payload))
        return tuple(issues)

    def require_event_payload(
        self,
        event: EventEnvelope,
        payload: Mapping[str, object],
    ) -> None:
        self._require(self.validate_event_payload(event, payload))

    @staticmethod
    def _require(issues: tuple[ValidationIssue, ...]) -> None:
        if issues:
            raise SchemaValidationError(issues)

    def _identity_issues(
        self,
        event_type: str,
        payload_schema: str,
        affects_domain_state: bool,
        envelope_version: int | None,
    ) -> tuple[EventSchemaDefinition | None, list[ValidationIssue]]:
        definition = self.definition_for(event_type)
        if definition is None:
            return None, [
                ValidationIssue(
                    ValidationCode.UNKNOWN_EVENT_TYPE,
                    "$.event_type",
                    f"event type is not registered: {event_type}",
                )
            ]
        issues: list[ValidationIssue] = []
        if payload_schema != definition.payload_schema:
            issues.append(
                ValidationIssue(
                    ValidationCode.EVENT_SCHEMA_MISMATCH,
                    "$.payload_schema",
                    f"expected {definition.payload_schema}, got {payload_schema}",
                )
            )
        if affects_domain_state is not definition.affects_domain_state:
            issues.append(
                ValidationIssue(
                    ValidationCode.AFFECTS_DOMAIN_STATE_MISMATCH,
                    "$.affects_domain_state",
                    f"expected {definition.affects_domain_state}",
                )
            )
        if (
            envelope_version is not None
            and envelope_version not in definition.envelope_versions
        ):
            issues.append(
                ValidationIssue(
                    ValidationCode.UNSUPPORTED_ENVELOPE_VERSION,
                    "$.envelope_schema_version",
                    f"unsupported envelope version: {envelope_version}",
                )
            )
        return definition, issues
