"""Keyword strategy generator for programmatic SEO campaigns."""
import logging
from typing import List, Dict, Optional
from scanners.base import BusinessInfo
from utils.ai_client import AIClient
from config import settings
import json

logger = logging.getLogger(__name__)

class KeywordStrategy:
    """Represents a keyword strategy for programmatic SEO."""
    def __init__(self, name: str, template: str, description: str, 
                 estimated_pages: int, icon: str, examples: List[str],
                 variables: List[str], priority: int = 5):
        self.name = name
        self.template = template
        self.description = description
        self.estimated_pages = estimated_pages
        self.icon = icon
        self.examples = examples
        self.variables = variables
        self.priority = priority

    def to_dict(self) -> Dict:
        return {
            'name': self.name,
            'template': self.template,
            'description': self.description,
            'estimated_pages': self.estimated_pages,
            'icon': self.icon,
            'examples': self.examples,
            'variables': self.variables,
            'priority': self.priority
        }

class StrategyGenerator:
    """Generates intelligent keyword strategies based on business analysis."""
    
    def __init__(self):
        self.ai_client = AIClient()
    
    async def generate_strategies(self, business_info: BusinessInfo) -> List[KeywordStrategy]:
        """Generate keyword strategies specific to the business."""
        prompt = f"""Based on this business analysis, generate 5-10 specific programmatic SEO strategies.

Business Information:
- Industry: {business_info.industry}
- Services: {', '.join(business_info.services[:5])}
- Products: {', '.join(business_info.products[:5])}
- Location: {business_info.location or 'Multiple locations'}
- Target Audience: {', '.join(business_info.target_audience[:3])}
- Keywords: {', '.join(business_info.keywords[:10])}

Generate keyword strategies that could create many pages at scale. Each strategy should have:
- name: A clear, specific name for this strategy
- template: The URL pattern template (e.g., "{{city}}-real-estate-market-analysis")
- description: What pages this strategy creates and why they're valuable
- estimated_pages: Realistic estimate of how many pages could be created
- icon: An emoji that represents this strategy
- examples: 3-4 example URLs this would generate
- variables: The template variables used (e.g., ["city", "state"])
- priority: 1-10 score based on SEO potential

Focus on strategies that:
1. Target specific search intents
2. Can scale to hundreds or thousands of pages
3. Match the business's expertise
4. Have clear commercial value
5. Target different stages of the customer journey

Return as a JSON array."""

        try:
            content = await self.ai_client.generate(
                prompt=prompt,
                temperature=0.7,
                max_tokens=2000
            )
            
            # Parse response
            strategies_data = json.loads(content)
            
            # Convert to KeywordStrategy objects
            strategies = []
            for data in strategies_data:
                strategy = KeywordStrategy(
                    name=data['name'],
                    template=data['template'],
                    description=data['description'],
                    estimated_pages=data['estimated_pages'],
                    icon=data['icon'],
                    examples=data['examples'],
                    variables=data['variables'],
                    priority=data.get('priority', 5)
                )
                strategies.append(strategy)
            
            # Sort by priority
            strategies.sort(key=lambda x: x.priority, reverse=True)
            
            return strategies[:10]  # Return top 10 strategies
            
        except Exception as e:
            logger.error(f"Error generating strategies: {e}")
            # Return fallback strategies
            return self._get_fallback_strategies(business_info)
    
    def _get_fallback_strategies(self, business_info: BusinessInfo) -> List[KeywordStrategy]:
        """Generate fallback strategies if AI generation fails."""
        strategies = []
        
        # Location-based strategy
        if business_info.services:
            strategies.append(KeywordStrategy(
                name=f"{business_info.services[0]} by Location",
                template=f"{{{{city}}}}-{business_info.services[0].lower().replace(' ', '-')}",
                description=f"Create location pages for {business_info.services[0]} services across different cities",
                estimated_pages=500,
                icon="📍",
                examples=[
                    f"austin-{business_info.services[0].lower().replace(' ', '-')}",
                    f"new-york-{business_info.services[0].lower().replace(' ', '-')}",
                    f"chicago-{business_info.services[0].lower().replace(' ', '-')}"
                ],
                variables=["city"],
                priority=8
            ))
        
        # Comparison strategy
        if len(business_info.services) > 1:
            strategies.append(KeywordStrategy(
                name="Service Comparisons",
                template="{service1}-vs-{service2}",
                description="Compare different services to help users make informed decisions",
                estimated_pages=50,
                icon="⚖️",
                examples=[
                    f"{business_info.services[0].lower().replace(' ', '-')}-vs-{business_info.services[1].lower().replace(' ', '-')}",
                ],
                variables=["service1", "service2"],
                priority=7
            ))
        
        # How-to guides
        strategies.append(KeywordStrategy(
            name="How-To Guides",
            template="how-to-{task}-{modifier}",
            description="Step-by-step guides for common tasks and problems",
            estimated_pages=100,
            icon="📚",
            examples=[
                "how-to-choose-best-service",
                "how-to-get-started-guide",
                "how-to-compare-options"
            ],
            variables=["task", "modifier"],
            priority=6
        ))
        
        return strategies

    async def generate_keywords_for_strategy(self, strategy: KeywordStrategy, 
                                           business_info: BusinessInfo,
                                           limit: int = 50) -> List[Dict]:
        """Generate actual keywords for a specific strategy."""
        prompt = f"""Generate {limit} specific keyword variations for this programmatic SEO strategy:

Strategy: {strategy.name}
Template: {strategy.template}
Variables: {', '.join(strategy.variables)}
Business: {business_info.industry}

Generate actual keyword combinations that:
1. Fill in the template variables with real values
2. Target high-intent searches
3. Have commercial value
4. Are likely to rank well

For each keyword provide:
- keyword: The full keyword phrase
- url_slug: The URL-friendly version
- title: A compelling page title
- search_volume_estimate: low/medium/high
- competition: low/medium/high
- intent: informational/commercial/transactional

Return as JSON array."""

        try:
            content = await self.ai_client.generate(
                prompt=prompt,
                temperature=0.8,
                max_tokens=2000
            )
            
            keywords_data = json.loads(content)
            
            # Add strategy information to each keyword
            for kw in keywords_data:
                kw['strategy_name'] = strategy.name
                kw['strategy_template'] = strategy.template
            
            return keywords_data[:limit]
            
        except Exception as e:
            logger.error(f"Error generating keywords for strategy: {e}")
            return []