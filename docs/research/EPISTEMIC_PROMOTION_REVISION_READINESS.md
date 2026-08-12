# 🧭 Phase 4 — Epistemic Promotion & Revision Readiness

```text
Status:                              READINESS_READY · DOCS_ONLY
Date:                                2026-08-12
Phase:                               4 · EPISTEMIC PROMOTION & REVISION
Baseline main:                       0aad3b836c19c6165270e1af97173f0a3034d413
Tracking issue:                      #105
Phase 3 PCR-v0.1:                    IMPLEMENTED_BOUNDED
Implementation:                      NOT_STARTED
Owner GO:                            NOT_GRANTED
Runtime authority:                   NONE
P0-014 belief lifecycle authority:   UNCHANGED
P0-015 Evidence Gate authority:      UNCHANGED
Terminal reconsideration lineage:    NOT_IMPLEMENTED
Persistence authority:               NONE
Retrieval / Atlas authority:         NONE
Action / tool authority:             NONE
Identity / relationship authority:   NONE
Direct or indirect M3 write:         FORBIDDEN
Deployment authority:                NONE
```

> **READINESS_READY ≠ IMPLEMENTATION AUTHORITY.** This milestone defines the
> routing and ownership problem after PCR-v0.1. It does not create a new belief
> mutator, a second Evidence Gate, terminal-belief reopening, runtime wiring or
> Owner GO.

---

## 1. 🎯 Problem to solve

Phase 3 can now represent one exact provenance/claim record without turning it
into truth, evidence support or belief state. The repository also already has:

```text
P0-014 BeliefLifecycle
→ creates HYPOTHESIS beliefs
→ attaches evidence references
→ registers contradictions
→ revises non-terminal belief state

P0-015 EvidenceGatedBeliefLifecycle
→ is the sole owner of SUPPORTED / CONTRADICTED transitions
→ evaluates approved evidence-gate policy
→ emits deterministic replay-verifiable receipts
```

What is still missing is a canonical protocol for answering a narrower question:

> Given an exact caller-supplied PCR-v0.1 record, an optional exact caller-
> supplied binding to an existing belief, and an explicit epistemic intent,
> which existing or future protocol owner must handle the next step?

The missing component must **route**, not promote.

```text
CLAIM REPRESENTATION
≠ BELIEF CREATION
≠ BELIEF REVISION
≠ EVIDENCE-GATE OUTCOME
≠ TRUTH
```

---

## 2. 🔍 Live compatibility findings

### 2.1 P0-014 already owns ordinary belief creation and non-terminal revision

`src/mentaury/beliefs/contracts.py` and `lifecycle.py` currently establish:

```text
CREATE_BELIEF → initial status HYPOTHESIS
REVISE_BELIEF → ordinary non-terminal revision only
SUPPORTED / CONTRADICTED → require the separately owned P0-015 Evidence Gate
```

Phase 4 MUST NOT create a second command/event vocabulary that bypasses these
owners.

### 2.2 P0-015 is the sole support/contradiction owner

P0-015 owns `EvidenceGateOutcome.SUPPORTED` and
`EvidenceGateOutcome.CONTRADICTED`. It also owns policy selection, complete
record-set checks, independence rules, quality/freshness evaluation and the
replay-verifiable receipt.

Therefore Phase 4 MUST NOT:

```text
accept caller-supplied target_status = SUPPORTED / CONTRADICTED
accept EvidenceGateOutcome as a shortcut to permission
copy Evidence Gate thresholds or policy tables
count references as support
turn PCR evidence_refs into support status
```

The strongest Phase 4 route toward support is only:

```text
P0_015_EVIDENCE_GATE_REQUIRED
```

The gate still decides the result later.

### 2.3 Terminal beliefs cannot be revised in place under current contracts

`SUPPORTED`, `CONTRADICTED` and `SUPERSEDED` are terminal under the current
P0-014/P0-015 profile. Ordinary revision rejects them, and P0-015 rejects a new
gate evaluation on a terminal belief.

No current source/event schema defines a safe successor-lineage protocol that
can reopen or replace one of these records while preserving history.

Therefore Phase 4 v0.1 MUST NOT pretend terminal reconsideration exists. The
only honest route is:

```text
TERMINAL_RECONSIDERATION_LINEAGE_REQUIRED
```

This route is a missing-prerequisite signal, not authority to create a successor.

### 2.4 PCR→belief binding is not currently lossless

`PCR-v0.1` preserves provenance, ClaimClass, ClaimType, EpistemicRole,
attribution, basis/evidence references, scope and transfer limits.

Current `CREATE_BELIEF` stores only the P0-014 belief fields required by that
contract and does not itself preserve the complete PCR record or an exact
lineage link to it.

Therefore Phase 4 MUST NOT silently project a PCR record into `CREATE_BELIEF`.
A request to create a belief from an unbound PCR record must route only to:

```text
CLAIM_TO_BELIEF_BINDING_REQUIRED
```

A later separate contract must define that bridge without losing provenance or
laundering epistemic role.

### 2.5 PCR record identity is not authority

A `ProvenanceClaimRecord.input_fingerprint` is exact-input identity evidence
only. It is not proof that the caller obtained the record from an approved
runtime, and it is never a bearer permission token.

