"""Minimal API for Vercel deployment"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import requests
from bs4 import BeautifulSoup
from typing import Optional, List, Dict, Any
import json

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class BusinessAnalysisRequest(BaseModel):
    business_description: Optional[str] = None
    business_url: Optional[str] = None

class KeywordGenerationRequest(BaseModel):
    business_info: Dict[str, Any]
    num_keywords: int = 10

class ContentGenerationRequest(BaseModel):
    keywords: List[str]
    business_info: Dict[str, Any]
    content_type: str = "blog_post"

@app.get("/")
async def root():
    return {"message": "Programmatic SEO Tool API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/api/analyze-business")
async def analyze_business(request: BusinessAnalysisRequest):
    """Analyze business from description or URL"""
    try:
        if request.business_url:
            # Simple URL scraping
            response = requests.get(request.business_url, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract basic info
            title = soup.find('title').text if soup.find('title') else ""
            description = ""
            meta_desc = soup.find('meta', attrs={'name': 'description'})
            if meta_desc:
                description = meta_desc.get('content', '')
            
            return {
                "business_info": {
                    "name": title,
                    "description": description or request.business_description or "",
                    "url": request.business_url,
                    "industry": "General",  # Simplified
                    "target_audience": "General audience"
                }
            }
        else:
            # Use description
            return {
                "business_info": {
                    "name": "Your Business",
                    "description": request.business_description or "",
                    "industry": "General",
                    "target_audience": "General audience"
                }
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/generate-keywords")
async def generate_keywords(request: KeywordGenerationRequest):
    """Generate keyword opportunities"""
    # Simplified keyword generation
    base_keywords = [
        "how to", "best", "guide", "tips", "tutorial",
        "vs", "comparison", "review", "alternative", "tool"
    ]
    
    business_name = request.business_info.get("name", "business")
    keywords = []
    
    for base in base_keywords[:request.num_keywords]:
        keywords.append({
            "keyword": f"{base} {business_name.lower()}",
            "search_volume": 1000,  # Mock data
            "difficulty": 50,
            "intent": "informational"
        })
    
    return {"keywords": keywords}

@app.post("/api/generate-content")
async def generate_content(request: ContentGenerationRequest):
    """Generate content for keywords"""
    # Simplified content generation
    contents = []
    
    for keyword in request.keywords[:5]:  # Limit to 5
        contents.append({
            "keyword": keyword,
            "title": f"{keyword.title()} - Complete Guide",
            "content": f"This is a placeholder for content about {keyword}.",
            "meta_description": f"Learn everything about {keyword} in this guide.",
            "status": "generated"
        })
    
    return {"contents": contents}

@app.post("/api/export")
async def export_content(format: str = "json"):
    """Export content in different formats"""
    # Simplified export
    sample_data = {
        "contents": [
            {
                "title": "Sample Content",
                "content": "This is sample content for export.",
                "meta_description": "Sample meta description"
            }
        ]
    }
    
    if format == "csv":
        return {
            "format": "csv",
            "data": "title,content,meta_description\nSample Content,This is sample content,Sample meta"
        }
    else:
        return {
            "format": "json",
            "data": sample_data
        }

# Handler for Vercel
handler = app