# 🧬 Phase 3 — Provenance + Claim Representation Readiness

```text
Status:                         READINESS_READY · DOCS_ONLY
Date:                           2026-08-12
Phase:                          3 · PROVENANCE + CLAIM REPRESENTATION
Baseline main:                  8e77f92a7edb2968b3297f9e32b667bceb3fb77f
Tracking issue:                 #98
Implementation:                 NOT_STARTED
Owner GO:                       NOT_GRANTED
Runtime authority:              NONE
Persistence authority:          NONE
Retrieval / Atlas authority:    NONE
Evidence Gate authority:        UNCHANGED
Identity / relationship:        NONE
Direct or indirect M3 write:    FORBIDDEN
Deployment authority:           NONE
```

> **READINESS_READY ≠ IMPLEMENTATION AUTHORITY.** This record defines the
> bounded problem and compatibility constraints only. It does not create
> runtime code, persistence, source admission, evidence promotion or Owner GO.

---

## 1. 🎯 Problem to solve

Mentaury already has bounded evidence/belief primitives and a Non-Projection
classifier, but it does not yet have one general immutable representation that
can preserve **where a claim came from, what kind of statement it is, what its
epistemic role is, and what scope it may later be evaluated within**.

The required distinction is structural:

```text
SOURCE / PROVENANCE
≠ CLAIM
≠ OBSERVATION
≠ EVIDENCE STATUS
≠ HYPOTHESIS
≠ INFERENCE
≠ INTERPRETATION
≠ BELIEF STATUS
≠ TRUTH
≠ IDENTITY
```

Phase 3 is therefore a representation milestone, not a truth-evaluation or
promotion milestone.

---

## 2. 🔍 Live compatibility findings

### 2.1 Evidence Gate remains the only owner of supported / contradicted

`src/mentaury/evidence/contracts.py` already owns:

```text
EvidenceGateOutcome.SUPPORTED
EvidenceGateOutcome.CONTRADICTED
EvidenceGateOutcome.INCONCLUSIVE
EvidenceGateOutcome.CONFLICT
```

Phase 3 MUST NOT create a second `SUPPORTED`, `CONTRADICTED`, confidence or
reliability decision vocabulary. A Provenance/Claim record may carry evidence
**references**, but references alone are not Evidence Gate results.

### 2.2 Existing claim vocabularies are orthogonal, not duplicates

The repository already has two different axes:

```text
NPG ClaimClass
= FACTUAL | CAUSAL | PREDICTIVE | NORMATIVE | VALUE |
  AUTOBIOGRAPHICAL_TESTIMONY | RELATIONSHIP_TESTIMONY |
  CONSENT_STATEMENT | INTERPRETIVE | METAPHORICAL

P0 ClaimType
= UNIVERSAL | STATISTICAL | CAUSAL | CONTEXTUAL | EXISTENTIAL | UNSPECIFIED
```

They answer different questions:

```text
ClaimClass → what kind of statement / testimony is this?
ClaimType  → what epistemic/evidence scope does the claim assert?
```

Neither may be inferred automatically from the other. A `CAUSAL` ClaimClass
still requires an explicit ClaimType, and a `CONTEXTUAL` ClaimType does not
make a statement factual, testimony, interpretation or metaphor.

### 2.3 Epistemic role is a third independent axis

To satisfy the architecture invariant `observation / evidence / hypothesis /
inference` must remain distinguishable, Phase 3 needs an explicit caller-
supplied role vocabulary:

```text
OBSERVATION
TESTIMONY
EVIDENCE_ASSERTION
HYPOTHESIS
INFERENCE
INTERPRETATION
METAPHORICAL_EXPRESSION
UNKNOWN
```

This role describes the represented proposition's position in reasoning. It is
not a truth status and does not grant promotion authority.

### 2.4 Existing source admission is not Phase 3

`research_source_record` in Identity Continuity §15 is the existing docs-only
owner for source-level research admission (`ACCEPT | CONTEXT_ONLY | REJECT`).
Phase 3 does not execute, duplicate or replace that gate. It records caller-
supplied provenance facts only.

### 2.5 NPG provenance is a gate input, not a general knowledge record

