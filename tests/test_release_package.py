from __future__ import annotations

import zipfile

from scripts.build_release_package import build_package


def test_release_package_builder_includes_manifest_paths(tmp_path) -> None:
    manifest = tmp_path / "release_package.yaml"
    sample = tmp_path / "sample.txt"
    sample.write_text("demo", encoding="utf-8")
    output = tmp_path / "package.zip"
    manifest.write_text(
        f"""
name: test-package
version: 1
output_path: {output}
include_paths:
  - {sample}
""",
        encoding="utf-8",
    )

    package = build_package(manifest)

    assert package == output
    with zipfile.ZipFile(package) as archive:
        assert sample.as_posix() in archive.namelist()