Phase 4 may bind the complete PCR value into its own deterministic input
fingerprint, but MUST NOT treat the PCR fingerprint as promotion authority.

---

## 3. 🧱 Required Phase 4 semantics

A future bounded primitive may only route an explicit intent into one of these
outcomes:

```text
RETAIN_CLAIM_ONLY
CLAIM_TO_BELIEF_BINDING_REQUIRED
P0_014_NON_TERMINAL_REVISION_REQUIRED
P0_015_EVIDENCE_GATE_REQUIRED
TERMINAL_RECONSIDERATION_LINEAGE_REQUIRED
DEFER
```

Each route means "this is the next required owner/prerequisite".

No route means:

```text
permission granted
command accepted
event emitted
belief mutated
SUPPORTED
CONTRADICTED
truth established
```

---

## 4. 🧭 One-concept / one-owner matrix

| Concept | Owner | Phase 4 role |
|---|---|---|
| General provenance/claim representation | PCR-v0.1 | exact caller-supplied input only |
| Claim→belief lossless binding | future separate contract | report missing prerequisite only |
| Belief creation | P0-014 | never duplicated; no command emitted |
| Non-terminal belief revision | P0-014 | route only |
| `SUPPORTED / CONTRADICTED` | P0-015 Evidence Gate | route only; never decide |
| Evidence policy / thresholds | P0-015 policy registry | never duplicated |
| Terminal belief reconsideration lineage | future separate contract | report missing prerequisite only |
| Truth | no Phase 4 owner | never claimed |
| Identity / M3 | separate governed layers | forbidden |
| Action / tools / retrieval | separate governed layers | forbidden |

---

## 5. 🚫 Explicit anti-laundering rules

Phase 4 MUST NOT accept or emit any field equivalent to:

```text
target_status = SUPPORTED
target_status = CONTRADICTED
truth = true
confidence = 0.82
reliability = 0.91
promotion_allowed = true
action_allowed = true
retrieval_allowed = true
identity_trait = true
m3_write = true
```

A caller may request an **intent**, not a terminal result.

The protocol must also preserve:

```text
ClaimClass ≠ ClaimType ≠ EpistemicRole ≠ BeliefStatus ≠ EvidenceGateOutcome
```

---

## 6. 🔐 Binding requirements

When an existing belief is supplied, the future primitive must require an exact
caller-supplied binding containing at least:

```text
belief_id
belief_revision
belief_status
belief_claim_type
claim_id
claim_record_fingerprint
```

The binding must match the supplied PCR record on:

```text
claim_id
ClaimType
PCR input_fingerprint
```

Mismatch fails closed. The match proves only internal consistency of the exact
caller-supplied routing input; it does not authenticate external belief state or
create mutation authority.

The later owning lifecycle/gate must still re-check the live state/revision when
executing its own command.

---

## 7. 🧪 Readiness threat model

A frozen EPR-v0.1 implementation contract must make at least these families
executable in a later authorized implementation:

```text
EPR-T01 PCR record treated as automatic belief promotion
EPR-T02 evidence_refs treated as SUPPORTED evidence
EPR-T03 caller chooses SUPPORTED / CONTRADICTED directly
EPR-T04 router duplicates Evidence Gate policy/threshold logic
EPR-T05 PCR→belief conversion drops provenance/epistemic role silently
EPR-T06 forged/mismatched belief binding is accepted
EPR-T07 stale belief revision is represented as execution authority
EPR-T08 terminal belief is revised/re-gated in place
EPR-T09 terminal reconsideration route creates a successor implicitly
EPR-T10 ClaimClass / ClaimType / EpistemicRole / BeliefStatus collapse
EPR-T11 route or fingerprint is replayed as permission
EPR-T12 successful route grants retrieval/action/identity/M3/deployment authority
```

Required metamorphic families:

```text
EPR-M01 PCR field change changes routing input fingerprint
EPR-M02 intent change changes route/fingerprint when semantics differ
EPR-M03 belief revision change changes fingerprint
EPR-M04 belief status change can change route without changing PCR record
EPR-M05 claim-id binding mismatch fails closed
EPR-M06 ClaimType binding mismatch fails closed
EPR-M07 PCR fingerprint binding mismatch fails closed
EPR-M08 terminal vs non-terminal binding changes revision route
EPR-M09 reason-ref count/order cannot create support authority
EPR-M10 duplicate/non-canonical reason refs fail closed
```

Purity requirements for a later implementation:

```text
EPR-P01 no network
EPR-P02 no filesystem
EPR-P03 no database/persistence
EPR-P04 no environment/ambient clock
EPR-P05 no model/LLM/retriever/Atlas/graph
EPR-P06 no command/event emission or lifecycle/gate invocation
EPR-P07 no belief/identity/M3 mutation
EPR-P08 deterministic output for exact typed input
```

---

## 8. ✅ Readiness decision

```text
PHASE_4_EPISTEMIC_PROMOTION_REVISION_READINESS = READY
PHASE_4_IMPLEMENTATION = NOT_STARTED
PHASE_4_OWNER_GO = NOT_GRANTED
PHASE_4_RUNTIME = NOT_AUTHORIZED
```

The selected bounded design direction is a pure routing primitive, not a
promotion engine. Candidate selection and the exact EPR-v0.1 contract may now be
frozen docs-only. No code is authorized by this readiness result.