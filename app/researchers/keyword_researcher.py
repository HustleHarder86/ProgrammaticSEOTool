"""Keyword research and expansion module."""
import logging
from typing import List, Dict, Optional
from app.scanners.base import BusinessInfo, ContentOpportunity
from config import settings

logger = logging.getLogger(__name__)

class KeywordResearcher:
    """Handles keyword research and expansion."""
    
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
    
    async def expand_keywords(self, opportunities: List[ContentOpportunity], business_info: BusinessInfo) -> List[Dict]:
        """Expand content opportunities into detailed keyword sets."""
        expanded_keywords = []
        
        for opp in opportunities[:30]:  # Process top 30 opportunities
            # Generate variations
            variations = await self._generate_keyword_variations(opp, business_info)
            
            for var in variations:
                expanded_keywords.append({
                    'keyword': var['keyword'],
                    'content_type': opp.content_type,
                    'priority': opp.priority,
                    'title_template': var.get('title_template', opp.title_template),
                    'search_intent': var.get('search_intent', 'informational'),
                    'estimated_difficulty': var.get('difficulty', 5),
                    'topic_cluster': var.get('topic_cluster', 'general')
                })
        
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