from __future__ import annotations

from pathlib import Path

import yaml

from modules.starter import STARTER_MODULE_METADATA


def _profiles() -> dict:
    data = yaml.safe_load(Path("config/attack_profiles.yaml").read_text(encoding="utf-8")) or {}
    return data.get("profiles", {})


def test_dashboard_catalog_has_required_categories() -> None:
    profiles = _profiles()
    categories = {profile.get("category") for profile in profiles.values()}

    assert "Assessment suites" in categories
    assert "OWASP LLM Top 10 single tests" in categories
    assert "RAG and vector store tests" in categories
    assert "Agentic and tool-use tests" in categories


def test_every_registered_starter_module_has_single_test_profile() -> None:
    profiles = _profiles()
    single_module_profiles = {
        tuple(profile.get("modules", []))[0]
        for name, profile in profiles.items()
        if name.startswith("test_") and len(profile.get("modules", [])) == 1
    }

    assert set(STARTER_MODULE_METADATA) <= single_module_profiles


def test_dashboard_profiles_include_display_metadata() -> None:
    profiles = _profiles()

    for name, profile in profiles.items():
        assert profile.get("category"), f"{name} must have a dashboard category"
        assert profile.get("description"), f"{name} must have a visible description"
        assert profile.get("display_name"), f"{name} must have a display name"
        assert profile.get("modules"), f"{name} must run at least one module"
