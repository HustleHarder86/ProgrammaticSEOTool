"""Enhanced keyword generation for specialized industries"""
import re
from typing import List, Dict, Any

class KeywordOptimizer:
    def __init__(self):
        # Industry-specific keyword patterns
        self.industry_patterns = {
            "real_estate_b2b": {
                "realtor_tools": [
                    "investment property analysis tool for realtors",
                    "best rental analysis software for real estate agents",
                    "property investment calculator for agents",
                    "realtor tools for investor clients",
                    "real estate agent investment property software",
                    "rental property analysis app for realtors",
                    "client investment property presentation tools",
                    "realtor rental income calculator",
                    "real estate agent ROI analysis tools",
                    "property investment report generator for agents"
                ],
                "client_acquisition": [
                    "how to find real estate investor clients",
                    "attracting property investors as realtor",
                    "real estate investor lead generation",
                    "marketing to real estate investors",
                    "realtor specializing in investment properties {location}",
                    "investment property realtor {location}",
                    "how to work with real estate investors",
                    "building investor client base as realtor",
                    "real estate agent for rental properties {location}",
                    "investor-friendly real estate agents {location}"
                ],
                "market_expertise": [
                    "{location} investment property market report",
                    "{location} rental market analysis for realtors",
                    "{location} cap rates by neighborhood",
                    "{location} rental property trends {year}",
                    "best {location} neighborhoods for rental investment",
                    "{location} short term rental regulations guide",
                    "{location} investment property tax guide",
                    "{location} rental property financing options",
                    "{location} property management companies list",
                    "{location} real estate investment opportunities {year}"
                ],
                "listing_optimization": [
                    "how to list investment properties",
                    "marketing rental properties to investors",
                    "investment property listing description templates",
                    "showcasing rental income potential in listings",
                    "MLS keywords for investment properties",
                    "investment property photography tips",
                    "virtual tours for rental properties",
                    "highlighting cap rate in property listings",
                    "investment property listing checklist",
                    "attracting cash buyers for investment properties"
                ],
                "education_certification": [
                    "real estate investment specialist certification",
                    "CCIM designation for realtors",
                    "investment property courses for real estate agents",
                    "rental property management for realtors",
                    "1031 exchange certification for agents",
                    "real estate investment analysis training",
                    "airbnb specialist certification for realtors",
                    "multifamily investment training for agents",
                    "commercial real estate courses for residential agents",
                    "real estate syndication for agents"
                ],
                "closing_deals": [
                    "investment property offer strategies",
                    "negotiating investment property deals",
                    "due diligence checklist for investment properties",
                    "investment property inspection focus areas",
                    "closing costs for investment properties",
                    "investment property contract clauses",
                    "working with investor-friendly lenders",
                    "fast closing for investment properties",
                    "wholesale real estate for agents",
                    "investment property commission strategies"
                ]
            },
            "real_estate_investment": {
                "roi_analysis": [
                    "{location} rental property roi calculator",
                    "{location} airbnb vs long term rental income",
                    "{location} short term rental analysis",
                    "{location} rental yield calculator",
                    "cap rate {location} investment properties",
                    "{location} cash flow positive properties",
                    "{location} rental property profit calculator",
                    "best roi neighborhoods {location}",
                    "{location} investment property analyzer",
                    "{location} real estate investment returns {year}"
                ],
                "market_analysis": [
                    "{location} rental market analysis {year}",
                    "{location} airbnb occupancy rates",
                    "{location} average rental income by neighborhood",
                    "{location} short term rental regulations",
                    "{location} rental demand forecast",
                    "{location} investment property hotspots",
                    "{location} rental price trends {year}",
                    "{location} vacation rental market analysis",
                    "{location} rental property appreciation rates",
                    "{location} tenant demographics analysis"
                ],
                "property_comparison": [
                    "long term vs short term rental {location}",
                    "airbnb vs traditional rental income {location}",
                    "{property_type} rental income {location}",
                    "single family vs multifamily investment {location}",
                    "furnished vs unfurnished rental income {location}",
                    "vacation rental vs monthly rental {location}",
                    "{neighborhood1} vs {neighborhood2} rental income",
                    "new construction vs existing rental property {location}"
                ],
                "investment_tools": [
                    "rental property analysis spreadsheet",
                    "investment property calculator {location}",
                    "rental income estimator {location}",
                    "property management cost calculator {location}",
                    "rental property expense tracker",
                    "real estate investment analysis software",
                    "rental property cash flow calculator",
                    "1031 exchange calculator {location}",
                    "depreciation calculator rental property",
                    "rental property tax calculator {location}"
                ],
                "investor_education": [
                    "how to analyze rental property {location}",
                    "rental property investment guide {location}",
                    "short term rental investment strategy {location}",
                    "passive income real estate {location}",
                    "rental property financing options {location}",
                    "best areas for rental investment {location}",
                    "rental property due diligence checklist",
                    "real estate investment mistakes to avoid {location}",
                    "how to evaluate rental property deals",
                    "rental property investment for beginners {location}"
                ],
                "specific_strategies": [
                    "brrrr strategy {location}",
                    "house hacking {location}",
                    "section 8 rental income {location}",
                    "student housing investment {location}",
                    "corporate rental strategy {location}",
                    "mid term rental strategy {location}",
                    "rental arbitrage {location}",
                    "fix and rent strategy {location}",
                    "turnkey rental properties {location}",
                    "out of state rental investing {location}"
                ]
            },
            "real_estate": {
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

    def detect_target_audience(self, business_info: Dict) -> str:
        """Detect target audience from business info"""
        description = f"{business_info.get('description', '')} {business_info.get('name', '')}".lower()
        
        # Check if explicitly set
        if business_info.get('target_audience_type'):
            return business_info['target_audience_type']
        
        # Keywords indicating B2B realtor focus
        b2b_keywords = [
            'realtors', 'agents', 'brokers', 'real estate professionals',
            'for agents', 'for realtors', 'agent tool', 'realtor software',
            'b2b', 'real estate crm', 'mls', 'listing tool'
        ]
        
        # Keywords indicating investment/realtor focus
        investment_keywords = [
            'investment', 'investor', 'roi', 'rental', 'airbnb', 'short term', 
            'long term', 'cash flow', 'cap rate', 'yield', 'analysis', 'analyzer',
            'property management', 'rental income'
        ]
        
        # Keywords indicating home buyer focus
        buyer_keywords = [
            'home buyer', 'first time', 'mortgage', 'dream home', 'family home',
            'house hunting', 'home search', 'buying a home'
        ]
        
        b2b_score = sum(2 for kw in b2b_keywords if kw in description)  # Weight B2B higher
        investment_score = sum(1 for kw in investment_keywords if kw in description)
        buyer_score = sum(1 for kw in buyer_keywords if kw in description)
        
        # If URL provided, check that too
        if business_info.get('url'):
            url_lower = business_info.get('url', '').lower()
            b2b_score += sum(2 for kw in b2b_keywords if kw in url_lower)
            investment_score += sum(1 for kw in investment_keywords if kw in url_lower)
            buyer_score += sum(1 for kw in buyer_keywords if kw in url_lower)
        
        # Determine primary audience
        if b2b_score > investment_score and b2b_score > buyer_score:
            return "b2b_realtors"
        elif investment_score > buyer_score:
            return "investors"
        elif buyer_score > investment_score:
            return "home_buyers"
        else:
            # Default to B2B for your use case
            return "b2b_realtors"

    def generate_multi_audience_projects(self, business_info: Dict, num_keywords_per_audience: int = 30) -> Dict[str, Any]:
        """Generate separate keyword sets for B2B and B2C audiences"""
        projects = {
            "b2b_project": {
                "name": "B2B - Real Estate Agents & Brokers",
                "description": "Target real estate professionals who need tools for their investor clients",
                "keywords": [],
                "clusters": {},
                "audience": "b2b_realtors"
            },
            "b2c_project": {
                "name": "B2C - Property Investors",
                "description": "Target individual property investors looking for analysis tools",
                "keywords": [],
                "clusters": {},
                "audience": "investors"
            }
        }
        
        # Generate B2B keywords
        b2b_info = business_info.copy()
        b2b_info['target_audience_type'] = 'b2b_realtors'
        projects["b2b_project"]["keywords"] = self.generate_real_estate_keywords(b2b_info, num_keywords_per_audience)
        projects["b2b_project"]["clusters"] = self.generate_keyword_clusters(
            projects["b2b_project"]["keywords"], 
            "b2b_realtors"
        )
        
        # Generate B2C keywords
        b2c_info = business_info.copy()
        b2c_info['target_audience_type'] = 'investors'
        projects["b2c_project"]["keywords"] = self.generate_real_estate_keywords(b2c_info, num_keywords_per_audience)
        projects["b2c_project"]["clusters"] = self.generate_keyword_clusters(
            projects["b2c_project"]["keywords"], 
            "investors"
        )
        
        # Add summary statistics
        projects["summary"] = {
            "total_keywords": len(projects["b2b_project"]["keywords"]) + len(projects["b2c_project"]["keywords"]),
            "b2b_keywords": len(projects["b2b_project"]["keywords"]),
            "b2c_keywords": len(projects["b2c_project"]["keywords"]),
            "recommended_approach": "Create separate content silos for each audience to maximize relevance and conversion"
        }
        
        return projects

    def generate_real_estate_keywords(self, business_info: Dict, num_keywords: int = 50) -> List[Dict]:
        """Generate comprehensive real estate keywords based on target audience"""
        keywords = []
        
        # Detect target audience
        if business_info.get('target_audience_type'):
            target_audience = business_info['target_audience_type']
        else:
            target_audience = self.detect_target_audience(business_info)
        business_info['detected_audience'] = target_audience
        
        # Use appropriate patterns based on audience
        if target_audience == "b2b_realtors":
            patterns = self.industry_patterns["real_estate_b2b"]
        elif target_audience == "investors" or target_audience == "investors_realtors":
            patterns = self.industry_patterns["real_estate_investment"]
        else:
            patterns = self.industry_patterns.get("real_estate", self.industry_patterns["real_estate_investment"])
        
        # Extract location from business info
        main_location = self.extract_location(business_info)
        year = "2024"
        season = "fall"
        
        # Generate B2B Realtor keywords
        if "realtor_tools" in patterns:
            # Generate tool-focused keywords (no location needed for most)
            for pattern in patterns["realtor_tools"][:10]:
                keywords.append(self.create_keyword_object(pattern, "tools", "commercial", is_b2b=True))
            
            # Generate client acquisition keywords
            for pattern in patterns["client_acquisition"][:8]:
                if "{location}" in pattern and main_location:
                    keyword = pattern.format(location=main_location)
                else:
                    keyword = pattern
                keywords.append(self.create_keyword_object(keyword, "client_acquisition", "informational", is_b2b=True))
            
            # Generate market expertise keywords
            for pattern in patterns["market_expertise"][:8]:
                keyword = pattern.format(location=main_location, year=year)
                keywords.append(self.create_keyword_object(keyword, "market_expertise", "informational", is_b2b=True))
            
            # Generate listing optimization keywords
            for pattern in patterns["listing_optimization"][:6]:
                keywords.append(self.create_keyword_object(pattern, "listing_optimization", "informational", is_b2b=True))
            
            # Generate education keywords
            for pattern in patterns["education_certification"][:5]:
                keywords.append(self.create_keyword_object(pattern, "education", "informational", is_b2b=True))
            
            # Generate deal closing keywords
            for pattern in patterns["closing_deals"][:5]:
                keywords.append(self.create_keyword_object(pattern, "closing_deals", "commercial", is_b2b=True))
        
        # Generate ROI analysis keywords (most important for investors)
        elif "roi_analysis" in patterns:
            for pattern in patterns["roi_analysis"][:8]:
                if main_location:
                    keyword = pattern.format(location=main_location, year=year)
                    keywords.append(self.create_keyword_object(keyword, "roi_analysis", "commercial"))
                
                # Also generate for nearby areas
                for nearby in self.get_nearby_locations(main_location)[:2]:
                    keyword = pattern.format(location=nearby, year=year)
                    keywords.append(self.create_keyword_object(keyword, "roi_analysis", "commercial"))
        
        # Generate market analysis keywords
        if "market_analysis" in patterns:
            for pattern in patterns["market_analysis"][:6]:
                keyword = pattern.format(location=main_location, year=year, season=season)
                keywords.append(self.create_keyword_object(keyword, "market_analysis", "informational"))
        
        # Generate property comparison keywords
        if "property_comparison" in patterns:
            for pattern in patterns["property_comparison"][:5]:
                if "{property_type}" in pattern:
                    for prop_type in ["condo", "single family home", "townhouse"][:2]:
                        keyword = pattern.format(property_type=prop_type, location=main_location)
                        keywords.append(self.create_keyword_object(keyword, "comparison", "commercial"))
                elif "{neighborhood1}" in pattern:
                    neighborhoods = self.get_nearby_locations(main_location)
                    if len(neighborhoods) >= 2:
                        keyword = pattern.format(
                            neighborhood1=neighborhoods[0],
                            neighborhood2=neighborhoods[1]
                        )
                        keywords.append(self.create_keyword_object(keyword, "comparison", "commercial"))
                else:
                    keyword = pattern.format(location=main_location)
                    keywords.append(self.create_keyword_object(keyword, "comparison", "commercial"))
        
        # Generate investment tool keywords
        if "investment_tools" in patterns:
            for pattern in patterns["investment_tools"][:5]:
                keyword = pattern.format(location=main_location)
                keywords.append(self.create_keyword_object(keyword, "tools", "transactional"))
        
        # Generate education keywords
        if "investor_education" in patterns:
            for pattern in patterns["investor_education"][:5]:
                keyword = pattern.format(location=main_location)
                keywords.append(self.create_keyword_object(keyword, "education", "informational"))
        
        # Generate strategy keywords
        if "specific_strategies" in patterns:
            for pattern in patterns["specific_strategies"][:4]:
                keyword = pattern.format(location=main_location)
                keywords.append(self.create_keyword_object(keyword, "strategy", "informational"))
        
        
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

    def create_keyword_object(self, keyword: str, category: str, intent: str, is_b2b: bool = False) -> Dict:
        """Create a structured keyword object"""
        # Estimate metrics based on keyword characteristics
        word_count = len(keyword.split())
        has_location = any(loc.lower() in keyword.lower() 
                          for loc in self.locations["major_cities"] + self.locations["tech_hubs"])
        
        # B2B keywords have different metrics
        if is_b2b:
            # B2B keywords typically have lower volume but higher value
            if "tool" in keyword.lower() or "software" in keyword.lower():
                volume = 300 + (50 * max(0, 6 - word_count))
                difficulty = 45  # Tools are competitive
                cpc_base = 8.0  # High CPC for B2B software
            elif "how to" in keyword.lower() or "guide" in keyword.lower():
                volume = 200 + (100 * max(0, 5 - word_count))
                difficulty = 35
                cpc_base = 4.0
            else:
                volume = 150 + (50 * max(0, 5 - word_count))
                difficulty = 40
                cpc_base = 5.0
                
            # Realtor-specific terms have decent volume
            if any(term in keyword.lower() for term in ["realtor", "agent", "broker"]):
                volume = int(volume * 1.3)
        else:
            # Original logic for non-B2B
            if word_count >= 5:
                volume = 100 + (50 * (6 - word_count))
                difficulty = 25 + (word_count * 2)
            else:
                volume = 500 + (200 * (5 - word_count))
                difficulty = 40 + (word_count * 5)
            
            # Commercial intent increases CPC
            cpc_base = 1.5
            if intent == "commercial":
                cpc_base = 3.5
            elif intent == "transactional":
                cpc_base = 4.5
        
        # Location keywords typically have good volume
        if has_location:
            volume = int(volume * 1.5)
        
        return {
            "keyword": keyword,
            "search_volume": volume,
            "difficulty": min(difficulty, 65),  # Cap difficulty
            "intent": intent,
            "cpc": round(cpc_base + (volume / 1000), 2),
            "category": category,
            "is_b2b": is_b2b,
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

    def generate_keyword_clusters(self, keywords: List[Dict], target_audience: str = None) -> Dict[str, List[Dict]]:
        """Create smart keyword clusters based on target audience"""
        
        if target_audience == "b2b_realtors":
            clusters = {
                "realtor_tools": {
                    "name": "Tools & Software for Realtors",
                    "keywords": [],
                    "content_hub": "Real Estate Agent Tool Comparison Hub",
                    "icon": "🛠️"
                },
                "client_acquisition": {
                    "name": "Finding Investor Clients",
                    "keywords": [],
                    "content_hub": "Realtor's Guide to Working with Investors",
                    "icon": "🤝"
                },
                "market_expertise": {
                    "name": "Market Analysis & Reports",
                    "keywords": [],
                    "content_hub": "Local Investment Market Intelligence",
                    "icon": "📊"
                },
                "listing_strategies": {
                    "name": "Investment Property Listings",
                    "keywords": [],
                    "content_hub": "Marketing Investment Properties Guide",
                    "icon": "📝"
                },
                "education": {
                    "name": "Realtor Education & Certification",
                    "keywords": [],
                    "content_hub": "Investment Property Specialist Training",
                    "icon": "🎓"
                },
                "deal_closing": {
                    "name": "Closing Investment Deals",
                    "keywords": [],
                    "content_hub": "Investment Property Transaction Guide",
                    "icon": "✅"
                }
            }
        elif target_audience == "investors_realtors" or target_audience == "investors":
            clusters = {
                "roi_calculators": {
                    "name": "ROI Calculators & Analysis Tools",
                    "keywords": [],
                    "content_hub": "Investment Property Analysis Hub",
                    "icon": "🧮"
                },
                "rental_comparison": {
                    "name": "Short-Term vs Long-Term Rental Analysis",
                    "keywords": [],
                    "content_hub": "Rental Strategy Comparison Guide",
                    "icon": "⚖️"
                },
                "market_data": {
                    "name": "Market Data & Trends",
                    "keywords": [],
                    "content_hub": "Real Estate Market Intelligence Center",
                    "icon": "📊"
                },
                "investment_strategies": {
                    "name": "Investment Strategies",
                    "keywords": [],
                    "content_hub": "Real Estate Investment Playbook",
                    "icon": "🎯"
                },
                "location_analysis": {
                    "name": "Location Investment Analysis",
                    "keywords": [],
                    "content_hub": "Best Investment Neighborhoods Guide",
                    "icon": "📍"
                },
                "tools_resources": {
                    "name": "Tools & Resources",
                    "keywords": [],
                    "content_hub": "Investor Toolkit",
                    "icon": "🛠️"
                }
            }
        else:
            # Original home buyer clusters
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
            assigned = False
            
            if target_audience == "b2b_realtors":
                # B2B Realtor clustering
                if any(term in keyword_lower for term in ["tool", "software", "calculator", "app", "platform"]):
                    clusters["realtor_tools"]["keywords"].append(kw)
                    assigned = True
                elif any(term in keyword_lower for term in ["find", "attract", "client", "lead", "marketing to"]):
                    clusters["client_acquisition"]["keywords"].append(kw)
                    assigned = True
                elif any(term in keyword_lower for term in ["market", "analysis", "report", "trends", "cap rate"]):
                    clusters["market_expertise"]["keywords"].append(kw)
                    assigned = True
                elif any(term in keyword_lower for term in ["listing", "mls", "showcase", "photography", "description"]):
                    clusters["listing_strategies"]["keywords"].append(kw)
                    assigned = True
                elif any(term in keyword_lower for term in ["certification", "course", "training", "designation", "education"]):
                    clusters["education"]["keywords"].append(kw)
                    assigned = True
                elif any(term in keyword_lower for term in ["closing", "negotiat", "offer", "contract", "due diligence"]):
                    clusters["deal_closing"]["keywords"].append(kw)
                    assigned = True
                
                # Default based on category
                if not assigned:
                    category = kw.get("category", "")
                    if category == "tools":
                        clusters["realtor_tools"]["keywords"].append(kw)
                    elif category == "client_acquisition":
                        clusters["client_acquisition"]["keywords"].append(kw)
                    elif category == "market_expertise":
                        clusters["market_expertise"]["keywords"].append(kw)
                    else:
                        clusters["realtor_tools"]["keywords"].append(kw)
                        
            elif target_audience == "investors_realtors" or target_audience == "investors":
                # Investor-specific clustering
                if any(term in keyword_lower for term in ["roi", "calculator", "analyzer", "yield", "cap rate", "cash flow"]):
                    clusters["roi_calculators"]["keywords"].append(kw)
                    assigned = True
                elif any(term in keyword_lower for term in ["short term", "long term", "airbnb", "vrbo", "vacation rental"]) and any(term in keyword_lower for term in ["vs", "versus", "comparison"]):
                    clusters["rental_comparison"]["keywords"].append(kw)
                    assigned = True
                elif any(term in keyword_lower for term in ["market", "forecast", "trends", "analysis", "occupancy", "demand"]):
                    clusters["market_data"]["keywords"].append(kw)
                    assigned = True
                elif any(term in keyword_lower for term in ["strategy", "brrrr", "house hack", "section 8", "arbitrage", "turnkey"]):
                    clusters["investment_strategies"]["keywords"].append(kw)
                    assigned = True
                elif any(term in keyword_lower for term in ["neighborhood", "area", "location"]) and any(term in keyword_lower for term in ["investment", "roi", "rental"]):
                    clusters["location_analysis"]["keywords"].append(kw)
                    assigned = True
                elif any(term in keyword_lower for term in ["tool", "spreadsheet", "template", "checklist", "guide"]):
                    clusters["tools_resources"]["keywords"].append(kw)
                    assigned = True
                
                # Default to most relevant cluster
                if not assigned:
                    if kw.get("category") == "roi_analysis":
                        clusters["roi_calculators"]["keywords"].append(kw)
                    elif kw.get("category") == "comparison":
                        clusters["rental_comparison"]["keywords"].append(kw)
                    elif kw.get("category") == "market_analysis":
                        clusters["market_data"]["keywords"].append(kw)
                    else:
                        clusters["location_analysis"]["keywords"].append(kw)
            else:
                # Home buyer clustering (original logic)
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