#!/usr/bin/env python3
"""
Comprehensive system test for Programmatic SEO Tool
Tests both backend API and simulates frontend interactions
"""

import requests
import json
import time
import sys
from datetime import datetime

# Configuration
BACKEND_URL = "http://localhost:8000"
FRONTEND_URL = "http://localhost:3000"

# Colors for output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def print_test(name, status, details=""):
    """Print test result with color"""
    if status == "PASS":
        print(f"{GREEN}✓ {name}{RESET} {details}")
    elif status == "FAIL":
        print(f"{RED}✗ {name}{RESET} {details}")
    elif status == "WARN":
        print(f"{YELLOW}⚠ {name}{RESET} {details}")
    else:
        print(f"{BLUE}→ {name}{RESET} {details}")

def test_backend_health():
    """Test backend health endpoint"""
    try:
        response = requests.get(f"{BACKEND_URL}/health")
        if response.status_code == 200:
            data = response.json()
            print_test("Backend Health Check", "PASS", f"- Database: {data.get('database_status')}")
            return True
        else:
            print_test("Backend Health Check", "FAIL", f"- Status: {response.status_code}")
            return False
    except Exception as e:
        print_test("Backend Health Check", "FAIL", f"- Error: {str(e)}")
        return False

def test_frontend_connectivity():
    """Test if frontend is running"""
    try:
        response = requests.get(FRONTEND_URL)
        if response.status_code == 200:
            print_test("Frontend Running", "PASS", "- Next.js server responding")
            return True
        else:
            print_test("Frontend Running", "FAIL", f"- Status: {response.status_code}")
            return False
    except Exception as e:
        print_test("Frontend Running", "FAIL", f"- Error: {str(e)}")
        return False

