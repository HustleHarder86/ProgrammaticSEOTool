# Programmatic SEO Tool - Backend

This is the FastAPI backend for the Programmatic SEO Tool, designed to be deployed on Railway.

## Features

- Business analysis from URL or text
- Programmatic SEO template generation
- Bulk page generation with AI
- Export to CSV, JSON, or WordPress
- Progress tracking for long operations

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

```bash
# AI Provider (at least one required)
PERPLEXITY_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here
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

# Run locally
uvicorn main:app --reload
```

## API Endpoints

- `GET /health` - Health check
- `POST /api/analyze-business` - Analyze business from URL/text
- `POST /api/generate-templates` - Generate SEO templates
- `POST /api/generate-keywords` - Generate keyword opportunities
- `POST /api/generate-content` - Generate content from templates
- `POST /api/export` - Export generated content

## Architecture

- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - Database ORM (PostgreSQL ready)
- **AI Agents** - Modular agents for different tasks
- **Async Support** - Handles long-running operations

## Database

The backend uses PostgreSQL in production (Railway) and SQLite for local development.
Database migrations are handled automatically on startup.