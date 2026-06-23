# Python Package Publishing

VulnoraIQ can be distributed as a Python package in addition to Windows/Linux/macOS release zip artifacts.

## What gets built

The `Build Python Package` workflow builds:

- source distribution: `vulnoraiq-<version>.tar.gz`
- wheel distribution: `vulnoraiq-<version>-py3-none-any.whl`

The Python Packaging User Guide recommends building distribution archives with `python -m build`, which creates a source distribution and a wheel under `dist/`.

## Trigger policy

The Python package workflow must not run on every commit, push, or pull request.

The workflow in `.github/workflows/python-package-publish.yml` runs only when:

1. a GitHub Release is published; or
2. a maintainer manually starts the workflow with `workflow_dispatch`.

For a published GitHub Release, the workflow builds and uploads package artifacts, but it does **not** publish to PyPI automatically.

## Publishing control

Manual workflow input controls publishing:

| Input | Behaviour |
| --- | --- |
| `none` | Build package artifacts only |
| `testpypi` | Build and publish to TestPyPI |
| `pypi` | Build and publish to PyPI |

Publishing uses PyPI Trusted Publishing through `pypa/gh-action-pypi-publish`, so maintainers should configure PyPI/TestPyPI trusted publishers instead of storing long-lived API tokens in GitHub secrets.

## Required PyPI setup

Before first publish:

1. Create/claim the `vulnoraiq` project on TestPyPI and PyPI, or confirm the project name is available.
2. Configure a trusted publisher for this repository and workflow:
   - repository: `sharRahul/vulnoraiq`
   - workflow: `python-package-publish.yml`
   - environment: `testpypi` for TestPyPI and `pypi` for PyPI
3. Add GitHub Environment protection rules for `testpypi` and `pypi` so package publication requires maintainer approval.
4. Run TestPyPI first.
5. Install and smoke-test from TestPyPI before publishing to PyPI.

## Local dry run

```bash
python -m pip install -e .[release]
python scripts/validate_package_metadata.py
python -m build
python -m twine check dist/*
```

## Install commands after publish

After PyPI publication:

```bash
python -m pip install vulnoraiq
vulnoraiq --target demo --profile baseline
vulnoraiq-web --host 127.0.0.1 --port 8787
```

## Important limitation

The Python package is useful for CLI/script installation and package distribution, but the repository zip artifacts remain the recommended standalone-app release for users who want the launcher files, docs, safe configuration, and local output layout together in one extracted folder.

Before treating the PyPI package as the primary installation path, validate a clean `pip install vulnoraiq` flow in a fresh virtual environment, including config discovery, launcher documentation, Web UI startup, and demo scan output.
