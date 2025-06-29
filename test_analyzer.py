"""Test script for the business analyzer."""
import asyncio
import aiohttp
import json

async def test_text_analysis():
    """Test business analysis with text input."""
    url = "http://localhost:8000/api/analyze-business"
    
    # Example business description
    data = {
        "input_type": "text",
        "content": """
        We are a digital marketing agency in Austin, Texas specializing in SEO, 
        content marketing, and social media management for small to medium-sized businesses. 
        Our services include keyword research, on-page optimization, link building, 
        content creation, and social media strategy. We help local businesses improve 
        their online visibility and attract more customers through organic search.
        """
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data) as response:
            if response.status == 200:
                result = await response.json()
                print("=== Text Analysis Results ===")
                print(f"Business Info:")
                print(json.dumps(result['business_info'], indent=2))
                print(f"\nTop Content Opportunities:")
                for opp in result['opportunities'][:5]:
                    print(f"- {opp['keyword']} ({opp['content_type']}) - Priority: {opp['priority']}")
            else:
                print(f"Error: {response.status}")
                print(await response.text())

async def test_url_analysis():
    """Test business analysis with URL input."""
    url = "http://localhost:8000/api/analyze-business"
    
    # Example URL (you can change this to any business website)
    data = {
        "input_type": "url",
        "content": "https://www.example.com"
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data) as response:
            if response.status == 200:
                result = await response.json()
                print("\n=== URL Analysis Results ===")
                print(f"Business Info:")
                print(json.dumps(result['business_info'], indent=2))
                print(f"\nTop Content Opportunities:")
                for opp in result['opportunities'][:5]:
                    print(f"- {opp['keyword']} ({opp['content_type']}) - Priority: {opp['priority']}")
            else:
                print(f"Error: {response.status}")
                print(await response.text())

async def main():
    """Run tests."""
    print("Testing Business Analyzer...")
    print("Make sure the FastAPI server is running on http://localhost:8000\n")
    
    # Test text analysis
    await test_text_analysis()
    
    # Uncomment to test URL analysis
    # await test_url_analysis()

if __name__ == "__main__":
    asyncio.run(main())