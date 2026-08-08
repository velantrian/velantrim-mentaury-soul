"""Offline structural validation for P0-001…P0-015 manifest presence.

Это presence-check обязательных путей, а не доказательство корректности
поведения. Поведенческие инварианты остаются зоной pytest / CI.
"""
from __future__ import annotations
import pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parents[1]
REQUIRED_PATHS = (
    "pyproject.toml", "requirements-dev.lock",
    "docs/ENVIRONMENT_MANIFEST.md", "docs/P0_008_TRANSACTIONAL_CONCURRENCY.md",
    "docs/P0_009_R0_INTEGRITY.md", "src/mentaury/__init__.py",
    "src/mentaury/py.typed", "src/mentaury/contracts/primitives.py",
    "src/mentaury/contracts/envelopes.py", "src/mentaury/contracts/canonical_json.py",
    "src/mentaury/storage/__init__.py", "src/mentaury/storage/sqlite_store.py",
    "src/mentaury/storage/atomic_batch.py", "src/mentaury/storage/idempotency.py",
    "src/mentaury/storage/concurrency.py", "src/mentaury/storage/stream_meta.py",
    "src/mentaury/storage/budget.py", "src/mentaury/storage/sealing.py",
    "src/mentaury/storage/integrity.py", "src/mentaury/storage/redaction.py",
    "src/mentaury/validation/__init__.py",
    "src/mentaury/validation/issues.py", "src/mentaury/validation/specs.py",
    "src/mentaury/validation/validator.py", "src/mentaury/validation/registry.py",
    # P0-013 R1 Replay
    "src/mentaury/replay/__init__.py",
    "src/mentaury/replay/contracts.py",
    "src/mentaury/replay/engine.py",
    # P0-014 Minimal Belief Lifecycle
    "src/mentaury/beliefs/__init__.py",
    "src/mentaury/beliefs/contracts.py",
    "src/mentaury/beliefs/lifecycle.py",
    "src/mentaury/beliefs/reducer.py",
    "src/mentaury/beliefs/schemas.py",
    # P0-015 Deterministic Evidence Gate
    "src/mentaury/beliefs/evidence_gate.py",
    "src/mentaury/beliefs/gated_reducer.py",
    "src/mentaury/evidence/__init__.py",
    "src/mentaury/evidence/contracts.py",
    "src/mentaury/evidence/gate.py",
    "src/mentaury/evidence/schemas.py",
    "tests/test_skeleton.py", "tests/test_envelopes.py",
    "tests/test_payload_cycle_protection.py", "tests/test_canonical_json.py",
    "tests/test_sqlite_store.py", "tests/test_schema_validation.py",
    "tests/test_one_of_semantics.py", "tests/test_resource_budgets.py",
    "tests/test_atomic_batch.py", "tests/test_idempotency.py",
    "tests/test_concurrency.py", "tests/test_integrity.py",
    "tests/test_redaction.py",
    "tests/test_r1_replay.py",
    "tests/test_belief_lifecycle.py",
    "tests/test_evidence_gate.py",
    "tests/fixtures/canonical_json_v1_vectors.json",
)
FORBIDDEN_RUNTIME_MODULES = (
    "identity_engine.py", "relationship_runtime.py", "character_engine.py",
    "curiosity_controller.py", "exo_cortex_runtime.py",
)


def missing_required_paths(
    root: pathlib.Path = ROOT,
    required_paths: tuple[str, ...] = REQUIRED_PATHS,
) -> list[str]:
    return [path for path in required_paths if not (root / path).exists()]


def forbidden_runtime_modules(root: pathlib.Path = ROOT) -> list[str]:
    src_root = root / "src"
    if not src_root.exists():
        return []
    return sorted(
        {
            path.name
            for path in src_root.rglob("*.py")
            if path.name in FORBIDDEN_RUNTIME_MODULES
        }
    )


def main() -> int:
    if sys.version_info[:2] != (3, 13):
        print(f"unsupported Python: {sys.version.split()[0]} (expected 3.13.x)")
        return 1
    missing = missing_required_paths()
    if missing:
        print("missing required paths:")
        for path in missing:
            print(f"- {path}")
        return 1
    found = forbidden_runtime_modules()
    if found:
        print("forbidden domain runtime modules found:")
        for name in found:
            print(f"- {name}")
        return 1
    print("Mentaury P0-001…P0-015 structural manifest validation: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
