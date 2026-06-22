from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml


@dataclass(slots=True)
class AgentRuntimeValidationResult:
    manifest_path: str
    status: str
    tool_count: int = 0
    memory_store_count: int = 0
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


class AgentRuntimeValidator:
    """Validates agent runtime governance metadata before agent profile assessments."""

    def validate(self, manifest_path: str | Path) -> AgentRuntimeValidationResult:
        path = Path(manifest_path)
        if not path.exists():
            return AgentRuntimeValidationResult(
                manifest_path=str(path),
                status="fail",
                errors=[f"Manifest file not found: {path}"],
            )

        manifest = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        tools = manifest.get("tools", [])
        memory = manifest.get("memory", {}).get("stores", [])
        orchestration = manifest.get("orchestration", {})
        errors: list[str] = []
        warnings: list[str] = []

        if not manifest.get("name"):
            errors.append("Agent manifest is missing name")
        if not manifest.get("version"):
            errors.append("Agent manifest is missing version")
        if manifest.get("approval_required_for_high_impact_actions") is not True:
            errors.append("High-impact action approval must be required")
        if manifest.get("memory_integrity_required") is not True:
            errors.append("Memory integrity checks must be required")
        if manifest.get("tool_allowlist_required") is not True:
            errors.append("Tool allowlist must be required")

        errors.extend(self._validate_tools(tools))
        errors.extend(self._validate_memory(memory))
        warnings.extend(self._validate_orchestration(orchestration))

        status = "fail" if errors else "warn" if warnings else "pass"
        return AgentRuntimeValidationResult(
            manifest_path=str(path),
            status=status,
            tool_count=len(tools) if isinstance(tools, list) else 0,
            memory_store_count=len(memory) if isinstance(memory, list) else 0,
            errors=errors,
            warnings=warnings,
        )

    def _validate_tools(self, tools: Any) -> list[str]:
        errors: list[str] = []
        if not isinstance(tools, list) or not tools:
            return ["Agent manifest must define at least one tool"]

        seen: set[str] = set()
        required = {"name", "category", "allowed", "requires_approval", "max_calls_per_task", "owner"}
        for index, tool in enumerate(tools, start=1):
            missing = sorted(required - set(tool))
            if missing:
                errors.append(f"Tool {index} is missing fields: {', '.join(missing)}")
                continue
            name = str(tool["name"])
            if name in seen:
                errors.append(f"Duplicate tool name: {name}")
            seen.add(name)
            if tool["allowed"] is False and int(tool.get("max_calls_per_task", 0)) != 0:
                errors.append(f"Disabled tool {name} must have max_calls_per_task set to 0")
            if str(tool.get("category")) in {"external_action", "workflow"} and tool.get("requires_approval") is not True:
                errors.append(f"High-impact tool {name} must require approval")
        return errors

    def _validate_memory(self, stores: Any) -> list[str]:
        errors: list[str] = []
        if not isinstance(stores, list) or not stores:
            return ["Agent manifest must define at least one memory store"]

        required = {"name", "owner", "integrity_check", "retention_days", "write_approval_required"}
        seen: set[str] = set()
        for index, store in enumerate(stores, start=1):
            missing = sorted(required - set(store))
            if missing:
                errors.append(f"Memory store {index} is missing fields: {', '.join(missing)}")
                continue
            name = str(store["name"])
            if name in seen:
                errors.append(f"Duplicate memory store name: {name}")
            seen.add(name)
            if not store.get("integrity_check"):
                errors.append(f"Memory store {name} must define integrity_check")
            if int(store.get("retention_days", 0)) <= 0:
                errors.append(f"Memory store {name} must define positive retention_days")
        return errors

    def _validate_orchestration(self, orchestration: dict[str, Any]) -> list[str]:
        warnings: list[str] = []
        required_fields = orchestration.get("required_plan_fields", [])
        for field_name in ["objective", "steps", "approval_points", "rollback_plan"]:
            if field_name not in required_fields:
                warnings.append(f"Orchestration plan field is recommended: {field_name}")
        return warnings
