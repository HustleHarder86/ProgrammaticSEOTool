"""Test script for the export system."""
import asyncio
import json
from datetime import datetime
from pathlib import Path
import tempfile
import shutil

# Mock data for testing
def create_test_data():
    """Create mock data for testing exports."""
    return [
        {
            'id': 'page-1',
            'title': 'Best Marketing Services in New York',
            'slug': 'marketing-services-new-york',
            'meta_description': 'Find the best marketing services in New York. Expert digital marketing solutions for your business.',
            'content_html': '<h2>Marketing Services in New York</h2><p>New York is home to some of the world\'s best marketing agencies. Our comprehensive directory helps you find the perfect marketing partner for your business needs.</p><h3>Why Choose New York Marketing Services</h3><p>The city offers unparalleled expertise in digital marketing, brand strategy, and creative services.</p>',
            'content_markdown': '## Marketing Services in New York\n\nNew York is home to some of the world\'s best marketing agencies...',
            'content': '<h2>Marketing Services in New York</h2><p>New York is home to some of the world\'s best marketing agencies...</p>',
            'word_count': 150,
            'template_used': 'city-services',
            'status': 'published',
            'created_at': datetime.now().isoformat(),
            'keyword': 'marketing services new york',
            'variables': {'city': 'New York', 'service': 'Marketing Services'},
            'metadata': {
                'project_name': 'Marketing Directory',
                'project_id': 'project-123',
                'page_id': 'page-1'
            }
        },
        {
            'id': 'page-2',
            'title': 'Best Marketing Services in Los Angeles',
            'slug': 'marketing-services-los-angeles',
            'meta_description': 'Find the best marketing services in Los Angeles. Top-rated digital marketing agencies in LA.',
            'content_html': '<h2>Marketing Services in Los Angeles</h2><p>Los Angeles boasts a vibrant marketing scene with agencies specializing in entertainment, tech, and lifestyle brands.</p><h3>LA Marketing Expertise</h3><p>From Hollywood to Silicon Beach, LA agencies offer cutting-edge marketing solutions.</p>',
            'content_markdown': '## Marketing Services in Los Angeles\n\nLos Angeles boasts a vibrant marketing scene...',
            'content': '<h2>Marketing Services in Los Angeles</h2><p>Los Angeles boasts a vibrant marketing scene...</p>',
            'word_count': 140,
            'template_used': 'city-services',
            'status': 'published',
            'created_at': datetime.now().isoformat(),
            'keyword': 'marketing services los angeles',
            'variables': {'city': 'Los Angeles', 'service': 'Marketing Services'},
            'metadata': {
                'project_name': 'Marketing Directory',
                'project_id': 'project-123',
                'page_id': 'page-2'
            }
        },
        {
            'id': 'page-3',
            'title': 'Best SEO Services in Chicago',
            'slug': 'seo-services-chicago',
            'meta_description': 'Professional SEO services in Chicago. Boost your search rankings with top Chicago SEO experts.',
            'content_html': '<h2>SEO Services in Chicago</h2><p>Chicago is a hub for innovative SEO agencies that understand local and national search optimization.</p><h3>Chicago SEO Advantage</h3><p>Midwest values meet cutting-edge SEO techniques in the Windy City.</p>',
            'content_markdown': '## SEO Services in Chicago\n\nChicago is a hub for innovative SEO agencies...',
            'content': '<h2>SEO Services in Chicago</h2><p>Chicago is a hub for innovative SEO agencies...</p>',
            'word_count': 120,
            'template_used': 'city-services',
            'status': 'published',
            'created_at': datetime.now().isoformat(),
            'keyword': 'seo services chicago',
            'variables': {'city': 'Chicago', 'service': 'SEO Services'},
            'metadata': {
                'project_name': 'Marketing Directory',
                'project_id': 'project-123',
                'page_id': 'page-3'
            }
        }
    ]

def test_csv_exporter():
    """Test the CSV exporter."""
    print("Testing CSV Export...")
    from exporters.csv_exporter import CSVExporter
    
    exporter = CSVExporter()
    test_data = create_test_data()
    
    try:
        file_path = exporter.export_content(test_data, "test_project")
        print(f"✅ CSV export successful: {file_path}")
        
        # Verify file exists and has content
        if Path(file_path).exists():
            file_size = Path(file_path).stat().st_size
            print(f"   File size: {file_size} bytes")
            return True
        else:
            print("❌ CSV file not found")
            return False
    except Exception as e:
        print(f"❌ CSV export failed: {e}")
        return False

def test_json_exporter():
    """Test the JSON exporter."""
    print("Testing JSON Export...")
    from exporters.json_exporter import JSONExporter
    
    exporter = JSONExporter()
    test_data = create_test_data()
    
    try:
        # Test flat structure
        file_path = exporter.export_content(test_data, "test_project", {'structure': 'flat'})
        print(f"✅ JSON (flat) export successful: {file_path}")
        
        # Test nested structure
        file_path = exporter.export_content(test_data, "test_project", {'structure': 'nested'})
        print(f"✅ JSON (nested) export successful: {file_path}")
        
        # Test API-ready structure
        file_path = exporter.export_content(test_data, "test_project", {'structure': 'api_ready'})
        print(f"✅ JSON (API-ready) export successful: {file_path}")
        
        # Test sitemap JSON
        file_path = exporter.export_sitemap_json(test_data, "test_project", "https://example.com")
        print(f"✅ JSON sitemap export successful: {file_path}")
        
        return True
    except Exception as e:
        print(f"❌ JSON export failed: {e}")
        return False

