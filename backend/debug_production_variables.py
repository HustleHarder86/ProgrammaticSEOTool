#!/usr/bin/env python3
"""
Debug the variable generation response in production
"""

import requests
import json

BACKEND_URL = "https://programmaticseotool-production.up.railway.app"

# Create a test project and template
print("Creating test project...")
proj_resp = requests.post(
    f"{BACKEND_URL}/api/analyze-business",
    json={"business_input": "Test real estate platform", "input_type": "text"}
)
print(f"Project creation: {proj_resp.status_code}")
if proj_resp.status_code != 200:
    print(f"Error: {proj_resp.text}")
    exit(1)

project_id = proj_resp.json()['project_id']
print(f"Project ID: {project_id}")

# Create template
print("\nCreating template...")
tmpl_resp = requests.post(
    f"{BACKEND_URL}/api/projects/{project_id}/templates",
    json={
        "name": "Test Template",
        "pattern": "{City} {Property} Calculator",
        "title_template": "{Property} Calculator for {City}",
        "meta_description_template": "Calculate ROI for {Property} in {City}",
        "h1_template": "{City} {Property} Investment Calculator",
        "content_sections": [{"type": "intro", "content": "Calculator content"}]
    }
)
print(f"Template creation: {tmpl_resp.status_code}")
if tmpl_resp.status_code not in [200, 201]:
    print(f"Error: {tmpl_resp.text}")
    exit(1)

template_id = tmpl_resp.json()['id']
print(f"Template ID: {template_id}")

# Generate variables
print("\nGenerating variables...")
var_resp = requests.post(
    f"{BACKEND_URL}/api/projects/{project_id}/templates/{template_id}/generate-variables",
    json={}
)
print(f"Variable generation: {var_resp.status_code}")
print(f"\nFull response:")
print(json.dumps(var_resp.json(), indent=2))

# Check if potential pages were created
print("\n\nChecking potential pages...")
pp_resp = requests.get(
    f"{BACKEND_URL}/api/projects/{project_id}/templates/{template_id}/potential-pages"
)
print(f"Potential pages check: {pp_resp.status_code}")
if pp_resp.status_code == 200:
    pp_data = pp_resp.json()
    print(f"Total potential pages: {pp_data.get('total_count', 0)}")
    if pp_data.get('potential_pages'):
        print(f"\nFirst 3 pages:")
        for i, page in enumerate(pp_data['potential_pages'][:3]):
            print(f"  {i+1}. {page['title']}")
else:
    print(f"Error: {pp_resp.text}")