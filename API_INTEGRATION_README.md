# API Integration Module

This module provides a unified API that orchestrates all 5 agents for complete programmatic SEO workflows.

## Quick Start

1. **Start the API server:**
   ```bash
   python -m uvicorn app.main:app --reload
   ```

2. **Test the integration:**
   ```bash
   python test_api_integration.py
   ```

## Main Features

### 🔄 Complete Workflow Automation
- Business analysis → Template creation → Data import → Page generation → Export
- Asynchronous execution with progress tracking
- Error handling and recovery

### 🎯 Individual Agent Control
- Use each agent independently
- Custom configurations per step
- Validation and preview capabilities

### 📊 Bulk Operations
- Generate hundreds of pages at once
- Multiple export formats
- Compression and scheduling

### 🔌 Integration Points
- RESTful API endpoints
- Background task processing
- Real-time status updates

## Key Endpoints

1. **Analyze Business**: `/api/analyze-business-templates`
2. **Create Template**: `/api/create-template`
3. **Import Data**: `/api/import-data`
4. **Generate Pages**: `/api/generate-pages-bulk`
5. **Export Content**: `/api/export-content`
6. **Complete Workflow**: `/api/complete-workflow`

## Architecture

```
┌─────────────────┐
│ API Integration │
└────────┬────────┘
         │
    ┌────┴────┐
    │ Agents  │
    ├─────────┤
    │ • Business Analyzer
    │ • Template Builder
    │ • Data Manager
    │ • Page Generator
    │ • Export Manager
    └─────────┘
```

## Error Handling

- Comprehensive validation at each step
- Graceful failure recovery
- Detailed error messages
- Workflow state persistence

## Performance

- Async operations for better throughput
- Batch processing capabilities
- Progress tracking for long operations
- Resource-efficient execution

See `API_INTEGRATION_DOCS.md` for complete documentation.