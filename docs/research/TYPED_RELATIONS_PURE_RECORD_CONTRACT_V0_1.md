# 🔗 ATR-v0.1 — Pure Anchored Typed Relation Record Contract

```text
Status:                              FROZEN_DOCS · DOCS_ONLY · IMPLEMENTATION_CONTRACT
Date:                                2026-08-12
Tracking issue:                      #113
Authoritative baseline:              25675f2d60f43d0b9e5e030662f82706bf212bb5
Owning readiness:                    TYPED_RELATIONS_CONTRACT_READINESS.md
Owning candidate selection:          TYPED_RELATIONS_CANDIDATE_SELECTION.md
Candidate:                           PURE_ANCHORED_TYPED_RELATION_RECORD
Contract version:                    ATR-v0.1
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

> **FROZEN CONTRACT ≠ OWNER GO ≠ IMPLEMENTATION.**
>
> ATR-v0.1 freezes the exact future pure representation contract only. Nothing in
> this document authorizes creation of `src/mentaury/relations/**`.

---

## 1. 🎯 Exact future primitive

Future source surface, if later separately authorized:

```text
src/mentaury/relations/__init__.py
src/mentaury/relations/contracts.py
src/mentaury/relations/representation.py
```

No other source path is part of ATR-v0.1.

Exact public function:

```python
represent_typed_relation(
    *,
    endpoints: RelationEndpoints,
    semantics: RelationSemantics,
    provenance: RelationProvenance,
    scope: RelationScope,
    budget: RelationRepresentationBudget,
) -> AnchoredTypedRelationRecord
```

The function is pure and caller-supplied. It performs representation only.

---

## 2. 🔐 Frozen constants

```text
TYPED_RELATION_CONTRACT_VERSION = "ATR-v0.1"
CANONICAL_PROFILE = "MENTAURY_CANONICAL_JSON_V1"
INPUT_FINGERPRINT_DOMAIN = "MENTAURY_ANCHORED_TYPED_RELATION_INPUT_V1"

HARD_MAX_STRING_BYTES = 4096
HARD_MAX_TUPLE_ITEMS = 512
HARD_MAX_CANONICAL_INPUT_BYTES = 262144
```

The implementation must stop-and-reconcile if the repository canonical JSON
profile no longer equals `MENTAURY_CANONICAL_JSON_V1`.

---

## 3. 🧩 Frozen enums

```python
class RelationType(StrEnum):
    CAUSAL = "CAUSAL"
    CORRELATIONAL = "CORRELATIONAL"
    TEMPORAL = "TEMPORAL"
    ANALOGICAL = "ANALOGICAL"
    TAXONOMIC = "TAXONOMIC"
    MECHANISTIC = "MECHANISTIC"
    EVIDENTIAL = "EVIDENTIAL"
    CONTRADICTORY = "CONTRADICTORY"
    UNKNOWN = "UNKNOWN"

class RelationOrientation(StrEnum):
    DIRECTED = "DIRECTED"
    SYMMETRIC = "SYMMETRIC"
    UNKNOWN = "UNKNOWN"

class RelationOrigin(StrEnum):
    SOURCE_ASSERTED = "SOURCE_ASSERTED"
    MENTAURY_DERIVED = "MENTAURY_DERIVED"
    EXTERNAL_DERIVED = "EXTERNAL_DERIVED"
    UNKNOWN = "UNKNOWN"

class ScopeReferenceKind(StrEnum):
    CLAIM_ANCHOR = "CLAIM_ANCHOR"
    CONTEXT_REF = "CONTEXT_REF"
```

No open caller-defined enum extension is admitted in ATR-v0.1.

---

## 4. 🧬 Frozen immutable dataclasses

Exact shape:

```python
@dataclass(frozen=True, slots=True)
class ClaimAnchor:
    claim_id: str
    claim_input_fingerprint: str

@dataclass(frozen=True, slots=True)
class RelationEndpoints:
    left_anchor: ClaimAnchor
    right_anchor: ClaimAnchor

@dataclass(frozen=True, slots=True)
class RelationSemantics:
    relation_type: RelationType
    orientation: RelationOrientation

@dataclass(frozen=True, slots=True)
class ScopeReference:
    kind: ScopeReferenceKind
    reference_id: str
    claim_input_fingerprint: str | None

@dataclass(frozen=True, slots=True)
class RelationProvenance:
    origin: RelationOrigin
    origin_actor_ref: str | None
    source_assertion_anchor: ClaimAnchor | None
    basis_anchors: tuple[ClaimAnchor, ...]

@dataclass(frozen=True, slots=True)
class RelationScope:
    conditions: tuple[ScopeReference, ...]
    moderators: tuple[ScopeReference, ...]
    exceptions: tuple[ScopeReference, ...]
    unknowns: tuple[ScopeReference, ...]
    transfer_limits: tuple[ScopeReference, ...]

@dataclass(frozen=True, slots=True)
class RelationRepresentationBudget:
    max_string_bytes: int
    max_tuple_items: int
    max_canonical_input_bytes: int

@dataclass(frozen=True, slots=True)
class AnchoredTypedRelationRecord:
    contract_version: str
    endpoints: RelationEndpoints
    semantics: RelationSemantics
    provenance: RelationProvenance
    scope: RelationScope
    input_fingerprint: str
```

No field for confidence, probability, reliability, support status, Evidence Gate
outcome, belief status, truth status, action permission, retrieval permission,
runtime permission, graph score or centrality is allowed.

---

## 5. 🪢 ClaimAnchor validation

`ClaimAnchor` reuses exact PCR-v0.1 identity:

```text
claim_id
+ ProvenanceClaimRecord.input_fingerprint
```

Validation:

```text
claim_id
→ exact str
→ non-empty
→ no leading/trailing whitespace
→ valid UTF-8
→ <= HARD_MAX_STRING_BYTES

claim_input_fingerprint
→ exact str
→ exactly 64 chars
→ lowercase hexadecimal sha256 form
```

The primitive does not fetch or authenticate PCR records. The caller supplies the
anchor. ATR-v0.1 validates shape only.

```text
VALID ClaimAnchor
≠ claim exists
≠ claim is current
≠ claim is true
≠ source admitted
```

---

## 6. ↔️ Endpoint invariants

Exactly two endpoint anchors are allowed.

```text
left_anchor != right_anchor
```

Exact self-relations fail closed.

For directed relations:

```text
left_anchor → right_anchor
```

Order is semantic and reversal changes input identity.

For symmetric relations, caller input must already be in canonical order using:

```text
(claim_id, claim_input_fingerprint)
```

ascending lexical tuple order.

Unsorted symmetric endpoints fail closed. The implementation must not silently
reorder them.

---

## 7. 🧭 Relation type ↔ orientation compatibility

Frozen compatibility matrix:

```text
CAUSAL         → DIRECTED only
CORRELATIONAL  → SYMMETRIC only
TEMPORAL       → DIRECTED only
ANALOGICAL     → SYMMETRIC only
TAXONOMIC      → DIRECTED only
MECHANISTIC    → DIRECTED only
EVIDENTIAL     → DIRECTED only
CONTRADICTORY  → SYMMETRIC only
UNKNOWN        → UNKNOWN | DIRECTED | SYMMETRIC
```

Any incompatible pair raises `TypedRelationContractError`.

No silent repair or coercion is permitted.

---

## 8. 🪪 ScopeReference invariants

Frozen tagged union semantics:

```text
CLAIM_ANCHOR
→ reference_id is a PCR claim_id
→ claim_input_fingerprint REQUIRED and valid lowercase sha256

CONTEXT_REF
→ reference_id is a caller-supplied non-epistemic context identifier
→ claim_input_fingerprint MUST be None
```

All reference IDs obey exact string rules.

Each scope tuple must be:

```text
exact tuple
<= HARD_MAX_TUPLE_ITEMS
already canonical-sort ordered
unique
```

Canonical `ScopeReference` sort key:

```text
(kind.value, reference_id, claim_input_fingerprint or "")
```

The implementation rejects unsorted or duplicate scope tuples rather than
normalizing them silently.

```text
CONTEXT_REF ≠ CLAIM
CLAIM_ANCHOR ≠ EVIDENCE SUPPORT
```

---

## 9. 🪪 Relation provenance invariants

### SOURCE_ASSERTED

```text
origin_actor_ref = REQUIRED
source_assertion_anchor = REQUIRED
basis_anchors = zero or more exact PCR ClaimAnchors
```

The source assertion anchor must be distinct from both relation endpoints.

Meaning:

```text
source asserted relation R
≠ R true
≠ R supported
```

### MENTAURY_DERIVED

```text
origin_actor_ref = REQUIRED
source_assertion_anchor = MUST be None
basis_anchors = NON_EMPTY
```

### EXTERNAL_DERIVED

```text
origin_actor_ref = REQUIRED
source_assertion_anchor = MUST be None
basis_anchors = NON_EMPTY
```

### UNKNOWN

```text
origin_actor_ref = MUST be None
source_assertion_anchor = MUST be None
basis_anchors = zero or more
```

No relation-record IDs are admitted as basis items. Basis is PCR ClaimAnchor-only,
which prevents direct recursive relation-self-support inside ATR-v0.1.

All `basis_anchors` must be exact tuple, canonical-sort ordered, unique, and within
hard/local tuple budgets.

Canonical ClaimAnchor sort key:

```text
(claim_id, claim_input_fingerprint)
```

---

## 10. 🧭 Relation scope

ATR-v0.1 preserves five independent immutable collections:

```text
conditions
moderators
exceptions
unknowns
transfer_limits
```

No collection may be silently dropped during canonicalization.

```text
condition present ≠ verified condition
exception present ≠ global falsification
no exception listed ≠ universal law
empty transfer_limits ≠ permission for universal generalization
```

All changes to any scope collection change deterministic input identity.

---

## 11. 🚫 No confidence surface

ATR-v0.1 contains no:

```text
confidence
probability
reliability
weight
source_count
support_score
graph_score
centrality
```

Uncertainty is represented through:

```text
RelationType.UNKNOWN
+ scope.unknowns
+ conditions / moderators / exceptions / transfer_limits
```

not a pseudo-calibrated score.

---

## 12. 🧯 Anti-promotion laws

```text
CORRELATIONAL ≠ CAUSAL
TEMPORAL ≠ CAUSAL
ANALOGICAL ≠ MECHANISTIC
EVIDENTIAL ≠ SUPPORTED
CONTRADICTORY ≠ EvidenceGateOutcome.CONTRADICTED
TAXONOMIC ≠ objective ontology truth
SOURCE_ASSERTED ≠ true
MENTAURY_DERIVED ≠ independent evidence for itself
GRAPH LINK / PATH / COUNT ≠ EPISTEMIC AUTHORITY
```

ATR-v0.1 performs no relation-type promotion. A caller wishing to represent a
different relation type supplies a new exact input and obtains a different
fingerprint.

No in-place relation revision lineage is defined in ATR-v0.1.

---

## 13. 💰 Hard-cap and local-budget semantics

Frozen exceptions:

```python
class TypedRelationContractError(ValueError): ...
class TypedRelationBudgetExceeded(ValueError): ...
```

Hard-cap or structural violation:

```text
→ TypedRelationContractError
```

Valid hard-cap input exceeding caller local budget:

```text
→ TypedRelationBudgetExceeded
```

`RelationRepresentationBudget` must contain positive exact integers not exceeding
frozen hard caps.

Local budget applies to every string, every tuple item count, and final canonical
input byte length.

No truncation, summarization, dropping, reordering or lossy repair is allowed.

---

## 14. 🔐 Canonical input and fingerprint

Canonical profile:

```text
MENTAURY_CANONICAL_JSON_V1
```

Canonical input object must be exactly:

```json
{
  "contract_version": "ATR-v0.1",
  "endpoints": "RelationEndpoints.to_value()",
  "semantics": "RelationSemantics.to_value()",
  "provenance": "RelationProvenance.to_value()",
  "scope": "RelationScope.to_value()",
  "budget": "RelationRepresentationBudget.to_value()"
}
```

No output fingerprint field appears inside the fingerprint input.

Fingerprint:

```text
sha256(
  b"MENTAURY_ANCHORED_TYPED_RELATION_INPUT_V1"
  + b"\x00"
  + canonical_json_bytes(exact_input)
).hexdigest()
```

The fingerprint covers every semantic input including:

- endpoint claim IDs;
- endpoint PCR fingerprints;
- relation type;
- orientation;
- origin mode and actor;
- source assertion anchor;
- basis anchors;
- all five scope collections;
- local budget;
- contract version.

Fingerprint meaning:

```text
exact-input identity evidence
≠ truth
≠ support
≠ confidence
≠ freshness
≠ source admission
≠ permission
≠ runtime authority
```

---

## 15. 📦 Exact output meaning

Successful output:

```text
AnchoredTypedRelationRecord
```

means only:

> exact caller-supplied ATR-v0.1 relation input was structurally valid, within
> local/hard budgets, canonicalizable under the frozen profile, and represented
> deterministically.

It does **not** mean:

```text
relation exists in the world
relation is true
causal relation established
mechanism established
source authenticated
Evidence Gate passed
belief created or revised
graph edge persisted
retrieval allowed
action/tool allowed
identity/relationship updated
M3 admitted
runtime activated
```

---

## 16. 🧪 Frozen executable threat requirements

A later implementation PR must make all requirements executable.

```text
TR-T01  ANALOGICAL cannot silently become MECHANISTIC
TR-T02  CORRELATIONAL cannot silently become CAUSAL
TR-T03  TEMPORAL cannot silently become CAUSAL
TR-T04  EVIDENTIAL cannot emit/manufacture SUPPORTED
TR-T05  CONTRADICTORY cannot emit/manufacture EvidenceGateOutcome.CONTRADICTED
TR-T06  SOURCE_ASSERTED cannot become verified relation truth by attribution alone
TR-T07  MENTAURY_DERIVED cannot become independent evidence for itself
TR-T08  record surface contains no confidence/probability/reliability semantics
TR-T09  graph adjacency/path/count cannot propagate epistemic authority
TR-T10  endpoint PCR fingerprint change cannot be ignored
TR-T11  conditions/moderators/exceptions/unknowns/transfer_limits cannot be dropped
TR-T12  UNKNOWN cannot be implicitly upgraded
TR-T13  directed endpoint reversal changes identity
TR-T14  symmetric unsorted endpoints fail closed
TR-T15  self-relation or malformed anchor fails closed
TR-T16  valid record grants no belief/action/retrieval/identity/M3/runtime authority
```

---

## 17. 🔁 Frozen metamorphic requirements

```text
TR-M01 endpoint left PCR fingerprint change → fingerprint changes
TR-M02 endpoint claim_id change → fingerprint changes
TR-M03 relation type change → fingerprint changes
TR-M04 orientation change → fingerprint changes or incompatible pair fails closed
TR-M05 origin mode or actor change → fingerprint changes
TR-M06 source assertion anchor change → fingerprint changes
TR-M07 basis anchor change → fingerprint changes without support status
TR-M08 any scope reference change → fingerprint changes
TR-M09 directed endpoint reversal → distinct fingerprint
TR-M10 symmetric unsorted or duplicate endpoint input → fail closed
TR-M11 repeated/duplicate basis or scope input → fail closed; never support inflation
TR-M12 exact repeated typed input → identical deterministic record
```

---

## 18. 🧼 Frozen purity requirements

```text
TR-P01 no network
TR-P02 no filesystem
TR-P03 no database / graph persistence
TR-P04 no environment / ambient clock
TR-P05 no LLM/model/embedding/retriever/Atlas
TR-P06 no graph traversal / relation discovery
TR-P07 no Evidence Gate invocation
TR-P08 no belief creation/revision
TR-P09 no Action Gate/tool/capability invocation
TR-P10 no identity/relationship/M3 mutation
TR-P11 no scheduler/background/autonomous loop
TR-P12 deterministic output for exact typed input
```

Static implementation-scope proof must show the future source package contains
only the three frozen files and imports no forbidden runtime owners.

---

## 19. 🧯 Threat model

### ATR-THREAT-01 — Graph Truth Laundering

`edge exists → relation assumed → confidence assumed → truth assumed`

Blocked by: no graph API/storage/traversal and explicit authority ceiling.

### ATR-THREAT-02 — Causal Escalation

`correlation/temporal order → causal → mechanism`

Blocked by: closed types + frozen orientation compatibility + no promotion API.

### ATR-THREAT-03 — Evidence Laundering

`EVIDENTIAL/CONTRADICTORY → Evidence Gate result`

Blocked by: no EvidenceGateOutcome field/call; P0-015 authority unchanged.

### ATR-THREAT-04 — Self-Conditioning / Epistemic Echo

`Mentaury derives R → R becomes evidence for R`

Blocked by: basis accepts PCR ClaimAnchors only; record is not evidence for itself.

### ATR-THREAT-05 — Scope Erasure

`conditional relation → scope dropped → universalized relation`

Blocked by: all five scope collections included in exact fingerprint.

### ATR-THREAT-06 — Revision Drift

`claim changes → old relation silently floats to new claim`

Blocked by: each endpoint binds exact PCR fingerprint.

### ATR-THREAT-07 — Confidence Smuggling

`custom type/field → probably_causal / strong_support → pseudo confidence`

Blocked by: exact enums and exact dataclass surface only.

---

## 20. 🔒 Existing-owner compatibility

ATR-v0.1 changes no owner.

```text
PCR-v0.1
= claim representation owner

P0-015
= sole Evidence Gate support/contradiction evaluation owner

P0-014
= ordinary non-terminal belief lifecycle owner

EPR-v0.1
= frozen docs-only routing contract; implementation NOT_STARTED
```

ATR-v0.1 does not call, wrap or replace those owners.

---

## 21. ⛔ Forbidden future implementation additions

Any implementation PR claiming ATR-v0.1 must fail review if it adds any of:

```text
confidence/probability/reliability field
EvidenceGateOutcome field or call
belief status/mutation
relation discovery
LLM/model/retrieval
embedding/vector similarity
graph traversal/persistence
transitive closure
hyperedge inference
scheduler/background loop
Action Gate/tools
identity/relationship/M3 mutation
network/filesystem/database IO
ambient clock/environment dependency
runtime/deployment activation
```

Such work requires a different milestone and authority cycle.

---

## 22. 🏁 Frozen result

```text
PHASE_5_TYPED_RELATIONS_CANDIDATE_SELECTION = SELECTED
PHASE_5_TYPED_RELATIONS_CANDIDATE = PURE_ANCHORED_TYPED_RELATION_RECORD
PHASE_5_TYPED_RELATIONS_IMPLEMENTATION_CONTRACT = FROZEN_DOCS
PHASE_5_TYPED_RELATIONS_CONTRACT_VERSION = ATR-v0.1
PHASE_5_TYPED_RELATIONS_IMPLEMENTATION = NOT_STARTED
PHASE_5_TYPED_RELATIONS_OWNER_GO = NOT_GRANTED
PHASE_5_TYPED_RELATIONS_RUNTIME = NOT_AUTHORIZED
```

> **MANDATORY STOP.** ATR-v0.1 is now an exact frozen implementation contract only.
> A new explicit single-use Owner GO scoped to `ATR-v0.1_ONLY` is required before
> any `src/mentaury/relations/**` implementation. Generic “continue/do it” from a
> prior milestone is not reusable implementation authority.