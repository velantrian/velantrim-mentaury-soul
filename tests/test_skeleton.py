from __future__ import annotations

import importlib

import mentaury


def test_package_imports_without_side_effect_runtime() -> None:
    assert mentaury.__version__ == "0.0.0"
    assert mentaury.SKELETON_STATUS == "P0-001_NEUTRAL_SKELETON"
    assert (
        mentaury.IMPLEMENTATION_STATUS
        == "P0-009_FULL_R0_INTEGRITY"
    )


def test_reserved_namespaces_are_importable() -> None:
    for module_name in (
        "mentaury.core",
        "mentaury.contracts",
        "mentaury.storage",
        "mentaury.validation",
    ):
        assert importlib.import_module(module_name) is not None


def test_domain_runtime_is_not_exposed() -> None:
    forbidden = {
        "identity_engine",
        "relationship_runtime",
        "character_engine",
        "curiosity_controller",
        "exo_cortex_runtime",
    }
    assert forbidden.isdisjoint(set(dir(mentaury)))
