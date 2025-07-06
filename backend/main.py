"""Main FastAPI application."""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict
import logging
from datetime import datetime
import os

from config import settings
from backend.models import init_db, get_db
from backend.agents.database_agent import DatabaseAgent
from sqlalchemy.orm import Session
from fastapi import Depends

# Initialize database on startup
init_db()

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL.upper()),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Programmatic SEO Tool",
    description="Generate thousands of SEO-optimized pages automatically",
    version="0.1.0",
    debug=settings.DEBUG
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class HealthResponse(BaseModel):
    status: str
    timestamp: datetime
    version: str
    ai_provider: Optional[str] = None

class BusinessInput(BaseModel):
    input_type: str  # "text" or "url"
    content: str  # Either business description or URL

class TemplateGenerationRequest(BaseModel):
    business_url_or_description: str
    market_context: Optional[Dict[str, str]] = None  # Additional context like location, industry focus
    
class KeywordGenerationRequest(BaseModel):
    business_input: BusinessInput
    max_keywords: int = 100
    include_variations: bool = True

class ContentGenerationRequest(BaseModel):
    keywords: List[str]
    template: str = "comparison"  # comparison, how-to, best-x-for-y, etc.
    variations_per_keyword: int = 1

class ProjectCreateRequest(BaseModel):
    name: str
    business_description: str
    business_url: Optional[str] = None
    industry: Optional[str] = None
    location: Optional[str] = None

class KeywordAddRequest(BaseModel):
    keywords: List[Dict[str, any]]

