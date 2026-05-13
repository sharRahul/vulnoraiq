from core.scanner import Scanner


def test_demo_baseline_scan_runs():
    result = Scanner(config_dir="config").scan(target_name="demo", profile_name="baseline")

    assert result.finding_count > 0
    assert result.target_name == "demo"
    assert result.highest_severity in {"info", "low", "medium", "high", "critical"}
