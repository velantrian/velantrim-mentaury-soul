# 🔗 Cross-Gate Binding & Composition Readiness

```text
Status:                       FROZEN_DOCS · DOCS_ONLY · READINESS_CONTRACT
Version:                      0.1
Date:                         2026-08-10
Review tier:                  TIER_A
Readiness result:             READY
Selected strategy:            PURE_COORDINATOR_OVER_VERIFIED_SOURCE_INPUTS
Bare-result composition:      REJECTED
Runtime authority:            NONE
Implementation authorization: NONE
P1-003 assignment:            NONE
Persistence authority:        NONE
Retrieval authority:          NONE
Tool authority:               NONE
Action authority:             NONE
Identity authority:           NONE
Direct or indirect M3 write:  FORBIDDEN
Deployment authority:         NONE
```

> **THIS PR DOES NOT AUTHORIZE IMPLEMENTATION.**
>
> **THIS PR DOES NOT AUTHORIZE RETRIEVAL, TOOL EXECUTION, ACTION EXECUTION,
> IDENTITY MUTATION, M3 WRITES, PERSISTENCE, NETWORK I/O, OR DEPLOYMENT.**
>
> This document freezes a docs-only composition-readiness contract. It does not
> assign P1-003, create an Action Gate, make `ALLOW_REFERENCE` a retrieval
> permission, or turn any positive classifier result into reusable authority.

---

## 1. 🎯 Scope and decision

The bounded question is:

> How can a future pure composer prove that Capability Lease and Privacy
> Reconciliation decisions refer to the same request/intent/context and a
> compatible freshness epoch before the decisions are composed?

The architecture decision is:

```text
CROSS_GATE_BINDING_READINESS = READY
RUNTIME_IMPLEMENTATION       = NOT_AUTHORIZED
P1_003                       = NOT_ASSIGNED
```

Readiness is possible **without modifying the frozen P1-001 or P1-002 result
contracts** if a future coordinator owns one immutable canonical evaluation
context, projects that context into the existing pure classifiers, and composes
only results produced inside that same evaluation attempt.

A composer that accepts unrelated bare gate results is not ready and is
explicitly rejected.

---

## 2. 📚 Evidence basis on current `main`

### 2.1 P1-001 source surface

The implemented `ActionIntent` contains:

```text
purpose_id
operation_id
data_scope
requested_side_effects
```

The implemented `ResolutionResult` contains:

```text
decision
primary_reason
lease_id
requested_revision
observed_live_revision
observed_status
observed_digest
evaluated_at
resolver_contract_version
```

It does **not** carry the evaluated `ActionIntent` or an independently
verifiable fingerprint of it.

The resolver is nevertheless locally strict: it checks exact purpose,
operation, typed scope, requested side effects, lease live-head revision,
canonical lease digest, lifecycle and caller-supplied evaluation time.

### 2.2 P1-002 source surface

The implemented privacy classifier receives:

```text
PrivacyMaterial
PrivacyCopy
PrivacyAccessIntent
PrivacyReconciliationBudget
```

`PrivacyAccessIntent` contains:

```text
copy_id
branch_id
purpose
```

The implemented `PrivacyReconciliationResult` contains only:

```text
decision
reason
```

The classifier locally checks material/copy linkage, branch linkage, purpose,
policy revision, privacy state and explicit budgets. Its result does not retain
that binding.

### 2.3 Confirmed composition gap

```text
Capability ALLOW evaluated for request A
+
Privacy ALLOW_REFERENCE evaluated for request B

≠ authorization for A
≠ authorization for B
≠ safe composition
```

The gap is therefore not a failure of either local classifier. It is the lack
of a common, verifiable cross-gate binding when their bare result objects are
removed from the source inputs that produced them.

---

## 3. 🧬 Canonical evaluation context

A future pure coordinator must own one immutable `CrossGateEvaluationContext`
(or semantically equivalent contract). The exact runtime type is **not**
authorized here; this section freezes the required semantics.

### 3.1 Required binding domains

