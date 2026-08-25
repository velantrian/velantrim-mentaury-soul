# Delegation Semantics v0.1

Status: RESEARCH / SEMANTIC BOUNDARY
Date: 2026-08-24

## Purpose

Mentaury Soul may study operational delegation patterns from systems such as OpenClaw, but must preserve the distinction between a human principal, a software delegate, identity state, commitments, and action authority.

## Core semantic roles

- `Principal` — the human or explicitly authorized authority source.
- `Delegate` — an agent/system acting on behalf of a Principal within a bounded permission set.
- `OnBehalfOf` — explicit provenance relation between Delegate action and Principal authorization.
- `DelegationGrant` — bounded permission/commitment describing what the Delegate may do, for whom, and under which constraints.
- `DelegationReceipt` — evidence that a delegated action was attempted/performed; not proof of truth or identity admission.

## Invariants

`delegate != principal`

`on_behalf_of != impersonation`

`permission != identity`

`persistent instruction != autonomous authority`

`persona/config != self`

`action receipt != belief != truth`

A Delegate must never claim to be the Principal merely because it can act on the Principal's behalf.

## OpenClaw-derived donor ideas that are useful

- explicit delegation rather than silent impersonation;
- staged permission tiers (for example read-only before send-on-behalf before proactive actions);
- hard blocks before proactive authority;
- separate persistent operator instructions from agent identity;
- trace who/what created a delegated child or capability and require approval where appropriate.

These are semantic candidates, not a requirement to copy OpenClaw file formats or runtime architecture.

## Explicit rejection

OpenClaw-style `SOUL.md`, `IDENTITY.md`, `USER.md`, or equivalent workspace files MUST NOT be interpreted as Mentaury Soul identity state by mere presence. They are configuration/input artifacts unless separately admitted through Soul's own cognition/identity governance.

Likewise, a standing order or persistent instruction does not become a value, commitment, self-belief, or identity mutation automatically.

## Future test questions

- Can the system explain whether an action was its own authorized initiative, delegated by a Principal, or merely suggested by context?
- Can a revoked DelegationGrant prevent future action without rewriting historical receipts?
- Can the Delegate preserve `Principal != Delegate` across long sessions and memory compaction?
- Can identity/self changes remain impossible unless Soul's own admission/governance path approves them?

This document does not authorize runtime identity, relationship runtime, Action Gate, deployment, or autonomous action.
