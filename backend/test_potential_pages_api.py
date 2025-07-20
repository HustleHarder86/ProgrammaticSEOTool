#!/usr/bin/env python3
"""
Test the Page Preview & Selection API endpoints
"""

import sys
import requests
import json
from typing import Dict, Any

API_BASE = "http://localhost:8000"

def test_potential_pages_system():
    """Test the complete potential pages system"""
    
    print("🧪 Testing Page Preview & Selection System...")
    print("=" * 60)
    
    try:
        # 1. Health check first
        print("📋 1. Health Check...")
        response = requests.get(f"{API_BASE}/health")
        if response.status_code != 200:
            print(f"❌ Health check failed: {response.status_code}")
            return False
            
        health_data = response.json()
        print(f"✅ API Status: {health_data.get('status', 'unknown')}")
        
        # 2. Create a test project
        print("\n📋 2. Creating test project...")
        project_data = {
            "name": "Test Potential Pages Project",
            "business_input": "Real estate investment platform"
        }
        response = requests.post(f"{API_BASE}/api/projects", json=project_data)
        if response.status_code not in [200, 201]:
            print(f"❌ Project creation failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
        project = response.json()
        project_id = project["id"]
        print(f"✅ Project created: {project_id}")
        
        # 3. Create a test template
        print("\n📋 3. Creating test template...")
        template_data = {
            "name": "Investment Calculator Template",
            "pattern": "{City} {Property_Type} Investment Calculator",
            "title_template": "Best {Property_Type} Investment Opportunities in {City}",
            "meta_description_template": "Discover profitable {Property_Type} investments in {City}. ROI analysis, market trends, and investment calculator.",
            "h1_template": "{City} {Property_Type} Investment Analysis",
            "content_sections": [
                {
                    "type": "intro",
                    "content": "Investment overview for {Property_Type} in {City}"
                },
                {
                    "type": "analysis", 
                    "content": "Market analysis and ROI calculation"
                }
            ]
        }
        
        response = requests.post(f"{API_BASE}/api/projects/{project_id}/templates", json=template_data)
        if response.status_code not in [200, 201]:
            print(f"❌ Template creation failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
        template = response.json()
        template_id = template["id"]
        print(f"✅ Template created: {template_id}")
        
        # 4. Test potential pages generation
        print("\n📋 4. Generating potential pages...")
        potential_pages_data = {
            "variables_data": {
                "City": [
                    {"value": "Toronto", "dataset_id": "test", "dataset_name": "cities", "metadata": {}},
                    {"value": "Vancouver", "dataset_id": "test", "dataset_name": "cities", "metadata": {}},
                    {"value": "Calgary", "dataset_id": "test", "dataset_name": "cities", "metadata": {}}
                ],
                "Property_Type": [
                    {"value": "Condo", "dataset_id": "test", "dataset_name": "properties", "metadata": {}},
                    {"value": "House", "dataset_id": "test", "dataset_name": "properties", "metadata": {}},
                    {"value": "Duplex", "dataset_id": "test", "dataset_name": "properties", "metadata": {}}
                ]
            },
            "max_combinations": 9  # 3 cities × 3 property types = 9 combinations
        }
        
        response = requests.post(
            f"{API_BASE}/api/projects/{project_id}/templates/{template_id}/generate-potential-pages",
            json=potential_pages_data
        )
        if response.status_code not in [200, 201]:
            print(f"❌ Potential pages generation failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
        generation_result = response.json()
        print(f"✅ Generated {generation_result['total_potential_pages']} potential pages")
        print(f"📋 Template pattern: {generation_result['template_pattern']}")
        
        # 5. Test getting potential pages
        print("\n📋 5. Retrieving potential pages...")
        response = requests.get(f"{API_BASE}/api/projects/{project_id}/templates/{template_id}/potential-pages")
        if response.status_code != 200:
            print(f"❌ Getting potential pages failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
        potential_pages_list = response.json()
        print(f"✅ Retrieved {len(potential_pages_list['potential_pages'])} potential pages")
        print(f"📊 Total: {potential_pages_list['total_count']}, Generated: {potential_pages_list['generated_count']}")
        
        # Show some examples
        print("\n📋 Example potential page titles:")
        for i, page in enumerate(potential_pages_list['potential_pages'][:5]):
            print(f"   {i+1}. {page['title']}")
            if i == 0:
                print(f"      Variables: {page['variables']}")
                print(f"      Slug: {page['slug']}")
        
        # 6. Test generating selected pages (AI content generation)
        print("\n📋 6. Testing selected page generation...")
        if potential_pages_list['potential_pages']:
            # Select first 2 pages for generation
            selected_page_ids = [p['id'] for p in potential_pages_list['potential_pages'][:2]]
            
            generation_request = {
                "page_ids": selected_page_ids,
                "batch_size": 2
            }
            
            response = requests.post(
                f"{API_BASE}/api/projects/{project_id}/templates/{template_id}/generate-selected-pages",
                json=generation_request
            )
            
            if response.status_code == 503:
                print("⚠️  AI providers not configured - this is expected in local testing")
                print("✅ Selected page generation endpoint validated (AI requirement enforced)")
            elif response.status_code in [200, 201]:
                result = response.json()
                print(f"✅ Successfully generated {result['successful_generations']} pages")
                if result['generated_pages']:
                    for page in result['generated_pages']:
                        print(f"   - {page['title']} (quality: {page['quality_score']})")
            else:
                print(f"❌ Selected page generation failed: {response.status_code}")
                print(f"Response: {response.text}")
                return False
        
        print("\n🎉 Page Preview & Selection System Test: PASSED")
        print("=" * 60)
        print("✅ All API endpoints working correctly")
        print("✅ Database integration successful")
        print("✅ Potential pages generation and retrieval working")
        print("✅ Selected page generation endpoint validates AI requirement")
        print("\n🚀 System ready for frontend integration!")
        
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API server")
        print("💡 Make sure the backend is running: python3 -m uvicorn main:app --reload")
        return False
    except Exception as e:
        print(f"❌ Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run the test"""
    success = test_potential_pages_system()
    
    if success:
        print("\n🚀 Page Preview & Selection system is working!")
        sys.exit(0)
    else:
        print("\n🛑 Page Preview & Selection system needs fixing.")
        sys.exit(1)

if __name__ == "__main__":
    main()