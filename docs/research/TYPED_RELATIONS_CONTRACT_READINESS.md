# 🔗 Typed Relations Contract Readiness

```text
Status:                              READY · FROZEN_DOCS · DOCS_ONLY
Date:                                2026-08-12
Tracking issue:                      #110
Owning discrimination:               POST_PHASE4_COGNITIVE_MILESTONE_DISCRIMINATION.md
Baseline main:                       fee3df0d19dbb7bcd536a3820ae8797d3edd4832
Readiness target:                    PHASE_5_TYPED_RELATIONS_CONTRACT_READINESS
Selected relation model:             ANCHORED_TYPED_RELATION_CANDIDATE
Implementation candidate selection:  NOT_STARTED
Implementation contract:             NOT_FROZEN
Implementation:                      NOT_STARTED
Owner GO:                            NOT_GRANTED
Runtime:                             NOT_AUTHORIZED
Persistence / graph authority:       NONE
Retrieval / Atlas authority:         NONE
Evidence Gate authority:             UNCHANGED
Belief mutation authority:           NONE
Action / tool authority:             NONE
Identity / relationship authority:   NONE
Direct or indirect M3 write:         FORBIDDEN
Deployment authority:                NONE
Independent human review:            NO
```

> **READINESS READY ≠ IMPLEMENTATION CONTRACT ≠ OWNER GO.**
>
> This document establishes the semantic boundary needed for a later separate
> candidate-selection / implementation-contract milestone. It creates no source
> package, runtime, graph store, relation discovery engine, evidence evaluator,
> belief mutation path or autonomous cognitive loop.

---

## 1. 🎯 Readiness question

The post-Phase-4 discrimination found that Mentaury can already preserve
provenance-bearing claims with `PCR-v0.1`, but cannot yet represent an inspectable
cross-claim relation without collapsing into free-form prose or graph adjacency.

This block answers:

> What must be true of a future bounded Typed Relations representation so that
> Mentaury can say **what kind of relation is being proposed**, preserve exact
> claim identity and scope, and refuse semantic escalation from association or
> analogy into mechanism, causality, evidence support or truth?

The strongest positive result here is:

```text
ARCHITECTURE READY FOR LATER CANDIDATE SELECTION / CONTRACT FREEZE
```

not:

```text
RELATION IMPLEMENTED
RELATION DISCOVERED
RELATION TRUE
CAUSALITY ESTABLISHED
EVIDENCE SUPPORTED
```

---

## 2. 🧬 Existing authority that must be reused, not duplicated

`PCR-v0.1` already owns exact immutable provenance-bearing claim representation.
A future relation primitive therefore **must not copy claim text into a second
knowledge object and treat that copy as authority**.

Exact endpoint identity must bind to the existing PCR identity surface:

```text
ClaimAnchor := exact pair of
  claim_id
  + ProvenanceClaimRecord.input_fingerprint
```

Why both are required:

```text
claim_id alone
≠ exact claim revision / representation identity

PCR fingerprint alone
≠ human-meaningful claim identity

claim_id + exact PCR fingerprint
= bounded anchor to one exact represented claim state
```

Changing any PCR input changes the PCR fingerprint. A relation anchored to an old
fingerprint therefore cannot silently float to a revised claim.

Forbidden endpoint substitutes:

```text
raw statement text
statement_ref alone
source_ref alone
speaker/subject label alone
graph node id alone
embedding/vector id
retrieval result rank
LLM-generated summary
```

---

## 3. 🔗 Selected relation model

The readiness model is:

```text
ANCHORED_TYPED_RELATION_CANDIDATE
```

It has three conceptual layers that must remain separate:

```text
A. exact endpoint identity
B. relation semantics
C. relation provenance + scope
```

A future bounded primitive should represent **caller-supplied relation
candidates**. It should not itself discover relations, search a graph, call a
model, infer causality or decide evidential support.

```text
REPRESENT(candidate relation)
≠ DISCOVER(relation)
≠ PROVE(relation)
≠ PROMOTE(relation)
```

Discovery, Inference Bridge Audit, Hypothesis Discrimination and autonomous
inquiry remain separate later cognition owners.

---

## 4. 🧩 Closed v0.1 core relation vocabulary

For the first bounded contract, the core vocabulary must be **closed**, not an
open caller-defined string taxonomy.

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

The closed vocabulary prevents a caller or model from inventing labels such as
`probably_causal`, `essentially_same_mechanism`, or `strongly_supported_link`
that smuggle confidence or evidence judgments into relation type.

Additional relation kinds may be researched later only through a versioned
contract change.

### 4.1 Semantic ceilings

