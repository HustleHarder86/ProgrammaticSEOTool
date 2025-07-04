# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What is Programmatic SEO?

Programmatic SEO is an SEO strategy that leverages **automation and templates to generate and optimize a large volume of web pages** by using data to populate templates, creating numerous pages efficiently. It focuses on targeting long-tail keywords with lower competition.

**Examples:**
- Tripadvisor: "Things to do in [City]" - thousands of city pages from one template
- Zillow: "[City] Real Estate" - location-based property pages
- Yelp: "Best [Business Type] in [City]" - local business directory pages

**Key Formula: Template + Data = Scale**

## Project Overview

The Programmatic SEO Tool is a versatile bulk page generator that works for ANY business type. It creates hundreds or thousands of SEO-optimized pages by combining templates with data.

### Core Features

1. **Business Analysis & Template Discovery**
   - Analyzes any business URL/description to understand offerings
   - Identifies template opportunities based on search patterns
   - Suggests relevant data types for page generation

2. **Template Management System**
   - Create reusable page templates with variable placeholders
   - Support multiple template types (location, comparison, use-case, feature)
   - Template library for common patterns

3. **Data-Driven Page Generation**
   - Import data via CSV or manual entry
   - Generate all possible combinations from template + data
   - Ensure unique elements on each page

4. **Bulk Page Creation**
   - Generate hundreds/thousands of pages from single template
   - SEO optimization built into every page
   - Maintain consistent structure while ensuring uniqueness

5. **Export & Publishing**
   - Export as CSV with all page data
   - WordPress XML format
   - Direct CMS integration capabilities

## Architecture Components

### Core Subagents

#### 1. Business Analyzer Agent
- **Purpose**: Understand any business and identify template opportunities
- **Key Functions**:
  - Analyze business URL/description
  - Identify core offerings and target audience
  - Suggest relevant template types
  - Recommend data categories

#### 2. Template Builder Agent
- **Purpose**: Create and manage reusable page templates
- **Key Functions**:
  - Design templates with variable placeholders
  - Validate template structure for SEO
  - Extract required variables
  - Maintain template library

#### 3. Data Manager Agent
- **Purpose**: Handle data import and combination generation
- **Key Functions**:
  - Import data from CSV or manual entry
  - Validate and clean data
  - Generate all possible combinations
  - Calculate page generation potential

#### 4. Page Generator Agent
- **Purpose**: Create bulk pages from templates + data
- **Key Functions**:
  - Populate templates with data
  - Ensure unique content elements
  - Optimize each page for SEO
  - Generate at scale (hundreds/thousands)

#### 5. Export Manager Agent
- **Purpose**: Export pages in various formats
- **Key Functions**:
  - Export as CSV
  - Generate WordPress XML
  - Create JSON for APIs
  - Maintain URL structure

## Universal Application Examples

### Real Estate SaaS
- **Template**: "[City] [Property Type] Investment Analysis"
- **Data**: Cities (Toronto, Vancouver), Property Types (Condo, House)
- **Result**: "Toronto Condo Investment Analysis", "Vancouver House Investment Analysis"

### Project Management Software
- **Template**: "[Industry] Project Management Best Practices"
- **Data**: Industries (Construction, Healthcare, Marketing)
- **Result**: "Construction Project Management Best Practices"

### E-commerce Store
- **Template**: "Best [Product Category] for [Use Case]"
- **Data**: Categories (Running Shoes, Hiking Boots), Use Cases (Beginners, Trail Running)
- **Result**: "Best Running Shoes for Beginners"

## Development Guidelines

When implementing features:
1. **Template First**: Always think in terms of templates and data, not individual pages
2. **Universal Design**: Ensure features work for ANY business type
3. **Data Validation**: Validate all imported data for quality
4. **Uniqueness**: Each generated page must have unique elements beyond the template
5. **SEO Built-in**: Every page must be SEO-optimized by default
6. **Scale Testing**: Test with hundreds of combinations to ensure performance

## Deployment Configuration (CRITICAL)

**This project is deployed on Vercel as a unified Next.js + FastAPI application.**

### Vercel Requirements
1. **Single Project Structure**: Frontend (Next.js) at root, Backend (FastAPI) in `/api`
2. **No Separate Frontend/Backend**: Everything deploys as one project
3. **API Routes**: FastAPI handles `/api/*` routes via `/api/main.py`
4. **Environment Variables**: Set in Vercel dashboard, not in code
5. **Python Runtime**: Must specify exact version (e.g., `python3.9`, not `python3`)

