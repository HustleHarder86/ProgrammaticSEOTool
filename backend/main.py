"""Minimal FastAPI backend to test Railway deployment"""
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy.orm import Session
from datetime import datetime
import os
from ai_client import AIClient
from database import get_db, init_db
from models import Project, Template, DataSet, GeneratedPage

app = FastAPI(title="Programmatic SEO Tool API")
ai_client = AIClient()

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