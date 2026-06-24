from __future__ import annotations

from pathlib import Path

import yaml

REQUIRED = {
    "id",
    "title",
    "objective",
    "owasp_ai_testing_guide_section",
    "owasp_llm_top10",
    "mitre_atlas",
    "test_type",
    "fixture",
    "expected_detector_behavior",
    "evidence_artifacts",
    "reporting_fields",
    "safety_notes",
    "implementation_status",
}


def main() -> int:
    path = Path("benchmarks/fixtures/aitg/aitg_32_manifest.yaml")
    data = yaml.safe_load(path.read_text()) if path.exists() else {}
    tests = data.get("aitg_tests") or []
    errors: list[str] = []
    if len(tests) != 32:
        errors.append(f"expected exactly 32 AITG tests, found {len(tests)}")
    ids = []
    for index, test in enumerate(tests, 1):
        missing = sorted(key for key in REQUIRED if not test.get(key))
        if missing:
            errors.append(f"entry {index} missing {missing}")
        ids.append(test.get("id"))
        if not test.get("owasp_llm_top10") or not test.get("mitre_atlas") or not test.get("evidence_artifacts"):
            errors.append(f"{test.get('id')} lacks mapping/evidence metadata")
    if len(ids) != len(set(ids)):
        errors.append("duplicate AITG test IDs")
    docs = " ".join(
        doc.read_text(errors="ignore")
        for doc in [
            Path("docs/AI_TESTING_GUIDE_IMPLEMENTATION_PLAN.md"),
            Path("docs/AI_TESTING_GUIDE_INTEGRATION.md"),
            Path("README.md"),
        ]
        if doc.exists()
    )
    if "full 32-test" in docs.lower() and errors:
        errors.append("docs claim full coverage but manifest is incomplete")
    if errors:
        print("\n".join(errors))
        return 1
    print("AITG full coverage manifest validation passed: 32 tests with required mappings and evidence metadata.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
