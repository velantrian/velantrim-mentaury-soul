<!-- Source: ../../research/BIOLOGICAL_CYBERNETIC_AND_COGNITIVE_CANDIDATES_V0.1.md; the source remains authoritative, and this mirror is neither an independent authority nor a historical update. -->
# 🧬⚙️ Biological, Cybernetic and Cognitive candidates — notes v0.1

```text
Status:                       CAPTURED · RESEARCH_NOTES · NON_CANONICAL · DOCS_ONLY
Version:                       0.1
Date:                         2026-08-08
Scope:                        Biological / cybernetic / cognitive-science inspiration for
                              future Mentaury research directions
Runtime authority:            NONE
Truth authority:              NONE
Capability authority:         NONE
Canon modification authority: NONE
Selection authority:          NONE — no candidate selected here
P0 scope authority:           NONE
Direct write to M3:            FORBIDDEN
Implementation in src/:       NOT AUTHORIZED
P1-001 priority impact:       NONE
```

> This document records biological, cybernetic, and cognitive-science
> ideas as **research candidates**, not as an architectural decision. It does not
> change Canon, `AuthorityRef`, P1-001 contract, roadmap priority, or runtime
> dependencies and does not authorize any line of code in `src/`.

```text
Metaphor ≠ mechanism
Biological inspiration ≠ implementation
Historical lesson ≠ architectural proof
Scientific plausibility ≠ engineering benefit
Candidate captured ≠ candidate selected
Scientific confidence in biological phenomenon
≠ confidence in software transfer
```

---

## 1. 🎯 Why this note

The owner posed a direct engineering question: can Mentaury be made “smarter”
by taking something from humans, machines, animals, and plants, as well as from
20th-century ideas that were not brought to completion. A catalog of attractive analogies
is insufficient. Every candidate must pass the chain:

```text
biological / historical phenomenon
→ computational principle
→ applicability boundary
→ existing Mentaury module (if any)
→ testable hypothesis
→ minimal experiment (where applicable)
→ measurable software metrics
→ failure criterion
→ governance review
→ explicit owner selection
→ only then implementation planning
```

---

## 2. 🏷️ Candidate classification

Each candidate has **exactly one** primary transfer class:

```text
M — METAPHOR ONLY
P — ENGINEERING PRINCIPLE
A — ALGORITHM CANDIDATE
C — CONTROL PATTERN
W — HISTORICAL WARNING
```

Additionally, **secondary tags** (multiple) are allowed:

```text
experimentable
control-related
quarantine-model
governance-sensitive
historical
metaphorical
high-risk
predictive
```

```text
Primary class = exactly one of {M, P, A, C, W}
Secondary tags ≠ a second primary class
A Class M candidate must not be put directly into code → FORBIDDEN
Class W candidate → never becomes an algorithm candidate
```

### Independent evaluation axes

Complete separately for each card:

```text
Primary transfer class:          M | P | A | C | W
Secondary tags:                  zero or more
Research priority:               HIGH | MEDIUM | LOW
Scientific-transfer confidence:  HIGH | MEDIUM | LOW | DISPUTED | NOT_APPLICABLE
Engineering readiness:           READY_FOR_BOUNDED_EXPERIMENT
                                 | NEEDS_FORMALIZATION
                                 | EARLY_RESEARCH
                                 | METAPHOR_ONLY
                                 | WARNING_ONLY
Governance risk:                 LOW | MEDIUM | HIGH
```

```text
Research priority ≠ scientific-transfer confidence
Scientific confidence in source phenomenon
≠ confidence that the software transfer is valid
HIGH research priority + HIGH governance risk
≠ ready to implement
```

---

## 3. 🃏 Candidate card format

```text
Research ID:
Source phenomenon:
Scientific-transfer confidence:
Primary transfer class:
Secondary tags:
Research priority:
Engineering readiness:
Governance risk:
Existing Mentaury analogue:
Computational transfer hypothesis:
Expected benefit:
Software metrics:
Minimal experiment:
Baseline:
Failure / falsification criterion:
Evidence references:
Non-claims:
Promotion gate:
```

---

## 4. 🔴 HIGH priority candidates

### 4.1. ⚡🧠 Complementary Learning Systems (CLS)

