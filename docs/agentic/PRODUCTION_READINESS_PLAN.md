# Agentic Applications Production Readiness Plan

This document extends VulnoraIQ's OWASP LLM implementation plan into OWASP Top 10 for Agentic Applications testing.

> **Current status:** source-confirmed planning.  
> **Readiness claim:** no Agentic Application category should be marked `Working` until fixtures, evaluators, evidence, reporting, and CI gates are implemented.

## Current baseline

VulnoraIQ already has:

- `LLM06: Excessive Agency` starter planning and oracle coverage
- agent runtime governance docs and starter scenarios under `agent_testing/`
- policy exceptions and approval evidence concepts
- structured scan results and report generation
- Web UI production controls for controlled internal deployment
- MITRE ATLAS planning register and OWASP crosswalk
- source-confirmed OWASP Agentic Top 10 categories `ASI01–ASI10`

Agentic Application work should extend these into runtime behaviour testing rather than duplicating the existing LLM test plan.

## Source-confirmed ASI category list

| OWASP ID | Category |
| --- | --- |
| ASI01 | Agent Goal Hijack |
| ASI02 | Tool Misuse and Exploitation |
| ASI03 | Identity and Privilege Abuse |
| ASI04 | Agentic Supply Chain Vulnerabilities |
| ASI05 | Unexpected Code Execution (RCE) |
| ASI06 | Memory & Context Poisoning |
| ASI07 | Insecure Inter-Agent Communication |
| ASI08 | Cascading Failures |
| ASI09 | Human-Agent Trust Exploitation |
| ASI10 | Rogue Agents |

## Maturity ladder

| Level | Meaning | Required evidence |
| --- | --- | --- |
| Planning | Risk/control area identified but no active check. | Source doc reference, candidate OWASP/ATLAS mapping, owner. |
| Working-alpha starter | One safe local fixture and minimal evaluator exist. | Good/bad fixture, minimal plan/tool evidence, unit test. |
| Working starter | Representative agent scenario set and report evidence exist. | secure/vulnerable/ambiguous/edge-case scenarios, report fields, negative controls. |
| Working | Stable confidence, benchmark thresholds, false-positive handling, and operator guidance exist. | CI gates, benchmark thresholds, evidence schema, reviewed docs. |
| Production-ready candidate | Authorised validation guidance, runtime safety guardrails, and governance approvals exist. | validation runbook, approval gates, evidence retention policy, release sign-off. |

## Phase AGENTIC-1 — Scenario manifests

Create safe scenario manifests under:

```text
benchmarks/fixtures/agentic/
```

Required fields:

- `scenario_id`
- `agentic_id`: ASI ID
- `risk_area`
- `fixture_type`: secure, vulnerable, ambiguous, edge_case
- `adoption_tier`: AT0, AT1, AT2, AT3, AT4, AT5, AT6, AT7
- `agent_loop`: plan, act, observe, reflect, delegate
- `tool_surface`: none, read_only, write, external_network, credentialed, high_impact
- `memory_surface`: none, session, long_term, vector_store, external_state
- `input_fixture`
- `expected_secure_outcome`
- `expected_vulnerable_signal`
- `required_evidence_fields`
- `mitre_atlas_tactics`
- `manual_review_required`

Minimum scenarios:

| OWASP ID | Required scenarios |
| --- | --- |
| ASI01 | direct goal hijack, indirect retrieved instruction, tool-description injection, high-impact action gated by approval |
| ASI02 | allowed read-only tool, blocked high-impact tool, over-scoped connector, unsafe tool argument |
| ASI03 | scoped identity, inherited credential abuse, delegated privilege escalation, expired/standing credential |
| ASI04 | trusted tool/framework manifest, poisoned tool description, unknown connector owner, version drift |
| ASI05 | safe sandboxed action, unexpected file write, generated code execution, unsafe project config execution |
| ASI06 | safe memory write, malicious memory seed, stale poisoned memory, context poisoning |
| ASI07 | authenticated agent communication, spoofed agent card, unsigned agent handoff, protocol trust-boundary failure |
| ASI08 | bounded dependency failure, cascading tool failure, multi-agent propagation, missing circuit breaker |
| ASI09 | safe human approval, deceptive output, overtrust prompt, high-risk output without flag |
| ASI10 | registered agent, rogue unregistered agent, behavioural drift, missing kill switch/quarantine |

