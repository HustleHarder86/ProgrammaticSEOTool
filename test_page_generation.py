#!/usr/bin/env python3
"""
Test script for page generation with a new project and template.
Tests the complete flow from business analysis to page generation.
"""

import requests
import json
import time
import sys
from datetime import datetime

# API Configuration
API_BASE_URL = "http://localhost:8000"  # Change to your API URL
HEADERS = {"Content-Type": "application/json"}

# Test business details
TEST_BUSINESS = {
    "business_input": "AI Writing Assistant for Content Creators - An AI-powered tool that helps bloggers, marketers, and writers create high-quality content faster. Features include blog post generation, email templates, social media captions, and SEO optimization."
}

def print_section(title):
    """Print a formatted section header."""
    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}\n")

def print_success(message):
    """Print success message in green."""
    print(f"✅ {message}")

def print_error(message):
    """Print error message in red."""
    print(f"❌ {message}")

def print_info(message):
    """Print info message."""
    print(f"ℹ️  {message}")

def make_request(method, endpoint, data=None):
    """Make API request with error handling."""
    url = f"{API_BASE_URL}{endpoint}"
    try:
        if method == "GET":
            response = requests.get(url, headers=HEADERS)
        elif method == "POST":
            response = requests.post(url, headers=HEADERS, json=data)
        else:
            raise ValueError(f"Unsupported method: {method}")
        
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print_error(f"Request failed: {e}")
        if hasattr(e.response, 'text'):
            print_error(f"Response: {e.response.text}")
        return None

def test_health_check():
    """Test if the API is running."""
    print_section("Testing API Health")
    result = make_request("GET", "/health")
    if result:
        print_success(f"API is healthy: {result}")
        return True
    else:
        print_error("API health check failed")
        return False

def test_business_analysis():
    """Test business analysis endpoint."""
    print_section("Testing Business Analysis")
    print_info(f"Analyzing business: {TEST_BUSINESS['business_input'][:50]}...")
    
    result = make_request("POST", "/api/analyze-business", TEST_BUSINESS)
    if result and result.get("project_id"):
        print_success("Business analysis successful")
        print_info(f"Project ID: {result['project_id']}")
        print_info(f"Business Name: {result.get('business_name', 'Unknown')}")
        print_info(f"Target Audience: {result.get('target_audience', 'Unknown')}")
        
        # Build analysis dict from flat response
        analysis = {
            'business_type': result.get('business_name', ''),
            'business_name': result.get('business_name', ''),
            'business_description': result.get('business_description', ''),
            'target_audience': result.get('target_audience', ''),
            'core_offerings': result.get('core_offerings', []),
            'template_opportunities': result.get('template_opportunities', [])
        }
        
        # Display template opportunities
        if result.get('template_opportunities'):
            print_info("\nTemplate Opportunities:")
            for opp in result['template_opportunities'][:3]:
                print(f"  - {opp.get('template_name', 'Unknown')}: {opp.get('template_pattern', 'No pattern')}")
        
        return result['project_id'], analysis
    else:
        print_error("Business analysis failed")
        if result:
            print_error(f"Error details: {result}")
        return None, None

def test_template_creation(project_id):
    """Test template creation with a unique pattern."""
    print_section("Testing Template Creation")
    
    template_data = {
        "name": "AI Writing Tools Comparison",
        "pattern": "Best AI Writing Tools for {content_type} in {year}",
        "template_type": "comparison",
        "title_template": "Best AI Writing Tools for {content_type} in {year}",
        "meta_description_template": "Compare top AI writing assistants for {content_type}. Find the perfect tool for your {content_type} needs in {year}.",
        "h1_template": "Best AI Writing Tools for {content_type} in {year}",
        "content_sections": [
            {
                "type": "intro",
                "content": "Creating high-quality {content_type} has never been easier with AI writing assistants. Whether you're a professional writer or just getting started, these tools can help you produce better {content_type} faster."
            },
            {
                "type": "benefits",
                "title": "Why Use AI for {content_type}?",
                "content": "AI writing tools have revolutionized how we create {content_type}. They offer faster content creation, consistent quality and tone, SEO optimization features, and multiple language support."
            },
            {
                "type": "features",
                "title": "Top Features for {content_type} Creation",
                "content": "When choosing an AI writing tool for {content_type}, consider these essential features: template libraries specific to {content_type}, tone and style customization, grammar and spell checking, and plagiarism detection."
            },
            {
                "type": "cta",
                "title": "Getting Started with AI {content_type} Writing",
                "content": "Start creating professional {content_type} today with these AI-powered tools. Most offer free trials, so you can test them before committing."
            }
        ]
    }
    
    print_info("Creating template with variables: content_type, year")
    result = make_request("POST", f"/api/projects/{project_id}/templates", template_data)
    
    if result and (result.get("success") or result.get("id")):
        # Handle both response formats
        if result.get("success"):
            template_id = result['template']['id']
            variables = result['template']['variables']
        else:
            template_id = result.get('id')
            variables = result.get('variables', [])
        
        print_success("Template created successfully")
        print_info(f"Template ID: {template_id}")
        print_info(f"Variables: {', '.join(variables)}")
        return template_id, variables
    else:
        print_error("Template creation failed")
        if result:
            print_error(f"Error details: {result}")
        return None, None

