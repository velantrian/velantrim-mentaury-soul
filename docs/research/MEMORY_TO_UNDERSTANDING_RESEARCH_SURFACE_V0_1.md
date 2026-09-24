# 🧠 Memory → Understanding Research Surface v0.1

**Status:** `OPEN_RESEARCH · NON_CANONICAL · DOCS_ONLY`  
**Date:** `2026-09-13`  
**Scope:** cognition-side use of available memory/information  
**Runtime authority:** `NONE`  
**Architecture promotion:** `NONE`  
**New organ/module:** `NO`

## 1. Purpose

This note defines a bounded research surface for studying how available information may or may not become demonstrated cognition. It does not define an implementation pipeline and does not introduce an `Understanding Engine`, `Composition Engine`, memory owner, persistence owner, or runtime component.

The motivating observation is that information may be present and semantically adequate as a representation while the resulting output still fails to demonstrate required relation composition or a decisive answer.

## 2. Core distinctions

```text
INFORMATION AVAILABLE
!=
UTILIZATION DEMONSTRATED

REPRESENTATION SUFFICIENCY
!=
UTILIZATION SUFFICIENCY

INFORMATION PRESENT
!=
COMPOSITION DEMONSTRATED

RELATION COMPOSITION
!=
DECISION EXPRESSION
```

The first two are bounded substrate-neutral research candidates routed to Native Kernel. The latter two remain cognition-side research candidates and are not frozen invariants.

## 3. Observable research questions

For a bounded task, distinguish at least four questions:

### P — Presence
Was the information required by the task represented in the supplied material?

### A — Cognitive access / availability
Was the relevant information available to the current bounded cognitive process, rather than merely existing elsewhere in durable memory?

Here `A` is a cognition-side research label only. It does not establish storage, retrieval, persistence, or representation-level authority; Native Kernel retains the substrate-neutral representation/availability boundary.

### C — Composition
Did the output demonstrate the relations needed to combine the relevant elements for the task?

### D — Decision expression
Did the final response express the warranted task-level decision, including a justified `UNKNOWN` / clarification / abstention when that is actually correct?

These labels are research shorthand only. They are not a frozen state machine, pipeline, enum, or runtime contract.

## 4. Why retrieval is insufficient as the research unit

Retrieval can establish that candidate material reached a bounded working surface. It does not by itself establish:

- attention;
- interpretation;
- relation composition;
- applicability under current scope;
- correct use;
- belief admission;
- identity admission;
- decision adequacy;
- action authorization.

Therefore:

```text
RETRIEVED
!=
UNDERSTOOD

CONTEXT PRESENCE
!=
DEMONSTRATED USE
```

## 5. Relation-composition failure class

A bounded failure may look like:

```text
A
B
C
D
```

all being present, while the task requires:

```text
A --depends-on--> B
B --only-if--> C
C --conflicts-with--> D
```

The absence of the complete required composition in an output does not prove a specific hidden internal failure. It only supports the observable claim that the required composition was not demonstrated.

```text
OUTPUT OMISSION
!=
IDENTIFIED INTERNAL MECHANISM
```

## 6. Relationship to Cognitive Orientation View v0.1

`Cognitive Orientation View v0.1` represents what is happening now, the active objective, constraints, live alternatives, critical unknowns, and a bounded next-step class.

This research surface does not modify that freeze.

```text
ORIENTATION
!=
UTILIZATION PROOF

ORIENTATION
!=
RELATION COMPOSITION ENGINE

CURRENT OBJECTIVE
!=
AUTOMATIC COGNITIVE MODE SELECTION
```

A future experiment may test whether orientation quality changes P/A/C/D outcomes, but no such dependency is assumed here.

## 7. Candidate cognitive arbitration question

A related open question is how a bounded cognitive process chooses among actions such as:

```text
recall
search
reopen source
associate
compare
reason
simulate
ask
abstain
stop
```

This is tentatively described as **cognitive arbitration / mode selection**.

It is not yet justified as a Soul primitive, engine, scheduler, or runtime owner.

Potential failure classes include:

```text
semantic drift
mode drift
goal drift
scope drift
authority drift
identity drift
```

These labels remain research vocabulary pending concrete discriminating fixtures.

## 8. Adversarial fixture seeds

Future bounded research may include cases where:

1. all required facts are present but one key relation is omitted;
2. a plausible relation is composed but is false under the supplied evidence;
3. one available fact has been superseded;
4. two correct sources apply under different scopes;
5. retrieval adds noise and the best answer requires no deeper retrieval;
6. an old rejected route matters because its rejection reason changes the next step;
7. a structurally similar situation uses different surface wording;
8. the correct cognitive mode is exploratory discussion, not implementation;
9. the correct answer is `UNKNOWN`, clarification, or abstention.

No fixture execution is authorized by this note.

## 9. Ownership boundary

