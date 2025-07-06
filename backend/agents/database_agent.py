"""Database Integration Agent for managing persistent storage."""
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from backend.models import Project, Keyword, Content, get_db
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class DatabaseAgent:
    """Handles all database operations for the SEO tool."""
    
    def __init__(self, db: Session):
        self.db = db
    
    # Project Operations
    def create_project(self, name: str, business_description: str, 
                      business_url: Optional[str] = None,
                      industry: Optional[str] = None,
                      location: Optional[str] = None) -> Project:
        """Create a new SEO project."""
        project = Project(
            name=name,
            business_description=business_description,
            business_url=business_url,
            industry=industry,
            location=location
        )
        self.db.add(project)
        self.db.commit()
        self.db.refresh(project)
        logger.info(f"Created project: {project.id} - {project.name}")
        return project
    
    def get_project(self, project_id: int) -> Optional[Project]:
        """Get project by ID."""
        return self.db.query(Project).filter(Project.id == project_id).first()
    
    def list_projects(self, limit: int = 100) -> List[Project]:
        """List all projects."""
        return self.db.query(Project).order_by(Project.created_at.desc()).limit(limit).all()
    
    def update_project(self, project_id: int, **kwargs) -> Optional[Project]:
        """Update project details."""
        project = self.get_project(project_id)
        if project:
            for key, value in kwargs.items():
                if hasattr(project, key):
                    setattr(project, key, value)
            project.updated_at = datetime.utcnow()
            self.db.commit()
            self.db.refresh(project)
        return project
    
    # Keyword Operations
    def add_keywords(self, project_id: int, keywords_data: List[Dict[str, Any]]) -> List[Keyword]:
        """Add keywords to a project."""
        keywords = []
        for kw_data in keywords_data:
            keyword = Keyword(
                project_id=project_id,
                keyword=kw_data['keyword'],
                search_volume=kw_data.get('search_volume'),
                difficulty=kw_data.get('difficulty'),
                content_type=kw_data.get('content_type'),
                priority=kw_data.get('priority', 5)
            )
            self.db.add(keyword)
            keywords.append(keyword)
        
        self.db.commit()
        logger.info(f"Added {len(keywords)} keywords to project {project_id}")
        return keywords
    
    def get_project_keywords(self, project_id: int, status: Optional[str] = None) -> List[Keyword]:
        """Get keywords for a project, optionally filtered by status."""
        query = self.db.query(Keyword).filter(Keyword.project_id == project_id)
        if status:
            query = query.filter(Keyword.status == status)
        return query.order_by(Keyword.priority.desc()).all()
    
    def update_keyword_status(self, keyword_id: int, status: str) -> Optional[Keyword]:
        """Update keyword status."""
        keyword = self.db.query(Keyword).filter(Keyword.id == keyword_id).first()
        if keyword:
            keyword.status = status
            self.db.commit()
            self.db.refresh(keyword)
        return keyword
    
    # Content Operations
    def save_content(self, project_id: int, keyword_id: Optional[int], 
                    title: str, content_html: str, content_markdown: str,
                    meta_description: str, slug: str, template_used: str,
                    word_count: int, variation_number: int = 1) -> Content:
        """Save generated content."""
        content = Content(
            project_id=project_id,
            keyword_id=keyword_id,
            title=title,
            meta_description=meta_description,
            slug=slug,
            content_html=content_html,
            content_markdown=content_markdown,
            word_count=word_count,
            template_used=template_used,
            variation_number=variation_number
        )
        self.db.add(content)
        self.db.commit()
        self.db.refresh(content)
        
        # Update keyword status if provided
        if keyword_id:
            self.update_keyword_status(keyword_id, 'generated')
        
        logger.info(f"Saved content: {content.id} - {content.title}")
        return content
    
    def get_project_content(self, project_id: int, status: Optional[str] = None) -> List[Content]:
        """Get all content for a project."""
        query = self.db.query(Content).filter(Content.project_id == project_id)
        if status:
            query = query.filter(Content.status == status)
        return query.order_by(Content.created_at.desc()).all()
    
    def update_content_status(self, content_id: int, status: str, 
                            published_url: Optional[str] = None) -> Optional[Content]:
        """Update content status and optionally set published URL."""
        content = self.db.query(Content).filter(Content.id == content_id).first()
        if content:
            content.status = status
            if status == 'published' and published_url:
                content.published_url = published_url
                content.published_at = datetime.utcnow()
            content.updated_at = datetime.utcnow()
            self.db.commit()
            self.db.refresh(content)
        return content
    
    def get_content_by_keyword(self, keyword_id: int) -> List[Content]:
        """Get all content variations for a keyword."""
        return self.db.query(Content).filter(
            Content.keyword_id == keyword_id
        ).order_by(Content.variation_number).all()
    
    # Statistics
    def get_project_stats(self, project_id: int) -> Dict[str, Any]:
        """Get statistics for a project."""
        project = self.get_project(project_id)
        if not project:
            return {}
        
        total_keywords = self.db.query(Keyword).filter(
            Keyword.project_id == project_id
        ).count()
        
        keywords_by_status = {}
        for status in ['pending', 'generated', 'published']:
            count = self.db.query(Keyword).filter(
                Keyword.project_id == project_id,
                Keyword.status == status
            ).count()
            keywords_by_status[status] = count
        
        total_content = self.db.query(Content).filter(
            Content.project_id == project_id
        ).count()
        
        content_by_status = {}
        for status in ['draft', 'ready', 'published']:
            count = self.db.query(Content).filter(
                Content.project_id == project_id,
                Content.status == status
            ).count()
            content_by_status[status] = count
        
        return {
            'project': project,
            'total_keywords': total_keywords,
            'keywords_by_status': keywords_by_status,
            'total_content': total_content,
            'content_by_status': content_by_status
        }