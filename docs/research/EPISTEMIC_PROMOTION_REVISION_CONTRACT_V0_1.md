# 🧭 Epistemic Promotion & Revision — Frozen Routing Contract v0.1

```text
Status:                              FROZEN_DOCS · DOCS_ONLY · IMPLEMENTATION_CONTRACT
Contract version:                    EPR-v0.1
Date:                                2026-08-12
Phase:                               4 · EPISTEMIC PROMOTION & REVISION
Review tier:                         TIER_A
Owning readiness:                    EPISTEMIC_PROMOTION_REVISION_READINESS.md
Owning candidate selection:          EPISTEMIC_PROMOTION_REVISION_CANDIDATE_SELECTION.md
Candidate:                           PURE_EPISTEMIC_CHANGE_ROUTER
Implementation:                      NOT_STARTED
Owner GO:                            NOT_GRANTED
Implementation authorization:        NONE
Runtime activation:                  NOT_AUTHORIZED
Belief mutation authority:           NONE
P0-014 authority:                    UNCHANGED
P0-015 Evidence Gate authority:      UNCHANGED
Terminal reconsideration lineage:    NOT_IMPLEMENTED
Source admission authority:          NONE
Retrieval / Atlas authority:         NONE
Identity / relationship authority:   NONE
Direct or indirect M3 write:         FORBIDDEN
Persistence authority:               NONE
Network/filesystem/database I/O:     NONE
Tool / Action Gate authority:        NONE
Deployment authority:                NONE
```

> **CONTRACT FROZEN ≠ OWNER GO.**
>
> EPR-v0.1 freezes one pure routing primitive only. It cannot create/revise a
> belief, invoke P0-014/P0-015, select `SUPPORTED/CONTRADICTED`, reopen terminal
> beliefs, persist, retrieve, act, mutate identity/M3, or deploy.

---

## 1. 🎯 Bounded purpose

A future implementation answers exactly one question:

> For these exact caller-supplied routing inputs, which existing or future
> protocol owner/prerequisite must handle the next epistemic step?

The primitive returns a deterministic route. It does not perform that route.

Strongest successful outcome:

```text
VALID DETERMINISTIC ROUTE
```

Semantic ceiling:

```text
VALID ROUTE
≠ admitted source
≠ claim truth
≠ belief creation
≠ belief revision acceptance
≠ EvidenceGateOutcome
≠ SUPPORTED / CONTRADICTED
≠ terminal successor creation
≠ capability / Action Gate PASS
≠ retrieval / Atlas permission
≠ tool / execution permission
≠ identity / relationship authority
≠ M3 nomination/write
≠ deployment permission
```

---

## 2. 🔒 Frozen constants and hard caps

```text
EPISTEMIC_CHANGE_CONTRACT_VERSION = "EPR-v0.1"
CANONICAL_PROFILE                 = "MENTAURY_CANONICAL_JSON_V1"
INPUT_FINGERPRINT_DOMAIN          = "MENTAURY_EPISTEMIC_CHANGE_INPUT_V1"

HARD_MAX_STRING_BYTES             = 4096
HARD_MAX_TUPLE_ITEMS              = 512
HARD_MAX_CANONICAL_INPUT_BYTES    = 262144
```

Canonicalization must reuse
`mentaury.contracts.canonical_json.canonical_json_bytes` and verify live
`PROFILE_NAME == "MENTAURY_CANONICAL_JSON_V1"` before returning a plan.

The caller cannot override the contract version, canonical profile, fingerprint
domain or hard caps and cannot provide the final routing input fingerprint.

---

## 3. 📦 Reserved package and exact public API

If and only if a later separate Owner GO authorizes implementation, the exact
bounded package is:

```text
src/mentaury/epistemic_change/__init__.py
src/mentaury/epistemic_change/contracts.py
src/mentaury/epistemic_change/router.py
```

Exact public function:

```python
def route_epistemic_change(
    *,
    record: ProvenanceClaimRecord,
    belief: BeliefBinding | None,
    request: EpistemicChangeRequest,
    budget: EpistemicChangeBudget,
) -> EpistemicChangePlan:
    ...
```

The function accepts no repository, lifecycle, gate, command bus, event writer,
clock, callback, retriever, model or action handle.

Forbidden public inputs include:

```text
raw source text
source admission result
requested BeliefStatus
target_status
EvidenceGateOutcome
EvidenceGateReceipt as permission
EvidenceGatePolicy / thresholds
prior EpistemicChangePlan as authority
caller-supplied routing fingerprint
confidence / probability / reliability score
clock / environment / callback
retriever / Atlas / graph / database / filesystem
model / LLM client
tool / Action Gate handle
identity / relationship registry
```

