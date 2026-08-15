# 📚 Velantrim Documentation Standard v1

This repository uses four documentation layers over one project truth:

```text
                 🧬 ONE PROJECT TRUTH
                         │
       ┌─────────────────┼─────────────────┐
       │                 │                 │
       ▼                 ▼                 ▼
   👤 HUMAN          🤖 AGENT          ⚙️ MACHINE
README / OVERVIEW    docs/ai/**       JSON / state
       │                 │                 │
       └─────────────────┴────────┬────────┘
                                  ▼
                         📚 EVIDENCE / HISTORY
```

## Core rule

```text
overview != current state != evidence != history
```

The four layers may present the same project differently, but they must not contradict the same underlying truth.

---

## 1. Human-first landing architecture

The maintained human route should move from **meaning to detail**, not from control-plane literals to meaning.

Preferred sequence:

```text
🧬 Project identity
        │
        ▼
👋 Human explanation / why this exists
        │
        ├────────────→ 🤖 Special for AI route
        │
        ▼
🧠 Mental model
        │
        ├── 🗺️ Mindmap
        ├── ⚙️ ASCII flow
        ├── 🌳 Structural tree
        ├── 🔄 Architecture diagram
        └── 💬 Commentary
        │
        ▼
📊 What actually exists today
        │
        ▼
🆚 Positioning / non-goals / distinctions
        │
        ▼
🧭 Reading routes
        │
        ▼
🔬 Current research boundary
        │
        ▼
🛠 Human quickstart / inspection path
        │
        ▼
📎 Exact technical / historical detail
```

The README may be shorter than the deep overview, but it must let a new human understand the project's purpose and current boundary before exposing dense milestone chronology.

`SYSTEM_OVERVIEW.md` is the deeper human map. It should explain the architecture without requiring the reader to decode PR numbers, SHA values or validator literals.

---

## 2. Visual semantics

Visuals are functional, not decorative duplicates:

```text
🗺️ Mindmap    = HOW CONCEPTS RELATE
⚙️ ASCII      = HOW INFORMATION / AUTHORITY FLOWS
🌳 Tree       = WHAT EXISTS
🔄 Diagram    = HOW ARCHITECTURAL LAYERS CONNECT
📊 Table      = WHAT EXISTS / MAY / MUST NOT DO
💬 Commentary = WHY THE ARCHITECTURE IS DESIGNED THIS WAY
```

Rules:

- keep visuals compact enough to scan on a phone;
- do not create five copies of the same paragraph in different formats;
- prefer stable semantic concepts over volatile SHA/CI values inside visuals;
- label conceptual/future flows when they are not executable pipelines;
- never let a visual imply authority that the current state does not grant.

---

## 3. Stable vs volatile content

### Stable human portrait

Prefer stable content for:

- purpose;
- core architecture;
- persistent invariants;
- non-goals;
- conceptual domains;
- reading routes;
- visual grammar.

### Volatile truth surfaces

Keep these in current-state/evidence layers:

- current phase;
- exact Owner GO state;
- PR/SHA/CI values;
- test counts;
- temporary blockers;
- review state;
- exact implementation/runtime checkpoint.

Avoid copying volatile evidence into every stable visual block.

---

## 4. Change classification

### STRUCTURAL_CHANGE

Changes architecture, project meaning, ownership, authority boundaries, invariants, subsystem responsibilities, runtime model or major roadmap direction.

Required action:

```text
verify owning change
→ review all maintained landing roles
→ update every affected human representation only
→ update agent navigation/manifest if ownership or routes changed
→ update current-state surfaces
→ preserve history
→ read back
```

A structural change is incomplete if it leaves the Executive Summary, mindmap, ASCII flow, tree, architecture diagram, capability table, commentary, non-goals or reading routes materially false.

### STATE_CHANGE

Changes phase, admission, Owner GO, implementation/readiness/runtime/action/production state without redesigning architecture.

Required action: remove stale high-level implications and update current-state/machine surfaces. Stable visual architecture normally remains unchanged.

### EVIDENCE_ONLY

Changes PR/SHA/CI/review/test counts/docs-sync evidence or bounded fixes that preserve architecture and high-level state meaning.

Required action: update evidence/current-state logs where needed. Do not churn stable landing visuals merely because evidence identifiers changed.

---

## 5. Human / AI / machine separation

### 👤 Human layer

Optimized for comprehension and navigation.

It may use:

- concise prose;
- emoji visual grammar;
- mindmaps;
- ASCII flows;
- trees;
- Mermaid architecture diagrams;
- capability/status tables;
- commentary and reading routes.

It is **not** authoritative proof of implementation or permission.

### 🤖 Agent layer

Optimized for bounded orientation, source-of-truth hierarchy, maintenance rules and context budgeting.

An AI must be able to determine:

- where current truth lives;
- which contract owns a behavior;
- which files are relevant;
- what authority is absent;
- which documentation surfaces become stale after a change.

### ⚙️ Machine layer

Optimized for deterministic state/navigation consumption.

`project_manifest.json` is the documentation/navigation contract. `docs/state/project_state.json` is a maintained snapshot, not an evergreen live-head claim.

### 📚 Evidence/history layer

Preserves milestone receipts, exact PR/SHA/CI/review evidence and research provenance.

History must not be rewritten just to make the current documentation cleaner.

---

## 6. Machine-readable contract

`project_manifest.json` describes:

- human landing surfaces;
- AI entry and agent contract;
- machine/current truth surfaces;
- visual roles;
- reading routes;
- update classes;
- structural path hints;
- Notion synchronization boundaries.

It is navigation and maintenance metadata, not implementation truth.

---

## 7. Staleness guard

```text
meaning changed
→ landing surfaces reviewed
→ affected representations refreshed
→ agent/machine routes refreshed when necessary
→ current truth refreshed
→ evidence/history preserved
→ post-update read-back
```

A change is incomplete if it makes a maintained Summary, Tree, Mindmap, ASCII flow, architecture diagram, boundary table, commentary, non-goal or reading route materially false.

The current documentation impact guard is **contract-level**, not executable CI. Structural path hints must therefore be treated conservatively as `REVIEW_REQUIRED` until the human landing layer has been checked.

An executable CI impact guard may be added later as a separate technical milestone.

---

## 8. Emoji visual grammar

Emoji carry lightweight semantic meaning:

```text
🧬 project / identity architecture
🧠 cognition / knowledge
🌱 provenance / origin
🧾 claim / record
⚖️ epistemic governance
🔗 relation
🪞 identity / continuity
🤝 relationship / commitment
🎭 character / presence
🛡 authority / boundary
🚦 state / permission gate
🧪 experiment / bounded laboratory
🔬 evidence / research
✅ established / implemented
🟡 incomplete / conditional / bounded
❌ absent / unauthorized
🧊 frozen contract
🤖 AI / agent
👤 human
⚙️ machine
📎 history / technical detail
```

Emoji never replace exact state literals where machine or governance precision is required.

---

## 9. Preservation rules

Always preserve these distinctions:

```text
presentation != proof
claim != belief
relation != truth
character != evidence
continuity != identity proof
contract freeze != implementation authority
implementation != runtime authority
runtime capability != action authority
```

Documentation must not accidentally promote architecture diagrams, roadmap arrows or human-friendly prose into claims of implemented runtime behavior.