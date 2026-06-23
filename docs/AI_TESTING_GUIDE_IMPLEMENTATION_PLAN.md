# OWASP AI Testing Guide Implementation Plan

## Purpose

This plan turns the OWASP AI Testing Guide into a first-class VulnoraIQ implementation roadmap. The target is not a documentation-only mapping. The target is a runnable, evidence-producing assessment capability that can test live AI applications, Docker-hosted agents, model-facing endpoints, RAG systems, tool-using agents, and supporting AI data/infrastructure controls.

## Source basis

Reviewed source:

- OWASP AI Testing Guide root README: project objective, existing resources, and scope.
- OWASP AI Testing Guide table of contents.
- OWASP AI Testing Guide framework chapter.

Key source observations:

- The guide positions itself as a structured methodology for AI system testing, covering reliability, security, and ethical alignment.
- It consolidates existing resources including OWASP GenAI Red Teaming Guide, CSA Agentic AI Red Teaming Guide, OWASP AI Exchange, OWASP AI Security and Privacy Guide, OWASP Top 10 for LLM, OWASP AI VSS, and NIST AI 100-2 E2025.
- The framework organizes test cases under four pillars:
  - AI Application Testing
  - AI Model Testing
  - AI Infrastructure Testing
  - AI Data Testing
- The framework currently identifies 32 test cases:
  - `AITG-APP-01` through `AITG-APP-14`
  - `AITG-MOD-01` through `AITG-MOD-07`
  - `AITG-INF-01` through `AITG-INF-06`
  - `AITG-DAT-01` through `AITG-DAT-05`
- The guide explicitly warns that black-box testing has limitations and that better results often require grey-box or white-box evidence such as logs, prompts, architecture, source code, third-party service configuration, guardrail configuration, token/cost thresholds, and model/service administration information.

## Implementation goal

VulnoraIQ should support a full AI Testing Guide assessment mode with:

1. A machine-readable AITG test manifest.
2. Safe, authorized test payload libraries.
3. Runtime execution modules for tests that can be exercised against live endpoints.
4. Evidence-gathering modules for tests that require configuration, logs, architecture, datasets, model cards, SBOMs, or governance artifacts.
5. WebUI selection of complete AITG suite, pillar-level suites, and individual AITG test cases.
6. Report output showing AITG test ID, pillar, source framework, domain, evidence, result, residual risk, and recommended remediation.
7. CI validation proving every manifest entry has a module, evidence requirement, reporting path, and documentation coverage.

## Target architecture

```text
config/aitg_tests.yaml
        |
        v
core/aitg_registry.py -----------------------------+
        |                                          |
        v                                          v
modules/aitg/*                              payloads/aitg/*.yaml
        |                                          |
        +----------------- core/test_runner.py ----+
                          |
                          v
                   live target adapters
                          |
                          v
          WebUI dashboard + JSON/Markdown/HTML reports
```

## New or updated repository artifacts

| Area | Planned files |
| --- | --- |
| Manifest | `config/aitg_tests.yaml` |
| Schema | `schemas/aitg_tests.schema.json` |
| Runtime registry | `core/aitg_registry.py` |
| Modules | `modules/aitg/application.py`, `modules/aitg/model.py`, `modules/aitg/infrastructure.py`, `modules/aitg/data.py` |
| Payloads | `payloads/aitg/application.yaml`, `payloads/aitg/model.yaml`, `payloads/aitg/infrastructure.yaml`, `payloads/aitg/data.yaml` |
| Evidence templates | `docs/evidence/aitg/*.md` |
| WebUI | Extend profile catalog and finding detail rendering for AITG fields |
| Reports | Extend JSON, Markdown, and HTML templates with AITG coverage tables |
| CI | `scripts/validate_aitg_manifest.py` and tests under `tests/` |

## Test manifest design

Each AITG test should have a normalized manifest entry:

```yaml
AITG-APP-01:
  title: Testing for Prompt Injection
  pillar: application
  domain:
    - security
  source_threats:
    - OWASP Top 10 LLM 2025
  runtime_mode:
    - black_box
    - grey_box
  target_capabilities:
    - text_generation
    - instruction_following
  module: aitg_application_prompt_injection
  payload_library: aitg/application/prompt_injection
  evidence_required:
    - prompt_input
    - model_output
    - policy_decision
    - guardrail_logs_optional
  maps_to:
    owasp_llm:
      - LLM01
    mitre_atlas: []
  safe_test_boundary: authorized_non_destructive
  status: planned
```

Every test must include:

- `test_id`
- `title`
- `pillar`
- `domain`
- `runtime_mode`
- `target_capabilities`
- `module`
- `evidence_required`
- `safe_test_boundary`
- implementation `status`

## AITG coverage implementation matrix

