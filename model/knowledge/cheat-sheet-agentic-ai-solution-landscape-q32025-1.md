# AI Security

> Source: `Cheat-Sheet_-Agentic-AI-Solution-Landscape-Q32025-1.pdf` (17 pages). Extracted 2026-06-27 for the Nora knowledge store.
> Raw PDF is gitignored; this Markdown is the tracked, reviewable copy.

<!-- page 1 -->
AI Security
Solutions Landscape
For Agentic AI
### Ai Security Solutions Initiative
### Q3 ‘2025
This document is produced  by the OWASP GenAI
Security Project  under Creative Commons
license, CC BY-SA 4.0

<!-- page 2 -->
AI Security Solutions Landscape
For Agentic AI Applications
### Ai Security Solutions Initiative
The Solutions Landscape monitors and maps the full Agentic AI lifecycle,
focusing on the DevOps–SecOps intersection to meet evolving security
needs. Guided by the Agentic AI Threats and Mitigations guide and SecOps
tasks, it highlights open-source and commercial solutions by stage,
identifying their coverage of Agentic SecOps duties and threat mitigation,
and leverages industry and community input as a peer-reviewed resource for
navigating agentic AI’s shifting security challenges. Updated Quarterly.
### Q3 ‘2025
This document is produced  by the OWASP GenAI
Security Project  under Creative Commons
license, CC BY-SA 4.0

<!-- page 3 -->
Agentic AI Security Landscape - Q2/3 2025
### Cheat Sheet
### Eunomatix
Operate
Open Source
Gold Sponsors
Silver Sponsors
Augment,
Fine Tune
Data
Develop &
Experiment
Test &
Evaluate
Release
Deploy
Scope &
Plan
Monitor
Govern
genai.owasp.org

<!-- page 4 -->
OWASP ASI Agentic
Taxonomy Reporting
& Support Built Into
These Products.
OWASP GenAI - ASI - Agentic Threat and
Mitigations Taxonomy Product Support
### Cheat Sheet
genai.owasp.org
## 18 Solution providers and open source projects  have
implemented the OWASP Agentic Risk and
mitigations taxonomy directly into their products to
help organizations identify and measure their
security posture and readiness related to Agentic Ai
applications and systems.
Open Source
Gold Sponsors
Silver Sponsors

<!-- page 5 -->
Monitor
●Available Agent Scanning
●Conduct adversarial
red-teaming: goal drift
●Run multi-agent scenario
simulations for collusion,
misalignment, or deception
detection.
● Validate agent decisions
against expected goal plans.
●Sandboxed testing of all tool
calls— code execution or
cloud API triggers
●Generate and verify model +
agent + tool SBOMs - shared
responsibility
●Sign model weights, plugin
manifests, and memory
snapshots.
●Ensure policy bundles  are
cryptographically validated at
deploy time.
●Register all agents in an
internal trust registry with
capability descriptors
●Enforce zero-trust policies
between agents, tools, and
external APIs
●Rotate all shared secrets,
keys, and tokens with
ephemeral, scoped
credentials.
●Apply runtime guardrails
(e.g., LLM ﬁrewalls, tool
allowlists)
●Conﬁgure inter-agent
authorization policies based
on capabilities and roles
●Conduct agentic threat
modeling
●Identify system-wide
non-human identities  and
authentication protocols.
●Draft policies for agent
privilege boundaries, tool
scopes and delegation logic.
●Deﬁne controls for memory
scoping, isolation, and
long-term persistence rules.
●Apply differential privacy or
obfuscation on sensitive
knowledge injected into
agent memory.
●Agent Action Audit
●Perform SAST/DAST on agent
planning code, tool wrappers,
and plugin interfaces.
●Harden agent loop logic
against inﬁnite loops, unsafe
function routing, unauth
self-modiﬁcation.
●Validate connector contracts
●Implement policy
enforcement hooks in App
Frameworks
○e.g. LangGraph, CrewAI,
or Semantic Kernel ﬂows.
●SAudit reﬂection accuracy by comparing stated
and observed planning outcomes.
●Ensure use of immutable logs (e.g., Sigstore,
Immudb) for forensic readiness.
●Correlate telemetry from agent step tracing, tool
execution, and message logs.
●Alert on anomalies like goal reversal, unexpected
plan depth, adversarial-input, excessive tool usage,
or rapid inter-agent chatter.
●Monitor agent memory
mutation patterns for drift,
poisoning, unauth
overwrites.
●Detect task replay, inﬁnite
delegation, or hallucination.
●Enable human-in-the-loop
override thresholds on
high-risk actions.
●Continuously scan loaded
plugins for CVEs and
privilege escalation vectors.
●Runtime guardrails  and
moderation, and tool use.
●Align control evidence with frameworks like EU AI
Act, NIST AI RMF, and ISO/IEC 42001.
●Automate goal alignment audits, including
adversarial review of long-term agent memory.
●Enforce role- and task-based access policies
across agent populations and tool access.
●Automate agent versioning, expiration, and
rotation policies.
The Agentic AI SecOps Framework  addresses the evolving security
demands of next-generation AI systems as they transition from simple
large language model (LLM) calls to fully autonomous, multi-agent
architectures. The framework extends existing DevOps and SecOps
methodologies to promote secure Agentic AI development, ensuring
that organizations can maintain security, reliability, compliance, and
auditability while safely embracing the capabilities of agentic AI.
OWASP Agentic AI SecOps Framework
### Cheat Sheet
Govern
Plan & Scope
Augment &
Fine Tune Data
Dev & Experiment
Test & Evaluation
Release
Deploy
Operate
genai.owasp.org

