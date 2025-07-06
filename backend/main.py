"""Minimal FastAPI backend to test Railway deployment"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os

app = FastAPI(title="Programmatic SEO Tool API")

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
    
    # For now, return mock data to test the endpoint
    # We'll add real AI analysis later
    mock_response = BusinessAnalysisResponse(
        business_name="Example Business",
        business_description="A business focused on " + request.business_input[:50],
        target_audience="Small to medium businesses",
        core_offerings=[
            "Product/Service 1",
            "Product/Service 2",
            "Product/Service 3"
        ],
        template_opportunities=[
            TemplateOpportunity(
                template_name="Location-Based Pages",
                template_pattern="[Service] in [City]",
                example_pages=[
                    "Web Design in Toronto",
                    "Web Design in Vancouver",
                    "Web Design in Montreal"
                ],
                estimated_pages=100,
                difficulty="Easy"
            ),
            TemplateOpportunity(
                template_name="Comparison Pages",
                template_pattern="[Product A] vs [Product B]",
                example_pages=[
                    "WordPress vs Wix",
                    "Shopify vs WooCommerce",
                    "Squarespace vs WordPress"
                ],
                estimated_pages=50,
                difficulty="Medium"
            )
        ]
    )
    
    return mock_response