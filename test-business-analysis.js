const { chromium } = require('playwright');
const fs = require('fs').promises;
const path = require('path');

// Create screenshots directory
const screenshotsDir = path.join(__dirname, 'test-screenshots');

async function ensureDir(dir) {
  try {
    await fs.mkdir(dir, { recursive: true });
  } catch (error) {
    console.error('Error creating directory:', error);
  }
}

async function takeScreenshot(page, name) {
  const screenshotPath = path.join(screenshotsDir, `${name}.png`);
  await page.screenshot({ path: screenshotPath, fullPage: true });
  console.log(`Screenshot saved: ${screenshotPath}`);
}

async function testBusinessAnalysis() {
  await ensureDir(screenshotsDir);
  
  const browser = await chromium.launch({ 
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });
  
  const context = await browser.newContext({
    viewport: { width: 1280, height: 720 }
  });
  
  const page = await context.newPage();
  
  try {
    console.log('\n=== Testing Business Analysis Flow ===\n');
    
    // Navigate to analyze page
    console.log('1. Navigating to Analyze page...');
    await page.goto('http://localhost:3000/analyze');
    await page.waitForTimeout(2000);
    await takeScreenshot(page, '02-analyze-page');
    console.log('✓ Analyze page loaded');
    
    // Check page elements
    const textarea = await page.locator('textarea').first();
    const analyzeButton = await page.locator('button:has-text("Analyze")');
    
    console.log('\n2. Page elements check:');
    console.log('- Textarea visible:', await textarea.isVisible());
    console.log('- Button visible:', await analyzeButton.isVisible());
    
    // Enter business description
    console.log('\n3. Entering business description...');
    await textarea.fill('Real estate investment analysis platform helping investors evaluate ROI, cash flow, and market trends for short-term rental properties in major cities across North America');
    await takeScreenshot(page, '03-business-entered');
    
    // Click analyze
    console.log('\n4. Clicking Analyze button...');
    await analyzeButton.click();
    
    // Wait for results with timeout
    console.log('\n5. Waiting for AI analysis results...');
    try {
      await page.waitForSelector('.template-card', { timeout: 15000 });
      await takeScreenshot(page, '04-analysis-results');
      console.log('✓ Analysis results received');
      
      // Count templates
      const templates = await page.locator('.template-card').count();
      console.log(`\n✓ Found ${templates} template suggestions`);
      
    } catch (error) {
      console.log('\n❌ No template results found - checking for errors');
      await takeScreenshot(page, '04-no-results-or-error');
      
      // Check for error messages
      const errorMessage = await page.locator('.error-message, .alert-destructive').first();
      if (await errorMessage.isVisible()) {
        console.log('Error message:', await errorMessage.textContent());
      }
    }
    
  } catch (error) {
    console.error('\nTest failed:', error.message);
    await takeScreenshot(page, 'error-screenshot');
  } finally {
    await browser.close();
  }
}

// Run the test
testBusinessAnalysis().catch(console.error);