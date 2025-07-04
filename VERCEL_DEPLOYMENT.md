# Vercel Deployment Guide

Your app is already configured for Vercel deployment! Here's what you need to do:

## 1. Environment Variables

Add these to your Vercel project settings (Settings → Environment Variables):

```bash
# Required (choose ONE):
PerplexityAPI=your-perplexity-api-key-here
# OR
OPENAI_API_KEY=your-openai-api-key-here  
# OR
ANTHROPIC_API_KEY=your-anthropic-api-key-here

# Optional (for enhanced features):
SERPAPI_KEY=your-serpapi-key  # For real keyword data
FIREBASE_PROJECT_ID=your-project-id  # For data persistence
```

## 2. Deploy Command

```bash
vercel
```

Or push to GitHub and connect to Vercel for automatic deployments.

## 3. What's Included

The Vercel deployment (`/api` folder) includes:

- ✅ **Perplexity API support** - Already configured!
- ✅ **Multiple interfaces**:
  - `/wizard` - New wizard interface (default)
  - `/pro` - Enhanced interface
  - `/app` - Basic interface
  - `/dashboard` - Usage dashboard
- ✅ **Full API endpoints**:
  - Business analysis
  - Keyword generation (with seed mode)
  - Content generation
  - Project management

## 4. Available Routes

After deployment, you'll have:

- `https://your-app.vercel.app/` → Wizard interface
- `https://your-app.vercel.app/wizard` → Wizard interface
- `https://your-app.vercel.app/pro` → Pro interface
- `https://your-app.vercel.app/dashboard` → Usage tracking
- `https://your-app.vercel.app/api` → API status
- `https://your-app.vercel.app/health` → Health check

## 5. Testing Your Deployment

Check if Perplexity is configured:
```bash
curl https://your-app.vercel.app/debug
```

This will show:
```json
{
  "env_vars": {
    "has_perplexity": true,
    ...
  }
}
```

## 6. Features with Perplexity

Perplexity is especially good for programmatic SEO because:
- It has web search built-in (great for current SEO trends)
- Lower cost than GPT-4
- Good at generating factual, search-optimized content
- The `sonar` model is designed for research tasks

## 7. No Additional Setup Needed!

Your `vercel.json` is already configured with:
- All route rewrites
- CORS headers
- API endpoints

Just deploy and go! 🚀