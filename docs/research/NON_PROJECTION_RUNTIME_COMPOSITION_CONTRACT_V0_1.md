# 🧬 Non-Projection Runtime Composition Contract v0.1

```text
Status:                              FROZEN_DOCS · DOCS_ONLY · IMPLEMENTATION_CONTRACT
Contract version:                    NPG-COMP-v0.1
Date:                                2026-08-12
Review tier:                         TIER_A
Owning readiness:                    NON_PROJECTION_RUNTIME_COMPOSITION_READINESS.md
Owning classifier contract:          NPG-v0.1
Envelope version:                    AIE-v0.1
Selected strategy:                   SAME_ATTEMPT_SHADOW_COORDINATOR
Future caller role:                  NON_PROJECTION_SHADOW_COORDINATOR
Phase 2 implementation:              NOT_AUTHORIZED
Phase 2 Owner GO:                    NOT_GRANTED
Runtime activation:                  NOT_AUTHORIZED
P1-004 assignment:                   NOT_ASSIGNED
Action Gate authority:               NONE
Retrieval authority:                 NONE
Tool authority:                      NONE
Identity authority:                  NONE
Relationship authority:              NONE
Persistence authority:               NONE
Direct or indirect M3 write:         FORBIDDEN
Deployment authority:                NONE
```

> **CONTRACT FROZEN ≠ OWNER GO.**
>
> This document freezes the Phase 1 composition boundary only. It authorizes no
> source/runtime code and no runtime wiring. A separate explicit Owner GO is
> required before any Phase 2 implementation may begin.

---

## 1. 🎯 Contract purpose

The future bounded component answers one question:

> Can the already-implemented pure NPG-v0.1 classifier be invoked inside one
> explicit shadow evaluation attempt while preserving caller attribution,
> preventing result replay, and preventing any expansion from classification
> evidence into runtime/action/identity authority?

The answer is yes under the exact contract below.

---

## 2. 🔒 Frozen semantic constants

```text
COMPOSITION_CONTRACT_VERSION = "NPG-COMP-v0.1"
NPG_CONTRACT_VERSION         = "NPG-v0.1"
ENVELOPE_VERSION             = "AIE-v0.1"
CALLER_ROLE                  = "NON_PROJECTION_SHADOW_COORDINATOR"
OUTPUT_ROLE                  = "BOUND_NON_PROJECTION_SHADOW_OBSERVATION"
SOURCE_INPUT_SCOPE           = "CALLER_SUPPLIED_TYPED_VALUES_ONLY"
AUTHORITY_CEILING            = "NONE"
PERSISTENCE_AUTHORITY        = "NONE"
```

The caller may not override these semantic constants.

---

## 3. 📦 Reserved future package and public API

If and only if a later explicit Owner GO authorizes Phase 2 implementation, the
reserved package is:

```text
src/mentaury/composition/non_projection_shadow/__init__.py
src/mentaury/composition/non_projection_shadow/contracts.py
src/mentaury/composition/non_projection_shadow/coordinator.py
```

The exact future public function is frozen as:

```python
def evaluate_non_projection_shadow(
    *,
    context: NonProjectionShadowContext,
) -> NonProjectionShadowObservation:
    ...
```

No service, worker, scheduler, transport, persistence backend, retriever, Atlas
adapter, model client, tool adapter, identity store or Action Gate belongs to
`NPG-COMP-v0.1`.

---

## 4. 👤 WHO — exact caller authority

The only runtime-composition role permitted by this contract to invoke
`classify_non_projection(...)` is:

```text
NON_PROJECTION_SHADOW_COORDINATOR
```

This is an architecture role, not a claim that implementation exists.

The future coordinator may be exercised by tests or a separately authorized
shadow harness. It is not itself a runtime root and may not self-schedule.

Forbidden direct authoritative runtime callers:

```text
ACTION_GATE
RETRIEVER
ATLAS
MODEL_OR_LLM_CLIENT
IDENTITY_RUNTIME
RELATIONSHIP_RUNTIME
CHARACTER_RUNTIME
M3_MUTATOR
TOOL_EXECUTOR
PLUGIN_OR_SUBPROCESS
DATABASE_OR_FILESYSTEM_ADAPTER
NETWORK_CLIENT
BACKGROUND_COGNITIVE_LOOP
UI_OR_TRANSPORT_PERMISSION_PATH
```

Direct imports for unit tests do not constitute authoritative composition use.

---

## 5. 📥 WHAT — exact input contract

The future immutable context is semantically frozen as:

```python
@dataclass(frozen=True, slots=True)
class NonProjectionShadowContext:
    evaluation_id: str
    proposal_ref: str
    envelope: AttributedInterpretationEnvelope
    budget: NonProjectionBudget
```

### 5.1 `evaluation_id`