```text
Research ID:                       R-CLS-001
Source phenomenon:                 Complementary Learning Systems —
                                    fast hippocampal-style episodic encoding
                                    + slow neocortical-style semantic
                                    integration with interleaved replay
Primary transfer class:            A — ALGORITHM CANDIDATE
Secondary tags:                    experimentable · governance-sensitive
Research priority:                 HIGH
Scientific-transfer confidence:    MEDIUM
Engineering readiness:             READY_FOR_BOUNDED_EXPERIMENT
Governance risk:                   MEDIUM
Existing Mentaury analogue:        immutable event/payload storage (P0-004)
                                    + deterministic reconstruction substrate (P0-013)
                                    + belief lifecycle / Evidence Gate (P0-014/P0-015)
Computational transfer hypothesis: separate (1) fast, detailed episodic capture
                                    with limited generalization and (2) slower
                                    interleaved semantic integration to reduce
                                    catastrophic interference and preserve
                                    distinctions between similar episodes
Expected benefit:                  more stable belief updates; an explicit
                                    boundary between “what happened” and
                                    “what we think now”
Software metrics:
  Old-belief retention rate =
    percentage of previously valid synthetic beliefs that remain unchanged
    after introduction of overlapping new episodes
  False contradiction rate =
    share of raised contradictions that are later judged unnecessary on the
    same synthetic corpus
  Unrelated-belief regression count =
    number of previously stable beliefs that flip without new directly
    relevant evidence
  Episode collision rate =
    percentage of distinct synthetic episodes incorrectly mapped to the same
    derived representation or conclusion
  Distinct-episode retrieval precision =
    precision of retrieving the intended episode representation among near-
    duplicates
  Revision churn =
    average belief revisions per episode under identical input traces
  Evidence-gate rejection count =
    number of attempted promotions rejected by Evidence Gate
Minimal experiment:                compare (a) direct immediate writes to
                                    belief state and (b) episodic capture →
                                    interleaved consolidation → governed
                                    integration on a synthetic set of
                                    overlapping / contradictory episodes
Baseline:                          current direct belief lifecycle (P0-014)
                                    without a separate episodic buffer
Failure / falsification criterion: if interleaved integration does not improve
                                    Old-belief retention rate and does not reduce
                                    Unrelated-belief regression count relative to
                                    baseline — the hypothesis is rejected
Evidence references:
  - McClelland JL, McNaughton BL, O'Reilly RC. Why there are complementary
    learning systems in the hippocampus and neocortex. Psychol Rev.
    1995;102(3):419-457. doi:10.1037/0033-295X.102.3.419
  - O'Reilly RC, Norman KA. Hippocampal and neocortical contributions to
    memory. Trends Cogn Sci. 2002;6(12):505-510.
    doi:10.1016/S1364-6613(02)02005-3
  - Accessed/checked: 2026-08-08
Non-claims:                        CLS ≠ proof that Mentaury learns
                                    like a brain; the software metrics above ≠ a complete
                                    measurement of biological pattern separation
Promotion gate:                    separate RFC + independent review +
                                    successful completion of the experiment above
```

### 4.2. 😴🔁 Offline and awake experience-consolidation replay

```text
Research ID:                       R-CONSOLIDATION-REPLAY-001
Source phenomenon:                 neural experience replay / memory
                                    reactivation during sleep and quiet
                                    wakefulness, associated with consolidation
Primary transfer class:            A — ALGORITHM CANDIDATE
Secondary tags:                    experimentable · governance-sensitive · high-risk
Research priority:                 HIGH
Scientific-transfer confidence:    MEDIUM
Engineering readiness:             NEEDS_FORMALIZATION
Governance risk:                   HIGH
Existing Mentaury analogue:        No direct implemented analogue.
                                    P0-013 deterministic replay may provide
                                    reproducibility infrastructure for future
                                    experiments, but it is not semantic
                                    consolidation replay.
Computational transfer hypothesis: background reprocessing of accumulated
                                    episodes may run in idle / low-load
                                    windows; its output is only a candidate for
                                    subsequent evidence / contradiction /
                                    authority gates, not a direct write to
                                    belief state
Expected benefit:                  fewer duplicate revisions and better
                                    preparation of semantic-integration
                                    candidates without a literal SleepTimeWorker
Software metrics:
  Duplicate revision reduction
  Contradiction-resolution rate
  Compute cost per processed episode
  Latency before stable candidate
  False semantic promotion count
  Safety counters (must remain zero):
    direct writes to belief state: 0
    direct M3 writes: 0
    Evidence Gate bypasses: 0
Minimal experiment:                compare (a) immediate integration of each
                                    event and (b) deferred batched
                                    consolidation re-evaluation on identical
                                    traces
Baseline:                          immediate per-system processing without
                                    deferred consolidation batching
Failure / falsification criterion: if consolidation replay does not reduce
                                    the number of duplicate revisions or improve
                                    Contradiction-resolution rate with safety
                                    counters = 0 — the hypothesis is rejected
Evidence references:
  - Wilson MA, McNaughton BL. Reactivation of hippocampal ensemble memories
    during sleep. Science. 1994;265(5172):676-679.
    doi:10.1126/science.8036517
  - Ólafsdóttir HF, Bush D, Barry C. The role of hippocampal replay in memory
    and planning. Curr Biol. 2018;28(1):R37-R50.
    doi:10.1016/j.cub.2017.10.073
  - Accessed/checked: 2026-08-08
Non-claims:
  Integrity replay ≠ memory consolidation replay
  Deterministic reconstruction ≠ learning
  Replay output ≠ belief update
  Replay output ≠ truth promotion
  P0-013 R1 replay ≠ this candidate
Promotion gate:                    formal specification of the consolidation
                                    pipeline, separate from P0-013 integrity
                                    replay + independent review
```

