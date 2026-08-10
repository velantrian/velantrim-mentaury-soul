# 🔐 P1-003 Pure Governed Constraint Composer — Bounded Implementation Authorization Receipt

```text
Status:                       OWNER_GO · AUTHORIZED_BOUNDED · NOT_STARTED
Authorization date:           2026-08-10
Milestone:                    P1-003 Pure Governed Constraint Composer v0.1
Contract authority:           docs/research/P1_003_PURE_GOVERNED_CONSTRAINT_COMPOSER_CONTRACT.md
Contract version:             P1-003-v0.1
Binding contract version:     CROSS-GATE-BINDING-v0.1
Canonical profile:            MENTAURY_CANONICAL_JSON_V1
Status authority:             docs/CURRENT_STATUS.md
Governance:                   SOLO_MAINTAINER · TIER_A
Independent human assurance:  NOT CLAIMED
P1-003 runtime assignment:    NOT_ASSIGNED
Implementation authorization: AUTHORIZED_BOUNDED · P1-003-v0.1 ONLY
Runtime deployment:           NOT AUTHORIZED
Action Gate authority:        NONE
Retrieval authority:          NONE
Tool authority:               NONE
Identity authority:           NONE
Relationship authority:       NONE
Direct or indirect M3 write:  FORBIDDEN
Character runtime activation: BLOCKED_PENDING_REQUIRED_VALIDATION
```

> **CONTRACT FROZEN ≠ OWNER GO.**
>
> **OWNER GO ≠ IMPLEMENTATION COMPLETE.**
>
> This receipt grants exactly one bounded, consumable authorization for a later
> separate implementation milestone against the already frozen P1-003 v0.1
> contract. It does not itself implement, activate, deploy, retrieve, execute or
> mutate anything.

---

## 1. 🎯 Explicit Owner GO

The repository owner explicitly authorized the next bounded implementation
milestone for the frozen `P1-003-v0.1` Pure Governed Constraint Composer.

```text
P1_003_CONTRACT = FROZEN_DOCS
P1_003_OWNER_GO = AUTHORIZED_BOUNDED
P1_003_OWNER_GO_AUTHORIZED_BOUNDED
P1_003_IMPLEMENTATION_NOT_STARTED
IMPLEMENTATION_AUTHORIZATION = AUTHORIZED_BOUNDED · P1-003-v0.1 ONLY
```

This Owner GO is:

```text
exact-contract-bound
scope-bound
one-time / consumable
non-transferable to broader milestones
```

It may be consumed only by the next separate bounded P1-003 implementation
milestone. It does not roll forward to any later runtime, Action Gate,
retrieval, tool, identity, relationship, M3, Character or deployment milestone.

The repository has no established `ASSIGNED_BOUNDED` runtime-assignment
vocabulary. Therefore this docs-only Owner GO does not invent one and does not
claim an active runtime assignment:

```text
P1_003_RUNTIME_ASSIGNMENT = NOT_ASSIGNED
```

The future implementation milestone may implement the frozen bounded package,
but runtime activation/deployment remains a separate authority transition.

---

## 2. 🧬 Exact frozen contract binding

This authorization is valid only for:

```text
COMPOSER_CONTRACT_VERSION  = P1-003-v0.1
BINDING_CONTRACT_VERSION   = CROSS-GATE-BINDING-v0.1
CANONICAL_PROFILE          = MENTAURY_CANONICAL_JSON_V1
COMMON_REQUEST_DOMAIN      = MENTAURY_P1_003_COMMON_REQUEST_V1
EVALUATION_EVIDENCE_DOMAIN = MENTAURY_P1_003_EVALUATION_EVIDENCE_V1
P1_001_EXPECTED_VERSION    = P1-001-v0.2
P1_002_EXPECTED_VERSION    = P1-002-v0.1
```

The authoritative frozen contract remains:

`docs/research/P1_003_PURE_GOVERNED_CONSTRAINT_COMPOSER_CONTRACT.md`

This receipt does not revise or supersede that contract.

---

## 3. 📦 Exact future implementation scope

The future implementation milestone may modify only the frozen bounded package
and the tests/docs needed to prove conformance:

```text
src/mentaury/composition/__init__.py
src/mentaury/composition/governed_constraints/__init__.py
src/mentaury/composition/governed_constraints/contracts.py
src/mentaury/composition/governed_constraints/composer.py
```

The exact public API remains:

```python
def compose_governed_constraints(
    *,
    context: CrossGateEvaluationContext,
) -> GovernedConstraintResult:
    ...
```

The exact frozen context and budget schemas remain unchanged. Bare P1 results,
caller digests/fingerprints, callback injection, ambient clock authority,
repository/service inputs, tool/backend handles and hidden discovery are not
authorized.

---

## 4. 🔗 Composition and result boundary

The future implementation must derive the existing gate intents from one
`CrossGateEvaluationContext` and evaluate both bounded gates in the same
attempt.

The strongest positive result remains exactly:

```text
Capability ALLOW
+ Privacy ALLOW_REFERENCE
+ verified same-attempt binding
= at most ELIGIBLE_FOR_NEXT_GATE
```

And explicitly:

