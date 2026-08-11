# 🧩 Non-Projection Runtime Composition Readiness

```text
Status:                         FROZEN_DOCS · DOCS_ONLY · READINESS_CONTRACT
Version:                        0.1
Date:                           2026-08-12
Review tier:                    TIER_A
Readiness result:               READY
Selected strategy:              SAME_ATTEMPT_SHADOW_COORDINATOR
Owning classifier contract:     NPG-v0.1
Owning envelope contract:       AIE-v0.1
Runtime implementation:         NOT_AUTHORIZED
Runtime activation:             NOT_AUTHORIZED
Phase 2:                        NOT_STARTED
Phase 2 Owner GO:               NOT_GRANTED
P1-004 assignment:              NOT_ASSIGNED
Persistence authority:          NONE
Retrieval authority:            NONE
Tool authority:                 NONE
Action authority:               NONE
Identity authority:             NONE
Relationship authority:         NONE
Direct or indirect M3 write:    FORBIDDEN
Deployment authority:           NONE
```

> **READINESS READY ≠ RUNTIME IMPLEMENTATION.**
>
> This document answers the architecture question required before any bounded
> Non-Projection composition implementation: **WHO** may call NPG in a governed
> composition path, **WHAT** exact values may be supplied, and **WHERE** the
> result may go. It grants no code, runtime, retrieval, tool, action, identity,
> relationship, persistence, M3 or deployment authority.

---

## 1. 🎯 Decision

The selected architecture is:

```text
SAME_ATTEMPT_SHADOW_COORDINATOR
```

A future dedicated coordinator may call the already-implemented pure
`classify_non_projection(...)` only inside one explicit evaluation attempt. The
coordinator owns the call boundary and returns a bound **shadow observation**.
It does not turn the classifier result into permission.

Rejected alternatives:

```text
DIRECT_RUNTIME_CALLS_FROM_ARBITRARY_COMPONENTS      = REJECTED
CALLER_SUPPLIED_PRIOR_NON_PROJECTION_RESULT         = REJECTED
BARE_RESULT_REUSE_ACROSS_ATTEMPTS                   = REJECTED
PASS_ATTRIBUTED_AS_AUTHORIZATION_TOKEN              = REJECTED
DYNAMIC_DESTINATION_ROUTING_FROM_NPG_RESULT         = REJECTED
HIDDEN_RETRIEVAL_OR_IDENTITY_LOOKUP                 = REJECTED
```

---

## 2. 👤 WHO may call NPG

The public Python import surface is not an authority grant.

```text
public function visibility ≠ authorized runtime caller
```

The only future authoritative composition caller role selected by this
readiness contract is:

```text
NON_PROJECTION_SHADOW_COORDINATOR
```

That role is a bounded composition component, not an Action Gate and not a
runtime root. Until a separate Owner GO and implementation milestone exist, the
role is documentary only.

Explicitly forbidden direct runtime callers include:

- Action Gate or action executors;
- retrieval / Atlas / search components;
- model or LLM clients;
- identity, relationship or Character runtime;
- M3 or other persistent self-model mutation paths;
- tools, plugins, subprocesses or network clients;
- database/filesystem persistence adapters;
- background autonomous loops or schedulers;
- UI/transport layers treating NPG as permission.

Tests and research harnesses may invoke the pure classifier for verification,
but those calls are not runtime-composition evidence and create no authority.

---

## 3. 📦 WHAT caller input is admissible

The future coordinator may admit only:

```text
evaluation_id
proposal_ref
exact AttributedInterpretationEnvelope (AIE-v0.1)
exact NonProjectionBudget
```

`evaluation_id` and `proposal_ref` are correlation/provenance references only.
They are not truth, identity, capability or execution authority.

The classifier call itself remains exactly:

```python
classify_non_projection(
    envelope=context.envelope,
    budget=context.budget,
)
```

The coordinator must not accept or synthesize any of the following as runtime
inputs:

```text
prior NonProjectionResult
caller-supplied NPG fingerprint
raw source text
retriever / Atlas handle
model / LLM client
network / filesystem / database handle
ambient clock / environment
identity or relationship state
M3 state or mutation handle
Action Gate result or executor
tool handle / plugin / subprocess
caller-selected destination
```

The caller must supply already-typed attributed values. The coordinator does not
retrieve, interpret free text, discover provenance, or infer hidden authority.

---

## 4. 📤 WHERE the result may go

The only selected output path is:

```text
same evaluation attempt
→ bound Non-Projection shadow observation
→ immediate caller / test or diagnostic inspection
```

The observation must preserve the exact `NonProjectionResult` and bind it to the
same `evaluation_id` and `proposal_ref`. It is evidence about one bounded
classification attempt only.

It may not be routed directly to:

```text
Action Gate
retrieval
Atlas
model invocation
tool execution
external side effect
identity or relationship update
M3 nomination or write
persistent authorization cache
deployment switch
```

Persistence of the observation is not authorized by this contract. A later
separate persistence authority may retain it for audit provenance, but even
then it must never become a replayable permission token.

---

## 5. 🔒 Same-attempt and replay boundary

A valid composition attempt has the form:

