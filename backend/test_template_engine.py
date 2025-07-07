"""Test script for template engine functionality"""
from template_engine import TemplateEngine

def test_template_engine():
    engine = TemplateEngine()
    
    # Test 1: Extract variables
    print("Test 1: Extract variables")
    template_string = "Best {product_type} for {use_case} in {location}"
    variables = engine.extract_variables(template_string)
    print(f"Template: {template_string}")
    print(f"Variables: {variables}")
    print()
    
    # Test 2: Validate template
    print("Test 2: Validate template")
    template_data = {
        'name': 'Product Recommendation Template',
        'pattern': 'Best {product_type} for {use_case}',
        'title_template': 'Best {product_type} for {use_case} - Top Picks 2024',
        'meta_description_template': 'Discover the best {product_type} for {use_case}. Expert reviews and recommendations.',
        'content_sections': [
            {
                'heading': 'Top {product_type} for {use_case}',
                'content': 'Our experts have tested the best {product_type} options for {use_case}.'
            }
        ]
    }
    validation = engine.validate_template(template_data)
    print(f"Is valid: {validation['is_valid']}")
    print(f"Variables found: {validation['variables']}")
    if validation['errors']:
        print(f"Errors: {validation['errors']}")
    if validation['warnings']:
        print(f"Warnings: {validation['warnings']}")
    print()
    
    # Test 3: Generate preview
    print("Test 3: Generate preview")
    sample_data = {
        'product_type': 'CRM Software',
        'use_case': 'Small Business'
    }
    preview = engine.generate_preview(template_data, sample_data)
    print(f"Filled pattern: {preview['filled_pattern']}")
    print(f"SEO Title: {preview['seo']['title']}")
    print(f"SEO Meta: {preview['seo']['meta_description']}")
    print(f"URL: {preview['seo']['url']}")
    print()
    
    # Test 4: Test with missing variables
    print("Test 4: Test with incomplete data")
    incomplete_data = {'product_type': 'Software'}  # Missing use_case
    preview2 = engine.generate_preview(template_data, incomplete_data)
    print(f"Filled pattern: {preview2['filled_pattern']}")
    print("Note: {use_case} should remain as placeholder")

if __name__ == "__main__":
    test_template_engine()