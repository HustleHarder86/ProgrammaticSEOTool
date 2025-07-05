"""Test script to demonstrate Template Builder Agent capabilities"""
from app.agents.template_builder import TemplateBuilderAgent

def test_template_builder():
    """Test the Template Builder Agent functionality"""
    
    # Initialize the agent
    builder = TemplateBuilderAgent()
    
    print("=== Template Builder Agent Test ===\n")
    
    # 1. List available pre-built templates
    print("1. Available Pre-built Templates:")
    templates = builder.list_templates(template_type="library")
    for template in templates:
        print(f"   - {template['name']} ({template['id']})")
        print(f"     Required variables: {', '.join(template['required_variables'])}")
        print(f"     Patterns: {template['patterns'][:2]}...")
        print()
    
    # 2. Create a custom template
    print("\n2. Creating Custom Template:")
    custom_template = builder.create_template(
        name="Real Estate Investment Analysis",
        pattern="{city} {property_type} Investment Analysis {year}",
        structure={
            "title_template": "{city} {property_type} Investment Analysis {year} - ROI Guide",
            "meta_description_template": "Comprehensive {property_type} investment analysis for {city} in {year}. Market trends, ROI calculations, and expert insights.",
            "h1_template": "{city} {property_type} Investment Analysis",
            "url_pattern": "/{city}-{property_type}-investment-{year}",
            "content_sections": [
                {
                    "heading": "{city} Real Estate Market Overview",
                    "content": "Current market conditions for {property_type} in {city}."
                },
                {
                    "heading": "Investment ROI Analysis",
                    "content": "Expected returns for {property_type} investments in {city} for {year}."
                },
                {
                    "heading": "Market Trends and Predictions",
                    "content": "Future outlook for {city} {property_type} market."
                }
            ]
        },
        template_type="investment"
    )
    
    if custom_template["success"]:
        print("   ✅ Template created successfully!")
        print(f"   Template ID: {custom_template['template']['id']}")
        print(f"   Variables: {', '.join(custom_template['template']['variables'])}")
        print("\n   Preview:")
        preview = custom_template['preview']
        print(f"   Title: {preview['structure']['title']}")
        print(f"   URL: {preview['structure']['url']}")
        print(f"   Meta: {preview['structure']['meta_description'][:80]}...")
    else:
        print("   ❌ Template creation failed:")
        for error in custom_template.get('errors', []):
            print(f"      - {error}")
    
    # 3. Validate template with data
    print("\n\n3. Validating Data for Template:")
    
    # Sample data sets
    data_sets = {
        "city": ["Toronto", "Vancouver", "Montreal", "Calgary", "Ottawa"],
        "property_type": ["Condo", "Townhouse", "Single Family Home", "Multi-Unit"],
        "year": ["2024", "2025"]
    }
    
    validation = builder.validate_data_for_template(
        template_id="investment_real_estate_investment_analysis",
        data_sets=data_sets
    )
    
    print(f"   Validation: {'✅ Valid' if validation['is_valid'] else '❌ Invalid'}")
    if validation['errors']:
        print("   Errors:")
        for error in validation['errors']:
            print(f"      - {error}")
    if validation['warnings']:
        print("   Warnings:")
        for warning in validation['warnings']:
            print(f"      - {warning}")
    
    print("\n   Data Summary:")
    for var, info in validation['data_summary'].items():
        print(f"   - {var}: {info['count']} values (sample: {', '.join(info['sample'])})")
    
    # 4. Estimate page count
    print("\n\n4. Estimating Page Count:")
    estimation = builder.estimate_page_count(
        template_id="investment_real_estate_investment_analysis",
        data_sets=data_sets
    )
    
    if "error" not in estimation:
        print(f"   Total pages to be generated: {estimation['total_pages']}")
        print(f"   Calculation: {estimation['calculation']}")
    else:
        print(f"   Error: {estimation['error']}")
    
    # 5. Generate preview with different data
    print("\n\n5. Generating Template Previews:")
    
    # Preview 1: Location + Service template
    location_template = builder.get_template("location_service")
    if location_template:
        preview_data = {
            "location": "Toronto",
            "service": "web development",
            "year": "2024"
        }
        
        preview = builder.generate_preview(location_template, preview_data)
        print("\n   Location + Service Template Preview:")
        print(f"   Pattern: {location_template['patterns'][0]}")
        print(f"   Filled: {preview['filled_pattern']}")
        if 'structure' in preview and 'title' in preview['structure']:
            print(f"   Title: {preview['structure']['title']}")
            print(f"   URL: {preview['structure']['url']}")
    
    # 6. Build complete page structure
    print("\n\n6. Building Complete Page Structure:")
    page_structure = builder.build_page_structure("location_service")
    
    print("   Page Structure Components:")
    print(f"   - SEO Elements: {list(page_structure['seo'].keys())}")
    print(f"   - Content Sections: {len(page_structure['content_sections'])}")
    print(f"   - Required Variables: {', '.join(page_structure['variables']['required'])}")
    print(f"   - Schema Markup Type: {page_structure['schema_markup'].get('@type', 'Unknown')}")
    
    # 7. Generate variations
    print("\n\n7. Generating Page Variations (first 5):")
    variations = builder.generate_variations(
        template_id="location_service",
        data_sets={
            "location": ["Toronto", "Vancouver", "Montreal"],
            "service": ["plumbing", "electrical", "HVAC"],
            "year": ["2024", "2025"]
        },
        limit=5
    )
    
    for i, variation in enumerate(variations, 1):
        print(f"   Variation {i}: {variation}")
    
    # 8. Export template
    print("\n\n8. Exporting Template Configuration:")
    export_config = builder.export_template("location_service")
    if "error" not in export_config:
        print("   Export successful! Configuration includes:")
        print(f"   - Name: {export_config['name']}")
        print(f"   - Type: {export_config['type']}")
        print(f"   - Patterns: {len(export_config.get('patterns', []))} patterns")
        print(f"   - Variables: {len(export_config.get('required_variables', []))} required, {len(export_config.get('optional_variables', []))} optional")
    
    print("\n=== Test Complete ===")

if __name__ == "__main__":
    test_template_builder()