# Deployment Guide

This guide describes the supported VulnoraIQ `0.2.0` deployment posture.

> **Scope:** VulnoraIQ `0.2.0` has passed the controlled internal enterprise production-readiness gate. It is suitable for single-organisation/internal deployment when configured with the controls below. It is **not** public internet-facing SaaS or multi-tenant ready without additional controls such as OIDC/SSO, tenant isolation, HA persistence, distributed rate limiting, WAF/CDN/DDoS protection, and external penetration testing.

## Quick start: local development

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e .[dev]

# Safe local CLI demo
vulnoraiq --target demo --profile baseline

# Local Web UI, bound to localhost
vulnoraiq-web --host 127.0.0.1 --port 8787
```

Health checks:

```bash
curl http://127.0.0.1:8787/healthz
curl http://127.0.0.1:8787/readyz
```

The demo target is safe and local. Configured non-demo targets require explicit authorisation.

## Quick start: production-mode validation

Production mode fails closed when unsafe runtime configuration is detected.

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

Production-mode validation checks:

- auth is enabled
- admin token is set and at least 20 characters
- known demo/default tokens are rejected
- internal development admin token is disabled
- JSON job store is rejected in production
- SQLite path is not obviously ephemeral or unsafe
- output directory is writable
- config directory is readable
- trusted proxy CIDRs are valid when proxy headers are enabled
- binding to `0.0.0.0` or `::` without trusted proxy configuration fails
- rate-limit, request-body, and CSRF TTL values are sane
- audit logging level is valid

## Container deployment

Build and run with persistent data:

```bash
docker build -t vulnoraiq:0.2.0-rc .
docker run --rm -p 8787:8787 \
  -v vulnoraiq-data:/data \
  -e VULNORAIQ_ENV=production \
  -e VULNORAIQ_AUTH_ENABLED=true \
  -e VULNORAIQ_ADMIN_TOKEN="$(openssl rand -hex 32)" \
  -e VULNORAIQ_JOB_STORE_BACKEND=sqlite \
  -e VULNORAIQ_JOB_STORE_PATH=/data/jobs.db \
  -e VULNORAIQ_WEB_OUTPUT_ROOT=/data/reports \
  vulnoraiq:0.2.0-rc
