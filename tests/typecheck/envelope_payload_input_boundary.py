"""Focused static check: вход конструктора P0-002 vs хранимый FrozenPayload."""

from mentaury.contracts import ActorRef, AuthorityRef, CommandEnvelope, PendingEvent
from mentaury.contracts.primitives import FrozenPayload


def _actor() -> ActorRef:
    return ActorRef(actor_type="operator", actor_id="operator:primary")


def _authority() -> AuthorityRef:
    return AuthorityRef(capability_lease_id="CAP-81", capability_revision=2)


source: dict[str, object] = {
    "statement": "alpha",
    "evidence": [{"id": "E-1"}],
}
command = CommandEnvelope(
    command_id="CMD-1",
    command_type="CREATE_BELIEF",
    command_schema="create-belief/v1",
    target_stream="belief:B-204",
    expected_stream_version=0,
    issued_at="2026-08-04T22:00:00Z",
    issuer=_actor(),
    authority=_authority(),
    correlation_id="CORR-12",
    idempotency_key="create-belief:B-204:request-1",
    payload=source,
)
stored_command: FrozenPayload = command.payload

nested: dict[str, object] = {"items": [1, 2, {"k": "v"}]}
pending = PendingEvent(
    event_type="BELIEF_CREATED",
    payload_schema="belief-created/v1",
    affects_domain_state=True,
    payload=nested,
)
stored_pending: FrozenPayload = pending.payload

already_frozen = CommandEnvelope(
    command_id="CMD-2",
    command_type="CREATE_BELIEF",
    command_schema="create-belief/v1",
    target_stream="belief:B-204",
    expected_stream_version=0,
    issued_at="2026-08-04T22:00:00Z",
    issuer=_actor(),
    authority=_authority(),
    correlation_id="CORR-13",
    idempotency_key="create-belief:B-204:request-2",
    payload=stored_command,
)
stored_again: FrozenPayload = already_frozen.payload

# Отрицательный случай: не-mapping не является входом freeze_payload.
# ignore обязателен; --warn-unused-ignores упадёт, если вход расширят до Any/object.
_rejected_command = CommandEnvelope(
    command_id="CMD-BAD",
    command_type="CREATE_BELIEF",
    command_schema="create-belief/v1",
    target_stream="belief:B-204",
    expected_stream_version=0,
    issued_at="2026-08-04T22:00:00Z",
    issuer=_actor(),
    authority=_authority(),
    correlation_id="CORR-BAD",
    idempotency_key="bad",
    payload=["not-a-mapping"],  # type: ignore[arg-type]
)
_rejected_pending = PendingEvent(
    "BELIEF_CREATED",
    "belief-created/v1",
    True,
    ["not-a-mapping"],  # type: ignore[arg-type]
)
