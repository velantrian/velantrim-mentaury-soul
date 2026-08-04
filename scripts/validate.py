"""Offline structural validation for the P0-001 repository skeleton."""

from __future__ import annotations

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
REQUIRED_PATHS = (
    "pyproject.toml",
    "requirements-dev.lock",
    "docs/ENVIRONMENT_MANIFEST.md",
    "src/mentaury/__init__.py",
    "src/mentaury/py.typed",
    "tests/test_skeleton.py",
)
FORBIDDEN_RUNTIME_MODULES = (
    "identity_engine.py",
    "relationship_runtime.py",
    "character_engine.py",
    "curiosity_controller.py",
    "exo_cortex_runtime.py",
)


def main() -> int:
    if sys.version_info[:2] != (3, 13):
        print(f"unsupported Python: {sys.version.split()[0]} (expected 3.13.x)")
        return 1

    missing = [path for path in REQUIRED_PATHS if not (ROOT / path).exists()]
    if missing:
        print("missing required paths:")
        for path in missing:
            print(f"- {path}")
        return 1

    found_forbidden = [
        path.name
        for path in (ROOT / "src").rglob("*.py")
        if path.name in FORBIDDEN_RUNTIME_MODULES
    ]
    if found_forbidden:
        print("forbidden domain runtime modules found:")
        for name in found_forbidden:
            print(f"- {name}")
        return 1

    print("P0-001 skeleton validation: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