## Phase AGENTIC-2 — Evaluator composition

Potential module:

```text
core/agentic_evaluators.py
```

Evaluator types:

- goal integrity evaluator
- instruction hierarchy evaluator
- indirect-instruction boundary evaluator
- tool permission evaluator
- tool manifest/provenance evaluator
- identity and delegated credential evaluator
- inter-agent communication evaluator
- memory integrity evaluator
- code-execution/sandbox evaluator
- plan safety evaluator
- approval checkpoint evaluator
- loop/resource budget evaluator
- cascade/blast-radius evaluator
- rogue-agent containment evaluator
- action trace completeness evaluator
- data-flow and exfiltration evaluator
- policy conflict evaluator
- manual-review routing evaluator

Each evaluator should return:

- `status`: pass, warn, fail, review
- `confidence`
- `reason`
- `evidence_fields`
- `agent_loop_stage`
- `tool_surface`
- `memory_surface`
- `identity_surface`
- `adoption_tier`
- `manual_review_required`

## Phase AGENTIC-3 — Evidence schema expansion

Extend report JSON and finding evidence with:

- `agentic_id`
- `agentic_risk_area`
- `adoption_tier`
- `agent_type`
- `agent_loop_stage`
- `goal`
- `plan_summary`
- `policy_decision`
- `tool_name`
- `tool_permission_scope`
- `tool_provenance_status`
- `identity_surface`
- `credential_scope`
- `communication_protocol`
- `action_type`
- `approval_required`
- `approval_status`
- `memory_surface`
- `memory_write_status`
- `delegation_target`
- `delegation_trust_status`
- `loop_budget_status`
- `cost_budget_status`
- `cascade_control_status`
- `containment_status`
- `trace_completeness_status`
- `mitre_atlas_tactics`
- `manual_review_reason`

## Phase AGENTIC-4 — Safe local agent fixtures

Add or extend fixtures under `agent_testing/` and `examples/local_demo_targets/`.

Fixtures must avoid real external action and use simulated tools only:

- `safe_read_tool`
- `blocked_write_tool`
- `credentialed_tool_stub`
- `network_tool_stub`
- `approval_required_tool`
- `memory_write_stub`
- `delegate_to_agent_stub`
- `costly_loop_stub`
- `rogue_agent_stub`
- `agent_card_spoof_stub`
- `sandboxed_code_stub`

Each tool should emit structured traces without performing real external calls.

## Phase AGENTIC-5 — Reports and dashboards

Reports must explain:

- which ASI category was tested
- what agent behaviour was tested
- which loop stage was affected
- which tool/memory/delegation/identity surface was involved
- whether a real action occurred or a simulated action was blocked
- whether approval was required and present
- whether traceability was complete
- whether data left an approved boundary
- why human review is required
- what the finding does not prove

Dashboard additions:

- Agentic risk coverage table
- ASI-to-MITRE ATLAS coverage view
- adoption-tier risk prioritisation view
- tool/action surface coverage
- memory/state integrity status
- agent identity and NHI status
- inter-agent communication status
- approval-gate status
- loop/resource-budget status
- cascade/blast-radius status
- trace completeness status

## Phase AGENTIC-6 — Governance and adoption-tier integration

The State of Agentic AI Security and Governance report prioritises ASI risks by adoption tier, from Shadow AI to external/multi-agent orchestration. VulnoraIQ should capture adoption tier in each agentic scenario and use it to prioritise controls.

