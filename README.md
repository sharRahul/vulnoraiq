# VulnoraIQ

**VulnoraIQ** is a self-hosted AI security testing application for authorised local or internal use with a browser GUI, CLI, reports, evidence, Agent Lab, and CI validation workflows.

VulnoraIQ is a **self-hosted internal application**. The same scope covers an **internal server** deployment when production auth, reverse proxy, TLS, audit, and backup controls are configured. The current release claim is scoped: **self-hosted laptop/server AI security testing application with controlled internal production-readiness gate passed**. Findings are framework evidence for human review, not certified VAPT-grade assurance. See [`docs/ASSESSMENT_ASSURANCE.md`](docs/ASSESSMENT_ASSURANCE.md).

## Current status

| Area | Current status |
| --- | --- |
| Version | `0.2.0` beta |
| GUI/WebUI | Yes. Browser-based React console served by `vulnoraiq-web` / `webui/hosted_server.py`. |
| Default desktop mode | Yes. Source-mode launcher starts VulnoraIQ natively on the host, uses Docker only for sandboxed Agent Lab runtimes, and stores output under `./scan-reports/`. |
| Advanced Docker Lab mode | Yes. Full Docker Compose lab remains available for servers, VMs, CI, and development. |
| Experimental Agent Lab | Yes. `/agent-lab` imports real AI-agent projects, configures LLM provider settings, selects CPU/GPU Docker runtime options, builds/runs the agent, auto-creates a target, and launches an authorised scan. See [`docs/AGENT_LAB.md`](docs/AGENT_LAB.md). |
| Persistence | SQLite job store with WAL mode, foreign keys, busy timeout, and schema versioning. |
| Future identity | Direct OIDC/JWT is deferred; see `docs/future-plans/OIDC_JWT_AUTH_PLAN.md`. |

## Prerequisites

Choose the path you want to run.

| Run path | Required before starting |
| --- | --- |
| Desktop Mode launcher | Docker Desktop or compatible Docker Engine with Docker Compose v2, Python 3.10+ for source checkouts, internet access for first image/dependency build, and a modern browser. Packaged desktop releases should later bundle the Python runtime. |
| Advanced Docker Lab launcher | Docker Engine or Docker Desktop with Docker Compose v2, internet access for the first image/dependency build, and a modern browser. |
| Experimental Agent Lab | Docker access plus host GPU container support when GPU mode is selected. Local Ollama/LM Studio providers should listen on the host and are reached through `host.docker.internal` from containers. |
| Source/package install | Python 3.10 or newer, `pip`, `venv`, Git for source checkouts, and a modern browser. |
| Local wheel build | Python 3.10 or newer plus the release extra: `pip install -e .[release]`. |
| WebUI development/tests | Node.js 20 or newer, npm, and Playwright browser dependencies. End users do not need Node.js when using release packages, Docker Lab mode, or the Python package. |

Before running any target, prepare explicit authorisation, target credentials through environment variables, owner/contact details, and an approved safety profile. Local launchers bind the WebUI to `127.0.0.1:8787` and are intended for local single-user use.

## Quick start

### Default desktop mode

For normal laptop/workstation use, start VulnoraIQ with the platform WebUI launcher:

| Platform | Launcher |
| --- | --- |
| Windows | `launch-vulnoraiq-webui.bat` |
| macOS | `launch-vulnoraiq-webui.command` |
| Linux | `launch-vulnoraiq-webui.sh` |

Desktop Mode does this:

1. starts VulnoraIQ natively on the host;
2. checks Docker is available for sandboxed Agent Lab runtimes;
3. creates local folders under `./scan-reports/` and `./agent-lab/`;
4. opens <http://127.0.0.1:8787>;
5. lets Agent Lab build/run imported agents in Docker containers only when needed.

Desktop Mode folder contract:

```text
scan-reports/
  jobs.db
  reports/
  evidence/
  audit/
  exports/

agent-lab/
  projects/
  deployments.yaml
```

To use Agent Lab, open <http://localhost:8787/agent-lab> after the WebUI is running.

### Advanced Docker Lab mode

Use Docker Lab mode for servers, VMs, CI, or reproducible full-stack lab testing:

| Platform | Launcher |
| --- | --- |
| Windows | `launch-vulnoraiq-docker-lab.bat` |
| macOS | `launch-vulnoraiq-docker-lab.command` |
| Linux | `launch-vulnoraiq-docker-lab.sh` |

Manual Docker Lab equivalent:

```bash
docker compose build
docker compose up -d
docker compose ps
```

Open the GUI/WebUI in your browser: <http://localhost:8787>.

The Docker Lab WebUI is published on host loopback only: `127.0.0.1:8787:8787`.

Useful Docker commands:

```bash
docker compose exec vulnoraiq-web vulnoraiq targets list
docker compose exec vulnoraiq-web vulnoraiq reports list
docker compose exec vulnoraiq-web vulnoraiq jobs list
```

Cleanly close the Docker lab:

```bash
docker compose down
```

Only use this when you intentionally want to delete local jobs, reports, evidence, audit data, Agent Lab imports, and Docker volumes:

```bash
docker compose down -v
```