```

The container runs as a non-root user, uses `/data` for SQLite DB and reports, exposes port `8787`, and includes a `/healthz` healthcheck.

## Docker Compose

```bash
cp .env.production.example .env.production
# Edit .env.production and replace every placeholder token before starting.
docker compose up --build
```

Do not commit real `.env.production` files. Commit only `.env.production.example` with placeholders.

## Authentication

Auth is **enabled by default** and fail-closed. Anonymous requests to protected routes receive HTTP `401`.

### Token auth, default mode

```bash
export VULNORAIQ_AUTH_MODE=token
export VULNORAIQ_AUTH_ENABLED=true
export VULNORAIQ_ADMIN_TOKEN="$(openssl rand -hex 32)"
export VULNORAIQ_ANALYST_TOKEN="$(openssl rand -hex 32)"
export VULNORAIQ_VIEWER_TOKEN="$(openssl rand -hex 32)"
```

Clients pass the token via the `X-VulnoraIQ-Token` header. Tokens are compared using constant-time comparison.

| Role | Permissions |
| --- | --- |
| `viewer` | view scans, download artifacts |
| `analyst` | viewer + start demo scans |
| `admin` | analyst + start configured-target scans, manage runtime |

### Trusted reverse-proxy identity mode

Use this only when an upstream proxy performs authentication and strips spoofed identity headers from untrusted clients.

```bash
export VULNORAIQ_AUTH_MODE=trusted_proxy
export VULNORAIQ_TRUST_PROXY_HEADERS=true
export VULNORAIQ_TRUSTED_PROXY_CIDRS="127.0.0.1/32,::1/128"
```

Supported identity headers:

| Header | Purpose |
| --- | --- |
| `X-Authenticated-User` | required username |
| `X-Authenticated-Email` | informational email |
| `X-Authenticated-Groups` | informational group list |
| `X-VulnoraIQ-Role` | `viewer`, `analyst`, or `admin`; unknown roles default to viewer |

Spoofed identity headers from untrusted client IPs are ignored.

### File-based auth fallback

If no token environment variables are set, development mode can read `config/web_users.yaml`. This fallback is **not allowed in production mode**.

For local development only:

```bash
cp config/web_users.example.yaml config/web_users.yaml
# Replace hashes with local-only values.
```

## Proxy IP trust

By default, VulnoraIQ does **not** trust `X-Forwarded-For`. This prevents client-IP spoofing.

```bash
export VULNORAIQ_TRUST_PROXY_HEADERS=true
export VULNORAIQ_TRUSTED_PROXY_CIDRS="10.0.0.0/8,172.16.0.0/12,192.168.0.0/16"
```

The server trusts forwarded client IPs only when the direct connection source is within a trusted CIDR.

## Web UI endpoints

| Endpoint | Auth | Purpose |
| --- | --- | --- |
| `/` | required | static Web UI |
| `/healthz` | public | liveness |
| `/readyz` | public | readiness based on target/profile config |
| `/metrics` | required by default | Prometheus metrics |
| `/api/csrf-token` | required | CSRF token for state-changing requests |
| `/api/config` | required | role-aware safe configuration view |
| `/api/scans` | required | list or create scans |
| `/api/scans/<id>` | required | scan details |
| `/api/scans/<id>/events` | required | Server-Sent Events stream |
| `/api/scans/<id>/artifact/<name>` | required | artifact download |

`POST /api/scans` requires `X-CSRF-Token`.

## Security features

### Request size and parsing

- `VULNORAIQ_MAX_REQUEST_BODY` defaults to `10485760` bytes / 10 MB.
- Oversized requests return HTTP `413`.
- Invalid `Content-Length` and malformed JSON return HTTP `400`.
- API errors are JSON responses with security headers.

### CSRF

- Tokens are scoped to the authenticated principal, or client IP for anonymous development flows.
- `VULNORAIQ_CSRF_TOKEN_TTL` defaults to `300` seconds.
- Expired tokens are cleaned periodically.

### Rate limiting and scan concurrency

```bash
export VULNORAIQ_RATE_LIMIT_WINDOW=60
export VULNORAIQ_RATE_LIMIT_MAX=60
export VULNORAIQ_MAX_CONCURRENT_SCANS=5
export VULNORAIQ_SCAN_QUEUE_LIMIT=20
```

The application rate limiter is in-memory and per-process. For public exposure or multi-instance deployment, enforce rate limiting at the reverse proxy/WAF layer and use a shared rate-limit backend in a future architecture.

### Security headers

Normal and error responses include:

- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: DENY`
- `X-XSS-Protection: 0`
- `Strict-Transport-Security` when appropriate for trusted TLS/proxy context
- `Referrer-Policy: strict-origin-when-cross-origin`
- strict `Content-Security-Policy`
- `Permissions-Policy: camera=(), microphone=(), geolocation=()`

## Persistence

SQLite is the default and production-supported backend for controlled internal deployment.

```bash
export VULNORAIQ_JOB_STORE_BACKEND=sqlite
export VULNORAIQ_JOB_STORE_PATH=/data/jobs.db
```

SQLite settings applied by the job store:

- WAL mode
- foreign keys enabled
- busy timeout
- schema version table
- `jobs` and `events` tables

JSON persistence is legacy/development only:

```bash
export VULNORAIQ_JOB_STORE_BACKEND=json
```

Production validation rejects the JSON backend.

## Audit logging

Audit events are emitted as JSON lines on the `vulnoraiq.audit` logger. Events include request ID, user, role, authentication state, client IP, method, path, status, and detail.

Example:

```json
{"timestamp":"2026-06-22T10:30:00+00:00","event":"scan_created","request_id":"abc123","user":"env-admin","role":"admin","authenticated":"true","client_ip":"10.0.0.10","method":"POST","path":"/api/scans","status":202,"detail":"target=demo profile=baseline job_id=..."}
```

