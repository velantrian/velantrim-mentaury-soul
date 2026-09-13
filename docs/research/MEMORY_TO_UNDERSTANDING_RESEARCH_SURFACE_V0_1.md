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
