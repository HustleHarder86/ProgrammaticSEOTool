"""WordPress XML export functionality."""
import xml.etree.ElementTree as ET
from xml.dom import minidom
import os
from typing import List, Dict
from datetime import datetime
from config import settings
import logging

logger = logging.getLogger(__name__)

class WordPressExporter:
    """Export content to WordPress XML format."""
    
    def export_content(self, content_list: List[Dict], project_name: str, site_url: str = "https://example.com") -> str:
        """Export content list to WordPress XML file."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{project_name}_wordpress_{timestamp}.xml"
        filepath = os.path.join(settings.EXPORTS_DIR, filename)
        
        # Ensure exports directory exists
        os.makedirs(settings.EXPORTS_DIR, exist_ok=True)
        
        # Create root RSS element
        rss = ET.Element('rss', {
            'version': '2.0',
            'xmlns:excerpt': 'http://wordpress.org/export/1.2/excerpt/',
            'xmlns:content': 'http://purl.org/rss/1.0/modules/content/',
            'xmlns:wfw': 'http://wellformedweb.org/CommentAPI/',
            'xmlns:dc': 'http://purl.org/dc/elements/1.1/',
            'xmlns:wp': 'http://wordpress.org/export/1.2/'
        })
        
        # Create channel
        channel = ET.SubElement(rss, 'channel')
        
        # Add channel metadata
        ET.SubElement(channel, 'title').text = project_name
        ET.SubElement(channel, 'link').text = site_url
        ET.SubElement(channel, 'description').text = f'Programmatic SEO content for {project_name}'
        ET.SubElement(channel, 'language').text = 'en-US'
        ET.SubElement(channel, 'wp:wxr_version').text = '1.2'
        ET.SubElement(channel, 'wp:base_site_url').text = site_url
        ET.SubElement(channel, 'wp:base_blog_url').text = site_url
        
        # Add content items
        for idx, content in enumerate(content_list):
            item = ET.SubElement(channel, 'item')
            
            # Basic post information
            ET.SubElement(item, 'title').text = content.get('title', '')
            ET.SubElement(item, 'link').text = f"{site_url}/{content.get('slug', '')}"
            ET.SubElement(item, 'pubDate').text = datetime.now().strftime('%a, %d %b %Y %H:%M:%S +0000')
            ET.SubElement(item, 'dc:creator').text = 'admin'
            ET.SubElement(item, 'guid', {'isPermaLink': 'false'}).text = f"{site_url}/?p={idx + 1000}"
            ET.SubElement(item, 'description').text = content.get('meta_description', '')
            ET.SubElement(item, 'content:encoded').text = self._wrap_cdata(content.get('content_html', ''))
            ET.SubElement(item, 'excerpt:encoded').text = self._wrap_cdata(content.get('meta_description', ''))
            ET.SubElement(item, 'wp:post_id').text = str(idx + 1000)
            ET.SubElement(item, 'wp:post_date').text = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            ET.SubElement(item, 'wp:post_type').text = 'post'
            ET.SubElement(item, 'wp:status').text = 'draft'
            ET.SubElement(item, 'wp:post_name').text = content.get('slug', '')
            ET.SubElement(item, 'wp:is_sticky').text = '0'
            
            # Add category based on content type
            category = ET.SubElement(item, 'category', {
                'domain': 'category',
                'nicename': content.get('template_used', 'general')
            })
            category.text = self._format_category(content.get('template_used', 'general'))
            
            # Add tags from keywords
            if content.get('keyword'):
                for tag in content['keyword'].split():
                    tag_elem = ET.SubElement(item, 'category', {
                        'domain': 'post_tag',
                        'nicename': tag.lower()
                    })
                    tag_elem.text = tag
        
        # Pretty print XML
        xml_string = self._prettify_xml(rss)
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(xml_string)
            
            logger.info(f"Successfully exported {len(content_list)} items to WordPress XML: {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"Error exporting to WordPress XML: {e}")
            raise
    
    def _wrap_cdata(self, text: str) -> str:
        """Wrap text in CDATA tags."""
        return f"<![CDATA[{text}]]>"
    
    def _format_category(self, template_type: str) -> str:
        """Format template type as category name."""
        return template_type.replace('-', ' ').title()
    
    def _prettify_xml(self, elem: ET.Element) -> str:
        """Return a pretty-printed XML string."""
        rough_string = ET.tostring(elem, encoding='unicode')
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="  ")