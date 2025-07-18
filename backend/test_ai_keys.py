#!/usr/bin/env python3
"""
Test AI API key detection and functionality
"""

import os
from api.ai_handler import AIHandler

def test_ai_key_detection():
    """Test if AI keys are properly detected"""
    print("🔑 Testing AI API Key Detection...")
    print("=" * 50)
    
    # Check environment variables
    openai_key = os.environ.get('OPENAI_API_KEY')
    anthropic_key = os.environ.get('ANTHROPIC_API_KEY') 
    perplexity_key = os.environ.get('PERPLEXITY_API_KEY')
    
    print(f"OPENAI_API_KEY: {'✅ Found' if openai_key else '❌ Not found'}")
    if openai_key:
        print(f"  Key preview: {openai_key[:10]}...{openai_key[-4:] if len(openai_key) > 14 else openai_key}")
    
    print(f"ANTHROPIC_API_KEY: {'✅ Found' if anthropic_key else '❌ Not found'}")
    if anthropic_key:
        print(f"  Key preview: {anthropic_key[:10]}...{anthropic_key[-4:] if len(anthropic_key) > 14 else anthropic_key}")
    
    print(f"PERPLEXITY_API_KEY: {'✅ Found' if perplexity_key else '❌ Not found'}")
    if perplexity_key:
        print(f"  Key preview: {perplexity_key[:10]}...{perplexity_key[-4:] if len(perplexity_key) > 14 else perplexity_key}")
    
    # Test AIHandler
    print("\n🤖 Testing AIHandler...")
    ai_handler = AIHandler()
    
    print(f"AIHandler.openai_key: {'✅ Found' if ai_handler.openai_key else '❌ Not found'}")
    print(f"AIHandler.anthropic_key: {'✅ Found' if ai_handler.anthropic_key else '❌ Not found'}")
    print(f"AIHandler.perplexity_key: {'✅ Found' if ai_handler.perplexity_key else '❌ Not found'}")
    print(f"AIHandler.has_ai_provider(): {'✅ YES' if ai_handler.has_ai_provider() else '❌ NO'}")
    
    # Test a simple generation if we have a key
    if ai_handler.has_ai_provider():
        print("\n🧪 Testing AI Content Generation...")
        test_prompt = "Write a 50-word summary about real estate investment."
        
        if ai_handler.perplexity_key:
            print("Testing Perplexity API...")
            try:
                result = ai_handler.generate_with_perplexity(test_prompt, max_tokens=100)
                if result:
                    print(f"✅ Perplexity working: {len(result)} characters generated")
                    print(f"Sample: {result[:100]}...")
                else:
                    print("❌ Perplexity returned no result")
            except Exception as e:
                print(f"❌ Perplexity error: {str(e)}")
        
        if ai_handler.openai_key:
            print("Testing OpenAI API...")
            try:
                result = ai_handler.generate_with_openai(test_prompt, max_tokens=100)
                if result:
                    print(f"✅ OpenAI working: {len(result)} characters generated")
                    print(f"Sample: {result[:100]}...")
                else:
                    print("❌ OpenAI returned no result")
            except Exception as e:
                print(f"❌ OpenAI error: {str(e)}")
                
        if ai_handler.anthropic_key:
            print("Testing Anthropic API...")
            try:
                result = ai_handler.generate_with_anthropic(test_prompt, max_tokens=100)
                if result:
                    print(f"✅ Anthropic working: {len(result)} characters generated")
                    print(f"Sample: {result[:100]}...")
                else:
                    print("❌ Anthropic returned no result")
            except Exception as e:
                print(f"❌ Anthropic error: {str(e)}")
    
    else:
        print("\n❌ No AI providers available - cannot test generation")
        print("\nTo fix this, set environment variables:")
        print("export OPENAI_API_KEY='your-key'")
        print("export ANTHROPIC_API_KEY='your-key'") 
        print("export PERPLEXITY_API_KEY='your-key'")

if __name__ == "__main__":
    test_ai_key_detection()