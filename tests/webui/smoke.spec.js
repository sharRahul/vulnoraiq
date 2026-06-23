const { test, expect } = require('@playwright/test');

test('loads the console shell', async ({ page }) => {
  await page.goto('/');
  await expect(page.getByRole('heading', { name: 'VulnoraIQ', exact: true })).toBeVisible();
  await expect(page.getByRole('heading', { name: 'Choose tests and run scan' })).toBeVisible();
});
