# Programmatic SEO Tool - Model Context Protocol (MCP)

This document serves as the comprehensive guide for building and maintaining the Programmatic SEO Tool. It should be referenced frequently during development.

## Core Understanding

### What is Programmatic SEO?
Programmatic SEO is the practice of using **templates + data** to generate large numbers of pages that target long-tail keywords. It's NOT about generating individual content pieces, but about creating scalable page templates that can be populated with data.

### Key Formula
```
Template + Data = Scale
```

### Real-World Examples
- **Tripadvisor**: "Things to do in [City]" → One template, thousands of city pages
- **Zillow**: "[City] Real Estate" → Location template with property data
- **Yelp**: "Best [Business Type] in [City]" → Business directory template

## System Architecture

### Core Workflow
```
1. Business Analysis → Understand what templates make sense
2. Template Creation → Design reusable page structures
3. Data Collection → Gather/import relevant data sets
4. Bulk Generation → Create all page combinations
5. Export/Publish → Deploy pages to website
```

### Technical Stack
- **Backend**: FastAPI (Python)
- **AI Integration**: Perplexity API (model: "sonar") - tested and working
- **Database**: SQLite for templates and generated pages
- **Export**: CSV, WordPress XML, JSON
- **Deployment**: Vercel-ready

## Subagent Specifications

### 1. Business Analyzer Agent (`business_analyzer.py`)

**Purpose**: Analyze any business to identify programmatic SEO opportunities

**Core Functions**:
```python
def analyze_business(url_or_description: str) -> BusinessAnalysis:
    """
    Extract business information and identify template opportunities
    Returns: industry, offerings, target_audience, template_suggestions
    """

def suggest_templates(business_analysis: BusinessAnalysis) -> List[Template]:
    """
    Based on business type, suggest relevant templates
    Examples:
    - Local business → Location-based templates
    - E-commerce → Product comparison templates
    - SaaS → Industry/use-case templates
    """

def identify_data_requirements(template: Template) -> List[DataType]:
    """
    For each template, identify what data is needed
    Example: "[City] [Service]" needs cities list and services list
    """
```

**Key Logic**:
- Use existing `analyze_business_comprehensive()` from `ai_handler.py`
- Focus on identifying repeatable patterns
- Suggest 3-5 template types per business
- Consider search intent and user behavior

### 2. Template Builder Agent (`template_builder.py`)

**Purpose**: Create and manage reusable page templates

**Core Functions**:
```python
def create_template(
    name: str,
    pattern: str,  # e.g., "[City] [Service] Prices"
    structure: dict
) -> Template:
    """
    Create a new template with variable placeholders
    """

def extract_variables(template: Template) -> List[Variable]:
    """
    Extract all variables from template
    Example: "[City] [Service]" → ['city', 'service']
    """

def validate_template(template: Template) -> ValidationResult:
    """
    Ensure template is SEO-friendly:
    - Title length (50-60 chars)
    - URL structure
    - Meta description capability
    - Content structure
    """

def generate_preview(template: Template, sample_data: dict) -> str:
    """
    Show how template looks with sample data
    """
```

**Template Structure**:
```python
{
    "title_template": "[City] [Service] - Professional Services",
    "url_template": "/[city]-[service]",
    "meta_description_template": "Find the best [service] in [city]. Compare prices and reviews.",
    "content_sections": [
        {
            "heading": "[Service] in [City] Overview",
            "content": "Dynamic content about [service] specific to [city]"
        }
    ]
}
```

### 3. Data Manager Agent (`data_manager.py`)

**Purpose**: Handle data import, validation, and combination generation

**Core Functions**:
```python
def import_csv(file_path: str, data_type: str) -> DataFrame:
    """
    Import data from CSV file
    Validate and clean data
    """

def add_data_manually(data_type: str, values: List[str]) -> None:
    """
    Add data entries manually
    Example: cities = ["Toronto", "Vancouver", "Calgary"]
    """

def validate_data(data: DataFrame) -> ValidationResult:
    """
    Check for:
    - Duplicates
    - Invalid characters
    - SEO-friendly formatting
    """

def generate_combinations(
    template: Template,
    data_sets: Dict[str, List]
) -> List[PageData]:
    """
    Generate all possible combinations
    Example: 10 cities × 5 services = 50 pages
    """

def estimate_page_count(template: Template, data_sets: Dict) -> int:
    """
    Calculate how many pages will be generated
    """
```

**Data Storage Structure**:
```python
{
    "cities": ["Toronto", "Vancouver", "Calgary", ...],
    "services": ["Plumbing", "Electrical", "HVAC", ...],
    "property_types": ["Condo", "House", "Townhouse", ...],
    "industries": ["Healthcare", "Finance", "Retail", ...]
}
```

### 4. Page Generator Agent (`page_generator.py`)

**Purpose**: Generate actual pages from templates and data

