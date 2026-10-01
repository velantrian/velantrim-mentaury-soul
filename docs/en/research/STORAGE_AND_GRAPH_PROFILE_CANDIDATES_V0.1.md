<!-- English mirror of [`../../research/STORAGE_AND_GRAPH_PROFILE_CANDIDATES_V0.1.md`](../../research/STORAGE_AND_GRAPH_PROFILE_CANDIDATES_V0.1.md); this mirror is not independent authority. -->

# 🗄️ Storage and Graph profile candidates — notes v0.1

```text
Status:                       CAPTURED · RESEARCH_NOTES · NON_CANONICAL · DOCS_ONLY
Version:                      0.1
Date:                         2026-08-07
Area:                         Future implementation profiles · Storage · Relationship indexes
Runtime authority:            NONE
Truth authority:              NONE
Capability authority:         NONE
Canon modification authority: NONE
Selection authority:          NONE — no profile selected here
P0 scope authority:           NONE
Direct writing to M3:         FORBIDDEN
Implementation in src/:       NOT AUTHORIZED
P1-001 priority impact:       NONE
```

> This document records future engineering profile candidates. It does not select
> PostgreSQL, Graphiti, LadybugDB, or any other engine; change the Canon; or
> authorize runtime. The current reference profile remains `Python + SQLite`.
> Graphiti and LadybugDB are **different product classes**, not interchangeable
> synonyms for “graph engine”: see section 4 for the precise distinction.

```text
Candidate named ≠ adopted profile
More powerful store ≠ required by Canon
Graph product ≠ relationship runtime
Research presence ≠ roadmap priority
```

---

## 1. 🎯 Why this note exists

Canon and P0 invariants are substrate-neutral:

```text
Implementation Profile ≠ Canon
Python + SQLite = replaceable first profile
```

Two natural questions arose for the owner:

1. Why SQLite now, rather than PostgreSQL as a more powerful main store?
2. Is a graph layer needed for relationships — a temporal context-graph framework such as Graphiti, or an embedded graph database such as LadybugDB?

The answer at the current checkpoint is: **do not connect either candidate**, but retain the candidates as `CAPTURED`, with explicit non-claims and criteria for a future selection.

---

## 2. 🧱 Current reference profile

```text
Profile:     Python 3.13 + standard-library SQLite
Role:        current P0 reference / proof profile
Runtime deps: NONE
Status:      IMPLEMENTED IN MAIN for P0-001…P0-015 event substrate
```

SQLite was chosen not as the “only destiny,” but as a minimal reproducible workshop for:

- immutable event/payload storage;
- atomic batches and idempotency;
- bounded concurrency;
- R0/R1 integrity and deterministic replay;
- governed redaction;
- an empty runtime-dependency boundary.

---

## 3. 🐘 PostgreSQL — future storage profile candidate

```text
Research ID:     R-STORE-PG-001
Candidate:       PostgreSQL
Disposition:     CAPTURED · NOT SELECTED
Role if ever adopted: durable / multi-writer storage profile
Canon impact:    NONE unless separate profile RFC is accepted
```

### Why not now

- P0 is still proving event-substrate invariants on one lightweight profile;
- Postgres adds operational surface: roles, backups, replication, and locks;
- “More powerful” does not automatically mean more correct for the current proof stage;
- changing the store without a profile contract can easily turn a blueprint into a dependency.

### What must be proven before any selection

```text
deterministic rebuild from authoritative history
+ redaction / privacy reconciliation
+ fail-closed admission and budgets
+ no silent M2/M3 promotion
+ profile replaceability retained
+ explicit owner RFC / ADR inside Mentaury
+ independent review
```

### Explicit non-claims

```text
PostgreSQL mentioned
≠ PostgreSQL adopted
≠ SQLite deprecated
≠ dual-write authorized
≠ production HA topology chosen
```

---

## 4. 🕸️ Graph-related candidates — two distinct product classes

Graphiti and LadybugDB are **not the same type of product** and must not be generalized under one “graph engine” label. They are presented below as two separate cards.

### 4.1. 🕰️ Graphiti — temporal context-graph framework candidate

```text
Research ID:          R-GRAPH-TEMPORAL-001
Candidate:            Graphiti
Product class:       temporal context-graph framework / engine
Role:                 builds and queries context graphs that change over time
Disposition:          CAPTURED · NOT SELECTED
Role if ever adopted: derived temporal relationship/context projection candidate
Authority over identity / M3: NONE
```

