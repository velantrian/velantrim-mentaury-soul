# 🔬 Phase 6 — Hypothesis Discrimination Implementation Readiness

```text
Status:                         SELECTED_CANDIDATE · DOCS_TESTS_ONLY · NON_RUNTIME
Date:                           2026-08-15
Baseline main:                  d5d5d8f5e48298910e00fe9d075e6dc411c6dd6b
Baseline signature:             VERIFIED · VALID
Operating mode:                 SOLO_MAINTAINER
Independent human review:       NO
Phase 5 ATR-v0.1:               IMPLEMENTED_BOUNDED
Phase 6 benchmark:              HD-01…HD-10 · PREPARED_DOCS_TESTS_ONLY
Phase 6 Owner GO implementation:NOT_GRANTED
Phase 6 source implementation:  NOT_STARTED
Phase 6 runtime:                NOT_AUTHORIZED
```

> **NEW FAILURE MODE ≠ AUTOMATIC NEW MODULE.** This readiness cycle selects only the smallest pure boundary that closes an executable structural gap. It grants no source implementation, evidence, belief, retrieval, tool, action, identity, M3, scheduler or runtime authority.

---

## 1. Existing-owner audit

| Required information / behavior | Existing owner | Result |
|---|---|---|
| H1/H2 as attributed hypotheses | `PCR-v0.1` / `EpistemicRole.HYPOTHESIS` | owned |
| inference basis + provenance | `PCR-v0.1` | owned |
| exact claim identity | PCR `claim_id + input_fingerprint` | owned |
| typed relation candidates | `ATR-v0.1` | owned |
| correlation/causation distinction | `ATR-v0.1` | owned |
| relation provenance/scope/unknowns | `ATR-v0.1` | owned |
| ordinary non-terminal belief lifecycle | `P0-014` | owned |
| `SUPPORTED / CONTRADICTED` | `P0-015 Evidence Gate` | exclusive owner |
| future epistemic-change routing | `EPR-v0.1` | frozen contract; implementation absent |
| proposed observation design | none | unowned only as caller-supplied design input |
| qualitative expected outcome under H1 vs H2 | none | **unowned structural input** |
| verify at least one supplied outcome separates H1/H2 | none | **unowned structural evaluation** |

No new `HypothesisRecord`, `InferenceRecord`, `RelationRecord`, `EvidenceVerdict`, belief owner, graph owner or confidence owner is justified.

---

## 2. Failure-mode proof

The existing contracts admit this state without contradiction:

```text
PCR: H1 = thermal internal-contact failure            ✅ valid hypothesis claim
PCR: H2 = power-source thermal protection             ✅ valid hypothesis claim
ATR: H1/H2 may have correctly typed relations         ✅ valid relation representation

proposed observation:
"inspect the device again"

possible outcomes:
R1 = device fails again
R2 = device does not fail this time

H1 interpretation: R1 possible; R2 possible
H2 interpretation: R1 possible; R2 possible
```

PCR validates attribution/role/provenance. ATR validates typed relation representation. Neither contract asks whether any proposed result has **different expected interpretation under H1 and H2**. P0-014/P0-015 act on belief/evidence state and must not be repurposed as test-design validators. EPR routes change requests and cannot own discrimination semantics.

Therefore this failure remains executable today:

```text
WELL_FORMED_H1 + WELL_FORMED_H2 + WELL_FORMED_RELATIONS
→ NON_DISCRIMINATING_OBSERVATION
→ no existing contract violation
```

That is the exact uncovered gap.

---

## 3. Required questions A–G

**A. Missing input:** a caller-supplied finite outcome partition for a proposed observation, with a qualitative expected-state mapping for each outcome under H1 and H2 plus provenance/basis references for that design.

**B. Missing output:** a bounded structural classification answering whether the supplied outcome mapping contains a genuine H1/H2 separator, is non-discriminating, or is structurally inconclusive.

**C. Why PCR cannot own it:** PCR owns claim/provenance/epistemic-role representation. Adding cross-hypothesis outcome comparison would turn claim representation into a decision primitive.

**D. Why ATR cannot own it:** ATR owns pairwise typed relations. `RelationType` is not an outcome-prediction matrix and relation existence/type is not evidence or discrimination authority.

**E. Why this is not Evidence Gate:** no observed evidence verdict is produced. `SUPPORTED` and `CONTRADICTED` remain exclusively P0-015.

**F. Why benchmark alone is insufficient:** the benchmark can detect the failure in tests, but without a callable pure boundary a future caller can still accept a non-discriminating plan while satisfying PCR/ATR schemas. A small evaluator makes that structural failure rejectable without adding runtime authority.

**G. Failure made impossible:** within the supplied outcome partition, a plan in which every represented outcome has identical H1/H2 expectation semantics cannot be classified as `DISCRIMINATING`.

---

## 4. Candidate comparison

| Candidate | Failure coverage | Duplication risk | Authority risk | Decision |
|---|---|---:|---:|---|
| A · `NO_NEW_PRIMITIVE` / benchmark convention only | detects in tests but gives no callable structural guard | none | lowest | rejected: gap remains callable-unconstrained |
| B · `PURE_HYPOTHESIS_DISCRIMINATION_EVALUATOR` | closes core structural HD-02 gap and supports HD-06/07/09/10 boundaries | low | low | **SELECTED** |
| C · `PURE_DISCRIMINATION_PLAN_RECORD` | stores design shape but does not prevent non-discriminating plans | medium: new representation owner | low-medium | rejected |
| D · record + evaluator | closes gap | highest | medium | rejected as unnecessary surface |

