"""Test CSV upload functionality"""
import requests
import json

# Base URL for local testing
BASE_URL = "http://localhost:8000"

def test_csv_upload():
    """Test CSV file upload"""
    
    print("Testing CSV Upload...")
    print("-" * 50)
    
    # First, create a test project
    print("\n1. Creating a test project...")
    project_data = {
        "name": "CSV Upload Test Project",
        "business_input": "Testing CSV upload",
        "business_analysis": {
            "business_name": "Test Business",
            "business_description": "Testing CSV upload functionality"
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
    
    # Upload CSV file
    print("\n2. Uploading CSV file...")
    with open("test_data.csv", "rb") as f:
        files = {"file": ("test_data.csv", f, "text/csv")}
        response = requests.post(
            f"{BASE_URL}/api/projects/{project_id}/data/upload",
            files=files
        )
    
    if response.status_code == 200:
        result = response.json()
        print(f"✓ CSV uploaded successfully")
        print(f"  - Dataset ID: {result['dataset_id']}")
        print(f"  - Name: {result['name']}")
        print(f"  - Rows: {result['row_count']}")
        print(f"  - Columns: {result['columns']}")
        print(f"  - Validation: {json.dumps(result['validation'], indent=2)}")
    else:
        print(f"✗ Failed to upload CSV: {response.text}")
        return
    
    # Clean up
    print("\n3. Cleaning up...")
    response = requests.delete(f"{BASE_URL}/api/projects/{project_id}")
    if response.status_code == 200:
        print("✓ Test project deleted")
    else:
        print(f"✗ Failed to delete project: {response.text}")
    
    print("\n" + "-" * 50)
    print("CSV upload test complete!")

if __name__ == "__main__":
    test_csv_upload()