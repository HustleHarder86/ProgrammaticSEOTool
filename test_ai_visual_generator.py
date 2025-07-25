#!/usr/bin/env python3
"""Test script for AI visual generator functionality"""

import os
import sys
sys.path.append('backend')

from ai_visual_generator import AIVisualGenerator
from smart_page_generator import SmartPageGenerator
from data_enricher import DataEnricher

def test_visual_enhancement():
    """Test visual enhancement with sample content"""
    
    # Sample content
    content_html = """<h1>Professional Plumbing Services in Austin</h1>

<p class='intro'>Find reliable plumbing services in Austin with 45 verified providers offering average ratings of 4.5 stars.</p>

<p>Austin's plumbing service market offers diverse options ranging from emergency repairs to full bathroom renovations. Local providers maintain competitive pricing between $95-$350 per service, with most offering same-day availability.</p>

<p>When selecting plumbing services in Austin, consider these important factors: experience level (most providers have 10 years in business), customer reviews and testimonials, response times (typically 2-4 hours for initial contact), and pricing transparency.</p>

<p>The plumbing industry in Austin has experienced steady growth, with demand increasing by 15% over the past year. Peak demand typically occurs during summer months, so booking in advance is recommended.</p>

<p class='cta'>Ready to find the perfect plumbing service? Compare Austin's top-rated providers and get quotes today.</p>"""

    # Template data
    template_data = {
        "pattern": "[Service] in [City]",
        "Service": "Plumbing Services",
        "City": "Austin"
    }
    
    # Enriched data
    enriched_data = {
        "primary_data": {
            "provider_count": 45,
            "average_rating": 4.5,
            "min_price": 95,
            "max_price": 350,
            "average_response_time": "2-4 hours",
            "top_providers": [
                {"name": "Austin Pro Plumbing", "rating": 4.8, "reviews": 342, "price": "$150", "response": "2h"},
                {"name": "Quick Fix Plumbers", "rating": 4.6, "reviews": 287, "price": "$125", "response": "1h"},
                {"name": "24/7 Emergency Plumbing", "rating": 4.7, "reviews": 456, "price": "$175", "response": "30min"},
                {"name": "Eco-Friendly Plumbing Co", "rating": 4.5, "reviews": 198, "price": "$140", "response": "3h"},
                {"name": "Austin's Best Plumbers", "rating": 4.9, "reviews": 523, "price": "$165", "response": "2h"}
            ]
        },
        "data_quality": 85
    }
    
    # Test visual generator
    print("Testing AI Visual Generator...")
    visual_generator = AIVisualGenerator()
    
    enhanced_content = visual_generator.enhance_content_with_visuals(
        content_html, template_data, enriched_data
    )
    
    print("\n=== ORIGINAL CONTENT ===")
    print(f"Length: {len(content_html)} characters")
    print("First 200 chars:", content_html[:200])
    
    print("\n=== ENHANCED CONTENT ===")
    print(f"Length: {len(enhanced_content)} characters")
    print(f"Increased by: {len(enhanced_content) - len(content_html)} characters")
    
    # Check if visual elements were added
    visual_indicators = [
        "info-box",
        "📊",
        "<table",
        "grid-template-columns",
        "background: linear-gradient",
        "Quick Stats",
        "Provider Name"
    ]
    
    print("\n=== VISUAL ELEMENTS CHECK ===")
    for indicator in visual_indicators:
        if indicator in enhanced_content:
            print(f"✅ Found: {indicator}")
        else:
            print(f"❌ Missing: {indicator}")
    
    # Save output for inspection
    output_file = "test_visual_output.html"
    with open(output_file, "w") as f:
        f.write("""<!DOCTYPE html>
<html>
<head>
    <title>Visual Generator Test</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
        .intro { font-size: 1.2em; color: #666; }
        .cta { background: #f0f0f0; padding: 20px; border-left: 4px solid #007bff; }
    </style>
</head>
<body>
""")
        f.write(enhanced_content)
        f.write("</body></html>")
    
    print(f"\n✅ Test output saved to: {output_file}")
    print("Open this file in a browser to see the visual elements")
    
    return enhanced_content

def test_full_generation():
    """Test full page generation with AI visuals"""
    print("\n" + "="*50)
    print("Testing Full Page Generation with AI Visuals")
    print("="*50)
    
    try:
        # Check if AI is configured
        from api.ai_handler import AIHandler
        ai_handler = AIHandler()
        
        if not ai_handler.has_ai_provider():
            print("⚠️  No AI provider configured. Using fallback visual generation.")
        else:
            print("✅ AI provider found. Using AI-enhanced visual generation.")
        
        # Create page generator
        generator = SmartPageGenerator()
        
        # Sample template and data
        template = {
            "pattern": "Is [Property Type] profitable in [City]? Investment Analysis",
            "title_pattern": "Is [Property Type] profitable in [City]? 2024 Investment Analysis",
            "h1_pattern": "[Property Type] Profitability in [City]: Data-Driven Analysis"
        }
        
        data_row = {
            "Property Type": "Single-Family Homes",
            "City": "Denver",
            "property type": "single-family homes",
            "city": "denver"
        }
        
        # Generate page
        print("\nGenerating page...")
        result = generator.generate_page(template, data_row, 0)
        
        if result:
            print(f"\n✅ Page generated successfully!")
            print(f"Title: {result['title']}")
            print(f"Word count: {result['word_count']}")
            print(f"Quality score: {result['quality_score']}")
            print(f"Content length: {len(result['content_html'])} characters")
            
            # Save full page
            with open("test_full_page.html", "w") as f:
                f.write(f"""<!DOCTYPE html>
<html>
<head>
    <title>{result['title']}</title>
    <meta name="description" content="{result['meta_description']}">
    <style>
        body {{ font-family: Georgia, serif; max-width: 800px; margin: 0 auto; padding: 20px; line-height: 1.6; }}
        h1 {{ font-family: Arial, sans-serif; }}
        .intro {{ font-size: 1.2em; color: #666; font-style: italic; }}
        .cta {{ background: #f9f9f9; padding: 20px; border-left: 4px solid #4CAF50; margin: 20px 0; }}
    </style>
</head>
<body>
{result['content_html']}
</body>
</html>""")
            
            print(f"\n✅ Full page saved to: test_full_page.html")
        else:
            print("\n❌ Page generation failed")
            
    except Exception as e:
        print(f"\n❌ Error during full generation test: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # Test visual enhancement
    test_visual_enhancement()
    
    # Test full generation
    test_full_generation()