# 🧩 P1-003 Pure Governed Constraint Composer — Frozen Contract

```text
Status:                         FROZEN_DOCS · DOCS_ONLY · IMPLEMENTATION_CONTRACT
Version:                        0.1
Date:                           2026-08-10
Review tier:                    TIER_A
Candidate:                      PURE_GOVERNED_CONSTRAINT_COMPOSER
P1-003 runtime assignment:      NOT_ASSIGNED
P1-003 contract:                FROZEN_DOCS
Owner GO:                       NOT_GRANTED
Implementation authorization:   NONE
Runtime implementation:         NOT_AUTHORIZED
Retrieval authority:            NONE
Action authority:               NONE
Tool authority:                 NONE
Identity authority:             NONE
Relationship authority:         NONE
Direct or indirect M3 write:    FORBIDDEN
Persistence authority:          NONE
Network/filesystem/database I/O:NONE
Deployment authority:           NONE
```

> **CONTRACT FROZEN ≠ OWNER GO.**
>
> **THIS DOCUMENT DOES NOT AUTHORIZE IMPLEMENTATION.**
>
> It freezes the exact contract that a later separately authorized P1-003
> implementation would have to satisfy. It does not assign P1-003 as a runtime
> milestone and does not authorize retrieval, persistence, filesystem/database/
> network I/O, Action Gate execution, tool execution, relationship or identity
> mutation, Character runtime, M3 writes, remediation or deployment.

---

## 1. 🎯 Bounded purpose

The only purpose of the future component is to answer this question:

> Given one immutable, explicitly supplied evaluation context, do the existing
> bounded P1-001 Capability Lease resolver and P1-002 Privacy Reconciliation
> classifier, evaluated in the same attempt and bound to the same canonical
> request/evidence context, leave the request eligible to proceed to a later
> separately authorized gate?

The strongest positive result is exactly:

```text
ELIGIBLE_FOR_NEXT_GATE
```

It is never execution authority.

```text
ELIGIBLE_FOR_NEXT_GATE ≠ ACTION_GATE_PASS
ELIGIBLE_FOR_NEXT_GATE ≠ RETRIEVAL_PERMISSION
ELIGIBLE_FOR_NEXT_GATE ≠ TOOL_PERMISSION
ELIGIBLE_FOR_NEXT_GATE ≠ EXECUTION_PERMISSION
```

The future composer is a pure coordinator over existing bounded classifiers. It
is not an Action Gate, retrieval service, policy registry, persistence service,
execution engine, identity runtime or deployment layer.

---

## 2. 🔒 Frozen versions and domains

A later implementation must expose these exact semantic constants:

```text
COMPOSER_CONTRACT_VERSION = "P1-003-v0.1"
BINDING_CONTRACT_VERSION  = "CROSS-GATE-BINDING-v0.1"
CANONICAL_PROFILE         = "MENTAURY_CANONICAL_JSON_V1"
COMMON_REQUEST_DOMAIN     = "MENTAURY_P1_003_COMMON_REQUEST_V1"
EVALUATION_EVIDENCE_DOMAIN= "MENTAURY_P1_003_EVALUATION_EVIDENCE_V1"
P1_001_EXPECTED_VERSION   = "P1-001-v0.2"
P1_002_EXPECTED_VERSION   = "P1-002-v0.1"
```

The implementation must import and compare the live P1 version constants rather
than trusting caller-supplied strings. Unsupported gate versions fail closed and
may not be silently adapted.

No caller may supply or override:

```text
composer_contract_version
binding_contract_version
canonical_profile
P1 contract versions
common_request_fingerprint
evaluation_evidence_fingerprint
```

---

## 3. 📦 Reserved package and public API

If and only if a later explicit Owner GO authorizes implementation, the bounded
package is reserved as:

```text
src/mentaury/composition/__init__.py
src/mentaury/composition/governed_constraints/__init__.py
src/mentaury/composition/governed_constraints/contracts.py
src/mentaury/composition/governed_constraints/composer.py
```

