#!/usr/bin/env node

const http = require('http');
const https = require('https');
const fs = require('fs');
const path = require('path');

console.log('🧪 Running End-to-End Test of Programmatic SEO Tool\n');

let testResults = [];
let projectId = null;
let templateId = null;

// Helper function to make HTTP requests
function makeRequest(options, postData = null) {
  return new Promise((resolve, reject) => {
    const protocol = options.protocol === 'https:' ? https : http;
    const req = protocol.request(options, (res) => {
      let data = '';
      res.on('data', (chunk) => { data += chunk; });
      res.on('end', () => {
        resolve({
          status: res.statusCode,
          headers: res.headers,
          data: data
        });
      });
    });

    req.on('error', reject);
    
    if (postData) {
      req.write(postData);
    }
    req.end();
  });
}

// Test functions
async function test1_CheckHealth() {
  console.log('1️⃣ Testing API Health...');
  
  try {
    const response = await makeRequest({
      hostname: 'localhost',
      port: 8000,
      path: '/health',
      method: 'GET'
    });
    
    const success = response.status === 200;
    testResults.push({ test: 'API Health', success, details: response.data });
    console.log(success ? '✅ API is healthy' : '❌ API health check failed');
    return success;
  } catch (error) {
    testResults.push({ test: 'API Health', success: false, error: error.message });
    console.log('❌ API is not running');
    return false;
  }
}

async function test2_BusinessAnalysis() {
  console.log('\n2️⃣ Testing Business Analysis...');
  
  const businessData = {
    business_input: "AI Writing Assistant for Content Creators - helps create blog posts, emails, and social media content",
    input_type: "text"
  };
  
  try {
    const response = await makeRequest({
      hostname: 'localhost',
      port: 8000,
      path: '/api/analyze-business',
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      }
    }, JSON.stringify(businessData));
    
    const success = response.status === 200;
    const data = JSON.parse(response.data);
    
    if (success && data.project_id) {
      projectId = data.project_id;
      console.log(`✅ Business analyzed - Project ID: ${projectId}`);
      console.log(`   Business: ${data.business_name}`);
      console.log(`   Templates found: ${data.template_opportunities.length}`);
    } else {
      console.log('❌ Business analysis failed');
    }
    
    testResults.push({ test: 'Business Analysis', success, projectId });
    return success;
  } catch (error) {
    testResults.push({ test: 'Business Analysis', success: false, error: error.message });
    console.log('❌ Business analysis error:', error.message);
    return false;
  }
}

async function test3_CreateTemplate() {
  console.log('\n3️⃣ Testing Template Creation...');
  
  if (!projectId) {
    console.log('⚠️  Skipping - no project ID');
    return false;
  }
  
  const templateData = {
    name: "AI Content Tools Comparison",
    pattern: "Best AI Tools for {ContentType} in {Year}",
    title_template: "Best AI Tools for {ContentType} in {Year} - Expert Review",
    meta_description_template: "Compare top AI tools for {ContentType}. Updated for {Year}.",
    h1_template: "Best AI Tools for {ContentType} in {Year}",
    content_sections: [
      {
        type: "intro",
        content: "Discover the best AI tools for creating {ContentType} in {Year}."
      }
    ]
  };
  
  try {
    const response = await makeRequest({
      hostname: 'localhost',
      port: 8000,
      path: `/api/projects/${projectId}/templates`,
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      }
    }, JSON.stringify(templateData));
    
    const success = response.status === 200;
    const data = JSON.parse(response.data);
    
    if (success && data.id) {
      templateId = data.id;
      console.log(`✅ Template created - ID: ${templateId}`);
      console.log(`   Variables: ${data.variables.join(', ')}`);
    } else {
      console.log('❌ Template creation failed');
    }
    
    testResults.push({ test: 'Template Creation', success, templateId });
    return success;
  } catch (error) {
    testResults.push({ test: 'Template Creation', success: false, error: error.message });
    console.log('❌ Template creation error:', error.message);
    return false;
  }
}

async function test4_GenerateVariables() {
  console.log('\n4️⃣ Testing AI Variable Generation...');
  
  if (!projectId || !templateId) {
    console.log('⚠️  Skipping - missing project or template');
    return false;
  }
  
  const requestData = {
    count: 10,
    business_context: {
      name: "AI Content Creator",
      description: "AI writing tools for content creation",
      target_audience: "Content creators and marketers",
      industry: "SaaS"
    }
  };
  
  try {
    const response = await makeRequest({
      hostname: 'localhost',
      port: 8000,
      path: `/api/projects/${projectId}/templates/${templateId}/generate-variables`,
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      }
    }, JSON.stringify(requestData));
    
    const success = response.status === 200;
    const data = JSON.parse(response.data);
    
    if (success && data.variables) {
      console.log('✅ Variables generated successfully');
      console.log(`   Total combinations: ${data.total_count}`);
      Object.entries(data.variables).forEach(([key, values]) => {
        console.log(`   ${key}: ${values.length} values`);
      });
    } else {
      console.log('❌ Variable generation failed');
    }
    
    testResults.push({ test: 'Variable Generation', success, totalCombinations: data.total_count });
    return { success, data };
  } catch (error) {
    testResults.push({ test: 'Variable Generation', success: false, error: error.message });
    console.log('❌ Variable generation error:', error.message);
    return { success: false };
  }
}