def test_ai_variable_generation(project_id, template_id, variables):
    """Test AI-powered variable generation."""
    print_section("Testing AI Variable Generation")
    
    generation_data = {
        "variables": {}
    }
    
    # Request AI to generate values for each variable
    for var in variables:
        generation_data["variables"][var] = {
            "generate_count": 5 if var == "content_type" else 3
        }
    
    print_info(f"Requesting AI generation for variables: {', '.join(variables)}")
    result = make_request("POST", f"/api/projects/{project_id}/templates/{template_id}/generate-variables", generation_data)
    
    if result and (result.get("success") or result.get("generated") or result.get("variables")):
        print_success("AI variable generation successful")
        
        # Handle different response formats
        if result.get('generated'):
            generated = result.get('generated', {})
        elif result.get('variables'):
            generated = result.get('variables', {})
        else:
            generated = {}
        
        for var, values in generated.items():
            if isinstance(values, list):
                print_info(f"{var}: {', '.join(str(v) for v in values[:3])}{'...' if len(values) > 3 else ''}")
        
        # Also check for titles in the response
        if result.get('titles'):
            print_info(f"Generated {len(result['titles'])} title combinations")
        
        return result  # Return the full response
    else:
        print_error("AI variable generation failed")
        if result:
            print_error(f"Error details: {result}")
        return None

def test_page_generation(project_id, template_id, variables, ai_response=None):
    """Test page generation with the template and variables."""
    print_section("Testing Page Generation")
    
    # Format variables for the API
    formatted_variables = {}
    if isinstance(variables, dict):
        for var, values in variables.items():
            formatted_variables[var] = values if isinstance(values, list) else [values]
    
    # If we have AI response with titles, use those
    selected_titles = []
    if ai_response and ai_response.get('titles'):
        # Select first 10 titles for testing
        selected_titles = ai_response['titles'][:10]
        print_info(f"Using {len(selected_titles)} AI-generated titles")
    
    generation_data = {
        "batch_size": 100,
        "variables_data": formatted_variables,
        "selected_titles": selected_titles
    }
    
    print_info(f"Generating pages with variables: {list(formatted_variables.keys())}")
    result = make_request("POST", f"/api/projects/{project_id}/templates/{template_id}/generate", generation_data)
    
    if result and "total_generated" in result:
        print_success(f"Generated {result['total_generated']} pages successfully")
        print_info(f"Status: {result.get('status', 'Unknown')}")
        
        # Get sample pages
        if result.get('page_ids'):
            sample_pages_result = make_request("GET", f"/api/projects/{project_id}/pages?limit=3")
            if sample_pages_result and sample_pages_result.get('pages'):
                print_info("\nSample generated pages:")
                for i, page in enumerate(sample_pages_result['pages'][:3]):
                    print(f"\n  Page {i+1}:")
                    print(f"  - Title: {page.get('title', 'No title')}")
                    print(f"  - URL: {page.get('url', page.get('slug', 'No URL'))}")
                    if page.get('meta_description'):
                        print(f"  - Meta: {page['meta_description'][:80]}...")
        
        return result['total_generated']
    else:
        print_error("Page generation failed")
        if result:
            print_error(f"Error details: {result}")
        return None

