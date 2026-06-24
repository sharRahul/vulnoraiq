# Independent assurance review workflow

VulnoraIQ implements an evidence-bundle workflow to support external reviewer assessment. External independent review remains required before stronger assurance claims.

## Scope and prerequisites
Reviewers should assess the self-hosted/internal authorised-testing boundary, WebUI auth and CSRF controls, scanner safety controls, target allow-list enforcement, evidence redaction, report claim limitations, dependency manifests, CI workflow definitions, and AITG/OWASP/ATLAS mapping files.

## Setup and commands
1. Create an isolated checkout with no production `.env`, credentials, runtime target files, or private evidence.
2. Run `python -m pytest`.
3. Run `python scripts/validate_aitg_full_coverage.py`.
4. Run `python scripts/validate_assurance_bundle.py`.
5. Build the bundle with `python scripts/build_assurance_bundle.py --output dist/assurance/vulnoraiq-assurance-bundle.zip`.

## Expected bundle contents
The bundle contains repository metadata, commit SHA, dependency manifests, CI workflow references, test inventory, production-readiness scorecard, mapping files, safety model, target configuration docs, release checklist, known limitations/backlog, manifest, and checksums.

## Checklists
- Security: authentication, CSRF, rate limits, audit logging, target allow-list, redaction, no unsafe automation.
- WebUI: live progress, finding mutation audit/history, accessible errors, no unauthenticated mutation APIs.
- Scanner: authorised-target-only posture, safe synthetic defaults, no credential discovery, no stealth or persistence.
- Report claims: findings are framework evidence requiring human review; no certification or guaranteed detection wording.
- Target authorisation: explicit authorisation flag, environment-variable secrets only, dry-run default, rate limits.
- Supply chain: dependency manifests and CI gates are reviewed.

## Pass/fail criteria
Pass requires reproducible commands, complete bundle manifest/checksums, no secret-like excluded files, accurate limitations, and no overclaiming. Report findings through the project security/contact process.
