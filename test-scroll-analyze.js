const { chromium } = require('playwright');

async function scrollAndCapture() {
  const browser = await chromium.launch();
  const page = await browser.newContext().then(c => c.newPage());
  
  await page.goto('http://localhost:3003/analyze');
  await page.waitForLoadState('networkidle');
  
  // Scroll down to see if results are below
  await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
  
  await page.screenshot({ path: 'test-screenshots/14-analyze-scrolled.png', fullPage: true });
  
  await browser.close();
}

scrollAndCapture();