<!-- page 6 -->
Scope & Plan
During planning of agentic AI apps, SecOps and DevOps must embed
security in the design, focusing on non-human identities, agent threat
modeling, privilege boundaries, and authentication. Memory scoping
and isolation are critical to prevent data leaks. Early collaboration
aligns agent workﬂows and tools with enforceable security, unlike
traditional post-design security.
Open Source
Gold Sponsors
Silver Sponsors
Agentic AI Security Landscape - Q2/3 2025
### Cheat Sheet
genai.owasp.org
Agentic DevOps
Agentic SecOps
●
Deﬁne the business goal and translate into
agent goals & roles
●
Choose model families (chat-LLM vs.
multimodal) & hosting mode.
●
Deﬁne agent architecture patterns (single,
hierarchical, swarm)
●
Identify  external services and tooling
●
Design inter-agent communication and tool
workﬂows
●
Select memory pattern (short-term context
vs long-term e.g. vector DB).
●
Create initial threat model and Service Level
Objectives.
●
Conduct agentic threat modeling (referencing
the threat modeling approach from the GenAI
Security Project - Agentic Security Initiative)
●
Identify system-wide non-human identities
(NHIs) and determine authentication protocols
(e.g., SPIFFE, mTLS).
●
Draft policies for agent privilege boundaries,
tool scopes (e.g., MCP), and delegation logic.
●
Deﬁne controls for memory scoping, isolation,
and long-term persistence rules.

<!-- page 7 -->
Augment, Fine Tune Data
In data augmentation & ﬁne-tuning, SecOps works with DevOps to
prevent risks from poisoned data, adversarial tuning, and
reasoning traces. They sanitize datasets, validate alignment, log
provenance, and protect sensitive memory with privacy controls.
This ensures compliant, trustworthy agentic AI before deployment.
Open Source
Gold Sponsors
Silver Sponsors
Agentic AI Security Landscape - Q2/3 2025
### Cheat Sheet
genai.owasp.org
Agentic DevOps
Agentic SecOps
●
Collect domain-speciﬁc corpora that agents
will reference during planning & reﬂection.
●
Generate tool-schema embeddings so
planners can choose the right action.
●
Fine-tune/reﬁne LLM on task-speciﬁc
dialogues that include multi-step reasoning
traces (ReAct, Tree-of-Thought).
●
Populate seed “agent memory” (company
knowledge, rules).
●
Scan datasets for prompt-poisoning, biased
instructions, or encoded policy bypasses.
●
Validate RLHF traces for ethical alignment,
adversarial manipulation, or leakage of secrets.
●
Register data lineage and provenance in
immutable logs.
●
Apply differential privacy or obfuscation on
sensitive knowledge injected into agent memory.
●
Agent Action Audit

<!-- page 8 -->
Develop & Experiment
In the Development & Experimentation phase of agentic AI, SecOps
partners with DevOps to secure dynamic agent loops, inter-agent
comms, and API/plugin use. They validate I/O contracts, embed
policy hooks, and test resilience to prevent unsafe behaviors.
Security shifts from static code focus to real-time orchestration and
co-engineering secure experimentation.
Open Source
Gold Sponsors
Silver Sponsors
Agentic AI Security Landscape - Q2/3 2025
### Cheat Sheet
genai.owasp.org
Agentic DevOps
Agentic SecOps
●
Implement agent loops
(Observe-Plan-Act-Reﬂect) with frameworks
such as LangGraph / AutoGen.
●
Build manager-worker graphs; encode
delegation policies.
●
Wire plugins for each external API (e.g., MCP)
and enforce input/output schemas.
●
Prototype interagent protocol (e.g. A2A)
handshake and capability negotiation.
●
Iterate on prompts, system instructions, and
guard-functions; run sandbox tests.
●
Perform SAST/DAST on agent planning code, tool
wrappers, and plugin interfaces.
●
Harden agent loop logic against inﬁnite loops,
unsafe function routing, and unauthorized
self-modiﬁcation.
●
Validate connector (e.g., MCP)  contracts
(input/output schemas and permissions).
●
Implement policy enforcement hooks in
Frameworks
o
e.g. LangGraph, CrewAI, or Semantic
Kernel ﬂows.

