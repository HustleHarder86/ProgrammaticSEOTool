"""Database Integration Agent for managing persistent storage."""
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from models import Project, Template, DataSet, GeneratedPage
from database import get_db
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
    
    # Template Operations
    def create_template(self, project_id: str, name: str, pattern: str, 
                       variables: List[str], template_sections: Dict[str, Any]) -> Template:
        """Create a new template."""
        template = Template(
            project_id=project_id,
            name=name,
            pattern=pattern,
            variables=variables,
            template_sections=template_sections
        )
        self.db.add(template)
        self.db.commit()
        self.db.refresh(template)
        logger.info(f"Created template: {template.id} - {template.name}")
        return template
    
    def get_template(self, template_id: str) -> Optional[Template]:
        """Get template by ID."""
        return self.db.query(Template).filter(Template.id == template_id).first()
    
    def list_project_templates(self, project_id: str) -> List[Template]:
        """List all templates for a project."""
        return self.db.query(Template).filter(Template.project_id == project_id).all()
    
    # DataSet Operations
    def create_dataset(self, project_id: str, name: str, data: List[Dict[str, Any]]) -> DataSet:
        """Create a new dataset."""
        dataset = DataSet(
            project_id=project_id,
            name=name,
            data=data
        )
        self.db.add(dataset)
        self.db.commit()
        self.db.refresh(dataset)
        logger.info(f"Created dataset: {dataset.id} - {dataset.name}")
        return dataset
    
    def get_dataset(self, dataset_id: str) -> Optional[DataSet]:
        """Get dataset by ID."""
        return self.db.query(DataSet).filter(DataSet.id == dataset_id).first()
    
    def list_project_datasets(self, project_id: str) -> List[DataSet]:
        """List all datasets for a project."""
        return self.db.query(DataSet).filter(DataSet.project_id == project_id).all()
    
    # GeneratedPage Operations
    def create_generated_page(self, project_id: str, template_id: str, 
                            dataset_id: str, title: str, url_slug: str,
                            content: str, seo_data: Dict[str, Any]) -> GeneratedPage:
        """Create a new generated page."""
        page = GeneratedPage(
            project_id=project_id,
            template_id=template_id,
            dataset_id=dataset_id,
            title=title,
            url_slug=url_slug,
            content=content,
            seo_data=seo_data
        )
        self.db.add(page)
        self.db.commit()
        self.db.refresh(page)
        logger.info(f"Created generated page: {page.id} - {page.title}")
        return page
    
    def get_generated_page(self, page_id: str) -> Optional[GeneratedPage]:
        """Get generated page by ID."""
        return self.db.query(GeneratedPage).filter(GeneratedPage.id == page_id).first()
    
    def list_project_pages(self, project_id: str, limit: int = 100) -> List[GeneratedPage]:
        """List all generated pages for a project."""
        return self.db.query(GeneratedPage).filter(
            GeneratedPage.project_id == project_id
        ).limit(limit).all()
    
    # Statistics
    def get_project_stats(self, project_id: str) -> Dict[str, Any]:
        """Get statistics for a project."""
        project = self.get_project(project_id)
        if not project:
            return {}
        
        total_templates = self.db.query(Template).filter(
            Template.project_id == project_id
        ).count()
        
        total_datasets = self.db.query(DataSet).filter(
            DataSet.project_id == project_id
        ).count()
        
        total_pages = self.db.query(GeneratedPage).filter(
            GeneratedPage.project_id == project_id
        ).count()
        
        return {
            'project': project,
            'total_templates': total_templates,
            'total_datasets': total_datasets,
            'total_pages': total_pages
        }