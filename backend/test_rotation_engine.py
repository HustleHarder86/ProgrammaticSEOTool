#!/usr/bin/env python3
"""Test script for the Prompt Rotation Engine"""

import time
from prompt_rotation_engine import get_rotation_engine
from content_variation_enhanced import ContentVariationEnhanced


def test_rotation_engine():
    """Test the prompt rotation engine functionality"""
    print("\n=== Testing Prompt Rotation Engine ===\n")
    
    rotation_engine = get_rotation_engine()
    
    # 1. Test rotation configuration
    print("1. Rotation Configuration:")
    config = rotation_engine.get_rotation_config()
    print("\nAvailable strategies:")
    for strategy, details in config["strategies"].items():
        print(f"  - {strategy}: {details['description']} (weight: {details['weight']})")
    
    print("\nVariation factors:")
    for factor, options in config["variation_factors"].items():
        print(f"  - {factor}: {', '.join(options)}")
    
    # 2. Test different rotation strategies
    print("\n2. Testing Rotation Strategies:")
    test_variations = ["variant_a", "variant_b", "variant_c", "variant_d"]
    
    for strategy in ["sequential", "least_used", "weighted_random"]:
        print(f"\n  Strategy: {strategy}")
        selections = []
        for i in range(6):
            selected, metadata = rotation_engine.select_prompt_variation(
                "test_prompt",
                test_variations,
                strategy=strategy
            )
            selections.append(selected)
            print(f"    Selection {i+1}: {selected} (usage: {metadata['usage_count']})")
        
        # Show distribution
        from collections import Counter
        distribution = Counter(selections)
        print(f"    Distribution: {dict(distribution)}")
    
    # 3. Test performance tracking
    print("\n3. Testing Performance Tracking:")
    
    # Simulate some performance data
    for i in range(10):
        variant = test_variations[i % len(test_variations)]
        success = i % 3 != 0  # 66% success rate except for first variant
        rotation_engine.record_performance(
            "test_prompt",
            variant,
            success,
            {"quality_score": 0.8 if success else 0.4}
        )
    
    # Test performance-based selection
    print("\n  Performance-based selection after tracking:")
    for i in range(4):
        selected, _ = rotation_engine.select_prompt_variation(
            "test_prompt",
            test_variations,
            strategy="performance_based"
        )
        print(f"    Selection {i+1}: {selected}")
    
    # 4. Test pattern detection
    print("\n4. Testing Pattern Detection:")
    
    test_content = """When it comes to real estate investing, timing is everything.
    Studies show that 75% of successful investors focus on market cycles.
    However, location remains the most critical factor.
    In conclusion, smart investors balance both timing and location."""
    
    patterns = rotation_engine.detect_content_patterns(test_content)
    print("\n  Detected patterns:")
    for pattern_type, pattern_list in patterns.items():
        if pattern_list:
            print(f"    {pattern_type}: {pattern_list}")
    
    # 5. Generate variation report
    print("\n5. Variation Report:")
    report = rotation_engine.get_variation_report()
    print(f"  Total variations used: {report['total_variations_used']}")
    print(f"  Total generations: {report['total_generations']}")
    print(f"  Pattern diversity: {report['pattern_diversity']:.2f}")
    
    if report["most_used"]:
        print("\n  Most used variations:")
        for key, count in report["most_used"][:3]:
            print(f"    {key}: {count} times")
    
    if report["best_performing"]:
        print("\n  Best performing:")
        for key, rate, total in report["best_performing"][:3]:
            print(f"    {key}: {rate:.2%} success rate ({total} uses)")
    
    print("\n=== Rotation Engine Test Complete ===\n")


def test_content_variation():
    """Test the enhanced content variation system"""
    print("\n=== Testing Content Variation System ===\n")
    
    variation_system = ContentVariationEnhanced()
    
    # Base content for testing
    base_content = """Is investing in real estate profitable in Miami?
    According to recent data, the average rental rate is $150 per night with 75% occupancy.
    Furthermore, the market has grown 15% year-over-year.
    However, initial investment costs remain high.
    In summary, real estate in Miami offers strong returns for patient investors."""
    
    print("1. Original Content:")
    print(base_content)
    print("\n" + "="*50 + "\n")
    
    # Generate variations
    print("2. Content Variations:")
    
    for i in range(3):
        print(f"\nVariation {i+1}:")
        varied_content, metadata = variation_system.create_varied_content(
            base_content,
            "evaluation_question",
            {"city": "Miami", "property_type": "condo"},
            variation_index=i,
            total_variations=10
        )
        
        print(varied_content)
        
        # Show what changed
        print("\n  Changes applied:")
        for change in metadata["variations_applied"]:
            if change.get("changed"):
                print(f"    - {change['type']}: ", end="")
                if "count" in change:
                    print(f"{change['count']} changes")
                elif "original" in change and "varied" in change:
                    print(f"'{change['original'][:30]}...' → '{change['varied'][:30]}...'")
                else:
                    print("modified")
    
    # 3. Show variation statistics
    print("\n3. Variation Statistics:")
    stats = variation_system.get_variation_stats()
    print(f"  Total patterns tracked: {stats['total_patterns_tracked']}")
    print(f"  Pattern types: {len(stats['pattern_types'])}")
    
    if stats["synonym_usage"]:
        print("\n  Synonym usage:")
        for word, count in list(stats["synonym_usage"].items())[:5]:
            print(f"    {word}: {count} replacements")
    
    print("\n=== Content Variation Test Complete ===\n")


if __name__ == "__main__":
    # Test rotation engine
    test_rotation_engine()
    
    # Test content variation
    test_content_variation()