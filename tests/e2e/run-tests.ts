import { exec } from 'child_process';
import * as fs from 'fs';
import * as path from 'path';

const SCREENSHOT_DIR = 'tests/e2e/screenshots';

async function runTests() {
  console.log('🚀 Starting Programmatic SEO Tool End-to-End Tests\n');
  
  // Ensure screenshot directory exists
  if (!fs.existsSync(SCREENSHOT_DIR)) {
    fs.mkdirSync(SCREENSHOT_DIR, { recursive: true });
  }
  
  // Clean previous screenshots
  const files = fs.readdirSync(SCREENSHOT_DIR);
  files.forEach(file => {
    if (file.endsWith('.png') || file.endsWith('.json')) {
      fs.unlinkSync(path.join(SCREENSHOT_DIR, file));
    }
  });
  
  console.log('📸 Running visual tests and capturing screenshots...\n');
  
  // Run Playwright tests
  exec('npx playwright test', (error, stdout, stderr) => {
    if (error) {
      console.error(`❌ Test execution failed: ${error}`);
      console.error(stderr);
      return;
    }
    
    console.log(stdout);
    
    // Generate screenshot gallery
    generateScreenshotGallery();
    
    // Analyze results
    analyzeTestResults();
  });
}

function generateScreenshotGallery() {
  console.log('\n📷 Generating screenshot gallery...\n');
  
  const screenshots = fs.readdirSync(SCREENSHOT_DIR)
    .filter(file => file.endsWith('.png'))
    .sort();
  
  const html = `
<!DOCTYPE html>
<html>
<head>
  <title>Programmatic SEO Tool - Test Screenshots</title>
  <style>
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      margin: 0;
      padding: 20px;
      background: #f5f5f5;
    }
    .container {
      max-width: 1200px;
      margin: 0 auto;
    }
    h1 {
      color: #333;
      text-align: center;
      margin-bottom: 40px;
    }
    .screenshot-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
      gap: 20px;
    }
    .screenshot-card {
      background: white;
      border-radius: 8px;
      overflow: hidden;
      box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    .screenshot-card img {
      width: 100%;
      height: auto;
      display: block;
    }
    .screenshot-card h3 {
      margin: 0;
      padding: 15px;
      background: #f8f9fa;
      font-size: 16px;
      color: #495057;
    }
    .timestamp {
      text-align: center;
      color: #666;
      margin-top: 20px;
    }
  </style>
</head>
<body>
  <div class="container">
    <h1>Programmatic SEO Tool - Visual Test Results</h1>
    <div class="screenshot-grid">
      ${screenshots.map(screenshot => `
        <div class="screenshot-card">
          <h3>${screenshot.replace('.png', '').replace(/-/g, ' ')}</h3>
          <img src="${screenshot}" alt="${screenshot}">
        </div>
      `).join('')}
    </div>
    <p class="timestamp">Generated on ${new Date().toLocaleString()}</p>
  </div>
</body>
</html>
  `;
  
  fs.writeFileSync(path.join(SCREENSHOT_DIR, 'gallery.html'), html);
  console.log(`✅ Screenshot gallery created at: ${SCREENSHOT_DIR}/gallery.html`);
}

function analyzeTestResults() {
  console.log('\n📊 Analyzing test results...\n');
  
  // Check for validation reports
  const validationDir = path.join(SCREENSHOT_DIR, 'validation');
  if (fs.existsSync(validationDir)) {
    const summaryPath = path.join(validationDir, 'visual-feedback-summary.json');
    if (fs.existsSync(summaryPath)) {
      const summary = JSON.parse(fs.readFileSync(summaryPath, 'utf-8'));
      
      console.log('=== Test Summary ===');
      console.log(`Overall Score: ${summary.summary.overallScore}/100`);
      console.log(`\nAccessibility:`);
      console.log(`  - Issues found: ${summary.accessibility.issues}`);
      console.log(`\nPerformance:`);
      console.log(`  - Average load time: ${Math.round(summary.performance.averageLoadTime)}ms`);
      console.log(`\nUI Consistency:`);
      console.log(`  - Recommendations: ${summary.uiConsistency.recommendations.length}`);
      
      if (summary.improvements.length > 0) {
        console.log(`\n🔧 Suggested Improvements:`);
        summary.improvements.forEach((imp: string, i: number) => {
          console.log(`  ${i + 1}. ${imp}`);
        });
      }
    }
  }
  
  console.log('\n✅ Test analysis complete!');
  console.log(`\n📁 View full results at: ${path.resolve(SCREENSHOT_DIR)}`);
}

// Run the tests
runTests();