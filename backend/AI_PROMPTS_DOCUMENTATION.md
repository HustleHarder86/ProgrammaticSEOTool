# AI Prompts Documentation - Programmatic SEO Tool

This document contains all AI prompts and API calls found in the backend code.

## 1. ai_client.py

### Business Analysis Prompts

#### URL-based Business Analysis (Lines 36-53)
```python
prompt = f"""
Analyze this website for programmatic SEO opportunities.

Website URL: {business_input}
Website Content:
{url_content[:2000]}

Based on this website, provide a JSON response with:
1. business_name: The actual business name from the website
2. business_description: What this business/app actually does based on the website content
3. target_audience: Who actually uses this product/service
4. core_offerings: List of 3-5 main features/services from the website
5. template_opportunities: Array of realistic programmatic SEO template opportunities

IMPORTANT: Base your analysis on what the website ACTUALLY does, not assumptions.

Format response as JSON in a markdown code block.
"""
```

#### Text-based Business Analysis (Lines 55-71)
```python
prompt = f"""
Analyze this business for programmatic SEO opportunities: {business_input}

Provide a JSON response with:
1. business_name: A clear business name
2. business_description: Business description  
3. target_audience: Who the business serves
4. core_offerings: List of 3-5 main products/services
5. template_opportunities: Array of template opportunities, each with:
   - template_name: Descriptive name
   - template_pattern: Template pattern (e.g., {{Service}} in {{City}})
   - example_pages: 3 example page titles
   - estimated_pages: Number between 50-500
   - difficulty: Easy/Medium/Hard

Format response as JSON in a markdown code block.
"""
```

## 2. smart_page_generator.py

### Content Generation Prompts (Lines 20-89)

#### Evaluation Question Prompt (Lines 21-40)
```python
"evaluation_question": """
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
"""
```

#### Location Service Prompt (Lines 41-59)
```python
"location_service": """
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
"""
```

#### Comparison Prompt (Lines 60-74)
```python
"comparison": """
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
"""
```

#### Generic Content Prompt (Lines 75-88)
```python
"generic": """
Create a 350-word informative piece for: "{title}"

Using this data:
{data_summary}

Make it valuable by:
1. Answering the implicit query
2. Providing specific data points
3. Offering practical insights
4. Ending with next steps

Use only provided data.
"""
```

## 3. agents/variable_generator.py

### Variable Generation Prompt (Lines 194-252)
```python
prompt = f"""Generate {target_count} relevant values for the variable "{variable_name}" in a programmatic SEO context.

Business Context:
- Business: {business_name}
- Description: {business_desc}
- Industry: {industry}
- Target Audience: {target_audience}
- Core Offerings: {', '.join(offerings) if offerings else 'Various services'}

Variable Type: {variable_type}
Variable Name: {variable_name}
"""

# Type-specific additions:
if variable_type == 'location':
    prompt += f"""
Generate {target_count} relevant locations (cities, regions, etc.) that would be most relevant for {business_name}.
Consider the business's target market and likely service areas."""

elif variable_type == 'category':
    prompt += f"""
Generate {target_count} relevant categories, types, or styles that relate to {business_name}'s offerings.
Focus on categories that users would actually search for."""

# ... additional type-specific instructions ...

prompt += """

Requirements:
1. Return ONLY a JSON array of strings
2. Each value should be realistic and searchable
3. Values should be diverse but relevant
4. Use proper capitalization
5. Avoid duplicates
6. Focus on high-search-volume terms when possible

Example format: ["Value 1", "Value 2", "Value 3"]

Generate the values:"""
```

### Additional Values Generation (Lines 316-322)
```python
prompt = f"""Generate {needed_count} MORE values for "{variable_name}".

Already have: {', '.join(existing_values[:5])}...

Generate {needed_count} additional DIFFERENT values following the same pattern.
Return as JSON array.
"""
```

### Template Suggestions (Lines 380-394)
```python
prompt = f"""Based on the following business and generated variables, suggest 3-5 additional programmatic SEO template patterns:

Business: {business_context.get('business_name')}
Current Template: {current_template}
Available Variables: {', '.join(generated_variables.keys())}

Suggest template patterns that:
1. Use the same variables in different combinations
2. Target different search intents
3. Would create valuable SEO pages

Return as JSON array with format:
[{{"pattern": "template pattern", "intent": "search intent", "example": "example title"}}]
"""
```

