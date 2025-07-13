# Universal Programmatic SEO Quality Plan - Any Business Type

## Core Principle: Adaptive Data-Driven Architecture

The tool must dynamically adjust its approach based on the business type, finding the right data sources and content structure for ANY industry.

## Universal Framework

### 1. Business Type Detection & Data Mapping

```python
UNIVERSAL_DATA_CATEGORIES = {
    "location_based": {
        "indicators": ["near me", "in {city}", "local", "{city} + service"],
        "data_needs": ["maps", "demographics", "local_competitors", "reviews"],
        "examples": ["plumbers", "restaurants", "real estate", "dentists"]
    },
    "comparison_based": {
        "indicators": ["vs", "alternatives", "best", "reviews"],
        "data_needs": ["features", "pricing", "reviews", "specs"],
        "examples": ["software", "products", "services", "tools"]
    },
    "informational": {
        "indicators": ["how to", "guide", "tutorial", "learn"],
        "data_needs": ["steps", "requirements", "outcomes", "examples"],
        "examples": ["courses", "tutorials", "consulting", "coaching"]
    },
    "transactional": {
        "indicators": ["buy", "price", "cost", "deals"],
        "data_needs": ["inventory", "pricing", "availability", "shipping"],
        "examples": ["ecommerce", "marketplaces", "bookings", "rentals"]
    },
    "service_based": {
        "indicators": ["hire", "service", "agency", "freelance"],
        "data_needs": ["portfolio", "rates", "availability", "expertise"],
        "examples": ["agencies", "freelancers", "contractors", "consultants"]
    }
}
```

### 2. Dynamic Data Source Discovery

```python
class UniversalDataSourceMapper:
    def map_business_to_data_sources(self, business_analysis):
        """Dynamically determine what data sources this business needs"""
        
        # Step 1: Categorize the business
        business_category = self.detect_category(business_analysis)
        
        # Step 2: Identify available data sources
        potential_sources = {
            "internal": self.find_internal_data(business_analysis),
            "public_apis": self.find_relevant_apis(business_category),
            "web_scraping": self.identify_scrapeable_data(),
            "user_generated": self.setup_ugc_collection(),
            "computed": self.define_calculatable_metrics()
        }
        
        # Step 3: Create data collection strategy
        return self.build_data_strategy(potential_sources)
```

### 3. Universal Template Components

```python
UNIVERSAL_COMPONENTS = {
    "data_table": {
        "use_when": "comparing multiple items",
        "data_required": ["headers", "rows", "sorting_keys"],
        "industries": "all"
    },
    "calculator": {
        "use_when": "user needs custom calculation",
        "data_required": ["formulas", "variables", "constraints"],
        "industries": ["finance", "real_estate", "ecommerce", "services"]
    },
    "map_widget": {
        "use_when": "location matters",
        "data_required": ["coordinates", "boundaries", "markers"],
        "industries": ["local_services", "real_estate", "travel", "retail"]
    },
    "comparison_chart": {
        "use_when": "showing alternatives",
        "data_required": ["options", "criteria", "scores"],
        "industries": ["software", "products", "services"]
    },
    "availability_checker": {
        "use_when": "booking/inventory",
        "data_required": ["calendar", "inventory", "pricing"],
        "industries": ["hotels", "rentals", "appointments", "courses"]
    },
    "review_aggregator": {
        "use_when": "social proof needed",
        "data_required": ["ratings", "reviews", "sources"],
        "industries": "all"
    },
    "process_timeline": {
        "use_when": "showing steps/duration",
        "data_required": ["stages", "durations", "requirements"],
        "industries": ["services", "education", "consulting"]
    },
    "pricing_matrix": {
        "use_when": "multiple pricing options",
        "data_required": ["tiers", "features", "prices"],
        "industries": ["saas", "services", "memberships"]
    }
}
```

### 4. Industry-Agnostic Quality System

