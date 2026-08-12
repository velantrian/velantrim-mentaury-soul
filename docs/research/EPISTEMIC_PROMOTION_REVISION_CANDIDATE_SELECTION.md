# 🧭 Phase 4 — Epistemic Promotion & Revision Candidate Selection

```text
Status:                              CANDIDATE_SELECTED · DOCS_ONLY
Date:                                2026-08-12
Phase:                               4 · EPISTEMIC PROMOTION & REVISION
Owning readiness:                    EPISTEMIC_PROMOTION_REVISION_READINESS.md
Selected candidate:                  PURE_EPISTEMIC_CHANGE_ROUTER
Implementation:                      NOT_STARTED
Owner GO:                            NOT_GRANTED
Runtime authority:                   NONE
P0-014 belief authority:             UNCHANGED
P0-015 Evidence Gate authority:      UNCHANGED
Terminal reconsideration lineage:    NOT_IMPLEMENTED
Persistence authority:               NONE
Direct or indirect M3 write:         FORBIDDEN
```

> **CANDIDATE SELECTED ≠ IMPLEMENTATION AUTHORIZED.**

---

## 1. 🎯 Selection criterion

The Phase 4 candidate must be the smallest deterministic component that can
preserve the architecture's owner boundaries while making the next epistemic
step explicit.

It must:

- accept an exact caller-supplied PCR-v0.1 record;
- optionally accept an exact caller-supplied belief binding;
- accept an explicit intent rather than a requested truth/status result;
- identify exactly one next protocol owner or missing prerequisite;
- never mutate a belief or produce a domain command/event;
- never duplicate Evidence Gate policy/evaluation;
- fail closed on binding mismatch;
- preserve terminal-belief immutability until a separate lineage contract exists.

---

## 2. Alternatives considered

### A. Direct `PROMOTE_CLAIM` engine — REJECT

Why rejected:

- would collapse representation into belief authority;
- would need to invent PCR→belief projection semantics that do not currently
  preserve complete provenance/epistemic-role/transfer-limit information;
- risks allowing caller intent to become a belief mutation;
- would overlap P0-014 and P0-015 authority.

### B. Add `SUPPORTED/CONTRADICTED` to PCR-v0.1 — REJECT

Why rejected:

- PCR is representation-only;
- support/contradiction belongs to P0-015;
- a field on the record could be forged or replayed as pseudo-authority;
- it would violate `Claim ≠ Evidence status ≠ Belief status ≠ Truth`.

### C. Let P0-014 `REVISE_BELIEF` select `SUPPORTED/CONTRADICTED` — REJECT

Why rejected:

- the existing lifecycle explicitly rejects these statuses and requires the
  separately reviewed Evidence Gate;
- widening P0-014 would destroy the one-owner boundary around evidence policy,
  complete evidence-set checks and replay-verifiable receipts.

### D. Reopen terminal beliefs in place — REJECT

Why rejected:

- current contracts deliberately treat `SUPPORTED`, `CONTRADICTED` and
  `SUPERSEDED` as terminal;
- no current lineage/successor schema exists;
- in-place reopening would blur historical evidence receipts and revision
  provenance.

### E. `PURE_EPISTEMIC_CHANGE_ROUTER` — SELECTED

The selected primitive only determines the next required protocol owner.

```text
exact PCR-v0.1 record
+ optional exact belief binding
+ explicit epistemic intent
        ↓
pure validation + deterministic routing
        ↓
one bounded route
```

Selected routes:

```text
RETAIN_CLAIM_ONLY
CLAIM_TO_BELIEF_BINDING_REQUIRED
P0_014_NON_TERMINAL_REVISION_REQUIRED
P0_015_EVIDENCE_GATE_REQUIRED
TERMINAL_RECONSIDERATION_LINEAGE_REQUIRED
DEFER
```

No route is permission.

---

## 3. Selected intent vocabulary

The caller may request only one of these intents:

```text
RETAIN_CLAIM
CREATE_BELIEF_FROM_CLAIM
REVISE_EXISTING_BELIEF
SEEK_EVIDENCE_GATE_DECISION
RECONSIDER_TERMINAL_BELIEF
DEFER
```

There is intentionally no caller input named:

```text
PROMOTE_TO_SUPPORTED
PROMOTE_TO_CONTRADICTED
MARK_TRUE
MARK_FALSE
```

The Evidence Gate remains the only component that can decide its own outcome.

---

## 4. Selected owner vocabulary

Each route identifies one owner/prerequisite only:

```text
PCR_V0_1
FUTURE_CLAIM_TO_BELIEF_BINDING
P0_014_BELIEF_LIFECYCLE
P0_015_EVIDENCE_GATE
FUTURE_TERMINAL_RECONSIDERATION_LINEAGE
NONE
```

This vocabulary names protocol ownership; it is not a capability or service
handle.

---

## 5. Selected routing rules

### No existing belief binding

```text
RETAIN_CLAIM                 → RETAIN_CLAIM_ONLY
CREATE_BELIEF_FROM_CLAIM     → CLAIM_TO_BELIEF_BINDING_REQUIRED
SEEK_EVIDENCE_GATE_DECISION  → CLAIM_TO_BELIEF_BINDING_REQUIRED
REVISE_EXISTING_BELIEF       → DEFER
RECONSIDER_TERMINAL_BELIEF   → DEFER
DEFER                        → DEFER
```

The router does not skip the missing claim→belief bridge.

### Existing non-terminal belief binding

```text
RETAIN_CLAIM                 → RETAIN_CLAIM_ONLY
CREATE_BELIEF_FROM_CLAIM     → DEFER
REVISE_EXISTING_BELIEF       → P0_014_NON_TERMINAL_REVISION_REQUIRED
SEEK_EVIDENCE_GATE_DECISION  → P0_015_EVIDENCE_GATE_REQUIRED
RECONSIDER_TERMINAL_BELIEF   → DEFER
DEFER                        → DEFER
```

### Existing terminal belief binding

For any intent that would revise, re-evaluate, replace or recreate the bound
terminal belief:

```text
→ TERMINAL_RECONSIDERATION_LINEAGE_REQUIRED
```

`RETAIN_CLAIM` and `DEFER` remain non-mutating routes.

---

## 6. Selected binding boundary

A supplied belief binding must match the exact PCR record on:

```text
claim_id
ClaimType
claim_record_fingerprint
```

The router does not infer these associations.

A successful match means only:

```text
caller-supplied routing inputs are internally consistent
```

It does not mean:

```text
belief state was externally authenticated
belief revision is still live/current
PCR fingerprint is trusted authority
mutation is authorized
```

The owning P0-014/P0-015 component must still validate its own exact live state
and revision later.

---

## 7. Selected package boundary

If and only if a later separate Owner GO is granted for the exact frozen
EPR-v0.1 contract, the reserved bounded package is:

```text
src/mentaury/epistemic_change/__init__.py
src/mentaury/epistemic_change/contracts.py
src/mentaury/epistemic_change/router.py
```

The package must not include:

```text
promoter.py
belief_writer.py
evidence_gate.py
lifecycle.py
lineage_store.py
repository.py
store.py
retriever.py
atlas.py
worker.py
scheduler.py
identity.py
action.py
tools.py
```

No existing P0/P1 source file is widened by the selected candidate.

---

## 8. Authority ceiling

The strongest successful result is a deterministic routing plan.

```text
VALID ROUTE
≠ source admission
≠ belief creation
≠ belief revision acceptance
≠ Evidence Gate outcome
≠ SUPPORTED
≠ CONTRADICTED
≠ truth
≠ retrieval permission
≠ action/tool permission
≠ identity/relationship authority
≠ M3 nomination/write
≠ runtime/deployment authority
```

---

## 9. Selection decision

```text
PHASE_4_CANDIDATE_SELECTION = SELECTED
PHASE_4_CANDIDATE = PURE_EPISTEMIC_CHANGE_ROUTER
NEXT_DOCS_STEP = FREEZE_EPR_V0_1_IMPLEMENTATION_CONTRACT
PHASE_4_OWNER_GO = NOT_GRANTED
PHASE_4_IMPLEMENTATION = NOT_STARTED
PHASE_4_RUNTIME = NOT_AUTHORIZED
```

The next allowed change in this milestone is the exact docs-only EPR-v0.1
contract freeze. No implementation authority follows from selection.