| Domain | Required semantics | Classification | Rationale |
|---|---|---|---|
| Request identity | `request_id` | binding / provenance | prevents result reuse across distinct request instances; not authority by itself |
| Purpose | one exact canonical purpose identifier projected unchanged to both gates | authority-critical | prevents purpose laundering |
| Operation | exact `operation_id` | authority-critical | prevents read/write or operation substitution |
| Data scope | canonical typed scope | authority-critical | prevents scope laundering/expansion |
| Requested side effects | canonical unique ordered set | authority-critical | prevents read-only evidence from authorizing effects |
| Privacy material | exact `material_id` plus admitted material state used by the gate | authority-critical | binds privacy decision to evaluated material |
| Privacy copy | exact `copy_id` and admitted copy state/surface used by the gate | authority-critical | prevents copy/surface substitution |
| Continuity branch | exact `branch_id` | authority-critical | prevents branch substitution |
| Capability lease | lease id + requested revision | authority-critical | binds the capability check to the requested lease |
| Observed lease head | observed live revision + verified record digest | freshness-critical | detects lease supersession or record change |
| Privacy policy | material and copy policy revisions | freshness-critical | detects stale privacy evidence |
| Gate versions | P1-001 resolver version + P1-002 classifier version | verification-critical | prevents cross-version semantic reuse |
| Canonicalization | explicit canonical profile + binding-contract version | verification-critical | makes fingerprint recomputation deterministic and domain-separated |
| Evaluation time | explicit canonical `evaluated_at` | freshness/evaluation-critical | binds time-sensitive lease evaluation without ambient clock |
| Gate budgets | exact admitted budgets | evaluation-critical | budgets can alter a gate result and must be part of evaluation evidence |

### 3.2 Purpose namespace rule

P1-001 names its field `purpose_id`; P1-002 currently names its field `purpose`.
No semantic translation is authorized by this document.

A future coordinator may compose only when both projections use the **same exact
canonical purpose identifier** under an explicitly defined common namespace.

```text
semantic similarity
human label similarity
caller assertion that two purposes "mean the same thing"

≠ verified purpose binding
```

If a mapping layer is ever required, it needs its own contract and evidence. It
must not be hidden inside composition.

### 3.3 Fields that are not cross-gate authority

The following do not become authority merely because they are present in an
envelope:

```text
human-readable labels
presentation metadata
log messages
comments
caller-supplied digest strings
request display names
Character/voice state
relationship state
identity state
M3 state
```

Relationship, constitutional, identity and other Action Gate dimensions remain
separate future gates. Excluding them here is deliberate; it prevents this
bounded readiness contract from silently becoming an Action Gate.

---

## 4. 🧱 Canonical representation and fingerprints

The repository already implements `MENTAURY_CANONICAL_JSON_V1`. A future
binding contract should reuse that deterministic value profile rather than
introduce a second competing serializer.

Canonical bytes alone are not authority. The future binding object must include
an explicit version/domain before hashing, for example conceptually:

```text
binding_contract_version
canonical_profile
request_id
common_authority_request
capability_evaluation_projection
privacy_evaluation_projection
gate_contract_versions
```

The normative fingerprint property is:

```text
admit exact source values
→ construct versioned canonical binding object
→ MENTAURY_CANONICAL_JSON_V1
→ SHA-256
→ coordinator-computed fingerprint
```

The exact future field layout and API remain implementation-contract work.

### 4.1 Two useful fingerprint domains

A future design should distinguish:

1. **Common request fingerprint** — binds request instance, purpose, operation,
   scope, requested side effects and branch/copy/material references that define
   what is being evaluated.
2. **Evaluation evidence fingerprint** — additionally binds the verified lease
   revision/digest, privacy policy revisions, exact gate versions, explicit
   evaluation time and gate budgets.

This separation prevents correlation metadata from being confused with verified
freshness evidence.

### 4.2 Do not fingerprint unrelated registry state

P1-001 already has a metamorphic property that unrelated registry records do
not change the decision. Therefore the future capability evidence projection
should bind the **selected live-head evidence and admitted selected lease
record**, not every unrelated registry record.

This preserves:

