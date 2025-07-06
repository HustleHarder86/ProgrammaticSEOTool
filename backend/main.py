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
        
        # Convert to response model
        template_opportunities = []
        for opp in analysis.get("template_opportunities", []):
            template_opportunities.append(TemplateOpportunity(
                template_name=opp["template_name"],
                template_pattern=opp["template_pattern"],
                example_pages=opp["example_pages"],
                estimated_pages=opp["estimated_pages"],
                difficulty=opp["difficulty"]
            ))
        
        response = BusinessAnalysisResponse(
            business_name=analysis["business_name"],
            business_description=analysis["business_description"],
            target_audience=analysis["target_audience"],
            core_offerings=analysis["core_offerings"],
            template_opportunities=template_opportunities
        )
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")