<!-- page 9 -->
Open Source
Gold Sponsors
Silver Sponsors
Agentic AI Security Landscape - Q2/3 2025
### Cheat Sheet
Test & Evaluate
In Test & Evaluation, SecOps partners with DevOps to
stress-test agentic AI in adversarial conditions, targeting
emergent risks like goal drift, prompt injection, and tool misuse.
They run red-team simulations, sandbox tool/API calls, and
validate decisions in multi-agent setups, focusing on behavioral
security beyond traditional QA or pen testing.
### Eunomatix
genai.owasp.org
Agentic DevOps
Agentic SecOps
●
Spin up synthetic multi-agent
arenas to stress-test
negotiation, bidding and
consensus ﬂows.
●
Run goal-drift,
prompt-injection, and
resource-exhaustion scenarios
against the planner.
●
Benchmark reﬂection latency
and memory-poisoning
resilience.
●
Validate generated tool calls in
a sandbox for RCE / over-scope.
●
Available Agent Scanning
●
Conduct adversarial red-teaming:
goal drift, prompt injection,
hallucination chaining, and
over-permissioned tool usage.
●
Run multi-agent scenario
simulations for collusion,
misalignment, or deception
detection.
●
Validate agent decisions against
expected goal plans.
●
Sandboxed testing of all tool
calls—particularly code execution
or cloud API triggers.

<!-- page 10 -->
Release
In the Release phase, SecOps teams work with DevOps to
securely package, validate, and register agentic AI apps. They
sign model weights, plugins, and memory to prevent tampering,
verify SBOMs for all components, enforce cryptographically
validated policies, and register agents in secure capability
registries, ensuring trusted, auditable deployments.
Open Source
Gold Sponsors
Silver Sponsors
Agentic AI Security Landscape - Q2/3 2025
### Cheat Sheet
genai.owasp.org
Agentic DevOps
Agentic SecOps
●
Package agent graphs, plugins, policies, and
memory snapshots
●
Generate Model & Tool SBOMs; sign artefacts
(Sigstore). - shared responsibility
●
Publish agent capability-cards to an internal
A2A registry.
●
Generate and verify model + agent + tool SBOMs -
shared responsibility
●
Sign model weights, plugin manifests, and
memory snapshots.
●
Ensure policy bundles (e.g., OPA/Rego) are
cryptographically validated at deploy time.
●
Register all agents in an internal trust registry
with capability descriptors.

<!-- page 11 -->
Deploy
In the Deploy phase, SecOps partners with DevOps to enable secure,
policy-compliant activation of agentic AI. They enforce zero-trust
comms, rotate ephemeral credentials, set LLM ﬁrewalls and
allowlists, and apply ﬁne-grained authorization so each agent runs
with least privilege, reducing risks in multi-agent environments.
Open Source
Gold Sponsors
Silver Sponsors
Agentic AI Security Landscape - Q2/3 2025
### Cheat Sheet
genai.owasp.org
Agentic DevOps
Agentic SecOps
●
Provision vector DB, memory store, tool
side-cars, and service-mesh with mTLS for
A2A traffic.
●
Apply least-privilege IAM roles to every agent
(non-human identities).
●
Load initial long-term memory and register
agents with discovery service.
●
Enable runtime guardrails / LLM ﬁrewall
●
Enforce zero-trust policies between agents,
tools, and external APIs via mTLS and
ﬁne-grained RBAC.
●
Rotate all shared secrets, keys, and tokens with
ephemeral, scoped credentials.
●
Apply runtime guardrails (e.g., LLM ﬁrewalls, tool
allowlists) before production traffic is enabled.
●
Conﬁgure inter-agent authorization policies
based on capabilities and roles

<!-- page 12 -->
Operate
In the Operate phase, SecOps teams partner with DevOps to secure the
dynamic footprint of agentic AI, where agents evolve, adapt, and act in
changing environments. They monitor memory mutations to prevent drift
or poisoning, detect abnormal loops or misuse, enforce HITL overrides,
and scan plugins for risks. This persistent, real-time vigilance ensures
secure, resilient operations as systems scale and self-orchestrate.
Open Source
Gold Sponsors
Silver Sponsors
Agentic AI Security Landscape - Q2/3 2025
### Cheat Sheet
genai.owasp.org
Agentic DevOps
Agentic SecOps
●
Run SRE playbooks: auto-scale inference pods,
rotate keys/tokens, prune memory.
●
Collect feedback / RLHF traces; schedule periodic
self-evaluation tasks.
●
Trigger automated reﬂection or human-in-the-loop
when agent conﬁdence drops.
●
- Orchestrate inter-agent workﬂows.
●
Monitor agent memory mutation patterns for
drift, poisoning, or unauthorized overwrites.
●
Detect task replay, inﬁnite delegation, or
hallucination loops.
●
Enable human-in-the-loop (HITL) override
thresholds on high-risk or ambiguous actions.
●
Continuously scan loaded plugins for CVEs and
privilege escalation vectors.
●
Runtime guardrails & moderation; anomalous
tool use.