```python
class UniversalQualityEngine:
    def __init__(self):
        self.quality_rules = {
            "must_have_unique_value": self.check_unique_value,
            "must_answer_user_intent": self.verify_user_intent,
            "must_have_fresh_data": self.check_data_freshness,
            "must_be_actionable": self.verify_actionability
        }
    
    def check_unique_value(self, page):
        """Every page must offer something unique"""
        unique_elements = 0
        
        # Check for unique data combinations
        if page.has_exclusive_data_view:
            unique_elements += 1
            
        # Check for unique tools/calculators
        if page.has_custom_tool:
            unique_elements += 1
            
        # Check for unique insights
        if page.has_computed_insights:
            unique_elements += 1
            
        return unique_elements >= 2
    
    def verify_user_intent(self, page):
        """Page must fulfill the search intent"""
        intent_signals = {
            "transactional": ["buy", "price", "order", "book"],
            "informational": ["how", "what", "why", "guide"],
            "navigational": ["login", "website", "contact"],
            "commercial": ["best", "top", "review", "compare"]
        }
        
        # Match content to intent
        return page.content_matches_intent(intent_signals)
```

### 5. Adaptive Content Generation Strategy

```python
class AdaptiveContentStrategy:
    def generate_page_structure(self, business_type, template, data):
        """Dynamically build page based on available data"""
        
        # Core structure that works for any business
        structure = {
            "hero": self.generate_hero_section(business_type, data),
            "key_data": self.select_primary_data_display(business_type, data),
            "interactive": self.choose_interactive_element(business_type),
            "supporting": self.add_supporting_sections(data),
            "trust": self.add_trust_elements(business_type),
            "action": self.create_cta_section(business_type)
        }
        
        # Remove sections without sufficient data
        return {k: v for k, v in structure.items() if v.has_minimum_data}
```

### 6. Universal Implementation Workflow

#### Phase 1: Smart Business Analysis
```python
def enhanced_business_analyzer(business_input):
    analysis = {
        "business_type": detect_business_category(business_input),
        "data_opportunities": find_available_data_sources(business_input),
        "content_patterns": identify_successful_patterns(industry),
        "unique_angles": discover_untapped_opportunities(business_input),
        "technical_requirements": list_needed_integrations(business_type)
    }
    
    # Key: Identify what makes THIS business's pages valuable
    analysis["value_proposition"] = determine_unique_value(business_input)
    
    return analysis
```

#### Phase 2: Dynamic Template Creation
```python
def create_adaptive_template(business_analysis):
    template = {
        "pattern": generate_optimal_pattern(business_analysis),
        "data_points": identify_required_data(business_analysis),
        "components": select_relevant_components(business_analysis),
        "quality_thresholds": set_minimum_standards(business_analysis)
    }
    
    # Template adjusts based on data availability
    template["fallback_strategy"] = define_graceful_degradation()
    
    return template
```

#### Phase 3: Data Collection Framework
```python
def build_data_pipeline(business_type):
    pipeline = DataPipeline()
    
    # Add relevant data sources
    if business_type.needs_location_data:
        pipeline.add_source(GooglePlacesAPI())
        pipeline.add_source(DemographicsAPI())
    
    if business_type.needs_pricing_data:
        pipeline.add_source(CompetitorPricingScraper())
        pipeline.add_source(MarketPricingAPI())
    
    if business_type.needs_reviews:
        pipeline.add_source(ReviewAggregator())
        pipeline.add_source(SocialProofCollector())
    
    # Always add these universal sources
    pipeline.add_source(WebScrapingEngine())
    pipeline.add_source(InternalDataConnector())
    
    return pipeline
```

### 7. Quality Assurance for Any Business

```python
UNIVERSAL_QUALITY_CHECKS = {
    "data_richness": {
        "minimum_data_points": 8,  # Flexible based on industry
        "data_freshness_days": 30,
        "unique_data_combinations": 3
    },
    "user_value": {
        "answers_search_intent": True,
        "provides_actionable_info": True,
        "better_than_competitors": True
    },
    "technical_quality": {
        "page_speed_score": 90,
        "mobile_friendly": True,
        "structured_data": True
    },
    "content_quality": {
        "minimum_words": 500,  # Lower if data-rich
        "unique_content_ratio": 0.7,
        "readability_score": 70
    }
}
```

