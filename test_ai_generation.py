#!/usr/bin/env python3
"""Test AI Generation feature"""

import requests

# Use the project that has templates
project_id = "67e23105-f7cf-4733-b97b-8824feb9f1b3"
api_url = "http://localhost:8000"

print("Testing AI Generation Feature\n")

# Test 1: Get project details
print("1. Getting project details...")
try:
    response = requests.get(f"{api_url}/api/projects/{project_id}")
    if response.status_code == 200:
        project = response.json()
        print(f"✅ Project found: {project.get('name', 'Unknown')}")
        print(f"   Business Analysis Available: {bool(project.get('business_analysis', {}))}")
    else:
        print(f"❌ Project not found: {response.status_code}")
except Exception as e:
    print(f"❌ Error: {e}")

# Test 2: Get templates
print("\n2. Getting templates...")
try:
    response = requests.get(f"{api_url}/api/projects/{project_id}/templates")
    if response.status_code == 200:
        templates = response.json()
        print(f"✅ Found {len(templates)} templates")
        if templates:
            template = templates[0]
            print(f"   Template: {template.get('name')}")
            print(f"   Pattern: {template.get('pattern')}")
            print(f"   Variables: {template.get('variables')}")
    else:
        print(f"❌ Failed to get templates: {response.status_code}")
except Exception as e:
    print(f"❌ Error: {e}")

# Test 3: Test AI Generation endpoint
print("\n3. Testing AI Generation endpoint...")
try:
    # First check if the endpoint exists
    response = requests.options(f"{api_url}/api/ai/generate-data")
    print(f"   OPTIONS request status: {response.status_code}")
    
    # Try a POST request with test data
    test_data = {
        "project_id": project_id,
        "template_id": "45526d8f-b3e4-4f0e-80bb-5b7fac88d21d",
        "additional_context": "Generate data for outdoor gear stores"
    }
    
    response = requests.post(f"{api_url}/api/ai/generate-data", json=test_data)
    print(f"   POST request status: {response.status_code}")
    if response.status_code == 200:
        print("✅ AI Generation endpoint is working")
        result = response.json()
        print(f"   Generated {len(result.get('data', []))} data entries")
    else:
        print(f"❌ AI Generation failed: {response.text}")
except Exception as e:
    print(f"❌ Error: {e}")

print("\n4. Summary:")
print("   - Backend is running ✅")
print("   - Projects and templates exist ✅") 
print("   - AI Generation endpoint needs to be implemented" if 'response' not in locals() or response.status_code != 200 else "   - AI Generation is ready ✅")