#!/usr/bin/env python3
"""
Test script to diagnose and fix export functionality issues
"""
import requests
import json
import time
import os

# Configuration
API_BASE_URL = os.getenv('API_BASE_URL', 'https://programmaticseotool-production.up.railway.app')

def test_export_with_existing_project():
    """Test export with an existing project that has pages"""
    print("=== Testing Export Functionality ===\n")
    
    # First, get a list of projects to find one with pages
    print("1. Getting list of projects...")
    response = requests.get(f"{API_BASE_URL}/api/projects")
    if response.status_code != 200:
        print(f"❌ Failed to get projects: {response.status_code}")
        return
    
    projects = response.json()
    print(f"✅ Found {len(projects)} projects")
    
    # Find a project with pages
    project_with_pages = None
    for project in projects:
        # Get pages for this project
        pages_response = requests.get(f"{API_BASE_URL}/api/projects/{project['id']}/pages")
        if pages_response.status_code == 200:
            pages = pages_response.json()
            if len(pages) > 0:
                project_with_pages = project
                print(f"✅ Found project '{project['name']}' with {len(pages)} pages")
                break
    
    if not project_with_pages:
        print("❌ No projects with pages found. Please generate some pages first.")
        return
    
    # Test CSV export
    print(f"\n2. Starting CSV export for project '{project_with_pages['name']}'...")
    export_data = {
        "format": "csv",
        "options": {
            "include_metadata": True
        }
    }
    
    response = requests.post(
        f"{API_BASE_URL}/api/projects/{project_with_pages['id']}/export",
        json=export_data
    )
    
    if response.status_code != 200:
        print(f"❌ Failed to start export: {response.status_code}")
        print(f"   Response: {response.text}")
        return
    
    export_result = response.json()
    export_id = export_result.get('export_id')
    print(f"✅ Export started with ID: {export_id}")
    
    # Poll for export status
    print("\n3. Checking export status...")
    max_attempts = 10
    for attempt in range(max_attempts):
        time.sleep(2)  # Wait 2 seconds between checks
        
        status_response = requests.get(f"{API_BASE_URL}/api/exports/{export_id}/status")
        if status_response.status_code != 200:
            print(f"❌ Failed to get export status: {status_response.status_code}")
            continue
        
        status_data = status_response.json()
        print(f"   Status: {status_data.get('status')} - Progress: {status_data.get('progress')}%")
        
        if status_data.get('status') == 'completed':
            print("✅ Export completed successfully!")
            
            # Try to download
            print("\n4. Attempting to download export...")
            download_response = requests.get(f"{API_BASE_URL}/api/exports/{export_id}/download")
            if download_response.status_code == 200:
                print("✅ Export file is downloadable")
                # Save first few lines as preview
                content = download_response.text
                lines = content.split('\n')[:5]
                print("\nPreview of exported CSV:")
                for line in lines:
                    print(f"   {line}")
            else:
                print(f"❌ Failed to download: {download_response.status_code}")
            break
            
        elif status_data.get('status') == 'failed':
            print(f"❌ Export failed: {status_data.get('error_message')}")
            break
    else:
        print("❌ Export timed out")

def test_export_directory():
    """Test if export directory is writable"""
    print("\n=== Testing Export Directory ===")
    
    # This would need to be run on the server
    print("Note: Directory write test needs to be run on the Railway server")
    print("The export directory should be: /backend/data/exports")
    print("Make sure this directory exists and is writable")

if __name__ == "__main__":
    # Test with Railway backend
    print(f"Testing with API: {API_BASE_URL}\n")
    
    test_export_with_existing_project()
    test_export_directory()
    
    print("\n=== Export Test Complete ===")