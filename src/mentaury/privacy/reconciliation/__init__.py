"""Public API for the pure P1-002 privacy reconciliation classifier."""

from .classifier import classify_privacy_reconciliation
from .contracts import (
    CLASSIFIER_CONTRACT_VERSION,
    CopyState,
    MaterialState,
    PrivacyAccessIntent,
    PrivacyClass,
    PrivacyContractError,
    PrivacyCopy,
    PrivacyDecision,
    PrivacyMaterial,
    PrivacyReason,
    PrivacyReconciliationBudget,
    PrivacyReconciliationResult,
    SurfaceKind,
)

__all__ = [
    "CLASSIFIER_CONTRACT_VERSION",
    "CopyState",
    "MaterialState",
    "PrivacyAccessIntent",
    "PrivacyClass",
    "PrivacyContractError",
    "PrivacyCopy",
    "PrivacyDecision",
    "PrivacyMaterial",
    "PrivacyReason",
    "PrivacyReconciliationBudget",
    "PrivacyReconciliationResult",
    "SurfaceKind",
    "classify_privacy_reconciliation",
]
