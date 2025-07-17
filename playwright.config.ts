import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests/e2e',
  fullyParallel: false,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: 1,
  reporter: 'html',
  use: {
    baseURL: 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
  },

  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
  ],

  webServer: [
    {
      command: 'cd backend && python3 -m uvicorn main:app --host 127.0.0.1 --port 8000',
      port: 8000,
      timeout: 120 * 1000,
      reuseExistingServer: true,
    },
    {
      command: 'npm run dev',
      port: 3000,
      timeout: 120 * 1000,
      reuseExistingServer: true,
    },
  ],
});