# 📚 CLOS Evidence Ledger

```text
Status: SUPPORTING RESEARCH LEDGER
Canon: NO
Runtime authority: NONE
Purpose: preserve claim → evidence → limitation → disposition traceability
```

This ledger is deliberately smaller than the full research history in Notion / Google Docs. It records only the evidence needed to understand why the current CLOS research families survived, what that evidence does **not** prove, and how the result is currently classified.

## Evidence classes

```text
DIRECT SUPPORT
STRUCTURAL ANALOGUE
COUNTEREXAMPLE
CONTESTED INTERPRETATION
INSPIRATION ONLY
NEGATIVE EVIDENCE / FAILED REPLICATION
LONGITUDINAL BEHAVIOURAL OBSERVATION
```

`MULTIPLE AI REPORTS AGREE ≠ INDEPENDENT REPLICATION`.

AI research passes are treated as synthesis/search assistance. Scientific support comes from the underlying literature or from explicitly bounded behavioural fixtures.

---

## 1. 🌍 Coverage / possibility-space adequacy

### CLOS claim under test

```text
UNCERTAINTY WITHIN THE REPRESENTED POSSIBILITY SPACE
≠
ADEQUACY OF THE REPRESENTED POSSIBILITY SPACE ITSELF
```

### Evidence map

| Source / family | Class | Supports | Does **not** prove |
|---|---|---|---|
| Open-world / open-set recognition research, including Bendale & Boult, *Towards Open World Recognition* (CVPR 2015) | DIRECT SUPPORT for machine failure family | Systems can be forced to handle inputs/classes outside the trained/represented closed set; closed-set confidence is insufficient in open-world settings | That a system can compute a universal percentage of “world coverage” |
| Model misspecification / M-open statistical reasoning | DIRECT SUPPORT for distinction | Inference may be well-defined conditional on a model family even when the family itself is wrong/incomplete | A unique CLOS state variable or scalar metric |
| Unknown-unknown discovery work, including Lakkaraju et al. (AAAI 2017) | DIRECT SUPPORT for practical discovery failure | Important errors may sit outside the currently inspected/represented region and require targeted discovery | Exhaustive discovery of all unknown unknowns |
| Open-set/OOD detection methods | STRUCTURAL ANALOGUE / PARTIAL TOOL | Detect some forms of novelty relative to a trained distribution | `OOD DETECTION = KNOWLEDGE THAT THE HYPOTHESIS SPACE IS COMPLETE/INCOMPLETE` |

### Current disposition

`REFINE / CROSSWALK`.

Live CLOS already contains coverage uncertainty as a research decomposition. No `Coverage Module` and no universal coverage scalar are established.

### Falsifier / downgrade condition

If all material failures currently attributed to coverage can be expressed without semantic loss by existing uncertainty/currentness/open-world qualifications, the architectural residual should be downgraded to `NO NEW CONSTRUCT`.

---

## 2. 💎 Lossy representation / candidate access

### CLOS claim under test

```text
SOURCE ≠ LOSSY DERIVED VIEW
NOT REPRESENTED ≠ ABSENT
NOT SURFACED AS A CANDIDATE ≠ IRRELEVANT
```

The strongest proposed failure is **candidate-space deformation**: a lossy representation controls what downstream reasoning is allowed to consider.

### Evidence map

| Source / family | Class | Supports | Does **not** prove |
|---|---|---|---|
| Information Bottleneck / task-relative compression (Tishby, Pereira & Bialek, 1999) | STRUCTURAL ANALOGUE | Compression is meaningful relative to a preservation/relevance objective; loss can be task-conditioned | That a compressed representation knows every future-relevant omitted fact |
| Rate-distortion theory | STRUCTURAL ANALOGUE | Lossy representation is a trade-off between information preservation and resource/rate constraints | A universal cognitive distortion function for CLOS |
| Search / diagnostic generation-vs-evaluation failures | DIRECT SUPPORT for pipeline failure family | An evaluator cannot evaluate an alternative that never enters the active consideration set | That every candidate generator must be exhaustive |
| Retrieval systems / embedding search practical failure modes | IMPLEMENTATION ANALOGUE | Approximate retrieval can suppress rare or differently expressed material before reasoning | That CLOS must use embeddings, vector search, GraphRAG or any specific fallback mechanism |
| Human gist / fuzzy-trace literature | STRUCTURAL ANALOGUE | Representations with different preservation properties can support different judgments | Mandatory `verbatim vs gist` memory architecture in CLOS |

### Critical correction retained

