"""
AI-Powered Programmatic SEO Strategy Generator

This module creates custom programmatic SEO strategies based on deep business analysis.
Instead of static templates, it generates dynamic, business-specific SEO plans.
"""

import json
import re
from typing import Dict, List, Any, Tuple, Optional
from datetime import datetime
from api.ai_handler import AIHandler


class AIStrategyGenerator:
    """
    Generates custom programmatic SEO strategies using AI analysis.
    
    Flow:
    1. Deep Business Analysis
    2. Market Opportunity Discovery  
    3. Dynamic Template Generation
    4. Intelligent Data Strategy
    5. Content Framework Creation
    """
    
    def __init__(self):
        self.ai_handler = AIHandler()
        
        if not self.ai_handler.has_ai_provider():
            raise RuntimeError(
                "❌ AI Strategy Generator requires AI providers. "
                "This advanced system needs AI to analyze businesses and create custom strategies."
            )
    
    async def generate_complete_strategy(self, business_input: str, business_url: str = None) -> Dict[str, Any]:
        """
        Generate a complete programmatic SEO strategy for a business.
        
        Args:
            business_input: Description of the business
            business_url: Optional URL for additional analysis
            
        Returns:
            Complete strategy with templates, data plans, and content framework
        """
        print("🧠 Starting AI-Powered Strategy Generation...")
        
        # Phase 1: Deep Business Intelligence
        business_intelligence = await self._analyze_business_intelligence(business_input, business_url)
        
        # Phase 2: Market Opportunity Discovery
        market_opportunities = await self._discover_market_opportunities(business_intelligence)
        
        # Phase 3: Dynamic Template Generation
        custom_templates = await self._generate_dynamic_templates(business_intelligence, market_opportunities)
        
        # Phase 4: Intelligent Data Strategy
        data_strategy = await self._create_data_strategy(business_intelligence, custom_templates)
        
        # Phase 5: Content Framework
        content_framework = await self._design_content_framework(business_intelligence, custom_templates)
        
        # Compile complete strategy
        strategy = {
            "business_intelligence": business_intelligence,
            "market_opportunities": market_opportunities,
            "custom_templates": custom_templates,
            "data_strategy": data_strategy,
            "content_framework": content_framework,
            "implementation_plan": self._create_implementation_plan(custom_templates, data_strategy),
            "generated_at": datetime.now().isoformat(),
            "strategy_version": "2.0_ai_powered"
        }
        
        print(f"✅ Complete strategy generated with {len(custom_templates)} custom templates")
        return strategy
    
    async def _analyze_business_intelligence(self, business_input: str, business_url: str = None) -> Dict[str, Any]:
        """Phase 1: Deep business analysis to understand what the business actually does"""
        
        print("📊 Phase 1: Analyzing business intelligence...")
        
        # Fetch URL content if provided
        url_content = ""
        if business_url:
            try:
                # Use the existing URL fetching from ai_client
                from ai_client import AIClient
                ai_client = AIClient()
                url_content = ai_client._fetch_url_content(business_url)
                print(f"   📄 Fetched {len(url_content)} characters from URL")
            except Exception as e:
                print(f"   ⚠️ Could not fetch URL content: {e}")
        
        prompt = f"""
        You are a world-class business analyst and programmatic SEO strategist. 
        Analyze this business deeply to understand their offerings, market, and SEO opportunities.
        
        Business Description: {business_input}
        
        {f"Website Content: {url_content[:2000]}" if url_content else ""}
        
        Provide a comprehensive analysis in JSON format:
        
        {{
            "business_core": {{
                "name": "Actual business name",
                "industry": "Specific industry/vertical",
                "business_model": "How they make money (SaaS, marketplace, services, etc.)",
                "value_proposition": "What unique value they provide",
                "target_customers": "Specific customer segments with titles/demographics",
                "price_range": "Typical pricing or price range if available"
            }},
            "market_position": {{
                "target_audience_personas": ["Persona 1 with details", "Persona 2 with details"],
                "customer_pain_points": ["Pain point 1", "Pain point 2", "Pain point 3"],
                "solution_benefits": ["Benefit 1", "Benefit 2", "Benefit 3"],
                "competitive_differentiation": "What makes them unique",
                "market_size_indicator": "Large/Medium/Small/Niche"
            }},
            "search_behavior_analysis": {{
                "primary_search_intents": ["Intent 1", "Intent 2", "Intent 3"],
                "customer_journey_stages": {{
                    "awareness": ["What they search when they have a problem"],
                    "consideration": ["What they search when researching solutions"],
                    "decision": ["What they search when ready to buy/use"]
                }},
                "geographic_relevance": "Local/Regional/National/Global",
                "seasonal_patterns": "Any seasonal search patterns"
            }},
            "content_opportunities": {{
                "high_volume_topics": ["Topic that gets lots of searches"],
                "long_tail_opportunities": ["Specific long-tail keyword areas"],
                "comparison_opportunities": ["What they compare against"],
                "educational_needs": ["What customers need to learn"],
                "local_opportunities": ["Location-based opportunities if relevant"]
            }}
        }}
        
        Be specific and actionable. Base everything on real market understanding.
        """
        
        try:
            response = self.ai_handler.generate(prompt, max_tokens=1500)
            if response:
                # Parse JSON from response
                json_match = re.search(r'\{.*\}', response, re.DOTALL)
                if json_match:
                    analysis = json.loads(json_match.group())
                    print("   ✅ Business intelligence analysis complete")
                    return analysis
        except Exception as e:
            print(f"   ❌ Business analysis failed: {e}")
        
        # Fallback analysis
        return self._get_fallback_business_analysis(business_input)
    
    async def _discover_market_opportunities(self, business_intelligence: Dict[str, Any]) -> Dict[str, Any]:
        """Phase 2: Identify specific programmatic SEO opportunities in the market"""
        
        print("🎯 Phase 2: Discovering market opportunities...")
        
        business_core = business_intelligence.get("business_core", {})
        search_behavior = business_intelligence.get("search_behavior_analysis", {})
        
        prompt = f"""
        You are a programmatic SEO expert. Based on this business analysis, identify specific opportunities
        for programmatic SEO that could generate hundreds or thousands of valuable pages.
        
        Business: {business_core.get("name", "Unknown")}
        Industry: {business_core.get("industry", "Unknown")}
        Target Customers: {business_core.get("target_customers", "Unknown")}
        
        Search Intents: {search_behavior.get("primary_search_intents", [])}
        Customer Journey: {search_behavior.get("customer_journey_stages", {})}
        
        Identify programmatic SEO opportunities in JSON format:
        
        {{
            "scalable_content_types": [
                {{
                    "content_type": "Location-based analysis",
                    "search_volume_potential": "High/Medium/Low",
                    "competition_level": "High/Medium/Low",
                    "user_value": "What value this provides to users",
                    "example_queries": ["Example search query 1", "Example search query 2"],
                    "scale_potential": "How many pages this could generate"
                }}
            ],
            "template_opportunities": [
                {{
                    "template_concept": "Descriptive name of template concept",
                    "search_intent": "What search intent this serves",
                    "target_keywords": ["Primary keyword pattern", "Secondary keyword pattern"],
                    "content_differentiation": "What makes this content unique/valuable",
                    "estimated_pages": "Number of pages this could generate"
                }}
            ],
            "data_multiplication_opportunities": [
                {{
                    "data_type": "Type of data to collect/use",
                    "multiplication_factor": "How this data multiplies (e.g., 50 cities × 10 services = 500 pages)",
                    "value_proposition": "Why users would want this specific data combination",
                    "competitive_advantage": "Why competitors likely don't have this"
                }}
            ],
            "market_gaps": [
                {{
                    "gap_description": "What's missing in the market",
                    "opportunity_size": "Large/Medium/Small",
                    "difficulty_to_execute": "Easy/Medium/Hard",
                    "first_mover_advantage": "Why being first matters here"
                }}
            ]
        }}
        
        Focus on opportunities that provide real user value, not just SEO volume.
        """
        
        try:
            response = self.ai_handler.generate(prompt, max_tokens=1200)
            if response:
                json_match = re.search(r'\{.*\}', response, re.DOTALL)
                if json_match:
                    opportunities = json.loads(json_match.group())
                    print(f"   ✅ Found {len(opportunities.get('template_opportunities', []))} template opportunities")
                    return opportunities
        except Exception as e:
            print(f"   ❌ Market opportunity discovery failed: {e}")
        
        return self._get_fallback_opportunities(business_intelligence)
    
    async def _generate_dynamic_templates(self, business_intelligence: Dict[str, Any], 
                                        market_opportunities: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Phase 3: Generate custom templates based on business analysis"""
        
        print("🎨 Phase 3: Generating dynamic templates...")
        
        business_core = business_intelligence.get("business_core", {})
        template_opportunities = market_opportunities.get("template_opportunities", [])
        
        templates = []
        
        for opportunity in template_opportunities[:5]:  # Generate top 5 opportunities
            template = await self._create_single_template(business_intelligence, opportunity)
            if template:
                templates.append(template)
        
        print(f"   ✅ Generated {len(templates)} custom templates")
        return templates
    
    async def _create_single_template(self, business_intelligence: Dict[str, Any], 
                                    opportunity: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create a single custom template based on opportunity analysis"""
        
        business_core = business_intelligence.get("business_core", {})
        
        prompt = f"""
        Create a specific programmatic SEO template for this opportunity:
        
        Business: {business_core.get("name", "Unknown")}
        Industry: {business_core.get("industry", "Unknown")}
        Template Concept: {opportunity.get("template_concept", "Unknown")}
        Search Intent: {opportunity.get("search_intent", "Unknown")}
        Target Keywords: {opportunity.get("target_keywords", [])}
        
        Generate a complete template in JSON format:
        
        {{
            "template_name": "Descriptive name for this template",
            "template_pattern": "Title pattern with variables like {{Variable1}} {{Variable2}} Analysis",
            "h1_pattern": "H1 pattern that's similar but slightly different",
            "search_intent_served": "Specific search intent this serves",
            "target_variables": [
                {{
                    "variable_name": "Variable1",
                    "description": "What this variable represents",
                    "example_values": ["Example 1", "Example 2", "Example 3"],
                    "data_source_suggestions": ["Where to get this data"]
                }}
            ],
            "content_strategy": {{
                "primary_value": "Main value this page provides to users",
                "content_sections": ["Section 1", "Section 2", "Section 3"],
                "unique_angle": "What makes this content different from competitors",
                "user_action_goal": "What we want users to do after reading"
            }},
            "seo_strategy": {{
                "primary_keyword_pattern": "Main keyword pattern",
                "secondary_keywords": ["Related keyword 1", "Related keyword 2"],
                "meta_description_template": "Template for meta descriptions",
                "internal_linking_opportunities": ["How to link between pages"]
            }},
            "scale_estimate": {{
                "variables_count": "How many values per variable",
                "total_page_potential": "Total pages possible",
                "priority_level": "High/Medium/Low based on opportunity"
            }}
        }}
        
        Make this template specific to the business and valuable to users.
        """
        
        try:
            response = self.ai_handler.generate(prompt, max_tokens=800)
            if response:
                json_match = re.search(r'\{.*\}', response, re.DOTALL)
                if json_match:
                    template = json.loads(json_match.group())
                    # Add generation metadata
                    template["generated_at"] = datetime.now().isoformat()
                    template["generation_method"] = "ai_dynamic"
                    return template
        except Exception as e:
            print(f"   ❌ Template generation failed: {e}")
        
        return None
    
    async def _create_data_strategy(self, business_intelligence: Dict[str, Any], 
                                  custom_templates: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Phase 4: Create intelligent data collection and structuring strategy"""
        
        print("📈 Phase 4: Creating data strategy...")
        
        # Extract all variables from templates
        all_variables = []
        for template in custom_templates:
            variables = template.get("target_variables", [])
            all_variables.extend(variables)
        
        prompt = f"""
        Create a comprehensive data strategy for these programmatic SEO templates.
        
        Business: {business_intelligence.get("business_core", {}).get("name", "Unknown")}
        
        Template Variables Needed:
        {json.dumps(all_variables, indent=2)}
        
        Create a data strategy in JSON format:
        
        {{
            "data_collection_plan": [
                {{
                    "variable_name": "Variable name",
                    "data_sources": ["Source 1", "Source 2"],
                    "collection_method": "How to collect this data",
                    "data_quality_requirements": "What makes good vs bad data",
                    "update_frequency": "How often to refresh this data",
                    "estimated_values": "How many values we can collect"
                }}
            ],
            "data_validation_rules": [
                {{
                    "variable": "Variable name",
                    "validation_rules": ["Rule 1", "Rule 2"],
                    "quality_thresholds": "Minimum quality requirements"
                }}
            ],
            "data_combination_strategy": {{
                "optimal_combinations": ["Which variables work best together"],
                "combination_priorities": ["Which combinations to prioritize"],
                "scale_calculations": "Total pages possible with full data"
            }},
            "implementation_phases": [
                {{
                    "phase": "Phase 1",
                    "data_to_collect": ["Priority data sets"],
                    "estimated_timeline": "Time to collect",
                    "page_generation_potential": "Pages possible with this phase"
                }}
            ]
        }}
        
        Focus on data that's realistic to collect and provides genuine user value.
        """
        
        try:
            response = self.ai_handler.generate(prompt, max_tokens=1000)
            if response:
                json_match = re.search(r'\{.*\}', response, re.DOTALL)
                if json_match:
                    strategy = json.loads(json_match.group())
                    print("   ✅ Data strategy created")
                    return strategy
        except Exception as e:
            print(f"   ❌ Data strategy creation failed: {e}")
        
        return {"error": "Data strategy generation failed", "fallback": True}
    
    async def _design_content_framework(self, business_intelligence: Dict[str, Any],
                                      custom_templates: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Phase 5: Design content framework and architecture"""
        
        print("🏗️ Phase 5: Designing content framework...")
        
        prompt = f"""
        Design a comprehensive content framework for this programmatic SEO strategy.
        
        Business: {business_intelligence.get("business_core", {}).get("name", "Unknown")}
        Industry: {business_intelligence.get("business_core", {}).get("industry", "Unknown")}
        
        Templates Created: {len(custom_templates)}
        
        Create a content framework in JSON format:
        
        {{
            "content_pillars": [
                {{
                    "pillar_name": "Main content theme",
                    "supporting_templates": ["Which templates support this pillar"],
                    "seo_value": "Why this pillar is valuable for SEO",
                    "user_value": "Why users care about this content"
                }}
            ],
            "internal_linking_strategy": {{
                "hub_pages": ["Central pages that link to many others"],
                "spoke_pages": ["Specific pages that link back to hubs"],
                "linking_patterns": ["How pages should link to each other"]
            }},
            "content_quality_standards": {{
                "minimum_word_count": "Minimum words per page",
                "unique_content_percentage": "How much content must be unique",
                "value_requirements": ["What makes content valuable"],
                "update_requirements": "How often to update content"
            }},
            "scalability_architecture": {{
                "content_generation_pipeline": "How to efficiently generate content",
                "quality_assurance_process": "How to maintain quality at scale",
                "performance_monitoring": "How to track content performance"
            }}
        }}
        """
        
        try:
            response = self.ai_handler.generate(prompt, max_tokens=800)
            if response:
                json_match = re.search(r'\{.*\}', response, re.DOTALL)
                if json_match:
                    framework = json.loads(json_match.group())
                    print("   ✅ Content framework designed")
                    return framework
        except Exception as e:
            print(f"   ❌ Content framework design failed: {e}")
        
        return {"error": "Content framework generation failed", "fallback": True}
    
    def _create_implementation_plan(self, custom_templates: List[Dict[str, Any]], 
                                  data_strategy: Dict[str, Any]) -> Dict[str, Any]:
        """Create step-by-step implementation plan"""
        
        total_potential = sum(
            template.get("scale_estimate", {}).get("total_page_potential", 0) 
            for template in custom_templates
        )
        
        return {
            "quick_wins": {
                "phase_1_templates": [t["template_name"] for t in custom_templates[:2]],
                "estimated_pages": str(total_potential // 3),
                "timeline": "2-4 weeks",
                "resources_needed": ["AI content generation", "Basic data collection"]
            },
            "scale_phase": {
                "all_templates": [t["template_name"] for t in custom_templates],
                "full_scale_pages": str(total_potential),
                "timeline": "2-3 months",
                "resources_needed": ["Complete data collection", "Content quality assurance"]
            },
            "success_metrics": [
                "Organic traffic growth",
                "Keyword ranking improvements", 
                "User engagement metrics",
                "Conversion rate optimization"
            ]
        }
    
    def _get_fallback_business_analysis(self, business_input: str) -> Dict[str, Any]:
        """Fallback business analysis when AI fails"""
        return {
            "business_core": {
                "name": "Business Analysis Pending",
                "industry": "General",
                "business_model": "Unknown",
                "value_proposition": "Analysis in progress",
                "target_customers": "To be determined",
                "price_range": "Unknown"
            },
            "market_position": {
                "target_audience_personas": ["Primary users", "Secondary users"],
                "customer_pain_points": ["Pain point analysis needed"],
                "solution_benefits": ["Benefits analysis needed"],
                "competitive_differentiation": "Analysis in progress",
                "market_size_indicator": "Unknown"
            },
            "search_behavior_analysis": {
                "primary_search_intents": ["Research needed"],
                "customer_journey_stages": {
                    "awareness": ["Analysis needed"],
                    "consideration": ["Analysis needed"], 
                    "decision": ["Analysis needed"]
                },
                "geographic_relevance": "Unknown",
                "seasonal_patterns": "Analysis needed"
            },
            "content_opportunities": {
                "high_volume_topics": ["Topic research needed"],
                "long_tail_opportunities": ["Research needed"],
                "comparison_opportunities": ["Research needed"],
                "educational_needs": ["Research needed"],
                "local_opportunities": ["Research needed"]
            }
        }
    
    def _get_fallback_opportunities(self, business_intelligence: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback opportunities when AI fails"""
        return {
            "scalable_content_types": [
                {
                    "content_type": "Location-based content",
                    "search_volume_potential": "Medium",
                    "competition_level": "Medium",
                    "user_value": "Location-specific information",
                    "example_queries": ["Service in city", "Location-based queries"],
                    "scale_potential": "50-500 pages"
                }
            ],
            "template_opportunities": [
                {
                    "template_concept": "Service location pages",
                    "search_intent": "Local service discovery",
                    "target_keywords": ["Service + location patterns"],
                    "content_differentiation": "Local market insights",
                    "estimated_pages": "100-300"
                }
            ],
            "data_multiplication_opportunities": [
                {
                    "data_type": "Geographic data",
                    "multiplication_factor": "Cities × Services",
                    "value_proposition": "Local relevance",
                    "competitive_advantage": "Comprehensive coverage"
                }
            ],
            "market_gaps": [
                {
                    "gap_description": "Analysis needed",
                    "opportunity_size": "Unknown",
                    "difficulty_to_execute": "Medium",
                    "first_mover_advantage": "To be determined"
                }
            ]
        }