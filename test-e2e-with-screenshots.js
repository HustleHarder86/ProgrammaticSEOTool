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

async function runE2ETest() {
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
    console.log('\n=== Starting E2E Test with Screenshots ===\n');
    
    // Step 1: Homepage
    console.log('1. Testing Homepage...');
    await page.goto('http://localhost:3000');
    await page.waitForTimeout(2000);
    await takeScreenshot(page, '01-homepage');
    console.log('✓ Homepage loaded successfully');
    
    // Step 2: Navigate to Analyze Business
    console.log('\n2. Testing Business Analysis...');
    await page.click('text="Analyze Business"');
    await page.waitForTimeout(1000);
    await takeScreenshot(page, '02-analyze-page');
    
    // Step 3: Enter business description
    console.log('\n3. Entering business description...');
    const businessInput = await page.locator('textarea[placeholder*="Describe your business"]');
    await businessInput.fill('Real estate investment analysis platform helping investors evaluate ROI, cash flow, and market trends for short-term rental properties');
    await takeScreenshot(page, '03-business-entered');
    
    // Step 4: Submit analysis
    console.log('\n4. Submitting for AI analysis...');
    await page.click('button:has-text("Analyze with AI")');
    await page.waitForTimeout(5000); // Wait for AI analysis
    await takeScreenshot(page, '04-analysis-results');
    console.log('✓ Business analysis completed');
    
    // Step 5: Select a template
    console.log('\n5. Selecting a template...');
    const firstTemplate = await page.locator('.template-card').first();
    if (await firstTemplate.isVisible()) {
      await firstTemplate.click();
      await page.waitForTimeout(1000);
      await takeScreenshot(page, '05-template-selected');
      console.log('✓ Template selected');
    }
    
    // Step 6: Create project
    console.log('\n6. Creating project...');
    const createButton = await page.locator('button:has-text("Create Project")');
    if (await createButton.isVisible()) {
      await createButton.click();
      await page.waitForTimeout(2000);
      await takeScreenshot(page, '06-project-created');
      console.log('✓ Project created');
    }
    
    // Step 7: Generate variables
    console.log('\n7. Testing variable generation...');
    const generateVariablesButton = await page.locator('button:has-text("Generate Variables")');
    if (await generateVariablesButton.isVisible()) {
      await generateVariablesButton.click();
      await page.waitForTimeout(5000);
      await takeScreenshot(page, '07-variables-generated');
      console.log('✓ Variables generated');
    }
    
    // Step 8: Generate pages
    console.log('\n8. Testing page generation...');
    const generatePagesButton = await page.locator('button:has-text("Generate Pages")');
    if (await generatePagesButton.isVisible()) {
      await generatePagesButton.click();
      await page.waitForTimeout(8000);
      await takeScreenshot(page, '08-pages-generated');
      console.log('✓ Pages generated');
    }
    
    // Step 9: Export
    console.log('\n9. Testing export functionality...');
    const exportButton = await page.locator('button:has-text("Export")');
    if (await exportButton.isVisible()) {
      await exportButton.click();
      await page.waitForTimeout(1000);
      await takeScreenshot(page, '09-export-dialog');
      console.log('✓ Export dialog opened');
    }
    
    console.log('\n=== E2E Test Completed Successfully ===\n');
    
  } catch (error) {
    console.error('\nTest failed:', error.message);
    await takeScreenshot(page, 'error-screenshot');
    throw error;
  } finally {
    await browser.close();
  }
}

// Run the test
runE2ETest().catch(console.error);