**Core Functions**:
```python
def generate_pages(
    template: Template,
    data_combinations: List[dict]
) -> List[GeneratedPage]:
    """
    Create all pages from template + data
    Ensure each page is unique
    """

def populate_template(
    template: Template,
    data: dict
) -> GeneratedPage:
    """
    Fill template with specific data point
    Example: {city: "Toronto", service: "Plumbing"}
    """

def add_unique_elements(page: GeneratedPage) -> GeneratedPage:
    """
    Add unique content to avoid duplicate penalties:
    - Local statistics
    - Specific examples
    - Unique descriptions
    Use existing content_variation.py logic
    """

def optimize_for_seo(page: GeneratedPage) -> GeneratedPage:
    """
    Ensure SEO best practices:
    - Proper heading structure
    - Keyword density
    - Internal linking opportunities
    - Meta tags
    """

def generate_batch(
    template: Template,
    data_combinations: List[dict],
    batch_size: int = 100
) -> Generator[List[GeneratedPage]]:
    """
    Generate pages in batches for performance
    """
```

### 5. Export Manager Agent (`export_manager.py`)

**Purpose**: Export generated pages in various formats

**Core Functions**:
```python
def export_csv(pages: List[GeneratedPage], output_path: str) -> None:
    """
    Export as CSV with columns:
    - URL
    - Title
    - Meta Description
    - Content
    - Additional SEO fields
    """

def export_wordpress(pages: List[GeneratedPage]) -> str:
    """
    Generate WordPress XML import file
    Maintain proper post structure
    """

def export_json(pages: List[GeneratedPage]) -> dict:
    """
    Export as JSON for API consumption
    """

def generate_sitemap(pages: List[GeneratedPage]) -> str:
    """
    Create XML sitemap for all generated pages
    """

def maintain_url_structure(pages: List[GeneratedPage]) -> None:
    """
    Ensure consistent URL patterns
    Check for conflicts
    """
```

## Implementation Guidelines

### Phase 1: Core Infrastructure
1. Set up FastAPI endpoints for new workflow
2. Create database schema for templates and pages
3. Implement basic template creation and validation

### Phase 2: Business Analysis
1. Adapt existing `analyze_business_comprehensive()` 
2. Build template suggestion logic
3. Create template library with common patterns

### Phase 3: Data Handling
1. Build CSV import functionality
2. Create data validation rules
3. Implement combination generator

### Phase 4: Page Generation
1. Build template population engine
2. Integrate content variation for uniqueness
3. Add SEO optimization layer

### Phase 5: Export and Testing
1. Implement multiple export formats
2. Test with various business types
3. Ensure scalability to 1000+ pages

## Code Reuse Strategy

### Keep and Adapt:
- `ai_handler.py` - Business analysis functions
- `content_variation.py` - Uniqueness algorithms
- URL parsing and extraction logic
- Perplexity API integration (working configuration)

### Delete:
- Keyword generation focused code
- Individual content generation logic
- Traffic estimation features
- Complex wizard interfaces

### New Components:
- Template management system
- Data import and validation
- Bulk page generation engine
- Enhanced export capabilities

## Testing Scenarios

### Real Estate SaaS
- Template: "[City] [Property Type] Investment Analysis"
- Data: 25 cities × 10 property types = 250 pages
- Verify: Each page has unique local data

### E-commerce
- Template: "Best [Product] for [Use Case]"
- Data: 20 products × 5 use cases = 100 pages
- Verify: Product descriptions vary

### Local Service
- Template: "[Service] in [Neighborhood]"
- Data: 10 services × 50 neighborhoods = 500 pages
- Verify: Local optimization present

## Common Patterns Library

### Location-Based Templates
- "[Service] in [City]"
- "[City] [Business Type] Directory"
- "Best [Product] in [Location]"

### Comparison Templates
- "[Product A] vs [Product B]"
- "[Service] Pricing Comparison [Year]"
- "[Option A] or [Option B] for [Use Case]"

### Industry/Use-Case Templates
- "[Industry] [Software] Solutions"
- "[Product] for [Target Audience]"
- "How to [Action] with [Product]"

### Feature-Based Templates
- "[Product] with [Feature]"
- "[Service] including [Benefit]"
- "[Solution] without [Common Problem]"

## Development Workflow

1. **Always start with the business** - What do they offer?
2. **Think in templates** - What patterns can we create?
3. **Identify data sources** - What data do we need?
4. **Calculate scale** - How many pages will this generate?
5. **Ensure uniqueness** - How do we make each page valuable?
6. **Test at scale** - Does it work with 500+ pages?

## Success Metrics

- ✅ Can analyze any business type
- ✅ Suggests relevant templates automatically
- ✅ Handles 1000+ page generation smoothly
- ✅ Each page is unique and SEO-optimized
- ✅ Multiple export formats work correctly
- ✅ Templates are reusable across projects

## Remember

**This is about scale through templates, not individual content creation.** Every feature should support the core workflow: Template + Data = Hundreds of Pages.