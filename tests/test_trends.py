from __future__ import annotations

import json

from dashboards.diff_trend_dashboard import build_summary, load_diffs, write_html
from dashboards.diff_trend_dashboard import write_markdown as write_diff_markdown
from reports.policy_trends import build_policy_trend, load_reports, write_json, write_markdown


def test_policy_trend_from_reports(tmp_path) -> None:
    report = tmp_path / "report.json"
    report.write_text(
        json.dumps(
            {
                "target": "demo",
                "profile": "baseline",
                "policy_status": "pass",
                "finding_count": 1,
                "highest_severity": "info",
                "policy_results": [{"policy_id": "severity_threshold", "status": "pass"}],
            }
        ),
        encoding="utf-8",
    )

    trend = build_policy_trend(load_reports(tmp_path))
    output = write_json(trend, tmp_path / "trend.json")
    markdown = write_markdown(trend, tmp_path / "trend.md")

    assert trend.report_count == 1
    assert output.exists()
    assert markdown.exists()


def test_diff_trend_dashboard_outputs(tmp_path) -> None:
    diff = tmp_path / "sample-diff.json"
    diff.write_text(
        json.dumps(
            {
                "baseline_report": "baseline.json",
                "current_report": "current.json",
                "finding_count_delta": 2,
                "policy_status_changed": True,
                "has_regression": True,
            }
        ),
        encoding="utf-8",
    )

    summary = build_summary(load_diffs(tmp_path))
    markdown = write_diff_markdown(summary, tmp_path / "dashboard.md")
    html = write_html(summary, tmp_path / "dashboard.html")

    assert summary["regression_count"] == 1
    assert markdown.exists()
    assert html.exists()
