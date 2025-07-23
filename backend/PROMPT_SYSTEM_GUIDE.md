# Centralized Prompt Configuration System Guide

## Overview

The Programmatic SEO Tool now features a centralized prompt configuration system that makes all AI prompts visible, configurable, and manageable without code changes.

## Key Features

1. **Centralized Configuration**: All prompts in one JSON file
2. **Prompt Rotation**: Automatic variation to reduce content duplication
3. **Tone Control**: Multiple tone options for content variety
4. **Model Configuration**: Centralized AI model settings
5. **Validation System**: Built-in content quality checks
6. **Easy Updates**: Change prompts without touching code

## File Structure

```
backend/
├── config/
│   ├── prompts_config.json      # Main prompt configuration
│   └── prompt_manager.py        # Prompt management system
├── smart_page_generator_enhanced.py  # Example integration
└── test_prompt_system.py        # Test script
```

## Configuration File Structure

### prompts_config.json

```json
{
  "version": "1.0.0",
  "models": {
    "primary": {...},
    "business_analysis": {...}
  },
  "prompts": {
    "business_analysis": {
      "url_based": {
        "system": "You are an expert...",
        "user": "Analyze this website...",
        "variations": ["professional", "analytical"]
      }
    },
    "content_generation": {
      "evaluation_question": {...},
      "location_service": {...}
    }
  },
  "prompt_styles": {
    "tones": {
      "professional": {...},
      "conversational": {...}
    }
  }
}
```

## Usage Examples

### 1. Basic Prompt Retrieval

```python
from config.prompt_manager import get_prompt_manager

prompt_manager = get_prompt_manager()

# Get a business analysis prompt
prompt = prompt_manager.get_prompt(
    category="business_analysis",
    prompt_type="text_based",
    variables={
        "business_input": "SaaS analytics platform"
    }
)

print(prompt["system"])  # System prompt
print(prompt["user"])    # User prompt with variables substituted
```

### 2. Using Tone Variations

```python
# Get content with specific tone
prompt = prompt_manager.get_prompt(
    category="content_generation",
    prompt_type="evaluation_question",
    variables={
        "title": "Is investing in Bitcoin profitable?",
        "data_summary": "Current price: $45,000..."
    },
    tone="expert"  # Will add expert tone modifiers
)
```

### 3. Prompt Rotation

```python
# Enable rotation for variety
for i in range(5):
    prompt = prompt_manager.get_prompt(
        category="content_generation",
        prompt_type="generic",
        variables={"title": "Test"},
        use_rotation=True  # Rotates through variations
    )
    # Each iteration may use a different variation
```

### 4. Content Validation

```python
# Validate generated content
content = "Your generated content here..."
validation = prompt_manager.validate_content(content)

if not validation["passed"]:
    print(f"Issues: {validation['issues']}")
```

## Adding New Prompts

### Step 1: Edit prompts_config.json

Add your prompt under the appropriate category:

```json
"prompts": {
  "content_generation": {
    "new_prompt_type": {
      "system": "You are a specialized content creator...",
      "user": "Create content for {topic} including {requirements}...",
      "variations": ["detailed", "concise", "technical"],
      "temperature": 0.8
    }
  }
}
```

### Step 2: Use in Code

```python
prompt = prompt_manager.get_prompt(
    category="content_generation",
    prompt_type="new_prompt_type",
    variables={
        "topic": "Machine Learning",
        "requirements": "examples and code"
    }
)
```

## Migrating Existing Code

### Before (Hardcoded Prompts):

```python
prompt = f"""Write a 350-word answer to: {title}
Use this data: {data}
Be conversational."""
```

### After (Centralized Prompts):

```python
prompt_data = prompt_manager.get_prompt(
    category="content_generation",
    prompt_type="evaluation_question",
    variables={"title": title, "data_summary": data},
    tone="conversational"
)
```

## Available Prompt Categories

1. **business_analysis**
   - url_based
   - text_based

2. **variable_generation**
   - default

3. **content_generation**
   - evaluation_question
   - location_service
   - comparison
   - generic

4. **meta_generation**
   - meta_description
   - title_optimization

5. **enhancement_prompts**
   - statistics
   - faq
   - local_context

## Available Tones

- professional
- conversational
- expert
- local-friendly

## Testing

Run the test script to verify the system:

```bash
python backend/test_prompt_system.py
```

## Best Practices

1. **Version Control**: Update version number when making significant prompt changes
2. **Variable Naming**: Use consistent variable names across prompts
3. **Tone Consistency**: Ensure tone modifiers align with brand voice
4. **Testing**: Always test prompts after changes
5. **Documentation**: Document new prompts and their purpose

## Benefits

1. **Transparency**: All prompts visible in one place
2. **Flexibility**: Change prompts without code deployment
3. **Consistency**: Centralized tone and style management
4. **Quality**: Built-in validation ensures content standards
5. **Variety**: Rotation reduces duplicate content
6. **Maintainability**: Easier to update and manage prompts

## Next Steps

1. Review and customize prompts in `prompts_config.json`
2. Add business-specific prompts and tones
3. Integrate prompt manager into existing generators
4. Set up A/B testing for prompt variations
5. Monitor content quality metrics