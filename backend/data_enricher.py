"""Data enrichment for programmatic SEO content generation"""
import json
import random
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime


class DataEnricher:
    """Manages and enriches data for content generation"""
    
    def __init__(self):
        # Define what data each template type needs
        self.template_data_requirements = {
            "evaluation_question": {
                "rental_property": [
                    "average_nightly_rate", "occupancy_rate", "total_listings",
                    "regulations", "roi_percentage", "peak_season", "average_monthly_revenue"
                ],
                "investment": [
                    "average_return", "risk_level", "market_growth", "entry_cost",
                    "competition_level", "success_rate"
                ]
            },
            "location_service": [
                "provider_count", "average_rating", "price_range", "top_providers",
                "average_response_time", "availability_percentage", "service_areas"
            ],
            "comparison": [
                "pricing", "features", "user_ratings", "pros", "cons",
                "best_for", "integrations", "support_options"
            ],
            "product_location": [
                "store_count", "price_range", "availability", "top_sellers",
                "average_price", "in_stock_percentage"
            ]
        }
        
        # Simulated market data (in production, this would come from APIs)
        self.market_data = {
            "rental_markets": {
                "winnipeg": {
                    "average_nightly_rate": 127,
                    "occupancy_rate": 68,
                    "total_listings": 342,
                    "growth_rate": 23,
                    "regulations": "STRs allowed with $250/year license",
                    "peak_season": "Summer (May-September)"
                },
                "toronto": {
                    "average_nightly_rate": 185,
                    "occupancy_rate": 72,
                    "total_listings": 1847,
                    "growth_rate": 15,
                    "regulations": "Principal residence only, 180-day limit",
                    "peak_season": "Summer and Fall"
                },
                "vancouver": {
                    "average_nightly_rate": 215,
                    "occupancy_rate": 65,
                    "total_listings": 892,
                    "growth_rate": -5,
                    "regulations": "Strict limits, business license required",
                    "peak_season": "Summer (June-August)"
                }
            },
            "property_performance": {
                "single-family home": {
                    "roi_average": 18,
                    "occupancy_bonus": 5,
                    "nightly_rate_multiplier": 1.2,
                    "typical_bedrooms": 3,
                    "monthly_expenses": 800
                },
                "condo": {
                    "roi_average": 15,
                    "occupancy_bonus": 0,
                    "nightly_rate_multiplier": 0.8,
                    "typical_bedrooms": 2,
                    "monthly_expenses": 600
                },
                "townhouse": {
                    "roi_average": 16,
                    "occupancy_bonus": 3,
                    "nightly_rate_multiplier": 1.0,
                    "typical_bedrooms": 2,
                    "monthly_expenses": 700
                }
            }
        }
    
    def get_template_data(self, template_type: str, variables: Dict[str, Any]) -> Dict[str, Any]:
        """Get enriched data for a specific template and variables"""
        
        # Extract key variables
        city = self._normalize_value(variables.get('city', variables.get('location', '')))
        property_type = self._normalize_value(variables.get('property_type', variables.get('property', '')))
        service = variables.get('service', '')
        
        # Determine content type
        if "rental" in template_type.lower() or property_type:
            return self._get_rental_property_data(city, property_type, variables)
        elif service:
            return self._get_service_data(city, service, variables)
        else:
            return self._get_generic_data(variables)
    
    def _normalize_value(self, value: str) -> str:
        """Normalize values for data lookup"""
        return value.lower().strip().replace('_', ' ')
    
    def _get_rental_property_data(self, city: str, property_type: str, 
                                  variables: Dict[str, Any]) -> Dict[str, Any]:
        """Get rental property specific data"""
        
        # Get base market data
        market = self.market_data["rental_markets"].get(city, self._get_default_market())
        property_data = self.market_data["property_performance"].get(
            property_type, 
            self.market_data["property_performance"]["single-family home"]
        )
        
        # Calculate specific metrics
        nightly_rate = int(market["average_nightly_rate"] * property_data["nightly_rate_multiplier"])
        occupancy = market["occupancy_rate"] + property_data["occupancy_bonus"]
        monthly_revenue = int((nightly_rate * 30 * occupancy / 100))
        monthly_profit = monthly_revenue - property_data["monthly_expenses"]
        roi = round((monthly_profit * 12) / (nightly_rate * 150) * 100, 1)  # Rough ROI calc
        
        return {
            "primary_data": {
                "city": city.title(),
                "property_type": property_type.title(),
                "average_nightly_rate": nightly_rate,
                "occupancy_rate": occupancy,
                "total_listings": market["total_listings"],
                "market_growth": market["growth_rate"],
                "regulations": market["regulations"],
                "peak_season": market["peak_season"],
                "monthly_revenue": monthly_revenue,
                "monthly_expenses": property_data["monthly_expenses"],
                "monthly_profit": monthly_profit,
                "roi_percentage": roi,
                "typical_bedrooms": property_data["typical_bedrooms"]
            },
            "enriched_data": {
                "market_strength": "strong" if market["growth_rate"] > 10 else "moderate",
                "regulation_status": "favorable" if "allowed" in market["regulations"].lower() else "restrictive",
                "profitability": "good" if roi > 15 else "moderate",
                "competition_level": "high" if market["total_listings"] > 1000 else "moderate"
            },
            "data_quality": 0.85,
            "data_sources": ["market_data", "property_analytics"]
        }
    
    def _get_service_data(self, city: str, service: str, 
                          variables: Dict[str, Any]) -> Dict[str, Any]:
        """Get service provider data"""
        
        # Generate realistic service data
        base_providers = random.randint(20, 200)
        
        return {
            "primary_data": {
                "city": city.title(),
                "service": service.title(),
                "provider_count": base_providers,
                "average_rating": round(random.uniform(4.0, 4.8), 1),
                "min_price": random.randint(50, 150),
                "max_price": random.randint(200, 500),
                "average_response_time": f"{random.randint(1, 4)} hours",
                "availability_percentage": random.randint(75, 95),
                "top_providers": [
                    {"name": f"Pro {service.title()} Services", "rating": 4.9, "reviews": random.randint(100, 500)},
                    {"name": f"{city.title()} {service.title()} Experts", "rating": 4.8, "reviews": random.randint(80, 400)},
                    {"name": f"Quick {service.title()}", "rating": 4.7, "reviews": random.randint(50, 300)}
                ]
            },
            "enriched_data": {
                "market_size": "large" if base_providers > 100 else "medium",
                "competition": "high" if base_providers > 150 else "moderate",
                "demand_level": "high" if variables.get('searches', 1000) > 500 else "moderate"
            },
            "data_quality": 0.75,
            "data_sources": ["provider_database", "review_aggregation"]
        }
    
    def _get_generic_data(self, variables: Dict[str, Any]) -> Dict[str, Any]:
        """Get generic data when specific type can't be determined"""
        return {
            "primary_data": variables,
            "enriched_data": {},
            "data_quality": 0.5,
            "data_sources": ["user_provided"]
        }
    
    def _get_default_market(self) -> Dict[str, Any]:
        """Get default market data when city not found"""
        return {
            "average_nightly_rate": 150,
            "occupancy_rate": 65,
            "total_listings": 200,
            "growth_rate": 10,
            "regulations": "Check local regulations",
            "peak_season": "Summer months"
        }
    
    def validate_data_completeness(self, template_type: str, data: Dict[str, Any]) -> Tuple[float, List[str]]:
        """Validate if we have enough data for quality content"""
        
        required_fields = self.template_data_requirements.get(template_type, [])
        if isinstance(required_fields, dict):
            # Handle nested requirements
            required_fields = required_fields.get(list(required_fields.keys())[0], [])
        
        present_fields = []
        missing_fields = []
        
        for field in required_fields:
            if field in data.get("primary_data", {}) and data["primary_data"][field]:
                present_fields.append(field)
            else:
                missing_fields.append(field)
        
        completeness = len(present_fields) / len(required_fields) if required_fields else 0.5
        
        return completeness, missing_fields