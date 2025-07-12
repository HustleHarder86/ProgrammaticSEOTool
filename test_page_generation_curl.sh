#!/bin/bash
# Curl-based test script for page generation

API_URL="http://localhost:8000"
PROJECT_ID=""
TEMPLATE_ID=""

echo "========================================"
echo "Testing Page Generation with Curl"
echo "========================================"

# Step 1: Health Check
echo -e "\n1. Testing API Health..."
curl -s "${API_URL}/health" | jq '.'

# Step 2: Analyze Business
echo -e "\n2. Analyzing Business..."
BUSINESS_RESPONSE=$(curl -s -X POST "${API_URL}/api/analyze-business" \
  -H "Content-Type: application/json" \
  -d '{
    "business_input": "AI Writing Assistant for Content Creators - An AI-powered tool that helps bloggers, marketers, and writers create high-quality content faster. Features include blog post generation, email templates, social media captions, and SEO optimization."
  }')

echo "$BUSINESS_RESPONSE" | jq '.'
PROJECT_ID=$(echo "$BUSINESS_RESPONSE" | jq -r '.project_id')
echo "Project ID: $PROJECT_ID"

# Step 3: Create Template
echo -e "\n3. Creating Template..."
TEMPLATE_RESPONSE=$(curl -s -X POST "${API_URL}/api/create-template" \
  -H "Content-Type: application/json" \
  -d "{
    \"project_id\": \"$PROJECT_ID\",
    \"name\": \"AI Writing Tools Comparison\",
    \"template_type\": \"comparison\",
    \"title_template\": \"Best AI Writing Tools for {content_type} in {year}\",
    \"meta_description_template\": \"Compare top AI writing assistants for {content_type}. Find the perfect tool for your {content_type} needs in {year}.\",
    \"content_template\": \"<h1>Best AI Writing Tools for {content_type} in {year}</h1><p>Creating high-quality {content_type} has never been easier with AI writing assistants.</p>\",
    \"url_pattern\": \"/ai-writing-tools/{content_type}-{year}\"
  }")

echo "$TEMPLATE_RESPONSE" | jq '.'
TEMPLATE_ID=$(echo "$TEMPLATE_RESPONSE" | jq -r '.template.id')
echo "Template ID: $TEMPLATE_ID"

# Step 4: Generate Pages with Manual Variables
echo -e "\n4. Generating Pages..."
PAGES_RESPONSE=$(curl -s -X POST "${API_URL}/api/generate-pages" \
  -H "Content-Type: application/json" \
  -d "{
    \"project_id\": \"$PROJECT_ID\",
    \"template_id\": \"$TEMPLATE_ID\",
    \"variables\": {
      \"content_type\": [\"Blog Posts\", \"Email Campaigns\", \"Social Media Posts\"],
      \"year\": [\"2024\", \"2025\"]
    },
    \"limit\": 10
  }")

echo "$PAGES_RESPONSE" | jq '.'

# Step 5: Export as CSV
echo -e "\n5. Exporting Pages..."
EXPORT_RESPONSE=$(curl -s -X POST "${API_URL}/api/export" \
  -H "Content-Type: application/json" \
  -d "{
    \"project_id\": \"$PROJECT_ID\",
    \"format\": \"csv\"
  }")

# Save the CSV data
echo "$EXPORT_RESPONSE" | jq -r '.data' > "test_export_$(date +%Y%m%d_%H%M%S).csv"
echo "Export saved to: test_export_$(date +%Y%m%d_%H%M%S).csv"

echo -e "\n========================================"
echo "Test Completed!"
echo "========================================"