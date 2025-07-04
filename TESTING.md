# Testing Keyword Generation

This guide shows how to test the keyword generation functionality of the Programmatic SEO Tool.

## Quick Start

The tool works perfectly with just an AI API key (OpenAI or Anthropic). No SEO API keys required!

### 1. Set up environment variables

Create a `.env` file with your AI API key:

```bash
# Choose one of these:
OPENAI_API_KEY=your-openai-api-key-here
# OR
ANTHROPIC_API_KEY=your-anthropic-api-key-here
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the API server

```bash
python -m uvicorn app.main:app --reload
```

### 4. Test keyword generation

In another terminal, run the test script:

```bash
./test_api.sh
```

## What the tool does with AI-only mode:

1. **Analyzes your business** - Extracts industry, services, and target audience
2. **Generates 5-10 programmatic SEO strategies** - Each strategy can generate 50-1000+ pages
3. **Creates keyword variations** - Long-tail, questions, location-based, comparisons
4. **Estimates metrics** - Provides AI-based estimates for search volume and difficulty
5. **Generates content** - Creates unique, SEO-optimized content for each keyword

## Example strategies for a digital marketing agency:

- **"Best [Service] for [Industry]"** - 500+ pages
- **"[Service] vs [Service] Comparison"** - 300+ pages  
- **"How to [Task] for [Business Type]"** - 400+ pages
- **"[Service] Pricing in [Location]"** - 200+ pages
- **"[Industry] [Service] Guide"** - 300+ pages

## Testing with Streamlit UI

You can also test using the visual interface:

```bash
# Run the wizard interface (recommended)
streamlit run streamlit_wizard.py

# Or run the traditional interface
streamlit run streamlit_app.py
```

## API Endpoints for Testing

- `POST /api/analyze-business` - Analyze a business from text or URL
- `POST /api/generate-strategies` - Generate programmatic SEO strategies
- `POST /api/generate-keywords-for-strategy` - Generate keywords for a specific strategy
- `POST /api/discover-keywords` - Discover related keywords from seed keywords
- `POST /api/generate-content` - Generate content for keywords

## Notes

- **For programmatic SEO, quantity > precision** - AI-generated keywords work great!
- **No rate limits** - Generate thousands of keywords without API restrictions
- **Cost effective** - Only pay for AI tokens, not expensive SEO APIs
- **Fast generation** - No external API calls means quick results

The tool is specifically designed for programmatic SEO where you want to create hundreds or thousands of pages targeting long-tail keywords. The AI excels at generating diverse keyword variations that capture search intent.