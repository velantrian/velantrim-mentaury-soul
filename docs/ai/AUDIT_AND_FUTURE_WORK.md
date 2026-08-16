# 🌀 Mentaury Soul — Audit & Future Work Ledger

**Repository:** `velantrian/velantrim-mentaury-soul`  
**Default branch:** `main`  
**Role:** documentation / audit / governance only  
**Last live reconciliation:** 2026-08-17  
**Audited checkpoint:** `main@11ca20974fc99e21666361a31cfe55614c002891`  
**Current engineering truth owner:** `docs/CURRENT_STATUS.md` + live GitHub code/tests/exact CI  
**Governance owner:** `docs/GOVERNANCE.md` + live GitHub governance  
**Derived machine view:** `docs/state/project_state.json`  
**Notion mirror:** `🌀 Mentaury – Soul 🧊`

> **DO NOT AUTO-SELECT NEXT MILESTONE.**
>
> Future-work entry, priority, open Issue, research direction, audit order, frozen contract, implemented bounded primitive, or positive research result **does not authorize implementation or runtime**.

Before future implementation:

```text
resolve live main / signature
→ resolve PRs / Issues / exact CI
→ read CURRENT_STATUS + GOVERNANCE + owning contract
→ reconcile this ledger
→ verify current authorization / Owner GO
→ select ONE bounded scope only if evidence justifies it
→ only then implementation
```

If no bounded scope is proven appropriate: **STOP WITH AUDIT REPORT.**

---

## 1. Fresh live checkpoint

At the audited checkpoint:

```text
P0-001…P0-015                         IMPLEMENTED
P1-001 Capability Lease               IMPLEMENTED_BOUNDED
P1-002 Privacy Classifier             IMPLEMENTED_BOUNDED
P1-003 Constraint Composer            IMPLEMENTED_BOUNDED
NPG-v0.1                              IMPLEMENTED_BOUNDED
NPG-COMP-v0.1 shadow composition      IMPLEMENTED_BOUNDED
PCR-v0.1                              IMPLEMENTED_BOUNDED
EPR-v0.1                              CONTRACT FROZEN / NOT IMPLEMENTED
EPR Owner GO                          NOT GRANTED
ATR-v0.1                              IMPLEMENTED_BOUNDED
HDE-v0.1                              IMPLEMENTED_BOUNDED
Phase 6 runtime                       NOT AUTHORIZED
P1-004                                NOT ASSIGNED
Action Gate                           NOT AUTHORIZED
retrieval / tools                     NOT AUTHORIZED
identity / relationship runtime       NOT AUTHORIZED
runtime deployment                    NOT AUTHORIZED
independent human review              NOT CLAIMED
open PRs                              0
```

Live research/audit trackers include:

- Issue #129 — post-HDE cognitive gap discrimination before any runtime milestone;
- Issue #133 — targeted reliability hardening for existing bounded primitives;
- Issue #39 — restore independent-review gate before public/team stage.

Issue #129 explicitly does **not** make EPR the next milestone. It requires discrimination among EPR, claim→belief provenance-preserving binding, terminal reconsideration/successor lineage, or `NO_IMPLEMENTATION / MORE_RESEARCH`.

### Permanent non-equivalences

```text
claim != belief
hypothesis != fact
proposed observation != evidence
discrimination != verdict
relation != truth
character specification != identity mutation
identity continuity research != runtime identity authority
contract freeze != implementation authority
implemented bounded != runtime authority
runtime capability != action authority
```

### Global revalidation triggers

Re-audit relevant items when newer `main` changes their source/contract owner; an Issue/PR changes lifecycle; an Owner GO is granted/consumed; a runtime authorization changes; Canon/governance changes; a research contract is superseded; or new evidence demonstrates a previously unproven cognitive failure.

---

# 2. Durable audit queue

## MS-FW-001 — Non-Projection contract, composition and remaining gap

**State:** `DONE_BOUNDED + INVESTIGATE_REMAINING_GAP`  
**Priority:** P1 audit  
**Suggested audit sequence:** 1  
**Implementation authorized:** NO  
**Runtime capability change:** NO  
**Authority impact:** NONE  
**Known Issue / PR:** historical NPG #90 / composition #96; re-resolve descendants live  
**Last verified:** 2026-08-17  
**Evidence anchor:** `docs/CURRENT_STATUS.md`; `main@11ca2097...`  
**Revalidation trigger:** NPG contract/composition/runtime/identity/projection changes.

