"""Minimal FastAPI for Vercel deployment"""
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import json

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Programmatic SEO Tool API", "status": "healthy"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.post("/api/analyze-business")
async def analyze_business(data: dict):
    return {
        "business_info": {
            "name": "Your Business",
            "description": data.get("business_description", ""),
            "url": data.get("business_url", ""),
            "industry": "General",
            "target_audience": "General audience"
        }
    }

@app.post("/api/generate-keywords")
async def generate_keywords(data: dict):
    keywords = []
    for i in range(5):
        keywords.append({
            "keyword": f"keyword {i+1}",
            "search_volume": 1000,
            "difficulty": 50,
            "intent": "informational"
        })
    return {"keywords": keywords}

@app.post("/api/generate-content") 
async def generate_content(data: dict):
    return {
        "contents": [{
            "title": "Sample Content",
            "content": "This is sample content.",
            "meta_description": "Sample meta description"
        }]
    }

@app.post("/api/export")
async def export_content(data: dict = {}):
    format_type = data.get("format", "json")
    return {
        "format": format_type,
        "data": {"message": "Export functionality"}
    }

# Handler for Vercel
handler = app