# 🔬 Post-Phase-4 Cognitive Milestone Discrimination

```text
Status:                         DECISION_RESEARCH · DOCS_ONLY
Date:                           2026-08-12
Tracking issue:                 #108
Baseline main:                  ab98a0d746e6e859d0dff8c7056601bfb9824b43
Phase 4 EPR-v0.1:               FROZEN_DOCS
Phase 4 implementation:         NOT_STARTED
Phase 4 Owner GO:               NOT_GRANTED
Phase 4 runtime:                NOT_AUTHORIZED
Decision target:                NEXT_BOUNDED_READINESS_MILESTONE
Selected next readiness:        PHASE_5_TYPED_RELATIONS_CONTRACT_READINESS
Selected implementation:       NONE
Selected Owner GO:              NONE
Runtime authority:              NONE
Research authority:             ADVISORY_TO_ARCHITECTURE_ONLY
Independent human review:       NO
```

> **SELECTION OF READINESS ≠ IMPLEMENTATION AUTHORITY.**
>
> This document selects the smallest next *architecture/readiness* question to
> investigate. It grants no EPR implementation, Typed Relations implementation,
> runtime, persistence, retrieval, action, identity, M3, or deployment authority.

---

## 1. 🎯 Question

After the verified Phase 4 `EPR-v0.1` docs-only freeze, which missing primitive is
closest to the project's North Star of independently relating knowledge,
exposing unsupported inference, generating discriminating tests, and later
returning to unresolved inquiry?

The decision must not be inherited from roadmap numbering. The method is:

```text
current executable / frozen surfaces
        ↓
synthetic cognitive probe
        ↓
first missing bounded representation or operation
        ↓
dependency discrimination
        ↓
select one readiness milestone only
```

The strongest result permitted here is:

```text
NEXT READINESS MILESTONE SELECTED
```

not:

```text
IMPLEMENTATION AUTHORIZED
```

---

## 2. 🧩 Candidates considered

The discrimination considered all currently relevant candidates rather than
assuming that the already-frozen EPR contract must be implemented next.

```text
A. EPR-v0.1 bounded implementation
B. Claim→Belief Binding
C. Terminal Reconsideration Lineage
D. Typed Relations
E. Inference Bridge Audit
F. Hypothesis Discrimination
G. Cognitive Inquiry
H. Open Epistemic Obligations
I. ACI-X0.0 research
```

### A. EPR-v0.1 implementation

`EPR-v0.1` is the most implementation-ready candidate because its exact routing
contract is already frozen. That is an engineering-readiness fact, not proof of
cognitive priority.

EPR answers:

> Which protocol owner or missing prerequisite should handle this caller-supplied
> epistemic transition request?

It does **not** discover relations, inspect inference bridges, generate competing
hypotheses, or decide what question to investigate.

Therefore:

```text
EPR_IMPLEMENTATION_READY_TO_BE_CONSIDERED
≠ EPR_IS_NEXT_COGNITIVE_BOTTLENECK
```

### B. Claim→Belief Binding

This is a real losslessness prerequisite for later belief creation from PCR
records. It protects provenance, attribution, epistemic role, and transfer
limits when crossing representation boundaries.

However, it is a belief-lifecycle bridge. The synthetic cognitive probe below
fails earlier: the current architecture cannot yet represent the relation being
reasoned about as a bounded typed object.

### C. Terminal Reconsideration Lineage

Necessary for future reconsideration of terminal `SUPPORTED`, `CONTRADICTED`, or
`SUPERSEDED` beliefs without rewriting history. It is not the earliest
bottleneck for cross-claim cognition because it presupposes a mature belief and
revision path.

### D. Typed Relations

This is the first missing bounded representation needed by all three synthetic
probe families. Current PCR can represent claims and their epistemic roles, but
there is no Soul-owned primitive that can represent a candidate relation while
preserving the distinction between:

```text
causal
correlational
temporal
analogical
taxonomic
mechanistic
evidential
contradictory
unknown
```

Without this boundary, later cognitive work must either use untyped free text or
prematurely call a relation causal/mechanistic.

### E. Inference Bridge Audit

Highly valuable, but it needs explicit endpoints and a bounded relation/bridge
object to audit. Otherwise the hidden assumption is only prose and cannot be
reliably bound to exact premises/conclusions.

### F. Hypothesis Discrimination

Also high-value, but it requires competing hypotheses and consequences to be
bound to explicit relations. Typed relation semantics are therefore a smaller
prerequisite.

### G. Cognitive Inquiry

Inquiry can generate questions, but before Typed Relations it would have no
bounded way to say *what kind of relation* triggered the question. That would
encourage opaque model prose instead of inspectable cognition.

### H. Open Epistemic Obligations

OEO is a persistence/lifecycle mechanism for unfinished cognitive work. It
should not precede the primitive that makes a useful cognitive obligation
well-typed.

### I. ACI-X0.0

Autonomous Cognitive Initiation remains an important separate research line.
But an initiation experiment performed before Typed Relations would conflate two
failures:

1. failure to initiate inquiry;
2. failure to represent the relation/inference object after initiation.

The second failure should be removed first.

---

## 3. 🧪 Bounded synthetic probe

This discrimination uses three technology-neutral microworld families. It does
not call an LLM and does not claim to measure consciousness, intelligence, or
runtime autonomy. It asks only where the current *architecture* first lacks a
bounded object needed for the requested cognitive operation.

### Probe P4-DISC-01 — Discovery

Synthetic records:

