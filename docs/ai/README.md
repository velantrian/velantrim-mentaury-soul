# 🤖 Mentaury Soul — AI Agent Entry Point

This is the compact orientation layer for AI coding agents, reviewers and maintainers. Its purpose is to reduce blind repository-wide scanning while preserving architectural distinctions.

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
10. only affected research contracts, source, tests, PRs and CI

## Source-of-truth hierarchy

```text
live merged GitHub code
→ executable tests and exact CI
→ CURRENT_STATUS + governance
→ accepted/frozen owning contracts
→ README / SYSTEM_OVERVIEW
→ docs/ai navigation
→ PR/issues/research proposals
→ Notion rationale/history
```

## Project identity

Mentaury Soul is a substrate-neutral research architecture for evolving digital individuality in which provenance, claims, beliefs, relations, identity continuity and character remain distinct and governed.

```text
tool output != belief
claim != belief
relation != truth
character != evidence
continuity != identity proof
contract freeze != runtime authority
implementation != action authority
```

## Context-budget route

```text
AI entry
→ project manifest
→ current status
→ affected component
→ owning contract
→ focused code/tests
→ wider search only when evidence demands it
```

## Documentation maintenance

Use `DOCUMENTATION_STANDARD.md` and `project_manifest.json`. Every change is classified as `STRUCTURAL_CHANGE`, `STATE_CHANGE` or `EVIDENCE_ONLY`. Structural changes require reviewing all maintained landing surfaces and updating only the representations whose meaning became stale.