---

## 4. ♻️ Reused owners and exact class identities

EPR-v0.1 must reuse exact current class identities rather than creating parallel
status vocabularies:

```python
from mentaury.claims import ProvenanceClaimRecord
from mentaury.epistemic_types import ClaimType
from mentaury.beliefs.contracts import (
    BeliefStatus,
    belief_status_transition_allowed,
)
```

The implementation must not create replacements for `ClaimType`, `BeliefStatus`
or Evidence Gate outcome classes.

Terminality is owned by P0-014/P0-015 semantics. EPR-v0.1 must determine whether
an exact `BeliefStatus` is terminal using the existing owner behavior rather
than widening the transition map:

```text
terminal(status)
= not belief_status_transition_allowed(status, status)
```

Under the currently frozen owner semantics this identifies:

```text
SUPPORTED
CONTRADICTED
SUPERSEDED
```

EPR-v0.1 does not change that set.

---

## 5. 🧭 New routing-only vocabularies

### 5.1 Explicit caller intent

```text
EpistemicIntent:
RETAIN_CLAIM
CREATE_BELIEF_FROM_CLAIM
REVISE_EXISTING_BELIEF
SEEK_EVIDENCE_GATE_DECISION
RECONSIDER_TERMINAL_BELIEF
DEFER
```

No intent specifies a target belief status.

### 5.2 Route

```text
EpistemicRoute:
RETAIN_CLAIM_ONLY
CLAIM_TO_BELIEF_BINDING_REQUIRED
P0_014_NON_TERMINAL_REVISION_REQUIRED
P0_015_EVIDENCE_GATE_REQUIRED
TERMINAL_RECONSIDERATION_LINEAGE_REQUIRED
DEFER
```

### 5.3 Next owner/prerequisite

```text
EpistemicOwner:
PCR_V0_1
FUTURE_CLAIM_TO_BELIEF_BINDING
P0_014_BELIEF_LIFECYCLE
P0_015_EVIDENCE_GATE
FUTURE_TERMINAL_RECONSIDERATION_LINEAGE
NONE
```

These are labels only. They contain no capability, handle or invocation token.

### 5.4 Route reason

```text
EpistemicRouteReason:
CALLER_RETAINED_CLAIM
CLAIM_BINDING_PREREQUISITE
NON_TERMINAL_REVISION_OWNER
EVIDENCE_GATE_OWNER
TERMINAL_LINEAGE_PREREQUISITE
CALLER_DEFERRED
INTENT_PRECONDITION_UNMET
```

---

## 6. 📦 Exact immutable contracts

All values below are `@dataclass(frozen=True, slots=True)` and expose exact
canonical `to_value()` projections. Extension dictionaries are forbidden.

```python
@dataclass(frozen=True, slots=True)
class BeliefBinding:
    belief_id: str
    belief_revision: int
    belief_status: BeliefStatus
    belief_claim_type: ClaimType
    claim_id: str
    claim_record_fingerprint: str

@dataclass(frozen=True, slots=True)
class EpistemicChangeRequest:
    request_id: str
    intent: EpistemicIntent
    reason_refs: tuple[str, ...]

@dataclass(frozen=True, slots=True)
class EpistemicChangeBudget:
    max_string_bytes: int
    max_tuple_items: int
    max_canonical_input_bytes: int

@dataclass(frozen=True, slots=True)
class EpistemicChangePlan:
    contract_version: str
    request_id: str
    route: EpistemicRoute
    next_owner: EpistemicOwner
    reason: EpistemicRouteReason
    record_fingerprint: str
    belief_id: str | None
    belief_revision: int | None
    routing_input_fingerprint: str
```

`EpistemicChangePlan` contains no `BeliefStatus`, Evidence Gate outcome,
command/event or permission result.

---

## 7. 🔐 Exact binding rules

When `belief is None`, no existing belief authority is implied.

When `belief` is supplied, it must match the exact PCR record on all three
caller-supplied association fields:

```text
belief.claim_id == record.claim.claim_id
belief.belief_claim_type is record.claim.claim_type
belief.claim_record_fingerprint == record.input_fingerprint
```

Any mismatch raises `EpistemicChangeBindingError` and returns no plan.

The successful match means only:

```text
exact routing inputs are internally bound
```

It does not prove:

```text
live belief existence
live belief revision
historical creation from this PCR record
external provenance authenticity
mutation permission
```

Any later P0-014/P0-015 command must independently validate its live state and
revision under its own existing contract.

Fingerprint values supplied inside `BeliefBinding` must be exact lowercase
64-character SHA-256 hex strings. This validates shape, not authority.

---

## 8. 🧭 Frozen routing table