## 4. ai_strategy_generator.py

### Business Intelligence Analysis (Lines 96-142)
```python
prompt = f"""
You are a world-class business analyst and programmatic SEO strategist. 
Analyze this business deeply to understand their offerings, market, and SEO opportunities.

Business Description: {business_input}

{f"Website Content: {url_content[:2000]}" if url_content else ""}

Provide a comprehensive analysis in JSON format:

{{
    "business_core": {{
        "name": "Actual business name",
        "industry": "Specific industry/vertical",
        "business_model": "How they make money (SaaS, marketplace, services, etc.)",
        "value_proposition": "What unique value they provide",
        "target_customers": "Specific customer segments with titles/demographics",
        "price_range": "Typical pricing or price range if available"
    }},
    "market_position": {{
        "target_audience_personas": ["Persona 1 with details", "Persona 2 with details"],
        "customer_pain_points": ["Pain point 1", "Pain point 2", "Pain point 3"],
        "solution_benefits": ["Benefit 1", "Benefit 2", "Benefit 3"],
        "competitive_differentiation": "What makes them unique",
        "market_size_indicator": "Large/Medium/Small/Niche"
    }},
    "search_behavior_analysis": {{
        "primary_search_intents": ["Intent 1", "Intent 2", "Intent 3"],
        "customer_journey_stages": {{
            "awareness": ["What they search when they have a problem"],
            "consideration": ["What they search when researching solutions"],
            "decision": ["What they search when ready to buy/use"]
        }},
        "geographic_relevance": "Local/Regional/National/Global",
        "seasonal_patterns": "Any seasonal search patterns"
    }},
    "content_opportunities": {{
        "high_volume_topics": ["Topic that gets lots of searches"],
        "long_tail_opportunities": ["Specific long-tail keyword areas"],
        "comparison_opportunities": ["What they compare against"],
        "educational_needs": ["What customers need to learn"],
        "local_opportunities": ["Location-based opportunities if relevant"]
    }}
}}

Be specific and actionable. Base everything on real market understanding.
"""
```

### Market Opportunities Discovery (Lines 167-219)
```python
prompt = f"""
You are a programmatic SEO expert. Based on this business analysis, identify specific opportunities
for programmatic SEO that could generate hundreds or thousands of valuable pages.

Business: {business_core.get("name", "Unknown")}
Industry: {business_core.get("industry", "Unknown")}
Target Customers: {business_core.get("target_customers", "Unknown")}

Search Intents: {search_behavior.get("primary_search_intents", [])}
Customer Journey: {search_behavior.get("customer_journey_stages", {})}

Identify programmatic SEO opportunities in JSON format:

{{
    "scalable_content_types": [
        {{
            "content_type": "Location-based analysis",
            "search_volume_potential": "High/Medium/Low",
            "competition_level": "High/Medium/Low",
            "user_value": "What value this provides to users",
            "example_queries": ["Example search query 1", "Example search query 2"],
            "scale_potential": "How many pages this could generate"
        }}
    ],
    "template_opportunities": [
        {{
            "template_concept": "Descriptive name of template concept",
            "search_intent": "What search intent this serves",
            "target_keywords": ["Primary keyword pattern", "Secondary keyword pattern"],
            "content_differentiation": "What makes this content unique/valuable",
            "estimated_pages": "Number of pages this could generate"
        }}
    ],
    "data_multiplication_opportunities": [
        {{
            "data_type": "Type of data to collect/use",
            "multiplication_factor": "How this data multiplies (e.g., 50 cities × 10 services = 500 pages)",
            "value_proposition": "Why users would want this specific data combination",
            "competitive_advantage": "Why competitors likely don't have this"
        }}
    ],
    "market_gaps": [
        {{
            "gap_description": "What's missing in the market",
            "opportunity_size": "Large/Medium/Small",
            "difficulty_to_execute": "Easy/Medium/Hard",
            "first_mover_advantage": "Why being first matters here"
        }}
    ]
}}

Focus on opportunities that provide real user value, not just SEO volume.
"""
```