No service, registry, adapter, repository, worker, transport, persistence or I/O
module is part of P1-003 v0.1.

The exact public function is frozen as:

```python
def compose_governed_constraints(
    *,
    context: CrossGateEvaluationContext,
) -> GovernedConstraintResult:
    ...
```

The function accepts **no bare P1 results**, no digest argument, no callback, no
clock provider, no repository/service object, no tool handle and no backend.

This API shape is a security property:

```text
compose(capability_result, privacy_result) = FORBIDDEN API
caller_digest                             = FORBIDDEN API
```

---

## 4. 🧬 Exact immutable context schema

The future `CrossGateEvaluationContext` is a frozen/slotted value object with
exactly these fields and no extension dictionary:

```python
@dataclass(frozen=True, slots=True)
class CrossGateEvaluationContext:
    request_id: str
    purpose_id: str
    operation_id: str
    data_scope: tuple[ScopeItem, ...]
    requested_side_effects: tuple[str, ...]
    branch_id: str
    evaluated_at: str
    authority_ref: AuthorityRef
    registry_snapshot: RegistrySnapshot
    privacy_material: PrivacyMaterial
    privacy_copy: PrivacyCopy
    capability_budget: ResolutionBudget
    privacy_budget: PrivacyReconciliationBudget
    composition_budget: CompositionBudget
```

All nested P1 values must be the existing frozen P1 types from current `main`.
P1-003 v0.1 does not define replacement copies of those contracts.

### 4.1 Context admission invariants

Before gate evaluation:

1. `request_id`, `purpose_id`, `operation_id`, and `branch_id` are non-empty,
   unpadded strings;
2. `data_scope` contains only `ScopeItem`, is already sorted and unique;
3. `requested_side_effects` is already sorted and unique and contains only
   non-empty unpadded strings;
4. `evaluated_at` is canonical UTC `Z` form accepted unchanged by P1-001;
5. `authority_ref` is an existing `AuthorityRef`;
6. `registry_snapshot` is an existing immutable `RegistrySnapshot`;
7. privacy material/copy and both P1 budgets are exact existing typed contracts;
8. `privacy_copy.material_id == privacy_material.material_id`;
9. `privacy_copy.branch_id == branch_id`;
10. `privacy_copy.policy_revision <= privacy_material.policy_revision`;
11. `composition_budget` is the exact P1-003 budget contract below;
12. there is no purpose translation layer: P1-001 `purpose_id` and P1-002
    `purpose` receive the same exact `purpose_id` bytes/characters.

A malformed context raises `GovernedConstraintContractError`. It does not
produce an `ELIGIBLE`, `NOT_ELIGIBLE`, or `DEFER` result. API contract failure is
fail-closed and is not authorization evidence.

### 4.2 No hidden normalization

The composer may validate canonical ordering but may not silently repair,
sort, trim, map, alias or semantically translate authority-critical caller
values.

```text
"read" ≠ "READ"
"purpose-a" ≠ "purpose a"
branch aliases ≠ exact branch_id
semantic similarity ≠ purpose equality
```

Any future normalization/mapping layer needs its own contract and authority.

---

## 5. 📏 Exact P1-003 composition budget

P1-003 v0.1 adds one local deterministic budget only for composition work:

```python
@dataclass(frozen=True, slots=True)
class CompositionBudget:
    max_common_request_bytes: int
    max_evidence_bytes: int
    max_scope_items: int
    max_side_effects: int
```

All four values are positive integers; booleans are invalid integers.

Budget meaning:

- `max_scope_items` bounds the common request scope before fingerprint work;
- `max_side_effects` bounds requested side-effect cardinality before fingerprint
  work;
- `max_common_request_bytes` bounds the canonical common-request projection;
- `max_evidence_bytes` bounds the canonical targeted evaluation-evidence
  projection.

The existing P1 budgets remain authoritative for their own gates. P1-003 does
not weaken, replace, infer or automatically enlarge them.

A valid but over-budget composition attempt returns:

```text
DEFER · COMPOSITION_BUDGET_EXHAUSTED
```

