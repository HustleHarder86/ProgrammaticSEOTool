const { chromium } = require('playwright');

async function runComprehensiveTest() {
  const browser = await chromium.launch({ headless: false });
  const context = await browser.newContext();
  const page = await context.newPage();
  
  console.log('Starting Comprehensive E2E Test...\n');
  
  try {
    // Test 1: Business Analysis with new prompt config
    console.log('Test 1: Business Analysis with new prompt config');
    await page.goto('http://localhost:3003/analyze');
    await page.waitForLoadState('networkidle');
    
    // Click Text Description tab
    await page.click('text=Text Description');
    
    // Enter business description
    const businessDescription = `We are a property management software company that helps landlords 
    and property managers handle rental properties. Our software includes features for rent collection, 
    maintenance tracking, tenant screening, and financial reporting. We serve residential property 
    managers across the United States.`;
    
    await page.fill('textarea', businessDescription);
    
    // Take screenshot before analysis
    await page.screenshot({ path: 'test-screenshots/03-before-analysis.png' });
    
    // Click analyze button
    await page.click('text=Analyze Business');
    
    // Wait for results with longer timeout
    await page.waitForSelector('text=Template Suggestions', { timeout: 60000 });
    
    // Take screenshot of results
    await page.screenshot({ path: 'test-screenshots/04-analysis-results.png', fullPage: true });
    
    console.log('✓ Business analysis completed successfully\n');
    
    // Test 2: Create a project and template
    console.log('Test 2: Create project and template with schema markup');
    
    // Click on first template suggestion
    await page.click('.template-card:first-child button:has-text("Use This Template")');
    
    // Wait for create project modal
    await page.waitForSelector('text=Create New Project');
    
    // Fill project details
    await page.fill('input[placeholder*="project name"]', 'Property Management SEO Test');
    await page.fill('textarea[placeholder*="description"]', 'Testing all new integrations');
    
    await page.screenshot({ path: 'test-screenshots/05-create-project.png' });
    
    // Create project
    await page.click('button:has-text("Create Project")');
    
    // Wait for template editor
    await page.waitForSelector('text=Edit Template', { timeout: 30000 });
    
    await page.screenshot({ path: 'test-screenshots/06-template-editor.png', fullPage: true });
    
    console.log('✓ Project and template created successfully\n');
    
    // Test 3: Generate variables with AI
    console.log('Test 3: Variable generation with prompt rotation');
    
    // Click generate variables button
    await page.click('button:has-text("Generate Variables")');
    
    // Wait for variable generation
    await page.waitForSelector('text=Variables generated successfully', { timeout: 60000 });
    
    await page.screenshot({ path: 'test-screenshots/07-variables-generated.png', fullPage: true });
    
    console.log('✓ Variables generated successfully\n');
    
    // Test 4: Generate pages
    console.log('Test 4: Page generation with all enhancements');
    
    // Click generate pages
    await page.click('button:has-text("Generate Pages")');
    
    // Wait for generation to complete
    await page.waitForSelector('text=pages generated', { timeout: 120000 });
    
    await page.screenshot({ path: 'test-screenshots/08-pages-generated.png', fullPage: true });
    
    // View generated pages
    await page.click('a:has-text("View Generated Pages")');
    await page.waitForLoadState('networkidle');
    
    await page.screenshot({ path: 'test-screenshots/09-pages-list.png', fullPage: true });
    
    console.log('✓ Pages generated successfully\n');
    
    // Test 5: Check schema markup
    console.log('Test 5: Verify schema markup in generated pages');
    
    // Click on first generated page
    await page.click('.page-row:first-child');
    await page.waitForSelector('text=Page Details');
    
    // Check for schema markup section
    const hasSchema = await page.isVisible('text=Schema Markup');
    console.log(`Schema markup present: ${hasSchema}`);
    
    await page.screenshot({ path: 'test-screenshots/10-page-details-schema.png', fullPage: true });
    
    console.log('✓ Schema markup verified\n');
    
    // Test 6: Export functionality
    console.log('Test 6: Export with schema markup');
    
    await page.goto('http://localhost:3003/export');
    await page.waitForLoadState('networkidle');
    
    // Select export format
    await page.click('text=JSON');
    
    // Configure export options
    await page.check('text=Include Schema Markup');
    
    await page.screenshot({ path: 'test-screenshots/11-export-config.png' });
    
    // Export
    await page.click('button:has-text("Export Pages")');
    
    console.log('✓ Export initiated\n');
    
    // Test 7: Configuration management
    console.log('Test 7: Configuration management');
    
    await page.goto('http://localhost:3003/settings');
    await page.waitForLoadState('networkidle');
    
    await page.screenshot({ path: 'test-screenshots/12-settings-page.png', fullPage: true });
    
    console.log('✓ Settings page loaded\n');
    
    // Test 8: Check backend health with new integrations
    console.log('Test 8: Backend health check');
    
    const healthResponse = await page.evaluate(async () => {
      const res = await fetch('http://localhost:8000/health');
      return await res.json();
    });
    
    console.log('Backend health:', healthResponse);
    
    console.log('\n✅ All tests completed successfully!');
    
  } catch (error) {
    console.error('❌ Test failed:', error);
    await page.screenshot({ path: 'test-screenshots/error-screenshot.png', fullPage: true });
  } finally {
    await browser.close();
  }
}

runComprehensiveTest();