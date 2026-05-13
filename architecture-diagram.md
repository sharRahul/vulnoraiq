# Architecture Diagram (Logical)

```
+----------------------+
|   Target AI Systems  |
| LLMs | RAG | Agents  |
+----------+-----------+
           |
           v
+----------------------+
|   Integration Layer  |
| APIs | SDKs | Agents |
+----------+-----------+
           |
           v
+----------------------+
|  VAPT Core Engine    |
| Scanner | Orchestrator|
| Attack Engine        |
+----------+-----------+
           |
           v
+----------------------+
|  Testing Modules     |
| OWASP LLM Modules    |
| RAG Testing          |
| Agent Testing        |
+----------+-----------+
           |
           v
+----------------------+
|  Analysis & Scoring  |
| Risk Engine          |
| Detection Logic      |
+----------+-----------+
           |
           v
+----------------------+
| Reporting & Dashboard|
| Reports | Metrics    |
+----------------------+
```
