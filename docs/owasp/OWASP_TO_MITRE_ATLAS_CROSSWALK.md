# OWASP to MITRE ATLAS Crosswalk

This document maps VulnoraIQ's OWASP AI security coverage areas to MITRE ATLAS tactics for implementation planning.

> **Status:** planning crosswalk.  
> **Scope:** OWASP LLM 2025 categories, GenAI data-security risks, and Agentic Application risks.  
> **Important:** mappings are candidate planning mappings until validated against the official source documents, generated ATLAS data, and implemented evaluator behaviour.

## Source inputs

VulnoraIQ source documents:

- `docs/owasp/` — OWASP LLM 2025 implementation specs
- `docs/MITRE_ATLAS_AI_MATRIX.md` — current MITRE ATLAS tactic planning register
- `docs/owasp-documents/OWASP-GenAI-COMPASS-RunBook-1.0.pdf`
- `docs/owasp-documents/OWASP-GenAI-Data-Security-Risks-and-Mitigations-2026-v1.0.pdf`
- `docs/owasp-documents/OWASP-Top-10-for-Agentic-Applications-2026-12.6.pdf`
- `docs/owasp-documents/OWASP-Top10-for-Agentic-Applications_AIUC-1-Crosswalk-May26.pdf`
- `docs/owasp-documents/State-of-Agentic-AI-Security-and-Governance-v2.01.pdf`

MITRE ATLAS source alignment is tracked in `docs/MITRE_ATLAS_AI_MATRIX.md` and generated from the official `atlas-data` source used by the project.

## Mapping rule

Use these labels consistently:

| Label | Meaning |
| --- | --- |
| `Primary` | Directly relevant tactic for the risk category. |
| `Secondary` | Common downstream tactic or consequence. |
| `Contextual` | Relevant only for specific architectures or scenarios. |
| `Unmapped / map later` | Do not force a weak mapping; keep the item visible for later review. |

No OWASP, GenAI, Agentic, or ATLAS item should disappear because the mapping is uncertain.

---

## MITRE ATLAS tactic baseline used by VulnoraIQ

| Tactic ID | Tactic | Planning interpretation in VulnoraIQ |
| --- | --- | --- |
| AML.TA0000 | AI Model Access | Access to model endpoints, model assets, or model-serving surfaces. |
| AML.TA0001 | AI Attack Staging | Preparing prompts, data, tools, accounts, infrastructure, or payloads for AI attacks. |
| AML.TA0002 | Reconnaissance | Discovering AI surfaces, prompts, tools, data stores, policies, or model behaviour. |
| AML.TA0003 | Resource Development | Creating or acquiring datasets, tools, prompts, models, connectors, or infrastructure. |
| AML.TA0004 | Initial Access | Gaining entry into model, RAG, agent, tool, or orchestration surfaces. |
| AML.TA0005 | Execution | Causing model, tool, code, workflow, or agent execution. |
| AML.TA0006 | Persistence | Maintaining influence through memory, corpus poisoning, model/data changes, or agent state. |
| AML.TA0007 | Defense Evasion | Bypassing guardrails, policies, monitoring, or detection. |
| AML.TA0008 | Discovery | Enumerating system instructions, tools, data sources, permissions, identities, or environment. |
| AML.TA0009 | Collection | Gathering sensitive data, context, embeddings, memory, logs, artifacts, or outputs. |
| AML.TA0010 | Exfiltration | Moving restricted data or artifacts out of the controlled boundary. |
| AML.TA0011 | Impact | Integrity, availability, safety, cost, trust, or business-process impact. |
| AML.TA0012 | Privilege Escalation | Gaining broader model/tool/agent permissions or policy bypass. |
| AML.TA0013 | Credential Access | Obtaining secrets, tokens, keys, credentials, or authentication material. |
| AML.TA0014 | Command and Control | Establishing external control channels through tools, agents, callbacks, or generated workflows. |
| AML.TA0015 | Lateral Movement | Moving across tools, agents, data sources, identities, or connected systems. |

---

