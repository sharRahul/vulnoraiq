from __future__ import annotations

import pytest

from scripts import desktop_launch
from webui.auth import WebAuthManager


def test_local_admin_auth_mode_resolves_to_local_admin(monkeypatch, tmp_path) -> None:
    monkeypatch.setenv("VULNORAIQ_AUTH_MODE", "local_admin")
    monkeypatch.delenv("VULNORAIQ_AUTH_ENABLED", raising=False)
    monkeypatch.delenv("VULNORAIQ_ENV", raising=False)

    manager = WebAuthManager(tmp_path / "missing_web_users.yaml")
    principal = manager.authenticate_token(None)

    assert manager.auth_mode() == "local_admin"
    assert principal is not None
    assert principal.username == "local-admin"
    assert principal.role == "admin"
    assert principal.authenticated is False
    assert manager.can(principal, "manage_runtime")
    assert manager.can(principal, "start_configured_scan")


def test_auth_enabled_false_is_legacy_alias_for_local_admin(monkeypatch, tmp_path) -> None:
    monkeypatch.delenv("VULNORAIQ_AUTH_MODE", raising=False)
    monkeypatch.setenv("VULNORAIQ_AUTH_ENABLED", "false")
    monkeypatch.delenv("VULNORAIQ_ENV", raising=False)

    manager = WebAuthManager(tmp_path / "missing_web_users.yaml")

    assert manager.auth_mode() == "local_admin"
    assert manager.authenticate_token(None) is not None


def test_desktop_launcher_defaults_to_single_user_admin(monkeypatch, tmp_path) -> None:
    monkeypatch.setattr(desktop_launch, "ROOT", tmp_path)
    monkeypatch.delenv("VULNORAIQ_AUTH_MODE", raising=False)
    monkeypatch.delenv("VULNORAIQ_AUTH_ENABLED", raising=False)

    env = desktop_launch._prepare_desktop_environment()

    assert env["VULNORAIQ_RUN_MODE"] == "desktop"
    assert env["VULNORAIQ_AUTH_MODE"] == "local_admin"
    assert "VULNORAIQ_AUTH_ENABLED" not in env
    assert env["VULNORAIQ_HOST"] == "127.0.0.1"
    assert env["VULNORAIQ_AGENT_LAB_ROOT"] == str(tmp_path / "agent-lab")


def test_local_admin_mode_requires_loopback_host(monkeypatch, tmp_path) -> None:
    monkeypatch.setenv("VULNORAIQ_AUTH_MODE", "local_admin")
    monkeypatch.delenv("VULNORAIQ_ENV", raising=False)
    monkeypatch.delenv("VULNORAIQ_LOCAL_ADMIN_BIND_OK", raising=False)

    manager = WebAuthManager(tmp_path / "missing_web_users.yaml")

    manager.validate_runtime_auth("127.0.0.1")
    manager.validate_runtime_auth("localhost")
    with pytest.raises(RuntimeError, match="loopback"):
        manager.validate_runtime_auth("0.0.0.0")


def test_local_admin_mode_is_rejected_in_production(monkeypatch, tmp_path) -> None:
    monkeypatch.setenv("VULNORAIQ_AUTH_MODE", "local_admin")
    monkeypatch.setenv("VULNORAIQ_ENV", "production")

    manager = WebAuthManager(tmp_path / "missing_web_users.yaml")

    with pytest.raises(RuntimeError, match="not allowed"):
        manager.validate_runtime_auth("127.0.0.1")


def test_docker_lab_can_explicitly_allow_container_bind(monkeypatch, tmp_path) -> None:
    monkeypatch.setenv("VULNORAIQ_AUTH_MODE", "local_admin")
    monkeypatch.setenv("VULNORAIQ_RUN_MODE", "docker_lab")
    monkeypatch.setenv("VULNORAIQ_LOCAL_ADMIN_BIND_OK", "true")
    monkeypatch.delenv("VULNORAIQ_ENV", raising=False)

    manager = WebAuthManager(tmp_path / "missing_web_users.yaml")

    manager.validate_runtime_auth("0.0.0.0")
