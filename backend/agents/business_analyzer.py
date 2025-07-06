"""Business Analyzer Agent for identifying programmatic SEO opportunities."""
import logging
import re
import json
from typing import List, Dict, Optional, Tuple
from urllib.parse import urlparse
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)

@dataclass
class BusinessAnalysis:
    """Results from business analysis."""
    business_name: str
    industry: str
    services: List[str]
    products: List[str]
    target_audience: List[str]
    locations: List[str]
    business_model: str
    value_proposition: str
    competitors: List[str] = field(default_factory=list)
    customer_journey_stages: List[str] = field(default_factory=list)
    
@dataclass
class TemplateOpportunity:
    """Represents a programmatic SEO template opportunity."""
    name: str
    pattern: str  # e.g., "[City] [Service] Provider"
    description: str
    estimated_pages: int
    data_requirements: List[str]  # e.g., ["cities", "services"]
    priority: int  # 1-10
    examples: List[str]
    search_intent: str  # informational, commercial, transactional
    
@dataclass
class DataRequirement:
    """Data needed for template implementation."""
    data_type: str  # e.g., "cities", "services", "features"
    description: str
    suggested_count: int
    data_source: str  # manual, csv, api, scraped
    examples: List[str]

class BusinessAnalyzerAgent:
    """Analyzes businesses to identify programmatic SEO opportunities."""
    
    def __init__(self, ai_handler=None):
        self.ai_handler = ai_handler
        self.template_patterns = self._load_template_patterns()
        
    def _load_template_patterns(self) -> Dict[str, List[Dict]]:
        """Load common template patterns by industry."""
        return {
            'real_estate': [
                {
                    'pattern': '[City] [Property Type] for [Purpose]',
                    'variables': ['city', 'property_type', 'purpose'],
                    'examples': ['Austin Condos for Investment', 'Denver Houses for Families']
                },
                {
                    'pattern': '[Neighborhood] Real Estate Market [Year]',
                    'variables': ['neighborhood', 'year'],
                    'examples': ['Downtown Austin Real Estate Market 2024']
                }
            ],
            'software': [
                {
                    'pattern': '[Software] vs [Competitor] Comparison',
                    'variables': ['software', 'competitor'],
                    'examples': ['Slack vs Teams Comparison', 'Notion vs Evernote Comparison']
                },
                {
                    'pattern': '[Feature] Software for [Industry]',
                    'variables': ['feature', 'industry'],
                    'examples': ['CRM Software for Real Estate', 'Project Management Software for Agencies']
                }
            ],
            'services': [
                {
                    'pattern': '[Service] in [Location]',
                    'variables': ['service', 'location'],
                    'examples': ['Plumbing in Austin', 'Web Design in New York']
                },
                {
                    'pattern': '[Service] for [Customer Type]',
                    'variables': ['service', 'customer_type'],
                    'examples': ['Accounting for Startups', 'Marketing for Dentists']
                }
            ],
            'ecommerce': [
                {
                    'pattern': 'Best [Product] for [Use Case]',
                    'variables': ['product', 'use_case'],
                    'examples': ['Best Laptops for Gaming', 'Best Cameras for Travel']
                },
                {
                    'pattern': '[Product] under [$Price]',
                    'variables': ['product', 'price'],
                    'examples': ['Smartphones under $500', 'Tablets under $300']
                }
            ]
        }
    
    def analyze_business(self, url_or_description: str) -> BusinessAnalysis:
        """Extract business information and identify opportunities."""
        # Determine if input is URL or description
        is_url = self._is_valid_url(url_or_description)
        
        business_info = {
            'url': url_or_description if is_url else None,
            'description': url_or_description if not is_url else None,
            'is_url': is_url
        }
        
        # Use AI to analyze the business
        if self.ai_handler:
            ai_analysis = self.ai_handler.analyze_business_comprehensive(business_info)
            return self._parse_ai_analysis(ai_analysis, business_info)
        else:
            # Fallback to basic analysis
            return self._basic_analysis(business_info)
    
    def suggest_templates(self, business_analysis: BusinessAnalysis) -> List[TemplateOpportunity]:
        """Suggest relevant templates based on business analysis."""
        templates = []
        
        # Determine primary template category
        industry_key = self._map_industry_to_key(business_analysis.industry)
        
        # Location-based templates (universal)
        if business_analysis.locations or self._is_location_relevant(business_analysis):
            templates.extend(self._generate_location_templates(business_analysis))
        
        # Service/Product comparison templates
        if len(business_analysis.services) > 1 or len(business_analysis.products) > 1:
            templates.extend(self._generate_comparison_templates(business_analysis))
        
        # Industry-specific templates
        if industry_key in self.template_patterns:
            templates.extend(self._generate_industry_templates(business_analysis, industry_key))
        
        # Customer segment templates
        if business_analysis.target_audience:
            templates.extend(self._generate_audience_templates(business_analysis))
        
        # Use case and how-to templates
        templates.extend(self._generate_howto_templates(business_analysis))
        
        # AI-powered custom templates if available
        if self.ai_handler:
            custom_templates = self._generate_ai_powered_templates(business_analysis)
            templates.extend(custom_templates)
        
        # Sort by priority
        templates.sort(key=lambda x: x.priority, reverse=True)
        
        return templates[:10]  # Return top 10 opportunities
    
    def identify_data_requirements(self, template: TemplateOpportunity) -> List[DataRequirement]:
        """Identify data needed for a template."""
        requirements = []
        
        # Extract variables from template pattern
        variables = re.findall(r'\[([^\]]+)\]', template.pattern)
        
        for var in variables:
            var_lower = var.lower().replace(' ', '_')
            
            if 'city' in var_lower or 'location' in var_lower:
                requirements.append(DataRequirement(
                    data_type='cities',
                    description='List of target cities for local SEO',
                    suggested_count=50,
                    data_source='csv',
                    examples=['Austin', 'Dallas', 'Houston', 'San Antonio', 'Phoenix']
                ))
            
            elif 'service' in var_lower:
                requirements.append(DataRequirement(
                    data_type='services',
                    description='List of services offered',
                    suggested_count=10,
                    data_source='manual',
                    examples=['Web Design', 'SEO', 'Digital Marketing', 'Branding']
                ))
            
            elif 'product' in var_lower:
                requirements.append(DataRequirement(
                    data_type='products',
                    description='List of products or product categories',
                    suggested_count=20,
                    data_source='csv',
                    examples=['Laptops', 'Smartphones', 'Tablets', 'Smartwatches']
                ))
            
            elif 'feature' in var_lower:
                requirements.append(DataRequirement(
                    data_type='features',
                    description='Key features or capabilities',
                    suggested_count=15,
                    data_source='manual',
                    examples=['Automation', 'Analytics', 'Collaboration', 'Integration']
                ))
            
            elif 'industry' in var_lower or 'customer' in var_lower:
                requirements.append(DataRequirement(
                    data_type='industries',
                    description='Target industries or customer segments',
                    suggested_count=12,
                    data_source='manual',
                    examples=['Healthcare', 'Finance', 'Retail', 'Manufacturing']
                ))
            
            elif 'price' in var_lower:
                requirements.append(DataRequirement(
                    data_type='price_points',
                    description='Price ranges for filtering',
                    suggested_count=5,
                    data_source='manual',
                    examples=['$100', '$250', '$500', '$1000', '$2500']
                ))
            
            elif 'year' in var_lower:
                requirements.append(DataRequirement(
                    data_type='years',
                    description='Years for temporal content',
                    suggested_count=3,
                    data_source='manual',
                    examples=['2024', '2025', '2026']
                ))
            
            else:
                # Generic data requirement
                requirements.append(DataRequirement(
                    data_type=var_lower,
                    description=f'List of {var} options',
                    suggested_count=10,
                    data_source='manual',
                    examples=[f'{var} 1', f'{var} 2', f'{var} 3']
                ))
        
        return requirements
    
    def calculate_page_potential(self, template: TemplateOpportunity, 
                               data_counts: Dict[str, int]) -> int:
        """Calculate how many pages a template could generate."""
        variables = re.findall(r'\[([^\]]+)\]', template.pattern)
        
        total_pages = 1
        for var in variables:
            var_key = var.lower().replace(' ', '_')
            if var_key in data_counts:
                total_pages *= data_counts[var_key]
        
        return total_pages
    
    def _is_valid_url(self, text: str) -> bool:
        """Check if text is a valid URL."""
        try:
            result = urlparse(text)
            return all([result.scheme, result.netloc])
        except:
            return False
    
    def _parse_ai_analysis(self, ai_analysis: Dict, business_info: Dict) -> BusinessAnalysis:
        """Parse AI analysis response into BusinessAnalysis object."""
        if not ai_analysis:
            return self._basic_analysis(business_info)
        
        # Extract from comprehensive analysis
        intel = ai_analysis.get('business_intelligence', '')
        
        # Parse key information
        services = self._extract_list_from_text(intel, 'services', 'products')
        products = self._extract_list_from_text(intel, 'products', 'features')
        audiences = self._extract_list_from_text(intel, 'customers', 'audience')
        
        return BusinessAnalysis(
            business_name=business_info.get('name', 'Unknown Business'),
            industry=self._extract_industry(intel),
            services=services[:5],
            products=products[:5],
            target_audience=audiences[:3],
            locations=self._extract_locations(intel),
            business_model=self._extract_business_model(intel),
            value_proposition=self._extract_value_prop(intel),
            competitors=self._extract_competitors(intel),
            customer_journey_stages=['awareness', 'consideration', 'decision', 'retention']
        )
    
    def _basic_analysis(self, business_info: Dict) -> BusinessAnalysis:
        """Fallback basic analysis without AI."""
        return BusinessAnalysis(
            business_name='Unknown Business',
            industry='General',
            services=['Service 1', 'Service 2'],
            products=[],
            target_audience=['General Audience'],
            locations=['United States'],
            business_model='Service Provider',
            value_proposition='Quality services at competitive prices'
        )
    
    def _map_industry_to_key(self, industry: str) -> str:
        """Map analyzed industry to template pattern key."""
        industry_lower = industry.lower()
        
        if any(term in industry_lower for term in ['real estate', 'property', 'realty']):
            return 'real_estate'
        elif any(term in industry_lower for term in ['software', 'saas', 'app', 'tech']):
            return 'software'
        elif any(term in industry_lower for term in ['ecommerce', 'retail', 'shop', 'store']):
            return 'ecommerce'
        else:
            return 'services'
    
    def _is_location_relevant(self, analysis: BusinessAnalysis) -> bool:
        """Determine if location-based templates are relevant."""
        location_indicators = ['local', 'near me', 'city', 'regional', 'nationwide']
        return any(
            indicator in analysis.business_model.lower() or 
            indicator in analysis.value_proposition.lower()
            for indicator in location_indicators
        )
    
    def _generate_location_templates(self, analysis: BusinessAnalysis) -> List[TemplateOpportunity]:
        """Generate location-based template opportunities."""
        templates = []
        
        if analysis.services:
            primary_service = analysis.services[0]
            templates.append(TemplateOpportunity(
                name=f"{primary_service} by Location",
                pattern=f"[City] {primary_service}",
                description=f"Location pages for {primary_service} services in different cities",
                estimated_pages=500,
                data_requirements=['cities'],
                priority=9,
                examples=[
                    f"Austin {primary_service}",
                    f"Dallas {primary_service}",
                    f"Houston {primary_service}"
                ],
                search_intent='commercial'
            ))
            
            # Neighborhood-level template
            templates.append(TemplateOpportunity(
                name=f"{primary_service} by Neighborhood",
                pattern=f"{primary_service} in [Neighborhood] [City]",
                description=f"Hyper-local pages targeting specific neighborhoods",
                estimated_pages=2000,
                data_requirements=['neighborhoods', 'cities'],
                priority=7,
                examples=[
                    f"{primary_service} in Downtown Austin",
                    f"{primary_service} in Upper East Side NYC"
                ],
                search_intent='commercial'
            ))
        
        return templates
    
    def _generate_comparison_templates(self, analysis: BusinessAnalysis) -> List[TemplateOpportunity]:
        """Generate comparison template opportunities."""
        templates = []
        
        if len(analysis.services) > 1:
            templates.append(TemplateOpportunity(
                name="Service Comparison Pages",
                pattern="[Service A] vs [Service B] Comparison",
                description="Help users compare different service options",
                estimated_pages=50,
                data_requirements=['services'],
                priority=8,
                examples=[
                    f"{analysis.services[0]} vs {analysis.services[1]} Comparison"
                ],
                search_intent='commercial'
            ))
        
        if analysis.competitors:
            templates.append(TemplateOpportunity(
                name="Competitor Comparisons",
                pattern="[Your Business] vs [Competitor] Comparison",
                description="Compare your offerings with competitors",
                estimated_pages=20,
                data_requirements=['competitors', 'features'],
                priority=6,
                examples=[
                    f"{analysis.business_name} vs {analysis.competitors[0]} Comparison"
                ],
                search_intent='commercial'
            ))
        
        return templates
    
    def _generate_industry_templates(self, analysis: BusinessAnalysis, 
                                   industry_key: str) -> List[TemplateOpportunity]:
        """Generate industry-specific templates."""
        templates = []
        patterns = self.template_patterns.get(industry_key, [])
        
        for pattern_info in patterns[:3]:  # Top 3 patterns
            # Customize pattern with business info
            pattern = pattern_info['pattern']
            
            # Estimate pages based on typical data sizes
            estimated_pages = 100
            for var in pattern_info['variables']:
                if 'city' in var or 'location' in var:
                    estimated_pages *= 50
                elif 'service' in var or 'product' in var:
                    estimated_pages *= 10
                else:
                    estimated_pages *= 5
            
            estimated_pages = min(estimated_pages, 5000)  # Cap at 5000
            
            templates.append(TemplateOpportunity(
                name=pattern.replace('[', '').replace(']', ''),
                pattern=pattern,
                description=f"Target searches for {pattern.lower()}",
                estimated_pages=estimated_pages,
                data_requirements=pattern_info['variables'],
                priority=7,
                examples=pattern_info['examples'],
                search_intent='commercial'
            ))
        
        return templates
    
    def _generate_audience_templates(self, analysis: BusinessAnalysis) -> List[TemplateOpportunity]:
        """Generate customer segment templates."""
        templates = []
        
        if analysis.services and analysis.target_audience:
            templates.append(TemplateOpportunity(
                name="Service for Customer Type",
                pattern="[Service] for [Customer Type]",
                description="Target specific customer segments with tailored content",
                estimated_pages=len(analysis.services) * len(analysis.target_audience) * 5,
                data_requirements=['services', 'customer_types'],
                priority=8,
                examples=[
                    f"{analysis.services[0]} for {analysis.target_audience[0]}",
                    f"{analysis.services[0]} for Small Businesses"
                ],
                search_intent='commercial'
            ))
        
        return templates
    
    def _generate_howto_templates(self, analysis: BusinessAnalysis) -> List[TemplateOpportunity]:
        """Generate how-to and guide templates."""
        templates = []
        
        # How-to guides
        templates.append(TemplateOpportunity(
            name="How-To Guides",
            pattern="How to [Action] with [Tool/Service]",
            description="Educational content targeting informational searches",
            estimated_pages=200,
            data_requirements=['actions', 'tools'],
            priority=6,
            examples=[
                "How to Get Started with Project Management",
                "How to Choose the Right CRM Software"
            ],
            search_intent='informational'
        ))
        
        # Ultimate guides
        if analysis.services:
            templates.append(TemplateOpportunity(
                name="Ultimate Guides",
                pattern="Ultimate Guide to [Topic] in [Year]",
                description="Comprehensive guides that build topical authority",
                estimated_pages=50,
                data_requirements=['topics', 'years'],
                priority=5,
                examples=[
                    f"Ultimate Guide to {analysis.services[0]} in 2024",
                    "Ultimate Guide to Digital Marketing in 2024"
                ],
                search_intent='informational'
            ))
        
        return templates
    
    def _extract_list_from_text(self, text: str, *keywords: str) -> List[str]:
        """Extract list items from text based on keywords."""
        items = []
        text_lower = text.lower()
        
        for keyword in keywords:
            if keyword in text_lower:
                # Look for bullet points or numbered lists after keyword
                pattern = rf'{keyword}[:\s]*([^\n]+(?:\n[-•*\d]+[^\n]+)*)'
                matches = re.findall(pattern, text_lower)
                
                for match in matches:
                    # Extract individual items
                    item_matches = re.findall(r'[-•*\d]+\s*([^\n]+)', match)
                    items.extend(item_matches)
        
        # Clean and deduplicate
        cleaned_items = []
        for item in items:
            cleaned = item.strip().strip('.,;-')
            if cleaned and len(cleaned) > 2:
                cleaned_items.append(cleaned.title())
        
        return list(dict.fromkeys(cleaned_items))  # Remove duplicates while preserving order
    
    def _extract_industry(self, text: str) -> str:
        """Extract industry from analysis text."""
        patterns = [
            r'industry:\s*([^\n]+)',
            r'business type:\s*([^\n]+)',
            r'sector:\s*([^\n]+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text.lower())
            if match:
                return match.group(1).strip().title()
        
        return 'General Business'
    
    def _extract_locations(self, text: str) -> List[str]:
        """Extract locations mentioned in text."""
        # Look for common location patterns
        locations = []
        
        # Cities
        city_pattern = r'\b(?:Austin|Dallas|Houston|New York|Los Angeles|Chicago|San Francisco|Boston|Seattle|Denver)\b'
        cities = re.findall(city_pattern, text, re.IGNORECASE)
        locations.extend(cities)
        
        # States
        state_pattern = r'\b(?:Texas|California|New York|Florida|Illinois|Washington|Colorado|Massachusetts)\b'
        states = re.findall(state_pattern, text, re.IGNORECASE)
        locations.extend(states)
        
        # Generic location indicators
        if 'nationwide' in text.lower():
            locations.append('United States')
        if 'global' in text.lower() or 'international' in text.lower():
            locations.append('International')
        
        return list(dict.fromkeys(locations))[:5]  # Unique, max 5
    
    def _extract_business_model(self, text: str) -> str:
        """Extract business model from text."""
        models = {
            'saas': 'Software as a Service',
            'subscription': 'Subscription-based',
            'marketplace': 'Marketplace Platform',
            'agency': 'Service Agency',
            'ecommerce': 'E-commerce',
            'consulting': 'Consulting Services',
            'b2b': 'Business to Business',
            'b2c': 'Business to Consumer'
        }
        
        text_lower = text.lower()
        for key, value in models.items():
            if key in text_lower:
                return value
        
        return 'Service Provider'
    
    def _extract_value_prop(self, text: str) -> str:
        """Extract value proposition from text."""
        patterns = [
            r'value proposition:\s*([^\n]+)',
            r'unique value:\s*([^\n]+)',
            r'they offer:\s*([^\n]+)',
            r'helps?\s+(?:businesses?|customers?|users?)\s+([^\n]+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text.lower())
            if match:
                return match.group(1).strip().capitalize()
        
        return 'Delivering quality solutions for business growth'
    
    def _extract_competitors(self, text: str) -> List[str]:
        """Extract competitors from text."""
        patterns = [
            r'competitors?:\s*([^\n]+)',
            r'compete with:\s*([^\n]+)',
            r'alternatives?:\s*([^\n]+)'
        ]
        
        competitors = []
        for pattern in patterns:
            match = re.search(pattern, text.lower())
            if match:
                # Split by common delimiters
                comp_text = match.group(1)
                comp_list = re.split(r'[,;]|\band\b', comp_text)
                competitors.extend([c.strip().title() for c in comp_list if c.strip()])
        
        return list(dict.fromkeys(competitors))[:5]  # Unique, max 5
    
    def _generate_ai_powered_templates(self, analysis: BusinessAnalysis) -> List[TemplateOpportunity]:
        """Use AI to generate custom template opportunities."""
        if not self.ai_handler:
            return []
        
        prompt = f"""Based on this business analysis, suggest 5 highly specific programmatic SEO template opportunities:

Business: {analysis.business_name}
Industry: {analysis.industry}
Services: {', '.join(analysis.services[:3])}
Products: {', '.join(analysis.products[:3])}
Target Audience: {', '.join(analysis.target_audience[:3])}
Business Model: {analysis.business_model}

Create templates following this exact format for each:
1. Template Pattern: Use [Variable] format like "[City] [Service] Experts"
2. Estimated Pages: Be realistic (50-5000 pages)
3. Priority: 1-10 based on commercial value
4. Search Intent: informational/commercial/transactional

Focus on:
- High commercial intent patterns
- Scalable to hundreds of pages
- Specific to this business type
- Different from generic templates

Return as JSON array with: pattern, name, description, estimated_pages, priority, search_intent, examples (3), variables"""

        try:
            response = self.ai_handler.generate(prompt, 800)
            if response:
                # Parse JSON from response
                start = response.find('[')
                end = response.rfind(']') + 1
                if start >= 0 and end > start:
                    template_data = json.loads(response[start:end])
                    
                    templates = []
                    for data in template_data[:5]:
                        templates.append(TemplateOpportunity(
                            name=data.get('name', data.get('pattern', '').replace('[', '').replace(']', '')),
                            pattern=data.get('pattern', ''),
                            description=data.get('description', ''),
                            estimated_pages=data.get('estimated_pages', 100),
                            data_requirements=data.get('variables', []),
                            priority=data.get('priority', 5),
                            examples=data.get('examples', []),
                            search_intent=data.get('search_intent', 'commercial')
                        ))
                    return templates
        except Exception as e:
            logger.error(f"Error generating AI-powered templates: {e}")
        
        return []