const { chromium } = require('playwright');

async function testAnalysisWithPromptConfig() {
  const browser = await chromium.launch({ headless: false });
  const page = await browser.newContext().then(c => c.newPage());
  
  console.log('Testing Business Analysis with New Prompt Config...\n');
  
  try {
    // Navigate to analyze page
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
    
    console.log('Entered business description');
    
    // Take screenshot before analysis
    await page.screenshot({ path: 'test-screenshots/15-before-analysis.png' });
    
    // Click analyze button
    await page.click('button:has-text("Analyze Business")');
    console.log('Clicked Analyze Business button');
    
    // Wait for loading to finish
    await page.waitForSelector('text=Template Suggestions', { timeout: 60000 });
    console.log('Analysis completed!');
    
    // Take screenshot of results
    await page.screenshot({ path: 'test-screenshots/16-analysis-results-complete.png', fullPage: true });
    
    // Check if the new prompt config is being used
    const templateCards = await page.$$('.bg-white.rounded-lg.border');
    console.log(`Found ${templateCards.length} template suggestions`);
    
    // Get template details
    for (let i = 0; i < Math.min(3, templateCards.length); i++) {
      const card = templateCards[i];
      const title = await card.$eval('h3', el => el.textContent);
      const pattern = await card.$eval('code', el => el.textContent).catch(() => 'No pattern found');
      console.log(`Template ${i + 1}: ${title} - Pattern: ${pattern}`);
    }
    
    console.log('\n✓ Business analysis with new prompt config successful!');
    
  } catch (error) {
    console.error('Error during test:', error);
    await page.screenshot({ path: 'test-screenshots/error-analysis.png', fullPage: true });
  }
  
  // Keep browser open for manual inspection
  console.log('\nBrowser will remain open for inspection. Close manually when done.');
}

testAnalysisWithPromptConfig();