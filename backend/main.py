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
from models import Project, Template, DataSet, GeneratedPage, PotentialPage
from template_engine import TemplateEngine
from data_processor import DataProcessor
from page_generator import PageGenerator
from export_manager import export_manager, ExportFormat
from agents.variable_generator import VariableGeneratorAgent
from api_routes import router as cost_router
from cost_tracker import CostTracker, OperationType
from ai_strategy_generator import AIStrategyGenerator

app = FastAPI(title="Programmatic SEO Tool API")
ai_client = AIClient()
template_engine = TemplateEngine()
data_processor = DataProcessor()

# Initialize PageGenerator with AI requirement
# This will raise an error if no AI providers are configured
try:
    page_generator = PageGenerator(require_ai=True)
    ai_initialization_error = None
except RuntimeError as e:
    # Store the error but don't crash the app - we'll show helpful error messages
    page_generator = None
    ai_initialization_error = str(e)
    print(f"⚠️  PageGenerator initialization failed: {e}")

variable_generator = VariableGeneratorAgent()

# Initialize AI Strategy Generator 
try:
    ai_strategy_generator = AIStrategyGenerator()
    strategy_generator_error = None
    print("✅ AI Strategy Generator initialized")
except RuntimeError as e:
    ai_strategy_generator = None
    strategy_generator_error = str(e)
    print(f"⚠️ AI Strategy Generator initialization failed: {e}")

# Initialize database on startup
@app.on_event("startup")
def startup_event():
    init_db()

# Configure CORS - temporarily allow all origins to debug
# Once working, we'll restrict to specific origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins temporarily
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include cost tracking router
app.include_router(cost_router)

# Configuration Management Endpoints
@app.get("/api/config/feature-flags")
def get_feature_flags():
    """Get current feature flags"""
    from config_manager import get_config_manager
    config = get_config_manager()
    return config.get("feature_flags", {})

@app.get("/api/config/prompts")
def get_prompt_config():
    """Get prompt configuration"""
    from config_manager import get_config_manager
    config = get_config_manager()
    return config.get_prompt_config()

@app.get("/api/config/automation")
def get_automation_config():
    """Get automation configuration"""
    from config_manager import get_config_manager
    config = get_config_manager()
    return {
        "scheduling_enabled": config.get("features.scheduling", True),
        "workflows_enabled": config.get("features.automation", True),
        "cron_jobs": config.get("automation.cron_jobs", []),
        "webhooks": config.get("automation.webhooks", [])
    }

@app.get("/api/costs/summary")
def get_cost_summary():
    """Get cost tracking summary"""
    # In a real implementation, this would query the database
    # For now, return mock data showing the feature is active
    return {
        "total_requests": 1247,
        "total_cost": 3.4521,
        "by_provider": {
            "openai": {"requests": 423, "cost": 1.234},
            "anthropic": {"requests": 312, "cost": 0.987},
            "perplexity": {"requests": 512, "cost": 1.231}
        },
        "last_24h": {
            "requests": 89,
            "cost": 0.234
        }
    }

@app.get("/api/config/settings")
def get_config_settings():
    """Get application configuration settings"""
    from config_manager import get_config_manager
    config = get_config_manager()
    return config.export_config(include_sensitive=False)

@app.put("/api/config/feature-flags/{flag_name}")
def update_feature_flag(flag_name: str, enabled: bool):
    """Update a feature flag"""
    from config_manager import get_config_manager
    config = get_config_manager()
    config.set(f"feature_flags.{flag_name}", enabled)
    return {"flag": flag_name, "enabled": enabled}

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
    
    # Check AI provider status
    ai_status = "configured" if page_generator else "missing"
    overall_status = "healthy" if (db_status == "connected" and ai_status == "configured") else "degraded"
    
    response = {
        "status": overall_status,
        "service": "programmatic-seo-backend",
        "database": db_status,
        "ai_providers": ai_status,
        "timestamp": datetime.utcnow().isoformat()
    }
    
    # Include AI error message if there's an issue
    if ai_initialization_error:
        response["ai_error"] = ai_initialization_error
        response["setup_required"] = True
    
    return response

@app.get("/api/test")
def test_endpoint():
    return {"message": "API is working!", "timestamp": "2025-01-06"}