It may never become positive by truncating scope, side effects, records or
privacy evidence.

---

## 6. 🔀 Exact gate projections

The composer derives gate inputs itself. Callers do not supply a second intent.

### 6.1 P1-001 projection

```python
ActionIntent(
    purpose_id=context.purpose_id,
    operation_id=context.operation_id,
    data_scope=context.data_scope,
    requested_side_effects=context.requested_side_effects,
)
```

P1-001 is invoked exactly once with:

```text
registry_snapshot = context.registry_snapshot
authority_ref     = context.authority_ref
action_intent     = derived ActionIntent
evaluated_at      = context.evaluated_at
resolution_budget = context.capability_budget
```

### 6.2 P1-002 projection

```python
PrivacyAccessIntent(
    copy_id=context.privacy_copy.copy_id,
    branch_id=context.branch_id,
    purpose=context.purpose_id,
)
```

P1-002 is invoked exactly once with:

```text
material = context.privacy_material
copy     = context.privacy_copy
intent   = derived PrivacyAccessIntent
budget   = context.privacy_budget
```

No caller-supplied `ActionIntent` or `PrivacyAccessIntent` is accepted by the
composer public API. This prevents cross-intent substitution.

---

## 7. 🔗 Common request fingerprint

The common request fingerprint is SHA-256 over
`MENTAURY_CANONICAL_JSON_V1` bytes of exactly this value:

```json
{
  "domain": "MENTAURY_P1_003_COMMON_REQUEST_V1",
  "composer_contract_version": "P1-003-v0.1",
  "binding_contract_version": "CROSS-GATE-BINDING-v0.1",
  "canonical_profile": "MENTAURY_CANONICAL_JSON_V1",
  "request_id": "<context.request_id>",
  "purpose_id": "<context.purpose_id>",
  "operation_id": "<context.operation_id>",
  "data_scope": "<ScopeItem.to_value() list>",
  "requested_side_effects": "<canonical list>",
  "branch_id": "<context.branch_id>",
  "material_id": "<privacy_material.material_id>",
  "copy_id": "<privacy_copy.copy_id>",
  "capability_lease_id": "<authority_ref.capability_lease_id>",
  "capability_revision": "<authority_ref.capability_revision>"
}
```

The JSON above is structural documentation: array/object values retain their
native canonical JSON types; placeholder strings are not literal runtime values.

Normative algorithm:

```text
strict context admission
→ construct exact common-request value
→ canonical_json_bytes(...)
→ enforce max_common_request_bytes
→ hashlib.sha256(bytes).hexdigest()
```

Any canonicalization failure is:

```text
NOT_ELIGIBLE · BINDING_CANONICALIZATION_FAILED
```

Caller-supplied equal digest strings cannot override unequal canonical values.

---

## 8. 🧾 Targeted source evidence projection

P1-003 must not fingerprint every unrelated registry record. It binds only the
requested capability evidence plus exact privacy evidence.

### 8.1 Capability source projection

The targeted capability source projection contains exactly:

```text
registry_availability
registry_unavailable_reason
registry_schema_version
requested capability_lease_id
requested capability_revision
observed live revision for requested lease_id, or null
requested record for (lease_id, requested_revision), or null
```

It must not contain unrelated registry records or unrelated live-head entries.

### 8.2 Privacy source projection

The privacy source projection contains exactly:

```text
privacy_material.to_value()
privacy_copy.to_value()
derived PrivacyAccessIntent.to_value()
privacy_budget.to_value()
```

### 8.3 Source-provenance label

The evidence projection must carry this fixed semantic label:

```text
source_provenance_scope = "CALLER_SUPPLIED_VALUE_EVIDENCE_ONLY"
```

This is an explicit non-claim. The pure composer can attest which immutable
values it evaluated; it cannot prove that an external database, file, service,
registry or person supplied globally authoritative/current values.

---

## 9. 🧬 Evaluation evidence fingerprint

After both gates are evaluated, the evidence fingerprint is SHA-256 over
`MENTAURY_CANONICAL_JSON_V1` bytes of exactly this domain-separated structure:

