#!/usr/bin/env python3
"""Test the frontend flow for page generation with potential pages"""

import requests
import json
import time

# Configuration
BASE_URL = "http://localhost:8000"
PROJECT_ID = "844fe485-b120-4c17-b37c-cc8f017c65cc"
TEMPLATE_ID = "5920efb6-a6cc-47ee-948f-6e6943aecd77"

print("🧪 Testing Frontend Page Generation Flow")
print("=" * 50)

# Step 1: Get project details
print("\n1️⃣ Getting project details...")
response = requests.get(f"{BASE_URL}/api/projects/{PROJECT_ID}")
if response.status_code == 200:
    project = response.json()
    print(f"✅ Project: {project['name']}")
else:
    print(f"❌ Failed to get project: {response.status_code}")
    exit(1)

# Step 2: Get template details
print("\n2️⃣ Getting template details...")
response = requests.get(f"{BASE_URL}/api/projects/{PROJECT_ID}/templates")
if response.status_code == 200:
    templates = response.json()
    if templates:
        template = templates[0]
        print(f"✅ Template: {template['name']} - Pattern: {template['pattern']}")
        print(f"   Variables: {', '.join(template['variables'])}")
    else:
        print("❌ No templates found")
        exit(1)
else:
    print(f"❌ Failed to get templates: {response.status_code}")
    exit(1)

# Step 3: Generate variables
print("\n3️⃣ Generating variables for template...")
response = requests.post(
    f"{BASE_URL}/api/projects/{PROJECT_ID}/templates/{TEMPLATE_ID}/generate-variables",
    json={}
)
if response.status_code == 200:
    result = response.json()
    print(f"✅ Variables generated successfully")
    print(f"   Potential pages created: {result.get('potential_pages_generated', 0)}")
else:
    print(f"❌ Failed to generate variables: {response.status_code}")
    print(f"   Response: {response.text}")

# Step 4: Get potential pages
print("\n4️⃣ Getting potential pages...")
response = requests.get(
    f"{BASE_URL}/api/projects/{PROJECT_ID}/templates/{TEMPLATE_ID}/potential-pages"
)
potential_pages = []
if response.status_code == 200:
    data = response.json()
    # Handle both dict response (with 'pages' key) and list response
    if isinstance(data, dict) and 'pages' in data:
        potential_pages = data['pages']
    elif isinstance(data, list):
        potential_pages = data
    else:
        # Try to extract pages from the response
        potential_pages = data.get('potential_pages', [])
    
    print(f"✅ Found {len(potential_pages)} potential pages")
    if potential_pages:
        print("   Sample pages:")
        for page in potential_pages[:5]:
            print(f"   - {page['title']} (ID: {page['id']})")
else:
    print(f"❌ Failed to get potential pages: {response.status_code}")
    print(f"   Response: {response.text}")

# Step 5: Test page selection and generation
print("\n5️⃣ Testing page selection and generation...")
if potential_pages:
    # Select first 3 pages
    selected_ids = [p['id'] for p in potential_pages[:3]]
    print(f"   Selecting {len(selected_ids)} pages for generation...")
    
    response = requests.post(
        f"{BASE_URL}/api/projects/{PROJECT_ID}/templates/{TEMPLATE_ID}/generate-selected-pages",
        json={"page_ids": selected_ids}
    )
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Pages generated successfully!")
        print(f"   Total generated: {result.get('generated_count', 0)}")
        print(f"   Status: {result.get('status', 'unknown')}")
    else:
        print(f"❌ Failed to generate pages: {response.status_code}")
        print(f"   Response: {response.text}")

print("\n" + "=" * 50)
print("✨ Test completed!")