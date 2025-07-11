"""Simple AI client for Perplexity API"""
import os
import requests
from typing import Dict, Any
from dotenv import load_dotenv
from urllib.parse import urlparse

load_dotenv()

class AIClient:
    def __init__(self):
        self.api_key = os.getenv('PERPLEXITY_API_KEY')
        self.base_url = "https://api.perplexity.ai"
        
    def analyze_business(self, business_input: str) -> Dict[str, Any]:
        """Use Perplexity to analyze a business for programmatic SEO opportunities"""
        
        print(f"Analyzing business: {business_input[:50]}...")
        print(f"API Key present: {bool(self.api_key)}")
        
        # Check if input is a URL
        is_url = business_input.startswith(('http://', 'https://'))
        url_content = ""
        
        if is_url:
            # Fetch URL content
            url_content = self._fetch_url_content(business_input)
            print(f"Fetched URL content length: {len(url_content)}")
        
        if not self.api_key:
            # Return enhanced mock data if no API key
            print("No API key, using mock data")
            return self._get_mock_analysis(business_input)
        
        if is_url and url_content:
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
        else:
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
        
        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "sonar",
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.7
                }
            )
            
            if response.status_code == 200:
                # Parse and return the response
                result = response.json()
                print(f"API Response: {result}")
                # Extract the actual content from Perplexity response
                # This will need adjustment based on actual Perplexity response format
                return self._parse_ai_response(result)
            else:
                print(f"API Error: {response.status_code} - {response.text}")
                return self._get_mock_analysis(business_input)
                
        except Exception as e:
            print(f"AI API error: {e}")
            return self._get_mock_analysis(business_input)
    
    def _fetch_url_content(self, url: str) -> str:
        """Fetch and extract text content from a URL"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            # Simple text extraction from HTML
            from html.parser import HTMLParser
            
            class TextExtractor(HTMLParser):
                def __init__(self):
                    super().__init__()
                    self.text = []
                    self.skip_tags = {'script', 'style', 'meta', 'link'}
                    self.current_tag = None
                
                def handle_starttag(self, tag, attrs):
                    self.current_tag = tag
                
                def handle_endtag(self, tag):
                    self.current_tag = None
                
                def handle_data(self, data):
                    if self.current_tag not in self.skip_tags:
                        text = data.strip()
                        if text:
                            self.text.append(text)
            
            parser = TextExtractor()
            parser.feed(response.text)
            
            # Join and clean up the text
            content = ' '.join(parser.text)
            # Remove extra whitespace
            content = ' '.join(content.split())
            
            return content[:3000]  # Limit content length
            
        except Exception as e:
            print(f"Error fetching URL content: {e}")
            return ""
    
    def _parse_ai_response(self, response: Dict) -> Dict[str, Any]:
        """Parse Perplexity response into our format"""
        try:
            # Get the AI response content
            content = response.get('choices', [{}])[0].get('message', {}).get('content', '')
            
            # Try to parse JSON from the response
            import json
            import re
            
            # Extract JSON from markdown code block
            json_match = re.search(r'```json\s*(.*?)\s*```', content, re.DOTALL)
            if json_match:
                json_str = json_match.group(1)
            else:
                # Try to extract raw JSON
                json_match = re.search(r'\{.*\}', content, re.DOTALL)
                if json_match:
                    json_str = json_match.group()
                else:
                    return self._get_mock_analysis("Failed to find JSON in response")
            
            # Parse the JSON
            parsed = json.loads(json_str)
            
            # Map Perplexity response to our format
            template_opportunities = []
            templates = parsed.get('template_opportunities', parsed.get('programmatic_seo_templates', []))
            for template in templates:
                template_opportunities.append({
                    "template_name": template.get('template_name', ''),
                    "template_pattern": template.get('template_pattern', template.get('pattern', '')),
                    "example_pages": template.get('example_pages', []),
                    "estimated_pages": template.get('estimated_pages', template.get('estimated_number_of_pages', 50)),
                    "difficulty": template.get('difficulty', template.get('difficulty_level', 'Medium'))
                })
            
            return {
                "business_name": parsed.get('business_name', 'Unknown Business'),
                "business_description": parsed.get('description', parsed.get('business_description', '')),
                "target_audience": ', '.join(parsed.get('target_audience', [])) if isinstance(parsed.get('target_audience'), list) else parsed.get('target_audience', ''),
                "core_offerings": parsed.get('core_offerings', []),
                "template_opportunities": template_opportunities
            }
            
        except Exception as e:
            print(f"Error parsing AI response: {e}")
            import traceback
            traceback.print_exc()
            return self._get_mock_analysis("AI parsing failed")
    
    async def generate(self, prompt: str, temperature: float = 0.7, max_tokens: int = 1000) -> str:
        """Generate text using Perplexity AI for variable generation and other tasks"""
        
        print(f"Generating with prompt: {prompt[:100]}...")
        print(f"API Key present: {bool(self.api_key)}")
        
        if not self.api_key:
            # Return mock data if no API key
            print("No API key, using mock data")
            return self._get_mock_generation(prompt)
        
        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "sonar",
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": temperature,
                    "max_tokens": max_tokens
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"API Response: {result}")
                # Extract the actual content from Perplexity response
                content = result.get('choices', [{}])[0].get('message', {}).get('content', '')
                return content
            else:
                print(f"API Error: {response.status_code} - {response.text}")
                return self._get_mock_generation(prompt)
                
        except Exception as e:
            print(f"AI API error: {e}")
            return self._get_mock_generation(prompt)
    
    def _get_mock_generation(self, prompt: str) -> str:
        """Return mock generation for testing"""
        prompt_lower = prompt.lower()
        
        if 'city' in prompt_lower or 'location' in prompt_lower:
            return '''["Toronto", "Vancouver", "Calgary", "Ottawa", "Montreal", "Edmonton", "Winnipeg", "Quebec City", "Hamilton", "London"]'''
        elif 'service' in prompt_lower:
            return '''["Digital Marketing", "Web Development", "SEO Consulting", "Social Media Management", "Content Creation", "Graphic Design", "Email Marketing", "PPC Advertising", "Brand Strategy", "Analytics"]'''
        elif 'product' in prompt_lower:
            return '''["Analytics Dashboard", "CRM Software", "Project Management Tool", "Marketing Automation", "Customer Support Platform", "Sales Pipeline", "Reporting System", "Data Visualization", "Lead Generation", "Conversion Tracking"]'''
        elif 'industry' in prompt_lower:
            return '''["Real Estate", "Healthcare", "Technology", "Finance", "Education", "Retail", "Manufacturing", "Hospitality", "Legal Services", "Consulting"]'''
        else:
            # Generic fallback
            return '''["Option 1", "Option 2", "Option 3", "Option 4", "Option 5", "Option 6", "Option 7", "Option 8", "Option 9", "Option 10"]'''
    
    def _get_mock_analysis(self, business_input: str) -> Dict[str, Any]:
        """Return mock analysis for testing"""
        # Enhanced mock data based on input
        business_lower = business_input.lower()
        
        if "real estate" in business_lower and ("analysis" in business_lower or "tool" in business_lower):
            return {
                "business_name": "Canadian Real Estate Analytics",
                "business_description": "SaaS platform providing comprehensive real estate analysis tools for Canadian realtors",
                "target_audience": "Canadian real estate agents and brokers",
                "core_offerings": [
                    "Market analysis reports",
                    "Property valuation tools",
                    "Neighborhood insights",
                    "Investment calculators"
                ],
                "template_opportunities": [
                    {
                        "template_name": "City Real Estate Market Analysis",
                        "template_pattern": "[City] Real Estate Market Report [Year]",
                        "example_pages": [
                            "Toronto Real Estate Market Report 2025",
                            "Vancouver Real Estate Market Report 2025",
                            "Calgary Real Estate Market Report 2025"
                        ],
                        "estimated_pages": 150,
                        "difficulty": "Easy"
                    },
                    {
                        "template_name": "Neighborhood Guides",
                        "template_pattern": "[Neighborhood], [City] Real Estate Guide",
                        "example_pages": [
                            "Yorkville, Toronto Real Estate Guide",
                            "Kitsilano, Vancouver Real Estate Guide",
                            "Beltline, Calgary Real Estate Guide"
                        ],
                        "estimated_pages": 500,
                        "difficulty": "Medium"
                    },
                    {
                        "template_name": "Property Type Analysis",
                        "template_pattern": "[Property Type] in [City] - Investment Analysis",
                        "example_pages": [
                            "Condos in Toronto - Investment Analysis",
                            "Townhouses in Vancouver - Investment Analysis",
                            "Single Family Homes in Ottawa - Investment Analysis"
                        ],
                        "estimated_pages": 200,
                        "difficulty": "Easy"
                    }
                ]
            }
        else:
            # Generic business analysis
            return {
                "business_name": "Example Business",
                "business_description": f"A business focused on {business_input[:100]}",
                "target_audience": "Small to medium businesses",
                "core_offerings": [
                    "Core Service 1",
                    "Core Service 2",
                    "Core Service 3"
                ],
                "template_opportunities": [
                    {
                        "template_name": "Location-Based Pages",
                        "template_pattern": "[Service] in [City]",
                        "example_pages": [
                            "Service in Toronto",
                            "Service in Vancouver",
                            "Service in Montreal"
                        ],
                        "estimated_pages": 100,
                        "difficulty": "Easy"
                    }
                ]
            }