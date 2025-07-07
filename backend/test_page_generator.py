"""Test script for the page generation engine"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.page_generator import PageGenerator
from backend.models import Template
from backend.content_variation import ContentVariationEngine

def test_variable_extraction():
    """Test extracting variables from template patterns"""
    pg = PageGenerator()
    
    test_patterns = [
        "[City] [Service] Provider",
        "Best [Product] for [UseCase]",
        "[Industry] [Solution] Guide",
        "How to [Action] in [Location]"
    ]
    
    print("Testing variable extraction:")
    for pattern in test_patterns:
        variables = pg.extract_variables_from_template(pattern)
        print(f"Pattern: {pattern}")
        print(f"Variables: {variables}")
        print()

def test_content_variation():
    """Test content variation engine"""
    cve = ContentVariationEngine()
    
    keyword = "Digital Marketing Services"
    
    print("Testing content variation:")
    
    # Test intro generation
    for i in range(3):
        intro = cve.generate_unique_intro(keyword, i)
        print(f"Intro {i+1}:")
        print(intro)
        print()
    
    # Test conclusion generation
    for i in range(3):
        conclusion = cve.generate_unique_conclusion(keyword, i)
        print(f"Conclusion {i+1}:")
        print(conclusion)
        print()

def test_url_slug_generation():
    """Test URL slug generation"""
    pg = PageGenerator()
    
    test_keywords = [
        "New York Web Design Services",
        "Best SEO Tools & Software",
        "How to Start a Business (Complete Guide)",
        "Marketing vs. Sales: What's the Difference?"
    ]
    
    print("Testing URL slug generation:")
    for keyword in test_keywords:
        slug = pg._generate_url_slug(keyword)
        print(f"Keyword: {keyword}")
        print(f"Slug: {slug}")
        print()

def test_sample_page_generation():
    """Test generating a sample page"""
    pg = PageGenerator()
    
    # Create a mock template
    class MockTemplate:
        pattern = "[City] [Service] Provider"
        variables = ["City", "Service"]
        template_sections = {
            'seo_structure': {
                'title_template': '[City] [Service] Provider | Expert Solutions',
                'meta_description_template': 'Find the best [Service] provider in [City]. Professional services with proven results.',
                'h1_template': '[City] [Service] Provider'
            },
            'content_sections': [
                {
                    'heading': 'Professional [Service] in [City]',
                    'content': 'Looking for reliable [Service] in [City]? Our team of experts delivers high-quality solutions tailored to your needs.'
                },
                {
                    'heading': 'Why Choose Our [Service]',
                    'content': 'With years of experience serving [City] businesses, we understand the local market and deliver results that matter.'
                }
            ]
        }
    
    template = MockTemplate()
    variables = {
        'City': {'value': 'Chicago'},
        'Service': {'value': 'Web Design'}
    }
    
    print("Testing sample page generation:")
    page_content = pg.generate_unique_content(template, variables, 0, 1)
    
    print(f"Title: {page_content['title']}")
    print(f"Meta Description: {page_content['meta_description']}")
    print(f"H1: {page_content['h1']}")
    print(f"Keyword: {page_content['keyword']}")
    print(f"Slug: {page_content['slug']}")
    print(f"\nContent Sections:")
    for section in page_content['content_sections']:
        if section.get('heading'):
            print(f"\n## {section['heading']}")
        print(section['content'])

if __name__ == "__main__":
    print("="*60)
    print("Page Generator Test Suite")
    print("="*60)
    
    test_variable_extraction()
    print("\n" + "="*60 + "\n")
    
    test_content_variation()
    print("\n" + "="*60 + "\n")
    
    test_url_slug_generation()
    print("\n" + "="*60 + "\n")
    
    test_sample_page_generation()
    
    print("\n" + "="*60)
    print("All tests completed!")
    print("="*60)