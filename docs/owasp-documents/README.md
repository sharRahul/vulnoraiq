# OWASP Source Document Review Index

This folder stores source PDFs used to expand VulnoraIQ beyond the current OWASP LLM 2025 starter implementation.

> **Status:** source-review queue.  
> **Rule:** do not treat GenAI or Agentic category names/IDs as official in VulnoraIQ until the relevant PDF text has been extracted, reviewed, and mapped into the planning docs.

## Source documents

| Source PDF | Review purpose | Target planning docs |
| --- | --- | --- |
| `OWASP-GenAI-COMPASS-RunBook-1.0.pdf` | Governance/runbook controls for GenAI assessment and operating model. | `docs/genai/README.md`, `docs/genai/PRODUCTION_READINESS_PLAN.md` |
| `OWASP-GenAI-Data-Security-Risks-and-Mitigations-2026-v1.0.pdf` | Data-security risk categories, mitigations, and evidence requirements. | `docs/genai/README.md`, `docs/genai/PRODUCTION_READINESS_PLAN.md`, `docs/owasp/OWASP_TO_MITRE_ATLAS_CROSSWALK.md` |
| `OWASP-Top-10-for-Agentic-Applications-2026-12.6.pdf` | Official Agentic Application category IDs/names/descriptions. | `docs/agentic/README.md`, `docs/agentic/PRODUCTION_READINESS_PLAN.md`, crosswalk |
| `OWASP-Top10-for-Agentic-Applications_AIUC-1-Crosswalk-May26.pdf` | AIUC crosswalk and relationship to Agentic Top 10 categories. | `docs/agentic/PRODUCTION_READINESS_PLAN.md`, crosswalk |
| `State-of-Agentic-AI-Security-and-Governance-v2.01.pdf` | Governance, lifecycle, oversight, and assurance context for agentic systems. | `docs/agentic/PRODUCTION_READINESS_PLAN.md`, `docs/ASSESSMENT_ASSURANCE.md` |

## Review workflow

1. Extract text from each PDF into a temporary review artifact.
2. Capture official category IDs, names, descriptions, examples, and mitigations.
3. Compare extracted categories with current planning rows.
4. Replace placeholder planning IDs with official IDs where appropriate.
5. Mark uncertain mappings as `candidate` or `Unmapped / map later`.
6. Update:
   - `docs/owasp/OWASP_TO_MITRE_ATLAS_CROSSWALK.md`
   - `docs/genai/README.md`
   - `docs/genai/PRODUCTION_READINESS_PLAN.md`
   - `docs/agentic/README.md`
   - `docs/agentic/PRODUCTION_READINESS_PLAN.md`
   - `docs/ASSESSMENT_ASSURANCE.md`
7. Add machine-readable mapping in `config/owasp_mitre_atlas_crosswalk.yaml` when the mapping is ready for validation.
8. Add CI validation to detect drift between source docs, planning docs, crosswalk, and report schema.

## Acceptance criteria for source review

A PDF is considered reviewed when:

- exact source category names are captured,
- source version/date is recorded,
- each source category has a planning row,
- each planning row has candidate OWASP and MITRE ATLAS mapping,
- unmapped items are preserved rather than removed,
- implementation status is clearly marked as `Planning`, `Working-alpha starter`, `Working starter`, or later,
- no documentation claims active coverage before fixtures/evaluators/tests exist.

## Current status

| Source PDF | Status |
| --- | --- |
| OWASP GenAI COMPASS RunBook | Pending extraction/review |
| OWASP GenAI Data Security Risks and Mitigations 2026 | Pending extraction/review |
| OWASP Top 10 for Agentic Applications 2026 | Pending extraction/review |
| Agentic Applications AIUC-1 Crosswalk | Pending extraction/review |
| State of Agentic AI Security and Governance | Pending extraction/review |