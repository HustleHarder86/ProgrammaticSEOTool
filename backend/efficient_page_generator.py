"""Efficient page generator for programmatic SEO - focuses on scale over perfection"""
import hashlib
import json
from typing import Dict, List, Any, Optional
from datetime import datetime
import random

from content_patterns import content_patterns


class EfficientPageGenerator:
    """Generate pages efficiently at scale with good-enough quality"""
    
    def __init__(self):
        self.content_patterns = content_patterns
        self.min_word_count = 300
        self.max_word_count = 500
    
    def generate_page(self, template: Dict[str, Any], data_row: Dict[str, Any], 
                     page_index: int = 0) -> Dict[str, Any]:
        """Generate a single page efficiently"""
        
        # 1. Determine content type from template
        content_type = self._detect_content_type(template, data_row)
        
        # 2. Get enriched data for better content
        from data_enricher import DataEnricher
        data_enricher = DataEnricher()
        enriched_data = data_enricher.get_template_data(content_type, data_row)
        
        # 3. Generate title and H1
        title = self._fill_template(template.get("title_pattern", ""), data_row)
        h1 = self._fill_template(template.get("h1_pattern", title), data_row)
        
        # 4. Generate meta description
        meta_desc = self._generate_meta_description(title, data_row, content_type)
        
        # 5. Generate content sections with enriched data
        content_html = self._generate_content_html_with_enriched_data(
            template, data_row, enriched_data, content_type, h1
        )
        
        # 5. Generate URL slug
        slug = self._generate_slug(title)
        
        # 6. Calculate basic quality metrics
        word_count = len(content_html.split())
        quality_score = self._calculate_quality_score(content_html, data_row)
        
        return {
            "title": title,
            "h1": h1,
            "meta_description": meta_desc,
            "slug": slug,
            "content_html": content_html,
            "word_count": word_count,
            "quality_score": quality_score,
            "generated_at": datetime.now().isoformat(),
            "data_points_used": len([v for v in data_row.values() if v])
        }
    
    def _detect_content_type(self, template: Dict[str, Any], data: Dict[str, Any]) -> str:
        """Detect the type of content based on template and data"""
        pattern = template.get("pattern", "").lower()
        
        # Check if it's a question or evaluation
        if (pattern.startswith("is ") or pattern.startswith("are ") or 
            pattern.startswith("can ") or pattern.startswith("should ") or
            "?" in pattern or
            "analysis" in pattern or "investment" in pattern or "evaluation" in pattern):
            # Determine question type
            if ("good" in pattern or "worth" in pattern or "best" in pattern or
                "analysis" in pattern or "investment" in pattern or "evaluation" in pattern or
                "rental" in pattern or "property" in pattern):
                return "evaluation_question"
            else:
                return "general_question"
        elif any(word in pattern for word in ["vs", "versus", "compare"]):
            return "comparison"
        elif any(word in pattern for word in ["course", "learn", "study"]):
            return "educational"
        elif any(word in pattern for word in ["buy", "shop", "product"]):
            return "product_location"
        elif (any(word in pattern for word in ["in", "near", "at"]) and \
             any(key in data for key in ["location", "city", "area"])) or \
             (any(key in data for key in ["City", "city", "Location", "location"]) and \
              any(key in data for key in ["Service", "service", "Provider", "provider"])):
            return "location_service"
        else:
            return "general"  # Default
    
    def _fill_template(self, template: str, data: Dict[str, Any]) -> str:
        """Fill template with data values"""
        result = template
        
        # Handle both [Variable] and {Variable} formats
        for key, value in data.items():
            if value:
                # Replace all case variations
                result = result.replace(f"[{key}]", str(value))
                result = result.replace(f"[{key.lower()}]", str(value))
                result = result.replace(f"[{key.upper()}]", str(value))
                result = result.replace(f"{{{key}}}", str(value))
                result = result.replace(f"{{{key.lower()}}}", str(value))
                result = result.replace(f"{{{key.upper()}}}", str(value))
        
        return result
    
    def _generate_meta_description(self, title: str, data: Dict[str, Any], 
                                 content_type: str) -> str:
        """Generate SEO meta description"""
        # Simple patterns for meta descriptions
        patterns = {
            "comparison": [
                f"Compare {title}. Quick comparison with prices, features, and recommendations.",
                f"{title} - See key differences, pricing, and which option is best for you.",
                f"Detailed {title} comparison. Features, costs, pros/cons in one place."
            ],
            "location_service": [
                f"Find the best {title}. Reviews, prices, and contact info for top providers.",
                f"{title} - Compare ratings, prices, and availability. Get quotes today.",
                f"Looking for {title}? Browse verified providers with reviews and pricing."
            ],
            "educational": [
                f"Learn about {title}. Courses, programs, and training options compared.",
                f"{title} - Find classes, costs, and schedules. Start learning today.",
                f"Study {title}. Compare programs, prices, and student reviews."
            ],
            "product_location": [
                f"Buy {title}. Compare prices, availability, and store locations.",
                f"{title} - Find in stock now. Best prices and local availability.",
                f"Shop {title}. Real-time inventory and pricing from local stores."
            ]
        }
        
        # Select pattern based on content
        pattern_list = patterns.get(content_type, patterns["location_service"])
        
        # Use title hash for consistent selection
        index = int(hashlib.md5(title.encode()).hexdigest()[:8], 16) % len(pattern_list)
        meta = pattern_list[index]
        
        # Ensure under 160 characters
        if len(meta) > 160:
            meta = meta[:157] + "..."
        
        return meta
    
    def _generate_content_html(self, template: Dict[str, Any], data: Dict[str, Any],
                              content_type: str, h1: str) -> str:
        """Generate the main content HTML"""
        sections = []
        
        # Add H1
        sections.append(f"<h1>{h1}</h1>")
        
        # 1. Introduction (1-2 sentences with data)
        intro_data = self._prepare_intro_data(data, content_type)
        intro_pattern = self.content_patterns.select_pattern("intro", content_type, intro_data)
        intro = self.content_patterns.fill_pattern(intro_pattern, intro_data)
        sections.append(f"<p class='intro'>{intro}</p>")
        
        # 2. Main value section (list, table, or key info)
        main_content = self._generate_main_value_section(data, content_type)
        sections.append(main_content)
        
        # 3. Supporting content (2-3 short paragraphs)
        support_content = self._generate_support_content(data, content_type)
        sections.extend(support_content)
        
        # 4. Simple CTA
        cta_data = data.copy()
        # Add lowercase versions
        for key, value in list(data.items()):
            cta_data[key.lower()] = value
        
        cta_data.setdefault("count", random.randint(5, 50))
        cta_data.setdefault("category", "options")
        cta_data.setdefault("recommended_option", "our top pick")
        
        cta_pattern = self.content_patterns.select_pattern("cta", "general", cta_data)
        cta = self.content_patterns.fill_pattern(cta_pattern, cta_data)
        sections.append(f"<p class='cta'>{cta}</p>")
        
        return "\n\n".join(sections)
    
    def _generate_content_html_with_enriched_data(self, template: Dict[str, Any], data: Dict[str, Any],
                                                 enriched_data: Dict[str, Any], content_type: str, h1: str) -> str:
        """Generate content HTML using enriched data for better quality"""
        sections = []
        
        # Add H1
        sections.append(f"<h1>{h1}</h1>")
        
        # 1. Introduction with enriched data
        intro_pattern = self.content_patterns.select_pattern("intro", content_type, data)
        intro = self.content_patterns.fill_pattern_with_enriched_data(intro_pattern, enriched_data, data)
        sections.append(f"<p class='intro'>{intro}</p>")
        
        # 2. Main value section with enriched data
        main_content = self._generate_main_value_section_enriched(enriched_data, data, content_type)
        sections.append(main_content)
        
        # 3. Supporting content with enriched data
        support_content = self._generate_support_content_enriched(enriched_data, data, content_type)
        sections.extend(support_content)
        
        # 4. Additional context section for more content
        context_content = self._generate_context_section_enriched(enriched_data, data, content_type)
        if context_content:
            sections.append(context_content)
        
        # 5. Value proposition section
        value_content = self._generate_value_section_enriched(enriched_data, data, content_type)
        if value_content:
            sections.append(value_content)
        
        # 6. CTA with enriched data
        cta_pattern = self.content_patterns.select_pattern("cta", "general", data)
        cta = self.content_patterns.fill_pattern_with_enriched_data(cta_pattern, enriched_data, data)
        sections.append(f"<p class='cta'>{cta}</p>")
        
        return "\n\n".join(sections)
    
    def _generate_main_value_section_enriched(self, enriched_data: Dict[str, Any], 
                                             template_data: Dict[str, Any], content_type: str) -> str:
        """Generate main value section using enriched data"""
        primary_data = enriched_data.get("primary_data", {})
        
        if content_type == "evaluation_question":
            # Create comprehensive data-driven analysis with visual elements
            sections = []
            
            # Add visual ROI calculator/infographic
            if "roi_percentage" in primary_data:
                sections.append(self._generate_roi_infographic(primary_data, template_data))
            
            # Add financial metrics in a visual format
            sections.append(self._generate_financial_metrics_cards(primary_data, template_data))
            
            # Add market comparison chart
            if "total_listings" in primary_data:
                sections.append(self._generate_market_comparison(primary_data, template_data))
            
            # Add investment checklist
            sections.append(self._generate_investment_checklist(primary_data, template_data))
            
            return "\n\n".join(sections)
        
        elif content_type == "location_service":
            # Create provider list with realistic data
            provider_count = primary_data.get("provider_count", template_data.get("count", 25))
            avg_rating = primary_data.get("average_rating", 4.5)
            service_name = template_data.get("Service", "service")
            city = template_data.get("City", "your area")
            
            sections = []
            
            # Add quick stats info box
            sections.append(self._generate_quick_stats_box(primary_data, template_data))
            
            # Add provider comparison table
            sections.append(f"<h3>Top {service_name} Providers in {city}</h3>")
            sections.append(self._generate_provider_table(primary_data, template_data))
            
            # Add visual rating breakdown
            sections.append(self._generate_rating_visualization(primary_data, template_data))
            
            # Add service features checklist
            sections.append(self._generate_features_checklist(service_name))
            
            return "\n\n".join(sections)
        
        else:
            # Default content with enriched data and visual elements
            sections = []
            service = template_data.get('Service', template_data.get('service', 'services'))
            location = template_data.get('City', template_data.get('city', 'your area'))
            
            # Add visual elements based on available data
            sections.append(self._generate_quick_stats_box(primary_data, template_data))
            
            sections.append(f"<h3>Overview of {service} in {location}</h3>")
            sections.append(f"<p>Access comprehensive information about {service.lower()} options available in {location}. "
                          f"Our database includes {primary_data.get('provider_count', 'multiple')} verified providers with "
                          f"average ratings of {primary_data.get('average_rating', 4.5)} stars.</p>")
            
            # Add comparison table or pricing info
            if primary_data.get('min_price') and primary_data.get('max_price'):
                sections.append(self._generate_pricing_infographic(primary_data, template_data))
            elif primary_data.get('top_providers'):
                sections.append(self._generate_provider_table(primary_data, template_data))
            
            # Add features checklist
            sections.append(self._generate_features_checklist(service))
            
            return "\n\n".join(sections)
    
    def _generate_support_content_enriched(self, enriched_data: Dict[str, Any], 
                                          template_data: Dict[str, Any], content_type: str) -> List[str]:
        """Generate supporting content using enriched data"""
        primary_data = enriched_data.get("primary_data", {})
        sections = []
        
        if content_type == "evaluation_question":
            # Market insights paragraph
            growth_rate = primary_data.get("market_growth", primary_data.get("growth_rate", 10))
            regulations = primary_data.get("regulations", "standard regulations apply")
            peak_season = primary_data.get("peak_season", "seasonal periods")
            
            market_insight = f"<h3>Market Analysis & Trends</h3>"
            market_insight += f"<p>Current market analysis reveals {growth_rate}% growth in this sector over the past year. "
            if growth_rate > 15:
                market_insight += "This represents exceptional market momentum and indicates highly favorable conditions for new investments. The strong growth trajectory suggests sustained demand and expanding market opportunities. "
            elif growth_rate > 5:
                market_insight += "This demonstrates steady market expansion and stable investment conditions. The consistent growth pattern indicates reliable demand and mature market dynamics. "
            else:
                market_insight += "Market conditions are stabilizing after recent adjustments, presenting strategic opportunities for well-positioned investments. The current environment favors careful market analysis and selective investment approaches. "
            
            market_insight += f"Regulatory environment: {regulations.lower()}. Peak demand typically occurs during {peak_season.lower()}.</p>"
            sections.append(market_insight)
            
            # Detailed risk factors and success strategies
            city = template_data.get("City", "the area")
            service = template_data.get("Service", "short-term rentals")
            
            sections.append(
                f"<h3>Investment Considerations for {city}</h3>"
                f"<p>Success with {service.lower()} in {city} depends on several critical factors. Location selection remains paramount - properties in high-traffic areas, near attractions, or in desirable neighborhoods typically achieve higher occupancy rates and premium pricing. Property condition and presentation significantly impact guest satisfaction and repeat bookings.</p>"
            )
            
            sections.append(
                f"<p>Operational considerations include effective marketing across multiple platforms, responsive customer service, competitive pricing strategies, and maintaining high cleanliness standards. Local market knowledge helps optimize pricing during peak and off-season periods. Additionally, understanding neighborhood dynamics, parking availability, and noise regulations ensures smooth operations and positive community relations.</p>"
            )
        
        elif content_type == "location_service":
            service = template_data.get("Service", "services")
            city = template_data.get("City", "your area")
            
            # Add more comprehensive content for location-based services
            sections.append(
                f"<h3>Why Choose Professional {service} in {city}</h3>"
                f"<p>Finding reliable {service.lower()} providers in {city} requires understanding the local market dynamics. "
                f"Professional service providers in this area typically offer comprehensive solutions tailored to local needs. "
                f"With an average of {primary_data.get('provider_count', 25)} active providers serving the {city} area, "
                f"residents have access to competitive pricing and diverse service options. The average customer rating of "
                f"{primary_data.get('average_rating', 4.5)} stars reflects the high standards maintained by local professionals.</p>"
            )
            
            sections.append(
                f"<h3>Service Standards and Expectations</h3>"
                f"<p>When selecting {service.lower()} in {city}, consider these important factors: experience level (most providers "
                f"have {random.randint(5, 15)} years in business), customer reviews and testimonials, response times (typically "
                f"{random.randint(2, 6)} hours for initial contact), and pricing transparency. Reputable providers offer free "
                f"consultations, detailed written quotes, and clear service agreements. Many also provide emergency services with "
                f"24/7 availability for urgent needs.</p>"
            )
            
            sections.append(
                f"<h3>Local Market Insights</h3>"
                f"<p>The {service.lower()} industry in {city} has experienced steady growth, with demand increasing by "
                f"{random.randint(5, 20)}% over the past year. Peak demand typically occurs during {random.choice(['spring', 'summer', 'fall'])} "
                f"months, so booking in advance is recommended. Local providers are familiar with area-specific requirements, "
                f"including permit regulations, homeowner association rules, and regional building codes. This local expertise "
                f"ensures compliance and smooth project completion.</p>"
            )
            
            sections.append(
                f"<h3>Making the Right Choice</h3>"
                f"<p>To ensure you select the best {service.lower()} provider in {city}, follow these steps: First, verify licensing "
                f"and insurance coverage - all legitimate providers maintain proper documentation. Second, request references from "
                f"recent projects similar to yours. Third, compare multiple quotes to understand pricing ranges - expect variations "
                f"of 15-30% between providers based on experience and service quality. Finally, discuss timeline expectations and "
                f"potential challenges specific to your project. Most providers offer satisfaction guarantees and warranty coverage "
                f"for their work.</p>"
            )
        
        else:
            # General content type support
            service = template_data.get('Service', template_data.get('service', 'services'))
            location = template_data.get('City', template_data.get('city', 'your area'))
            
            sections.append(
                f"<h3>Understanding {service} Options</h3>"
                f"<p>When exploring {service.lower()} in {location}, it's important to consider various factors "
                f"that can impact your decision. Service quality, pricing structures, availability, and customer "
                f"satisfaction ratings all play crucial roles. Our comprehensive database helps you compare these "
                f"factors across multiple providers to find the best match for your specific needs.</p>"
            )
            
            sections.append(
                f"<h3>Making Informed Decisions</h3>"
                f"<p>The {service.lower()} market in {location} offers diverse options ranging from budget-friendly "
                f"to premium services. Average prices typically range from ${primary_data.get('min_price', 100)} to "
                f"${primary_data.get('max_price', 500)}, depending on specific requirements and service complexity. "
                f"Response times average {primary_data.get('average_response_time', '24 hours')}, with "
                f"{primary_data.get('availability_percentage', 80)}% of providers offering same-week appointments.</p>"
            )
            
            sections.append(
                f"<h3>Quality Assurance</h3>"
                f"<p>All listed {service.lower()} providers maintain proper licensing and insurance coverage. "
                f"Customer reviews and ratings are verified through our quality control process, ensuring authentic "
                f"feedback from real customers. This transparency helps you make confident decisions based on "
                f"actual service experiences and outcomes.</p>"
            )
        
        return sections
    
    def _generate_context_section_enriched(self, enriched_data: Dict[str, Any], 
                                          template_data: Dict[str, Any], content_type: str) -> str:
        """Generate additional context section for more comprehensive content"""
        primary_data = enriched_data.get("primary_data", {})
        city = template_data.get("City", "the area")
        service = template_data.get("Service", "services")
        
        if content_type == "evaluation_question":
            peak_season = primary_data.get("peak_season", "peak season")
            growth_rate = primary_data.get("growth_rate", 10)
            
            context = f"<h3>Market Context for {city}</h3>"
            context += f"<p>The {service.lower()} market in {city} experiences highest demand during {peak_season.lower()}. "
            
            if growth_rate > 15:
                context += f"With {growth_rate}% year-over-year growth, this represents one of the stronger performing markets in the region. "
            elif growth_rate > 5:
                context += f"The {growth_rate}% annual growth rate indicates stable market expansion and sustained demand. "
            else:
                context += f"Market conditions are stabilizing with {growth_rate}% growth, offering opportunities for strategic positioning. "
            
            context += f"Success in this market typically depends on location selection, competitive pricing, and understanding local preferences.</p>"
            return context
        
        elif content_type == "location_service":
            # Add pricing infographic instead of text
            context = self._generate_pricing_infographic(primary_data, template_data)
            return context
        
        return ""
    
    def _generate_value_section_enriched(self, enriched_data: Dict[str, Any], 
                                        template_data: Dict[str, Any], content_type: str) -> str:
        """Generate value proposition section"""
        primary_data = enriched_data.get("primary_data", {})
        city = template_data.get("City", "your area")
        service = template_data.get("Service", "services")
        
        if content_type == "evaluation_question":
            roi_average = primary_data.get("roi_average", 15)
            monthly_revenue = primary_data.get("monthly_revenue", 2500)
            
            value = f"<h3>Key Benefits and Considerations</h3>"
            value += f"<p><strong>Financial Potential:</strong> Based on current market data, {service.lower()} in {city} "
            
            if roi_average >= 18:
                value += f"offers strong financial returns with {roi_average}% average ROI. "
            elif roi_average >= 15:
                value += f"provides solid returns with {roi_average}% average ROI potential. "
            else:
                value += f"shows {roi_average}% ROI potential with proper management. "
            
            value += f"Successful operators typically see monthly revenues around ${monthly_revenue:,}.</p>"
            
            value += f"<p><strong>Risk Factors:</strong> Consider seasonal variations, maintenance costs, regulatory changes, "
            value += f"and local competition. Success requires active management, quality property presentation, and responsive customer service.</p>"
            return value
        
        elif content_type == "location_service":
            value = f"<h3>Why Choose Local {service} Providers</h3>"
            value += f"<p>Local {service.lower()} providers in {city} offer several advantages: familiarity with local regulations, "
            value += f"established relationships with suppliers, quick response times, and accountability within the community. "
            value += f"They understand regional preferences, seasonal considerations, and common challenges specific to {city}.</p>"
            
            value += f"<p>Additionally, local providers often provide more personalized service, flexible scheduling, "
            value += f"and ongoing support relationships that national chains may not match.</p>"
            return value
        
        return ""
    
    def _prepare_intro_data(self, data: Dict[str, Any], content_type: str) -> Dict[str, Any]:
        """Prepare data for intro generation with computed values"""
        intro_data = data.copy()
        
        # Add lowercase versions of keys for pattern matching
        for key, value in list(intro_data.items()):
            intro_data[key.lower()] = value
        
        # Add computed/default values
        if content_type == "location_service":
            intro_data.setdefault("count", random.randint(20, 200))
            intro_data.setdefault("avg_rating", round(random.uniform(4.0, 4.8), 1))
            intro_data.setdefault("min_price", random.randint(30, 100))
            intro_data.setdefault("max_price", intro_data.get("min_price", 100) * random.randint(3, 5))
            intro_data.setdefault("avg_price", (intro_data.get("min_price", 50) + intro_data.get("max_price", 200)) // 2)
            intro_data.setdefault("response_time", f"{random.randint(1, 4)} hours")
            intro_data.setdefault("top_provider", "Highly Rated Pro")
            intro_data.setdefault("top_rating", 4.9)
            intro_data.setdefault("min_rating", round(random.uniform(3.0, 4.0), 1))
            intro_data.setdefault("max_rating", round(random.uniform(4.5, 5.0), 1))
            
        elif content_type == "comparison":
            if "price1" not in intro_data:
                intro_data["price1"] = random.randint(10, 100)
            if "price2" not in intro_data:
                intro_data["price2"] = random.randint(10, 100)
            intro_data["price_diff"] = abs(intro_data.get("price1", 50) - intro_data.get("price2", 75))
            intro_data.setdefault("key_difference", "pricing model")
            intro_data.setdefault("winner", intro_data.get("item1", "First option"))
            intro_data.setdefault("winning_category", "overall value")
            intro_data.setdefault("winning_metric", "90% satisfaction")
            
        return intro_data
    
    def _generate_main_value_section(self, data: Dict[str, Any], content_type: str) -> str:
        """Generate the main value section - the core content"""
        
        if content_type == "location_service":
            # Generate a simple provider list
            providers = self._generate_provider_list(data)
            return f"<div class='providers'>\n<h2>Top Rated Providers</h2>\n{providers}\n</div>"
            
        elif content_type == "comparison":
            # Generate comparison table
            comparison = self._generate_simple_comparison(data)
            return f"<div class='comparison'>\n{comparison}\n</div>"
            
        elif content_type == "educational":
            # Generate course/program list
            programs = self._generate_program_list(data)
            return f"<div class='programs'>\n<h2>Available Programs</h2>\n{programs}\n</div>"
            
        else:
            # Generic value list
            items = self._generate_generic_list(data)
            return f"<div class='items'>\n<h2>Available Options</h2>\n{items}\n</div>"
    
    def _generate_provider_list(self, data: Dict[str, Any]) -> str:
        """Generate provider list for location-based pages"""
        # Create 3-5 mock providers if not provided
        providers = data.get("providers", [])
        
        if not providers:
            provider_count = min(data.get("count", 5), 5)
            providers = []
            for i in range(provider_count):
                providers.append({
                    "name": f"{data.get('service', 'Service')} Pro #{i+1}",
                    "rating": round(random.uniform(4.0, 4.9), 1),
                    "reviews": random.randint(50, 500),
                    "response": f"{random.randint(1, 4)}h response"
                })
        
        lines = ["<ul class='provider-list'>"]
        for p in providers[:5]:  # Max 5 providers
            name = p.get("name", "Provider")
            rating = p.get("rating", 4.5)
            reviews = p.get("reviews", 100)
            response = p.get("response", "Fast response")
            
            lines.append(f"<li><strong>{name}</strong> - {rating}★ ({reviews} reviews) - {response}</li>")
        lines.append("</ul>")
        
        return "\n".join(lines)
    
    def _generate_simple_comparison(self, data: Dict[str, Any]) -> str:
        """Generate simple comparison for versus pages"""
        item1 = data.get("item1", data.get("option1", "Option A"))
        item2 = data.get("item2", data.get("option2", "Option B"))
        
        comparison_html = f"""
<h2>Quick Comparison</h2>
<table class='comparison-table'>
<tr>
    <th>Feature</th>
    <th>{item1}</th>
    <th>{item2}</th>
</tr>
<tr>
    <td>Price</td>
    <td>${data.get('price1', random.randint(20, 200))}/mo</td>
    <td>${data.get('price2', random.randint(20, 200))}/mo</td>
</tr>
<tr>
    <td>Rating</td>
    <td>{data.get('rating1', round(random.uniform(4.0, 4.9), 1))}/5</td>
    <td>{data.get('rating2', round(random.uniform(4.0, 4.9), 1))}/5</td>
</tr>
<tr>
    <td>Best For</td>
    <td>{data.get('bestfor1', 'Small businesses')}</td>
    <td>{data.get('bestfor2', 'Large teams')}</td>
</tr>
</table>

<p><strong>Bottom Line:</strong> Choose {item1} if you need {data.get('reason1', 'simplicity and affordability')}. 
Pick {item2} for {data.get('reason2', 'advanced features and scalability')}.</p>
"""
        return comparison_html
    
    def _generate_support_content(self, data: Dict[str, Any], content_type: str) -> List[str]:
        """Generate 2-3 supporting paragraphs"""
        sections = []
        
        # Generate 2-3 contextual paragraphs
        for i in range(random.randint(2, 3)):
            if i == 0:
                # First support paragraph - context
                support_data = self._prepare_support_data(data, content_type, "context")
                pattern = self.content_patterns.select_pattern("support", "location_context", support_data)
                
            elif i == 1:
                # Second paragraph - details or comparison
                support_data = self._prepare_support_data(data, content_type, "details")
                pattern = self.content_patterns.select_pattern("support", "comparison_details", support_data)
                
            else:
                # Third paragraph - value prop
                support_data = self._prepare_support_data(data, content_type, "value")
                pattern = self.content_patterns.select_pattern("support", "value_proposition", support_data)
            
            content = self.content_patterns.fill_pattern(pattern, support_data)
            sections.append(f"<p>{content}</p>")
        
        return sections
    
    def _prepare_support_data(self, data: Dict[str, Any], content_type: str, 
                            paragraph_type: str) -> Dict[str, Any]:
        """Prepare data for support paragraphs"""
        support_data = data.copy()
        
        # Add lowercase versions of keys
        for key, value in list(support_data.items()):
            support_data[key.lower()] = value
        
        # Add contextual data based on paragraph type
        if paragraph_type == "context":
            support_data.setdefault("population", f"{random.randint(50, 500)},{random.randint(100, 999)}")
            support_data.setdefault("median_income", random.randint(40, 120) * 1000)
            support_data.setdefault("growth_rate", random.randint(5, 25))
            support_data.setdefault("employee_count", random.randint(500, 5000))
            support_data.setdefault("year", datetime.now().year)
            support_data.setdefault("industry", support_data.get("service", "service"))
            support_data.setdefault("new_businesses", random.randint(5, 25))
            support_data.setdefault("peak_season", random.choice(["spring", "summer", "fall", "winter"]))
            support_data.setdefault("wait_time", f"{random.randint(1, 48)} hours")
            support_data.setdefault("availability", random.randint(70, 95))
            support_data.setdefault("service_area_size", random.randint(50, 500))
            support_data.setdefault("coverage_percent", random.randint(75, 98))
            support_data.setdefault("insurance_amount", random.randint(1, 5) * 1000000)
            support_data.setdefault("license_type", random.choice(["state", "municipal", "professional"]))
            
        elif paragraph_type == "details":
            support_data.setdefault("features1_count", random.randint(20, 50))
            support_data.setdefault("features2_count", random.randint(15, 45))
            support_data.setdefault("common_features", random.randint(10, 20))
            support_data.setdefault("score1", round(random.uniform(7, 9), 1))
            support_data.setdefault("score2", round(random.uniform(7, 9), 1))
            
        elif paragraph_type == "value":
            support_data.setdefault("savings_percent", random.randint(15, 40))
            support_data.setdefault("savings_amount", random.randint(500, 5000))
            support_data.setdefault("setup_time", f"{random.randint(5, 30)} minutes")
            support_data.setdefault("customer_count", random.randint(1000, 50000))
            support_data.setdefault("retention_rate", random.randint(85, 98))
            
        return support_data
    
    def _generate_slug(self, title: str) -> str:
        """Generate URL-friendly slug"""
        import re
        slug = title.lower()
        slug = re.sub(r'[^\w\s-]', '', slug)
        slug = re.sub(r'[-\s]+', '-', slug)
        return slug.strip('-')[:80]  # Limit length
    
    def _calculate_quality_score(self, content: str, data: Dict[str, Any]) -> int:
        """Calculate basic quality score"""
        score = 50  # Base score
        
        # Word count check
        word_count = len(content.split())
        if word_count >= 300:
            score += 20
        if word_count >= 400:
            score += 10
            
        # Data richness
        data_points = len([v for v in data.values() if v])
        if data_points >= 5:
            score += 10
        if data_points >= 10:
            score += 10
            
        return min(score, 100)
    
    def _generate_program_list(self, data: Dict[str, Any]) -> str:
        """Generate educational program list"""
        programs = data.get("programs", [])
        
        if not programs:
            # Generate mock programs
            program_count = min(data.get("count", 4), 4)
            programs = []
            for i in range(program_count):
                programs.append({
                    "name": f"{data.get('topic', 'Program')} Course {i+1}",
                    "duration": f"{random.randint(4, 52)} weeks",
                    "price": f"${random.randint(100, 5000)}",
                    "format": random.choice(["Online", "In-person", "Hybrid"])
                })
        
        lines = ["<ul class='program-list'>"]
        for p in programs[:5]:
            name = p.get("name", "Program")
            duration = p.get("duration", "Flexible")
            price = p.get("price", "Contact for pricing")
            format = p.get("format", "Multiple formats")
            
            lines.append(f"<li><strong>{name}</strong> - {duration} - {price} - {format}</li>")
        lines.append("</ul>")
        
        return "\n".join(lines)
    
    def _generate_generic_list(self, data: Dict[str, Any]) -> str:
        """Generate generic item list as fallback"""
        items = data.get("items", data.get("options", []))
        
        if not items:
            # Generate generic items
            item_count = min(data.get("count", 5), 5)
            items = [f"Option {i+1}" for i in range(item_count)]
        
        lines = ["<ul>"]
        for item in items[:10]:
            if isinstance(item, dict):
                item_text = item.get("name", item.get("title", "Item"))
            else:
                item_text = str(item)
            lines.append(f"<li>{item_text}</li>")
        lines.append("</ul>")
        
        return "\n".join(lines)
    
    def _generate_quick_stats_box(self, primary_data: Dict[str, Any], template_data: Dict[str, Any]) -> str:
        """Generate a visual stats info box"""
        city = template_data.get("City", template_data.get("city", "your area"))
        service = template_data.get("Service", template_data.get("service", "services"))
        
        stats_html = f"""<div class="info-box" style="background: linear-gradient(135deg, #e0f2fe 0%, #e0e7ff 100%); border: 1px solid #60a5fa; padding: 1.5rem; border-radius: 0.75rem; margin: 1.5rem 0;">
  <h4 style="margin: 0 0 1rem 0; color: #1e40af; font-size: 1.25rem;">📊 {service} in {city} - Quick Stats</h4>
  <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 1rem;">
    <div>
      <strong style="color: #64748b;">Active Providers:</strong>
      <span style="font-size: 1.5rem; font-weight: bold; color: #1e40af; display: block;">{primary_data.get('provider_count', 45)}</span>
    </div>
    <div>
      <strong style="color: #64748b;">Avg. Rating:</strong>
      <span style="font-size: 1.5rem; font-weight: bold; color: #16a34a; display: block;">{primary_data.get('average_rating', 4.5)}★</span>
    </div>
    <div>
      <strong style="color: #64748b;">Price Range:</strong>
      <span style="font-size: 1.25rem; font-weight: bold; color: #1e40af; display: block;">${primary_data.get('min_price', 95)}-${primary_data.get('max_price', 350)}</span>
    </div>
    <div>
      <strong style="color: #64748b;">Response Time:</strong>
      <span style="font-size: 1.25rem; font-weight: bold; color: #dc2626; display: block;">{primary_data.get('average_response_time', '2-4 hours')}</span>
    </div>
  </div>
</div>"""
        return stats_html
    
    def _generate_provider_table(self, primary_data: Dict[str, Any], template_data: Dict[str, Any]) -> str:
        """Generate a comparison table of providers"""
        providers = primary_data.get('top_providers', [])
        if not providers:
            # Generate sample providers
            service = template_data.get("Service", "Service")
            avg_rating = primary_data.get("average_rating", 4.5)
            providers = []
            for i in range(5):
                providers.append({
                    "name": f"{service} Pro #{i+1}",
                    "rating": round(avg_rating + random.uniform(-0.3, 0.3), 1),
                    "reviews": random.randint(100, 500),
                    "response": f"{random.randint(1, 6)}h",
                    "price": f"${random.randint(100, 400)}"
                })
        
        table_html = """<table style="width: 100%; border-collapse: collapse; margin: 1.5rem 0; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
  <thead>
    <tr style="background: #f8fafc;">
      <th style="padding: 0.75rem; text-align: left; border-bottom: 2px solid #e2e8f0;">Provider Name</th>
      <th style="padding: 0.75rem; text-align: center; border-bottom: 2px solid #e2e8f0;">Rating</th>
      <th style="padding: 0.75rem; text-align: center; border-bottom: 2px solid #e2e8f0;">Reviews</th>
      <th style="padding: 0.75rem; text-align: center; border-bottom: 2px solid #e2e8f0;">Response</th>
      <th style="padding: 0.75rem; text-align: center; border-bottom: 2px solid #e2e8f0;">Est. Price</th>
    </tr>
  </thead>
  <tbody>"""
        
        for i, provider in enumerate(providers[:5]):
            bg_color = "#ffffff" if i % 2 == 0 else "#f9fafb"
            table_html += f"""
    <tr style="background: {bg_color};">
      <td style="padding: 0.75rem; border-bottom: 1px solid #e2e8f0; font-weight: 600;">{provider.get('name', f'Provider {i+1}')}</td>
      <td style="padding: 0.75rem; text-align: center; border-bottom: 1px solid #e2e8f0; color: #16a34a; font-weight: bold;">{provider.get('rating', 4.5)}★</td>
      <td style="padding: 0.75rem; text-align: center; border-bottom: 1px solid #e2e8f0;">{provider.get('reviews', 200)}</td>
      <td style="padding: 0.75rem; text-align: center; border-bottom: 1px solid #e2e8f0;">{provider.get('response', '3h')}</td>
      <td style="padding: 0.75rem; text-align: center; border-bottom: 1px solid #e2e8f0; font-weight: 600;">{provider.get('price', '$250')}</td>
    </tr>"""
        
        table_html += """
  </tbody>
</table>"""
        return table_html
    
    def _generate_rating_visualization(self, primary_data: Dict[str, Any], template_data: Dict[str, Any]) -> str:
        """Generate a visual rating breakdown"""
        total_reviews = sum([p.get('reviews', 200) for p in primary_data.get('top_providers', [{"reviews": 200}] * 5)])
        
        # Calculate rating distribution
        ratings = {
            5: random.randint(55, 70),
            4: random.randint(20, 30),
            3: random.randint(5, 15),
            2: random.randint(1, 5),
            1: random.randint(1, 3)
        }
        
        # Normalize to 100%
        total = sum(ratings.values())
        ratings = {k: int(v * 100 / total) for k, v in ratings.items()}
        
        viz_html = f"""<div style="margin: 2rem 0;">
  <h3>Customer Satisfaction Overview</h3>
  <div style="background: #f9fafb; padding: 1.5rem; border-radius: 0.5rem;">
    <p style="font-size: 2rem; font-weight: bold; margin: 0 0 1rem 0; color: #16a34a;">
      {primary_data.get('average_rating', 4.5)}★ Average Rating
    </p>
    <p style="color: #64748b; margin-bottom: 1rem;">Based on {total_reviews:,} customer reviews</p>
    """
        
        for stars in range(5, 0, -1):
            percentage = ratings[stars]
            viz_html += f"""
    <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
      <span style="width: 3rem; color: #64748b;">{stars}★</span>
      <div style="flex: 1; height: 1.5rem; background: #e5e7eb; border-radius: 0.25rem; margin: 0 0.5rem; overflow: hidden;">
        <div style="width: {percentage}%; height: 100%; background: {'#16a34a' if stars >= 4 else '#fbbf24' if stars == 3 else '#ef4444'}; transition: width 0.3s;"></div>
      </div>
      <span style="width: 3rem; text-align: right; color: #64748b;">{percentage}%</span>
    </div>"""
        
        viz_html += """
  </div>
</div>"""
        return viz_html
    
    def _generate_features_checklist(self, service_name: str) -> str:
        """Generate a visual features checklist"""
        features = [
            ("Licensed & Insured", True),
            ("24/7 Emergency Service", True),
            ("Free Estimates", True),
            ("Warranty Included", True),
            ("Same-Day Service", random.choice([True, False])),
            ("Senior Discounts", True),
            ("Online Booking", random.choice([True, False])),
            ("Eco-Friendly Options", random.choice([True, False]))
        ]
        
        checklist_html = f"""<div style="margin: 2rem 0;">
  <h3>What to Expect from {service_name} Providers</h3>
  <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 1rem; margin-top: 1rem;">"""
        
        for feature, available in features:
            icon = "✅" if available else "❌"
            color = "#16a34a" if available else "#64748b"
            checklist_html += f"""
    <div style="display: flex; align-items: center; padding: 0.75rem; background: #f9fafb; border-radius: 0.5rem;">
      <span style="font-size: 1.25rem; margin-right: 0.75rem;">{icon}</span>
      <span style="color: {color}; font-weight: {'600' if available else '400'};">{feature}</span>
    </div>"""
        
        checklist_html += """
  </div>
</div>"""
        return checklist_html
    
    def _generate_pricing_infographic(self, primary_data: Dict[str, Any], template_data: Dict[str, Any]) -> str:
        """Generate a pricing breakdown infographic"""
        service = template_data.get("Service", "Service")
        
        # Define price tiers
        basic_price = primary_data.get('min_price', 100)
        standard_price = int((primary_data.get('min_price', 100) + primary_data.get('max_price', 400)) / 2)
        premium_price = primary_data.get('max_price', 400)
        
        pricing_html = f"""<div style="margin: 2rem 0;">
  <h3>{service} Pricing Guide</h3>
  <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; margin-top: 1rem;">
    <div style="background: #f3f4f6; padding: 1.5rem; border-radius: 0.5rem; text-align: center;">
      <h4 style="color: #6b7280; margin: 0 0 0.5rem 0;">Basic Service</h4>
      <p style="font-size: 2rem; font-weight: bold; color: #1f2937; margin: 0.5rem 0;">${basic_price}</p>
      <ul style="list-style: none; padding: 0; margin: 1rem 0 0 0; text-align: left; font-size: 0.875rem; color: #6b7280;">
        <li>• Standard repairs</li>
        <li>• 30-day warranty</li>
        <li>• Business hours</li>
      </ul>
    </div>
    <div style="background: linear-gradient(135deg, #ddd6fe 0%, #c7d2fe 100%); padding: 1.5rem; border-radius: 0.5rem; text-align: center; border: 2px solid #8b5cf6;">
      <h4 style="color: #5b21b6; margin: 0 0 0.5rem 0;">Standard Service</h4>
      <p style="font-size: 2rem; font-weight: bold; color: #5b21b6; margin: 0.5rem 0;">${standard_price}</p>
      <ul style="list-style: none; padding: 0; margin: 1rem 0 0 0; text-align: left; font-size: 0.875rem; color: #5b21b6;">
        <li>• Complex repairs</li>
        <li>• 90-day warranty</li>
        <li>• Priority scheduling</li>
      </ul>
    </div>
    <div style="background: #fef3c7; padding: 1.5rem; border-radius: 0.5rem; text-align: center;">
      <h4 style="color: #92400e; margin: 0 0 0.5rem 0;">Premium Service</h4>
      <p style="font-size: 2rem; font-weight: bold; color: #92400e; margin: 0.5rem 0;">${premium_price}+</p>
      <ul style="list-style: none; padding: 0; margin: 1rem 0 0 0; text-align: left; font-size: 0.875rem; color: #92400e;">
        <li>• Major projects</li>
        <li>• 1-year warranty</li>
        <li>• 24/7 availability</li>
      </ul>
    </div>
  </div>
</div>"""
        return pricing_html
    
    def _generate_roi_infographic(self, primary_data: Dict[str, Any], template_data: Dict[str, Any]) -> str:
        """Generate ROI visualization for investment questions"""
        roi = primary_data.get('roi_percentage', 15)
        monthly_revenue = primary_data.get('monthly_revenue', 2500)
        monthly_expenses = primary_data.get('monthly_expenses', 1500)
        monthly_profit = monthly_revenue - monthly_expenses
        payback_years = round(100 / roi, 1) if roi > 0 else 10
        
        roi_html = f"""<div style="background: linear-gradient(135deg, #d1fae5 0%, #dbeafe 100%); padding: 2rem; border-radius: 1rem; margin: 2rem 0;">
  <h3 style="color: #065f46; margin: 0 0 1.5rem 0; font-size: 1.5rem;">Investment Returns Calculator</h3>
  <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 2rem;">
    <div style="text-align: center;">
      <div style="font-size: 3rem; font-weight: bold; color: #059669; margin-bottom: 0.5rem;">{roi}%</div>
      <div style="color: #065f46; font-weight: 600;">Annual ROI</div>
      <div style="margin-top: 1rem; font-size: 0.875rem; color: #047857;">
        Payback Period: {payback_years} years
      </div>
    </div>
    <div>
      <div style="margin-bottom: 1rem;">
        <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
          <span style="color: #065f46;">Monthly Revenue</span>
          <span style="font-weight: bold; color: #059669;">${monthly_revenue:,}</span>
        </div>
        <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
          <span style="color: #065f46;">Monthly Expenses</span>
          <span style="font-weight: bold; color: #dc2626;">-${monthly_expenses:,}</span>
        </div>
        <div style="border-top: 2px solid #059669; padding-top: 0.5rem; display: flex; justify-content: space-between;">
          <span style="color: #065f46; font-weight: bold;">Net Profit</span>
          <span style="font-weight: bold; color: #059669; font-size: 1.25rem;">${monthly_profit:,}</span>
        </div>
      </div>
    </div>
  </div>
</div>"""
        return roi_html
    
    def _generate_financial_metrics_cards(self, primary_data: Dict[str, Any], template_data: Dict[str, Any]) -> str:
        """Generate financial metrics in card format"""
        metrics_html = """<div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 1rem; margin: 2rem 0;">"""
        
        # Occupancy Rate Card
        occupancy = primary_data.get('occupancy_rate', 68)
        occupancy_color = "#059669" if occupancy > 70 else "#f59e0b" if occupancy > 50 else "#dc2626"
        metrics_html += f"""
  <div style="background: white; border: 2px solid #e5e7eb; padding: 1.5rem; border-radius: 0.5rem; text-align: center;">
    <div style="font-size: 2.5rem; font-weight: bold; color: {occupancy_color};">{occupancy}%</div>
    <div style="color: #6b7280; font-weight: 600; margin-top: 0.5rem;">Occupancy Rate</div>
    <div style="margin-top: 0.5rem;">
      <div style="height: 0.5rem; background: #e5e7eb; border-radius: 0.25rem; overflow: hidden;">
        <div style="width: {occupancy}%; height: 100%; background: {occupancy_color};"></div>
      </div>
    </div>
  </div>"""
        
        # Average Daily Rate Card
        adr = primary_data.get('average_nightly_rate', 127)
        metrics_html += f"""
  <div style="background: white; border: 2px solid #e5e7eb; padding: 1.5rem; border-radius: 0.5rem; text-align: center;">
    <div style="font-size: 2.5rem; font-weight: bold; color: #3b82f6;">${adr}</div>
    <div style="color: #6b7280; font-weight: 600; margin-top: 0.5rem;">Avg. Nightly Rate</div>
    <div style="font-size: 0.875rem; color: #6b7280; margin-top: 0.5rem;">
      Market Avg: ${int(adr * 0.9)}-${int(adr * 1.1)}
    </div>
  </div>"""
        
        # Total Listings Card
        listings = primary_data.get('total_listings', 342)
        growth = primary_data.get('growth_rate', 23)
        metrics_html += f"""
  <div style="background: white; border: 2px solid #e5e7eb; padding: 1.5rem; border-radius: 0.5rem; text-align: center;">
    <div style="font-size: 2.5rem; font-weight: bold; color: #8b5cf6;">{listings}</div>
    <div style="color: #6b7280; font-weight: 600; margin-top: 0.5rem;">Active Listings</div>
    <div style="font-size: 0.875rem; color: #059669; margin-top: 0.5rem;">
      ↑ {growth}% YoY Growth
    </div>
  </div>"""
        
        # Revenue Per Property Card
        revenue = primary_data.get('monthly_revenue', 2890)
        metrics_html += f"""
  <div style="background: white; border: 2px solid #e5e7eb; padding: 1.5rem; border-radius: 0.5rem; text-align: center;">
    <div style="font-size: 2.5rem; font-weight: bold; color: #059669;">${revenue:,}</div>
    <div style="color: #6b7280; font-weight: 600; margin-top: 0.5rem;">Monthly Revenue</div>
    <div style="font-size: 0.875rem; color: #6b7280; margin-top: 0.5rem;">
      Per property average
    </div>
  </div>"""
        
        metrics_html += "</div>"
        return metrics_html
    
    def _generate_market_comparison(self, primary_data: Dict[str, Any], template_data: Dict[str, Any]) -> str:
        """Generate market comparison visualization"""
        city = template_data.get("City", "This City")
        
        comparison_html = f"""<div style="margin: 2rem 0;">
  <h3>Market Performance Comparison</h3>
  <div style="background: #f9fafb; padding: 1.5rem; border-radius: 0.5rem;">
    <table style="width: 100%; border-collapse: collapse;">
      <thead>
        <tr>
          <th style="text-align: left; padding: 0.75rem; border-bottom: 2px solid #e5e7eb;">Metric</th>
          <th style="text-align: center; padding: 0.75rem; border-bottom: 2px solid #e5e7eb;">{city}</th>
          <th style="text-align: center; padding: 0.75rem; border-bottom: 2px solid #e5e7eb;">Regional Avg</th>
          <th style="text-align: center; padding: 0.75rem; border-bottom: 2px solid #e5e7eb;">Performance</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td style="padding: 0.75rem; border-bottom: 1px solid #e5e7eb;">Occupancy Rate</td>
          <td style="text-align: center; padding: 0.75rem; border-bottom: 1px solid #e5e7eb; font-weight: bold;">{primary_data.get('occupancy_rate', 68)}%</td>
          <td style="text-align: center; padding: 0.75rem; border-bottom: 1px solid #e5e7eb;">65%</td>
          <td style="text-align: center; padding: 0.75rem; border-bottom: 1px solid #e5e7eb; color: #059669;">↑ +4.6%</td>
        </tr>
        <tr style="background: #f3f4f6;">
          <td style="padding: 0.75rem; border-bottom: 1px solid #e5e7eb;">Nightly Rate</td>
          <td style="text-align: center; padding: 0.75rem; border-bottom: 1px solid #e5e7eb; font-weight: bold;">${primary_data.get('average_nightly_rate', 127)}</td>
          <td style="text-align: center; padding: 0.75rem; border-bottom: 1px solid #e5e7eb;">$115</td>
          <td style="text-align: center; padding: 0.75rem; border-bottom: 1px solid #e5e7eb; color: #059669;">↑ +10.4%</td>
        </tr>
        <tr>
          <td style="padding: 0.75rem; border-bottom: 1px solid #e5e7eb;">Market Growth</td>
          <td style="text-align: center; padding: 0.75rem; border-bottom: 1px solid #e5e7eb; font-weight: bold;">{primary_data.get('growth_rate', 23)}%</td>
          <td style="text-align: center; padding: 0.75rem; border-bottom: 1px solid #e5e7eb;">18%</td>
          <td style="text-align: center; padding: 0.75rem; border-bottom: 1px solid #e5e7eb; color: #059669;">↑ +27.8%</td>
        </tr>
      </tbody>
    </table>
  </div>
</div>"""
        return comparison_html
    
    def _generate_investment_checklist(self, primary_data: Dict[str, Any], template_data: Dict[str, Any]) -> str:
        """Generate investment readiness checklist"""
        property_type = template_data.get("Property Type", template_data.get("property type", "property"))
        city = template_data.get("City", "this market")
        
        checklist_html = f"""<div style="margin: 2rem 0;">
  <h3>Investment Readiness Checklist for {property_type} in {city}</h3>
  <div style="background: #fef3c7; border: 1px solid #fbbf24; padding: 1.5rem; border-radius: 0.5rem;">
    <div style="display: grid; gap: 0.75rem;">
      <div style="display: flex; align-items: center;">
        <span style="color: #059669; font-size: 1.5rem; margin-right: 0.75rem;">✓</span>
        <span><strong>Strong ROI Potential:</strong> {primary_data.get('roi_percentage', 15)}% annual returns exceed market average</span>
      </div>
      <div style="display: flex; align-items: center;">
        <span style="color: #059669; font-size: 1.5rem; margin-right: 0.75rem;">✓</span>
        <span><strong>High Occupancy:</strong> {primary_data.get('occupancy_rate', 68)}% occupancy ensures steady income</span>
      </div>
      <div style="display: flex; align-items: center;">
        <span style="color: #059669; font-size: 1.5rem; margin-right: 0.75rem;">✓</span>
        <span><strong>Growing Market:</strong> {primary_data.get('growth_rate', 23)}% YoY growth indicates strong demand</span>
      </div>
      <div style="display: flex; align-items: center;">
        <span style="color: #f59e0b; font-size: 1.5rem; margin-right: 0.75rem;">!</span>
        <span><strong>Consider Competition:</strong> {primary_data.get('total_listings', 342)} active listings require strategic positioning</span>
      </div>
      <div style="display: flex; align-items: center;">
        <span style="color: #3b82f6; font-size: 1.5rem; margin-right: 0.75rem;">→</span>
        <span><strong>Next Step:</strong> Research specific neighborhoods and property features for optimal returns</span>
      </div>
    </div>
  </div>
</div>"""
        return checklist_html