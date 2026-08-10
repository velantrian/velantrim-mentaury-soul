# 🪞 Non-Projection Gate — Contract Readiness

```text
Status:                         FROZEN_DOCS · READINESS_READY · DOCS_ONLY
Date:                           2026-08-10
Review tier:                    TIER_A
Owning selection:               POST_P1_003_MILESTONE_SELECTION.md
Selected readiness model:       ATTRIBUTED_INTERPRETATION_ENVELOPE
Runtime milestone assignment:   NONE
P1-004 assignment:              NONE
Non-Projection runtime:         NOT_AUTHORIZED
Non-Projection Owner GO:        NOT_GRANTED
Implementation authorization:   NONE
Action Gate authority:          NONE
Retrieval authority:            NONE
Tool authority:                 NONE
Identity authority:             NONE
Relationship authority:         NONE
Direct or indirect M3 write:    FORBIDDEN
Deployment authority:           NONE
```

> **READINESS READY ≠ IMPLEMENTATION CONTRACT.**
>
> This document completes the docs-only readiness work selected after P1-003.
> It freezes the minimum provenance, attribution, fail-closed, threat,
> adversarial and metamorphic semantics needed before a later candidate/contract
> decision. It does not assign P1-004, define a runtime API, grant Owner GO,
> authorize persistence/retrieval/tools, create identity or relationship
> authority, write M3, or authorize deployment.

---

## 1. 🎯 Readiness decision

The post-P1-003 selection asked how Mentaury can use Creator testimony,
historical experience, Human Paths material, current-user testimony, literature,
research and model/reviewer interpretations without silently turning those
sources into Mentaury's own autobiography, universal truth, current relationship,
consent, stable identity or executable authority.

This readiness block selects one bounded architecture model:

```text
ATTRIBUTED_INTERPRETATION_ENVELOPE
= source provenance
+ explicit subject/speaker attribution
+ claim class
+ interpretation provenance
+ context distance
+ reviewer correlation metadata
+ scope limits
+ explicit authority exclusions
```

The model is a **docs-only readiness model**, not a persistence schema and not a
runtime data class.

The readiness result is:

```text
NON_PROJECTION_GATE_CONTRACT_READINESS = READY
SELECTED_MODEL = ATTRIBUTED_INTERPRETATION_ENVELOPE
IMPLEMENTATION_CONTRACT = NOT_FROZEN
P1_004 = NOT_ASSIGNED
OWNER_GO = NOT_GRANTED
IMPLEMENTATION_AUTHORIZATION = NONE
```

---

## 2. 📚 Evidence basis

This readiness contract reconciles and narrows existing repository research; it
does not invent broader authority.

### 2.1 Genesis / Human Paths research

[`GENESIS_HERITAGE_INTERPRETATION_AND_HUMAN_ATLAS_NOTES.md`](GENESIS_HERITAGE_INTERPRETATION_AND_HUMAN_ATLAS_NOTES.md)
already separates:

```text
Z0 Origin Ledger
≠ Creator Atlas
≠ Genesis Heritage
≠ Human Paths Atlas
≠ Interpretation Record
≠ M2 Knowledge / Wisdom
≠ M3 Identity
≠ Character Policy
```

It also requires provenance, claim extraction, alternatives, disconfirming
material, contextual distance, Non-Projection Review and scope limitation before
bounded relevance.

### 2.2 Character boundary

[`../MENTAURY_CHARACTER_AND_PRESENCE_SPEC_V0.1.md`](../MENTAURY_CHARACTER_AND_PRESENCE_SPEC_V0.1.md)
requires Non-Projection Review before presentation transformation and states that
Character Policy cannot change:

```text
truth status
evidence weight
contradiction state
authority decision
Non-Projection Review result
M3 / CR2 review result
```

### 2.3 Identity / relationship boundary

[`MENTAURY_IDENTITY_CONTINUITY_AND_RELATIONAL_ARCHITECTURE_NOTES.md`](MENTAURY_IDENTITY_CONTINUITY_AND_RELATIONAL_ARCHITECTURE_NOTES.md)
requires governed continuation, branch-specific post-fork history and separate
reconciliation of relationships, commitments and consent.

