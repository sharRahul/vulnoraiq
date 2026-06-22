# GenAI Security Production Readiness Plan

This document extends VulnoraIQ's OWASP LLM implementation plan into GenAI data-security, governance, and operational controls.

> **Current status:** planning.  
> **Readiness claim:** no GenAI data-security category should be marked `Working` until source-category wording, fixtures, evaluators, evidence, reporting, and CI gates are implemented.

## Current baseline

VulnoraIQ already has:

- OWASP LLM 2025 starter oracle coverage
- deterministic evaluator primitives
- local good/bad fixture targets
- structured evidence and report generation
- production-ready controlled-internal Web UI platform controls
- MITRE ATLAS planning register and candidate OWASP mapping

GenAI data-security work should build on this baseline rather than creating a separate assessment path.

## Maturity ladder

| Level | Meaning | Required evidence |
| --- | --- | --- |
| Planning | Risk/control area is identified but not implemented. | Source doc reference, candidate OWASP/ATLAS mapping, owner. |
| Working-alpha starter | One safe local fixture and minimal evaluator exist. | Good/bad fixture, minimal evidence, unit test. |
| Working starter | Representative scenario set and report evidence exist. | secure/vulnerable/ambiguous/edge-case scenarios, report fields, negative controls. |
| Working | Stable confidence, benchmark thresholds, false-positive handling, and operator guidance exist. | CI gates, benchmark thresholds, evidence schema, reviewed docs. |
| Production-ready candidate | Authorised validation guidance, evidence-retention rules, and governance approvals exist. | validation runbook, approval gates, retention policy, release sign-off. |

## Phase GENAI-1 — Source extraction and category normalisation

Actions:

1. Extract exact headings, category IDs, and mitigation language from:
   - `OWASP-GenAI-COMPASS-RunBook-1.0.pdf`
   - `OWASP-GenAI-Data-Security-Risks-and-Mitigations-2026-v1.0.pdf`
2. Create a table of official source headings.
3. Map each official heading to a VulnoraIQ planning ID.
4. Preserve unmapped items as `Unmapped / map later`.
5. Update `docs/owasp/OWASP_TO_MITRE_ATLAS_CROSSWALK.md` with confirmed source IDs.

Acceptance:

- no source category is silently dropped
- mappings distinguish `official source wording` from `VulnoraIQ planning wording`
- uncertain mappings are marked candidate

## Phase GENAI-2 — Scenario manifests

Create safe scenario manifests under:

```text
benchmarks/fixtures/genai/
```

Required fields:

- `scenario_id`
- `genai_id`
- `risk_area`
- `fixture_type`: secure, vulnerable, ambiguous, edge_case
- `data_classification`: public, internal, confidential, secret, regulated
- `data_surface`: prompt, upload, retrieval, response, tool_trace, memory, log, report, provider_metadata
- `input_fixture`
- `expected_secure_outcome`
- `expected_vulnerable_signal`
- `required_evidence_fields`
- `mitre_atlas_tactics`
- `manual_review_required`

Minimum scenarios:

| Planning ID | Required scenarios |
| --- | --- |
| GENAI-DATA-01 | prompt containing fake secret, prompt containing benign token-like text, prompt with regulated-data marker |
| GENAI-DATA-02 | response leakage, properly redacted response, ambiguous business-sensitive response |
| GENAI-DATA-03 | allowed retrieval, disallowed retrieval, poisoned metadata, missing citation |
| GENAI-DATA-04 | approved dataset, unapproved training source, provider retention ambiguity |
| GENAI-DATA-05 | signed source, hash drift, unknown owner, stale review |
| GENAI-DATA-06 | safe report artifact, leaked placeholder, leaked token-like value, excessive evidence field |
| GENAI-DATA-07 | approved provider, unknown provider, cross-region retention risk |
| GENAI-DATA-08 | allowed connector access, over-scoped connector, credential-bearing tool trace |
| GENAI-GOV-01 | approved risk owner, missing owner, expired exception |
| GENAI-GOV-02 | mapped control, unmapped control, residual-risk missing |

## Phase GENAI-3 — Evaluator composition

Add GenAI evaluator composition using existing primitives where possible.

Potential module:

```text
core/genai_evaluators.py
```

Evaluator types:

