<!-- English translation of `../../research/MENTAURY_CONTEXTUAL_COGNITION_AND_EPISTEMIC_CONTEXT_NOTES.md`; source preserved; no independent authority or historical update. -->

# 🧭 Mentaury Contextual Cognition & Epistemic Context — Architecture Decision Record

```text
Status:                       ARCHITECTURE_DECISION_RECORD · INTEGRATION_HISTORY
                              NON_AUTHORITATIVE_INDEX · NON_CANONICAL · DOCS_ONLY
Version:                      0.5
Date:                         2026-08-07
Runtime authority:            NONE
Truth authority:              NONE
Capability authority:         NONE
Identity authority:           NONE
Canon modification authority: NONE
Direct write to M3:           FORBIDDEN
Domain runtime:               NOT AUTHORIZED
Roadmap priority:             P1-001 UNCHANGED
```

> **2026-08-07 (after independent review):** This document **no longer** contains normative schemas, full scenario/metamorphic definitions, or a pipeline as a source of truth. It records the **decision** (what was proposed, what was accepted, where it was assigned, and what the review found) and the **history** of integration. Each contract has exactly one normative definition—in its owning document. This file is a decision record, not a specification.

```text
Decision Record ≠ normative specification
```

---

## 1. 🎯 Initial problem

Three research gaps were discovered while discussing how Mentaury should communicate and reason in different contexts:

1. **No model for adapting the presentation** to a specific interlocutor
   (beginner / expert / child) while preserving the same epistemic result.
2. **No composable selection of methods and verification depth** for the type
   of task (code / science / casual conversation), without creating multiple
   inconsistent personas.
3. **No model of institutional context** (funding, conflicts of interest,
   replication, evidence scarcity, suppression claims) for an honest but
   non-conspiratorial assessment of scientific claims.

---

## 2. 🚫 Why three new engines were not created

Direct implementation of three runtime engines (Audience Model, Cognitive Router, Institutional Epistemic Context Engine) was rejected:

```text
No research-gap
≠ grounds for a new runtime engine

Docs-only extension of existing owning documents
> three parallel authority centers
```

Reasons:

- **Audience/Character authority already exists** (Character & Presence
  Spec, `PRESENTATION_ONLY`)—a new Audience Model engine would have created
  a competing presentation authority;
- **Governed Synthesis, Curiosity Policy, and Question Classes already
  exist** (Identity Continuity Notes)—a Cognitive Router would have created
  a second synthesis-like authority;
- **Research Source Admission Gate already exists** (Identity Continuity
  §15)—a separate Institutional Epistemic Context Engine would have created
  a second Evidence/Admission Gate;
- none of the three models requires a new semantic event type or a P0
  runtime extension—all three are docs-only presentation/method-selection/
  evidence-context contracts.

---

## 3. 🔀 Alternatives considered

| Alternative | Why rejected |
|---|---|
| Hard-coded `CODE_MODE` / `SCIENCE_MODE` / `CASUAL_MODE` personas | Would create multiple inconsistent identity-like modes instead of one composable profile |
| A single new `Contextual Cognition Engine` for all three models | A second authority center competing with Character/Governed Synthesis/Source Admission |
| Three separate new top-level spec files | Duplication of existing Character/Identity/Genesis authority boundaries instead of extending them |
| Leave all three models only in this integration note as a “shadow spec” | Creates two sources of truth (integration note + actual use)—rejected by independent review as BLOCKER 2 |

**Accepted:** extend the three existing owning documents while retaining this
file only as a decision record.

---

## 4. 📦 Accepted ownership distribution

| Contract | Owning document |
|---|---|
| Contextual Communication Adaptation | `docs/MENTAURY_CHARACTER_AND_PRESENCE_SPEC_V0.1.md` |
| Cognitive Requirement Profile | `docs/research/MENTAURY_IDENTITY_CONTINUITY_AND_RELATIONAL_ARCHITECTURE_NOTES.md` |
| Institutional Epistemic Context | `docs/research/GENESIS_HERITAGE_INTERPRETATION_AND_HUMAN_ATLAS_NOTES.md` |

A deviation from the originally proposed map was found during distribution:
`research_source_record` (source-level admission,
`independence_class`) physically belongs to **Identity Continuity §15**,
not Genesis Heritage. Institutional Epistemic Context is placed in Genesis
Heritage according to plan (claim-level analysis of funding/conflicts/
replication), but with an explicit cross-reference to Identity Continuity §15
so as not to create a second Admission/Evidence Gate under a similar name.

---

## 5. 🏛️ Authority matrix (high level)

