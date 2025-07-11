"""Test script for AI variable generation feature"""
import asyncio
import json
import sys
import os

# Add the backend directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from agents.variable_generator import VariableGeneratorAgent

async def test_variable_generation():
    """Test the AI variable generation"""
    generator = VariableGeneratorAgent()
    
    # Test case 1: Canadian Real Estate Tool
    print("=== Test Case 1: Canadian Real Estate Tool ===")
    template_pattern = "{City} with Best Investment Potential"
    business_context = {
        "business_name": "Canadian Real Estate Investment Tool",
        "business_description": "A platform that helps investors find the best real estate opportunities in Canadian cities",
        "target_audience": "Real estate investors",
        "industry": "Real Estate",
        "core_offerings": ["Market Analysis", "Investment Calculators", "Property Listings"]
    }
    additional_context = "Focus on major Canadian cities only"
    
    try:
        result = await generator.generate_variables(
            template_pattern=template_pattern,
            business_context=business_context,
            additional_context=additional_context,
            target_count=10
        )
        
        print(f"Generated {len(result['variables']['City'])} cities:")
        for city in result['variables']['City'][:5]:
            print(f"  - {city}")
        print(f"  ... and {len(result['variables']['City']) - 5} more")
        
        print(f"\nTotal possible titles: {result['total_count']}")
        print("Sample titles:")
        for title in result['titles'][:5]:
            print(f"  - {title}")
        
        # Validate the results
        validation = generator.validate_generated_variables(result['variables'])
        print(f"\nValidation: {'✓ Passed' if validation['is_valid'] else '✗ Failed'}")
        if validation['warnings']:
            print("Warnings:", validation['warnings'])
        
    except Exception as e:
        print(f"Error: {str(e)}")
    
    # Test case 2: Social Media Starter Pack Tool
    print("\n\n=== Test Case 2: Social Media Starter Pack Tool ===")
    template_pattern = "Best {Niche} Starter Packs on {Platform}"
    business_context = {
        "business_name": "Social Media Starter Pack Tool",
        "business_description": "Discover and create curated starter packs for different niches",
        "target_audience": "Social media users and content creators",
        "industry": "Social Media",
        "core_offerings": ["Starter Pack Discovery", "Custom Pack Creation", "Trending Analysis"]
    }
    
    try:
        result = await generator.generate_variables(
            template_pattern=template_pattern,
            business_context=business_context,
            target_count=8
        )
        
        print(f"Generated variables:")
        for var_name, values in result['variables'].items():
            print(f"\n{var_name}: {len(values)} values")
            for value in values[:3]:
                print(f"  - {value}")
            if len(values) > 3:
                print(f"  ... and {len(values) - 3} more")
        
        print(f"\nTotal possible combinations: {result['total_count']}")
        print("Sample titles:")
        for title in result['titles'][:10]:
            print(f"  - {title}")
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    print("Testing AI Variable Generation Feature\n")
    asyncio.run(test_variable_generation())