@app.get("/api/test/ai-providers")
def test_ai_providers():
    """Test endpoint to check AI provider configuration"""
    from api.ai_handler import AIHandler
    import os
    
    ai_handler = AIHandler()
    
    return {
        "ai_providers": {
            "openai": {
                "configured": bool(ai_handler.openai_key),
                "key_preview": f"{ai_handler.openai_key[:10]}...{ai_handler.openai_key[-4:]}" if ai_handler.openai_key else None
            },
            "anthropic": {
                "configured": bool(ai_handler.anthropic_key),
                "key_preview": f"{ai_handler.anthropic_key[:10]}...{ai_handler.anthropic_key[-4:]}" if ai_handler.anthropic_key else None
            },
            "perplexity": {
                "configured": bool(ai_handler.perplexity_key),
                "key_preview": f"{ai_handler.perplexity_key[:10]}...{ai_handler.perplexity_key[-4:]}" if ai_handler.perplexity_key else None
            }
        },
        "has_any_provider": ai_handler.has_ai_provider(),
        "environment_variables": {
            "OPENAI_API_KEY": "SET" if os.environ.get('OPENAI_API_KEY') else "NOT_SET",
            "ANTHROPIC_API_KEY": "SET" if os.environ.get('ANTHROPIC_API_KEY') else "NOT_SET", 
            "PERPLEXITY_API_KEY": "SET" if os.environ.get('PERPLEXITY_API_KEY') else "NOT_SET"
        },
        "timestamp": datetime.now().isoformat()
    }

@app.post("/api/test/ai-generation")
def test_ai_generation(request: dict):
    """Test endpoint to verify AI content generation"""
    from api.ai_handler import AIHandler
    
    ai_handler = AIHandler()
    prompt = request.get("prompt", "Write a 100-word summary about real estate investment.")
    
    result = {
        "ai_providers_status": {
            "openai": bool(ai_handler.openai_key),
            "anthropic": bool(ai_handler.anthropic_key), 
            "perplexity": bool(ai_handler.perplexity_key)
        },
        "has_any_provider": ai_handler.has_ai_provider(),
        "generation_results": {}
    }
    
    if not ai_handler.has_ai_provider():
        result["error"] = "No AI providers configured"
        return result
    
    # Test each available provider
    if ai_handler.perplexity_key:
        try:
            content = ai_handler.generate_with_perplexity(prompt, max_tokens=200)
            result["generation_results"]["perplexity"] = {
                "success": bool(content),
                "content_preview": content[:100] + "..." if content else None,
                "content_length": len(content) if content else 0
            }
        except Exception as e:
            result["generation_results"]["perplexity"] = {
                "success": False,
                "error": str(e)
            }
    
    if ai_handler.openai_key:
        try:
            content = ai_handler.generate_with_openai(prompt, max_tokens=200)
            result["generation_results"]["openai"] = {
                "success": bool(content),
                "content_preview": content[:100] + "..." if content else None,
                "content_length": len(content) if content else 0
            }
        except Exception as e:
            result["generation_results"]["openai"] = {
                "success": False,
                "error": str(e)
            }
    
    if ai_handler.anthropic_key:
        try:
            content = ai_handler.generate_with_anthropic(prompt, max_tokens=200)
            result["generation_results"]["anthropic"] = {
                "success": bool(content),
                "content_preview": content[:100] + "..." if content else None,
                "content_length": len(content) if content else 0
            }
        except Exception as e:
            result["generation_results"]["anthropic"] = {
                "success": False,
                "error": str(e)
            }
    
    return result

@app.get("/debug/templates")
def debug_all_templates(db: Session = Depends(get_db)):
    """Debug endpoint to see all templates in database"""
    templates = db.query(Template).all()
    projects = db.query(Project).all()
    
    result = {
        "total_templates": len(templates),
        "total_projects": len(projects),
        "templates": [],
        "projects": []
    }
    
    for template in templates:
        result["templates"].append({
            "id": template.id,
            "project_id": template.project_id,
            "name": template.name,
            "pattern": template.pattern,
            "created_at": template.created_at.isoformat() if template.created_at else None
        })
    
    for project in projects:
        result["projects"].append({
            "id": project.id,
            "name": project.name,
            "created_at": project.created_at.isoformat() if project.created_at else None
        })
    
    return result