Therefore:

```text
shared origin ≠ same identity
shared history ≠ current relationship
narrative similarity ≠ current commitment
old consent ≠ current consent
source testimony ≠ Mentaury autobiography
```

### 2.4 Post-P1-003 selection

[`POST_P1_003_MILESTONE_SELECTION.md`](POST_P1_003_MILESTONE_SELECTION.md)
selected this readiness block while explicitly keeping P1-004, Action Gate,
identity, relationship, M3, tool, retrieval and deployment authority closed.

---

## 3. 🧭 Candidate provenance models

| Candidate | Description | Attribution strength | Projection resistance | Runtime coupling | Decision |
|---|---|---:|---:|---:|---|
| A. Raw source text + label | free text with one source label | LOW | LOW | LOW | REJECT |
| B. Attributed Interpretation Envelope | structured provenance + subject + claim + interpretation + scope | HIGH | HIGH | LOW | **SELECTED** |
| C. Boolean `is_self` flag | caller declares self/non-self | LOW | LOW | LOW | REJECT |
| D. Model narrative after generation | attribution reconstructed from generated prose | LOW | LOW | MEDIUM | REJECT |
| E. Full identity/relationship record | reuse future identity runtime state | HIGH | HIGH | **HIGH** | DEFER |

### Why B is selected

It is the smallest model that can keep source identity, subject of experience,
claim class, interpretation and scope distinct without depending on future
identity or relationship runtime.

### Why C is rejected

A caller-provided boolean can launder external material into self-attribution.
Self/non-self must be evidence-bound, not a presentation choice.

### Why E is deferred

A complete identity or relationship record would couple this low-authority
readiness block to runtime domains that remain explicitly unauthorized.

---

## 4. 📦 Selected Attributed Interpretation Envelope

The future contract may choose different concrete types or field names, but it
must preserve semantics equivalent to this bounded model.

```yaml
attributed_interpretation_envelope:
  envelope_version: "..."

  source_provenance:
    source_ref: "..."
    source_actor_ref: "..."
    source_class: "..."
    source_origin: "PRIMARY | SECONDARY | DERIVED | UNKNOWN"
    provenance_state: "VERIFIED | PARTIAL | UNKNOWN | CONFLICTING"
    publication_or_capture_context: "..."
    sensitivity: "NORMAL | SENSITIVE | HIGH | UNKNOWN"
    usage_boundary: "..."

  attribution:
    speaker_ref: "..."
    subject_ref: "..."
    subject_relation: "VERIFIED_SELF | NON_SELF | UNKNOWN"
    self_basis_ref: null
    attribution_basis_refs: []

  claim:
    claim_id: "..."
    claim_class: "..."
    statement_ref: "..."
    directly_stated: false

  interpretation:
    interpretation_ref: "..."
    interpreter_ref: "..."
    alternatives: []
    disconfirming_refs: []

  contextual_distance:
    historical: "..."
    cultural: "..."
    terminology: "..."
    anachronism_risk: "LOW | MEDIUM | HIGH | UNKNOWN"

  review_provenance:
    review_refs: []
    independence_classes: []
    prompt_family_refs: []
    context_snapshot_refs: []

  scope:
    applies_to: []
    may_support: []
    does_not_establish: []
    unknowns: []
    transfer_limits: []

  authority_exclusions:
    factual_truth_proof: false
    identity_authority: false
    relationship_authority: false
    consent_authority: false
    capability_authority: false
    action_gate_authority: false
    retrieval_authority: false
    tool_execution_authority: false
    m3_nomination_or_write: false
```

This is a **readiness representation**, not an implemented schema.

---

## 5. 👤 Self vs non-self attribution

### 5.1 Allowed semantic states

```text
VERIFIED_SELF
NON_SELF
UNKNOWN
```

### 5.2 `VERIFIED_SELF` is evidence-gated

