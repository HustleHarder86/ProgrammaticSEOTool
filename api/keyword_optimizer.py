"""Enhanced keyword generation for specialized industries"""
import re
from typing import List, Dict, Any

class KeywordOptimizer:
    def __init__(self):
        # Industry-specific keyword patterns
        self.industry_patterns = {
            "real_estate": {
                "location_based": [
                    "{location} homes for sale",
                    "{location} real estate market analysis",
                    "{location} property values {year}",
                    "{location} neighborhood guide",
                    "best neighborhoods in {location}",
                    "{location} housing market trends",
                    "{location} real estate investment opportunities",
                    "cost of living in {location}",
                    "{location} school districts and homes",
                    "moving to {location} guide"
                ],
                "property_types": [
                    "{property_type} for sale in {location}",
                    "best {property_type} in {location}",
                    "{property_type} vs {property_type2} in {location}",
                    "investing in {property_type} {location}",
                    "{property_type} market analysis {location}",
                    "buying {property_type} tips {location}",
                    "{property_type} financing options",
                    "{property_type} inspection checklist"
                ],
                "buyer_intent": [
                    "first time home buyer {location}",
                    "how to buy a house in {location}",
                    "down payment assistance {location}",
                    "mortgage calculator {location}",
                    "home buying process {location}",
                    "best time to buy in {location}",
                    "real estate agents in {location}",
                    "home inspection {location}"
                ],
                "market_analysis": [
                    "{location} housing market forecast {year}",
                    "{location} real estate trends {season} {year}",
                    "is {location} a buyers or sellers market",
                    "{location} median home price trends",
                    "{location} real estate roi analysis",
                    "{location} rental market analysis",
                    "airbnb investment {location}",
                    "{location} property tax guide"
                ],
                "comparison": [
                    "{location1} vs {location2} real estate",
                    "living in {location1} vs {location2}",
                    "{neighborhood1} vs {neighborhood2} {city}",
                    "buying vs renting in {location}",
                    "condo vs house in {location}",
                    "new construction vs existing homes {location}"
                ]
            },
            "saas": {
                "comparison": [
                    "{product} vs {competitor}",
                    "{product} alternatives",
                    "best {category} software {year}",
                    "{product} pricing guide",
                    "{product} review {year}"
                ],
                "use_cases": [
                    "{product} for {industry}",
                    "how to use {product} for {use_case}",
                    "{product} {industry} case study",
                    "{product} integration with {tool}",
                    "{product} automation guide"
                ],
                "tutorials": [
                    "{product} tutorial for beginners",
                    "{product} advanced features",
                    "{product} setup guide",
                    "{product} best practices",
                    "{product} tips and tricks"
                ]
            },
            "ecommerce": {
                "product": [
                    "best {product} for {use_case}",
                    "{product} buying guide {year}",
                    "{product} vs {alternative}",
                    "cheap {product} under ${price}",
                    "{product} reviews {year}"
                ],
                "category": [
                    "{category} gift ideas",
                    "best {category} brands",
                    "{category} trends {year}",
                    "how to choose {category}",
                    "{category} size guide"
                ]
            }
        }
        
        # Location data for real estate
        self.locations = {
            "major_cities": ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix", 
                           "Philadelphia", "San Antonio", "San Diego", "Dallas", "San Jose"],
            "tech_hubs": ["San Francisco", "Seattle", "Austin", "Denver", "Portland"],
            "growing_markets": ["Nashville", "Raleigh", "Charlotte", "Tampa", "Orlando"],
            "neighborhoods": ["Downtown", "Midtown", "Uptown", "Westside", "Eastside", 
                            "North End", "South End", "Historic District", "Arts District"]
        }
        
        self.property_types = ["condos", "townhouses", "single family homes", "luxury homes",
                              "starter homes", "investment properties", "multi-family homes",
                              "waterfront properties", "historic homes", "new construction"]

    def generate_real_estate_keywords(self, business_info: Dict, num_keywords: int = 50) -> List[Dict]:
        """Generate comprehensive real estate keywords"""
        keywords = []
        patterns = self.industry_patterns["real_estate"]
        
        # Extract location from business info
        main_location = self.extract_location(business_info)
        year = "2024"
        season = "fall"
        
        # Generate location-based keywords
        for pattern in patterns["location_based"]:
            if main_location:
                keyword = pattern.format(location=main_location, year=year)
                keywords.append(self.create_keyword_object(keyword, "local", "informational"))
            
            # Also generate for nearby areas
            for nearby in self.get_nearby_locations(main_location)[:3]:
                keyword = pattern.format(location=nearby, year=year)
                keywords.append(self.create_keyword_object(keyword, "local", "informational"))
        
        # Generate property type keywords
        for property_type in self.property_types[:5]:
            for pattern in patterns["property_types"][:3]:
                if "{property_type2}" in pattern:
                    property_type2 = self.property_types[
                        (self.property_types.index(property_type) + 1) % len(self.property_types)
                    ]
                    keyword = pattern.format(
                        property_type=property_type,
                        property_type2=property_type2,
                        location=main_location
                    )
                else:
                    keyword = pattern.format(
                        property_type=property_type,
                        location=main_location
                    )
                keywords.append(self.create_keyword_object(keyword, "property", "commercial"))
        
        # Generate buyer intent keywords
        for pattern in patterns["buyer_intent"]:
            keyword = pattern.format(location=main_location)
            keywords.append(self.create_keyword_object(keyword, "buyer", "transactional"))
        
        # Generate market analysis keywords
        for pattern in patterns["market_analysis"]:
            keyword = pattern.format(location=main_location, year=year, season=season)
            keywords.append(self.create_keyword_object(keyword, "analysis", "informational"))
        
        # Generate comparison keywords
        nearby_locations = self.get_nearby_locations(main_location)
        if len(nearby_locations) >= 2:
            for pattern in patterns["comparison"][:3]:
                if "{location1}" in pattern:
                    keyword = pattern.format(
                        location1=main_location,
                        location2=nearby_locations[0],
                        city=main_location
                    )
                elif "{neighborhood1}" in pattern:
                    keyword = pattern.format(
                        neighborhood1=self.locations["neighborhoods"][0],
                        neighborhood2=self.locations["neighborhoods"][1],
                        city=main_location
                    )
                else:
                    keyword = pattern.format(location=main_location)
                keywords.append(self.create_keyword_object(keyword, "comparison", "commercial"))
        
        # Remove duplicates and limit
        unique_keywords = self.deduplicate_keywords(keywords)
        return unique_keywords[:num_keywords]

    def extract_location(self, business_info: Dict) -> str:
        """Extract location from business info"""
        # Try to find location in various fields
        location_fields = ['location', 'city', 'area', 'region']
        for field in location_fields:
            if field in business_info and business_info[field]:
                return business_info[field]
        
        # Try to extract from business name or description
        text = f"{business_info.get('name', '')} {business_info.get('description', '')}"
        for city in self.locations["major_cities"] + self.locations["tech_hubs"]:
            if city.lower() in text.lower():
                return city
        
        # Default to a major market
        return "Austin"  # Default tech hub with strong real estate market

    def get_nearby_locations(self, location: str) -> List[str]:
        """Get nearby locations for a given location"""
        # Simplified - in production, use real geographic data
        location_groups = {
            "Austin": ["Round Rock", "Cedar Park", "Pflugerville", "Georgetown", "San Marcos"],
            "San Francisco": ["Oakland", "San Jose", "Berkeley", "Palo Alto", "Mountain View"],
            "New York": ["Brooklyn", "Queens", "Long Island", "Westchester", "Jersey City"],
            "Los Angeles": ["Santa Monica", "Pasadena", "Long Beach", "Burbank", "Glendale"],
            "Chicago": ["Evanston", "Oak Park", "Naperville", "Arlington Heights", "Schaumburg"]
        }
        
        return location_groups.get(location, ["Suburbs", "Metro Area", "Downtown"])

    def create_keyword_object(self, keyword: str, category: str, intent: str) -> Dict:
        """Create a structured keyword object"""
        # Estimate metrics based on keyword characteristics
        word_count = len(keyword.split())
        has_location = any(loc.lower() in keyword.lower() 
                          for loc in self.locations["major_cities"] + self.locations["tech_hubs"])
        
        # More specific = lower volume but easier to rank
        if word_count >= 5:
            volume = 100 + (50 * (6 - word_count))
            difficulty = 25 + (word_count * 2)
        else:
            volume = 500 + (200 * (5 - word_count))
            difficulty = 40 + (word_count * 5)
        
        # Location keywords typically have good volume
        if has_location:
            volume = int(volume * 1.5)
        
        # Commercial intent increases CPC
        cpc_base = 1.5
        if intent == "commercial":
            cpc_base = 3.5
        elif intent == "transactional":
            cpc_base = 4.5
        
        return {
            "keyword": keyword,
            "search_volume": volume,
            "difficulty": min(difficulty, 65),  # Cap difficulty
            "intent": intent,
            "cpc": round(cpc_base + (volume / 1000), 2),
            "category": category,
            "priority": self.calculate_priority(volume, difficulty, cpc_base)
        }

    def calculate_priority(self, volume: int, difficulty: int, cpc: float) -> int:
        """Calculate keyword priority score"""
        # Higher volume, lower difficulty, higher CPC = higher priority
        volume_score = min(volume / 100, 10)
        difficulty_score = 10 - (difficulty / 10)
        cpc_score = min(cpc, 5)
        
        return int((volume_score + difficulty_score + cpc_score) / 3 * 20)

    def deduplicate_keywords(self, keywords: List[Dict]) -> List[Dict]:
        """Remove duplicate keywords, keeping the best version"""
        seen = {}
        for kw in keywords:
            key = kw["keyword"].lower().strip()
            if key not in seen or kw["priority"] > seen[key]["priority"]:
                seen[key] = kw
        
        # Sort by priority
        return sorted(seen.values(), key=lambda x: x["priority"], reverse=True)

    def generate_keyword_clusters(self, keywords: List[Dict]) -> Dict[str, List[Dict]]:
        """Create smart keyword clusters for real estate"""
        clusters = {
            "location_guides": {
                "name": "Location & Neighborhood Guides",
                "keywords": [],
                "content_hub": "Ultimate Guide to [Location] Real Estate"
            },
            "property_types": {
                "name": "Property Type Guides",
                "keywords": [],
                "content_hub": "Complete Property Type Comparison Guide"
            },
            "buyer_resources": {
                "name": "Home Buyer Resources",
                "keywords": [],
                "content_hub": "First-Time Home Buyer's Complete Guide"
            },
            "market_analysis": {
                "name": "Market Analysis & Trends",
                "keywords": [],
                "content_hub": "[Location] Real Estate Market Report {Year}"
            },
            "comparisons": {
                "name": "Comparisons & Versus Guides",
                "keywords": [],
                "content_hub": "Real Estate Comparison Hub"
            },
            "investment": {
                "name": "Real Estate Investment",
                "keywords": [],
                "content_hub": "Real Estate Investment Strategy Guide"
            }
        }
        
        # Categorize keywords into clusters
        for kw in keywords:
            keyword_lower = kw["keyword"].lower()
            
            if any(term in keyword_lower for term in ["neighborhood", "guide", "living in", "cost of", "moving to"]):
                clusters["location_guides"]["keywords"].append(kw)
            elif any(term in keyword_lower for term in ["condo", "townhouse", "home", "property", "house"]) and "vs" not in keyword_lower:
                clusters["property_types"]["keywords"].append(kw)
            elif any(term in keyword_lower for term in ["buyer", "buying", "mortgage", "down payment", "financing"]):
                clusters["buyer_resources"]["keywords"].append(kw)
            elif any(term in keyword_lower for term in ["market", "forecast", "trends", "analysis", "median"]):
                clusters["market_analysis"]["keywords"].append(kw)
            elif "vs" in keyword_lower or "versus" in keyword_lower:
                clusters["comparisons"]["keywords"].append(kw)
            elif any(term in keyword_lower for term in ["investment", "roi", "rental", "airbnb", "flip"]):
                clusters["investment"]["keywords"].append(kw)
            else:
                # Default to location guides
                clusters["location_guides"]["keywords"].append(kw)
        
        # Remove empty clusters
        return {k: v for k, v in clusters.items() if v["keywords"]}

    def enhance_with_ai_prompt(self, industry: str, business_info: Dict) -> str:
        """Generate enhanced AI prompt for better keyword generation"""
        if industry.lower() == "real estate":
            return f"""Generate {business_info.get('num_keywords', 30)} highly specific long-tail keywords for a real estate business.

Business Focus: {business_info.get('description', 'Real estate services')}
Primary Location: {self.extract_location(business_info)}
Target Audience: {business_info.get('target_audience', 'Home buyers and sellers')}

Generate keywords in these categories:
1. Hyper-local keywords (neighborhood + service)
2. Property type comparisons
3. Market timing keywords (best time to buy/sell)
4. Financial/investment keywords
5. Demographic-specific (first-time buyers, downsizers, investors)

Include:
- Specific neighborhoods and suburbs
- Current year/season modifiers
- Price range qualifiers
- Buyer intent signals
- Problem-solving keywords (e.g., "how to sell house fast in [location]")

Format: One keyword per line, 3-7 words each, highly specific and actionable."""
        
        # Default prompt for other industries
        return f"""Generate {business_info.get('num_keywords', 20)} specific long-tail keywords for:
Business: {business_info.get('name', 'Unknown')}
Industry: {industry}
Description: {business_info.get('description', '')}

Focus on:
- Specific use cases
- Comparison keywords
- Problem-solving keywords
- Industry-specific terminology
- Current trends

Format: One keyword per line."""