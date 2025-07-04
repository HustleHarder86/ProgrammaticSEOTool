# Subagent Implementation Plan

## Overview
Based on the codebase analysis, we have identified several subagents that need to be implemented to complete the Programmatic SEO Tool architecture. This plan outlines the implementation approach for each agent, prioritized by business value.

## Existing Components (Already Implemented)
- ✅ Business Analysis Agent (TextBusinessAnalyzer, URLBusinessScanner)
- ✅ Strategy Generation Agent (StrategyGenerator)
- ✅ Keyword Research Agent (KeywordResearcher)
- ✅ Content Generation Agent (ContentGenerator)
- ✅ Export Agent (CSVExporter, WordPressExporter)

## Implementation Plan

### Phase 1: High Priority - Core Infrastructure

#### 1. Database Integration Agent
- [x] Create `app/agents/database_agent.py`
- [x] Implement SQLAlchemy session management
- [x] Add CRUD operations for projects, keywords, and content
- [x] Create migration scripts for database initialization
- [x] Add database connection to FastAPI dependency injection
- [x] Update endpoints to persist data

#### 2. SEO Data Agent
- [x] Create `app/agents/seo_data_agent.py`
- [x] Add SerpAPI integration for real keyword data
- [x] Add Ubersuggest API integration (if API key available)
- [x] Implement caching mechanism to reduce API costs
- [x] Create fallback to AI estimates when APIs unavailable
- [x] Update KeywordResearcher to use real data

#### 3. Content Variation Agent
- [x] Create `app/agents/content_variation_agent.py`
- [x] Implement content fingerprinting algorithm
- [x] Add variation detection and scoring
- [x] Create content uniqueness validator
- [x] Integrate with ContentGenerator
- [x] Add variation parameters to content generation

### Phase 2: Medium Priority - Automation Features

#### 4. Project Management Agent
- [ ] Create `app/agents/project_management_agent.py`
- [ ] Design project state machine (draft → in_progress → completed)
- [ ] Implement project workflow coordination
- [ ] Add progress tracking and reporting
- [ ] Create project dashboard endpoints
- [ ] Update UI to show project status

#### 5. Publishing Queue Agent
- [ ] Create `app/agents/publishing_queue_agent.py`
- [ ] Design queue data structure
- [ ] Implement scheduling algorithm
- [ ] Add batch publishing support
- [ ] Create publishing status tracking
- [ ] Add API endpoints for queue management

#### 6. WordPress Publishing Agent
- [ ] Create `app/agents/wordpress_agent.py`
- [ ] Implement WordPress REST API client
- [ ] Add authentication handling
- [ ] Create post creation and update methods
- [ ] Handle categories, tags, and metadata
- [ ] Add error handling and retry logic

### Phase 3: Lower Priority - Monitoring & Optimization

#### 7. Analytics Agent
- [ ] Create `app/agents/analytics_agent.py`
- [ ] Design metrics schema
- [ ] Implement performance tracking
- [ ] Add ranking monitoring (if API available)
- [ ] Create analytics dashboard endpoints
- [ ] Generate ROI reports

#### 8. Rate Limiting Agent
- [ ] Create `app/agents/rate_limiting_agent.py`
- [ ] Implement token bucket algorithm
- [ ] Add API-specific rate limits
- [ ] Create request queue with priorities
- [ ] Add backoff strategies
- [ ] Integrate with all external API calls

#### 9. Logging Agent
- [ ] Create `app/agents/logging_agent.py`
- [ ] Set up structured logging
- [ ] Add log aggregation
- [ ] Implement error tracking
- [ ] Create audit trails
- [ ] Add monitoring dashboards

## Next Steps
1. Review this plan and get user approval
2. Start with Phase 1 implementation
3. Test each agent thoroughly before moving to the next
4. Update documentation as we go
5. Keep changes simple and modular

## Current Testing Plan

### Immediate Tasks:
1. Fix URL input issue in wizard interface
2. Complete Content Variation Agent (last high-priority agent)
3. Run end-to-end test of the full user flow
4. Verify Perplexity API works at each step

### Testing Flow:
1. **Input Business URL** → Fix the URL parsing issue
2. **Generate Keywords** → Test with Perplexity API
3. **Generate Content** → Ensure unique variations
4. **Export Results** → Verify CSV/JSON export

## Review Section

### Phase 1 - Database Integration Agent (Completed)

**High-level Summary of Changes:**
1. Created `app/agents/database_agent.py` with full CRUD operations for projects, keywords, and content
2. Added 5 new database-backed API endpoints to `app/main.py`:
   - `POST /api/projects` - Create new SEO projects
   - `GET /api/projects` - List all projects
   - `GET /api/projects/{id}` - Get project details with statistics
   - `POST /api/projects/{id}/keywords` - Add keywords to a project
   - `POST /api/projects/{id}/generate-content` - Generate and save content for keywords
3. Database models were already defined in `app/models.py` but weren't being used
4. Integration is complete and ready for testing

**Key Features Added:**
- Full project lifecycle management
- Keyword tracking with status updates
- Content storage with variation support
- Statistics and progress tracking

### Phase 1 - SEO Data Agent (Completed)

**High-level Summary of Changes:**
1. Created `app/agents/seo_data_agent.py` with real keyword research API integration
2. Integrated SerpAPI for real search data (when API key is available)
3. Added caching mechanism to reduce API costs (7-day cache)
4. Implemented fallback to AI estimates when no API keys are configured
5. Enhanced KeywordResearcher to use real SEO data including:
   - Search volume
   - Keyword difficulty
   - CPC and competition data
   - Related searches
6. Added new keyword discovery methods with priority scoring
7. Added new API endpoint: `POST /api/discover-keywords`

**Key Features Added:**
- Real-time keyword data from SerpAPI
- Smart caching to minimize API costs
- Keyword discovery from seed keywords
- Priority scoring based on volume, difficulty, and CPC
- Search intent detection
- Content type classification

### Phase 1 - Content Variation Agent (Completed)

**High-level Summary of Changes:**
1. Created `app/agents/content_variation_agent.py` with comprehensive uniqueness features
2. Implemented content fingerprinting to detect duplicate content
3. Added unique element injection (tables, FAQs, pros/cons, etc.)
4. Created title variation system to ensure unique titles
5. Integrated with ContentGenerator for automatic variation
6. Added uniqueness scoring for quality assurance

**Key Features Added:**
- Content fingerprinting with normalization
- Automatic unique element insertion
- Title variation generation
- Comparison tables, FAQs, checklists
- Uniqueness score calculation

**Current Status:**
- All Phase 1 agents completed!
- Ready for end-to-end testing