Audit logs must not include auth tokens, CSRF tokens, request bodies, secrets, or full report contents.

Recommended operations:

- ship logs to SIEM using journald, Filebeat, Fluent Bit, or your standard log shipper
- retain audit logs according to internal policy
- alert on repeated `auth_failure`, `authz_failure`, `csrf_failure`, `rate_limit_exceeded`, `artifact_traversal_attempt`, and `scan_queue_full`

## Reverse proxy and TLS

The built-in HTTP server should run behind a reverse proxy for controlled enterprise deployment.

### nginx example

```nginx
limit_req_zone $binary_remote_addr zone=vulnoraiq:10m rate=30r/s;

server {
    listen 443 ssl;
    server_name vulnoraiq.example.com;

    ssl_certificate /etc/ssl/certs/vulnoraiq.crt;
    ssl_certificate_key /etc/ssl/private/vulnoraiq.key;

    limit_req zone=vulnoraiq burst=10 nodelay;

    location / {
        proxy_pass http://127.0.0.1:8787;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_buffering off;
        proxy_cache off;
        proxy_read_timeout 86400s;
    }
}
```

### Caddy example

```caddy
vulnoraiq.example.com {
    reverse_proxy 127.0.0.1:8787 {
        header_up X-Real-IP {remote_host}
        header_up X-Forwarded-For {remote_host}
        header_up X-Forwarded-Proto {scheme}
    }
}
```

## Metrics and monitoring

- `/healthz` — liveness probe
- `/readyz` — readiness probe
- `/metrics` — Prometheus-format metrics, auth-protected by default via `VULNORAIQ_METRICS_AUTH_REQUIRED=true`

Example authenticated metrics scrape:

```bash
curl -H "X-VulnoraIQ-Token: $VULNORAIQ_ADMIN_TOKEN" http://127.0.0.1:8787/metrics
```

Useful metrics include auth failures, authorization failures, CSRF failures, rate-limit blocks, scans created/completed/failed, active scans, artifact downloads, oversized requests, scan queue full, internal errors, uptime, and build info.

## Backup and restore

### Backup

```bash
python scripts/backup_sqlite_store.py \
  /data/jobs.db \
  /data/backups/jobs-$(date +%Y%m%d-%H%M%S).db \
  --compress \
  --validate \
  --retention 90
```

### Restore

```bash
# Stop the service first.
python scripts/restore_sqlite_store.py \
  /data/backups/jobs-YYYYMMDD-HHMMSS.db.gz \
  /data/jobs.db \
  --compressed \
  --validate
```

### Restore drill

At least once per release candidate:

1. Create a backup from a test database.
2. Restore to a new temporary DB path.
3. Run validation.
4. Start the Web UI against the restored DB.
5. Confirm scan history and artifacts behave as expected.

## Filesystem permissions

```bash
sudo useradd --system --no-create-home vulnoraiq || true
sudo mkdir -p /data /data/reports /data/backups
sudo chown -R vulnoraiq:vulnoraiq /data
sudo chmod 750 /data
```

The runtime user needs write access to `/data/jobs.db` and `/data/reports`. Configuration should be read-only for the runtime user where possible.

## Secrets management

- Never bake secrets into Docker images.
- Never commit real `.env.production` files.
- Use environment variables or a secret manager.
- Rotate tokens by generating a new token, updating runtime configuration, restarting the service, and invalidating the old value.
- Keep `.env.production.example` placeholder-only.

## systemd example

