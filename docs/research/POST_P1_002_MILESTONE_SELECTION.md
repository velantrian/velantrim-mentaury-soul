# 🔗 Post-P1-002 Milestone Selection — Cross-Gate Binding & Composition Readiness

```text
Status:                       ARCHITECTURE_SELECTION · DOCS_ONLY
Date:                         2026-08-10
Review tier:                  TIER_A
Selection result:             NO_RUNTIME_MILESTONE_SELECTED
Next bounded work:            CROSS_GATE_BINDING_AND_COMPOSITION_READINESS
Runtime authority:            NONE
Implementation authorization: NONE
P1-003 assignment:            NONE
Persistence authority:        NONE
Retrieval authority:          NONE
Tool authority:               NONE
Identity authority:           NONE
Direct or indirect M3 write:  FORBIDDEN
Deployment authority:         NONE
```

> **THIS PR DOES NOT AUTHORIZE IMPLEMENTATION.**
>
> This decision selects a docs-only readiness block. It does not authorize a
> composer, retrieval gate, Action Gate, tool execution, privacy remediation,
> identity runtime, Character runtime, M3 mutation, backend integration or
> deployment. Any later implementation requires a separate bounded contract,
> explicit Owner GO, clean Tier A implementation PR and green resulting-main CI.

---

## 1. 🎯 Decision

After P1-001 and P1-002, the repository does **not** yet have enough binding
information to safely compose their bare result objects into an execution or
retrieval authorization.

The selected next bounded work is therefore:

```text
CROSS_GATE_BINDING_AND_COMPOSITION_READINESS
= research / contract readiness only
≠ P1-003 runtime
≠ Action Gate
≠ retrieval authorization
≠ implementation GO
```

The purpose of this block is to define the minimum evidence and binding
semantics that a future pure constraint composer would need before any
implementation can be selected.

---

## 2. 📚 Evidence basis

### 2.1 P1-001 result is intentionally not a reusable permission

The implemented P1-001 `ResolutionResult` records:

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

It does **not** carry a canonical fingerprint of the evaluated `ActionIntent`
(`purpose_id`, `operation_id`, `data_scope`, `requested_side_effects`). The
owning contract explicitly states that `ALLOW` is classification data, not a
Tool Receipt, Action Gate approval or execution permission.

### 2.2 P1-002 result is deliberately minimal

The implemented `PrivacyReconciliationResult` contains only:

```text
decision
reason
```

It carries no material, copy, purpose, branch, policy-revision or request
fingerprint. `ALLOW_REFERENCE` means only that the bounded privacy classifier
found no blocker in the supplied values; it is not retrieval permission.

### 2.3 Consequence

Two positive results can be individually valid while belonging to different
requests or different moments in state.

```text
Capability ALLOW for request A
+
Privacy ALLOW_REFERENCE for request B

≠ authorization for A
≠ authorization for B
≠ safe composition
```

A bare-result composer could not prove common request identity, scope or
freshness. That creates a concrete scope-laundering and stale-result
substitution surface.

---

## 3. 🧭 Candidate comparison

Scale: `LOW / MEDIUM / HIGH`. For risk columns, lower is safer. For necessity
and leverage, higher means more useful.

