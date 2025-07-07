"""Enhanced Export Manager with job management and progress tracking."""
import os
import json
import asyncio
import logging
from typing import Dict, List, Optional, Any, Union
from datetime import datetime, timedelta
from pathlib import Path
from dataclasses import dataclass, asdict
from enum import Enum
from concurrent.futures import ThreadPoolExecutor
import zipfile
import shutil
from sqlalchemy.orm import Session

from config import settings
from database import get_db
from models import Project, GeneratedPage
from exporters.csv_exporter import CSVExporter
from exporters.wordpress_exporter import WordPressExporter
from exporters.json_exporter import JSONExporter
from exporters.html_exporter import HTMLExporter

logger = logging.getLogger(__name__)


class ExportStatus(Enum):
    """Export job status enumeration."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class ExportFormat(Enum):
    """Supported export formats."""
    CSV = "csv"
    JSON = "json"
    WORDPRESS = "wordpress"
    HTML = "html"


@dataclass
class ExportJob:
    """Export job tracking class."""
    id: str
    project_id: str
    format: ExportFormat
    status: ExportStatus
    progress: float
    total_items: int
    processed_items: int
    created_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    error_message: Optional[str] = None
    file_path: Optional[str] = None
    download_url: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class ExportManager:
    """Enhanced export manager with job management and progress tracking."""
    
    def __init__(self):
        """Initialize the export manager."""
        self.csv_exporter = CSVExporter()
        self.wordpress_exporter = WordPressExporter()
        self.json_exporter = JSONExporter()
        self.html_exporter = HTMLExporter()
        
        # Job tracking
        self.active_jobs: Dict[str, ExportJob] = {}
        self.completed_jobs: Dict[str, ExportJob] = {}
        self.executor = ThreadPoolExecutor(max_workers=3)
        
        # Ensure exports directory exists
        self.exports_dir = Path(settings.EXPORTS_DIR)
        self.exports_dir.mkdir(parents=True, exist_ok=True)
    
    def start_export(
        self,
        project_id: str,
        format: Union[str, ExportFormat],
        options: Optional[Dict[str, Any]] = None
    ) -> str:
        """Start a new export job."""
        # Convert format to enum if needed
        if isinstance(format, str):
            try:
                format = ExportFormat(format.lower())
            except ValueError:
                raise ValueError(f"Unsupported export format: {format}")
        
        # Generate unique job ID
        job_id = f"export_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{os.urandom(4).hex()}"
        
        # Create export job
        export_job = ExportJob(
            id=job_id,
            project_id=project_id,
            format=format,
            status=ExportStatus.PENDING,
            progress=0.0,
            total_items=0,
            processed_items=0,
            created_at=datetime.now(),
            metadata=options or {}
        )
        
        # Store job
        self.active_jobs[job_id] = export_job
        
        # Start export in background
        future = self.executor.submit(self._execute_export, job_id)
        
        logger.info(f"Started export job {job_id} for project {project_id} in format {format.value}")
        return job_id
    
    def get_export_status(self, job_id: str) -> Optional[Dict[str, Any]]:
        """Get the status of an export job."""
        # Check active jobs
        if job_id in self.active_jobs:
            job = self.active_jobs[job_id]
            return self._job_to_dict(job)
        
        # Check completed jobs
        if job_id in self.completed_jobs:
            job = self.completed_jobs[job_id]
            return self._job_to_dict(job)
        
        return None
    
    def get_download_url(self, job_id: str) -> Optional[str]:
        """Get the download URL for a completed export."""
        job = self.completed_jobs.get(job_id)
        if job and job.status == ExportStatus.COMPLETED and job.file_path:
            return f"/api/exports/{job_id}/download"
        return None
    
    def get_file_path(self, job_id: str) -> Optional[str]:
        """Get the file path for a completed export."""
        job = self.completed_jobs.get(job_id)
        if job and job.status == ExportStatus.COMPLETED:
            return job.file_path
        return None
    
    def cancel_export(self, job_id: str) -> bool:
        """Cancel an active export job."""
        if job_id in self.active_jobs:
            job = self.active_jobs[job_id]
            if job.status in [ExportStatus.PENDING, ExportStatus.IN_PROGRESS]:
                job.status = ExportStatus.CANCELLED
                logger.info(f"Cancelled export job {job_id}")
                return True
        return False
    
    def list_exports(self, project_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """List all export jobs, optionally filtered by project."""
        all_jobs = list(self.active_jobs.values()) + list(self.completed_jobs.values())
        
        if project_id:
            all_jobs = [job for job in all_jobs if job.project_id == project_id]
        
        # Sort by created_at descending
        all_jobs.sort(key=lambda x: x.created_at, reverse=True)
        
        return [self._job_to_dict(job) for job in all_jobs]
    
    def cleanup_old_exports(self, days_old: int = 7) -> int:
        """Clean up old export files and jobs."""
        cutoff_date = datetime.now() - timedelta(days=days_old)
        cleaned_count = 0
        
        # Clean up completed jobs
        jobs_to_remove = []
        for job_id, job in self.completed_jobs.items():
            if job.completed_at and job.completed_at < cutoff_date:
                # Remove file if it exists
                if job.file_path and os.path.exists(job.file_path):
                    try:
                        os.remove(job.file_path)
                        logger.info(f"Removed old export file: {job.file_path}")
                    except Exception as e:
                        logger.error(f"Error removing file {job.file_path}: {e}")
                
                jobs_to_remove.append(job_id)
                cleaned_count += 1
        
        # Remove old jobs from memory
        for job_id in jobs_to_remove:
            del self.completed_jobs[job_id]
        
        logger.info(f"Cleaned up {cleaned_count} old export jobs")
        return cleaned_count
    
    def _execute_export(self, job_id: str) -> None:
        """Execute the export job."""
        job = self.active_jobs.get(job_id)
        if not job:
            logger.error(f"Export job {job_id} not found")
            return
        
        try:
            # Update job status
            job.status = ExportStatus.IN_PROGRESS
            job.started_at = datetime.now()
            
            # Get database session
            db = next(get_db())
            
            try:
                # Get project and pages
                project = db.query(Project).filter(Project.id == job.project_id).first()
                if not project:
                    raise ValueError(f"Project {job.project_id} not found")
                
                # Get pages to export
                pages_query = db.query(GeneratedPage).filter(
                    GeneratedPage.project_id == job.project_id
                )
                
                # Apply filters from metadata
                if job.metadata:
                    if job.metadata.get('template_id'):
                        pages_query = pages_query.filter(
                            GeneratedPage.template_id == job.metadata['template_id']
                        )
                    
                    if job.metadata.get('limit'):
                        pages_query = pages_query.limit(job.metadata['limit'])
                
                pages = pages_query.all()
                
                if not pages:
                    raise ValueError("No pages found to export")
                
                job.total_items = len(pages)
                
                # Convert pages to export format
                export_data = self._prepare_pages_for_export(pages, project)
                
                # Update progress
                job.progress = 25.0
                job.processed_items = 0
                
                # Execute format-specific export
                if job.format == ExportFormat.CSV:
                    file_path = self._export_csv(export_data, project.name, job)
                elif job.format == ExportFormat.JSON:
                    file_path = self._export_json(export_data, project.name, job)
                elif job.format == ExportFormat.WORDPRESS:
                    file_path = self._export_wordpress(export_data, project.name, job)
                elif job.format == ExportFormat.HTML:
                    file_path = self._export_html(export_data, project.name, job)
                else:
                    raise ValueError(f"Unsupported export format: {job.format}")
                
                # Complete the job
                job.status = ExportStatus.COMPLETED
                job.completed_at = datetime.now()
                job.progress = 100.0
                job.processed_items = job.total_items
                job.file_path = file_path
                job.download_url = f"/api/exports/{job_id}/download"
                
                logger.info(f"Export job {job_id} completed successfully")
                
            finally:
                db.close()
                
        except Exception as e:
            logger.error(f"Export job {job_id} failed: {str(e)}")
            job.status = ExportStatus.FAILED
            job.error_message = str(e)
            job.completed_at = datetime.now()
        
        finally:
            # Move job to completed
            if job_id in self.active_jobs:
                self.completed_jobs[job_id] = self.active_jobs.pop(job_id)
    
    def _prepare_pages_for_export(self, pages: List[GeneratedPage], project: Project) -> List[Dict[str, Any]]:
        """Prepare pages data for export."""
        export_data = []
        
        for page in pages:
            # Extract content based on page structure
            content_html = ""
            content_markdown = ""
            
            if isinstance(page.content, dict):
                content_html = page.content.get('html', '')
                content_markdown = page.content.get('markdown', '')
                if not content_html and 'sections' in page.content:
                    # Build HTML from sections
                    sections = page.content['sections']
                    content_html = self._build_html_from_sections(sections)
            elif isinstance(page.content, str):
                content_html = page.content
            
            # Extract metadata
            meta_data = page.meta_data or {}
            
            page_data = {
                'id': page.id,
                'title': page.title,
                'slug': meta_data.get('slug', self._generate_slug(page.title)),
                'meta_description': meta_data.get('meta_description', ''),
                'content_html': content_html,
                'content_markdown': content_markdown,
                'content': content_html,  # Fallback content
                'word_count': len(content_html.split()) if content_html else 0,
                'template_used': meta_data.get('template_id', ''),
                'status': 'published',
                'created_at': page.created_at.isoformat() if page.created_at else datetime.now().isoformat(),
                'keyword': meta_data.get('keyword', ''),
                'variables': meta_data.get('variables', {}),
                'metadata': {
                    'project_name': project.name,
                    'project_id': project.id,
                    'page_id': page.id
                }
            }
            
            export_data.append(page_data)
        
        return export_data
    
    def _build_html_from_sections(self, sections: List[Dict[str, Any]]) -> str:
        """Build HTML content from page sections."""
        html_parts = []
        
        for section in sections:
            if section.get('type') == 'heading':
                level = section.get('level', 2)
                content = section.get('content', '')
                html_parts.append(f'<h{level}>{content}</h{level}>')
            elif section.get('type') == 'paragraph':
                content = section.get('content', '')
                html_parts.append(f'<p>{content}</p>')
            elif section.get('type') == 'list':
                items = section.get('items', [])
                list_html = '<ul>'
                for item in items:
                    list_html += f'<li>{item}</li>'
                list_html += '</ul>'
                html_parts.append(list_html)
            else:
                # Generic content
                content = section.get('content', '')
                if content:
                    html_parts.append(f'<p>{content}</p>')
        
        return '\n'.join(html_parts)
    
    def _generate_slug(self, title: str) -> str:
        """Generate a URL-friendly slug from title."""
        import re
        slug = re.sub(r'[^a-zA-Z0-9\s-]', '', title.lower())
        slug = re.sub(r'\s+', '-', slug)
        return slug.strip('-')
    
    def _export_csv(self, data: List[Dict[str, Any]], project_name: str, job: ExportJob) -> str:
        """Export data to CSV format."""
        job.progress = 50.0
        file_path = self.csv_exporter.export_content(data, project_name)
        job.progress = 90.0
        return file_path
    
    def _export_json(self, data: List[Dict[str, Any]], project_name: str, job: ExportJob) -> str:
        """Export data to JSON format."""
        job.progress = 50.0
        file_path = self.json_exporter.export_content(data, project_name)
        job.progress = 90.0
        return file_path
    
    def _export_wordpress(self, data: List[Dict[str, Any]], project_name: str, job: ExportJob) -> str:
        """Export data to WordPress XML format."""
        job.progress = 50.0
        site_url = job.metadata.get('site_url', 'https://example.com')
        file_path = self.wordpress_exporter.export_content(data, project_name, site_url)
        job.progress = 90.0
        return file_path
    
    def _export_html(self, data: List[Dict[str, Any]], project_name: str, job: ExportJob) -> str:
        """Export data to HTML format."""
        job.progress = 50.0
        file_path = self.html_exporter.export_content(data, project_name)
        job.progress = 90.0
        return file_path
    
    def _job_to_dict(self, job: ExportJob) -> Dict[str, Any]:
        """Convert export job to dictionary."""
        return {
            'id': job.id,
            'project_id': job.project_id,
            'format': job.format.value,
            'status': job.status.value,
            'progress': job.progress,
            'total_items': job.total_items,
            'processed_items': job.processed_items,
            'created_at': job.created_at.isoformat(),
            'started_at': job.started_at.isoformat() if job.started_at else None,
            'completed_at': job.completed_at.isoformat() if job.completed_at else None,
            'error_message': job.error_message,
            'download_url': job.download_url,
            'metadata': job.metadata
        }


# Global export manager instance
export_manager = ExportManager()