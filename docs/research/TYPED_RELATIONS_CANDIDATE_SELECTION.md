# 🔗 Phase 5 Typed Relations — Candidate Selection

```text
Status:                              SELECTED · DOCS_ONLY
Date:                                2026-08-12
Tracking issue:                      #113
Authoritative baseline:              25675f2d60f43d0b9e5e030662f82706bf212bb5
Owning readiness:                    TYPED_RELATIONS_CONTRACT_READINESS.md
Selected candidate:                  PURE_ANCHORED_TYPED_RELATION_RECORD
Selected contract version:           ATR-v0.1
Implementation contract:             FREEZE_IN_THIS_BOUNDED_BLOCK
Implementation:                      NOT_STARTED
Owner GO:                            NOT_GRANTED
Runtime:                             NOT_AUTHORIZED
Persistence / graph authority:       NONE
Evidence Gate authority:             UNCHANGED
Belief mutation authority:           NONE
Action / tool authority:             NONE
Identity / relationship authority:   NONE
Direct or indirect M3 write:         FORBIDDEN
Deployment authority:                NONE
Independent human review:            NO
```

> **CANDIDATE SELECTED ≠ IMPLEMENTED ≠ OWNER GO.**
>
> This decision selects the smallest pure representation primitive that satisfies
> the frozen Typed Relations readiness boundary. It does not authorize source
> code, graph persistence, relation discovery, evidence evaluation, belief
> mutation, autonomous cognition or runtime activation.

---

## 1. 🎯 Selection question

Phase 5 readiness established that Mentaury needs one inspectable representation
for a candidate relation between two exact PCR-v0.1 claim states. The selection
question is therefore:

> Which smallest primitive can preserve exact endpoint identity, relation type,
> directionality, origin, scope and derivation basis **without** becoming a graph
> truth system, an Evidence Gate, a confidence surface or an inference engine?

The answer is:

```text
PURE_ANCHORED_TYPED_RELATION_RECORD
```

The selected primitive is intentionally a **record constructor**, not a finder,
ranker, evaluator, promoter or runtime coordinator.

```text
REPRESENT(candidate relation)
≠ DISCOVER(relation)
≠ INFER(relation)
≠ PROVE(relation)
≠ PROMOTE(relation)
≠ STORE(relation)
```

---

## 2. 🧪 Candidate comparison

| Candidate | Disposition | Reason |
|---|---|---|
| `FREE_FORM_GRAPH_EDGE` | ❌ Reject | graph topology becomes an attractive unowned truth/confidence surface; weak provenance and scope discipline |
| `TYPED_EDGE_WITH_CONFIDENCE` | ❌ Reject | numeric/ordinal confidence would create a pseudo Evidence Gate with no owner or calibration semantics |
| `MULTI_PREMISE_RELATION_HYPEREDGE` | ❌ Defer | collapses representation into inference composition before Inference Bridge Audit / Hypothesis Discrimination exist |
| `PURE_ANCHORED_TYPED_RELATION_RECORD` | ✅ Select | pairwise, exact PCR-bound, caller-supplied, pure, deterministic, independently testable, no mutation or graph authority |

The selected primitive fixes the demonstrated bottleneck from the bounded
Discovery / Restraint / False Bridge probes: Mentaury can preserve claims, but
cannot yet name and inspect a relation without free prose or graph adjacency.

---

## 3. 🧬 Selected candidate identity

```text
Candidate:      PURE_ANCHORED_TYPED_RELATION_RECORD
Contract:       ATR-v0.1
Future package: src/mentaury/relations/
Future API:     represent_typed_relation(...)
```

The future record has four semantic inputs:

```text
1. exact endpoints
2. relation semantics
3. relation provenance
4. relation scope
```

plus a caller-supplied local representation budget.

The primitive computes its own deterministic fingerprint. A caller-supplied final
fingerprint is forbidden.

---

## 4. 🔐 Exact endpoint authority

The selected candidate reuses PCR-v0.1 identity rather than copying claim text.

```text
ClaimAnchor
= claim_id
+ exact ProvenanceClaimRecord.input_fingerprint
```

Forbidden substitutes:

```text
raw statement text
statement_ref alone
source_ref alone
graph node id
embedding/vector id
retrieval rank
LLM summary
```

An endpoint PCR fingerprint change therefore creates a different relation input
identity. A relation cannot silently float to a revised claim.

---

## 5. 🧩 Frozen semantic axes

The later exact contract must keep these axes separate:

```text
RELATION TYPE
≠ ORIENTATION
≠ ORIGIN
≠ SCOPE
≠ CONFIDENCE
≠ EVIDENCE STATUS
≠ TRUTH
```

Core v0.1 relation type vocabulary remains closed:

```text
CAUSAL
CORRELATIONAL
TEMPORAL
ANALOGICAL
TAXONOMIC
MECHANISTIC
EVIDENTIAL
CONTRADICTORY
UNKNOWN
```

Orientation remains:

```text
DIRECTED
SYMMETRIC
UNKNOWN
```

Origin remains:

```text
SOURCE_ASSERTED
MENTAURY_DERIVED
EXTERNAL_DERIVED
UNKNOWN
```

No caller-defined enum strings are admitted in ATR-v0.1.

---

## 6. 🧭 Scope-reference decision

Readiness left one specific shape decision open: scope entries sometimes refer to
an epistemic claim and sometimes to non-epistemic context.