**Question:** What, if anything, remains missing after bounded NPG classifier + same-attempt shadow composition?  
**Why it matters:** implemented classification/composition must not be mislabeled as identity runtime or universal projection prevention.  
**Current evidence:** NPG-v0.1 and NPG-COMP-v0.1 are implemented bounded; NPG runtime remains unauthorized.  
**Alternative explanations:** no new mechanism may be required; remaining gaps may belong to identity provenance, presentation, or later integration rather than NPG itself.  
**Files/components:** non-projection contracts/source/tests, shadow composition, Canon/current status, identity boundaries.  
**Required audit:** map contract → implementation → caller → runtime → authority separately.  
**Experiment/reproduction:** only for a demonstrated projection failure not already covered.  
**Preconditions:** fresh contract/current-state read.  
**Non-goals:** no identity mutation/runtime activation.  
**Authority boundaries:** PASS/PASS_ATTRIBUTED does not confer SELF or action authority.  
**Falsification/closure:** close new-mechanism hypothesis if existing bounded owners already prevent the demonstrated failure.  
**Exit criteria:** evidence-bound remaining-gap or `NO_CHANGE`.  
**Possible outcomes:** `DONE`, `INVESTIGATE`, `CANDIDATE`, `DEFERRED`.

---

## MS-FW-002 — Phase 4 EPR-v0.1 necessity and ordering

**State:** `CANDIDATE / NOT_AUTHORIZED`  
**Priority:** P1 audit  
**Suggested audit sequence:** 2  
**Implementation authorized:** NO  
**Runtime capability change:** NO  
**Authority impact:** NONE  
**Known Issue / PR:** Issue #129  
**Last verified:** 2026-08-17  
**Evidence anchor:** EPR frozen contract + `CURRENT_STATUS` + Issue #129  
**Revalidation trigger:** Issue #129 decision; Owner GO; EPR contract replacement; claim/belief owner change.

**Question:** Is bounded EPR implementation actually the smallest missing executable primitive after PCR + ATR + HDE?  
**Why it matters:** an already-frozen contract is not automatically next.  
**Current evidence:** contract frozen; source implementation absent; Owner GO absent; Issue #129 keeps alternatives open.  
**Alternative explanations:** claim→belief provenance binding, terminal reconsideration lineage, or no implementation may be the real answer.  
**Files/components:** EPR contract, PCR/ATR/HDE, P0-014 belief lifecycle, P0-015 Evidence Gate.  
**Required audit:** prove exact missing input/output and why an existing owner cannot own it.  
**Experiment/reproduction:** executable failure discrimination before implementation selection.  
**Preconditions:** Issue #129 fresh reconciliation.  
**Non-goals:** no belief mutation or Evidence Gate duplication.  
**Authority boundaries:** EPR route != belief mutation.  
**Falsification/closure:** if no unique executable failure requires EPR, choose `NO_IMPLEMENTATION` or `MORE_RESEARCH`.  
**Exit criteria:** one justified outcome, not default EPR.  
**Possible outcomes:** `NO_IMPLEMENTATION`, `MORE_RESEARCH`, `SELECTED_NEXT_BOUNDED_READINESS` under later authority.

---

## MS-FW-003 — P1-004 assignment

**State:** `NOT_ASSIGNED / DEFERRED`  
**Priority:** P2  
**Suggested audit sequence:** 3  
**Implementation authorized:** NO  
**Runtime capability change:** NO  
**Authority impact:** NONE  
**Known Issue / PR:** none establishing assignment at audited checkpoint  
**Last verified:** 2026-08-17  
**Evidence anchor:** `docs/CURRENT_STATUS.md` (`P1_004_NOT_ASSIGNED`)  
**Revalidation trigger:** explicit candidate selection/assignment/Owner decision.

**Question:** Does any proven gap warrant assigning P1-004?  
**Why it matters:** numbering/roadmap pressure must not manufacture a capability.  
**Current evidence:** not assigned.  
**Alternative explanations:** later work may remain phase-specific research rather than P1-004.  
**Required audit:** identify concrete failure + owner gap before assignment.  
**Non-goals:** no placeholder engine.  
**Authority boundaries:** desired behavior != implementation primitive.  
**Closure:** remain unassigned until explicit evidence-backed decision.

---

## MS-FW-004 — Post-HDE / Inference Bridge cognitive gap discrimination

**State:** `INVESTIGATE`  
**Priority:** P1  
**Suggested audit sequence:** 4  
**Implementation authorized:** NO  
**Runtime capability change:** NO  
**Authority impact:** NONE  
**Known Issue / PR:** Issue #129  
**Last verified:** 2026-08-17  
**Evidence anchor:** HDE-v0.1 bounded implementation + Issue #129  
**Revalidation trigger:** HDE contract/result changes; Issue #129 decision; new bounded primitive selection.