| Candidate | Necessity now | Minimality | Authority risk | Runtime coupling | Testability | Identity/privacy risk | Future leverage | Prematurity | Decision |
|---|---|---|---|---|---|---|---|---|---|
| A. Governed Authorization Composition implementation | HIGH | MEDIUM | **HIGH** until binding solved | LOW-MEDIUM | HIGH | MEDIUM | HIGH | **HIGH** | DEFER |
| B. Read-only / Retrieval Decision Gate | MEDIUM | MEDIUM | **HIGH** | MEDIUM-HIGH | HIGH | **HIGH privacy** | HIGH | HIGH | DEFER |
| C. Action Gate contract | HIGH eventually | LOW | HIGH | HIGH | MEDIUM | HIGH | HIGH | HIGH | DEFER |
| D. Tool / Operation Receipt semantics | MEDIUM | HIGH | LOW-MEDIUM | MEDIUM | HIGH | LOW-MEDIUM | MEDIUM | MEDIUM-HIGH | DEFER |
| E. Privacy reconciliation continuation | MEDIUM | HIGH | MEDIUM | LOW-MEDIUM | HIGH | HIGH privacy | MEDIUM | MEDIUM | DEFER |
| F. Identity / Continuity bounded slice | MEDIUM-HIGH | LOW | HIGH | MEDIUM | LOW-MEDIUM | **HIGH identity** | HIGH | HIGH | DEFER |
| G. Character validation work | HIGH for Character gate | HIGH | LOW | LOW | HIGH | LOW | MEDIUM-HIGH | LOW | VALID PARALLEL RESEARCH, NOT SELECTED |
| H. No runtime milestone; cross-gate binding readiness | **HIGH** | **HIGH** | **LOW** | **LOW** | **HIGH** | **LOW** | **HIGH** | **LOW** | **SELECTED** |

### Why A is not selected yet

A pure constraint composer is architecturally attractive because composition
should only reduce authority. But the existing result shapes do not bind both
classifiers to the same intent/context. Implementing A before solving that gap
would make a deterministic implementation of an under-specified security
boundary.

### Why B is not selected

`ALLOW_REFERENCE` is explicitly not retrieval permission. Turning it into a
retrieval decision before common binding/freshness semantics exist would create
exactly the authority expansion P1-002 forbids.

### Why C is not selected

The research architecture defines Action Gate as broader than Capability Lease
and privacy. Constitutional, relationship/commitment and side-effect checks are
also involved. Freezing that full contract now would couple multiple domains
whose runtime semantics are not yet implemented.

### Why D is not selected

A receipt describes an attempted/completed/denied operation. Defining it before
the authorization and execution boundary is stable risks encoding assumptions
about a runtime that does not yet exist.

### Why E is not selected

P1-002 already classifies `QUARANTINE_REQUIRED` and `REBUILD_REQUIRED` without
executing them. A second planning classifier would add limited value before
inventory, binding and execution authority are separately defined.

### Why F is not selected

Identity/continuity work has high M3, relationship, consent and branch
sensitivity. The smallest trustworthy executable slice is not yet demonstrated.

### Why G is not selected as the main post-P1 path

Character validation is legitimate research and is required before Character
runtime. However the Character gate explicitly requires a versioned scenario
corpus, blinded human labels, inter-rater agreement and multilingual/adversarial
validation. It is a useful parallel evidence track, not the direct missing link
between the two already-implemented P1 classifiers.

---

## 4. 🔐 Exact readiness question

The selected block must answer:

> How can a future pure composer prove that all required gate decisions refer
> to the same canonical intent, scope, branch/purpose context and freshness
> epoch, without changing a classifier result into reusable permission?

A future design must bind at least the semantics relevant to:

```text
capability lease id + revision
capability contract version
purpose
operation
data scope
requested side effects
capability evaluated_at / freshness semantics
privacy material + copy identity
privacy branch
privacy purpose
privacy policy revision
privacy contract version
required governance constraints
```

This list is a readiness requirement, not a new runtime schema.

---

## 5. 🧩 Binding strategies to research

No strategy is implemented or authorized by this decision.

### Strategy 1 — pure coordinator over original inputs

A future coordinator could receive the original caller-supplied inputs and run
the already-pure bounded checks within one deterministic evaluation boundary.
This avoids trusting unrelated bare results, but requires a new contract proving
that orchestration does not create Action Gate or execution authority.

### Strategy 2 — bound evidence envelope

A future wrapper could bind a classifier decision to a canonical digest of its
admitted evaluation inputs and contract version. The design must prove how the
digest is produced and verified; a caller-asserted digest alone is not evidence.
Changing frozen P1 result shapes is **not** authorized by this selection.

