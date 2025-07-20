# AI Strategy-Driven Programmatic SEO Tool - Backend

This is the revolutionary **AI Strategy Generation** FastAPI backend that creates custom programmatic SEO strategies instead of using static templates. Analyzes businesses to generate tailored templates and content strategies.

## 🚀 Revolutionary Features

- **AI Strategy Generation**: Creates custom programmatic SEO strategies for any business
- **Dynamic Template Creation**: AI generates templates based on real user search intent
- **Business Intelligence Analysis**: Deep understanding of business model and market
- **Intelligent Data Planning**: AI recommends optimal data structures and sources
- **Content Strategy Framework**: SEO architecture and internal linking strategies
- **Implementation Engine**: Converts strategies into working templates and pages
- **Scale with Intent**: Generate hundreds/thousands of pages that serve real user value

## ⚡ AI Strategy-First Architecture

**REVOLUTIONARY**: This tool uses AI to generate custom programmatic SEO strategies instead of static templates.

**Business Analysis + AI Strategy Generation + Custom Templates + Data = Scale with Intent**

### Revolutionary AI Strategy Process:
1. **Deep Business Analysis** - AI understands business model, customers, market
2. **Opportunity Discovery** - AI identifies scalable content opportunities
3. **Dynamic Template Creation** - AI generates custom templates for real user search intent
4. **Data Strategy Design** - AI recommends optimal data structures
5. **Implementation** - Convert strategies into working templates and pages

### Why AI Strategy Generation is Game-Changing:
- **Business-Specific**: Every strategy tailored to your unique business
- **Intent-Driven**: Templates serve actual user search intent, not generic patterns
- **Competitive Advantage**: Creates opportunities competitors don't have
- **Scalable Quality**: Maintains excellence even with thousands of pages

## Deployment on Railway

### Quick Deploy

1. Fork/clone this repository
2. Sign up at [railway.app](https://railway.app)
3. Create new project → Deploy from GitHub
4. Select your repository
5. Set root directory to `/backend`
6. Add environment variables (see below)
7. Deploy!

### Required Environment Variables

**CRITICAL**: At least one AI provider is mandatory for the tool to function.

```bash
# AI Provider (MANDATORY - at least one required)
PERPLEXITY_API_KEY=your_key_here    # Recommended for SEO content
OPENAI_API_KEY=your_key_here         # Alternative option
ANTHROPIC_API_KEY=your_key_here      # Alternative option
ANTHROPIC_API_KEY=your_key_here

# Frontend URL (your Vercel deployment)
FRONTEND_URL=https://your-app.vercel.app

# Database (Railway provides this automatically)
DATABASE_URL=postgresql://...
```

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env with your keys

# Initialize database
python init_db.py

# Run locally
uvicorn main:app --reload
```

## Testing Requirements

**CRITICAL**: Before pushing any code changes, you MUST run comprehensive tests.

See [TESTING_PROTOCOL.md](../TESTING_PROTOCOL.md) for complete testing requirements.

### Quick Test Commands

```bash
# Test content generation (most important)
python test_content_generation_comprehensive.py

# Test API endpoints
python test_api_integration.py

# Test with real user scenarios
python test_user_workflows.py

# Performance testing
python test_performance_benchmarks.py
```

### Pre-Push Checklist

Before pushing ANY code:
- [ ] Content generation produces quality output (no "various options")
- [ ] All API endpoints return proper responses
- [ ] Error handling works for edge cases
- [ ] Performance is acceptable for bulk operations
- [ ] No regression in existing functionality
- [ ] Comprehensive test suite passes

**NO CODE SHOULD BE PUSHED WITHOUT COMPLETING THESE TESTS**

## API Endpoints

### Revolutionary AI Strategy Endpoints
- `POST /api/generate-ai-strategy` - **NEW**: Generate complete custom programmatic SEO strategy
- `POST /api/projects/{id}/implement-ai-strategy` - **NEW**: Convert AI strategy into templates

### Core System Endpoints  
- `GET /health` - Health check with AI provider status
- `POST /api/analyze-business` - Analyze business from URL/text
- `POST /api/projects/{id}/templates/{tid}/generate` - Generate pages from templates
- `POST /api/projects/{id}/export` - Export generated content

### Debug & Testing Endpoints
- `GET /api/test/ai-providers` - Check AI provider configuration
- `POST /api/test/ai-generation` - Test AI content generation
- `GET /api/costs/all-projects` - View API usage costs

## Architecture

- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - Database ORM (PostgreSQL ready)
- **AI Agents** - Modular agents for different tasks
- **Async Support** - Handles long-running operations

## Database

The backend uses PostgreSQL in production (Railway) and SQLite for local development.
Database migrations are handled automatically on startup.