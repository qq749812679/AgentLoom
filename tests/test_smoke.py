import importlib


def test_import_core_modules_importable() -> None:
    # Top-level package
    assert importlib.import_module("mscen") is not None

    # Common submodules (exist in repo)
    assert importlib.import_module("mscen.agents.orchestrator") is not None
    assert importlib.import_module("mscen.connectors.factory") is not None
    assert importlib.import_module("mscen.ui.wizard") is not None 