# Prompt Rotation Engine Guide

## Overview

The Prompt Rotation Engine is a sophisticated system designed to maximize content variety and avoid duplication patterns in programmatic SEO content generation at scale.

## Key Features

### 1. Multiple Rotation Strategies

- **Sequential Rotation**: Cycles through variations in order
- **Weighted Random**: Prioritizes less-used variations
- **Least Used**: Always selects the least frequently used option
- **Performance Based**: Selects based on past success rates
- **Time Based**: Rotates based on time intervals

### 2. Pattern Detection & Avoidance

- Detects opening phrases, closing phrases, transitions
- Tracks sentence structure patterns
- Maintains history to avoid repetition
- Calculates diversity scores

### 3. Content Variation System

- Opening variations (questions, statements, data-driven)
- Transition word rotation
- Synonym replacement with controlled rates
- Sentence structure variations
- Closing variations (action, summary, question)

### 4. Performance Tracking

- Records success rates for each variation
- A/B testing capabilities
- Performance-based selection
- Detailed reporting

## Usage Examples

### Basic Rotation

```python
from prompt_rotation_engine import get_rotation_engine

rotation_engine = get_rotation_engine()

# Select from variations
variations = ["professional", "conversational", "expert", "friendly"]
selected, metadata = rotation_engine.select_prompt_variation(
    prompt_type="tone",
    available_variations=variations,
    strategy="weighted_random"  # or "sequential", "least_used", etc.
)

print(f"Selected: {selected}")
print(f"Usage count: {metadata['usage_count']}")
```

### Performance Tracking

```python
# Record performance after generation
rotation_engine.record_performance(
    prompt_type="content_generation",
    variation="professional",
    success=True,
    metadata={
        "quality_score": 0.85,
        "word_count": 350,
        "readability": 8.5
    }
)

# Performance-based selection will now favor high-performing variations
selected, _ = rotation_engine.select_prompt_variation(
    "content_generation",
    variations,
    strategy="performance_based"
)
```

### Content Variation

```python
from content_variation_enhanced import ContentVariationEnhanced

variation_system = ContentVariationEnhanced()

# Create varied content
base_content = "Your original content here..."

varied_content, metadata = variation_system.create_varied_content(
    base_content=base_content,
    content_type="evaluation_question",
    variables={"city": "Miami", "service": "plumbing"},
    variation_index=0,  # Current variation number
    total_variations=100  # Total being generated
)

print(varied_content)
print(f"Strategy used: {metadata['strategy']}")
```

## Rotation Strategies Explained

### 1. Sequential Rotation
```python
# Cycles through options in order: A, B, C, A, B, C...
strategy="sequential"
```
Best for: Even distribution, predictable variety

### 2. Weighted Random
```python
# Less-used options have higher selection probability
strategy="weighted_random"
```
Best for: Natural variety with good distribution

### 3. Least Used
```python
# Always picks the option used least frequently
strategy="least_used"
```
Best for: Maximum distribution, testing all options

### 4. Performance Based
```python
# Selects based on past success rates
strategy="performance_based"
```
Best for: Optimizing quality over time

### 5. Time Based
```python
# Rotates options based on time intervals
strategy="time_based"
```
Best for: Temporal variety, seasonal content

## Content Variation Strategies

### Variation by Scale

- **Light (1-10 pages)**: Minor variations only
- **Moderate (10-100 pages)**: Balanced variations
- **Heavy (100-1000 pages)**: Significant variations
- **Extreme (1000+ pages)**: Maximum variation

### Variation Elements

1. **Opening Variations**
   - Question openings
   - Statement openings
   - Data-driven openings

2. **Transition Variations**
   - Addition: Furthermore → Additionally → Moreover
   - Contrast: However → Nevertheless → On the other hand
   - Cause: Therefore → Consequently → As a result

3. **Synonym Variations**
   - Controlled replacement rate
   - Context-aware substitution
   - Case matching

4. **Structure Variations**
   - Sentence reordering
   - Clause rearrangement
   - Active/passive voice

5. **Closing Variations**
   - Action-oriented
   - Summary-based
   - Question endings

## Pattern Detection

### What's Tracked

```python
patterns = rotation_engine.detect_content_patterns(content)
# Returns:
{
    "opening_phrases": ["When it comes to..."],
    "closing_phrases": ["smart investors balance..."],
    "transition_words": ["however", "furthermore"],
    "sentence_structures": ["compound", "simple", "causal"]
}
```

### Diversity Scoring

```python
report = rotation_engine.get_variation_report()
print(f"Pattern diversity: {report['pattern_diversity']}")  # 0.0-1.0
```

## Best Practices

### 1. Strategy Selection

```python
# Let the engine auto-select based on context
strategy="auto"

# Or choose based on your needs:
# - Testing phase: use "least_used"
# - Production: use "performance_based" or "weighted_random"
# - Small scale: use "sequential"
```

### 2. Performance Tracking

```python
# Always record performance for optimization
try:
    content = generate_content()
    quality = assess_quality(content)
    rotation_engine.record_performance(
        prompt_type, variation, 
        success=quality > 0.7,
        metadata={"quality": quality}
    )
except Exception as e:
    rotation_engine.record_performance(
        prompt_type, variation, 
        success=False,
        metadata={"error": str(e)}
    )
```

### 3. Scaling Considerations

```python
# Adjust variation intensity based on scale
if total_pages < 100:
    strategy = "light"
elif total_pages < 1000:
    strategy = "moderate"
else:
    strategy = "heavy"
```

### 4. History Management

```python
# History is auto-saved every 10 uses
# Manual save if needed:
rotation_engine._save_history()

# Clear history to reset:
rotation_engine.history = rotation_engine._create_empty_history()
```

## Configuration

### Customizing Variation Templates

Edit `content_variation_enhanced.py` to add your own templates:

```python
self.variation_templates["openings"]["custom"] = [
    "Your custom opening {variable}",
    "Another variation {topic}"
]
```

### Adding Synonyms

```python
self.synonym_banks["analyze"] = [
    "examine", "investigate", "explore", "study", "evaluate"
]
```

## Monitoring & Reporting

### Get Usage Statistics

```python
report = rotation_engine.get_variation_report()

print(f"Total variations: {report['total_variations_used']}")
print(f"Total generations: {report['total_generations']}")
print(f"Pattern diversity: {report['pattern_diversity']}")

# Most used variations
for key, count in report["most_used"]:
    print(f"{key}: {count} times")

# Best performing
for key, rate, total in report["best_performing"]:
    print(f"{key}: {rate:.1%} success ({total} uses)")
```

### Content Variation Stats

```python
stats = variation_system.get_variation_stats()
print(f"Patterns tracked: {stats['total_patterns_tracked']}")
print(f"Synonym usage: {stats['synonym_usage']}")
```

## Testing

Run the test script:

```bash
python backend/test_rotation_engine.py
```

This will demonstrate:
- All rotation strategies
- Performance tracking
- Pattern detection
- Content variation
- Statistics and reporting

## Benefits

1. **Avoid Duplicate Content**: Ensures variety even at massive scale
2. **Optimize Performance**: Learn which variations work best
3. **Natural Variety**: Creates human-like content diversity
4. **Scale Confidently**: Generate thousands of unique pages
5. **Track Everything**: Full visibility into variation usage
6. **A/B Testing**: Built-in capability to test variations