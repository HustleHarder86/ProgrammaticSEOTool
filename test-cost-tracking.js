#!/usr/bin/env node

const http = require('http');

console.log('🧪 Testing Cost Tracking API\n');

async function makeRequest(options, postData = null) {
  return new Promise((resolve, reject) => {
    const req = http.request(options, (res) => {
      let data = '';
      res.on('data', (chunk) => { data += chunk; });
      res.on('end', () => {
        resolve({
          status: res.statusCode,
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

async function testCostTracking() {
  try {
    // 1. Test pricing endpoint
    console.log('1️⃣ Testing pricing endpoint...');
    const pricingResponse = await makeRequest({
      hostname: 'localhost',
      port: 8000,
      path: '/api/costs/pricing',
      method: 'GET'
    });
    
    if (pricingResponse.status === 200) {
      console.log('✅ Pricing endpoint working');
      const pricing = JSON.parse(pricingResponse.data);
      console.log('   Providers:', Object.keys(pricing.pricing).join(', '));
    } else {
      console.log('❌ Pricing endpoint failed');
    }
    
    // 2. Test cost estimation
    console.log('\n2️⃣ Testing cost estimation...');
    const estimateResponse = await makeRequest({
      hostname: 'localhost',
      port: 8000,
      path: '/api/costs/estimate?operation=business_analysis&provider=perplexity&count=1',
      method: 'GET'
    });
    
    if (estimateResponse.status === 200) {
      console.log('✅ Cost estimation working');
      const estimate = JSON.parse(estimateResponse.data);
      console.log(`   Estimated cost: $${estimate.estimated_cost}`);
      console.log(`   Estimated tokens: ${estimate.estimated_total_tokens}`);
    } else {
      console.log('❌ Cost estimation failed');
    }
    
    // 3. Test project costs summary
    console.log('\n3️⃣ Testing project costs summary...');
    const summaryResponse = await makeRequest({
      hostname: 'localhost',
      port: 8000,
      path: '/api/costs/projects',
      method: 'GET'
    });
    
    if (summaryResponse.status === 200) {
      console.log('✅ Project costs endpoint working');
      const summaries = JSON.parse(summaryResponse.data);
      console.log(`   Found ${summaries.length} projects with costs`);
      if (summaries.length > 0) {
        console.log(`   Top project: ${summaries[0].project_name} - $${summaries[0].total_cost}`);
      }
    } else {
      console.log('❌ Project costs endpoint failed');
    }
    
    // 4. Run a business analysis to generate costs
    console.log('\n4️⃣ Running business analysis to generate costs...');
    const analysisResponse = await makeRequest({
      hostname: 'localhost',
      port: 8000,
      path: '/api/analyze-business',
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      }
    }, JSON.stringify({
      business_input: "Test business for cost tracking - AI-powered analytics platform",
      input_type: "text"
    }));
    
    if (analysisResponse.status === 200) {
      console.log('✅ Business analysis completed');
      const analysis = JSON.parse(analysisResponse.data);
      const projectId = analysis.project_id;
      
      // 5. Check costs for this project
      console.log('\n5️⃣ Checking costs for new project...');
      const projectCostResponse = await makeRequest({
        hostname: 'localhost',
        port: 8000,
        path: `/api/costs/projects/${projectId}`,
        method: 'GET'
      });
      
      if (projectCostResponse.status === 200) {
        console.log('✅ Project cost tracking working');
        const costs = JSON.parse(projectCostResponse.data);
        console.log(`   Total cost: $${costs.total_cost}`);
        console.log(`   Total tokens: ${costs.total_tokens}`);
        console.log(`   API calls: ${costs.total_calls}`);
        console.log(`   Operations:`, Object.keys(costs.by_operation).join(', '));
      } else {
        console.log('❌ Project cost retrieval failed');
      }
    } else {
      console.log('❌ Business analysis failed');
    }
    
    console.log('\n✨ Cost tracking test complete!');
    
  } catch (error) {
    console.error('\n❌ Test failed:', error.message);
  }
}

// Run the test
testCostTracking();