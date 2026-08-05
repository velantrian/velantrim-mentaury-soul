from __future__ import annotations

import pytest

from mentaury.storage import ResourceBudgetExceeded, VerificationBudget


def test_budget_requires_positive_explicit_limits() -> None:
    with pytest.raises(ValueError, match="max_events"):
        VerificationBudget(0, 10, 10)
    with pytest.raises(ValueError, match="max_payload_bytes"):
        VerificationBudget(1, 0, 10)
    with pytest.raises(ValueError, match="max_total_payload_bytes"):
        VerificationBudget(1, 10, 0)
    with pytest.raises(ValueError, match=">= max_payload_bytes"):
        VerificationBudget(1, 11, 10)


def test_budget_rejects_boolean_limits() -> None:
    with pytest.raises(ValueError, match="max_events"):
        VerificationBudget(True, 10, 10)


def test_budget_dimension_is_reported_without_hidden_default() -> None:
    budget = VerificationBudget(2, 8, 12)

    with pytest.raises(ResourceBudgetExceeded) as captured:
        budget.require_total_payload_size(13)

    assert captured.value.dimension == "total_payload_bytes"
    assert captured.value.limit == 12
    assert captured.value.observed == 13
    assert "RESOURCE_BUDGET_EXCEEDED" in str(captured.value)