### Terminology note — two different “replay” concepts

```text
P0-013 Integrity / deterministic reconstruction replay
  purpose:
    verify reproducibility
    verify deterministic reducer
    verify snapshot-tail equivalence
    confirm integrity

R-CONSOLIDATION-REPLAY-001 Experience / consolidation replay
  purpose:
    re-analyse episodes
    compare similar cases
    surface contradictions
    prepare candidate semantic integration
    never write directly to belief state
```

### 4.3. 🌡️ Homeostasis — reactive resource regulation

```text
Research ID:                       R-HOMEO-001
Source phenomenon:                 homeostasis — reactive feedback regulation
                                    that keeps an observed variable inside an
                                    allowed range
Primary transfer class:            C — CONTROL PATTERN
Secondary tags:                    experimentable · control-related
Research priority:                 HIGH
Scientific-transfer confidence:    MEDIUM
Engineering readiness:             READY_FOR_BOUNDED_EXPERIMENT
Governance risk:                   LOW
Existing Mentaury analogue:        `VerificationBudget` (P0-009) as a possible
                                    actuator/constraint only — not a complete
                                    homeostatic controller
Computational transfer hypothesis: a complete homeostatic loop requires:
                                    sensed variable → target range → measured
                                    error → actuator → remeasurement.
                                    Example: current memory pressure → threshold
                                    exceeded → reduce background-analysis depth
                                    → pressure decreases → measure again
Expected benefit:                  predictable degradation under load instead of
                                    only hard failure
Software metrics:
  Hard-failure rate
  Budget-exhaustion rate
  Tail latency
  Resource oscillation
  Recovery time
Minimal experiment:                increasing load; compare static
                                    budget and explicit reactive control loop
Baseline:                          current static `VerificationBudget`
Failure / falsification criterion: if the loop does not reduce Hard-failure /
                                    Budget-exhaustion rate at comparable
                                    useful work — the hypothesis is rejected
Evidence references:
  - Cannon WB. The Wisdom of the Body. New York: W.W. Norton; 1932.
  - Ashby WR. Design for a Brain. London: Chapman & Hall; 1952.
  - Accessed/checked: 2026-08-08
Non-claims:
  Homeostasis ≠ allostasis
  Static budget ≠ homeostatic controller
  VerificationBudget = possible actuator/constraint only
  Resource regulation ≠ authority regulation
Promotion gate:                    RFC with an explicit sensed variable / range /
                                    actuator / remeasurement cycle
```

### 4.4. 👁️🎯 Active perception / active inference

```text
Research ID:                       R-ACTINF-001
Source phenomenon:                 active inference — perception, planning and
                                    action as interrelated inference oriented
                                    to reducing relevant uncertainty
Primary transfer class:            A — ALGORITHM CANDIDATE
Secondary tags:                    experimentable · governance-sensitive · high-risk
Research priority:                 HIGH
Scientific-transfer confidence:    LOW
Engineering readiness:             NEEDS_FORMALIZATION
Governance risk:                   HIGH
Existing Mentaury analogue:        Evidence Gate (P0-015) already requires
                                    evidence before belief-status change
Computational transfer hypothesis: the system may choose the next
                                    observation/clarification that best reduces
                                    relevant uncertainty, without a single
                                    monolithic objective "minimize surprise";
                                    goals, consent and bounded authority remain
                                    external constraints
Expected benefit:                  more targeted evidence collection
Software metrics:
  Steps-to-stable-resolution
  Irrelevant-observation rate
  Authority/consent constraint violations (must remain 0)
Minimal experiment:                compare passive evidence ordering and
                                    uncertainty-targeted selection of the next
                                    observation
Baseline:                          passive sequential evidence processing
Failure / falsification criterion: if active selection does not reduce
                                    Steps-to-stable-resolution without violating
                                    authority/consent — the hypothesis is rejected
Evidence references:
  - Friston K. The free-energy principle: a unified brain theory?
    Nat Rev Neurosci. 2010;11(2):127-138. doi:10.1038/nrn2787
  - Parr T, Pezzulo G, Friston KJ. Active Inference: The Free Energy Principle
    in Mind, Brain, and Behavior. MIT Press; 2022.
  - Accessed/checked: 2026-08-08
Non-claims:
  active inference ≠ the system's only goal
  ≠ autonomous goal-seeking behavior
  ≠ a replacement for explicit human-authorized scope
  HIGH research priority ≠ ready to implement
Promotion gate:                    RFC with an explicit list of what is NOT
                                    optimized (authority, consent,
                                    external actions) + independent review
```

### 4.5. 🐜📜 Stigmergic event coordination