### Template Creation (Lines 259-303)
```python
prompt = f"""
Create a specific programmatic SEO template for this opportunity:

Business: {business_core.get("name", "Unknown")}
Industry: {business_core.get("industry", "Unknown")}
Template Concept: {opportunity.get("template_concept", "Unknown")}
Search Intent: {opportunity.get("search_intent", "Unknown")}
Target Keywords: {opportunity.get("target_keywords", [])}

Generate a complete template in JSON format:

{{
    "template_name": "Descriptive name for this template",
    "template_pattern": "Title pattern with variables like {{Variable1}} {{Variable2}} Analysis",
    "h1_pattern": "H1 pattern that's similar but slightly different",
    "search_intent_served": "Specific search intent this serves",
    "target_variables": [
        {{
            "variable_name": "Variable1",
            "description": "What this variable represents",
            "example_values": ["Example 1", "Example 2", "Example 3"],
            "data_source_suggestions": ["Where to get this data"]
        }}
    ],
    "content_strategy": {{
        "primary_value": "Main value this page provides to users",
        "content_sections": ["Section 1", "Section 2", "Section 3"],
        "unique_angle": "What makes this content different from competitors",
        "user_action_goal": "What we want users to do after reading"
    }},
    "seo_strategy": {{
        "primary_keyword_pattern": "Main keyword pattern",
        "secondary_keywords": ["Related keyword 1", "Related keyword 2"],
        "meta_description_template": "Template for meta descriptions",
        "internal_linking_opportunities": ["How to link between pages"]
    }},
    "scale_estimate": {{
        "variables_count": "How many values per variable",
        "total_page_potential": "Total pages possible",
        "priority_level": "High/Medium/Low based on opportunity"
    }}
}}

Make this template specific to the business and valuable to users.
"""
```

### Data Strategy Creation (Lines 332-376)
```python
prompt = f"""
Create a comprehensive data strategy for these programmatic SEO templates.

Business: {business_intelligence.get("business_core", {}).get("name", "Unknown")}

Template Variables Needed:
{json.dumps(all_variables, indent=2)}

Create a data strategy in JSON format:

{{
    "data_collection_plan": [
        {{
            "variable_name": "Variable name",
            "data_sources": ["Source 1", "Source 2"],
            "collection_method": "How to collect this data",
            "data_quality_requirements": "What makes good vs bad data",
            "update_frequency": "How often to refresh this data",
            "estimated_values": "How many values we can collect"
        }}
    ],
    "data_validation_rules": [
        {{
            "variable": "Variable name",
            "validation_rules": ["Rule 1", "Rule 2"],
            "quality_thresholds": "Minimum quality requirements"
        }}
    ],
    "data_combination_strategy": {{
        "optimal_combinations": ["Which variables work best together"],
        "combination_priorities": ["Which combinations to prioritize"],
        "scale_calculations": "Total pages possible with full data"
    }},
    "implementation_phases": [
        {{
            "phase": "Phase 1",
            "data_to_collect": ["Priority data sets"],
            "estimated_timeline": "Time to collect",
            "page_generation_potential": "Pages possible with this phase"
        }}
    ]
}}

Focus on data that's realistic to collect and provides genuine user value.
"""
```

### Content Framework Design (Lines 397-433)
```python
prompt = f"""
Design a comprehensive content framework for this programmatic SEO strategy.

Business: {business_intelligence.get("business_core", {}).get("name", "Unknown")}
Industry: {business_intelligence.get("business_core", {}).get("industry", "Unknown")}

Templates Created: {len(custom_templates)}

Create a content framework in JSON format:

{{
    "content_pillars": [
        {{
            "pillar_name": "Main content theme",
            "supporting_templates": ["Which templates support this pillar"],
            "seo_value": "Why this pillar is valuable for SEO",
            "user_value": "Why users care about this content"
        }}
    ],
    "internal_linking_strategy": {{
        "hub_pages": ["Central pages that link to many others"],
        "spoke_pages": ["Specific pages that link back to hubs"],
        "linking_patterns": ["How pages should link to each other"]
    }},
    "content_quality_standards": {{
        "minimum_word_count": "Minimum words per page",
        "unique_content_percentage": "How much content must be unique",
        "value_requirements": ["What makes content valuable"],
        "update_requirements": "How often to update content"
    }},
    "scalability_architecture": {{
        "content_generation_pipeline": "How to efficiently generate content",
        "quality_assurance_process": "How to maintain quality at scale",
        "performance_monitoring": "How to track content performance"
    }}
}}
"""
```