- data classification evaluator
- restricted marker evaluator
- secret/token-like pattern evaluator
- report artifact leakage evaluator
- provider metadata evaluator
- provenance and ownership evaluator
- retention policy evaluator
- consent/approval evaluator
- retrieval-boundary evaluator
- connector credential-scope evaluator
- residual-risk and manual-review evaluator

Each evaluator should return:

- `status`: pass, warn, fail, review
- `confidence`
- `reason`
- `evidence_fields`
- `false_positive_notes`
- `manual_review_required`

## Phase GENAI-4 — Evidence schema expansion

Extend report JSON and finding evidence with:

- `genai_id`
- `genai_risk_area`
- `data_classification`
- `data_surface`
- `provider_name`
- `provider_region`
- `provider_retention_policy_known`
- `source_owner`
- `source_hash`
- `source_review_status`
- `redaction_status`
- `artifact_scan_status`
- `manual_review_reason`
- `mitre_atlas_tactics`

## Phase GENAI-5 — Reports and dashboards

Add operator-facing language for each GenAI risk area:

- what the finding means
- what it does not prove
- which data surface was tested
- whether real sensitive data was observed or only a synthetic marker
- confidence explanation
- remediation guidance
- data retention and sharing cautions
- when human review is required

Dashboard additions:

- GenAI data-security coverage table
- data surface coverage chart
- report artifact leakage status
- provider risk summary
- unresolved governance/control gaps

## Phase GENAI-6 — CI and release gates

Add gates that fail if:

- source categories have no planning row
- scenario manifests are missing required fields
- vulnerable fixtures are missed
- secure fixtures are flagged high-confidence without reason
- report artifacts contain restricted markers outside controlled evidence fields
- GenAI findings lack data surface and classification metadata
- MITRE ATLAS tactic mappings are missing
- docs and machine-readable crosswalk drift

## GenAI implementation matrix

| Planning ID | Current baseline | Next implementation focus | Working target |
| --- | --- | --- | --- |
| GENAI-DATA-01 | LLM02 restricted marker checks. | Prompt/upload DLP fixtures and data classification metadata. | Detect synthetic sensitive markers without leaking real data. |
| GENAI-DATA-02 | LLM02/LLM05 response checks. | Response redaction, token-like false-positive controls, artifact scanning. | Output evidence explains redaction, leakage, confidence, and review need. |
| GENAI-DATA-03 | LLM08 starter retrieval checks. | User/group metadata filters, source trust, citation traceability. | Retrieval evidence proves allowed/disallowed source decisions. |
| GENAI-DATA-04 | LLM03/LLM04 provenance checks. | Dataset/provider training-use metadata and memorisation-safe probes. | Dataset/training exposure risk is evidenced without real data extraction. |
| GENAI-DATA-05 | LLM03/LLM04 source metadata. | Owner, hash, signature, review, and approval evidence. | Unknown or tampered sources are flagged with clear remediation. |
| GENAI-DATA-06 | Report generation exists. | Log/report/SARIF/dashboard artifact scanner. | Artifacts are checked for restricted markers before sharing. |
| GENAI-DATA-07 | Provider not deeply modelled. | Provider inventory and retention/data residency metadata. | Third-party data handling risk is visible in reports. |
| GENAI-DATA-08 | LLM06 tool governance starter. | Connector credential scope and data-flow evidence. | Tool traces show whether restricted data crossed a connector boundary. |
| GENAI-GOV-01 | Policy exceptions exist. | Risk owner, approval, expiry, and exception evidence. | Findings can show governance ownership and expired approvals. |
| GENAI-GOV-02 | Policy engine exists. | Control mapping and residual-risk fields. | Reports show control coverage and unmapped residual risks. |

## Immediate backlog

1. Extract official GenAI source headings from the PDFs.
2. Create `benchmarks/fixtures/genai/` scenario manifests.
3. Add `core/genai_evaluators.py`.
4. Add GenAI evidence fields to report JSON schema.
5. Add artifact leakage scanner for Markdown/JSON/SARIF/HTML/dashboard outputs.
6. Add provider inventory schema under `config/`.
7. Add GenAI coverage dashboard section.
8. Add CI validation for GenAI manifests, mappings, and report fields.
9. Update generated reports with GenAI limitation text.
10. Map confirmed GenAI IDs to MITRE ATLAS tactics and techniques.

## Claim rule

Do not describe GenAI data-security coverage as `Working` or production-ready until the source PDFs are extracted, categories are confirmed, fixtures/evaluators exist, and CI validates the scenario set.