```ini
[Unit]
Description=VulnoraIQ Web UI
After=network.target

[Service]
Type=simple
User=vulnoraiq
Group=vulnoraiq
WorkingDirectory=/app
Environment=VULNORAIQ_ENV=production
Environment=VULNORAIQ_AUTH_ENABLED=true
Environment=VULNORAIQ_ADMIN_TOKEN=replace-with-secret-manager-value
Environment=VULNORAIQ_JOB_STORE_BACKEND=sqlite
Environment=VULNORAIQ_JOB_STORE_PATH=/data/jobs.db
Environment=VULNORAIQ_WEB_OUTPUT_ROOT=/data/reports
ExecStart=/usr/local/bin/vulnoraiq-web --host 127.0.0.1 --port 8787
Restart=on-failure
RestartSec=5
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

## Environment variable reference

| Variable | Default | Description |
| --- | --- | --- |
| `VULNORAIQ_ENV` | — | Set to `production` for production-mode validation |
| `VULNORAIQ_HOST` | `127.0.0.1` | Bind address |
| `VULNORAIQ_PORT` | `8787` | Bind port |
| `VULNORAIQ_AUTH_ENABLED` | `true` | Enable authentication |
| `VULNORAIQ_AUTH_MODE` | `token` | `token` or `trusted_proxy` |
| `VULNORAIQ_ADMIN_TOKEN` | — | Admin token, required in production, min 20 chars |
| `VULNORAIQ_ANALYST_TOKEN` | — | Analyst token |
| `VULNORAIQ_VIEWER_TOKEN` | — | Viewer token |
| `VULNORAIQ_LOG_LEVEL` | `INFO` | `DEBUG`, `INFO`, `WARNING`, or `ERROR` |
| `VULNORAIQ_CONFIG_DIR` | `config` | Config directory |
| `VULNORAIQ_WEB_USERS_PATH` | `config/web_users.yaml` | Development file-auth fallback path |
| `VULNORAIQ_WEB_OUTPUT_ROOT` | `reports/output/webui` | Report output root |
| `VULNORAIQ_JOB_STORE_BACKEND` | `sqlite` | `sqlite` or development-only `json` |
| `VULNORAIQ_JOB_STORE_PATH` | `reports/output/webui/jobs.db` | Store path |
| `VULNORAIQ_MAX_REQUEST_BODY` | `10485760` | Max request body in bytes |
| `VULNORAIQ_RATE_LIMIT_WINDOW` | `60` | Rate-limit window in seconds |
| `VULNORAIQ_RATE_LIMIT_MAX` | `60` | Max requests per window per IP |
| `VULNORAIQ_CSRF_TOKEN_TTL` | `300` | CSRF token lifetime in seconds |
| `VULNORAIQ_TRUST_PROXY_HEADERS` | `false` | Trust proxy-provided client IP/identity headers |
| `VULNORAIQ_TRUSTED_PROXY_CIDRS` | — | Comma-separated trusted proxy CIDRs |
| `VULNORAIQ_METRICS_AUTH_REQUIRED` | `true` | Require auth for `/metrics` |
| `VULNORAIQ_MAX_CONCURRENT_SCANS` | `5` | Max active scans |
| `VULNORAIQ_SCAN_QUEUE_LIMIT` | `20` | Queue capacity before rejection |

## Production checklist

- [ ] Set `VULNORAIQ_ENV=production`.
- [ ] Set a strong `VULNORAIQ_ADMIN_TOKEN`.
- [ ] Keep `VULNORAIQ_AUTH_ENABLED=true`.
- [ ] Use SQLite backend and persistent `/data` volume.
- [ ] Validate runtime config with `scripts/validate_runtime_production_config.py`.
- [ ] Run behind TLS-terminating reverse proxy for any non-local access.
- [ ] Configure `VULNORAIQ_TRUST_PROXY_HEADERS` and `VULNORAIQ_TRUSTED_PROXY_CIDRS` only for trusted proxies.
- [ ] Configure proxy/WAF rate limiting for exposed deployments.
- [ ] Ship audit logs to SIEM/log management.
- [ ] Set up periodic SQLite backups and test restore.
- [ ] Run `scripts/validate_production_testing_readiness.py` before release.
- [ ] Run Docker smoke test if deploying via container.
- [ ] Review [`ASSESSMENT_ASSURANCE.md`](ASSESSMENT_ASSURANCE.md) before sharing scan results externally.

## Explicit non-goals for `0.2.0`

`0.2.0` does not claim:

- public SaaS readiness
- multi-tenant isolation
- HA database operation
- distributed rate limiting
- built-in OIDC/JWT validation
- built-in WAF/CDN/DDoS protection
- certified VAPT-grade scanner assurance