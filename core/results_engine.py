from __future__ import annotations

from collections import Counter
from dataclasses import asdict
from typing import Any

from core.types import Finding, ScanResult


class ResultsEngine:
    """Normalises and summarises module output."""

    def normalise(self, result: ScanResult) -> dict[str, Any]:
        severity_counts = Counter(f.severity.lower() for f in result.findings)
        owasp_counts = Counter(f.owasp_id for f in result.findings)
        return {
            "target": result.target_name,
            "profile": result.profile_name,
            "started_at": result.started_at.isoformat(),
            "completed_at": result.completed_at.isoformat(),
            "finding_count": result.finding_count,
            "highest_severity": result.highest_severity,
            "severity_counts": dict(severity_counts),
            "owasp_counts": dict(owasp_counts),
            "findings": [self._finding_to_dict(f) for f in result.findings],
        }

    @staticmethod
    def _finding_to_dict(finding: Finding) -> dict[str, Any]:
        data = asdict(finding)
        data["severity"] = finding.severity.lower()
        return data
