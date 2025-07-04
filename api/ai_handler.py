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