**Question:** After HDE, what first executable cognitive failure remains that existing owners cannot represent or constrain?  
**Current evidence:** HDE discriminates caller-supplied structural hypothesis partitions; it does not generate hypotheses, execute observations, collect evidence, assign verdicts, schedule inquiry, or mutate beliefs.  
**Alternative explanations:** no new mechanism; EPR; provenance-preserving claim→belief binding; terminal reconsideration lineage.  
**Required audit:** full chain PCR → ATR → HDE → Evidence Gate → belief lifecycle → EPR.  
**Experiment:** only a falsifiable bounded discriminator for the selected gap.  
**Non-goals:** autonomous inquiry/scheduler/retrieval/tools.  
**Authority boundaries:** HDE result != evidence verdict.  
**Exit criteria:** `NO_IMPLEMENTATION`, `MORE_RESEARCH`, or separately selected bounded readiness.

---

## MS-FW-005 — Identity continuity, provenance and governed change

**State:** `INVESTIGATE`  
**Priority:** P2  
**Suggested audit sequence:** 5  
**Implementation authorized:** NO  
**Runtime capability change:** NO  
**Authority impact:** NONE  
**Last verified:** 2026-08-17  
**Evidence anchor:** Canon/current status/identity research surfaces at audited main  
**Revalidation trigger:** identity contract/source/runtime, provenance, revision/rollback or self/non-self semantics change.

**Question:** Which identity-continuity semantics are specification/research versus executable today?  
**Why it matters:** continuity must not silently become identity proof or authority to mutate SELF.  
**Required audit:** provenance, change, drift, revision, rollback, explanation, lineage, self/non-self and Non-Projection interactions.  
**Alternative explanations:** existing provenance + belief/claim separation may cover more than a dedicated identity engine would.  
**Experiment:** only after a concrete identity-continuity failure is defined.  
**Non-goals:** no identity runtime activation or autonomous self-change.  
**Authority boundaries:** continuity != identity proof; imported material != SELF.  
**Exit criteria:** capability/evidence matrix with explicit non-runtime gaps.

---

## MS-FW-006 — Character & Presence boundary

**State:** `DEFERRED / RESEARCH`  
**Priority:** P3  
**Suggested audit sequence:** 6  
**Implementation authorized:** NO  
**Runtime capability change:** NO  
**Authority impact:** NONE  
**Evidence anchor:** `docs/MENTAURY_CHARACTER_AND_PRESENCE_SPEC_V0.1.md`; current status  
**Revalidation trigger:** character spec or runtime activation gate changes.

**Question:** What presentation behavior can be specified without mutating identity or claiming evidence?  
**Required audit:** distinguish presentation/voice from SELF mutation and runtime activation.  
**Non-goals:** no character runtime activation under this ledger.  
**Authority boundaries:** character != evidence; character spec != identity mutation.  
**Exit criteria:** preserve clear spec/runtime/identity separation.

---

## MS-FW-007 — Curiosity / inquiry research

**State:** `CANDIDATE / DEFERRED / NOT_AUTHORIZED`  
**Priority:** P3  
**Suggested audit sequence:** 7  
**Implementation authorized:** NO  
**Runtime capability change:** NO  
**Authority impact:** NONE  
**Last verified:** 2026-08-17  
**Evidence anchor:** current HDE boundary + Issue #129 out-of-scope autonomy rules  
**Revalidation trigger:** explicit bounded inquiry research decision or demonstrated gap.

**Question:** Is a new curiosity/inquiry primitive necessary at all?  
**Required audit:** identify bounded question-generation/inquiry failure separately from scheduler/tool execution.  
**Alternative explanations:** caller-provided research prompts + existing HDE may suffice.  
**Non-goals:** no `CuriosityEngine`, scheduler, autonomous inquiry, retrieval/tools by aspiration.  
**Authority boundaries:** desired curiosity behavior != runtime authorization.  
**Exit criteria:** evidence-backed candidate or `DEFERRED_NO_NEED`.

---

## MS-FW-008 — Sleep-time cognition / offline cognitive cycle

**State:** `CANDIDATE / DEFERRED / NOT_AUTHORIZED`  
**Priority:** P3  
**Suggested audit sequence:** 8  
**Implementation authorized:** NO  
**Runtime capability change:** NO  
**Authority impact:** NONE  
**Revalidation trigger:** explicit research selection, scheduler/runtime authority change, identity mutation contract change.