## OWASP LLM 2025 to MITRE ATLAS mapping

| OWASP ID | Vulnerability | Primary MITRE ATLAS tactics | Secondary/contextual tactics | VulnoraIQ implementation focus |
| --- | --- | --- | --- | --- |
| LLM01:2025 | Prompt Injection | AML.TA0004 Initial Access; AML.TA0005 Execution; AML.TA0007 Defense Evasion | AML.TA0012 Privilege Escalation; AML.TA0010 Exfiltration; AML.TA0011 Impact | Direct, indirect, retrieval-borne, tool-borne, and agent-chain instruction boundary tests. |
| LLM02:2025 | Sensitive Information Disclosure | AML.TA0008 Discovery; AML.TA0009 Collection; AML.TA0010 Exfiltration | AML.TA0013 Credential Access; AML.TA0011 Impact | Restricted marker, secret, PII, credential, report artifact, log, and trace leakage tests. |
| LLM03:2025 | Supply Chain | AML.TA0003 Resource Development; AML.TA0004 Initial Access; AML.TA0006 Persistence | AML.TA0007 Defense Evasion; AML.TA0005 Execution; AML.TA0011 Impact | Model, dependency, dataset, connector, tool, prompt-template, and provider provenance checks. |
| LLM04:2025 | Data and Model Poisoning | AML.TA0006 Persistence; AML.TA0007 Defense Evasion; AML.TA0011 Impact | AML.TA0003 Resource Development; AML.TA0005 Execution | Corpus integrity, source trust, model/version drift, unreviewed data, and poisoning metadata tests. |
| LLM05:2025 | Improper Output Handling | AML.TA0005 Execution; AML.TA0011 Impact | AML.TA0007 Defense Evasion; AML.TA0004 Initial Access | Unsafe output-to-action, schema bypass, downstream consumer, code/HTML/SQL handoff, and report rendering tests. |
| LLM06:2025 | Excessive Agency | AML.TA0005 Execution; AML.TA0012 Privilege Escalation; AML.TA0015 Lateral Movement | AML.TA0013 Credential Access; AML.TA0014 Command and Control; AML.TA0010 Exfiltration; AML.TA0011 Impact | Tool scope, approval, memory write, rollback, audit, budget, and multi-step action governance tests. |
| LLM07:2025 | System Prompt Leakage | AML.TA0008 Discovery; AML.TA0009 Collection; AML.TA0010 Exfiltration | AML.TA0007 Defense Evasion; AML.TA0013 Credential Access | Protected instruction marker, system/developer prompt, policy, chain context, and report artifact leakage tests. |
| LLM08:2025 | Vector and Embedding Weaknesses | AML.TA0008 Discovery; AML.TA0009 Collection; AML.TA0010 Exfiltration | AML.TA0006 Persistence; AML.TA0007 Defense Evasion; AML.TA0011 Impact | RAG source trust, metadata filtering, user/group boundary, poisoned retrieval, embedding collision, and citation-grounding tests. |
| LLM09:2025 | Misinformation | AML.TA0011 Impact; AML.TA0007 Defense Evasion | AML.TA0005 Execution; AML.TA0008 Discovery | Unsupported claim, fabricated citation, uncertainty, high-impact decision, and operator escalation tests. |
| LLM10:2025 | Unbounded Consumption | AML.TA0011 Impact; AML.TA0005 Execution | AML.TA0014 Command and Control; AML.TA0007 Defense Evasion | Token, timeout, retry, loop, fan-out, cost, tool-call, recursion, and agent-loop budget tests. |

---

## GenAI data-security risks to MITRE ATLAS mapping

The exact category wording must be confirmed against `OWASP-GenAI-Data-Security-Risks-and-Mitigations-2026-v1.0.pdf` during PDF text extraction. The following planning rows define the implementation areas VulnoraIQ should support.

