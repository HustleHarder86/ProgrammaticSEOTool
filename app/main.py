"""Main FastAPI application."""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict
import logging
from datetime import datetime
import os

from config import settings
from app.models import init_db

# Initialize database on startup
init_db()

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level.upper()),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Programmatic SEO Tool",
    description="Generate thousands of SEO-optimized pages automatically",
    version="0.1.0",
    debug=settings.debug
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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
    
class KeywordGenerationRequest(BaseModel):
    business_input: BusinessInput
    max_keywords: int = 100
    include_variations: bool = True

class ContentGenerationRequest(BaseModel):
    keywords: List[str]
    template: str = "comparison"  # comparison, how-to, best-x-for-y, etc.
    variations_per_keyword: int = 1

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Programmatic SEO Tool API",
        "docs": "/docs",
        "health": "/health"
    }

# Health check endpoint
@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    # Check AI provider configuration
    ai_provider = None
    if settings.has_openai:
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
            detail="No AI provider configured. Please set OPENAI_API_KEY or ANTHROPIC_API_KEY in .env"
        )
    
    try:
        if request.input_type == "text":
            # Use text analyzer
            from app.scanners.text_analyzer import TextBusinessAnalyzer
            analyzer = TextBusinessAnalyzer()
            business_info = await analyzer.analyze(request.content)
            opportunities = await analyzer.identify_opportunities(business_info)
        elif request.input_type == "url":
            # Use URL scanner
            from app.scanners.url_scanner import URLBusinessScanner
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

# Generate keywords endpoint
@app.post("/api/generate-keywords")
async def generate_keywords(request: KeywordGenerationRequest):
    """Generate keyword opportunities from business analysis."""
    if not settings.has_ai_provider:
        raise HTTPException(
            status_code=503,
            detail="No AI provider configured. Please set OPENAI_API_KEY or ANTHROPIC_API_KEY in .env"
        )
    
    try:
        # First analyze the business
        if request.business_input.input_type == "text":
            from app.scanners.text_analyzer import TextBusinessAnalyzer
            analyzer = TextBusinessAnalyzer()
            business_info = await analyzer.analyze(request.business_input.content)
            opportunities = await analyzer.identify_opportunities(business_info)
        else:
            from app.scanners.url_scanner import URLBusinessScanner
            async with URLBusinessScanner() as scanner:
                business_info = await scanner.analyze(request.business_input.content)
                opportunities = await scanner.identify_opportunities(business_info)
        
        # Expand keywords
        from app.researchers.keyword_researcher import KeywordResearcher
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
            detail="No AI provider configured. Please set OPENAI_API_KEY or ANTHROPIC_API_KEY in .env"
        )
    
    try:
        from app.generators.content_generator import ContentGenerator
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
            from app.exporters.csv_exporter import CSVExporter
            exporter = CSVExporter()
            filepath = exporter.export_content(content or [], "seo_content")
        elif format == "wordpress":
            from app.exporters.wordpress_exporter import WordPressExporter
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug
    )