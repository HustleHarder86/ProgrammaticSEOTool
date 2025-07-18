#!/usr/bin/env python3
"""
Comprehensive test for content generation quality
Tests the Phase 1 fixes for data flow and variable mapping
"""

import sys
import traceback
from typing import Dict, List, Any
from data_mapper import data_mapper
from content_patterns import content_patterns
from data_enricher import DataEnricher
from efficient_page_generator import EfficientPageGenerator
from smart_page_generator import SmartPageGenerator


class ContentGenerationTester:
    """Comprehensive tester for content generation quality"""
    
    def __init__(self):
        self.data_enricher = DataEnricher()
        self.efficient_generator = EfficientPageGenerator()
        self.smart_generator = SmartPageGenerator()
        self.test_results = []
        
    def run_all_tests(self):
        """Run all content generation tests"""
        print("🧪 Starting Comprehensive Content Generation Tests")
        print("=" * 60)
        
        # Test 1: Data Mapper Functionality
        print("\n1. Testing Data Mapper...")
        self.test_data_mapper()
        
        # Test 2: Variable Substitution
        print("\n2. Testing Variable Substitution...")
        self.test_variable_substitution()
        
        # Test 3: Content Pattern Quality
        print("\n3. Testing Content Pattern Quality...")
        self.test_content_pattern_quality()
        
        # Test 4: End-to-End Content Generation
        print("\n4. Testing End-to-End Content Generation...")
        self.test_end_to_end_generation()
        
        # Test 5: AI Provider Scenarios
        print("\n5. Testing AI Provider Scenarios...")
        self.test_ai_provider_scenarios()
        
        # Generate final report
        self.generate_test_report()
        
    def test_data_mapper(self):
        """Test data mapper functionality"""
        try:
            # Test data transformation
            enriched_data = {
                "primary_data": {
                    "average_nightly_rate": 127,
                    "occupancy_rate": 68,
                    "total_listings": 342,
                    "growth_rate": 23,
                    "regulations": "STRs allowed with $250/year license",
                    "roi_average": 18
                }
            }
            
            template_variables = {
                "Service": "Short-Term Rental Investment Analysis",
                "City": "Winnipeg"
            }
            
            transformed = data_mapper.transform_data(enriched_data, template_variables)
            
            # Validate transformations
            assert "Service" in transformed
            assert "City" in transformed
            assert "average_nightly_rate" in transformed
            assert "occupancy_rate" in transformed
            assert "profitability" in transformed
            assert "answer" in transformed
            
            # Test business logic mappings
            assert transformed["average_nightly_rate"] == 127
            assert transformed["occupancy_rate"] == 68
            assert transformed["profitability"] in ["highly profitable", "profitable", "moderately profitable"]
            assert transformed["answer"] in ["Yes", "Yes, with proper management"]
            
            print("   ✅ Data Mapper: PASSED")
            self.test_results.append(("Data Mapper", "PASSED", "All transformations working correctly"))
            
        except Exception as e:
            print(f"   ❌ Data Mapper: FAILED - {str(e)}")
            self.test_results.append(("Data Mapper", "FAILED", str(e)))
            traceback.print_exc()
    
    def test_variable_substitution(self):
        """Test that variable substitution works without 'various options'"""
        try:
            # Test pattern with enriched data
            enriched_data = {
                "primary_data": {
                    "average_nightly_rate": 127,
                    "occupancy_rate": 68,
                    "total_listings": 342,
                    "roi_average": 18
                }
            }
            
            template_variables = {
                "Service": "Short-Term Rental Investment Analysis",
                "City": "Halifax"
            }
            
            # Test intro pattern
            pattern = "{answer}, {Service} can be {profitability} in {City}. Average occupancy: {occupancy_rate}%, typical nightly rate: ${average_nightly_rate}."
            
            result = content_patterns.fill_pattern_with_enriched_data(pattern, enriched_data, template_variables)
            
            # Validate no placeholder text
            assert "various options" not in result.lower()
            assert "${" not in result or result.count("$") == result.count("${")  # Either no $ or properly formatted
            assert "None" not in result
            assert "{" not in result  # No unfilled variables
            
            # Validate content makes sense
            assert "Halifax" in result
            assert "Short-Term Rental Investment Analysis" in result
            assert "68%" in result
            assert "$127" in result
            
            print("   ✅ Variable Substitution: PASSED")
            self.test_results.append(("Variable Substitution", "PASSED", "No placeholder text found"))
            
        except Exception as e:
            print(f"   ❌ Variable Substitution: FAILED - {str(e)}")
            self.test_results.append(("Variable Substitution", "FAILED", str(e)))
            traceback.print_exc()
    
    def test_content_pattern_quality(self):
        """Test content pattern quality across different types"""
        test_cases = [
            {
                "content_type": "evaluation_question",
                "template_vars": {"Service": "short-term rental investment", "City": "Toronto"},
                "expected_words": 300
            },
            {
                "content_type": "location_service", 
                "template_vars": {"Service": "Real Estate Analysis Services", "City": "Vancouver"},
                "expected_words": 250
            },
            {
                "content_type": "comparison",
                "template_vars": {"Service": "Investment Property Analysis", "City": "Montreal"},
                "expected_words": 200
            }
        ]
        
        all_passed = True
        
        for case in test_cases:
            try:
                # Generate content using EfficientPageGenerator with proper evaluation pattern
                template = {
                    "title_pattern": "Is {Service} a good investment in {City}?",
                    "pattern": "Is {Service} a good investment in {City}?",
                    "h1_pattern": "{Service} Investment Analysis - {City}"
                }
                
                result = self.efficient_generator.generate_page(template, case["template_vars"])
                
                # Quality checks
                content = result.get("content_html", "")
                word_count = len(content.split())
                
                # Check for quality issues
                quality_issues = []
                
                if "various options" in content.lower():
                    quality_issues.append("Contains 'various options' placeholder")
                
                if word_count < 150:
                    quality_issues.append(f"Too short: {word_count} words")
                
                if "None" in content:
                    quality_issues.append("Contains 'None' values")
                
                if content.count("{") != content.count("}"):
                    quality_issues.append("Unfilled template variables")
                
                if quality_issues:
                    print(f"   ❌ {case['content_type']}: FAILED - {', '.join(quality_issues)}")
                    self.test_results.append((f"Content Quality - {case['content_type']}", "FAILED", "; ".join(quality_issues)))
                    all_passed = False
                else:
                    print(f"   ✅ {case['content_type']}: PASSED ({word_count} words)")
                    self.test_results.append((f"Content Quality - {case['content_type']}", "PASSED", f"{word_count} words generated"))
                    
            except Exception as e:
                print(f"   ❌ {case['content_type']}: ERROR - {str(e)}")
                self.test_results.append((f"Content Quality - {case['content_type']}", "ERROR", str(e)))
                all_passed = False
        
        if all_passed:
            print("   ✅ Overall Content Pattern Quality: PASSED")
        else:
            print("   ❌ Overall Content Pattern Quality: ISSUES FOUND")
    
    def test_end_to_end_generation(self):
        """Test complete end-to-end content generation"""
        try:
            # Real-world test case
            template = {
                "title_pattern": "Is {Service} a good investment in {City}?",
                "pattern": "Is {Service} a good investment in {City}?",
                "h1_pattern": "{Service} Investment Analysis - {City}"
            }
            
            data_row = {
                "Service": "single-family home short-term rental",
                "City": "Calgary"
            }
            
            # Test with EfficientPageGenerator (fallback)
            efficient_result = self.efficient_generator.generate_page(template, data_row)
            
            # Validate structure
            required_fields = ["title", "h1", "meta_description", "content_html", "word_count", "quality_score"]
            missing_fields = [field for field in required_fields if field not in efficient_result]
            
            if missing_fields:
                raise Exception(f"Missing required fields: {missing_fields}")
            
            # Validate content quality
            content = efficient_result["content_html"]
            word_count = efficient_result["word_count"]
            
            if word_count < 200:
                raise Exception(f"Content too short: {word_count} words")
            
            if "various options" in content.lower():
                raise Exception("Contains 'various options' placeholder")
            
            if "Calgary" not in content:
                raise Exception("City name not properly substituted")
            
            if "single-family home" not in content.lower():
                raise Exception("Service name not properly substituted")
            
            print("   ✅ End-to-End Generation: PASSED")
            print(f"      - Word count: {word_count}")
            print(f"      - Quality score: {efficient_result['quality_score']}")
            print(f"      - Title: {efficient_result['title']}")
            
            self.test_results.append(("End-to-End Generation", "PASSED", f"{word_count} words, quality {efficient_result['quality_score']}"))
            
        except Exception as e:
            print(f"   ❌ End-to-End Generation: FAILED - {str(e)}")
            self.test_results.append(("End-to-End Generation", "FAILED", str(e)))
            traceback.print_exc()
    
    def test_ai_provider_scenarios(self):
        """Test both with and without AI providers"""
        try:
            # Test AI fallback scenario (when AI not configured)
            template = {
                "title_pattern": "Is {Service} a good investment in {City}?",
                "pattern": "Is {Service} a good investment in {City}?",
                "h1_pattern": "{Service} Investment Analysis - {City}"
            }
            
            data_row = {
                "Service": "single-family home short-term rental",
                "City": "Edmonton"
            }
            
            # Test SmartPageGenerator fallback
            smart_result = self.smart_generator.generate_page(template, data_row)
            
            # Should fall back to pattern-based generation but with improved quality
            content = smart_result.get("content_html", "")
            
            if "various options" in content.lower():
                raise Exception("AI fallback still contains 'various options'")
            
            if len(content.split()) < 150:
                raise Exception(f"AI fallback content too short: {len(content.split())} words")
            
            print("   ✅ AI Provider Scenarios: PASSED")
            print(f"      - Fallback content length: {len(content.split())} words")
            
            self.test_results.append(("AI Provider Scenarios", "PASSED", f"Fallback working with {len(content.split())} words"))
            
        except Exception as e:
            print(f"   ❌ AI Provider Scenarios: FAILED - {str(e)}")
            self.test_results.append(("AI Provider Scenarios", "FAILED", str(e)))
            traceback.print_exc()
    
    def generate_test_report(self):
        """Generate final test report"""
        print("\n" + "=" * 60)
        print("📊 COMPREHENSIVE TEST REPORT")
        print("=" * 60)
        
        passed_tests = sum(1 for _, status, _ in self.test_results if status == "PASSED")
        total_tests = len(self.test_results)
        
        print(f"\nOverall Results: {passed_tests}/{total_tests} tests passed")
        
        if passed_tests == total_tests:
            print("🎉 ALL TESTS PASSED! Content generation quality fixes are working.")
            return True
        else:
            print("⚠️  Some tests failed. Review the issues above.")
            
        print("\nDetailed Results:")
        for test_name, status, details in self.test_results:
            status_icon = "✅" if status == "PASSED" else "❌"
            print(f"  {status_icon} {test_name}: {status}")
            if details:
                print(f"      {details}")
        
        return passed_tests == total_tests


def main():
    """Run comprehensive content generation tests"""
    tester = ContentGenerationTester()
    success = tester.run_all_tests()
    
    if success:
        print("\n🚀 Ready for deployment! All quality checks passed.")
        sys.exit(0)
    else:
        print("\n🛑 Fix required issues before deployment.")
        sys.exit(1)


if __name__ == "__main__":
    main()