<p><em>English mirror of the <a href="../../research/NATIVE_KERNEL_RESEARCH_INPUT_NOTES_V0.1.md">Russian source</a>; this mirror is not independent authority.</em></p>

# 🧬 Native Kernel as an external research input — notes v0.1

```text
Status:                        DOCS_ONLY · NON_CANONICAL · RESEARCH_NOTES · DRAFT
Version:                       0.1
Date:                          2026-08-07
Source:                        preserved from claude/audit-relationships-6866cw@a00001bcf7244dbb9d5dbbf162a830eafe329699
Scope:                         Cross-project research input · Replay · Redaction · Evidence Gate · Relations
Runtime authority:             NONE
Truth authority:               NONE
Capability authority:          NONE
Canon modification authority:  NONE
P0 scope authority:            NONE
Direct M3 write:               FORBIDDEN
Skeleton readiness:            NOT_AUTHORIZED
NO RUNTIME AUTHORITY:          CONFIRMED
NO TRUTH AUTHORITY:            CONFIRMED
NO CAPABILITY AUTHORITY:       CONFIRMED
NO DIRECT M3 WRITE:            CONFIRMED
```

> This document records how Mentaury may treat the
> `velantrim-native-kernel` research track as an external source of ideas. It does not create
> runtime, extend P0, change the frozen Canon v0.1, or turn Native Kernel
> proposals into approved Mentaury mechanisms. It conforms to the boundaries of
> [`docs/VELANTRIM_ECOSYSTEM.md`](../../VELANTRIM_ECOSYSTEM.md) and the external
> Native Kernel document
> [`INTEGRATION_BOUNDARIES.md`](https://github.com/velantrian/velantrim-native-kernel/blob/main/docs/INTEGRATION_BOUNDARIES.md)
> (the “Native Kernel and Mentaury Soul” section).

---

## 1. 🎯 Purpose

A cross-repository audit (see [`docs/VELANTRIM_ECOSYSTEM.md`](../../VELANTRIM_ECOSYSTEM.md),
the Native Kernel role and mandatory boundaries) showed that mechanisms already
implemented and tested in Mentaury structurally intersect with abstract contracts
that Native Kernel only proposes:

| Mentaury (implemented and tested) | Native Kernel (proposed / contract-level, runtime `NOT_STARTED`) |
|---|---|
| `P0-013` — deterministic R1 replay: `state_hash(full replay) == state_hash(snapshot + tail)` | [`ADR-0002`](https://github.com/velantrian/velantrim-native-kernel/blob/main/docs/adr/0002-state-checkpoints-are-disposable.md) (disposable State Checkpoints) and [`ADR-0004`](https://github.com/velantrian/velantrim-native-kernel/blob/main/docs/adr/0004-rebuild-from-authoritative-history.md) (rebuild from authoritative history) |
| `P0-010` — governed same-stream redaction with a byte-for-byte immutable event row | future “redaction-aware history” primitive (see the external [`INTEGRATION_BOUNDARIES.md`](https://github.com/velantrian/velantrim-native-kernel/blob/main/docs/INTEGRATION_BOUNDARIES.md); a separate ADR in Native Kernel has not yet been accepted as implementation) |
| `P0-015` — Deterministic Evidence Gate: evidence set → deterministic receipt → belief status | Receipts and the proposed Audit Curiosity profile (external [`INTEGRATION_BOUNDARIES.md`](https://github.com/velantrian/velantrim-native-kernel/blob/main/docs/INTEGRATION_BOUNDARIES.md)) |
| Relationships / commitments as first-class objects (`MENTAURY_IDENTITY_CONTINUITY_AND_RELATIONAL_ARCHITECTURE_NOTES.md`) | [`ADR-0006`](https://github.com/velantrian/velantrim-native-kernel/blob/main/docs/adr/0006-causal-links-are-relations.md) — causal/typed relations as relations, separate from lineage (`ACCEPTED` contract direction; implementation `NOT_STARTED`) |

The purpose of this note is to record how Mentaury may use Native Kernel as a
research input, symmetrically to how Native Kernel describes an independent
boundary with Mentaury in
[`INTEGRATION_BOUNDARIES.md`](https://github.com/velantrian/velantrim-native-kernel/blob/main/docs/INTEGRATION_BOUNDARIES.md)
(“Native Kernel and Mentaury Soul”). This does **not** assert the existence of
a separate Native Kernel ADR titled “Mentaury as external research input” and
it does **not** refer to a nonexistent local `INTEGRATION_BOUNDARIES.md` inside
Mentaury.

---

## 2. 🔍 What This Does NOT Mean

```text
Native Kernel ADR-0006 exists
≠ Mentaury has acquired a typed-relation storage schema

Native Kernel proposes redaction-aware history
≠ P0-010 is rewritten for a foreign contract

Problem overlap
≠ shared runtime
≠ shared package
≠ shared schema
≠ authority transfer
≠ automatic M2/M3 promotion
≠ Native Kernel integration authorized
```

As in the main ecosystem document: Native Kernel events, projections, or
Receipts do not automatically become Mentaury M2/M3. This note does not cancel
or weaken any boundary from [`docs/VELANTRIM_ECOSYSTEM.md`](../../VELANTRIM_ECOSYSTEM.md).

---

## 3. 🧭 How Mentaury May Use Native Kernel as a Research Input

- **Relationships / typed relations.** If Native Kernel [`ADR-0006`](https://github.com/velantrian/velantrim-native-kernel/blob/main/docs/adr/0006-causal-links-are-relations.md) (relations as a separate axis, not mixed with lineage) matures to implementation, it is a possible future candidate for a storage form for Mentaury’s relationship model (`Identity & Relational Research v0.1`). Recognizing an idea ≠ accepting it immediately; a separate research pass and explicit schema review inside Mentaury are required before anything enters even the M2 candidate stage.
- **Redaction-aware history as a more general abstraction.** Mentaury’s P0-010 already solves a narrow version of the problem (one SQLite implementation, one stream). If Native Kernel designs a more general substrate-neutral redaction primitive, it may become a source of ideas for a future revision of P0-010 — not the other way around: Mentaury does not import foreign code, but independently implements any accepted idea.
- **A vocabulary for evidence-gated transitions.** Evidence Gate (P0-015) and Native Kernel Receipts solve structurally the same task (“evidence → deterministic gate → state change”). A shared vocabulary may facilitate future discussion, but it does not create a shared runtime and does not replace Non-Projection review.

## 4. 🚧 Mandatory Conditions Before Any Concrete Step

As in [`docs/VELANTRIM_ECOSYSTEM.md`](../../VELANTRIM_ECOSYSTEM.md), any movement from “the idea seemed similar” to “Mentaury changes something” requires:

```text
external idea (Native Kernel ADR/RFC)
→ separate Mentaury research document analyzing applicability
→ explicit schema and provenance
→ Non-Projection review
→ deterministic tests
→ rollback
→ Receipts
→ operator approval
```

This note itself is not such a lower-level research document — it only records
that the task exists and where to find the relevant Native Kernel ADRs at the
next step.

---

## 5. 📌 Current Decision

```text
Status:            RESEARCH INPUT NOTED · NO ACTION TAKEN
Canon v0.1:        UNCHANGED
P0 scope:          UNCHANGED
Skeleton authority: NOT_AUTHORIZED
Execution milestone: NOT CREATED
P1-001 priority:   UNCHANGED
```

This note is not transferred into `MENTAURY_P0_IMPLEMENTATION_PLAN.md` and does
not create a new P0/P1 task by itself. It serves as a navigation point for a
future decision if and when Native Kernel ADR-0002/0004/0006 move from
contract/docs status to `REPOSITORY_REPRODUCED` / implemented runtime — and even
then a separate Mentaury promotion gate will be required.

### Preservation note

```text
Source branch: claude/audit-relationships-6866cw
Source head:   a00001bcf7244dbb9d5dbbf162a830eafe329699
Unique file:   docs/research/NATIVE_KERNEL_RESEARCH_INPUT_NOTES_V0.1.md
Fixes on preserve:
- local INTEGRATION_BOUNDARIES.md reference → external Native Kernel URL
- stale ADR-0010 mentaury-research-input URL removed (ADR-0010 is now foundational-contract-families)
- complementarity section pointer aligned to current main ecosystem doc
- explicit non-claims: no shared runtime, no authority transfer, no automatic M2/M3
```

See also:
[`docs/VELANTRIM_ECOSYSTEM.md`](../../VELANTRIM_ECOSYSTEM.md) ·
external [`INTEGRATION_BOUNDARIES.md`](https://github.com/velantrian/velantrim-native-kernel/blob/main/docs/INTEGRATION_BOUNDARIES.md) ·
[`ADR-0002`](https://github.com/velantrian/velantrim-native-kernel/blob/main/docs/adr/0002-state-checkpoints-are-disposable.md) ·
[`ADR-0004`](https://github.com/velantrian/velantrim-native-kernel/blob/main/docs/adr/0004-rebuild-from-authoritative-history.md) ·
[`ADR-0006`](https://github.com/velantrian/velantrim-native-kernel/blob/main/docs/adr/0006-causal-links-are-relations.md) ·
[`ADR-0010`](https://github.com/velantrian/velantrim-native-kernel/blob/main/docs/adr/0010-foundational-contract-families.md) (foundational contract families; not a mentaury-import ADR).
