# Production Hardening Backlog

Status: active blocker register
Current operational readiness: 3/10
Target: controlled production assessment readiness, not SaaS multi-tenant production hosting.

## Current verdict

VulnoraIQ is a strong early-stage framework for local and controlled GenAI security assessment workflows, but it is not production-ready. The codebase has useful scanner, payload, report, CI, and OWASP coverage foundations, while operational hardening remains the main blocker.

## Critical blockers

| ID | Area | Current risk | Required outcome | Status |
| --- | --- | --- | --- | --- |
| PRD-001 | Logging | Runtime visibility is incomplete and web request logging is suppressed. | Structured application logging with request, job, scan, error, and audit events. | Open |
| PRD-002 | Web server | Hosted UI runs on Python's built-in threaded HTTP server. | Documented reverse-proxy or ASGI/WSGI production deployment path. | Open |
| PRD-003 | Web UI consolidation | Multiple server entry points or legacy UI paths can create maintenance ambiguity. | One supported web runtime with legacy paths removed or clearly deprecated. | Open |
| PRD-004 | Authentication | Local demo auth is not a production identity model. | Auth enabled for non-local deployments, no default shared credentials, token source from environment or secret manager. | Open |
| PRD-005 | Web hardening | HTTPS termination, CSRF protections, rate limiting, and security headers are not production-complete. | Reverse proxy guidance plus app-level security headers and request limits. | Open |
| PRD-006 | Configuration | Several runtime paths are fixed to repository-local defaults. | Environment-variable overrides for config, output, auth, job store, and target contract paths. | Open |
| PRD-007 | Persistence | JSON file persistence is suitable for demos but not multi-user production. | SQLite/PostgreSQL-backed job, audit, and scan persistence with migrations. | Open |
| PRD-008 | Containerisation | No deployable container baseline is guaranteed. | Dockerfile, .dockerignore, and documented local container run path. | Open |
| PRD-009 | Quality gates | Developer tooling is minimal. | Ruff, mypy, formatting, and CI enforcement for lint/type checks. | Open |
| PRD-010 | Observability | No dedicated monitoring or readiness endpoints were guaranteed. | Health, readiness, metrics, and structured status endpoints. | In progress |

## First hardening tranche

1. Add explicit production-hardening backlog and keep README/status claims aligned.
2. Add health and readiness endpoints for the hosted web UI.
3. Replace CLI startup print with logger output and restore useful server-side diagnostics.
4. Add lint/type-check configuration and CI-ready test hooks.
5. Add container baseline and deployment notes.
6. Add environment-variable overrides for auth config and web output paths.
7. Add tests that prevent accidental production-ready claims until blockers are closed.

## Production claim rule

Do not describe VulnoraIQ as production-ready until all critical blockers are closed, tests enforce the operational controls, and the README/implementation status documents are updated with evidence.
