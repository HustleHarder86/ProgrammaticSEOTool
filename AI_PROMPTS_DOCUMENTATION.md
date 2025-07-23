# AI Prompts Documentation - Content Generation System

This document details the exact AI prompts and data flow used in the Programmatic SEO Tool content generation system.

## Overview

The system has two main content generation paths:
1. **AI-Enhanced Generation** (SmartPageGenerator) - Uses AI providers when available
2. **Pattern-Based Generation** (EfficientPageGenerator) - Uses templates and enriched data

## Current AI Provider Status

⚠️ **IMPORTANT**: Based on the test logs, **NO AI PROVIDER IS CURRENTLY CONFIGURED**. The system shows:
```
No AI provider configured
```

This means all content is being generated via the **Pattern-Based Generation** path, not AI prompts.

## AI Prompts (When AI Providers Are Available)

### 1. SmartPageGenerator AI Prompts

Located in: `backend/smart_page_generator.py`

#### Evaluation Question Prompt
```
Write a 350-400 word answer to: "{title}"

Use ONLY this verified data:
{data_summary}

Structure your response:
1. Start with a clear yes/no answer backed by the data
2. Present 3-4 key data points that support your answer
3. Include specific numbers and percentages from the data
4. Address potential concerns or considerations
5. End with actionable next steps

Important:
- Use ONLY the data provided above
- Be specific with numbers, don't round excessively
- Write in a conversational but informative tone
- Make it scannable with short paragraphs
- Do NOT invent any statistics or data points
```

#### Location Service Prompt
```
Create a 350-word overview for: "{title}"

Use ONLY this verified data:
{data_summary}

Structure:
1. Opening with provider count and average rating
2. List top 3-4 providers with their ratings
3. Local market insights (pricing, availability)
4. What makes this location unique for this service
5. Clear call-to-action

Requirements:
- Include all specific numbers from the data
- Make it locally relevant
- Focus on helping users make decisions
- Natural, helpful tone
```

#### Comparison Prompt
```
Write a 350-word comparison for: "{title}"

Use ONLY this data:
{data_summary}

Structure:
1. Quick verdict - which is better for what use case
2. Key differences table or list
3. Pricing comparison with specific numbers
4. Best use cases for each option
5. Final recommendation based on data

Keep it factual and data-driven.
```

#### Generic Prompt
```
Create a 350-word informative piece for: "{title}"

Using this data:
{data_summary}

Make it valuable by:
1. Answering the implicit query
2. Providing specific data points
3. Offering practical insights
4. Ending with next steps

Use only provided data.
```

## Current Pattern-Based Generation (What's Actually Running)

Since no AI provider is configured, the system uses pattern-based generation with enriched data.

### Step-by-Step Content Generation Process

#### Step 1: Data Enrichment
**File**: `backend/data_enricher.py`

**Input Example**:
```python
{
    "Service": "single-family home short-term rental",
    "City": "Calgary"
}
```

**DataEnricher Logic**:
1. Detects content type based on service keywords
2. If service contains "rental", "investment", "property", "home" → rental property data
3. Otherwise → service provider data

**Enriched Data Output**:
```python
{
    "primary_data": {
        "city": "Calgary",
        "property_type": "Single-Family Home Short-Term Rental",
        "average_nightly_rate": 180,
        "occupancy_rate": 70,
        "total_listings": 200,
        "market_growth": 10,
        "regulations": "Check local regulations",
        "peak_season": "Summer months",
        "monthly_revenue": 3780,
        "monthly_expenses": 800,
        "monthly_profit": 2980,
        "roi_percentage": 132.4,
        "typical_bedrooms": 3
    },
    "enriched_data": {
        "market_strength": "moderate",
        "regulation_status": "restrictive",
        "profitability": "good",
        "competition_level": "moderate"
    },
    "data_quality": 0.85
}
```

#### Step 2: Data Mapping
**File**: `backend/data_mapper.py`

**Business Logic Mappings**:
```python
# Profitability mapping
roi = 132.4%, occupancy = 70%
→ "profitability": "highly profitable"

# Answer mapping
roi >= 15 and occupancy >= 60
→ "answer": "Yes"

# Market strength mapping
listings = 200, growth = 10%
→ "market_strength": "emerging"
```

**Transformed Data** (subset):
```python
{
    "Service": "single-family home short-term rental",
    "City": "Calgary",
    "average_nightly_rate": 180,
    "occupancy_rate": 70,
    "profitability": "highly profitable",
    "answer": "Yes",
    "market_strength": "emerging",
    "monthly_revenue": 3780,
    "roi_percentage": 132.4
}
```

#### Step 3: Content Pattern Application
**File**: `backend/content_patterns.py`

**Intro Pattern** (selected based on content type):
```
"{answer}, {Service} can be {profitability} in {City}. Average occupancy: {occupancy_rate}%, typical nightly rate: ${average_nightly_rate}."
```

**After Variable Substitution**:
```
"Yes, single-family home short-term rental can be highly profitable in Calgary. Average occupancy: 70%, typical nightly rate: $180."
```