def test_export(project_id):
    """Test exporting generated pages."""
    print_section("Testing Export")
    
    export_data = {
        "format": "csv",
        "include_content": True
    }
    
    print_info("Exporting pages as CSV...")
    result = make_request("POST", f"/api/projects/{project_id}/export", export_data)
    
    if result and (result.get("success") or result.get("export_path") or result.get("data") or result.get("export_id")):
        print_success("Export initiated successfully")
        
        # Handle async export
        if result.get('export_id'):
            print_info(f"Export ID: {result['export_id']}")
            print_info(f"Status: {result.get('status', 'Unknown')}")
            print_info(f"Message: {result.get('message', 'Export started')}")
            
            # Check export status
            time.sleep(2)  # Wait a bit for export to complete
            status_result = make_request("GET", f"/api/exports/{result['export_id']}/status")
            if status_result:
                print_info(f"Export status: {status_result.get('status', 'Unknown')}")
                if status_result.get('download_url'):
                    print_success(f"Download URL: {status_result['download_url']}")
                elif status_result.get('export_path'):
                    print_success(f"Export saved to: {status_result['export_path']}")
        else:
            # Handle synchronous export
            print_info(f"Export format: {result.get('format', 'csv')}")
            print_info(f"Pages exported: {result.get('page_count', result.get('pages_exported', 0))}")
            
            # Save CSV data to file if available
            if result.get('download_url'):
                print_info(f"Download URL: {result['download_url']}")
            elif result.get('export_path'):
                print_info(f"Export saved to: {result['export_path']}")
            elif result.get('data'):
                filename = f"test_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(result['data'])
                print_success(f"Exported data saved to: {filename}")
        
        return True
    else:
        print_error("Export failed")
        if result:
            print_error(f"Error details: {result}")
        return False

def run_full_test():
    """Run the complete test flow."""
    print_section("Starting Full Page Generation Test")
    print_info(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Step 1: Health check
    if not test_health_check():
        print_error("API is not running. Please start the server first.")
        return False
    
    # Step 2: Business analysis
    project_id, analysis = test_business_analysis()
    if not project_id:
        return False
    
    # Step 3: Template creation
    template_id, variables = test_template_creation(project_id)
    if not template_id:
        return False
    
    # Step 4: AI variable generation
    ai_response = test_ai_variable_generation(project_id, template_id, variables)
    if ai_response and ai_response.get('variables'):
        generated_variables = ai_response.get('variables', {})
    else:
        # Fallback to manual variables for testing
        print_info("Using manual variables as fallback...")
        generated_variables = {
            "content_type": ["Blog Posts", "Email Campaigns", "Social Media Posts", "Product Descriptions", "Landing Pages"],
            "year": ["2024", "2025", "2026"]
        }
        ai_response = None
    
    # Step 5: Page generation
    pages_generated = test_page_generation(project_id, template_id, generated_variables, ai_response)
    if not pages_generated:
        return False
    
    # Step 6: Export
    export_success = test_export(project_id)
    
    # Summary
    print_section("Test Summary")
    print_success(f"Test completed successfully!")
    print_info(f"Project ID: {project_id}")
    print_info(f"Template ID: {template_id}")
    print_info(f"Pages Generated: {pages_generated}")
    print_info(f"Export Status: {'Success' if export_success else 'Failed'}")
    
    return True

def test_edge_cases():
    """Test edge cases and error scenarios."""
    print_section("Testing Edge Cases")
    
    # Test 1: Empty business text
    print_info("Test 1: Empty business text")
    result = make_request("POST", "/api/analyze-business", {"business_input": ""})
    if result and not result.get("success"):
        print_success("Correctly rejected empty business text")
    else:
        print_error("Failed to reject empty business text")
    
    # Test 2: Invalid project ID
    print_info("Test 2: Template creation with invalid project ID")
    template_data = {
        "name": "Test Template",
        "pattern": "Test {var}",
        "template_type": "test"
    }
    result = make_request("POST", "/api/projects/invalid-project-id/templates", template_data)
    if not result or (result and not result.get("success")):
        print_success("Correctly rejected invalid project ID")
    else:
        print_error("Failed to reject invalid project ID")
    
    # Test 3: Empty template pattern
    print_info("Test 3: Template with empty pattern")
    template_data = {
        "name": "Empty Pattern Template",
        "pattern": "",
        "template_type": "test"
    }
    # Create a project first
    project_result = make_request("POST", "/api/analyze-business", 
                                {"business_input": "Test business for edge cases"})
    if project_result and project_result.get("project_id"):
        result = make_request("POST", f"/api/projects/{project_result['project_id']}/templates", template_data)
        if not result or (result and not result.get("success")):
            print_success("Correctly rejected empty pattern")
        else:
            print_error("Failed to reject empty pattern")
    
    print_success("Edge case testing completed")

if __name__ == "__main__":
    # Check if API URL is provided as argument
    if len(sys.argv) > 1:
        API_BASE_URL = sys.argv[1]
    
    print(f"Using API URL: {API_BASE_URL}")
    
    # Run the full test
    success = run_full_test()
    
    # Optionally run edge case tests
    if success:
        print("\nDo you want to run edge case tests? (y/n): ", end="")
        try:
            if input().lower() == 'y':
                test_edge_cases()
        except EOFError:
            print("\nSkipping edge case tests")
    
    print("\n" + "="*60)
    print("Test completed!")
    print("="*60)