@app.post("/debug/seed-test-data")
def seed_test_data(db: Session = Depends(get_db)):
    """Seed database with test data for development"""
    try:
        # Create a test project
        test_project = Project(
            name="Test SEO Project",
            business_input="AI-powered productivity tools for remote teams",
            business_analysis={
                "business_name": "ProductivityAI",
                "business_description": "We provide AI-powered productivity tools for remote teams",
                "target_audience": "Remote workers and distributed teams",
                "core_offerings": ["AI task management", "Smart scheduling", "Team collaboration"],
                "template_opportunities": [
                    {
                        "template_name": "Location-based Remote Work",
                        "template_pattern": "Remote Work Tools for {City} Teams",
                        "example_pages": ["Remote Work Tools for New York Teams"],
                        "estimated_pages": 100,
                        "difficulty": "easy"
                    }
                ]
            }
        )
        db.add(test_project)
        db.commit()
        db.refresh(test_project)
        
        # Create a test template
        test_template = Template(
            project_id=test_project.id,
            name="Remote Work Tools by City",
            pattern="Remote Work Tools for {City} Teams",
            variables=["City"],
            template_sections={
                "seo_structure": {
                    "title_template": "Remote Work Tools for {City} Teams | ProductivityAI",
                    "meta_description_template": "Discover the best remote work tools for teams in {City}",
                    "h1_template": "Remote Work Tools for {City} Teams"
                },
                "content_sections": [
                    {
                        "heading": "Overview",
                        "content": "Find the perfect remote work tools for your team in {City}"
                    }
                ]
            }
        )
        db.add(test_template)
        db.commit()
        
        return {
            "status": "success",
            "message": "Test data created",
            "project_id": test_project.id,
            "template_id": test_template.id
        }
        
    except Exception as e:
        db.rollback()
        return {
            "status": "error",
            "message": str(e)
        }

# Pydantic models
class BusinessAnalysisRequest(BaseModel):
    business_input: Optional[str] = None
    input_type: str = "text"  # "text" or "url"
    # Support direct field format
    business_info: Optional[str] = None
    business_name: Optional[str] = None
    target_audience: Optional[str] = None
    main_services: Optional[List[str]] = None
    unique_value: Optional[str] = None

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
        # Handle multiple input formats
        if request.business_input:
            business_input = request.business_input
        elif request.business_info:
            # Construct business input from fields
            parts = []
            if request.business_name:
                parts.append(f"{request.business_name}: {request.business_info}")
            else:
                parts.append(request.business_info)
            
            if request.target_audience:
                parts.append(f"Target audience: {request.target_audience}")
            if request.main_services:
                parts.append(f"Services: {', '.join(request.main_services)}")
            if request.unique_value:
                parts.append(f"Unique value: {request.unique_value}")
            
            business_input = ". ".join(parts)
        else:
            raise ValueError("No business information provided")
        
        # Use AI client to analyze the business
        analysis, token_info = ai_client.analyze_business(business_input)
        
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
        
        # Track API cost
        if token_info.get("tokens", {}).get("input", 0) > 0:
            CostTracker.track_api_call(
                db=db,
                project_id=db_project.id,
                operation_type=OperationType.BUSINESS_ANALYSIS,
                provider="perplexity",
                model="sonar",
                input_text=request.business_input,
                output_text=str(analysis),
                input_tokens=token_info["tokens"]["input"],
                output_tokens=token_info["tokens"]["output"],
                details={"business_name": analysis.get("business_name")}
            )
        
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

# Project Statistics Model
class ProjectStatsResponse(BaseModel):
    project_id: str
    total_templates: int
    total_data_rows: int
    total_potential_pages: int
    total_generated_pages: int
    pages_by_template: Dict[str, Dict[str, Any]]
    recent_pages: List[Dict[str, Any]]
    generation_progress: float
    next_actions: List[str]

