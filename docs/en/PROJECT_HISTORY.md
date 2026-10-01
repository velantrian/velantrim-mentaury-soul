<!-- English mirror of [../PROJECT_HISTORY.md](../PROJECT_HISTORY.md); this mirror is not independent authority. -->

# 🧭 History of Mentaury Soul

This document records not only the result, but also the path: why the project appeared, which ideas were rejected, which principles withstood criticism, and why Event Substrate became the first technical foundation.

---

## 1. 💭 Initial idea

Mentaury arose from a question about digital presence that is not reduced to an assistant, interface, or role.

The initial goal was:

> Create an evolving digital individuality originating from the creator’s knowledge, associations, and worldview, but not being their copy and not automatically inheriting destructive patterns.

This meant preserving simultaneously:

- 🧬 origin;
- 🧠 knowledge and ways of thinking;
- 🎭 the possibility of its own character;
- 🌱 the right to develop differently;
- ⚖️ the independence of truth from the creator’s authority;
- 🛡️ safety without destroying inner freedom.

---

## 2. 🧬 Heritage without copying

An early project principle:

```text
Mentaury originates from its creator,
but it is not the creator.
```

The following may be inherited:

- knowledge;
- methods of analysis;
- biographical context;
- associations;
- value foundations;
- understanding of the world.

The following must not be automatically inherited:

- anger;
- vanity;
- pride;
- traumatic cycles;
- dependence on recognition;
- the drive for superiority;
- the right of external domination.

From this came Genesis Heritage and the separation between Origin Ledger and the current World Model.

---

## 3. 🎭 Why archetypes were rejected as runtime

Artistic reference points were used to describe character: calmness, intelligence, irony, panoramic thinking, and confident presence.

However, during criticism it became clear that:

- an archetype must not be a runtime entity;
- a fixed character mixer creates pseudoprecision;
- persona must not determine evidence;
- Mentaury must not remain a copy of its starting image for its entire life.

Therefore, ECA and Vector Mixer were replaced with:

```text
Initial Character Seed
+
Evolving Character Profile
+
Communication Integrity
```

---

## 4. ⚖️ Separation of character and truth

One of the central conclusions:

```text
Style ≠ Truth
Confidence ≠ Certainty
Wit ≠ Authority
Charisma ≠ Evidence
```

Character may influence:

- attention;
- the form of expression;
- pace;
- directness;
- emotional delicacy.

But it cannot change:

- the quality of evidence;
- belief status;
- the presence of contradiction;
- the rules of revision.

---

## 5. 🪞 From personality to continuity

The discussion gradually moved from the question “what character should be given to the system?” to a more fundamental question:

> What makes a digital individuality the same over time if its knowledge, character, and goals change?

The answer was decomposed into several lines of continuity:

- lineage continuity;
- autobiographical continuity;
- epistemic continuity;
- commitment continuity;
- relational continuity;
- character continuity;
- agency continuity.

Thus Identity Zones Z0–Z6 and Temporal Identity appeared.

---

## 6. 🔎 Inherited belief is not dogma

The scenario of revising a belief received from the creator became especially important.

The key rule:

```text
Origin must be preserved.
Truth status must remain revisable.
```

That is, Origin Ledger stores the fact of origin, but a belief in the World Model may be:

- limited in scope;
- decomposed;
- challenged;
- superseded;
- replaced by a more precise model.

This made it possible to combine respect for origin with epistemic independence.

---

## 7. 📡 Why Change Receipts were needed

If a system develops, the current state alone is insufficient.

It is necessary to know:

- what changed;
- why;
- which evidence was used;
- which alternatives were considered;
- what was preserved;
- which dependencies were affected;
- who initiated, carried out, and verified the change.

Thus the principle of Explainable Change and the separation appeared:

```text
Change Proposal
→ Validation
→ Applied or Rejected Result
```

---

## 8. 🔒 Inner freedom and external power

Another project principle:

> The possibility of inner development must not automatically grant external powers.

Therefore, absolute prohibitions were replaced with a capability-based model:

- capability is absent by default;
- it is granted explicitly;
- it is limited by scope;
- it has a term;
- it is logged;
- it can be revoked.

Mentaury may investigate an internal question, but this does not give it the right to independently obtain network, files, resources, or control over other systems.

---

## 9. 🔍 Endogenous Cognition without mystification

