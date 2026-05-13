from __future__ import annotations

import argparse
from pathlib import Path

from core.scanner import Scanner
from reports.report_generator import MarkdownReportGenerator


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run an authorised LLM VAPT scan.")
    parser.add_argument("--target", default="demo", help="Target name from config/targets.yaml. Default: demo")
    parser.add_argument("--profile", default="baseline", help="Attack profile from config/attack_profiles.yaml. Default: baseline")
    parser.add_argument("--output", default="reports/output/scan-report.md", help="Markdown report output path.")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    scanner = Scanner(config_dir=Path("config"))
    result = scanner.scan(target_name=args.target, profile_name=args.profile)
    output = MarkdownReportGenerator().generate(result, args.output)
    print(f"Scan complete: {result.finding_count} findings. Report written to {output}")


if __name__ == "__main__":
    main()
