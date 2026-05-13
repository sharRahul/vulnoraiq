from pathlib import Path

from core.scanner import Scanner
from reports.report_generator import MarkdownReportGenerator


def test_report_generator_writes_markdown(tmp_path: Path):
    result = Scanner(config_dir="config").scan(target_name="demo", profile_name="baseline")
    output = MarkdownReportGenerator().generate(result, tmp_path / "report.md")

    assert output.exists()
    assert "LLM VAPT Report" in output.read_text(encoding="utf-8")
