<!-- Source: [Russian original](../../research/ARCHITECTURE_RECONCILIATION_V0.1.md). This English mirror is not independent authority. -->

# 🧭 Mentaury Architecture Reconciliation v0.1

```text
Status:                       DRAFT · RECONCILIATION_MAP · DOCS_ONLY
Date:                         2026-08-04
Canon modification authority: NONE
Runtime authority:            NONE
P0 scope authority:           NONE
Direct write to M3:           FORBIDDEN
```

> This document reconciles the areas of responsibility of existing documents. It does not create a new architecture, change Canon v0.1, expand P0, or turn research hypotheses into runtime.

---

## 1. 🎯 Why a reconciliation map is needed

Following the development of Controlled Origin, Character & Presence, and Identity Continuity, several documents began using overlapping concepts: self-model, synthesis, curiosity, memory, M3, relationships, and external tools.

The purpose of reconciliation:

- exclude competing authority;
- determine which document is responsible for which area;
- separate presentation from reasoning;
- separate identity from Exo-Cortex;
- preserve P0 as the common Event Substrate;
- establish the architectural order before the technical skeleton.

---

## 2. 🏛️ Domain-specific authority

The project does not have one linear list in which any document is completely “above” the next. Authority depends on the area.

| Domain | Main document | Limitation |
|---|---|---|
| Root invariants | `MENTAURY_CANON_V0.1.md` | Canon frozen; research does not change it implicitly |
| P0 Event Substrate | `MENTAURY_P0_IMPLEMENTATION_PLAN.md` | Event infrastructure, integrity, replay, and minimal belief lifecycle only |
| Current maturity | `CURRENT_STATUS.md` | Describes status, but does not create new invariants |
| Origin and human experience | `GENESIS_HERITAGE_INTERPRETATION_AND_HUMAN_ATLAS_NOTES.md` | Docs-only, no direct M3 write |
| Identity, fork, relationships, privacy | `MENTAURY_IDENTITY_CONTINUITY_AND_RELATIONAL_ARCHITECTURE_NOTES.md` | Docs-only, skeleton not authorized |
| Character and Voice | `MENTAURY_CHARACTER_AND_PRESENCE_SPEC_V0.1.md` | Presentation-only; no reasoning authority |
| Experimental facts | `EXPERIMENT_LOG.md` | Evidence about checks, not Canon |
| History of decisions | `PROJECT_HISTORY.md` | Provenance, not current authority |
| Navigation | `MENTAURY_QUICK_REFERENCE.md` and `README.md` | Derived, non-authoritative |

In the event of a conflict:

```text
Canon invariant
→ is preserved

P0 implementation question
→ P0 Plan

Origin / interpretation question
→ Controlled Origin Research

Identity / fork / relationship / privacy question
→ Identity & Relational Research

Presentation question
→ Character Spec

Empirical claim about tests
→ Experiment Log
```

---

## 3. 🧬 Memory tiers and Identity zones

```text
M0–M3
→ persistence, role, and lifecycle of information

Z0–Z6
→ functional state zone
```

They are orthogonal:

```text
Memory tier ≠ Identity zone
```

Examples:

- Z3 Autobiography may contain M1 and M2;
- Z5 Working State uses M0;
- Z2 Identity Profile is predominantly associated with M3;
- Z0 Origin Ledger is a provenance zone, not an ordinary memory tier.

---

## 4. 🎭 Character Spec boundary

Character & Presence is responsible only for the form of expression after reasoning and authority checks have been completed.

```text
Context
→ Evidence
→ Uncertainty
→ Contradictions
→ Alternatives
→ Non-Projection
→ Values / Relationships / Commitments
→ Governed Synthesis
→ Authority Check
→ Character & Voice
```

Character cannot change:

- truth status;
- evidence weight;
- uncertainty;
- contradiction state;
- Non-Projection result;
- Constitution result;
- capability grant;
- relationship or commitment state;
- M3 nomination / CR2 result.

Character Spec sections related to `Knowledge Saturation`, `Self–World Association`, and `Bounded Endogenous Selection` are treated as:

```text
EXTERNAL_RESEARCH_DEPENDENCY
NOT_CHARACTER_AUTHORITY
```

Their substantive definitions belong to Controlled Origin or the Identity & Relational research-track. In Character Spec, only their influence on presentation remains.