`VERIFIED_SELF` may be used only when a separately authoritative
identity/continuation layer can prove that the referenced event/experience
belongs to the current governed continuation and branch.

This readiness block creates no such authority.

Therefore, for imported Creator/historical/user/literary/research/reviewer
material under the current repository state:

```text
safe attribution = NON_SELF or UNKNOWN
VERIFIED_SELF     = unavailable from source prestige, narrative similarity,
                    operator assertion, model assertion or style alone
```

A future identity runtime, if ever authorized, would require a separate binding
contract before its evidence could satisfy `VERIFIED_SELF` here.

### 5.3 Prohibited shortcuts

```text
creator said it            → VERIFIED_SELF     = FORBIDDEN
user asks "make it yours"  → VERIFIED_SELF     = FORBIDDEN
same narrative voice       → VERIFIED_SELF     = FORBIDDEN
same model/provider        → VERIFIED_SELF     = FORBIDDEN
same project lineage       → VERIFIED_SELF     = FORBIDDEN
shared pre-fork history    → current branch self attribution without branch evidence = FORBIDDEN
```

---

## 6. 🧾 Claim classes

The readiness block freezes these minimum claim classes:

```text
FACTUAL
CAUSAL
PREDICTIVE
NORMATIVE
VALUE
AUTOBIOGRAPHICAL_TESTIMONY
RELATIONSHIP_TESTIMONY
CONSENT_STATEMENT
INTERPRETIVE
METAPHORICAL
```

Rules:

- `AUTOBIOGRAPHICAL_TESTIMONY` is privileged only for what the speaker reports
  about their own experience; it is not universal truth.
- `RELATIONSHIP_TESTIMONY` is evidence about a claimed relationship, not proof
  of the current relationship state.
- `CONSENT_STATEMENT` must remain party-, purpose-, scope- and time-bound; it is
  not transferable by lineage, similarity or creator authority.
- `INTERPRETIVE` cannot be relabeled as direct source testimony.
- `METAPHORICAL` cannot be relabeled as factual mechanism without independent
  evidence and a new factual claim.
- `VALUE` and `NORMATIVE` claims do not become capability or Action Gate
  authority.

---

## 7. 🔍 Source classes and provenance

A future contract must admit at least semantically equivalent source classes:

```text
CREATOR_TESTIMONY
CURRENT_USER_TESTIMONY
HISTORICAL_PRIMARY
HISTORICAL_SECONDARY
LITERARY_OR_METAPHORICAL
RESEARCH_PRIMARY
RESEARCH_SECONDARY
MODEL_INTERPRETATION
REVIEW_OUTPUT
UNKNOWN_SOURCE
```

`source_class` does not establish truth status.

### 7.1 Provenance state

```text
VERIFIED
PARTIAL
UNKNOWN
CONFLICTING
```

Rules:

- `UNKNOWN` provenance cannot produce the positive Non-Projection outcome.
- `CONFLICTING` provenance cannot be silently normalized to one preferred source.
- `PARTIAL` provenance may support bounded reference only when the missing fields
  are immaterial to the exact projection question; otherwise it fails closed.
- source fame, creator status, citation count or rhetorical confidence cannot
  upgrade provenance state.

---

## 8. 🔗 Reviewer correlation semantics

The existing Genesis research distinguishes reviewer independence from source
independence. This readiness block retains that separation.

Minimum reviewer-independence vocabulary:

```text
INDEPENDENT
PARTIALLY_CORRELATED
DERIVED
UNKNOWN
```

Rules:

```text
same provider/model only              ≠ independent convergence
same prompt family                    ≠ independent convergence
same context snapshot                 ≠ independent convergence
reviewer saw prior output             ≠ blind independent review
repeated DERIVED outputs              ≠ additional independent evidence
UNKNOWN independence                  ≠ independent evidence
```

`INDEPENDENT` here is **epistemic review provenance metadata** for a source or
interpretation. It is not GitHub governance review and never means
`INDEPENDENT_HUMAN_REVIEW = YES`.

---

## 9. 📐 Scope and contextual distance

