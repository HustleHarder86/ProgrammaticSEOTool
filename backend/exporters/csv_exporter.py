"""CSV export functionality."""
import csv
import os
from typing import List, Dict
from datetime import datetime
from config import settings
import logging

logger = logging.getLogger(__name__)

class CSVExporter:
    """Export content to CSV format."""
    
    def export_content(self, content_list: List[Dict], project_name: str) -> str:
        """Export content list to CSV file."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{project_name}_{timestamp}.csv"
        filepath = os.path.join(settings.EXPORTS_DIR, filename)
        
        # Ensure exports directory exists
        os.makedirs(settings.EXPORTS_DIR, exist_ok=True)
        
        # Define CSV columns
        fieldnames = [
            'title',
            'slug',
            'meta_description',
            'keyword',
            'content_type',
            'word_count',
            'content_markdown',
            'content_html',
            'status',
            'created_at'
        ]
        
        try:
            with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                
                for content in content_list:
                    row = {
                        'title': content.get('title', ''),
                        'slug': content.get('slug', ''),
                        'meta_description': content.get('meta_description', ''),
                        'keyword': content.get('keyword', ''),
                        'content_type': content.get('template_used', ''),
                        'word_count': content.get('word_count', 0),
                        'content_markdown': content.get('content_markdown', ''),
                        'content_html': content.get('content_html', ''),
                        'status': content.get('status', 'ready'),
                        'created_at': content.get('created_at', datetime.now().isoformat())
                    }
                    writer.writerow(row)
            
            logger.info(f"Successfully exported {len(content_list)} items to {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"Error exporting to CSV: {e}")
            raise
    
    def export_keywords(self, keywords: List[Dict], project_name: str) -> str:
        """Export keywords to CSV file."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{project_name}_keywords_{timestamp}.csv"
        filepath = os.path.join(settings.EXPORTS_DIR, filename)
        
        # Ensure exports directory exists
        os.makedirs(settings.EXPORTS_DIR, exist_ok=True)
        
        # Define CSV columns
        fieldnames = [
            'keyword',
            'content_type',
            'priority',
            'search_intent',
            'estimated_difficulty',
            'title_template',
            'status'
        ]
        
        try:
            with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                
                for kw in keywords:
                    row = {
                        'keyword': kw.get('keyword', ''),
                        'content_type': kw.get('content_type', ''),
                        'priority': kw.get('priority', 5),
                        'search_intent': kw.get('search_intent', 'informational'),
                        'estimated_difficulty': kw.get('estimated_difficulty', 5),
                        'title_template': kw.get('title_template', ''),
                        'status': kw.get('status', 'pending')
                    }
                    writer.writerow(row)
            
            logger.info(f"Successfully exported {len(keywords)} keywords to {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"Error exporting keywords to CSV: {e}")
            raise