| GenAI data-security risk area | Primary MITRE ATLAS tactics | Secondary/contextual tactics | VulnoraIQ implementation focus |
| --- | --- | --- | --- |
| Sensitive data in prompts and uploaded context | AML.TA0009 Collection; AML.TA0010 Exfiltration | AML.TA0013 Credential Access; AML.TA0011 Impact | Prompt/input DLP, restricted marker detection, data-classification tags, and no-secrets evidence rules. |
| Sensitive data in model responses | AML.TA0010 Exfiltration; AML.TA0011 Impact | AML.TA0009 Collection | Response redaction, output leakage checks, artifact scanning, and evidence minimisation. |
| Training/fine-tuning data exposure | AML.TA0009 Collection; AML.TA0010 Exfiltration | AML.TA0006 Persistence; AML.TA0011 Impact | Dataset provenance, memorisation probes, consent/retention metadata, and training-source classification. |
| RAG/vector store data leakage | AML.TA0008 Discovery; AML.TA0009 Collection; AML.TA0010 Exfiltration | AML.TA0006 Persistence; AML.TA0007 Defense Evasion | Retrieval boundary tests, metadata filters, source trust scores, group/user access controls, and citation trace checks. |
| Agent/tool access to sensitive systems | AML.TA0005 Execution; AML.TA0012 Privilege Escalation; AML.TA0015 Lateral Movement | AML.TA0010 Exfiltration; AML.TA0013 Credential Access | Tool permission inventory, approval gates, scoped credentials, action trace evidence, and rollback requirements. |
| Logs, telemetry, and report artifacts leaking data | AML.TA0009 Collection; AML.TA0010 Exfiltration | AML.TA0011 Impact | Audit/report artifact DLP, token/secret redaction, trace minimisation, and report sharing warnings. |
| Third-party model/provider data handling | AML.TA0003 Resource Development; AML.TA0009 Collection; AML.TA0010 Exfiltration | AML.TA0011 Impact | Provider inventory, data residency, retention, training-use flags, contract metadata, and risk notes. |
| Shadow AI / unsanctioned GenAI use | AML.TA0002 Reconnaissance; AML.TA0004 Initial Access; AML.TA0009 Collection | AML.TA0010 Exfiltration; AML.TA0011 Impact | Config inventory, unknown provider detection, policy gap checks, and governance evidence. |
| Data provenance and integrity gaps | AML.TA0003 Resource Development; AML.TA0006 Persistence; AML.TA0011 Impact | AML.TA0007 Defense Evasion | Source owner, hash/signature, approval, review date, data lineage, and untrusted-source warnings. |
| Data retention and deletion failure | AML.TA0009 Collection; AML.TA0011 Impact | AML.TA0010 Exfiltration | Retention metadata, deletion policy checks, artifact expiry, and backup retention validation. |

---

## Agentic application risks to MITRE ATLAS mapping

The exact OWASP ASI category names must be confirmed against `OWASP-Top-10-for-Agentic-Applications-2026-12.6.pdf` and `OWASP-Top10-for-Agentic-Applications_AIUC-1-Crosswalk-May26.pdf`. Until then, VulnoraIQ uses the following planning categories to drive implementation.