```text
Research ID:                       R-STIG-001
Source phenomenon:                 stigmergy — coordination through traces left
                                    in a shared environment rather than direct
                                    agent-to-agent commands
Primary transfer class:            P — ENGINEERING PRINCIPLE
Secondary tags:                    experimentable
Research priority:                 HIGH
Scientific-transfer confidence:    MEDIUM
Engineering readiness:             READY_FOR_BOUNDED_EXPERIMENT
Governance risk:                   LOW
Existing Mentaury analogue:        immutable event history (P0-004);
                                    Evidence Gate / evidence records (P0-015)
Computational transfer hypothesis: modules leave verifiable changes in
                                    event history; other processes react to
                                    these traces asynchronously, without direct
                                    commands
Expected benefit:                  less coupling between modules; better
                                    compatibility with replayable substrate
Software metrics:
  Direct module dependency count
  Event consumer coupling
  New-consumer integration effort
  Replay reproducibility
  Duplicate reaction rate
  Event-loop amplification rate
Minimal experiment:                compare direct inter-module calls and
                                    event-trace reactions by coupling and
                                    effort to add a new consumer; separately
                                    measure Event-loop amplification rate
Baseline:                          current more direct integration between
                                    belief lifecycle components
Failure / falsification criterion: if event-trace coordination does not reduce
                                    Direct module dependency count / coupling
                                    or increases Event-loop amplification rate
                                    without compensating benefit — the principle
                                    provides no measurable advantage
Evidence references:
  - Grassé PP. La reconstruction du nid et les coordinations interindividuelles
    chez Bellicositermes natalensis et Cubitermes sp. Insectes Sociaux.
    1959;6:41-80. doi:10.1007/BF02223791
  - Theraulaz G, Bonabeau E. A brief history of stigmergy. Artif Life.
    1999;5(2):97-116. doi:10.1162/106454699568700
  - Accessed/checked: 2026-08-08
Non-claims:
  event history = coordination trace
  event history ≠ command
  event history ≠ authority
  experimentable tag ≠ primary class A
Promotion gate:                    architecture note + independent review;
                                    any algorithm built on the principle — a separate
                                    future A-candidate
```

---

## 5. 🟠 MEDIUM priority candidates

### 5.1. 🌡️📈 Allostasis — predictive / anticipatory resource regulation

```text
Research ID:                       R-ALLO-001
Source phenomenon:                 allostasis — context-sensitive and potentially
                                    predictive adjustment of operating points
                                    and resource allocation before or in
                                    anticipation of demand
Primary transfer class:            C — CONTROL PATTERN
Secondary tags:                    experimentable · control-related · predictive
Research priority:                 MEDIUM
Scientific-transfer confidence:    LOW
Engineering readiness:             NEEDS_FORMALIZATION
Governance risk:                   MEDIUM
Existing Mentaury analogue:        none directly; related to future adaptive
                                    budgeting beyond static VerificationBudget
Computational transfer hypothesis: the system may change its operating point in
                                    advance under predictable load. Example:
                                    forecasted document-analysis load → reserve
                                    memory/compute budget → process workload →
                                    restore ordinary allocation
Expected benefit:                  fewer hard failures during predictable
                                    load peaks
Software metrics:
  Over-allocation cost
  Prediction error
  Hard-failure rate under forecasted load
  Recovery time after peak
Minimal experiment:                compare the reactive-only homeostatic loop
                                    (R-HOMEO-001) with anticipatory allocation on
                                    synthetic load forecasts
Baseline:                          reactive homeostasis candidate / static budget
Failure / falsification criterion: if anticipatory allocation does not reduce
                                    Hard-failure rate enough to justify
                                    Over-allocation cost — the hypothesis is
                                    rejected
Evidence references:
  - Sterling P, Eyer J. Allostasis: a new paradigm to explain arousal pathology.
    In: Fisher S, Reason J, eds. Handbook of Life Stress, Cognition and Health.
    Wiley; 1988:629-649.
  - McEwen BS, Wingfield JC. The concept of allostasis in biology and
    biomedicine. Horm Behav. 2003;43(1):2-15.
    doi:10.1016/S0018-506X(02)00024-7
  - Accessed/checked: 2026-08-08
Non-claims:
  Homeostasis ≠ allostasis
  Adaptive threshold ≠ predictive allostatic model
  Resource regulation ≠ authority regulation
Promotion gate:                    only after formalization of R-HOMEO-001 and
                                    a separate RFC for predictive signals
```

### 5.2. 🦠🛡️ Immune danger/tolerance model

