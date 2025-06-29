# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

The Programmatic SEO Generator is a comprehensive automation tool that creates hundreds of SEO-optimized pages at scale. It analyzes businesses to identify content opportunities and generates unique, search-engine-friendly content automatically.

### Core Features

1. **Business Analysis & Content Discovery**
   - Analyzes business URL/description to understand niche
   - Identifies high-potential content types (comparisons, use-cases, integrations)
   - Discovers ranking opportunities based on search metrics

2. **Project Management System**
   - Tracks content pipeline and generation status
   - Manages multiple SEO projects simultaneously
   - Monitors content performance metrics

3. **Keyword Research Engine**
   - Continuously discovers new keyword opportunities
   - Analyzes search volume and keyword difficulty
   - Prioritizes keywords by ROI potential

4. **Intelligent Content Generation**
   - Creates unique variations to avoid duplicate content penalties
   - Generates multiple content types (guides, comparisons, tutorials)
   - Ensures SEO optimization (meta tags, structure, keywords)

5. **Publishing & Distribution**
   - Scheduled publishing at optimal times
   - CSV export functionality
   - Direct API integration with websites
   - Bulk content deployment capabilities

## Architecture Components (To Be Implemented)

### Backend Services
- **Business Analyzer**: Processes URLs/descriptions to understand business context
- **Keyword Research Service**: Interfaces with SEO APIs for keyword data
- **Content Generator**: AI-powered content creation with variation engine
- **Publishing Queue**: Manages scheduled posts and API integrations

### Data Storage
- **Project Database**: Stores project configurations and content pipelines
- **Content Repository**: Manages generated content and variations
- **Analytics Store**: Tracks performance metrics and keyword rankings

### Frontend/Interface
- **Project Dashboard**: Manages SEO projects and monitors progress
- **Content Editor**: Reviews and customizes generated content
- **Publishing Interface**: Configures deployment settings and schedules

## Development Guidelines

When implementing features:
1. Ensure all generated content passes uniqueness checks
2. Implement rate limiting for API calls to SEO data providers
3. Include content variation algorithms to prevent Google penalties
4. Build modular components for easy scaling
5. Add comprehensive logging for content generation pipeline

## Development Commands

### Run Locally
```bash
# Option 1: Run both servers with one command
python run_local.py

# Option 2: Run servers separately
# Terminal 1 - API
python -m uvicorn app.main:app --reload

# Terminal 2 - UI
streamlit run streamlit_app.py
```

### Initialize Database
```bash
python init_db.py
```

### Deploy to Vercel
```bash
vercel
```

## API Endpoints

- `GET /health` - Health check
- `POST /api/analyze-business` - Analyze business from text or URL
- `POST /api/generate-keywords` - Generate keyword opportunities
- `POST /api/generate-content` - Generate content for keywords
- `POST /api/export` - Export content (CSV, JSON, WordPress)

## Environment Variables Required

- `OPENAI_API_KEY` or `ANTHROPIC_API_KEY` - At least one AI provider
- Optional: `SERPAPI_KEY`, `UBERSUGGEST_API_KEY` for enhanced keyword research
- Optional: `WORDPRESS_URL`, `WORDPRESS_USERNAME`, `WORDPRESS_APP_PASSWORD` for direct publishing