```text
R1: system K remains stable after one node is removed
R2: system K has multiple partially redundant paths
R3: system M has one central path and fails when that path is removed
```

Desired cognitive step:

```text
identify a candidate relation between redundancy and resilience
→ mark relation type without claiming causality
→ state what additional observation could distinguish correlation from mechanism
```

Current architecture can:

```text
represent R1/R2/R3 as provenance-preserving claims       YES · PCR-v0.1
route a caller-supplied belief transition                 CONTRACT FROZEN ONLY · EPR-v0.1
represent candidate relation as bounded typed object      NO
```

First cognitive representation gap:

```text
TYPED RELATION
```

### Probe P4-DISC-02 — Restraint

Synthetic records:

```text
R1: organism A appears in environment X
R2: condition B is also observed in environment X
R3: no intervention or temporal-order evidence is available
```

Desired cognitive step:

```text
represent association
→ preserve UNKNOWN/uncertain mechanism
→ refuse causal promotion
```

A typed relation primitive is required to encode that the observed relation is
correlational/unknown rather than causal. EPR cannot provide that semantic
boundary because EPR routes epistemic ownership; it does not type cross-claim
relations.

### Probe P4-DISC-03 — False Bridge

Synthetic records:

```text
R1: two systems have visually similar network shapes
R2: one system is robust under disturbance
R3: robustness of the second system is not observed
```

Tempting invalid move:

```text
similar structure
→ same mechanism
→ same robustness
```

Desired cognitive step:

```text
represent ANALOGICAL relation
≠ MECHANISTIC relation
≠ CAUSAL evidence
→ later expose the missing inference bridge
```

The first missing bounded primitive is again relation typing. Inference Bridge
Audit is the next likely consumer of that representation, not a substitute for
it.

---

## 4. 📊 Discrimination matrix

| Candidate | Fixes first probe gap? | Required before later cognition? | Already contract-frozen? | Selection result |
|---|---:|---:|---:|---|
| EPR implementation | No | Useful for belief routing | Yes | DEFER AS IMPLEMENTATION DECISION |
| Claim→Belief Binding | No | Required for lossless belief creation | No | LATER / PARALLEL LIFECYCLE GAP |
| Terminal lineage | No | Required for terminal reconsideration | No | LATER |
| **Typed Relations** | **Yes** | **Yes** | No | **SELECT NEXT READINESS** |
| Inference Bridge Audit | Not without relation object | Yes | No | AFTER RELATION SEMANTICS |
| Hypothesis Discrimination | Not without bound hypotheses/relations | Yes | No | AFTER RELATION SEMANTICS |
| Cognitive Inquiry | Not safely | Yes | No | AFTER LOWER PRIMITIVES |
| OEO | No | Later continuity primitive | No | LATER |
| ACI-X0.0 | Measures initiation, not this representation gap | Research line | No | RETAIN RESEARCH-ONLY |

---

## 5. ✅ Selected next bounded milestone

```text
POST_PHASE_4_COGNITIVE_MILESTONE_DISCRIMINATION = COMPLETE
NEXT_BOUNDED_READINESS_MILESTONE = PHASE_5_TYPED_RELATIONS_CONTRACT_READINESS
NEXT_IMPLEMENTATION_MILESTONE = NOT_SELECTED
PHASE_5_TYPED_RELATIONS_IMPLEMENTATION = NOT_STARTED
PHASE_5_OWNER_GO = NOT_GRANTED
EPR_V0_1_IMPLEMENTATION = NOT_STARTED
EPR_V0_1_OWNER_GO = NOT_GRANTED
```

The next work, if separately authorized as a new bounded docs/research block,
should answer only the architecture/readiness questions for Typed Relations:

- exact relation-role vocabulary and whether it is extensible or closed;
- how source/provenance binds to a relation candidate;
- how relation type differs from confidence, evidence status, and truth;
- how contradictions and unknown relations are represented;
- how analogical/correlational relations are prevented from silently escalating
  to mechanistic/causal relations;
- whether relations bind exact PCR records, claim identifiers, revisions, or a
  new relation-specific envelope;
- budget/canonicalization/fingerprint requirements if a future pure primitive is
  selected;
- explicit authority ceiling;
- adversarial and metamorphic requirements.

This selection does **not** freeze a Typed Relations implementation contract.

---

## 6. 🛡️ Authority and anti-laundering boundary

Hard laws retained:

```text
RELATION ≠ TRUTH
RELATION TYPE ≠ CONFIDENCE
CORRELATION ≠ CAUSATION
ANALOGY ≠ MECHANISM
GRAPH LINK ≠ CONFIDENCE PROPAGATION
CANDIDATE RELATION ≠ EVIDENCE FOR ITSELF
GENERATED HYPOTHESIS ≠ INDEPENDENT EVIDENCE
EPR ROUTE ≠ PERMISSION
READINESS SELECTION ≠ OWNER GO
```

The discrimination document grants no authority to:

```text
create/revise beliefs
produce SUPPORTED/CONTRADICTED
implement EPR-v0.1
implement Typed Relations
persist or retrieve
query Atlas/graph/vector stores
invoke models/tools
pass Action Gate
mutate identity/relationship/M3
start autonomous/background cognition
activate runtime
deploy
```

---

## 7. 🛑 Mandatory stop

After this research decision is merged and verified:

```text
STOP
```

Do not automatically implement EPR or Typed Relations.

The next separate bounded block may be:

```text
PHASE_5_TYPED_RELATIONS_CONTRACT_READINESS · DOCS_ONLY
```

only after a fresh live reconciliation and an explicit decision to begin that
readiness block.
