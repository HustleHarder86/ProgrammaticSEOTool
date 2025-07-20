# AI Strategy-Driven Programmatic SEO Tool

Revolutionary tool that uses **AI to generate custom programmatic SEO strategies** instead of static templates. Analyzes your business to create tailored templates, data strategies, and content that serves real user search intent.

## What is AI Strategy-Driven Programmatic SEO?

Instead of generic templates, AI analyzes your business to create custom strategies. Think:
- Real Estate SaaS: AI generates "Is {Property Type} profitable in {City}? ROI Analysis"
- Project Management: AI creates "{Industry} Project Management Guide" with industry-specific insights  
- E-commerce Tools: AI designs "{Platform} Conversion Optimization" with platform-specific strategies

**Revolutionary Formula: Business Analysis + AI Strategy Generation + Custom Templates + Data = Scale with Intent**

## 🚀 Why AI Strategy Generation is Revolutionary

- **Business-Specific**: Every strategy is tailored to your unique business and industry
- **Intent-Driven**: Templates serve actual user search intent, not generic patterns
- **Competitive Advantage**: Creates opportunities competitors don't have
- **Scalable Quality**: Maintains excellence even with massive page generation
- **Real User Value**: Content answers what users actually search for

## Revolutionary Features

- **AI Business Intelligence**: Deep analysis of your business model, market, and customers
- **Dynamic Strategy Generation**: AI creates custom programmatic SEO strategies
- **Intent-Driven Templates**: Templates designed around actual user search patterns
- **Intelligent Data Planning**: AI recommends optimal data structures and sources
- **Content Strategy Framework**: SEO architecture and content planning
- **Implementation Engine**: Convert strategies into working templates and pages
- **Scale with Quality**: Generate hundreds/thousands of pages that serve real user value
- **Multiple Export Options**: CSV, WordPress XML, or API-ready JSON

## 🔧 AI Configuration Required

**CRITICAL**: This tool requires AI providers for content generation.

Set at least one environment variable:
```bash
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key  
PERPLEXITY_API_KEY=your_perplexity_key
```

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
# Supports: Perplexity, OpenAI, or Anthropic (only need one)
```

5. Initialize the database:
```bash
python init_db.py
```

6. Run the backend:
```bash
cd backend
python -m uvicorn main:app --reload
```

The API will be available at http://localhost:8000

7. Run the frontend (in a new terminal):
```bash
npm install
npm run dev
```

The UI will be available at http://localhost:3000

## ⚠️ CRITICAL: Testing Requirements

**Before pushing ANY code changes, you MUST run comprehensive tests.**

This project has a mandatory testing protocol to ensure code quality and minimize manual testing.

### Pre-Push Testing Checklist

Before committing any changes:

```bash
# 1. Test content generation quality
python backend/test_content_generation_comprehensive.py

# 2. Test API integration
python backend/test_api_integration.py

# 3. Test user workflows
python backend/test_user_workflows.py

# 4. Performance testing
python backend/test_performance_benchmarks.py
```

### Quality Standards

All generated content must meet these criteria:
- ✅ No placeholder text ("various options", "${variable}")
- ✅ 300-400 word count for main content
- ✅ Proper grammar and sentence structure
- ✅ Relevant and accurate information
- ✅ SEO-optimized titles and meta descriptions

See [TESTING_PROTOCOL.md](TESTING_PROTOCOL.md) for complete testing requirements.

**NO CODE SHOULD BE PUSHED WITHOUT PASSING ALL TESTS**

## API Documentation

Visit http://localhost:8000/docs for interactive API documentation.

## Quick Start

### Example: Real Estate SaaS

1. **Analyze Your Business**:
   ```
   Input: "Real estate investment analysis tool"
   Output: Template suggestions like "[City] [Property Type] Investment Analysis"
   ```

2. **Choose a Template**:
   ```
   Template: "[City] Real Estate Investment Calculator"
   Variables: {city}, {property_type}
   ```

3. **Add Your Data**:
   ```
   Cities: Toronto, Vancouver, Calgary, Montreal...
   Property Types: Condo, House, Duplex...
   ```

4. **Generate Pages**:
   ```
   Result: 100+ pages like:
   - "Toronto Condo Investment Calculator"
   - "Vancouver House Investment Calculator"
   - "Calgary Duplex Investment Calculator"
   ```

5. **Export & Publish**: Download all pages as CSV or WordPress-ready content

### More Examples

**E-commerce Store**:
- Template: "Best [Product] for [Use Case]"
- Data: Products × Use Cases
- Result: "Best Running Shoes for Marathon Training"

**SaaS Platform**:
- Template: "[Industry] [Software Type] Guide"
- Data: Industries × Features
- Result: "Healthcare CRM Software Guide"

**Local Service**:
- Template: "[Service] in [Neighborhood] [City]"
- Data: Services × Locations
- Result: "Plumbing Services in Downtown Toronto"

## Development

### Backend
- FastAPI with async support
- SQLite database (no setup required)
- Modular agent-based architecture
- Support for multiple AI providers (Perplexity, OpenAI, Anthropic)

### Frontend (Next.js)
- Next.js 14 with App Router
- TypeScript for type safety
- Tailwind CSS + shadcn/ui for modern UI
- Real-time updates with WebSockets
- Responsive design for all devices

## License

Personal use only.