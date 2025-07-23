// Test the frontend UI flow
const puppeteer = require('puppeteer');

async function testFrontendFlow() {
  console.log('🧪 Testing Frontend UI Flow');
  console.log('=' .repeat(50));
  
  const browser = await puppeteer.launch({
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });
  
  try {
    const page = await browser.newPage();
    
    // Test 1: Navigate to project page
    console.log('\n1️⃣ Testing project page...');
    await page.goto('http://localhost:3001/projects/844fe485-b120-4c17-b37c-cc8f017c65cc');
    await page.waitForSelector('h1', { timeout: 10000 });
    
    const projectTitle = await page.$eval('h1', el => el.textContent);
    console.log(`✅ Project page loaded: ${projectTitle}`);
    
    // Test 2: Check for template
    console.log('\n2️⃣ Looking for template...');
    const templateExists = await page.$('code') !== null;
    if (templateExists) {
      const templatePattern = await page.$eval('code', el => el.textContent);
      console.log(`✅ Template found: ${templatePattern}`);
    }
    
    // Test 3: Click Generate Pages button
    console.log('\n3️⃣ Testing Generate Pages navigation...');
    const generateButton = await page.$('a[href*="/generate"]');
    if (generateButton) {
      const href = await generateButton.evaluate(el => el.href);
      console.log(`✅ Generate button found with href: ${href}`);
      
      // Navigate to generate page
      await generateButton.click();
      await page.waitForNavigation({ waitUntil: 'networkidle0' });
      
      const currentUrl = page.url();
      console.log(`✅ Navigated to: ${currentUrl}`);
      
      // Test 4: Check if template is loaded on generate page
      console.log('\n4️⃣ Checking generate page content...');
      await page.waitForSelector('h1', { timeout: 5000 });
      
      // Check for potential pages selector
      const hasPotentialPages = await page.$('.potential-pages-selector') !== null;
      const hasTemplateInfo = await page.$eval('body', body => body.textContent.includes('Test Template Creation'));
      
      if (hasPotentialPages) {
        console.log('✅ Potential pages selector is displayed!');
      } else if (hasTemplateInfo) {
        console.log('✅ Template information is displayed');
      } else {
        console.log('⚠️ Expected UI elements not found');
      }
    } else {
      console.log('❌ Generate Pages button not found');
    }
    
  } catch (error) {
    console.error('❌ Test failed:', error.message);
  } finally {
    await browser.close();
  }
  
  console.log('\n' + '='.repeat(50));
  console.log('✨ UI test completed!');
}

// Run the test
testFrontendFlow().catch(console.error);