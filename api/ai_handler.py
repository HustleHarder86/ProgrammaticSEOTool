"""AI integration for content generation"""
import os
import json
from urllib.request import Request, urlopen
from urllib.error import URLError

# Import content variation engine
try:
    from .content_variation import ContentVariationEngine, enhance_content_quality, ensure_minimum_quality
    variation_engine = ContentVariationEngine()
except:
    variation_engine = None

# Import keyword optimizer
try:
    from .keyword_optimizer import KeywordOptimizer
    keyword_optimizer = KeywordOptimizer()
except:
    keyword_optimizer = None

class AIHandler:
    def __init__(self):
        self.openai_key = os.environ.get('OPENAI_API_KEY')
        self.anthropic_key = os.environ.get('ANTHROPIC_API_KEY')
        self.perplexity_key = os.environ.get('PerplexityAPI')
        
    def has_ai_provider(self):
        """Check if at least one AI provider is configured"""
        return bool(self.openai_key or self.anthropic_key or self.perplexity_key)
    
    def generate_with_openai(self, prompt, max_tokens=500):
        """Generate content using OpenAI API"""
        if not self.openai_key:
            return None
            
        headers = {
            'Authorization': f'Bearer {self.openai_key}',
            'Content-Type': 'application/json'
        }
        
        data = {
            'model': 'gpt-3.5-turbo',
            'messages': [{'role': 'user', 'content': prompt}],
            'max_tokens': max_tokens,
            'temperature': 0.7
        }
        
        try:
            req = Request('https://api.openai.com/v1/chat/completions',
                         data=json.dumps(data).encode(),
                         headers=headers,
                         method='POST')
            
            with urlopen(req, timeout=30) as response:
                result = json.loads(response.read().decode())
                return result['choices'][0]['message']['content']
        except Exception as e:
            print(f"OpenAI error: {e}")
            return None
    
    def generate_with_anthropic(self, prompt, max_tokens=500):
        """Generate content using Anthropic API"""
        if not self.anthropic_key:
            return None
            
        headers = {
            'x-api-key': self.anthropic_key,
            'Content-Type': 'application/json',
            'anthropic-version': '2023-06-01'
        }
        
        data = {
            'model': 'claude-3-haiku-20240307',
            'messages': [{'role': 'user', 'content': prompt}],
            'max_tokens': max_tokens
        }
        
        try:
            req = Request('https://api.anthropic.com/v1/messages',
                         data=json.dumps(data).encode(),
                         headers=headers,
                         method='POST')
            
            with urlopen(req, timeout=30) as response:
                result = json.loads(response.read().decode())
                return result['content'][0]['text']
        except Exception as e:
            print(f"Anthropic error: {e}")
            return None
    
    def generate_with_perplexity(self, prompt, max_tokens=500):
        """Generate content using Perplexity API"""
        if not self.perplexity_key:
            return None
            
        headers = {
            'Authorization': f'Bearer {self.perplexity_key}',
            'Content-Type': 'application/json'
        }
        
        data = {
            'model': 'sonar',  # Simple model name
            'messages': [{'role': 'user', 'content': prompt}],
            'max_tokens': max_tokens,
            'temperature': 0.7
        }
        
        try:
            req = Request('https://api.perplexity.ai/chat/completions',
                         data=json.dumps(data).encode(),
                         headers=headers,
                         method='POST')
            
            with urlopen(req, timeout=30) as response:
                result = json.loads(response.read().decode())
                return result['choices'][0]['message']['content']
        except URLError as e:
            if hasattr(e, 'read'):
                error_body = e.read().decode()
                print(f"Perplexity API error response: {error_body}")
            print(f"Perplexity URL error: {e}")
            return None
        except Exception as e:
            print(f"Perplexity error: {e}")
            return None
    
    def generate(self, prompt, max_tokens=500):
        """Generate content using available AI provider"""
        # Try Perplexity first (good for SEO/web research)
        result = self.generate_with_perplexity(prompt, max_tokens)
        if result:
            return result
            
        # Try OpenAI
        result = self.generate_with_openai(prompt, max_tokens)
        if result:
            return result
            
        # Fall back to Anthropic
        result = self.generate_with_anthropic(prompt, max_tokens)
        if result:
            return result
            
        # No AI provider available or all failed
        return None

    def analyze_business_with_ai(self, business_info):
        """Use AI to analyze business and suggest content types"""
        if not self.has_ai_provider():
            return None
            
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
        
        response = self.generate(prompt, 300)
        if response:
            try:
                # Try to parse JSON from response
                start = response.find('{')
                end = response.rfind('}') + 1
                if start >= 0 and end > start:
                    return json.loads(response[start:end])
            except:
                pass
        return None
    
    def analyze_business_comprehensive(self, business_info, market_context=None):
        """Comprehensive business analysis following human SEO expert approach"""
        if not self.has_ai_provider():
            return None
        
        # Phase 1: Deep Business Understanding
        business_intelligence = self._extract_business_intelligence(business_info)
        
        # Phase 2: Customer Search Behavior Analysis  
        customer_analysis = self._analyze_customer_search_behavior(business_intelligence, market_context)
        
        # Phase 3: Content Opportunity Discovery
        content_opportunities = self._discover_content_opportunities(business_intelligence, customer_analysis, market_context)
        
        return {
            'business_intelligence': business_intelligence,
            'customer_analysis': customer_analysis,
            'content_opportunities': content_opportunities,
            'comprehensive_analysis': True
        }
    
    def _extract_business_intelligence(self, business_info):
        """Phase 1: Deep business understanding like a human SEO expert"""
        
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
        
        try:
            response = self.generate(prompt, 800)
            return response if response else "Business analysis unavailable"
        except Exception as e:
            print(f"Error in business intelligence extraction: {e}")
            return "Business analysis unavailable"
    
    def _analyze_customer_search_behavior(self, business_intelligence, market_context):
        """Phase 2: Understand what customers would actually search for"""
        
        additional_context = market_context.get('additional_context', '') if market_context else ''
        
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
        
        try:
            response = self.generate(prompt, 800)
            return response if response else "Customer analysis unavailable"
        except Exception as e:
            print(f"Error in customer search analysis: {e}")
            return "Customer analysis unavailable"
    
    def _discover_content_opportunities(self, business_intelligence, customer_analysis, market_context):
        """Phase 3: Identify specific content types that would rank and convert - ChatGPT style"""
        
        additional_context = market_context.get('additional_context', '') if market_context else ''
        
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
        
        try:
            response = self.generate(prompt, 1000)
            return response if response else "Content opportunity analysis unavailable"
        except Exception as e:
            print(f"Error in content opportunity discovery: {e}")
            return "Content opportunity analysis unavailable"

    def generate_keywords_with_ai(self, business_info, num_keywords=10):
        """Use AI to generate keyword suggestions"""
        industry = business_info.get('industry', 'General').lower()
        
        # Use specialized keyword generation for supported industries
        if keyword_optimizer and 'real estate' in industry:
            # Generate comprehensive real estate keywords
            keyword_objects = keyword_optimizer.generate_real_estate_keywords(business_info, num_keywords)
            # Return just the keyword strings for backward compatibility
            return [kw['keyword'] for kw in keyword_objects]
        
        if not self.has_ai_provider():
            return None
        
        # Use enhanced prompt from keyword optimizer if available
        if keyword_optimizer:
            prompt = keyword_optimizer.enhance_with_ai_prompt(industry, business_info)
        else:
            # Fallback to original prompt
            prompt = f"""Generate {num_keywords} SEO keyword opportunities for:
Business: {business_info.get('name', 'Unknown')}
Industry: {business_info.get('industry', 'General')}
Target: {business_info.get('target_audience', 'General audience')}

Provide keywords that are:
- Long-tail (3-5 words)
- Have commercial or informational intent
- Realistic for a small business to rank for

Format as a simple list, one per line."""
        
        response = self.generate(prompt, 400)  # Increased token limit
        if response:
            # Parse keywords from response
            keywords = []
            for line in response.strip().split('\n'):
                line = line.strip().strip('-').strip('•').strip('*').strip('1234567890.').strip()
                if line and len(line) > 5 and not line.lower().startswith(('generate', 'keyword', 'note:')):
                    keywords.append(line)
            return keywords[:num_keywords]
        return None

    def generate_content_with_ai(self, keyword, business_info, ensure_unique=True):
        """Use AI to generate content for a keyword with uniqueness"""
        if not self.has_ai_provider():
            return None
        
        # Get unique structure if variation engine available
        structure = None
        if variation_engine and ensure_unique:
            structure = variation_engine.generate_unique_structure(keyword, "general")
            
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
        
        response = self.generate(prompt, 1000)
        if response:
            try:
                # Parse JSON response
                start = response.find('{')
                end = response.rfind('}') + 1
                if start >= 0 and end > start:
                    content_data = json.loads(response[start:end])
                    
                    # Apply variations if available
                    if variation_engine and ensure_unique:
                        # Generate full content from sections
                        full_content = content_data.get('intro', '')
                        sections = content_data.get('content_sections', [])
                        
                        if isinstance(sections, list):
                            for section in sections:
                                if isinstance(section, dict):
                                    full_content += f"\n\n## {section.get('title', '')}\n{section.get('content', '')}"
                                else:
                                    full_content += f"\n\n{section}"
                        
                        # Apply variations
                        variations = variation_engine.vary_content(full_content, keyword, 1)
                        if variations:
                            content_data['content'] = variations[0]['content']
                        
                        # Enhance quality
                        if enhance_content_quality:
                            content_data['content'] = enhance_content_quality(
                                content_data.get('content', full_content),
                                keyword,
                                business_info
                            )
                        
                        # Add unique elements
                        content_data['unique_elements'] = structure.get('unique_elements', [])
                    
                    return content_data
            except Exception as e:
                print(f"Content generation error: {e}")
                
        # Fallback response
        return {
            'title': f"{keyword.title()} - Expert Guide for {business_info.get('industry', 'Your Industry')}",
            'meta_description': f"Discover expert insights on {keyword}. Comprehensive guide with practical tips and strategies.",
            'intro': f"Looking for information about {keyword}? This comprehensive guide provides expert insights tailored for {business_info.get('target_audience', 'professionals')}.",
            'outline': ["Introduction", "Key Concepts", "Implementation Guide", "Best Practices", "Common Challenges", "Conclusion"],
            'content': "Content generation in progress..."
        }