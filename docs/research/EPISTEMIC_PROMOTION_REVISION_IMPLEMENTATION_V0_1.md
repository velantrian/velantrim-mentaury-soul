# EPR-v0.1 bounded implementation note

```text
Stage: V1 2 / 5
Primitive: PURE_EPISTEMIC_CHANGE_ROUTER
Contract: EPR-v0.1
Runtime activation: NONE
Persistence authority: NONE
Belief mutation authority: NONE
Evidence Gate authority: UNCHANGED
Identity / relationship / M3 authority: NONE
Tools / retrieval / network / deployment: NONE
```

## What is implemented

`mentaury.epistemic_change.route_epistemic_change()` implements the frozen routing table in `EPISTEMIC_PROMOTION_REVISION_CONTRACT_V0_1.md`.

It accepts only an exact PCR record, an optional caller-supplied `BeliefBinding`, an explicit `EpistemicChangeRequest`, and local resource limits. It returns a deterministic `EpistemicChangePlan` naming the next owner/prerequisite.

It performs no route.

```text
route != execution
route != permission
route != belief mutation
route != Evidence Gate verdict
route != terminal successor
```

## Stage 1 relationship

CBP-v0.1 is now implemented in `main`. EPR-v0.1 nevertheless preserves the already-frozen enum literal `FUTURE_CLAIM_TO_BELIEF_BINDING` because changing the frozen EPR-v0.1 vocabulary during implementation would silently change its contract. In EPR-v0.1 this value is a routing label only; it is not an assertion that the repository still lacks CBP-v0.1 and it carries no invocation handle.

A later version may rename that label only through an explicit versioned contract change. This V1 stage does not expand scope to do so.

## Terminality

EPR does not define its own terminal status set. It delegates terminality semantics to the existing P0-014 owner exactly as frozen:

```text
terminal(status) = not belief_status_transition_allowed(status, status)
```

Thus current terminal statuses remain `SUPPORTED`, `CONTRADICTED`, and `SUPERSEDED` without widening the P0 transition map.

## Fail-closed binding

When a belief binding is supplied, all three association fields must match the PCR record:

- claim ID;
- exact `ClaimType` identity;
- PCR input fingerprint.

Mismatch raises `EpistemicChangeBindingError` and produces no plan.

## Authority boundary

The package does not import lifecycle executors, Evidence Gate code, persistence, network, retrieval, model clients, identity/relationship state, or Action Gate code. It constructs no `CommandEnvelope`, `PendingEvent`, receipt, capability, target status, or successor lineage.