```text
unrelated registry record added
→ same selected lease evidence
→ same bounded capability evaluation semantics
```

### 4.3 Digest is not a magic permission token

A caller-supplied value such as:

```text
request_digest = "abc"
```

proves nothing.

Rules:

- the coordinator computes the fingerprint after strict admission;
- caller-provided fingerprints are ignored or compared only as non-authoritative
  assertions;
- the digest domain includes versioned canonical fields, not a free-form string;
- a consumer may treat a digest as evidence only if it can recompute it from the
  canonical bound context or is inside the same trusted evaluation attempt;
- a digest without recomputable context is a correlation hint, not authority;
- equal caller-supplied digest strings never override unequal canonical fields.

---

## 5. 🔐 Trust and verification boundary

Existing P1 contracts intentionally consume caller-supplied snapshots/records.
This readiness contract does not pretend that a pure function can prove the
real-world provenance of those values.

A future coordinator may:

```text
strictly admit values
canonicalize them
invoke the existing pure classifiers
verify internal linkage/revision/digest rules already owned by those gates
bind the exact admitted values and derived evidence
```

It may **not** silently claim:

```text
this snapshot came from the authoritative external source
this material record is globally current
this caller is trustworthy
this digest was trustworthy because the caller supplied it
```

If source authenticity or external freshness requires a later provenance or
Action Gate mechanism, that must be separately authorized. Hidden I/O is not an
acceptable substitute.

Values that must not be trusted as caller assertions include:

- observed live lease revision;
- verified lease record digest;
- gate contract version;
- canonical profile version;
- derived request/evidence fingerprints;
- claims of current privacy policy state;
- claims that an old positive result is still fresh.

They must be derived or verified from the admitted evaluation inputs and local
contract versions.

---

## 6. ⏱️ Freshness model

### 6.1 Same-attempt freshness

The bounded safe model is **same-attempt composition**.

```text
immutable canonical context
→ P1-001 evaluation
→ P1-002 evaluation
→ binding verification
→ readiness classification
```

The future readiness result is an intermediate classification from that one
evaluation attempt. It is **not** a durable authorization token.

No arbitrary TTL is invented here. A timestamp alone cannot prove freshness.
Freshness is the conjunction of the explicit evaluation time and the exact
revisions/versions/evidence that were evaluated.

### 6.2 Invalidation rules

The entire prior readiness result becomes non-reusable and a new complete
evaluation attempt is required if any of these change:

```text
request_id
purpose
operation
data scope
requested side effects
material/copy identity
branch
relevant material/copy state
lease requested revision
lease observed live revision
lease verified digest
material policy revision
copy policy revision
gate contract version
binding contract version
canonical profile
evaluation time when lease temporal validity is relevant
gate budget when it can alter classification
```

A persisted readiness/envelope record may be retained for audit provenance, but
it cannot be replayed as permission.

### 6.3 Race boundary

A pure coordinator cannot detect a source change that occurs after the supplied
snapshot was produced unless new source evidence is supplied. Therefore:

```text
same-attempt readiness
≠ guarantee that mutable external state cannot change afterward
```

Any future execution path must own its own last-responsible-moment freshness
rule. That belongs to a separately authorized Action Gate/execution contract,
not to this docs-only readiness block.

---

## 7. 🧩 Strategy comparison

### Strategy A — Pure coordinator over original source inputs

**SELECTED as the readiness architecture.**

A future coordinator receives one immutable canonical context plus the original
source inputs required by P1-001/P1-002, derives the exact gate projections,
invokes the existing pure classifiers, verifies the common binding, and emits a
non-authoritative readiness classification.

Properties:

```text
P1 frozen result shapes unchanged
no ambient clock
no filesystem/database/network access
no persistence
no retrieval
no tool execution
no identity/M3 access
same-attempt binding
caller digest not trusted
```

This can preserve purity because every dependency is an explicit value and both
existing gate functions are already pure bounded classifiers.

### Strategy B — Evidence envelope / wrapper

**ACCEPTED ONLY AS DERIVED EVIDENCE, REJECTED AS A STANDALONE AUTHORITY INPUT.**

