# Deployment Notes

Status: local/container baseline only. This is not yet a hardened production deployment guide.

## Local Web UI

```bash
vulnoraiq-web --host 127.0.0.1 --port 8787
```

Health checks:

```bash
curl http://127.0.0.1:8787/healthz
curl http://127.0.0.1:8787/readyz
```

## Container baseline

Build and run the local container:

```bash
docker build -t vulnoraiq:local .
docker run --rm -p 8787:8787 vulnoraiq:local
```

The container exposes `/healthz` for Docker health checks.

## Environment variables

| Variable | Purpose | Default |
| --- | --- | --- |
| `VULNORAIQ_HOST` | Hosted Web UI bind host | `127.0.0.1` locally, `0.0.0.0` in Dockerfile |
| `VULNORAIQ_PORT` | Hosted Web UI port | `8787` |
| `VULNORAIQ_LOG_LEVEL` | Python logging level | `INFO` |
| `VULNORAIQ_CONFIG_DIR` | Config directory | `config` |
| `VULNORAIQ_WEB_USERS_PATH` | Web user/auth config path | `config/web_users.yaml` |
| `VULNORAIQ_WEB_OUTPUT_ROOT` | Web UI report output root | `reports/output/webui` |
| `VULNORAIQ_JOB_STORE_PATH` | Web UI JSON job store path | `reports/output/webui/jobs.json` |

## Production deployment blockers

Before using this beyond a controlled lab or trusted internal test environment, complete the production hardening backlog:

- terminate HTTPS at a reverse proxy or trusted ingress;
- enable strong authentication and remove default local demo credentials;
- add rate limiting and CSRF protections for browser-originating requests;
- replace JSON file persistence with a database-backed job and audit store;
- run under a production web runtime or gateway rather than relying directly on the built-in development HTTP server;
- add metrics, alerting, backup, and retention controls;
- document secret management and token rotation.

See `docs/PRODUCTION_HARDENING_BACKLOG.md` for the active blocker register.