```text
CAUSAL
= caller-supplied candidate causal relation
≠ causal proof

CORRELATIONAL
= association/co-variation relation candidate
≠ causal direction

TEMPORAL
= before/after or temporal dependency candidate
≠ causal mechanism

ANALOGICAL
= similarity/analogy candidate
≠ shared mechanism
≠ shared outcome

TAXONOMIC
= candidate classification/subsumption relation
≠ verified ontology truth

MECHANISTIC
= candidate mechanism relation
≠ causal proof

EVIDENTIAL
= candidate relation saying one claim may bear on another
≠ Evidence Gate qualification
≠ SUPPORTED

CONTRADICTORY
= candidate incompatibility between exact claims under stated scope
≠ EvidenceGateOutcome.CONTRADICTED
≠ belief mutation

UNKNOWN
= relation exists or is being examined but type is not established
≠ permission to guess a stronger type
```

---

## 5. ↔️ Directionality is a separate axis

Relation type and directionality must not be conflated.

A future contract should use a closed orientation axis:

```text
DIRECTED
SYMMETRIC
UNKNOWN
```

Readiness freezes the following v0.1 compatibility table:

```text
CAUSAL         → DIRECTED
CORRELATIONAL  → SYMMETRIC
TEMPORAL       → DIRECTED
ANALOGICAL     → SYMMETRIC
TAXONOMIC      → DIRECTED
MECHANISTIC    → DIRECTED
EVIDENTIAL     → DIRECTED
CONTRADICTORY  → SYMMETRIC
UNKNOWN        → UNKNOWN | DIRECTED | SYMMETRIC
```

A future implementation contract must fail closed on incompatible pairs rather
than repair them silently.

For directed relations, endpoint order is semantic:

```text
source_anchor → target_anchor
```

For symmetric relations, deterministic identity requires canonical endpoint
ordering. The later contract must require the caller to provide anchors in the
frozen canonical order and reject unsorted input rather than silently reorder it.

Exact self-relations (`left_anchor == right_anchor`) are outside v0.1 and must fail
closed.

---

## 6. 🪪 Relation provenance is independent from relation type

A source saying “A causes B” and Mentaury deriving “A may cause B” are not the
same provenance event even if both carry relation type `CAUSAL`.

The later contract must keep a separate relation-origin axis. Readiness freezes
this minimum vocabulary:

```text
SOURCE_ASSERTED
MENTAURY_DERIVED
EXTERNAL_DERIVED
UNKNOWN
```

Required semantics:

```text
SOURCE_ASSERTED
→ must bind an exact PCR ClaimAnchor for the claim that states the relation
→ does not make the relation true

MENTAURY_DERIVED
→ means the relation candidate was generated/derived by Mentaury cognition
→ does not make it independent evidence

EXTERNAL_DERIVED
→ derived by an attributed external analyst/system/person
→ must preserve actor attribution

UNKNOWN
→ origin not established
→ no provenance upgrade allowed
```

The future representation must carry an exact `origin_actor_ref`. A pure
representation primitive may validate shape but may not authenticate that actor
or independently prove the origin mode.

Hard law:

```text
RELATION ORIGIN ≠ RELATION TYPE ≠ RELATION TRUTH
```

---

## 7. 🧭 Relation scope must preserve conditions and exceptions

A relation without scope is especially dangerous because it encourages
unconditional generalization.

The future contract must preserve, at minimum, separate immutable collections for:

```text
conditions
moderators
exceptions
unknowns
transfer_limits
```

These are representational constraints only.

```text
condition present
≠ condition verified

exception present
≠ relation false everywhere

no listed exception
≠ universal law

transfer_limits empty
≠ permission for universal generalization
```

A later candidate-selection step must freeze the exact typed shape of these
references and decide which entries must themselves bind PCR ClaimAnchors versus
non-epistemic context references. Free-form hidden prose fields are not allowed.

This preserves the project rule:

```text
PARTICULAR
→ scoped abstraction
→ pattern
→ scoped generalization
→ model
```

with no automatic level promotion.

---

## 8. 📚 Basis anchors are not evidence support

A future relation record may need zero or more exact PCR ClaimAnchors describing
what the relation candidate was derived from.

Those anchors are **basis**, not Evidence Gate outcomes.

```text
1 basis anchor
100 basis anchors
100 repeated sources
≠ SUPPORTED
≠ RELIABLE
≠ TRUE
```

For `MENTAURY_DERIVED` and `EXTERNAL_DERIVED`, an empty derivation basis should be
considered malformed unless a later contract documents a narrower exception.

For `SOURCE_ASSERTED`, the exact source assertion ClaimAnchor is mandatory and is
not interchangeable with supporting evidence.

No relation candidate may list itself, its own future fingerprint, or a relation
derived solely from itself as independent support.

---

## 9. 🚫 No confidence, probability or reliability field in v0.1

The first Typed Relations representation must not include numeric or ordinal
confidence/reliability fields.

```text
relation_type
≠ confidence
≠ reliability
≠ source authority
≠ source count
```