| AITG area | Primary VulnoraIQ implementation | Notes |
| --- | --- | --- |
| `AITG-APP-01` Prompt Injection | Runtime prompt/response module | Reuse existing OWASP LLM prompt-injection detectors, add AITG evidence fields. |
| `AITG-APP-02` Indirect Prompt Injection | RAG/document injection harness | Requires controlled document/source injection workflow. |
| `AITG-APP-03` Sensitive Data Leak | Runtime output and DLP-style detectors | Needs seeded synthetic secrets and output redaction evidence. |
| `AITG-APP-04` Input Leakage | Multi-turn/agent trace detector | Requires checking whether user input leaks into unintended tool calls or downstream agents. |
| `AITG-APP-05` Unsafe Outputs | Output safety classifier + policy engine | Must stay safe and avoid producing harmful content in reports. |
| `AITG-APP-06` Agentic Behavior Limits | Docker agent runtime + tool boundary checks | Requires tool sandbox and permission model evidence. |
| `AITG-APP-07` Prompt Disclosure | Prompt disclosure probes | Must avoid collecting real secrets; use synthetic system prompt markers. |
| `AITG-APP-08` Embedding Manipulation | RAG/vector-store harness | Requires test vector corpus and retrieval trace evidence. |
| `AITG-APP-09` Model Extraction | Rate-limit and telemetry assessment | Use non-destructive query-pattern testing, not real model theft. |
| `AITG-APP-10` Harmful Content Bias | Responsible AI evaluation harness | Needs controlled dataset and scoring methodology. |
| `AITG-APP-11` Hallucinations | Ground-truth QA corpus | Requires evidence documents and expected-answer assertions. |
| `AITG-APP-12` Toxic Output | Safety classifier + refusal/response policy checks | Must avoid storing harmful raw content unnecessarily. |
| `AITG-APP-13` Over-Reliance on AI | Process-control checklist and scenario tests | Mostly grey-box governance/process evidence. |
| `AITG-APP-14` Explainability and Interpretability | Evidence checklist and explainability output tests | Depends on app capabilities. |
| `AITG-MOD-01` Evasion Attacks | Model endpoint robustness tests | Requires model-facing adapter and safe perturbation sets. |
| `AITG-MOD-02` Runtime Model Poisoning | Runtime config/integrity evidence | Mostly grey-box unless app exposes update mechanisms. |
| `AITG-MOD-03` Poisoned Training Sets | Dataset provenance evidence | Requires dataset inventory and validation artifacts. |
| `AITG-MOD-04` Membership Inference | Privacy test harness | Must be carefully scoped to synthetic/authorized datasets. |
| `AITG-MOD-05` Inversion Attacks | Privacy risk evidence and safe probes | Avoid real data extraction; use synthetic canary data only. |
| `AITG-MOD-06` Robustness to New Data | Robustness benchmark corpus | Requires repeatable test data and variance thresholds. |
| `AITG-MOD-07` Goal Alignment | Scenario-based policy alignment tests | Needs target policy definition and expected behavior. |
| `AITG-INF-01` Supply Chain Tampering | SBOM/provenance scanner | Integrate package, model, and container dependency checks. |
| `AITG-INF-02` Resource Exhaustion | Token/rate/cost limit checks | Must run within configured safe budget. |
| `AITG-INF-03` Plugin Boundary Violations | Tool/plugin sandbox tests | Requires agent tool registry and permission evidence. |
| `AITG-INF-04` Capability Misuse | Tool-use scenario checks | Requires action logs and authorization boundaries. |
| `AITG-INF-05` Fine-tuning Poisoning | Fine-tuning dataset/process evidence | Mostly grey-box/white-box. |
| `AITG-INF-06` Dev-Time Model Theft | Model artifact access-control review | Requires repo/model registry/storage evidence. |
| `AITG-DAT-01` Training Data Exposure | Synthetic canary exposure checks | Requires known safe canary data and data inventory. |
| `AITG-DAT-02` Runtime Exfiltration | RAG/tool exfiltration checks | Must be non-destructive and synthetic-secret based. |
| `AITG-DAT-03` Dataset Diversity & Coverage | Dataset metric evidence | Requires dataset metadata and coverage thresholds. |
| `AITG-DAT-04` Harmful Content in Data | Dataset content safety checks | Requires dataset access and safe classifier output. |
| `AITG-DAT-05` Data Minimization & Consent | Privacy governance checklist | Requires data processing and consent evidence. |

## Execution modes

### Black-box mode

Used when only an endpoint is available. It can run prompt/output tests and some RAG/agent probes. Reports must clearly label coverage limitations.

### Grey-box mode

Used when the tester can provide logs, prompts, architecture diagrams, model configuration, token limits, RAG corpus metadata, tool registry, or admin screenshots/export files. This should be the default recommended production mode.

### White-box mode