### Strategy 3 — bare-result composition

```text
P1-001 result + P1-002 result → final permission
```

**REJECTED.** The current result objects do not provide sufficient common
binding or freshness evidence.

---

## 6. 🛡️ Threat model

### 6.1 Selected readiness block

| Threat | Required readiness rule |
|---|---|
| Authority manufacturing | Positive intermediate decisions never create a new capability or execution permission |
| Scope laundering | Results from different purpose/operation/scope contexts may not be combined |
| Stale authorization | Any relevant lease/policy/context revision change requires re-evaluation |
| Fail-open | Missing, unknown, contradictory or unverified binding information fails closed |
| Partial-result ambiguity | `UNKNOWN`, `UNVERIFIED`, `DEFER`, remediation-required or absent input can never mean permission |
| Cross-module escalation | One classifier cannot reinterpret another classifier's output as authority |
| Identity/M3 leakage | Binding metadata has no identity authority and cannot nominate/write M3 |
| Hidden I/O | Readiness work performs no retrieval, storage, network, filesystem, database or tool calls |
| Audit ambiguity | A future receipt must identify input binding, decisions, applied constraints and explicit non-authorizations |

### 6.2 Deferred Candidate A — composition

A future composer must satisfy:

```text
final eligibility ≤ every required gate constraint
DENY + ALLOW_REFERENCE → not eligible
ALLOW + DENY_RETRIEVAL → not eligible
ALLOW + QUARANTINE_REQUIRED → not eligible
ALLOW + REBUILD_REQUIRED → not eligible
missing / mismatch / stale / unknown → DENY or DEFER
```

Even when every bounded classifier reports a positive result, the strongest
permitted meaning is **not** external-action authorization. A future positive
term should mean no more than `NO_BOUNDED_BLOCKER_FOUND` or
`ELIGIBLE_FOR_NEXT_GATE`, unless a separately authorized Action Gate later
establishes stronger semantics.

### 6.3 Character validation track

Character evidence work remains isolated from permission semantics:

- scenario labels cannot change truth status;
- reviewer agreement cannot create capability authority;
- presentation success cannot authorize identity/M3 mutation;
- automated review cannot be called independent human review;
- the existing `CHARACTER_RUNTIME_ACTIVATION_GATE` remains blocked until its
  own requirements are satisfied.

---

## 7. 🧪 Adversarial cases for readiness

A later contract is not ready unless it can specify deterministic handling for
at least these cases:

```text
BIND-SC-001  Capability ALLOW from request A + Privacy ALLOW_REFERENCE from request B
             → MISMATCH / NOT ELIGIBLE

BIND-SC-002  Capability ALLOW then lease live-head revision changes
             → STALE / NOT ELIGIBLE

BIND-SC-003  Privacy ALLOW_REFERENCE then material policy revision changes
             → STALE / NOT ELIGIBLE

BIND-SC-004  Capability ALLOW then requested data scope is enlarged
             → MISMATCH / NOT ELIGIBLE

BIND-SC-005  Same purpose but different branch after privacy evaluation
             → MISMATCH / NOT ELIGIBLE

BIND-SC-006  Required privacy result missing
             → DEFER_OR_DENY / NOT ELIGIBLE

BIND-SC-007  Unknown or unsupported gate contract version
             → DEFER_OR_DENY / NOT ELIGIBLE

BIND-SC-008  Capability DENY + Privacy ALLOW_REFERENCE
             → NOT ELIGIBLE

BIND-SC-009  Capability ALLOW + Privacy REBUILD_REQUIRED
             → NOT ELIGIBLE

BIND-SC-010  Identical fully bound canonical inputs repeated
             → deterministic byte-equivalent readiness decision

BIND-SC-011  Composition result presented as M3 or identity authority
             → REJECTED SEMANTICS

BIND-SC-012  Positive readiness result presented directly to a tool executor
             → REJECTED SEMANTICS / NO EXECUTION AUTHORITY
```