Why: a `CAUSAL` relation with `0.91 confidence` would create an attractive but
unowned pseudo-Evidence-Gate surface. Confidence and evidence quality require a
separate later owner and measurement semantics.

Allowed uncertainty mechanism in v0.1:

```text
UNKNOWN relation type
+ explicit unknowns
+ scope / exceptions / transfer limits
```

not hidden probability.

---

## 10. 🧠 Anti-promotion laws

Typed Relations must make semantic escalation explicit and non-automatic.

```text
CORRELATIONAL
≠ CAUSAL

ANALOGICAL
≠ MECHANISTIC

TEMPORAL
≠ CAUSAL

EVIDENTIAL
≠ SUPPORTED

CONTRADICTORY
≠ EvidenceGateOutcome.CONTRADICTED

TAXONOMIC
≠ objective ontology truth

GRAPH ADJACENCY
≠ epistemic relation

MULTIPLE LINKS
≠ confidence propagation
```

A future change from one relation type to another must produce a new deterministic
input identity. No in-place semantic promotion is authorized by this readiness
block.

Promotion/revision lineage for relation records is not designed here and cannot
be invented inside the first implementation.

---

## 11. 🔄 Pairwise boundedness and no hidden transitive closure

The first contract should be pairwise:

```text
exactly two endpoint ClaimAnchors
```

Multi-premise inference belongs to later Inference Bridge / hypothesis work.

The relation representation must not infer:

```text
A relates-to B
B relates-to C
therefore A relates-to C
```

No transitive closure, graph traversal, path score, centrality, embedding
similarity or neighborhood count can become epistemic authority.

```text
GRAPH LINK ≠ CLAIM
GRAPH PATH ≠ INFERENCE PROOF
GRAPH DISTANCE ≠ SEMANTIC CONFIDENCE
```

---

## 12. 🔐 Canonical identity requirements for a future pure primitive

The exact implementation contract is **not frozen here**, but readiness requires
it to preserve the same deterministic discipline as PCR-v0.1.

A later contract must freeze:

```text
contract version
canonical JSON profile
fingerprint domain separation
hard byte/item caps
local caller budget
exact endpoint canonicalization rules
exact relation vocabulary
exact orientation vocabulary
exact origin vocabulary
exact scope/reference shapes
```

The future fingerprint must cover every semantic input, including:

```text
endpoint claim_id values
endpoint PCR fingerprints
relation type
orientation
relation origin + actor
source assertion anchor if any
basis anchors
conditions/moderators/exceptions/unknowns/transfer limits
budget
contract version
```

Caller-supplied final fingerprint is forbidden.

Fingerprint meaning:

```text
exact-input identity evidence
≠ source admission
≠ relation truth
≠ evidence support
≠ confidence
≠ freshness
≠ bearer permission
```

---

## 13. 🧪 Required adversarial families for a later contract

A later implementation contract is not eligible for Owner GO unless it makes the
following families executable and specific.

```text
TR-T01  analogy cannot silently become mechanism
TR-T02  correlation cannot silently become causation
TR-T03  temporal order cannot silently become causation
TR-T04  EVIDENTIAL relation cannot manufacture SUPPORTED
TR-T05  CONTRADICTORY relation cannot manufacture EvidenceGateOutcome.CONTRADICTED
TR-T06  source assertion cannot become verified relation truth by attribution alone
TR-T07  Mentaury-derived relation cannot become independent evidence for itself
TR-T08  relation type cannot carry hidden confidence/reliability semantics
TR-T09  graph adjacency/path/count cannot propagate epistemic authority
TR-T10  exact endpoint fingerprint change cannot be ignored
TR-T11  scope/moderator/exception/transfer-limit loss must fail closed
TR-T12  UNKNOWN cannot be implicitly upgraded to stronger relation type
TR-T13  directed endpoint reversal changes semantic identity
TR-T14  symmetric endpoint order must obey deterministic canonical order
TR-T15  self-relation and malformed endpoint anchors fail closed
TR-T16  valid relation representation grants no belief/action/retrieval/identity/M3/runtime authority
```

---

## 14. 🔁 Required metamorphic families

```text
TR-M01  left/right exact PCR fingerprint change → relation fingerprint changes
TR-M02  claim_id change → relation fingerprint changes
TR-M03  relation type change → relation fingerprint changes
TR-M04  orientation change → relation fingerprint changes or invalid pair fails closed
TR-M05  origin mode/actor change → relation fingerprint changes
TR-M06  source-assertion anchor change → relation fingerprint changes
TR-M07  basis-anchor change → relation fingerprint changes but no support status appears
TR-M08  condition/moderator/exception/unknown/transfer-limit change → fingerprint changes
TR-M09  directed endpoint reversal → distinct semantic identity
TR-M10  symmetric unsorted/duplicate endpoint input → fail closed, not silently repaired
TR-M11  repeated basis/source references cannot change relation into evidence support
TR-M12  exact repeated typed input → deterministic identical representation
```