Rejected:

```text
LOSSY VIEW MAY NEVER EXCLUDE
```

Retained:

```text
LOSSY VIEW MAY SOMETIMES EXCLUDE WITHIN A JUSTIFIED, SCOPED SUFFICIENCY CONTRACT.
LOSSY OMISSION MUST NOT SILENTLY BECOME GLOBAL NEGATIVE EVIDENCE.
```

And:

```text
DECLARED LOSS ≠ COMPLETE KNOWLEDGE OF EVERYTHING OMITTED
```

### Current disposition

`STRONGEST MATERIAL RESIDUAL CANDIDATE · REFINE / FIXTURE`.

### Falsifier / downgrade condition

If the Hidden Exception fixture is handled entirely by existing Meaning Envelope, source lineage, currentness and UNKNOWN semantics without a new distinction, disposition becomes `MERGE / NO NEW CONSTRUCT`.

---

## 3. 🛑 Task-bounded sufficiency / reason-typed stopping

### CLOS claim under test

```text
STOP ≠ TRUTH ESTABLISHED
STOP ≠ SEARCH EXHAUSTED
JUSTIFIED STOP ≠ PERMANENT CLOSURE
```

### Evidence map

| Source / family | Class | Supports | Does **not** prove |
|---|---|---|---|
| Herbert Simon — bounded rationality / satisficing | DIRECT SUPPORT for phenomenon | Real decision systems often terminate without exhaustive global optimization | A single quantitative CLOS stopping equation |
| Charnov, *Optimal Foraging, the Marginal Value Theorem* (1976) | STRUCTURAL ANALOGUE / FORMAL CASE | Leaving a search/foraging patch can be rational before all possibilities are exhausted | Universal cognition law or truth criterion |
| Rational metareasoning / value-of-computation work | DIRECT SUPPORT for one stopping basis | Further computation can be evaluated by expected decision benefit vs computational cost | Authority, prohibition, unavailable evidence, deadlines and irreducible uncertainty all reduce to one economic scalar |
| Animal uncertainty-response / opt-out studies | STRUCTURAL ANALOGUE | Some systems behave differently when their basis is weak/uncertain | Human-like conscious metacognition or a mandatory digital implementation |

### Minimum obligation retained

```text
TERMINATION MUST NOT ERASE THE MATERIAL REASON AND STATUS UNDER WHICH COGNITION TERMINATED.
```

Reopening is task/state/evidence/condition bounded.

### Current disposition

`MERGE / REFINE`.

Substantial semantics already exist in CLOS; no `Stopping Module` is established.

---

## 4. ⚖️ Endogenous state vs external-world evidence

### CLOS claim under test

```text
ENDOGENOUS SIGNAL ≠ EXTERNAL-WORLD EVIDENCE BY DEFAULT
```

### Evidence map

| Source / family | Class | Supports | Does **not** prove |
|---|---|---|---|
| Illusory-truth / repetition-familiarity research | DIRECT SUPPORT for failure family | Repetition/familiarity can change judged truth/confidence without adding independent world evidence | That internal states are never evidential |
| Information cascades / dependent social testimony | DIRECT SUPPORT for provenance problem | Agreement count can exceed independent evidence count | That consensus has zero evidential value in all settings |
| Dataset shift / calibration drift | STRUCTURAL ANALOGUE | Internal confidence calibration can become stale when environment/data relation changes | A universal drift detector or automatic correction rule |

### Correction retained

Absolute statement rejected:

```text
INTERNAL STATE CAN NEVER BE EVIDENCE
```

A signal may have evidential role when a justified causal/provenance/calibration relationship exists.

### Current disposition

`VERIFY / MERGE INTO EXISTING PROVENANCE + EPISTEMIC STATUS DISCIPLINE`.

---

## 5. ♻️ Retrieval / reconstruction / revision

### Evidence map

| Source / family | Class | Supports | Does **not** prove |
|---|---|---|---|
| Nader, Schafe & LeDoux, *Fear memories require protein synthesis in the amygdala for reconsolidation after retrieval* (Nature 2000) | DIRECT SUPPORT for bounded biological phenomenon | Reactivated memory can become labile under experimental conditions | `EVERY RETRIEVAL → REVISION` or a required digital Reconsolidation Module |
| Reconsolidation boundary-condition literature | CONTESTED / CONDITIONAL | Prediction error and other conditions matter in some paradigms | Prediction error as universal CLOS revision trigger |

### Substrate-neutral result retained

