from __future__ import annotations

from pathlib import Path

INDEX = Path("webui/static/index.html")
APP = Path("webui/static/app.js")
SCAN_PROGRESS_CSS = Path("webui/static/scan-progress.css")


def test_running_scan_progress_panel_is_present() -> None:
    html = INDEX.read_text(encoding="utf-8")

    for expected in (
        "active-scan-card",
        "active-scan-title",
        "active-scan-detail",
        "active-scan-percent",
        "progress-bar",
        "active-scan-target",
        "active-scan-profile",
        "active-scan-stage",
        "active-scan-updated",
        "active-scan-message",
    ):
        assert expected in html

    assert "/static/scan-progress.css" in html


def test_running_scan_progress_javascript_updates_live_details() -> None:
    script = APP.read_text(encoding="utf-8")

    for expected in (
        "function renderActiveScan",
        "function updateActiveScanFromJob",
        "active-scan-card",
        "active-scan-target",
        "active-scan-profile",
        "active-scan-stage",
        "active-scan-updated",
        "active-scan-message",
        "progress-bar",
        "Scan completed. Dashboard and report outputs are ready.",
    ):
        assert expected in script


def test_running_scan_progress_css_is_responsive_and_accessible() -> None:
    css = SCAN_PROGRESS_CSS.read_text(encoding="utf-8")

    for expected in (
        ".active-scan-card",
        ".scan-visual",
        ".progress-bar-shell",
        ".scan-stage-grid",
        "@media (max-width: 1100px)",
        "@media (max-width: 760px)",
        "@media (max-width: 520px)",
        "@media (prefers-reduced-motion: reduce)",
        "@keyframes scan-pulse",
        "@keyframes progress-shimmer",
    ):
        assert expected in css
