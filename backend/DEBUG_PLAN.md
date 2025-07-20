# Comprehensive Debug & Fix Plan for Programmatic SEO Tool

## Tool Purpose & Goals
The Programmatic SEO Tool is designed to:
1. **Analyze any business** and generate custom SEO strategies
2. **Create bulk pages** (100s-1000s) using templates + data
3. **Generate high-quality AI content** that provides real value
4. **Preview all potential pages** before generation
5. **Export pages** for publishing on websites

## Current Architecture
- **Frontend**: Next.js on Vercel (https://programmatic-seo-tool.vercel.app)
- **Backend**: FastAPI on Railway (https://programmaticseotool-production.up.railway.app)
- **Database**: SQLite (local) / PostgreSQL (production)
- **AI Providers**: Perplexity, OpenAI, Anthropic

## Systematic Debug Plan

### Phase 1: Identify Current Issues
1. Check production logs on Railway
2. Test frontend-backend connectivity
3. Verify environment variables on both platforms
4. Test each major workflow step

### Phase 2: End-to-End Testing Checklist

#### A. Business Analysis Flow
- [ ] Frontend form submission works
- [ ] API receives business input correctly
- [ ] AI analyzes business successfully
- [ ] Template suggestions returned
- [ ] Project saved to database

#### B. Template Creation Flow
- [ ] Create template from suggestion
- [ ] Variables extracted correctly
- [ ] Template preview works
- [ ] Template saved to database

#### C. Data Generation Flow
- [ ] AI generates variables automatically
- [ ] Manual data import works (CSV)
- [ ] Data validation passes
- [ ] Combinations calculated correctly

#### D. Page Preview & Selection Flow
- [ ] Generate potential pages button works
- [ ] All combinations displayed correctly
- [ ] Page titles show variables filled in
- [ ] Selection interface functional
- [ ] Batch size selection works

#### E. Page Generation Flow
- [ ] Selected pages generate with AI content
- [ ] Content quality meets standards (300+ words)
- [ ] Progress tracking works
- [ ] Generated pages saved to database
- [ ] Can view generated pages

#### F. Export Flow
- [ ] Export formats available (CSV, JSON, WordPress)
- [ ] Export process completes
- [ ] Download links work
- [ ] Exported content is correct

### Phase 3: Common Issues to Check

1. **CORS Configuration**
   - Verify Railway backend allows Vercel frontend
   - Check headers and origins

2. **Environment Variables**
   - NEXT_PUBLIC_API_URL on Vercel
   - AI API keys on Railway
   - Database connection strings

3. **API Endpoints**
   - All endpoints accessible from frontend
   - Proper error handling
   - Response formats match frontend expectations

4. **Database Issues**
   - Migrations applied in production
   - Tables exist and have correct schema
   - Relationships working properly

5. **AI Integration**
   - API keys valid and working
   - Rate limits not exceeded
   - Proper fallback handling

### Phase 4: Debug Tools

1. **Backend Health Check**
   ```bash
   curl https://programmaticseotool-production.up.railway.app/health
   ```

2. **Frontend API Test**
   ```javascript
   // Run in browser console on Vercel site
   fetch(`${process.env.NEXT_PUBLIC_API_URL}/health`)
     .then(r => r.json())
     .then(console.log)
   ```

3. **Database Check**
   ```python
   # Check all tables exist
   python check_database_schema.py
   ```

4. **AI Provider Test**
   ```python
   # Test each AI provider
   python test_ai_providers.py
   ```

### Phase 5: Fix Priority

1. **Critical (Blocking Usage)**
   - Frontend-backend connectivity
   - Business analysis failures
   - Page generation errors

2. **High (Major Features)**
   - Page preview not showing
   - AI content generation issues
   - Data import problems

3. **Medium (Quality)**
   - Export formatting
   - UI/UX improvements
   - Performance optimization

### Phase 6: Testing Protocol

After each fix:
1. Test locally first
2. Run comprehensive test suite
3. Deploy to staging (if available)
4. Test in production
5. Document the fix

### Phase 7: Success Criteria

The tool is working when:
- [ ] User can analyze a business
- [ ] Templates are generated with AI
- [ ] Data can be added (AI or manual)
- [ ] Page preview shows all combinations
- [ ] User can select and generate pages
- [ ] Content quality is high (300+ words, relevant)
- [ ] Pages can be exported
- [ ] No 500 errors in production
- [ ] Complete workflow takes < 5 minutes

## Next Steps
1. Start with Phase 1 to identify specific issues
2. Use test files to validate each component
3. Fix issues in priority order
4. Run full end-to-end test after each fix
5. Update documentation with findings