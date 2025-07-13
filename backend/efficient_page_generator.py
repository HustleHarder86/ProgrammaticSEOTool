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
        
        # 2. Generate title and H1
        title = self._fill_template(template.get("title_pattern", ""), data_row)
        h1 = self._fill_template(template.get("h1_pattern", title), data_row)
        
        # 3. Generate meta description
        meta_desc = self._generate_meta_description(title, data_row, content_type)
        
        # 4. Generate content sections
        content_html = self._generate_content_html(
            template, data_row, content_type, h1
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
        
        if any(word in pattern for word in ["vs", "versus", "compare"]):
            return "comparison"
        elif any(word in pattern for word in ["in", "near", "at"]) and \
             any(key in data for key in ["location", "city", "area"]):
            return "location_service"
        elif any(word in pattern for word in ["course", "learn", "study"]):
            return "educational"
        elif any(word in pattern for word in ["buy", "shop", "product"]):
            return "product_location"
        else:
            return "location_service"  # Default
    
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