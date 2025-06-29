# Programmatic SEO Tool

A personal tool for generating thousands of SEO-optimized pages automatically.

## Features

- **Dual Input Methods**: Analyze businesses via text description or URL scanning
- **Keyword Research**: Discover high-potential keywords automatically
- **Content Generation**: Create unique, SEO-optimized content at scale
- **Export Options**: CSV, JSON, or direct WordPress integration

## Setup

1. Clone the repository:
```bash
git clone <your-repo-url>
cd ProgrammaticSEOTool
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment:
```bash
cp .env.example .env
# Edit .env with your API keys
```

5. Run the application:
```bash
python -m uvicorn app.main:app --reload
```

The API will be available at http://localhost:8000

## API Documentation

Visit http://localhost:8000/docs for interactive API documentation.

## Quick Start

1. **Analyze a business**:
   - Text input: Describe your business
   - URL input: Provide your website URL

2. **Generate keywords**: Get 50-100 keyword opportunities

3. **Create content**: Generate unique pages for each keyword

4. **Export**: Download as CSV or publish to WordPress

## Development

- FastAPI backend with async support
- SQLite database (no setup required)
- Modular architecture for easy extension

## License

Personal use only.