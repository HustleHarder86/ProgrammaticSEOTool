"""Test script for API integration endpoints"""
import asyncio
import aiohttp
import json
from datetime import datetime

BASE_URL = "http://localhost:8000/api"

async def test_workflow():
    """Test the complete workflow"""
    async with aiohttp.ClientSession() as session:
        
        # Step 1: Test business analysis
        print("\n1. Testing Business Analysis...")
        business_data = {
            "input_type": "text",
            "content": "We are a digital marketing agency specializing in SEO, content marketing, and PPC advertising for small businesses in major US cities.",
            "market_context": {
                "location": "United States",
                "industry": "Digital Marketing"
            }
        }
        
        async with session.post(f"{BASE_URL}/analyze-business-templates", json=business_data) as resp:
            if resp.status == 200:
                result = await resp.json()
                print(f"✓ Business analyzed: {result['business_analysis']['business_name']}")
                print(f"  - Industry: {result['business_analysis']['industry']}")
                print(f"  - Suggested templates: {result['total_templates']}")
                
                # Show first template
                if result['suggested_templates']:
                    first_template = result['suggested_templates'][0]
                    print(f"  - Top template: {first_template['template']['name']}")
                    print(f"    Pattern: {first_template['template']['pattern']}")
            else:
                print(f"✗ Business analysis failed: {resp.status}")
                return
        
        # Step 2: Test template creation
        print("\n2. Testing Template Creation...")
        template_data = {
            "business_analysis": result['business_analysis'],
            "template_pattern": "{city} {service} Agency",
            "template_name": "City Service Agency Template",
            "custom_variables": ["city", "service", "specialization"]
        }
        
        async with session.post(f"{BASE_URL}/create-template", json=template_data) as resp:
            if resp.status == 200:
                template_result = await resp.json()
                template_id = template_result['template_id']
                print(f"✓ Template created: {template_id}")
            else:
                print(f"✗ Template creation failed: {resp.status}")
                return
        
        # Step 3: Test template validation
        print("\n3. Testing Template Validation...")
        validation_data = {
            "template_id": template_id,
            "sample_data": {
                "city": "New York",
                "service": "SEO",
                "specialization": "Local Business"
            }
        }
        
        async with session.post(f"{BASE_URL}/validate-template", json=validation_data) as resp:
            if resp.status == 200:
                validation_result = await resp.json()
                print(f"✓ Template validation: {'Valid' if validation_result['valid'] else 'Invalid'}")
                if validation_result.get('preview'):
                    print(f"  - Preview URL: {validation_result['preview']['url']}")
            else:
                print(f"✗ Template validation failed: {resp.status}")
        
        # Step 4: Test data import
        print("\n4. Testing Data Import...")
        import_data = {
            "data_json": [
                {"city": "New York", "service": "SEO", "specialization": "E-commerce"},
                {"city": "Los Angeles", "service": "PPC", "specialization": "Local Business"},
                {"city": "Chicago", "service": "Content Marketing", "specialization": "B2B"},
                {"city": "Houston", "service": "SEO", "specialization": "Healthcare"},
                {"city": "Phoenix", "service": "Social Media", "specialization": "Restaurants"}
            ],
            "data_type": "location_service"
        }
        
        async with session.post(f"{BASE_URL}/import-data", json=import_data) as resp:
            if resp.status == 200:
                import_result = await resp.json()
                data_set_id = import_result['data_set_id']
                print(f"✓ Data imported: {import_result['total_records']} records")
                print(f"  - Data set ID: {data_set_id}")
            else:
                print(f"✗ Data import failed: {resp.status}")
                return
        
        # Step 5: Test page generation
        print("\n5. Testing Page Generation...")
        generation_data = {
            "template_id": template_id,
            "data_set_id": data_set_id,
            "limit": 5,
            "enable_variations": True,
            "internal_linking": True,
            "ai_enhancement": True
        }
        
        async with session.post(f"{BASE_URL}/generate-pages-bulk", json=generation_data) as resp:
            if resp.status == 200:
                generation_result = await resp.json()
                print(f"✓ Pages generated: {generation_result['generated_pages']}")
                print(f"  - Unique pages: {generation_result['unique_pages']}")
                print(f"  - Variations: {generation_result['variations_created']}")
                print(f"  - Internal links: {generation_result['internal_links_added']}")
                page_ids = generation_result['page_ids']
            else:
                print(f"✗ Page generation failed: {resp.status}")
                error = await resp.text()
                print(f"  Error: {error}")
                return
        
        # Step 6: Test export
        print("\n6. Testing Export...")
        export_data = {
            "page_ids": page_ids[:3],  # Export first 3 pages
            "formats": ["csv", "json"],
            "compression": False
        }
        
        async with session.post(f"{BASE_URL}/export-content", json=export_data) as resp:
            if resp.status == 200:
                export_result = await resp.json()
                print(f"✓ Content exported:")
                print(f"  - Export ID: {export_result['export_id']}")
                print(f"  - Formats: {', '.join(export_result['formats_exported'])}")
                print(f"  - Files: {len(export_result['file_paths'])}")
            else:
                print(f"✗ Export failed: {resp.status}")

