"""Bounded capability-authority contracts.

Importing this package performs no network, database, filesystem, clock,
registry, tool, event, identity, or M3 operation.
"""

from .lease import (
    ActionIntent,
    CapabilityLeaseRecord,
    GrantedBy,
    LeaseStatus,
    REGISTRY_SCHEMA_VERSION,
    RESOLVER_CONTRACT_VERSION,
    RegistryAvailability,
    RegistrySnapshot,
    ResolutionBudget,
    ResolutionDecision,
    ResolutionReason,
    ResolutionResult,
    ScopeItem,
    capability_lease_digest,
    resolve_capability_lease,
)

__all__ = [
    "ActionIntent",
    "CapabilityLeaseRecord",
    "GrantedBy",
    "LeaseStatus",
    "REGISTRY_SCHEMA_VERSION",
    "RESOLVER_CONTRACT_VERSION",
    "RegistryAvailability",
    "RegistrySnapshot",
    "ResolutionBudget",
    "ResolutionDecision",
    "ResolutionReason",
    "ResolutionResult",
    "ScopeItem",
    "capability_lease_digest",
    "resolve_capability_lease",
]
