"""Minimal FastAPI backend to test Railway deployment"""
from fastapi import FastAPI, HTTPException, Depends, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from datetime import datetime
import os
from ai_client import AIClient
from database import get_db, init_db
from models import Project, Template, DataSet, GeneratedPage
from template_engine import TemplateEngine
from data_processor import DataProcessor
from page_generator import PageGenerator
from export_manager import export_manager, ExportFormat
from agents.variable_generator import VariableGeneratorAgent

app = FastAPI(title="Programmatic SEO Tool API")
ai_client = AIClient()
template_engine = TemplateEngine()
data_processor = DataProcessor()
page_generator = PageGenerator()
variable_generator = VariableGeneratorAgent()

# Initialize database on startup
@app.on_event("startup")
def startup_event():
    init_db()

# Configure CORS
# For production, use specific origins with regex support
origins = [
    "http://localhost:3000",  # Local development
    "http://localhost:3001",  # Local development (alternate port)
    "http://localhost:3002",  # Local development (alternate port)
    "http://localhost:3003",  # Local development (alternate port)
    "https://programmatic-seo-tool.vercel.app",  # Production Vercel
    "https://programmaticseotool.vercel.app",  # Production Vercel (no dash)
]

# Function to check if origin should be allowed
def is_allowed_origin(origin: str) -> bool:
    # Allow exact matches
    if origin in origins:
        return True
    # Allow Vercel preview deployments
    if origin and origin.startswith("https://programmatic-seo-tool-") and origin.endswith(".vercel.app"):
        return True
    if origin and origin.startswith("https://programmaticseotool-") and origin.endswith(".vercel.app"):
        return True
    return False

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex="https://(programmatic-seo-tool|programmaticseotool)(-[a-z0-9]+)?\.vercel\.app",
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Programmatic SEO Tool API is running!"}

@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    try:
        # Test database connection with proper SQLAlchemy syntax
        from sqlalchemy import text
        result = db.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception as e:
        db_status = f"error: {str(e)}"
    
    return {
        "status": "healthy",
        "service": "programmatic-seo-backend",
        "database": db_status,
        "timestamp": datetime.utcnow().isoformat()
    }

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

# Data-related Pydantic models
class DataSetResponse(BaseModel):
    id: str
    project_id: str
    name: str
    row_count: int
    columns: List[str]
    created_at: datetime
    
    class Config:
        from_attributes = True
        
    @classmethod
    def from_orm(cls, db_dataset):
        # Extract columns from the stored data
        columns = []
        if db_dataset.data and len(db_dataset.data) > 0:
            columns = list(db_dataset.data[0].keys())
        
        return cls(
            id=db_dataset.id,
            project_id=db_dataset.project_id,
            name=db_dataset.name,
            row_count=db_dataset.row_count,
            columns=columns,
            created_at=db_dataset.created_at
        )

class DataSetDetailResponse(BaseModel):
    id: str
    project_id: str
    name: str
    data: List[Dict[str, Any]]
    row_count: int
    columns: List[str]
    created_at: datetime
    
    class Config:
        from_attributes = True
        
    @classmethod
    def from_orm(cls, db_dataset):
        # Extract columns from the stored data
        columns = []
        if db_dataset.data and len(db_dataset.data) > 0:
            columns = list(db_dataset.data[0].keys())
        
        return cls(
            id=db_dataset.id,
            project_id=db_dataset.project_id,
            name=db_dataset.name,
            data=db_dataset.data,
            row_count=db_dataset.row_count,
            columns=columns,
            created_at=db_dataset.created_at
        )

class DataUploadResponse(BaseModel):
    dataset_id: str
    name: str
    row_count: int
    columns: List[str]
    validation: Dict[str, Any]

class ManualDataCreate(BaseModel):
    name: str
    data: List[Dict[str, Any]]

class DataValidationResponse(BaseModel):
    is_valid: bool
    missing_columns: List[str]
    warnings: List[str]
    column_mapping_suggestions: Dict[str, Optional[str]]

