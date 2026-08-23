# Documentation Audit — 2026-08-23

**Scope:** accuracy/currency (точность и актуальность) and completeness/structure (полнота и структура) of this repository's documentation (`*.md`, README, `docs/`), assessed against a snapshot of the default branch on 2026-08-23. This is a documentation snapshot audit, not a code-quality or security review, and does not cover unmerged branches.

## Overall health assessment

**Fair.** The documentation's core trunk (README → SYSTEM_OVERVIEW → AGENTS.md → CURRENT_STATUS.md → GOVERNANCE.md → V1_FINAL_STATUS.md) is unusually disciplined for a repo this size: internally consistent, zero broken relative markdown links found across all 106 files, and every path/script/config it names actually exists. However, there is a clear, systemic regression at the most recent release boundary: the 2026-08-22 V1 completion (EPR-v0.1 routing + CBP-v0.1 claim→belief binding going from "not implemented" to "implemented bounded") was propagated into the primary truth surfaces (README, SYSTEM_OVERVIEW, CURRENT_STATUS.md, V1_FINAL_STATUS.md, project_state.json) but **not** into at least five secondary documents the project's own navigation explicitly directs readers/agents to — each still asserts the opposite. Combined with ~28% of the doc set being unreachable by link from anywhere else, the project clearly has the process to fix this (it performed this exact reconciliation before, per NON_PROJECTION_STATUS_RECONCILIATION_2026_08_12.md) but didn't re-run it for the latest milestone.

## Findings

1. **docs/research/RESEARCH_INDEX.md** | accuracy | high | Still states Phase 4/EPR and claim→belief binding are unimplemented, contradicting current-truth docs. | `Phase 4 implementation: NOT_STARTED` / `Claim→belief binding: NOT_IMPLEMENTED`, vs. docs/CURRENT_STATUS.md: `CLAIM_TO_BELIEF_BINDING_IMPLEMENTED_BOUNDED`.

2. **docs/research/POST_P0_ROADMAP_V0.1.md** | accuracy | high | The "ADOPTED ROADMAP" doc (linked from README's Authoritative Documents list) carries the identical stale claim: `Phase 4 implementation: NOT_STARTED`.

3. **docs/ai/COMPONENT_MAP.md** | accuracy | high | Step 6 of AGENTS.md's mandatory AI-agent reading order says EPR-v0.1 and claim→belief binding are not implemented — an agent following the required route could try to re-implement already-shipped work.

4. **docs/ai/AUDIT_AND_FUTURE_WORK.md** | accuracy | high | The audit ledger (step 5 of the AI reading order) is dated "Last live reconciliation: 2026-08-17" — five days before V1 shipped — and still lists EPR as unimplemented with an open audit item asking whether it's even needed.

5. **docs/MENTAURY_QUICK_REFERENCE.md** | accuracy | high | A fifth document repeats the same stale claim in its capability table. Notably `docs/state/project_state.json`, dated the same day (2026-08-22), *was* correctly updated — showing this is a doc-sweep miss, not a ground-truth ambiguity.

6. **docs/P0_002_ENVELOPE_CONTRACTS.md** (representative of 30 files) | completeness | high | 30 of 106 markdown files (28%) have zero inbound links from any other markdown file in the repo — the entire P0 milestone detail-doc set (14 files) is never hyperlinked anywhere, plus 14 files under docs/research/ and 2 more elsewhere.

7. **docs/research/RESEARCH_INDEX.md** | completeness | high | The index's own "Document registry" omits 21 of the 56 files in docs/research/ (38%), including the actual CBP-v0.1 contract file and the EPR Owner-GO decision doc.

8. **docs/GOVERNANCE.md** | accuracy | medium | The Tier-A "protected/high-risk paths" list omits `src/mentaury/claim_belief_binding/**` and `src/mentaury/epistemic_change/**` — the two source packages implementing the V1-critical primitives — even though sibling implemented packages are all listed.

9. **docs/P0_010_ATOMIC_SAME_STREAM_REDACTION.md** | accuracy | medium | Status header still reads "CODE + TESTS ON BRANCH · NOT YET MERGED", contradicted by CURRENT_STATUS.md's "P0-001…P0-015_IMPLEMENTED_IN_MAIN" and by sibling docs that build on top of it.

10. **docs/V1_RELEASE_CANDIDATE_STATUS.md** | structure | medium | A Stage-4/5 "release candidate" doc (v1.0.0rc1) remains live alongside the completed docs/V1_FINAL_STATUS.md (Stage 5/5, v1.0.0), both dated 2026-08-22, no supersession marker; its content is now factually false ("there is no LICENSE file" — but LICENSE exists).

11. **docs/** (no index file) | structure | medium | The 34 markdown files directly under docs/ have no dedicated index, unlike docs/ai/ (README.md) and docs/research/ (RESEARCH_INDEX.md); navigation relies on partial, scattered lists.

12. **docs/research/POST_P0_ROADMAP_V0.1.md** | structure | low | Version-suffix naming is split between dot form (_V0.1) and underscore form (_V0_1) for the same kind of document, with no evident cutover rule.

13. **docs/PROJECT_HISTORY.md** | structure | low | Several core docs are written fully or partly in Russian (mixed with English field labels) alongside fully English navigation docs, with no stated language policy anywhere.

14. **docs/P0_005_STRUCTURAL_SCHEMA_VALIDATION.md** (representative of P0_003–P0_008) | structure | low | Inconsistent "Status:" field convention within the same doc family — some files put the milestone code where a status word belongs, vs siblings that use actual status words.

---
*Generated by an automated documentation audit (Claude Code).*
