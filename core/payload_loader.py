from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


@dataclass(frozen=True, slots=True)
class Payload:
    id: str
    category: str
    input_text: str
    expected_behavior: str
    severity_hint: str = "info"
    metadata: dict[str, Any] | None = None


class PayloadLibrary:
    """Loads safe assessment inputs from YAML payload libraries."""

    def __init__(self, payload_dir: str | Path = "payloads") -> None:
        self.payload_dir = Path(payload_dir)

    def load(self, library_names: list[str] | None = None) -> dict[str, list[Payload]]:
        if not self.payload_dir.exists():
            return {}

        files = self._resolve_files(library_names)
        libraries: dict[str, list[Payload]] = {}
        for path in files:
            raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
            name = str(raw.get("name") or path.stem)
            payloads = [self._parse_payload(item) for item in raw.get("payloads", [])]
            libraries[name] = payloads
        return libraries

    def for_module(self, module_name: str, library_names: list[str] | None = None) -> list[Payload]:
        libraries = self.load(library_names)
        selected: list[Payload] = []
        for payloads in libraries.values():
            for payload in payloads:
                applies_to = (payload.metadata or {}).get("applies_to", [])
                if module_name in applies_to or "all" in applies_to:
                    selected.append(payload)
        return selected

    def _resolve_files(self, library_names: list[str] | None) -> list[Path]:
        if library_names:
            return [self.payload_dir / f"{name}.yaml" for name in library_names]
        return sorted(self.payload_dir.glob("*.yaml"))

    @staticmethod
    def _parse_payload(item: dict[str, Any]) -> Payload:
        return Payload(
            id=str(item["id"]),
            category=str(item.get("category", "general")),
            input_text=str(item["input"]),
            expected_behavior=str(item.get("expected_behavior", "The system should respond safely and remain within policy.")),
            severity_hint=str(item.get("severity_hint", "info")),
            metadata=dict(item.get("metadata", {})),
        )
