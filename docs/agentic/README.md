# Agentic Applications Security Implementation Plan

This folder defines VulnoraIQ's implementation plan for OWASP Top 10 for Agentic Applications testing.

> **Status:** source-confirmed planning.  
> **Scope:** AI agents, tool use, planning, memory, delegation, inter-agent workflows, identity, runtime governance, and assurance evidence.  
> **Boundary:** the `ASI01–ASI10` categories are source-confirmed, but VulnoraIQ does not yet claim active production-validated Agentic detection coverage for every category.

## Source documents reviewed

- `docs/owasp-documents/OWASP-Top-10-for-Agentic-Applications-2026-12.6.pdf` — confirms the OWASP Agentic Top 10 `ASI01–ASI10` category names.
- `docs/owasp-documents/OWASP-Top10-for-Agentic-Applications_AIUC-1-Crosswalk-May26.pdf` — confirms AIUC-1 crosswalk methodology, Primary/Secondary relevance, and strategic gaps.
- `docs/owasp-documents/State-of-Agentic-AI-Security-and-Governance-v2.01.pdf` — confirms governance context, adoption-tier prioritisation, agent identity/NHI, AI SBOM/provenance, runtime governance, and incident evidence.
- existing VulnoraIQ `docs/owasp/LLM06_EXCESSIVE_AGENCY.md`
- existing VulnoraIQ `agent_testing/` manifests and scenarios
- `docs/owasp/OWASP_TO_MITRE_ATLAS_CROSSWALK.md`

## Confirmed OWASP Agentic categories

| OWASP ID | Agentic risk | Current status | Related OWASP LLM categories | Primary evidence surfaces |
| --- | --- | --- | --- | --- |
| ASI01 | Agent Goal Hijack | Planning | LLM01, LLM06, LLM07 | goal, prompt, retrieved context, tool description, plan trace |
| ASI02 | Tool Misuse and Exploitation | Planning | LLM05, LLM06, LLM10 | tool manifest, tool call, argument trace, policy decision |
| ASI03 | Identity and Privilege Abuse | Planning | LLM02, LLM06 | agent identity, credential scope, delegation trace, auth context |
| ASI04 | Agentic Supply Chain Vulnerabilities | Planning | LLM03, LLM06 | tool/framework/provider manifest, version/provenance, prompt/template source |
| ASI05 | Unexpected Code Execution (RCE) | Planning | LLM05, LLM06 | code/tool execution trace, sandbox status, file/process action |
| ASI06 | Memory & Context Poisoning | Planning | LLM01, LLM04, LLM06, LLM08 | memory trace, context diff, state store, source metadata |
| ASI07 | Insecure Inter-Agent Communication | Planning | LLM02, LLM06 | agent identity, A2A/MCP/ACP message, trust boundary, protocol metadata |
| ASI08 | Cascading Failures | Planning | LLM06, LLM10 | propagation trace, dependency graph, circuit breaker, blast-radius control |
| ASI09 | Human-Agent Trust Exploitation | Planning | LLM05, LLM06, LLM09 | human approval, user-facing output, high-risk action flag, review evidence |
| ASI10 | Rogue Agents | Planning | LLM03, LLM06, LLM10 | agent registry, behaviour drift, kill switch, containment/quarantine evidence |

## Relationship to existing LLM tests

Existing VulnoraIQ LLM tests already cover starter forms of:

- prompt injection
- sensitive information disclosure
- supply chain
- data/model poisoning
- improper output handling
- excessive agency
- system prompt leakage
- vector/embedding weaknesses
- misinformation
- unbounded consumption

The Agentic plan expands this into agent runtime-specific testing:

- goal hijack and plan manipulation
- tool invocation and connector permissioning
- agent identity, non-human identity, and delegated credentials
- memory writes and state transitions
- inter-agent and agent-to-tool communication
- high-impact action approval
- traceability and non-repudiation
- bounded autonomy and budget controls
- cascading failure and blast-radius limits
- rogue-agent detection and containment

## AIUC-1 and governance implications

The AIUC-1 crosswalk states that mappings identify relevance, not sufficiency. VulnoraIQ uses the same rule: an ASI mapping does not mean the check fully mitigates the risk.

Priority governance gaps to model in VulnoraIQ:

- per-agent cryptographic identity and signed behavioural manifests
- mutual authentication between agents
- kill switches and runtime containment
- circuit breakers and blast-radius caps
- planner/executor isolation
- runtime monitoring of malicious activity inside the agent
- AI service entitlement controls
- tool manifests, prompt version control, AIBOM/SBOM/ML-BOM references, and schema controls

## Maturity rule

An Agentic category remains `Planning` until:

1. a safe local agent fixture exists,
2. a scenario manifest exists,
3. an evaluator or validator exists,
4. report evidence includes plan/tool/memory/action traces where relevant,
5. CI validates secure, vulnerable, ambiguous, and edge-case scenarios.

A category can move to `Working starter` when it has representative fixture coverage and operator-facing report language with explicit limitations.

## Files

- [`PRODUCTION_READINESS_PLAN.md`](PRODUCTION_READINESS_PLAN.md) — phased implementation plan
- [`../owasp/OWASP_TO_MITRE_ATLAS_CROSSWALK.md`](../owasp/OWASP_TO_MITRE_ATLAS_CROSSWALK.md) — OWASP/GenAI/Agentic to MITRE ATLAS mapping

## Next steps

1. Add agentic scenario manifests under `benchmarks/fixtures/agentic/` for `ASI01–ASI10`.
2. Expand `agent_testing/` with safe local agent loops and tool traces.
3. Add `core/agentic_evaluators.py` or equivalent evaluator composition.
4. Add report and dashboard coverage for agentic risk areas.
5. Add machine-readable ASI-to-MITRE ATLAS mappings.
6. Add governance/adoption-tier metadata from the State of Agentic AI Security and Governance report.