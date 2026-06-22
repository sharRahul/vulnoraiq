from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import requests
import yaml

from core.mitre_atlas import MitreAtlasMapping

DEFAULT_CONFIG = "config/atlas_refresh.yaml"


def load_yaml(path: str | Path) -> dict[str, Any]:
    return yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}


def load_source(source: str | Path) -> dict[str, Any]:
    source_text = str(source)
    if source_text.startswith("http://") or source_text.startswith("https://"):
        response = requests.get(source_text, timeout=30)
        response.raise_for_status()
        return yaml.safe_load(response.text) or {}
    return load_yaml(source)


def refresh_mapping(source: str | Path, existing_mapping_path: str | Path = "config/mitre_atlas_mapping.yaml", output_path: str | Path | None = None) -> Path:
    atlas_data = load_source(source)
    existing = load_yaml(existing_mapping_path)
    source_techniques = {
        str(item["id"]): {
            "name": str(item.get("name", item["id"])),
            "rationale": existing.get("techniques", {}).get(str(item["id"]), {}).get("rationale", "Imported from ATLAS source data."),
        }
        for item in atlas_data.get("matrices", [{}])[0].get("techniques", [])
        if str(item.get("id", "")).startswith("AML.T")
    }
    preserved_techniques = dict(existing.get("techniques", {}))
    preserved_techniques.update(source_techniques)
    refreshed = {
        "source": {
            **existing.get("source", {}),
            "atlas_version": atlas_data.get("version", existing.get("source", {}).get("atlas_version")),
            "refreshed_from": str(source),
        },
        "techniques": {key: preserved_techniques[key] for key in sorted(preserved_techniques)},
        "module_mappings": existing.get("module_mappings", {}),
    }
    output = Path(output_path or existing_mapping_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(yaml.safe_dump(refreshed, sort_keys=False), encoding="utf-8")
    validation = MitreAtlasMapping(output).validate()
    if validation.status == "fail":
        raise RuntimeError(f"Refreshed ATLAS mapping failed validation: {validation.errors}")
    return output


def main() -> None:
    parser = argparse.ArgumentParser(description="Refresh local MITRE ATLAS mapping metadata.")
    parser.add_argument("--config", default=DEFAULT_CONFIG)
    parser.add_argument("--source", default=None, help="ATLAS YAML URL or local file path. Defaults to config source URL.")
    parser.add_argument("--existing", default="config/mitre_atlas_mapping.yaml")
    parser.add_argument("--output", default="config/mitre_atlas_mapping.yaml")
    args = parser.parse_args()
    config = load_yaml(args.config)
    source = args.source or config.get("source", {}).get("default_url")
    output = refresh_mapping(source, args.existing, args.output)
    print(f"MITRE ATLAS mapping refreshed at {output}")


if __name__ == "__main__":
    main()
