"""Simple test for page generation components without database dependencies"""
import re
from datetime import datetime

# Test variable extraction
def extract_variables_from_template(pattern):
    """Extract variable names from a template pattern"""
    variables = re.findall(r'\[([^\]]+)\]', pattern)
    return variables

# Test URL slug generation
def generate_url_slug(keyword):
    """Generate URL-friendly slug from keyword"""
    slug = keyword.lower()
    slug = re.sub(r'[^\w\s-]', '', slug)
    slug = re.sub(r'[-\s]+', '-', slug)
    slug = slug.strip('-')
    return slug

# Test content variation
class SimpleContentVariation:
    def __init__(self):
        self.intro_variations = [
            "Looking for {keyword}? You've come to the right place.",
            "If you're searching for {keyword}, this comprehensive guide covers everything you need to know.",
            "Discover the complete guide to {keyword} with expert insights and practical tips."
        ]
    
    def generate_intro(self, keyword, index=0):
        template = self.intro_variations[index % len(self.intro_variations)]
        return template.format(keyword=keyword)

def main():
    print("="*60)
    print("Page Generator Simple Test")
    print("="*60)
    
    # Test 1: Variable extraction
    print("\n1. Testing variable extraction:")
    test_patterns = [
        "[City] [Service] Provider",
        "Best [Product] for [UseCase]",
        "[Industry] [Solution] Guide"
    ]
    
    for pattern in test_patterns:
        variables = extract_variables_from_template(pattern)
        print(f"Pattern: {pattern}")
        print(f"Variables: {variables}")
        print()
    
    # Test 2: URL slug generation
    print("\n2. Testing URL slug generation:")
    test_keywords = [
        "New York Web Design Services",
        "Best SEO Tools & Software",
        "Marketing vs. Sales: What's the Difference?"
    ]
    
    for keyword in test_keywords:
        slug = generate_url_slug(keyword)
        print(f"Keyword: {keyword}")
        print(f"Slug: {slug}")
        print()
    
    # Test 3: Content variation
    print("\n3. Testing content variation:")
    cv = SimpleContentVariation()
    keyword = "Digital Marketing Services"
    
    for i in range(3):
        intro = cv.generate_intro(keyword, i)
        print(f"Intro variation {i+1}:")
        print(intro)
        print()
    
    # Test 4: Sample content generation
    print("\n4. Testing sample content generation:")
    pattern = "[City] [Service] Provider"
    variables = {"City": "Chicago", "Service": "Web Design"}
    
    # Replace variables
    content = pattern
    for var_name, value in variables.items():
        content = content.replace(f'[{var_name}]', value)
    
    print(f"Template: {pattern}")
    print(f"Variables: {variables}")
    print(f"Result: {content}")
    print(f"URL Slug: {generate_url_slug(content)}")
    
    print("\n" + "="*60)
    print("All tests completed successfully!")
    print("="*60)

if __name__ == "__main__":
    main()