`AIE-v0.1` already contains `SourceProvenance`, attribution, claim and scope
fields for one Non-Projection evaluation. Reusing the entire AIE as the general
knowledge representation would incorrectly pull projection intent, reviewer
state and NPG-specific authority exclusions into every claim record.

The correct architecture is therefore:

```text
GENERAL PROVENANCE + CLAIM RECORD
        ↓ explicit projection when needed
AIE-v0.1 / NPG-v0.1
```

not:

```text
AIE-v0.1 = universal knowledge schema
```

---

## 3. 🧱 Required representation semantics

A future bounded component must represent, without deciding truth:

1. source identity/reference;
2. source actor if known;
3. source class/origin/provenance state;
4. capture/publication context and usage boundary;
5. material provenance gaps;
6. claim identifier and statement reference;
7. ClaimClass;
8. ClaimType;
9. epistemic role;
10. direct-vs-derived status;
11. speaker and subject attribution;
12. basis/evidence references;
13. explicit scope and transfer limits;
14. deterministic canonical fingerprint.

No raw retrieval or source discovery belongs in this phase.

---

## 4. 🚫 Forbidden semantic fields

The representation MUST NOT own or accept fields that smuggle later authority:

```text
supported = true
contradicted = true
truth = true
confidence = 0.82
reliability = 0.91
admission_status = ACCEPT
promote_to_belief = true
identity_trait = true
action_allowed = true
retrieval_allowed = true
m3_write = true
```

If later layers need these concepts they must reference the owning receipts or
run the owning gate. Representation alone cannot manufacture them.

---

## 5. 🧭 One-concept / one-owner matrix

| Concept | Existing / future owner | Phase 3 role |
|---|---|---|
| Source-level research admission | Identity Continuity §15 | reference only; no decision |
| NPG projection decision | `NPG-v0.1` | later explicit projection view only |
| `SUPPORTED / CONTRADICTED` | Evidence Gate | never duplicated |
| Belief lifecycle status | P0-014 beliefs | never duplicated |
| ClaimClass | NPG vocabulary | reuse exact semantic vocabulary |
| ClaimType | `mentaury.epistemic_types` | reuse exact class identity |
| Epistemic role | Phase 3 | new representation-only axis |
| Claim scope / transfer limits | Phase 3 record | representation only |
| Promotion / revision | future Phase 4 | explicitly excluded |

---

## 6. 🧪 Readiness threat model

The frozen implementation contract must cover at least:

```text
PCR-T01  creator testimony → Mentaury autobiography laundering
PCR-T02  ClaimClass → ClaimType implicit coercion
PCR-T03  ClaimType → ClaimClass implicit coercion
PCR-T04  epistemic-role collapse (observation/evidence/hypothesis/inference)
PCR-T05  derived interpretation presented as directly stated source claim
PCR-T06  missing/unknown provenance silently treated as verified
PCR-T07  evidence references treated as Evidence Gate support
PCR-T08  source admission status smuggled into representation
PCR-T09  supported/contradicted/truth status injected into representation
PCR-T10  analogy/correlation/inference laundered into causation
PCR-T11  uncalibrated numeric confidence/reliability laundering
PCR-T12  representation record treated as retrieval/action/identity/M3 authority
```

Required metamorphic families:

```text
PCR-M01  source_ref change changes fingerprint
PCR-M02  statement_ref change changes fingerprint
PCR-M03  ClaimClass change changes fingerprint without changing ClaimType
PCR-M04  ClaimType change changes fingerprint without changing ClaimClass
PCR-M05  epistemic-role change changes fingerprint
PCR-M06  directly_stated change changes fingerprint
PCR-M07  speaker/subject attribution change changes fingerprint
PCR-M08  scope/transfer-limit change changes fingerprint
PCR-M09  evidence/basis ref count or order cannot create support status
PCR-M10  duplicate/non-canonical tuple input fails closed
```

---

## 7. ✅ Readiness decision

```text
PHASE_3_PROVENANCE_CLAIM_REPRESENTATION_READINESS = READY
IMPLEMENTATION = NOT_STARTED
OWNER_GO = NOT_GRANTED
RUNTIME = NOT_AUTHORIZED
```

A separate candidate-selection record may now choose one bounded pure
representation primitive. A separate implementation contract may then freeze
its exact API and test obligations. Neither step grants implementation authority.
