# 🔁 Terminal Reconsideration Lineage — Frozen Contract v0.1

```text
Status:                              FROZEN_DOCS_CANDIDATE · DOCS_ONLY
Contract version:                    TRL-v0.1
V1 stage:                            3 / 5
Candidate:                           PURE_TERMINAL_SUCCESSOR_LINEAGE_PLANNER
Implementation:                      NOT_STARTED
Implementation Owner GO:             NOT_GRANTED
Runtime activation:                  NOT_AUTHORIZED
Terminal belief in-place mutation:   FORBIDDEN
Successor creation authority:        NONE
P0-014 authority:                    UNCHANGED
P0-015 Evidence Gate authority:      UNCHANGED
EPR-v0.1 authority:                  ROUTING_ONLY · UNCHANGED
CBP-v0.1 authority:                  GENESIS_BINDING_ONLY · UNCHANGED
Persistence / I/O:                   NONE
Identity / relationship / M3:        NONE
Action / deployment authority:       NONE
```

> **A terminal belief is never reopened in place.**
>
> TRL-v0.1 only defines the lineage information required before a future owner
> may create a new successor belief lineage. It does not create that successor.

---

## 1. 🎯 Bounded problem

P0-014/P0-015 currently make these belief states terminal:

```text
SUPPORTED
CONTRADICTED
SUPERSEDED
```

EPR-v0.1 correctly routes attempts to revise, re-gate or reconsider such a
belief to:

```text
TERMINAL_RECONSIDERATION_LINEAGE_REQUIRED
```

What is missing is a bounded, explicit answer to:

> Which exact terminal belief snapshot and which exact PCR claim record would a
> future successor lineage be derived from, without reopening or modifying the
> terminal stream?

TRL-v0.1 freezes that missing protocol surface only.

---

## 2. 🧠 Human meaning

A person or system can later reconsider a conclusion without pretending the old
conclusion never existed.

The intended history is:

```text
old belief A
  └─ terminal at revision N
       └─ reconsideration basis is recorded
            └─ future successor belief B may be created by its own owner
```

Not:

```text
old belief A terminal
  → silently reopen A
  → rewrite its past
```

This preserves continuity and correctability at the same time.

---

## 3. 🔒 Frozen invariants

```text
terminal belief != mutable belief
reconsideration != reversal of history
lineage plan != successor creation
lineage plan != belief
lineage plan != Evidence Gate verdict
lineage plan != PCR truth
lineage plan != permission
lineage plan != capability lease
lineage plan != runtime authority
```

A terminal belief's existing event history and status remain untouched.

---

## 4. 📦 Reserved future package

A later separately authorized implementation, if approved, is limited to:

```text
src/mentaury/terminal_lineage/__init__.py
src/mentaury/terminal_lineage/contracts.py
src/mentaury/terminal_lineage/planner.py
```

No source files are created by this contract-freeze PR.

Exact future public function:

```python
def plan_terminal_successor_lineage(
    *,
    terminal: TerminalBeliefSnapshot,
    record: ProvenanceClaimRecord,
    request: TerminalReconsiderationRequest,
    budget: TerminalLineageBudget,
) -> TerminalSuccessorLineagePlan:
    ...
```

The function accepts no lifecycle, reducer, Evidence Gate, store, command bus,
clock, filesystem, network, retriever, model, tool or identity handle.

---

## 5. ♻️ Existing owners reused

Future implementation must reuse exact current class identities:

```python
from mentaury.claims import ProvenanceClaimRecord
from mentaury.epistemic_types import ClaimType
from mentaury.beliefs.contracts import (
    BeliefStatus,
    belief_status_transition_allowed,
)
```

Terminality must remain derived from the existing owner rule:

```text
terminal(status)
= not belief_status_transition_allowed(status, status)
```

TRL-v0.1 cannot widen or narrow terminal states.

---

## 6. 📦 Frozen immutable contracts

All future values are `@dataclass(frozen=True, slots=True)` with exact `to_value()`
projections and no extension dictionaries.

```python
@dataclass(frozen=True, slots=True)
class TerminalBeliefSnapshot:
    belief_id: str
    belief_revision: int
    belief_status: BeliefStatus
    belief_claim_type: ClaimType
    origin_claim_id: str | None
    origin_claim_record_fingerprint: str | None
    terminal_event_id: str
    terminal_event_hash: str

@dataclass(frozen=True, slots=True)
class TerminalReconsiderationRequest:
    request_id: str
    reason_refs: tuple[str, ...]

@dataclass(frozen=True, slots=True)
class TerminalLineageBudget:
    max_string_bytes: int
    max_tuple_items: int
    max_canonical_input_bytes: int

@dataclass(frozen=True, slots=True)
class TerminalSuccessorLineagePlan:
    contract_version: str
    request_id: str
    predecessor_belief_id: str
    predecessor_revision: int
    predecessor_status: BeliefStatus
    predecessor_terminal_event_id: str
    predecessor_terminal_event_hash: str
    reconsideration_claim_id: str
    reconsideration_record_fingerprint: str
    successor_creation_owner: str
    lineage_input_fingerprint: str
```

The exact frozen `successor_creation_owner` literal is:

```text
P0_014_BELIEF_LIFECYCLE_VIA_NEW_LINEAGE
```

It is a routing label only, not a callable handle or authorization token.

---

## 7. 🔐 Admission rules

### 7.1 Terminal snapshot

Future planner accepts an exact `TerminalBeliefSnapshot` only when:

- `belief_revision` is exact positive `int`, never `bool`;
- `belief_status` is an exact `BeliefStatus` member;
- existing owner semantics classify that status as terminal;
- identifiers are exact non-empty unpadded UTF-8 strings;
- `terminal_event_hash` is exact lowercase `sha256:<64 hex>`;
- origin claim ID/fingerprint are both present or both absent;
- an origin fingerprint, when present, is exact lowercase 64-character SHA-256 hex.