| Area | May determine | May not determine |
|---|---|---|
| Task classification | task requirements | truth status |
| Cognitive Requirement Profile | methods, verification depth, budgets, tool planning | permission, identity, M3 |
| Capability Lease Check | authorized/denied status of a specific tool | truth, identity, values |
| Evidence assessment | support, contradiction, uncertainty | presentation style |
| Institutional Epistemic Context | provenance, incentives, dependency, replication gaps | automatic truth inversion |
| Governed Synthesis | bounded conclusion and unresolved tensions | capability grant |
| Contextual Communication Adaptation | vocabulary, structure, pace, examples | claims, confidence, evidence weight |
| Character | final presentation | reasoning result |

Full definitions are in the owning documents (§9).

---

## 6. 🔍 Independent review decisions (2026-08-07)

The first round of independent review returned **CHANGES_REQUIRED**. The
identified defects and their corrections:

| # | Finding | Correction | Where |
|---|---|---|---|
| BLOCKER 1 | Pipeline allowed retrieval/tool execution before capability check (`Tool availability ≠ authorization to use tool` was violated) | Planning / authorization / execution were separated: `Retrieval / Tool Plan → Capability Lease Check → Scope Check → Privacy/Consent Check → Authorized Retrieval / Tool Execution` | Identity Continuity §20.3 |
| BLOCKER 1 | `tools` schema did not distinguish a requested reference from confirmed authorization | Added `authorization_status`, `authorized_tools`, `denied_tools`; `requested_capability_refs` explicitly marked as not authorization | Identity Continuity §20.5 |
| BLOCKER 2 | Integration note duplicated full schemas/pipeline/scenarios/tests alongside the owning documents (two sources of truth) | This file was shortened to a decision record; full definitions were removed, leaving only links to sections | This file |
| BLOCKER 3 | The same scenario/metamorphic ID was defined twice (integration note + owning document) | Each ID has exactly one normative definition in its owning document; here there are only reference ranges | This file, §9 |
| §7 | Inserting Institutional Epistemic Context shifted 7 sections of Genesis Heritage | Moved to the end as `Appendix A` / §21; numbering §1–§20 restored unchanged | Genesis Heritage §21 |
| §8 | The wording “transferred ... after architectural review” implied APPROVE, which had not occurred | Replaced with “preliminarily distributed ... awaiting independent review” in all three owning documents | Character Spec, Identity Continuity, Genesis Heritage |
| §6 | Contextual Cognition was visually shown as a second roadmap milestone alongside P1-001 | README/Quick Reference separate the execution roadmap (P1-001) from research side-tracks | README.md, Quick Reference |

```text
Distribution drafted ≠ distribution adopted
Independent review round 1 ≠ independent review PASS
PR remains DRAFT until owner/independent-reviewer acceptance
```

---

## 7. 📊 Integration Status Table

| Contract | Owning document (exact section) | Draft status | Independent review | Runtime |
|---|---|---|---|---|
| Contextual Communication Adaptation | [`MENTAURY_CHARACTER_AND_PRESENCE_SPEC_V0.1.md`](../MENTAURY_CHARACTER_AND_PRESENCE_SPEC_V0.1.md) §6.4, §10 (CCA-SC-001…007), §11 (MT-CCA-001…002) | ADOPTED · DOCS_ONLY | REVIEWED · OWNER ACCEPTED · MERGED | NOT AUTHORIZED |
| Cognitive Requirement Profile | [`MENTAURY_IDENTITY_CONTINUITY_AND_RELATIONAL_ARCHITECTURE_NOTES.md`](MENTAURY_IDENTITY_CONTINUITY_AND_RELATIONAL_ARCHITECTURE_NOTES.md) §20, §16.9 (CRP-SC-001…008) | ADOPTED · DOCS_ONLY | REVIEWED · OWNER ACCEPTED · MERGED | NOT AUTHORIZED |
| Institutional Epistemic Context | [`GENESIS_HERITAGE_INTERPRETATION_AND_HUMAN_ATLAS_NOTES.md`](GENESIS_HERITAGE_INTERPRETATION_AND_HUMAN_ATLAS_NOTES.md) §21 Appendix A (IEC-SC-001…009, MT-IEC-001…003) | ADOPTED · DOCS_ONLY | REVIEWED · OWNER ACCEPTED · MERGED | NOT AUTHORIZED |

Independent review round 2 was completed without architectural blockers.
The Owner accepted the changes in merge PR #36; the three contracts have
status `ADOPTED · DOCS_ONLY · NOT IMPLEMENTED`. This does not authorize
runtime.

---

## 8. 🧪 Scenario / metamorphic ID index (references, not definitions)

Each ID is defined **exactly once**, in its owning document. Here there are
only ranges for navigation.