async function test5_GeneratePages(variableData) {
  console.log('\n5️⃣ Testing Page Generation...');
  
  if (!projectId || !templateId || !variableData) {
    console.log('⚠️  Skipping - missing requirements');
    return false;
  }
  
  // Select first 3 titles
  const selectedTitles = variableData.titles.slice(0, 3);
  const variablesData = {};
  
  // Extract variables for selected titles
  Object.entries(variableData.variables).forEach(([key, values]) => {
    variablesData[key] = values.slice(0, 3);
  });
  
  const requestData = {
    batch_size: 3,
    selected_titles: selectedTitles,
    variables_data: variablesData
  };
  
  try {
    const response = await makeRequest({
      hostname: 'localhost',
      port: 8000,
      path: `/api/projects/${projectId}/templates/${templateId}/generate`,
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      }
    }, JSON.stringify(requestData));
    
    const success = response.status === 200;
    const data = JSON.parse(response.data);
    
    if (success && data.total_generated > 0) {
      console.log(`✅ Pages generated successfully`);
      console.log(`   Generated: ${data.total_generated} pages`);
      console.log(`   Page IDs: ${data.page_ids.slice(0, 3).join(', ')}...`);
    } else {
      console.log('❌ Page generation failed');
    }
    
    testResults.push({ test: 'Page Generation', success, pagesGenerated: data.total_generated });
    return success;
  } catch (error) {
    testResults.push({ test: 'Page Generation', success: false, error: error.message });
    console.log('❌ Page generation error:', error.message);
    return false;
  }
}

async function test6_Export() {
  console.log('\n6️⃣ Testing Export Functionality...');
  
  if (!projectId) {
    console.log('⚠️  Skipping - no project ID');
    return false;
  }
  
  const exportData = {
    format: "csv",
    include_metadata: true
  };
  
  try {
    const response = await makeRequest({
      hostname: 'localhost',
      port: 8000,
      path: `/api/projects/${projectId}/export`,
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      }
    }, JSON.stringify(exportData));
    
    const success = response.status === 200;
    const data = JSON.parse(response.data);
    
    if (success && data.export_id) {
      console.log(`✅ Export initiated successfully`);
      console.log(`   Export ID: ${data.export_id}`);
      console.log(`   Status: ${data.status}`);
    } else {
      console.log('❌ Export failed');
    }
    
    testResults.push({ test: 'Export', success, exportId: data.export_id });
    return success;
  } catch (error) {
    testResults.push({ test: 'Export', success: false, error: error.message });
    console.log('❌ Export error:', error.message);
    return false;
  }
}

// Run all tests
async function runAllTests() {
  console.log('Starting end-to-end tests...\n');
  console.log('Frontend URL: http://localhost:3000');
  console.log('Backend URL: http://localhost:8000\n');
  
  // Run tests in sequence
  const healthOk = await test1_CheckHealth();
  if (!healthOk) {
    console.log('\n⚠️  Backend is not running. Please start it with:');
    console.log('cd backend && python3 -m uvicorn main:app --host 127.0.0.1 --port 8000');
    return;
  }
  
  const analysisOk = await test2_BusinessAnalysis();
  if (analysisOk) {
    await test3_CreateTemplate();
    const variableResult = await test4_GenerateVariables();
    if (variableResult.success) {
      await test5_GeneratePages(variableResult.data);
      await test6_Export();
    }
  }
  
  // Generate summary
  console.log('\n' + '='.repeat(60));
  console.log('📊 TEST SUMMARY');
  console.log('='.repeat(60) + '\n');
  
  const passed = testResults.filter(r => r.success).length;
  const failed = testResults.filter(r => !r.success).length;
  
  console.log(`Total Tests: ${testResults.length}`);
  console.log(`✅ Passed: ${passed}`);
  console.log(`❌ Failed: ${failed}`);
  console.log(`Success Rate: ${Math.round((passed / testResults.length) * 100)}%`);
  
  console.log('\nDetailed Results:');
  testResults.forEach(result => {
    const icon = result.success ? '✅' : '❌';
    console.log(`${icon} ${result.test}`);
    if (result.error) {
      console.log(`   Error: ${result.error}`);
    }
  });
  
  // Save results
  const report = {
    timestamp: new Date().toISOString(),
    summary: {
      total: testResults.length,
      passed,
      failed,
      successRate: Math.round((passed / testResults.length) * 100)
    },
    results: testResults,
    projectId,
    templateId
  };
  
  fs.writeFileSync('e2e-test-report.json', JSON.stringify(report, null, 2));
  console.log('\n📁 Full report saved to: e2e-test-report.json');
  
  if (passed === testResults.length) {
    console.log('\n🎉 All tests passed! Your Programmatic SEO Tool is working perfectly!');
  } else {
    console.log('\n⚠️  Some tests failed. Check the details above.');
  }
}

// Run the tests
runAllTests().catch(console.error);