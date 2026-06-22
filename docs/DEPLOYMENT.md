# Deployment Guide

## Quick Start

```bash
# Install
pip install -e .

# Run the web UI (binds to 127.0.0.1:8787 by default)
vulnoraiq-web

# Health checks
curl http://127.0.0.1:8787/healthz
curl http://127.0.0.1:8787/readyz
```

## Container

A `Dockerfile` is provided for local container builds:

```bash
docker build -t vulnoraiq:local .
docker run --rm -p 8787:8787 vulnoraiq:local
```

## Authentication

Auth is **enabled by default** and fail-closed — anonymous requests receive HTTP 401.

### Token-based auth via environment variables (recommended for production)

Set these env vars to configure token-based authentication:

```bash
export VULNORAIQ_AUTH_ENABLED=true
export VULNORAIQ_ADMIN_TOKEN="<generate-a-strong-random-token>"
export VULNORAIQ_ANALYST_TOKEN="<another-random-token>"
export VULNORAIQ_VIEWER_TOKEN="<yet-another-random-token>"
```

Role permissions:

| Role | Permissions |
| --- | --- |
| `viewer` | view scans, download artifacts |
| `analyst` | viewer + start demo scans |
| `admin` | analyst + start configured-target scans, manage runtime |

Clients pass the token via the `X-VulnoraIQ-Token` header.

### File-based auth fallback

If no token env vars are set, the manager reads `config/web_users.yaml`. The committed defaults use
SHA-256 hashes that are trivially reversible — **replace them for any non-development deployment**.

### Disabling auth

Not recommended for production, but available for development:

```bash
export VULNORAIQ_AUTH_ENABLED=false
```

## Security Features (built-in)

All features are enabled by default and configurable via environment variables.

### Request size limit

Rejects requests with bodies larger than `VULNORAIQ_MAX_REQUEST_BODY` bytes (default: 10 MB).

### Rate limiting

In-memory sliding-window rate limiter. Default: 60 requests per 60-second window per IP.

| Variable | Default | Description |
| --- | --- | --- |
| `VULNORAIQ_RATE_LIMIT_WINDOW` | `60` | Window in seconds |
| `VULNORAIQ_RATE_LIMIT_MAX` | `60` | Max requests per window |

### CSRF protection

State-changing `POST /api/scans` requests require a valid `X-CSRF-Token` header.
Obtain a token via `GET /api/csrf-token` (which returns `{"csrf_token": "..."}`).

### Security headers

Every response includes:

- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: DENY`
- `X-XSS-Protection: 0`
- `Strict-Transport-Security: max-age=31536000; includeSubDomains`
- `Referrer-Policy: strict-origin-when-cross-origin`
- `Content-Security-Policy: default-src 'self'; ...`
- `Permissions-Policy: camera=(), microphone=(), geolocation=()`

## Persistence

Two backends are available, selected via `VULNORAIQ_JOB_STORE_BACKEND`:

### SQLite (default, recommended for production)

```bash
export VULNORAIQ_JOB_STORE_BACKEND=sqlite
export VULNORAIQ_JOB_STORE_PATH=/data/vulnoraiq/jobs.db
```

Uses a single SQLite database with indexed `jobs` and `events` tables.
Suitable for single-server deployments. Back up the database file regularly.

### JSON file (legacy)

```bash
export VULNORAIQ_JOB_STORE_BACKEND=json
export VULNORAIQ_JOB_STORE_PATH=/data/vulnoraiq/jobs.json
```

Thread-safe with `RLock`. Suitable for low-traffic development use only.

## Audit Log

An audit log is emitted on a dedicated `vulnoraiq.audit` logger. Events include
scan creation with actor identity, target, profile, and job ID.

In production, configure a log shipper (e.g., Filebeat, Fluentd) to forward
the audit log to your SIEM or centralized logging platform.

```
2025-01-15 10:30:00,000 AUDIT event=server_start user=anonymous role=viewer authenticated=False ip=127.0.0.1 detail=host=127.0.0.1 port=8787
2025-01-15 10:30:05,000 AUDIT event=scan_created user=admin role=admin authenticated=True ip=10.0.0.1 detail=target=demo profile=baseline job_id=abc123
```

## Reverse Proxy & TLS

The built-in HTTP server is intended to run behind a reverse proxy that terminates TLS.

### nginx example

```nginx
server {
    listen 443 ssl;
    server_name vulnoraiq.example.com;

    ssl_certificate /etc/ssl/certs/vulnoraiq.crt;
    ssl_certificate_key /etc/ssl/private/vulnoraiq.key;

    location / {
        proxy_pass http://127.0.0.1:8787;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # SSE support
        proxy_buffering off;
        proxy_cache off;
        proxy_read_timeout 86400s;
    }
}
```

### Caddy example

```
vulnoraiq.example.com {
    reverse_proxy 127.0.0.1:8787
}
```

## Metrics & Monitoring

- `/healthz` — liveness probe (returns `{"status": "ok"}`)
- `/readyz` — readiness probe (checks targets and profiles are loaded)

Integrate with your monitoring stack by polling these endpoints. Example
Prometheus blackbox exporter configuration:

```yaml
modules:
  vulnoraiq_health:
    prober: http
    http:
      valid_status_codes: [200]
      method: GET
      url: "http://127.0.0.1:8787/healthz"