<!-- page 13 -->
Open Source
Gold Sponsors
Silver Sponsors
Agentic AI Security Landscape - Q2/3 2025
### Cheat Sheet
Monitor
In the Monitor phase, SecOps teams collaborate with DevOps
to secure agentic AI’s dynamic, evolving footprint. Unlike
static systems, these agents produce context-rich traces that
shift with reasoning and interactions. SecOps correlates
agent steps, tool calls, and inter-agent comms to catch
anomalies like goal reversal or adversarial inputs, using
immutable logs and audits to drive proactive, behavior-aware
security.
genai.owasp.org
Agentic DevOps
Agentic SecOps
●
Stream agent-step telemetry
via OpenTelemetry; correlate
tool errors with planning nodes.
●
Track KPIs: goal-completion
rate, average reasoning depth,
vector-store growth,
inter-agent latency.
●
Alert on anomaly patterns
(looping, hallucination
cascades, excessive privilege
use).
●
Correlate telemetry from agent
step tracing, tool execution, and
message logs.
●
Alert on anomalies like goal
reversal, unexpected plan depth,
adversarial-input, excessive tool
usage, or rapid inter-agent chatter.
●
Audit reﬂection accuracy by
comparing stated and observed
planning outcomes.
●
Use immutable logs (e.g., Sigstore,
Immudb) for forensic readiness.

<!-- page 14 -->
Open Source
Gold Sponsors
Silver Sponsors
Agentic AI Security Landscape - Q2/3 2025
### Cheat Sheet
Govern
In the Govern phase, SecOps partners with DevOps to uphold
compliance, access control, and lifecycle governance for
evolving agentic AI. They enforce role- and task-based policies,
automate agent versioning and retirement, and guard against
privilege creep. With immutable logs, audits, and alignment to
AI regulations, they ensure long-term security, accountability,
and trust in dynamic multi-agent systems.
genai.owasp.org
Agentic DevOps
LLMSecOps
●
Maintain registry of agent
versions, roles, and approved
tools; enforce retirement policy.
●
Run quarterly attestation of A2A
trust graph and MCP connector
scopes.
●
Archive immutable logs for audit;
map evidence to EU AI Act / NIST
RMF controls.
●
Periodically review alignment
metrics and update
constitutional rules.
●
Enforce role- and task-based
access policies across agent
populations and their tool access.
●
Automate agent versioning,
expiration, and rotation policies.
●
Align control evidence with
frameworks like EU AI Act, NIST AI
RMF, and ISO/IEC 42001.
●
Automate goal alignment audits,
including adversarial review of
long-term agent memory.

<!-- page 15 -->
Acknowledgement
OWASP Gen AI Solutions Landscape Initiative :
Lead:  Scott Clinton
Contributors
Reviewers
Initiative Slack Channel: #team-genai-ai-solutions-landscape-initiative
Andy Smith
Arun John
Aurora Starita
Blanca Rivera Campos
Bryan Nakayama
Dan Guido
Dennys Pereira
Emmanuel Guilherme
Fabrizio Cilli
Garvin LeClaire
Heather Linn
Helen Oakley
Ishan Anand
Jason Ross
Joshua Berkoh
Marcel Winandy
Markus Hupfauer
Migel Fernandes
Mohit Yadav
Rachel James
Rammohan Thirupasur
Rico Komenda
Rammohan Thirupasur
Talesh Seeparsan
Teruhiro Tagomori
Todd Hathaway
Ron F. Del Rosario
Vaibhav Malik
Aurora Starita
Bryan Nakayama
Dennys Pereira
Emmanuel Guilherme
Fabrizio Cilli
Garvin LeClaire
Helen Oakley
Ishan Anand
Jason Ross
Marcel Winandy
Markus Hupfauer
Migel Fernandes
Mohit Yadav
Rachel James
Rico Komenda
Talesh Seeparsan
Teruhiro Tagomori
Todd Hathaway
Ron F. Del Rosario
Vaibhav Malik

<!-- page 16 -->
Gen AI Security Project Sponsors
Supporting Community Operations And Outreach Through Direct Financial Sponsorship

<!-- page 17 -->
Contributing to the Landscape Guide
Use the QR Code and
associated form to submit
an Agentic AI Security
Landscape entry
For Agentic AI
