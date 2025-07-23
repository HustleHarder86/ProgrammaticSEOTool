const { chromium } = require('playwright');

async function testSimpleFlow() {
  const browser = await chromium.launch({ headless: false });
  const page = await browser.newContext().then(c => c.newPage());
  
  console.log('Testing Simple Flow with New Integrations...\n');
  
  try {
    // Test 1: Business Analysis
    console.log('Test 1: Business Analysis from Create Project Flow');
    await page.goto('http://localhost:3003/projects/new');
    await page.waitForLoadState('networkidle');
    
    // Enter business description
    const businessDescription = `We are a property management software company that helps landlords 
    and property managers handle rental properties. Our software includes features for rent collection, 
    maintenance tracking, tenant screening, and financial reporting.`;
    
    await page.fill('textarea', businessDescription);
    
    await page.screenshot({ path: 'test-screenshots/30-business-input.png' });
    
    // Click analyze
    await page.click('button:has-text("Analyze Business")');
    
    // Wait for results
    console.log('Waiting for analysis results...');
    await page.waitForSelector('text=Template Suggestions', { timeout: 60000 });
    
    await page.screenshot({ path: 'test-screenshots/31-template-suggestions.png', fullPage: true });
    
    console.log('✓ Business analysis completed');
    
    // Test 2: Select a template
    console.log('\nTest 2: Selecting a template');
    
    // Click on first template
    await page.click('.bg-white.rounded-lg.border >> nth=0');
    await delay(1000);
    
    await page.screenshot({ path: 'test-screenshots/32-template-selected.png' });
    
    // Click continue/next
    const nextButton = await page.$('button:has-text("Next")') || await page.$('button:has-text("Continue")');
    if (nextButton) {
      await nextButton.click();
      console.log('✓ Template selected');
    }
    
    // Test 3: Import Data step
    console.log('\nTest 3: Data import step');
    await page.waitForSelector('text=Import Data');
    
    await page.screenshot({ path: 'test-screenshots/33-import-data-step.png' });
    
    // Generate variables with AI instead
    const generateButton = await page.$('button:has-text("Generate with AI")');
    if (generateButton) {
      await generateButton.click();
      console.log('Generating variables with AI...');
      
      await page.waitForSelector('text=Variables generated', { timeout: 60000 });
      console.log('✓ Variables generated with AI');
    }
    
    // Test 4: Check generated pages
    console.log('\nTest 4: Checking for generated pages');
    await page.goto('http://localhost:3003/projects');
    await page.waitForLoadState('networkidle');
    
    // Click on the project
    await page.click('.bg-white.rounded-lg.border >> nth=0');
    
    await page.waitForSelector('text=Templates');
    await page.screenshot({ path: 'test-screenshots/34-project-details.png', fullPage: true });
    
    console.log('✓ Project created successfully');
    
    // Test 5: Check settings page
    console.log('\nTest 5: Configuration Management');
    await page.goto('http://localhost:3003/settings');
    await page.waitForLoadState('networkidle');
    
    await page.screenshot({ path: 'test-screenshots/35-settings-config.png', fullPage: true });
    
    console.log('✓ Settings page accessible');
    
    console.log('\n✅ Basic flow test completed!');
    
  } catch (error) {
    console.error('\n❌ Test failed:', error.message);
    await page.screenshot({ path: 'test-screenshots/error-simple-flow.png', fullPage: true });
  }
  
  console.log('\nBrowser will remain open. Close manually when done.');
}

function delay(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

testSimpleFlow();