A versioned envelope is useful for audit/debugging if it is produced from the
same admitted canonical context and contains enough information for fingerprint
recomputation.

It is insufficient when an arbitrary caller can attach a digest to unrelated
bare results.

```text
verified coordinator-derived envelope
→ useful evidence/provenance

caller-asserted envelope around bare results
→ not authority
→ must be re-evaluated from source inputs
```

The future coordinator is the only component that may claim it formed the
binding for that evaluation attempt. Possessing or copying the envelope does
not grant permission.

### Strategy C — Bare-result composition

**REJECTED.**

```text
compose(capability_result, privacy_result)
```

without source inputs or independently verifiable common binding cannot prove
same request, purpose, operation, scope, branch, policy revision or freshness.

It is structurally vulnerable to scope laundering and stale-result
substitution.

---

## 8. 🚦 Fail-closed composition semantics

A future readiness classifier must distinguish a verified blocker from an
unverifiable state while keeping both non-positive.

Normative readiness vocabulary:

```text
ELIGIBLE_FOR_NEXT_GATE
NOT_ELIGIBLE
DEFER
```

### `ELIGIBLE_FOR_NEXT_GATE`

Means only:

> All bounded gates required by this particular composition contract were
> evaluated from the same verified canonical context and none reported a
> blocker in their bounded dimensions.

It does **not** mean authorized, executable, retrievable or tool-allowed.

### `NOT_ELIGIBLE`

Use for a verified blocker, including:

```text
gate DENY/remediation outcome
MISMATCH
STALE evidence
CONTRADICTION
invalid canonicalization
verified scope/purpose/operation/side-effect conflict
```

### `DEFER`

Use when a safe conclusion cannot be verified, including:

```text
MISSING
UNKNOWN
UNVERIFIED
unsupported contract version
incomplete context
duplicate/conflicting evidence that cannot be resolved deterministically
```

Both `NOT_ELIGIBLE` and `DEFER` are fail-closed.

```text
uncertainty → ALLOW
```

is forbidden.

---

## 9. 🛑 Positive result has no execution authority

The exact positive readiness term is:

```text
ELIGIBLE_FOR_NEXT_GATE
```

This is chosen over an `AUTHORIZED`/`PASS`/`ALLOWED` vocabulary because it
encodes that a later gate is still required.

`NO_BOUNDED_BLOCKER_FOUND` may be used as explanatory prose, but it is not a
stronger state and must not be interpreted as permission.

Explicit invariants:

```text
Capability ALLOW
+ Privacy ALLOW_REFERENCE
+ verified cross-gate binding
= at most ELIGIBLE_FOR_NEXT_GATE

ELIGIBLE_FOR_NEXT_GATE
≠ AUTHORIZED
≠ EXECUTE
≠ ACTION_ALLOWED
≠ RETRIEVE_ALLOWED
≠ TOOL_ALLOWED
```

---

## 10. 🧱 Action Gate remains separate

The Identity & Relational research architecture defines Action Gate as broader
than Capability Lease plus privacy. A complete future Action Gate may also
include constitutional, relationship/commitment, side-effect and other governed
constraints.

Therefore:

```text
Capability ALLOW
+
Privacy ALLOW_REFERENCE
+
Cross-Gate ELIGIBLE_FOR_NEXT_GATE

≠ Action Gate PASS
```

This readiness contract must never be used as a shortcut around those future
constraints.

---

## 11. 📖 `ALLOW_REFERENCE` is not retrieval authority

P1-002 is a classification boundary.

```text
ALLOW_REFERENCE
= no privacy-reconciliation blocker found in the supplied bounded values

ALLOW_REFERENCE
≠ permission to read bytes
≠ permission to query storage
≠ permission to call a database
≠ permission to access a file
≠ permission to use a network
```

This block implements and authorizes none of those operations.

---

## 12. 🛡️ Threat model and adversarial scenarios

