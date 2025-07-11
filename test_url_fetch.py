#!/usr/bin/env python3
"""Test URL content fetching"""

import sys
sys.path.append('backend')

from ai_client import AIClient

# Test URL
url = "https://starter-pack-app.vercel.app/"

client = AIClient()

# Test URL content fetching
print("Fetching content from:", url)
print("-" * 60)

content = client._fetch_url_content(url)

print("Content length:", len(content))
print("\nFirst 500 characters:")
print(content[:500])
print("\n" + "-" * 60)

# Now test the full analysis
print("\nTesting full analysis:")
result = client.analyze_business(url)

print("\nBusiness Name:", result.get('business_name'))
print("Description:", result.get('business_description'))
print("\nTemplate opportunities found:", len(result.get('template_opportunities', [])))