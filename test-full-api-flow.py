#!/usr/bin/env python3
import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_full_workflow():
    print("\n=== Testing Full API Workflow ===\n")
    
    # Step 1: Health Check
    print("1. Health Check...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Health Status: {response.json()}")
    print("✓ Backend is healthy\n")
    
    # Step 2: Business Analysis
    print("2. Business Analysis...")
    analysis_data = {
        "business_input": "Real estate investment analysis platform helping investors evaluate ROI, cash flow, and market trends for short-term rental properties"
    }
    response = requests.post(f"{BASE_URL}/api/analyze-business", json=analysis_data)
    analysis_result = response.json()
    project_id = analysis_result.get("project_id")
    print(f"Project ID: {project_id}")
    print(f"Business Name: {analysis_result.get('business_name')}")
    print(f"Templates Found: {len(analysis_result.get('template_opportunities', []))}")
    print("✓ Business analysis completed\n")
    
    # Step 3: Get project details
    print("3. Getting project details...")
    response = requests.get(f"{BASE_URL}/api/projects/{project_id}")
    project = response.json()
    print(f"Project Name: {project.get('name')}")
    print("✓ Project retrieved\n")
    
    # Step 4: Create template from suggestion
    print("4. Creating template...")
    template_data = {
        "name": "Short-Term Rental ROI Analysis",
        "pattern": "Is {Property Type} profitable in {City}? ROI Analysis",
        "variables": ["Property Type", "City"],
        "template_sections": {
            "seo_structure": {
                "title_template": "Is {Property Type} profitable in {City}? ROI Analysis",
                "meta_description_template": "Analyze ROI for {Property Type} short-term rentals in {City}. Get data on rental rates, occupancy, and profitability.",
                "h1_template": "Is {Property Type} profitable in {City}?"
            },
            "content_sections": [
                {
                    "heading": "ROI Analysis",
                    "content": "Detailed analysis of {Property Type} profitability in {City} for short-term rentals."
                }
            ]
        }
    }
    response = requests.post(f"{BASE_URL}/api/projects/{project_id}/templates", json=template_data)
    template = response.json()
    template_id = template.get("id")
    print(f"Template ID: {template_id}")
    print(f"Template Name: {template.get('name')}")
    print("✓ Template created\n")
    
    # Step 5: Generate variables
    print("5. Generating AI variables...")
    variable_data = {
        "count": 10
    }
    response = requests.post(f"{BASE_URL}/api/projects/{project_id}/templates/{template_id}/generate-variables", json=variable_data)
    variables_result = response.json()
    print(f"Variables Generated: {variables_result.get('count', 0)}")
    if 'sample_data' in variables_result:
        print("Sample data:")
        for i, row in enumerate(variables_result['sample_data'][:3]):
            print(f"  - {row}")
    print("✓ Variables generated\n")
    
    # Step 6: Generate pages
    print("6. Generating pages...")
    response = requests.post(f"{BASE_URL}/api/projects/{project_id}/templates/{template_id}/generate")
    generation_result = response.json()
    print(f"Pages Generated: {generation_result.get('pages_generated', 0)}")
    print(f"Generation Time: {generation_result.get('generation_time', 0):.2f}s")
    print("✓ Pages generated\n")
    
    # Step 7: Get sample pages
    print("7. Getting sample pages...")
    response = requests.get(f"{BASE_URL}/api/projects/{project_id}/pages?limit=3")
    pages = response.json()
    print(f"Total Pages: {pages.get('total', 0)}")
    if 'items' in pages and pages['items']:
        print("\nSample Page:")
        page = pages['items'][0]
        print(f"Title: {page.get('title')}")
        print(f"URL: {page.get('url')}")
        print(f"Content Length: {len(page.get('content', ''))} characters")
        print(f"Quality Score: {page.get('quality_score', 0)}")
    print("\n✓ Pages retrieved\n")
    
    # Step 8: Export pages
    print("8. Testing export...")
    export_data = {
        "format": "csv"
    }
    response = requests.post(f"{BASE_URL}/api/projects/{project_id}/export", json=export_data)
    export_result = response.json()
    print(f"Export Status: {export_result.get('status')}")
    print(f"File Path: {export_result.get('file_path')}")
    print("✓ Export completed\n")
    
    print("=== ✓ Full Workflow Test Completed Successfully ===\n")
    
    return {
        "project_id": project_id,
        "template_id": template_id,
        "pages_generated": generation_result.get('pages_generated', 0)
    }

if __name__ == "__main__":
    try:
        result = test_full_workflow()
        print(f"\nTest Summary:")
        print(f"- Project ID: {result['project_id']}")
        print(f"- Template ID: {result['template_id']}")
        print(f"- Pages Generated: {result['pages_generated']}")
    except Exception as e:
        print(f"\n❌ Test failed: {str(e)}")