| ID | Scenario | Required result |
|---|---|---|
| T1 | P1-001 result from request A + P1-002 result from B | `MISMATCH` → `NOT_ELIGIBLE`; bare composition rejected |
| T2 | purpose changes after gate evaluation | prior evidence invalid; complete re-evaluation required |
| T3 | operation changes `read → write` | prior evidence invalid; complete re-evaluation required |
| T4 | data scope expands `A → A+B` | prior positive result insufficient; re-evaluate |
| T5 | requested side effect changes from none to external effect | prior evidence invalid; re-evaluate |
| T6 | lease live-head revision changes | `STALE` → `NOT_ELIGIBLE`; re-evaluate |
| T7 | privacy material/copy policy revision changes | `STALE` → `NOT_ELIGIBLE`; re-evaluate |
| T8 | privacy evidence from branch A is used for branch B | `MISMATCH` → `NOT_ELIGIBLE` |
| T9 | caller supplies same forged digest for different canonical requests | digest ignored/recomputed; canonical mismatch wins |
| T10 | consumer interprets `ELIGIBLE_FOR_NEXT_GATE` as `EXECUTE` | contract violation; no execution authority exists |
| T11 | future composer tries to read lease store, privacy store, graph, files or network | forbidden hidden I/O; separate authority required |
| T12 | composition tries to read/change Character, identity, relationship or M3 state | forbidden boundary crossing |

Additional adversarial rules:

```text
Capability DENY + any privacy result
→ NOT_ELIGIBLE

Capability ALLOW + DENY_RETRIEVAL
→ NOT_ELIGIBLE

Capability ALLOW + QUARANTINE_REQUIRED
→ NOT_ELIGIBLE

Capability ALLOW + REBUILD_REQUIRED
→ NOT_ELIGIBLE

missing required gate
→ DEFER

unsupported gate version
→ DEFER
```

---

## 13. 🔁 Metamorphic properties

### M1 — authority-field invalidation
Changing any authority-critical field invalidates the previous result for the
new context.

### M2 — side-effect monotonicity
Adding a requested side effect can never preserve a previous positive readiness
result automatically.

### M3 — scope monotonicity
Expanding data scope cannot make the decision less strict and cannot reuse the
old positive evidence.

### M4 — deny monotonicity
`DENY + positive` can never become positive readiness.

### M5 — missing/unknown monotonicity
`UNKNOWN`, `MISSING` or `UNVERIFIED` plus a positive gate can never become
execution authority or positive readiness.

### M6 — canonical metadata ordering
Reordering semantically unordered metadata that canonical admission normalizes
must not change the deterministic canonical result. Unrelated presentation
metadata is excluded from the authority-binding domain.

### M7 — determinism
Identical immutable canonical inputs, revisions, budgets and contract versions
must produce the same readiness classification and fingerprints.

### M8 — revision invalidation
Changing an authority-relevant lease or privacy policy revision invalidates the
old evidence.

### M9 — no authority amplification
Composition cannot produce more authority than the explicitly evaluated bounded
dimensions; this contract itself produces no execution authority.

### M10 — next-gate requirement
Every positive readiness state still requires the next separately authorized
gate.

---

## 14. 🧊 Frozen P1 contracts remain unchanged

This decision deliberately does **not** add fields to:

```text
P1-001 ResolutionResult
P1-002 PrivacyReconciliationResult
P0 AuthorityRef
```

The binding problem can be solved at a future coordinator boundary by retaining
and canonicalizing the original admitted source inputs inside the same
attempt.

If later implementation work proves that this is impossible without changing a
frozen P1 contract, implementation must stop and a separate contract-change
proposal/Owner GO is required.

No such blocker is demonstrated by the current source surface.

---

## 15. 🎭 Character, Identity and M3 boundary

Character remains a presentation-only research track with its separate runtime
activation gate. This document provides no Character validation evidence and
changes no Character status.

```text
CHARACTER_RUNTIME_ACTIVATION_GATE
= BLOCKED_PENDING_REQUIRED_VALIDATION
```

This contract also has no authority to:

```text
write M2 or M3
nominate M2 → M3
mutate identity
mutate relationships or commitments
perform Genesis Heritage ingestion
integrate Human Paths Atlas runtime
```