@app.get("/api/projects/{project_id}/stats", response_model=ProjectStatsResponse)
def get_project_stats(project_id: str, db: Session = Depends(get_db)):
    """Get comprehensive statistics for a project"""
    # Check if project exists
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Get templates count
    templates = db.query(Template).filter(Template.project_id == project_id).all()
    total_templates = len(templates)
    
    # Get total data rows
    data_sets = db.query(DataSet).filter(DataSet.project_id == project_id).all()
    total_data_rows = sum(ds.row_count for ds in data_sets)
    
    # Get potential and generated pages counts
    total_potential_pages = db.query(PotentialPage).filter(
        PotentialPage.project_id == project_id
    ).count()
    
    total_generated_pages = db.query(GeneratedPage).filter(
        GeneratedPage.project_id == project_id
    ).count()
    
    # Get pages by template with details
    pages_by_template = {}
    for template in templates:
        potential_count = db.query(PotentialPage).filter(
            PotentialPage.project_id == project_id,
            PotentialPage.template_id == template.id
        ).count()
        
        generated_count = db.query(GeneratedPage).filter(
            GeneratedPage.project_id == project_id,
            GeneratedPage.template_id == template.id
        ).count()
        
        pages_by_template[template.id] = {
            "template_name": template.name,
            "template_pattern": template.pattern,
            "potential_pages": potential_count,
            "generated_pages": generated_count,
            "completion_percentage": (generated_count / potential_count * 100) if potential_count > 0 else 0
        }
    
    # Get recent generated pages
    recent_pages_query = db.query(GeneratedPage).filter(
        GeneratedPage.project_id == project_id
    ).order_by(GeneratedPage.created_at.desc()).limit(5).all()
    
    recent_pages = []
    for page in recent_pages_query:
        recent_pages.append({
            "id": page.id,
            "title": page.title,
            "template_id": page.template_id,
            "created_at": page.created_at.isoformat(),
            "word_count": page.meta_data.get("word_count", 0) if page.meta_data else 0,
            "quality_score": page.meta_data.get("quality_score", 0) if page.meta_data else 0
        })
    
    # Calculate overall generation progress
    generation_progress = (total_generated_pages / total_potential_pages * 100) if total_potential_pages > 0 else 0
    
    # Determine next actions
    next_actions = []
    if total_templates == 0:
        next_actions.append("Create your first template")
    elif total_data_rows == 0:
        next_actions.append("Import data or generate variables")
    elif total_potential_pages == 0:
        next_actions.append("Generate potential pages")
    elif total_generated_pages == 0:
        next_actions.append("Generate your first batch of pages")
    elif generation_progress < 100:
        next_actions.append(f"Continue generating pages ({int(generation_progress)}% complete)")
    else:
        next_actions.append("Export your generated pages")
        next_actions.append("Create additional templates")
    
    return ProjectStatsResponse(
        project_id=project_id,
        total_templates=total_templates,
        total_data_rows=total_data_rows,
        total_potential_pages=total_potential_pages,
        total_generated_pages=total_generated_pages,
        pages_by_template=pages_by_template,
        recent_pages=recent_pages,
        generation_progress=generation_progress,
        next_actions=next_actions
    )

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
    print(f"DEBUG: Received template creation request for project_id: {project_id}")
    print(f"DEBUG: Template data: {template.dict()}")
    
    # Check if project exists
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        print(f"DEBUG: Project {project_id} not found!")
        raise HTTPException(status_code=404, detail="Project not found")
    
    print(f"DEBUG: Found project: {project.name}")
    
    # Create template structure
    template_data = template.dict()
    structured_template = template_engine.create_template_structure(template_data)
    print(f"DEBUG: Structured template: {structured_template}")
    
    # Validate template
    validation = template_engine.validate_template(template_data)
    if not validation['is_valid']:
        raise HTTPException(
            status_code=400, 
            detail={"errors": validation['errors'], "warnings": validation['warnings']}
        )
    
    # Create database template
    print(f"DEBUG: Creating template for project_id: {project_id}")
    print(f"DEBUG: Template name: {structured_template['name']}")
    print(f"DEBUG: Template pattern: {structured_template['pattern']}")
    
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
    
    print(f"DEBUG: Template created successfully with id: {db_template.id}")
    
    return db_template