```

## Backup & Retention

### SQLite

```bash
# Online backup (low-traffic periods recommended)
sqlite3 /data/vulnoraiq/jobs.db ".backup /data/backups/jobs-$(date +%Y%m%d).db"

# Restore
sqlite3 /data/vulnoraiq/jobs.db ".restore /data/backups/jobs-20250115.db"
```

### JSON

Simply copy `jobs.json` to your backup destination.

### Retention policy

There is no built-in retention job. Implement a cron or systemd timer:

```
0 2 * * * find /data/backups -name "jobs-*.db" -mtime +90 -delete
```

## Environment Variables Reference

| Variable | Default | Description |
| --- | --- | --- |
| `VULNORAIQ_HOST` | `127.0.0.1` | Bind address |
| `VULNORAIQ_PORT` | `8787` | Bind port |
| `VULNORAIQ_AUTH_ENABLED` | `true` | Enable authentication |
| `VULNORAIQ_ADMIN_TOKEN` | — | Admin bearer token |
| `VULNORAIQ_ANALYST_TOKEN` | — | Analyst bearer token |
| `VULNORAIQ_VIEWER_TOKEN` | — | Viewer bearer token |
| `VULNORAIQ_LOG_LEVEL` | `INFO` | Python logging level |
| `VULNORAIQ_CONFIG_DIR` | `config` | Config directory |
| `VULNORAIQ_WEB_USERS_PATH` | `config/web_users.yaml` | Auth config path |
| `VULNORAIQ_WEB_OUTPUT_ROOT` | `reports/output/webui` | Report output root |
| `VULNORAIQ_JOB_STORE_BACKEND` | `sqlite` | Persistence backend (`sqlite` or `json`) |
| `VULNORAIQ_JOB_STORE_PATH` | `reports/output/webui/jobs.db` | Store path |
| `VULNORAIQ_MAX_REQUEST_BODY` | `10485760` | Max request body in bytes (10 MB) |
| `VULNORAIQ_RATE_LIMIT_WINDOW` | `60` | Rate limit window in seconds |
| `VULNORAIQ_RATE_LIMIT_MAX` | `60` | Max requests per window per IP |

## Production Checklist

- [ ] Run behind a reverse proxy with TLS termination
- [ ] Set `VULNORAIQ_ADMIN_TOKEN`, `VULNORAIQ_ANALYST_TOKEN`, `VULNORAIQ_VIEWER_TOKEN`
- [ ] Verify `VULNORAIQ_AUTH_ENABLED=true` (default)
- [ ] Use SQLite backend (`VULNORAIQ_JOB_STORE_BACKEND=sqlite`, default)
- [ ] Configure audit log shipping to SIEM
- [ ] Set up periodic database backups
- [ ] Set up monitoring on `/healthz` and `/readyz`
- [ ] Configure log rotation for audit and application logs
- [ ] Keep `config/web_users.yaml` out of version control or strip demo hashes
