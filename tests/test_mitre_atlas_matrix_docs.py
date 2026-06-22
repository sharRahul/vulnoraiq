from __future__ import annotations

from pathlib import Path

import yaml


MATRIX_DOC = Path("docs/MITRE_ATLAS_AI_MATRIX.md")
MAPPING_FILE = Path("config/mitre_atlas_mapping.yaml")


def test_mitre_atlas_matrix_doc_exists() -> None:
    assert MATRIX_DOC.exists()
    text = MATRIX_DOC.read_text(encoding="utf-8")
    assert "MITRE ATLAS Matrix for AI" in text
    assert "Implementation checklist for adding techniques later" in text


def test_mitre_atlas_matrix_doc_lists_all_configured_techniques() -> None:
    mapping = yaml.safe_load(MAPPING_FILE.read_text(encoding="utf-8")) or {}
    doc = MATRIX_DOC.read_text(encoding="utf-8")

    missing = [technique_id for technique_id in mapping.get("techniques", {}) if technique_id not in doc]

    assert missing == []


def test_mitre_atlas_matrix_doc_lists_all_module_mappings() -> None:
    mapping = yaml.safe_load(MAPPING_FILE.read_text(encoding="utf-8")) or {}
    doc = MATRIX_DOC.read_text(encoding="utf-8")

    missing_modules = [module_name for module_name in mapping.get("module_mappings", {}) if module_name not in doc]

    assert missing_modules == []