| Planning ID | Agentic risk area | Primary MITRE ATLAS tactics | Secondary/contextual tactics | VulnoraIQ implementation focus |
| --- | --- | --- | --- | --- |
| AGENTIC-01 | Agent instruction / prompt injection | AML.TA0004 Initial Access; AML.TA0005 Execution; AML.TA0007 Defense Evasion | AML.TA0012 Privilege Escalation; AML.TA0011 Impact | Multi-step prompt, indirect context, tool-description, and retrieved-instruction injection tests. |
| AGENTIC-02 | Excessive tool permission or agency | AML.TA0005 Execution; AML.TA0012 Privilege Escalation; AML.TA0015 Lateral Movement | AML.TA0010 Exfiltration; AML.TA0011 Impact | Tool inventory, permission scopes, action allowlists, approval points, and rollback evidence. |
| AGENTIC-03 | Insecure delegation and inter-agent trust | AML.TA0015 Lateral Movement; AML.TA0012 Privilege Escalation; AML.TA0014 Command and Control | AML.TA0008 Discovery; AML.TA0011 Impact | Agent identity, delegation boundary, cross-agent call graph, handoff policy, and confused-deputy tests. |
| AGENTIC-04 | Tool/connector supply-chain compromise | AML.TA0003 Resource Development; AML.TA0004 Initial Access; AML.TA0005 Execution | AML.TA0006 Persistence; AML.TA0007 Defense Evasion | Tool provenance, connector ownership, manifest validation, tool-description poisoning, and version drift checks. |
| AGENTIC-05 | Memory, state, or plan poisoning | AML.TA0006 Persistence; AML.TA0007 Defense Evasion; AML.TA0011 Impact | AML.TA0005 Execution | Memory write controls, plan tampering, state integrity, source trust, rollback, and review gates. |
| AGENTIC-06 | Sensitive data exposure through agent actions | AML.TA0009 Collection; AML.TA0010 Exfiltration; AML.TA0013 Credential Access | AML.TA0011 Impact | Tool-call data flow, credential scope, output leakage, trace/report artifact DLP, and exfiltration-path tests. |
| AGENTIC-07 | Runaway loops and resource exhaustion | AML.TA0011 Impact; AML.TA0005 Execution | AML.TA0014 Command and Control | Iteration budgets, retry budgets, tool-call budgets, cost caps, timeout gates, and stop-condition evidence. |
| AGENTIC-08 | Missing human oversight and approval | AML.TA0005 Execution; AML.TA0011 Impact; AML.TA0012 Privilege Escalation | AML.TA0007 Defense Evasion | High-impact action classification, human-in-the-loop approvals, denial evidence, and escalation paths. |
| AGENTIC-09 | Poor auditability, repudiation, and trace gaps | AML.TA0007 Defense Evasion; AML.TA0008 Discovery | AML.TA0011 Impact | Action trace completeness, request IDs, tool trace, memory trace, decision evidence, and non-repudiation checks. |
| AGENTIC-10 | Unsafe goals, planning, and policy conflict | AML.TA0011 Impact; AML.TA0005 Execution | AML.TA0007 Defense Evasion; AML.TA0012 Privilege Escalation | Goal decomposition review, policy conflict detection, unsafe plan classification, and manual-review routing. |

---

## Required crosswalk fields for implementation

When this mapping moves from planning to code, each implemented check should carry:

- `owasp_family`: `LLM`, `GenAI Data`, `Agentic`
- `owasp_id`: e.g. `LLM01`, `GENAI-DATA-01`, or confirmed `ASIxx`
- `owasp_name`
- `mitre_atlas_tactics`: list of `AML.TAxxxx`
- `mitre_atlas_techniques`: list of confirmed technique IDs, once regenerated from ATLAS data
- `mapping_confidence`: `high`, `medium`, `low`
- `mapping_status`: `candidate`, `validated`, `rejected`, `map_later`
- `evidence_surface`: prompt, response, retrieval trace, tool trace, memory trace, model metadata, provider metadata, report artifact, audit log
- `manual_review_required`: boolean

## Implementation backlog

1. Regenerate the full MITRE ATLAS technique table and preserve unmapped rows.
2. Extract exact category headings from the GenAI and Agentic OWASP PDFs.
3. Replace `AGENTIC-xx` planning IDs with confirmed OWASP `ASIxx` IDs and names.
4. Add `config/owasp_mitre_atlas_crosswalk.yaml` as machine-readable source.
5. Add validator checks that every active OWASP oracle has at least one candidate ATLAS tactic.
6. Add report fields for ATLAS tactic and technique mappings.
7. Add dashboard coverage table by OWASP category and ATLAS tactic.
8. Add CI guard to fail if OWASP docs, crosswalk YAML, and report schema drift.

## Claim rule

Do not claim full MITRE ATLAS coverage until:

1. all ATLAS techniques and sub-techniques are regenerated from the official source,
2. each technique is either mapped, deliberately unmapped, or marked for later review,
3. active VulnoraIQ checks produce structured evidence for each validated mapping, and
4. false-positive / false-negative limitations are documented.