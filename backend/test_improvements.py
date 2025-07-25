#!/usr/bin/env python3
"""Test script to validate visual element and template quality improvements"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ai_visual_generator import AIVisualGenerator
from ai_strategy_generator import AIStrategyGenerator
from api.template_generator import TemplateGenerator
from api.ai_handler import AIHandler
import asyncio
import json


def test_visual_content_detection():
    """Test that visual generator properly detects content types"""
    print("\n=== Testing Visual Content Type Detection ===\n")
    
    visual_gen = AIVisualGenerator()
    
    test_cases = [
        {
            "pattern": "Viome vs Thorne",
            "expected_type": "comparison",
            "description": "Should detect comparison content"
        },
        {
            "pattern": "How to start investing in real estate",
            "expected_type": "how_to",
            "description": "Should detect how-to content"
        },
        {
            "pattern": "Is Airbnb profitable in Toronto",
            "expected_type": "investment",
            "description": "Should detect investment/ROI content"
        },
        {
            "pattern": "Best plumbers in Chicago",
            "expected_type": "location_service",
            "description": "Should detect location-based service"
        },
        {
            "pattern": "iPhone 15 Pro price comparison",
            "expected_type": "product",
            "description": "Should detect product content"
        }
    ]
    
    passed = 0
    failed = 0
    
    for test in test_cases:
        detected_type = visual_gen._detect_content_type(test["pattern"], {})
        
        if detected_type == test["expected_type"]:
            print(f"✅ PASS: {test['description']}")
            print(f"   Pattern: '{test['pattern']}'")
            print(f"   Detected: {detected_type}\n")
            passed += 1
        else:
            print(f"❌ FAIL: {test['description']}")
            print(f"   Pattern: '{test['pattern']}'")
            print(f"   Expected: {test['expected_type']}")
            print(f"   Got: {detected_type}\n")
            failed += 1
    
    print(f"\nResults: {passed} passed, {failed} failed")
    return failed == 0


def test_visual_selection():
    """Test that appropriate visuals are selected for each content type"""
    print("\n=== Testing Visual Selection for Content Types ===\n")
    
    visual_gen = AIVisualGenerator()
    
    test_cases = [
        {
            "pattern": "Salesforce vs HubSpot comparison",
            "check_visual": "intro_visual",
            "expected_type": "comparison_cards",
            "description": "Comparison should show comparison cards"
        },
        {
            "pattern": "How to optimize SEO for e-commerce",
            "check_visual": "intro_visual", 
            "expected_type": "process_steps",
            "description": "How-to should show process steps"
        },
        {
            "pattern": "Airbnb ROI calculator Miami",
            "check_visual": "intro_visual",
            "expected_type": "stats_box",
            "expected_focus": "roi",
            "description": "Investment content should show ROI stats"
        }
    ]
    
    passed = 0
    failed = 0
    
    for test in test_cases:
        template_data = {"pattern": test["pattern"]}
        strategy = visual_gen._get_default_visual_strategy(template_data)
        
        visual = strategy.get(test["check_visual"], {})
        visual_type = visual.get("type")
        visual_focus = visual.get("focus")
        
        if visual_type == test["expected_type"]:
            if "expected_focus" in test:
                if visual_focus == test["expected_focus"]:
                    print(f"✅ PASS: {test['description']}")
                    print(f"   Pattern: '{test['pattern']}'")
                    print(f"   Visual: {visual_type} (focus: {visual_focus})\n")
                    passed += 1
                else:
                    print(f"❌ FAIL: {test['description']}")
                    print(f"   Expected focus: {test['expected_focus']}")
                    print(f"   Got focus: {visual_focus}\n")
                    failed += 1
            else:
                print(f"✅ PASS: {test['description']}")
                print(f"   Pattern: '{test['pattern']}'")
                print(f"   Visual: {visual_type}\n")
                passed += 1
        else:
            print(f"❌ FAIL: {test['description']}")
            print(f"   Pattern: '{test['pattern']}'")
            print(f"   Expected: {test['expected_type']}")
            print(f"   Got: {visual_type}\n")
            failed += 1
    
    print(f"\nResults: {passed} passed, {failed} failed")
    return failed == 0


def test_template_quality():
    """Test that generated templates match actual search queries"""
    print("\n=== Testing Template Quality (Search Query Focus) ===\n")
    
    # Check if AI provider is available
    ai_handler = AIHandler()
    if not ai_handler.has_ai_provider():
        print("⚠️  No AI provider configured - skipping AI template tests")
        print("   Set OPENAI_API_KEY, ANTHROPIC_API_KEY, or PERPLEXITY_API_KEY to test AI features\n")
        return True
    
    # Test predefined templates
    template_gen = TemplateGenerator()
    
    # Check location-based templates
    location_templates = template_gen.template_library["location_based"]["templates"]
    
    good_patterns = [
        "cost", "price", "near me", "reviews", "best", "cheap", "find"
    ]
    
    bad_patterns = [
        "simplify", "enhance", "streamline", "optimize", "transform", "elevate"
    ]
    
    print("Checking predefined templates for search query quality...")
    
    issues = []
    good_count = 0
    
    for template in location_templates[:5]:  # Check first 5
        # Check for good patterns
        has_good = any(pattern in template.lower() for pattern in good_patterns)
        # Check for bad patterns
        has_bad = any(pattern in template.lower() for pattern in bad_patterns)
        
        if has_bad:
            issues.append(f"❌ Bad pattern found: '{template}' (contains marketing jargon)")
        elif has_good:
            good_count += 1
            print(f"✅ Good template: '{template}'")
        else:
            print(f"⚠️  Neutral template: '{template}'")
    
    if issues:
        print("\nIssues found:")
        for issue in issues:
            print(issue)
    
    print(f"\nTemplate quality: {good_count}/{len(location_templates[:5])} templates match search patterns")
    
    return len(issues) == 0


async def test_ai_template_generation():
    """Test that AI generates search-focused templates"""
    print("\n=== Testing AI Template Generation ===\n")
    
    # Check if AI provider is available
    ai_handler = AIHandler()
    if not ai_handler.has_ai_provider():
        print("⚠️  No AI provider configured - skipping this test")
        return True
    
    try:
        strategy_gen = AIStrategyGenerator()
        
        # Test business
        business_input = "Real estate investment analysis platform"
        
        print("Testing template generation for:", business_input)
        print("This may take a moment...\n")
        
        # Generate strategy
        strategy = await strategy_gen.generate_complete_strategy(business_input)
        
        # Check generated templates
        templates = strategy.get("custom_templates", [])
        
        if not templates:
            print("❌ No templates generated")
            return False
        
        print(f"Generated {len(templates)} templates:\n")
        
        good_count = 0
        bad_count = 0
        
        bad_patterns = ["simplify", "enhance", "streamline", "optimize your", "transform"]
        
        for i, template in enumerate(templates[:3]):  # Check first 3
            pattern = template.get("template_pattern", "")
            name = template.get("template_name", "")
            
            print(f"{i+1}. {name}")
            print(f"   Pattern: {pattern}")
            
            # Check for bad patterns
            has_bad = any(bad in pattern.lower() for bad in bad_patterns)
            
            if has_bad:
                print("   ❌ Contains marketing jargon\n")
                bad_count += 1
            else:
                print("   ✅ Looks like a real search query\n")
                good_count += 1
        
        success_rate = good_count / (good_count + bad_count) if (good_count + bad_count) > 0 else 0
        print(f"\nAI Template Quality: {good_count} good, {bad_count} bad ({success_rate*100:.0f}% good)")
        
        return bad_count == 0
        
    except Exception as e:
        print(f"❌ Error testing AI generation: {e}")
        return False


def main():
    """Run all tests"""
    print("=" * 60)
    print("Testing Programmatic SEO Tool Improvements")
    print("=" * 60)
    
    all_passed = True
    
    # Test 1: Visual content detection
    if not test_visual_content_detection():
        all_passed = False
    
    # Test 2: Visual selection
    if not test_visual_selection():
        all_passed = False
    
    # Test 3: Template quality
    if not test_template_quality():
        all_passed = False
    
    # Test 4: AI template generation (async)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    if not loop.run_until_complete(test_ai_template_generation()):
        all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("✅ All tests passed! The improvements are working correctly.")
    else:
        print("❌ Some tests failed. Please review the output above.")
    print("=" * 60)


if __name__ == "__main__":
    main()