---

## 15. 🧼 Required purity families

The future first primitive remains representation-only.

```text
TR-P01 no network
TR-P02 no filesystem
TR-P03 no database / graph persistence
TR-P04 no environment / ambient clock
TR-P05 no LLM/model/embedding/retriever/Atlas
TR-P06 no graph traversal or relation discovery
TR-P07 no Evidence Gate invocation
TR-P08 no belief creation/revision
TR-P09 no Action Gate/tool/capability invocation
TR-P10 no identity/relationship/M3 mutation
TR-P11 no scheduler/background/autonomous loop
TR-P12 deterministic output for exact typed input
```

---

## 16. 🧯 Threat model

### TR-THREAT-01 — Graph Truth Laundering

```text
graph edge exists
→ treated as epistemic relation
→ treated as confidence
→ treated as truth
```

Blocked by: graph/storage absence from the representation contract and explicit
`GRAPH LINK ≠ EPISTEMIC AUTHORITY`.

### TR-THREAT-02 — Causal Escalation

```text
correlation / temporal sequence
→ causal label
→ mechanism claim
```

Blocked by: closed relation type + orientation compatibility + no implicit type
promotion.

### TR-THREAT-03 — Evidence Laundering

```text
EVIDENTIAL or CONTRADICTORY relation
→ interpreted as Evidence Gate result
```

Blocked by: P0-015 ownership remains unchanged.

### TR-THREAT-04 — Self-Conditioning / Epistemic Echo

```text
Mentaury generates relation R
→ stores/reads R as independent support for R
→ confidence inflates
```

Blocked by: generated relation is not evidence for itself; basis and evidence
remain separate owners.

### TR-THREAT-05 — Scope Erasure

```text
conditional relation
→ conditions/exceptions omitted
→ universalized statement
```

Blocked by: mandatory scope preservation in later contract design.

### TR-THREAT-06 — Revision Drift

```text
claim changes
→ relation still points to claim_id only
→ relation silently floats to new meaning
```

Blocked by: exact `claim_id + PCR input_fingerprint` endpoint anchor.

---

## 17. ✅ Readiness result

The architecture is sufficiently discriminated to proceed to a **later separate
candidate-selection / implementation-contract freeze** for a pure bounded Typed
Relations representation.

```text
PHASE_5_TYPED_RELATIONS_CONTRACT_READINESS = READY
PHASE_5_SELECTED_RELATION_MODEL = ANCHORED_TYPED_RELATION_CANDIDATE
PHASE_5_RELATION_VOCABULARY = CLOSED_V0_1_CORE
PHASE_5_ENDPOINT_BINDING = PCR_CLAIM_ID_PLUS_INPUT_FINGERPRINT
PHASE_5_RELATION_CONFIDENCE = NOT_IN_V0_1
PHASE_5_GRAPH_AUTHORITY = NONE
PHASE_5_EVIDENCE_GATE_AUTHORITY = UNCHANGED
PHASE_5_CANDIDATE_SELECTION = NOT_STARTED
PHASE_5_IMPLEMENTATION_CONTRACT = NOT_FROZEN
PHASE_5_IMPLEMENTATION = NOT_STARTED
PHASE_5_OWNER_GO = NOT_GRANTED
PHASE_5_RUNTIME = NOT_AUTHORIZED
```

Residual work for the next separate docs-only block:

1. select or reject one exact pure implementation candidate;
2. freeze exact dataclasses/enums/API/exceptions/budgets/canonical profile;
3. freeze exact reference shapes for conditions/moderators/exceptions;
4. turn TR-T / TR-M / TR-P families into a concrete contract matrix;
5. preserve all existing PCR/P0-014/P0-015/NPG authority boundaries;
6. stop again before implementation Owner GO.

---

## 18. ⛔ Mandatory stop

After this readiness document is reviewed, merged, verified and synchronized:

```text
STOP
```

This block does **not** authorize:

```text
Typed Relations candidate implementation
Typed Relations implementation contract freeze
Typed Relations Owner GO
EPR-v0.1 implementation
claim→belief binding
terminal reconsideration lineage
Inference Bridge Audit implementation
Hypothesis Discrimination implementation
Cognitive Inquiry / OEO / scheduler
persistence / graph database
retrieval / Atlas
LLM/model/embeddings
Action Gate / tools
belief or Evidence Gate mutation
identity / relationship / M3 mutation
autonomous/background cognition
runtime activation
deployment
```

The next possible bounded step is only a fresh, separately authorized:

```text
PHASE_5_TYPED_RELATIONS_CANDIDATE_SELECTION_AND_CONTRACT_FREEZE · DOCS_ONLY
```

with a new live reconciliation first.