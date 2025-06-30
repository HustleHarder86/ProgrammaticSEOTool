"""Seed keyword and variation generator for true programmatic SEO"""
from typing import List, Dict, Any
import itertools

class SeedKeywordGenerator:
    def __init__(self):
        # Real estate seed templates
        self.seed_templates = {
            "location_based": {
                "templates": [
                    "{location} {property_type} for sale",
                    "{location} {property_type} rental income",
                    "best {location} neighborhoods for {investment_type}",
                    "{location} real estate market {metric}",
                    "{property_type} in {location} {price_range}",
                    "{location} {property_type} roi calculator",
                    "is {location} good for {investment_type}",
                    "{location} vs {location2} real estate investment",
                    "{location} {property_type} cap rate",
                    "{location} rental property {analysis_type}"
                ],
                "variables": {
                    "location": [],  # Will be populated dynamically
                    "property_type": [
                        "condo", "townhouse", "single family home", "duplex", 
                        "multifamily", "apartment building", "commercial property"
                    ],
                    "investment_type": [
                        "airbnb", "long term rental", "short term rental", 
                        "student housing", "section 8", "vacation rental"
                    ],
                    "metric": [
                        "analysis", "trends 2024", "forecast 2025", "statistics",
                        "appreciation rate", "rental demand", "inventory levels"
                    ],
                    "price_range": [
                        "under 200k", "under 300k", "under 500k", "luxury",
                        "starter homes", "fixer uppers", "turnkey"
                    ],
                    "analysis_type": [
                        "cash flow analysis", "expense calculator", "profit calculator",
                        "management costs", "tax benefits", "depreciation schedule"
                    ]
                }
            },
            "comparison_based": {
                "templates": [
                    "{item1} vs {item2} for {purpose}",
                    "compare {item1} and {item2} {metric}",
                    "{item1} or {item2} better for {user_type}",
                    "{item1} vs {item2} {location}"
                ],
                "variables": {
                    "item1": ["airbnb", "vrbo", "long term rental", "flip"],
                    "item2": ["long term rental", "short term rental", "hotel", "traditional rental"],
                    "purpose": ["passive income", "cash flow", "appreciation", "tax benefits"],
                    "user_type": ["beginners", "retirees", "remote workers", "investors"],
                    "metric": ["roi", "profitability", "risk", "management effort"]
                }
            },
            "tool_based": {
                "templates": [
                    "{tool_type} calculator for {location}",
                    "free {tool_type} spreadsheet {location}",
                    "{location} {tool_type} analysis tool",
                    "best {tool_type} software for {user_type}"
                ],
                "variables": {
                    "tool_type": [
                        "rental property roi", "airbnb income", "cap rate",
                        "cash flow", "mortgage", "1031 exchange", "depreciation"
                    ],
                    "user_type": ["real estate agents", "property investors", "landlords"]
                }
            }
        }
        
        # B2B Realtor Templates
        self.b2b_templates = {
            "agent_tools": {
                "templates": [
                    "{tool} for real estate agents in {location}",
                    "best {tool} for {agent_type} realtors",
                    "how to use {tool} to {goal}",
                    "{tool} vs {tool2} for real estate agents"
                ],
                "variables": {
                    "tool": [
                        "investment property analyzer", "rental calculator",
                        "roi calculator", "market analysis tool", "cma software"
                    ],
                    "agent_type": ["new", "experienced", "luxury", "commercial"],
                    "goal": [
                        "win more listings", "attract investors", "close deals faster",
                        "analyze investments", "present to clients"
                    ],
                    "tool2": ["spreadsheets", "manual calculations", "competitor tools"]
                }
            }
        }

    def generate_location_list(self, base_location: str, include_nearby: bool = True) -> List[str]:
        """Generate comprehensive location list"""
        locations = [base_location]
        
        # Add state if city provided
        city_state_map = {
            "Austin": "Texas", "Dallas": "Texas", "Houston": "Texas",
            "Phoenix": "Arizona", "Denver": "Colorado", "Miami": "Florida",
            "Seattle": "Washington", "Portland": "Oregon", "Nashville": "Tennessee"
        }
        
        if base_location in city_state_map:
            state = city_state_map[base_location]
            locations.append(f"{base_location} TX")  # Short form
            locations.append(f"{base_location} {state}")  # Full state
            
            # Add neighborhoods (simplified - in production use real data)
            neighborhoods = {
                "Austin": ["Downtown Austin", "East Austin", "South Austin", "North Austin",
                          "Zilker", "Hyde Park", "Mueller", "Domain", "Westlake", "Lakeway"],
                "Dallas": ["Uptown Dallas", "Downtown Dallas", "Highland Park", "Preston Hollow",
                          "Deep Ellum", "Bishop Arts", "Knox Henderson", "Lakewood"],
                # Add more cities...
            }
            
            if base_location in neighborhoods:
                locations.extend(neighborhoods[base_location])
            
            # Add nearby cities
            nearby_cities = {
                "Austin": ["Round Rock", "Cedar Park", "Pflugerville", "Georgetown", "Dripping Springs"],
                "Dallas": ["Plano", "Frisco", "Richardson", "Arlington", "Fort Worth"],
                # Add more...
            }
            
            if include_nearby and base_location in nearby_cities:
                locations.extend(nearby_cities[base_location])
        
        return locations

    def calculate_variations(self, seed_config: Dict) -> int:
        """Calculate total number of variations from a seed configuration"""
        total = 1
        for var_name, var_values in seed_config["variables"].items():
            if var_values:  # Only count non-empty lists
                total *= len(var_values)
        return total * len(seed_config["templates"])

    def generate_from_seeds(self, seeds: List[Dict], location: str = "Austin") -> Dict[str, Any]:
        """Generate all keyword variations from seed configurations"""
        results = {
            "summary": {
                "total_seeds": len(seeds),
                "total_variations": 0,
                "by_category": {}
            },
            "keywords": [],
            "seed_details": []
        }
        
        # Populate locations
        locations = self.generate_location_list(location)
        
        for seed in seeds:
            category = seed["category"]
            template_group = seed["template_group"]
            
            # Get the template configuration
            if category == "location_based":
                config = self.seed_templates["location_based"].copy()
                config["variables"]["location"] = locations
                
                # Handle location2 for comparison templates
                if "{location2}" in str(config["templates"]):
                    config["variables"]["location2"] = locations[1:6]  # Different locations for comparison
            
            elif category == "comparison_based":
                config = self.seed_templates["comparison_based"].copy()
                if seed.get("include_location"):
                    config["variables"]["location"] = locations[:5]  # Limit for comparisons
            
            elif category == "tool_based":
                config = self.seed_templates["tool_based"].copy()
                config["variables"]["location"] = locations
            
            elif category == "b2b_agent":
                config = self.b2b_templates["agent_tools"].copy()
                config["variables"]["location"] = locations[:10]  # Focus on main areas
            
            else:
                continue
            
            # Calculate variations for this seed
            variation_count = self.calculate_variations(config)
            
            seed_detail = {
                "category": category,
                "template_count": len(config["templates"]),
                "variable_combinations": variation_count // len(config["templates"]),
                "total_variations": variation_count,
                "templates": config["templates"][:3] + ["..."] if len(config["templates"]) > 3 else config["templates"]
            }
            
            results["seed_details"].append(seed_detail)
            results["summary"]["total_variations"] += variation_count
            
            if category not in results["summary"]["by_category"]:
                results["summary"]["by_category"][category] = 0
            results["summary"]["by_category"][category] += variation_count
            
            # Generate sample keywords (first 10 from each seed)
            generated = self._generate_keywords_from_config(config, limit=10)
            for kw in generated:
                results["keywords"].append({
                    "keyword": kw,
                    "seed_category": category,
                    "seed_template": template_group
                })
        
        return results

    def _generate_keywords_from_config(self, config: Dict, limit: int = None) -> List[str]:
        """Generate actual keywords from a configuration"""
        keywords = []
        count = 0
        
        for template in config["templates"]:
            # Extract variable names from template
            import re
            var_names = re.findall(r'\{(\w+)\}', template)
            
            if not var_names:
                keywords.append(template)
                continue
            
            # Get variable values
            var_values = []
            for var in var_names:
                if var in config["variables"] and config["variables"][var]:
                    var_values.append(config["variables"][var])
                else:
                    var_values.append([var])  # Use variable name as placeholder
            
            # Generate combinations
            for combination in itertools.product(*var_values):
                if limit and count >= limit:
                    return keywords
                
                # Create keyword by replacing variables
                keyword = template
                for var_name, var_value in zip(var_names, combination):
                    keyword = keyword.replace(f"{{{var_name}}}", var_value)
                
                keywords.append(keyword)
                count += 1
        
        return keywords

    def get_seed_suggestions(self, business_type: str = "real_estate") -> List[Dict]:
        """Get suggested seed configurations based on business type"""
        if business_type == "real_estate_investment":
            return [
                {
                    "name": "Location-Based Property Analysis",
                    "category": "location_based",
                    "template_group": "property_analysis",
                    "estimated_keywords": "500-2000 per city",
                    "description": "Generate location-specific property investment keywords",
                    "example": "Austin condo rental income, Dallas townhouse roi calculator"
                },
                {
                    "name": "Investment Strategy Comparisons",
                    "category": "comparison_based",
                    "template_group": "strategy_comparison",
                    "estimated_keywords": "200-500",
                    "description": "Compare different investment strategies",
                    "example": "airbnb vs long term rental for passive income"
                },
                {
                    "name": "ROI Calculators by Location",
                    "category": "tool_based",
                    "template_group": "calculators",
                    "estimated_keywords": "300-1000",
                    "description": "Location-specific calculator keywords",
                    "example": "rental property roi calculator for Austin"
                },
                {
                    "name": "Agent Tools & Resources",
                    "category": "b2b_agent",
                    "template_group": "agent_tools",
                    "estimated_keywords": "200-500",
                    "description": "B2B keywords for real estate professionals",
                    "example": "best investment property analyzer for real estate agents"
                }
            ]
        
        return []