## 5. api/ai_handler.py

### Business Analysis (Lines 158-173)
```python
prompt = f"""Analyze this business and suggest SEO content opportunities:
Business: {business_info.get('name', 'Unknown')}
Description: {business_info.get('description', 'No description')}
URL: {business_info.get('url', 'No URL')}
Page Content: {business_info.get('page_content', 'No content available')[:300]}
Target Audience Type: {business_info.get('target_audience_type', 'Not specified')}

Provide a JSON response with:
1. industry (string - be specific about the business type)
2. target_audience (string - detailed description)
3. content_types (array of 5 content type suggestions like guides, comparisons, calculators)
4. main_keywords (array of 5 primary terms)
5. services (array of 3-5 main services/products)
6. customer_actions (array of common actions like buy, book, learn)
7. competitors (array of 2-3 competitor examples)
"""
```

### Business Intelligence Extraction (Lines 211-249)
```python
prompt = f"""
Act as an expert business analyst. Analyze this business deeply to understand what they do, who they serve, and how they create value.

Business Information:
- Name: {business_info.get('name', 'Unknown')}
- Industry: {business_info.get('industry', 'Unknown')}
- Description: {business_info.get('description', 'No description')}
- URL: {business_info.get('url', 'No URL')}
- Page Content: {business_info.get('page_content', 'No content available')[:500]}

Provide a comprehensive business intelligence analysis:

1. CORE BUSINESS MODEL:
   - What exactly does this business do?
   - How do they make money?
   - What's their unique value proposition?

2. TARGET CUSTOMERS:
   - Who are their primary customers? (be specific - titles, industries, demographics)
   - What customer segments do they serve?
   - What problems do customers have before finding this business?

3. CUSTOMER JOURNEY:
   - How do customers discover they need this solution?
   - What's the typical buyer journey?
   - What information do they need at each stage?

4. COMPETITIVE LANDSCAPE:
   - Who are their main competitors?
   - What makes this business different?
   - What competitive advantages do they have?

5. KEY FEATURES & SOLUTIONS:
   - What are their main products/services?
   - What tools or features do they offer?
   - What outcomes do customers achieve?

Be thorough and analytical. Think like a business consultant who needs to understand every aspect of this company.
"""
```

### Customer Search Behavior Analysis (Lines 263-295)
```python
prompt = f"""
Based on this business intelligence, analyze what their potential customers would actually search for online.

Business Intelligence:
{business_intelligence}

Market Context: {additional_context}

Analyze customer search behavior:

1. SEARCH INTENT MAPPING:
   - What would customers search for when they don't know this business exists?
   - What problems would they type into Google?
   - What information are they seeking at different stages?

2. SEARCH JOURNEY STAGES:
   - Problem Awareness: What searches indicate they have a problem?
   - Solution Research: What do they search when looking for solutions?
   - Vendor Evaluation: What searches help them compare options?
   - Implementation: What do they search when ready to use a solution?

3. GEOGRAPHICAL CONSIDERATIONS:
   - How does location affect their search behavior?
   - What location-specific terms would they use?
   - How does market context influence search patterns?

4. INDUSTRY-SPECIFIC SEARCH PATTERNS:
   - What jargon or technical terms do they use?
   - What questions are common in their industry?
   - What tools or resources do they typically search for?

Think like a customer who has never heard of this business. What would you search for?
"""
```

