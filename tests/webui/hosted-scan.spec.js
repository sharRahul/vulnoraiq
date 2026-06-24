const { test, expect } = require('@playwright/test');

async function selectPreferredOption(page, selector, preferredValue) {
  await page.waitForFunction((selectSelector) => {
    const select = document.querySelector(selectSelector);
    return select && select.options.length > 0;
  }, selector);
  const values = await page.locator(`${selector} option`).evaluateAll((options) => options.map((option) => option.value));
  const selected = values.includes(preferredValue) ? preferredValue : values[0];
  await page.locator(selector).selectOption(selected);
  return selected;
}

async function latestJob(page) {
  const response = await page.request.get('/api/scans');
  expect(response.ok()).toBeTruthy();
  const data = await response.json();
  return (data.jobs || [])[0] || null;
}

test('starts a hosted demo scan through the WebUI', async ({ page }) => {
  await page.goto('/');
  await expect(page.getByRole('heading', { name: 'VulnoraIQ', exact: true })).toBeVisible();

  const target = await selectPreferredOption(page, '#target-select', 'demo');
  const profile = await selectPreferredOption(page, '#profile-select', 'baseline');

  await expect(page.locator('#active-scan-elapsed')).toBeVisible();
  await expect(page.locator('#active-scan-eta')).toBeVisible();

  await page.getByRole('button', { name: 'Start selected assessment' }).click();
  await expect(page.locator('#active-scan-card')).not.toHaveClass(/idle/);

  await expect.poll(async () => {
    const job = await latestJob(page);
    return job && job.target === target && job.profile === profile ? 'created' : 'missing';
  }, { timeout: 30_000, intervals: [500, 1000, 2000] }).toBe('created');

  const job = await latestJob(page);
  expect(job).toBeTruthy();
  expect(job.id).toBeTruthy();
  expect(['queued', 'running', 'completed', 'failed']).toContain(job.status);
});
