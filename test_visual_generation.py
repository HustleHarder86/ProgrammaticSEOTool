"""Test script for improved AI visual generation"""
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.ai_visual_generator import AIVisualGenerator
from backend.api.ai_handler import AIHandler

# Sample blog content with specific statistics
sample_blog_content = """
<h1>Is Airbnb Profitable in Winnipeg? 2024 Analysis</h1>
<p>Many property owners in Winnipeg are wondering whether short-term rentals through Airbnb can be a profitable investment. Based on current market data, the answer is yes - with the right property and management approach.</p>

<p>The average nightly rate for Airbnb properties in Winnipeg is $127, with an impressive occupancy rate of 68%. This translates to potential monthly revenue of approximately $2,591 for a typical single-family home. After accounting for expenses averaging $800 per month, property owners can expect monthly profits around $1,791.</p>

<p>Winnipeg's short-term rental market has shown strong growth, with a 23% increase in listings over the past year. The city currently has 342 active short-term rental properties, indicating a healthy but not oversaturated market. The peak season runs from May through September, when occupancy rates can reach as high as 85%.</p>

<p>Single-family homes tend to perform best, with an average ROI of 18% annually. Condos follow closely with a 15% average return, while townhouses typically see 16% ROI. The city's regulations are relatively favorable, requiring only a $250 annual license for short-term rental operations.</p>

<p>For investors considering entering the Winnipeg Airbnb market, the data suggests strong potential for profitability, especially with properties in desirable neighborhoods near downtown or major attractions.</p>
"""

sample_comparison_content = """
<h1>Viome vs Thorne: Comprehensive Comparison for 2024</h1>
<p>When choosing between Viome and Thorne for personalized health testing, understanding the key differences is crucial for making the right decision.</p>

<p>Viome offers comprehensive gut microbiome testing starting at $89 per month for their basic plan, while Thorne's premium testing package costs $79 monthly. Viome analyzes over 30,000 microbial genes, providing insights into your gut health, while Thorne focuses on blood biomarkers with 45 different health indicators.</p>

<p>In terms of testing frequency, Viome recommends retesting every 6 months to track changes in your microbiome, whereas Thorne suggests quarterly testing for optimal health monitoring. Customer satisfaction ratings are strong for both, with Viome averaging 4.3 stars from 1,247 reviews and Thorne scoring 4.5 stars from 892 customer reviews.</p>

<p>Viome excels in microbiome analysis and personalized food recommendations, making it ideal for those with digestive issues or seeking dietary optimization. Thorne's strength lies in comprehensive blood work and hormone testing, better suited for athletes or those monitoring specific health conditions.</p>

<p>Both companies offer mobile apps for tracking results, but Viome's app includes meal planning features while Thorne integrates with fitness trackers. Shipping times are comparable, with both delivering test kits within 3-5 business days.</p>
"""

def test_visual_generation():
    """Test the AI visual generator with sample content"""
    
    # Check if AI is configured
    ai_handler = AIHandler()
    if not ai_handler.has_ai_provider():
        print("❌ No AI provider configured. Please set one of:")
        print("   - OPENAI_API_KEY")
        print("   - ANTHROPIC_API_KEY")
        print("   - PERPLEXITY_API_KEY")
        return
    
    generator = AIVisualGenerator()
    
    # Test 1: Investment content
    print("=" * 80)
    print("TEST 1: Investment/Profitability Content")
    print("=" * 80)
    
    template_data_investment = {
        'title': 'Is Airbnb Profitable in Winnipeg?',
        'pattern': 'Is [Service] Profitable in [City]?',
        'City': 'Winnipeg',
        'Service': 'Airbnb'
    }
    
    enriched_data_investment = {
        'primary_data': {
            'average_nightly_rate': 127,
            'occupancy_rate': 68,
            'total_listings': 342,
            'roi_percentage': 18,
            'monthly_revenue': 2591,
            'monthly_expenses': 800
        }
    }
    
    enhanced_content_1 = generator.enhance_content_with_visuals(
        sample_blog_content,
        template_data_investment,
        enriched_data_investment
    )
    
    print("\nOriginal word count:", len(sample_blog_content.split()))
    print("Enhanced word count:", len(enhanced_content_1.split()))
    print("\nEnhanced content preview:")
    print(enhanced_content_1[:1000] + "...\n")
    
    # Test 2: Comparison content
    print("=" * 80)
    print("TEST 2: Comparison Content")
    print("=" * 80)
    
    template_data_comparison = {
        'title': 'Viome vs Thorne',
        'pattern': '[Product1] vs [Product2]',
        'Product1': 'Viome',
        'Product2': 'Thorne'
    }
    
    enriched_data_comparison = {
        'primary_data': {
            'viome_price': '$89/month',
            'thorne_price': '$79/month',
            'viome_rating': 4.3,
            'thorne_rating': 4.5,
            'viome_reviews': 1247,
            'thorne_reviews': 892
        }
    }
    
    enhanced_content_2 = generator.enhance_content_with_visuals(
        sample_comparison_content,
        template_data_comparison,
        enriched_data_comparison
    )
    
    print("\nOriginal word count:", len(sample_comparison_content.split()))
    print("Enhanced word count:", len(enhanced_content_2.split()))
    print("\nEnhanced content preview:")
    print(enhanced_content_2[:1000] + "...\n")
    
    # Save full results for inspection
    with open('test_visual_output_investment.html', 'w', encoding='utf-8') as f:
        f.write(f"""<!DOCTYPE html>
<html>
<head>
    <title>Visual Generation Test - Investment</title>
    <style>
        body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }}
        h1 {{ color: #333; }}
        p {{ line-height: 1.6; color: #666; }}
    </style>
</head>
<body>
{enhanced_content_1}
</body>
</html>""")
    
    with open('test_visual_output_comparison.html', 'w', encoding='utf-8') as f:
        f.write(f"""<!DOCTYPE html>
<html>
<head>
    <title>Visual Generation Test - Comparison</title>
    <style>
        body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }}
        h1 {{ color: #333; }}
        p {{ line-height: 1.6; color: #666; }}
    </style>
</head>
<body>
{enhanced_content_2}
</body>
</html>""")
    
    print("✅ Test completed! Check test_visual_output_*.html files for full results")


if __name__ == "__main__":
    test_visual_generation()