### 4.2. 🗄️ LadybugDB — embedded graph database candidate

```text
Research ID:          R-GRAPH-EMBEDDED-001
Candidate:            LadybugDB
Product class:       embedded property-graph database / DBMS
Role:                 standalone storage and graph-query execution layer
Disposition:          CAPTURED · NOT SELECTED
Role if ever adopted: alternative/derived storage+query layer candidate
Authority over identity / M3: NONE
```

### Current repository truth

- neither a temporal context-graph framework nor an embedded graph database is **connected** in Mentaury;
- relationships/commitments remain research (`DOCS_ONLY`);
- mentions of graph edges in privacy/research notes ≠ a selected graph product;
- Native Kernel ADR-0006 and Mentaury relationship research may later inform the shape, but they do not import another system’s runtime.

### Why neither Graphiti nor LadybugDB should be connected now

- relationship runtime and identity runtime are not yet authorized;
- a framework for temporal context graphs (Graphiti) and an embedded graph DBMS (LadybugDB) solve different problems and require separate evaluation, rather than one “graph yes/no” decision;
- a graph index/store is a derived surface subject to privacy, rebuild, redaction, and consent;
- an early vendor/engine choice locks in the workshop before the blueprint;
- P1-001 (Capability Lease Resolution) remains the first execution milestone.

### What must be proven before any selection (for each candidate separately)

```text
authoritative history remains source of truth
+ graph/index is rebuildable projection, not authority
+ consent / redaction / restore reconciliation
+ no silent belief or identity promotion
+ bounded schema + provenance
+ Non-Projection review
+ explicit owner RFC / ADR inside Mentaury
+ independent review
+ product-class-specific evaluation (framework vs DBMS have different
  operational, deployment and threat surfaces)
```

### Explicit non-claims

```text
Graphiti named
≠ selected
≠ same product class as LadybugDB
≠ relationship runtime authorized

LadybugDB named
≠ selected
≠ same product class as Graphiti
≠ relationship runtime authorized

Either candidate named
≠ shared graph with Native Kernel / Titan / Crystal
≠ automatic M2/M3 write path
```

---

## 5. 🧭 Promotion gate before any wiring

Any transition from “candidate recorded” to “code/dependency in the repository” requires:

```text
problem demonstrated against current SQLite profile
+ existing mechanisms shown insufficient
+ minimal bounded profile slice defined
+ inputs / outputs / invariants specified
+ explicit non-goals recorded
+ threat / privacy model recorded
+ Canon and P0 compatibility checked
+ previous milestone completed or explicitly superseded
+ independent architecture review
+ explicit repository-owner authorization
= eligible for profile implementation planning
```

Before this gate:

```text
docs-only capture: ALLOWED
dependency add:    FORBIDDEN
src/ wiring:       FORBIDDEN
roadmap jump:      FORBIDDEN
```

---

## 6. 📌 Current decision

```text
SQLite reference profile:                    RETAINED
PostgreSQL:                                  CAPTURED · NOT SELECTED
Graphiti (temporal context-graph framework): CAPTURED · NOT SELECTED
LadybugDB (embedded graph database):         CAPTURED · NOT SELECTED
Runtime wiring:                              NOT AUTHORIZED
Execution milestone created:                 NO
P1-001 priority:                             UNCHANGED
```

See also:

- [`../../ENVIRONMENT_MANIFEST.md`](../../ENVIRONMENT_MANIFEST.md) — current profile facts;
- [`../MENTAURY_P0_IMPLEMENTATION_PLAN.md`](../MENTAURY_P0_IMPLEMENTATION_PLAN.md) — `Implementation Profile ≠ Canon`;
- [`NATIVE_KERNEL_RESEARCH_INPUT_NOTES_V0.1.md`](NATIVE_KERNEL_RESEARCH_INPUT_NOTES_V0.1.md) — external research input boundary;
- [`MENTAURY_IDENTITY_CONTINUITY_AND_RELATIONAL_ARCHITECTURE_NOTES.md`](MENTAURY_IDENTITY_CONTINUITY_AND_RELATIONAL_ARCHITECTURE_NOTES.md) — relationships research (docs-only).