```text
SOURCE ≠ RETRIEVED FORM ≠ RECONSTRUCTION ≠ INTERPRETATION ≠ REVISION ≠ CURRENT COMMITMENT
```

Disposition: `MERGE / REFINE EXISTING MEMORY + REVISION`.

---

## 6. 🧬 Past-dependent state without explicit recall

### Evidence map

| Source / family | Class | Supports | Does **not** prove |
|---|---|---|---|
| Declarative vs non-declarative memory literature | DIRECT SUPPORT for human/animal phenomenon | Behaviour can depend on history without explicit episodic/declarative recall | Need for a separate CLOS `Implicit Memory Module` |
| Habituation / adaptive state in non-neural organisms | STRUCTURAL ANALOGUE | Persistent history-dependent response changes need not look like explicit records | Conscious cognition, representation or autobiographical memory |
| Continual learning / learned policy / calibration state in machines | DIRECT SUPPORT for machine phenomenon | Parameters/policies/calibration can encode past dependence outside explicit retrievable records | That every material adaptive change lacks provenance or must be individually logged |

### Current disposition

`REAL PHENOMENON · GAP NOT ESTABLISHED · CROSSWALK WITH ADAPTIVE STATE / CONTINUUM / SELF-REGULATION / METACOGNITION`.

---

## 7. 🌹 Rosebud long-horizon observations

Rosebud is not treated as scientific authority about its hidden implementation. It is used as a longitudinal behavioural probe.

### Observation packet

| Observation | Class | Supports | Limitation |
|---|---|---|---|
| Rosebud reported difficulty separating independent recall from reconstruction using current excerpts | LONGITUDINAL BEHAVIOURAL OBSERVATION / SELF-REPORT | `RECALLED ≠ INFERRED` is operationally important | Does not reveal hidden memory implementation |
| Rosebud explicitly identified status-promotion, provenance-erosion and correction-precedence risks | SELF-AUDIT / HYPOTHESIS GENERATION | Useful long-horizon failure classes | Self-report alone is not proof of actual frequency |
| Rosebud described `coverage uncertainty` as absent although live CLOS already contained it | BOUNDED LONGITUDINAL MISMATCH | Confident partial recall/current-state coverage can fail | Single bounded mismatch; not universal failure claim |
| Broad Native Kernel/CLOS memory cluster mixed project/scope vocabulary | BOUNDED SCOPE-EROSION SIGNAL | `TRUE SOMEWHERE IN HISTORY ≠ CURRENTLY TRUE OF THIS SURFACE` | Requires repeated delayed fixtures before stronger claim |

Strong pattern candidate:

```text
CONTENT MAY SURVIVE
WHILE
SOURCE / STATUS / CURRENTNESS / CORRECTION HISTORY DEGRADES
```

Current disposition: `FIXTURE SOURCE / CONTINUITY EVIDENCE`, not a new module.

---

## 8. Rejected architecture promotions

| Proposal | Reason for rejection / downgrade |
|---|---|
| Three universal CLOS laws | Cross-domain convergence is not universality proof |
| Coverage Module | Existing uncertainty/status semantics already partially cover the problem |
| Universal coverage scalar | No justified measure of “percentage of reality covered” |
| Universal MVT/VOI STOP law | Only one family of stopping reasons |
| Lossy view may never exclude | Bounded cognition requires scoped pruning/exclusion |
| Exhaustive declared-loss list | Unknown loss cannot be exhaustively declared by definition |
| Verbatim/gist mandatory architecture | Substrate-specific human theory |
| Prediction-error reconsolidation law | Conditional/contested biological mechanism |
| Implicit Memory Module | Phenomenon may be existing adaptive/policy/state semantics |
| Entropy as truth/coverage/stopping authority | Entropy is representation-dependent and can fall while epistemic state worsens |
| Physarum/plant adaptation proves cognition | Adaptation/history dependence does not establish cognition/representation |

---

## 9. Evidence-to-architecture rule

```text
SOURCE FOUND
≠ CLAIM ESTABLISHED
≠ FUNCTIONAL INVARIANT
≠ CLOS RESIDUAL GAP
≠ NEW CONSTRUCT
≠ OWNER ADOPTION
≠ RUNTIME AUTHORIZATION
```

For architecture promotion, use:

```text
claim
→ evidence class
→ competing explanation
→ live CLOS crosswalk
→ observable residual failure
→ discriminating fixture
→ falsifier
→ owner disposition
```

If the existing architecture can express the required behaviour without material semantic loss, the correct result is:

`NO NEW CONSTRUCT NEEDED`.
