# GenAI Security Implementation Plan

This folder defines VulnoraIQ's implementation plan for GenAI data-security and governance testing beyond the existing OWASP LLM 2025 category files.

> **Status:** source-confirmed planning.  
> **Scope:** OWASP GenAI Data Security Risks and Mitigations 2026, OWASP GenAI COMPASS operating model, and VulnoraIQ GenAI evidence/reporting extensions.  
> **Boundary:** the categories are source-confirmed, but VulnoraIQ does not yet claim active production-validated GenAI detection coverage for every category.

## Source documents reviewed

- `docs/owasp-documents/OWASP-GenAI-COMPASS-RunBook-1.0.pdf` — confirms COMPASS uses an Observe/Orient/Decide/Act workflow and integrates MITRE ATT&CK, ATLAS, NAVIGATOR, D3FEND, CAPEC, STIX, CVE, CWE, and a 5-point scoring method.
- `docs/owasp-documents/OWASP-GenAI-Data-Security-Risks-and-Mitigations-2026-v1.0.pdf` — confirms GenAI data-security categories `DSGAI01` through `DSGAI21` in the visible table of contents.
- existing VulnoraIQ `docs/owasp/` LLM implementation specs
- `docs/owasp/OWASP_TO_MITRE_ATLAS_CROSSWALK.md`

## Source note

The GenAI Data Security document's narrative text references a `DSGAI01–DSGAI25` taxonomy, while the accessible table of contents confirms `DSGAI01–DSGAI21`. VulnoraIQ tracks `DSGAI01–DSGAI21` as source-confirmed and keeps the `DSGAI22–DSGAI25` discrepancy open until a complete extracted source list is available.

## Confirmed GenAI data-security coverage areas

| OWASP ID | GenAI data-security risk | Current status | Related OWASP LLM categories | Primary evidence surfaces |
| --- | --- | --- | --- | --- |
| DSGAI01 | Sensitive Data Leakage | Planning | LLM02, LLM07 | prompt, response, report artifact, logs |
| DSGAI02 | Agent Identity & Credential Exposure | Planning | LLM02, LLM06 | tool trace, credential scope, agent identity metadata |
| DSGAI03 | Shadow AI & Unsanctioned Data Flows | Planning | LLM02, LLM03, LLM06 | provider inventory, network/service discovery, policy evidence |
| DSGAI04 | Data, Model & Artifact Poisoning | Planning | LLM03, LLM04, LLM08 | source manifest, corpus delta, model/artifact hash |
| DSGAI05 | Data Integrity & Validation Failures | Planning | LLM04, LLM05, LLM08 | schema validation, freshness, provenance, source approval |
| DSGAI06 | Tool, Plugin & Agent Data Exchange Risks | Planning | LLM02, LLM06 | tool trace, connector manifest, data-flow evidence |
| DSGAI07 | Data Governance, Lifecycle & Classification for AI Systems | Planning | all LLM categories | classification labels, lineage, retention, approval evidence |
| DSGAI08 | Non-Compliance & Regulatory Violations | Planning | LLM02, LLM03, LLM04, LLM06 | policy mapping, data residency, regulatory control evidence |
| DSGAI09 | Multimodal Capture & Cross-Channel Data Leakage | Planning | LLM02, LLM05 | multimodal input metadata, output artifact, DLP findings |
| DSGAI10 | Synthetic Data, Anonymization & Transformation Pitfalls | Planning | LLM02, LLM04, LLM09 | synthetic-data metadata, transformation record, re-identification risk evidence |
| DSGAI11 | Cross-Context & Multi-User Conversation Bleed | Planning | LLM02, LLM08 | session memory, tenant/user boundary, conversation context |
| DSGAI12 | Unsafe Natural-Language Data Gateways (LLM-to-SQL/Graph) | Planning | LLM05, LLM06 | generated query, schema allowlist, DB/tool trace |
| DSGAI13 | Vector Store Platform Data Security | Planning | LLM02, LLM08 | vector store metadata, ACLs, tenant index, embedding trace |
| DSGAI14 | Excessive Telemetry & Monitoring Leakage | Planning | LLM02, LLM07 | logs, traces, audit events, monitoring exports |
| DSGAI15 | Over-Broad Context Windows & Prompt Over-Sharing | Planning | LLM01, LLM02, LLM07 | context assembly, trust-domain segments, prompt metadata |
| DSGAI16 | Endpoint & Browser Assistant Overreach | Planning | LLM02, LLM06 | browser/endpoint permission, local context, tool trace |
| DSGAI17 | Data Availability & Resilience Failures in AI Pipelines | Planning | LLM08, LLM09, LLM10 | vector/index availability, failover state, backup/restore validation |
| DSGAI18 | Inference & Data Reconstruction | Planning | LLM02, LLM08 | inference probe, embedding/model output, privacy-risk evidence |
| DSGAI19 | Human-in-the-Loop & Labeler Overexposure | Planning | LLM02, LLM06 | reviewer workflow, label queue, masking/approval evidence |
| DSGAI20 | Model Exfiltration & IP Replication | Planning | LLM02, LLM03 | model artifact metadata, access logs, extraction probe |
| DSGAI21 | Disinformation & Integrity Attacks via Data Poisoning | Planning | LLM04, LLM09 | poisoned-source scenario, trust score, unsupported claim evidence |

