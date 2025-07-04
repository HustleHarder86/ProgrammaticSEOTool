# End-to-End Testing Guide

## Testing Your Website with the Programmatic SEO Tool

### Step 1: Deploy to Vercel
1. Make sure your Vercel environment variable is set:
   - `PerplexityAPI=your-perplexity-api-key`

2. Deploy the latest code:
   ```bash
   vercel --prod
   ```

### Step 2: Access the Wizard Interface
1. Go to your deployed URL: `https://your-app.vercel.app/`
2. You should see the wizard interface (Step 1: Analyze Business)

### Step 3: Analyze Your Business
1. Enter your website URL in the "Business Website" field
2. Add a description of your business (optional but helpful)
3. Select target audience (B2B, B2C, or Auto-detect)
4. Click "Analyze Business"

**What to expect:**
- Loading spinner saying "Analyzing your business with AI..."
- Success message with your business industry and target audience
- Market context section appears for customization

### Step 4: Generate Keywords (Step 2)
1. Click "Next" to proceed to keyword generation
2. You'll see AI-generated SEO strategies tailored to your business
3. Select the strategies you want (each shows estimated pages)
4. Click "Generate Keywords"

**What to expect:**
- Multiple strategy cards with estimated page counts
- Strategies specific to your business type
- Total estimated pages counter

### Step 5: Generate Content (Step 3)
1. Click "Next" to proceed to content generation
2. You'll see all generated keywords
3. Select keywords you want content for
4. Configure settings:
   - Articles to generate (default: 5)
   - Minimum word count (default: 1500)
   - Ensure uniqueness checkbox (should be checked)
5. Click "Generate Content"

**What to expect:**
- Content generation with unique elements
- Each article will have variations like:
  - Comparison tables
  - FAQ sections
  - Pros/cons lists
  - Custom data points

### Step 6: Export Results
1. After content generation, you can export in multiple formats:
   - CSV (for spreadsheet analysis)
   - JSON (for developers)
   - WordPress (for direct import)

## Troubleshooting

### If URL analysis fails:
- Check browser console (F12) for the cleaned URL being sent
- Make sure URL starts with https:// or http://
- Try without quotes or extra spaces

### If keywords don't generate:
- Check that Perplexity API key is set in Vercel
- Look at browser console for any API errors
- Try with a business description if URL fails

### If content is too similar:
- The Content Variation Agent should add unique elements
- Check that "Ensure uniqueness" is checked
- Each article should have different structures/elements

## What Makes Content Unique

With the Content Variation Agent, each piece of content will have:
1. **Unique titles** - Variations like "Complete Guide", "2024 Edition", etc.
2. **Different structures** - Some have FAQs, others have comparison tables
3. **Custom elements** - Statistics, checklists, pros/cons lists
4. **Fingerprint tracking** - Prevents duplicate content

## Success Metrics

A successful test will show:
- ✅ Business analyzed correctly with industry identified
- ✅ 50-500+ keywords generated based on strategies
- ✅ Unique content for each keyword
- ✅ Variation elements visible in content
- ✅ Export working properly

## Debug Mode

To see more details about what's happening:
1. Open browser developer console (F12)
2. Check the Network tab for API calls
3. Look for console.log messages about URL cleaning
4. Visit `/debug` endpoint to see environment status

Good luck with your testing! The tool should generate hundreds of unique, SEO-optimized pages for your website.