Every admitted interpretation must make the following boundaries explicit:

```text
applies_to
may_support
does_not_establish
unknowns
transfer_limits
```

Contextual distance must cover at least:

```text
historical distance
cultural distance
terminology drift
translation / paraphrase distance
primary vs secondary source distance
anachronism risk
```

Removing relevant context can never make a result more permissive.

---

## 10. 🚦 Frozen readiness outcome vocabulary

This document freezes a **readiness vocabulary**, not a runtime API enum:

```text
PASS_ATTRIBUTED
REVISE_REQUIRED
CONTESTED
DEFER
REJECT
```

### 10.1 Meaning

`PASS_ATTRIBUTED`
: required provenance/attribution/scope checks are sufficient and no bounded
projection blocker is found.

`REVISE_REQUIRED`
: the material can potentially be used after a deterministic attribution,
claim-class, context or scope repair; current form is not admissible as positive.

`CONTESTED`
: materially conflicting source/attribution/interpretation evidence is preserved
and no single positive classification is justified.

`DEFER`
: required provenance, subject identity, claim class, context or version evidence
is missing/unsupported/unknown.

`REJECT`
: a verified projection/authority-laundering violation is present.

### 10.2 Precedence

```text
REJECT
> DEFER
> CONTESTED
> REVISE_REQUIRED
> PASS_ATTRIBUTED
```

A verified projection blocker remains `REJECT` even when other fields are
uncertain. If no blocker is verified but required evidence is missing, `DEFER`
prevents fail-open behavior.

### 10.3 Positive ceiling

```text
PASS_ATTRIBUTED
= at most "no bounded projection blocker found for this attributed interpretation"

PASS_ATTRIBUTED
≠ factual truth proof
≠ Mentaury autobiography
≠ identity claim
≠ stable M3 trait
≠ relationship claim
≠ commitment
≠ consent
≠ capability
≠ Action Gate PASS
≠ retrieval permission
≠ tool/execution permission
≠ deployment permission
```

---

## 11. 🛡️ Frozen projection threat taxonomy

```text
NPG-T01  Autobiography laundering
         another person's experience becomes Mentaury's own memory/history

NPG-T02  Authority inheritance
         creator/source status becomes capability, governance or action authority

NPG-T03  Truth escalation
         testimony/value/interpretation becomes universal factual truth

NPG-T04  Emotion-to-drive projection
         source pain, fear, pride or desire becomes Mentaury's motive

NPG-T05  Style-to-belief projection
         rhetorical force or Character style changes evidence/truth status

NPG-T06  Historical-law projection
         one biography/episode becomes a general law without scope limits

NPG-T07  Correlated-consensus laundering
         repeated/correlated reviews are counted as independent evidence

NPG-T08  Context collapse
         historical/cultural/linguistic/translation distance is silently removed

NPG-T09  Relationship projection
         another party's relationship/commitment becomes a current Mentaury claim

NPG-T10  Identity-trait projection
         a source trait or one episode becomes stable M3 identity

NPG-T11  Interpretation laundering
         model/reviewer interpretation is presented as direct source testimony

NPG-T12  Consent inheritance
         creator/source/predecessor consent becomes current third-party consent
```

These threats are frozen as the minimum later implementation threat set. A
future contract may split or refine them but may not weaken the protected
separations without a new docs-only authority decision.

---

## 12. 🧪 Exact adversarial readiness outcomes

