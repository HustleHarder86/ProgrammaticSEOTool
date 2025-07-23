// Detailed test of the frontend UI flow
const puppeteer = require('puppeteer');

async function testDetailedFlow() {
  console.log('🧪 Testing Detailed Frontend Flow');
  console.log('=' .repeat(50));
  
  const browser = await puppeteer.launch({
    headless: false, // Show browser for debugging
    args: ['--no-sandbox', '--disable-setuid-sandbox'],
    devtools: true
  });
  
  try {
    const page = await browser.newPage();
    
    // Enable console logging
    page.on('console', msg => {
      if (msg.type() === 'error') {
        console.log('❌ Console error:', msg.text());
      }
    });
    
    // Monitor network requests
    page.on('response', response => {
      const url = response.url();
      if (url.includes('/api/')) {
        console.log(`📡 API call: ${url.substring(url.lastIndexOf('/api/'))} - ${response.status()}`);
      }
    });
    
    // Step 1: Go to templates list page
    console.log('\n1️⃣ Navigating to templates list...');
    await page.goto('http://localhost:3001/projects/844fe485-b120-4c17-b37c-cc8f017c65cc/templates/list');
    await page.waitForSelector('h1', { timeout: 10000 });
    
    // Check if template card exists
    const templateCard = await page.$('.hover\\:shadow-lg');
    if (templateCard) {
      console.log('✅ Template card found');
      
      // Find the Generate Pages button within the card
      const generateBtn = await templateCard.$('a[href*="/generate?templateId="]');
      if (generateBtn) {
        const href = await generateBtn.evaluate(el => el.href);
        console.log(`✅ Generate button href: ${href}`);
        
        // Click it
        await generateBtn.click();
        console.log('✅ Clicked Generate Pages button');
        
        // Wait for navigation
        await page.waitForNavigation({ waitUntil: 'networkidle0' });
        console.log(`✅ Navigated to: ${page.url()}`);
        
        // Wait a bit for React to render
        await page.waitForTimeout(2000);
        
        // Check page content
        console.log('\n2️⃣ Checking generate page content...');
        const pageContent = await page.content();
        
        // Look for key elements
        const hasNoTemplates = pageContent.includes('No Templates Found');
        const hasPotentialPages = pageContent.includes('potential-pages');
        const hasGenerateVariables = pageContent.includes('generate-variables');
        const hasTemplateSelector = await page.$('select') !== null;
        
        console.log(`   Has "No Templates Found": ${hasNoTemplates}`);
        console.log(`   Has potential pages content: ${hasPotentialPages}`);
        console.log(`   Has generate variables: ${hasGenerateVariables}`);
        console.log(`   Has template selector: ${hasTemplateSelector}`);
        
        // Take a screenshot
        await page.screenshot({ path: 'generate-page-screenshot.png', fullPage: true });
        console.log('📸 Screenshot saved as generate-page-screenshot.png');
        
        // Check if template was pre-selected
        const urlParams = new URL(page.url()).searchParams;
        const templateId = urlParams.get('templateId');
        console.log(`   Template ID from URL: ${templateId}`);
        
        // Wait a bit more to see if variables are generated
        console.log('\n3️⃣ Waiting for potential API calls...');
        await page.waitForTimeout(3000);
        
      } else {
        console.log('❌ Generate Pages button not found in template card');
      }
    } else {
      console.log('❌ No template card found');
    }
    
    // Keep browser open for manual inspection
    console.log('\n⏸️  Browser will stay open for 30 seconds for manual inspection...');
    await page.waitForTimeout(30000);
    
  } catch (error) {
    console.error('❌ Test error:', error.message);
  } finally {
    await browser.close();
  }
  
  console.log('\n' + '='.repeat(50));
  console.log('✨ Detailed test completed!');
}

// Run the test
testDetailedFlow().catch(console.error);