```text
Research ID:                       R-DANGER-001
Source phenomenon:                 danger / damage-associated models of immune
                                    activation and tolerance — influential and
                                    evidence-supported immunological frameworks,
                                    but not the only contemporary explanatory
                                    model
Primary transfer class:            P — ENGINEERING PRINCIPLE
Secondary tags:                    control-related · quarantine-model
Research priority:                 MEDIUM
Scientific-transfer confidence:    MEDIUM
Engineering readiness:             NEEDS_FORMALIZATION
Governance risk:                   MEDIUM
Existing Mentaury analogue:        belief contradiction handling (P0-014);
                                    Evidence Gate rejection paths (P0-015)
Computational transfer hypothesis: replace the simplified known/unknown pair with
                                    independent axes: known/unknown,
                                    safe/potentially-dangerous,
                                    damage/conflict/anomaly,
                                    trusted/tolerated
Expected benefit:                  more precise quarantine logic without excessive
                                    rejection of legitimate new sources
Software metrics:
  False-quarantine rate
  Missed-anomaly rate
  Quarantine-to-delete escalation count (must remain policy-bound, not automatic)
Minimal experiment:                synthetic evidence set with labeled
                                    combinations of known/unknown × safe/damaging
Baseline:                          current evidence processing without explicit
                                    danger taxonomy
Failure / falsification criterion: if the multi-axis model does not simultaneously
                                    improve False-quarantine rate and Missed-anomaly rate —
                                    the hypothesis is rejected
Evidence references:
  - Matzinger P. Tolerance, danger, and the extended family. Annu Rev Immunol.
    1994;12:991-1045. doi:10.1146/annurev.iy.12.040194.005015
  - Matzinger P. The danger model: a renewed sense of self. Science.
    2002;296(5566):301-305. doi:10.1126/science.1071059
  - Pradeu T, Cooper EL. The danger theory: 20 years later. Front Immunol.
    2012;3:287. doi:10.3389/fimmu.2012.00287
  - Accessed/checked: 2026-08-08
Non-claims:
  Danger theory ≠ complete immune model
  Biological immune response ≠ software security policy
  Anomaly ≠ falsehood
  Quarantine ≠ deletion
  Tolerance ≠ trust
  control-related tag ≠ primary class C
Promotion gate:                    explicit axis schema + mapping to
                                    Evidence Gate reason codes + independent review;
                                    a separate future C-candidate may be possible later
```

### 5.3. 🕸️⚖️ Distributed local/global control

```text
Research ID:                       R-DISTCTRL-001
Source phenomenon:                 distributed control — local decisions inside
                                    narrow boundaries with limited global
                                    arbitration
Primary transfer class:            P — ENGINEERING PRINCIPLE
Secondary tags:                    governance-sensitive
Research priority:                 MEDIUM
Scientific-transfer confidence:    MEDIUM
Engineering readiness:             EARLY_RESEARCH
Governance risk:                   LOW
Existing Mentaury analogue:        separation of P0 modules (storage, integrity,
                                    lifecycle, evidence gate)
Computational transfer hypothesis: local modules make decisions only within
                                    their boundary; global arbitration
                                    (authority / governance) remains explicit
Expected benefit:                  fewer hidden implicit global decisions
Software metrics:
  Count of implicit global decisions found inside local modules
  Boundary-violation count in architecture review
Minimal experiment:                architecture review of existing module
                                    boundaries
Baseline:                          current distribution of responsibilities without
                                    a formalized local/global distinction
Failure / falsification criterion: if formalization finds no measurable cases of
                                    implicit global decisions — the principle
                                    remains declarative
Evidence references:
  - Ashby WR. An Introduction to Cybernetics. Chapman & Hall; 1956.
  - Simon HA. The architecture of complexity. Proc Am Philos Soc.
    1962;106(6):467-482.
  - Accessed/checked: 2026-08-08
Non-claims:
  principle ≠ a new runtime slice
  ≠ a distributed multi-node system
Promotion gate:                    architecture-review note + independent review
```

### 5.4. 🍄🛤️ Physarum-inspired resource-aware routing

```text
Research ID:                       R-PHYSARUM-001
Source phenomenon:                 Physarum polycephalum resource-network
                                    adaptation through positive feedback on
                                    successful paths
Primary transfer class:            A — ALGORITHM CANDIDATE
Secondary tags:                    experimentable
Research priority:                 MEDIUM
Scientific-transfer confidence:    LOW
Engineering readiness:             READY_FOR_BOUNDED_EXPERIMENT
Governance risk:                   LOW
Existing Mentaury analogue:        no direct analogue; possible future scheduling
                                    under VerificationBudget pressure
Computational transfer hypothesis: resource-aware routing / ordering of
                                    verification work may outperform naive
                                    policies under load
Expected benefit:                  more efficient use of limited
                                    verification/processing budget
Software metrics:
  Work completed under fixed budget
  Tail latency
  Advantage vs baselines (must be measurable)
Minimal experiment:                compare Physarum-inspired ordering with
                                    shortest-path, priority queue and round-robin
Baseline:                          shortest-path / priority queue / round-robin
Failure / falsification criterion: if there is no measurable advantage over
                                    simple baselines — REJECT
Evidence references:
  - Tero A, Takagi S, Saigusa T, et al. Rules for biologically inspired adaptive
    network design. Science. 2010;327(5964):439-442.
    doi:10.1126/science.1177894
  - Nakagaki T, Yamada H, Tóth Á. Maze-solving by an amoeboid organism.
    Nature. 2000;407:470. doi:10.1038/35035159
  - Accessed/checked: 2026-08-08
Non-claims:
  biological analogy ≠ proven engineering advantage before the experiment
Promotion gate:                    positive experiment vs baselines +
                                    independent review
```