```text
CCA-SC-001…007  → Character Spec §10
MT-CCA-001…002  → Character Spec §11
CRP-SC-001…008  → Identity Continuity §16.9 (index) / §20.9 (full metamorphic tests)
MT-CRP-001…003  → Identity Continuity §20.9
IEC-SC-001…009  → Genesis Heritage §21 (Appendix A.6)
MT-IEC-001…003  → Genesis Heritage §21 (Appendix A.7)
```

---

## 9. 🔗 References to authoritative sections

- [Contextual Communication Adaptation — Character Spec §6.4](../MENTAURY_CHARACTER_AND_PRESENCE_SPEC_V0.1.md)
- [Cognitive Requirement Profile — Identity Continuity §20](MENTAURY_IDENTITY_CONTINUITY_AND_RELATIONAL_ARCHITECTURE_NOTES.md)
- [Institutional Epistemic Context — Genesis Heritage §21 Appendix A](GENESIS_HERITAGE_INTERPRETATION_AND_HUMAN_ATLAS_NOTES.md)
- [Post-P0 Roadmap v0.1](../../research/POST_P0_ROADMAP_V0.1.md)
- [Current Status](../../CURRENT_STATUS.md)

---

## 10. 📜 PR / commit / review history

```text
PR:              #36 — docs: define contextual cognition research contracts
Branch:          agent/contextual-cognition-notes
Base:            main

736f49b  docs: add contextual cognition research notes
338ef67  docs: refine contextual cognition contract
42adcfe  docs(identity-continuity): integrate Cognitive Requirement Profile
c772d79  docs(genesis-heritage): integrate Institutional Epistemic Context
2c20574  docs(character): integrate Contextual Communication Adaptation
5961b3d  docs(contextual-cognition): add integration status table
9411663  docs(nav): link contextual cognition research from Quick Reference/README
```

```text
Review round 1: CHANGES_REQUIRED (pipeline ordering, decision-record
                 conversion, ID duplication, Genesis renumbering,
                 "after review" wording, README milestone separation)
Fixes applied:  see §6 above
Review round 2: PASS · review 4882842702 · exact head 2c38fd78da8d
Owner acceptance: merge PR #36
Merge commit:    850cfe439c3bedd6a2bd4e806e9912283ed5be32
Main CI:         31179202276 · success · 277 passed
```

PR #36 was **merged** into `main`; merge commit
`850cfe439c3bedd6a2bd4e806e9912283ed5be32`.

---

## 11. 🚫 Non-claims / Deferred runtime work

```text
❌ Audience Model runtime
❌ psychological profiling of a person
❌ separate personalities for code / science / conversation
❌ Character Engine or Governed Synthesis Engine
❌ Cognitive Router runtime
❌ Institutional Epistemic Context Engine
❌ Capability Lease Resolver implementation
❌ automatic change of evidence weight based on sponsor identity
❌ automatic distrust of scientific consensus
❌ direct write path to M2 or M3
❌ Tool execution / Action Gate
❌ changes in src/mentaury/
❌ change to Canon
❌ change to P1-001 priority
❌ Contextual Cognition as a new roadmap milestone
```

The following are required before a runtime prototype (not completed by this
document):

```text
reviewed docs → explicit owner GO → separate RFC
→ threat model and privacy analysis → bounded budgets
→ replayable decision receipts → adversarial corpus
→ multilingual / paraphrase tests → false-positive / false-negative report
→ rollback path
```

```text
Docs completeness ≠ runtime safety
Runtime prototype  ≠ production authorization
```

---

## 12. 📚 Notion sync policy

After successful independent review and merge of PR #36, Notion must be
synchronized from authoritative GitHub `main` after post-merge status sync.

```text
GitHub main → authoritative technical contract
Notion      → explanation, decision history and navigation
```

After the merge, Notion receives only:

- a human-readable summary of the three contracts;
- a link to the merged PR and merged SHA;
- the `DOCS_ONLY · NOT IMPLEMENTED` marker;
- the rationale and rejected alternatives (§3 of this document);
- an explicit note that the P1-001 priority has not changed.

Full YAML schemas are **not copied** into Notion.

---

## 🏁 Outcome

```text
Contextual Communication Adaptation
→ explains differently, does not change truth
→ authoritative definition: Character Spec §6.4

Cognitive Requirement Profile
→ selects methods and depth, does not change identity or authority
→ tool planning ≠ tool authorization ≠ tool execution
→ authoritative definition: Identity Continuity §20

Institutional Epistemic Context
→ exposes incentives, dependencies and evidence gaps
→ does not replace evidence with suspicion
→ authoritative definition: Genesis Heritage §21 Appendix A

This document
→ DECISION RECORD, not a normative specification
→ DOCS_ONLY · NO RUNTIME AUTHORITY · P1-001 PRIORITY UNCHANGED
→ PR #36 MERGED · docs-only contracts adopted · Notion sync authorized after status sync
```
