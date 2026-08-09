"""Regression tests for order-independent beliefs/evidence imports.

The former cycle was:

``evidence.contracts``
→ ``mentaury.beliefs.contracts``
→ package ``beliefs.__init__``
→ ``beliefs.evidence_gate``
→ partially initialized ``mentaury.evidence``.

Every import-order check runs in a fresh interpreter so an already populated
``sys.modules`` cannot mask the failure.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SRC = str(ROOT / "src")


def _run_fresh(code: str) -> subprocess.CompletedProcess[str]:
    env = dict(os.environ)
    existing_pythonpath = env.get("PYTHONPATH")
    env["PYTHONPATH"] = (
        SRC
        if not existing_pythonpath
        else os.pathsep.join((SRC, existing_pythonpath))
    )
    return subprocess.run(
        [sys.executable, "-c", code],
        check=False,
        capture_output=True,
        text=True,
        env=env,
        cwd=str(ROOT),
        timeout=30,
    )


@pytest.mark.parametrize(
    "code",
    [
        "import mentaury.evidence",
        "import mentaury.beliefs",
        "import mentaury.beliefs; import mentaury.evidence",
        "import mentaury.evidence; import mentaury.beliefs",
        "import mentaury.evidence.contracts",
        "import mentaury.beliefs.contracts",
        "from mentaury.evidence import EvidenceGate",
        "from mentaury.beliefs import BeliefLifecycle",
    ],
)
def test_fresh_interpreter_imports_do_not_depend_on_order(code: str) -> None:
    result = _run_fresh(code)
    assert result.returncode == 0, result.stderr


def test_epistemic_enum_identity_is_shared_across_public_modules() -> None:
    code = """
from mentaury.epistemic_types import ClaimType as A
from mentaury.beliefs.contracts import ClaimType as B
from mentaury.evidence.contracts import ClaimType as C
from mentaury.beliefs import ClaimType as D
assert A is B is C is D
assert A.__module__ == "mentaury.epistemic_types"

from mentaury.epistemic_types import EvidenceSide as W
from mentaury.beliefs.contracts import EvidenceSide as X
from mentaury.evidence.contracts import EvidenceSide as Y
from mentaury.beliefs import EvidenceSide as Z
assert W is X is Y is Z
assert W.__module__ == "mentaury.epistemic_types"
print("ok")
"""
    result = _run_fresh(code)
    assert result.returncode == 0, result.stderr
    assert result.stdout.strip() == "ok"
