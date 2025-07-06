"""Simple AI client for Perplexity API"""
import os
import requests
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()

class AIClient:
    def __init__(self):
        self.api_key = os.getenv('PERPLEXITY_API_KEY')
        self.base_url = "https://api.perplexity.ai"
        
    def analyze_business(self, business_input: str) -> Dict[str, Any]:
        """Use Perplexity to analyze a business for programmatic SEO opportunities"""
        
        if not self.api_key:
            # Return enhanced mock data if no API key
            return self._get_mock_analysis(business_input)
        
        prompt = f"""
        Analyze this business for programmatic SEO opportunities: {business_input}
        
        Provide:
        1. Business name and description
        2. Target audience
        3. Core offerings (3-5 main products/services)
        4. Template opportunities for programmatic SEO with:
           - Template name
           - Pattern (e.g., [Service] in [City])
           - 3 example pages
           - Estimated number of pages possible
           - Difficulty level (Easy/Medium/Hard)
        
        Focus on templates that could generate 50+ pages.
        Format as JSON.
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
                # Extract the actual content from Perplexity response
                # This will need adjustment based on actual Perplexity response format
                return self._parse_ai_response(result)
            else:
                return self._get_mock_analysis(business_input)
                
        except Exception as e:
            print(f"AI API error: {e}")
            return self._get_mock_analysis(business_input)
    
    def _parse_ai_response(self, response: Dict) -> Dict[str, Any]:
        """Parse Perplexity response into our format"""
        # This is a placeholder - adjust based on actual Perplexity response
        return self._get_mock_analysis("AI-enhanced analysis")
    
    def _get_mock_analysis(self, business_input: str) -> Dict[str, Any]:
        """Return mock analysis for testing"""
        # Enhanced mock data based on input
        if "real estate" in business_input.lower():
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