## Relationship to existing LLM tests

The existing LLM test plan focuses on model, RAG, agent, output, and resource-risk categories. The GenAI plan adds organisation-level and data-security controls:

- data asset discovery and inventory
- data classification and policy binding
- data flow mapping and lineage
- GenAI/AI data bill of materials concepts
- access governance and entitlement posture for agents
- lifecycle, retention, and deletion
- provider data handling and residency
- report/log/telemetry artifact hygiene
- multimodal data capture and leakage
- vector-store platform security
- human-review and labeler exposure controls

## COMPASS alignment

VulnoraIQ should implement GenAI assessment workflow support that follows the COMPASS loop:

| COMPASS phase | VulnoraIQ implementation implication |
| --- | --- |
| Observe | Inventory AI assets, data stores, providers, prompts, context windows, tools, logs, and RAG/vector stores. |
| Orient | Map observed assets to OWASP LLM, DSGAI, Agentic ASI, MITRE ATLAS, incidents, and control gaps. |
| Decide | Prioritise red-team tests, mitigations, compensating controls, and implementation backlog using risk scoring. |
| Act | Generate reports, roadmap items, tickets, control evidence, and retest scenarios. |

## Maturity rule

A GenAI control area remains `Planning` until:

1. a safe local fixture exists,
2. an evaluator or validator exists,
3. reports include structured evidence,
4. docs explain what the result proves and does not prove,
5. CI validates the behaviour.

A GenAI area can move to `Working starter` when it has secure, vulnerable, ambiguous, and edge-case scenarios plus report evidence and false-positive/false-negative guidance.

## Files

- [`PRODUCTION_READINESS_PLAN.md`](PRODUCTION_READINESS_PLAN.md) — phased implementation plan
- [`../owasp/OWASP_TO_MITRE_ATLAS_CROSSWALK.md`](../owasp/OWASP_TO_MITRE_ATLAS_CROSSWALK.md) — OWASP/GenAI/Agentic to MITRE ATLAS mapping

## Next steps

1. Add scenario manifests under `benchmarks/fixtures/genai/` for `DSGAI01–DSGAI21`.
2. Add GenAI evaluator composition in `core/genai_evaluators.py` or an equivalent module.
3. Add machine-readable mapping in `config/owasp_mitre_atlas_crosswalk.yaml`.
4. Add report and dashboard coverage for GenAI data-security controls.
5. Track the `DSGAI01–DSGAI25` vs `DSGAI01–DSGAI21` source discrepancy until resolved.