class KeywordDiscoveryRequest(BaseModel):
    seed_keywords: List[str]
    limit: int = 50

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint."""
    agents_loaded = False
    try:
        # Check if agents are available
        from backend.agents.business_analyzer import BusinessAnalyzerAgent
        from backend.agents.template_builder import TemplateBuilderAgent
        from backend.agents.data_manager import DataManagerAgent
        from backend.agents.page_generator import PageGeneratorAgent
        from backend.agents.export_manager import ExportManagerAgent
        agents_loaded = True
    except:
        pass
    
    return {
        "message": "Programmatic SEO Tool API",
        "version": "2.0.0",
        "docs": "/docs",
        "health": "/health",
        "agents_loaded": agents_loaded,
        "endpoints": {
            "legacy": "/api/analyze-business, /api/generate-keywords, /api/generate-content",
            "new": "/api/analyze-business-templates, /api/create-template, /api/generate-pages-bulk, /api/complete-workflow"
        }
    }

# Health check endpoint
@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    # Check AI provider configuration
    ai_provider = None
    if settings.has_perplexity:
        ai_provider = "perplexity"
    elif settings.has_openai:
        ai_provider = "openai"
    elif settings.has_anthropic:
        ai_provider = "anthropic"
    
    if not ai_provider:
        logger.warning("No AI provider configured")
    
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now(),
        version="0.1.0",
        ai_provider=ai_provider
    )

# Analyze business endpoint
@app.post("/api/analyze-business")
async def analyze_business(request: BusinessInput):
    """Analyze business from text description or URL."""
    if not settings.has_ai_provider:
        raise HTTPException(
            status_code=503,
            detail="No AI provider configured. Please set PERPLEXITY_API_KEY, OPENAI_API_KEY, or ANTHROPIC_API_KEY in .env"
        )
    
    try:
        if request.input_type == "text":
            # Use text analyzer
            from backend.scanners.text_analyzer import TextBusinessAnalyzer
            analyzer = TextBusinessAnalyzer()
            business_info = await analyzer.analyze(request.content)
            opportunities = await analyzer.identify_opportunities(business_info)
        elif request.input_type == "url":
            # Use URL scanner
            from backend.scanners.url_scanner import URLBusinessScanner
            async with URLBusinessScanner() as scanner:
                business_info = await scanner.analyze(request.content)
                opportunities = await scanner.identify_opportunities(business_info)
        else:
            raise HTTPException(status_code=400, detail="Invalid input_type. Use 'text' or 'url'")
        
        return {
            "business_info": business_info.dict(),
            "opportunities": [opp.dict() for opp in opportunities[:20]],  # Return top 20
            "total_opportunities": len(opportunities)
        }
        
    except Exception as e:
        logger.error(f"Error in business analysis: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Generate programmatic SEO templates endpoint
@app.post("/api/generate-templates")
async def generate_templates(request: TemplateGenerationRequest):
    """Generate programmatic SEO template opportunities for a business."""
    if not settings.has_ai_provider:
        raise HTTPException(
            status_code=503,
            detail="No AI provider configured. Please set PERPLEXITY_API_KEY, OPENAI_API_KEY, or ANTHROPIC_API_KEY in .env"
        )
    
    try:
        # Import AI handler with proper path
        import sys
        import os
        sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
        from api.ai_handler import AIHandler
        from backend.agents.business_analyzer import BusinessAnalyzerAgent
        
        # Initialize agents
        ai_handler = AIHandler()
        analyzer = BusinessAnalyzerAgent(ai_handler)
        
        # Analyze business
        business_analysis = analyzer.analyze_business(request.business_url_or_description)
        
        # Generate template suggestions
        templates = analyzer.suggest_templates(business_analysis)
        
        # Get data requirements for each template
        template_data = []
        for template in templates:
            data_reqs = analyzer.identify_data_requirements(template)
            
            template_data.append({
                "name": template.name,
                "pattern": template.pattern,
                "description": template.description,
                "estimated_pages": template.estimated_pages,
                "priority": template.priority,
                "search_intent": template.search_intent,
                "examples": template.examples,
                "data_requirements": [
                    {
                        "type": req.data_type,
                        "description": req.description,
                        "suggested_count": req.suggested_count,
                        "source": req.data_source,
                        "examples": req.examples
                    }
                    for req in data_reqs
                ]
            })
        
        return {
            "business_analysis": {
                "name": business_analysis.business_name,
                "industry": business_analysis.industry,
                "services": business_analysis.services,
                "products": business_analysis.products,
                "target_audience": business_analysis.target_audience,
                "business_model": business_analysis.business_model,
                "value_proposition": business_analysis.value_proposition
            },
            "templates": template_data,
            "total_templates": len(template_data)
        }
        
    except Exception as e:
        logger.error(f"Error generating templates: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Generate keyword strategies endpoint
@app.post("/api/generate-strategies")
async def generate_strategies(business_info: dict):
    """Generate keyword strategies based on business analysis."""
    if not settings.has_ai_provider:
        raise HTTPException(
            status_code=503,
            detail="No AI provider configured. Please set PERPLEXITY_API_KEY, OPENAI_API_KEY, or ANTHROPIC_API_KEY in .env"
        )
    
    try:
        from backend.researchers.strategy_generator import StrategyGenerator
        from backend.scanners.base import BusinessInfo
        
        # Convert dict to BusinessInfo object
        info = BusinessInfo(**business_info)
        
        generator = StrategyGenerator()
        strategies = await generator.generate_strategies(info)
        
        return {
            "strategies": [s.to_dict() for s in strategies],
            "total": len(strategies)
        }
        
    except Exception as e:
        logger.error(f"Error generating strategies: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Generate keywords for strategy endpoint
@app.post("/api/generate-keywords-for-strategy")
async def generate_keywords_for_strategy(strategy: dict, business_info: dict, limit: int = 50):
    """Generate keywords for a specific strategy."""
    if not settings.has_ai_provider:
        raise HTTPException(
            status_code=503,
            detail="No AI provider configured. Please set PERPLEXITY_API_KEY, OPENAI_API_KEY, or ANTHROPIC_API_KEY in .env"
        )
    
    try:
        from backend.researchers.strategy_generator import StrategyGenerator, KeywordStrategy
        from backend.scanners.base import BusinessInfo
        
        # Convert dicts to objects
        info = BusinessInfo(**business_info)
        strat = KeywordStrategy(**strategy)
        
        generator = StrategyGenerator()
        keywords = await generator.generate_keywords_for_strategy(strat, info, limit)
        
        return {
            "keywords": keywords,
            "total": len(keywords),
            "strategy": strategy["name"]
        }
        
    except Exception as e:
        logger.error(f"Error generating keywords for strategy: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Generate keywords endpoint (legacy - kept for compatibility)
@app.post("/api/generate-keywords")
async def generate_keywords(request: KeywordGenerationRequest):
    """Generate keyword opportunities from business analysis."""
    if not settings.has_ai_provider:
        raise HTTPException(
            status_code=503,
            detail="No AI provider configured. Please set PERPLEXITY_API_KEY, OPENAI_API_KEY, or ANTHROPIC_API_KEY in .env"
        )
    
    try:
        # First analyze the business
        if request.business_input.input_type == "text":
            from backend.scanners.text_analyzer import TextBusinessAnalyzer
            analyzer = TextBusinessAnalyzer()
            business_info = await analyzer.analyze(request.business_input.content)
            opportunities = await analyzer.identify_opportunities(business_info)
        else:
            from backend.scanners.url_scanner import URLBusinessScanner
            async with URLBusinessScanner() as scanner:
                business_info = await scanner.analyze(request.business_input.content)
                opportunities = await scanner.identify_opportunities(business_info)
        
        # Expand keywords
        from backend.researchers.keyword_researcher import KeywordResearcher
        researcher = KeywordResearcher()
        expanded_keywords = await researcher.expand_keywords(opportunities, business_info)
        
        # Cluster keywords
        clusters = await researcher.cluster_keywords(expanded_keywords)
        
        return {
            "business_info": business_info.dict(),
            "keywords": expanded_keywords[:request.max_keywords],
            "total_keywords": len(expanded_keywords),
            "clusters": {k: len(v) for k, v in clusters.items()}
        }
        
    except Exception as e:
        logger.error(f"Error generating keywords: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Generate content endpoint
@app.post("/api/generate-content")
async def generate_content(request: ContentGenerationRequest):
    """Generate content for selected keywords."""
    if not settings.has_ai_provider:
        raise HTTPException(
            status_code=503,
            detail="No AI provider configured. Please set PERPLEXITY_API_KEY, OPENAI_API_KEY, or ANTHROPIC_API_KEY in .env"
        )
    
    try:
        from backend.generators.content_generator import ContentGenerator
        generator = ContentGenerator()
        
        generated_content = []
        
        # Generate content for each keyword
        for keyword in request.keywords[:10]:  # Limit to 10 for API response time
            for variation in range(1, min(request.variations_per_keyword + 1, 4)):  # Max 3 variations
                content = await generator.generate_content(
                    keyword=keyword,
                    template_type=request.template,
                    business_info={},  # Would come from session/database in production
                    variation=variation
                )
                content["keyword"] = keyword
                generated_content.append(content)
        
        return {
            "content": generated_content,
            "total_pieces": len(generated_content),
            "template_used": request.template
        }
        
    except Exception as e:
        logger.error(f"Error generating content: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Export endpoint
@app.post("/api/export")
async def export_content(format: str = "csv", content: List[Dict] = None):
    """Export generated content."""
    if format not in ["csv", "json", "wordpress"]:
        raise HTTPException(
            status_code=400,
            detail="Invalid format. Choose from: csv, json, wordpress"
        )
    
    try:
        if format == "csv":
            from backend.exporters.csv_exporter import CSVExporter
            exporter = CSVExporter()
            filepath = exporter.export_content(content or [], "seo_content")
        elif format == "wordpress":
            from backend.exporters.wordpress_exporter import WordPressExporter
            exporter = WordPressExporter()
            filepath = exporter.export_content(content or [], "seo_content")
        else:  # json
            import json
            filepath = os.path.join(settings.exports_dir, f"seo_content_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
            with open(filepath, 'w') as f:
                json.dump(content or [], f, indent=2)
        
        # Return file for download
        from fastapi.responses import FileResponse
        return FileResponse(filepath, filename=os.path.basename(filepath))
        
    except Exception as e:
        logger.error(f"Error exporting content: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Project Management Endpoints
@app.post("/api/projects")
async def create_project(request: ProjectCreateRequest, db: Session = Depends(get_db)):
    """Create a new SEO project."""
    try:
        db_agent = DatabaseAgent(db)
        project = db_agent.create_project(
            name=request.name,
            business_description=request.business_description,
            business_url=request.business_url,
            industry=request.industry,
            location=request.location
        )
        return {
            "project_id": project.id,
            "name": project.name,
            "created_at": project.created_at
        }
    except Exception as e:
        logger.error(f"Error creating project: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/projects")
async def list_projects(limit: int = 100, db: Session = Depends(get_db)):
    """List all projects."""
    try:
        db_agent = DatabaseAgent(db)
        projects = db_agent.list_projects(limit=limit)
        return {
            "projects": [
                {
                    "id": p.id,
                    "name": p.name,
                    "industry": p.industry,
                    "created_at": p.created_at,
                    "updated_at": p.updated_at
                }
                for p in projects
            ],
            "total": len(projects)
        }
    except Exception as e:
        logger.error(f"Error listing projects: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/projects/{project_id}")
async def get_project(project_id: int, db: Session = Depends(get_db)):
    """Get project details and statistics."""
    try:
        db_agent = DatabaseAgent(db)
        stats = db_agent.get_project_stats(project_id)
        if not stats:
            raise HTTPException(status_code=404, detail="Project not found")
        
        return {
            "project": {
                "id": stats["project"].id,
                "name": stats["project"].name,
                "business_description": stats["project"].business_description,
                "business_url": stats["project"].business_url,
                "industry": stats["project"].industry,
                "location": stats["project"].location,
                "created_at": stats["project"].created_at,
                "updated_at": stats["project"].updated_at
            },
            "statistics": {
                "total_keywords": stats["total_keywords"],
                "keywords_by_status": stats["keywords_by_status"],
                "total_content": stats["total_content"],
                "content_by_status": stats["content_by_status"]
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting project: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/projects/{project_id}/keywords")
async def add_keywords(project_id: int, request: KeywordAddRequest, db: Session = Depends(get_db)):
    """Add keywords to a project."""
    try:
        db_agent = DatabaseAgent(db)
        keywords = db_agent.add_keywords(project_id, request.keywords)
        return {
            "added": len(keywords),
            "keywords": [
                {
                    "id": k.id,
                    "keyword": k.keyword,
                    "search_volume": k.search_volume,
                    "difficulty": k.difficulty,
                    "content_type": k.content_type,
                    "status": k.status
                }
                for k in keywords
            ]
        }
    except Exception as e:
        logger.error(f"Error adding keywords: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/projects/{project_id}/generate-content")
async def generate_project_content(
    project_id: int, 
    keyword_ids: List[int],
    template: str = "comparison",
    db: Session = Depends(get_db)
):
    """Generate content for project keywords and save to database."""
    if not settings.has_ai_provider:
        raise HTTPException(
            status_code=503,
            detail="No AI provider configured. Please set PERPLEXITY_API_KEY, OPENAI_API_KEY, or ANTHROPIC_API_KEY in .env"
        )
    
    try:
        db_agent = DatabaseAgent(db)
        project = db_agent.get_project(project_id)
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        
        from backend.generators.content_generator import ContentGenerator
        generator = ContentGenerator()
        
        generated = []
        
        # Get keywords by IDs
        keywords = db_agent.get_project_keywords(project_id)
        keywords_to_generate = [k for k in keywords if k.id in keyword_ids]
        
        for keyword in keywords_to_generate:
            # Generate content
            content = await generator.generate_content(
                keyword=keyword.keyword,
                template_type=template,
                business_info={
                    "name": project.name,
                    "description": project.business_description,
                    "industry": project.industry,
                    "location": project.location
                },
                variation=1
            )
            
            # Save to database
            saved_content = db_agent.save_content(
                project_id=project_id,
                keyword_id=keyword.id,
                title=content["title"],
                content_html=content["content_html"],
                content_markdown=content["content_markdown"],
                meta_description=content["meta_description"],
                slug=content["slug"],
                template_used=template,
                word_count=content["word_count"]
            )
            
            generated.append({
                "content_id": saved_content.id,
                "keyword": keyword.keyword,
                "title": saved_content.title,
                "status": saved_content.status
            })
        
        return {
            "project_id": project_id,
            "generated": len(generated),
            "content": generated
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating project content: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/discover-keywords")
async def discover_keywords(request: KeywordDiscoveryRequest):
    """Discover new keyword opportunities using real SEO data."""
    try:
        from backend.researchers.keyword_researcher import KeywordResearcher
        researcher = KeywordResearcher()
        
        # Discover keywords using SEO data
        discovered = await researcher.discover_new_keywords(
            seed_keywords=request.seed_keywords,
            limit=request.limit
        )
        
        return {
            "keywords": discovered,
            "total": len(discovered),
            "seed_keywords": request.seed_keywords
        }
        
    except Exception as e:
        logger.error(f"Error discovering keywords: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Include the new API integration routes
try:
    from backend.api_integration import router as integration_router
    app.include_router(integration_router)
    logger.info("API integration routes loaded successfully")
except ImportError as e:
    logger.warning(f"Could not load API integration routes: {e}")
except Exception as e:
    logger.error(f"Error loading API integration routes: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug
    )