import { test, expect } from '@playwright/test';

test.describe('EMBER Dashboard', () => {

  test.beforeEach(async ({ page }) => {
    await page.goto('/');
  });

  // ──────────────────────────────────────────────
  // Layout & header
  // ──────────────────────────────────────────────
  test('renders app shell and header', async ({ page }) => {
    await expect(page.getByTestId('ember-app')).toBeVisible();
    await expect(page.getByTestId('header')).toBeVisible();
    await expect(page.locator('.logo-text')).toHaveText('EMBER');
    await expect(page.locator('.sync-info')).toContainText('Synced');
  });

  // ──────────────────────────────────────────────
  // Risk Gauge
  // ──────────────────────────────────────────────
  test.describe('Risk Gauge', () => {
    test('renders risk card with gauge', async ({ page }) => {
      await expect(page.getByTestId('risk-card')).toBeVisible();
      await expect(page.getByTestId('risk-gauge')).toBeVisible();
    });

    test('displays numeric risk score', async ({ page }) => {
      const gauge = page.getByTestId('risk-gauge');
      const scoreText = gauge.locator('text').first();
      await expect(scoreText).toBeVisible();
      const text = await scoreText.textContent();
      expect(Number(text)).toBeGreaterThanOrEqual(0);
      expect(Number(text)).toBeLessThanOrEqual(100);
    });

    test('risk caption is displayed', async ({ page }) => {
      await expect(page.locator('.risk-caption')).toBeVisible();
    });
  });

  // ──────────────────────────────────────────────
  // Alert Panel
  // ──────────────────────────────────────────────
  test.describe('Alert Panel', () => {
    test('renders alert panel', async ({ page }) => {
      await expect(page.getByTestId('alert-panel')).toBeVisible();
    });

    test('shows correct alert count badge', async ({ page }) => {
      const badge = page.getByTestId('alert-count');
      await expect(badge).toBeVisible();
      const count = await badge.textContent();
      expect(Number(count)).toBeGreaterThan(0);
    });

    test('renders high severity alerts', async ({ page }) => {
      const highAlerts = page.locator('[data-severity="high"]');
      await expect(highAlerts.first()).toBeVisible();
    });

    test('dismissing an alert removes it from the panel', async ({ page }) => {
      // Count initial alerts
      const initialAlerts = await page.locator('.alert-item').count();
      expect(initialAlerts).toBeGreaterThan(0);

      // Dismiss first alert
      const firstDismiss = page.locator('.dismiss-btn').first();
      await firstDismiss.click();

      // Count should decrease
      await expect(page.locator('.alert-item')).toHaveCount(initialAlerts - 1);
    });

    test('shows no-alerts state after dismissing all', async ({ page }) => {
      // Dismiss all alerts
      while (await page.locator('.dismiss-btn').count() > 0) {
        await page.locator('.dismiss-btn').first().click();
      }
      await expect(page.getByTestId('no-alerts')).toBeVisible();
      await expect(page.getByTestId('alert-count')).not.toBeVisible();
    });
  });

  // ──────────────────────────────────────────────
  // Biometric Chart
  // ──────────────────────────────────────────────
  test.describe('Biometric Chart', () => {
    test('renders chart card with metric tabs', async ({ page }) => {
      await expect(page.getByTestId('chart-card')).toBeVisible();
      await expect(page.getByTestId('metric-tabs')).toBeVisible();
    });

    test('all four metric tabs are present', async ({ page }) => {
      await expect(page.getByTestId('tab-hrv')).toBeVisible();
      await expect(page.getByTestId('tab-sleep')).toBeVisible();
      await expect(page.getByTestId('tab-readiness')).toBeVisible();
      await expect(page.getByTestId('tab-riskScore')).toBeVisible();
    });

    test('riskScore tab is active by default', async ({ page }) => {
      const riskTab = page.getByTestId('tab-riskScore');
      await expect(riskTab).toHaveClass(/active/);
    });

    test('clicking HRV tab switches chart metric', async ({ page }) => {
      await page.getByTestId('tab-hrv').click();
      await expect(page.getByTestId('tab-hrv')).toHaveClass(/active/);
      await expect(page.getByTestId('tab-riskScore')).not.toHaveClass(/active/);
      await expect(page.getByTestId('biometric-chart')).toHaveAttribute('data-metric', 'hrv');
    });

    test('clicking Sleep tab switches chart metric', async ({ page }) => {
      await page.getByTestId('tab-sleep').click();
      await expect(page.getByTestId('biometric-chart')).toHaveAttribute('data-metric', 'sleep');
    });

    test('chart renders recharts SVG', async ({ page }) => {
      await expect(page.locator('.recharts-responsive-container')).toBeVisible();
      await expect(page.locator('.recharts-line')).toBeVisible();
    });
  });

  // ──────────────────────────────────────────────
  // Accessibility
  // ──────────────────────────────────────────────
  test.describe('Accessibility', () => {
    test('dismiss buttons have aria-labels', async ({ page }) => {
      const dismissBtns = page.locator('.dismiss-btn');
      const count = await dismissBtns.count();
      for (let i = 0; i < count; i++) {
        await expect(dismissBtns.nth(i)).toHaveAttribute('aria-label');
      }
    });
  });
});