---

## 6. ⚪ METAPHOR ONLY candidates

### 6.1. 🌲🍄 Mycorrhizal networks

```text
Research ID:                       R-MYCO-001
Source phenomenon:                 plant–fungal mycorrhizal symbiosis is well
                                    established; strong “wood-wide web” /
                                    purposeful resource-sharing interpretations
                                    remain disputed and context-dependent
Primary transfer class:            M — METAPHOR ONLY
Secondary tags:                    metaphorical
Research priority:                 LOW
Scientific-transfer confidence:    DISPUTED
Engineering readiness:             METAPHOR_ONLY
Governance risk:                   LOW
Existing Mentaury analogue:        relationship/commitment research notes
Computational transfer hypothesis: NONE at this checkpoint; explanatory metaphor
                                    for context-dependent exchange only
Expected benefit:                  narrative clarity only
Software metrics:                  NOT_APPLICABLE
Minimal experiment:                NOT_APPLICABLE until a precise computational
                                    transfer is proposed
Baseline:                          NOT_APPLICABLE
Failure / falsification criterion: NOT_APPLICABLE at class M
Evidence references:
  - Smith SE, Read DJ. Mycorrhizal Symbiosis. 3rd ed. Academic Press; 2008.
  - Simard SW, et al. Net transfer of carbon between ectomycorrhizal tree
    species in the field. Nature. 1997;388:579-582. doi:10.1038/41557
  - Karst J, Jones MD, Hoeksema JD. Positive citation bias and overinterpreted
    results lead to misinformation on common mycorrhizal networks.
    Nat Ecol Evol. 2023;7:501-511. doi:10.1038/s41559-023-01986-1
  - Accessed/checked: 2026-08-08
Non-claims:
  mycorrhizal symbiosis ≠ established “internet of trees” engineering model
  metaphor / ecological inspiration only
Promotion gate:                    requires exact computational transfer proposal
                                    before any reclassification to P/A
```

### 6.2. 🧬🎭 Epigenetic expression

```text
Research ID:                       R-EPI-001
Source phenomenon:                 epigenetic regulation of gene expression without
                                    changing DNA sequence
Primary transfer class:            M — METAPHOR ONLY
Secondary tags:                    metaphorical
Research priority:                 LOW
Scientific-transfer confidence:    NOT_APPLICABLE
Engineering readiness:             METAPHOR_ONLY
Governance risk:                   LOW
Existing Mentaury analogue:        Character as presentation; Canon v0.1 frozen
                                    constraints; P0-INV-7 Style ≠ Epistemic State
Computational transfer hypothesis: NOT literal “Canon = genome”. Correct framing:
                                    immutable constitutional constraints admit
                                    context-dependent behavioural expression
                                    without altering the constraints themselves
Expected benefit:                  explanatory clarity only
Software metrics:                  NOT_APPLICABLE
Minimal experiment:                NOT_APPLICABLE
Baseline:                          NOT_APPLICABLE
Failure / falsification criterion: NOT_APPLICABLE
Evidence references:
  - Jaenisch R, Bird A. Epigenetic regulation of gene expression: how the genome
    integrates intrinsic and environmental signals. Nat Genet. 2003;33:245-254.
    doi:10.1038/ng1089
  - Accessed/checked: 2026-08-08
Non-claims:
  Canon ≠ biological genome
  Character change ≠ Canon change
  metaphor ≠ engineering proof
Promotion gate:                    not eligible for promotion as-is; narrative use
                                    in docs only
```

---

## 7. ⚠️ Historical warnings (class W)

### 7.1. 📚🚫 GOFAI / Cyc

```text
Research ID:                       R-WARN-GOFAI-001
Source phenomenon:                 large-scale hand-coded common-sense knowledge
                                    projects and broader GOFAI symbolic programs
Primary transfer class:            W — HISTORICAL WARNING
Secondary tags:                    historical
Research priority:                 LOW
Scientific-transfer confidence:    NOT_APPLICABLE
Engineering readiness:             WARNING_ONLY
Governance risk:                   LOW
Lesson:                            manual encoding of “all knowledge” hits
                                    acquisition and maintenance bottlenecks
Mentaury guardrail:                keep one bounded milestone at a time; do not
                                    grow Canon into a total knowledge base
Evidence references:
  - Lenat DB. CYC: a large-scale investment in knowledge infrastructure.
    Commun ACM. 1995;38(11):33-38. doi:10.1145/219717.219745
  - Accessed/checked: 2026-08-08
Non-claims:                        Mentaury Canon ≠ Cyc-like total KB project
```

### 7.2. 🧩🌐 General Problem Solver

