# Code Cleanup and Adaptation Plan

## Overview
Transform the existing keyword-focused SEO tool into a template-based programmatic SEO generator.

## Files to KEEP (with adaptations)

### API Folder
1. **ai_handler.py**
   - Keep: Perplexity integration, business analysis
   - Adapt: Focus on template discovery
   - Remove: Keyword/content generation methods

2. **content_variation.py**
   - Keep entirely for uniqueness algorithms

3. **main.py**
   - Keep: URL parsing, basic structure
   - Adapt: New endpoints for templates/data/bulk generation

4. **usage_tracker.py**
   - Keep as-is for API usage tracking

### App Folder
1. **app/templates/content_templates.py**
   - Perfect foundation for template system
   - Expand with more template types

2. **app/researchers/strategy_generator.py**
   - Excellent for bulk operations
   - Already uses template patterns

3. **app/exporters/**
   - Keep both CSV and WordPress exporters

4. **app/agents/content_variation_agent.py**
   - Essential for page uniqueness

5. **app/models.py**
   - Database schema supports bulk operations

## Files to DELETE

### API Folder
- **keyword_optimizer.py** - Keyword research focused
- **enhanced-interface.html** - Complex UI not needed
- **interface.html** - Old interface
- **firebase_config.py** - Not using Firebase
- **minimal.py**, **simple.py**, **test.py** - Test/unused files

### App Folder
- **app/agents/seo_data_agent.py** - Individual keyword research
- **app/researchers/keyword_researcher.py** - Not template-based
- **app/scanners/** - Individual analysis focused
- **app/generators/content_generator.py** - Rewrite for bulk

### Root Folder
- Multiple README files (keep only main README.md)
- Test files not being used
- Streamlit files if not using that UI

## Files to HEAVILY ADAPT

1. **seed_generator.py** → **template_generator.py**
   - Already has template/variable system
   - Transform from keywords to data patterns
   - Perfect foundation for our needs

## New Structure

```
ProgrammaticSEOTool/
├── CLAUDE.md
├── README.md
├── PROGRAMMATIC_SEO_MCP.md
├── api/
│   ├── ai_handler.py (adapted)
│   ├── content_variation.py
│   ├── template_generator.py (from seed_generator)
│   ├── main.py (new endpoints)
│   └── usage_tracker.py
├── app/
│   ├── agents/
│   │   ├── business_analyzer.py (new)
│   │   ├── template_builder.py (new)
│   │   ├── data_manager.py (new)
│   │   ├── page_generator.py (adapted from content_variation)
│   │   └── export_manager.py (from exporters)
│   ├── templates/
│   │   └── library/ (template collection)
│   ├── models.py
│   └── main.py
├── data/
│   ├── templates/
│   └── exports/
└── requirements.txt
```

## Implementation Order

1. **Phase 1**: Delete unnecessary files
2. **Phase 2**: Adapt core files (ai_handler, main.py)
3. **Phase 3**: Transform seed_generator → template_generator
4. **Phase 4**: Create new agents based on MCP
5. **Phase 5**: Test with real examples

## Key Transformations

1. **Endpoints**:
   - `/analyze-business` → Returns template suggestions
   - `/generate-keywords` → `/create-template`
   - `/generate-content` → `/generate-pages`
   - Add: `/import-data`, `/preview-pages`

2. **Business Analysis**:
   - Identify repeatable patterns
   - Suggest data categories
   - Recommend template formulas

3. **Template System**:
   - Variable extraction
   - Data validation
   - Bulk generation

## Success Criteria

- ✅ Can generate 500+ pages from one template
- ✅ Each page has unique elements
- ✅ Works for any business type
- ✅ Simple workflow: Template → Data → Pages
- ✅ Multiple export formats work