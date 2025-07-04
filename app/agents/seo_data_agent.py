"""SEO Data Agent for integrating real keyword research APIs."""
import os
import json
import logging
import hashlib
from typing import List, Dict, Optional, Any
from datetime import datetime, timedelta
import aiohttp
from config import settings

logger = logging.getLogger(__name__)

class SEODataAgent:
    """Handles integration with real SEO data providers."""
    
    def __init__(self):
        self.serpapi_key = settings.serpapi_key
        self.ubersuggest_key = settings.ubersuggest_api_key
        self.cache_dir = settings.cache_dir / "seo_data"
        self.cache_dir.mkdir(exist_ok=True)
        self.cache_ttl = timedelta(days=7)  # Cache for 7 days
    
    def _get_cache_key(self, provider: str, query: str, params: Dict = None) -> str:
        """Generate cache key for API results."""
        cache_data = f"{provider}:{query}:{json.dumps(params or {}, sort_keys=True)}"
        return hashlib.md5(cache_data.encode()).hexdigest()
    
    def _get_cached_data(self, cache_key: str) -> Optional[Dict]:
        """Retrieve cached data if available and not expired."""
        cache_file = self.cache_dir / f"{cache_key}.json"
        
        if cache_file.exists():
            try:
                with open(cache_file, 'r') as f:
                    data = json.load(f)
                
                # Check if cache is still valid
                cached_time = datetime.fromisoformat(data['cached_at'])
                if datetime.now() - cached_time < self.cache_ttl:
                    logger.info(f"Using cached data for {cache_key}")
                    return data['results']
                    
            except Exception as e:
                logger.error(f"Error reading cache: {e}")
        
        return None
    
    def _save_to_cache(self, cache_key: str, data: Dict):
        """Save data to cache."""
        cache_file = self.cache_dir / f"{cache_key}.json"
        
        try:
            with open(cache_file, 'w') as f:
                json.dump({
                    'cached_at': datetime.now().isoformat(),
                    'results': data
                }, f)
        except Exception as e:
            logger.error(f"Error saving to cache: {e}")
    
    async def get_keyword_data(self, keyword: str, location: Optional[str] = None) -> Dict[str, Any]:
        """Get keyword data from available APIs with fallback."""
        # Try SerpAPI first
        if self.serpapi_key:
            data = await self._get_serpapi_data(keyword, location)
            if data:
                return data
        
        # Try Ubersuggest
        if self.ubersuggest_key:
            data = await self._get_ubersuggest_data(keyword)
            if data:
                return data
        
        # Fallback to AI estimates
        return self._get_ai_estimates(keyword)
    
    async def _get_serpapi_data(self, keyword: str, location: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Get keyword data from SerpAPI."""
        cache_key = self._get_cache_key("serpapi", keyword, {"location": location})
        
        # Check cache first
        cached = self._get_cached_data(cache_key)
        if cached:
            return cached
        
        try:
            params = {
                "q": keyword,
                "api_key": self.serpapi_key,
                "engine": "google",
                "hl": "en",
                "gl": "us"
            }
            
            if location:
                params["location"] = location
            
            async with aiohttp.ClientSession() as session:
                async with session.get("https://serpapi.com/search", params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        # Extract relevant SEO data
                        result = {
                            "keyword": keyword,
                            "search_volume": self._estimate_volume_from_serp(data),
                            "difficulty": self._estimate_difficulty_from_serp(data),
                            "cpc": data.get("ads", [{}])[0].get("cpc", 0),
                            "competition": len(data.get("organic_results", [])),
                            "related_searches": [r["query"] for r in data.get("related_searches", [])[:5]],
                            "source": "serpapi",
                            "timestamp": datetime.now().isoformat()
                        }
                        
                        self._save_to_cache(cache_key, result)
                        return result
                        
        except Exception as e:
            logger.error(f"Error fetching SerpAPI data: {e}")
        
        return None
    
    async def _get_ubersuggest_data(self, keyword: str) -> Optional[Dict[str, Any]]:
        """Get keyword data from Ubersuggest API."""
        cache_key = self._get_cache_key("ubersuggest", keyword)
        
        # Check cache first
        cached = self._get_cached_data(cache_key)
        if cached:
            return cached
        
        # Note: Ubersuggest API implementation would go here
        # This is a placeholder as the actual API may have different endpoints
        logger.info("Ubersuggest API not implemented yet")
        return None
    
    def _estimate_volume_from_serp(self, serp_data: Dict) -> int:
        """Estimate search volume from SERP features."""
        # Basic estimation based on SERP features
        base_volume = 1000
        
        if serp_data.get("knowledge_graph"):
            base_volume *= 2
        if serp_data.get("people_also_ask"):
            base_volume *= 1.5
        if len(serp_data.get("ads", [])) > 3:
            base_volume *= 2
        
        return int(base_volume)
    
    def _estimate_difficulty_from_serp(self, serp_data: Dict) -> int:
        """Estimate keyword difficulty from SERP features."""
        difficulty = 5
        
        # More ads = more commercial = harder
        if len(serp_data.get("ads", [])) > 3:
            difficulty += 2
        
        # Featured snippets = competitive
        if serp_data.get("answer_box") or serp_data.get("featured_snippet"):
            difficulty += 1
        
        # Many PAA = informational, slightly easier
        if len(serp_data.get("people_also_ask", [])) > 3:
            difficulty -= 1
        
        return max(1, min(10, difficulty))
    
    def _get_ai_estimates(self, keyword: str) -> Dict[str, Any]:
        """Fallback AI-based estimates when no API data available."""
        # Simple heuristic estimates
        word_count = len(keyword.split())
        
        # Longer keywords = lower volume, easier difficulty
        if word_count <= 2:
            volume = 5000
            difficulty = 7
        elif word_count <= 4:
            volume = 1000
            difficulty = 5
        else:
            volume = 100
            difficulty = 3
        
        return {
            "keyword": keyword,
            "search_volume": volume,
            "difficulty": difficulty,
            "cpc": 0,
            "competition": 0,
            "related_searches": [],
            "source": "ai_estimate",
            "timestamp": datetime.now().isoformat()
        }
    
    async def get_bulk_keyword_data(self, keywords: List[str], location: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get data for multiple keywords efficiently."""
        results = []
        
        # Process in batches to avoid rate limits
        batch_size = 10
        for i in range(0, len(keywords), batch_size):
            batch = keywords[i:i + batch_size]
            
            # Process batch concurrently
            import asyncio
            batch_results = await asyncio.gather(
                *[self.get_keyword_data(kw, location) for kw in batch],
                return_exceptions=True
            )
            
            for kw, result in zip(batch, batch_results):
                if isinstance(result, Exception):
                    logger.error(f"Error getting data for {kw}: {result}")
                    results.append(self._get_ai_estimates(kw))
                else:
                    results.append(result)
        
        return results
    
    async def discover_related_keywords(self, seed_keyword: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Discover related keywords from a seed keyword."""
        # Get initial data
        initial_data = await self.get_keyword_data(seed_keyword)
        
        # Start with related searches
        related_keywords = initial_data.get("related_searches", [])
        
        # Add variations
        variations = self._generate_keyword_variations(seed_keyword)
        related_keywords.extend(variations)
        
        # Get data for all related keywords
        unique_keywords = list(set(related_keywords))[:limit]
        return await self.get_bulk_keyword_data(unique_keywords)
    
    def _generate_keyword_variations(self, keyword: str) -> List[str]:
        """Generate simple keyword variations."""
        variations = []
        base_words = keyword.lower().split()
        
        # Add question variations
        question_words = ["how", "what", "why", "when", "where", "who"]
        for q in question_words:
            variations.append(f"{q} {keyword}")
        
        # Add intent modifiers
        modifiers = ["best", "top", "cheap", "free", "review", "guide", "tutorial"]
        for mod in modifiers:
            variations.append(f"{mod} {keyword}")
            variations.append(f"{keyword} {mod}")
        
        # Add year if not present
        import re
        if not re.search(r'\b20\d{2}\b', keyword):
            current_year = datetime.now().year
            variations.append(f"{keyword} {current_year}")
        
        return variations[:20]  # Limit variations