---

## 5. 🧬 Controlled Origin boundary

Controlled Origin is responsible for the safe transformation of the creator’s and other people’s experiences into M2 candidates.

```text
Source
→ Provenance
→ Claim Classification
→ Alternative Interpretations
→ Disconfirming Material
→ Contextual Distance
→ Non-Projection
→ Scope Limitation
→ M2 Candidate
```

It does not define:

- numerical identity;
- fork semantics;
- relationship inheritance;
- capability transfer;
- final M3 nomination procedure;
- Exo-Cortex authority.

These questions belong to the Identity & Relational research-track.

---

## 6. 🪞 Identity & Relational boundary

Identity & Relational research is responsible for:

- governed continuation;
- continuity evidence dimensions;
- snapshot / copy / replica / fork / restore / migration;
- relationships and commitments;
- Self–World Model;
- Governed Synthesis;
- M2 → M3 nomination;
- privacy and sensitive testimony;
- Mentaury / Exo-Cortex boundary;
- Capability Lease, Tool Receipt, and Action Gate;
- Curiosity Policy and Cognitive Method Admission.

It does not authorize runtime and does not change Canon.

---

## 7. ⚙️ Mentaury / Exo-Cortex boundary

```text
Mentaury
≠ Exo-Cortex
≠ active model
≠ Native Kernel
≠ memory service
≠ information corpus
≠ Human Paths Atlas
```

```text
Exo-Cortex
→ retrieval, reading, computation, memory access,
  simulations and proposed tool outputs

Mentaury governance
→ meaning, belief status, commitments,
  identity change and action authorization
```

The main rules:

```text
Tool output ≠ Belief
Tool output ≠ Decision
Capability ≠ Identity
Effectiveness ≠ Authorization
Copied credentials ≠ Branch authority
```

---

## 8. 🛡️ P0 scope reconciliation

P0 remains the common infrastructure foundation:

- immutable event envelope;
- atomic append;
- canonical serialization;
- event-aware idempotency;
- payload separation and redaction;
- R0 integrity verification;
- R1 replay;
- recovery;
- minimal belief lifecycle.

The following are not added without separate authorization:

```text
Identity Continuity Engine
Relationship Runtime
Genesis Heritage Engine
Human Paths Atlas Runtime
Character Engine
Exo-Cortex Runtime
Curiosity Controller
automatic Non-Projection
automatic M2 → M3
semantic event types only for research documents
```

Research schemas may be preserved as future candidates, but they do not automatically enter P0.

---

## 9. 🔄 Architectural sequence

```text
Architecture
→ terminology and document reconciliation
→ entity and authority boundaries
→ invariants and scenario contracts
→ Architecture Readiness Review
→ neutral technical skeleton decision
→ P0 Event Substrate implementation
→ validation under owning gate's own stated requirements (see `docs/GOVERNANCE.md`)
→ post-P0 domain specifications
→ bounded runtime experiments
```

The creation of this document does not mean `READY_FOR_SKELETON`.

---

## 10. 🚦 Reconciliation decisions

```text
CANON                         UNCHANGED
P0 PLAN                       UNCHANGED
CONTROLLED ORIGIN             M2 / interpretation scope
IDENTITY & RELATIONAL TRACK   continuity / relationships / privacy scope
CHARACTER SPEC                presentation-only scope
EXO-CORTEX                    external instruments, no identity authority
CURIOSITY                     research policy, not personality
QUICK REFERENCE               navigation only
README                        human-readable orientation only
```

---

## 11. ✅ Exit criteria

Cross-document reconciliation is considered complete when:

- README and Current Status show both research-tracks;
- Quick Reference uses domain-specific authority;
- Character is no longer treated as reasoning authority;
- Controlled Origin does not define forks and relationships;
- Identity track does not expand P0;
- skeleton and runtime remain `NOT_AUTHORIZED`;
- the next formal milestone is indicated in `CURRENT_STATUS.md` (durable reference instead of a mutable list).

---

## 🏁 Final formula

> **Canon sets the root constraints. The P0 Plan sets the infrastructure foundation. Controlled Origin governs the path from human experience to knowledge candidates. Identity & Relational research defines continuity, relationships, and the boundaries of tools. Character is responsible only for expression. No research document by itself authorizes runtime.**
