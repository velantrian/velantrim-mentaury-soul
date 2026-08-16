#!/usr/bin/env python3
"""Trusted-base research scope and anti-self-authorization guard.

The policy used to judge BASE..HEAD is loaded from the trusted base revision,
never from the PR head. HEAD policy may narrow scope but cannot expand authority
or weaken immutable forbidden roots. This is a structural guard, not a semantic
security proof.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

IMMUTABLE_FORBIDDEN_ROOTS = (
    "src/",
    "deploy/",
    "infra/",
    ".github/workflows/deploy",
    ".github/workflows/release",
)


def load_policy(path: Path) -> dict[str, Any]:
    try:
        policy = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"SCOPE-INVALID-POLICY: {exc}") from exc
    if policy.get("policy_state") != "RESEARCH_ONLY":
        raise ValueError("SCOPE-INVALID-POLICY: policy_state must be RESEARCH_ONLY")
    ceiling = policy.get("authority_ceiling")
    if not isinstance(ceiling, dict) or any(value is not False for value in ceiling.values()):
        raise ValueError("SCOPE-AUTHORITY-CEILING: all authority ceiling flags must be false")
    for key in ("allowed_prefixes", "always_forbidden_prefixes", "authority_artifact_prefixes", "implementation_prefixes"):
        if not isinstance(policy.get(key), list):
            raise ValueError(f"SCOPE-INVALID-POLICY: {key} must be a list")
    return policy


def changed_paths(base: str, head: str) -> list[str]:
    result = subprocess.run(
        ["git", "diff", "--name-only", "--diff-filter=ACMR", base, head, "--"],
        check=False, text=True, capture_output=True,
    )
    if result.returncode != 0:
        raise ValueError(f"SCOPE-GIT-DIFF: {result.stderr.strip()}")
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def matches_prefix(path: str, prefixes: list[str] | tuple[str, ...]) -> bool:
    return any(path == prefix or path.startswith(prefix) for prefix in prefixes)


def prefix_is_covered_by(prefix: str, covering_prefixes: list[str] | tuple[str, ...]) -> bool:
    """True when prefix is equal to or narrower than a covering prefix."""
    return any(prefix == base or prefix.startswith(base) for base in covering_prefixes)


def validate_policy_transition(base: dict[str, Any], head: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    base_allowed = base["allowed_prefixes"]
    head_allowed = head["allowed_prefixes"]
    for prefix in head_allowed:
        if not prefix_is_covered_by(prefix, base_allowed):
            errors.append(f"SCOPE-HEAD-POLICY-EXPANDS-ALLOWLIST: {prefix}")
    for root in IMMUTABLE_FORBIDDEN_ROOTS:
        if not matches_prefix(root, head["always_forbidden_prefixes"]):
            errors.append(f"SCOPE-HEAD-POLICY-REMOVES-IMMUTABLE-FORBIDDEN-ROOT: {root}")
    for key, base_value in base["authority_ceiling"].items():
        if base_value is False and head["authority_ceiling"].get(key) is not False:
            errors.append(f"SCOPE-HEAD-POLICY-EXPANDS-AUTHORITY: {key}")
    return errors


def validate(base_policy: dict[str, Any], paths: list[str], head_policy: dict[str, Any] | None = None) -> list[str]:
    errors: list[str] = []
    allowed = base_policy["allowed_prefixes"]
    forbidden = tuple(set(base_policy["always_forbidden_prefixes"]) | set(IMMUTABLE_FORBIDDEN_ROOTS))
    authority = base_policy["authority_artifact_prefixes"]
    implementation = base_policy["implementation_prefixes"]

    if not paths:
        errors.append("SCOPE-EMPTY-DIFF: no changed files to validate")
        return errors

    authority_changed = any(matches_prefix(path, authority) for path in paths)
    implementation_changed = any(matches_prefix(path, implementation) for path in paths)
    workflow_changed = any(path.startswith(".github/workflows/") for path in paths)

    for path in paths:
        if matches_prefix(path, forbidden):
            errors.append(f"SCOPE-FORBIDDEN-PATH: {path}")
        elif not matches_prefix(path, allowed):
            errors.append(f"SCOPE-NOT-ALLOWED-IN-RESEARCH-ONLY: {path}")

    if authority_changed and implementation_changed:
        errors.append("SCOPE-ANTI-SELF-AUTHORIZATION: authority artifact and implementation path changed in one PR")
    if authority_changed and workflow_changed:
        errors.append("SCOPE-AUTHORITY-WORKFLOW-COCHANGE: authority artifact and workflow changed in one PR")
    if head_policy is not None:
        errors.extend(validate_policy_transition(base_policy, head_policy))
    return sorted(set(errors))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", required=True)
    parser.add_argument("--head", required=True)
    parser.add_argument("--base-policy", type=Path, required=True)
    parser.add_argument("--head-policy", type=Path, required=True)
    args = parser.parse_args()
    try:
        base_policy = load_policy(args.base_policy)
        head_policy = load_policy(args.head_policy)
        errors = validate(base_policy, changed_paths(args.base, args.head), head_policy)
    except ValueError as exc:
        print(exc, file=sys.stderr)
        return 2
    if errors:
        print("PR SCOPE GUARD FAIL", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print("PR SCOPE GUARD PASS: trusted-base research boundary preserved")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
