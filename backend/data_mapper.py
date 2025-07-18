"""Data transformation layer for content generation"""
from typing import Dict, List, Any, Optional
import random


class DataMapper:
    """Maps DataEnricher output to ContentPatterns variables"""
    
    def __init__(self):
        # Define business logic mappings for derived variables
        self.business_logic_mappings = {
            "profitability": self._map_profitability,
            "performance": self._map_performance,
            "market_strength": self._map_market_strength,
            "ranking": self._map_ranking,
            "regulation_status": self._map_regulation_status,
            "monthly_revenue": self._calculate_monthly_revenue,
            "answer": self._generate_answer,
            "answer_intro": self._generate_answer_intro,
            "supporting_fact": self._generate_supporting_fact,
            "main_reason": self._generate_main_reason,
            "trend": self._generate_trend
        }
    
    def transform_data(self, enriched_data: Dict[str, Any], template_variables: Dict[str, Any]) -> Dict[str, Any]:
        """Transform enriched data to match template variables"""
        
        # Start with template variables (user-provided data like city, service)
        transformed = template_variables.copy()
        
        # Add direct mappings from enriched data
        if "primary_data" in enriched_data:
            primary_data = enriched_data["primary_data"]
            
            # Direct value mappings
            direct_mappings = {
                "average_nightly_rate": primary_data.get("average_nightly_rate"),
                "occupancy_rate": primary_data.get("occupancy_rate"),
                "total_listings": primary_data.get("total_listings"),
                "growth_rate": primary_data.get("growth_rate"),
                "regulations": primary_data.get("regulations"),
                "peak_season": primary_data.get("peak_season"),
                "roi_percentage": primary_data.get("roi_average"),
                "avg_rating": 4.5,  # Default good rating
                "min_price": primary_data.get("average_nightly_rate", 100) * 0.7 if primary_data.get("average_nightly_rate") else 70,
                "max_price": primary_data.get("average_nightly_rate", 100) * 1.3 if primary_data.get("average_nightly_rate") else 130,
                "avg_price": primary_data.get("average_nightly_rate", 100),
                "response_time": "2-4 hours",
                "count": primary_data.get("total_listings", 50),
                "top_provider": "Top Rated Pro",
                "top_rating": 4.8,
                "min_rating": 3.5,
                "max_rating": 5.0
            }
            
            # Add direct mappings (only if not None)
            for key, value in direct_mappings.items():
                if value is not None:
                    transformed[key] = value
        
        # Apply business logic mappings
        for var_name, mapping_func in self.business_logic_mappings.items():
            if var_name not in transformed:  # Don't override existing values
                try:
                    transformed[var_name] = mapping_func(enriched_data, template_variables)
                except Exception as e:
                    # Fallback to reasonable default
                    transformed[var_name] = self._get_safe_default(var_name)
        
        return transformed
    
    def _map_profitability(self, enriched_data: Dict[str, Any], template_vars: Dict[str, Any]) -> str:
        """Map ROI data to profitability description"""
        primary_data = enriched_data.get("primary_data", {})
        roi = primary_data.get("roi_average", 15)
        occupancy = primary_data.get("occupancy_rate", 65)
        
        if roi >= 18 and occupancy >= 70:
            return "highly profitable"
        elif roi >= 15 and occupancy >= 65:
            return "profitable"
        elif roi >= 12:
            return "moderately profitable"
        else:
            return "potentially profitable"
    
    def _map_performance(self, enriched_data: Dict[str, Any], template_vars: Dict[str, Any]) -> str:
        """Map data to performance description"""
        primary_data = enriched_data.get("primary_data", {})
        roi = primary_data.get("roi_average", 15)
        growth = primary_data.get("growth_rate", 10)
        
        if roi >= 18 and growth >= 15:
            return "strong"
        elif roi >= 15 and growth >= 10:
            return "good"
        elif roi >= 12:
            return "moderate"
        else:
            return "developing"
    
    def _map_market_strength(self, enriched_data: Dict[str, Any], template_vars: Dict[str, Any]) -> str:
        """Map market data to strength description"""
        primary_data = enriched_data.get("primary_data", {})
        listings = primary_data.get("total_listings", 100)
        growth = primary_data.get("growth_rate", 10)
        
        if listings >= 1000 and growth >= 15:
            return "strong"
        elif listings >= 500 and growth >= 10:
            return "steady"
        elif listings >= 200:
            return "emerging"
        else:
            return "developing"
    
    def _map_ranking(self, enriched_data: Dict[str, Any], template_vars: Dict[str, Any]) -> str:
        """Generate ranking based on performance metrics"""
        primary_data = enriched_data.get("primary_data", {})
        roi = primary_data.get("roi_average", 15)
        occupancy = primary_data.get("occupancy_rate", 65)
        
        combined_score = (roi / 20) + (occupancy / 100)
        
        if combined_score >= 1.5:
            return "in the top tier"
        elif combined_score >= 1.2:
            return "above average"
        elif combined_score >= 1.0:
            return "as competitive"
        else:
            return "as developing"
    
    def _map_regulation_status(self, enriched_data: Dict[str, Any], template_vars: Dict[str, Any]) -> str:
        """Map regulations to status description"""
        primary_data = enriched_data.get("primary_data", {})
        regulations = primary_data.get("regulations", "").lower()
        
        if "strict" in regulations or "prohibited" in regulations:
            return "with restrictive regulations"
        elif "license" in regulations or "permit" in regulations:
            return "with licensing requirements"
        elif "allowed" in regulations:
            return "with permissive regulations"
        else:
            return "with standard regulations"
    
    def _calculate_monthly_revenue(self, enriched_data: Dict[str, Any], template_vars: Dict[str, Any]) -> int:
        """Calculate estimated monthly revenue"""
        primary_data = enriched_data.get("primary_data", {})
        nightly_rate = primary_data.get("average_nightly_rate", 100)
        occupancy_rate = primary_data.get("occupancy_rate", 65)
        
        # Calculate: (nightly_rate * 30 days * occupancy_rate/100)
        monthly_revenue = int(nightly_rate * 30 * (occupancy_rate / 100))
        return monthly_revenue
    
    def _generate_answer(self, enriched_data: Dict[str, Any], template_vars: Dict[str, Any]) -> str:
        """Generate yes/no answer for evaluation questions"""
        primary_data = enriched_data.get("primary_data", {})
        roi = primary_data.get("roi_average", 15)
        occupancy = primary_data.get("occupancy_rate", 65)
        
        # Business logic for yes/no decisions
        if roi >= 15 and occupancy >= 60:
            return "Yes"
        elif roi >= 12 and occupancy >= 55:
            return "Yes, with proper management"
        else:
            return "It depends on your specific situation"
    
    def _generate_answer_intro(self, enriched_data: Dict[str, Any], template_vars: Dict[str, Any]) -> str:
        """Generate answer introduction"""
        answer = self._generate_answer(enriched_data, template_vars)
        if answer == "Yes":
            return "The data shows a positive outlook"
        elif "depends" in answer:
            return "Market conditions vary"
        else:
            return "Analysis indicates potential"
    
    def _generate_supporting_fact(self, enriched_data: Dict[str, Any], template_vars: Dict[str, Any]) -> str:
        """Generate supporting fact from data"""
        primary_data = enriched_data.get("primary_data", {})
        growth = primary_data.get("growth_rate", 10)
        listings = primary_data.get("total_listings", 100)
        
        if growth > 15:
            return f"the market has grown {growth}% year-over-year"
        elif listings > 500:
            return f"there are {listings} active listings"
        else:
            return "market fundamentals remain solid"
    
    def _generate_main_reason(self, enriched_data: Dict[str, Any], template_vars: Dict[str, Any]) -> str:
        """Generate main reason from strongest data point"""
        primary_data = enriched_data.get("primary_data", {})
        occupancy = primary_data.get("occupancy_rate", 65)
        roi = primary_data.get("roi_average", 15)
        
        if occupancy >= 70:
            return f"strong {occupancy}% occupancy rates"
        elif roi >= 18:
            return f"attractive {roi}% ROI potential"
        else:
            return "favorable market conditions"
    
    def _generate_trend(self, enriched_data: Dict[str, Any], template_vars: Dict[str, Any]) -> str:
        """Generate trend description"""
        primary_data = enriched_data.get("primary_data", {})
        growth = primary_data.get("growth_rate", 10)
        
        if growth >= 15:
            return "strong growth"
        elif growth >= 5:
            return "steady growth"
        elif growth >= 0:
            return "stable performance"
        else:
            return "market adjustment"
    
    def _get_safe_default(self, var_name: str) -> str:
        """Get safe default for unmapped variables"""
        var_lower = var_name.lower()
        
        if "count" in var_lower or "number" in var_lower:
            return str(random.randint(25, 150))
        elif "price" in var_lower or "cost" in var_lower:
            return str(random.randint(75, 200))
        elif "rating" in var_lower or "score" in var_lower:
            return str(round(random.uniform(4.0, 4.8), 1))
        elif "percent" in var_lower or "rate" in var_lower:
            return str(random.randint(65, 85))
        elif "city" in var_lower or "location" in var_lower:
            return "your city"
        elif "service" in var_lower or "product" in var_lower:
            return "available services"
        elif "provider" in var_lower or "company" in var_lower:
            return "top-rated providers"
        else:
            return "quality options"
    
    def validate_mapping(self, template_pattern: str, transformed_data: Dict[str, Any]) -> List[str]:
        """Validate that all template variables can be filled"""
        import re
        
        # Extract variables from template pattern
        variables = re.findall(r'\{([^}]+)\}', template_pattern)
        
        missing_vars = []
        for var in variables:
            if var not in transformed_data:
                missing_vars.append(var)
        
        return missing_vars


# Singleton instance
data_mapper = DataMapper()