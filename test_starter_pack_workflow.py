#!/usr/bin/env python3
"""Test full workflow for Starter Pack App"""

import requests
import json
import time

API_URL = "http://localhost:8000"

print("🚀 Testing Starter Pack App Workflow\n")

# Step 1: Create Project
print("1️⃣ Creating project...")
project_data = {
    "name": "Starter Pack App SEO",
    "business_input": "Starter Pack App is a tool for creating and sharing curated lists of social media accounts to follow on platforms like Bluesky. Users can create themed starter packs to help new users discover relevant accounts in specific niches or communities.",
    "business_analysis": None
}

response = requests.post(f"{API_URL}/api/projects", json=project_data)
if response.status_code == 200:
    project = response.json()
    project_id = project['id']
    print(f"✅ Project created: {project_id}")
else:
    print(f"❌ Failed to create project: {response.status_code}")
    exit(1)

# Step 2: Create Template
print("\n2️⃣ Creating template...")
template_data = {
    "name": "Niche Platform Starter Packs",
    "pattern": "Best {Niche} Starter Packs on {Platform}",
    "title_template": "Best {Niche} Starter Packs on {Platform} - 2024 Guide",
    "meta_description_template": "Discover the best {Niche} starter packs on {Platform}. Curated lists of must-follow accounts for {Niche} enthusiasts.",
    "h1_template": "Best {Niche} Starter Packs on {Platform}",
    "content_sections": [
        {
            "heading": "Top {Niche} Accounts to Follow",
            "content": "Get started on {Platform} with these essential {Niche} accounts. Our curated starter pack helps you instantly connect with the {Niche} community."
        },
        {
            "heading": "Why Use {Niche} Starter Packs",
            "content": "Starter packs make it easy to find quality {Niche} content on {Platform}. Skip the search and follow these pre-vetted accounts."
        },
        {
            "heading": "Building Your {Niche} Network",
            "content": "Connect with other {Niche} enthusiasts on {Platform} using our starter pack recommendations."
        }
    ]
}

response = requests.post(f"{API_URL}/api/projects/{project_id}/templates", json=template_data)
if response.status_code == 200:
    template = response.json()
    template_id = template['id']
    print(f"✅ Template created: {template_id}")
    print(f"   Variables: {template.get('variables', [])}")
else:
    print(f"❌ Failed to create template: {response.status_code}")
    print(f"   Error: {response.text}")
    exit(1)

# Step 3: Import Data
print("\n3️⃣ Importing data...")
data_payload = {
    "name": "Starter Pack Niches and Platforms",
    "data": [
        {"Niche": "Tech", "Platform": "Bluesky"},
        {"Niche": "Design", "Platform": "Bluesky"},
        {"Niche": "Marketing", "Platform": "Twitter"},
        {"Niche": "AI", "Platform": "Bluesky"},
        {"Niche": "Photography", "Platform": "Instagram"},
        {"Niche": "Gaming", "Platform": "Twitter"},
        {"Niche": "Finance", "Platform": "LinkedIn"},
        {"Niche": "Food", "Platform": "Instagram"},
        {"Niche": "Travel", "Platform": "Twitter"},
        {"Niche": "Fitness", "Platform": "Instagram"}
    ]
}

response = requests.post(f"{API_URL}/api/projects/{project_id}/data", json=data_payload)
if response.status_code == 200:
    dataset = response.json()
    dataset_id = dataset['id']
    print(f"✅ Data imported: {dataset_id}")
    print(f"   Rows: {len(data_payload['data'])}")
else:
    print(f"❌ Failed to import data: {response.status_code}")
    exit(1)

# Step 4: Preview Generation
print("\n4️⃣ Previewing page generation...")
preview_data = {
    "template_id": template_id,
    "dataset_id": dataset_id,
    "limit": 3
}

response = requests.post(
    f"{API_URL}/api/projects/{project_id}/templates/{template_id}/generate-preview",
    json=preview_data
)

if response.status_code == 200:
    preview = response.json()
    print(f"✅ Preview generated: {len(preview.get('pages', []))} pages")
    for i, page in enumerate(preview.get('pages', [])[:3]):
        print(f"\n   Page {i+1}:")
        print(f"   Title: {page.get('seo_title', 'N/A')}")
        print(f"   URL: {page.get('url_slug', 'N/A')}")
else:
    print(f"❌ Failed to generate preview: {response.status_code}")

# Step 5: Generate All Pages
print("\n5️⃣ Generating all pages...")
generate_data = {"batch_size": 100}

response = requests.post(
    f"{API_URL}/api/projects/{project_id}/templates/{template_id}/generate",
    json=generate_data
)

if response.status_code == 200:
    result = response.json()
    print(f"✅ Pages generated: {result.get('total_generated', 0)}")
else:
    print(f"❌ Failed to generate pages: {response.status_code}")
    print(f"   Error: {response.text}")

# Step 6: Export as CSV
print("\n6️⃣ Exporting as CSV...")
export_data = {
    "format": "csv",
    "include_seo_data": True
}

response = requests.post(f"{API_URL}/api/projects/{project_id}/export", json=export_data)
if response.status_code == 200:
    export_job = response.json()
    export_id = export_job.get('export_id')
    print(f"✅ Export started: {export_id}")
    
    # Wait and check status
    time.sleep(2)
    status_response = requests.get(f"{API_URL}/api/exports/{export_id}/status")
    if status_response.status_code == 200:
        status = status_response.json()
        print(f"   Status: {status.get('status')}")
        if status.get('status') == 'completed':
            print(f"   File: {status.get('file_path')}")
else:
    print(f"❌ Failed to start export: {response.status_code}")

print("\n✨ Workflow test complete!")