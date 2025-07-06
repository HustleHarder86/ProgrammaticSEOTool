"""Main API Integration Module - Orchestrates all agents for the complete workflow"""
import asyncio
import json
import logging
import uuid
from typing import Dict, List, Optional, Any, Union
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from enum import Enum

from fastapi import APIRouter, HTTPException, BackgroundTasks, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

# Import all agents
from agents.business_analyzer import BusinessAnalyzerAgent, BusinessAnalysis, TemplateOpportunity
from agents.template_builder import TemplateBuilderAgent
from agents.data_manager import DataManagerAgent
from agents.page_generator import PageGeneratorAgent
from agents.export_manager import ExportManagerAgent
from agents.database_agent import DatabaseAgent

# Import utilities
from models import get_db
from api.ai_handler import AIHandler
from config import settings

logger = logging.getLogger(__name__)

# Create API router
router = APIRouter(prefix="/api", tags=["integration"])

# Workflow status tracking
class WorkflowStatus(str, Enum):
    PENDING = "pending"
    ANALYZING = "analyzing"
    BUILDING_TEMPLATE = "building_template"
    IMPORTING_DATA = "importing_data"
    GENERATING_PAGES = "generating_pages"
    EXPORTING = "exporting"
    COMPLETED = "completed"
    FAILED = "failed"

@dataclass
class WorkflowState:
    """Tracks the state of a workflow operation"""
    id: str
    status: WorkflowStatus
    current_step: str
    progress: float  # 0.0 to 1.0
    created_at: datetime
    updated_at: datetime
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

# Global workflow tracker
workflow_tracker: Dict[str, WorkflowState] = {}

# Request/Response Models
class BusinessAnalysisRequest(BaseModel):
    input_type: str = Field(..., description="'text' or 'url'")
    content: str = Field(..., description="Business description or URL")
    market_context: Optional[Dict[str, str]] = Field(None, description="Additional context")

class TemplateCreationRequest(BaseModel):
    business_analysis: Dict[str, Any] = Field(..., description="Business analysis results")
    template_pattern: str = Field(..., description="Template pattern to build")
    template_name: str = Field(..., description="Name for the template")
    custom_variables: Optional[List[str]] = Field(None, description="Additional variables")

class TemplateValidationRequest(BaseModel):
    template_id: str = Field(..., description="Template ID to validate")
    sample_data: Dict[str, str] = Field(..., description="Sample data for preview")

class DataImportRequest(BaseModel):
    file_path: Optional[str] = Field(None, description="Path to CSV/JSON file")
    data_json: Optional[List[Dict[str, Any]]] = Field(None, description="Direct JSON data")
    data_type: str = Field(..., description="Type of data being imported")
    validation_rules: Optional[Dict[str, Any]] = Field(None, description="Custom validation rules")

class PageGenerationRequest(BaseModel):
    template_id: str = Field(..., description="Template to use")
    data_set_id: str = Field(..., description="Data set to use")
    limit: Optional[int] = Field(None, description="Max pages to generate")
    enable_variations: bool = Field(True, description="Generate content variations")
    internal_linking: bool = Field(True, description="Enable internal linking")
    ai_enhancement: bool = Field(True, description="Use AI to enhance content")

class ExportRequest(BaseModel):
    page_ids: Optional[List[str]] = Field(None, description="Specific pages to export")
    formats: List[str] = Field(..., description="Export formats")
    compression: bool = Field(False, description="Compress output")
    wordpress_config: Optional[Dict[str, str]] = Field(None, description="WordPress API config")
    scheduling: Optional[Dict[str, Any]] = Field(None, description="Publishing schedule")

class CompleteWorkflowRequest(BaseModel):
    business_input: BusinessAnalysisRequest
    template_selection: Optional[str] = Field(None, description="Auto-select template pattern")
    data_source: DataImportRequest
    generation_config: Optional[Dict[str, Any]] = Field(None, description="Page generation settings")
    export_config: ExportRequest

