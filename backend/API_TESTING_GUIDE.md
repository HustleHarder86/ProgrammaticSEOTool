# API Testing Guide for Railway Backend

## Base URL
Replace `YOUR_RAILWAY_URL` with your actual Railway deployment URL:
```
https://programmaticseotool-production.up.railway.app
```

## 1. Health Check Endpoint

### Test Command:
```bash
curl https://YOUR_RAILWAY_URL/health
```

### Expected Response:
```json
{
  "status": "healthy",
  "service": "programmatic-seo-backend",
  "database": "connected",
  "timestamp": "2025-01-07T12:00:00.000000"
}
```

## 2. Test API Endpoint

### Test Command:
```bash
curl https://YOUR_RAILWAY_URL/api/test
```

### Expected Response:
```json
{
  "message": "API is working!",
  "timestamp": "2025-01-06"
}
```

## 3. Business Analysis Endpoint

### Test Command:
```bash
curl -X POST https://YOUR_RAILWAY_URL/api/analyze-business \
  -H "Content-Type: application/json" \
  -d '{
    "business_input": "Digital marketing agency specializing in SEO and PPC",
    "input_type": "text"
  }'
```

### Expected Response:
```json
{
  "project_id": "uuid-string",
  "business_name": "Digital Marketing Agency",
  "business_description": "...",
  "target_audience": "...",
  "core_offerings": ["SEO", "PPC", "..."],
  "template_opportunities": [
    {
      "template_name": "Location-based Services",
      "template_pattern": "[Service] in [City]",
      "example_pages": ["SEO in New York", "..."],
      "estimated_pages": 500,
      "difficulty": "Low"
    }
  ]
}
```

## 4. List Projects

### Test Command:
```bash
curl https://YOUR_RAILWAY_URL/api/projects
```

### Expected Response:
```json
[
  {
    "id": "uuid-string",
    "name": "Project Name",
    "business_input": "...",
    "created_at": "2025-01-07T..."
  }
]
```

## 5. Get Project Details

### Test Command:
```bash
curl https://YOUR_RAILWAY_URL/api/projects/PROJECT_ID
```

## 6. Create Template

### Test Command:
```bash
curl -X POST https://YOUR_RAILWAY_URL/api/projects/PROJECT_ID/templates \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Location Pages",
    "template_type": "location",
    "template_html": "<h1>{{service}} in {{city}}</h1>",
    "variables": ["service", "city"],
    "seo_settings": {
      "meta_title": "{{service}} in {{city}} | Company",
      "meta_description": "Best {{service}} services in {{city}}"
    }
  }'
```

## 7. Upload Data (CSV)

### Test Command:
```bash
curl -X POST https://YOUR_RAILWAY_URL/api/projects/PROJECT_ID/data/upload \
  -F "file=@test_data.csv"
```

## 8. Generate Pages

### Test Command:
```bash
curl -X POST https://YOUR_RAILWAY_URL/api/projects/PROJECT_ID/templates/TEMPLATE_ID/generate \
  -H "Content-Type: application/json" \
  -d '{
    "batch_size": 10
  }'
```

## 9. Export Pages

### Test Command:
```bash
curl -X POST https://YOUR_RAILWAY_URL/api/projects/PROJECT_ID/export \
  -H "Content-Type: application/json" \
  -d '{
    "format": "csv"
  }'
```

## Testing with HTTPie (Alternative)

If you prefer HTTPie:

```bash
# Health check
http GET YOUR_RAILWAY_URL/health

# Business analysis
http POST YOUR_RAILWAY_URL/api/analyze-business \
  business_input="Digital marketing agency" \
  input_type="text"

# List projects
http GET YOUR_RAILWAY_URL/api/projects
```

## Common Issues and Solutions

### CORS Errors
- Verify frontend URL is in the CORS origins list
- Check browser console for specific error

### 500 Internal Server Error
- Check Railway logs for stack trace
- Verify all environment variables are set
- Test database connection with /health

### 401 Unauthorized
- Ensure API keys are set in Railway environment
- Check if using correct API key format

### Connection Refused
- Verify Railway deployment is successful
- Check if using HTTPS (not HTTP)
- Confirm Railway URL is correct