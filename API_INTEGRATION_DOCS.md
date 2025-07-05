# API Integration Documentation

## Overview

The API Integration module (`/app/api_integration.py`) orchestrates all 5 agents to provide a complete programmatic SEO workflow:

1. **Business Analyzer Agent** - Analyzes businesses and suggests templates
2. **Template Builder Agent** - Creates and validates page templates  
3. **Data Manager Agent** - Imports and manages data
4. **Page Generator Agent** - Generates SEO-optimized pages
5. **Export Manager Agent** - Exports content in multiple formats

## Core Endpoints

### 1. Business Analysis & Template Suggestions

**POST** `/api/analyze-business-templates`

Analyzes a business and suggests programmatic SEO template opportunities.

```json
{
  "input_type": "text|url",
  "content": "Business description or URL",
  "market_context": {
    "location": "United States",
    "industry": "Digital Marketing"
  }
}
```

**Response:**
```json
{
  "business_analysis": {
    "business_name": "...",
    "industry": "...",
    "services": [...],
    "target_audience": [...]
  },
  "suggested_templates": [
    {
      "template": {
        "name": "Location + Service",
        "pattern": "{city} {service} Provider",
        "estimated_pages": 1000,
        "priority": 9
      },
      "data_requirements": [
        {
          "type": "cities",
          "suggested_count": 50,
          "source": "csv"
        }
      ]
    }
  ]
}
```

### 2. Template Creation

**POST** `/api/create-template`

Creates a new page template with custom pattern.

```json
{
  "business_analysis": {...},
  "template_pattern": "{city} {service} Agency",
  "template_name": "City Service Template",
  "custom_variables": ["city", "service", "specialization"]
}
```

### 3. Template Validation

**POST** `/api/validate-template`

Validates template with sample data and provides preview.

```json
{
  "template_id": "template_123",
  "sample_data": {
    "city": "New York",
    "service": "SEO"
  }
}
```

### 4. Data Import

**POST** `/api/import-data`

Imports data from CSV/JSON for template population.

```json
{
  "file_path": "/path/to/data.csv",
  "data_json": [...],  // Alternative to file_path
  "data_type": "location_service",
  "validation_rules": {...}
}
```

### 5. Bulk Page Generation

**POST** `/api/generate-pages-bulk`

Generates pages using template and imported data.

```json
{
  "template_id": "template_123",
  "data_set_id": "data_456",
  "limit": 100,
  "enable_variations": true,
  "internal_linking": true,
  "ai_enhancement": true
}
```

### 6. Content Export

**POST** `/api/export-content`

Exports generated content in multiple formats.

```json
{
  "page_ids": ["page1", "page2"],
  "formats": ["csv", "json", "wordpress"],
  "compression": true,
  "wordpress_config": {
    "url": "https://site.com",
    "username": "admin",
    "password": "app_password"
  },
  "scheduling": {
    "start_date": "2024-01-01",
    "posts_per_day": 5
  }
}
```

### 7. Complete Workflow

**POST** `/api/complete-workflow`

Runs the entire workflow asynchronously from analysis to export.

```json
{
  "business_input": {
    "input_type": "text",
    "content": "Business description"
  },
  "template_selection": "{pattern}",  // Optional
  "data_source": {
    "data_json": [...]
  },
  "generation_config": {
    "limit": 50,
    "enable_variations": true
  },
  "export_config": {
    "formats": ["csv", "wordpress"],
    "compression": false
  }
}
```

### 8. Workflow Status

**GET** `/api/workflow-status/{workflow_id}`

Check status of async workflow operations.

**Response:**
```json
{
  "workflow_id": "uuid",
  "status": "generating_pages",
  "current_step": "Generating page 45 of 100",
  "progress": 0.45,
  "created_at": "2024-01-01T10:00:00",
  "result": {...}  // When completed
}
```

## Utility Endpoints

### Get Supported Formats
**GET** `/api/supported-formats`

Returns all supported export formats and presets.

### Get Template Library
**GET** `/api/template-library`

Returns available template patterns and configurations.

### Test AI Connection
**POST** `/api/test-ai-connection`

Tests connection to configured AI provider.

## Workflow States

- `pending` - Workflow initialized
- `analyzing` - Analyzing business
- `building_template` - Creating template
- `importing_data` - Importing data
- `generating_pages` - Generating pages
- `exporting` - Exporting content
- `completed` - Successfully completed
- `failed` - Failed with error

## Error Handling

All endpoints return standard HTTP status codes:
- `200` - Success
- `400` - Bad request (invalid input)
- `404` - Resource not found
- `500` - Server error
- `503` - Service unavailable (no AI provider)

Error responses include detail:
```json
{
  "detail": "Error message describing the issue"
}
```

## Usage Example

```python
import requests

# 1. Analyze business
response = requests.post(
    "http://localhost:8000/api/analyze-business-templates",
    json={
        "input_type": "text",
        "content": "Digital marketing agency"
    }
)
analysis = response.json()

# 2. Create template
template_response = requests.post(
    "http://localhost:8000/api/create-template",
    json={
        "business_analysis": analysis["business_analysis"],
        "template_pattern": "{city} {service}",
        "template_name": "Location Service"
    }
)
template = template_response.json()

# 3. Import data
data_response = requests.post(
    "http://localhost:8000/api/import-data",
    json={
        "data_json": [
            {"city": "New York", "service": "SEO"},
            {"city": "Los Angeles", "service": "PPC"}
        ],
        "data_type": "location_service"
    }
)
data = data_response.json()

# 4. Generate pages
pages_response = requests.post(
    "http://localhost:8000/api/generate-pages-bulk",
    json={
        "template_id": template["template_id"],
        "data_set_id": data["data_set_id"],
        "enable_variations": True
    }
)
pages = pages_response.json()

# 5. Export content
export_response = requests.post(
    "http://localhost:8000/api/export-content",
    json={
        "formats": ["csv", "json"],
        "compression": True
    }
)
export = export_response.json()
```

## Testing

Run the test suite:

```bash
python test_api_integration.py
```

This will test:
- Individual endpoint functionality
- Complete workflow execution
- Error handling
- Utility endpoints

## Configuration

Required environment variables:
- `OPENAI_API_KEY` or `ANTHROPIC_API_KEY` - For AI content generation
- `WORDPRESS_URL`, `WORDPRESS_USERNAME`, `WORDPRESS_APP_PASSWORD` - For WordPress export

## Performance Considerations

- Page generation is the most resource-intensive operation
- Use `limit` parameter to control batch sizes
- Enable compression for large exports
- Monitor workflow status for long-running operations
- Consider using background tasks for workflows > 100 pages