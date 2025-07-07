#!/bin/bash

# API Testing Script for Programmatic SEO Tool
# This script provides curl commands to test all API endpoints

# Configuration
BASE_URL="${BASE_URL:-https://programmaticseotool-production.up.railway.app}"
PROJECT_ID=""
TEMPLATE_ID=""
DATASET_ID=""
EXPORT_ID=""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "========================================="
echo "Programmatic SEO Tool - API Testing"
echo "Base URL: $BASE_URL"
echo "========================================="

# Function to print test header
print_test() {
    echo -e "\n${YELLOW}TEST: $1${NC}"
    echo "----------------------------------------"
}

# Function to check response
check_response() {
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}✓ Success${NC}"
    else
        echo -e "${RED}✗ Failed with code: $1${NC}"
    fi
}

# Test 1: Health Check
print_test "Health Check"
echo "curl -X GET $BASE_URL/health"
response=$(curl -s -w "\n%{http_code}" -X GET "$BASE_URL/health")
http_code=$(echo "$response" | tail -n 1)
body=$(echo "$response" | sed '$d')
echo "Response: $body"
check_response $((200 - http_code))

# Test 2: API Test Endpoint
print_test "API Test Endpoint"
echo "curl -X GET $BASE_URL/api/test"
response=$(curl -s -w "\n%{http_code}" -X GET "$BASE_URL/api/test")
http_code=$(echo "$response" | tail -n 1)
body=$(echo "$response" | sed '$d')
echo "Response: $body"
check_response $((200 - http_code))

# Test 3: Analyze Business
print_test "Analyze Business"
echo "curl -X POST $BASE_URL/api/analyze-business"
response=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/api/analyze-business" \
  -H "Content-Type: application/json" \
  -d '{
    "business_input": "EcoTech Solutions - Sustainable energy management software for commercial buildings. We help reduce energy costs by 30% through AI-powered optimization.",
    "input_type": "text"
  }')
http_code=$(echo "$response" | tail -n 1)
body=$(echo "$response" | sed '$d')
echo "Response: $body"
check_response $((200 - http_code))

# Extract project_id if successful
if [ "$http_code" -eq "200" ]; then
    PROJECT_ID=$(echo "$body" | grep -o '"project_id":"[^"]*' | cut -d'"' -f4)
    echo -e "${GREEN}Project ID: $PROJECT_ID${NC}"
fi

# Test 4: List Projects
print_test "List Projects"
echo "curl -X GET $BASE_URL/api/projects"
response=$(curl -s -w "\n%{http_code}" -X GET "$BASE_URL/api/projects")
http_code=$(echo "$response" | tail -n 1)
body=$(echo "$response" | sed '$d')
echo "Response (truncated): ${body:0:200}..."
check_response $((200 - http_code))

# Test 5: Get Project Details
if [ ! -z "$PROJECT_ID" ]; then
    print_test "Get Project Details"
    echo "curl -X GET $BASE_URL/api/projects/$PROJECT_ID"
    response=$(curl -s -w "\n%{http_code}" -X GET "$BASE_URL/api/projects/$PROJECT_ID")
    http_code=$(echo "$response" | tail -n 1)
    body=$(echo "$response" | sed '$d')
    echo "Response (truncated): ${body:0:200}..."
    check_response $((200 - http_code))
fi

# Test 6: Create Template
if [ ! -z "$PROJECT_ID" ]; then
    print_test "Create Template"
    echo "curl -X POST $BASE_URL/api/projects/$PROJECT_ID/templates"
    response=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/api/projects/$PROJECT_ID/templates" \
      -H "Content-Type: application/json" \
      -d '{
        "name": "Energy Solutions by Building Type",
        "pattern": "[Solution Type] for [Building Type]",
        "title_template": "{Solution Type} for {Building Type} - Save 30% on Energy Costs",
        "meta_description_template": "Discover how {Solution Type} can help {Building Type} reduce energy consumption and costs by up to 30%.",
        "h1_template": "Energy-Saving {Solution Type} for {Building Type}",
        "content_sections": [
          {
            "heading": "Why {Building Type} Need {Solution Type}",
            "content": "Learn about the unique energy challenges faced by {Building Type} and how our solutions address them."
          },
          {
            "heading": "Benefits of {Solution Type}",
            "content": "Explore the key benefits and ROI of implementing {Solution Type} in your {Building Type}."
          }
        ],
        "template_type": "solution"
      }')
    http_code=$(echo "$response" | tail -n 1)
    body=$(echo "$response" | sed '$d')
    echo "Response: $body"
    check_response $((200 - http_code))
    
    # Extract template_id if successful
    if [ "$http_code" -eq "200" ]; then
        TEMPLATE_ID=$(echo "$body" | grep -o '"id":"[^"]*' | cut -d'"' -f4)
        echo -e "${GREEN}Template ID: $TEMPLATE_ID${NC}"
    fi
