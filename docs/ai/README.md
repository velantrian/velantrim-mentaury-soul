# 🤖 Mentaury Soul — AI Agent Entry Point

This directory is the compact orientation layer for AI coding agents, reviewers and maintainers.

Its purpose is to reduce blind repository-wide scanning while preserving architectural distinctions.

## Required reading order

1. `../../README.md`
2. `../../SYSTEM_OVERVIEW.md`
3. `../../AGENTS.md`
4. `project_manifest.json`
5. `../CURRENT_STATUS.md`
6. `../GOVERNANCE.md`
7. `COMPONENT_MAP.md`
8. `KNOWN_RISKS.md`
9. `REVIEW_GUIDE.md`
10. affected research contract/source/tests/PR/CI only

## Source-of-truth hierarchy

```text
live merged GitHub code
→ executable tests and exact CI
→ CURRENT_STATUS + governance
→ accepted/frozen owning contracts
→ README / SYSTEM_OVERVIEW orientation
→ docs/ai navigation layer
→ PR/issues/research proposals
→ Notion rationale/history
```

Notion may be newer as presentation or synchronization history, but implemented technical truth must be reproducible from GitHub.

## Project identity in one sentence

Mentaury Soul is a substrate-neutral research architecture for evolving digital individuality in which provenance, claims, beliefs, relations, identity continuity and character remain distinct and governed.

## Non-collapse rules

```text
tool output       != belief
memory tier       != identity zone
claim             != belief
relation          != truth
character         != evidence
continuity        != metaphysical identity proof
contract freeze   != runtime authority
implementation    != action authority
```

## Context-budget route

```text
AI entry point
→ project manifest
→ current status
→ affected component
→ owning contract
→ focused code/tests
→ wider repository search only when evidence demands it
```

Do not load all research documents by default.

## Documentation maintenance

The repository follows **Velantrim Documentation Standard v1** in `DOCUMENTATION_STANDARD.md`.

Every change is classified as `STRUCTURAL_CHANGE`, `STATE_CHANGE` or `EVIDENCE_ONLY`.

A structural change requires reviewing every maintained landing surface and updating only the surfaces whose meaning became stale. Visual artifacts have separate semantics; they are not decorative duplicates.

Machine-readable navigation and maintenance rules live in `project_manifest.json`.

Run the deterministic guard before proposing documentation closure:

```bash
python scripts/check_documentation_impact.py --validate-repo
```
