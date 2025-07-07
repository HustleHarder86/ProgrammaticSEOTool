# Page Generation Engine

## Overview
The page generation engine is responsible for creating bulk SEO-optimized pages by combining templates with data. It can efficiently handle the generation of 1000+ pages with unique content variations.

## Components

### 1. `page_generator.py`
Main engine that handles:
- Template variable extraction
- Dataset loading and mapping
- Combination generation
- Content population
- Batch processing for large-scale generation
- Quality enhancement with internal linking

### 2. `content_variation.py`
Content variation engine that ensures uniqueness:
- Multiple intro/conclusion variations
- Sentence structure variation
- Synonym replacement
- Contextual content addition
- Keyword density optimization
- Internal linking
- Quality metrics

### 3. API Endpoints (in `main.py`)

#### Preview Generation
```
POST /api/projects/{project_id}/templates/{template_id}/generate-preview
```
- Generates 5 sample pages to preview
- Shows total possible pages
- Uses sample data if no datasets available

#### Full Generation
```
POST /api/projects/{project_id}/templates/{template_id}/generate
```
- Generates all possible page combinations
- Processes in batches (default: 100)
- Stores pages in database
- Returns page IDs and count

#### Page Retrieval
```
GET /api/projects/{project_id}/pages
```
- List generated pages with pagination
- Optional template filter
- Returns page metadata

```
GET /api/projects/{project_id}/pages/{page_id}
```
- Get full page content
- Optional enhancement with internal linking
- Returns complete page data

#### Page Deletion
```
DELETE /api/projects/{project_id}/pages
```
- Delete all or template-specific pages
- Returns deletion count

## Features

### 1. Variable Extraction
- Automatically extracts variables from template patterns
- Example: `[City] [Service] Provider` → Variables: ["City", "Service"]

### 2. Data Combination
- Generates all possible combinations from datasets
- Example: 50 cities × 20 services = 1,000 pages

### 3. Content Uniqueness
- 8+ intro variations
- 5+ conclusion variations
- Synonym replacement
- Dynamic content sections (FAQ, statistics, case studies)
- Contextual additions (temporal, geographic, industry)

### 4. SEO Optimization
- Proper keyword density (1.5-3.5%)
- Internal linking between related pages
- Schema markup suggestions
- URL slug generation
- Meta title/description templates

### 5. Quality Assurance
- Minimum word count (800+)
- Required elements (headers, lists, paragraphs)
- Quality scoring system
- Readability checks

### 6. Scalability
- Batch processing for large datasets
- Efficient database operations
- Duplicate detection via content hashing
- Memory-efficient generation

## Usage Example

1. **Create Template**
```json
{
  "name": "Location Service Pages",
  "pattern": "[City] [Service] Provider",
  "title_template": "[City] [Service] | Professional Services",
  "meta_description_template": "Find the best [Service] in [City]. Expert solutions.",
  "content_sections": [
    {
      "heading": "Professional [Service] in [City]",
      "content": "Looking for [Service] in [City]? We deliver results."
    }
  ]
}
```

2. **Upload Data**
- CSV with columns: City, Service
- Or manual data entry

3. **Generate Preview**
- See 5 sample pages
- Check quality and formatting

4. **Generate All Pages**
- Creates all combinations
- Processes in batches
- Tracks progress

5. **Export or Publish**
- Use export endpoints for CSV/WordPress
- Or integrate with CMS

## Performance

- **Variable Extraction**: < 1ms per template
- **Combination Generation**: < 100ms for 10,000 combinations
- **Page Generation**: ~10-50ms per page
- **Batch Processing**: 100 pages/batch
- **Memory Usage**: Constant regardless of total pages

## Quality Metrics

Each generated page includes:
- Word count (target: 1200-2000)
- Keyword density percentage
- Quality score (0-100)
- Readability elements
- Internal link count
- Unique elements added

## Future Enhancements

1. **AI-powered content generation** for even more variation
2. **Image generation** for unique visuals
3. **Multi-language support**
4. **A/B testing variations**
5. **Real-time preview updates**
6. **Advanced internal linking strategies**