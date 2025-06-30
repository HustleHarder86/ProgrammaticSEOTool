"""Seed keyword and variation generator for true programmatic SEO"""
from typing import List, Dict, Any
import itertools

class SeedKeywordGenerator:
    def __init__(self):
        # Generic seed templates adaptable to any business
        self.generic_templates = {
            "location_based": {
                "templates": [
                    "{location} {service}",
                    "best {service} in {location}",
                    "{service} near me {location}",
                    "{location} {service} {metric}",
                    "top {service} {location} {year}",
                    "{service} {location} reviews",
                    "{location} vs {location2} {service}",
                    "affordable {service} {location}",
                    "{service} {location} {price_range}",
                    "{location} {service} {business_attribute}"
                ],
                "variables": {
                    "location": [],  # Will be populated dynamically
                    "service": [],  # Will be populated based on business
                    "metric": [
                        "cost", "prices", "reviews", "ratings", "comparison",
                        "guide", "tips", "benefits", "pros and cons"
                    ],
                    "year": ["2024", "2025"],
                    "price_range": [
                        "budget", "cheap", "affordable", "premium", "luxury"
                    ],
                    "business_attribute": [
                        "hours", "location", "services", "specialties", "expertise"
                    ]
                }
            },
            "comparison_based": {
                "templates": [
                    "{item1} vs {item2}",
                    "{item1} or {item2} which is better",
                    "compare {item1} and {item2} {metric}",
                    "{item1} vs {item2} for {use_case}",
                    "difference between {item1} and {item2}",
                    "{item1} alternatives to {item2}"
                ],
                "variables": {
                    "item1": [],  # Will be populated based on business
                    "item2": [],  # Will be populated based on business
                    "metric": ["features", "pricing", "performance", "quality", "value"],
                    "use_case": []  # Will be populated based on business
                }
            },
            "how_to_based": {
                "templates": [
                    "how to {action} {topic}",
                    "how to {action} {topic} {modifier}",
                    "guide to {action} {topic}",
                    "step by step {action} {topic}",
                    "tutorial {action} {topic}",
                    "{action} {topic} for beginners",
                    "best way to {action} {topic}"
                ],
                "variables": {
                    "action": [],  # Will be populated based on business
                    "topic": [],  # Will be populated based on business
                    "modifier": [
                        "quickly", "easily", "professionally", "cheaply", 
                        "without experience", "like a pro", "in 2024"
                    ]
                }
            },
            "tool_based": {
                "templates": [
                    "{tool_type} for {use_case}",
                    "free {tool_type} {modifier}",
                    "best {tool_type} {year}",
                    "{tool_type} {platform}",
                    "{tool_type} vs {tool_type2}",
                    "how to use {tool_type}"
                ],
                "variables": {
                    "tool_type": [],  # Will be populated based on business
                    "use_case": [],  # Will be populated based on business
                    "modifier": ["online", "download", "app", "software", "tool"],
                    "platform": ["windows", "mac", "ios", "android", "web"],
                    "year": ["2024", "2025"]
                }
            },
            "question_based": {
                "templates": [
                    "what is {topic}",
                    "why {question} {topic}",
                    "when to {action} {topic}",
                    "where to {action} {topic}",
                    "is {topic} {attribute}",
                    "can {topic} {capability}",
                    "should I {action} {topic}"
                ],
                "variables": {
                    "topic": [],  # Will be populated based on business
                    "question": ["use", "choose", "buy", "try", "consider"],
                    "action": [],  # Will be populated based on business
                    "attribute": ["worth it", "legit", "safe", "reliable", "good"],
                    "capability": []  # Will be populated based on business
                }
            }
        }
        
        # Industry-specific examples (for reference)
        self.industry_examples = {
            "real_estate": {
                "service": ["homes", "condos", "apartments", "real estate", "properties"],
                "action": ["buy", "sell", "rent", "invest in", "find"],
                "tool_type": ["calculator", "analyzer", "estimator", "tracker"]
            },
            "ecommerce": {
                "service": ["products", "deals", "shipping", "returns"],
                "action": ["shop", "buy", "order", "return", "track"],
                "tool_type": ["price tracker", "comparison tool", "coupon finder"]
            },
            "saas": {
                "service": ["software", "platform", "solution", "tool"],
                "action": ["integrate", "setup", "use", "optimize", "migrate"],
                "tool_type": ["integration", "api", "plugin", "extension"]
            },
            "local_business": {
                "service": ["service", "repair", "installation", "consultation"],
                "action": ["book", "schedule", "find", "hire", "contact"],
                "tool_type": ["booking system", "scheduler", "locator", "directory"]
            }
        }

    def generate_location_list(self, base_location: str = None, include_nearby: bool = True, 
                              market_context: str = None, location_list: str = None) -> List[str]:
        """Generate flexible location list based on provided context"""
        
        locations = []
        
        # If specific locations provided, use those
        if location_list:
            # Parse comma-separated locations
            locations = [loc.strip() for loc in location_list.split(',') if loc.strip()]
            
            # Add variations if requested
            if include_nearby:
                base_locations = locations.copy()
                for loc in base_locations:
                    # Add common variations
                    locations.append(f"near {loc}")
                    locations.append(f"{loc} area")
                    
                    # Add market context if provided
                    if market_context:
                        locations.append(f"{loc} {market_context}")
        
        # If no specific list but base location provided
        elif base_location:
            locations = [base_location]
            
            # Add generic nearby variations
            if include_nearby:
                locations.extend([
                    f"{base_location} downtown",
                    f"{base_location} suburbs",
                    f"near {base_location}",
                    f"{base_location} area",
                    f"greater {base_location}"
                ])
                
                # Add market context variations
                if market_context:
                    locations.extend([
                        f"{base_location} {market_context}",
                        f"{market_context} {base_location}"
                    ])
        
        # Default fallback
        if not locations:
            locations = ["online", "remote", "virtual", "nationwide"]
        
        return locations

    def calculate_variations(self, seed_config: Dict) -> int:
        """Calculate total number of variations from a seed configuration"""
        total = 1
        for var_name, var_values in seed_config["variables"].items():
            if var_values:  # Only count non-empty lists
                total *= len(var_values)
        return total * len(seed_config["templates"])

    def generate_from_seeds(self, seeds: List[Dict], business_info: Dict = None, 
                           market_context: Dict = None) -> Dict[str, Any]:
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
        
        # Get locations from context
        location = market_context.get('location', 'online') if market_context else 'online'
        location_list = market_context.get('location_list', '') if market_context else ''
        market_region = market_context.get('market_region', '') if market_context else ''
        
        locations = self.generate_location_list(
            base_location=location,
            location_list=location_list,
            market_context=market_region
        )
        
        # Populate business-specific variables
        business_variables = self._extract_business_variables(business_info)
        
        for seed in seeds:
            category = seed["category"]
            template_group = seed["template_group"]
            
            # Get the template configuration
            config = self.generic_templates.get(category, {}).copy()
            
            if not config:
                continue
                
            # Populate variables with business-specific data
            for var_name in config["variables"]:
                if var_name == "location":
                    config["variables"]["location"] = locations
                elif var_name == "location2":
                    config["variables"]["location2"] = locations[1:6] if len(locations) > 1 else locations
                elif var_name in business_variables:
                    config["variables"][var_name] = business_variables[var_name]
                elif not config["variables"][var_name]:  # Empty list
                    # Use generic fallbacks
                    config["variables"][var_name] = self._get_generic_variables(var_name)
            
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

    def get_seed_suggestions(self, business_info: Dict = None) -> List[Dict]:
        """Get generic seed suggestions adaptable to any business"""
        
        # Extract business context
        business_name = business_info.get('name', 'business') if business_info else 'business'
        industry = business_info.get('industry', '').lower() if business_info else ''
        
        # Generic suggestions that adapt to any business
        suggestions = [
            {
                "name": "Location-Based Keywords",
                "category": "location_based",
                "template_group": "location_services",
                "estimated_keywords": "500-2000 per location",
                "description": f"Generate location-specific keywords for {business_name}",
                "example": f"best {business_name} in Austin, {business_name} near me New York",
                "id": "location_based"
            },
            {
                "name": "Comparison Keywords",
                "category": "comparison_based",
                "template_group": "vs_comparisons",
                "estimated_keywords": "200-800",
                "description": "Compare your business with competitors or alternatives",
                "example": f"{business_name} vs competitors, alternatives to {business_name}",
                "id": "comparison_based"
            },
            {
                "name": "How-To & Guide Keywords",
                "category": "how_to_based",
                "template_group": "guides",
                "estimated_keywords": "300-1500",
                "description": "Educational content around your products/services",
                "example": f"how to use {business_name}, guide to {business_name} features",
                "id": "how_to_based"
            },
            {
                "name": "Tool & Calculator Keywords",
                "category": "tool_based",
                "template_group": "tools",
                "estimated_keywords": "200-1000",
                "description": "Keywords for tools, calculators, and resources",
                "example": f"{business_name} calculator, free {business_name} tool",
                "id": "tool_based"
            },
            {
                "name": "Question-Based Keywords",
                "category": "question_based",
                "template_group": "questions",
                "estimated_keywords": "400-2000",
                "description": "Answer common questions about your business",
                "example": f"what is {business_name}, is {business_name} worth it",
                "id": "question_based"
            }
        ]
        
        return suggestions
    
    def _extract_business_variables(self, business_info: Dict) -> Dict[str, List[str]]:
        """Extract variables from business info for seed templates"""
        if not business_info:
            return {}
            
        variables = {}
        
        # Extract service/product names
        business_name = business_info.get('name', 'service')
        description = business_info.get('description', '')
        
        # Basic service variations
        variables['service'] = [
            business_name.lower(),
            business_name.lower().replace(' ', ''),
            business_name.lower().replace(' ', '-')
        ]
        
        # Extract actions based on business type
        if 'software' in description.lower() or 'app' in description.lower():
            variables['action'] = ['use', 'install', 'setup', 'integrate', 'optimize']
            variables['tool_type'] = ['software', 'app', 'platform', 'tool', 'solution']
        elif 'service' in description.lower():
            variables['action'] = ['book', 'hire', 'find', 'choose', 'compare']
            variables['tool_type'] = ['service', 'provider', 'company', 'professional']
        else:
            variables['action'] = ['get', 'find', 'choose', 'buy', 'use']
            variables['tool_type'] = ['solution', 'option', 'choice', 'provider']
            
        # Common use cases
        variables['use_case'] = [
            'small business', 'enterprise', 'startups', 'personal use',
            'professionals', 'teams', 'freelancers'
        ]
        
        # Extract from content types if available
        content_types = business_info.get('content_types', [])
        if content_types:
            variables['topic'] = [ct.replace(' ', '-') for ct in content_types[:5]]
        else:
            variables['topic'] = [business_name.lower()]
            
        # Items for comparison
        variables['item1'] = variables['service'][:3]
        variables['item2'] = ['competitor', 'alternative', 'other-option']
        
        # Capabilities
        variables['capability'] = [
            'help', 'improve', 'automate', 'simplify', 'enhance'
        ]
        
        return variables
    
    def _get_generic_variables(self, var_name: str) -> List[str]:
        """Get generic fallback variables"""
        generic_vars = {
            'service': ['service', 'product', 'solution'],
            'action': ['use', 'get', 'find', 'choose'],
            'topic': ['features', 'benefits', 'options'],
            'tool_type': ['tool', 'resource', 'solution'],
            'use_case': ['business', 'personal', 'professional'],
            'item1': ['option1', 'choice1', 'solution1'],
            'item2': ['option2', 'choice2', 'solution2']
        }
        return generic_vars.get(var_name, [var_name])