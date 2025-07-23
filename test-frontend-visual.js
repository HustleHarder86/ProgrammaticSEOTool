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

async function testFrontendVisual() {
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
    console.log('\n=== Testing Frontend Visual Flow ===\n');
    
    // Navigate to projects page
    console.log('1. Navigating to Projects page...');
    await page.goto('http://localhost:3000/projects');
    await page.waitForTimeout(2000);
    await takeScreenshot(page, 'frontend-01-projects');
    
    // Click on a project if exists
    const projectCard = await page.locator('.project-card, [href*="/projects/"]').first();
    if (await projectCard.isVisible()) {
      console.log('2. Clicking on first project...');
      await projectCard.click();
      await page.waitForTimeout(2000);
      await takeScreenshot(page, 'frontend-02-project-details');
    }
    
    // Navigate to templates page
    console.log('3. Navigating to Templates...');
    await page.goto('http://localhost:3000/templates');
    await page.waitForTimeout(2000);
    await takeScreenshot(page, 'frontend-03-templates');
    
    // Navigate to data page
    console.log('4. Navigating to Data...');
    await page.goto('http://localhost:3000/data');
    await page.waitForTimeout(2000);
    await takeScreenshot(page, 'frontend-04-data');
    
    // Navigate to export page
    console.log('5. Navigating to Export...');
    await page.goto('http://localhost:3000/export');
    await page.waitForTimeout(2000);
    await takeScreenshot(page, 'frontend-05-export');
    
    console.log('\n✓ Frontend visual test completed\n');
    
  } catch (error) {
    console.error('\nTest failed:', error.message);
    await takeScreenshot(page, 'frontend-error');
  } finally {
    await browser.close();
  }
}

// Run the test
testFrontendVisual().catch(console.error);