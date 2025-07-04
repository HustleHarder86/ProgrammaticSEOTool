"""Keyword research and expansion module."""
import logging
from typing import List, Dict, Optional
from app.scanners.base import BusinessInfo, ContentOpportunity
from app.agents.seo_data_agent import SEODataAgent
from config import settings

logger = logging.getLogger(__name__)

class KeywordResearcher:
    """Handles keyword research and expansion."""
    
    def __init__(self):
        self.ai_client = self._setup_ai_client()
        self.seo_agent = SEODataAgent()
    
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
    
    async def expand_keywords(self, opportunities: List[ContentOpportunity], business_info: BusinessInfo) -> List[Dict]:
        """Expand content opportunities into detailed keyword sets."""
        expanded_keywords = []
        
        for opp in opportunities[:30]:  # Process top 30 opportunities
            # Generate variations
            variations = await self._generate_keyword_variations(opp, business_info)
            
            # Get real SEO data for each variation
            for var in variations:
                # Fetch real keyword data
                seo_data = await self.seo_agent.get_keyword_data(
                    var['keyword'], 
                    location=business_info.location
                )
                
                expanded_keywords.append({
                    'keyword': var['keyword'],
                    'content_type': opp.content_type,
                    'priority': opp.priority,
                    'title_template': var.get('title_template', opp.title_template),
                    'search_intent': var.get('search_intent', 'informational'),
                    'search_volume': seo_data.get('search_volume', 0),
                    'difficulty': seo_data.get('difficulty', var.get('difficulty', 5)),
                    'cpc': seo_data.get('cpc', 0),
                    'competition': seo_data.get('competition', 0),
                    'topic_cluster': var.get('topic_cluster', 'general'),
                    'data_source': seo_data.get('source', 'ai_estimate')
                })
        
        # Sort by search volume and priority
        expanded_keywords.sort(key=lambda x: (x['search_volume'], x['priority']), reverse=True)
        
        return expanded_keywords
    
    async def _generate_keyword_variations(self, opportunity: ContentOpportunity, business_info: BusinessInfo) -> List[Dict]:
        """Generate keyword variations for a content opportunity."""
        prompt = f"""Generate keyword variations for this content opportunity:
        
Base Keyword: {opportunity.keyword}
Content Type: {opportunity.content_type}
Business: {business_info.industry} in {business_info.location or 'multiple locations'}
Services: {', '.join(business_info.services[:5])}

Generate 3-5 keyword variations that:
1. Target different search intents (informational, commercial, transactional)
2. Include long-tail variations
3. Consider local search if applicable
4. Include question-based queries

Format as JSON array with: keyword, search_intent, difficulty (1-10), title_template"""

        try:
            if settings.has_openai:
                response = self.ai_client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7
                )
                content = response.choices[0].message.content
            else:  # Anthropic
                response = self.ai_client.messages.create(
                    model="claude-3-haiku-20240307",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7,
                    max_tokens=500
                )
                content = response.content[0].text
            
            # Parse response
            import json
            variations = json.loads(content)
            return variations[:5]  # Limit to 5 variations
            
        except Exception as e:
            logger.error(f"Error generating keyword variations: {e}")
            # Return original keyword if generation fails
            return [{
                'keyword': opportunity.keyword,
                'search_intent': 'informational',
                'difficulty': 5,
                'title_template': opportunity.title_template
            }]
    
    async def cluster_keywords(self, keywords: List[Dict]) -> Dict[str, List[Dict]]:
        """Group keywords into topic clusters."""
        clusters = {}
        
        # Simple clustering by content type and topic
        for kw in keywords:
            cluster_key = f"{kw['content_type']}_{kw.get('topic_cluster', 'general')}"
            if cluster_key not in clusters:
                clusters[cluster_key] = []
            clusters[cluster_key].append(kw)
        
        return clusters
    
    async def discover_new_keywords(self, seed_keywords: List[str], limit: int = 100) -> List[Dict]:
        """Discover new keyword opportunities from seed keywords."""
        all_keywords = []
        
        for seed in seed_keywords[:10]:  # Limit to 10 seed keywords
            discovered = await self.seo_agent.discover_related_keywords(seed, limit=20)
            
            for kw_data in discovered:
                all_keywords.append({
                    'keyword': kw_data['keyword'],
                    'search_volume': kw_data.get('search_volume', 0),
                    'difficulty': kw_data.get('difficulty', 5),
                    'cpc': kw_data.get('cpc', 0),
                    'competition': kw_data.get('competition', 0),
                    'content_type': self._determine_content_type(kw_data['keyword']),
                    'search_intent': self._determine_search_intent(kw_data['keyword']),
                    'data_source': kw_data.get('source', 'unknown'),
                    'priority': self._calculate_priority(kw_data)
                })
        
        # Remove duplicates and sort by priority
        unique_keywords = {kw['keyword']: kw for kw in all_keywords}.values()
        sorted_keywords = sorted(unique_keywords, key=lambda x: x['priority'], reverse=True)
        
        return list(sorted_keywords)[:limit]
    
    def _determine_content_type(self, keyword: str) -> str:
        """Determine content type based on keyword."""
        keyword_lower = keyword.lower()
        
        if 'vs' in keyword_lower or 'versus' in keyword_lower:
            return 'comparison'
        elif 'how' in keyword_lower:
            return 'how-to'
        elif 'best' in keyword_lower:
            return 'best-x-for-y'
        elif 'review' in keyword_lower:
            return 'review'
        elif 'guide' in keyword_lower:
            return 'guide'
        else:
            return 'informational'
    
    def _determine_search_intent(self, keyword: str) -> str:
        """Determine search intent based on keyword."""
        keyword_lower = keyword.lower()
        
        commercial_terms = ['buy', 'price', 'cost', 'cheap', 'discount', 'deal']
        transactional_terms = ['download', 'get', 'purchase', 'order', 'signup']
        
        if any(term in keyword_lower for term in transactional_terms):
            return 'transactional'
        elif any(term in keyword_lower for term in commercial_terms):
            return 'commercial'
        elif 'review' in keyword_lower or 'best' in keyword_lower:
            return 'commercial_investigation'
        else:
            return 'informational'
    
    def _calculate_priority(self, keyword_data: Dict) -> int:
        """Calculate keyword priority based on multiple factors."""
        priority = 5  # Base priority
        
        # High search volume increases priority
        if keyword_data.get('search_volume', 0) > 5000:
            priority += 3
        elif keyword_data.get('search_volume', 0) > 1000:
            priority += 2
        elif keyword_data.get('search_volume', 0) > 100:
            priority += 1
        
        # Lower difficulty increases priority
        difficulty = keyword_data.get('difficulty', 5)
        if difficulty <= 3:
            priority += 2
        elif difficulty <= 5:
            priority += 1
        elif difficulty >= 8:
            priority -= 1
        
        # Higher CPC can indicate commercial value
        if keyword_data.get('cpc', 0) > 2:
            priority += 1
        
        return min(10, max(1, priority))