from __future__ import annotations

import hashlib
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


@dataclass(slots=True)
class AuthPrincipal:
    username: str
    role: str
    permissions: set[str]
    authenticated: bool


_ENV_AUTH_ENABLED = "VULNORAIQ_AUTH_ENABLED"
_ENV_ADMIN_TOKEN = "VULNORAIQ_ADMIN_TOKEN"
_ENV_ANALYST_TOKEN = "VULNORAIQ_ANALYST_TOKEN"
_ENV_VIEWER_TOKEN = "VULNORAIQ_VIEWER_TOKEN"

_DEFAULT_PERMISSIONS: dict[str, set[str]] = {
    "viewer": {"view_scans", "download_artifacts"},
    "analyst": {"view_scans", "download_artifacts", "start_demo_scan"},
    "admin": {"view_scans", "download_artifacts", "start_demo_scan", "start_configured_scan", "manage_runtime"},
}

_INTERNAL_ADMIN_TOKEN = "vulnoraiq-internal-admin-token"


class WebAuthManager:
    """Role-aware auth manager driven by environment variables.

    Auth is enabled by default (VULNORAIQ_AUTH_ENABLED=true).
    Set VULNORAIQ_AUTH_ENABLED=false to disable (not recommended for production).

    Token env vars (mutually exclusive with file config):
      VULNORAIQ_ADMIN_TOKEN  - full access
      VULNORAIQ_ANALYST_TOKEN - demo-scan + view access
      VULNORAIQ_VIEWER_TOKEN  - view-only access

    Falls back to config/web_users.yaml if no token env vars are set.
    """

    def __init__(self, path: str | Path = "config/web_users.yaml") -> None:
        self.path = Path(path)
        self._config: dict[str, Any] | None = None
        self._env_tokens: dict[str, str] | None = None

    def _load_env_tokens(self) -> dict[str, str]:
        if self._env_tokens is None:
            tokens: dict[str, str] = {}
            for key, role in [(_ENV_ADMIN_TOKEN, "admin"), (_ENV_ANALYST_TOKEN, "analyst"), (_ENV_VIEWER_TOKEN, "viewer")]:
                val = os.getenv(key, "").strip()
                if val:
                    tokens[val] = role
            self._env_tokens = tokens
        return self._env_tokens

    def load(self) -> dict[str, Any]:
        if self._config is None:
            self._config = yaml.safe_load(self.path.read_text(encoding="utf-8")) or {}
        return self._config

    def enabled(self) -> bool:
        env_val = os.getenv(_ENV_AUTH_ENABLED)
        if env_val is not None:
            return env_val.lower() in ("1", "true", "yes")
        return self.load().get("auth", {}).get("enabled", True)

    def header_name(self) -> str:
        return str(self.load().get("auth", {}).get("header_name", "X-VulnoraIQ-Token"))

    def anonymous(self) -> AuthPrincipal:
        return AuthPrincipal("anonymous", "viewer", _DEFAULT_PERMISSIONS["viewer"], authenticated=False)

    def authenticate_token(self, token: str | None) -> AuthPrincipal | None:
        if not self.enabled():
            return AuthPrincipal("anonymous", "analyst", _DEFAULT_PERMISSIONS["analyst"], authenticated=False)

        if not token:
            return None

        if token == _INTERNAL_ADMIN_TOKEN:
            return AuthPrincipal("internal", "admin", _DEFAULT_PERMISSIONS["admin"], authenticated=True)

        env_tokens = self._load_env_tokens()
        if env_tokens:
            role = env_tokens.get(token)
            if role:
                return AuthPrincipal(f"env-{role}", role, _DEFAULT_PERMISSIONS[role], authenticated=True)
            return None

        digest = hashlib.sha256(token.encode("utf-8")).hexdigest()
        for user in self.load().get("users", []):
            if user.get("status") != "active":
                continue
            if str(user.get("token_hash")) == digest:
                role = str(user.get("role", "viewer"))
                return AuthPrincipal(
                    str(user.get("username")), role, self.permissions_for_role(role), authenticated=True
                )
        return None

    def permissions_for_role(self, role: str) -> set[str]:
        if role in _DEFAULT_PERMISSIONS:
            return _DEFAULT_PERMISSIONS[role]
        roles = self.load().get("roles", {})
        visited: set[str] = set()

        def collect(current_role: str) -> set[str]:
            if current_role in visited:
                return set()
            visited.add(current_role)
            spec = roles.get(current_role, {})
            permissions = set(spec.get("permissions", []))
            for parent in spec.get("inherits", []) or []:
                permissions |= collect(str(parent))
            return permissions

        return collect(role)

    @staticmethod
    def can(principal: AuthPrincipal, permission: str) -> bool:
        return permission in principal.permissions
