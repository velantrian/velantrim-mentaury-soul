from __future__ import annotations

import importlib

import mentaury


def test_root_package_exposes_only_version_metadata_without_runtime() -> None:
    assert mentaury.__version__ == "0.0.0"
    assert not hasattr(mentaury, "SKELETON_STATUS")
    assert not hasattr(mentaury, "IMPLEMENTATION_STATUS")
    assert set(mentaury.__all__) == {"__version__"}


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