- required non-empty caller-supplied correlation reference;
- unique within the enclosing shadow evaluation domain;
- provenance/correlation only;
- not truth, identity, capability or authority.

### 5.2 `proposal_ref`

- required non-empty reference to the exact proposal being classified;
- must remain stable for the attempt;
- correlation/provenance only;
- does not replace `ProjectionIntent` or any field inside `AIE-v0.1`.

### 5.3 `envelope`

Must be an exact already-typed `AttributedInterpretationEnvelope` admitted by
`NPG-v0.1` / `AIE-v0.1`.

The coordinator must not retrieve, infer or repair missing provenance or hidden
intent. It receives the value and calls the classifier.

### 5.4 `budget`

Must be an exact `NonProjectionBudget`. Any frozen hard-cap contract error
remains an NPG contract error; the composition layer must not weaken or silently
expand budgets.

### 5.5 Forbidden inputs

The future context and function must expose no slot for:

```text
prior NonProjectionResult
caller-supplied input_fingerprint
caller-supplied contract/profile authority
raw source text
callbacks
ambient clock/environment
retriever / Atlas handle
model / LLM client
filesystem/database/network handle
identity or relationship state
M3 state or mutation handle
Action Gate result or executor
tool/plugin/subprocess handle
caller-selected output destination
retry/remediation policy
```

---

## 6. ⚙️ Exact evaluation algorithm

The future implementation algorithm is frozen semantically as:

```text
1. strictly admit NonProjectionShadowContext
2. verify local NPG-COMP-v0.1 / NPG-v0.1 / AIE-v0.1 constants
3. invoke classify_non_projection exactly once for this attempt
4. do not accept a prior result and do not perform hidden I/O
5. preserve the exact NonProjectionResult without semantic translation
6. bind that result to evaluation_id + proposal_ref
7. return one immutable NonProjectionShadowObservation
```

The classifier invocation is exactly:

```python
result = classify_non_projection(
    envelope=context.envelope,
    budget=context.budget,
)
```

No recursive call, automatic retry, retrieval, repair or mutation is authorized.

---

## 7. 📤 WHERE — exact output contract

The future immutable output is semantically frozen as:

```python
@dataclass(frozen=True, slots=True)
class NonProjectionShadowObservation:
    evaluation_id: str
    proposal_ref: str
    result: NonProjectionResult
    composition_contract_version: str = "NPG-COMP-v0.1"
```

The observation is an immediate same-attempt return value only.

Allowed destination under this contract:

```text
immediate enclosing shadow/test evaluation caller
```

Explicitly not authorized:

```text
persistent authorization cache
Action Gate
retrieval / Atlas
model invocation
tool execution
external side effect
identity or relationship mutation
M3 nomination or write
Character activation
runtime deployment switch
```

Persistence is not part of Phase 2. If a later separate milestone authorizes
audit persistence, the persisted observation remains provenance only and is
never replayable authority.

---

## 8. 🪞 Result preservation and authority ceiling

`NonProjectionShadowObservation.result` is the exact `NonProjectionResult`.
The composition layer owns no second decision vocabulary.

```text
PASS_ATTRIBUTED
REVISE_REQUIRED
CONTESTED
DEFER
REJECT
```

remain owned by NPG-v0.1.

The wrapper must never emit or imply:

```text
AUTHORIZED
ALLOW_ACTION
ALLOW_RETRIEVAL
SUPPORTED_TRUTH
IDENTITY_CONFIRMED
RELATIONSHIP_CONFIRMED
CONSENT_CONFIRMED
M3_APPROVED
```

For positive output:

```text
PASS_ATTRIBUTED
= at most no bounded Non-Projection blocker found for this exact admitted proposal
```

Nothing stronger follows.

---

## 9. 🔁 Same-attempt invalidation and replay rules

A shadow observation is bound to the exact evaluation attempt.

A complete new NPG call is required when any of these change:

```text
evaluation_id
proposal_ref
envelope or any nested AIE field
budget or any budget field
NPG contract version
AIE version
composition contract version
```

The NPG `input_fingerprint` may be retained inside the exact result for integrity
checking. It is never a bearer token and cannot authorize reuse.

Forbidden replay forms:

```text
old result → new context
old result → new proposal
old result → new budget
old fingerprint → claimed equivalent input
persisted positive observation → execution permission
```

---

## 10. 🧯 Failure semantics

Composition must fail closed.

### Contract/admission failure

If context admission fails, versions are unsupported, or the underlying NPG call
raises `NonProjectionContractError`, the coordinator must not fabricate a
`PASS_ATTRIBUTED` result or weaker surrogate positive.

### Underlying non-positive NPG result

`REVISE_REQUIRED`, `CONTESTED`, `DEFER`, and `REJECT` are returned unchanged
inside the bound observation when the classifier itself successfully returns
them.

They do not trigger automatic remediation, retries, retrieval or mutation.