#### Step 4: Enhanced Content Generation
**File**: `backend/efficient_page_generator.py`

The system generates multiple content sections:

##### Section 1: Introduction (from pattern above)
```html
<p class='intro'>Yes, single-family home short-term rental can be highly profitable in Calgary. Average occupancy: 70%, typical nightly rate: $180.</p>
```

##### Section 2: Financial Performance Metrics
```html
<div class='key-metrics'>
<h3>Financial Performance Metrics</h3>
<p><strong>Average Nightly Rate:</strong> $180 - This rate positions properties competitively within the local market while maintaining profitability potential.</p>
<p><strong>Occupancy Rate:</strong> 70% - Strong performance indicating healthy demand in the local market.</p>
<p><strong>Market Size:</strong> 200 active listings - Focused market with targeted opportunities for investment.</p>
<p><strong>Expected ROI:</strong> 132.4% - Excellent returns exceeding market averages.</p>
<p><strong>Monthly Financials:</strong> Revenue $3,780, Expenses $800, Net Profit $2,980.</p>
</div>
```

##### Section 3: Market Analysis & Trends
```html
<h3>Market Analysis & Trends</h3>
<p>Current market analysis reveals 10% growth in this sector over the past year. This demonstrates steady market expansion and stable investment conditions. The consistent growth pattern indicates reliable demand and mature market dynamics. Regulatory environment: check local regulations. Peak demand typically occurs during summer months.</p>
```

##### Section 4: Investment Considerations
```html
<h3>Investment Considerations for Calgary</h3>
<p>Success with single-family home short-term rental in Calgary depends on several critical factors. Location selection remains paramount - properties in high-traffic areas, near attractions, or in desirable neighborhoods typically achieve higher occupancy rates and premium pricing. Property condition and presentation significantly impact guest satisfaction and repeat bookings.</p>
<p>Operational considerations include effective marketing across multiple platforms, responsive customer service, competitive pricing strategies, and maintaining high cleanliness standards. Local market knowledge helps optimize pricing during peak and off-season periods. Additionally, understanding neighborhood dynamics, parking availability, and noise regulations ensures smooth operations and positive community relations.</p>
```

##### Section 5: Market Context
```html
<h3>Market Context for Calgary</h3>
<p>The single-family home short-term rental market in Calgary experiences highest demand during summer months. The 10% annual growth rate indicates stable market expansion and sustained demand. Success in this market typically depends on location selection, competitive pricing, and understanding local preferences.</p>
```

##### Section 6: Key Benefits and Considerations
```html
<h3>Key Benefits and Considerations</h3>
<p><strong>Financial Potential:</strong> Based on current market data, single-family home short-term rental in Calgary offers strong financial returns with 132.4% average ROI. Successful operators typically see monthly revenues around $3,780.</p>
<p><strong>Risk Factors:</strong> Consider seasonal variations, maintenance costs, regulatory changes, and local competition. Success requires active management, quality property presentation, and responsive customer service.</p>
```

## Content Type Detection Logic

**File**: `backend/efficient_page_generator.py`

```python
def _detect_content_type(self, template, data):
    pattern = template.get("pattern", "").lower()
    
    # Check if it's a question or evaluation
    if (pattern.startswith("is ") or pattern.startswith("are ") or 
        pattern.startswith("can ") or pattern.startswith("should ") or
        "?" in pattern or
        "analysis" in pattern or "investment" in pattern or "evaluation" in pattern):
        
        # Determine question type
        if ("good" in pattern or "worth" in pattern or "best" in pattern or
            "analysis" in pattern or "investment" in pattern or "evaluation" in pattern or
            "rental" in pattern or "property" in pattern):
            return "evaluation_question"
        else:
            return "general_question"
    # ... other content types
```

**Example**:
- Input: `"Is {Service} a good investment in {City}?"` 
- Contains "?" and "investment" → `"evaluation_question"`

## Data Quality Thresholds

**File**: `backend/smart_page_generator.py`

```python
# Check data quality (be more lenient since we have better fallback now)
if enriched_data["data_quality"] < 0.3:
    # Only fall back to old method for very poor data quality
    return super().generate_page(template, data_row, page_index)
```

**Current data quality**: 0.85 (well above 0.3 threshold)

## AI Provider Configuration

To enable AI-enhanced content generation, set environment variables:

```bash
# At least one required
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key  
PERPLEXITY_API_KEY=your_perplexity_key
```

**Current Status**: None configured → Pattern-based generation only

## Content Generation Quality Metrics

**Final Output Metrics**:
- **Word Count**: 343 words (target: 300-400)
- **Quality Score**: 70/100
- **Content Sections**: 6 comprehensive sections
- **Data Points Used**: 12+ real metrics
- **Placeholder Text**: 0 instances ("various options" eliminated)

## Summary

The current high-quality content is generated through:
1. **Smart data enrichment** with realistic market data
2. **Business logic mapping** for derived insights
3. **Pattern-based content generation** with multiple detailed sections
4. **Enhanced content structure** with proper headings and analysis

The AI prompts are ready for use but require API key configuration to activate AI-enhanced generation.