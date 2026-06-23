# WebUI Testing

The WebUI test layer adds browser-level smoke coverage on top of the existing Python CI gates.

## Local commands

```bash
python -m pip install -e .[dev]
npm install
npx playwright install chromium
npm run test:webui
```

The Playwright configuration starts the hosted WebUI on `127.0.0.1:8787` with authentication disabled and writes temporary job output under `reports/output/webui-playwright`.

## CI behavior

Browser tests run only on the Python 3.12 CI matrix leg to avoid multiplying browser setup across all supported Python versions. The existing Python lint, type-check, pytest, package metadata, mapping, readiness, and demo scan gates remain unchanged.

## Current coverage

- Loads the static console shell.
- Verifies the primary VulnoraIQ and scan-selection headings render.

## Future coverage

- Login/token flow when auth is enabled.
- Demo scan queueing and dashboard rendering.
- Catalog, history, and findings filtering.
- Accessibility checks with axe once the layout stabilizes.
- Advisory visual snapshots before turning visual regression into a required gate.