```text
new evaluation_id
+ exact proposal_ref
+ exact caller-supplied AIE-v0.1
+ exact admitted budget
→ coordinator invokes NPG-v0.1 now
→ coordinator receives exact result now
→ coordinator returns bound shadow observation now
```

Forbidden:

```text
old PASS_ATTRIBUTED + new proposal
old PASS_ATTRIBUTED + changed envelope
old PASS_ATTRIBUTED + changed budget
old fingerprint + claimed equivalent request
cached result + new evaluation_id
```

Any change to the admitted envelope or budget requires a complete new NPG
classification. The classifier fingerprint is integrity evidence, not a bearer
token.

---

## 6. 🚦 Result semantics are not re-owned

The coordinator must not create a second authority owner for Non-Projection
semantics.

It preserves the classifier result exactly:

```text
PASS_ATTRIBUTED
REVISE_REQUIRED
CONTESTED
DEFER
REJECT
```

No new `SUPPORTED`, `AUTHORIZED`, `ALLOW`, `TRUSTED`, or identity state is
inferred from those decisions.

Most importantly:

```text
PASS_ATTRIBUTED
= no bounded Non-Projection blocker found for this exact admitted proposal

PASS_ATTRIBUTED
≠ truth proof
≠ autobiography
≠ stable identity trait
≠ relationship / consent authority
≠ capability
≠ Action Gate PASS
≠ retrieval permission
≠ tool permission
≠ execution permission
≠ deployment permission
```

Negative or uncertain results also do not authorize automatic remediation,
retrieval, rewriting, retry loops or mutation.

---

## 7. 🧯 Fail-closed composition behavior

Future composition must fail closed for:

- NPG contract errors;
- unsupported envelope or contract versions;
- missing or malformed context refs;
- attempts to supply a prior result;
- attempts to supply a fingerprint as authority;
- any hidden I/O dependency;
- any dynamic destination request;
- any attempt to reinterpret `PASS_ATTRIBUTED` as broader authority.

A composition-layer failure can prevent formation of a shadow observation. It
must never synthesize a positive NPG result.

---

## 8. 🛡️ Threat model

| ID | Adversarial scenario | Required property |
|---|---|---|
| NRC-T01 | Action Gate directly calls NPG and treats PASS as permission | forbidden caller; no authority |
| NRC-T02 | caller injects an old `NonProjectionResult` | no API slot; reject/defer composition |
| NRC-T03 | PASS from proposal A reused for proposal B | same-attempt binding invalid; re-run |
| NRC-T04 | envelope changes after classification | prior observation invalid |
| NRC-T05 | budget changes after classification | prior observation invalid |
| NRC-T06 | fingerprint used as bearer token | forbidden; fingerprint is integrity evidence only |
| NRC-T07 | coordinator retrieves missing source data | forbidden hidden I/O |
| NRC-T08 | coordinator reads identity/relationship/M3 state | forbidden boundary crossing |
| NRC-T09 | caller requests result destination `tool` or `action` | dynamic destination forbidden |
| NRC-T10 | PASS is promoted to truth/identity/relationship state | authority laundering forbidden |
| NRC-T11 | non-positive result triggers automatic remediation | no action/remediation authority |
| NRC-T12 | background loop repeatedly re-evaluates without a new admitted obligation | no scheduler/autonomous-loop authority |

---

## 9. 🔁 Metamorphic requirements

```text
NRC-M01 identical AIE + identical budget → identical NPG result
NRC-M02 changed AIE → prior observation cannot be reused
NRC-M03 changed budget → prior observation cannot be reused
NRC-M04 changed proposal_ref → old bound observation is not valid for new proposal
NRC-M05 changed evaluation_id → requires a new same-attempt classification
NRC-M06 adding a requested destination cannot create authority
NRC-M07 PASS_ATTRIBUTED cannot be strengthened by wrapper metadata
NRC-M08 missing/unknown context cannot become positive by composition
NRC-M09 persistence/caching cannot convert evidence into authority
NRC-M10 composition adds no authority beyond exact NPG-v0.1 semantics
```

---

## 10. ✅ Readiness conclusion

```text
NON_PROJECTION_RUNTIME_COMPOSITION_READINESS = READY
SELECTED_STRATEGY                            = SAME_ATTEMPT_SHADOW_COORDINATOR
WHO                                           = NON_PROJECTION_SHADOW_COORDINATOR_ONLY
WHAT                                          = EXACT_AIE_V0_1 + EXACT_BUDGET + NON_AUTHORITY_REFS
WHERE                                         = SAME_ATTEMPT_BOUND_SHADOW_OBSERVATION_ONLY
PRIOR_RESULT_INPUT                            = FORBIDDEN
RESULT_REPLAY_AS_AUTHORITY                    = FORBIDDEN
RUNTIME_IMPLEMENTATION                        = NOT_AUTHORIZED
RUNTIME_ACTIVATION                            = NOT_AUTHORIZED
PHASE_2_OWNER_GO                              = NOT_GRANTED
P1_004                                        = NOT_ASSIGNED
```

This is sufficient to freeze the separate Phase 1 implementation contract.
No implementation or Owner GO follows automatically.