# Data endpoints
@app.post("/api/projects/{project_id}/data/upload", response_model=DataUploadResponse)
async def upload_csv_data(
    project_id: str,
    file: UploadFile = File(...),
    template_id: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Upload CSV data for a project"""
    # Check if project exists
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    try:
        # Process the CSV file
        data, columns, row_count = await data_processor.process_csv_upload(file)
        
        # Prepare data for storage
        dataset_name = file.filename.replace('.csv', '')
        prepared_data = data_processor.prepare_data_for_storage(data, dataset_name)
        
        # Create dataset in database
        db_dataset = DataSet(
            project_id=project_id,
            name=prepared_data['name'],
            data=prepared_data['data'],
            row_count=prepared_data['row_count']
        )
        db.add(db_dataset)
        db.commit()
        db.refresh(db_dataset)
        
        # Validate against template if provided
        validation = {"is_valid": True, "missing_columns": [], "warnings": []}
        if template_id:
            template = db.query(Template).filter(Template.id == template_id).first()
            if template:
                validation = data_processor.validate_data_for_template(data, template.variables)
        
        return DataUploadResponse(
            dataset_id=db_dataset.id,
            name=db_dataset.name,
            row_count=db_dataset.row_count,
            columns=columns,
            validation=validation
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

@app.get("/api/projects/{project_id}/data", response_model=List[DataSetResponse])
def get_project_data(project_id: str, db: Session = Depends(get_db)):
    """Get all datasets for a project"""
    # Check if project exists
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    datasets = db.query(DataSet).filter(DataSet.project_id == project_id).all()
    return [DataSetResponse.from_orm(ds) for ds in datasets]

@app.get("/api/projects/{project_id}/data/{dataset_id}", response_model=DataSetDetailResponse)
def get_dataset_detail(project_id: str, dataset_id: str, db: Session = Depends(get_db)):
    """Get detailed data for a specific dataset"""
    dataset = db.query(DataSet).filter(
        DataSet.id == dataset_id,
        DataSet.project_id == project_id
    ).first()
    
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
    
    return DataSetDetailResponse.from_orm(dataset)

@app.post("/api/projects/{project_id}/data", response_model=DataSetResponse)
def create_manual_data(
    project_id: str,
    data_create: ManualDataCreate,
    db: Session = Depends(get_db)
):
    """Create a dataset manually (not from CSV upload)"""
    # Check if project exists
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Validate data
    if not data_create.data:
        raise HTTPException(status_code=400, detail="Data cannot be empty")
    
    # Prepare data for storage
    prepared_data = data_processor.prepare_data_for_storage(data_create.data, data_create.name)
    
    # Create dataset
    db_dataset = DataSet(
        project_id=project_id,
        name=prepared_data['name'],
        data=prepared_data['data'],
        row_count=prepared_data['row_count']
    )
    db.add(db_dataset)
    db.commit()
    db.refresh(db_dataset)
    
    return DataSetResponse.from_orm(db_dataset)

@app.delete("/api/projects/{project_id}/data/{dataset_id}")
def delete_dataset(project_id: str, dataset_id: str, db: Session = Depends(get_db)):
    """Delete a dataset"""
    dataset = db.query(DataSet).filter(
        DataSet.id == dataset_id,
        DataSet.project_id == project_id
    ).first()
    
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
    
    db.delete(dataset)
    db.commit()
    
    return {"message": "Dataset deleted successfully"}

class ValidateDatasetRequest(BaseModel):
    template_id: str

@app.post("/api/projects/{project_id}/data/{dataset_id}/validate", response_model=DataValidationResponse)
def validate_dataset_for_template(
    project_id: str,
    dataset_id: str,
    request: ValidateDatasetRequest,
    db: Session = Depends(get_db)
):
    """Validate a dataset against a template's requirements"""
    template_id = request.template_id
    # Get dataset
    dataset = db.query(DataSet).filter(
        DataSet.id == dataset_id,
        DataSet.project_id == project_id
    ).first()
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
    
    # Get template
    template = db.query(Template).filter(Template.id == template_id).first()
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    
    # Validate data
    validation = data_processor.validate_data_for_template(dataset.data, template.variables)
    
    # Get column mapping suggestions
    data_columns = list(dataset.data[0].keys()) if dataset.data else []
    mapping_suggestions = data_processor.get_column_mapping_suggestions(data_columns, template.variables)
    
    return DataValidationResponse(
        is_valid=validation['is_valid'],
        missing_columns=validation['missing_columns'],
        warnings=validation['warnings'],
        column_mapping_suggestions=mapping_suggestions
    )

# Page generation endpoints
class GeneratePreviewRequest(BaseModel):
    limit: int = 5

class GeneratePreviewResponse(BaseModel):
    pages: List[Dict[str, Any]]
    total_possible_pages: int
    preview_count: int

class GeneratePagesRequest(BaseModel):
    batch_size: int = 100
    selected_titles: Optional[List[str]] = None
    variables_data: Optional[Dict[str, List[str]]] = None

class GeneratePagesResponse(BaseModel):
    total_generated: int
    page_ids: List[str]
    status: str

class PageListResponse(BaseModel):
    pages: List[Dict[str, Any]]
    total: int
    offset: int
    limit: int

@app.post("/api/projects/{project_id}/templates/{template_id}/generate-preview", response_model=GeneratePreviewResponse)
def generate_preview_pages(
    project_id: str,
    template_id: str,
    request: GeneratePreviewRequest,
    db: Session = Depends(get_db)
):
    """Generate preview pages to see what will be created"""
    try:
        # Generate preview pages
        preview_pages = page_generator.generate_preview_pages(
            project_id, template_id, db, limit=request.limit
        )
        
        # Calculate total possible pages
        template = db.query(Template).filter(Template.id == template_id).first()
        if not template:
            raise HTTPException(status_code=404, detail="Template not found")
        
        variable_data = page_generator.load_datasets_for_variables(project_id, template, db)
        all_combinations = page_generator.generate_all_combinations(variable_data)
        total_possible = len(all_combinations)
        
        return GeneratePreviewResponse(
            pages=preview_pages,
            total_possible_pages=total_possible,
            preview_count=len(preview_pages)
        )
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Preview generation failed: {str(e)}")

# Variable generation models
class GenerateVariablesRequest(BaseModel):
    additional_context: Optional[str] = None
    target_count: int = 25

class GenerateVariablesResponse(BaseModel):
    variables: Dict[str, List[str]]
    titles: List[str]
    total_count: int
    template_pattern: str
    variable_types: Dict[str, str]

@app.post("/api/projects/{project_id}/templates/{template_id}/generate-variables", response_model=GenerateVariablesResponse)
async def generate_variables(
    project_id: str,
    template_id: str,
    request: GenerateVariablesRequest,
    db: Session = Depends(get_db)
):
    """Generate AI-powered variables for a template based on business context"""
    try:
        # Get project and template
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        
        template = db.query(Template).filter(
            Template.id == template_id,
            Template.project_id == project_id
        ).first()
        if not template:
            raise HTTPException(status_code=404, detail="Template not found")
        
        # Get business context from project
        business_context = project.business_analysis or {}
        
        # Generate variables using AI
        result = await variable_generator.generate_variables(
            template_pattern=template.pattern,
            business_context=business_context,
            additional_context=request.additional_context,
            target_count=request.target_count
        )
        
        # Validate generated variables
        validation = variable_generator.validate_generated_variables(result["variables"])
        if not validation["is_valid"]:
            raise HTTPException(
                status_code=400,
                detail={"errors": validation["errors"], "warnings": validation["warnings"]}
            )
        
        return GenerateVariablesResponse(**result)
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Variable generation failed: {str(e)}")

@app.post("/api/projects/{project_id}/templates/{template_id}/generate", response_model=GeneratePagesResponse)
def generate_all_pages(
    project_id: str,
    template_id: str,
    request: GeneratePagesRequest,
    db: Session = Depends(get_db)
):
    """Generate all pages from template and data"""
    try:
        # Check if project and template exist
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        
        template = db.query(Template).filter(
            Template.id == template_id,
            Template.project_id == project_id
        ).first()
        if not template:
            raise HTTPException(status_code=404, detail="Template not found")
        
        # Generate pages
        if request.selected_titles and request.variables_data:
            # Use AI-generated variables and selected titles
            total_generated, page_ids = page_generator.generate_pages_from_variables(
                project_id, template_id, 
                request.variables_data,
                request.selected_titles,
                db, batch_size=request.batch_size
            )
        else:
            # Use traditional CSV data
            total_generated, page_ids = page_generator.generate_all_pages(
                project_id, template_id, db, batch_size=request.batch_size
            )
        
        return GeneratePagesResponse(
            total_generated=total_generated,
            page_ids=page_ids,
            status="completed" if total_generated > 0 else "no_pages_generated"
        )
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Page generation failed: {str(e)}")

@app.get("/api/projects/{project_id}/pages", response_model=PageListResponse)
def get_generated_pages(
    project_id: str,
    template_id: Optional[str] = None,
    offset: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """Get generated pages for a project"""
    # Check if project exists
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Get pages
    pages = page_generator.get_generated_pages(
        project_id, template_id, db, offset=offset, limit=limit
    )
    
    # Count total pages
    query = db.query(GeneratedPage).filter(GeneratedPage.project_id == project_id)
    if template_id:
        query = query.filter(GeneratedPage.template_id == template_id)
    total = query.count()
    
    # Convert to response format
    page_list = []
    for page in pages:
        page_data = {
            'id': page.id,
            'title': page.title,
            'slug': page.meta_data.get('slug', ''),
            'keyword': page.meta_data.get('keyword', ''),
            'variables': page.meta_data.get('variables', {}),
            'created_at': page.created_at.isoformat() if page.created_at else None,
            'quality_score': page.content.get('quality_metrics', {}).get('quality_score', 0) if isinstance(page.content, dict) else 0
        }
        page_list.append(page_data)
    
    return PageListResponse(
        pages=page_list,
        total=total,
        offset=offset,
        limit=limit
    )

@app.get("/api/projects/{project_id}/pages/{page_id}")
def get_single_page(
    project_id: str,
    page_id: str,
    enhance: bool = False,
    db: Session = Depends(get_db)
):
    """Get a single generated page with full content"""
    # Get page
    page = db.query(GeneratedPage).filter(
        GeneratedPage.id == page_id,
        GeneratedPage.project_id == project_id
    ).first()
    
    if not page:
        raise HTTPException(status_code=404, detail="Page not found")
    
    # Get project for enhancement
    project = db.query(Project).filter(Project.id == project_id).first()
    
    # Prepare response
    page_data = {
        'id': page.id,
        'project_id': page.project_id,
        'template_id': page.template_id,
        'title': page.title,
        'content': page.content,
        'meta_data': page.meta_data,
        'created_at': page.created_at.isoformat() if page.created_at else None
    }
    
    # Enhance if requested
    if enhance and project:
        # Get all pages for internal linking
        all_pages = db.query(GeneratedPage).filter(
            GeneratedPage.project_id == project_id
        ).limit(100).all()
        
        enhanced_content = page_generator.enhance_page_quality(page, project, all_pages)
        page_data['enhanced_content'] = enhanced_content
    
    return page_data

@app.delete("/api/projects/{project_id}/pages")
def delete_generated_pages(
    project_id: str,
    template_id: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Delete generated pages for a project or template"""
    # Check if project exists
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Build query
    query = db.query(GeneratedPage).filter(GeneratedPage.project_id == project_id)
    if template_id:
        query = query.filter(GeneratedPage.template_id == template_id)
    
    # Count pages to delete
    count = query.count()
    
    # Delete pages
    query.delete()
    db.commit()
    
    return {
        "message": f"Successfully deleted {count} pages",
        "deleted_count": count
    }

# Export-related Pydantic models
class ExportRequest(BaseModel):
    format: str  # csv, json, wordpress, html
    options: Optional[Dict[str, Any]] = None

class ExportResponse(BaseModel):
    export_id: str
    status: str
    message: str

class ExportStatusResponse(BaseModel):
    id: str
    project_id: str
    format: str
    status: str
    progress: float
    total_items: int
    processed_items: int
    created_at: str
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    error_message: Optional[str] = None
    download_url: Optional[str] = None

# Export endpoints
@app.post("/api/projects/{project_id}/export", response_model=ExportResponse)
def start_export(
    project_id: str,
    request: ExportRequest,
    db: Session = Depends(get_db)
):
    """Start a new export job for a project."""
    # Validate project exists
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Validate format
    try:
        export_format = ExportFormat(request.format.lower())
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported export format: {request.format}. Supported formats: csv, json, wordpress, html"
        )
    
    try:
        # Start export job
        export_id = export_manager.start_export(
            project_id=project_id,
            format=export_format,
            options=request.options
        )
        
        return ExportResponse(
            export_id=export_id,
            status="started",
            message=f"Export job {export_id} started successfully"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start export: {str(e)}")

@app.get("/api/exports/{export_id}/status", response_model=ExportStatusResponse)
def get_export_status(export_id: str):
    """Get the status of an export job."""
    status = export_manager.get_export_status(export_id)
    
    if not status:
        raise HTTPException(status_code=404, detail="Export job not found")
    
    return ExportStatusResponse(**status)

@app.get("/api/exports/{export_id}/download")
def download_export(export_id: str):
    """Download the exported file."""
    file_path = export_manager.get_file_path(export_id)
    
    if not file_path or not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Export file not found or not ready")
    
    # Get filename from path
    filename = os.path.basename(file_path)
    
    return FileResponse(
        path=file_path,
        filename=filename,
        media_type='application/octet-stream'
    )

@app.get("/api/projects/{project_id}/exports")
def list_project_exports(project_id: str, db: Session = Depends(get_db)):
    """List all export jobs for a project."""
    # Validate project exists
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    exports = export_manager.list_exports(project_id=project_id)
    return {"exports": exports}

@app.get("/api/exports")
def list_all_exports():
    """List all export jobs across all projects."""
    exports = export_manager.list_exports()
    return {"exports": exports}

@app.delete("/api/exports/{export_id}")
def cancel_export(export_id: str):
    """Cancel an active export job."""
    success = export_manager.cancel_export(export_id)
    
    if not success:
        raise HTTPException(
            status_code=400,
            detail="Export job not found or cannot be cancelled"
        )
    
    return {"message": f"Export job {export_id} cancelled successfully"}

@app.post("/api/exports/cleanup")
def cleanup_old_exports(days_old: int = 7):
    """Clean up old export files and jobs."""
    try:
        cleaned_count = export_manager.cleanup_old_exports(days_old)
        return {
            "message": f"Cleaned up {cleaned_count} old export jobs",
            "cleaned_count": cleaned_count
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Cleanup failed: {str(e)}")