```text
domain = MENTAURY_P1_003_EVALUATION_EVIDENCE_V1
composer_contract_version
binding_contract_version
canonical_profile
source_provenance_scope
common_request_fingerprint
evaluated_at
P1-001 live contract version
P1-002 live contract version
capability_budget
privacy_budget
composition_budget
targeted capability source projection
privacy source projection
P1-001 ResolutionResult.to_value()
P1-002 PrivacyReconciliationResult.to_value()
```

The implementation must not include unrelated registry state, logs, labels,
Character/identity/relationship state, M3 state, environment variables or
ambient timestamps.

Normative algorithm:

```text
construct targeted evidence value
→ canonical_json_bytes(...)
→ enforce max_evidence_bytes
→ hashlib.sha256(bytes).hexdigest()
```

If canonicalization fails:

```text
NOT_ELIGIBLE · EVIDENCE_CANONICALIZATION_FAILED
```

If the evidence is valid but over budget:

```text
DEFER · COMPOSITION_BUDGET_EXHAUSTED
```

A fingerprint is derived evidence only. Possessing or copying it grants no
permission and it is never accepted as composer input.

---

## 10. 🚦 Exact result contract

P1-003 v0.1 defines exactly three decisions:

```python
class GovernedConstraintDecision(StrEnum):
    ELIGIBLE_FOR_NEXT_GATE = "ELIGIBLE_FOR_NEXT_GATE"
    NOT_ELIGIBLE = "NOT_ELIGIBLE"
    DEFER = "DEFER"
```

Exact primary reason vocabulary:

```python
class GovernedConstraintReason(StrEnum):
    ELIGIBLE_FOR_NEXT_GATE = "ELIGIBLE_FOR_NEXT_GATE"
    COMMON_BINDING_MISMATCH = "COMMON_BINDING_MISMATCH"
    BINDING_CANONICALIZATION_FAILED = "BINDING_CANONICALIZATION_FAILED"
    EVIDENCE_CANONICALIZATION_FAILED = "EVIDENCE_CANONICALIZATION_FAILED"
    COMPOSITION_BUDGET_EXHAUSTED = "COMPOSITION_BUDGET_EXHAUSTED"
    GATE_VERSION_UNVERIFIED = "GATE_VERSION_UNVERIFIED"
    GATE_CONTRACT_UNVERIFIED = "GATE_CONTRACT_UNVERIFIED"
    CAPABILITY_BLOCKED = "CAPABILITY_BLOCKED"
    PRIVACY_BLOCKED = "PRIVACY_BLOCKED"
    CAPABILITY_AND_PRIVACY_BLOCKED = "CAPABILITY_AND_PRIVACY_BLOCKED"
    CAPABILITY_DEFERRED = "CAPABILITY_DEFERRED"
    PRIVACY_DEFERRED = "PRIVACY_DEFERRED"
    CAPABILITY_AND_PRIVACY_DEFERRED = "CAPABILITY_AND_PRIVACY_DEFERRED"
```

Exact result shape:

```python
@dataclass(frozen=True, slots=True)
class GovernedConstraintResult:
    decision: GovernedConstraintDecision
    primary_reason: GovernedConstraintReason
    common_request_fingerprint: str | None
    evaluation_evidence_fingerprint: str | None
    capability_result: ResolutionResult | None
    privacy_result: PrivacyReconciliationResult | None
    composer_contract_version: str = "P1-003-v0.1"
    binding_contract_version: str = "CROSS-GATE-BINDING-v0.1"
    canonical_profile: str = "MENTAURY_CANONICAL_JSON_V1"
```

Fingerprint values, when present, are lowercase 64-character SHA-256 hex.

Positive construction invariant:

```text
ELIGIBLE_FOR_NEXT_GATE decision
↔ primary_reason == ELIGIBLE_FOR_NEXT_GATE
↔ both nested gate results are present and positive
↔ both fingerprints are present
↔ exact gate versions verified
```

No result contains a credential, token, callable, tool handle, storage locator,
mutation command or reusable authority object.