fi

# Test 7: List Templates
if [ ! -z "$PROJECT_ID" ]; then
    print_test "List Templates"
    echo "curl -X GET $BASE_URL/api/projects/$PROJECT_ID/templates"
    response=$(curl -s -w "\n%{http_code}" -X GET "$BASE_URL/api/projects/$PROJECT_ID/templates")
    http_code=$(echo "$response" | tail -n 1)
    body=$(echo "$response" | sed '$d')
    echo "Response: $body"
    check_response $((200 - http_code))
fi

# Test 8: Create Dataset
if [ ! -z "$PROJECT_ID" ]; then
    print_test "Create Dataset"
    echo "curl -X POST $BASE_URL/api/projects/$PROJECT_ID/data"
    response=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/api/projects/$PROJECT_ID/data" \
      -H "Content-Type: application/json" \
      -d '{
        "name": "Building Types and Solutions",
        "data": [
          {"Solution Type": "Smart HVAC Systems", "Building Type": "Office Buildings"},
          {"Solution Type": "Smart HVAC Systems", "Building Type": "Retail Stores"},
          {"Solution Type": "LED Lighting Automation", "Building Type": "Office Buildings"},
          {"Solution Type": "LED Lighting Automation", "Building Type": "Warehouses"},
          {"Solution Type": "Solar Panel Integration", "Building Type": "Manufacturing Plants"},
          {"Solution Type": "Energy Monitoring Dashboard", "Building Type": "Hotels"}
        ]
      }')
    http_code=$(echo "$response" | tail -n 1)
    body=$(echo "$response" | sed '$d')
    echo "Response: $body"
    check_response $((200 - http_code))
    
    # Extract dataset_id if successful
    if [ "$http_code" -eq "200" ]; then
        DATASET_ID=$(echo "$body" | grep -o '"id":"[^"]*' | cut -d'"' -f4)
        echo -e "${GREEN}Dataset ID: $DATASET_ID${NC}"
    fi
fi

# Test 9: Validate Dataset
if [ ! -z "$PROJECT_ID" ] && [ ! -z "$DATASET_ID" ] && [ ! -z "$TEMPLATE_ID" ]; then
    print_test "Validate Dataset for Template"
    echo "curl -X POST $BASE_URL/api/projects/$PROJECT_ID/data/$DATASET_ID/validate"
    response=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/api/projects/$PROJECT_ID/data/$DATASET_ID/validate" \
      -H "Content-Type: application/json" \
      -d "{\"template_id\": \"$TEMPLATE_ID\"}")
    http_code=$(echo "$response" | tail -n 1)
    body=$(echo "$response" | sed '$d')
    echo "Response: $body"
    check_response $((200 - http_code))
fi

# Test 10: Generate Preview
if [ ! -z "$PROJECT_ID" ] && [ ! -z "$TEMPLATE_ID" ]; then
    print_test "Generate Preview Pages"
    echo "curl -X POST $BASE_URL/api/projects/$PROJECT_ID/templates/$TEMPLATE_ID/generate-preview"
    response=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/api/projects/$PROJECT_ID/templates/$TEMPLATE_ID/generate-preview" \
      -H "Content-Type: application/json" \
      -d '{"limit": 2}')
    http_code=$(echo "$response" | tail -n 1)
    body=$(echo "$response" | sed '$d')
    echo "Response (truncated): ${body:0:500}..."
    check_response $((200 - http_code))
fi

