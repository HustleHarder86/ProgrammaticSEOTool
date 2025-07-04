#!/bin/bash

# Test script for Programmatic SEO Tool API
# This script tests keyword generation using the API endpoints

echo "🚀 Testing Programmatic SEO Tool - Keyword Generation"
echo "===================================================="

# Note: Make sure the API server is running:
# python3 -m uvicorn app.main:app --reload

API_URL="http://localhost:8000"

echo -e "\n1️⃣ Testing business analysis endpoint..."
echo "Analyzing a digital marketing agency..."

curl -X POST "$API_URL/api/analyze-business" \
  -H "Content-Type: application/json" \
  -d '{
    "input_type": "text",
    "content": "We are a digital marketing agency specializing in SEO and content marketing. We help small businesses improve their online visibility through strategic content creation, keyword optimization, and link building."
  }' | python3 -m json.tool

echo -e "\n\n2️⃣ Testing strategy generation..."
echo "Generating programmatic SEO strategies..."

# You would need to copy the business_info from the previous response
# For demo purposes, here's a simplified version:

curl -X POST "$API_URL/api/generate-strategies" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Digital Marketing Agency",
    "industry": "Digital Marketing",
    "services": ["SEO Services", "Content Marketing", "Link Building", "Technical SEO", "Local SEO"],
    "products": [],
    "target_audience": ["Small Businesses", "Local Businesses"],
    "value_propositions": ["Improve Online Visibility", "Strategic Content Creation"],
    "locations": []
  }' | python3 -m json.tool

echo -e "\n\n3️⃣ Testing keyword discovery..."
echo "Discovering keywords from seed keywords..."

curl -X POST "$API_URL/api/discover-keywords" \
  -H "Content-Type: application/json" \
  -d '{
    "seed_keywords": ["SEO audit", "content marketing strategy", "local SEO"],
    "limit": 20
  }' | python3 -m json.tool

echo -e "\n\n✅ Test completed!"
echo "Note: The tool works with just an AI API key (OpenAI/Anthropic)."
echo "SEO metrics shown are AI estimates when no SEO API keys are configured."