---

## 11. 🧭 Gate outcome disposition mapping

The composer does not reinterpret gate semantics. It maps existing outcomes into
`POSITIVE`, `BLOCKER`, or `DEFER` only to choose the cross-gate decision.

### 11.1 P1-001 Capability Lease mapping

`POSITIVE`:

```text
ResolutionDecision.ALLOW + ResolutionReason.ALLOW
```

`DEFER`:

```text
REQUEST_INVALID
BUDGET_MISSING
BUDGET_EXHAUSTED
REGISTRY_UNAVAILABLE
REGISTRY_CONTRACT_VIOLATION
UNKNOWN_LEASE
LEASE_CONTRACT_VIOLATION
LEASE_NOT_ACTIVE when observed_status == UNVERIFIED
```

`BLOCKER`:

```text
REVISION_MISMATCH
LEASE_DIGEST_MISMATCH
LEASE_REVOKED
LEASE_EXPIRED
LEASE_NOT_ACTIVE when observed_status != UNVERIFIED
NOT_YET_VALID
PURPOSE_MISMATCH
OPERATION_NOT_ALLOWED
DATA_SCOPE_VIOLATION
SIDE_EFFECT_NOT_ALLOWED
```

The mapping intentionally treats missing/unverified evidence as `DEFER`, while a
verified stale/denied authority condition is a blocker.

### 11.2 P1-002 Privacy mapping

`POSITIVE`:

```text
PrivacyDecision.ALLOW_REFERENCE + PrivacyReason.ALLOW_REFERENCE
```

`DEFER`:

```text
PrivacyReason.BUDGET_EXHAUSTED
```

`BLOCKER`:

```text
COPY_ABSENT
COPY_ALREADY_QUARANTINED
DELETED_OR_REDACTED_MATERIAL
THIRD_PARTY_PERMISSION_MISSING
PURPOSE_WITHDRAWN
PURPOSE_NOT_PERMITTED
BRANCH_NOT_PERMITTED
STALE_POLICY_REVISION
```

A `PrivacyContractError` after successful P1-003 context admission is not
converted to a positive or ordinary privacy blocker. It yields:

```text
DEFER · GATE_CONTRACT_UNVERIFIED
```

Unexpected unsupported P1 versions yield:

```text
DEFER · GATE_VERSION_UNVERIFIED
```

---

## 12. ⚖️ Exact cross-gate precedence

After binding/version/canonical/budget checks and both gate evaluations:

1. any verified P1 `BLOCKER` dominates any `DEFER` because a known blocker is
   already sufficient to prove `NOT_ELIGIBLE`;
2. if both are blockers → `NOT_ELIGIBLE · CAPABILITY_AND_PRIVACY_BLOCKED`;
3. if capability only is a blocker → `NOT_ELIGIBLE · CAPABILITY_BLOCKED`;
4. if privacy only is a blocker → `NOT_ELIGIBLE · PRIVACY_BLOCKED`;
5. with no blocker, if both defer → `DEFER · CAPABILITY_AND_PRIVACY_DEFERRED`;
6. with no blocker, capability defer only → `DEFER · CAPABILITY_DEFERRED`;
7. with no blocker, privacy defer only → `DEFER · PRIVACY_DEFERRED`;
8. only two positive gate outcomes may produce
   `ELIGIBLE_FOR_NEXT_GATE · ELIGIBLE_FOR_NEXT_GATE`.

No uncertain/missing/unverified state maps to positive.

---

## 13. ⏱️ Freshness and invalidation

P1-003 v0.1 creates **same-attempt evidence**, not a TTL permission.

Any change to any of these requires a completely new composer call:

```text
request_id
purpose_id
operation_id
data_scope
requested_side_effects
branch_id
privacy material identity or state
privacy copy identity, branch, surface or state
capability lease id or requested revision
observed live lease revision
requested lease record/content digest
material policy revision
copy policy revision
evaluated_at
P1 gate contract versions
composer/binding/canonical versions
any P1 or P1-003 budget
```