# API Integration Class
class APIIntegration:
    """Main integration class that orchestrates all agents"""
    
    def __init__(self):
        self.ai_handler = AIHandler() if settings.has_ai_provider else None
        self.business_analyzer = BusinessAnalyzerAgent(self.ai_handler)
        self.template_builder = TemplateBuilderAgent()
        self.data_manager = DataManagerAgent()
        # Page generator will be initialized when needed with proper AI client
        self.page_generator = None
        self.export_manager = ExportManagerAgent()
        self.executor = ThreadPoolExecutor(max_workers=4)
    
    def create_workflow_id(self) -> str:
        """Generate unique workflow ID"""
        return str(uuid.uuid4())
    
    def update_workflow_status(
        self, 
        workflow_id: str, 
        status: WorkflowStatus, 
        current_step: str,
        progress: float,
        result: Optional[Dict[str, Any]] = None,
        error: Optional[str] = None
    ):
        """Update workflow status"""
        if workflow_id in workflow_tracker:
            state = workflow_tracker[workflow_id]
            state.status = status
            state.current_step = current_step
            state.progress = progress
            state.updated_at = datetime.now()
            if result:
                state.result = result
            if error:
                state.error = error
    
    async def analyze_business_templates(
        self, 
        request: BusinessAnalysisRequest
    ) -> Dict[str, Any]:
        """Analyze business and suggest templates"""
        try:
            # Analyze business
            if request.input_type == "text":
                business_analysis = self.business_analyzer.analyze_business(request.content)
            else:
                business_analysis = await self.business_analyzer.analyze_business_url(request.content)
            
            # Get template suggestions
            templates = self.business_analyzer.suggest_templates(business_analysis)
            
            # Get data requirements for each template
            template_data = []
            for template in templates:
                data_reqs = self.business_analyzer.identify_data_requirements(template)
                template_data.append({
                    "template": template.__dict__,
                    "data_requirements": [req.__dict__ for req in data_reqs]
                })
            
            return {
                "business_analysis": business_analysis.__dict__,
                "suggested_templates": template_data,
                "total_templates": len(templates)
            }
            
        except Exception as e:
            logger.error(f"Business analysis error: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    async def create_template(
        self,
        request: TemplateCreationRequest
    ) -> Dict[str, Any]:
        """Create a new template"""
        try:
            # Extract business info
            business_info = request.business_analysis
            
            # Create template
            template_data = {
                "pattern": request.template_pattern,
                "name": request.template_name,
                "variables": request.custom_variables or []
            }
            
            template = self.template_builder.create_template_from_pattern(
                pattern=template_data["pattern"],
                template_type="custom",
                custom_config={
                    "name": template_data["name"],
                    "description": f"Template for {business_info.get('industry', 'business')}",
                    "variables": template_data["variables"]
                }
            )
            
            return {
                "template_id": template["template_id"],
                "template": template,
                "validation": template.get("validation", {})
            }
            
        except Exception as e:
            logger.error(f"Template creation error: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    async def validate_template(
        self,
        request: TemplateValidationRequest
    ) -> Dict[str, Any]:
        """Validate template with sample data"""
        try:
            # Get template
            template = self.template_builder.templates.get(request.template_id)
            if not template:
                raise HTTPException(status_code=404, detail="Template not found")
            
            # Validate with sample data
            validation_result = self.template_builder.validate_template(
                template_id=request.template_id,
                sample_data=[request.sample_data]
            )
            
            # Generate preview
            preview = self.template_builder.preview_generation(
                template_id=request.template_id,
                data_combinations=[request.sample_data],
                limit=1
            )
            
            return {
                "valid": validation_result["valid"],
                "issues": validation_result.get("issues", []),
                "preview": preview[0] if preview else None
            }
            
        except Exception as e:
            logger.error(f"Template validation error: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    async def import_data(
        self,
        request: DataImportRequest
    ) -> Dict[str, Any]:
        """Import data for template population"""
        try:
            # Import data
            if request.file_path:
                result = self.data_manager.import_csv(
                    file_path=request.file_path,
                    data_type=request.data_type
                )
            elif request.data_json:
                # Save JSON data temporarily
                temp_file = f"/tmp/data_{datetime.now().timestamp()}.json"
                with open(temp_file, 'w') as f:
                    json.dump(request.data_json, f)
                
                result = self.data_manager.import_json(
                    file_path=temp_file,
                    data_type=request.data_type
                )
            else:
                raise HTTPException(status_code=400, detail="No data source provided")
            
            # Apply validation if provided
            if request.validation_rules:
                validation_result = self.data_manager.validate_data_set(
                    data_set_id=result["data_set_id"],
                    custom_rules=request.validation_rules
                )
                result["validation"] = validation_result
            
            return result
            
        except Exception as e:
            logger.error(f"Data import error: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    async def generate_pages_bulk(
        self,
        request: PageGenerationRequest
    ) -> Dict[str, Any]:
        """Generate pages in bulk"""
        try:
            # Initialize page generator if needed
            if not self.page_generator:
                from agents.page_generator import PageGeneratorAgent
                self.page_generator = PageGeneratorAgent()
            
            # Get data combinations
            data_combinations = self.data_manager.get_data_combinations(
                data_set_id=request.data_set_id,
                limit=request.limit
            )
            
            # Generate pages
            generation_result = await self.page_generator.generate_pages(
                template_id=request.template_id,
                data_combinations=data_combinations,
                enable_variations=request.enable_variations,
                variation_count=3 if request.enable_variations else 1,
                internal_linking=request.internal_linking,
                ai_enhancement=request.ai_enhancement
            )
            
            return {
                "generated_pages": len(generation_result["pages"]),
                "unique_pages": generation_result["stats"]["unique_pages"],
                "variations_created": generation_result["stats"]["variations_created"],
                "internal_links_added": generation_result["stats"]["internal_links_added"],
                "page_ids": [p["page_id"] for p in generation_result["pages"]],
                "sample_pages": generation_result["pages"][:3]  # First 3 as samples
            }
            
        except Exception as e:
            logger.error(f"Page generation error: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    async def export_content(
        self,
        request: ExportRequest,
        db: Session
    ) -> Dict[str, Any]:
        """Export generated content"""
        try:
            # Prepare pages for export
            if request.page_ids:
                pages = [
                    self.page_generator.generated_pages.get(pid)
                    for pid in request.page_ids
                    if pid in self.page_generator.generated_pages
                ]
            else:
                pages = list(self.page_generator.generated_pages.values())
            
            if not pages:
                raise HTTPException(status_code=404, detail="No pages found for export")
            
            # Configure export
            export_config = {
                "formats": request.formats,
                "compression": request.compression,
                "wordpress_config": request.wordpress_config,
                "scheduling": request.scheduling
            }
            
            # Execute export
            export_result = await self.export_manager.export_pages(
                pages=pages,
                export_config=export_config,
                output_dir=settings.exports_dir
            )
            
            return {
                "export_id": export_result["export_id"],
                "formats_exported": export_result["formats"],
                "total_pages": export_result["total_pages"],
                "file_paths": export_result["file_paths"],
                "wordpress_deployment": export_result.get("wordpress_deployment"),
                "scheduled_posts": export_result.get("scheduled_posts", 0)
            }
            
        except Exception as e:
            logger.error(f"Export error: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    async def run_complete_workflow(
        self,
        request: CompleteWorkflowRequest,
        background_tasks: BackgroundTasks
    ) -> Dict[str, Any]:
        """Run the complete workflow asynchronously"""
        workflow_id = self.create_workflow_id()
        
        # Initialize workflow state
        workflow_tracker[workflow_id] = WorkflowState(
            id=workflow_id,
            status=WorkflowStatus.PENDING,
            current_step="Initializing",
            progress=0.0,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        # Run workflow in background
        background_tasks.add_task(
            self._execute_complete_workflow,
            workflow_id,
            request
        )
        
        return {
            "workflow_id": workflow_id,
            "status": "started",
            "check_status_url": f"/api/workflow-status/{workflow_id}"
        }
    
    async def _execute_complete_workflow(
        self,
        workflow_id: str,
        request: CompleteWorkflowRequest
    ):
        """Execute the complete workflow"""
        try:
            # Step 1: Business Analysis
            self.update_workflow_status(
                workflow_id, 
                WorkflowStatus.ANALYZING,
                "Analyzing business",
                0.1
            )
            
            analysis_result = await self.analyze_business_templates(request.business_input)
            
            # Step 2: Template Creation/Selection
            self.update_workflow_status(
                workflow_id,
                WorkflowStatus.BUILDING_TEMPLATE,
                "Creating template",
                0.3
            )
            
            # Auto-select best template if not specified
            if request.template_selection:
                template_pattern = request.template_selection
            else:
                templates = analysis_result["suggested_templates"]
                if templates:
                    template_pattern = templates[0]["template"]["pattern"]
                else:
                    raise Exception("No suitable templates found")
            
            template_request = TemplateCreationRequest(
                business_analysis=analysis_result["business_analysis"],
                template_pattern=template_pattern,
                template_name=f"Auto-generated template for {analysis_result['business_analysis']['business_name']}"
            )
            
            template_result = await self.create_template(template_request)
            
            # Step 3: Data Import
            self.update_workflow_status(
                workflow_id,
                WorkflowStatus.IMPORTING_DATA,
                "Importing data",
                0.5
            )
            
            data_result = await self.import_data(request.data_source)
            
            # Step 4: Page Generation
            self.update_workflow_status(
                workflow_id,
                WorkflowStatus.GENERATING_PAGES,
                "Generating pages",
                0.7
            )
            
            generation_config = request.generation_config or {}
            page_request = PageGenerationRequest(
                template_id=template_result["template_id"],
                data_set_id=data_result["data_set_id"],
                **generation_config
            )
            
            pages_result = await self.generate_pages_bulk(page_request)
            
            # Step 5: Export
            self.update_workflow_status(
                workflow_id,
                WorkflowStatus.EXPORTING,
                "Exporting content",
                0.9
            )
            
            # Create a mock session for export
            from models import get_db
            db = next(get_db())
            
            export_result = await self.export_content(request.export_config, db)
            
            # Complete workflow
            self.update_workflow_status(
                workflow_id,
                WorkflowStatus.COMPLETED,
                "Workflow completed",
                1.0,
                result={
                    "business_analysis": analysis_result,
                    "template": template_result,
                    "data_import": data_result,
                    "pages_generated": pages_result,
                    "export": export_result
                }
            )
            
        except Exception as e:
            logger.error(f"Workflow error: {e}")
            self.update_workflow_status(
                workflow_id,
                WorkflowStatus.FAILED,
                "Workflow failed",
                workflow_tracker[workflow_id].progress,
                error=str(e)
            )

# Initialize integration
integration = APIIntegration()

# API Endpoints
@router.post("/analyze-business-templates")
async def analyze_business_templates(request: BusinessAnalysisRequest):
    """Analyze business and suggest programmatic SEO templates"""
    return await integration.analyze_business_templates(request)

@router.post("/create-template")
async def create_template(request: TemplateCreationRequest):
    """Create a new page template"""
    return await integration.create_template(request)

@router.post("/validate-template")
async def validate_template(request: TemplateValidationRequest):
    """Validate template with sample data"""
    return await integration.validate_template(request)

@router.post("/import-data")
async def import_data(request: DataImportRequest):
    """Import data for template population"""
    return await integration.import_data(request)

@router.post("/generate-pages-bulk")
async def generate_pages_bulk(request: PageGenerationRequest):
    """Generate pages in bulk using template and data"""
    return await integration.generate_pages_bulk(request)

@router.post("/export-content")
async def export_content(request: ExportRequest, db: Session = Depends(get_db)):
    """Export generated content in various formats"""
    return await integration.export_content(request, db)

@router.get("/workflow-status/{workflow_id}")
async def get_workflow_status(workflow_id: str):
    """Check the status of a workflow operation"""
    if workflow_id not in workflow_tracker:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    state = workflow_tracker[workflow_id]
    return {
        "workflow_id": state.id,
        "status": state.status,
        "current_step": state.current_step,
        "progress": state.progress,
        "created_at": state.created_at,
        "updated_at": state.updated_at,
        "result": state.result,
        "error": state.error,
        "metadata": state.metadata
    }

@router.post("/complete-workflow")
async def run_complete_workflow(
    request: CompleteWorkflowRequest,
    background_tasks: BackgroundTasks
):
    """Run the complete workflow from business analysis to export"""
    return await integration.run_complete_workflow(request, background_tasks)

# Utility endpoints
@router.get("/supported-formats")
async def get_supported_formats():
    """Get list of supported export formats"""
    return {
        "formats": ExportManagerAgent.SUPPORTED_FORMATS,
        "presets": ExportManagerAgent.EXPORT_PRESETS
    }

@router.get("/template-library")
async def get_template_library():
    """Get available template patterns"""
    return {
        "templates": integration.template_builder.template_library,
        "total": len(integration.template_builder.template_library)
    }

@router.post("/test-ai-connection")
async def test_ai_connection():
    """Test AI provider connection"""
    if not settings.has_ai_provider:
        return {
            "connected": False,
            "error": "No AI provider configured"
        }
    
    try:
        # Test with a simple prompt
        test_result = await integration.ai_handler.generate(
            "Say 'Connection successful' if you can read this.",
            max_tokens=20
        )
        
        return {
            "connected": True,
            "provider": settings.ai_provider,
            "response": test_result
        }
    except Exception as e:
        return {
            "connected": False,
            "error": str(e)
        }