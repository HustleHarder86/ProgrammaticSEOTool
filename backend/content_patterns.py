"""Content patterns for efficient programmatic SEO content generation"""
import random
import hashlib
import json
from typing import Dict, List, Any, Optional
from data_mapper import data_mapper


class ContentPatterns:
    """Manages content variation patterns for programmatic SEO"""
    
    def __init__(self):
        # Introduction patterns for different business types
        self.intro_patterns = {
            "evaluation_question": [
                "{answer}, {Service} can be {profitability} in {City}. Average occupancy: {occupancy_rate}%, typical nightly rate: ${average_nightly_rate}.",
                "{Service} properties in {City} show {performance} potential. ROI averages {roi_percentage}% with {market_strength} demand.",
                "Short-term rental data for {Service} in {City}: {occupancy_rate}% occupancy, ${monthly_revenue} average monthly revenue, {regulation_status}.",
                "{City}'s {Service} rental market offers {market_strength} returns. Expect ${average_nightly_rate}/night rates with {occupancy_rate}% occupancy.",
                "Analysis shows {Service} in {City} ranks {ranking} for profitability. Key metrics: ${average_nightly_rate}/night, {occupancy_rate}% occupancy."
            ],
            "general_question": [
                "The answer is {answer}. In {city}, {supporting_fact} with {data_point}.",
                "{answer_intro}. Data shows {statistic} in {city} for {topic}.",
                "Based on {city} data: {answer}. Key factor: {main_reason}.",
                "For {topic} in {city}: {answer}. {percentage}% of cases show {trend}.",
                "{answer}. {city} statistics indicate {supporting_data}."
            ],
            "location_service": [
                "Find {count} {Service} providers in {City} with average rating of {avg_rating} stars. Prices start from ${min_price}.",
                "Compare {count} {Service} options in {City}. Most popular: {top_provider} with {top_rating} rating.",
                "Discover trusted {Service} in {City}. {count} verified providers available with prices from ${min_price} to ${max_price}.",
                "{City} offers {count} {Service} providers. Average cost: ${avg_price} with typical response time of {response_time}.",
                "Looking for {Service} in {City}? Browse {count} options with ratings from {min_rating} to {max_rating} stars."
            ],
            "comparison": [
                "{item1} vs {item2}: Quick comparison shows {key_difference}. {item1} costs ${price1} while {item2} is ${price2}.",
                "Comparing {item1} and {item2}? Main difference: {item1} offers {feature1} while {item2} focuses on {feature2}.",
                "Choose between {item1} and {item2}. {winner} leads in {winning_category} with {winning_metric}.",
                "{item1} suits {use_case1} at ${price1}. {item2} better for {use_case2} at ${price2}. {recommendation}",
                "Quick answer: {item1} for {scenario1}, {item2} for {scenario2}. Price difference: ${price_diff}."
            ],
            "product_location": [
                "Shop {product} in {location} at {count} stores. Best price: ${best_price} at {best_store}.",
                "{count} {location} retailers sell {product}. Average price: ${avg_price}. In stock at {availability}% of locations.",
                "Find {product} near {location}. Top seller: {top_seller} with {sales_count} units sold this month.",
                "{product} available in {location} from ${min_price}. Most popular model: {popular_model} at {count} stores.",
                "Buy {product} in {location} today. {in_stock_count} stores have inventory starting at ${starting_price}."
            ],
            "educational": [
                "Learn {topic} in {location} with {count} options. Average course length: {avg_duration}. Cost from ${min_cost}.",
                "{count} {topic} programs in {location}. Top-rated: {top_program} with {rating} satisfaction score.",
                "Study {topic} in {location}. {online_count} online and {offline_count} in-person options available.",
                "{topic} training in {location} starts at ${starting_price}. Most programs complete in {typical_duration}.",
                "Master {topic} with {count} {location} providers. Beginner-friendly options from ${beginner_price}."
            ]
        }
        
        # Supporting content patterns
        self.support_patterns = {
            "location_context": [
                "{city} has {population} residents with median income of ${median_income}. The {industry} sector employs {employee_count} people locally.",
                "The {city} market for {service} has grown {growth_rate}% over the past year. {new_businesses} new providers entered the market in {year}.",
                "In {city}, demand for {service} peaks during {peak_season}. Average wait time: {wait_time} with {availability}% same-day availability.",
                "{city}'s {industry} market serves {service_area_size} square miles. Most providers cover {coverage_percent}% of the metro area.",
                "Local regulations in {city} require {service} providers to maintain ${insurance_amount} insurance and {license_type} licensing."
            ],
            "comparison_details": [
                "Key features comparison: {item1} includes {features1_count} features while {item2} offers {features2_count}. Overlap: {common_features} shared features.",
                "Performance metrics: {item1} scores {score1}/10 in {category1}. {item2} achieves {score2}/10 in {category2}. Overall winner depends on use case.",
                "User feedback shows {item1} preferred by {percent1}% for {reason1}. {item2} chosen by {percent2}% who need {reason2}.",
                "Integration options: {item1} connects with {integrations1} tools. {item2} supports {integrations2} platforms. Both integrate with {common_integrations}.",
                "Support comparison: {item1} offers {support1} support hours. {item2} provides {support2} response time. User satisfaction: {satisfaction1}% vs {satisfaction2}%."
            ],
            "value_proposition": [
                "Save {savings_percent}% compared to {alternative}. Average customer saves ${savings_amount} annually.",
                "Get started in {setup_time} with {complexity} setup process. No {requirement} required.",
                "Join {customer_count} satisfied customers. {retention_rate}% continue after {time_period}.",
                "Rated {rating}/5 based on {review_count} reviews. {recommend_percent}% would recommend to others.",
                "Free {free_feature} included. Premium features start at ${premium_price} per {billing_period}."
            ]
        }
        
        # CTA patterns
        self.cta_patterns = [
            "Compare all {count} options below.",
            "Get started with {recommended_option} today.",
            "View detailed comparison table.",
            "Check current availability and pricing.",
            "Browse all {category} options in {location}.",
            "See which {service} is right for you.",
            "Find your perfect match below."
        ]
    
    def select_pattern(self, pattern_type: str, category: str, data: Dict[str, Any]) -> str:
        """Select appropriate pattern based on data hash for consistency"""
        # Use data to deterministically select pattern
        data_str = json.dumps(sorted(data.items()))
        hash_val = int(hashlib.md5(data_str.encode()).hexdigest()[:8], 16)
        
        if pattern_type == "intro":
            patterns = self.intro_patterns.get(category, self.intro_patterns["location_service"])
        elif pattern_type == "support":
            patterns = self.support_patterns.get(category, self.support_patterns["location_context"])
        elif pattern_type == "cta":
            patterns = self.cta_patterns
        else:
            patterns = ["Default content for {keyword}."]
        
        # Select pattern based on hash
        pattern_index = hash_val % len(patterns)
        return patterns[pattern_index]
    
    def fill_pattern(self, pattern: str, data: Dict[str, Any]) -> str:
        """Fill pattern with data, using defaults for missing values"""
        # Extract all variables from pattern
        import re
        variables = re.findall(r'\{(\w+)\}', pattern)
        
        # Create a copy of data with all required variables
        safe_data = {}
        
        # First, copy all provided data
        for key, value in data.items():
            if value is not None and value != "":
                safe_data[key] = value
        
        # Then, fill in missing variables with defaults
        for var in variables:
            if var not in safe_data:
                safe_data[var] = self._get_default_value(var)
        
        # Fill the pattern
        try:
            return pattern.format(**safe_data)
        except KeyError as e:
            # This shouldn't happen now, but just in case
            missing_key = str(e).strip("'")
            safe_data[missing_key] = self._get_default_value(missing_key)
            return pattern.format(**safe_data)
    
    def fill_pattern_with_enriched_data(self, pattern: str, enriched_data: Dict[str, Any], 
                                       template_variables: Dict[str, Any]) -> str:
        """Fill pattern using enriched data with proper variable mapping"""
        
        # Transform enriched data to match pattern variables
        transformed_data = data_mapper.transform_data(enriched_data, template_variables)
        
        # Validate mapping
        missing_vars = data_mapper.validate_mapping(pattern, transformed_data)
        if missing_vars:
            # Fill missing variables with safe defaults
            for var in missing_vars:
                transformed_data[var] = self._get_default_value(var)
        
        # Fill the pattern
        try:
            return pattern.format(**transformed_data)
        except KeyError as e:
            # Fallback to safe fill
            return self.fill_pattern(pattern, transformed_data)
    
    def _get_default_value(self, key: str) -> Any:
        """Get sensible default value based on key name"""
        key_lower = key.lower()
        
        if any(word in key_lower for word in ["count", "number", "total"]):
            return random.randint(10, 200)
        elif any(word in key_lower for word in ["price", "cost", "fee"]):
            return random.randint(50, 500)
        elif any(word in key_lower for word in ["rating", "score", "stars"]):
            return round(random.uniform(3.5, 4.9), 1)
        elif any(word in key_lower for word in ["percent", "rate"]):
            return random.randint(60, 95)
        elif "location" in key_lower or "city" in key_lower or "area" in key_lower:
            return "your area"
        elif "service" in key_lower or "product" in key_lower:
            return "services"
        elif "time" in key_lower or "duration" in key_lower:
            return f"{random.randint(1, 30)} days"
        elif "name" in key_lower or "provider" in key_lower:
            return "top providers"
        else:
            return "quality options"
    
    def generate_list_content(self, items: List[Dict[str, Any]], list_type: str) -> str:
        """Generate formatted list content"""
        if not items:
            return "No items currently available."
        
        # Limit to top 10 items
        items = items[:10]
        
        if list_type == "providers":
            lines = []
            for item in items:
                name = item.get("name", "Provider")
                rating = item.get("rating", round(random.uniform(3.5, 4.9), 1))
                reviews = item.get("reviews", random.randint(10, 500))
                lines.append(f"• {name} - {rating}★ ({reviews} reviews)")
            return "\n".join(lines)
        
        elif list_type == "features":
            lines = []
            for item in items:
                feature = item.get("feature", item.get("name", "Feature"))
                description = item.get("description", "")
                if description:
                    lines.append(f"• {feature}: {description}")
                else:
                    lines.append(f"• {feature}")
            return "\n".join(lines)
        
        elif list_type == "locations":
            lines = []
            for item in items:
                location = item.get("location", item.get("name", "Location"))
                metric = item.get("metric", "")
                if metric:
                    lines.append(f"• {location} - {metric}")
                else:
                    lines.append(f"• {location}")
            return "\n".join(lines)
        
        else:
            # Generic list
            lines = []
            for item in items:
                if isinstance(item, dict):
                    text = item.get("name", item.get("title", str(item)))
                else:
                    text = str(item)
                lines.append(f"• {text}")
            return "\n".join(lines)
    
    def generate_comparison_table(self, item1: Dict[str, Any], item2: Dict[str, Any], 
                                 criteria: List[str] = None) -> str:
        """Generate simple comparison table"""
        if not criteria:
            # Use common comparison criteria
            criteria = ["Price", "Rating", "Features", "Support", "Ease of Use"]
        
        lines = [
            f"**{item1.get('name', 'Option 1')} vs {item2.get('name', 'Option 2')}**",
            ""
        ]
        
        for criterion in criteria[:5]:  # Limit to 5 criteria
            val1 = item1.get(criterion.lower(), self._get_comparison_value(criterion))
            val2 = item2.get(criterion.lower(), self._get_comparison_value(criterion))
            lines.append(f"**{criterion}**: {val1} vs {val2}")
        
        return "\n".join(lines)
    
    def _get_comparison_value(self, criterion: str) -> str:
        """Get random but reasonable comparison value"""
        criterion_lower = criterion.lower()
        
        if "price" in criterion_lower:
            return f"${random.randint(10, 200)}/mo"
        elif "rating" in criterion_lower:
            return f"{round(random.uniform(3.5, 4.9), 1)}/5"
        elif "support" in criterion_lower:
            return random.choice(["24/7", "Business hours", "Email only", "Phone & email"])
        elif "ease" in criterion_lower:
            return random.choice(["Very easy", "Easy", "Moderate", "Some learning curve"])
        elif "features" in criterion_lower:
            return f"{random.randint(10, 50)} features"
        else:
            return random.choice(["Good", "Very good", "Excellent", "Average"])


# Singleton instance
content_patterns = ContentPatterns()