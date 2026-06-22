from __future__ import annotations

from typing import Iterable

from core.payload_loader import PayloadLibrary
from core.risk_scoring import score_findings
from core.types import Finding, ScanContext
from modules.registry import ModuleRegistry


class TestRunner:
    """Runs assessment modules resolved from the module registry."""

    def __init__(self, registry: ModuleRegistry | None = None, payload_library: PayloadLibrary | None = None) -> None:
        self.registry = registry or ModuleRegistry()
        self.payload_library = payload_library or PayloadLibrary()

    def run_modules(self, module_names: Iterable[str], context: ScanContext) -> list[Finding]:
        findings: list[Finding] = []
        library_names = context.config.get("default", {}).get("payload_libraries")
        for module_name in module_names:
            module = self.registry.get(module_name)
            payloads = self.payload_library.for_module(module_name, library_names=library_names)
            findings.append(module.run(context, payloads))
        return score_findings(findings)