```text
🧬 Native Kernel
  availability / representation / provenance / semantic distinctions

🌀 Mentaury Soul
  cognition-side utilization / relation composition /
  understanding-oriented research / decision expression

🌎 Continuum
  continuity and originating CONT-E0T empirical result

🪁 Mentaury-Kernel
  cross-domain preservation only; no new invariant from this note
```

## 10. Stop rule

Do not create a new component merely because a research label is useful.

A stronger contract is justified only when a concrete bounded failure:

1. cannot be represented by existing distinctions;
2. causes a materially different correct next-step orientation or cognitive outcome;
3. survives adversarial alternative explanations;
4. is repaired by a smaller explicit distinction than by a new engine.

Until then:

```text
RESEARCH SURFACE != ARCHITECTURE CONTRACT
FUNCTION != MODULE
PHENOMENON != MECHANISM
CORRECT OUTPUT != PROOF OF UNDERSTANDING
FAILURE TO COMPOSE != PROOF OF NO UNDERSTANDING
```

## 11. Practical thread-memory / relevance checkpoint — 2026-09-16

A direct product-use observation sharpens the research surface: a remembered item can be true and personally meaningful while still being a poor input to the current task.

Therefore the bounded research unit should distinguish at least:

```text
DURABLE MEMORY EXISTS
!=
MEMORY RETRIEVED
!=
MEMORY TASK-RELEVANT
!=
MEMORY USED APPROPRIATELY
```

Additional distinctions:

```text
PERSONALLY RELEVANT != TASK RELEVANT
RECALLED != TRUE
OLD MEMORY != CURRENT STATE
NOT RETRIEVED != ABSENT
```

A minimal **Active Thread** is a candidate working representation of current cognitive position, not a new storage owner or Soul module:

```text
WHERE WE STOPPED
WHAT REMAINS OPEN
NEXT STEP
OPTIONAL PRIMARY SOURCES
```

Active Thread is a practical checkpoint projection that may draw on the frozen `Cognitive Orientation View v0.1` (§6), materially relevant bounded history, and source references. It does not modify, extend, or compete with that freeze and does not introduce new orientation semantics, persistence ownership, or runtime requirements.

A separate navigation map can answer where knowledge lives; the Active Thread answers where the current thought is. The two functions should not be collapsed by default.

For early dogfooding, an initial set of three observable dimensions is useful for collecting failure cases without promoting them to scientific validation:

- **Continuity** — did a fresh context recover the correct working position?
- **Relevance** — did the recalled material help the present task?
- **Intrusion** — did true-but-irrelevant memory distort or distract the current task?

These observations may later motivate bounded fixtures around cognition-side memory use, but they are not themselves TCE or EDCA experiments.

```text
THREAD MEMORY DOGFOODING != CONTROLLED EXPERIMENT
GOOD RETRIEVAL != EDCA
ACTIVE THREAD SUCCESS != TCE PASS
USEFUL BEHAVIOR != UNDERSTANDING PROOF
```

The practical target is intentionally modest: make context rollover survivable for real work, then use the resulting failure corpus to decide whether the next missing distinction belongs to continuity, provenance/version qualification, routing/orientation, applicability, or another existing owner.

## 12. Source-bound donor note — retrieval, reconstruction, and recursive derivation · 2026-09-24

**Status:** `SOURCE-BOUND RESEARCH NOTE · NON-CANONICAL · DOCS_ONLY`  
**Runtime authority:** `NONE`  
**Architecture promotion:** `NONE`  
**New organ/module:** `NO`

Source: user-supplied transcript of a 10:39 YouTube video by Keith Scott-Mumby, discussed in the research thread as “fractal memory”.

### Transcript-supported core

The bounded donor value is that human memory is reconstructive rather than guaranteed verbatim replay, and that reconsolidation research is relevant to the possibility that retrieved memories can, under some conditions, become labile and be updated.

Do not strengthen this into:

```text
EVERY RETRIEVAL REWRITES MEMORY
```

Boundary conditions matter.

### Author-specific / not established here

The transcript's `MIMP → MIMP+ → MIMP++` / “fractalization” framing, any suggestion of a pristine recoverable original, and related branded terminology are treated as source claims or metaphor, not as an established scientific mechanism.

### Velantrim research inference

A derived-representation chain such as:

```text
SOURCE / EVENT
→ INTERPRETATION
→ SUMMARY
→ SUMMARY-OF-SUMMARY
```

may accumulate provenance, status, commitment, or authority drift if a later representation is treated as though it were the source.

This is a cognition-side failure candidate, not a demonstrated mechanism and not a new invariant. It cross-references existing substrate-neutral distinctions:

```text
SUMMARY != SOURCE
RETRIEVAL != REVISION
CURRENT != HISTORY
```

Research caution:

- keep a reopenable path to the primary source/event;
- keep derived interpretations attributable;
- do not let retrieval or summary silently replace source history;
- do not allow repetition of a derived representation to acquire durable authority.

This note creates no experiment ID and authorizes no implementation.