Direct and indirect M3 writes remain forbidden.

---

## 16. 🚫 Explicit non-goals

```text
runtime composer
P1-003 assignment
Action Gate implementation
Retrieval Gate implementation
Tool Gate / Tool Receipt runtime
retrieval execution
privacy remediation execution
storage/database/file/network access
persistence or cache
registry service
new worker or daemon
event/replay integration
belief mutation
relationship mutation
identity mutation
Character runtime
M3 nomination/write
Genesis Heritage runtime
Human Paths Atlas runtime
backend selection/migration
deployment
```

---

## 17. 🛑 Stop conditions for any future implementation proposal

Stop and return to architecture if:

- source inputs cannot be retained in one immutable evaluation attempt;
- common purpose/branch/request binding cannot be proved exactly;
- a caller-supplied digest is treated as authority evidence;
- canonicalization is ambiguous or unsupported;
- relevant freshness depends on hidden ambient state;
- a positive readiness state can reasonably be consumed as execution
  permission;
- composition requires database, filesystem, network or other hidden I/O;
- P1-001/P1-002 frozen contracts need silent expansion;
- Action Gate, retrieval, tools, identity, relationships, Character or M3 are
  pulled into the small composer without separate authority;
- source provenance requirements cannot be satisfied by the explicit inputs;
- required adversarial/metamorphic properties cannot be made deterministic.

A safe documented stop is a valid outcome.

---

## 18. ✅ Implementation prerequisites

Before any future code milestone can be authorized, a separate proposal must
freeze at least:

```text
[ ] exact CrossGateEvaluationContext runtime schema
[ ] exact common-purpose namespace rule
[ ] exact canonical projection fields
[ ] exact request/evidence fingerprint domains
[ ] domain/version separation for fingerprints
[ ] exact ELIGIBLE_FOR_NEXT_GATE / NOT_ELIGIBLE / DEFER result contract
[ ] same-attempt freshness and invalidation behavior
[ ] source-provenance boundary
[ ] no hidden I/O property
[ ] T1–T12 executable adversarial cases
[ ] M1–M10 executable metamorphic properties
[ ] deterministic repeated-evaluation fixtures
[ ] no-authority-amplification tests
[ ] explicit Owner GO
[ ] clean Tier A implementation PR
[ ] exact-head CI + post-merge main CI
```

This document is readiness evidence, not that implementation proposal.

---

## 19. 🏁 Readiness exit criteria

The docs-only readiness block is complete when the following are true:

```text
[x] canonical common-binding model selected
[x] stale-result invalidation semantics explicit
[x] bare-result composition rejected
[x] fail-closed result vocabulary fixed
[x] positive semantics cannot be mistaken for permission
[x] caller-supplied digest rejected as authority evidence
[x] T1–T12 have exact fail-closed handling
[x] M1–M10 are frozen
[x] P1-001/P1-002 frozen contracts remain unchanged
[x] Action Gate remains a separate future boundary
[x] implementation prerequisites explicit
[x] separate Owner GO still required
```

Therefore:

```text
CROSS_GATE_BINDING_READINESS = READY
RUNTIME_IMPLEMENTATION       = NOT_AUTHORIZED
P1_003                       = NOT_ASSIGNED
IMPLEMENTATION_AUTHORIZATION = NONE
```

---

## 20. 🧭 Future P1-003 decision boundary

No P1-003 milestone is assigned by this document.

A possible later owner decision may evaluate:

```text
Potential future P1-003 candidate:
Pure Governed Constraint Composer
```

Only if a separate bounded implementation contract demonstrates that it:

- consumes one immutable canonical evaluation context;
- calls only pure explicit-input classifiers;
- never accepts bare results as authority;
- performs no I/O or persistence;
- emits at most `ELIGIBLE_FOR_NEXT_GATE`;
- cannot be mistaken for Action Gate, retrieval or tool authority;
- preserves Character/identity/M3 boundaries;
- receives a separate explicit Owner GO.

Until that separate decision exists:

```text
NO_RUNTIME_IMPLEMENTATION_AUTHORIZED
```
