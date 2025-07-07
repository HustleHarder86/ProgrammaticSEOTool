"""JSON export functionality for programmatic SEO content."""
import json
import os
from typing import List, Dict, Any
from datetime import datetime
from pathlib import Path

from config import settings
import logging

logger = logging.getLogger(__name__)


class JSONExporter:
    """Export content to JSON format with various structure options."""
    
    def __init__(self):
        """Initialize the JSON exporter."""
        self.exports_dir = Path(settings.EXPORTS_DIR)
        self.exports_dir.mkdir(parents=True, exist_ok=True)
    
    def export_content(
        self,
        content_list: List[Dict[str, Any]],
        project_name: str,
        export_options: Dict[str, Any] = None
    ) -> str:
        """Export content list to JSON file with configurable structure."""
        if export_options is None:
            export_options = {}
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{project_name}_export_{timestamp}.json"
        filepath = self.exports_dir / filename
        
        # Build export structure based on options
        export_structure = export_options.get('structure', 'flat')
        
        if export_structure == 'nested':
            export_data = self._create_nested_structure(content_list, project_name)
        elif export_structure == 'grouped':
            export_data = self._create_grouped_structure(content_list, project_name)
        elif export_structure == 'api_ready':
            export_data = self._create_api_ready_structure(content_list, project_name)
        else:
            export_data = self._create_flat_structure(content_list, project_name)
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(
                    export_data,
                    f,
                    indent=2,
                    ensure_ascii=False,
                    separators=(',', ': ')
                )
            
            logger.info(f"Successfully exported {len(content_list)} items to JSON: {filepath}")
            return str(filepath)
            
        except Exception as e:
            logger.error(f"Error exporting to JSON: {e}")
            raise
    
    def _create_flat_structure(self, content_list: List[Dict[str, Any]], project_name: str) -> Dict[str, Any]:
        """Create a flat JSON structure with all content in an array."""
        return {
            'export_info': {
                'project_name': project_name,
                'export_format': 'json',
                'export_date': datetime.now().isoformat(),
                'total_items': len(content_list),
                'structure': 'flat'
            },
            'content': content_list
        }
    
    def _create_nested_structure(self, content_list: List[Dict[str, Any]], project_name: str) -> Dict[str, Any]:
        """Create a nested JSON structure organized by template/category."""
        nested_data = {}
        
        for item in content_list:
            template_type = item.get('template_used', 'general')
            
            if template_type not in nested_data:
                nested_data[template_type] = {
                    'category': template_type,
                    'count': 0,
                    'pages': []
                }
            
            nested_data[template_type]['pages'].append(item)
            nested_data[template_type]['count'] += 1
        
        return {
            'export_info': {
                'project_name': project_name,
                'export_format': 'json',
                'export_date': datetime.now().isoformat(),
                'total_items': len(content_list),
                'structure': 'nested',
                'categories': list(nested_data.keys())
            },
            'content': nested_data
        }
    
    def _create_grouped_structure(self, content_list: List[Dict[str, Any]], project_name: str) -> Dict[str, Any]:
        """Create a grouped JSON structure with metadata and content separated."""
        metadata = []
        content = []
        
        for item in content_list:
            # Extract metadata
            meta_item = {
                'id': item.get('id'),
                'title': item.get('title', ''),
                'slug': item.get('slug', ''),
                'meta_description': item.get('meta_description', ''),
                'keyword': item.get('keyword', ''),
                'template_used': item.get('template_used', ''),
                'word_count': item.get('word_count', 0),
                'created_at': item.get('created_at', ''),
                'variables': item.get('variables', {})
            }
            metadata.append(meta_item)
            
            # Extract content
            content_item = {
                'id': item.get('id'),
                'content_html': item.get('content_html', ''),
                'content_markdown': item.get('content_markdown', ''),
                'content': item.get('content', '')
            }
            content.append(content_item)
        
        return {
            'export_info': {
                'project_name': project_name,
                'export_format': 'json',
                'export_date': datetime.now().isoformat(),
                'total_items': len(content_list),
                'structure': 'grouped'
            },
            'metadata': metadata,
            'content': content
        }
    
    def _create_api_ready_structure(self, content_list: List[Dict[str, Any]], project_name: str) -> Dict[str, Any]:
        """Create an API-ready JSON structure optimized for REST API consumption."""
        pages = []
        
        for item in content_list:
            # Create API-friendly page object
            page = {
                'id': item.get('id'),
                'type': 'page',
                'attributes': {
                    'title': item.get('title', ''),
                    'slug': item.get('slug', ''),
                    'meta_description': item.get('meta_description', ''),
                    'content': {
                        'html': item.get('content_html', ''),
                        'markdown': item.get('content_markdown', ''),
                        'text': self._strip_html(item.get('content_html', ''))
                    },
                    'seo': {
                        'title': item.get('title', ''),
                        'description': item.get('meta_description', ''),
                        'keywords': item.get('keyword', '').split(',') if item.get('keyword') else []
                    },
                    'template': item.get('template_used', ''),
                    'variables': item.get('variables', {}),
                    'stats': {
                        'word_count': item.get('word_count', 0),
                        'character_count': len(item.get('content_html', ''))
                    },
                    'timestamps': {
                        'created_at': item.get('created_at', ''),
                        'updated_at': item.get('created_at', '')
                    }
                },
                'relationships': {
                    'project': {
                        'data': {
                            'type': 'project',
                            'id': item.get('metadata', {}).get('project_id', '')
                        }
                    }
                }
            }
            pages.append(page)
        
        return {
            'data': pages,
            'meta': {
                'total_count': len(content_list),
                'project_name': project_name,
                'export_date': datetime.now().isoformat(),
                'format': 'json_api',
                'version': '1.0'
            },
            'links': {
                'self': f'/api/projects/{project_name}/export'
            }
        }
    
    def export_sitemap_json(self, content_list: List[Dict[str, Any]], project_name: str, base_url: str = None) -> str:
        """Export content as a JSON sitemap structure."""
        if base_url is None:
            base_url = "https://example.com"
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{project_name}_sitemap_{timestamp}.json"
        filepath = self.exports_dir / filename
        
        sitemap_data = {
            'sitemap_info': {
                'project_name': project_name,
                'base_url': base_url,
                'generated_at': datetime.now().isoformat(),
                'total_urls': len(content_list)
            },
            'urls': []
        }
        
        for item in content_list:
            url_data = {
                'loc': f"{base_url.rstrip('/')}/{item.get('slug', '')}",
                'lastmod': item.get('created_at', datetime.now().isoformat()),
                'changefreq': 'weekly',
                'priority': self._calculate_priority(item),
                'title': item.get('title', ''),
                'description': item.get('meta_description', ''),
                'keywords': item.get('keyword', '').split(',') if item.get('keyword') else [],
                'word_count': item.get('word_count', 0),
                'template': item.get('template_used', '')
            }
            sitemap_data['urls'].append(url_data)
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(sitemap_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Successfully exported sitemap JSON: {filepath}")
            return str(filepath)
            
        except Exception as e:
            logger.error(f"Error exporting sitemap JSON: {e}")
            raise
    
    def export_analytics_json(self, content_list: List[Dict[str, Any]], project_name: str) -> str:
        """Export content with analytics-focused structure."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{project_name}_analytics_{timestamp}.json"
        filepath = self.exports_dir / filename
        
        # Calculate analytics data
        total_word_count = sum(item.get('word_count', 0) for item in content_list)
        avg_word_count = total_word_count / len(content_list) if content_list else 0
        
        # Group by template
        template_stats = {}
        for item in content_list:
            template = item.get('template_used', 'unknown')
            if template not in template_stats:
                template_stats[template] = {
                    'count': 0,
                    'total_words': 0,
                    'avg_words': 0
                }
            template_stats[template]['count'] += 1
            template_stats[template]['total_words'] += item.get('word_count', 0)
        
        # Calculate averages
        for template, stats in template_stats.items():
            stats['avg_words'] = stats['total_words'] / stats['count'] if stats['count'] > 0 else 0
        
        analytics_data = {
            'project_analytics': {
                'project_name': project_name,
                'analysis_date': datetime.now().isoformat(),
                'summary': {
                    'total_pages': len(content_list),
                    'total_words': total_word_count,
                    'average_words_per_page': round(avg_word_count, 2),
                    'unique_templates': len(template_stats),
                    'templates_used': list(template_stats.keys())
                },
                'template_breakdown': template_stats
            },
            'pages': [
                {
                    'id': item.get('id'),
                    'title': item.get('title', ''),
                    'slug': item.get('slug', ''),
                    'template': item.get('template_used', ''),
                    'word_count': item.get('word_count', 0),
                    'keyword': item.get('keyword', ''),
                    'meta_description_length': len(item.get('meta_description', '')),
                    'created_at': item.get('created_at', ''),
                    'variables': item.get('variables', {}),
                    'estimated_reading_time': self._calculate_reading_time(item.get('word_count', 0))
                }
                for item in content_list
            ]
        }
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(analytics_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Successfully exported analytics JSON: {filepath}")
            return str(filepath)
            
        except Exception as e:
            logger.error(f"Error exporting analytics JSON: {e}")
            raise
    
    def _strip_html(self, html_content: str) -> str:
        """Strip HTML tags from content to get plain text."""
        import re
        # Remove HTML tags
        clean_text = re.sub(r'<[^>]+>', '', html_content)
        # Clean up extra whitespace
        clean_text = re.sub(r'\s+', ' ', clean_text).strip()
        return clean_text
    
    def _calculate_priority(self, item: Dict[str, Any]) -> float:
        """Calculate URL priority based on content characteristics."""
        # Base priority
        priority = 0.5
        
        # Boost for longer content
        word_count = item.get('word_count', 0)
        if word_count > 1000:
            priority += 0.3
        elif word_count > 500:
            priority += 0.2
        elif word_count > 200:
            priority += 0.1
        
        # Boost for having meta description
        if item.get('meta_description'):
            priority += 0.1
        
        # Boost for having keywords
        if item.get('keyword'):
            priority += 0.1
        
        # Ensure priority is between 0.1 and 1.0
        return min(max(priority, 0.1), 1.0)
    
    def _calculate_reading_time(self, word_count: int) -> int:
        """Calculate estimated reading time in minutes (assuming 200 words per minute)."""
        if word_count == 0:
            return 0
        return max(1, round(word_count / 200))