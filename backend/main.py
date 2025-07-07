"""Minimal FastAPI backend to test Railway deployment"""
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from datetime import datetime
import os
from ai_client import AIClient
from database import get_db, init_db
from models import Project, Template, DataSet, GeneratedPage
from template_engine import TemplateEngine

app = FastAPI(title="Programmatic SEO Tool API")
ai_client = AIClient()
template_engine = TemplateEngine()

# Initialize database on startup
@app.on_event("startup")
def startup_event():
    init_db()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Programmatic SEO Tool API is running!"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "programmatic-seo-backend"}

@app.get("/api/test")
def test_endpoint():
    return {"message": "API is working!", "timestamp": "2025-01-06"}

# Pydantic models
class BusinessAnalysisRequest(BaseModel):
    business_input: str
    input_type: str = "text"  # "text" or "url"

class TemplateOpportunity(BaseModel):
    template_name: str
    template_pattern: str
    example_pages: List[str]
    estimated_pages: int
    difficulty: str

class BusinessAnalysisResponse(BaseModel):
    project_id: str
    business_name: str
    business_description: str
    target_audience: str
    core_offerings: List[str]
    template_opportunities: List[TemplateOpportunity]

@app.post("/api/analyze-business", response_model=BusinessAnalysisResponse)
async def analyze_business(request: BusinessAnalysisRequest, db: Session = Depends(get_db)):
    """Analyze a business and suggest programmatic SEO templates"""
    
    try:
        # Use AI client to analyze the business
        analysis = ai_client.analyze_business(request.business_input)
        
        # Validate the analysis has required fields
        required_fields = ["business_name", "business_description", "target_audience", "core_offerings", "template_opportunities"]
        for field in required_fields:
            if field not in analysis:
                print(f"Missing field in analysis: {field}")
                raise ValueError(f"Analysis missing required field: {field}")
        
        # Convert to response model
        template_opportunities = []
        for opp in analysis.get("template_opportunities", []):
            try:
                template_opportunities.append(TemplateOpportunity(
                    template_name=opp.get("template_name", "Unknown"),
                    template_pattern=opp.get("template_pattern", "Unknown"),
                    example_pages=opp.get("example_pages", []),
                    estimated_pages=opp.get("estimated_pages", 0),
                    difficulty=opp.get("difficulty", "Medium")
                ))
            except Exception as opp_error:
                print(f"Error processing template opportunity: {opp_error}")
                continue
        
        # Create a new project in the database
        db_project = Project(
            name=analysis.get("business_name", "Unknown Business"),
            business_input=request.business_input,
            business_analysis=analysis
        )
        db.add(db_project)
        db.commit()
        db.refresh(db_project)
        
        response = BusinessAnalysisResponse(
            project_id=db_project.id,
            business_name=analysis.get("business_name", "Unknown Business"),
            business_description=analysis.get("business_description", "No description"),
            target_audience=analysis.get("target_audience", "General audience"),
            core_offerings=analysis.get("core_offerings", []),
            template_opportunities=template_opportunities
        )
        
        return response
        
    except Exception as e:
        print(f"Error in analyze_business endpoint: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

# Project-related Pydantic models
class ProjectCreate(BaseModel):
    name: str
    business_input: str
    business_analysis: Optional[dict] = None

class ProjectResponse(BaseModel):
    id: str
    name: str
    business_input: str
    business_analysis: Optional[dict]
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True

class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    business_input: Optional[str] = None
    business_analysis: Optional[dict] = None

# CRUD endpoints for projects
@app.post("/api/projects", response_model=ProjectResponse)
def create_project(project: ProjectCreate, db: Session = Depends(get_db)):
    """Create a new project with business analysis"""
    db_project = Project(
        name=project.name,
        business_input=project.business_input,
        business_analysis=project.business_analysis
    )
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

@app.get("/api/projects", response_model=List[ProjectResponse])
def list_projects(db: Session = Depends(get_db)):
    """List all projects"""
    projects = db.query(Project).all()
    return projects

@app.get("/api/projects/{project_id}", response_model=ProjectResponse)
def get_project(project_id: str, db: Session = Depends(get_db)):
    """Get project details with templates and data"""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@app.put("/api/projects/{project_id}", response_model=ProjectResponse)
def update_project(project_id: str, project_update: ProjectUpdate, db: Session = Depends(get_db)):
    """Update project"""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    update_data = project_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(project, field, value)
    
    db.commit()
    db.refresh(project)
    return project

@app.delete("/api/projects/{project_id}")
def delete_project(project_id: str, db: Session = Depends(get_db)):
    """Delete project and all related data"""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    db.delete(project)
    db.commit()
    return {"message": "Project deleted successfully"}

# Template-related Pydantic models
class TemplateCreate(BaseModel):
    name: str
    pattern: str
    title_template: Optional[str] = None
    meta_description_template: Optional[str] = None
    h1_template: Optional[str] = None
    content_sections: Optional[List[dict]] = []
    template_type: Optional[str] = "custom"

class TemplateUpdate(BaseModel):
    name: Optional[str] = None
    pattern: Optional[str] = None
    title_template: Optional[str] = None
    meta_description_template: Optional[str] = None
    h1_template: Optional[str] = None
    content_sections: Optional[List[dict]] = None
    template_type: Optional[str] = None

class TemplateResponse(BaseModel):
    id: str
    project_id: str
    name: str
    pattern: str
    variables: List[str]
    created_at: datetime
    
    class Config:
        from_attributes = True

class TemplateDetailResponse(BaseModel):
    id: str
    project_id: str
    name: str
    pattern: str
    variables: List[str]
    template_sections: Optional[Dict[str, Any]]
    example_pages: Optional[List[Any]]
    created_at: datetime
    
    class Config:
        from_attributes = True

class TemplatePreviewRequest(BaseModel):
    sample_data: Dict[str, str]

class TemplatePreviewResponse(BaseModel):
    pattern: str
    filled_pattern: str
    seo: Dict[str, str]
    content_sections: List[Dict[str, str]]
    sample_data: Dict[str, str]

# Template endpoints
@app.post("/api/projects/{project_id}/templates", response_model=TemplateResponse)
def create_template(project_id: str, template: TemplateCreate, db: Session = Depends(get_db)):
    """Create a new template for a project"""
    # Check if project exists
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Create template structure
    template_data = template.dict()
    structured_template = template_engine.create_template_structure(template_data)
    
    # Validate template
    validation = template_engine.validate_template(template_data)
    if not validation['is_valid']:
        raise HTTPException(
            status_code=400, 
            detail={"errors": validation['errors'], "warnings": validation['warnings']}
        )
    
    # Create database template
    db_template = Template(
        project_id=project_id,
        name=structured_template['name'],
        pattern=structured_template['pattern'],
        variables=structured_template['variables'],
        template_sections={
            'seo_structure': structured_template.get('seo_structure', {}),
            'content_sections': template_data.get('content_sections', [])
        },
        example_pages=[]  # Will be populated later
    )
    
    db.add(db_template)
    db.commit()
    db.refresh(db_template)
    
    return db_template

@app.get("/api/projects/{project_id}/templates", response_model=List[TemplateResponse])
def list_project_templates(project_id: str, db: Session = Depends(get_db)):
    """List all templates for a project"""
    # Check if project exists
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    templates = db.query(Template).filter(Template.project_id == project_id).all()
    return templates

@app.get("/api/templates/{template_id}", response_model=TemplateDetailResponse)
def get_template(template_id: str, db: Session = Depends(get_db)):
    """Get a single template by ID with all details"""
    template = db.query(Template).filter(Template.id == template_id).first()
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    return template

@app.put("/api/templates/{template_id}", response_model=TemplateResponse)
def update_template(template_id: str, template_update: TemplateUpdate, db: Session = Depends(get_db)):
    """Update an existing template"""
    # Get template
    template = db.query(Template).filter(Template.id == template_id).first()
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    
    # Update fields
    update_data = template_update.dict(exclude_unset=True)
    
    # If pattern or template fields are being updated, re-validate and extract variables
    template_fields = ['pattern', 'title_template', 'meta_description_template', 'h1_template', 'content_sections']
    if any(field in update_data for field in template_fields):
        # Get current template sections
        current_sections = template.template_sections or {}
        current_seo = current_sections.get('seo_structure', {})
        
        # Create full template data for validation
        template_data = {
            'name': update_data.get('name', template.name),
            'pattern': update_data.get('pattern', template.pattern),
            'title_template': update_data.get('title_template', current_seo.get('title_template')),
            'meta_description_template': update_data.get('meta_description_template', current_seo.get('meta_description_template')),
            'h1_template': update_data.get('h1_template', current_seo.get('h1_template')),
            'content_sections': update_data.get('content_sections', current_sections.get('content_sections', []))
        }
        
        # Validate
        validation = template_engine.validate_template(template_data)
        if not validation['is_valid']:
            raise HTTPException(
                status_code=400,
                detail={"errors": validation['errors'], "warnings": validation['warnings']}
            )
        
        # Extract new variables
        update_data['variables'] = validation['variables']
        
        # Update template_sections
        update_data['template_sections'] = {
            'seo_structure': {
                'title_template': template_data['title_template'],
                'meta_description_template': template_data['meta_description_template'],
                'h1_template': template_data['h1_template']
            },
            'content_sections': template_data['content_sections']
        }
    
    # Apply updates
    for field, value in update_data.items():
        if hasattr(template, field):
            setattr(template, field, value)
    
    db.commit()
    db.refresh(template)
    
    return template

@app.post("/api/templates/{template_id}/preview", response_model=TemplatePreviewResponse)
def preview_template(template_id: str, preview_request: TemplatePreviewRequest, db: Session = Depends(get_db)):
    """Preview a template with sample data"""
    # Get template
    template = db.query(Template).filter(Template.id == template_id).first()
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    
    # Build template data structure
    template_sections = template.template_sections or {}
    seo_structure = template_sections.get('seo_structure', {})
    content_sections = template_sections.get('content_sections', [])
    
    # Use stored template data or provide defaults
    template_data = {
        'pattern': template.pattern,
        'title_template': seo_structure.get('title_template', f"{template.pattern} - Professional Services"),
        'meta_description_template': seo_structure.get('meta_description_template', f"Find the best services for {template.pattern}. Compare options and get started today."),
        'h1_template': seo_structure.get('h1_template', template.pattern),
        'content_sections': content_sections if content_sections else [
            {
                'heading': 'Overview',
                'content': f'Learn about {template.pattern} and how we can help.'
            },
            {
                'heading': 'Our Services',
                'content': 'Detailed information about our offerings and expertise.'
            },
            {
                'heading': 'Why Choose Us',
                'content': 'Benefits and advantages of working with our team.'
            }
        ]
    }
    
    # Generate preview
    preview = template_engine.generate_preview(template_data, preview_request.sample_data)
    
    return TemplatePreviewResponse(**preview)

@app.delete("/api/templates/{template_id}")
def delete_template(template_id: str, db: Session = Depends(get_db)):
    """Delete a template"""
    template = db.query(Template).filter(Template.id == template_id).first()
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    
    db.delete(template)
    db.commit()
    return {"message": "Template deleted successfully"}