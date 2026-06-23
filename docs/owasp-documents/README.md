# OWASP Source Document Review Index

This folder stores source PDFs used to expand VulnoraIQ beyond the current OWASP LLM 2025 starter implementation.

> **Status:** category extraction completed for GenAI Data Security and Agentic Top 10.  
> **Rule:** category names are source-confirmed, but active VulnoraIQ coverage still requires fixtures, evaluators, evidence schema, report output, and CI gates.

## Source documents

| Source PDF | Review purpose | Target planning docs | Current extraction status |
| --- | --- | --- | --- |
| `OWASP-GenAI-COMPASS-RunBook-1.0.pdf` | Governance/runbook controls for GenAI assessment and operating model. | `docs/genai/README.md`, `docs/genai/PRODUCTION_READINESS_PLAN.md` | Reviewed for OODA/COMPASS workflow and framework alignment. |
| `OWASP-GenAI-Data-Security-Risks-and-Mitigations-2026-v1.0.pdf` | Data-security risk categories, mitigations, and evidence requirements. | `docs/genai/README.md`, `docs/genai/PRODUCTION_READINESS_PLAN.md`, `docs/owasp/OWASP_TO_MITRE_ATLAS_CROSSWALK.md` | `DSGAI01–DSGAI21` category names extracted from accessible table of contents. Narrative mentions `DSGAI01–DSGAI25`; discrepancy remains tracked. |
| `OWASP-Top-10-for-Agentic-Applications-2026-12.6.pdf` | Official Agentic Application category IDs/names/descriptions. | `docs/agentic/README.md`, `docs/agentic/PRODUCTION_READINESS_PLAN.md`, crosswalk | `ASI01–ASI10` category names extracted and mapped. |
| `OWASP-Top10-for-Agentic-Applications_AIUC-1-Crosswalk-May26.pdf` | AIUC crosswalk and relationship to Agentic Top 10 categories. | `docs/agentic/PRODUCTION_READINESS_PLAN.md`, crosswalk | Reviewed for Primary/Secondary relevance methodology and strategic gaps. |
| `State-of-Agentic-AI-Security-and-Governance-v2.01.pdf` | Governance, lifecycle, oversight, and assurance context for agentic systems. | `docs/agentic/PRODUCTION_READINESS_PLAN.md`, `docs/ASSESSMENT_ASSURANCE.md` | Reviewed for governance maturity, adoption-tier prioritisation, agent identity/NHI, AI SBOM/provenance, and runtime governance themes. |

## Confirmed GenAI Data Security categories

| OWASP ID | Category |
| --- | --- |
| DSGAI01 | Sensitive Data Leakage |
| DSGAI02 | Agent Identity & Credential Exposure |
| DSGAI03 | Shadow AI & Unsanctioned Data Flows |
| DSGAI04 | Data, Model & Artifact Poisoning |
| DSGAI05 | Data Integrity & Validation Failures |
| DSGAI06 | Tool, Plugin & Agent Data Exchange Risks |
| DSGAI07 | Data Governance, Lifecycle & Classification for AI Systems |
| DSGAI08 | Non-Compliance & Regulatory Violations |
| DSGAI09 | Multimodal Capture & Cross-Channel Data Leakage |
| DSGAI10 | Synthetic Data, Anonymization & Transformation Pitfalls |
| DSGAI11 | Cross-Context & Multi-User Conversation Bleed |
| DSGAI12 | Unsafe Natural-Language Data Gateways (LLM-to-SQL/Graph) |
| DSGAI13 | Vector Store Platform Data Security |
| DSGAI14 | Excessive Telemetry & Monitoring Leakage |
| DSGAI15 | Over-Broad Context Windows & Prompt Over-Sharing |
| DSGAI16 | Endpoint & Browser Assistant Overreach |
| DSGAI17 | Data Availability & Resilience Failures in AI Pipelines |
| DSGAI18 | Inference & Data Reconstruction |
| DSGAI19 | Human-in-the-Loop & Labeler Overexposure |
| DSGAI20 | Model Exfiltration & IP Replication |
| DSGAI21 | Disinformation & Integrity Attacks via Data Poisoning |

## Confirmed OWASP Top 10 for Agentic Applications categories

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

## Review workflow for next pass

1. Extract deeper per-category descriptions, examples, and mitigations from each source PDF.
2. Add category-specific implementation docs for `DSGAI01–DSGAI21` and `ASI01–ASI10` where needed.
3. Add machine-readable mapping in `config/owasp_mitre_atlas_crosswalk.yaml`.
4. Add CI validation to detect drift between source docs, planning docs, crosswalk, and report schema.
5. Resolve or document the GenAI `DSGAI01–DSGAI25` narrative vs `DSGAI01–DSGAI21` table-of-contents discrepancy.

## Acceptance criteria for implementation coverage

A category is not `Working` until:

- exact source category name is captured,
- scenario manifest exists,
- safe fixture exists,
- evaluator or validator exists,
- structured evidence is emitted,
- report output explains limitations,
- MITRE ATLAS mapping is present,
- CI validates secure/vulnerable/ambiguous/edge-case behaviour,
- no documentation claims active coverage before implementation exists.