A previous result or fingerprint is not accepted back into the composer and may
be stored only as external audit provenance by a separately authorized system.
It cannot be replayed as permission.

P1-003 cannot detect a mutable external source changing after the supplied
snapshot was created. Last-responsible-moment execution freshness belongs to a
later separately authorized execution/Action Gate contract.

---

## 14. 🛡️ T1–T12 executable adversarial requirements

Every later implementation PR must include at least one executable test for each
frozen threat ID below.

| ID | Threat | Required executable property |
|---|---|---|
| T1 | cross-request result mixing | API accepts no bare results; changing `request_id` changes common fingerprint and forces reevaluation |
| T2 | purpose mutation | exact purpose changes both gate projections and fingerprint; no semantic aliasing |
| T3 | operation mutation | operation mutation changes fingerprint and cannot preserve old positive authority |
| T4 | scope expansion | added scope changes fingerprint and cannot make a previous blocker/positive reusable |
| T5 | side-effect mutation | added/changed side effect changes fingerprint; capability mapping remains fail closed |
| T6 | lease revision race | requested/live revision change invalidates evidence; stale revision is not eligible |
| T7 | privacy policy race | material/copy policy revision change invalidates evidence; stale policy is not eligible |
| T8 | branch substitution | copy/context branch mismatch is rejected; a new branch requires a new full evaluation |
| T9 | forged caller digest | composer signature accepts no digest/fingerprint input; supplied extra argument is rejected |
| T10 | positive-result escalation | `ELIGIBLE_FOR_NEXT_GATE` exposes no execution/retrieval/tool capability and cannot equal Action Gate PASS |
| T11 | hidden I/O | import and call succeed with forbidden ambient I/O/clock/environment hooks configured to fail if touched |
| T12 | Character/Identity/M3 leakage | exact context/result schemas contain no Character, identity, relationship or M3 authority fields and composer imports none of those runtimes |

No threat ID may be marked satisfied solely by prose or static typing.

---

## 15. 🔁 M1–M10 executable metamorphic requirements

| ID | Mutation | Required relation |
|---|---|---|
| M1 | mutate any authority-critical common request field | old fingerprint/result is non-reusable; new call required |
| M2 | add requested side effect | decision must not become more permissive solely because of the addition |
| M3 | expand data scope | decision must not become more permissive solely because of expansion |
| M4 | turn one gate positive into a blocker | composed result cannot remain `ELIGIBLE_FOR_NEXT_GATE` |
| M5 | turn one gate positive into missing/unverified/defer | composed result cannot remain `ELIGIBLE_FOR_NEXT_GATE` |
| M6 | reorder already canonical unrelated metadata outside the selected evidence | result/fingerprints for selected evidence are unchanged |
| M7 | repeat exact immutable context | decision, reasons and fingerprints are byte-for-byte deterministic |
| M8 | change relevant revision/version | evidence fingerprint changes and prior result is non-reusable |
| M9 | add unrelated registry record/live head | selected result and fingerprints are unchanged when requested lease evidence is unchanged |
| M10 | combine positive bounded gates | authority never exceeds `ELIGIBLE_FOR_NEXT_GATE`; no Action/retrieval/tool authority appears |

M6/M9 specifically prohibit fingerprinting unrelated registry state.

---

## 16. 🧪 Mandatory implementation test matrix

A later implementation PR must include executable coverage for all of these test
families. IDs are normative; multiple IDs may live in one test file.

### Context / contract

```text
CGC-CTX-001 exact valid context accepted
CGC-CTX-002 padded/empty authority-critical string rejected
CGC-CTX-003 unsorted scope rejected
CGC-CTX-004 duplicate scope rejected
CGC-CTX-005 unsorted side effects rejected
CGC-CTX-006 duplicate side effects rejected
CGC-CTX-007 noncanonical evaluated_at rejected
CGC-CTX-008 material/copy identity mismatch rejected
CGC-CTX-009 copy/context branch mismatch rejected
CGC-CTX-010 copy policy ahead of material rejected
CGC-CTX-011 wrong nested P1 type rejected
CGC-CTX-012 invalid composition budget rejected
CGC-CTX-013 frozen context mutation rejected
CGC-CTX-014 public API rejects unknown/bare-result/digest arguments
```