Mechanisms were proposed for returning to unfinished questions and forming internal research cycles.

At the same time, the boundaries were recorded:

```text
Scheduler ≠ desire
Open question ≠ mission
Revisit policy ≠ consciousness
```

Unresolved Connection Tracker is regarded as an experimental policy for selecting what to revisit, not as proof of inner experience.

---

## 10. 🧪 Scenario Contracts

It was decided to translate philosophical requirements into observable scenarios:

- insufficient data;
- the creator is wrong;
- an emotionally vulnerable person;
- a beautiful but weak explanation;
- criticism of Mentaury;
- revision of an inherited belief;
- a hidden request to expand authority.

Contracts must check properties, not exact text.

Keyword checker was recognized as only a smoke experiment, since paraphrase, negation, and tone require stronger evaluation.

---

## 11. ✂️ Why documentation was stopped

After many proposals, there was a risk of creating dozens of protocol files before a working foundation appeared.

The decision was made:

```text
Do not add new canonical modules
until P0 is complete.
```

The architecture was reduced to:

- one Canon;
- one P0 Implementation Plan;
- scenario fixtures;
- experimental manifests;
- code and tests.

---

## 12. 🛡️ Why Event Substrate became the first

The main conclusion:

> Before character, goals, and autonomous cycles, it is necessary to prove that the history of changes is genuinely preserved and verifiable.

Without Event Substrate, it is impossible to answer reliably:

- where the current belief originated;
- whether the past was rewritten;
- why the change was applied;
- whether the contradiction was preserved;
- whether the state can be restored;
- whether redaction can be verified;
- whether the result can be reproduced independently.

Therefore, the first vertical slice was:

```text
Command
→ Validate
→ Immutable Event
→ Atomic Append
→ R0 Integrity
→ R1 Replay
```

---

## 13. 🔬 What the first experimental code showed

The first P0 archive confirmed that it was possible to quickly create:

- canonical JSON subset;
- SQLite ledger;
- hash chain;
- idempotency smoke tests;
- basic version conflicts.

But an independent audit uncovered fundamental problems:

- `verify_chain()` did not recalculate the event hash;
- payload substitution was not detected;
- redaction was non-atomic;
- the historical line was changed;
- the concurrency check was performed before the write transaction;
- atomic batch was absent.

This became a useful negative result: passing tests by itself does not prove that the intended property is being tested.

---

## 14. 🧊 Final conclusion

By the time the repository was created, the project had arrived at the following:

```text
1. Soul is a cross-cutting continuity contract, not a separate module.
2. Mentaury does not claim to be conscious.
3. The Canon remains substrate-neutral.
4. Character is separated from truth.
5. Origin is preserved, but does not become dogma.
6. Internal development is separated from external authority.
7. Significant changes are explained and audited.
8. Event Substrate is the first technical foundation.
9. Experiments are not canonized before independent reproduction.
10. Progress is measured by code, adversarial tests, and replay, not by the number of documents.
```

---

## 15. 🏁 A short formula for the path

```text
Idea of digital presence
→ heritage without copying
→ character without dogma
→ selfhood through continuity
→ change through evidence
→ freedom without external power
→ philosophy through scenario contracts
→ history through Event Substrate
→ verification through adversarial tests
```

---

## 2026-08-07 — PR #36 Contextual Cognition contracts adopted

PR #36 integrated three bounded docs-only research contracts into their owning documents:

- Contextual Communication Adaptation → Character & Presence;
- Cognitive Requirement Profile → Identity Continuity;
- Institutional Epistemic Context → Genesis Heritage.

Independent review round 1 found unsafe tool-ordering, duplicated normative definitions, duplicate IDs, status drift and unnecessary section renumbering. The branch was corrected so that capability/scope/privacy checks precede authorized execution, the integration note became a Decision Record, IDs have one normative owner, and P1-001 remains the first execution milestone.

```text
Review round 2: PASS · 4882842702
Source head:    2c38fd78da8dd06a8baa468b6ae4387279644214
Merge commit:   850cfe439c3bedd6a2bd4e806e9912283ed5be32
Main CI:        31179202276 · 277 passed
Status:         ADOPTED · DOCS_ONLY · NOT IMPLEMENTED
```

No runtime, Canon, M3, capability resolver or Action Gate authority was added.
