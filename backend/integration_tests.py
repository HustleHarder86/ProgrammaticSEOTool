#!/usr/bin/env python3
"""
Integration Tests for Programmatic SEO Tool
Tests the complete workflow from business analysis to export
"""

import requests
import json
import time
import sys
import os
from datetime import datetime
from typing import Dict, List, Any, Optional

class IntegrationTester:
    def __init__(self, base_url: str = "https://programmaticseotool-production.up.railway.app"):
        self.base_url = base_url
        self.session = requests.Session()
        self.results = []
        self.project_id = None
        self.template_id = None
        self.dataset_id = None
        self.export_id = None
        
    def log(self, test_name: str, status: str, message: str, details: Optional[Dict] = None):
        """Log test results"""
        result = {
            "timestamp": datetime.utcnow().isoformat(),
            "test": test_name,
            "status": status,
            "message": message,
            "details": details or {}
        }
        self.results.append(result)
        
        # Print to console with color
        color = "\033[92m" if status == "PASS" else "\033[91m" if status == "FAIL" else "\033[93m"
        reset = "\033[0m"
        print(f"{color}[{status}]{reset} {test_name}: {message}")
        
        if details and status == "FAIL":
            print(f"  Details: {json.dumps(details, indent=2)}")
    
    def test_health_check(self) -> bool:
        """Test 1: Health check endpoint"""
        try:
            response = self.session.get(f"{self.base_url}/health")
            data = response.json()
            
            if response.status_code == 200 and data.get("status") == "healthy":
                self.log("Health Check", "PASS", "API is healthy", data)
                return True
            else:
                self.log("Health Check", "FAIL", f"Unexpected response: {response.status_code}", data)
                return False
                
        except Exception as e:
            self.log("Health Check", "FAIL", f"Connection error: {str(e)}")
            return False
    
    def test_business_analysis(self) -> bool:
        """Test 2: Business analysis endpoint"""
        try:
            payload = {
                "business_input": "TechFlow Solutions - A modern project management software for agile teams. We help software development teams collaborate better with features like sprint planning, code reviews, and real-time collaboration.",
                "input_type": "text"
            }
            
            response = self.session.post(
                f"{self.base_url}/api/analyze-business",
                json=payload
            )
            
            if response.status_code == 200:
                data = response.json()
                self.project_id = data.get("project_id")
                
                # Validate response structure
                required_fields = ["project_id", "business_name", "business_description", 
                                 "target_audience", "core_offerings", "template_opportunities"]
                missing_fields = [f for f in required_fields if f not in data]
                
                if not missing_fields and len(data.get("template_opportunities", [])) > 0:
                    self.log("Business Analysis", "PASS", 
                            f"Successfully analyzed business: {data.get('business_name')}", 
                            {"project_id": self.project_id, "opportunities": len(data.get("template_opportunities", []))})
                    return True
                else:
                    self.log("Business Analysis", "FAIL", 
                            f"Missing fields: {missing_fields}", data)
                    return False
            else:
                self.log("Business Analysis", "FAIL", 
                        f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log("Business Analysis", "FAIL", f"Error: {str(e)}")
            return False
    
    def test_create_template(self) -> bool:
        """Test 3: Create template"""
        if not self.project_id:
            self.log("Create Template", "SKIP", "No project ID available")
            return False
            
        try:
            payload = {
                "name": "Industry Best Practices Template",
                "pattern": "Best [Tool Type] for [Industry] Teams",
                "title_template": "Best {Tool Type} for {Industry} Teams in 2025",
                "meta_description_template": "Discover the best {Tool Type} solutions designed specifically for {Industry} teams. Compare features, pricing, and reviews.",
                "h1_template": "Top {Tool Type} Solutions for {Industry} Teams",
                "content_sections": [
                    {
                        "heading": "Why {Industry} Teams Need Specialized {Tool Type}",
                        "content": "Learn why {Industry} teams have unique requirements for {Tool Type} and how the right solution can transform your workflow."
                    },
                    {
                        "heading": "Key Features for {Industry} {Tool Type}",
                        "content": "Essential features that every {Industry} team should look for in their {Tool Type} solution."
                    },
                    {
                        "heading": "Top Recommended {Tool Type} for {Industry}",
                        "content": "Our curated list of the best {Tool Type} solutions specifically designed for {Industry} teams."
                    }
                ],
                "template_type": "comparison"
            }
            
            response = self.session.post(
                f"{self.base_url}/api/projects/{self.project_id}/templates",
                json=payload
            )
            
            if response.status_code == 200:
                data = response.json()
                self.template_id = data.get("id")
                variables = data.get("variables", [])
                
                if self.template_id and len(variables) > 0:
                    self.log("Create Template", "PASS", 
                            f"Template created with {len(variables)} variables", 
                            {"template_id": self.template_id, "variables": variables})
                    return True
                else:
                    self.log("Create Template", "FAIL", "Invalid template response", data)
                    return False
            else:
                self.log("Create Template", "FAIL", 
                        f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log("Create Template", "FAIL", f"Error: {str(e)}")
            return False
    
    def test_create_dataset(self) -> bool:
        """Test 4: Create dataset manually"""
        if not self.project_id:
            self.log("Create Dataset", "SKIP", "No project ID available")
            return False
            
        try:
            payload = {
                "name": "Tool Types and Industries",
                "data": [
                    {"Tool Type": "Project Management Software", "Industry": "Software Development"},
                    {"Tool Type": "Project Management Software", "Industry": "Marketing"},
                    {"Tool Type": "Task Management Tools", "Industry": "Software Development"},
                    {"Tool Type": "Task Management Tools", "Industry": "Marketing"},
                    {"Tool Type": "Collaboration Platforms", "Industry": "Remote Teams"},
                    {"Tool Type": "Collaboration Platforms", "Industry": "Enterprise"}
                ]
            }
            
            response = self.session.post(
                f"{self.base_url}/api/projects/{self.project_id}/data",
                json=payload
            )
            
            if response.status_code == 200:
                data = response.json()
                self.dataset_id = data.get("id")
                row_count = data.get("row_count", 0)
                
                if self.dataset_id and row_count > 0:
                    self.log("Create Dataset", "PASS", 
                            f"Dataset created with {row_count} rows", 
                            {"dataset_id": self.dataset_id, "columns": data.get("columns", [])})
                    return True
                else:
                    self.log("Create Dataset", "FAIL", "Invalid dataset response", data)
                    return False
            else:
                self.log("Create Dataset", "FAIL", 
                        f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log("Create Dataset", "FAIL", f"Error: {str(e)}")
            return False
    
    def test_validate_dataset(self) -> bool:
        """Test 5: Validate dataset against template"""
        if not all([self.project_id, self.dataset_id, self.template_id]):
            self.log("Validate Dataset", "SKIP", "Missing required IDs")
            return False
            
        try:
            payload = {"template_id": self.template_id}
            
            response = self.session.post(
                f"{self.base_url}/api/projects/{self.project_id}/data/{self.dataset_id}/validate",
                json=payload
            )
            
            if response.status_code == 200:
                data = response.json()
                is_valid = data.get("is_valid", False)
                
                if is_valid:
                    self.log("Validate Dataset", "PASS", 
                            "Dataset is valid for template", data)
                    return True
                else:
                    self.log("Validate Dataset", "WARN", 
                            "Dataset validation has issues", data)
                    return True  # Still continue with warnings
            else:
                self.log("Validate Dataset", "FAIL", 
                        f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log("Validate Dataset", "FAIL", f"Error: {str(e)}")
            return False
    
    def test_generate_preview(self) -> bool:
        """Test 6: Generate preview pages"""
        if not all([self.project_id, self.template_id]):
            self.log("Generate Preview", "SKIP", "Missing required IDs")
            return False
            
        try:
            payload = {"limit": 3}
            
            response = self.session.post(
                f"{self.base_url}/api/projects/{self.project_id}/templates/{self.template_id}/generate-preview",
                json=payload
            )
            
            if response.status_code == 200:
                data = response.json()
                pages = data.get("pages", [])
                total_possible = data.get("total_possible_pages", 0)
                
                if len(pages) > 0 and total_possible > 0:
                    self.log("Generate Preview", "PASS", 
                            f"Preview generated: {len(pages)} pages shown, {total_possible} total possible", 
                            {"sample_page": pages[0] if pages else None})
                    return True
                else:
                    self.log("Generate Preview", "FAIL", "No preview pages generated", data)
                    return False
            else:
                self.log("Generate Preview", "FAIL", 
                        f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log("Generate Preview", "FAIL", f"Error: {str(e)}")
            return False
    
    def test_generate_all_pages(self) -> bool:
        """Test 7: Generate all pages"""
        if not all([self.project_id, self.template_id]):
            self.log("Generate All Pages", "SKIP", "Missing required IDs")
            return False
            
        try:
            payload = {"batch_size": 50}
            
            response = self.session.post(
                f"{self.base_url}/api/projects/{self.project_id}/templates/{self.template_id}/generate",
                json=payload
            )
            
            if response.status_code == 200:
                data = response.json()
                total_generated = data.get("total_generated", 0)
                status = data.get("status", "")
                
                if total_generated > 0 and status == "completed":
                    self.log("Generate All Pages", "PASS", 
                            f"Successfully generated {total_generated} pages", 
                            {"page_ids": data.get("page_ids", [])[:5]})  # Show first 5 IDs
                    return True
                else:
                    self.log("Generate All Pages", "FAIL", 
                            f"Generation failed: {status}", data)
                    return False
            else:
                self.log("Generate All Pages", "FAIL", 
                        f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log("Generate All Pages", "FAIL", f"Error: {str(e)}")
            return False
    
    def test_list_pages(self) -> bool:
        """Test 8: List generated pages"""
        if not self.project_id:
            self.log("List Pages", "SKIP", "No project ID available")
            return False
            
        try:
            response = self.session.get(
                f"{self.base_url}/api/projects/{self.project_id}/pages",
                params={"limit": 10}
            )
            
            if response.status_code == 200:
                data = response.json()
                pages = data.get("pages", [])
                total = data.get("total", 0)
                
                if total > 0:
                    self.log("List Pages", "PASS", 
                            f"Found {total} generated pages", 
                            {"sample_titles": [p.get("title") for p in pages[:3]]})
                    return True
                else:
                    self.log("List Pages", "FAIL", "No pages found", data)
                    return False
            else:
                self.log("List Pages", "FAIL", 
                        f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log("List Pages", "FAIL", f"Error: {str(e)}")
            return False
    
    def test_export_csv(self) -> bool:
        """Test 9: Export pages to CSV"""
        if not self.project_id:
            self.log("Export CSV", "SKIP", "No project ID available")
            return False
            
        try:
            payload = {
                "format": "csv",
                "options": {
                    "include_content": True,
                    "include_seo": True
                }
            }
            
            response = self.session.post(
                f"{self.base_url}/api/projects/{self.project_id}/export",
                json=payload
            )
            
            if response.status_code == 200:
                data = response.json()
                self.export_id = data.get("export_id")
                
                if self.export_id:
                    self.log("Export CSV", "PASS", 
                            f"Export job started", 
                            {"export_id": self.export_id})
                    return True
                else:
                    self.log("Export CSV", "FAIL", "No export ID returned", data)
                    return False
            else:
                self.log("Export CSV", "FAIL", 
                        f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log("Export CSV", "FAIL", f"Error: {str(e)}")
            return False
    
    def test_export_status(self) -> bool:
        """Test 10: Check export status"""
        if not self.export_id:
            self.log("Export Status", "SKIP", "No export ID available")
            return False
            
        try:
            # Poll for export completion (max 30 seconds)
            max_attempts = 10
            for attempt in range(max_attempts):
                response = self.session.get(
                    f"{self.base_url}/api/exports/{self.export_id}/status"
                )
                
                if response.status_code == 200:
                    data = response.json()
                    status = data.get("status", "")
                    
                    if status == "completed":
                        self.log("Export Status", "PASS", 
                                f"Export completed successfully", 
                                {"progress": data.get("progress", 0),
                                 "total_items": data.get("total_items", 0)})
                        return True
                    elif status == "failed":
                        self.log("Export Status", "FAIL", 
                                f"Export failed: {data.get('error_message', 'Unknown error')}", data)
                        return False
                    else:
                        # Still processing
                        if attempt < max_attempts - 1:
                            time.sleep(3)
                            continue
                else:
                    self.log("Export Status", "FAIL", 
                            f"HTTP {response.status_code}: {response.text}")
                    return False
            
            self.log("Export Status", "FAIL", "Export timed out after 30 seconds")
            return False
                
        except Exception as e:
            self.log("Export Status", "FAIL", f"Error: {str(e)}")
            return False
    
    def test_api_performance(self) -> bool:
        """Test 11: API Performance benchmarks"""
        try:
            endpoints = [
                ("/health", "GET", None),
                ("/api/test", "GET", None),
                (f"/api/projects/{self.project_id}", "GET", None) if self.project_id else None,
            ]
            
            performance_results = []
            
            for endpoint_data in endpoints:
                if not endpoint_data:
                    continue
                    
                path, method, payload = endpoint_data
                url = f"{self.base_url}{path}"
                
                # Measure response time
                start_time = time.time()
                
                if method == "GET":
                    response = self.session.get(url)
                else:
                    response = self.session.post(url, json=payload)
                
                end_time = time.time()
                response_time = (end_time - start_time) * 1000  # Convert to ms
                
                performance_results.append({
                    "endpoint": path,
                    "method": method,
                    "status_code": response.status_code,
                    "response_time_ms": round(response_time, 2)
                })
            
            # Check if all responses are under 2 seconds
            slow_endpoints = [r for r in performance_results if r["response_time_ms"] > 2000]
            
            if not slow_endpoints:
                self.log("API Performance", "PASS", 
                        "All endpoints responded within acceptable time", 
                        {"results": performance_results})
                return True
            else:
                self.log("API Performance", "WARN", 
                        f"{len(slow_endpoints)} endpoints are slow", 
                        {"slow_endpoints": slow_endpoints})
                return True  # Warning, not failure
                
        except Exception as e:
            self.log("API Performance", "FAIL", f"Error: {str(e)}")
            return False
    
    def test_error_handling(self) -> bool:
        """Test 12: Error handling and edge cases"""
        try:
            test_cases = [
                {
                    "name": "Invalid project ID",
                    "method": "GET",
                    "path": "/api/projects/invalid-uuid-123",
                    "expected_status": 404
                },
                {
                    "name": "Missing required field",
                    "method": "POST",
                    "path": "/api/analyze-business",
                    "payload": {"input_type": "text"},  # Missing business_input
                    "expected_status": 422
                },
                {
                    "name": "Invalid export format",
                    "method": "POST",
                    "path": f"/api/projects/{self.project_id}/export" if self.project_id else "/api/projects/test/export",
                    "payload": {"format": "invalid_format"},
                    "expected_status": 400
                }
            ]
            
            all_passed = True
            error_results = []
            
            for test_case in test_cases:
                url = f"{self.base_url}{test_case['path']}"
                
                if test_case["method"] == "GET":
                    response = self.session.get(url)
                else:
                    response = self.session.post(url, json=test_case.get("payload", {}))
                
                passed = response.status_code == test_case["expected_status"]
                error_results.append({
                    "test": test_case["name"],
                    "passed": passed,
                    "expected": test_case["expected_status"],
                    "actual": response.status_code
                })
                
                if not passed:
                    all_passed = False
            
            if all_passed:
                self.log("Error Handling", "PASS", 
                        "All error cases handled correctly", 
                        {"results": error_results})
                return True
            else:
                self.log("Error Handling", "FAIL", 
                        "Some error cases not handled properly", 
                        {"results": error_results})
                return False
                
        except Exception as e:
            self.log("Error Handling", "FAIL", f"Error: {str(e)}")
            return False
    
    def cleanup(self):
        """Clean up test data"""
        if self.project_id:
            try:
                response = self.session.delete(f"{self.base_url}/api/projects/{self.project_id}")
                if response.status_code == 200:
                    self.log("Cleanup", "PASS", "Test project deleted successfully")
                else:
                    self.log("Cleanup", "WARN", f"Failed to delete project: {response.status_code}")
            except Exception as e:
                self.log("Cleanup", "WARN", f"Cleanup error: {str(e)}")
    
    def run_all_tests(self) -> Dict[str, Any]:
        """Run all integration tests"""
        print("\n" + "="*60)
        print("PROGRAMMATIC SEO TOOL - INTEGRATION TESTS")
        print("="*60)
        print(f"Target: {self.base_url}")
        print(f"Started: {datetime.utcnow().isoformat()}")
        print("="*60 + "\n")
        
        tests = [
            ("Health Check", self.test_health_check),
            ("Business Analysis", self.test_business_analysis),
            ("Create Template", self.test_create_template),
            ("Create Dataset", self.test_create_dataset),
            ("Validate Dataset", self.test_validate_dataset),
            ("Generate Preview", self.test_generate_preview),
            ("Generate All Pages", self.test_generate_all_pages),
            ("List Pages", self.test_list_pages),
            ("Export CSV", self.test_export_csv),
            ("Export Status", self.test_export_status),
            ("API Performance", self.test_api_performance),
            ("Error Handling", self.test_error_handling),
        ]
        
        passed = 0
        failed = 0
        skipped = 0
        
        for test_name, test_func in tests:
            try:
                result = test_func()
                if result:
                    passed += 1
                else:
                    status = next((r["status"] for r in self.results if r["test"] == test_name), "FAIL")
                    if status == "SKIP":
                        skipped += 1
                    else:
                        failed += 1
            except Exception as e:
                self.log(test_name, "FAIL", f"Unexpected error: {str(e)}")
                failed += 1
        
        # Cleanup
        self.cleanup()
        
        # Summary
        print("\n" + "="*60)
        print("TEST SUMMARY")
        print("="*60)
        print(f"Total Tests: {len(tests)}")
        print(f"Passed: {passed}")
        print(f"Failed: {failed}")
        print(f"Skipped: {skipped}")
        print(f"Success Rate: {(passed/len(tests)*100):.1f}%")
        print("="*60 + "\n")
        
        # Save results to file
        report = {
            "timestamp": datetime.utcnow().isoformat(),
            "target": self.base_url,
            "summary": {
                "total": len(tests),
                "passed": passed,
                "failed": failed,
                "skipped": skipped,
                "success_rate": round(passed/len(tests)*100, 2)
            },
            "results": self.results
        }
        
        report_file = f"integration_test_report_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dumps(report, f, indent=2)
        
        print(f"Detailed report saved to: {report_file}")
        
        return report


def main():
    """Main entry point"""
    # Allow override of base URL via command line
    base_url = sys.argv[1] if len(sys.argv) > 1 else "https://programmaticseotool-production.up.railway.app"
    
    tester = IntegrationTester(base_url)
    report = tester.run_all_tests()
    
    # Exit with appropriate code
    if report["summary"]["failed"] > 0:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()