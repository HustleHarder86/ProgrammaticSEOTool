#!/usr/bin/env python3
"""Test script for the centralized prompt configuration system"""

import json
from config.prompt_manager import get_prompt_manager


def test_prompt_system():
    """Test the prompt configuration system"""
    print("\n=== Testing Centralized Prompt System ===\n")
    
    # Get prompt manager instance
    prompt_manager = get_prompt_manager()
    
    # 1. List available prompts
    print("1. Available Prompts:")
    prompts = prompt_manager.list_prompts()
    for category, types in prompts.items():
        print(f"\n  {category}:")
        for prompt_type in types:
            print(f"    - {prompt_type}")
    
    # 2. Get available tones
    print("\n2. Available Tones:")
    tones = prompt_manager.get_tone_options()
    for tone in tones:
        print(f"  - {tone}")
    
    # 3. Test business analysis prompt
    print("\n3. Testing Business Analysis Prompt:")
    business_prompt = prompt_manager.get_prompt(
        category="business_analysis",
        prompt_type="text_based",
        variables={
            "business_input": "Real estate investment platform"
        },
        tone="professional"
    )
    print(f"\nSystem: {business_prompt['system'][:100]}...")
    print(f"\nUser prompt preview: {business_prompt['user'][:200]}...")
    
    # 4. Test content generation with rotation
    print("\n4. Testing Content Generation with Rotation:")
    for i in range(3):
        content_prompt = prompt_manager.get_prompt(
            category="content_generation",
            prompt_type="evaluation_question",
            variables={
                "title": "Is Airbnb profitable in Miami?",
                "data_summary": "Average rate: $150/night, Occupancy: 75%"
            },
            use_rotation=True
        )
        # Extract style from prompt
        style_line = [line for line in content_prompt['user'].split('\n') if 'Style:' in line]
        if style_line:
            print(f"  Iteration {i+1}: {style_line[0].strip()}")
    
    # 5. Test variable generation prompt
    print("\n5. Testing Variable Generation Prompt:")
    var_prompt = prompt_manager.get_prompt(
        category="variable_generation",
        prompt_type="default",
        variables={
            "count": "25",
            "variable_name": "City",
            "template_pattern": "Real Estate Investment in {City}",
            "business_type": "real estate analytics"
        }
    )
    print(f"\nVariable generation prompt preview: {var_prompt['user'][:150]}...")
    
    # 6. Test content validation
    print("\n6. Testing Content Validation:")
    test_content = "This is a test content with only 20 words to check validation."
    validation = prompt_manager.validate_content(test_content)
    print(f"  Validation passed: {validation['passed']}")
    print(f"  Word count: {validation['word_count']}")
    if validation['issues']:
        print("  Issues found:")
        for issue in validation['issues']:
            print(f"    - {issue}")
    
    # 7. Test model configuration
    print("\n7. Testing Model Configuration:")
    for use_case in ["primary", "business_analysis", "fallback"]:
        config = prompt_manager.get_model_config(use_case)
        print(f"\n  {use_case}:")
        print(f"    Provider: {config.get('provider')}")
        print(f"    Model: {config.get('model')}")
        print(f"    Temperature: {config.get('temperature')}")
    
    print("\n=== Prompt System Test Complete ===\n")


if __name__ == "__main__":
    test_prompt_system()