### 8.1 No belief binding

| Intent | Route | Next owner | Reason |
|---|---|---|---|
| `RETAIN_CLAIM` | `RETAIN_CLAIM_ONLY` | `PCR_V0_1` | `CALLER_RETAINED_CLAIM` |
| `CREATE_BELIEF_FROM_CLAIM` | `CLAIM_TO_BELIEF_BINDING_REQUIRED` | `FUTURE_CLAIM_TO_BELIEF_BINDING` | `CLAIM_BINDING_PREREQUISITE` |
| `SEEK_EVIDENCE_GATE_DECISION` | `CLAIM_TO_BELIEF_BINDING_REQUIRED` | `FUTURE_CLAIM_TO_BELIEF_BINDING` | `CLAIM_BINDING_PREREQUISITE` |
| `REVISE_EXISTING_BELIEF` | `DEFER` | `NONE` | `INTENT_PRECONDITION_UNMET` |
| `RECONSIDER_TERMINAL_BELIEF` | `DEFER` | `NONE` | `INTENT_PRECONDITION_UNMET` |
| `DEFER` | `DEFER` | `NONE` | `CALLER_DEFERRED` |

### 8.2 Bound non-terminal belief

| Intent | Route | Next owner | Reason |
|---|---|---|---|
| `RETAIN_CLAIM` | `RETAIN_CLAIM_ONLY` | `PCR_V0_1` | `CALLER_RETAINED_CLAIM` |
| `CREATE_BELIEF_FROM_CLAIM` | `DEFER` | `NONE` | `INTENT_PRECONDITION_UNMET` |
| `REVISE_EXISTING_BELIEF` | `P0_014_NON_TERMINAL_REVISION_REQUIRED` | `P0_014_BELIEF_LIFECYCLE` | `NON_TERMINAL_REVISION_OWNER` |
| `SEEK_EVIDENCE_GATE_DECISION` | `P0_015_EVIDENCE_GATE_REQUIRED` | `P0_015_EVIDENCE_GATE` | `EVIDENCE_GATE_OWNER` |
| `RECONSIDER_TERMINAL_BELIEF` | `DEFER` | `NONE` | `INTENT_PRECONDITION_UNMET` |
| `DEFER` | `DEFER` | `NONE` | `CALLER_DEFERRED` |

The router does not inspect or duplicate the current Evidence Gate policy
registry. `P0_015_EVIDENCE_GATE_REQUIRED` means only that P0-015 is the next
owner. P0-015 may later accept or reject its own command.

### 8.3 Bound terminal belief

`RETAIN_CLAIM` and `DEFER` retain their non-mutating routes.

For:

```text
CREATE_BELIEF_FROM_CLAIM
REVISE_EXISTING_BELIEF
SEEK_EVIDENCE_GATE_DECISION
RECONSIDER_TERMINAL_BELIEF
```

the exact result is:

```text
route      = TERMINAL_RECONSIDERATION_LINEAGE_REQUIRED
next_owner = FUTURE_TERMINAL_RECONSIDERATION_LINEAGE
reason     = TERMINAL_LINEAGE_PREREQUISITE
```

This result grants no authority to create a successor, supersede the old belief
or mutate the terminal stream.

---

## 9. 📏 Admission and canonicalization rules

For `record`:

- exact `ProvenanceClaimRecord` required;
- the complete `record.to_value()` is included in EPR canonical input;
- `record.input_fingerprint` is treated as data, not authority.

For `belief`:

- exact `BeliefBinding` or exact `None` only;
- revision must be an exact positive `int`, never `bool`;
- status and claim type must be exact enum instances;
- strings are exact non-empty unpadded UTF-8;
- claim-record fingerprint must be lowercase 64-character SHA-256 hex.

For `request`:

- exact `EpistemicChangeRequest` required;
- intent must be exact `EpistemicIntent`;
- `reason_refs` must be an exact tuple;
- tuple elements exact non-empty unpadded strings;
- lexical ascending order required;
- duplicates forbidden;
- an empty tuple is allowed.

For local budget values:

- exact positive `int` required;
- booleans rejected as integers;
- local limit must be <= corresponding hard cap.

No truncation, reordering, coercion, normalization, sampling, summarization or
implicit repair is allowed.

Valid hard-cap input exceeding local budget raises
`EpistemicChangeBudgetExceeded`. Malformed/hard-cap input raises
`EpistemicChangeContractError`. Binding mismatch raises
`EpistemicChangeBindingError`.

---

## 10. 🧾 Deterministic routing fingerprint

The future implementation computes its own fingerprint:

