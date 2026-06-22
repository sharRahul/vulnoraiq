from __future__ import annotations

import argparse
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


@dataclass(slots=True)
class HtmlExportResult:
    status: str
    output_path: str
    included_files: list[str]


class HtmlExportPackager:
    """Packages branded HTML reports and supporting artifacts for presentation."""

    def __init__(self, branding_path: str | Path = "config/report_branding.yaml") -> None:
        self.branding_path = Path(branding_path)

    def package(self, input_dir: str | Path = "reports/output", output_path: str | Path | None = None) -> HtmlExportResult:
        branding = yaml.safe_load(self.branding_path.read_text(encoding="utf-8")) or {}
        output = Path(output_path or branding.get("exports", {}).get("default_html_bundle", "reports/output/vulnoraiq-html-export.zip"))
        output.parent.mkdir(parents=True, exist_ok=True)
        root = Path(input_dir)
        files = [path for path in sorted(root.rglob("*")) if path.is_file() and self._include(path, branding)]
        manifest = self._manifest(branding, files)
        with zipfile.ZipFile(output, mode="w", compression=zipfile.ZIP_DEFLATED) as archive:
            for file_path in files:
                archive.write(file_path, arcname=str(file_path.relative_to(root)))
            archive.writestr("VULNORAIQ_EXPORT_MANIFEST.yaml", yaml.safe_dump(manifest, sort_keys=False))
        return HtmlExportResult("pass", str(output), [str(path) for path in files])

    @staticmethod
    def _include(path: Path, branding: dict[str, Any]) -> bool:
        suffix = path.suffix.lower()
        if suffix == ".html":
            return True
        if suffix == ".json" and branding.get("exports", {}).get("include_raw_json", True):
            return True
        if suffix == ".md" and branding.get("exports", {}).get("include_markdown", True):
            return True
        if suffix == ".sarif" and branding.get("exports", {}).get("include_sarif", True):
            return True
        return False

    @staticmethod
    def _manifest(branding: dict[str, Any], files: list[Path]) -> dict[str, Any]:
        return {
            "brand": branding.get("brand", {}),
            "file_count": len(files),
            "files": [str(path) for path in files],
        }


def main() -> None:
    parser = argparse.ArgumentParser(description="Build a branded VulnoraIQ HTML export bundle.")
    parser.add_argument("--input-dir", default="reports/output")
    parser.add_argument("--output", default=None)
    parser.add_argument("--branding", default="config/report_branding.yaml")
    args = parser.parse_args()
    result = HtmlExportPackager(args.branding).package(args.input_dir, args.output)
    print(f"HTML export package written to {result.output_path}")


if __name__ == "__main__":
    main()
