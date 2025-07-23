#!/usr/bin/env node

const http = require('http');
const fs = require('fs');

console.log('🧪 COMPREHENSIVE END-TO-END TEST - Programmatic SEO Tool\n');
console.log('📅 Date:', new Date().toISOString());
console.log('⚡ Limiting to 3 pages to minimize API costs\n');
console.log('='*60 + '\n');

let testResults = {
  summary: { total: 0, passed: 0, failed: 0 },
  tests: [],
  costTracking: { before: null, after: null, costIncurred: 0 },
  artifacts: { projectId: null, templateId: null, exportId: null }
};

// Helper function to make HTTP requests
async function makeRequest(options, postData = null) {
  return new Promise((resolve, reject) => {
    const req = http.request(options, (res) => {
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

function logTest(name, success, details = {}) {
  testResults.summary.total++;
  if (success) {
    testResults.summary.passed++;
    console.log(`✅ ${name}`);
  } else {
    testResults.summary.failed++;
    console.log(`❌ ${name}`);
  }
  testResults.tests.push({ name, success, details, timestamp: new Date().toISOString() });
  if (details.message) {
    console.log(`   ${details.message}`);
  }
}

async function runTests() {
  try {
    // TEST 1: API Health Check
    console.log('\n🏥 TEST 1: API Health Check\n');
    const healthResponse = await makeRequest({
      hostname: 'localhost',
      port: 8000,
      path: '/health',
      method: 'GET'
    });
    
    const healthOk = healthResponse.status === 200;
    logTest('API Health Check', healthOk, {
      status: healthResponse.status,
      response: healthOk ? JSON.parse(healthResponse.data) : null
    });

    if (!healthOk) {
      console.log('\n⚠️  Backend not running. Please start with: python3 run_local.py');
      return;
    }

    // TEST 2: Cost Tracking - Initial State
    console.log('\n💰 TEST 2: Cost Tracking - Initial State\n');
    const initialCostsResponse = await makeRequest({
      hostname: 'localhost',
      port: 8000,
      path: '/api/costs/projects',
      method: 'GET'
    });
    
    const costsOk = initialCostsResponse.status === 200;
    const initialCosts = costsOk ? JSON.parse(initialCostsResponse.data) : [];
    testResults.costTracking.before = initialCosts;
    
    logTest('Cost Tracking API', costsOk, {
      projectCount: initialCosts.length,
      totalCost: initialCosts.reduce((sum, p) => sum + p.total_cost, 0).toFixed(4)
    });

    // TEST 3: Business Analysis
    console.log('\n🔍 TEST 3: Business Analysis\n');
    const businessData = {
      business_input: "Sustainable Fashion E-commerce Platform - We sell eco-friendly clothing made from recycled materials, organic cotton, and sustainable fabrics. Our target audience is environmentally conscious millennials and Gen Z consumers.",
      input_type: "text"
    };
    
    const analysisResponse = await makeRequest({
      hostname: 'localhost',
      port: 8000,
      path: '/api/analyze-business',
      method: 'POST',
      headers: { 'Content-Type': 'application/json' }
    }, JSON.stringify(businessData));
    
    const analysisOk = analysisResponse.status === 200;
    const analysisData = analysisOk ? JSON.parse(analysisResponse.data) : null;
    
    if (analysisOk) {
      testResults.artifacts.projectId = analysisData.project_id;
      logTest('Business Analysis', true, {
        projectId: analysisData.project_id,
        businessName: analysisData.business_name,
        templates: analysisData.template_opportunities.length,
        message: `Created project: ${analysisData.business_name} with ${analysisData.template_opportunities.length} template opportunities`
      });
    } else {
      logTest('Business Analysis', false, { error: analysisResponse.data });
    }

    // TEST 4: Template Creation
    console.log('\n📝 TEST 4: Template Creation\n');
    if (testResults.artifacts.projectId) {
      const templateData = {
        name: "Sustainable Fashion by Category and City",
        pattern: "Sustainable {Category} Fashion in {City} - Eco-Friendly Shopping",
        title_template: "Sustainable {Category} Fashion in {City} | Eco-Friendly {Category}",
        meta_description_template: "Shop sustainable {Category} in {City}. Eco-friendly, ethically made {Category} from recycled materials.",
        h1_template: "Sustainable {Category} Fashion in {City}",
        content_sections: [
          {
            type: "intro",
            content: "Discover the best sustainable {Category} options in {City}. Our eco-friendly {Category} collection features items made from recycled materials and organic fabrics."
          },
          {
            type: "benefits", 
            content: "Why choose sustainable {Category}? Reduce environmental impact while staying stylish in {City}."
          }
        ]
      };
      
      const templateResponse = await makeRequest({
        hostname: 'localhost',
        port: 8000,
        path: `/api/projects/${testResults.artifacts.projectId}/templates`,
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
      }, JSON.stringify(templateData));
      
      const templateOk = templateResponse.status === 200;
      const templateResult = templateOk ? JSON.parse(templateResponse.data) : null;
      
      if (templateOk) {
        testResults.artifacts.templateId = templateResult.id;
        logTest('Template Creation', true, {
          templateId: templateResult.id,
          variables: templateResult.variables,
          message: `Created template with variables: ${templateResult.variables.join(', ')}`
        });
      } else {
        logTest('Template Creation', false, { error: templateResponse.data });
      }
    }

    // TEST 5: AI Variable Generation
    console.log('\n🤖 TEST 5: AI Variable Generation\n');
    if (testResults.artifacts.projectId && testResults.artifacts.templateId) {
      const variableRequest = {
        count: 3,  // Minimal for cost savings
        business_context: {
          name: "EcoFashion Store",
          description: "Sustainable fashion e-commerce",
          target_audience: "Eco-conscious consumers",
          industry: "Fashion/E-commerce"
        }
      };
      
      const variableResponse = await makeRequest({
        hostname: 'localhost',
        port: 8000,
        path: `/api/projects/${testResults.artifacts.projectId}/templates/${testResults.artifacts.templateId}/generate-variables`,
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
      }, JSON.stringify(variableRequest));
      
      const variableOk = variableResponse.status === 200;
      const variableData = variableOk ? JSON.parse(variableResponse.data) : null;
      
      if (variableOk) {
        logTest('Variable Generation', true, {
          totalCombinations: variableData.total_count,
          variables: Object.keys(variableData.variables).map(k => `${k}: ${variableData.variables[k].length} values`),
          message: `Generated ${variableData.total_count} possible combinations`
        });
      } else {
        logTest('Variable Generation', false, { error: variableResponse.data });
      }
    }

    // TEST 6: Page Generation (LIMITED TO 3)
    console.log('\n📄 TEST 6: Page Generation (Limited to 3)\n');
    if (testResults.artifacts.projectId && testResults.artifacts.templateId) {
      // First get the generated variables
      const varsResponse = await makeRequest({
        hostname: 'localhost',
        port: 8000,
        path: `/api/projects/${testResults.artifacts.projectId}/templates/${testResults.artifacts.templateId}/generate-variables`,
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
      }, JSON.stringify({ count: 3 }));
      
      if (varsResponse.status === 200) {
        const varsData = JSON.parse(varsResponse.data);
        
        // Select only first 3 titles
        const selectedTitles = varsData.titles.slice(0, 3);
        const variablesData = {};
        Object.entries(varsData.variables).forEach(([key, values]) => {
          variablesData[key] = values.slice(0, 3);
        });
        
        const pageGenRequest = {
          batch_size: 3,
          selected_titles: selectedTitles,
          variables_data: variablesData
        };
        
        const pageResponse = await makeRequest({
          hostname: 'localhost',
          port: 8000,
          path: `/api/projects/${testResults.artifacts.projectId}/templates/${testResults.artifacts.templateId}/generate`,
          method: 'POST',
          headers: { 'Content-Type': 'application/json' }
        }, JSON.stringify(pageGenRequest));
        
        const pageOk = pageResponse.status === 200;
        const pageData = pageOk ? JSON.parse(pageResponse.data) : null;
        
        if (pageOk) {
          logTest('Page Generation', true, {
            pagesGenerated: pageData.total_generated,
            pageIds: pageData.page_ids,
            message: `Generated ${pageData.total_generated} pages (limited for cost savings)`
          });
        } else {
          logTest('Page Generation', false, { error: pageResponse.data });
        }
      }
    }

    // TEST 7: Export Functionality
    console.log('\n📦 TEST 7: Export Functionality\n');
    if (testResults.artifacts.projectId) {
      const exportRequest = {
        format: "csv",
        include_metadata: true
      };
      
      const exportResponse = await makeRequest({
        hostname: 'localhost',
        port: 8000,
        path: `/api/projects/${testResults.artifacts.projectId}/export`,
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
      }, JSON.stringify(exportRequest));
      
      const exportOk = exportResponse.status === 200;
      const exportData = exportOk ? JSON.parse(exportResponse.data) : null;
      
      if (exportOk) {
        testResults.artifacts.exportId = exportData.export_id;
        logTest('Export Creation', true, {
          exportId: exportData.export_id,
          format: 'CSV',
          status: exportData.status,
          message: `Export initiated with ID: ${exportData.export_id}`
        });
      } else {
        logTest('Export Creation', false, { error: exportResponse.data });
      }
    }

    // TEST 8: Cost Tracking - Final State
    console.log('\n💸 TEST 8: Cost Tracking - Final State\n');
    const finalCostsResponse = await makeRequest({
      hostname: 'localhost',
      port: 8000,
      path: '/api/costs/projects',
      method: 'GET'
    });
    
    const finalCostsOk = finalCostsResponse.status === 200;
    const finalCosts = finalCostsOk ? JSON.parse(finalCostsResponse.data) : [];
    testResults.costTracking.after = finalCosts;
    
    // Calculate cost difference
    const initialTotal = testResults.costTracking.before.reduce((sum, p) => sum + p.total_cost, 0);
    const finalTotal = finalCosts.reduce((sum, p) => sum + p.total_cost, 0);
    testResults.costTracking.costIncurred = finalTotal - initialTotal;
    
    logTest('Cost Tracking Update', finalCostsOk, {
      newProjects: finalCosts.length - testResults.costTracking.before.length,
      totalCostIncurred: testResults.costTracking.costIncurred.toFixed(4),
      message: `Total API cost for this test: $${testResults.costTracking.costIncurred.toFixed(4)}`
    });

    // TEST 9: Project Cost Details
    if (testResults.artifacts.projectId) {
      console.log('\n📊 TEST 9: Project Cost Breakdown\n');
      const projectCostResponse = await makeRequest({
        hostname: 'localhost',
        port: 8000,
        path: `/api/costs/projects/${testResults.artifacts.projectId}`,
        method: 'GET'
      });
      
      const projectCostOk = projectCostResponse.status === 200;
      const projectCosts = projectCostOk ? JSON.parse(projectCostResponse.data) : null;
      
      if (projectCostOk) {
        logTest('Project Cost Details', true, {
          totalCost: projectCosts.total_cost,
          totalTokens: projectCosts.total_tokens,
          operations: Object.keys(projectCosts.by_operation),
          message: `Project used ${projectCosts.total_tokens} tokens across ${projectCosts.total_calls} API calls`
        });
        
        // Show breakdown by operation
        console.log('\n   Cost Breakdown by Operation:');
        Object.entries(projectCosts.by_operation).forEach(([op, data]) => {
          console.log(`   - ${op}: $${data.cost.toFixed(4)} (${data.count} calls, ${data.tokens} tokens)`);
        });
      } else {
        logTest('Project Cost Details', false);
      }
    }

    // TEST 10: Frontend Accessibility
    console.log('\n🌐 TEST 10: Frontend Accessibility\n');
    const frontendResponse = await makeRequest({
      hostname: 'localhost',
      port: 3000,
      path: '/',
      method: 'GET'
    });
    
    const frontendOk = frontendResponse.status === 200;
    logTest('Frontend Homepage', frontendOk, {
      status: frontendResponse.status,
      message: frontendOk ? 'Frontend is accessible' : 'Frontend not running'
    });

    // Check cost tracking page
    const costPageResponse = await makeRequest({
      hostname: 'localhost',
      port: 3000,
      path: '/costs',
      method: 'GET'
    });
    
    const costPageOk = costPageResponse.status === 200;
    logTest('Cost Tracking Page', costPageOk, {
      status: costPageResponse.status,
      message: costPageOk ? 'Cost tracking UI is accessible' : 'Cost tracking page not found'
    });

  } catch (error) {
    console.error('\n❌ Test suite error:', error.message);
    testResults.summary.failed++;
  }

  // Generate final report
  generateReport();
}

function generateReport() {
  console.log('\n' + '='*60);
  console.log('📊 FINAL TEST REPORT');
  console.log('='*60 + '\n');
  
  const successRate = (testResults.summary.passed / testResults.summary.total * 100).toFixed(1);
  
  console.log(`Total Tests: ${testResults.summary.total}`);
  console.log(`✅ Passed: ${testResults.summary.passed}`);
  console.log(`❌ Failed: ${testResults.summary.failed}`);
  console.log(`📈 Success Rate: ${successRate}%`);
  
  console.log('\n💰 COST SUMMARY:');
  console.log(`Total API Cost: $${testResults.costTracking.costIncurred.toFixed(4)}`);
  console.log(`Cost per Test: $${(testResults.costTracking.costIncurred / testResults.summary.total).toFixed(4)}`);
  
  if (testResults.artifacts.projectId) {
    console.log('\n🎯 ARTIFACTS CREATED:');
    console.log(`Project ID: ${testResults.artifacts.projectId}`);
    console.log(`Template ID: ${testResults.artifacts.templateId}`);
    console.log(`Export ID: ${testResults.artifacts.exportId}`);
  }
  
  // Save detailed report
  const reportData = {
    timestamp: new Date().toISOString(),
    summary: {
      ...testResults.summary,
      successRate: parseFloat(successRate)
    },
    costAnalysis: {
      totalCost: testResults.costTracking.costIncurred,
      costPerTest: testResults.costTracking.costIncurred / testResults.summary.total,
      projectsCreated: testResults.costTracking.after.length - testResults.costTracking.before.length
    },
    artifacts: testResults.artifacts,
    tests: testResults.tests
  };
  
  fs.writeFileSync('test-report-full.json', JSON.stringify(reportData, null, 2));
  console.log('\n📁 Detailed report saved to: test-report-full.json');
  
  if (successRate === '100.0') {
    console.log('\n🎉 ALL TESTS PASSED! The Programmatic SEO Tool is fully functional!');
  } else {
    console.log('\n⚠️  Some tests failed. Check the details above.');
  }
}

// Run the tests
console.log('🚀 Starting comprehensive test suite...\n');
runTests();