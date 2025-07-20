#!/usr/bin/env python3
"""
Test complete workflow end-to-end for Programmatic SEO Tool
"""

import requests
import json
import sys
import time
from typing import Dict, Any, List

# Use production backend
BACKEND_URL = "https://programmaticseotool-production.up.railway.app"

class WorkflowTester:
    def __init__(self):
        self.backend_url = BACKEND_URL
        self.project_id = None
        self.template_id = None
        self.errors = []
        self.warnings = []
        
    def log_error(self, step: str, error: str):
        """Log an error for reporting"""
        self.errors.append(f"{step}: {error}")
        print(f"❌ {step}: {error}")
        
    def log_warning(self, step: str, warning: str):
        """Log a warning for reporting"""
        self.warnings.append(f"{step}: {warning}")
        print(f"⚠️  {step}: {warning}")
        
    def test_business_analysis(self) -> bool:
        """Test Step 1: Business Analysis"""
        print("\n📊 Step 1: Business Analysis")
        print("-" * 40)
        
        try:
            # Test with a real business case
            business_data = {
                "business_input": "Real estate investment analysis platform that helps investors evaluate rental properties, calculate ROI, and make data-driven investment decisions across different cities and property types.",
                "input_type": "text"
            }
            
            response = requests.post(
                f"{self.backend_url}/api/analyze-business",
                json=business_data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                self.project_id = result.get('project_id')
                print(f"✅ Business analyzed successfully")
                print(f"   - Project ID: {self.project_id}")
                print(f"   - Business: {result.get('business_name', 'Unknown')}")
                print(f"   - Templates suggested: {len(result.get('template_opportunities', []))}")
                
                # Show template suggestions
                for i, template in enumerate(result.get('template_opportunities', [])[:3]):
                    print(f"   - Template {i+1}: {template.get('template_pattern', 'Unknown')}")
                
                return True
            else:
                self.log_error("Business Analysis", f"Failed with status {response.status_code}: {response.text[:200]}")
                return False
                
        except Exception as e:
            self.log_error("Business Analysis", str(e))
            return False
            
    def test_template_creation(self) -> bool:
        """Test Step 2: Template Creation"""
        print("\n🎨 Step 2: Template Creation")
        print("-" * 40)
        
        if not self.project_id:
            self.log_error("Template Creation", "No project ID available")
            return False
            
        try:
            # Create a template based on common pattern
            template_data = {
                "name": "City Property Investment Calculator",
                "pattern": "{City} {Property_Type} Investment Calculator",
                "title_template": "{Property_Type} Investment Calculator for {City} - ROI Analysis",
                "meta_description_template": "Calculate ROI for {Property_Type} investments in {City}. Free investment calculator with market data and rental income analysis.",
                "h1_template": "{City} {Property_Type} Investment Calculator",
                "content_sections": [
                    {
                        "type": "intro",
                        "content": "Comprehensive investment analysis for {Property_Type} properties in {City}"
                    },
                    {
                        "type": "calculator",
                        "content": "ROI calculation and market analysis tools"
                    }
                ]
            }
            
            response = requests.post(
                f"{self.backend_url}/api/projects/{self.project_id}/templates",
                json=template_data,
                timeout=30
            )
            
            if response.status_code in [200, 201]:
                result = response.json()
                self.template_id = result.get('id')
                print(f"✅ Template created successfully")
                print(f"   - Template ID: {self.template_id}")
                print(f"   - Pattern: {result.get('pattern', 'Unknown')}")
                print(f"   - Variables: {result.get('variables', [])}")
                return True
            else:
                self.log_error("Template Creation", f"Failed with status {response.status_code}: {response.text[:200]}")
                return False
                
        except Exception as e:
            self.log_error("Template Creation", str(e))
            return False
            
    def test_variable_generation(self) -> bool:
        """Test Step 3: AI Variable Generation"""
        print("\n🤖 Step 3: AI Variable Generation")
        print("-" * 40)
        
        if not self.project_id or not self.template_id:
            self.log_error("Variable Generation", "Missing project or template ID")
            return False
            
        try:
            response = requests.post(
                f"{self.backend_url}/api/projects/{self.project_id}/templates/{self.template_id}/generate-variables",
                json={},
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Variables generated successfully")
                print(f"   - Total combinations: {result.get('total_combinations', 0)}")
                
                # Show sample data
                variables_data = result.get('variables_data', {})
                for var_name, var_values in variables_data.items():
                    print(f"   - {var_name}: {len(var_values)} values")
                    if var_values:
                        print(f"     Sample: {var_values[0].get('value', 'Unknown')}")
                
                return True
            else:
                self.log_error("Variable Generation", f"Failed with status {response.status_code}: {response.text[:200]}")
                return False
                
        except Exception as e:
            self.log_error("Variable Generation", str(e))
            return False
            
    def test_page_preview(self) -> bool:
        """Test Step 4: Page Preview & Selection"""
        print("\n👁️  Step 4: Page Preview & Selection")
        print("-" * 40)
        
        if not self.project_id or not self.template_id:
            self.log_error("Page Preview", "Missing project or template ID")
            return False
            
        try:
            # First, generate potential pages
            print("   Generating potential pages...")
            response = requests.post(
                f"{self.backend_url}/api/projects/{self.project_id}/templates/{self.template_id}/generate-potential-pages",
                json={"max_combinations": 20},  # Limit for testing
                timeout=30
            )
            
            if response.status_code not in [200, 201]:
                self.log_error("Page Preview Generation", f"Failed with status {response.status_code}: {response.text[:200]}")
                return False
                
            generation_result = response.json()
            print(f"   ✅ Generated {generation_result.get('total_potential_pages', 0)} potential pages")
            
            # Now retrieve potential pages
            print("   Retrieving potential pages...")
            response = requests.get(
                f"{self.backend_url}/api/projects/{self.project_id}/templates/{self.template_id}/potential-pages",
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                potential_pages = result.get('potential_pages', [])
                print(f"✅ Page preview working")
                print(f"   - Total pages: {result.get('total_count', 0)}")
                print(f"   - Already generated: {result.get('generated_count', 0)}")
                print(f"   - Available to generate: {result.get('remaining_count', 0)}")
                
                # Show sample titles
                print("   Sample page titles:")
                for i, page in enumerate(potential_pages[:5]):
                    print(f"     {i+1}. {page.get('title', 'Unknown')}")
                
                return True
            else:
                self.log_error("Page Preview Retrieval", f"Failed with status {response.status_code}")
                return False
                
        except Exception as e:
            self.log_error("Page Preview", str(e))
            return False
            
    def test_page_generation(self) -> bool:
        """Test Step 5: Page Generation"""
        print("\n🚀 Step 5: Page Generation")
        print("-" * 40)
        
        if not self.project_id or not self.template_id:
            self.log_error("Page Generation", "Missing project or template ID")
            return False
            
        try:
            # Get potential pages first
            response = requests.get(
                f"{self.backend_url}/api/projects/{self.project_id}/templates/{self.template_id}/potential-pages?limit=3",
                timeout=30
            )
            
            if response.status_code != 200:
                self.log_error("Page Generation", "Cannot retrieve potential pages")
                return False
                
            potential_pages = response.json().get('potential_pages', [])
            if not potential_pages:
                self.log_warning("Page Generation", "No potential pages available")
                return False
                
            # Select first 2 pages for generation
            page_ids = [p['id'] for p in potential_pages[:2]]
            
            print(f"   Generating {len(page_ids)} pages...")
            response = requests.post(
                f"{self.backend_url}/api/projects/{self.project_id}/templates/{self.template_id}/generate-selected-pages",
                json={"page_ids": page_ids},
                timeout=120  # Longer timeout for AI generation
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Pages generated successfully")
                print(f"   - Requested: {result.get('total_requested', 0)}")
                print(f"   - Generated: {result.get('successful_generations', 0)}")
                
                # Show generated pages
                for page in result.get('generated_pages', []):
                    print(f"   - {page.get('title', 'Unknown')}")
                    print(f"     Word count: {page.get('word_count', 0)}")
                    print(f"     Quality score: {page.get('quality_score', 0)}")
                
                return result.get('successful_generations', 0) > 0
            else:
                self.log_error("Page Generation", f"Failed with status {response.status_code}: {response.text[:200]}")
                return False
                
        except Exception as e:
            self.log_error("Page Generation", str(e))
            return False
            
    def test_export(self) -> bool:
        """Test Step 6: Export Functionality"""
        print("\n📦 Step 6: Export Functionality")
        print("-" * 40)
        
        if not self.project_id:
            self.log_error("Export", "No project ID available")
            return False
            
        try:
            # Test CSV export
            export_data = {
                "format": "csv",
                "options": {}
            }
            
            response = requests.post(
                f"{self.backend_url}/api/projects/{self.project_id}/export",
                json=export_data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                export_id = result.get('export_id')
                print(f"✅ Export started successfully")
                print(f"   - Export ID: {export_id}")
                print(f"   - Format: CSV")
                
                # Check export status
                time.sleep(2)  # Wait for export to process
                status_response = requests.get(
                    f"{self.backend_url}/api/exports/{export_id}/status",
                    timeout=30
                )
                
                if status_response.status_code == 200:
                    status = status_response.json()
                    print(f"   - Status: {status.get('status', 'unknown')}")
                    print(f"   - Progress: {status.get('progress', 0)}%")
                    return True
                    
            else:
                self.log_error("Export", f"Failed with status {response.status_code}")
                return False
                
        except Exception as e:
            self.log_error("Export", str(e))
            return False
            
    def run_complete_workflow(self):
        """Run the complete workflow test"""
        print("🧪 Complete Workflow Test for Programmatic SEO Tool")
        print("=" * 60)
        print(f"🚂 Backend: {self.backend_url}")
        print("=" * 60)
        
        # Run all steps
        steps = [
            ("Business Analysis", self.test_business_analysis),
            ("Template Creation", self.test_template_creation),
            ("Variable Generation", self.test_variable_generation),
            ("Page Preview", self.test_page_preview),
            ("Page Generation", self.test_page_generation),
            ("Export", self.test_export)
        ]
        
        results = {}
        for step_name, test_func in steps:
            results[step_name] = test_func()
            if not results[step_name] and step_name in ["Business Analysis", "Template Creation"]:
                print(f"\n🛑 Critical step '{step_name}' failed. Stopping tests.")
                break
        
        # Summary
        print("\n" + "=" * 60)
        print("📊 WORKFLOW TEST SUMMARY")
        print("=" * 60)
        
        total_steps = len(results)
        passed_steps = sum(1 for passed in results.values() if passed)
        
        print(f"\n✅ Passed: {passed_steps}/{total_steps}")
        print(f"❌ Failed: {total_steps - passed_steps}/{total_steps}")
        
        # Show results
        print("\nStep Results:")
        for step, passed in results.items():
            status = "✅" if passed else "❌"
            print(f"  {status} {step}")
        
        # Show errors
        if self.errors:
            print(f"\n❌ Errors ({len(self.errors)}):")
            for error in self.errors:
                print(f"  - {error}")
        
        # Show warnings
        if self.warnings:
            print(f"\n⚠️  Warnings ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"  - {warning}")
        
        # Recommendations
        if self.errors:
            print("\n🔧 Recommendations:")
            if "Page Preview" in str(self.errors):
                print("  - Check if potential_pages table exists in production DB")
                print("  - Verify database migrations were applied")
            if "AI" in str(self.errors) or "Variable Generation" in str(self.errors):
                print("  - Verify AI API keys are set in Railway environment")
                print("  - Check AI provider rate limits")
            if "CORS" in str(self.errors):
                print("  - Update CORS configuration in backend")
                print("  - Verify frontend URL in environment variables")
        
        return passed_steps == total_steps

def main():
    """Run the complete workflow test"""
    tester = WorkflowTester()
    success = tester.run_complete_workflow()
    
    if success:
        print("\n🎉 All workflow steps passed!")
        print("🚀 The Programmatic SEO Tool is working correctly!")
    else:
        print("\n🛑 Some workflow steps failed.")
        print("📝 Please review the errors and recommendations above.")
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()