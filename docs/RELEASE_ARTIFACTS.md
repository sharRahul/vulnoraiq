# Release Artifacts

This document describes how VulnoraIQ release artifacts are built for Windows, Linux, and macOS.

## Trigger policy

Platform release artifacts must **not** be built on every commit, push, or pull request.

The `Build Release Artifacts` workflow in `.github/workflows/release-build.yml` runs only when:

1. a GitHub Release is published; or
2. a maintainer manually starts the workflow with `workflow_dispatch`.

Normal CI remains in `.github/workflows/ci.yml` and `.github/workflows/python-ci.yml`.

## Artifacts produced

The release workflow builds one zip package per platform:

| Platform | Artifact |
| --- | --- |
| Windows | `vulnoraiq-<version>-windows.zip` |
| Linux | `vulnoraiq-<version>-linux.zip` |
| macOS | `vulnoraiq-<version>-macos.zip` |

Each archive includes:

- launcher files for supported local startup;
- application source packages;
- Web UI static assets;
- safe configuration files;
- documentation;
- `LICENSE`, `NOTICE`, `SECURITY.md`, `ACCEPTABLE_USE.md`, and `THIRD_PARTY_NOTICES.md`;
- a generated `START_HERE.txt` with platform-specific startup instructions.

Generated reports, local SQLite databases, secrets, keys, virtual environments, build output, and local config files are excluded.

## Build command

A maintainer can build a single platform package locally:

```bash
python scripts/build_platform_release_package.py \
  --platform linux \
  --version 0.2.0 \
  --output-dir dist/release
```

Supported platform values:

- `windows`
- `linux`
- `macos`

## Manual workflow run

From GitHub Actions, run **Build Release Artifacts** manually and provide:

- `version`: the release version or tag name to embed in artifact names;
- `upload_to_release`: `true` only when a GitHub Release with the same tag/name already exists and artifacts should be attached to it.

## Published release run

When a GitHub Release is published, the workflow:

1. resolves the release tag as the artifact version;
2. builds Windows, Linux, and macOS packages on matching hosted runners;
3. uploads all packages as workflow artifacts;
4. uploads the packages to the GitHub Release using `gh release upload`.

## Release quality gate

Before building artifacts, each platform job runs:

```bash
python scripts/validate_package_metadata.py
python scripts/validate_owasp_atlas_mappings.py
python scripts/validate_genai_readiness.py
python scripts/validate_production_testing_readiness.py --output-dir reports/output/production-readiness
```

This keeps release artifacts aligned with package metadata, OWASP/MITRE mapping governance, GenAI readiness, and production-readiness documentation.

## Current limitations

The current release artifacts are repository-checkout style zip packages with platform launchers. They are not signed native installers. Signed `.exe`, `.msi`, `.pkg`, `.dmg`, `.deb`, `.rpm`, Homebrew, Winget, or notarised macOS releases remain future maturity items.