```text
ELIGIBLE_FOR_NEXT_GATE ≠ ACTION_GATE_PASS
ELIGIBLE_FOR_NEXT_GATE ≠ RETRIEVAL_PERMISSION
ELIGIBLE_FOR_NEXT_GATE ≠ TOOL_PERMISSION
ELIGIBLE_FOR_NEXT_GATE ≠ EXECUTION_PERMISSION
ELIGIBLE_FOR_NEXT_GATE ≠ IDENTITY_AUTHORITY
ELIGIBLE_FOR_NEXT_GATE ≠ RELATIONSHIP_AUTHORITY
ELIGIBLE_FOR_NEXT_GATE ≠ M3_AUTHORITY
ELIGIBLE_FOR_NEXT_GATE ≠ DEPLOYMENT_AUTHORITY
```

The exact decision vocabulary remains:

```text
ELIGIBLE_FOR_NEXT_GATE
NOT_ELIGIBLE
DEFER
```

---

## 5. 🔥 Frozen fail-closed semantics

The implementation authorization preserves the frozen precedence:

```text
binding mismatch
→ NOT_ELIGIBLE

canonicalization failure
→ NOT_ELIGIBLE

unsupported gate version
→ DEFER

composition budget exhaustion
→ DEFER

verified blocker
→ NOT_ELIGIBLE

no blocker + uncertainty/defer
→ DEFER

exact double-positive + valid binding/fingerprints
→ ELIGIBLE_FOR_NEXT_GATE
```

No implementation PR may weaken or reinterpret these semantics.

---

## 6. 🛡️ Mandatory threat, metamorphic and purity evidence

The future implementation milestone must satisfy all frozen requirements:

```text
T1…T12
M1…M10
CGC-CTX-001…012
CGC-FP-001…010
CGC-DEC-001…012
CGC-T-001…012
CGC-M-001…010
CGC-PURE-001…006
```

The implementation must also prove the frozen no-hidden-I/O boundary. It may not
use filesystem authority, `sqlite3.connect`, network/socket, subprocess,
environment as authority, ambient time, ambient randomness/UUID, persistence,
event append, retrieval adapters, tool adapters, backend discovery, plugin
discovery or a dynamic DI container.

Pure deterministic imports required by the frozen P1 contracts/resolvers,
classifier and canonical JSON helpers remain the only intended dependency
surface.

---

## 7. ⛔ Compatibility stop

If implementation requires any change to:

```text
P1-001 semantics
P1-001 result shape
P1-002 semantics
P1-002 result shape
MENTAURY_CANONICAL_JSON_V1
frozen P1-003 v0.1 semantics
```

then this authorization is insufficient.

Required disposition:

```text
STOP_CURRENT_IMPLEMENTATION
→ NEW_DOCS_ONLY_CONTRACT_REVISION
→ REVIEW
→ NEW_OWNER_DECISION
```

A compatibility tweak may not be smuggled into the implementation PR.

---

## 8. 🚫 Explicitly not authorized

```text
services
repositories
adapters
workers
transports
persistence
database integrations
network I/O
filesystem authority
retrieval execution
Action Gate
tool execution
backend discovery
plugin discovery
new DI framework
identity runtime
relationship runtime
Genesis runtime
Human Paths Atlas runtime
Character runtime activation
direct or indirect M3 write
P1-001 changes
P1-002 changes
canonical JSON changes
runtime deployment
```

The following repository boundaries remain unchanged:

```text
ACTION_GATE = NOT_AUTHORIZED
RETRIEVAL_EXECUTION = NOT_AUTHORIZED
TOOL_EXECUTION = NOT_AUTHORIZED
IDENTITY_RUNTIME = NOT_AUTHORIZED
RELATIONSHIP_RUNTIME = NOT_AUTHORIZED
DIRECT_OR_INDIRECT_M3_WRITE = FORBIDDEN
RUNTIME_DEPLOYMENT = NOT_AUTHORIZED
CHARACTER_RUNTIME_ACTIVATION_GATE = BLOCKED_PENDING_REQUIRED_VALIDATION
```

Issue #39 remains open as the future genuine independent/team-review lifecycle
trigger and is not a current solo-maintainer blocker.

---

## 9. 🎟️ Consumption rule

This Owner GO is not reusable authority.

```text
Owner GO receipt merged + resulting-main CI success
→ authorization becomes available to exactly one separate bounded implementation milestone

implementation milestone consumes the authorization
→ receipt later becomes OWNER_GO_CONSUMED only after verified implementation completion
```

The implementation milestone must start with a fresh live-state preflight and
must bind itself to this exact receipt and the frozen P1-003 v0.1 contract.

---

## 10. 🛑 Mandatory stop after this authorization milestone

This authorization PR must stop before implementation.

```text
P1_003_OWNER_GO_AUTHORIZED_BOUNDED
P1_003_IMPLEMENTATION_NOT_STARTED
NEXT_BOUNDED_MILESTONE = P1_003_PURE_GOVERNED_CONSTRAINT_COMPOSER_BOUNDED_IMPLEMENTATION
```

No `src/mentaury/composition/**` file is created by this Owner GO milestone.

Any implementation is a new strictly serialized authority milestone with a new
live preflight, separate branch/PR, exact-head Tier A evidence and resulting-main
CI.
