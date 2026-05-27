import { test, expect } from '@playwright/test';

test.describe('JoSAA Top 25 Tool', () => {
  test('default run renders results', async ({ page }) => {
    await page.goto('/tools/josaa-top-25');
    await page.getByLabel(/jee rank/i).fill('15000');
    await page.getByRole('button', { name: /generate top 25/i }).click();
    await expect(page.getByText(/candidate pool after filters/i)).toBeVisible();
    await expect(page.locator('table')).toBeVisible();
  });

  test('constrained run and compare rank columns', async ({ page }) => {
    await page.goto('/tools/josaa-top-25');
    await page.getByLabel(/jee rank/i).fill('12000');
    await page.getByLabel(/compare with another rank/i).fill('18000');
    await page.getByLabel(/preferred branches/i).fill('computer science');
    await page.getByLabel(/preferred institutes/i).fill('iit');
    await page.getByRole('button', { name: /generate top 25/i }).click();
    await expect(page.getByText(/compare %/i)).toBeVisible();
  });

  test('no-result path is graceful', async ({ page }) => {
    await page.goto('/tools/josaa-top-25');
    await page.getByLabel(/jee rank/i).fill('999999');
    await page.getByLabel(/preferred institutes/i).fill('some impossible institute xyz');
    await page.getByRole('button', { name: /generate top 25/i }).click();
    await expect(page.getByText(/no matching programs found/i)).toBeVisible();
  });

  test('export csv appears after result', async ({ page }) => {
    await page.goto('/tools/josaa-top-25');
    await page.getByLabel(/jee rank/i).fill('22000');
    await page.getByRole('button', { name: /generate top 25/i }).click();
    const exportBtn = page.getByRole('button', { name: /export top 25 csv/i });
    await expect(exportBtn).toBeVisible();
  });
});