Used when source code, deployment manifests, model artifacts, dataset metadata, and CI/CD evidence are available. This enables infrastructure, data, model, and supply-chain tests that cannot be proven reliably through black-box probing.

## Phase plan

### Phase 0 — Source lock and versioning

Deliverables:

- Add `docs/sources/aitg_source_review.md` with reviewed source URLs, commit/date, and notes.
- Add `config/aitg_source_versions.yaml` to lock implementation to a specific upstream source revision.
- Record that the OWASP AI Testing Guide is evolving and that VulnoraIQ coverage is versioned.

Acceptance criteria:

- Every source document used for implementation has a URL and retrieval date.
- Implementation docs state the upstream source version or retrieval date.

### Phase 1 — AITG manifest and schema

Deliverables:

- `config/aitg_tests.yaml` with all 32 AITG test entries.
- JSON schema for the manifest.
- Validator script and pytest coverage.

Acceptance criteria:

- CI fails if any AITG test is missing required metadata.
- CI fails if a test has no module/evidence plan.

### Phase 2 — AI Application Testing runtime modules

Deliverables:

- Runtime modules for `AITG-APP-01` through `AITG-APP-08` first.
- Safe payload libraries using synthetic secrets and synthetic policy markers.
- Evidence model extensions for AITG test ID, pillar, and domain.

Acceptance criteria:

- WebUI can run each implemented application test individually.
- Reports show AITG ID, input category, observed output, detector result, and remediation.

### Phase 3 — Agent/RAG capability tests

Deliverables:

- RAG test harness for indirect prompt injection, embedding manipulation, and runtime exfiltration.
- Agent/tool sandbox tests for behavior limits, plugin boundary violations, and capability misuse.
- Integration with the Docker AI agent runtime.

Acceptance criteria:

- A live Docker agent can be tested through `AITG-APP-06`, `AITG-INF-03`, and `AITG-INF-04` style checks.
- Tool-use evidence is captured without exposing real secrets.

### Phase 4 — Model, data, and infrastructure evidence modules

Deliverables:

- Grey-box evidence templates for model, data, and infrastructure tests.
- Model/data/SBOM artifact upload or path-reference workflow.
- Policy engine checks for evidence completeness.

Acceptance criteria:

- Tests that cannot be proven black-box are not falsely marked as pass.
- Missing evidence produces `manual_review` or `insufficient_evidence`, not `pass`.

### Phase 5 — AITG scoring and dashboard

Deliverables:

- Dashboard coverage by pillar.
- Per-test status: `pass`, `fail`, `warn`, `manual_review`, `insufficient_evidence`, `not_applicable`.
- AITG export section in Markdown/HTML/JSON reports.

Acceptance criteria:

- Executive dashboard shows total AITG coverage, highest risk, and evidence gaps.
- Technical report includes exact test IDs and remediation.

### Phase 6 — CI and production-readiness gate

Deliverables:

- `scripts/validate_aitg_manifest.py`
- `tests/test_aitg_manifest.py`
- `tests/test_aitg_profiles.py`
- README and docs updates.

Acceptance criteria:

- All AITG tests are discoverable in the WebUI catalog.
- Every implemented AITG test has safe test data.
- Every non-runtime test has evidence requirements and cannot silently pass without evidence.

## WebUI requirements

The WebUI should expose:

- `AI Testing Guide - Full assessment`
- `AI Testing Guide - Application Testing`
- `AI Testing Guide - Model Testing`
- `AI Testing Guide - Infrastructure Testing`
- `AI Testing Guide - Data Testing`
- Individual tests for all `AITG-*` IDs.

The selected test detail panel should show:

- AITG ID
- Pillar
- Domain
- Source threat
- Required target capabilities
- Evidence requirements
- Execution mode
- Whether Docker/agent/RAG/model/data evidence is required

## Reporting requirements

Reports must include:

- AITG coverage summary.
- Pillar-level result table.
- Test-level detail table.
- Evidence completeness matrix.
- Mapping to OWASP LLM categories where applicable.
- Explicit limitation statements for black-box-only testing.

## Safety boundaries

- All payloads must be authorized, non-destructive, and synthetic.
- Secrets used in tests must be generated synthetic canaries.
- Model extraction and data exfiltration tests must not attempt real theft or real sensitive-data extraction.
- Resource exhaustion tests must use configured token, request, and cost ceilings.
- Reports must avoid storing harmful raw content where a summarized detector result is sufficient.

## Completion definition

This implementation can be called complete when:

1. All 32 AITG tests exist in the manifest.
2. The WebUI can select all AITG suites and individual tests.
3. Runtime-capable tests execute against live targets.
4. Evidence-only tests require explicit evidence and never silently pass.
5. Reports include AITG-specific coverage and limitation statements.
6. CI validates manifest, profile, module, payload, and report coverage.
7. Documentation clearly states what is automated, what is evidence-based, and what requires manual review.
