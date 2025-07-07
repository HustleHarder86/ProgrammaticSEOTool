# Template API Documentation

## Overview
The Template API provides endpoints for creating, managing, and previewing page templates in the Programmatic SEO Tool. Templates use `{variable}` syntax for placeholders that will be replaced with actual data during page generation.

## Endpoints

### 1. Create Template
**POST** `/api/projects/{project_id}/templates`

Creates a new template for a specific project.

#### Request Body
```json
{
  "name": "Location Service Template",
  "pattern": "{service} in {location}",
  "title_template": "{service} Services in {location} - Professional & Affordable",
  "meta_description_template": "Find the best {service} services in {location}. Compare prices, read reviews, and book online.",
  "h1_template": "Professional {service} Services in {location}",
  "content_sections": [
    {
      "heading": "About {service} in {location}",
      "content": "Overview of {service} services available in {location}."
    },
    {
      "heading": "Why Choose Our {service} Services",
      "content": "Benefits and advantages of choosing our {service} services."
    }
  ],
  "template_type": "location_service"
}
```

#### Response
```json
{
  "id": "uuid-here",
  "project_id": "project-uuid",
  "name": "Location Service Template",
  "pattern": "{service} in {location}",
  "variables": ["service", "location"],
  "created_at": "2025-01-07T12:00:00Z"
}
```

### 2. List Project Templates
**GET** `/api/projects/{project_id}/templates`

Lists all templates for a specific project.

#### Response
```json
[
  {
    "id": "uuid-here",
    "project_id": "project-uuid",
    "name": "Location Service Template",
    "pattern": "{service} in {location}",
    "variables": ["service", "location"],
    "created_at": "2025-01-07T12:00:00Z"
  }
]
```

### 3. Get Template Details
**GET** `/api/templates/{template_id}`

Retrieves detailed information about a specific template.

#### Response
```json
{
  "id": "uuid-here",
  "project_id": "project-uuid",
  "name": "Location Service Template",
  "pattern": "{service} in {location}",
  "variables": ["service", "location"],
  "template_sections": {
    "seo_structure": {
      "title_template": "{service} Services in {location} - Professional & Affordable",
      "meta_description_template": "Find the best {service} services in {location}.",
      "h1_template": "Professional {service} Services in {location}"
    },
    "content_sections": [
      {
        "heading": "About {service} in {location}",
        "content": "Overview of {service} services available in {location}."
      }
    ]
  },
  "example_pages": [],
  "created_at": "2025-01-07T12:00:00Z"
}
```

### 4. Update Template
**PUT** `/api/templates/{template_id}`

Updates an existing template. All fields are optional.

#### Request Body
```json
{
  "name": "Updated Template Name",
  "pattern": "{service} near {location}",
  "title_template": "Updated title template",
  "content_sections": [
    {
      "heading": "New Section",
      "content": "New content"
    }
  ]
}
```

### 5. Preview Template
**POST** `/api/templates/{template_id}/preview`

Generates a preview of how the template will look with sample data.

#### Request Body
```json
{
  "sample_data": {
    "service": "plumbing",
    "location": "Toronto"
  }
}
```

#### Response
```json
{
  "pattern": "{service} in {location}",
  "filled_pattern": "plumbing in Toronto",
  "seo": {
    "title": "plumbing Services in Toronto - Professional & Affordable",
    "meta_description": "Find the best plumbing services in Toronto. Compare prices, read reviews, and book online.",
    "h1": "Professional plumbing Services in Toronto",
    "url": "/plumbing-in-toronto"
  },
  "content_sections": [
    {
      "heading": "About plumbing in Toronto",
      "content": "Overview of plumbing services available in Toronto."
    }
  ],
  "sample_data": {
    "service": "plumbing",
    "location": "Toronto"
  }
}
```

### 6. Delete Template
**DELETE** `/api/templates/{template_id}`

Deletes a template from the system.

#### Response
```json
{
  "message": "Template deleted successfully"
}
```

## Variable Syntax

Templates use `{variable_name}` syntax for placeholders. Variables must:
- Start with a letter
- Contain only letters, numbers, and underscores
- Be unique within the template

## Validation Rules

1. **Template Name**: Required, must be provided
2. **Pattern**: Required, must contain at least one variable
3. **Variables**: Automatically extracted from pattern and all template fields
4. **SEO Guidelines**:
   - Title template: Recommended 50-60 characters
   - Meta description: Maximum 160 characters
   - URL pattern: Automatically generated from pattern, lowercase with hyphens

## Error Responses

### 400 Bad Request
```json
{
  "detail": {
    "errors": ["Template must contain at least one {variable} placeholder"],
    "warnings": ["Title might be too long. Recommended: 50-60 characters"]
  }
}
```

### 404 Not Found
```json
{
  "detail": "Template not found"
}
```

## Usage Example

1. Create a project first using `/api/analyze-business`
2. Create a template for the project using the project ID
3. Preview the template with sample data to see how it will look
4. Use the template ID when generating pages with actual data