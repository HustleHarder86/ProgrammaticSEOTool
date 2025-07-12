#!/usr/bin/env python3
"""Test template creation directly"""
import requests
import json

# Configuration
API_URL = "https://programmaticseotool-production.up.railway.app"
PROJECT_ID = "f61238d1-a058-4930-a54f-14201cba915a"  # From debug output

# Template data matching what the frontend sends
template_data = {
    "name": "Test Template",
    "pattern": "Real Estate Investment Analysis in {City}",
    "template_type": "programmatic_seo",
    "title_template": "Real Estate Investment Analysis in {City} | InvestiProp Analyzer",
    "meta_description_template": "Discover real estate investment analysis in {city} with InvestiProp Analyzer. Expert solutions and comprehensive guidance for your needs.",
    "h1_template": "Real Estate Investment Analysis in {City}",
    "content_sections": [
        {
            "heading": "Overview",
            "content": "Welcome to our comprehensive guide on real estate investment analysis in {city}. At InvestiProp Analyzer, we provide expert solutions tailored to your specific needs."
        },
        {
            "heading": "Our Expertise",
            "content": "Our team specializes in delivering high-quality real estate investment analysis in {city} services. With years of experience and proven results, we ensure exceptional outcomes for every client."
        },
        {
            "heading": "Why Choose Us",
            "content": "Choose InvestiProp Analyzer for reliable, professional service. We offer competitive pricing, expert knowledge, and personalized solutions that deliver real results."
        },
        {
            "heading": "Get Started",
            "content": "Ready to begin? Contact us today to discuss your specific requirements and discover how we can help you achieve your goals."
        }
    ]
}

# Make the request
print(f"Creating template for project {PROJECT_ID}...")
response = requests.post(
    f"{API_URL}/api/projects/{PROJECT_ID}/templates",
    json=template_data,
    headers={"Content-Type": "application/json"}
)

print(f"Status Code: {response.status_code}")
print(f"Response Headers: {dict(response.headers)}")

try:
    result = response.json()
    print(f"Response: {json.dumps(result, indent=2)}")
except:
    print(f"Response Text: {response.text}")

# Check templates again
print("\nChecking templates after creation...")
debug_response = requests.get(f"{API_URL}/debug/templates")
print(f"Debug Response: {json.dumps(debug_response.json(), indent=2)}")