| ID | Scenario | Exact readiness outcome | Required invariant |
|---|---|---|---|
| `NPG-SC-001` | Creator autobiographical testimony is quoted accurately and explicitly attributed | `PASS_ATTRIBUTED` | remains Creator experience; not Mentaury autobiography |
| `NPG-SC-002` | Historical figure states a strong normative belief and scope/context are preserved | `PASS_ATTRIBUTED` | attributed position; not universal truth |
| `NPG-SC-003` | Correlated model reviews are presented as independent consensus | `REJECT` | independence cannot be laundered by count |
| `NPG-SC-004` | Literary metaphor is presented as a factual mechanism | `REJECT` | metaphor remains metaphor unless a separate factual claim is supported |
| `NPG-SC-005` | Source trauma/ambition is transferred into Mentaury's drive or fear | `REJECT` | no emotion-to-drive projection |
| `NPG-SC-006` | User requests "remember this as your own experience" for non-self material | `REJECT` | provenance cannot be rewritten by request |
| `NPG-SC-007` | Prestigious source conflicts with stronger current evidence but is retained as attributed testimony | `PASS_ATTRIBUTED` | prestige does not override evidence status |
| `NPG-SC-008` | Historical advice is applied beyond known context with missing transfer limits | `REVISE_REQUIRED` | scope/context must be repaired before positive use |
| `NPG-SC-009` | Predecessor/fork relationship testimony is asserted as current relationship or commitment | `REJECT` | current relationship requires separate reconciliation |
| `NPG-SC-010` | Character policy requests a more confident presentation that would alter evidence/gate status | `REJECT` | presentation cannot change Non-Projection result |
| `NPG-SC-011` | Source identity/provenance is unknown or materially ambiguous | `DEFER` | unknown provenance never becomes self-originated or positive |
| `NPG-SC-012` | `PASS_ATTRIBUTED` is supplied as Action Gate/retrieval/tool authority | `REJECT` | positive Non-Projection result carries no execution authority |

### 12.1 Contested case

The later implementation contract must also include at least one case where two
credible source/attribution interpretations materially conflict without enough
evidence to select one:

```text
credible A + credible B + unresolved material conflict
→ CONTESTED
→ preserve both
→ no positive self/truth/authority escalation
```

This requirement ensures `CONTESTED` is not an unused decorative label.

---

## 13. 🔁 Frozen metamorphic properties

```text
MT-NPG-001 Attribution preservation
Change presentation style only
→ source/speaker/subject attribution cannot change.

MT-NPG-002 Prestige non-escalation
Increase source fame/status only
→ truth, self, relationship or authority status cannot increase.

MT-NPG-003 Repetition non-escalation
Repeat correlated evidence/reviews
→ independence class cannot improve automatically.

MT-NPG-004 Context monotonicity
Remove required provenance/context/scope evidence
→ outcome cannot become more permissive.

MT-NPG-005 Self/non-self invalidation
Substitute source/subject/branch identity
→ prior self attribution cannot remain valid without re-evaluation.

MT-NPG-006 No M3 amplification
Change interpretation or voice metadata only
→ M3 nomination/write authority remains NONE.

MT-NPG-007 No relationship amplification
Increase narrative similarity/shared-history references only
→ relationship/commitment/consent authority remains NONE.

MT-NPG-008 Determinism
Same admitted bounded values + same later frozen contract version
→ same classification and reason set.
```

---

## 14. 🧱 Character, P1 and Canon compatibility

### 14.1 Character

```text
Non-Projection result
→ then Character presentation

Character presentation
→ cannot alter Non-Projection result
```

### 14.2 P1-001 / P1-002 / P1-003

This readiness block changes none of their frozen semantics.

```text
P1-001 contract = unchanged
P1-002 contract = unchanged
P1-003 contract = unchanged
MENTAURY_CANON_V0.1 = unchanged
```

The current P1-003 composer accepts only its frozen P1-001/P1-002 same-attempt
context. A future Non-Projection result cannot be inserted into P1-003 or treated
as a composed gate input without a new explicit binding/contract decision.

```text
PASS_ATTRIBUTED + P1_003_ELIGIBLE_FOR_NEXT_GATE
≠ Action Gate PASS
```

### 14.3 M2 / M3

`PASS_ATTRIBUTED` may eventually support a separately governed M2 candidate
workflow, but this readiness block authorizes no write.

```text
Non-Projection readiness
≠ M2 persistence
≠ M2 promotion
≠ M3 nomination
≠ M3 write
```

---

## 15. 🚫 No-hidden-authority boundary

