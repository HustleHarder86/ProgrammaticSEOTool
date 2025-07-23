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

async function testTemplateSelection() {
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
    console.log('\n=== Testing Template Selection & Project Creation ===\n');
    
    // Start from analyze page with results
    console.log('1. Running business analysis first...');
    await page.goto('http://localhost:3000/analyze');
    await page.waitForTimeout(2000);
    
    // Enter business description
    const textarea = await page.locator('textarea').first();
    await textarea.fill('Real estate investment analysis platform');
    
    // Click analyze
    await page.click('button:has-text("Analyze Business")');
    console.log('Waiting for analysis results...');
    await page.waitForSelector('.template-card', { timeout: 15000 });
    
    // Select first template
    console.log('\n2. Selecting first template...');
    const firstTemplateButton = await page.locator('button:has-text("Select Template")').first();
    await firstTemplateButton.click();
    await page.waitForTimeout(2000);
    await takeScreenshot(page, '05-template-selected');
    
    // Check if we're on the create project page or if a project was created
    const url = page.url();
    console.log('Current URL:', url);
    
    // Look for project creation elements
    const projectNameInput = await page.locator('input[name="projectName"], input[placeholder*="project"]').first();
    if (await projectNameInput.isVisible()) {
      console.log('\n3. Creating project...');
      await projectNameInput.fill('Real Estate ROI Analysis');
      await takeScreenshot(page, '06-project-name-entered');
      
      const createButton = await page.locator('button:has-text("Create"), button:has-text("Save")');
      if (await createButton.isVisible()) {
        await createButton.click();
        await page.waitForTimeout(3000);
      }
    }
    
    // Check if we're now on a project page
    await takeScreenshot(page, '07-after-project-creation');
    const newUrl = page.url();
    console.log('New URL:', newUrl);
    
    // Look for generate variables button
    console.log('\n4. Looking for variable generation...');
    const generateButton = await page.locator('button:has-text("Generate Variables"), button:has-text("Generate Data")');
    if (await generateButton.isVisible()) {
      console.log('✓ Found variable generation button');
      await generateButton.click();
      await page.waitForTimeout(5000);
      await takeScreenshot(page, '08-variables-generated');
    } else {
      console.log('❌ Variable generation button not found');
    }
    
  } catch (error) {
    console.error('\nTest failed:', error.message);
    await takeScreenshot(page, 'error-template-selection');
  } finally {
    await browser.close();
  }
}

// Run the test
testTemplateSelection().catch(console.error);