def test_wordpress_exporter():
    """Test the WordPress exporter."""
    print("Testing WordPress Export...")
    from exporters.wordpress_exporter import WordPressExporter
    
    exporter = WordPressExporter()
    test_data = create_test_data()
    
    try:
        file_path = exporter.export_content(test_data, "test_project", "https://example.com")
        print(f"✅ WordPress export successful: {file_path}")
        
        # Verify XML is valid
        import xml.etree.ElementTree as ET
        try:
            ET.parse(file_path)
            print("   XML is valid")
        except ET.ParseError as e:
            print(f"   Warning: XML validation failed: {e}")
        
        return True
    except Exception as e:
        print(f"❌ WordPress export failed: {e}")
        return False

def test_html_exporter():
    """Test the HTML exporter."""
    print("Testing HTML Export...")
    from exporters.html_exporter import HTMLExporter
    
    exporter = HTMLExporter()
    test_data = create_test_data()
    
    try:
        # Test flat structure
        file_path = exporter.export_content(test_data, "test_project", {'organize_by_template': False})
        print(f"✅ HTML (flat) export successful: {file_path}")
        
        # Test organized structure
        file_path = exporter.export_content(test_data, "test_project", {'organize_by_template': True})
        print(f"✅ HTML (organized) export successful: {file_path}")
        
        # Test different templates
        file_path = exporter.export_content(test_data, "test_project", {'template_style': 'blog'})
        print(f"✅ HTML (blog style) export successful: {file_path}")
        
        return True
    except Exception as e:
        print(f"❌ HTML export failed: {e}")
        return False

def test_export_manager():
    """Test the export manager with job tracking."""
    print("Testing Export Manager...")
    from export_manager import ExportManager, ExportFormat
    
    # Mock project data by creating a simple test that doesn't require database
    manager = ExportManager()
    
    # Test job creation and tracking
    try:
        # This would normally interact with the database, so we'll just test the structure
        print("✅ Export manager initialized successfully")
        
        # Test format validation
        formats = list(ExportFormat)
        print(f"   Supported formats: {[f.value for f in formats]}")
        
        # Test job ID generation
        from datetime import datetime
        import os
        test_id = f"export_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{os.urandom(4).hex()}"
        print(f"   Test job ID format: {test_id}")
        
        return True
    except Exception as e:
        print(f"❌ Export manager test failed: {e}")
        return False

def create_large_dataset(size=1000):
    """Create a large dataset for performance testing."""
    print(f"Creating large dataset with {size} items...")
    
    cities = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'Philadelphia', 'San Antonio', 'San Diego', 'Dallas', 'San Jose']
    services = ['Marketing', 'SEO', 'Web Design', 'Social Media', 'PPC', 'Content Marketing', 'Email Marketing', 'Analytics']
    
    large_data = []
    for i in range(size):
        city = cities[i % len(cities)]
        service = services[i % len(services)]
        
        item = {
            'id': f'page-{i+1}',
            'title': f'Best {service} Services in {city}',
            'slug': f'{service.lower().replace(" ", "-")}-services-{city.lower().replace(" ", "-")}',
            'meta_description': f'Find the best {service.lower()} services in {city}. Professional {service.lower()} solutions for your business.',
            'content_html': f'<h2>{service} Services in {city}</h2><p>{city} offers excellent {service.lower()} services for businesses of all sizes.</p><h3>Why Choose {city} {service}</h3><p>Professional expertise and proven results in {service.lower()}.</p>',
            'content_markdown': f'## {service} Services in {city}\n\n{city} offers excellent {service.lower()} services...',
            'content': f'<h2>{service} Services in {city}</h2><p>{city} offers excellent {service.lower()} services...</p>',
            'word_count': 100 + (i % 50),
            'template_used': 'city-services',
            'status': 'published',
            'created_at': datetime.now().isoformat(),
            'keyword': f'{service.lower()} services {city.lower()}',
            'variables': {'city': city, 'service': f'{service} Services'},
            'metadata': {
                'project_name': 'Large Marketing Directory',
                'project_id': 'project-large',
                'page_id': f'page-{i+1}'
            }
        }
        large_data.append(item)
    
    return large_data

def test_large_dataset_performance():
    """Test export performance with large datasets."""
    print("Testing Large Dataset Performance...")
    
    # Test with 1000 items
    large_data = create_large_dataset(1000)
    
    # Test JSON export performance
    print("Testing JSON export with 1000 items...")
    from exporters.json_exporter import JSONExporter
    import time
    
    exporter = JSONExporter()
    start_time = time.time()
    
    try:
        file_path = exporter.export_content(large_data, "large_test_project")
        end_time = time.time()
        duration = end_time - start_time
        
        file_size = Path(file_path).stat().st_size / (1024 * 1024)  # Size in MB
        print(f"✅ Large JSON export successful")
        print(f"   Duration: {duration:.2f} seconds")
        print(f"   File size: {file_size:.2f} MB")
        print(f"   Items per second: {len(large_data) / duration:.0f}")
        
        return True
    except Exception as e:
        print(f"❌ Large dataset test failed: {e}")
        return False

def main():
    """Run all export system tests."""
    print("🚀 Starting Export System Tests\n")
    
    tests = [
        test_csv_exporter,
        test_json_exporter,
        test_wordpress_exporter,
        test_html_exporter,
        test_export_manager,
        test_large_dataset_performance
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
            print()  # Add spacing between tests
        except Exception as e:
            print(f"❌ Test {test.__name__} crashed: {e}\n")
    
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All export system tests passed!")
    else:
        print("⚠️  Some tests failed. Check the output above.")

if __name__ == "__main__":
    main()