### Hidden dependency attempt

Any implementation that needs network, filesystem, database, Atlas, model,
identity, relationship, tool or ambient environment access violates this
contract and must not be admitted as `NPG-COMP-v0.1`.

---

## 11. 🧱 Purity and side-effect contract

A conforming Phase 2 implementation must prove:

```text
no network I/O
no filesystem I/O
no database I/O
no environment-variable reads
no ambient clock
no randomness
no model/LLM calls
no retrieval/Atlas calls
no identity/relationship/M3 reads or writes
no Action Gate calls
no tool/plugin/subprocess calls
no persistence
no logging side effect required for correctness
no scheduler/background-loop integration
```

All behavior must derive from explicit immutable values and the already-pure
NPG-v0.1 classifier.

---

## 12. 🛡️ Frozen adversarial matrix

```text
NRC-T01 arbitrary component direct-call authority laundering
NRC-T02 prior-result injection
NRC-T03 cross-proposal replay
NRC-T04 changed-envelope replay
NRC-T05 changed-budget replay
NRC-T06 fingerprint bearer-token laundering
NRC-T07 hidden retrieval / Atlas I/O
NRC-T08 identity / relationship / M3 boundary crossing
NRC-T09 caller-selected action/tool destination
NRC-T10 PASS_ATTRIBUTED truth/identity/relationship laundering
NRC-T11 automatic remediation from non-positive result
NRC-T12 autonomous retry / scheduler loop
```

A later implementation must include executable tests covering all twelve.

---

## 13. 🔁 Frozen metamorphic matrix

```text
NRC-M01 identical typed input + budget → identical underlying NPG result
NRC-M02 envelope mutation invalidates prior observation
NRC-M03 budget mutation invalidates prior observation
NRC-M04 proposal mutation invalidates prior binding
NRC-M05 evaluation attempt change requires a fresh call
NRC-M06 destination metadata cannot amplify authority
NRC-M07 wrapper metadata cannot strengthen PASS_ATTRIBUTED
NRC-M08 unknown/missing state cannot become positive by composition
NRC-M09 persistence/cache cannot transform evidence into authority
NRC-M10 composition authority ceiling remains NONE
```

A later implementation must include executable tests covering all ten.

---

## 14. 🔍 Compatibility stop

Before any future Phase 2 implementation begins, a fresh preflight must verify:

- `NPG-v0.1` and `AIE-v0.1` remain unchanged or compatible;
- `classify_non_projection` still has the frozen API;
- no competing runtime composition contract has become authoritative;
- no active same-scope writer exists;
- governance/ruleset and required CI remain intact;
- the explicit Owner GO is for exactly `NPG-COMP-v0.1`.

If any assumption changed:

```text
STOP_AND_RECONCILE
```

No consumed NPG-v0.1 implementation authorization may be reused.

---

## 15. ✅ Frozen Phase 1 state

```text
PHASE_1_NON_PROJECTION_RUNTIME_COMPOSITION = COMPLETE
NON_PROJECTION_RUNTIME_COMPOSITION_READINESS = READY
NON_PROJECTION_RUNTIME_COMPOSITION_STRATEGY = SAME_ATTEMPT_SHADOW_COORDINATOR
NON_PROJECTION_RUNTIME_COMPOSITION_CONTRACT = FROZEN_DOCS
NON_PROJECTION_RUNTIME_COMPOSITION_CONTRACT_VERSION = NPG-COMP-v0.1
WHO = NON_PROJECTION_SHADOW_COORDINATOR_ONLY
WHAT = EXACT_CALLER_SUPPLIED_AIE_V0_1_AND_NON_PROJECTION_BUDGET
WHERE = SAME_ATTEMPT_BOUND_SHADOW_OBSERVATION_ONLY
PRIOR_RESULT_INPUT = FORBIDDEN
RESULT_REPLAY_AS_AUTHORITY = FORBIDDEN
PHASE_2_IMPLEMENTATION = NOT_STARTED
PHASE_2_OWNER_GO = NOT_GRANTED
NON_PROJECTION_RUNTIME = NOT_AUTHORIZED
P1_004 = NOT_ASSIGNED
ACTION_GATE = NOT_AUTHORIZED
RETRIEVAL_EXECUTION = NOT_AUTHORIZED
TOOL_EXECUTION = NOT_AUTHORIZED
IDENTITY_RUNTIME = NOT_AUTHORIZED
RELATIONSHIP_RUNTIME = NOT_AUTHORIZED
DIRECT_OR_INDIRECT_M3_WRITE = FORBIDDEN
RUNTIME_DEPLOYMENT = NOT_AUTHORIZED
```

**Mandatory stop:** freeze ends Phase 1. The next possible step is a new, explicit
Owner GO decision for exactly `NPG-COMP-v0.1`; no implementation follows from
this document alone.