Install from a source/package checkout and run locally without the launcher:

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
python -m pip install --upgrade pip
pip install -e .[dev]
vulnoraiq-web --host 127.0.0.1 --port 8787
```

Open <http://127.0.0.1:8787>. Cleanly close with `Ctrl+C` in the terminal that started `vulnoraiq-web`.

## WebUI and CLI

The supported GUI is the built React console under `webui/static/console/`; the source app lives in `webui/console/`. It is a browser GUI, not a native desktop window. The experimental Agent Lab static assets live under `webui/static/agent-lab/`.

The primary WebUI launchers start Desktop Mode. The explicit `launch-vulnoraiq-docker-lab.*` launchers start the full Docker Compose lab.

You can also run the launcher backends directly:

```bash
python scripts/desktop_launch.py       # Desktop Mode
python scripts/bootstrap_launch.py     # Advanced Docker Lab Mode
```

See [`docs/RUN_MODES_DESKTOP_AND_DOCKER_LAB.md`](docs/RUN_MODES_DESKTOP_AND_DOCKER_LAB.md) for the architecture plan.

## Deployment and security boundary

Local desktop and Docker Lab launcher paths are for single-user controlled use. Shared/internal-server deployment requires production configuration validation, real secrets, TLS at a trusted reverse proxy, audit retention, backups, and authorised target governance.

Agent Lab is experimental because it can build and run imported code through local Docker. Keep it loopback-only unless production auth, reverse proxy/TLS, audit, and an explicit risk decision are in place.

```bash
export VULNORAIQ_ENV=production
export VULNORAIQ_AUTH_ENABLED=true
export VULNORAIQ_ADMIN_TOKEN="$(openssl rand -hex 32)"
export VULNORAIQ_JOB_STORE_BACKEND=sqlite
export VULNORAIQ_JOB_STORE_PATH=/data/jobs.db
export VULNORAIQ_WEB_OUTPUT_ROOT=/data/reports
python scripts/validate_runtime_production_config.py
vulnoraiq-web --host 127.0.0.1 --port 8787
```

Use trusted reverse-proxy identity only when the proxy authenticates users and strips spoofed identity headers. Direct OIDC/JWT remains future work, not a blocker for current local single-user usage.

## Validation and release gates

```bash
ruff check .
mypy .
pytest -q
python -m pip check
pip-audit
python scripts/validate_package_metadata.py
python scripts/validate_owasp_atlas_mappings.py
python scripts/validate_genai_readiness.py
python scripts/validate_production_testing_readiness.py --output-dir reports/output/production-readiness
python scripts/validate_runtime_production_config.py
```

WebUI browser flow:

```bash
npm install
npx playwright install chromium --with-deps
npm run test:webui:hosted
```

## Documentation and roadmap

| Need | Document |
| --- | --- |
| User guide | [`docs/USER_GUIDE.md`](docs/USER_GUIDE.md) |
| Run modes | [`docs/RUN_MODES_DESKTOP_AND_DOCKER_LAB.md`](docs/RUN_MODES_DESKTOP_AND_DOCKER_LAB.md) |
| Experimental Agent Lab | [`docs/AGENT_LAB.md`](docs/AGENT_LAB.md), [`docs/AGENT_LAB_PLAN.md`](docs/AGENT_LAB_PLAN.md) |
| Documentation index and status | [`docs/README.md`](docs/README.md), [`docs/IMPLEMENTATION_STATUS.md`](docs/IMPLEMENTATION_STATUS.md) |
| Docker lab | [`docs/DOCKER_TESTING.md`](docs/DOCKER_TESTING.md) |
| Deployment and operations | [`docs/DEPLOYMENT.md`](docs/DEPLOYMENT.md), [`docs/RUNBOOK.md`](docs/RUNBOOK.md), [`docs/INCIDENT_RESPONSE.md`](docs/INCIDENT_RESPONSE.md) |
| WebUI and CLI | [`docs/WEBUI_GUIDE.md`](docs/WEBUI_GUIDE.md), [`docs/WEB_UI_TEST_CATALOG.md`](docs/WEB_UI_TEST_CATALOG.md), [`docs/CLI_GUIDE.md`](docs/CLI_GUIDE.md) |
| Safety and targets | [`docs/SAFETY_MODEL.md`](docs/SAFETY_MODEL.md), [`docs/TARGET_CONFIGURATION.md`](docs/TARGET_CONFIGURATION.md) |
| Release and supply chain | [`docs/RELEASE_CHECKLIST.md`](docs/RELEASE_CHECKLIST.md), [`docs/RELEASE_ARTIFACTS.md`](docs/RELEASE_ARTIFACTS.md), [`docs/SUPPLY_CHAIN_PIPELINE.md`](docs/SUPPLY_CHAIN_PIPELINE.md), [`docs/PYPI_PACKAGE.md`](docs/PYPI_PACKAGE.md) |
| Readiness and assurance | [`docs/PRODUCTION_READINESS_SCORECARD.md`](docs/PRODUCTION_READINESS_SCORECARD.md), [`docs/PRODUCTION_HARDENING_BACKLOG.md`](docs/PRODUCTION_HARDENING_BACKLOG.md), [`docs/ASSESSMENT_ASSURANCE.md`](docs/ASSESSMENT_ASSURANCE.md) |
| Future identity plan | [`docs/future-plans/OIDC_JWT_AUTH_PLAN.md`](docs/future-plans/OIDC_JWT_AUTH_PLAN.md) |

## License and notices

VulnoraIQ-specific source code and documentation are licensed under Apache-2.0. See [`LICENSE`](LICENSE).

Some documentation and planning data is derived from MITRE ATLAS. MITRE ATLAS data is copyright 2021-2026 MITRE and licensed under the Apache License, Version 2.0. See [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md).