ATR-v0.1 therefore selects one explicit tagged reference shape:

```text
ScopeReferenceKind.CLAIM_ANCHOR
→ reference_id = exact PCR claim_id
→ claim_input_fingerprint = exact lowercase sha256 PCR fingerprint

ScopeReferenceKind.CONTEXT_REF
→ reference_id = caller-supplied non-epistemic context identifier
→ claim_input_fingerprint = None
```

This prevents a context string from being silently treated as a claim while also
avoiding a requirement to invent PCR claims for every operational context label.

Hard law:

```text
CONTEXT_REF ≠ CLAIM ≠ EVIDENCE
```

---

## 7. 🪪 Provenance decision

The selected record has an explicit relation-origin object.

```text
SOURCE_ASSERTED
→ exact source-assertion ClaimAnchor REQUIRED
→ origin_actor_ref REQUIRED
→ relation still not true by attribution alone

MENTAURY_DERIVED
→ source-assertion anchor FORBIDDEN
→ origin_actor_ref REQUIRED
→ non-empty basis ClaimAnchors REQUIRED
→ generated relation is not independent evidence for itself

EXTERNAL_DERIVED
→ source-assertion anchor FORBIDDEN
→ origin_actor_ref REQUIRED
→ non-empty basis ClaimAnchors REQUIRED
→ external derivation is attributed, not authenticated truth

UNKNOWN
→ source-assertion anchor FORBIDDEN
→ origin_actor_ref MUST be absent
→ no provenance upgrade is permitted
```

All basis items are exact PCR ClaimAnchors only. ATR-v0.1 admits no relation-record
reference as its own derivation basis, which structurally blocks direct recursive
self-support.

---

## 8. ↔️ Endpoint order decision

Directed relation order is semantic:

```text
left_anchor → right_anchor
```

Symmetric relation order is identity-only and must be supplied in the frozen
canonical anchor order. ATR-v0.1 must reject unsorted symmetric endpoints rather
than silently reorder them.

Canonical ClaimAnchor key:

```text
(claim_id, claim_input_fingerprint)
```

Exact self-relations are forbidden in v0.1.

---

## 9. 🧯 Semantic ceilings

```text
CAUSAL ≠ causal proof
CORRELATIONAL ≠ causal direction
TEMPORAL ≠ causal mechanism
ANALOGICAL ≠ shared mechanism
MECHANISTIC ≠ causal proof
TAXONOMIC ≠ objective ontology truth
EVIDENTIAL ≠ SUPPORTED
CONTRADICTORY ≠ EvidenceGateOutcome.CONTRADICTED
UNKNOWN ≠ permission to guess a stronger type
GRAPH LINK / PATH / COUNT ≠ EPISTEMIC AUTHORITY
```

No numeric or ordinal confidence/reliability field is part of ATR-v0.1.

---

## 10. 🔒 Authority ownership retained

ATR-v0.1 does not change any existing owner:

```text
PCR-v0.1
→ owns exact claim representation

P0-015 Evidence Gate
→ remains sole owner of SUPPORTED / CONTRADICTED evaluation semantics

P0-014
→ remains owner of ordinary non-terminal belief lifecycle mutation

EPR-v0.1
→ remains frozen docs-only and unimplemented
```

Typed Relations may represent an `EVIDENTIAL` or `CONTRADICTORY` candidate relation
without emitting an Evidence Gate result.

---

## 11. ✅ Why this candidate is independently testable

A pure constructor can be tested with caller-supplied immutable values only.

It is possible to verify independently that:

- exact endpoint changes change the relation fingerprint;
- incompatible type/orientation pairs fail closed;
- symmetric unsorted endpoints fail closed;
- source/derived provenance invariants are enforced;
- conditions/moderators/exceptions/unknowns/transfer limits affect identity;
- hard-cap and local-budget failures are distinct;
- no confidence/EvidenceGateOutcome/belief/action fields are produced;
- no network/filesystem/database/LLM/retrieval/graph traversal is required.

This makes the candidate suitable for a later bounded implementation **if and
only if** a separate explicit Owner GO is granted after contract freeze.

---

## 12. 🚫 Not selected in this milestone

```text
relation discovery engine
relation ranking
confidence model
evidence scoring
causal inference
mechanism inference
transitive closure
graph traversal
graph persistence
hyperedge / multi-premise inference
Inference Bridge Audit
Hypothesis Discrimination
Cognitive Inquiry
OEO lifecycle
scheduler/significance
shadow cognitive loop
persistent autonomous cognition
identity/self-model evolution
```

Those remain separate future problems and cannot be smuggled into the selected
record primitive.

---

## 13. 🏁 Selection result

```text
PHASE_5_TYPED_RELATIONS_CANDIDATE_SELECTION = SELECTED
PHASE_5_TYPED_RELATIONS_CANDIDATE = PURE_ANCHORED_TYPED_RELATION_RECORD
PHASE_5_TYPED_RELATIONS_CONTRACT_VERSION = ATR-v0.1
PHASE_5_IMPLEMENTATION = NOT_STARTED
PHASE_5_OWNER_GO = NOT_GRANTED
PHASE_5_RUNTIME = NOT_AUTHORIZED
```

The exact implementation contract is frozen separately in:

`TYPED_RELATIONS_PURE_RECORD_CONTRACT_V0_1.md`

> **STOP BOUNDARY:** candidate selection is architecture, not authority. No
> `src/mentaury/relations/**` implementation is authorized by this document.