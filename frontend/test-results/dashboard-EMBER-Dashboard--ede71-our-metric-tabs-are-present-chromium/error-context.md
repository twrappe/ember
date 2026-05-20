# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: dashboard.spec.ts >> EMBER Dashboard >> Biometric Chart >> all four metric tabs are present
- Location: tests\e2e\dashboard.spec.ts:94:5

# Error details

```
Error: expect(locator).toBeVisible() failed

Locator: getByTestId('tab-hrv')
Expected: visible
Timeout: 5000ms
Error: element(s) not found

Call log:
  - Expect "toBeVisible" with timeout 5000ms
  - waiting for getByTestId('tab-hrv')

```

```yaml
- banner:
  - text: EMBER
  - button "Refresh data":
    - img
- main:
  - text: ⚠ Failed to fetch
  - button "Retry"
```

# Test source

```ts
  1   | import { test, expect } from '@playwright/test';
  2   | 
  3   | test.describe('EMBER Dashboard', () => {
  4   | 
  5   |   test.beforeEach(async ({ page }) => {
  6   |     await page.goto('/');
  7   |   });
  8   | 
  9   |   // ──────────────────────────────────────────────
  10  |   // Layout & header
  11  |   // ──────────────────────────────────────────────
  12  |   test('renders app shell and header', async ({ page }) => {
  13  |     await expect(page.getByTestId('ember-app')).toBeVisible();
  14  |     await expect(page.getByTestId('header')).toBeVisible();
  15  |     await expect(page.locator('.logo-text')).toHaveText('EMBER');
  16  |     await expect(page.locator('.sync-info')).toContainText('Synced');
  17  |   });
  18  | 
  19  |   // ──────────────────────────────────────────────
  20  |   // Risk Gauge
  21  |   // ──────────────────────────────────────────────
  22  |   test.describe('Risk Gauge', () => {
  23  |     test('renders risk card with gauge', async ({ page }) => {
  24  |       await expect(page.getByTestId('risk-card')).toBeVisible();
  25  |       await expect(page.getByTestId('risk-gauge')).toBeVisible();
  26  |     });
  27  | 
  28  |     test('displays numeric risk score', async ({ page }) => {
  29  |       const gauge = page.getByTestId('risk-gauge');
  30  |       const scoreText = gauge.locator('text').first();
  31  |       await expect(scoreText).toBeVisible();
  32  |       const text = await scoreText.textContent();
  33  |       expect(Number(text)).toBeGreaterThanOrEqual(0);
  34  |       expect(Number(text)).toBeLessThanOrEqual(100);
  35  |     });
  36  | 
  37  |     test('risk caption is displayed', async ({ page }) => {
  38  |       await expect(page.locator('.risk-caption')).toBeVisible();
  39  |     });
  40  |   });
  41  | 
  42  |   // ──────────────────────────────────────────────
  43  |   // Alert Panel
  44  |   // ──────────────────────────────────────────────
  45  |   test.describe('Alert Panel', () => {
  46  |     test('renders alert panel', async ({ page }) => {
  47  |       await expect(page.getByTestId('alert-panel')).toBeVisible();
  48  |     });
  49  | 
  50  |     test('shows correct alert count badge', async ({ page }) => {
  51  |       const badge = page.getByTestId('alert-count');
  52  |       await expect(badge).toBeVisible();
  53  |       const count = await badge.textContent();
  54  |       expect(Number(count)).toBeGreaterThan(0);
  55  |     });
  56  | 
  57  |     test('renders high severity alerts', async ({ page }) => {
  58  |       const highAlerts = page.locator('[data-severity="high"]');
  59  |       await expect(highAlerts.first()).toBeVisible();
  60  |     });
  61  | 
  62  |     test('dismissing an alert removes it from the panel', async ({ page }) => {
  63  |       // Count initial alerts
  64  |       const initialAlerts = await page.locator('.alert-item').count();
  65  |       expect(initialAlerts).toBeGreaterThan(0);
  66  | 
  67  |       // Dismiss first alert
  68  |       const firstDismiss = page.locator('.dismiss-btn').first();
  69  |       await firstDismiss.click();
  70  | 
  71  |       // Count should decrease
  72  |       await expect(page.locator('.alert-item')).toHaveCount(initialAlerts - 1);
  73  |     });
  74  | 
  75  |     test('shows no-alerts state after dismissing all', async ({ page }) => {
  76  |       // Dismiss all alerts
  77  |       while (await page.locator('.dismiss-btn').count() > 0) {
  78  |         await page.locator('.dismiss-btn').first().click();
  79  |       }
  80  |       await expect(page.getByTestId('no-alerts')).toBeVisible();
  81  |       await expect(page.getByTestId('alert-count')).not.toBeVisible();
  82  |     });
  83  |   });
  84  | 
  85  |   // ──────────────────────────────────────────────
  86  |   // Biometric Chart
  87  |   // ──────────────────────────────────────────────
  88  |   test.describe('Biometric Chart', () => {
  89  |     test('renders chart card with metric tabs', async ({ page }) => {
  90  |       await expect(page.getByTestId('chart-card')).toBeVisible();
  91  |       await expect(page.getByTestId('metric-tabs')).toBeVisible();
  92  |     });
  93  | 
  94  |     test('all four metric tabs are present', async ({ page }) => {
> 95  |       await expect(page.getByTestId('tab-hrv')).toBeVisible();
      |                                                 ^ Error: expect(locator).toBeVisible() failed
  96  |       await expect(page.getByTestId('tab-sleep')).toBeVisible();
  97  |       await expect(page.getByTestId('tab-readiness')).toBeVisible();
  98  |       await expect(page.getByTestId('tab-riskScore')).toBeVisible();
  99  |     });
  100 | 
  101 |     test('riskScore tab is active by default', async ({ page }) => {
  102 |       const riskTab = page.getByTestId('tab-riskScore');
  103 |       await expect(riskTab).toHaveClass(/active/);
  104 |     });
  105 | 
  106 |     test('clicking HRV tab switches chart metric', async ({ page }) => {
  107 |       await page.getByTestId('tab-hrv').click();
  108 |       await expect(page.getByTestId('tab-hrv')).toHaveClass(/active/);
  109 |       await expect(page.getByTestId('tab-riskScore')).not.toHaveClass(/active/);
  110 |       await expect(page.getByTestId('biometric-chart')).toHaveAttribute('data-metric', 'hrv');
  111 |     });
  112 | 
  113 |     test('clicking Sleep tab switches chart metric', async ({ page }) => {
  114 |       await page.getByTestId('tab-sleep').click();
  115 |       await expect(page.getByTestId('biometric-chart')).toHaveAttribute('data-metric', 'sleep');
  116 |     });
  117 | 
  118 |     test('chart renders recharts SVG', async ({ page }) => {
  119 |       await expect(page.locator('.recharts-responsive-container')).toBeVisible();
  120 |       await expect(page.locator('.recharts-line')).toBeVisible();
  121 |     });
  122 |   });
  123 | 
  124 |   // ──────────────────────────────────────────────
  125 |   // Accessibility
  126 |   // ──────────────────────────────────────────────
  127 |   test.describe('Accessibility', () => {
  128 |     test('dismiss buttons have aria-labels', async ({ page }) => {
  129 |       const dismissBtns = page.locator('.dismiss-btn');
  130 |       const count = await dismissBtns.count();
  131 |       for (let i = 0; i < count; i++) {
  132 |         await expect(dismissBtns.nth(i)).toHaveAttribute('aria-label');
  133 |       }
  134 |     });
  135 |   });
  136 | });
  137 | 
```