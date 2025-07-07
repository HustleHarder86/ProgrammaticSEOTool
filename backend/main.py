"""Minimal FastAPI backend to test Railway deployment"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
from ai_client import AIClient

app = FastAPI(title="Programmatic SEO Tool API")
ai_client = AIClient()

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
    business_name: str
    business_description: str
    target_audience: str
    core_offerings: List[str]
    template_opportunities: List[TemplateOpportunity]

@app.post("/api/analyze-business", response_model=BusinessAnalysisResponse)
async def analyze_business(request: BusinessAnalysisRequest):
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
        
        response = BusinessAnalysisResponse(
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