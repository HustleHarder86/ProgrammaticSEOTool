#!/usr/bin/env python3
"""Test script for Business Analyzer Agent."""
import asyncio
import json
from api.ai_handler import AIHandler
from app.agents.business_analyzer import BusinessAnalyzerAgent

def test_business_analyzer():
    """Test the business analyzer with sample inputs."""
    
    # Initialize
    ai_handler = AIHandler()
    analyzer = BusinessAnalyzerAgent(ai_handler)
    
    # Test cases
    test_cases = [
        "A real estate agency in Austin, TX specializing in luxury homes and investment properties",
        "https://www.example.com",
        "SaaS company providing project management software for remote teams",
        "Local plumbing service company serving the Dallas-Fort Worth area"
    ]
    
    for test_input in test_cases:
        print(f"\n{'='*60}")
        print(f"Testing: {test_input[:50]}...")
        print('='*60)
        
        try:
            # Analyze business
            analysis = analyzer.analyze_business(test_input)
            print(f"\nBusiness Analysis:")
            print(f"- Name: {analysis.business_name}")
            print(f"- Industry: {analysis.industry}")
            print(f"- Services: {', '.join(analysis.services[:3])}")
            print(f"- Target Audience: {', '.join(analysis.target_audience[:3])}")
            print(f"- Business Model: {analysis.business_model}")
            
            # Get template suggestions
            templates = analyzer.suggest_templates(analysis)
            print(f"\nTop Template Opportunities:")
            for i, template in enumerate(templates[:5], 1):
                print(f"\n{i}. {template.name}")
                print(f"   Pattern: {template.pattern}")
                print(f"   Est. Pages: {template.estimated_pages:,}")
                print(f"   Priority: {template.priority}/10")
                print(f"   Examples:")
                for example in template.examples[:2]:
                    print(f"   - {example}")
                
                # Get data requirements
                data_reqs = analyzer.identify_data_requirements(template)
                print(f"   Data Requirements:")
                for req in data_reqs:
                    print(f"   - {req.data_type}: {req.suggested_count} items ({req.data_source})")
        
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    print("Testing Business Analyzer Agent...")
    test_business_analyzer()
    print("\nTest complete!")