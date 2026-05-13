from __future__ import annotations

from pathlib import Path

from core.results_engine import ResultsEngine
from core.types import ScanResult


class MarkdownReportGenerator:
    """Generates audit-friendly Markdown reports."""

    def __init__(self) -> None:
        self.results_engine = ResultsEngine()

    def generate(self, result: ScanResult, output_path: str | Path) -> Path:
        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)
        normalised = self.results_engine.normalise(result)
        lines = [
            f"# LLM VAPT Report - {normalised['target']}",
            "",
            "## Executive Summary",
            "",
            f"- Profile: `{normalised['profile']}`",
            f"- Findings: `{normalised['finding_count']}`",
            f"- Highest severity: `{normalised['highest_severity']}`",
            "",
            "## Severity Counts",
            "",
        ]
        for severity, count in sorted(normalised["severity_counts"].items()):
            lines.append(f"- {severity}: {count}")
        lines.extend(["", "## Findings", ""])
        for index, finding in enumerate(normalised["findings"], start=1):
            lines.extend([
                f"### {index}. {finding['title']}",
                "",
                f"- Severity: `{finding['severity']}`",
                f"- Score: `{finding.get('score')}`",
                f"- OWASP: `{finding['owasp_id']}`",
                f"- Component: `{finding['affected_component']}`",
                f"- MITRE ATLAS: `{', '.join(finding.get('mitre_atlas') or []) or 'Not mapped'}`",
                "",
                finding["description"],
                "",
                f"Recommendation: {finding['recommendation']}",
                "",
            ])
        output.write_text("\n".join(lines), encoding="utf-8")
        return output
