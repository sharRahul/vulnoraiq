# OWASP LLM Modules

This folder is reserved for concrete OWASP LLM Top 10 2025 test modules.

The current runnable foundation maps module keys in `core/test_runner.py` so the framework can run immediately. As the project matures, each mapped key should be expanded into its own package:

- `owasp_llm01_prompt_injection/`
- `owasp_llm02_sensitive_information_disclosure/`
- `owasp_llm03_supply_chain/`
- `owasp_llm04_data_and_model_poisoning/`
- `owasp_llm05_improper_output_handling/`
- `owasp_llm06_excessive_agency/`
- `owasp_llm07_system_prompt_leakage/`
- `owasp_llm08_vector_embedding_weaknesses/`
- `owasp_llm09_misinformation/`
- `owasp_llm10_unbounded_consumption/`

Every module should return findings with severity, OWASP mapping, evidence, affected component, recommendation, and optional MITRE ATLAS metadata.
