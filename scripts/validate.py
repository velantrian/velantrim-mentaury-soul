"""Offline structural validation for P0-002 envelope contracts."""

from __future__ import annotations

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
REQUIRED_PATHS = (
    "pyproject.toml",
    "requirements-dev.lock",
    "docs/ENVIRONMENT_MANIFEST.md",
    "docs/P0_002_ENVELOPE_CONTRACTS.md",
    "src/mentaury/__init__.py",
    "src/mentaury/py.typed",
    "src/mentaury/contracts/primitives.py",
    "src/mentaury/contracts/envelopes.py",
    "tests/test_skeleton.py",
    "tests/test_envelopes.py",
)
FORBIDDEN_RUNTIME_MODULES = (
    "identity_engine.py",
    "relationship_runtime.py",
    "character_engine.py",
    "curiosity_controller.py",
    "exo_cortex_runtime.py",
    "event_store.py",
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
        print("forbidden runtime modules found:")
        for name in found_forbidden:
            print(f"- {name}")
        return 1

    print("P0-002 envelope contract validation: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
