// Test the complete frontend flow with templates
const puppeteer = require('puppeteer');

async function testCompleteFlow() {
  console.log('🧪 Testing Complete Page Generation Flow');
  console.log('=' .repeat(50));
  
  const browser = await puppeteer.launch({
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });
  
  try {
    const page = await browser.newPage();
    
    // Enable console and network logging
    page.on('console', msg => {
      if (msg.type() === 'log' && msg.text().includes('Variables generated')) {
        console.log('📝 Console:', msg.text());
      }
    });
    
    page.on('response', response => {
      const url = response.url();
      if (url.includes('/api/') && !url.includes('/health')) {
        const method = response.request().method();
        console.log(`📡 ${method} ${url.substring(url.lastIndexOf('/api/'))} - ${response.status()}`);
      }
    });
    
    // Test 1: Go to templates list page
    console.log('\n1️⃣ Testing templates list page...');
    const templatesUrl = 'http://localhost:3001/projects/844fe485-b120-4c17-b37c-cc8f017c65cc/templates/list';
    await page.goto(templatesUrl, { waitUntil: 'networkidle0' });
    
    // Wait for templates to load
    await page.waitForSelector('.hover\\:shadow-lg', { timeout: 10000 });
    console.log('✅ Templates list loaded');
    
    // Check if template card exists
    const templateExists = await page.$eval('.hover\\:shadow-lg', el => el !== null);
    if (templateExists) {
      console.log('✅ Template card found');
      
      // Find and click the Generate Pages button
      const generateBtn = await page.$('a[href*="/generate?templateId="]');
      if (generateBtn) {
        const href = await generateBtn.evaluate(el => el.href);
        console.log(`✅ Generate button found: ${href}`);
        
        // Click the button
        await generateBtn.click();
        await page.waitForNavigation({ waitUntil: 'networkidle0' });
        
        console.log(`✅ Navigated to: ${page.url()}`);
        
        // Wait for page to load and check content
        await new Promise(resolve => setTimeout(resolve, 3000)); // Give time for React and API calls
        
        // Test 2: Check if variables are being generated
        console.log('\n2️⃣ Checking for variable generation...');
        
        // Check for loading state
        const hasLoader = await page.$('.animate-spin') !== null;
        if (hasLoader) {
          console.log('✅ Loading spinner detected - variables being generated');
          
          // Wait for loading to complete
          await page.waitForSelector('.animate-spin', { hidden: true, timeout: 30000 });
          console.log('✅ Loading completed');
        }
        
        // Test 3: Check for potential pages selector
        console.log('\n3️⃣ Checking for potential pages interface...');
        await new Promise(resolve => setTimeout(resolve, 2000));
        
        // Look for key elements
        const pageContent = await page.content();
        const hasPotentialPages = pageContent.includes('potential pages') || pageContent.includes('Potential Pages');
        const hasSelectButtons = pageContent.includes('Select') || pageContent.includes('Generate Selected');
        const hasPageTitles = pageContent.includes('Short-Term Rental') || pageContent.includes('in Toronto');
        
        console.log(`   Has potential pages text: ${hasPotentialPages}`);
        console.log(`   Has selection UI: ${hasSelectButtons}`);
        console.log(`   Has page titles: ${hasPageTitles}`);
        
        // Check for the actual component elements
        const hasCheckboxes = await page.$$('input[type="checkbox"]');
        console.log(`   Found ${hasCheckboxes.length} checkboxes`);
        
        // Take a screenshot for debugging
        await page.screenshot({ path: 'complete-flow-screenshot.png', fullPage: true });
        console.log('📸 Screenshot saved as complete-flow-screenshot.png');
        
        // Test 4: Try selecting some pages
        if (hasCheckboxes.length > 0) {
          console.log('\n4️⃣ Testing page selection...');
          
          // Click first 3 checkboxes
          for (let i = 0; i < Math.min(3, hasCheckboxes.length); i++) {
            await hasCheckboxes[i].click();
            console.log(`   ✅ Selected page ${i + 1}`);
          }
          
          // Look for generate button
          const generateSelectedBtn = await page.$('button:has-text("Generate Selected")');
          if (generateSelectedBtn) {
            console.log('✅ Generate Selected Pages button found');
          }
        }
        
      } else {
        console.log('❌ Generate Pages button not found in template card');
      }
    } else {
      console.log('❌ No template card found');
    }
    
  } catch (error) {
    console.error('❌ Test error:', error.message);
    
    // Take error screenshot
    const page = (await browser.pages())[0];
    if (page) {
      await page.screenshot({ path: 'error-screenshot.png', fullPage: true });
      console.log('📸 Error screenshot saved');
    }
  } finally {
    await browser.close();
  }
  
  console.log('\n' + '='.repeat(50));
  console.log('✨ Complete flow test finished!');
}

// Run the test
testCompleteFlow().catch(console.error);