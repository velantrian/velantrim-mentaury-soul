# 🗄️ Storage and Graph profile candidates — notes v0.1

```text
Статус:                       CAPTURED · RESEARCH_NOTES · NON_CANONICAL · DOCS_ONLY
Версия:                       0.1
Дата:                         2026-08-07
Область:                      Future implementation profiles · Storage · Relationship indexes
Runtime authority:            NONE
Truth authority:              NONE
Capability authority:         NONE
Canon modification authority: NONE
Selection authority:          NONE — no profile selected here
P0 scope authority:           NONE
Прямая запись в M3:           FORBIDDEN
Implementation in src/:       NOT AUTHORIZED
P1-001 priority impact:       NONE
```

> Этот документ фиксирует будущие кандидаты engineering profiles. Он не выбирает
> PostgreSQL, Graphiti, LadybugDB или любой другой движок, не меняет Canon и не
> авторизует runtime. Текущий reference profile остаётся `Python + SQLite`.

```text
Candidate named ≠ adopted profile
More powerful store ≠ required by Canon
Graph product ≠ relationship runtime
Research presence ≠ roadmap priority
```

---

## 1. 🎯 Зачем эта заметка

Canon и P0-инварианты substrate-neutral:

```text
Implementation Profile ≠ Canon
Python + SQLite = replaceable first profile
```

Возникли два естественных вопроса владельца:

1. почему сейчас SQLite, а не PostgreSQL как более мощный main store;
2. нужен ли graph layer (Graphiti, LadybugDB или аналог) для relationships.

Ответ на текущем checkpoint: **не подключать**, а сохранить как `CAPTURED`
кандидаты с явными non-claims и критериями будущего выбора.

---

## 2. 🧱 Current reference profile

```text
Profile:     Python 3.13 + standard-library SQLite
Role:        current P0 reference / proof profile
Runtime deps: NONE
Status:      IMPLEMENTED IN MAIN for P0-001…P0-015 event substrate
```

SQLite выбран не как «единственная судьба», а как минимальная воспроизводимая
мастерская для:

- immutable event/payload storage;
- atomic batches и idempotency;
- bounded concurrency;
- R0/R1 integrity и deterministic replay;
- governed redaction;
- empty runtime-dependency boundary.

---

## 3. 🐘 PostgreSQL — future storage profile candidate

```text
Research ID:     R-STORE-PG-001
Candidate:       PostgreSQL
Disposition:     CAPTURED · NOT SELECTED
Role if ever adopted: durable / multi-writer storage profile
Canon impact:    NONE unless separate profile RFC is accepted
```

### Почему не сейчас

- P0 ещё доказывает event-substrate invariants на одном лёгком профиле;
- Postgres добавляет operational surface: roles, backups, replication, locks;
- «более мощный» ≠ автоматически более правильный для текущего proof stage;
- смена store без profile contract легко превращает чертёж в зависимость.

### Что должно быть доказано до любого selection

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

## 4. 🕸️ Graph engines — future relationship-index candidates

```text
Research ID:     R-GRAPH-IDX-001
Candidates:      Graphiti, LadybugDB, and unspecified future graph/index engines
Disposition:     CAPTURED · NOT SELECTED
Role if ever adopted: derived relationship index / projection candidate
Authority over identity / M3: NONE
```

### Текущая правда репозитория

- graph DB runtime в Mentaury **не подключён**;
- relationships/commitments остаются research (`DOCS_ONLY`);
- упоминания graph edges в privacy/research notes ≠ выбранный graph product;
- Native Kernel ADR-0006 и Mentaury relationship research могут позже
  информировать форму, но не импортируют чужой runtime.

### Почему не подключать Graphiti / LadybugDB сейчас

- relationship runtime и identity runtime ещё не авторизованы;
- graph index — это derived surface (privacy, rebuild, redaction, consent);
- ранний выбор vendor/engine закрепляет мастерскую раньше чертежа;
- P1-001 (Capability Lease Resolution) остаётся первым execution milestone.

### Что должно быть доказано до любого selection

```text
authoritative history remains source of truth
+ graph/index is rebuildable projection, not authority
+ consent / redaction / restore reconciliation
+ no silent belief or identity promotion
+ bounded schema + provenance
+ Non-Projection review
+ explicit owner RFC / ADR inside Mentaury
+ independent review
```

### Explicit non-claims

```text
Graphiti / LadybugDB named
≠ selected
≠ relationship runtime authorized
≠ shared graph with Native Kernel / Titan / Crystal
≠ automatic M2/M3 write path
```

---

## 5. 🧭 Promotion gate before any wiring

Любой переход от «кандидат записан» к «код/зависимость в репозитории» требует:

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

До этого gate:

```text
docs-only capture: ALLOWED
dependency add:    FORBIDDEN
src/ wiring:       FORBIDDEN
roadmap jump:      FORBIDDEN
```

---

## 6. 📌 Текущее решение

```text
SQLite reference profile:     RETAINED
PostgreSQL:                   CAPTURED · NOT SELECTED
Graphiti / LadybugDB / other: CAPTURED · NOT SELECTED
Runtime wiring:               NOT AUTHORIZED
Execution milestone created:  NO
P1-001 priority:              UNCHANGED
```

См. также:

- [`../ENVIRONMENT_MANIFEST.md`](../ENVIRONMENT_MANIFEST.md) — current profile facts;
- [`../MENTAURY_P0_IMPLEMENTATION_PLAN.md`](../MENTAURY_P0_IMPLEMENTATION_PLAN.md) — `Implementation Profile ≠ Canon`;
- [`NATIVE_KERNEL_RESEARCH_INPUT_NOTES_V0.1.md`](NATIVE_KERNEL_RESEARCH_INPUT_NOTES_V0.1.md) — external research input boundary;
- [`MENTAURY_IDENTITY_CONTINUITY_AND_RELATIONAL_ARCHITECTURE_NOTES.md`](MENTAURY_IDENTITY_CONTINUITY_AND_RELATIONAL_ARCHITECTURE_NOTES.md) — relationships research (docs-only).
