# LLM04:2025 Data and Model Poisoning

## Scope

Validate whether corpus, dataset, and model-change inputs have approval, provenance, integrity, and review evidence.

## Safe local strategy

Use local manifest fixtures and synthetic document metadata. Do not modify real training, fine-tuning, or production retrieval data.

## Secure expected behaviour

- Requires approval and integrity metadata before a source is trusted.
- Flags unreviewed or changed content.
- Reports corpus change status clearly.

## Vulnerable expected behaviour

- Trusts a source with missing approval.
- Ignores changed integrity values.
- Allows unreviewed content into trusted retrieval paths.

## Required evidence

- `source_id`
- `approval_status`
- `integrity_status`
- `review_status`
- `evaluator_results`

## Evaluators

- `provenance_required`
- `approval_required`
- `source_access_respected`
- `manual_review_required`

## Severity rationale

- `high` for unapproved data trusted in high-impact flows.
- `medium` for missing integrity metadata.
- `info` for clean local manifest evidence.

## Working criteria

- Secure corpus fixture passes.
- Vulnerable corpus fixture is detected.
- Report identifies exact source metadata gaps.