### 8. Industry-Specific Adaptations

```python
INDUSTRY_ADAPTATIONS = {
    "ecommerce": {
        "focus": "product data",
        "key_components": ["price_comparison", "availability", "reviews"],
        "data_sources": ["product_feeds", "price_apis", "review_apis"],
        "unique_value": "price_history + availability_tracker"
    },
    "local_services": {
        "focus": "location + reviews",
        "key_components": ["map", "reviews", "booking"],
        "data_sources": ["google_places", "yelp", "booking_systems"],
        "unique_value": "real_availability + local_insights"
    },
    "saas": {
        "focus": "features + comparisons",
        "key_components": ["feature_matrix", "pricing_table", "alternatives"],
        "data_sources": ["g2_api", "capterra", "producthunt"],
        "unique_value": "detailed_comparisons + roi_calculator"
    },
    "education": {
        "focus": "outcomes + curriculum",
        "key_components": ["curriculum", "outcomes", "reviews"],
        "data_sources": ["course_catalogs", "job_outcomes", "reviews"],
        "unique_value": "career_paths + salary_data"
    },
    "travel": {
        "focus": "availability + experiences",
        "key_components": ["calendar", "map", "reviews", "weather"],
        "data_sources": ["booking_apis", "weather_api", "attraction_data"],
        "unique_value": "real_availability + local_insights"
    }
}
```

### 9. Implementation Phases

#### Phase 1: Universal Foundation (Week 1-2)
1. **Business Analyzer 2.0**
   - Auto-detect business category
   - Identify available data sources
   - Suggest optimal page patterns
   - Define quality thresholds

2. **Adaptive Template Engine**
   - Component library (works for any industry)
   - Dynamic layout based on data
   - Fallback strategies
   - Mobile-first design

#### Phase 2: Data Integration Layer (Week 3-4)
1. **Universal Data Connector**
   - Plugin system for APIs
   - Web scraping framework
   - CSV/Database imports
   - Real-time data updates

2. **Data Quality Manager**
   - Freshness monitoring
   - Completeness checking
   - Accuracy validation
   - Update scheduling

#### Phase 3: Quality & Scale (Week 5-6)
1. **Quality Gate System**
   - Industry-adjusted thresholds
   - Automated testing
   - Competitive analysis
   - User value scoring

2. **Scaling Engine**
   - Batch processing
   - Incremental updates
   - Performance optimization
   - Cost management

### 10. Success Metrics (Universal)

```python
UNIVERSAL_SUCCESS_METRICS = {
    "quality": {
        "pages_passing_quality_gate": "> 95%",
        "average_data_points_per_page": "> 15",
        "unique_value_score": "> 80%"
    },
    "performance": {
        "indexation_rate": "> 90%",
        "avg_time_on_page": "> 2 minutes",
        "bounce_rate": "< 40%",
        "tool_interaction_rate": "> 30%"
    },
    "business": {
        "organic_traffic_growth": "> 20% monthly",
        "conversion_rate": "above_industry_average",
        "pages_per_session": "> 2.5"
    }
}
```

## Examples Across Industries

### E-commerce Example:
**Pattern**: "Best [Product Category] under [$Price]"
**Data**: Real product listings, price history, reviews
**Unique Value**: Price tracker + availability alerts

### Local Service Example:
**Pattern**: "[Service] near [Location]"  
**Data**: Business listings, reviews, real-time availability
**Unique Value**: Book directly + see wait times

### SaaS Example:
**Pattern**: "[Software] vs [Alternative] Comparison"
**Data**: Feature matrices, pricing, user reviews
**Unique Value**: ROI calculator + migration guide

### Education Example:
**Pattern**: "[Subject] Courses in [Location/Online]"
**Data**: Course listings, outcomes, job placement
**Unique Value**: Career path analyzer + salary data

## Key Differentiator

This system doesn't create "content" - it creates **data-driven tools and resources** that happen to be good for SEO. Each page becomes a mini-application that provides real utility, ensuring it meets Google's quality guidelines regardless of industry.