A non-terminal snapshot fails closed.

### 7.2 Reconsideration record

The exact `ProvenanceClaimRecord` is included in canonical input.

Its presence means only:

```text
this PCR record is the caller-supplied reconsideration basis
```

It does not mean the claim is true, admitted as evidence, or sufficient to create
or promote a successor belief.

### 7.3 Request

`reason_refs` must be an exact tuple, lexically sorted and duplicate-free. No
normalization, sorting or repair occurs inside the planner.

---

## 8. 🧬 Lineage semantics

A valid plan binds:

```text
predecessor terminal identity
+ predecessor terminal revision/status/event anchor
+ optional predecessor PCR genesis identity
+ exact reconsideration PCR record identity
+ exact request identity
```

The plan MUST NOT contain:

```text
successor_belief_id
successor statement text
requested BeliefStatus
EvidenceGateOutcome
EvidenceGateReceipt
CREATE_BELIEF command
PendingEvent
CapabilityLease
Action decision
```

Why no successor ID? Because assigning or creating a successor belongs to the
future creation owner, not the lineage planner.

---

## 9. 🚫 No in-place terminal mutation

Future TRL implementation MUST NOT call or construct inputs for:

```text
BeliefLifecycle.decide on predecessor stream
EvidenceGatedBeliefLifecycle.decide on predecessor stream
EvidenceGate.evaluate
BeliefReducer / EvidenceGatedBeliefReducer mutation
store append
```

It cannot revise, attach evidence to, register contradictions on, re-gate,
supersede again, or otherwise mutate the predecessor terminal belief.

---

## 10. 🔗 CBP-v0.1 relationship

If the predecessor carries a CBP-v0.1 genesis binding, TRL preserves that
identity as predecessor history only.

The reconsideration PCR record is a separate exact record identity.

```text
predecessor origin claim != reconsideration claim
```

They may happen to have the same claim ID/fingerprint, but TRL does not infer
that repetition adds evidence, confidence or authority.

---

## 11. 🧭 EPR-v0.1 relationship

EPR-v0.1 may return:

```text
TERMINAL_RECONSIDERATION_LINEAGE_REQUIRED
```

That route does not invoke TRL automatically.

A caller must separately construct valid TRL typed inputs. The EPR routing plan
is not accepted as authority and is not required as an input to TRL-v0.1.

This prevents route replay from becoming permission.

---

## 12. 🧾 Deterministic fingerprint

Frozen constants for future implementation:

```text
TERMINAL_LINEAGE_CONTRACT_VERSION = "TRL-v0.1"
CANONICAL_PROFILE                 = "MENTAURY_CANONICAL_JSON_V1"
INPUT_FINGERPRINT_DOMAIN          = "MENTAURY_TERMINAL_LINEAGE_INPUT_V1"

HARD_MAX_STRING_BYTES             = 4096
HARD_MAX_TUPLE_ITEMS              = 512
HARD_MAX_CANONICAL_INPUT_BYTES    = 262144
```

Future fingerprint:

```text
sha256(
  b"MENTAURY_TERMINAL_LINEAGE_INPUT_V1\x00"
  + canonical_json_bytes({
      "contract_version": "TRL-v0.1",
      "terminal": terminal.to_value(),
      "record": record.to_value(),
      "request": request.to_value(),
      "budget": budget.to_value(),
    })
).hexdigest()
```

This is exact-input identity evidence only.

---

## 13. 🧪 Frozen test requirements

```text
TRL-T01 non-terminal predecessor fails closed
TRL-T02 SUPPORTED predecessor may be represented but never reopened
TRL-T03 CONTRADICTED predecessor may be represented but never re-gated in place
TRL-T04 SUPERSEDED predecessor may be represented but never revised in place
TRL-T05 predecessor terminal event ID/hash are preserved exactly
TRL-T06 predecessor CBP origin identity is preserved when present
TRL-T07 reconsideration PCR record remains distinct from predecessor identity
TRL-T08 plan contains no successor ID/status/command/event
TRL-T09 reason refs cannot manufacture truth/support/permission
TRL-T10 no EPR plan is accepted as authority input
TRL-T11 same exact typed input is deterministic
TRL-T12 semantic input changes alter lineage fingerprint
TRL-T13 malformed/hash/budget inputs fail closed
TRL-T14 no network/filesystem/database/model/retrieval/tool imports
TRL-T15 planner invokes no P0-014/P0-015 owner
TRL-T16 plan grants no identity/relationship/M3/action/deployment authority
```

---

## 14. 📏 Definition of Done for Stage 3

Stage 3 is complete only when both sub-gates are complete:

```text
3A CONTRACT FREEZE
- bounded contract merged
- exact-head CI PASS
- P0/P1 = 0
- no src/** implementation

3B BOUNDED IMPLEMENTATION
- separate explicit Owner GO after contract merge
- exact frozen TRL-v0.1 package only
- TRL-T01…T16 executable PASS
- full repository CI PASS
- P0/P1 = 0
- no runtime/deployment authority
```

Stage 3 completion does not authorize runtime activation.

---

## 15. ⛔ Mandatory stop boundary

After contract freeze alone:

```text
TRL_CONTRACT = FROZEN_DOCS
TRL_IMPLEMENTATION = NOT_STARTED
TRL_IMPLEMENTATION_OWNER_GO = NOT_GRANTED
TERMINAL_IN_PLACE_MUTATION = FORBIDDEN
RUNTIME = NOT_AUTHORIZED
```

A later implementation requires a new explicit Owner GO after this contract is
merged. That GO is single-use for `TRL-v0.1` implementation only.