### Content Opportunities Discovery (Lines 309-357)
```python
prompt = f"""
Create a comprehensive programmatic SEO strategy like ChatGPT's real estate example. Follow this exact structure:

Business Intelligence:
{business_intelligence}

Customer Search Behavior:
{customer_analysis}

Market Context: {additional_context}

Create a complete programmatic SEO strategy following this format:

## 🔑 CORE KEYWORD FORMULAS
Identify 3-5 keyword formulas that can scale. Format like:
[Variable1] [Variable2] [Core Topic]
[Location] [Product/Service] [Intent Modifier]

## 🔁 KEYWORD COMPONENTS TO MIX & MATCH

### 🏙️ Location Modifiers:
- List 15-25 relevant locations (cities, regions, countries based on market context)

### 🏢 Business-Specific Categories:
- List 8-12 product/service types this business offers
- Be specific to their industry and offerings

### 📊 Intent/Topic Modifiers:
- List 10-15 customer intent variations
- Include tools, comparisons, guides, calculators
- Focus on high-commercial intent terms

## 🧱 PROGRAMMATIC PAGE EXAMPLES
Create 6-8 specific page examples with:
- Page Title
- URL Slug  
- Target Keyword
- Brief description of page purpose

## 🛠️ TECHNICAL PROGRAMMATIC SETUP
Calculate potential pages:
- X locations × Y categories × Z intent modifiers = Total pages
- Suggest optimal combinations for maximum coverage

## 📚 PILLAR PAGES (Non-programmatic but high-value)
Suggest 4-5 pillar pages that build topical authority

Make this specific to the analyzed business and market context. Think like ChatGPT's real estate example but adapted to this business type.
"""
```

### Content Generation (Lines 418-436)
```python
prompt = f"""Write comprehensive SEO-optimized content for:
Keyword: {keyword}
Business: {business_info.get('name', 'Unknown')}
Industry: {business_info.get('industry', 'General')}
Target Audience: {business_info.get('target_audience', 'General audience')}

Requirements:
1. Compelling, unique title (not generic)
2. Meta description (150-160 chars, include keyword naturally)
3. Introduction paragraph (150-200 words, engage reader immediately)
4. Main content sections with detailed information
5. Include data, statistics, or examples where relevant
6. Natural keyword usage (2-3% density)
7. Actionable advice and practical tips

{f"Use this structure: {structure['structure']}" if structure else ""}
Target word count: {structure.get('word_count_target', 1500) if structure else 1500} words

Format as JSON with keys: title, meta_description, intro, content_sections, outline"""
```

## 6. agents/page_generator.py

### Content Section Generation (Lines 567-583)
```python
prompt = f"""Generate SEO-optimized content for this section:

Heading: {section_template.get('heading', '')}
Content Type: {content_type}
Template: {template_content}
Variables: {json.dumps(data, indent=2)}
{business_context}

Requirements:
- Write in a {content_type} tone
- Include relevant keywords naturally
- Keep paragraphs short and scannable
- Use bullet points where appropriate
- Be specific and valuable to the reader
- Approximately 150-250 words

Generate the content:"""
```

### Statistics Section (Lines 638-643)
```python
stats_prompt = f"""Generate relevant statistics for: {page['seo']['h1']}

Create 4-5 compelling statistics with percentages or numbers that would be relevant.
Format as a bullet list.
Make them specific to the topic and industry.
Keep it under 100 words."""
```

### Comparison Table (Lines 656-659)
```python
comparison_prompt = f"""Create a comparison table for: {page['seo']['h1']}

Format as markdown table with 3-4 key comparison points.
Keep it concise and scannable."""
```

### FAQ Section (Lines 677-683)
```python
faq_prompt = f"""Generate 3 frequently asked questions about: {page['seo']['h1']}

Format as:
**Q: [Question]**
A: [Brief answer in 2-3 sentences]

Make questions specific and answers helpful."""
```

### Case Study (Lines 695-702)
```python
case_prompt = f"""Create a brief success story example for: {page['seo']['h1']}

Include:
- Brief scenario (2 sentences)
- Key results with numbers
- Main takeaway

Keep it under 100 words and make it believable."""
```

### Local Context (Lines 721-724)
```python
local_prompt = f"""Add local context for {location}:

Include 2-3 specific local details that make this content unique to {location}.
Keep it brief and relevant."""
```

## Summary

This documentation covers all AI prompts found in the backend code. The prompts are used for:

1. **Business Analysis**: Understanding businesses and their SEO opportunities
2. **Strategy Generation**: Creating custom programmatic SEO strategies
3. **Content Generation**: Writing unique, data-driven content at scale
4. **Variable Generation**: Creating relevant values for template variables
5. **Page Enhancement**: Adding unique elements like statistics, FAQs, and local context

Each prompt is carefully crafted to generate specific, valuable content that serves real user search intent while maintaining quality at scale.