#!/usr/bin/env python3
"""
Example: Using the Business Analyzer Agent to discover programmatic SEO opportunities.

This example shows how to:
1. Analyze a business from description or URL
2. Get template suggestions with estimated page counts
3. Identify data requirements for each template
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from api.ai_handler import AIHandler
from app.agents.business_analyzer import BusinessAnalyzerAgent

def main():
    # Initialize the Business Analyzer with AI handler
    ai_handler = AIHandler()
    analyzer = BusinessAnalyzerAgent(ai_handler)
    
    # Example 1: Real Estate Business
    print("=" * 70)
    print("EXAMPLE 1: Real Estate Investment Company")
    print("=" * 70)
    
    real_estate_description = """
    Austin Real Estate Investments is a full-service real estate investment firm 
    specializing in residential and commercial properties across Texas. We help 
    investors find, analyze, and manage profitable real estate opportunities in 
    Austin, Dallas, Houston, and San Antonio. Our services include property 
    analysis, market research, property management, and investment consulting.
    """
    
    # Analyze the business
    analysis = analyzer.analyze_business(real_estate_description)
    
    print(f"\nBusiness Analysis:")
    print(f"- Industry: {analysis.industry}")
    print(f"- Services: {', '.join(analysis.services[:3])}")
    print(f"- Locations: {', '.join(analysis.locations[:3])}")
    
    # Get template suggestions
    templates = analyzer.suggest_templates(analysis)
    
    print(f"\n📋 TEMPLATE OPPORTUNITIES (Top 5):")
    for i, template in enumerate(templates[:5], 1):
        print(f"\n{i}. {template.name}")
        print(f"   Pattern: {template.pattern}")
        print(f"   Estimated Pages: {template.estimated_pages:,}")
        print(f"   Priority: {'⭐' * (template.priority // 2)}")
        print(f"   Intent: {template.search_intent}")
        print(f"   Examples:")
        for example in template.examples[:2]:
            print(f"     • {example}")
        
        # Show data requirements
        data_reqs = analyzer.identify_data_requirements(template)
        if data_reqs:
            print(f"   Data Needed:")
            for req in data_reqs:
                print(f"     • {req.data_type}: ~{req.suggested_count} items")
    
    # Example 2: SaaS Business
    print("\n" + "=" * 70)
    print("EXAMPLE 2: Project Management SaaS")
    print("=" * 70)
    
    saas_description = """
    TaskFlow Pro is a cloud-based project management software designed for 
    creative agencies and marketing teams. We offer features like task tracking, 
    team collaboration, client portals, time tracking, and resource management. 
    Our platform integrates with popular tools like Slack, Google Drive, and 
    Adobe Creative Cloud.
    """
    
    analysis2 = analyzer.analyze_business(saas_description)
    templates2 = analyzer.suggest_templates(analysis2)
    
    print(f"\n📋 TEMPLATE OPPORTUNITIES (Top 3):")
    for i, template in enumerate(templates2[:3], 1):
        print(f"\n{i}. {template.name}")
        print(f"   Pattern: {template.pattern}")
        print(f"   Estimated Pages: {template.estimated_pages:,}")
        
        # Calculate actual page count with sample data
        sample_data = {
            'industry': 10,
            'feature': 8,
            'tool': 15,
            'use_case': 12
        }
        actual_pages = analyzer.calculate_page_potential(template, sample_data)
        if actual_pages != template.estimated_pages:
            print(f"   With Sample Data: {actual_pages:,} pages")
    
    # Example 3: URL Analysis
    print("\n" + "=" * 70)
    print("EXAMPLE 3: Analyzing from URL")
    print("=" * 70)
    
    # This would analyze a real website if AI handler has web access
    url = "https://www.example-plumbing-service.com"
    print(f"\nAnalyzing: {url}")
    print("(In production, this would fetch and analyze the actual website)")
    
    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY: How to Use This for Programmatic SEO")
    print("=" * 70)
    print("""
1. Analyze your business using description or URL
2. Review template opportunities and pick the best ones
3. Prepare data for each template variable (CSV or manual entry)
4. Generate hundreds/thousands of pages automatically
5. Export and publish to your website

Example: "[City] Real Estate Investment Guide"
- Cities: 50 locations
- Result: 50 unique, SEO-optimized pages
- Each page targets: "Austin real estate investment guide", etc.
    """)

if __name__ == "__main__":
    main()