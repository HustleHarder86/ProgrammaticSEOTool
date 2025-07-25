"""Template and page generator for true programmatic SEO - creates pages at scale using templates + data"""
from typing import List, Dict, Any, Optional
import itertools
import pandas as pd
import json
import csv
from io import StringIO

class TemplateGenerator:
    def __init__(self):
        # Template library for programmatic SEO - adaptable to any business
        self.template_library = {
            "location_based": {
                "templates": [
                    "{service} {location}",
                    "best {service} in {location}",
                    "{service} near me",
                    "{location} {service} cost",
                    "{service} {location} prices",
                    "{service} {location} reviews",
                    "cheap {service} {location}",
                    "{service} companies {location}",
                    "{location} {service} near me",
                    "find {service} in {location}"
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
            "problem_solution": {
                "templates": [
                    "how to fix {problem}",
                    "{problem} solutions",
                    "solve {problem}",
                    "fix {problem} fast",
                    "best way to fix {problem}",
                    "{problem} troubleshooting",
                    "{problem} not working",
                    "why is my {problem}"
                ],
                "variables": {
                    "problem": [],  # Will be populated based on business
                    "solution": [],  # Will be populated based on business
                    "audience": ["beginners", "professionals", "small business", "enterprises"],
                    "method": [],  # Will be populated based on business
                    "solution_type": ["software", "service", "tool", "guide", "checklist"],
                    "solve": ["fix", "resolve", "handle", "manage", "overcome"],
                    "avoid": ["expensive tools", "technical knowledge", "hiring experts"],
                    "year": ["2024", "2025"]
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
            },
            "integration_based": {
                "templates": [
                    "{product} integration with {platform}",
                    "how to connect {product} to {platform}",
                    "{product} {platform} API",
                    "{product} and {platform} workflow",
                    "sync {product} with {platform}"
                ],
                "variables": {
                    "product": [],  # Will be populated based on business
                    "platform": ["Salesforce", "HubSpot", "Slack", "Google Workspace", "Microsoft 365", "Zapier", "Stripe", "QuickBooks"]
                }
            },
            "pricing_based": {
                "templates": [
                    "{product} pricing {year}",
                    "{product} {plan_type} plan",
                    "is {product} {price_attribute}",
                    "{product} cost for {user_type}",
                    "{product} pricing vs {competitor}"
                ],
                "variables": {
                    "product": [],  # Will be populated based on business
                    "plan_type": ["free", "starter", "pro", "enterprise", "basic", "premium"],
                    "price_attribute": ["free", "worth it", "expensive", "affordable"],
                    "user_type": ["small business", "startups", "enterprises", "freelancers"],
                    "competitor": [],  # Will be populated based on business
                    "year": ["2024", "2025"]
                }
            },
            "product_based": {
                "templates": [
                    "best {product_type} for {use_case}",
                    "{product_type} {attribute} {year}",
                    "top {number} {product_type} {category}",
                    "{product_type} under {price}",
                    "{product_type} with {feature}"
                ],
                "variables": {
                    "product_type": [],  # Will be populated based on business
                    "use_case": ["beginners", "professionals", "students", "home use", "business"],
                    "attribute": ["reviews", "comparison", "guide", "recommendations"],
                    "number": ["10", "5", "20", "15"],
                    "category": ["2024", "budget", "premium", "new"],
                    "price": ["$50", "$100", "$200", "$500"],
                    "feature": [],  # Will be populated based on business
                    "year": ["2024", "2025"]
                }
            },
            "deals_based": {
                "templates": [
                    "{product} {deal_type} {time_period}",
                    "{product} promo code {year}",
                    "{product} {percent} off",
                    "save on {product} {method}",
                    "{product} {holiday} sale"
                ],
                "variables": {
                    "product": [],  # Will be populated based on business
                    "deal_type": ["coupon", "discount", "deals", "sale", "clearance"],
                    "time_period": ["today", "this week", "this month", "2024", "2025"],
                    "percent": ["10%", "20%", "30%", "50%", "25%"],
                    "method": ["student discount", "bulk pricing", "annual plan", "referral"],
                    "holiday": ["black friday", "cyber monday", "christmas", "new year"],
                    "year": ["2024", "2025"]
                }
            },
            "service_based": {
                "templates": [
                    "{service} for {business_type}",
                    "{location} {service} {specialization}",
                    "hire {service} {modifier}",
                    "{service} {price_range} {location}",
                    "find {service} near {location}"
                ],
                "variables": {
                    "service": [],  # Will be populated based on business
                    "business_type": ["small business", "startups", "enterprises", "nonprofits", "agencies"],
                    "location": [],  # Will be populated if location-based
                    "specialization": [],  # Will be populated based on business
                    "modifier": ["online", "remote", "local", "certified", "experienced"],
                    "price_range": ["affordable", "cheap", "premium", "budget-friendly"]
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
        
        # Store imported data sources
        self.data_sources = {}
        # Store generated pages  
        self.generated_pages = []

    def import_data_from_csv(self, csv_content: str, data_name: str) -> Dict[str, List[str]]:
        """Import data from CSV for template variables"""
        try:
            # Parse CSV
            df = pd.read_csv(StringIO(csv_content))
            
            # Extract columns as data sources
            data = {}
            for column in df.columns:
                # Clean and store unique values
                values = df[column].dropna().unique().tolist()
                data[column.lower().replace(' ', '_')] = [str(v).strip() for v in values]
            
            # Store for later use
            self.data_sources[data_name] = data
            return data
            
        except Exception as e:
            print(f"Error importing CSV: {e}")
            return {}
    
    def create_template(self, name: str, pattern: str, page_structure: Dict[str, str]) -> Dict:
        """Create a custom template for page generation"""
        # Extract variables from pattern
        import re
        variables = re.findall(r'\{(\w+)\}', pattern)
        
        template = {
            "name": name,
            "pattern": pattern,
            "variables": variables,
            "page_structure": page_structure,
            "url_pattern": pattern.lower().replace(' ', '-').replace('{', '').replace('}', '')
        }
        
        # Add to library
        self.template_library[name] = template
        return template
    
    def generate_pages_from_template(self, template_name: str, data: Dict[str, List[str]], 
                                   limit: int = None) -> List[Dict]:
        """Generate all page combinations from template + data"""
        template = self.template_library.get(template_name)
        if not template:
            print(f"Template '{template_name}' not found")
            return []
        
        # Get pattern and variables
        pattern = template.get('pattern', template.get('templates', [''])[0])
        variables = template.get('variables', [])
        
        # Ensure all variables have data
        variable_data = []
        for var in variables:
            if var in data:
                variable_data.append(data[var])
            else:
                print(f"Warning: No data provided for variable '{var}'")
                variable_data.append([''])
        
        # Generate all combinations
        pages = []
        for combo in itertools.product(*variable_data):
            # Create page from template
            page_data = {}
            variable_map = dict(zip(variables, combo))
            
            # Generate title
            title = pattern
            for var, val in variable_map.items():
                title = title.replace(f'{{{var}}}', val)
            
            # Generate URL
            url = title.lower().replace(' ', '-')
            
            # Generate meta description
            meta_desc = f"Explore {title}. Find information, resources, and tools."
            
            # Store page data
            page_data = {
                'title': title,
                'url': f"/{url}",
                'meta_description': meta_desc,
                'variables': variable_map,
                'template': template_name
            }
            
            pages.append(page_data)
            
            if limit and len(pages) >= limit:
                break
        
        self.generated_pages = pages
        return pages

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
            config = self.template_library.get(category, {}).copy()
            
            if not config:
                print(f"Warning: No template found for category '{category}' - trying AI regeneration")
                # Try to regenerate this specific template with AI
                try:
                    from .ai_handler import AIHandler
                    ai = AIHandler()
                    if ai.has_ai_provider():
                        # Generate template specifically for this category with market context
                        ai_template = self._generate_single_template_with_ai(category, business_info, ai, market_context)
                        if ai_template:
                            config = ai_template
                            # Store for future use in this session
                            self.template_library[category] = config
                        else:
                            print(f"AI failed to generate template for '{category}' - skipping")
                            continue
                    else:
                        print(f"No AI available to regenerate template for '{category}' - skipping")
                        continue
                except Exception as e:
                    print(f"Error regenerating template for '{category}': {e} - skipping")
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
            print(f"Category '{category}': {len(config['templates'])} templates, {variation_count} total variations")
            
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
            
            # Generate keywords (limit based on total variations)
            # For large variation counts, generate a reasonable sample
            max_per_seed = min(variation_count, 500)  # Cap at 500 per seed to avoid timeout
            generated = self._generate_keywords_from_config(config, limit=max_per_seed)
            
            print(f"Generated {len(generated)} keywords for category '{category}'")
            
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

    def get_template_suggestions(self, business_info: Dict = None, use_ai: bool = True, market_context: Dict = None) -> List[Dict]:
        """Get intelligent seed suggestions based on business type"""
        
        if not business_info:
            return []
            
        # Try AI-generated templates first
        if use_ai:
            try:
                from .ai_handler import AIHandler
                ai = AIHandler()
                if ai.has_ai_provider():
                    print(f"Attempting comprehensive AI template generation for business: {business_info.get('name', 'Unknown')}")
                    ai_suggestions = self._get_ai_template_suggestions(business_info, ai, market_context)
                    if ai_suggestions:
                        print(f"AI generated {len(ai_suggestions)} suggestions successfully")
                        return ai_suggestions
                    else:
                        print("AI returned empty suggestions - falling back to generic")
                else:
                    print("No AI provider available - falling back to generic")
            except Exception as e:
                print(f"AI template generation failed: {e}")
                import traceback
                traceback.print_exc()
        
        # Extract business context (fallback to generic)
        business_name = business_info.get('name', 'business')
        industry = business_info.get('industry', '').lower()
        description = business_info.get('description', '').lower()
        services = business_info.get('services', [])
        
        # Determine business characteristics
        is_local = self._is_location_dependent(industry, description)
        is_saas = self._is_software_service(industry, description)
        is_ecommerce = self._is_ecommerce(industry, description)
        is_professional = self._is_professional_service(industry, description)
        is_educational = self._is_educational(industry, description)
        
        suggestions = []
        
        # Location-based (only for location-dependent businesses)
        if is_local:
            suggestions.append({
                "name": "📍 Location-Based Keywords",
                "category": "location_based",
                "template_group": "location_services",
                "estimated_keywords": "500-3000 per location",
                "description": f"Target local searches for {business_name}",
                "example": f"best {business_name} in [city], {business_name} near me",
                "id": "location_based",
                "relevance": "high",
                "templates": self._get_location_templates(industry)
            })
        
        # Comparison keywords (relevant for most businesses)
        if is_saas or is_ecommerce or is_professional:
            suggestions.append({
                "name": "⚖️ Comparison & Alternative Keywords",
                "category": "comparison_based",
                "template_group": "vs_comparisons",
                "estimated_keywords": "300-1200",
                "description": "Capture users comparing solutions",
                "example": f"{business_name} vs [competitor], alternatives to {business_name}",
                "id": "comparison_based",
                "relevance": "high" if is_saas else "medium",
                "templates": self._get_comparison_templates(industry)
            })
        
        # How-to content (based on business type)
        if is_saas or is_educational or is_professional:
            suggestions.append({
                "name": "📚 How-To & Tutorial Keywords",
                "category": "how_to_based",
                "template_group": "guides",
                "estimated_keywords": "400-2000",
                "description": "Educational content for your audience",
                "example": self._get_howto_example(business_name, industry),
                "id": "how_to_based",
                "relevance": "high",
                "templates": self._get_howto_templates(industry)
            })
        
        # Problem/Solution keywords
        suggestions.append({
            "name": "🎯 Problem & Solution Keywords",
            "category": "problem_solution",
            "template_group": "solutions",
            "estimated_keywords": "500-2500",
            "description": "Target users searching for solutions",
            "example": self._get_problem_example(business_name, industry),
            "id": "problem_solution",
            "relevance": "high",
            "templates": self._get_problem_templates(industry)
        })
        
        # Industry-specific templates
        if is_saas:
            suggestions.extend(self._get_saas_specific_suggestions(business_name))
        elif is_ecommerce:
            suggestions.extend(self._get_ecommerce_specific_suggestions(business_name))
        elif is_professional:
            suggestions.extend(self._get_professional_specific_suggestions(business_name, industry))
        
        # Question-based (universal but customized)
        suggestions.append({
            "name": "❓ Question-Based Keywords",
            "category": "question_based",
            "template_group": "questions",
            "estimated_keywords": "300-1500",
            "description": "Answer common questions in your industry",
            "example": self._get_question_example(business_name, industry),
            "id": "question_based",
            "relevance": "medium",
            "templates": self._get_question_templates(industry)
        })
        
        # Sort by relevance
        suggestions.sort(key=lambda x: {"high": 0, "medium": 1, "low": 2}.get(x.get("relevance", "medium"), 1))
        
        return suggestions
    
    def _is_location_dependent(self, industry: str, description: str) -> bool:
        """Check if business depends on location"""
        location_keywords = [
            'real estate', 'restaurant', 'clinic', 'hospital', 'store', 'shop',
            'service', 'repair', 'salon', 'gym', 'fitness', 'dental', 'medical',
            'law firm', 'accounting', 'local', 'contractor', 'plumber', 'electrician'
        ]
        return any(keyword in industry or keyword in description for keyword in location_keywords)
    
    def _is_software_service(self, industry: str, description: str) -> bool:
        """Check if business is SaaS/software"""
        saas_keywords = [
            'software', 'saas', 'app', 'platform', 'tool', 'api', 'cloud',
            'automation', 'crm', 'management system', 'analytics', 'dashboard'
        ]
        return any(keyword in industry or keyword in description for keyword in saas_keywords)
    
    def _is_ecommerce(self, industry: str, description: str) -> bool:
        """Check if business is e-commerce"""
        ecommerce_keywords = [
            'ecommerce', 'e-commerce', 'online store', 'shop', 'marketplace',
            'products', 'selling', 'retail', 'wholesale', 'dropship'
        ]
        return any(keyword in industry or keyword in description for keyword in ecommerce_keywords)
    
    def _is_professional_service(self, industry: str, description: str) -> bool:
        """Check if business is professional service"""
        prof_keywords = [
            'consulting', 'agency', 'law', 'legal', 'accounting', 'financial',
            'marketing', 'design', 'development', 'freelance', 'coaching'
        ]
        return any(keyword in industry or keyword in description for keyword in prof_keywords)
    
    def _is_educational(self, industry: str, description: str) -> bool:
        """Check if business is educational"""
        edu_keywords = [
            'education', 'course', 'training', 'tutorial', 'learning',
            'academy', 'school', 'certification', 'workshop', 'bootcamp'
        ]
        return any(keyword in industry or keyword in description for keyword in edu_keywords)
    
    def _get_location_templates(self, industry: str) -> List[str]:
        """Get location templates based on industry"""
        if 'real estate' in industry:
            return [
                "{location} {property_type} for {purpose}",
                "{property_type} in {location} {price_range}",
                "{location} real estate {metric}"
            ]
        elif 'restaurant' in industry or 'food' in industry:
            return [
                "best {cuisine} restaurant in {location}",
                "{location} {meal_type} delivery",
                "restaurants near me in {location}"
            ]
        else:
            return [
                "best {service} in {location}",
                "{service} near me {location}",
                "{location} {service} reviews"
            ]
    
    def _get_comparison_templates(self, industry: str) -> List[str]:
        """Get comparison templates based on industry"""
        if 'software' in industry or 'saas' in industry:
            return [
                "{product} vs {competitor} {year}",
                "{product} alternatives for {use_case}",
                "compare {product} and {competitor} pricing"
            ]
        else:
            return [
                "{service} vs {alternative}",
                "is {service} better than {alternative}",
                "{service} compared to {alternative}"
            ]
    
    def _get_howto_templates(self, industry: str) -> List[str]:
        """Get how-to templates based on industry"""
        if 'software' in industry:
            return [
                "how to {action} with {product}",
                "{product} {feature} tutorial",
                "getting started with {product}"
            ]
        elif 'service' in industry:
            return [
                "how to {achieve_goal} with {service}",
                "guide to {service_type} services",
                "{service} process explained"
            ]
        else:
            return [
                "how to {action} {topic}",
                "step by step {process} guide",
                "{topic} tutorial for beginners"
            ]
    
    def _get_problem_templates(self, industry: str) -> List[str]:
        """Get problem/solution templates"""
        return [
            "how to fix {problem} with {solution}",
            "{problem} solutions for {audience}",
            "solve {problem} using {method}",
            "{audience} {problem} {solution_type}",
            "best way to {solve} {problem}"
        ]
    
    def _get_question_templates(self, industry: str) -> List[str]:
        """Get question templates based on industry"""
        return [
            "what is {concept} in {industry}",
            "why {action} is important for {audience}",
            "when to {action} your {topic}",
            "how much does {service} cost",
            "is {product} worth it for {use_case}"
        ]
    
    def _get_saas_specific_suggestions(self, business_name: str) -> List[Dict]:
        """Get SaaS-specific seed suggestions"""
        return [
            {
                "name": "🔌 Integration & API Keywords",
                "category": "integration_based",
                "template_group": "integrations",
                "estimated_keywords": "200-800",
                "description": "Target integration searches",
                "example": f"{business_name} {{'integration'}} with {{'platform'}}",
                "id": "integration_based",
                "relevance": "high"
            },
            {
                "name": "💰 Pricing & Plans Keywords",
                "category": "pricing_based",
                "template_group": "pricing",
                "estimated_keywords": "100-400",
                "description": "Capture pricing research searches",
                "example": f"{business_name} pricing, {business_name} free trial",
                "id": "pricing_based",
                "relevance": "high"
            }
        ]
    
    def _get_ecommerce_specific_suggestions(self, business_name: str) -> List[Dict]:
        """Get e-commerce specific suggestions"""
        return [
            {
                "name": "🛍️ Product Category Keywords",
                "category": "product_based",
                "template_group": "products",
                "estimated_keywords": "1000-5000",
                "description": "Target product searches",
                "example": "best {{'product_type'}} for {{'use_case'}}",
                "id": "product_based",
                "relevance": "high"
            },
            {
                "name": "💸 Deals & Discount Keywords",
                "category": "deals_based",
                "template_group": "deals",
                "estimated_keywords": "200-1000",
                "description": "Capture bargain hunters",
                "example": f"{business_name} coupon code, {business_name} black friday",
                "id": "deals_based",
                "relevance": "medium"
            }
        ]
    
    def _get_professional_specific_suggestions(self, business_name: str, industry: str) -> List[Dict]:
        """Get professional service specific suggestions"""
        return [
            {
                "name": "💼 Service-Specific Keywords",
                "category": "service_based",
                "template_group": "services",
                "estimated_keywords": "300-1500",
                "description": "Target specific service searches",
                "example": f"{industry} services for {{'business_type'}}",
                "id": "service_based",
                "relevance": "high"
            }
        ]
    
    def _get_howto_example(self, business_name: str, industry: str) -> str:
        """Get relevant how-to example"""
        if 'software' in industry:
            return f"how to integrate {business_name}, {business_name} API tutorial"
        elif 'marketing' in industry:
            return "how to improve SEO, content marketing guide"
        else:
            return f"how to use {business_name}, getting started guide"
    
    def _get_problem_example(self, business_name: str, industry: str) -> str:
        """Get relevant problem/solution example"""
        if 'software' in industry:
            return "fix slow website loading, automate repetitive tasks"
        elif 'health' in industry:
            return "reduce back pain naturally, improve sleep quality"
        else:
            return f"solve {{'problem'}} with {business_name}"
    
    def _get_question_example(self, business_name: str, industry: str) -> str:
        """Get relevant question example"""
        if 'software' in industry:
            return f"what is {business_name}, how much does {business_name} cost"
        else:
            return f"is {business_name} worth it, {business_name} reviews"
    
    def _extract_business_variables(self, business_info: Dict) -> Dict[str, List[str]]:
        """Extract variables from business info for page templates"""
        if not business_info:
            return {}
            
        variables = {}
        
        # Extract basic info
        business_name = business_info.get('name', 'service')
        description = business_info.get('description', '').lower()
        industry = business_info.get('industry', '').lower()
        services = business_info.get('services', [])
        
        # Core business variations
        name_parts = business_name.lower().split()
        variables['service'] = [
            business_name.lower(),
            business_name.lower().replace(' ', ''),
            business_name.lower().replace(' ', '-'),
            name_parts[0] if name_parts else business_name.lower()
        ]
        
        # Product/service names for different contexts
        variables['product'] = variables['service']
        variables['product_type'] = services[:3] if services else variables['service']
        
        # Extract actions based on business type
        actions = business_info.get('customer_actions', [])
        if actions:
            variables['action'] = actions[:5]
        elif 'software' in description or 'saas' in industry:
            variables['action'] = ['use', 'setup', 'integrate', 'optimize', 'configure']
        elif 'service' in description:
            variables['action'] = ['book', 'hire', 'find', 'choose', 'schedule']
        elif 'ecommerce' in industry or 'shop' in description:
            variables['action'] = ['buy', 'order', 'purchase', 'shop', 'find']
        else:
            variables['action'] = ['get', 'find', 'choose', 'learn', 'start']
            
        # Tool types based on business
        if 'software' in industry or 'saas' in industry:
            variables['tool_type'] = ['software', 'app', 'platform', 'tool', 'system']
        elif 'service' in industry:
            variables['tool_type'] = ['service', 'provider', 'professional', 'expert']
        else:
            variables['tool_type'] = ['solution', 'tool', 'resource', 'platform']
            
        # Common use cases
        variables['use_case'] = [
            'small business', 'enterprises', 'startups', 'freelancers',
            'agencies', 'teams', 'individuals', 'professionals'
        ]
        
        # Topics from content types or services
        content_types = business_info.get('content_types', [])
        if content_types:
            variables['topic'] = [ct.lower().replace(' ', '-') for ct in content_types[:5]]
        elif services:
            variables['topic'] = [s.lower().replace(' ', '-') for s in services[:5]]
        else:
            variables['topic'] = [business_name.lower(), 'features', 'benefits']
            
        # Competitors for comparisons
        competitors = business_info.get('competitors', [])
        if competitors:
            variables['item1'] = [business_name.lower()]
            variables['item2'] = [c.lower() for c in competitors[:3]]
            variables['competitor'] = competitors[:3]
        else:
            variables['item1'] = variables['service'][:3]
            variables['item2'] = ['alternative-1', 'alternative-2', 'competitor']
            variables['competitor'] = ['competitor']
        
        # Problems and solutions
        if 'software' in industry:
            variables['problem'] = ['slow processes', 'data silos', 'manual tasks', 'inefficiency', 'errors']
            variables['solution'] = ['automation', 'integration', 'optimization', 'streamlining']
            variables['method'] = ['API', 'automation', 'integration', 'workflow']
        elif 'marketing' in industry:
            variables['problem'] = ['low traffic', 'poor conversion', 'no leads', 'low engagement']
            variables['solution'] = ['SEO', 'content strategy', 'optimization', 'campaigns']
            variables['method'] = ['content marketing', 'SEO', 'social media', 'email']
        else:
            variables['problem'] = ['high costs', 'inefficiency', 'complexity', 'time waste']
            variables['solution'] = [business_name.lower(), 'automation', 'optimization']
            variables['method'] = ['technology', 'expertise', 'tools', 'strategy']
        
        # Capabilities
        variables['capability'] = [
            'help you', 'improve', 'automate', 'simplify', 'enhance',
            'streamline', 'optimize', 'scale'
        ]
        
        # Features (extract from description or use generic)
        if 'features' in business_info:
            variables['feature'] = business_info['features'][:5]
        else:
            variables['feature'] = ['advanced analytics', 'easy integration', 'user-friendly', 'automation']
        
        # Specializations
        if services:
            variables['specialization'] = services[:3]
        else:
            variables['specialization'] = ['expertise', 'solutions', 'services']
        
        # Additional solve variations
        variables['solve'] = ['fix', 'resolve', 'handle', 'eliminate', 'overcome']
        
        return variables
    
    def _get_generic_variables(self, var_name: str) -> List[str]:
        """Get generic fallback variables"""
        generic_vars = {
            'service': ['service', 'product', 'solution', 'software', 'platform'],
            'action': ['use', 'get', 'find', 'choose', 'implement', 'setup'],
            'topic': ['features', 'benefits', 'options', 'capabilities', 'functions'],
            'tool_type': ['tool', 'calculator', 'analyzer', 'tracker', 'dashboard'],
            'use_case': ['business', 'startups', 'enterprises', 'teams', 'projects'],
            'item1': ['option1', 'choice1', 'solution1', 'tool1', 'platform1'],
            'item2': ['option2', 'choice2', 'solution2', 'tool2', 'platform2'],
            'problem': ['challenges', 'issues', 'difficulties', 'problems', 'obstacles'],
            'solution': ['solutions', 'fixes', 'remedies', 'approaches', 'methods'],
            'audience': ['businesses', 'teams', 'professionals', 'users', 'companies'],
            'method': ['approach', 'strategy', 'technique', 'process', 'system'],
            'solve': ['fix', 'resolve', 'address', 'handle', 'overcome'],
            'avoid': ['mistakes', 'errors', 'pitfalls', 'problems', 'issues'],
            'year': ['2024', '2025'],
            'price_range': ['affordable', 'budget', 'premium', 'enterprise', 'free'],
            'modifier': ['best', 'top', 'leading', 'popular', 'recommended'],
            'metric': ['cost', 'price', 'roi', 'performance', 'efficiency'],
            'property_type': ['homes', 'condos', 'apartments', 'properties', 'real estate'],
            'time': ['2024', '2025', 'this year', 'forecast', 'trends']
        }
        return generic_vars.get(var_name, [var_name])
    
    def _get_ai_template_suggestions(self, business_info: Dict, ai_handler, market_context: Dict = None) -> List[Dict]:
        """Generate custom page templates using comprehensive business analysis"""
        
        # First, get comprehensive business analysis like a human would
        print("Performing comprehensive business analysis...")
        comprehensive_analysis = ai_handler.analyze_business_comprehensive(business_info, market_context)
        
        if not comprehensive_analysis:
            print("Comprehensive analysis failed, falling back to basic approach")
            return self._get_basic_ai_template_suggestions(business_info, ai_handler)
        
        # Extract components from ChatGPT-style analysis
        content_opportunities = comprehensive_analysis.get('content_opportunities', '')
        seed_templates = self._extract_seed_templates_from_strategy(content_opportunities, business_info)
        
        if seed_templates:
            print(f"Extracted {len(seed_templates)} page templates from comprehensive strategy")
            return seed_templates
        
        # Fallback: Use AI to generate templates directly from the comprehensive analysis
        prompt = f"""
        Based on this comprehensive programmatic SEO strategy, convert the keyword formulas and components into actionable page templates.

        COMPREHENSIVE SEO STRATEGY:
        {content_opportunities}

        Convert the identified keyword formulas and components into 4-6 page templates for our tool.

        For each template provide:
        1. name: Strategic name with emoji (from the strategy)
        2. category: Unique category ID based on keyword formulas
        3. templates: Keyword patterns using variables (based on formulas like [Location] [Product] [Intent])
        4. variables: Use the location modifiers, business categories, and intent modifiers from the strategy
        5. description: Brief explanation based on the strategy
        6. estimated_keywords: Calculate based on variable combinations
        7. example: Show example keywords from the programmatic page examples

        Extract directly from the provided strategy - don't create new content.
        
        Return as JSON array.
        """
        
        try:
            print(f"Sending AI prompt for business: {business_info.get('name', 'Unknown')}")
            # Use the AI handler's generate method
            response_text = ai_handler.generate(prompt, max_tokens=2000)
            
            if not response_text:
                print("No response from AI")
                return []
            
            print(f"AI response received: {len(response_text)} characters")
            
            # Extract JSON from response
            import json
            import re
            
            content = response_text
            
            # Find JSON array in response
            json_match = re.search(r'\[[\s\S]*\]', content)
            if json_match:
                templates_data = json.loads(json_match.group())
                
                # Format for our system
                suggestions = []
                for template in templates_data:
                    # Ensure all required fields
                    suggestion = {
                        "name": template.get('name', 'Custom Template'),
                        "category": template.get('category', 'custom'),
                        "template_group": template.get('category', 'custom'),
                        "id": template.get('category', 'custom'),
                        "description": template.get('description', ''),
                        "estimated_keywords": template.get('estimated_keywords', '100+'),
                        "example": template.get('example', ''),
                        "relevance": "high",
                        "templates": template.get('templates', []),
                        "variables": template.get('variables', {})
                    }
                    
                    # Add to generic templates for generation
                    self.template_library[suggestion['category']] = {
                        'templates': suggestion['templates'],
                        'variables': suggestion['variables']
                    }
                    
                    suggestions.append(suggestion)
                
                print(f"AI generated {len(suggestions)} custom page templates")
                return suggestions
                
        except Exception as e:
            print(f"Error generating AI seed suggestions: {e}")
            
        # Return empty if AI generation fails
        return []
    
    def _generate_single_template_with_ai(self, category: str, business_info: Dict, ai_handler, market_context: Dict = None) -> Dict:
        """Generate a specific template for a missing category using AI"""
        
        # Extract intelligent market context using AI
        market_intelligence = self._extract_market_intelligence(business_info, market_context, ai_handler)
        
        prompt = f"""
        Generate a programmatic SEO keyword template for '{category}' that matches ACTUAL GOOGLE SEARCHES.
        
        Business Context:
        - Name: {business_info.get('name', 'Unknown')}
        - Industry: {business_info.get('industry', 'Unknown')}
        - Description: {business_info.get('description', 'No description')}
        
        Market Intelligence (AI-extracted):
        {market_intelligence}
        
        CRITICAL RULES:
        1. Templates MUST match queries people actually type into Google
        2. Use the market intelligence to create location/industry-specific searches
        3. Avoid marketing jargon - use customer language
        
        Examples of GOOD search patterns:
        - "{{city}} {{service}} cost" (price searches)
        - "{{product}} reviews {{year}}" (research queries)
        - "how to {{action}} {{topic}}" (how-to searches)
        - "{{item1}} vs {{item2}} comparison" (versus searches)
        - "{{service}} calculator" (tool searches)
        
        Examples of BAD patterns (AVOID):
        - "optimize your {{process}}" (marketing speak)
        - "enhance {{experience}} solutions" (corporate jargon)
        - "streamline {{workflow}} efficiency" (nobody searches this)
        
        Create a template configuration with:
        1. templates: List of 3-5 ACTUAL search query patterns using variables
        2. variables: Dictionary with realistic values from the market intelligence
        
        Focus on '{category}' searches that real people make.
        
        Return as JSON:
        {{
            "templates": ["actual search pattern with {{var1}}", "real query {{var2}} {{var3}}"],
            "variables": {{
                "var1": ["realistic value 1", "realistic value 2"],
                "var2": ["actual term 1", "actual term 2"]
            }}
        }}
        """
        
        try:
            response_text = ai_handler.generate(prompt, max_tokens=800)
            
            if not response_text:
                return None
            
            # Extract JSON from response
            import json
            import re
            
            # Find JSON object in response
            json_match = re.search(r'\{[\s\S]*\}', response_text)
            if json_match:
                template_data = json.loads(json_match.group())
                
                # Validate structure
                if 'templates' in template_data and 'variables' in template_data:
                    return template_data
                    
        except Exception as e:
            print(f"Error generating single template for '{category}': {e}")
            
        return None
    
    def _extract_market_intelligence(self, business_info: Dict, market_context: Dict, ai_handler) -> str:
        """Extract market intelligence from business info and market context using AI"""
        
        # Collect all available context
        additional_context = market_context.get('additional_context', '') if market_context else ''
        location_list = market_context.get('location_list', '') if market_context else ''
        market_region = market_context.get('market_region', '') if market_context else ''
        
        business_name = business_info.get('name', 'Unknown')
        industry = business_info.get('industry', 'Unknown')
        description = business_info.get('description', '')
        
        prompt = f"""
        Analyze the following business and market context to extract market intelligence for keyword generation:
        
        Business Information:
        - Name: {business_name}
        - Industry: {industry}
        - Description: {description}
        
        Market Context:
        - Additional Context: {additional_context}
        - Location List: {location_list}
        - Market Region: {market_region}
        
        Extract and provide the following market intelligence:
        
        1. GEOGRAPHIC SCOPE:
           - Primary markets/countries mentioned or implied
           - Key cities/regions that would be relevant
           - Geographic modifiers (Canadian, European, US-based, etc.)
        
        2. MARKET SEGMENTS:
           - Target customer types (enterprise, consumer, luxury, budget, etc.)
           - Market maturity (emerging, established, niche, mainstream)
           - Business model focus (B2B, B2C, marketplace, etc.)
        
        3. INDUSTRY-SPECIFIC TERMS:
           - Key products/services this business offers
           - Industry jargon and terminology customers would search for
           - Competitive landscape terms
        
        4. TEMPORAL CONTEXT:
           - Relevant years, seasons, or time periods
           - Market trends or timing considerations
        
        Based on the context "{additional_context}", be especially detailed about geographic and market segment implications.
        
        Provide a structured analysis that will help generate relevant keyword variables.
        """
        
        try:
            print(f"Extracting market intelligence for: {business_name} with context: {additional_context}")
            response = ai_handler.generate(prompt, max_tokens=500)
            
            if response:
                print(f"Market intelligence extracted: {len(response)} characters")
                return response
            else:
                print("No market intelligence response from AI")
                return f"Market Context: {additional_context}, Industry: {industry}, Business: {business_name}"
                
        except Exception as e:
            print(f"Error extracting market intelligence: {e}")
            return f"Market Context: {additional_context}, Industry: {industry}, Business: {business_name}"
    
    def _get_basic_ai_template_suggestions(self, business_info: Dict, ai_handler) -> List[Dict]:
        """Fallback to basic AI template generation if comprehensive analysis fails"""
        
        prompt = f"""
        You are an expert in programmatic SEO. Analyze this business and create templates that match ACTUAL GOOGLE SEARCHES.

        Business Information:
        - Name: {business_info.get('name', 'Unknown')}
        - Industry: {business_info.get('industry', 'Unknown')}
        - Description: {business_info.get('description', 'No description')}
        - Target Audience: {business_info.get('target_audience', 'General')}

        CRITICAL: Create templates that match queries people ACTUALLY type into Google.
        
        Good template examples:
        - "{{city}} {{service}} prices" (people search for costs)
        - "best {{product}} for {{use_case}}" (comparison intent)
        - "{{service}} near me" (local intent)
        - "is {{product}} worth it" (evaluation queries)
        - "{{tool}} calculator {{city}}" (tool searches)
        
        Bad template examples (AVOID):
        - "simplify {{process}} in {{city}}" (corporate jargon)
        - "enhance your {{service}}" (marketing speak)
        - "streamline {{topic}} experience" (nobody searches this)

        Create 4-6 programmatic SEO templates for this business.

        For each template provide:
        1. name: Descriptive name with emoji
        2. category: Unique category ID (match search intent)
        3. templates: List of 3-5 ACTUAL search query patterns using variables
        4. variables: Dictionary with realistic values (10-20 each)
        5. description: What search intent this serves
        6. estimated_keywords: Realistic estimate
        7. example: 2-3 examples of ACTUAL searches this generates

        Every template MUST match real search behavior, not marketing language.
        
        Return as JSON array.
        """
        
        try:
            response_text = ai_handler.generate(prompt, max_tokens=2000)
            
            if not response_text:
                return []
            
            # Extract JSON from response
            import json
            import re
            
            content = response_text
            
            # Find JSON array in response
            json_match = re.search(r'\[[\s\S]*\]', content)
            if json_match:
                templates_data = json.loads(json_match.group())
                
                # Format for our system
                suggestions = []
                for template in templates_data:
                    suggestion = {
                        "name": template.get('name', 'Custom Template'),
                        "category": template.get('category', 'custom'),
                        "template_group": template.get('category', 'custom'),
                        "id": template.get('category', 'custom'),
                        "description": template.get('description', ''),
                        "estimated_keywords": template.get('estimated_keywords', '100+'),
                        "example": template.get('example', ''),
                        "relevance": "high",
                        "templates": template.get('templates', []),
                        "variables": template.get('variables', {})
                    }
                    
                    # Add to generic templates for generation
                    self.template_library[suggestion['category']] = {
                        'templates': suggestion['templates'],
                        'variables': suggestion['variables']
                    }
                    
                    suggestions.append(suggestion)
                
                return suggestions
                
        except Exception as e:
            print(f"Error in basic AI template generation: {e}")
            
        return []
    
    def _extract_seed_templates_from_strategy(self, strategy_content: str, business_info: Dict) -> List[Dict]:
        """Extract page templates directly from ChatGPT-style strategy analysis"""
        
        # Try to parse the strategy content to extract components
        templates = []
        
        try:
            # Look for location modifiers
            locations = self._extract_list_from_section(strategy_content, "Location Modifiers", "🏙️")
            
            # Look for business categories
            categories = self._extract_list_from_section(strategy_content, "Business-Specific Categories", "🏢")
            
            # Look for intent modifiers  
            intents = self._extract_list_from_section(strategy_content, "Intent/Topic Modifiers", "📊")
            
            # Look for keyword formulas
            formulas = self._extract_keyword_formulas(strategy_content)
            
            if locations and categories and intents and formulas:
                print(f"Extracted components: {len(locations)} locations, {len(categories)} categories, {len(intents)} intents")
                
                # Create page templates based on extracted components
                for i, formula in enumerate(formulas[:3]):  # Max 3 formulas
                    template = {
                        "name": f"📍 {formula['name']}",
                        "category": f"extracted_formula_{i+1}",
                        "template_group": f"extracted_formula_{i+1}",
                        "id": f"extracted_formula_{i+1}",
                        "description": f"Based on formula: {formula['pattern']}",
                        "estimated_keywords": str(len(locations) * len(categories) * len(intents)),
                        "example": f"Example: {formula.get('example', 'Generated keyword example')}",
                        "relevance": "high",
                        "templates": formula['templates'],
                        "variables": {
                            "location": locations[:15],  # Limit to 15 locations
                            "category": categories[:10],  # Limit to 10 categories  
                            "intent": intents[:8]  # Limit to 8 intents
                        }
                    }
                    
                    # Add to generic templates for generation
                    self.template_library[template['category']] = {
                        'templates': template['templates'],
                        'variables': template['variables']
                    }
                    
                    templates.append(template)
                
                return templates
            else:
                print("Could not extract all required components from strategy")
                return []
                
        except Exception as e:
            print(f"Error extracting templates from strategy: {e}")
            return []
    
    def _extract_list_from_section(self, content: str, section_name: str, emoji: str) -> List[str]:
        """Extract list items from a markdown section"""
        import re
        
        # Find section with emoji or text
        pattern = f"{emoji}.*?{section_name}:?(.*?)(?=###|##|$)"
        match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
        
        if not match:
            # Try without emoji
            pattern = f"{section_name}:?(.*?)(?=###|##|$)"
            match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
        
        if match:
            section_content = match.group(1)
            # Extract list items (lines starting with - or bullet points)
            items = re.findall(r'[-•*]\s*([^\n]+)', section_content)
            # Clean up items
            cleaned_items = [item.strip().lower() for item in items if len(item.strip()) > 2]
            return cleaned_items[:20]  # Limit to 20 items
        
        return []
    
    def _extract_keyword_formulas(self, content: str) -> List[Dict]:
        """Extract keyword formulas from strategy content"""
        import re
        
        formulas = []
        
        # Look for formula patterns like [Variable1] [Variable2] [Topic]
        formula_patterns = re.findall(r'\[([^\]]+)\]\s*\[([^\]]+)\]\s*\[([^\]]+)\]', content)
        
        for i, (var1, var2, var3) in enumerate(formula_patterns[:3]):
            formula = {
                "name": f"{var1} {var2} {var3}",
                "pattern": f"[{var1}] [{var2}] [{var3}]",
                "templates": [
                    f"{{{var1.lower().replace(' ', '_')}}} {{{var2.lower().replace(' ', '_')}}} {{{var3.lower().replace(' ', '_')}}}",
                    f"best {{{var1.lower().replace(' ', '_')}}} {{{var2.lower().replace(' ', '_')}}} {{{var3.lower().replace(' ', '_')}}}",
                    f"{{{var2.lower().replace(' ', '_')}}} {{{var3.lower().replace(' ', '_')}}} in {{{var1.lower().replace(' ', '_')}}}",
                ]
            }
            formulas.append(formula)
        
        # If no bracket formulas found, create generic ones
        if not formulas:
            formulas = [
                {
                    "name": "Location Category Analysis",
                    "pattern": "[Location] [Category] [Intent]", 
                    "templates": [
                        "{location} {category} {intent}",
                        "best {category} {intent} {location}",
                        "{category} {intent} in {location}"
                    ]
                }
            ]
        
        return formulas