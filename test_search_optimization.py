"""Test search term optimization for template generation"""
import asyncio
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.ai_strategy_generator import AIStrategyGenerator
from backend.api.ai_handler import AIHandler

# Test cases with formal terms that should be converted
test_cases = [
    {
        "formal": "Condominium Rental Profitability in British Columbia",
        "expected_contains": ["condo", "BC"],
        "should_not_contain": ["condominium", "British Columbia"]
    },
    {
        "formal": "Automobile Dealerships in Los Angeles",
        "expected_contains": ["car", "LA"],
        "should_not_contain": ["automobile", "Los Angeles"]
    },
    {
        "formal": "Physical Fitness Centers in New York City",
        "expected_contains": ["gym", "NYC"],
        "should_not_contain": ["fitness center", "New York City"]
    },
    {
        "formal": "Attorney Services in San Francisco",
        "expected_contains": ["lawyer", "SF"],
        "should_not_contain": ["attorney", "San Francisco"]
    }
]

async def test_search_optimization():
    """Test the search term optimization"""
    
    # Check if AI is configured
    ai_handler = AIHandler()
    if not ai_handler.has_ai_provider():
        print("❌ No AI provider configured. Please set one of:")
        print("   - OPENAI_API_KEY")
        print("   - ANTHROPIC_API_KEY")
        print("   - PERPLEXITY_API_KEY")
        return
    
    try:
        generator = AIStrategyGenerator()
        
        print("🧪 Testing Search Term Optimization")
        print("=" * 60)
        
        passed = 0
        failed = 0
        
        for test_case in test_cases:
            formal_text = test_case["formal"]
            print(f"\n📝 Testing: {formal_text}")
            
            # Test the conversion
            converted = await generator._convert_to_search_terms(formal_text)
            print(f"✨ Converted to: {converted}")
            
            # Check expectations
            test_passed = True
            
            # Check that expected terms are present
            for expected in test_case["expected_contains"]:
                if expected.lower() not in converted.lower():
                    print(f"   ❌ Missing expected term: '{expected}'")
                    test_passed = False
                else:
                    print(f"   ✅ Found expected term: '{expected}'")
            
            # Check that formal terms are NOT present
            for should_not in test_case["should_not_contain"]:
                if should_not.lower() in converted.lower():
                    print(f"   ❌ Still contains formal term: '{should_not}'")
                    test_passed = False
                else:
                    print(f"   ✅ Removed formal term: '{should_not}'")
            
            if test_passed:
                passed += 1
                print("   ✅ PASSED")
            else:
                failed += 1
                print("   ❌ FAILED")
        
        # Test a complete template optimization
        print("\n" + "=" * 60)
        print("📋 Testing Complete Template Optimization")
        
        test_template = {
            'template_pattern': 'Is {Property Type} Investment Profitable in {City}?',
            'h1_pattern': 'Condominium Investment Analysis for British Columbia',
            'template_name': 'Real Estate Profitability in British Columbia',
            'target_variables': [
                {
                    'variable_name': 'Property Type',
                    'example_values': ['Condominium', 'Single Family Home', 'Townhouse']
                },
                {
                    'variable_name': 'City',
                    'example_values': ['British Columbia', 'Los Angeles', 'New York City']
                }
            ]
        }
        
        print("\nOriginal template:")
        print(f"  Pattern: {test_template['template_pattern']}")
        print(f"  H1: {test_template['h1_pattern']}")
        print(f"  Name: {test_template['template_name']}")
        
        optimized = await generator._optimize_for_search_terms(test_template)
        
        print("\nOptimized template:")
        print(f"  Pattern: {optimized['template_pattern']}")
        print(f"  H1: {optimized['h1_pattern']}")
        print(f"  Name: {optimized['template_name']}")
        
        # Check variable values
        print("\nVariable optimizations:")
        for var in optimized.get('target_variables', []):
            print(f"\n  {var['variable_name']}:")
            for i, (orig, opt) in enumerate(zip(test_template['target_variables'][0]['example_values'], 
                                               var.get('example_values', []))):
                print(f"    {orig} → {opt}")
        
        print("\n" + "=" * 60)
        print(f"Summary: {passed} passed, {failed} failed")
        
        if failed == 0:
            print("✅ All search optimization tests passed!")
        else:
            print(f"⚠️  {failed} tests failed")
            
    except Exception as e:
        print(f"❌ Error during testing: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_search_optimization())