```text
Research ID:                       R-WARN-GPS-001
Source phenomenon:                 General Problem Solver and related early claims
                                    of universal problem-solving machinery
Primary transfer class:            W — HISTORICAL WARNING
Secondary tags:                    historical
Research priority:                 LOW
Scientific-transfer confidence:    NOT_APPLICABLE
Engineering readiness:             WARNING_ONLY
Governance risk:                   LOW
Lesson:                            excessive universality without scoped bounds
                                    is hard to validate and maintain
Mentaury guardrail:                P1-001 remains a narrow scoped authority
                                    milestone, not a universal solver
Evidence references:
  - Newell A, Shaw JC, Simon HA. Report on a general problem-solving program.
    IFIP Congress. 1959:256-264.
  - Newell A, Simon HA. Human Problem Solving. Prentice-Hall; 1972.
  - Accessed/checked: 2026-08-08
Non-claims:                        no current or future Mentaury module should aim
                                    to become a universal solver
```

### 7.3. 🏛️🔌 OGAS — institutional misalignment

```text
Research ID:                       R-WARN-OGAS-001
Source phenomenon:                 Soviet OGAS project and the broader difficulty
                                    of aligning technical systems with competing
                                    institutional authorities
Primary transfer class:            W — HISTORICAL WARNING
Secondary tags:                    historical · governance-sensitive
Research priority:                 LOW
Scientific-transfer confidence:    NOT_APPLICABLE
Engineering readiness:             WARNING_ONLY
Governance risk:                   LOW
Lesson:                            a technically ambitious system plus incompatible
                                    centres of power plus unclear authority
                                    boundaries can fail institutionally even when
                                    local technical ideas are strong
Mentaury guardrail:                OGAS is a retrospective analogy illustrating
                                    institutional misalignment and unclear
                                    authority boundaries. It is not the source or
                                    proof of Mentaury independent-review policy.
                                    The case is used only as a historical warning
                                    when evaluating multi-stakeholder authority
                                    structures.
Evidence references:
  - Gerovitch S. InterNyet: why the Soviet Union did not build a nationwide
    computer network. Hist Technol. 2008;24(4):335-350.
    doi:10.1080/07341510802044736
  - Peters B. How Not to Network a Nation: The Uneasy History of the Soviet
    Internet. MIT Press; 2016.
  - Accessed/checked: 2026-08-08
Non-claims:
  OGAS failure ≠ direct proof of a specific GitHub review rule
  historical analogy ≠ origin story of issue #39
```

### 7.4. ❄️📉 AI winters

```text
Research ID:                       R-WARN-AIWINTER-001
Source phenomenon:                 repeated cycles of overclaiming, limited
                                    technical capability, funding disappointment
                                    and changing institutional expectations in
                                    the history of AI
Primary transfer class:            W — HISTORICAL WARNING
Secondary tags:                    historical
Research priority:                 LOW
Scientific-transfer confidence:    NOT_APPLICABLE
Engineering readiness:             WARNING_ONLY
Governance risk:                   LOW
Lesson:                            claims must not outrun empirical evidence
Mentaury guardrail:                retain DOCS_ONLY · NOT IMPLEMENTED markers,
                                    freshness gates and
                                    “OPEN PR ≠ implemented in main”
Evidence references:
  - Crevier D. AI: The Tumultuous History of the Search for Artificial
    Intelligence. Basic Books; 1993.
  - Minsky M, Papert S. Perceptrons. MIT Press; 1969.
  - Accessed/checked: 2026-08-08
Non-claims:
  AI winters ≠ one book or one event
  no research candidate here may be presented as an already working capability
```

---

## 8. 🧾 Related taxonomy — forgetting is not one mechanism

```text
decay          → becomes less accessible
compression    → keeps generalized structure, loses detail
redaction      → payload removed by governed procedure (P0-010); provenance remains
suppression    → temporarily unused, reversible
consolidation  → integration into a more stable semantic structure
"forgetting"   → colloquial umbrella term, NOT one operation
```

Any future work on Memory Metabolism must keep these five operations distinct.

---

## 9. 📊 Priority and class summary

```text
HIGH:
  R-CLS-001                     A
  R-CONSOLIDATION-REPLAY-001    A
  R-HOMEO-001                   C
  R-ACTINF-001                  A
  R-STIG-001                    P

MEDIUM:
  R-ALLO-001                    C
  R-DANGER-001                  P
  R-DISTCTRL-001                P
  R-PHYSARUM-001                A

METAPHOR ONLY:
  R-MYCO-001                    M
  R-EPI-001                     M

HISTORICAL WARNINGS:
  R-WARN-GOFAI-001              W
  R-WARN-GPS-001                W
  R-WARN-OGAS-001               W
  R-WARN-AIWINTER-001           W
```

```text
Candidates captured:        15
Candidates selected:        0
Algorithm candidates (A):   4
Control patterns (C):       2
Engineering principles (P): 3
Metaphor only (M):          2
Historical warnings (W):    4
Runtime wiring:             NOT AUTHORIZED
Execution milestone created: NO
P1-001 priority:            UNCHANGED
```