def test_business_analysis():
    """Test business analysis endpoint"""
    print_test("Business Analysis Test", "INFO", "")
    
    test_data = {
        "business_input": "Canva is a graphic design platform that allows users to create social media graphics, presentations, posters and other visual content."
    }
    
    try:
        response = requests.post(
            f"{BACKEND_URL}/api/analyze-business",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print_test("  - AI Analysis", "PASS", f"- Found {len(data.get('template_suggestions', []))} template suggestions")
            if data.get('template_suggestions'):
                print(f"    Sample template: {data['template_suggestions'][0].get('template_pattern', 'N/A')}")
            return True
        else:
            print_test("  - AI Analysis", "FAIL", f"- Status: {response.status_code}")
            print(f"    Response: {response.text}")
            return False
    except Exception as e:
        print_test("  - AI Analysis", "FAIL", f"- Error: {str(e)}")
        return False

def test_project_creation():
    """Test creating a new project"""
    print_test("Project Management Test", "INFO", "")
    
    project_data = {
        "name": f"Test Project {datetime.now().strftime('%Y%m%d_%H%M%S')}",
        "business_input": "Test e-commerce store selling outdoor gear",
        "business_analysis": None
    }
    
    try:
        # Create project
        response = requests.post(
            f"{BACKEND_URL}/api/projects",
            json=project_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            project = response.json()
            project_id = project.get('id')
            print_test("  - Create Project", "PASS", f"- Project ID: {project_id}")
            
            # Get project details
            detail_response = requests.get(f"{BACKEND_URL}/api/projects/{project_id}")
            if detail_response.status_code == 200:
                print_test("  - Get Project Details", "PASS", "")
                return project_id
            else:
                print_test("  - Get Project Details", "FAIL", f"- Status: {detail_response.status_code}")
                return None
        else:
            print_test("  - Create Project", "FAIL", f"- Status: {response.status_code}")
            print(f"    Response: {response.text}")
            return None
    except Exception as e:
        print_test("  - Create Project", "FAIL", f"- Error: {str(e)}")
        return None

def test_template_creation(project_id):
    """Test template creation"""
    if not project_id:
        print_test("Template Creation Test", "SKIP", "- No project ID")
        return None
        
    print_test("Template Creation Test", "INFO", "")
    
    template_data = {
        "name": "Location Pages",
        "pattern": "Best {Product} in {City}",
        "title_template": "Best {Product} in {City} - 2024 Guide",
        "meta_description_template": "Find the best {Product} in {City}. Compare prices, read reviews, and discover top-rated options.",
        "h1_template": "Best {Product} in {City}",
        "content_sections": [
            {
                "heading": "Overview",
                "content": "Looking for the best {Product} in {City}? We've got you covered!"
            },
            {
                "heading": "Top {Product} Options",
                "content": "Discover amazing {Product} deals and selections in {City} area."
            }
        ]
    }
    
    try:
        response = requests.post(
            f"{BACKEND_URL}/api/projects/{project_id}/templates",
            json=template_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            template = response.json()
            template_id = template.get('id')
            print_test("  - Create Template", "PASS", f"- Template ID: {template_id}")
            return template_id
        else:
            print_test("  - Create Template", "FAIL", f"- Status: {response.status_code}")
            print(f"    Response: {response.text}")
            return None
    except Exception as e:
        print_test("  - Create Template", "FAIL", f"- Error: {str(e)}")
        return None

def test_data_import(project_id):
    """Test data import via JSON"""
    if not project_id:
        print_test("Data Import Test", "SKIP", "- No project ID")
        return None
        
    print_test("Data Import Test", "INFO", "")
    
    data_payload = {
        "name": "Test Cities and Products",
        "data": [
            {"City": "New York", "Product": "Running Shoes"},
            {"City": "New York", "Product": "Hiking Boots"},
            {"City": "New York", "Product": "Camping Gear"},
            {"City": "Los Angeles", "Product": "Running Shoes"},
            {"City": "Los Angeles", "Product": "Hiking Boots"},
            {"City": "Los Angeles", "Product": "Camping Gear"},
            {"City": "Chicago", "Product": "Running Shoes"},
            {"City": "Chicago", "Product": "Hiking Boots"},
            {"City": "Chicago", "Product": "Camping Gear"},
            {"City": "Houston", "Product": "Running Shoes"},
            {"City": "Houston", "Product": "Hiking Boots"},
            {"City": "Houston", "Product": "Camping Gear"},
            {"City": "Phoenix", "Product": "Running Shoes"},
            {"City": "Phoenix", "Product": "Hiking Boots"},
            {"City": "Phoenix", "Product": "Camping Gear"}
        ]
    }
    
    try:
        response = requests.post(
            f"{BACKEND_URL}/api/projects/{project_id}/data",
            json=data_payload,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            dataset = response.json()
            dataset_id = dataset.get('id')
            print_test("  - Import Data", "PASS", f"- Dataset ID: {dataset_id}")
            print(f"    Total rows: {len(data_payload['data'])} entries")
            return dataset_id
        else:
            print_test("  - Import Data", "FAIL", f"- Status: {response.status_code}")
            print(f"    Response: {response.text}")
            return None
    except Exception as e:
        print_test("  - Import Data", "FAIL", f"- Error: {str(e)}")
        return None

def test_page_generation(project_id, template_id, dataset_id):
    """Test page generation"""
    if not all([project_id, template_id, dataset_id]):
        print_test("Page Generation Test", "SKIP", "- Missing prerequisites")
        return None
        
    print_test("Page Generation Test", "INFO", "")
    
    # First test preview
    preview_data = {
        "template_id": template_id,
        "dataset_id": dataset_id,
        "limit": 3
    }
    
    try:
        # Preview generation
        preview_response = requests.post(
            f"{BACKEND_URL}/api/projects/{project_id}/templates/{template_id}/generate-preview",
            json=preview_data,
            headers={"Content-Type": "application/json"}
        )
        
        if preview_response.status_code == 200:
            preview = preview_response.json()
            print_test("  - Preview Generation", "PASS", f"- {len(preview.get('pages', []))} preview pages")
        else:
            print_test("  - Preview Generation", "FAIL", f"- Status: {preview_response.status_code}")
        
        # Full generation
        generate_data = {
            "batch_size": 100
        }
        
        generate_response = requests.post(
            f"{BACKEND_URL}/api/projects/{project_id}/templates/{template_id}/generate",
            json=generate_data,
            headers={"Content-Type": "application/json"}
        )
        
        if generate_response.status_code == 200:
            result = generate_response.json()
            print_test("  - Full Generation", "PASS", f"- {result.get('pages_generated', 0)} pages created")
            return True
        else:
            print_test("  - Full Generation", "FAIL", f"- Status: {generate_response.status_code}")
            return False
            
    except Exception as e:
        print_test("  - Page Generation", "FAIL", f"- Error: {str(e)}")
        return False

def test_export(project_id):
    """Test export functionality"""
    if not project_id:
        print_test("Export Test", "SKIP", "- No project ID")
        return None
        
    print_test("Export Test", "INFO", "")
    
    export_data = {
        "format": "csv",
        "include_seo_data": True
    }
    
    try:
        response = requests.post(
            f"{BACKEND_URL}/api/projects/{project_id}/export",
            json=export_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            export_job = response.json()
            export_id = export_job.get('export_id')
            print_test("  - Start Export", "PASS", f"- Export ID: {export_id}")
            
            # Check status
            time.sleep(2)  # Wait for export to process
            status_response = requests.get(f"{BACKEND_URL}/api/exports/{export_id}/status")
            
            if status_response.status_code == 200:
                status = status_response.json()
                print_test("  - Export Status", "PASS", f"- Status: {status.get('status')}")
                return True
            else:
                print_test("  - Export Status", "FAIL", f"- Status: {status_response.status_code}")
                return False
        else:
            print_test("  - Start Export", "FAIL", f"- Status: {response.status_code}")
            return False
            
    except Exception as e:
        print_test("  - Export", "FAIL", f"- Error: {str(e)}")
        return False

def main():
    """Run all tests"""
    print(f"\n{BLUE}={'='*60}{RESET}")
    print(f"{BLUE}Programmatic SEO Tool - System Test{RESET}")
    print(f"{BLUE}={'='*60}{RESET}\n")
    
    # Check if servers are running
    print(f"{YELLOW}Checking server connectivity...{RESET}\n")
    
    backend_ok = test_backend_health()
    frontend_ok = test_frontend_connectivity()
    
    if not backend_ok:
        print(f"\n{RED}Backend server is not running!{RESET}")
        print("Please run: python3 run_local.py")
        sys.exit(1)
    
    if not frontend_ok:
        print(f"\n{YELLOW}Frontend server is not running (optional for API tests){RESET}")
    
    print(f"\n{YELLOW}Running functional tests...{RESET}\n")
    
    # Test business analysis
    test_business_analysis()
    
    # Test full workflow
    project_id = test_project_creation()
    template_id = test_template_creation(project_id)
    dataset_id = test_data_import(project_id)
    test_page_generation(project_id, template_id, dataset_id)
    test_export(project_id)
    
    print(f"\n{BLUE}={'='*60}{RESET}")
    print(f"{GREEN}Test suite completed!{RESET}")
    print(f"{BLUE}={'='*60}{RESET}\n")

if __name__ == "__main__":
    main()