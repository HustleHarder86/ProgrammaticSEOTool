"""Text-based business analyzer using AI."""
import json
import logging
from typing import List, Dict, Optional
from app.scanners.base import BusinessAnalyzer, BusinessInfo, ContentOpportunity
from config import settings

logger = logging.getLogger(__name__)

class TextBusinessAnalyzer(BusinessAnalyzer):
    """Analyzes business descriptions using AI."""
    
    def __init__(self):
        self.ai_client = self._setup_ai_client()
    
    def _setup_ai_client(self):
        """Set up the AI client based on available API keys."""
        if settings.has_openai:
            from openai import OpenAI
            return OpenAI(api_key=settings.openai_api_key)
        elif settings.has_anthropic:
            from anthropic import Anthropic
            return Anthropic(api_key=settings.anthropic_api_key)
        else:
            raise ValueError("No AI provider configured")
    
    async def analyze(self, business_description: str) -> BusinessInfo:
        """Extract structured business information from text description."""
        prompt = f"""Analyze this business description and extract structured information.
        
Business Description: {business_description}

Extract the following information in JSON format:
- name: Business name if mentioned
- description: Brief summary of the business
- services: List of services offered
- products: List of products sold
- industry: Primary industry/niche
- location: Location if mentioned (city, state, country)
- target_audience: List of target customer segments
- unique_selling_points: Key differentiators
- keywords: Important keywords and phrases for SEO

Respond with valid JSON only."""

        try:
            if settings.has_openai:
                response = self.ai_client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.3
                )
                content = response.choices[0].message.content
            else:  # Anthropic
                response = self.ai_client.messages.create(
                    model="claude-3-haiku-20240307",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.3,
                    max_tokens=1000
                )
                content = response.content[0].text
            
            # Parse JSON response
            data = json.loads(content)
            
            # Create BusinessInfo object
            business_info = BusinessInfo(
                name=data.get("name"),
                description=data.get("description", business_description[:200]),
                services=data.get("services", []),
                products=data.get("products", []),
                industry=data.get("industry"),
                location=data.get("location"),
                target_audience=data.get("target_audience", []),
                unique_selling_points=data.get("unique_selling_points", []),
                keywords=data.get("keywords", [])
            )
            
            logger.info(f"Successfully analyzed business: {business_info.industry}")
            return business_info
            
        except Exception as e:
            logger.error(f"Error analyzing business description: {e}")
            # Return basic info on error
            return BusinessInfo(
                description=business_description[:200],
                keywords=business_description.lower().split()[:10]
            )
    
    async def identify_opportunities(self, business_info: BusinessInfo) -> List[ContentOpportunity]:
        """Generate content opportunities from business information."""
        opportunities = []
        
        # Service-based opportunities
        for service in business_info.services[:5]:  # Limit to top 5 services
            # How-to guide
            opportunities.append(ContentOpportunity(
                keyword=f"how to {service.lower()}",
                content_type="how-to",
                priority=8,
                title_template=f"How to {{location}} - Complete Guide",
                description=f"Step-by-step guide for {service}"
            ))
            
            # Best X for Y
            if business_info.target_audience:
                for audience in business_info.target_audience[:3]:
                    opportunities.append(ContentOpportunity(
                        keyword=f"best {service.lower()} for {audience.lower()}",
                        content_type="best-x-for-y",
                        priority=7,
                        title_template=f"Best {{service}} for {{audience}} in 2024",
                        description=f"Curated list of {service} options for {audience}"
                    ))
        
        # Location-based opportunities
        if business_info.location:
            for service in business_info.services[:3]:
                opportunities.append(ContentOpportunity(
                    keyword=f"{service.lower()} {business_info.location.lower()}",
                    content_type="location-based",
                    priority=9,
                    title_template=f"{{service}} in {{location}} - Find the Best Options",
                    description=f"Local {service} services in {business_info.location}"
                ))
        
        # Comparison opportunities
        if len(business_info.services) > 1:
            for i in range(min(3, len(business_info.services) - 1)):
                opportunities.append(ContentOpportunity(
                    keyword=f"{business_info.services[i].lower()} vs {business_info.services[i+1].lower()}",
                    content_type="comparison",
                    priority=6,
                    title_template=f"{{option1}} vs {{option2}}: Which is Right for You?",
                    description=f"Detailed comparison of {business_info.services[i]} and {business_info.services[i+1]}"
                ))
        
        # Industry-specific opportunities
        if business_info.industry:
            opportunities.append(ContentOpportunity(
                keyword=f"{business_info.industry.lower()} guide",
                content_type="ultimate-guide",
                priority=7,
                title_template=f"Ultimate Guide to {{industry}} in 2024",
                description=f"Comprehensive guide to {business_info.industry}"
            ))
        
        # Sort by priority
        opportunities.sort(key=lambda x: x.priority, reverse=True)
        
        return opportunities[:50]  # Return top 50 opportunities