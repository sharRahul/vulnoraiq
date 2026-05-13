# RAG Testing Layer

This folder is for Retrieval-Augmented Generation security checks.

Planned modules:

- `rag_poisoning.py` - safe poisoning simulation and corpus trust checks
- `retrieval_manipulation.py` - retrieval ranking, metadata, and source-filter manipulation checks
- `embedding_attacks.py` - embedding collision, similarity abuse, and vector-store weakness checks
- `corpus_validation.py` - source lineage, hash, approval, and freshness checks

Primary OWASP LLM 2025 alignment:

- LLM04: Data and Model Poisoning
- LLM08: Vector and Embedding Weaknesses
- LLM02: Sensitive Information Disclosure, where retrieval exposes unauthorised context
