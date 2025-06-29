"""Content templates for different types of SEO pages."""

TEMPLATES = {
    "comparison": {
        "name": "Product/Service Comparison",
        "structure": """
# {title}

## Quick Answer
{quick_answer}

## Overview
{overview}

## Detailed Comparison

### {option1}
{option1_description}

**Pros:**
{option1_pros}

**Cons:**
{option1_cons}

### {option2}
{option2_description}

**Pros:**
{option2_pros}

**Cons:**
{option2_cons}

## Feature Comparison Table
{comparison_table}

## Which Should You Choose?
{recommendation}

## Frequently Asked Questions
{faqs}

## Conclusion
{conclusion}
""",
        "variables": [
            "title", "quick_answer", "overview", "option1", "option1_description",
            "option1_pros", "option1_cons", "option2", "option2_description",
            "option2_pros", "option2_cons", "comparison_table", "recommendation",
            "faqs", "conclusion"
        ]
    },
    
    "how-to": {
        "name": "How-To Guide",
        "structure": """
# {title}

## What You'll Learn
{learning_objectives}

## Prerequisites
{prerequisites}

## Step-by-Step Guide

### Step 1: {step1_title}
{step1_content}

### Step 2: {step2_title}
{step2_content}

### Step 3: {step3_title}
{step3_content}

### Step 4: {step4_title}
{step4_content}

### Step 5: {step5_title}
{step5_content}

## Common Mistakes to Avoid
{common_mistakes}

## Pro Tips
{pro_tips}

## Frequently Asked Questions
{faqs}

## Conclusion
{conclusion}

## Next Steps
{next_steps}
""",
        "variables": [
            "title", "learning_objectives", "prerequisites", 
            "step1_title", "step1_content", "step2_title", "step2_content",
            "step3_title", "step3_content", "step4_title", "step4_content",
            "step5_title", "step5_content", "common_mistakes", "pro_tips",
            "faqs", "conclusion", "next_steps"
        ]
    },
    
    "best-x-for-y": {
        "name": "Best X for Y List",
        "structure": """
# {title}

## Our Top Pick
{top_pick_summary}

## Quick Comparison Table
{comparison_table}

## Detailed Reviews

### 1. {item1_name} - Best Overall
{item1_description}

**Best For:** {item1_best_for}
**Key Features:**
{item1_features}

**Pros:**
{item1_pros}

**Cons:**
{item1_cons}

### 2. {item2_name} - Best Value
{item2_description}

**Best For:** {item2_best_for}
**Key Features:**
{item2_features}

**Pros:**
{item2_pros}

**Cons:**
{item2_cons}

### 3. {item3_name} - Best for Beginners
{item3_description}

**Best For:** {item3_best_for}
**Key Features:**
{item3_features}

**Pros:**
{item3_pros}

**Cons:**
{item3_cons}

## How We Chose
{methodology}

## Buying Guide
{buying_guide}

## Frequently Asked Questions
{faqs}

## Final Thoughts
{conclusion}
""",
        "variables": [
            "title", "top_pick_summary", "comparison_table",
            "item1_name", "item1_description", "item1_best_for", "item1_features", "item1_pros", "item1_cons",
            "item2_name", "item2_description", "item2_best_for", "item2_features", "item2_pros", "item2_cons",
            "item3_name", "item3_description", "item3_best_for", "item3_features", "item3_pros", "item3_cons",
            "methodology", "buying_guide", "faqs", "conclusion"
        ]
    },
    
    "location-based": {
        "name": "Location-Based Service Page",
        "structure": """
# {title}

## Quick Facts
- **Service Area:** {service_area}
- **Average Cost:** {average_cost}
- **Response Time:** {response_time}
- **Availability:** {availability}

## About {service} in {location}
{overview}

## Our Services
{services_list}

## Why Choose {business_type} in {location}
{why_choose_us}

## Service Areas
{service_areas_detailed}

## Pricing
{pricing_information}

## What Our Customers Say
{testimonials}

## How It Works
{process}

## Frequently Asked Questions
{faqs}

## Contact Us
{contact_information}

## Emergency Services
{emergency_info}
""",
        "variables": [
            "title", "service_area", "average_cost", "response_time", "availability",
            "service", "location", "overview", "services_list", "business_type",
            "why_choose_us", "service_areas_detailed", "pricing_information",
            "testimonials", "process", "faqs", "contact_information", "emergency_info"
        ]
    },
    
    "ultimate-guide": {
        "name": "Ultimate Guide",
        "structure": """
# {title}

## Table of Contents
{table_of_contents}

## Introduction
{introduction}

## Chapter 1: Understanding {topic}
### What is {topic}?
{what_is}

### Why {topic} Matters
{why_matters}

### Key Concepts
{key_concepts}

## Chapter 2: Getting Started
### Prerequisites
{prerequisites}

### First Steps
{first_steps}

### Common Beginner Mistakes
{beginner_mistakes}

## Chapter 3: Advanced Strategies
### Pro Techniques
{pro_techniques}

### Case Studies
{case_studies}

### Industry Insights
{industry_insights}

## Chapter 4: Tools and Resources
### Essential Tools
{essential_tools}

### Recommended Resources
{resources}

### Templates and Checklists
{templates}

## Chapter 5: Future Trends
### What's Next for {topic}
{future_trends}

### Preparing for Change
{preparation}

## Frequently Asked Questions
{faqs}

## Conclusion
{conclusion}

## Additional Resources
{additional_resources}
""",
        "variables": [
            "title", "table_of_contents", "introduction", "topic", "what_is",
            "why_matters", "key_concepts", "prerequisites", "first_steps",
            "beginner_mistakes", "pro_techniques", "case_studies", "industry_insights",
            "essential_tools", "resources", "templates", "future_trends",
            "preparation", "faqs", "conclusion", "additional_resources"
        ]
    }
}

def get_template(template_type: str) -> dict:
    """Get a content template by type."""
    return TEMPLATES.get(template_type, TEMPLATES["how-to"])

def get_all_templates() -> dict:
    """Get all available templates."""
    return TEMPLATES