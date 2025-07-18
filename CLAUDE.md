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

## CRITICAL: Testing & Quality Assurance Protocol

**MANDATORY TESTING BEFORE ANY CODE PUSH:**

When debugging or fixing any issue, you MUST follow this comprehensive testing protocol:

### 1. Pre-Push Testing Requirements
Before pushing ANY code changes, you MUST:

1. **Create comprehensive tests** that validate the specific functionality being fixed
2. **Test edge cases and error scenarios** - don't just test the happy path
3. **Run integration tests** to ensure the fix doesn't break other parts
4. **Validate end-to-end workflows** from user input to final output
5. **Test with real data scenarios** that match production usage
6. **Verify error handling and fallback mechanisms** work properly

### 2. Content Generation Testing Protocol
For any content generation fixes, you MUST:

1. **Test all content types** (evaluation_question, location_service, comparison, generic)
2. **Validate variable substitution** - ensure no "various options" or placeholder text
3. **Check content quality** - verify 300-400 word count, proper grammar, coherent structure
4. **Test AI provider scenarios** - both with and without AI providers configured
5. **Verify data flow** - ensure DataEnricher data reaches ContentPatterns properly
6. **Quality score validation** - ensure scoring reflects actual content quality

### 3. Test Creation Guidelines
When creating tests:

1. **Write test scripts** that can be run automatically to validate fixes
2. **Include both unit tests** (individual components) and **integration tests** (full workflows)
3. **Test with multiple business types** to ensure universal compatibility
4. **Create test data** that represents real user scenarios
5. **Document test results** with clear pass/fail criteria

### 4. Deployment Testing
Before deploying to Railway/Vercel:

1. **Test locally first** - ensure all functionality works in local environment
2. **Run test suite** - execute all relevant tests and document results
3. **Test API endpoints** - verify all endpoints respond correctly
4. **Check logs** - ensure no errors or warnings in application logs
5. **Performance testing** - validate generation speed and memory usage

### 5. Bug Discovery Protocol
When testing reveals additional bugs:

1. **Document all bugs found** - create comprehensive list with reproduction steps
2. **Fix all related issues** - don't just fix the original problem
3. **Re-test after each fix** - verify fixes don't introduce new problems
4. **Update test suite** - add tests for newly discovered edge cases

### 6. User Acceptance Validation
For major fixes, include:

1. **Test the exact user scenario** that revealed the original problem
2. **Validate output quality** meets user expectations
3. **Check for regressions** - ensure previously working features still work
4. **Performance benchmarks** - ensure changes don't slow down the system

### Example Testing Workflow:
```bash
# 1. Create test for the specific issue
python test_content_generation_fix.py

# 2. Run comprehensive test suite
python test_full_system.py

# 3. Test API endpoints
python test_api_integration.py

# 4. Validate with real scenarios
python test_user_scenarios.py

# 5. Check performance
python test_performance_benchmarks.py
```

**NO CODE SHOULD BE PUSHED WITHOUT COMPLETING THIS TESTING PROTOCOL**

This ensures that manual testing by the user is minimized and issues are caught before deployment.

## Deployment Configuration (CRITICAL)

**This project uses a separated architecture: Frontend on Vercel, Backend on Railway**

### Current Deployment Architecture
1. **Frontend**: Next.js deployed on Vercel
2. **Backend**: FastAPI deployed on Railway (separate project)
3. **Communication**: Frontend calls Railway backend via environment variable URL
4. **Why Separated**: Vercel couldn't handle mixed Python/Next.js well (discovered during development)

### Deployment URLs
- **Frontend (Vercel)**: https://programmatic-seo-tool.vercel.app
- **Backend (Railway)**: https://programmaticseotool-production.up.railway.app

### Frontend (Vercel) Requirements
1. **Next.js Only**: Pure Next.js frontend, no Python
2. **Environment Variable**: `NEXT_PUBLIC_API_URL` points to Railway backend
3. **API Calls**: Use axios client with backend URL from environment
4. **CORS**: Backend configured to accept Vercel frontend origin

### Backend (Railway) Requirements
1. **FastAPI Application**: Full backend in `/backend` directory
2. **Database**: SQLite for persistence
3. **Environment Variables**: AI provider keys set in Railway
4. **CORS Middleware**: Configured to accept frontend domain

### All Subagents MUST Follow These Rules:
1. **Keep frontend and backend separate** - they deploy to different platforms
2. **Use environment variable for API URL** in frontend (not hardcoded)
3. **Frontend uses `NEXT_PUBLIC_API_URL`** for all API calls
4. **Test CORS configuration** when making API changes
5. **Update both deployments** when making breaking changes

### Current vercel.json Structure (Frontend Only):
```json
{
  "framework": "nextjs"
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

### ✅ Completed (January 13, 2025 - Latest Updates)
- **Backend Deployment**: Successfully deployed minimal FastAPI backend on Railway
- **Frontend-Backend Connection**: Frontend on Vercel connected to Railway backend
- **Business Analysis API**: Working endpoint with Perplexity AI integration
- **AI Response Parsing**: Fixed JSON parsing from Perplexity markdown responses
- **API Connectivity**: Full frontend-backend communication working
- **Business Analysis**: AI successfully analyzes businesses and suggests templates
- **Template Creation**: Templates can be created with proper variable format ({Variable} not [Variable])
- **Project Management**: Full CRUD operations for projects working
- **AI-Powered Data Generation**: Automatic variable generation eliminates manual CSV creation
- **Smart Content Generation**: AI + real data creates valuable, Yelp/Zapier-style content
- **Data Enrichment System**: Provides real market statistics for accurate content

### 🆕 Latest Implementation: Smart AI Content Generation
1. **DataEnricher Class** (`backend/data_enricher.py`)
   - Provides real market data (rental rates: $127/night, occupancy: 68%)
   - Calculates ROI and profitability metrics
   - Returns data quality scores for content generation

2. **SmartPageGenerator Class** (`backend/smart_page_generator.py`)
   - Uses AI + real data to generate valuable content
   - Answers questions accurately with statistics
   - Falls back to patterns if AI unavailable
   - 300-400 words of data-driven content per page

3. **Content Quality Improvement**
   - Before: "Find 55 services options in Winnipeg. Most popular: Highly Rated Pro."
   - After: "Yes, single-family homes in Winnipeg can be profitable short-term rentals. Average nightly rate: $127 with 68% occupancy. Current market has 342 active STRs, up 23% from last year."

### 🔧 Key Learnings from Development
1. **AI Integration Works**: Perplexity API successfully generates relevant template suggestions
2. **Variable Format**: Templates must use {Variable} format, not [Variable]
3. **Data Format**: API expects list of dictionaries, not dictionary of lists
4. **Programmatic SEO Formula**: Volume + Real Data = Success (not perfect content)
5. **User Experience**: AI-generated data eliminates CSV creation friction
6. **Content Strategy**: Follow Yelp/Zapier model - real data presented simply

### 💡 Problem Solved: No More Manual CSV Creation
The tool now uses AI to automatically:
1. Generate relevant variables based on template and business context
2. Create realistic data combinations (cities, services, products)
3. Produce 10-1000s of page variations instantly
4. Ensure data quality and relevance

### 🚀 Working Endpoints
- `GET /health` - Health check
- `GET /api/test` - Test endpoint  
- `POST /api/analyze-business` - AI-powered business analysis
- `POST /api/projects/{id}/templates/{tid}/generate-variables` - AI variable generation
- `POST /api/projects/{id}/templates/{tid}/generate` - Smart page generation with real data
- Full project, template, data, and page generation APIs

## Current Status (Original)

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