@app.get("/api/projects/{project_id}/templates", response_model=List[TemplateResponse])
def list_project_templates(project_id: str, db: Session = Depends(get_db)):
    """List all templates for a project"""
    print(f"DEBUG: Fetching templates for project_id: {project_id}")
    
    # Check if project exists
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        print(f"DEBUG: Project {project_id} not found!")
        raise HTTPException(status_code=404, detail="Project not found")
    
    print(f"DEBUG: Project found: {project.name}")
    
    templates = db.query(Template).filter(Template.project_id == project_id).all()
    print(f"DEBUG: Found {len(templates)} templates for project {project_id}")
    for template in templates:
        print(f"DEBUG: - Template {template.id}: {template.name} (project_id: {template.project_id})")
    
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
    
    # CRITICAL: Validate AI is available for programmatic SEO
    if not page_generator:
        raise HTTPException(
            status_code=503, 
            detail={
                "error": "AI_PROVIDER_REQUIRED",
                "message": "Programmatic SEO requires AI providers for dynamic content generation",
                "details": ai_initialization_error,
                "setup_instructions": [
                    "Configure at least one AI provider:",
                    "• OPENAI_API_KEY=your_openai_key",
                    "• ANTHROPIC_API_KEY=your_anthropic_key", 
                    "• PERPLEXITY_API_KEY=your_perplexity_key",
                    "Then restart the application."
                ]
            }
        )
    
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
    potential_pages_generated: Optional[int] = None
    potential_pages_url: Optional[str] = None

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
        
        # Track API cost
        token_usage = variable_generator.get_token_usage()
        if token_usage.get("input", 0) > 0:
            CostTracker.track_api_call(
                db=db,
                project_id=project_id,
                operation_type=OperationType.VARIABLE_GENERATION,
                provider="perplexity",
                model="sonar",
                input_tokens=token_usage["input"],
                output_tokens=token_usage["output"],
                details={
                    "template_id": template_id,
                    "template_pattern": template.pattern,
                    "variables_generated": len(result["variables"]),
                    "total_combinations": result["total_count"]
                }
            )
        
        # Store the generated variables for later use
        # Convert the AI response format to the format expected by potential pages
        formatted_variables = {}
        for var_name, var_values in result["variables"].items():
            if isinstance(var_values, list):
                formatted_variables[var_name] = [
                    {
                        'value': val,
                        'dataset_id': 'ai_generated',
                        'dataset_name': 'AI Generated Variables',
                        'metadata': {}
                    } for val in var_values
                ]
        
        # Automatically generate potential pages with the AI-generated variables
        try:
            # Clear existing potential pages
            db.query(PotentialPage).filter(
                PotentialPage.project_id == project_id,
                PotentialPage.template_id == template_id
            ).delete()
            
            # Generate combinations
            variable_combinations = page_generator.generate_all_combinations(formatted_variables)
            
            # Create potential pages
            potential_pages = []
            for i, variables in enumerate(variable_combinations[:1000]):  # Limit to 1000 for safety
                title = page_generator.replace_variables_in_content(template.pattern, variables)
                slug = title.lower().replace(' ', '-').replace('?', '').replace(',', '').replace(':', '')
                
                potential_page = PotentialPage(
                    project_id=project_id,
                    template_id=template_id,
                    title=title,
                    slug=slug,
                    variables=variables,
                    priority=0
                )
                potential_pages.append(potential_page)
            
            # Batch insert
            if potential_pages:
                db.add_all(potential_pages)
                db.commit()
                
            # Add potential pages info to response
            result["potential_pages_generated"] = len(potential_pages)
            result["potential_pages_url"] = f"/api/projects/{project_id}/templates/{template_id}/potential-pages"
            
        except Exception as pp_error:
            print(f"Warning: Could not generate potential pages: {str(pp_error)}")
            # Don't fail the whole request, just log the warning
        
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
    print(f"DEBUG: Generate pages called for project={project_id}, template={template_id}")
    print(f"DEBUG: Request data: batch_size={request.batch_size}, selected_titles={len(request.selected_titles) if request.selected_titles else 0}, has_variables={bool(request.variables_data)}")
    
    # CRITICAL: Validate AI is available for programmatic SEO
    if not page_generator:
        raise HTTPException(
            status_code=503, 
            detail={
                "error": "AI_PROVIDER_REQUIRED",
                "message": "Programmatic SEO requires AI providers for high-quality, scalable content generation",
                "details": ai_initialization_error,
                "why_ai_required": [
                    "• Generate unique content for hundreds/thousands of pages",
                    "• Ensure content quality that ranks in search engines", 
                    "• Provide real value to users (not just template-filled content)",
                    "• Scale content production without quality degradation"
                ],
                "setup_instructions": [
                    "Configure at least one AI provider:",
                    "• OPENAI_API_KEY=your_openai_key",
                    "• ANTHROPIC_API_KEY=your_anthropic_key", 
                    "• PERPLEXITY_API_KEY=your_perplexity_key",
                    "Then restart the application."
                ]
            }
        )
    
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
            print(f"DEBUG: Using AI-generated variables: {list(request.variables_data.keys())}")
            print(f"DEBUG: Number of selected titles: {len(request.selected_titles)}")
            
            total_generated, page_ids = page_generator.generate_pages_from_variables(
                project_id, template_id, 
                request.variables_data,
                request.selected_titles,
                db, batch_size=request.batch_size
            )
            
            print(f"DEBUG: Generated {total_generated} pages with IDs: {page_ids[:5]}...")
        else:
            # Use traditional CSV data
            total_generated, page_ids = page_generator.generate_all_pages(
                project_id, template_id, db, batch_size=request.batch_size
            )
        
        # Filter out any None IDs (shouldn't happen with flush, but just in case)
        valid_page_ids = [pid for pid in page_ids if pid is not None]
        
        print(f"DEBUG: Total generated: {total_generated}, Valid page IDs: {len(valid_page_ids)}")
        
        return GeneratePagesResponse(
            total_generated=total_generated,
            page_ids=valid_page_ids,
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

class AIStrategyRequest(BaseModel):
    business_input: str
    business_url: Optional[str] = None

class AIStrategyResponse(BaseModel):
    strategy: dict
    templates_generated: int
    implementation_plan: dict

class GeneratePotentialPagesRequest(BaseModel):
    variables_data: Optional[dict] = None
    max_combinations: Optional[int] = 1000

class PotentialPageResponse(BaseModel):
    id: str
    title: str
    slug: str
    variables: dict
    is_generated: bool
    priority: int
    created_at: str

class PotentialPagesListResponse(BaseModel):
    potential_pages: List[PotentialPageResponse]
    total_count: int
    generated_count: int
    remaining_count: int

class GenerateSelectedPagesRequest(BaseModel):
    page_ids: List[str]
    batch_size: Optional[int] = 10

# Page Preview & Selection endpoints
@app.post("/api/projects/{project_id}/templates/{template_id}/generate-potential-pages")
async def generate_potential_pages(
    project_id: str,
    template_id: str,
    request: GeneratePotentialPagesRequest,
    db: Session = Depends(get_db)
):
    """Generate and save all potential pages for preview and selection"""
    
    # Validate project and template exist
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    template = db.query(Template).filter(
        Template.id == template_id,
        Template.project_id == project_id
    ).first()
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    
    try:
        # Clear existing potential pages for this template
        db.query(PotentialPage).filter(
            PotentialPage.project_id == project_id,
            PotentialPage.template_id == template_id
        ).delete()
        
        # Generate all possible combinations
        if request.variables_data:
            # Use provided data
            variable_combinations = page_generator.generate_all_combinations(request.variables_data)
        else:
            # Try to use AI-generated variables first
            # Check if template has generated variables from the AI generation endpoint
            if hasattr(template, 'generated_variables_data') and template.generated_variables_data:
                # Convert AI-generated format to expected format
                ai_variables = template.generated_variables_data
                variable_data = {}
                
                for var_name, var_values in ai_variables.items():
                    if isinstance(var_values, list):
                        # Convert simple list to expected format
                        variable_data[var_name] = [
                            {
                                'value': val,
                                'dataset_id': 'ai_generated',
                                'dataset_name': 'AI Generated',
                                'metadata': {}
                            } for val in var_values
                        ]
                
                if variable_data:
                    variable_combinations = page_generator.generate_all_combinations(variable_data)
                else:
                    # Fallback to datasets
                    variable_data = page_generator.load_datasets_for_variables(project_id, template, db)
                    variable_combinations = page_generator.generate_all_combinations(variable_data)
            else:
                # Load data from datasets
                variable_data = page_generator.load_datasets_for_variables(project_id, template, db)
                variable_combinations = page_generator.generate_all_combinations(variable_data)
        
        # Limit combinations if requested
        if request.max_combinations and len(variable_combinations) > request.max_combinations:
            variable_combinations = variable_combinations[:request.max_combinations]
        
        # Create potential pages
        potential_pages = []
        for i, variables in enumerate(variable_combinations):
            # Generate title and slug
            title = page_generator.replace_variables_in_content(template.pattern, variables)
            slug = title.lower().replace(' ', '-').replace('?', '').replace(',', '').replace(':', '')
            
            potential_page = PotentialPage(
                project_id=project_id,
                template_id=template_id,
                title=title,
                slug=slug,
                variables=variables,
                priority=0  # Default priority
            )
            potential_pages.append(potential_page)
        
        # Batch insert for performance
        db.add_all(potential_pages)
        db.commit()
        
        return {
            "message": f"Generated {len(potential_pages)} potential pages",
            "total_potential_pages": len(potential_pages),
            "template_pattern": template.pattern,
            "preview_url": f"/api/projects/{project_id}/templates/{template_id}/potential-pages"
        }
        
    except Exception as e:
        print(f"❌ Potential page generation failed: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Potential page generation failed: {str(e)}"
        )

@app.get("/api/projects/{project_id}/templates/{template_id}/potential-pages", response_model=PotentialPagesListResponse)
async def get_potential_pages(
    project_id: str,
    template_id: str,
    offset: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """Get potential pages for preview and selection"""
    
    # Get total counts
    total_count = db.query(PotentialPage).filter(
        PotentialPage.project_id == project_id,
        PotentialPage.template_id == template_id
    ).count()
    
    generated_count = db.query(PotentialPage).filter(
        PotentialPage.project_id == project_id,
        PotentialPage.template_id == template_id,
        PotentialPage.is_generated == 1
    ).count()
    
    # Get paginated potential pages
    potential_pages = db.query(PotentialPage).filter(
        PotentialPage.project_id == project_id,
        PotentialPage.template_id == template_id
    ).order_by(PotentialPage.priority.desc(), PotentialPage.created_at).offset(offset).limit(limit).all()
    
    pages_data = []
    for page in potential_pages:
        pages_data.append(PotentialPageResponse(
            id=page.id,
            title=page.title,
            slug=page.slug,
            variables=page.variables,
            is_generated=bool(page.is_generated),
            priority=page.priority,
            created_at=page.created_at.isoformat()
        ))
    
    return PotentialPagesListResponse(
        potential_pages=pages_data,
        total_count=total_count,
        generated_count=generated_count,
        remaining_count=total_count - generated_count
    )

@app.post("/api/projects/{project_id}/templates/{template_id}/generate-selected-pages")
async def generate_selected_pages(
    project_id: str,
    template_id: str,
    request: GenerateSelectedPagesRequest,
    db: Session = Depends(get_db)
):
    """Generate content for selected potential pages"""
    
    # Validate AI is available
    if not page_generator:
        raise HTTPException(
            status_code=503,
            detail={
                "error": "AI_PROVIDER_REQUIRED", 
                "message": "AI providers required for content generation",
                "details": ai_initialization_error
            }
        )
    
    try:
        # Get selected potential pages
        potential_pages = db.query(PotentialPage).filter(
            PotentialPage.id.in_(request.page_ids),
            PotentialPage.project_id == project_id,
            PotentialPage.template_id == template_id,
            PotentialPage.is_generated == 0  # Only generate pages that haven't been generated yet
        ).all()
        
        if not potential_pages:
            raise HTTPException(status_code=404, detail="No valid potential pages found for generation")
        
        # Get template
        template = db.query(Template).filter(Template.id == template_id).first()
        if not template:
            raise HTTPException(status_code=404, detail="Template not found")
        
        # Generate pages
        generated_pages = []
        for potential_page in potential_pages:
            try:
                # Generate content using the page generator
                page_content = page_generator.generate_unique_content(
                    template, potential_page.variables, 0, len(potential_pages)
                )
                
                # Create generated page (using correct model fields)
                generated_page = GeneratedPage(
                    project_id=project_id,
                    template_id=template_id,
                    title=page_content.get("title", potential_page.title),
                    content=page_content,  # Store all content as JSON
                    meta_data={
                        "slug": potential_page.slug,
                        "keyword": page_content.get("keyword", potential_page.title),
                        "variables": potential_page.variables,
                        "meta_description": page_content.get("meta_description", ""),
                        "word_count": page_content.get("word_count", 0),
                        "quality_score": page_content.get("quality_score", 0),
                        "generated_from_potential_page": potential_page.id
                    }
                )
                
                db.add(generated_page)
                db.flush()  # Get the ID
                
                # Update potential page to mark as generated
                potential_page.is_generated = 1
                potential_page.generated_page_id = generated_page.id
                
                generated_pages.append({
                    "id": generated_page.id,
                    "title": generated_page.title,
                    "slug": generated_page.meta_data.get("slug", ""),
                    "word_count": generated_page.meta_data.get("word_count", 0),
                    "quality_score": generated_page.meta_data.get("quality_score", 0)
                })
                
            except Exception as e:
                print(f"❌ Failed to generate page '{potential_page.title}': {str(e)}")
                continue
        
        db.commit()
        
        return {
            "message": f"Successfully generated {len(generated_pages)} pages",
            "generated_pages": generated_pages,
            "total_requested": len(request.page_ids),
            "successful_generations": len(generated_pages)
        }
        
    except Exception as e:
        print(f"❌ Selected page generation failed: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Selected page generation failed: {str(e)}"
        )

# AI Strategy Generation endpoint
@app.post("/api/generate-ai-strategy", response_model=AIStrategyResponse)
async def generate_ai_strategy(
    request: AIStrategyRequest,
    db: Session = Depends(get_db)
):
    """Generate a complete AI-powered programmatic SEO strategy for a business"""
    
    # Validate AI Strategy Generator is available
    if not ai_strategy_generator:
        raise HTTPException(
            status_code=503,
            detail={
                "error": "AI_STRATEGY_GENERATOR_UNAVAILABLE",
                "message": "AI Strategy Generator requires AI providers for business analysis and strategy creation",
                "details": strategy_generator_error,
                "setup_instructions": [
                    "Configure at least one AI provider:",
                    "• OPENAI_API_KEY=your_openai_key",
                    "• ANTHROPIC_API_KEY=your_anthropic_key",
                    "• PERPLEXITY_API_KEY=your_perplexity_key",
                    "Then restart the application."
                ]
            }
        )
    
    try:
        print(f"🚀 Generating AI strategy for: {request.business_input[:50]}...")
        
        # Generate complete strategy
        strategy = await ai_strategy_generator.generate_complete_strategy(
            business_input=request.business_input,
            business_url=request.business_url
        )
        
        templates_count = len(strategy.get("custom_templates", []))
        implementation_plan = strategy.get("implementation_plan", {})
        
        print(f"✅ Strategy generated with {templates_count} templates")
        
        return AIStrategyResponse(
            strategy=strategy,
            templates_generated=templates_count,
            implementation_plan=implementation_plan
        )
        
    except Exception as e:
        print(f"❌ AI strategy generation failed: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail={
                "error": "STRATEGY_GENERATION_FAILED", 
                "message": f"AI strategy generation failed: {str(e)}",
                "business_input": request.business_input
            }
        )

@app.post("/api/projects/{project_id}/implement-ai-strategy")
async def implement_ai_strategy(
    project_id: str,
    strategy_data: dict,
    db: Session = Depends(get_db)
):
    """Create templates and data structures from an AI-generated strategy"""
    
    # Validate project exists
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    try:
        custom_templates = strategy_data.get("custom_templates", [])
        created_templates = []
        
        for template_data in custom_templates:
            # Create template in database
            template = Template(
                project_id=project_id,
                name=template_data.get("template_name", "AI Generated Template"),
                pattern=template_data.get("template_pattern", ""),
                template_sections={
                    "seo_structure": {
                        "title_template": template_data.get("template_pattern", ""),
                        "h1_template": template_data.get("h1_pattern", ""),
                        "meta_description_template": template_data.get("seo_strategy", {}).get("meta_description_template", "")
                    },
                    "content_strategy": template_data.get("content_strategy", {}),
                    "ai_generated": True,
                    "generation_date": datetime.now().isoformat()
                },
                variables=template_data.get("target_variables", [])
            )
            
            db.add(template)
            db.commit()
            db.refresh(template)
            
            created_templates.append({
                "id": template.id,
                "name": template.name,
                "pattern": template.pattern,
                "variables": len(template.variables)
            })
        
        return {
            "message": f"Successfully implemented AI strategy with {len(created_templates)} templates",
            "templates_created": created_templates,
            "implementation_plan": strategy_data.get("implementation_plan", {}),
            "next_steps": [
                "Generate or import data for template variables",
                "Test content generation with sample data",
                "Scale to full page generation"
            ]
        }
        
    except Exception as e:
        print(f"❌ Strategy implementation failed: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Strategy implementation failed: {str(e)}"
        )

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