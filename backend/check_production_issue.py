#!/usr/bin/env python3
"""
Debug specific production issues with the Programmatic SEO Tool
"""

import requests
import json
import sys

BACKEND_URL = "https://programmaticseotool-production.up.railway.app"

def debug_variable_generation():
    """Debug why variable generation returns 0 combinations"""
    
    print("🔍 Debugging Variable Generation Issue")
    print("=" * 60)
    
    # First create a fresh project and template
    print("\n1️⃣ Creating test project...")
    project_response = requests.post(
        f"{BACKEND_URL}/api/analyze-business",
        json={
            "business_input": "Test project for debugging variable generation",
            "input_type": "text"
        },
        timeout=30
    )
    
    if project_response.status_code != 200:
        print(f"❌ Failed to create project: {project_response.status_code}")
        return
        
    project_id = project_response.json()['project_id']
    print(f"✅ Project created: {project_id}")
    
    # Create template
    print("\n2️⃣ Creating test template...")
    template_response = requests.post(
        f"{BACKEND_URL}/api/projects/{project_id}/templates",
        json={
            "name": "Debug Template",
            "pattern": "{City} {Service} Guide",
            "title_template": "{Service} Guide for {City}",
            "meta_description_template": "Complete guide to {Service} in {City}",
            "h1_template": "{City} {Service} Guide",
            "content_sections": [{"type": "intro", "content": "Guide content"}]
        },
        timeout=30
    )
    
    if template_response.status_code not in [200, 201]:
        print(f"❌ Failed to create template: {template_response.status_code}")
        return
        
    template = template_response.json()
    template_id = template['id']
    print(f"✅ Template created: {template_id}")
    print(f"   Variables: {template['variables']}")
    
    # Test variable generation with explicit data
    print("\n3️⃣ Testing variable generation endpoint...")
    
    # First, check if the endpoint expects any specific format
    var_response = requests.post(
        f"{BACKEND_URL}/api/projects/{project_id}/templates/{template_id}/generate-variables",
        json={},  # Empty body as per API
        timeout=60
    )
    
    print(f"   Status: {var_response.status_code}")
    if var_response.status_code == 200:
        result = var_response.json()
        print(f"   Response: {json.dumps(result, indent=2)}")
        
        # Check the structure
        if 'variables_data' in result:
            print(f"\n   Variables data structure:")
            for var, values in result.get('variables_data', {}).items():
                print(f"   - {var}: {len(values) if isinstance(values, list) else 'not a list'} values")
    else:
        print(f"   Error: {var_response.text[:500]}")
    
    # Test manual data addition
    print("\n4️⃣ Testing manual data addition...")
    
    # Try adding a dataset
    dataset_response = requests.post(
        f"{BACKEND_URL}/api/projects/{project_id}/data",
        json={
            "name": "Test Data",
            "data": [
                {"City": "Toronto", "Service": "Plumbing"},
                {"City": "Vancouver", "Service": "Electrical"},
                {"City": "Calgary", "Service": "HVAC"}
            ]
        },
        timeout=30
    )
    
    print(f"   Dataset creation status: {dataset_response.status_code}")
    if dataset_response.status_code in [200, 201]:
        print("   ✅ Dataset created successfully")
    else:
        print(f"   ❌ Dataset creation failed: {dataset_response.text[:200]}")
    
    # Now test potential pages generation with manual data
    print("\n5️⃣ Testing potential pages generation...")
    
    # Method 1: Let it use datasets
    potential_response = requests.post(
        f"{BACKEND_URL}/api/projects/{project_id}/templates/{template_id}/generate-potential-pages",
        json={},
        timeout=30
    )
    
    print(f"   Method 1 (use datasets) - Status: {potential_response.status_code}")
    if potential_response.status_code in [200, 201]:
        result = potential_response.json()
        print(f"   Pages generated: {result.get('total_potential_pages', 0)}")
    
    # Method 2: Provide explicit data
    potential_response2 = requests.post(
        f"{BACKEND_URL}/api/projects/{project_id}/templates/{template_id}/generate-potential-pages",
        json={
            "variables_data": {
                "City": [
                    {"value": "Toronto", "dataset_id": "manual", "dataset_name": "manual", "metadata": {}},
                    {"value": "Vancouver", "dataset_id": "manual", "dataset_name": "manual", "metadata": {}}
                ],
                "Service": [
                    {"value": "Plumbing", "dataset_id": "manual", "dataset_name": "manual", "metadata": {}},
                    {"value": "Electrical", "dataset_id": "manual", "dataset_name": "manual", "metadata": {}}
                ]
            },
            "max_combinations": 10
        },
        timeout=30
    )
    
    print(f"\n   Method 2 (explicit data) - Status: {potential_response2.status_code}")
    if potential_response2.status_code in [200, 201]:
        result = potential_response2.json()
        print(f"   Pages generated: {result.get('total_potential_pages', 0)}")
    else:
        print(f"   Error: {potential_response2.text[:300]}")
    
    # Check if potential_pages table exists
    print("\n6️⃣ Checking database schema...")
    
    # Try to retrieve potential pages (will fail if table doesn't exist)
    check_response = requests.get(
        f"{BACKEND_URL}/api/projects/{project_id}/templates/{template_id}/potential-pages",
        timeout=30
    )
    
    if check_response.status_code == 200:
        print("   ✅ Potential pages table appears to exist")
        result = check_response.json()
        print(f"   Total potential pages: {result.get('total_count', 0)}")
    elif check_response.status_code == 500:
        print("   ❌ Potential pages table might not exist in production")
        print(f"   Error: {check_response.text[:200]}")
    
    print("\n" + "=" * 60)
    print("🔍 DIAGNOSIS:")
    print("=" * 60)
    
    print("\nPossible issues:")
    print("1. The potential_pages table might not exist in production database")
    print("2. The variable generation endpoint might not be returning data in expected format")
    print("3. The page generator might not be finding the correct methods")
    print("\nRecommended fixes:")
    print("1. Run database migration on Railway to create potential_pages table")
    print("2. Check Railway logs for specific errors")
    print("3. Verify all imports and method names in production")

def main():
    """Run debugging"""
    debug_variable_generation()

if __name__ == "__main__":
    main()