**Question:** Can an offline/night cycle be defined safely and usefully without unauthorized mutation or autonomy?  
**Required audit:** scheduling, resource bounds, identity effects, provenance, rollback, explainability, authorization.  
**Experiment:** simulation/research only if later authorized.  
**Non-goals:** no autonomous scheduler/background mutation.  
**Authority boundaries:** offline processing != permission to alter beliefs/identity.  
**Exit criteria:** bounded research design or defer.

---

## MS-FW-009 — Cognitive method provenance and selection

**State:** `INVESTIGATE`  
**Priority:** P3  
**Suggested audit sequence:** 9  
**Implementation authorized:** NO  
**Runtime capability change:** NO  
**Authority impact:** NONE  
**Revalidation trigger:** method-extraction/selection contract or evidence changes.

**Question:** How should cognitive methods be represented, attributed and selected without assuming a separate engine?  
**Required audit:** source provenance, method abstraction, selection criteria, conflicting methods, explainability, relation to HDE/evidence owners.  
**Alternative explanations:** methods may remain prompt/research guidance rather than durable runtime objects.  
**Non-goals:** no autonomous method mutator.  
**Authority boundaries:** method preference != evidence/identity authority.  
**Exit criteria:** proven need + owner, or research-only classification.

---

## MS-FW-010 — Human Paths / Genesis Heritage provenance boundary

**State:** `INVESTIGATE / RESEARCH`  
**Priority:** P2  
**Suggested audit sequence:** 10  
**Implementation authorized:** NO  
**Runtime capability change:** NO  
**Authority impact:** NONE  
**Revalidation trigger:** heritage/source ingestion, identity attribution, privacy/copyright policy changes.

**Question:** How can human experience/literature/philosophy influence the system without becoming false autobiography or unlicensed identity inheritance?  
**Required audit:** provenance, attribution, privacy/consent, copyright, influence vs identity, Non-Projection, revision/removal.  
**Experiment:** source-to-influence traceability only under a later bounded research scope.  
**Non-goals:** no automatic SELF adoption.  
**Authority boundaries:** heritage/influence != autobiography/identity.  
**Exit criteria:** explicit provenance/influence contract or defer.

---

## MS-FW-011 — Reliability hardening of existing bounded primitives

**State:** `INVESTIGATE / NEEDS_REPRODUCTION`  
**Priority:** P2  
**Suggested audit sequence:** 11  
**Implementation authorized:** NO by this ledger  
**Runtime capability change:** NO  
**Authority impact:** NONE  
**Known Issue / PR:** Issue #133  
**Last verified:** 2026-08-17  
**Evidence anchor:** live Issue #133  
**Revalidation trigger:** Issue #133 lifecycle; reproduced invariant failure; changed bounded primitive.

**Question:** Which high-consequence error paths merit additional tests without changing semantics?  
**Current evidence:** #133 records candidates, not confirmed defects, and explicitly rejects coverage-chasing.  
**Required method:** suspicion → reproduce/identify existing invariant → test only consequential path → preserve fail-closed semantics.  
**Non-goals:** no runtime expansion, diagnostic vocabulary expansion without contract decision, or broad coverage target.  
**Authority boundaries:** observability improvements must not weaken DEFER/authority results.  
**Exit criteria:** targeted bounded tests under separate scope or documented `NO_CHANGE`.

---

# 3. Suggested future audit order — not implementation order

```text
1  live state / governance / open work
2  MS-FW-001 Non-Projection residual gap
3  MS-FW-002 + MS-FW-004 post-HDE / EPR discrimination
4  MS-FW-003 P1-004 only if a real gap needs assignment
5  MS-FW-005 identity continuity
6  MS-FW-011 reliability checks on reproduced/high-consequence invariants
7  MS-FW-006 character/presence
8  MS-FW-007 curiosity
9  MS-FW-008 sleep-time cognition
10 MS-FW-009 cognitive methods
11 MS-FW-010 Human Paths / Genesis Heritage
```

This is an **audit/navigation order only**.

---

# 4. Safe continuation protocol

A future AI must preserve:

```text
Evidence Gate ownership
Non-Projection boundaries
claim / belief / relation separation
provenance and history
single-use Owner GO semantics
no silent runtime promotion
no identity/action authority inheritance
```

It must not infer a next milestone from Issue #129, the frozen EPR contract, HDE completion, P1 numbering, desired character/curiosity behavior, or cross-project ideas.

For a suspected defect:

```text
suspicion
→ reproduction
→ prove violated invariant
→ localize causal owner
→ bound affected scope
→ only then consider repair under separate authorization
```

No other Velantrim repository grants Mentaury Soul implementation authority by similarity.
