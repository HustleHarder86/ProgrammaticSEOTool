"""Test keyword generation functionality."""
import asyncio
import json
from app.scanners.text_analyzer import TextBusinessAnalyzer
from app.researchers.keyword_researcher import KeywordResearcher
from app.researchers.strategy_generator import StrategyGenerator

async def test_keyword_generation():
    """Test the keyword generation pipeline."""
    
    # Test business description
    business_description = """
    We are a digital marketing agency specializing in SEO and content marketing. 
    We help small businesses improve their online visibility through strategic 
    content creation, keyword optimization, and link building. Our services include 
    technical SEO audits, content strategy, and local SEO optimization.
    """
    
    print("🚀 Testing Keyword Generation Pipeline\n")
    print("=" * 60)
    
    # Step 1: Analyze business
    print("\n1️⃣ Analyzing business description...")
    analyzer = TextBusinessAnalyzer()
    business_info = await analyzer.analyze(business_description)
    print(f"✅ Industry: {business_info.industry}")
    print(f"✅ Services: {', '.join(business_info.services[:5])}")
    
    # Step 2: Generate strategies
    print("\n2️⃣ Generating programmatic SEO strategies...")
    strategy_gen = StrategyGenerator()
    strategies = await strategy_gen.generate_strategies(business_info)
    print(f"✅ Generated {len(strategies)} strategies:")
    for i, strategy in enumerate(strategies[:5], 1):
        print(f"   {i}. {strategy.name} (~{strategy.estimated_pages} pages)")
    
    # Step 3: Generate keywords for first strategy
    print(f"\n3️⃣ Generating keywords for strategy: '{strategies[0].name}'...")
    keywords = await strategy_gen.generate_keywords_for_strategy(
        strategies[0], 
        business_info, 
        limit=20
    )
    print(f"✅ Generated {len(keywords)} keywords:")
    for i, kw in enumerate(keywords[:10], 1):
        print(f"   {i}. {kw}")
    
    # Step 4: Test traditional keyword expansion
    print("\n4️⃣ Testing traditional keyword expansion...")
    opportunities = await analyzer.identify_opportunities(business_info)
    researcher = KeywordResearcher()
    expanded = await researcher.expand_keywords(opportunities[:5], business_info)
    
    print(f"✅ Expanded to {len(expanded)} keywords with variations:")
    for i, kw in enumerate(expanded[:5], 1):
        print(f"   {i}. {kw['keyword']}")
        print(f"      - Type: {kw['content_type']}")
        print(f"      - Volume: {kw.get('search_volume', 'AI estimate')}")
        print(f"      - Difficulty: {kw.get('difficulty', 5)}/10")
        print(f"      - Data source: {kw.get('data_source', 'ai_estimate')}")
    
    # Step 5: Test keyword discovery (if seed keywords provided)
    print("\n5️⃣ Testing keyword discovery from seed keywords...")
    seed_keywords = ["SEO audit", "content marketing"]
    discovered = await researcher.discover_new_keywords(seed_keywords, limit=10)
    
    print(f"✅ Discovered {len(discovered)} related keywords:")
    for i, kw in enumerate(discovered[:5], 1):
        print(f"   {i}. {kw['keyword']}")
        print(f"      - Intent: {kw['search_intent']}")
        print(f"      - Priority: {kw['priority']}/10")
    
    print("\n" + "=" * 60)
    print("✅ Keyword generation test completed successfully!")
    print("\nNote: Using AI estimates for keyword metrics (no SEO API keys configured)")

if __name__ == "__main__":
    asyncio.run(test_keyword_generation())