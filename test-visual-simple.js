#!/usr/bin/env node

const http = require('http');
const fs = require('fs');
const path = require('path');

// Simple visual test without Playwright
console.log('🧪 Running Simple Visual Test of Programmatic SEO Tool\n');

const tests = [
  { name: 'API Health Check', url: 'http://localhost:8000/health', method: 'GET' },
  { name: 'Frontend Check', url: 'http://localhost:3000', method: 'GET' },
  { 
    name: 'Business Analysis', 
    url: 'http://localhost:8000/api/analyze-business',
    method: 'POST',
    data: {
      business_input: "Test Digital Marketing Agency",
      input_type: "text"
    }
  }
];

async function runTest(test) {
  return new Promise((resolve, reject) => {
    const url = new URL(test.url);
    const options = {
      hostname: url.hostname,
      port: url.port,
      path: url.pathname,
      method: test.method,
      headers: {
        'Content-Type': 'application/json'
      }
    };

    const req = http.request(options, (res) => {
      let data = '';
      res.on('data', (chunk) => { data += chunk; });
      res.on('end', () => {
        resolve({
          test: test.name,
          status: res.statusCode,
          success: res.statusCode >= 200 && res.statusCode < 300,
          response: data.substring(0, 200) + (data.length > 200 ? '...' : '')
        });
      });
    });

    req.on('error', (error) => {
      resolve({
        test: test.name,
        status: 0,
        success: false,
        error: error.message
      });
    });

    if (test.data) {
      req.write(JSON.stringify(test.data));
    }
    req.end();
  });
}

async function runAllTests() {
  const results = [];
  
  for (const test of tests) {
    console.log(`Running: ${test.name}...`);
    const result = await runTest(test);
    results.push(result);
    
    if (result.success) {
      console.log(`✅ ${test.name} - Status: ${result.status}`);
    } else {
      console.log(`❌ ${test.name} - Failed: ${result.error || `Status ${result.status}`}`);
    }
  }
  
  // Generate report
  generateReport(results);
}

function generateReport(results) {
  console.log('\n📊 Test Summary Report\n');
  
  const passed = results.filter(r => r.success).length;
  const failed = results.filter(r => !r.success).length;
  
  console.log(`Total Tests: ${results.length}`);
  console.log(`✅ Passed: ${passed}`);
  console.log(`❌ Failed: ${failed}`);
  console.log(`Success Rate: ${Math.round((passed / results.length) * 100)}%`);
  
  // Save detailed report
  const report = {
    timestamp: new Date().toISOString(),
    summary: {
      total: results.length,
      passed,
      failed,
      successRate: Math.round((passed / results.length) * 100)
    },
    results,
    recommendations: generateRecommendations(results)
  };
  
  fs.writeFileSync('test-report.json', JSON.stringify(report, null, 2));
  console.log('\n📁 Detailed report saved to: test-report.json');
}

function generateRecommendations(results) {
  const recommendations = [];
  
  results.forEach(result => {
    if (!result.success) {
      if (result.test === 'API Health Check') {
        recommendations.push('Backend API is not running. Run: cd backend && python3 -m uvicorn main:app');
      }
      if (result.test === 'Frontend Check') {
        recommendations.push('Frontend is not running. Run: npm run dev');
      }
      if (result.test === 'Business Analysis') {
        recommendations.push('Business analysis endpoint failed. Check API keys in .env file');
      }
    }
  });
  
  return recommendations;
}

// Manual visual feedback collection
console.log('\n📸 Visual Feedback Instructions:\n');
console.log('1. Open http://localhost:3000 in your browser');
console.log('2. Take screenshots of key pages:');
console.log('   - Homepage');
console.log('   - Business Analysis (/analyze)');
console.log('   - Template Builder');
console.log('   - Page Generation');
console.log('3. Save screenshots to tests/screenshots/');
console.log('\nPress Ctrl+C when done to see the test report.\n');

// Run tests
runAllTests();