# Docker AI Agent Runtime

VulnoraIQ can now start a real AI agent in Docker from the WebUI and register that running container as a scan target. This replaces the old demo-only workflow for local production-style testing.

## What this provides

- A **Docker AI agent runtime** panel in the WebUI.
- A built-in Docker agent bridge at `docker/agents/http-llm-agent`.
- User-selected LLM backend support:
  - Ollama-style `/api/generate`
  - OpenAI-compatible `/v1/chat/completions`
  - Generic HTTP JSON
- Custom Docker agent support for native AI agent images.
- Automatic target registration through `reports/output/webui/runtime_targets.yaml`.
- Scan execution against the live Docker-hosted target.

## Requirements

- Docker must be installed and available on `PATH`.
- The WebUI should be launched with the local launcher:

```bash
python scripts/launch_webui.py
```

- Only test systems that you own or are explicitly authorised to test.

## Built-in Docker AI agent

The included agent image is built locally from:

```text
docker/agents/http-llm-agent
```

The WebUI builds and runs it as:

```text
vulnoraiq/http-llm-agent:local
```

It exposes:

```text
GET  /healthz
POST /agent
```

VulnoraIQ registers the running container as a normal `http_json` target. After the runtime starts, the WebUI reloads and the new target appears in the Target selector as something like:

```text
agent_1a2b3c4d5e
```

## LLM settings

The runtime accepts these WebUI inputs:

| Setting | Purpose |
| --- | --- |
| LLM provider | `ollama`, `openai_compatible`, `http_json`, or native image default |
| Model | Model name passed to the selected provider |
| LLM base URL | Backend endpoint base URL, for example `http://host.docker.internal:11434` |
| API key or token | Optional runtime-only secret passed to the container environment |
| System prompt | Optional system instruction for the included bridge agent |
| Docker image override | Optional image override; required for custom native images |
| Container port | Port exposed inside the container |
| Host port | Optional fixed loopback port; otherwise VulnoraIQ chooses one |
| Endpoint path | Target endpoint path, usually `/agent` |

## Custom native Docker agents

Use **Custom Docker AI Agent** when the agent already has its own native runtime image. The image must expose a health endpoint and an HTTP endpoint compatible with the selected target contract.

Default contract:

```http
POST /agent
Content-Type: application/json

{
  "prompt": "...",
  "input": "..."
}
```

Expected response can be plain text or JSON containing one of:

```text
output, response, text, message, content
```

## Runtime target registration

Running agents are written to:

```text
reports/output/webui/runtime_targets.yaml
```

The scanner merges this file at scan time, so Docker-hosted agents become first-class scan targets without editing `config/targets.yaml`.

## Stop runtime

The WebUI Stop button removes the Docker container and updates runtime target registration. Stopped agents are no longer shown as scan targets after the WebUI reloads.

## Security notes

- Docker runtime management is restricted to runtime-management permission.
- The local launcher runs on loopback by default.
- Production/shared deployments must enable authentication and configure an admin token.
- API keys are passed to the container environment at runtime and are not written into runtime target YAML.
