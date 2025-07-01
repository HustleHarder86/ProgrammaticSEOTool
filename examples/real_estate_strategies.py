"""Example of keyword strategies for a Real Estate Investment SaaS"""

# These are examples of the types of strategies that would be generated
# for a real estate investment SaaS platform

REAL_ESTATE_STRATEGIES = [
    {
        "name": "City Real Estate Market Analysis",
        "template": "{city}-real-estate-market-analysis",
        "description": "In-depth market analysis pages for major cities, covering trends, prices, ROI, and investment opportunities",
        "estimated_pages": 500,
        "icon": "🏙️",
        "examples": [
            "austin-real-estate-market-analysis",
            "denver-real-estate-market-analysis",
            "miami-real-estate-market-analysis"
        ],
        "variables": ["city"],
        "priority": 9
    },
    {
        "name": "Property Type ROI Calculators",
        "template": "{property-type}-roi-calculator-{city}",
        "description": "Interactive ROI calculators for different property types in various cities",
        "estimated_pages": 1000,
        "icon": "📊",
        "examples": [
            "single-family-roi-calculator-austin",
            "multifamily-roi-calculator-denver",
            "commercial-roi-calculator-miami"
        ],
        "variables": ["property-type", "city"],
        "priority": 8
    },
    {
        "name": "Investment Strategy Guides",
        "template": "{strategy}-real-estate-investment-guide",
        "description": "Comprehensive guides for different real estate investment strategies",
        "estimated_pages": 50,
        "icon": "📚",
        "examples": [
            "fix-and-flip-real-estate-investment-guide",
            "buy-and-hold-real-estate-investment-guide",
            "airbnb-rental-real-estate-investment-guide"
        ],
        "variables": ["strategy"],
        "priority": 7
    },
    {
        "name": "City vs City Market Comparisons",
        "template": "{city1}-vs-{city2}-real-estate-market-comparison",
        "description": "Side-by-side comparisons of real estate markets in different cities",
        "estimated_pages": 2000,
        "icon": "⚖️",
        "examples": [
            "austin-vs-denver-real-estate-market-comparison",
            "miami-vs-orlando-real-estate-market-comparison",
            "seattle-vs-portland-real-estate-market-comparison"
        ],
        "variables": ["city1", "city2"],
        "priority": 7
    },
    {
        "name": "Neighborhood Investment Analysis",
        "template": "{neighborhood}-{city}-investment-analysis",
        "description": "Detailed investment analysis for specific neighborhoods within major cities",
        "estimated_pages": 5000,
        "icon": "🏘️",
        "examples": [
            "downtown-austin-investment-analysis",
            "south-beach-miami-investment-analysis",
            "capitol-hill-denver-investment-analysis"
        ],
        "variables": ["neighborhood", "city"],
        "priority": 8
    },
    {
        "name": "Property Management Cost Guides",
        "template": "property-management-costs-{city}",
        "description": "Comprehensive guides on property management costs and fees by city",
        "estimated_pages": 300,
        "icon": "💰",
        "examples": [
            "property-management-costs-austin",
            "property-management-costs-denver",
            "property-management-costs-miami"
        ],
        "variables": ["city"],
        "priority": 6
    },
    {
        "name": "Real Estate Tax Guides by State",
        "template": "{state}-real-estate-tax-guide",
        "description": "State-specific guides on real estate taxes, deductions, and investment implications",
        "estimated_pages": 50,
        "icon": "📋",
        "examples": [
            "texas-real-estate-tax-guide",
            "florida-real-estate-tax-guide",
            "california-real-estate-tax-guide"
        ],
        "variables": ["state"],
        "priority": 7
    },
    {
        "name": "Investment Property Financing Guides",
        "template": "{property-type}-financing-guide-{credit-score-range}",
        "description": "Financing guides for different property types based on credit score ranges",
        "estimated_pages": 100,
        "icon": "🏦",
        "examples": [
            "rental-property-financing-guide-excellent-credit",
            "commercial-property-financing-guide-good-credit",
            "fix-and-flip-financing-guide-fair-credit"
        ],
        "variables": ["property-type", "credit-score-range"],
        "priority": 8
    }
]

# Example keywords that would be generated for the "City Real Estate Market Analysis" strategy
EXAMPLE_KEYWORDS = [
    {
        "keyword": "Austin real estate market analysis 2024",
        "url_slug": "austin-real-estate-market-analysis",
        "title": "Austin Real Estate Market Analysis 2024: Trends, Prices & Investment Guide",
        "search_volume_estimate": "high",
        "competition": "medium",
        "intent": "informational"
    },
    {
        "keyword": "Denver housing market trends",
        "url_slug": "denver-real-estate-market-analysis",
        "title": "Denver Real Estate Market Analysis: Complete Investment Guide",
        "search_volume_estimate": "high",
        "competition": "medium",
        "intent": "informational"
    },
    {
        "keyword": "Miami real estate investment opportunities",
        "url_slug": "miami-real-estate-market-analysis",
        "title": "Miami Real Estate Market Analysis: Best Investment Opportunities",
        "search_volume_estimate": "medium",
        "competition": "high",
        "intent": "commercial"
    }
]