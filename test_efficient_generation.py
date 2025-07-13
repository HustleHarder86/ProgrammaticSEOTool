#!/usr/bin/env python3
"""Test the efficient page generation implementation"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from efficient_page_generator import EfficientPageGenerator
import json
import time

def test_efficient_generation():
    """Test the efficient page generator"""
    print("=== Testing Efficient Page Generation ===\n")
    
    generator = EfficientPageGenerator()
    
    # Test Case 1: Location + Service
    print("1. Testing Location + Service Page Generation")
    template1 = {
        "pattern": "[Service] in [City]",
        "title_pattern": "[Service] in [City] | Find Top Providers",
        "h1_pattern": "[Service] in [City]"
    }
    
    data1 = {
        "Service": "Plumbers",
        "City": "Toronto",
        "count": 127,
        "avg_rating": 4.2,
        "min_price": 85,
        "max_price": 150
    }
    
    start_time = time.time()
    result1 = generator.generate_page(template1, data1, 0)
    end_time = time.time()
    
    print(f"Generated in {(end_time - start_time) * 1000:.2f}ms")
    print(f"Title: {result1['title']}")
    print(f"Word count: {result1['word_count']}")
    print(f"Quality score: {result1['quality_score']}")
    print(f"\nFirst 200 chars of content:")
    print(result1['content_html'][:200] + "...")
    print("-" * 50)
    
    # Test Case 2: Comparison Page
    print("\n2. Testing Comparison Page Generation")
    template2 = {
        "pattern": "[Product1] vs [Product2]",
        "title_pattern": "[Product1] vs [Product2] Comparison",
        "h1_pattern": "[Product1] vs [Product2]"
    }
    
    data2 = {
        "Product1": "Mailchimp",
        "Product2": "ConvertKit",
        "price1": 0,
        "price2": 15,
        "rating1": 4.5,
        "rating2": 4.7
    }
    
    start_time = time.time()
    result2 = generator.generate_page(template2, data2, 0)
    end_time = time.time()
    
    print(f"Generated in {(end_time - start_time) * 1000:.2f}ms")
    print(f"Title: {result2['title']}")
    print(f"Word count: {result2['word_count']}")
    print(f"Quality score: {result2['quality_score']}")
    print("-" * 50)
    
    # Test Case 3: Bulk Generation Speed Test
    print("\n3. Testing Bulk Generation Speed")
    print("Generating 100 pages...")
    
    cities = ["Toronto", "Vancouver", "Montreal", "Calgary", "Edmonton"]
    services = ["Plumbers", "Electricians", "Painters", "Landscapers", "Cleaners"]
    
    start_time = time.time()
    pages_generated = 0
    
    for city in cities:
        for service in services:
            data = {
                "Service": service,
                "City": city,
                "count": 50 + pages_generated,
                "avg_rating": 4.0 + (pages_generated % 9) * 0.1
            }
            
            result = generator.generate_page(template1, data, pages_generated)
            pages_generated += 1
            
            if pages_generated >= 100:
                break
        if pages_generated >= 100:
            break
    
    end_time = time.time()
    total_time = end_time - start_time
    
    print(f"\nGenerated {pages_generated} pages in {total_time:.2f} seconds")
    print(f"Average time per page: {(total_time / pages_generated) * 1000:.2f}ms")
    print(f"Pages per minute: {(pages_generated / total_time) * 60:.0f}")
    
    # Test Case 4: Content Variation
    print("\n4. Testing Content Variation")
    print("Generating 3 similar pages to check variation...")
    
    same_data = {
        "Service": "Dentists",
        "City": "Ottawa",
        "count": 75
    }
    
    variations = []
    for i in range(3):
        result = generator.generate_page(template1, same_data, i)
        intro = result['content_html'].split('</p>')[0]  # Get first paragraph
        variations.append(intro)
        print(f"\nVariation {i+1} intro:")
        print(intro.replace('<p class=\'intro\'>', '').replace('<h1>', '').replace('</h1>', ''))
    
    # Check that variations are different
    if len(set(variations)) == len(variations):
        print("\n✅ All variations are unique!")
    else:
        print("\n⚠️ Some variations are identical")
    
    print("\n=== Test Complete ===")

if __name__ == "__main__":
    test_efficient_generation()