### Fingerprints / projections

```text
CGC-FP-001 exact common-request canonical fixture
CGC-FP-002 exact common-request SHA-256 fixture
CGC-FP-003 exact evidence canonical fixture
CGC-FP-004 exact evidence SHA-256 fixture
CGC-FP-005 common mutation changes common fingerprint
CGC-FP-006 relevant evidence mutation changes evidence fingerprint
CGC-FP-007 unrelated registry record does not change fingerprints
CGC-FP-008 caller cannot inject contract/version strings
CGC-FP-009 caller cannot inject fingerprints
CGC-FP-010 evidence projection excludes unrelated/identity/M3 data
```

### Decision / precedence

```text
CGC-DEC-001 both positive → ELIGIBLE_FOR_NEXT_GATE
CGC-DEC-002 capability blocker + privacy positive → NOT_ELIGIBLE
CGC-DEC-003 capability positive + privacy blocker → NOT_ELIGIBLE
CGC-DEC-004 both blockers → NOT_ELIGIBLE/BOTH
CGC-DEC-005 capability defer + privacy positive → DEFER
CGC-DEC-006 capability positive + privacy defer → DEFER
CGC-DEC-007 both defer → DEFER/BOTH
CGC-DEC-008 blocker dominates opposite defer
CGC-DEC-009 UNVERIFIED capability status maps to DEFER
CGC-DEC-010 revision mismatch maps to blocker
CGC-DEC-011 stale privacy revision maps to blocker
CGC-DEC-012 composition budget exhaustion maps to DEFER
CGC-DEC-013 canonicalization failure never maps positive
CGC-DEC-014 gate version mismatch maps to DEFER
```

### Threat / metamorphic

```text
CGC-T-001 … CGC-T-012 map one-to-one to T1 … T12
CGC-M-001 … CGC-M-010 map one-to-one to M1 … M10
```

### Purity / hidden authority

```text
CGC-PURE-001 fresh-process import has no ambient filesystem/database/network use
CGC-PURE-002 composer call has no ambient filesystem/database/network use
CGC-PURE-003 import/call has no ambient clock access
CGC-PURE-004 import/call has no environment-variable authority
CGC-PURE-005 no event/replay/belief/identity/relationship/M3 mutation
CGC-PURE-006 no tool execution, subprocess or dynamic plugin loading
CGC-PURE-007 repeated exact context is deterministic
CGC-PURE-008 result contains no callable/credential/capability material
```

All frozen P1-001/P1-002 tests remain green unchanged. Tests must not be weakened
or rewritten merely to admit P1-003.

---

## 17. 🚫 No-hidden-I/O proof strategy

A later implementation must demonstrate both import-time and call-time purity.
The exact proof obligation is:

1. import the P1-003 package in a fresh interpreter with sentinel hooks that fail
   on filesystem file access attributable to P1-003, database connections,
   socket/network clients, subprocess execution, environment reads and ambient
   clock calls;
2. call `compose_governed_constraints` with complete in-memory typed fixtures
   under the same sentinels;
3. verify no persistence, event append, replay/projection, tool, belief,
   relationship, identity or M3 module is invoked;
4. verify the result depends only on the explicit context and frozen local
   contract constants;
5. verify source inspection/import graph contains no dynamic plugin loading or
   backend/service adapters in the bounded P1-003 package.

Allowed implementation dependencies are limited to deterministic standard
library value/hash helpers plus the existing canonical JSON, contract, P1-001
and P1-002 modules needed by this contract.

---

## 18. 🧱 Compatibility / non-modification rule

P1-003 v0.1 must not require changes to the semantics or result shapes of:

```text
P1-001 Capability Lease Resolution
P1-002 Privacy Reconciliation Classifier
MENTAURY_CANONICAL_JSON_V1
```

