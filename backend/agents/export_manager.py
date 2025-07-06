"""Export Manager Agent - Handles multi-format exports with bulk operations and deployment guides"""
import os
import json
import csv
import zipfile
import shutil
import asyncio
import logging
from typing import List, Dict, Any, Optional, Union, Tuple
from datetime import datetime, timedelta
from pathlib import Path
import xml.etree.ElementTree as ET
from xml.dom import minidom
import markdown
import requests
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed

# Import dependencies
from exporters.csv_exporter import CSVExporter
from exporters.wordpress_exporter import WordPressExporter
from agents.page_generator import PageGeneratorAgent
from models import Content, Project, Keyword, get_db
from config import settings

logger = logging.getLogger(__name__)

class ExportManagerAgent:
    """
    Agent responsible for managing exports across multiple formats with bulk operations,
    compression, progress tracking, and deployment guides.
    """
    
    # Supported export formats
    SUPPORTED_FORMATS = {
        'csv': 'Comma-separated values for spreadsheet import',
        'json': 'JSON format for API consumption',
        'wordpress': 'WordPress XML format for direct import',
        'html': 'Static HTML files ready for deployment',
        'markdown': 'Markdown files for static site generators',
        'wordpress_api': 'Direct WordPress API deployment',
        'bulk_zip': 'Compressed archive with multiple formats'
    }
    
    # Export templates/presets
    EXPORT_PRESETS = {
        'basic': {
            'formats': ['csv'],
            'include_metadata': False,
            'compress': False
        },
        'complete': {
            'formats': ['csv', 'json', 'html'],
            'include_metadata': True,
            'compress': True
        },
        'wordpress_ready': {
            'formats': ['wordpress', 'csv'],
            'include_metadata': True,
            'compress': False
        },
        'static_site': {
            'formats': ['markdown', 'json'],
            'include_metadata': True,
            'compress': True,
            'organize_by_category': True
        },
        'api_deployment': {
            'formats': ['json', 'wordpress_api'],
            'include_metadata': True,
            'compress': False,
            'batch_size': 50
        }
    }
    
    def __init__(self):
        """Initialize the Export Manager Agent"""
        self.csv_exporter = CSVExporter()
        self.wordpress_exporter = WordPressExporter()
        self.page_generator = PageGeneratorAgent()
        self.export_history = []
        self.active_exports = {}
        self.export_stats = {
            'total_exports': 0,
            'successful_exports': 0,
            'failed_exports': 0,
            'total_items_exported': 0,
            'formats_used': defaultdict(int)
        }
    
    async def export_content(
        self,
        project_id: int,
        format: Union[str, List[str]],
        options: Optional[Dict[str, Any]] = None,
        preset: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Export content in specified format(s) with options
        
        Args:
            project_id: ID of project to export
            format: Export format(s) - can be string or list
            options: Export options (filters, metadata, etc.)
            preset: Use a predefined export preset
            
        Returns:
            Export result with file paths and statistics
        """
        # Initialize export
        export_id = self._generate_export_id()
        self.active_exports[export_id] = {
            'status': 'initializing',
            'progress': 0,
            'started_at': datetime.now().isoformat()
        }
        
        try:
            # Apply preset if specified
            if preset and preset in self.EXPORT_PRESETS:
                preset_config = self.EXPORT_PRESETS[preset]
                format = preset_config.get('formats', [format] if isinstance(format, str) else format)
                options = {**preset_config, **(options or {})}
            
            # Ensure format is a list
            formats = [format] if isinstance(format, str) else format
            
            # Validate formats
            invalid_formats = [f for f in formats if f not in self.SUPPORTED_FORMATS]
            if invalid_formats:
                raise ValueError(f"Unsupported formats: {invalid_formats}")
            
            # Get content to export
            content_data = await self._get_content_for_export(project_id, options)
            
            if not content_data['content']:
                raise ValueError("No content found for export")
            
            # Update progress
            self.active_exports[export_id]['status'] = 'exporting'
            self.active_exports[export_id]['total_items'] = len(content_data['content'])
            
            # Export in each format
            export_results = {}
            for fmt in formats:
                logger.info(f"Exporting {len(content_data['content'])} items in {fmt} format")
                
                result = await self._export_in_format(
                    content_data,
                    fmt,
                    options or {},
                    export_id
                )
                export_results[fmt] = result
                self.export_stats['formats_used'][fmt] += 1
            
            # Apply compression if requested
            final_path = None
            if options and options.get('compress', False):
                final_path = await self._compress_exports(
                    export_results,
                    content_data['project_name'],
                    export_id
                )
            
            # Generate deployment guide
            deployment_guide = self._generate_deployment_guide(
                formats,
                export_results,
                content_data['project_name']
            )
            
            # Save deployment guide
            guide_path = self._save_deployment_guide(
                deployment_guide,
                content_data['project_name']
            )
            
            # Update export history
            export_record = {
                'export_id': export_id,
                'project_id': project_id,
                'project_name': content_data['project_name'],
                'formats': formats,
                'item_count': len(content_data['content']),
                'options': options,
                'results': export_results,
                'compressed_path': final_path,
                'deployment_guide': guide_path,
                'completed_at': datetime.now().isoformat(),
                'duration': (datetime.now() - datetime.fromisoformat(
                    self.active_exports[export_id]['started_at']
                )).total_seconds()
            }
            
            self.export_history.append(export_record)
            self.export_stats['total_exports'] += 1
            self.export_stats['successful_exports'] += 1
            self.export_stats['total_items_exported'] += len(content_data['content'])
            
            # Clean up active export
            self.active_exports[export_id]['status'] = 'completed'
            self.active_exports[export_id]['progress'] = 100
            
            return {
                'success': True,
                'export_id': export_id,
                'formats': formats,
                'item_count': len(content_data['content']),
                'files': export_results,
                'compressed_file': final_path,
                'deployment_guide': guide_path,
                'duration': export_record['duration']
            }
            
        except Exception as e:
            logger.error(f"Export failed: {str(e)}")
            self.active_exports[export_id]['status'] = 'failed'
            self.active_exports[export_id]['error'] = str(e)
            self.export_stats['failed_exports'] += 1
            
            return {
                'success': False,
                'export_id': export_id,
                'error': str(e)
            }
    
    async def bulk_export(
        self,
        project_ids: List[int],
        format: Union[str, List[str]],
        options: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Export multiple projects in bulk
        
        Args:
            project_ids: List of project IDs to export
            format: Export format(s)
            options: Export options
            
        Returns:
            Bulk export results
        """
        bulk_export_id = self._generate_export_id()
        results = {
            'bulk_export_id': bulk_export_id,
            'total_projects': len(project_ids),
            'successful': 0,
            'failed': 0,
            'project_results': {}
        }
        
        # Process projects in parallel with thread pool
        with ThreadPoolExecutor(max_workers=5) as executor:
            future_to_project = {
                executor.submit(
                    asyncio.run,
                    self.export_content(pid, format, options)
                ): pid
                for pid in project_ids
            }
            
            for future in as_completed(future_to_project):
                project_id = future_to_project[future]
                try:
                    result = future.result()
                    results['project_results'][project_id] = result
                    if result['success']:
                        results['successful'] += 1
                    else:
                        results['failed'] += 1
                except Exception as e:
                    logger.error(f"Bulk export failed for project {project_id}: {str(e)}")
                    results['project_results'][project_id] = {
                        'success': False,
                        'error': str(e)
                    }
                    results['failed'] += 1
        
        # Create master archive if requested
        if options and options.get('create_master_archive', True):
            master_archive = await self._create_master_archive(
                results['project_results'],
                bulk_export_id
            )
            results['master_archive'] = master_archive
        
        return results
    
    async def schedule_export(
        self,
        project_id: int,
        format: Union[str, List[str]],
        schedule: Dict[str, Any],
        options: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Schedule an export for later execution
        
        Args:
            project_id: Project to export
            format: Export format(s)
            schedule: Schedule configuration (cron, interval, etc.)
            options: Export options
            
        Returns:
            Scheduled export information
        """
        scheduled_export = {
            'schedule_id': self._generate_export_id(),
            'project_id': project_id,
            'format': format,
            'schedule': schedule,
            'options': options,
            'created_at': datetime.now().isoformat(),
            'next_run': self._calculate_next_run(schedule),
            'status': 'scheduled'
        }
        
        # In a production system, this would integrate with a task scheduler
        # For now, we'll just log it
        logger.info(f"Scheduled export created: {scheduled_export['schedule_id']}")
        
        return scheduled_export
    
    def get_export_progress(self, export_id: str) -> Dict[str, Any]:
        """Get progress of an active export"""
        if export_id in self.active_exports:
            return self.active_exports[export_id]
        
        # Check history
        for export in self.export_history:
            if export['export_id'] == export_id:
                return {
                    'status': 'completed',
                    'progress': 100,
                    'completed_at': export['completed_at'],
                    'results': export['results']
                }
        
        return {
            'status': 'not_found',
            'error': f'Export {export_id} not found'
        }
    
    def get_export_history(
        self,
        project_id: Optional[int] = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Get export history, optionally filtered by project"""
        history = self.export_history
        
        if project_id:
            history = [h for h in history if h.get('project_id') == project_id]
        
        # Sort by completed_at descending
        history.sort(key=lambda x: x.get('completed_at', ''), reverse=True)
        
        return history[:limit]
    
    def validate_export_format(
        self,
        content: List[Dict[str, Any]],
        format: str
    ) -> Dict[str, Any]:
        """
        Validate content before export
        
        Args:
            content: Content to validate
            format: Target export format
            
        Returns:
            Validation results
        """
        validation = {
            'valid': True,
            'errors': [],
            'warnings': [],
            'item_count': len(content)
        }
        
        # Format-specific validation
        if format == 'wordpress':
            # Check required fields
            for idx, item in enumerate(content):
                if not item.get('title'):
                    validation['errors'].append(f"Item {idx}: Missing title")
                if not item.get('content_html') and not item.get('content'):
                    validation['errors'].append(f"Item {idx}: Missing content")
                if len(item.get('title', '')) > 200:
                    validation['warnings'].append(f"Item {idx}: Title exceeds recommended length")
        
        elif format == 'html':
            # Check for valid HTML content
            for idx, item in enumerate(content):
                if not item.get('slug'):
                    validation['errors'].append(f"Item {idx}: Missing slug for filename")
                if not item.get('content_html') and not item.get('content'):
                    validation['warnings'].append(f"Item {idx}: No HTML content found")
        
        elif format == 'markdown':
            # Check for content that can be converted
            for idx, item in enumerate(content):
                if not item.get('content_markdown') and not item.get('content'):
                    validation['warnings'].append(f"Item {idx}: No markdown content found")
        
        # General validation
        if not content:
            validation['errors'].append("No content to export")
        
        if validation['errors']:
            validation['valid'] = False
        
        return validation
    
    def get_export_stats(self) -> Dict[str, Any]:
        """Get export statistics"""
        return {
            **self.export_stats,
            'active_exports': len(self.active_exports),
            'history_count': len(self.export_history),
            'most_used_format': max(
                self.export_stats['formats_used'].items(),
                key=lambda x: x[1]
            )[0] if self.export_stats['formats_used'] else None,
            'average_export_duration': self._calculate_average_duration()
        }
    
    # Private helper methods
    
    async def _get_content_for_export(
        self,
        project_id: int,
        options: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Get content from database for export"""
        db = next(get_db())
        
        try:
            # Get project
            project = db.query(Project).filter(Project.id == project_id).first()
            if not project:
                raise ValueError(f"Project {project_id} not found")
            
            # Build query
            query = db.query(Content).filter(Content.project_id == project_id)
            
            # Apply filters from options
            if options.get('status'):
                query = query.filter(Content.status == options['status'])
            
            if options.get('template_used'):
                query = query.filter(Content.template_used == options['template_used'])
            
            if options.get('date_from'):
                query = query.filter(Content.created_at >= options['date_from'])
            
            if options.get('date_to'):
                query = query.filter(Content.created_at <= options['date_to'])
            
            # Get content
            content_items = query.all()
            
            # Convert to dict format
            content_data = []
            for item in content_items:
                data = {
                    'id': item.id,
                    'title': item.title,
                    'slug': item.slug,
                    'meta_description': item.meta_description,
                    'content_html': item.content_html,
                    'content_markdown': item.content_markdown,
                    'content': item.content_html or item.content_markdown,
                    'word_count': item.word_count,
                    'template_used': item.template_used,
                    'status': item.status,
                    'created_at': item.created_at.isoformat() if item.created_at else None,
                    'keyword': item.keyword.keyword if item.keyword else None
                }
                
                # Include metadata if requested
                if options.get('include_metadata', True):
                    data['metadata'] = {
                        'project_name': project.name,
                        'industry': project.industry,
                        'variation_number': item.variation_number,
                        'published_url': item.published_url
                    }
                
                content_data.append(data)
            
            return {
                'project_name': project.name,
                'project_id': project_id,
                'content': content_data,
                'total_count': len(content_data)
            }
            
        finally:
            db.close()
    
    async def _export_in_format(
        self,
        content_data: Dict[str, Any],
        format: str,
        options: Dict[str, Any],
        export_id: str
    ) -> Dict[str, Any]:
        """Export content in specific format"""
        project_name = content_data['project_name']
        content = content_data['content']
        
        # Validate before export
        validation = self.validate_export_format(content, format)
        if not validation['valid']:
            raise ValueError(f"Validation failed: {validation['errors']}")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if format == 'csv':
            # Use existing CSV exporter
            filepath = self.csv_exporter.export_content(content, project_name)
            return {
                'format': 'csv',
                'filepath': filepath,
                'item_count': len(content)
            }
        
        elif format == 'json':
            # Export as JSON
            filename = f"{project_name}_{timestamp}.json"
            filepath = os.path.join(settings.exports_dir, filename)
            
            export_data = {
                'project': project_name,
                'exported_at': datetime.now().isoformat(),
                'item_count': len(content),
                'content': content
            }
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)
            
            return {
                'format': 'json',
                'filepath': filepath,
                'item_count': len(content)
            }
        
        elif format == 'wordpress':
            # Use existing WordPress exporter
            site_url = options.get('site_url', 'https://example.com')
            filepath = self.wordpress_exporter.export_content(
                content,
                project_name,
                site_url
            )
            return {
                'format': 'wordpress',
                'filepath': filepath,
                'item_count': len(content)
            }
        
        elif format == 'html':
            # Export as HTML files
            export_dir = os.path.join(
                settings.exports_dir,
                f"{project_name}_html_{timestamp}"
            )
            os.makedirs(export_dir, exist_ok=True)
            
            # Organize by category if requested
            if options.get('organize_by_category', False):
                for item in content:
                    category = item.get('template_used', 'general')
                    category_dir = os.path.join(export_dir, category)
                    os.makedirs(category_dir, exist_ok=True)
                    
                    filename = f"{item.get('slug', f'page-{item[\"id\"]}')}.html"
                    filepath = os.path.join(category_dir, filename)
                    
                    html_content = self._generate_html_page(item, options)
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(html_content)
            else:
                for item in content:
                    filename = f"{item.get('slug', f'page-{item[\"id\"]}')}.html"
                    filepath = os.path.join(export_dir, filename)
                    
                    html_content = self._generate_html_page(item, options)
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(html_content)
            
            # Create index file
            index_content = self._generate_index_html(content, project_name)
            with open(os.path.join(export_dir, 'index.html'), 'w') as f:
                f.write(index_content)
            
            return {
                'format': 'html',
                'directory': export_dir,
                'item_count': len(content),
                'files_created': len(content) + 1  # +1 for index
            }
        
        elif format == 'markdown':
            # Export as Markdown files
            export_dir = os.path.join(
                settings.exports_dir,
                f"{project_name}_markdown_{timestamp}"
            )
            os.makedirs(export_dir, exist_ok=True)
            
            for item in content:
                # Convert content to markdown if needed
                if item.get('content_markdown'):
                    md_content = item['content_markdown']
                else:
                    # Basic HTML to markdown conversion
                    md_content = self._html_to_markdown(item.get('content_html', ''))
                
                # Add frontmatter
                frontmatter = self._generate_frontmatter(item)
                full_content = f"{frontmatter}\n\n# {item['title']}\n\n{md_content}"
                
                filename = f"{item.get('slug', f'page-{item["id"]}')}.md"
                filepath = os.path.join(export_dir, filename)
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(full_content)
            
            return {
                'format': 'markdown',
                'directory': export_dir,
                'item_count': len(content)
            }
        
        elif format == 'wordpress_api':
            # Direct WordPress API deployment
            if not all([settings.wordpress_url, settings.wordpress_username, settings.wordpress_app_password]):
                raise ValueError("WordPress API credentials not configured")
            
            results = await self._deploy_to_wordpress_api(content, options)
            
            return {
                'format': 'wordpress_api',
                'deployment_results': results,
                'item_count': len(content)
            }
        
        else:
            raise ValueError(f"Unsupported format: {format}")
    
    def _generate_html_page(self, item: Dict[str, Any], options: Dict[str, Any]) -> str:
        """Generate complete HTML page"""
        template = options.get('html_template', '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <meta name="description" content="{meta_description}">
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; color: #333; max-width: 800px; margin: 0 auto; padding: 20px; }}
        h1 {{ color: #2c3e50; margin-bottom: 20px; }}
        h2 {{ color: #34495e; margin-top: 30px; }}
        p {{ margin-bottom: 15px; }}
        .metadata {{ background: #f8f9fa; padding: 15px; border-radius: 5px; margin-bottom: 30px; font-size: 0.9em; color: #666; }}
    </style>
</head>
<body>
    <div class="metadata">
        <strong>Published:</strong> {created_at}<br>
        <strong>Category:</strong> {template_used}<br>
        <strong>Word Count:</strong> {word_count}
    </div>
    {content}
</body>
</html>''')
        
        return template.format(
            title=item.get('title', 'Untitled'),
            meta_description=item.get('meta_description', ''),
            created_at=item.get('created_at', 'Unknown'),
            template_used=item.get('template_used', 'General'),
            word_count=item.get('word_count', 0),
            content=item.get('content_html', item.get('content', ''))
        )
    
    def _generate_index_html(self, content: List[Dict[str, Any]], project_name: str) -> str:
        """Generate index HTML page"""
        items_html = ""
        
        # Group by category
        by_category = defaultdict(list)
        for item in content:
            category = item.get('template_used', 'general')
            by_category[category].append(item)
        
        for category, items in by_category.items():
            items_html += f"<h2>{category.replace('-', ' ').title()}</h2>\n<ul>\n"
            for item in items:
                slug = item.get('slug', f"page-{item['id']}")
                items_html += f'  <li><a href="{slug}.html">{item["title"]}</a></li>\n'
            items_html += "</ul>\n"
        
        return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{project_name} - Content Index</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; color: #333; max-width: 800px; margin: 0 auto; padding: 20px; }}
        h1 {{ color: #2c3e50; }}
        h2 {{ color: #34495e; margin-top: 30px; }}
        ul {{ list-style-type: none; padding-left: 0; }}
        li {{ margin-bottom: 10px; }}
        a {{ color: #3498db; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
        .stats {{ background: #f8f9fa; padding: 20px; border-radius: 5px; margin-bottom: 30px; }}
    </style>
</head>
<body>
    <h1>{project_name} - Content Index</h1>
    <div class="stats">
        <strong>Total Pages:</strong> {len(content)}<br>
        <strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    </div>
    {items_html}
</body>
</html>'''
    
    def _generate_frontmatter(self, item: Dict[str, Any]) -> str:
        """Generate frontmatter for markdown files"""
        frontmatter = {
            'title': item.get('title', 'Untitled'),
            'date': item.get('created_at', datetime.now().isoformat()),
            'description': item.get('meta_description', ''),
            'slug': item.get('slug', ''),
            'categories': [item.get('template_used', 'general')],
            'tags': item.get('keyword', '').split() if item.get('keyword') else [],
            'draft': item.get('status') != 'published'
        }
        
        # Convert to YAML frontmatter
        lines = ['---']
        for key, value in frontmatter.items():
            if isinstance(value, list):
                lines.append(f"{key}:")
                for v in value:
                    lines.append(f"  - {v}")
            elif isinstance(value, bool):
                lines.append(f"{key}: {str(value).lower()}")
            else:
                lines.append(f"{key}: {value}")
        lines.append('---')
        
        return '\n'.join(lines)
    
    def _html_to_markdown(self, html: str) -> str:
        """Basic HTML to Markdown conversion"""
        # This is a simplified conversion - in production, use a proper library
        import re
        
        # Remove script and style tags
        html = re.sub(r'<script.*?</script>', '', html, flags=re.DOTALL)
        html = re.sub(r'<style.*?</style>', '', html, flags=re.DOTALL)
        
        # Convert headers
        for i in range(6, 0, -1):
            html = re.sub(f'<h{i}>(.*?)</h{i}>', lambda m: f"{'#' * i} {m.group(1)}", html)
        
        # Convert paragraphs
        html = re.sub(r'<p>(.*?)</p>', r'\1\n\n', html)
        
        # Convert links
        html = re.sub(r'<a href="(.*?)">(.*?)</a>', r'[\2](\1)', html)
        
        # Convert bold and italic
        html = re.sub(r'<strong>(.*?)</strong>', r'**\1**', html)
        html = re.sub(r'<b>(.*?)</b>', r'**\1**', html)
        html = re.sub(r'<em>(.*?)</em>', r'*\1*', html)
        html = re.sub(r'<i>(.*?)</i>', r'*\1*', html)
        
        # Convert lists
        html = re.sub(r'<li>(.*?)</li>', r'- \1', html)
        html = re.sub(r'<ul>|</ul>', '', html)
        html = re.sub(r'<ol>|</ol>', '', html)
        
        # Remove remaining tags
        html = re.sub(r'<[^>]+>', '', html)
        
        # Clean up whitespace
        html = re.sub(r'\n{3,}', '\n\n', html)
        
        return html.strip()
    
    async def _deploy_to_wordpress_api(
        self,
        content: List[Dict[str, Any]],
        options: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Deploy content directly to WordPress via API"""
        results = []
        batch_size = options.get('batch_size', 10)
        
        # WordPress API endpoint
        api_url = f"{settings.wordpress_url}/wp-json/wp/v2/posts"
        
        # Authentication
        auth = (settings.wordpress_username, settings.wordpress_app_password)
        
        # Process in batches
        for i in range(0, len(content), batch_size):
            batch = content[i:i + batch_size]
            
            for item in batch:
                try:
                    # Prepare post data
                    post_data = {
                        'title': item['title'],
                        'content': item.get('content_html', item.get('content', '')),
                        'excerpt': item.get('meta_description', ''),
                        'status': options.get('post_status', 'draft'),
                        'categories': [],  # Would need category mapping
                        'tags': [],  # Would need tag mapping
                    }
                    
                    # Make API request
                    response = requests.post(
                        api_url,
                        json=post_data,
                        auth=auth,
                        headers={'Content-Type': 'application/json'}
                    )
                    
                    if response.status_code == 201:
                        result = response.json()
                        results.append({
                            'success': True,
                            'post_id': result['id'],
                            'url': result['link'],
                            'title': item['title']
                        })
                    else:
                        results.append({
                            'success': False,
                            'title': item['title'],
                            'error': f"API error: {response.status_code} - {response.text}"
                        })
                    
                except Exception as e:
                    results.append({
                        'success': False,
                        'title': item['title'],
                        'error': str(e)
                    })
                
                # Rate limiting
                await asyncio.sleep(0.5)
        
        return results
    
    async def _compress_exports(
        self,
        export_results: Dict[str, Dict[str, Any]],
        project_name: str,
        export_id: str
    ) -> str:
        """Compress all export files into a single archive"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        archive_name = f"{project_name}_export_{timestamp}.zip"
        archive_path = os.path.join(settings.exports_dir, archive_name)
        
        with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for format, result in export_results.items():
                if 'filepath' in result:
                    # Single file
                    arcname = os.path.basename(result['filepath'])
                    zipf.write(result['filepath'], arcname)
                elif 'directory' in result:
                    # Directory of files
                    for root, dirs, files in os.walk(result['directory']):
                        for file in files:
                            file_path = os.path.join(root, file)
                            arcname = os.path.relpath(file_path, settings.exports_dir)
                            zipf.write(file_path, arcname)
        
        logger.info(f"Created archive: {archive_path}")
        return archive_path
    
    def _generate_deployment_guide(
        self,
        formats: List[str],
        results: Dict[str, Dict[str, Any]],
        project_name: str
    ) -> str:
        """Generate deployment instructions for exported content"""
        guide = f"""# Deployment Guide for {project_name}

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Export Summary

You have successfully exported your content in the following formats:

"""
        
        for fmt in formats:
            if fmt in results:
                result = results[fmt]
                guide += f"- **{fmt.upper()}**: {result.get('item_count', 0)} items\n"
                if 'filepath' in result:
                    guide += f"  - File: `{os.path.basename(result['filepath'])}`\n"
                elif 'directory' in result:
                    guide += f"  - Directory: `{os.path.basename(result['directory'])}`\n"
        
        guide += "\n## Deployment Instructions by Format\n\n"
        
        # Format-specific instructions
        if 'csv' in formats:
            guide += """### CSV Deployment

1. **Import to CMS**:
   - Most CMS platforms support CSV import
   - Map columns: title, slug, meta_description, content, etc.
   - Set appropriate publish status

2. **Spreadsheet Analysis**:
   - Open in Excel/Google Sheets for review
   - Use filters to organize by content type
   - Bulk edit metadata if needed

"""
        
        if 'wordpress' in formats:
            guide += """### WordPress XML Deployment

1. **Import via WordPress Admin**:
   - Go to Tools > Import > WordPress
   - Upload the XML file
   - Assign authors and download attachments
   - Review import settings

2. **Post-Import Tasks**:
   - Set featured images
   - Configure permalinks
   - Assign categories/tags
   - Review and publish drafts

"""
        
        if 'html' in formats:
            guide += """### HTML Files Deployment

1. **Static Hosting**:
   - Upload entire directory to web server
   - Ensure index.html is in root
   - Configure server for clean URLs

2. **CDN Deployment**:
   - Use services like Netlify, Vercel, or GitHub Pages
   - Deploy directory as static site
   - Configure custom domain

3. **Integration with CMS**:
   - Import HTML content into page builders
   - Preserve formatting and structure
   - Update internal links

"""
        
        if 'markdown' in formats:
            guide += """### Markdown Files Deployment

1. **Static Site Generators**:
   - **Hugo**: Place in content/ directory
   - **Jekyll**: Place in _posts/ with proper naming
   - **Gatsby**: Import via gatsby-source-filesystem
   - **Next.js**: Use in pages/ or with MDX

2. **GitHub/GitLab**:
   - Create repository for content
   - Use built-in rendering for preview
   - Set up CI/CD for automatic deployment

3. **CMS Integration**:
   - Netlify CMS: Configure collections
   - Forestry.io: Import as content sections
   - Strapi: Use markdown field type

"""
        
        if 'wordpress_api' in formats:
            guide += """### WordPress API Deployment

Your content has been deployed directly to WordPress via API.

**Post-Deployment Tasks**:
1. Review posts in WordPress admin
2. Set featured images
3. Assign categories and tags
4. Schedule or publish posts
5. Configure SEO settings

"""
        
        # General best practices
        guide += """## Best Practices

### SEO Optimization
1. **URL Structure**: Ensure URLs match your site structure
2. **Internal Linking**: Update links to match production URLs
3. **Meta Tags**: Verify all meta descriptions are unique
4. **Sitemaps**: Generate and submit XML sitemaps

### Content Review
1. **Quality Check**: Review a sample of pages for formatting
2. **Image Optimization**: Add alt text and compress images
3. **Mobile Preview**: Test responsive design
4. **Load Testing**: Check page performance

### Monitoring
1. **Analytics Setup**: Add tracking codes
2. **Search Console**: Submit pages for indexing
3. **Performance Monitoring**: Set up page speed tracking
4. **Error Tracking**: Monitor 404s and other errors

## Troubleshooting

### Common Issues

**Import Failures**:
- Check file encoding (UTF-8 recommended)
- Verify required fields are present
- Reduce batch size for large imports

**Formatting Problems**:
- Review HTML/Markdown conversion
- Check for special characters
- Validate against target platform requirements

**Performance Issues**:
- Implement pagination for large archives
- Use CDN for static assets
- Enable caching where possible

## Support

For additional help with deployment:
- Review platform-specific documentation
- Test with small batches first
- Keep backups of original exports

"""
        
        return guide
    
    def _save_deployment_guide(self, guide: str, project_name: str) -> str:
        """Save deployment guide to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{project_name}_deployment_guide_{timestamp}.md"
        filepath = os.path.join(settings.exports_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(guide)
        
        return filepath
    
    async def _create_master_archive(
        self,
        project_results: Dict[int, Dict[str, Any]],
        bulk_export_id: str
    ) -> str:
        """Create master archive for bulk export"""
        archive_name = f"bulk_export_{bulk_export_id}.zip"
        archive_path = os.path.join(settings.exports_dir, archive_name)
        
        with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for project_id, result in project_results.items():
                if result.get('success') and 'files' in result:
                    # Create project subdirectory in archive
                    project_prefix = f"project_{project_id}/"
                    
                    for format, file_info in result['files'].items():
                        if 'filepath' in file_info:
                            arcname = project_prefix + os.path.basename(file_info['filepath'])
                            zipf.write(file_info['filepath'], arcname)
                        elif 'directory' in file_info:
                            for root, dirs, files in os.walk(file_info['directory']):
                                for file in files:
                                    file_path = os.path.join(root, file)
                                    rel_path = os.path.relpath(file_path, file_info['directory'])
                                    arcname = project_prefix + format + "/" + rel_path
                                    zipf.write(file_path, arcname)
        
        return archive_path
    
    def _generate_export_id(self) -> str:
        """Generate unique export ID"""
        return f"export_{datetime.now().strftime('%Y%m%d%H%M%S')}_{os.urandom(4).hex()}"
    
    def _calculate_next_run(self, schedule: Dict[str, Any]) -> str:
        """Calculate next run time for scheduled export"""
        # Simplified implementation - in production, use proper scheduling library
        if schedule.get('interval') == 'daily':
            next_run = datetime.now().replace(hour=0, minute=0, second=0) + timedelta(days=1)
        elif schedule.get('interval') == 'weekly':
            next_run = datetime.now() + timedelta(days=7)
        else:
            next_run = datetime.now() + timedelta(hours=1)
        
        return next_run.isoformat()
    
    def _calculate_average_duration(self) -> float:
        """Calculate average export duration"""
        durations = [
            h.get('duration', 0)
            for h in self.export_history
            if 'duration' in h
        ]
        
        return sum(durations) / len(durations) if durations else 0.0