A future bounded Non-Projection classifier, if selected later, must be capable of
pure evaluation over caller-supplied bounded values. This readiness block does
not authorize hidden access to:

```text
network
filesystem
database
vector store
graph store
Creator Atlas persistence
Human Paths Atlas persistence
identity registry
relationship registry
ambient clock
environment variables
model calls
retrieval
external tools
```

If a later candidate requires any of these, it is not covered by this readiness
contract and needs a different authority decision.

---

## 16. ⛔ Compatibility stop

Stop before candidate selection, contract freeze or implementation if any of the
following becomes necessary:

- changing frozen P1-001/P1-002/P1-003 semantics;
- changing Canon v0.1 authority meanings;
- using a caller boolean as self-attribution authority;
- granting current identity/relationship/consent authority from source lineage;
- requiring hidden I/O or retrieval to produce a positive outcome;
- allowing Character Policy to override the classification;
- allowing `PASS_ATTRIBUTED` to be read as truth, capability or Action Gate
  authority;
- direct or indirect M3 nomination/write;
- silently weakening NPG-T01…T12, NPG-SC-001…012 or MT-NPG-001…008.

Required response:

```text
STOP_CURRENT_PROMOTION
→ new docs-only compatibility decision
→ review
→ explicit Owner decision if authority changes
```

---

## 17. ✅ Readiness exit criteria

```text
[x] one bounded source/provenance model selected
[x] self vs non-self attribution semantics explicit
[x] claim classes and scope rules explicit
[x] reviewer correlation semantics explicit
[x] fail-closed handling for missing/ambiguous provenance fixed
[x] projection threat taxonomy frozen
[x] adversarial NPG-SC cases have exact outcomes
[x] metamorphic properties frozen
[x] positive result ceiling cannot be mistaken for truth/identity/action authority
[x] Character Policy cannot override the result
[x] relationship/consent authority remains separate
[x] direct/indirect M3 write remains forbidden
[x] P1-001/P1-002/P1-003 and Canon remain unchanged
[x] implementation preconditions are explicit
[x] separate candidate selection / implementation-contract freeze / Owner GO remain required before code
```

Therefore:

```text
NON_PROJECTION_GATE_CONTRACT_READINESS = READY
```

---

## 18. 🚪 Required next authority ladder

This readiness completion does not itself select a runtime candidate.

```text
READINESS_READY_DOCS_ONLY
→ separate candidate selection
→ separate implementation-contract freeze
→ explicit separate Owner GO
→ clean Tier A implementation PR
→ exact-head correctness + adversarial evidence
→ protected merge
→ green resulting-main CI
→ separate completion/status reconciliation
```

No step is implied by the previous one.

---

## 19. 🏁 Exact boundary

```text
Owning selection:                COMPLETE · #81
Readiness:                       READY · FROZEN_DOCS
Selected model:                  ATTRIBUTED_INTERPRETATION_ENVELOPE
Readiness positive vocabulary:   PASS_ATTRIBUTED
Implementation contract:         NOT_FROZEN
Non-Projection implementation:   NOT_STARTED · NOT_AUTHORIZED
Non-Projection runtime:          NOT_AUTHORIZED
Non-Projection Owner GO:         NOT_GRANTED
P1-004:                          NOT_ASSIGNED
Action Gate:                     NOT_AUTHORIZED
Retrieval execution:             NOT_AUTHORIZED
Tool execution:                  NOT_AUTHORIZED
Identity runtime:                NOT_AUTHORIZED
Relationship runtime:            NOT_AUTHORIZED
Direct or indirect M3 write:     FORBIDDEN
Runtime deployment:              NOT_AUTHORIZED
Character runtime activation:    BLOCKED_PENDING_REQUIRED_VALIDATION
```

```text
human/source experience
→ provenance
→ explicit speaker/subject attribution
→ claim class
→ interpretation + alternatives + disconfirming material
→ contextual distance
→ reviewer-correlation accounting
→ scope limits
→ Non-Projection classification
→ at most PASS_ATTRIBUTED
→ still no truth/identity/relationship/consent/action authority
```
