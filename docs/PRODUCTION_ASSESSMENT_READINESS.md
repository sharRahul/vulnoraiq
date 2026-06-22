# Production Assessment Readiness

VulnoraIQ now includes an authorised production-assessment testing path for OWASP LLM application review.

This readiness level means the framework can run controlled checks against systems the tester owns or is explicitly authorised to assess. It does not certify exploitability, business impact, regulatory compliance, or final risk acceptance without human tester review.

## Implemented readiness controls

- Production OWASP detector rules for all 10 OWASP LLM 2025 categories.
- Per-interaction detector status, verdict, confidence, risk score, matched signals, and missing-evidence tracking.
- Scanner metadata for the active production detector profile and coverage count.
- Functional acceptance validation that checks the production detector coverage marker.
- Readiness validation that runs the demo full profile and verifies detector failures are not present in the safe local path.
- Explicit non-demo authorisation gate before configured target testing.

## Required operating conditions

1. Only assess owned or explicitly approved targets.
2. Replace placeholder endpoints in `config/targets.yaml`.
3. Validate target contracts before testing.
4. Preserve generated Markdown, JSON, SARIF, dashboard, and readiness artifacts.
5. Review every finding manually before treating it as confirmed risk.