### All Subagents MUST Follow These Rules:
1. **Never create separate frontend/backend projects**
2. **Always use relative API paths** (e.g., `/api/analyze`, not `http://localhost:8000/api/analyze`)
3. **Never hardcode URLs** - use relative paths
4. **Keep vercel.json minimal** - only Python runtime and rewrites
5. **Test deployment compatibility** before pushing

### Current vercel.json Structure:
```json
{
  "functions": {
    "api/main.py": {
      "runtime": "python3.9"
    }
  },
  "rewrites": [
    {
      "source": "/api/:path*",
      "destination": "/api/main"
    }
  ]
}
```

## Workflow Rules

When working on any development task, follow these steps:

1. **First think through the problem** - Read the codebase for relevant files and write a plan to tasks/todo.md
2. **Create checkable todo items** - The plan should have a list of todo items that you can check off as you complete them
3. **Check in before starting** - Before beginning work, verify the plan with the user
4. **Work systematically** - Begin working on the todo items, marking them as complete as you go
5. **Provide high-level explanations** - Every step of the way, give a high-level explanation of what changes were made
6. **Keep it simple** - Make every task and code change as simple as possible. Avoid massive or complex changes. Every change should impact as little code as possible. Everything is about simplicity.
7. **Add review section** - Finally, add a review section to the todo.md file with a summary of the changes made and any other relevant information

## Development Commands

### Run Locally
```bash
# Option 1: Run both servers with one command
python run_local.py

# Option 2: Run servers separately
# Terminal 1 - API (FastAPI)
python -m uvicorn app.main:app --reload

# Terminal 2 - Frontend (Next.js)
cd frontend
npm run dev
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
- `POST /api/generate-templates` - Generate programmatic SEO template opportunities
- `POST /api/create-template` - Create or save a page template
- `POST /api/import-data` - Import data for template variables
- `POST /api/generate-pages` - Generate all pages from template + data
- `POST /api/export` - Export pages (CSV, JSON, WordPress)

## Environment Variables Required

- `OPENAI_API_KEY` or `ANTHROPIC_API_KEY` or `PerplexityAPI` - At least one AI provider
- Optional: `WORDPRESS_URL`, `WORDPRESS_USERNAME`, `WORDPRESS_APP_PASSWORD` for direct publishing

## Important Implementation Notes

### What Works (Keep These)
1. **Perplexity API Configuration**: Use model "sonar" - tested and working
2. **URL Content Extraction**: Current implementation successfully extracts business info
3. **Business Analysis**: `analyze_business_comprehensive()` provides good foundation
4. **Content Variation Engine**: Uniqueness algorithms work well for bulk pages
5. **Vercel Deployment**: Current setup works without filesystem errors

### Common Pitfalls to Avoid
1. **Don't focus on keyword discovery** - Users will provide their own data
2. **Don't estimate traffic/metrics** - Focus on page generation only
3. **Don't create complex wizards** - Simple template → data → pages flow
4. **Don't generate individual content** - Think bulk generation from templates

## Current Status (As of January 2025)

### Completed
- **Agent Architecture**: All 5 core agents (Business Analyzer, Template Builder, Data Manager, Page Generator, Export Manager) are fully implemented
- **API Integration**: Complete REST API with all endpoints working
- **AI Support**: Perplexity, OpenAI, and Anthropic providers integrated
- **Database**: SQLite database with full project/content tracking
- **Export Formats**: CSV, JSON, WordPress XML export working
- **Workflow Automation**: Complete end-to-end workflow from business analysis to export

### In Progress
- **Next.js Frontend**: Building a modern React-based UI with Next.js 14 App Router
- **Real SEO Data**: Currently using AI-generated mock data; need to integrate Ubersuggest/SerpAPI for real metrics

### Next Steps
1. Create the Next.js frontend with modern UI components and workflow
2. Test the complete workflow end-to-end
3. Integrate real SEO data providers
4. Add production-ready error handling and logging

## Frontend Architecture (Next.js)

### Technology Stack
- **Framework**: Next.js 14 with App Router
- **UI Components**: shadcn/ui + Tailwind CSS
- **State Management**: Zustand for global state
- **Data Fetching**: TanStack Query (React Query)
- **Forms**: React Hook Form + Zod validation
- **Charts**: Recharts for data visualization

### Key Frontend Features
1. **Responsive Design**: Mobile-first approach
2. **Real-time Updates**: WebSocket support for long-running tasks
3. **File Uploads**: Drag-and-drop CSV import
4. **Interactive Preview**: Live template preview with data
5. **Export Queue**: Background export processing with progress