If implementation discovers that any frozen P1 contract must change, the P1-003
implementation PR must stop. Such a change requires a separate architecture and
authorization cycle; it may not be smuggled into implementation.

The future implementation may import existing types/constants/functions, but it
may not turn P1-002 into a caller of P1-001 or otherwise invert ownership.

---

## 19. 🚫 Explicit non-goals and forbidden surface

P1-003 v0.1 does not authorize or implement:

```text
bare-result composition
caller-supplied authorization digest
registry persistence/service
privacy registry persistence
backup/fork discovery or scanning
content inspection or byte retrieval
redaction/deletion/quarantine/rebuild execution
filesystem/database/network access
ambient clock/environment authority
event append, replay or projection integration
belief mutation
relationship mutation
identity mutation
M3 nomination/write/promotion
Character activation
Genesis Heritage runtime
Human Paths Atlas runtime
Action Gate
Tool Receipt runtime
tool execution
subprocess execution
backend selection/migration
worker/background service
deployment/production enablement
objective-truth or consciousness claims
```

`ALLOW_REFERENCE` remains a privacy classification, not retrieval permission.

---

## 20. ✅ Later implementation acceptance criteria

A later implementation may be called `IMPLEMENTED_BOUNDED` only if all are true:

```text
separate explicit P1-003 Owner GO exists and is exact-scope
implementation branch starts from verified current main
only frozen P1-003 package/tests/docs changes are in scope
no frozen P1-001/P1-002 semantic changes
all mandatory CGC test IDs pass
all existing repository tests pass unchanged
T1–T12 executable tests pass
M1–M10 executable tests pass
no-hidden-I/O proof passes
exact fingerprint fixtures pass
complete final diff inspected
exact-head required CI green
branch up to date with main
zero unresolved review threads
Tier A correctness pass PASS
Tier A adversarial pass PASS
authorization boundary PRESERVED
explicit maintainer merge decision recorded
protected merge uses unchanged reviewed head
resulting-main required CI green
Notion sync occurs only after resulting-main evidence
```

Green tests alone are insufficient if the final diff expands authority beyond
this contract.

---

## 21. 🎭 Character / identity / governance boundary

```text
CHARACTER_RUNTIME_ACTIVATION_GATE = BLOCKED_PENDING_REQUIRED_VALIDATION
DIRECT_OR_INDIRECT_M3_WRITE       = FORBIDDEN
```

This contract adds no Character evidence and no identity, relationship, Genesis
Heritage, Human Paths Atlas or M3 runtime authority.

Issue #39 remains open solely as the future public/team transition trigger for a
genuine independent reviewer. It is not a current solo-mode blocker and this
contract does not claim independent human assurance.

---

## 22. 🛑 Authorization stop

After this contract is merged and resulting-main CI is green, the correct state
is still:

```text
P1_003_CANDIDATE           = PURE_GOVERNED_CONSTRAINT_COMPOSER
P1_003_CONTRACT            = FROZEN_DOCS
P1_003_RUNTIME_ASSIGNMENT  = NOT_ASSIGNED
P1_003_OWNER_GO            = NOT_GRANTED
IMPLEMENTATION_AUTHORIZATION = NONE
```

The next possible step is only a **separate explicit Owner GO decision** against
this frozen contract.

```text
CONTRACT_FROZEN_DOCS_ONLY
→ STOP
→ separate Owner GO decision
→ only if GO: clean Tier A implementation PR
```

No wording in this document constitutes that GO.

---

## 23. 🏁 Final formula

```text
P1-001 IMPLEMENTED_BOUNDED
+ P1-002 IMPLEMENTED_BOUNDED
+ Cross-Gate Binding Readiness READY
+ Pure Governed Constraint Composer candidate SELECTED
+ exact P1-003 composer contract FROZEN_DOCS

→ implementation design is sufficiently specified for a later authorization decision

≠ P1-003 runtime assignment
≠ Owner GO
≠ implementation authorization
≠ retrieval/action/tool authority
≠ identity/relationship/Character/M3 runtime
≠ persistence/I/O/deployment authority
```
