#!/usr/bin/env python3
"""Test templates API endpoint"""

import requests

project_id = "c9f3b1f8-d1a5-4bec-8219-64b8f1b1e8c2"
api_url = "http://localhost:8000"

print(f"Testing templates for project: {project_id}\n")

# Test 1: Get project details
print("1. Getting project details...")
try:
    response = requests.get(f"{api_url}/api/projects/{project_id}")
    if response.status_code == 200:
        project = response.json()
        print(f"✅ Project found: {project.get('name', 'Unknown')}")
        print(f"   Business: {project.get('business_analysis', {}).get('business_name', 'N/A')}")
    else:
        print(f"❌ Project not found: {response.status_code}")
        print(f"   Response: {response.text}")
except Exception as e:
    print(f"❌ Error: {e}")

# Test 2: Get templates
print("\n2. Getting templates...")
try:
    response = requests.get(f"{api_url}/api/projects/{project_id}/templates")
    if response.status_code == 200:
        templates = response.json()
        print(f"✅ Found {len(templates)} templates")
        for i, template in enumerate(templates):
            print(f"\n   Template {i+1}:")
            print(f"   - Name: {template.get('name')}")
            print(f"   - Pattern: {template.get('pattern')}")
            print(f"   - Variables: {template.get('variables')}")
    else:
        print(f"❌ Failed to get templates: {response.status_code}")
        print(f"   Response: {response.text}")
except Exception as e:
    print(f"❌ Error: {e}")

# Test 3: List all projects to find the right one
print("\n3. Listing all projects...")
try:
    response = requests.get(f"{api_url}/api/projects")
    if response.status_code == 200:
        projects = response.json()
        print(f"✅ Found {len(projects)} total projects")
        for project in projects:
            print(f"\n   Project: {project.get('name')}")
            print(f"   - ID: {project.get('id')}")
            print(f"   - Business: {project.get('business_input', 'N/A')[:50]}...")
except Exception as e:
    print(f"❌ Error: {e}")