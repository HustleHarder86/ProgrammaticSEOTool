"""Test script for data endpoints"""
import requests
import json
from pathlib import Path

# Base URL for local testing
BASE_URL = "http://localhost:8000"

def test_data_endpoints():
    """Test the data import and management endpoints"""
    
    print("Testing Data Endpoints...")
    print("-" * 50)
    
    # First, create a test project
    print("\n1. Creating a test project...")
    project_data = {
        "name": "Test Data Import Project",
        "business_input": "A test project for data import",
        "business_analysis": {
            "business_name": "Test Business",
            "business_description": "Testing data import functionality"
        }
    }
    
    response = requests.post(f"{BASE_URL}/api/projects", json=project_data)
    if response.status_code == 200:
        project = response.json()
        project_id = project['id']
        print(f"✓ Project created: {project_id}")
    else:
        print(f"✗ Failed to create project: {response.text}")
        return
    
    # Test manual data creation
    print("\n2. Creating manual dataset...")
    manual_data = {
        "name": "Cities Dataset",
        "data": [
            {"city": "New York", "state": "NY", "population": "8.3M"},
            {"city": "Los Angeles", "state": "CA", "population": "4M"},
            {"city": "Chicago", "state": "IL", "population": "2.7M"},
            {"city": "Houston", "state": "TX", "population": "2.3M"},
            {"city": "Phoenix", "state": "AZ", "population": "1.7M"}
        ]
    }
    
    response = requests.post(f"{BASE_URL}/api/projects/{project_id}/data", json=manual_data)
    if response.status_code == 200:
        dataset = response.json()
        dataset_id = dataset['id']
        print(f"✓ Dataset created: {dataset_id}")
        print(f"  - Name: {dataset['name']}")
        print(f"  - Rows: {dataset['row_count']}")
        print(f"  - Columns: {dataset['columns']}")
    else:
        print(f"✗ Failed to create dataset: {response.text}")
        return
    
    # Get all datasets for project
    print("\n3. Listing project datasets...")
    response = requests.get(f"{BASE_URL}/api/projects/{project_id}/data")
    if response.status_code == 200:
        datasets = response.json()
        print(f"✓ Found {len(datasets)} dataset(s)")
        for ds in datasets:
            print(f"  - {ds['name']} ({ds['row_count']} rows)")
    else:
        print(f"✗ Failed to list datasets: {response.text}")
    
    # Get detailed dataset
    print("\n4. Getting dataset details...")
    response = requests.get(f"{BASE_URL}/api/projects/{project_id}/data/{dataset_id}")
    if response.status_code == 200:
        details = response.json()
        print(f"✓ Dataset details retrieved")
        print(f"  - First row: {json.dumps(details['data'][0], indent=2)}")
    else:
        print(f"✗ Failed to get dataset details: {response.text}")
    
    # Create a template to test validation
    print("\n5. Creating a template for validation testing...")
    template_data = {
        "name": "City Services",
        "pattern": "[city] [service] Providers",
        "title_template": "[city] [service] - Find Top Providers",
        "meta_description_template": "Discover the best [service] providers in [city]. Compare options and get started today.",
        "h1_template": "[service] Providers in [city]"
    }
    
    response = requests.post(f"{BASE_URL}/api/projects/{project_id}/templates", json=template_data)
    if response.status_code == 200:
        template = response.json()
        template_id = template['id']
        print(f"✓ Template created: {template_id}")
        print(f"  - Variables: {template['variables']}")
    else:
        print(f"✗ Failed to create template: {response.text}")
        return
    
    # Validate dataset against template
    print("\n6. Validating dataset against template...")
    response = requests.post(
        f"{BASE_URL}/api/projects/{project_id}/data/{dataset_id}/validate",
        params={"template_id": template_id}
    )
    if response.status_code == 200:
        validation = response.json()
        print(f"✓ Validation complete")
        print(f"  - Is valid: {validation['is_valid']}")
        print(f"  - Missing columns: {validation['missing_columns']}")
        print(f"  - Warnings: {validation['warnings']}")
        print(f"  - Column mapping suggestions: {json.dumps(validation['column_mapping_suggestions'], indent=2)}")
    else:
        print(f"✗ Failed to validate dataset: {response.text}")
    
    # Clean up - delete the test project
    print("\n7. Cleaning up...")
    response = requests.delete(f"{BASE_URL}/api/projects/{project_id}")
    if response.status_code == 200:
        print("✓ Test project deleted")
    else:
        print(f"✗ Failed to delete project: {response.text}")
    
    print("\n" + "-" * 50)
    print("Data endpoint tests complete!")

if __name__ == "__main__":
    test_data_endpoints()