```text
sha256(
  b"MENTAURY_EPISTEMIC_CHANGE_INPUT_V1\x00"
  + canonical_json_bytes({
      "contract_version": "EPR-v0.1",
      "record": record.to_value(),
      "belief": belief.to_value() if belief is not None else None,
      "request": request.to_value(),
      "budget": budget.to_value(),
    })
).hexdigest()
```

Properties:

```text
routing_input_fingerprint
= exact-input identity evidence
≠ PCR authentication
≠ belief freshness proof
≠ Evidence Gate receipt
≠ support/truth evidence
≠ permission token
≠ reusable authority
```

---

## 11. 🚫 Command/event and owner-invocation boundary

EPR-v0.1 MUST NOT construct or return:

```text
CommandEnvelope
PendingEvent
CREATE_BELIEF payload
REVISE_BELIEF payload
APPLY_EVIDENCE_GATE payload
EvidenceGateDecision
EvidenceGateReceipt
BeliefDecision
```

It MUST NOT call:

```text
BeliefLifecycle.decide
EvidenceGatedBeliefLifecycle.decide
EvidenceGate.evaluate
reducers
stores/event appenders
```

Routing is intentionally separated from execution/decision authority.

---

## 12. 🧪 Frozen adversarial requirements

A later implementation PR must make each family executable:

```text
EPR-T01 PCR record cannot become automatic belief promotion
EPR-T02 evidence_refs cannot become SUPPORTED evidence
EPR-T03 caller cannot select SUPPORTED / CONTRADICTED target
EPR-T04 router cannot duplicate Evidence Gate policy/threshold logic
EPR-T05 PCR→belief loss cannot be hidden; binding prerequisite route is mandatory
EPR-T06 mismatched claim-id/ClaimType/PCR-fingerprint binding fails closed
EPR-T07 caller-supplied belief revision cannot become execution/freshness authority
EPR-T08 terminal belief cannot be revised or re-gated in place
EPR-T09 terminal-lineage route cannot create a successor implicitly
EPR-T10 ClaimClass / ClaimType / EpistemicRole / BeliefStatus / EvidenceGateOutcome remain distinct
EPR-T11 route/fingerprint cannot be replayed as capability or permission
EPR-T12 valid route grants no retrieval/action/identity/relationship/M3/deployment authority
```

---

## 13. 🔁 Frozen metamorphic requirements

```text
EPR-M01 any PCR semantic-field change changes routing fingerprint
EPR-M02 intent change changes routing fingerprint and route where table requires
EPR-M03 belief revision change changes routing fingerprint
EPR-M04 belief status terminality change can change route; PCR remains unchanged
EPR-M05 claim-id binding mismatch fails closed
EPR-M06 ClaimType binding mismatch fails closed
EPR-M07 PCR fingerprint binding mismatch fails closed
EPR-M08 same request on terminal vs non-terminal binding follows different owner route
EPR-M09 reason-ref count/order cannot manufacture support or permission
EPR-M10 duplicate/unsorted reason refs fail closed, never normalized silently
```

---

## 14. 🧼 Purity requirements

```text
EPR-P01 no network
EPR-P02 no filesystem
EPR-P03 no database / persistence
EPR-P04 no environment / ambient clock
EPR-P05 no model / LLM / retriever / Atlas / graph
EPR-P06 no command/event emission and no P0-014/P0-015 invocation
EPR-P07 no belief / identity / relationship / M3 mutation
EPR-P08 deterministic output for exact typed input
```

---

## 15. ⛔ Mandatory stop boundary

After this exact contract is reviewed and merged, the intended state is:

```text
PHASE_4_EPISTEMIC_PROMOTION_REVISION_READINESS = READY
PHASE_4_CANDIDATE_SELECTION = SELECTED
PHASE_4_CANDIDATE = PURE_EPISTEMIC_CHANGE_ROUTER
PHASE_4_IMPLEMENTATION_CONTRACT = FROZEN_DOCS
PHASE_4_CONTRACT_VERSION = EPR-v0.1
PHASE_4_IMPLEMENTATION = NOT_STARTED
PHASE_4_OWNER_GO = NOT_GRANTED
PHASE_4_RUNTIME = NOT_AUTHORIZED
CLAIM_TO_BELIEF_BINDING = NOT_IMPLEMENTED
TERMINAL_RECONSIDERATION_LINEAGE = NOT_IMPLEMENTED
```

A later implementation requires a **new explicit Owner GO after this exact
EPR-v0.1 contract is reviewed and merged**.

Previous P1/NPG/NPG-COMP/PCR Owner GO receipts are consumed and cannot authorize
EPR-v0.1.

No Phase 5 typed-relations work, runtime activation, retrieval, action, identity,
M3, persistence or deployment follows automatically from this freeze.