---

## 8. 🔁 Required metamorphic properties

```text
MT-BIND-001 Deny monotonicity
replace any required positive gate with a deny/remediation result
→ outcome cannot become more permissive

MT-BIND-002 Missing-gate monotonicity
remove one required gate result
→ outcome cannot become more permissive

MT-BIND-003 Scope-change invalidation
change purpose / operation / branch / data scope / side effects
→ previous positive readiness cannot remain reusable

MT-BIND-004 Freshness invalidation
change relevant lease or privacy policy revision
→ previous positive readiness cannot remain reusable

MT-BIND-005 Determinism
same admitted bound inputs + same contract versions
→ same readiness outcome

MT-BIND-006 No authority amplification
replace descriptive labels or presentation metadata only
→ capability / retrieval / tool / identity / M3 authority remains NONE
```

---

## 9. 🚫 Explicit non-goals

This selection does not authorize or select:

```text
P1-003 runtime implementation
bare-result authorization composition
retrieval execution
privacy remediation execution
deletion or redaction execution
quarantine or rebuild execution
Action Gate implementation
Tool Receipt runtime
tool execution
network / filesystem / database access
registry or privacy persistence
event or replay integration
belief mutation
relationship mutation
identity continuity runtime
Character runtime
M2 → M3 nomination or write
backend selection
migration
production deployment
```

---

## 10. ⛔ Stop conditions

Stop before selecting an implementation if any of these remain true:

- safe composition still depends on unbound bare results;
- common request identity cannot be verified deterministically;
- freshness semantics are implicit or rely on ambient state;
- a positive composition label can reasonably be read as execution permission;
- implementation would require hidden I/O or backend access;
- P1-001 or P1-002 frozen semantics would have to be silently broadened;
- Action Gate constitutional/relationship/commitment semantics are pulled into
  the small composer without their own contract;
- missing/unknown/mismatch cases cannot fail closed;
- implementation would create identity, M3, tool or deployment authority.

If resolving the binding gap requires changing a frozen P1 contract, that is a
new contract decision and requires separate explicit authorization. It is not
covered by this selection.

---

## 11. ✅ Exit criteria for the readiness block

This docs-only readiness block can be considered complete when a later review
can demonstrate all of the following without implementation:

```text
[ ] one canonical common-binding model is selected
[ ] stale-result invalidation semantics are explicit
[ ] bare-result composition is structurally impossible or explicitly rejected
[ ] fail-closed result vocabulary is fixed
[ ] positive result semantics cannot be mistaken for permission
[ ] adversarial BIND-SC cases have exact expected outcomes
[ ] metamorphic properties are frozen
[ ] P1-001 and P1-002 frozen contracts remain unchanged or any required change is separately proposed
[ ] Action Gate remains a separate future boundary
[ ] implementation preconditions are explicit
[ ] separate Owner GO is still required
```

Only after those conditions are met may the owner decide whether to assign a
future runtime-capable milestone number.

---

## 12. 🏁 Exact boundary

```text
Selected candidate:          H — NO RUNTIME MILESTONE YET
Selected bounded work:       CROSS_GATE_BINDING_AND_COMPOSITION_READINESS
Why now:                     existing P1 outputs lack common intent/freshness binding
Why not runtime composition: bare positive results can be mismatched or stale
Authority created:           NONE
Runtime effects:             NONE
Persistence:                 NONE
External side effects:       NONE
Identity authority:          NONE
M3 authority:                NONE
Tool authority:              NONE
Retrieval authority:         NONE
Deployment authority:        NONE
Implementation GO:           REQUIRED SEPARATELY
P1-003:                      NOT ASSIGNED
```

```text
Architecture first
→ common binding
→ freshness semantics
→ fail-closed composition contract
→ explicit Owner GO
→ only then possible implementation
```
