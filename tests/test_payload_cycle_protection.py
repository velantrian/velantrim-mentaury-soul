from __future__ import annotations

import pytest

from mentaury.contracts import PendingEvent


def test_mapping_cycle_is_rejected_with_controlled_error() -> None:
    payload: dict[str, object] = {}
    payload["self"] = payload

    with pytest.raises(TypeError, match="cyclic payload container"):
        PendingEvent(
            event_type="TEST_EVENT",
            payload_schema="test-event/v1",
            affects_domain_state=True,
            payload=payload,
        )


def test_sequence_cycle_is_rejected_with_controlled_error() -> None:
    sequence: list[object] = []
    sequence.append(sequence)

    with pytest.raises(TypeError, match="cyclic payload container"):
        PendingEvent(
            event_type="TEST_EVENT",
            payload_schema="test-event/v1",
            affects_domain_state=True,
            payload={"items": sequence},
        )


def test_shared_non_cyclic_container_is_allowed() -> None:
    shared = {"value": "alpha"}
    event = PendingEvent(
        event_type="TEST_EVENT",
        payload_schema="test-event/v1",
        affects_domain_state=True,
        payload={"left": shared, "right": shared},
    )

    assert event.payload["left"] == {"value": "alpha"}
    assert event.payload["right"] == {"value": "alpha"}
