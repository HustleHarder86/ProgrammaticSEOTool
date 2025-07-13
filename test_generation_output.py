#!/usr/bin/env python3
"""Test the output quality of generated pages"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from efficient_page_generator import EfficientPageGenerator

def test_full_output():
    """Test and display full page output"""
    generator = EfficientPageGenerator()
    
    # Test 1: Location + Service
    print("=== Location + Service Page ===\n")
    
    template = {
        "pattern": "[Service] in [City]",
        "title_pattern": "[Service] in [City] | Find Top Providers",
        "h1_pattern": "[Service] in [City]"
    }
    
    data = {
        "Service": "Plumbers",
        "City": "Toronto",
        "count": 127,
        "avg_rating": 4.2,
        "min_price": 85,
        "max_price": 150
    }
    
    result = generator.generate_page(template, data, 0)
    
    print(f"Title: {result['title']}")
    print(f"Meta Description: {result['meta_description']}")
    print(f"Slug: {result['slug']}")
    print(f"Word Count: {result['word_count']}")
    print(f"Quality Score: {result['quality_score']}")
    print(f"\nFull Content HTML:\n")
    print(result['content_html'])
    print("\n" + "="*60 + "\n")
    
    # Test 2: Comparison Page
    print("=== Comparison Page ===\n")
    
    template2 = {
        "pattern": "[Product1] vs [Product2]",
        "title_pattern": "[Product1] vs [Product2] Comparison 2025",
        "h1_pattern": "[Product1] vs [Product2]"
    }
    
    data2 = {
        "Product1": "Mailchimp",
        "Product2": "ConvertKit",
        "item1": "Mailchimp",
        "item2": "ConvertKit",
        "price1": 0,
        "price2": 15,
        "rating1": 4.5,
        "rating2": 4.7,
        "bestfor1": "Small businesses",
        "bestfor2": "Content creators",
        "reason1": "free plan and ease of use",
        "reason2": "automation and segmentation"
    }
    
    result2 = generator.generate_page(template2, data2, 0)
    
    print(f"Title: {result2['title']}")
    print(f"Meta Description: {result2['meta_description']}")
    print(f"Slug: {result2['slug']}")
    print(f"Word Count: {result2['word_count']}")
    print(f"\nFull Content HTML:\n")
    print(result2['content_html'])

if __name__ == "__main__":
    test_full_output()