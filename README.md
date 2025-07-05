# Programmatic SEO Tool

Create hundreds or thousands of SEO-optimized pages using the power of templates + data. Works for ANY business type.

## What is Programmatic SEO?

Programmatic SEO uses templates and data to generate pages at scale. Think:
- Tripadvisor's "Things to do in [City]" pages
- Zillow's "[City] Real Estate" pages  
- Yelp's "Best [Business] in [Location]" pages

**Formula: One Template + Your Data = Hundreds of Pages**

## Features

- **Universal Business Analysis**: Works for any business type or industry
- **Smart Template Creation**: Generate templates with variable placeholders
- **Bulk Data Import**: CSV upload or manual data entry
- **Instant Page Generation**: Create 100s of pages in seconds
- **SEO Optimization**: Every page optimized for search engines
- **Multiple Export Options**: CSV, WordPress XML, or API-ready JSON

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

5. Run the application:
```bash
python -m uvicorn app.main:app --reload
```

The API will be available at http://localhost:8000

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

- FastAPI backend with async support
- SQLite database (no setup required)
- Modular architecture for easy extension

## License

Personal use only.