# Test 11: Generate All Pages
if [ ! -z "$PROJECT_ID" ] && [ ! -z "$TEMPLATE_ID" ]; then
    print_test "Generate All Pages"
    echo "curl -X POST $BASE_URL/api/projects/$PROJECT_ID/templates/$TEMPLATE_ID/generate"
    response=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/api/projects/$PROJECT_ID/templates/$TEMPLATE_ID/generate" \
      -H "Content-Type: application/json" \
      -d '{"batch_size": 50}')
    http_code=$(echo "$response" | tail -n 1)
    body=$(echo "$response" | sed '$d')
    echo "Response: $body"
    check_response $((200 - http_code))
fi

# Test 12: List Generated Pages
if [ ! -z "$PROJECT_ID" ]; then
    print_test "List Generated Pages"
    echo "curl -X GET $BASE_URL/api/projects/$PROJECT_ID/pages?limit=5"
    response=$(curl -s -w "\n%{http_code}" -X GET "$BASE_URL/api/projects/$PROJECT_ID/pages?limit=5")
    http_code=$(echo "$response" | tail -n 1)
    body=$(echo "$response" | sed '$d')
    echo "Response (truncated): ${body:0:500}..."
    check_response $((200 - http_code))
fi

# Test 13: Export to CSV
if [ ! -z "$PROJECT_ID" ]; then
    print_test "Export to CSV"
    echo "curl -X POST $BASE_URL/api/projects/$PROJECT_ID/export"
    response=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/api/projects/$PROJECT_ID/export" \
      -H "Content-Type: application/json" \
      -d '{
        "format": "csv",
        "options": {
          "include_content": true,
          "include_seo": true
        }
      }')
    http_code=$(echo "$response" | tail -n 1)
    body=$(echo "$response" | sed '$d')
    echo "Response: $body"
    check_response $((200 - http_code))
    
    # Extract export_id if successful
    if [ "$http_code" -eq "200" ]; then
        EXPORT_ID=$(echo "$body" | grep -o '"export_id":"[^"]*' | cut -d'"' -f4)
        echo -e "${GREEN}Export ID: $EXPORT_ID${NC}"
    fi
fi

# Test 14: Check Export Status
if [ ! -z "$EXPORT_ID" ]; then
    print_test "Check Export Status"
    echo "curl -X GET $BASE_URL/api/exports/$EXPORT_ID/status"
    
    # Poll for completion
    for i in {1..5}; do
        response=$(curl -s -w "\n%{http_code}" -X GET "$BASE_URL/api/exports/$EXPORT_ID/status")
        http_code=$(echo "$response" | tail -n 1)
        body=$(echo "$response" | sed '$d')
        
        status=$(echo "$body" | grep -o '"status":"[^"]*' | cut -d'"' -f4)
        echo "Attempt $i - Status: $status"
        
        if [ "$status" = "completed" ] || [ "$status" = "failed" ]; then
            echo "Final Response: $body"
            break
        fi
        
        sleep 2
    done
    check_response $((200 - http_code))
fi

# Test 15: Error Handling - Invalid Project ID
print_test "Error Handling - Invalid Project ID"
echo "curl -X GET $BASE_URL/api/projects/invalid-uuid-123"
response=$(curl -s -w "\n%{http_code}" -X GET "$BASE_URL/api/projects/invalid-uuid-123")
http_code=$(echo "$response" | tail -n 1)
body=$(echo "$response" | sed '$d')
echo "Response: $body"
echo -e "Expected: 404, Got: $http_code"
if [ "$http_code" -eq "404" ]; then
    echo -e "${GREEN}✓ Error handling works correctly${NC}"
else
    echo -e "${RED}✗ Unexpected response code${NC}"
fi

# Test 16: Cleanup - Delete Test Project
if [ ! -z "$PROJECT_ID" ]; then
    print_test "Cleanup - Delete Test Project"
    echo "curl -X DELETE $BASE_URL/api/projects/$PROJECT_ID"
    response=$(curl -s -w "\n%{http_code}" -X DELETE "$BASE_URL/api/projects/$PROJECT_ID")
    http_code=$(echo "$response" | tail -n 1)
    body=$(echo "$response" | sed '$d')
    echo "Response: $body"
    check_response $((200 - http_code))
fi

echo -e "\n========================================="
echo "Testing Complete!"
echo "========================================="

# Save test results
echo -e "\nTo save these results:"
echo "export PROJECT_ID=$PROJECT_ID"
echo "export TEMPLATE_ID=$TEMPLATE_ID"
echo "export DATASET_ID=$DATASET_ID"
echo "export EXPORT_ID=$EXPORT_ID"