async def test_complete_workflow():
    """Test the complete workflow endpoint"""
    async with aiohttp.ClientSession() as session:
        print("\n\nTesting Complete Workflow Endpoint...")
        
        workflow_data = {
            "business_input": {
                "input_type": "text",
                "content": "Online fitness coaching platform offering personalized workout plans and nutrition guidance"
            },
            "template_selection": "{city} {service} Online",
            "data_source": {
                "data_json": [
                    {"city": "Austin", "service": "Fitness Coaching"},
                    {"city": "Denver", "service": "Personal Training"},
                    {"city": "Seattle", "service": "Nutrition Coaching"}
                ],
                "data_type": "location_service"
            },
            "generation_config": {
                "limit": 3,
                "enable_variations": True
            },
            "export_config": {
                "formats": ["csv", "json"],
                "compression": True
            }
        }
        
        # Start workflow
        async with session.post(f"{BASE_URL}/complete-workflow", json=workflow_data) as resp:
            if resp.status == 200:
                start_result = await resp.json()
                workflow_id = start_result['workflow_id']
                print(f"✓ Workflow started: {workflow_id}")
                
                # Poll for status
                for i in range(30):  # Poll for up to 30 seconds
                    await asyncio.sleep(1)
                    
                    async with session.get(f"{BASE_URL}/workflow-status/{workflow_id}") as status_resp:
                        if status_resp.status == 200:
                            status = await status_resp.json()
                            print(f"  Status: {status['status']} - {status['current_step']} ({status['progress']*100:.0f}%)")
                            
                            if status['status'] == 'completed':
                                print("\n✓ Workflow completed successfully!")
                                print(f"  - Business analyzed")
                                print(f"  - Template created")
                                print(f"  - Data imported") 
                                print(f"  - Pages generated: {status['result']['pages_generated']['generated_pages']}")
                                print(f"  - Content exported")
                                break
                            elif status['status'] == 'failed':
                                print(f"\n✗ Workflow failed: {status['error']}")
                                break
            else:
                print(f"✗ Failed to start workflow: {resp.status}")

async def test_utility_endpoints():
    """Test utility endpoints"""
    async with aiohttp.ClientSession() as session:
        print("\n\nTesting Utility Endpoints...")
        
        # Test supported formats
        async with session.get(f"{BASE_URL}/supported-formats") as resp:
            if resp.status == 200:
                formats = await resp.json()
                print(f"✓ Supported export formats: {len(formats['formats'])}")
                for fmt, desc in list(formats['formats'].items())[:3]:
                    print(f"  - {fmt}: {desc}")
        
        # Test template library
        async with session.get(f"{BASE_URL}/template-library") as resp:
            if resp.status == 200:
                library = await resp.json()
                print(f"\n✓ Template library: {library['total']} templates")
                for name, template in list(library['templates'].items())[:3]:
                    print(f"  - {name}: {template['description']}")
        
        # Test AI connection
        async with session.post(f"{BASE_URL}/test-ai-connection") as resp:
            if resp.status == 200:
                ai_test = await resp.json()
                if ai_test['connected']:
                    print(f"\n✓ AI Provider connected: {ai_test['provider']}")
                else:
                    print(f"\n✗ AI Provider not connected: {ai_test['error']}")

async def main():
    """Run all tests"""
    print("=" * 60)
    print("API Integration Test Suite")
    print("=" * 60)
    
    # Test individual endpoints
    await test_workflow()
    
    # Test complete workflow
    await test_complete_workflow()
    
    # Test utility endpoints
    await test_utility_endpoints()
    
    print("\n" + "=" * 60)
    print("Tests completed!")

if __name__ == "__main__":
    asyncio.run(main())