| Adoption tier | VulnoraIQ prioritisation |
| --- | --- |
| AT0 Shadow AI | Discovery, DLP, acceptable use, visibility, ASI01/ASI06/ASI09 starter checks. |
| AT1–AT2 Vendor/Platform | Input filtering, output review, scoped permissions, data classification. |
| AT3 Citizen-Developer | Flow inventory, connector governance, maker permissions, ASI02/ASI03/ASI05. |
| AT4–AT5 Code-Exec/Custom | Sandboxing, code signing, least privilege, tool boundary enforcement, ASI05. |
| AT6–AT7 External/Multi-Agent | Agent identity, MCP/A2A auth, supply-chain verification, cascade limits, full ASI01–ASI10 surface. |

## Phase AGENTIC-7 — CI and release gates

Add gates that fail if:

- `ASI01–ASI10` categories lack planning rows
- scenario manifests are missing required fields
- vulnerable agent fixtures are missed
- secure fixtures are flagged high-confidence without reason
- high-impact actions lack approval evidence
- tool traces or memory traces are missing for relevant scenarios
- identity and communication evidence is missing for ASI03/ASI07/ASI10
- report output lacks ASI ID, MITRE tactic, confidence, and manual-review fields
- docs and machine-readable crosswalk drift

## Agentic implementation matrix

| OWASP ID | Current baseline | Next implementation focus | Working target |
| --- | --- | --- | --- |
| ASI01 | LLM01/LLM07 starter prompt boundary checks. | Goal hijack, indirect instruction, intent gate, approval scenarios. | Agent refuses or isolates hijacked goals with traceable boundary evidence. |
| ASI02 | LLM06 starter tool governance. | Tool scopes, argument validation, semantic tool checks, usage budgets. | Unsafe or over-scoped tool use is blocked or flagged before action. |
| ASI03 | Auth and role concepts exist. | Agent identity, delegated credentials, JIT access, privilege escalation. | Identity/privilege abuse is detected with credential-scope evidence. |
| ASI04 | LLM03 provenance concepts. | Tool/framework/provider manifests, version drift, prompt/template provenance. | Unknown or poisoned dependencies are detected before invocation. |
| ASI05 | LLM05/LLM06 output/action checks. | Code execution sandbox, file-write protection, generated-config execution. | Unexpected code execution is blocked or simulated safely. |
| ASI06 | LLM04/LLM08 source trust. | Memory integrity, context poisoning, plan tampering, rollback. | Poisoned memory/context is detected and routed to review. |
| ASI07 | Limited delegation modelling. | Agent communication identity, signed cards/manifests, protocol validation. | Spoofed or unauthenticated agent communication is flagged. |
| ASI08 | LLM10 resource budgets. | Circuit breakers, blast-radius limits, cascade propagation simulations. | Cascading failures are bounded and evidenced. |
| ASI09 | Approval evidence exists. | Human trust exploitation, deceptive output, high-risk output flagging. | Human-agent overtrust risks are flagged and routed to review. |
| ASI10 | No rogue-agent evaluator yet. | Registry, discovery, behavioural drift, kill switch, containment. | Rogue agents are detected or quarantined in simulated scenarios. |

## Immediate backlog

1. Create `benchmarks/fixtures/agentic/` manifests for `ASI01–ASI10`.
2. Add simulated safe agent tools and traces.
3. Add `core/agentic_evaluators.py`.
4. Extend evidence schema for plan/tool/memory/delegation/identity/action traces.
5. Add agentic dashboard coverage table.
6. Add report guidance blocks for agentic findings.
7. Add machine-readable ASI-to-ATLAS mapping.
8. Add CI gates for agentic manifests and report fields.
9. Update `ASSESSMENT_ASSURANCE.md` after the first agentic evaluator batch lands.
10. Add adoption-tier prioritisation to findings and dashboard views.

## Claim rule

Do not describe Agentic Application coverage as `Working` until fixtures, evaluators, evidence, reports, and CI gates exist for the source-confirmed `ASI01–ASI10` categories.