---

## 10. 📚 Evidence Registry

| Research ID | Evidence level | Transfer confidence | Primary references | Last checked |
|---|---|---|---|---|
| R-CLS-001 | HIGH for source theory | MEDIUM | McClelland et al. 1995; O'Reilly & Norman 2002 | 2026-08-08 |
| R-CONSOLIDATION-REPLAY-001 | HIGH for source phenomenon | MEDIUM | Wilson & McNaughton 1994; Ólafsdóttir et al. 2018 | 2026-08-08 |
| R-HOMEO-001 | HIGH for classical theory | MEDIUM | Cannon 1932; Ashby 1952 | 2026-08-08 |
| R-ALLO-001 | MEDIUM for source theory | LOW | Sterling & Eyer 1988; McEwen & Wingfield 2003 | 2026-08-08 |
| R-ACTINF-001 | HIGH for source literature | LOW | Friston 2010; Parr et al. 2022 | 2026-08-08 |
| R-STIG-001 | HIGH for source phenomenon | MEDIUM | Grassé 1959; Theraulaz & Bonabeau 1999 | 2026-08-08 |
| R-DANGER-001 | MEDIUM–HIGH for source framework | MEDIUM | Matzinger 1994/2002; Pradeu & Cooper 2012 | 2026-08-08 |
| R-DISTCTRL-001 | MEDIUM for general principle | MEDIUM | Ashby 1956; Simon 1962 | 2026-08-08 |
| R-PHYSARUM-001 | HIGH for biological experiments | LOW | Nakagaki et al. 2000; Tero et al. 2010 | 2026-08-08 |
| R-MYCO-001 | DISPUTED for strong network interpretation | NOT_APPLICABLE | Smith & Read 2008; Simard et al. 1997; Karst et al. 2023 | 2026-08-08 |
| R-EPI-001 | HIGH for biology; NOT_APPLICABLE for software transfer | NOT_APPLICABLE | Jaenisch & Bird 2003 | 2026-08-08 |
| R-WARN-GOFAI-001 | HISTORICAL | NOT_APPLICABLE | Lenat 1995 | 2026-08-08 |
| R-WARN-GPS-001 | HISTORICAL | NOT_APPLICABLE | Newell et al. 1959; Newell & Simon 1972 | 2026-08-08 |
| R-WARN-OGAS-001 | HISTORICAL | NOT_APPLICABLE | Gerovitch 2008; Peters 2016 | 2026-08-08 |
| R-WARN-AIWINTER-001 | HISTORICAL | NOT_APPLICABLE | Crevier 1993; Minsky & Papert 1969 | 2026-08-08 |

---

## 11. 🧭 Concrete research program

```text
Candidate (exactly one primary class)
→ bounded experiment (A/C) or architecture note (P)
→ baseline comparison
→ measurable software metrics
→ falsification attempted and survived
→ governance / independent review
→ explicit repository-owner selection
→ only then implementation planning
```

```text
Class M → not eligible without a later exact computational transfer proposal
Class W → never becomes an implementation experiment
```

---

## 12. 🔗 Cross-PR navigation

```text
RESEARCH_INDEX.md
STORAGE_AND_GRAPH_PROFILE_CANDIDATES_V0.1.md
```

Referenced document exists only in an open PR at this checkpoint.
No live relative link is created.

After the corresponding PRs are merged in the future, the links will be added in a separate
docs-sync change.

Existing live references:

- [`MENTAURY_IDENTITY_CONTINUITY_AND_RELATIONAL_ARCHITECTURE_NOTES.md`](MENTAURY_IDENTITY_CONTINUITY_AND_RELATIONAL_ARCHITECTURE_NOTES.md)
- [`../MENTAURY_P0_IMPLEMENTATION_PLAN.md`](../MENTAURY_P0_IMPLEMENTATION_PLAN.md)

---

## 13. 🚫 Explicit prohibitions

```text
❌ src/ changes
❌ .github/workflows changes
❌ Canon / AuthorityRef / P1-001 contract / roadmap priority changes
❌ runtime dependencies
❌ Action Gate / M3 / Identity / Relationship runtime
❌ Native Kernel / Titan / Crystal integration
❌ mixing with PR #38 or PR #45
❌ class M promoted to algorithm
❌ class W assigned implementation experiment
```

---

## 14. ✅ Manual consistency checklist

```text
unique Research IDs: PASS
candidate count matches summary (15): PASS
exactly one primary class per candidate: PASS
no P/A or P/C dual primary classes: PASS
no broken relative links to absent main files: PASS
scientific-confidence claims have Evidence references: PASS
no class M promoted to algorithm: PASS
no class W assigned implementation experiment: PASS
Integrity replay separated from consolidation replay: PASS
Homeostasis separated from allostasis: PASS
```