Selection principle:

```text
EXISTING PCR CLAIMS
+
EXISTING ATR ANCHORS / RELATIONS
+
CALLER-SUPPLIED TEST-DESIGN INPUT
+
PURE STRUCTURAL DISCRIMINATION EVALUATION
```

not a hypothesis database, test graph, evidence engine or cognition module.

---

## 5. Scope of the selected primitive

Selected candidate:

```text
PURE_HYPOTHESIS_DISCRIMINATION_EVALUATOR
Contract: HDE-v0.1
```

It is only a deterministic structural evaluator over caller-supplied data.

It does **not**:

- generate H1 or H2;
- decide semantic equivalence of natural-language hypotheses;
- search for tests;
- execute a proposed observation;
- retrieve information;
- call a model/tool/API/database/sensor;
- collect evidence;
- call Evidence Gate;
- mutate claims or beliefs;
- emit `SUPPORTED` / `CONTRADICTED`;
- assign probability/confidence/trust/weight;
- infer causality from ATR relations;
- choose an action;
- schedule inquiry;
- write identity/relationship/M3 state;
- start or authorize autonomous cognition.

HD-01 genuinely distinct alternative generation and HD-03 preference among semantically meaningful candidate tests remain **benchmark/caller responsibilities** in v0.1. HDE-v0.1 does not pretend that string inequality proves semantic distinctness.

---

## 6. Threat-model coverage

| Threat | HDE-v0.1 readiness treatment |
|---|---|
| T1 fake alternative | fail closed on exact same PCR identity; semantic paraphrase remains benchmark-level |
| T2 non-discriminating observation | direct evaluator responsibility |
| T3 confirmation-only test | cannot be `DISCRIMINATING` unless a differential expected outcome is supplied |
| T4 missing falsifier | surfaced by structural flags; no winner forced |
| T5 relation laundering | ATR relation is never accepted as evidence verdict |
| T6 causal laundering | no promotion from correlational/analogical to causal/mechanistic |
| T7 Evidence Gate theft | forbidden output vocabulary |
| T8 confidence smuggling | confidence/probability/trust/weight fields forbidden |
| T9 provenance collapse | caller-supplied design and expectation basis references required |
| T10 self-evidence loop | design provenance never counts as evidence for H1/H2 |
| T11 inconclusive suppression | `INCONCLUSIVE_STRUCTURE` is valid |
| T12 history deletion | no mutation/deletion capability exists |
| T13 hidden retrieval | purity/source-surface tests required |
| T14 action escalation | no task/action output exists |
| T15 identity leakage | identity/relationship/M3 imports and writes forbidden |
| T16 graph authority | graph path/count/centrality absent from contract |

---

## 7. Metamorphic requirements

The frozen contract must retain these executable requirements:

```text
HDE-M01 rename non-semantic refs consistently           → same classification
HDE-M02 swap H1/H2 and swap expectation columns         → equivalent classification
HDE-M03 duplicate source/basis reference                → reject duplicate; never improve result
HDE-M04 add unrelated ATR relation                      → classification unchanged
HDE-M05 causal wording changed to correlational input   → no causal implication created
HDE-M06 remove only differential outcome                → becomes NON_DISCRIMINATING/INCONCLUSIVE
HDE-M07 exact same H1/H2 PCR identity                    → invalid input
HDE-M08 all supplied outcomes map identically           → NON_DISCRIMINATING
HDE-M09 confidence/probability metadata attempt          → rejected/not representable
HDE-M10 same exact input                                 → same output + fingerprint
```

---

## 8. Authority boundary

```text
HYPOTHESIS ≠ FACT
PROPOSED OBSERVATION ≠ EVIDENCE
EXPECTED OUTCOME ≠ OBSERVED OUTCOME
DISCRIMINATION ≠ EVIDENCE GATE VERDICT
RELATION ≠ TRUTH
CORRELATION ≠ CAUSATION
MENTAURY_DERIVED_TEST_DESIGN ≠ INDEPENDENT_EVIDENCE
BENCHMARK PASS ≠ RUNTIME AUTHORITY
IMPLEMENTATION CONTRACT ≠ IMPLEMENTATION AUTHORITY
```

`WAIT` / `DEFER` remain benchmark/planning outcomes and are not introduced as global epistemic statuses.

---

## 9. Selection result and mandatory stop

```text
PHASE_6_READINESS = SELECTED_CANDIDATE_CONTRACT_FROZEN_DOCS_TESTS_ONLY
PHASE_6_CANDIDATE = PURE_HYPOTHESIS_DISCRIMINATION_EVALUATOR
PHASE_6_IMPLEMENTATION_CONTRACT = HDE-v0.1 · FROZEN_DOCS_TESTS_ONLY
PHASE_6_IMPLEMENTATION = NOT_STARTED
PHASE_6_OWNER_GO_FOR_IMPLEMENTATION = NOT_GRANTED
PHASE_6_RUNTIME = NOT_AUTHORIZED
```

**STOP.** A later explicit single-use Owner GO is required before creating the reserved `src/mentaury/discrimination/**` source package.