"""Regression: beliefs/evidence не зависят от порядка импорта.

Цикл раньше возникал потому, что ``evidence.contracts`` тянул
``mentaury.beliefs.contracts``, package ``beliefs.__init__`` импортировал
``evidence_gate``, а тот — частично инициализированный ``mentaury.evidence``.

Тесты запускают свежий интерпретатор через subprocess, чтобы не маскировать
проблему уже заполненным ``sys.modules``.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SRC = str(ROOT / "src")


def _run_fresh(code: str) -> subprocess.CompletedProcess[str]:
    import os

    env = dict(os.environ)
    env["PYTHONPATH"] = SRC
    return subprocess.run(
        [sys.executable, "-c", code],
        check=False,
        capture_output=True,
        text=True,
        env=env,
        cwd=str(ROOT),
    )


@pytest.mark.parametrize(
    "code",
    [
        "import mentaury.evidence",
        "import mentaury.beliefs",
        "import mentaury.beliefs; import mentaury.evidence",
        "import mentaury.evidence; import mentaury.beliefs",
        "from mentaury.evidence import EvidenceGate",
        "from mentaury.beliefs import BeliefLifecycle",
    ],
)
def test_fresh_interpreter_imports_do_not_depend_on_order(code: str) -> None:
    result = _run_fresh(code)
    assert result.returncode == 0, result.stderr


def test_claim_type_identity_is_shared_across_modules() -> None:
    code = """
from mentaury.epistemic_types import ClaimType as A
from mentaury.beliefs.contracts import ClaimType as B
from mentaury.evidence.contracts import ClaimType as C
assert A is B
assert B is C
from mentaury.epistemic_types import EvidenceSide as X
from mentaury.beliefs.contracts import EvidenceSide as Y
from mentaury.evidence.contracts import EvidenceSide as Z
assert X is Y
assert Y is Z
print("ok")
"""
    result = _run_fresh(code)
    assert result.returncode == 0, result.stderr
    assert "ok" in result.stdout
