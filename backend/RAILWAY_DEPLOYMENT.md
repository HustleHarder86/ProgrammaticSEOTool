# Railway Deployment Guide

## 1. Railway Project Setup

### In Railway Dashboard:
1. Create new project
2. Select "Deploy from GitHub repo"
3. Choose the `ProgrammaticSEOTool` repository
4. Set root directory to `/backend`

## 2. Environment Variables

Add these variables in Railway dashboard (Settings → Variables):

### Required (at least one):
```
PERPLEXITY_API_KEY=your_perplexity_api_key_here
# OR
OPENAI_API_KEY=your_openai_api_key_here
# OR
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

### Optional but Recommended:
```
FRONTEND_URL=https://programmatic-seo-tool.vercel.app
DATABASE_URL=sqlite:///./programmatic_seo.db
EXPORT_DIR=./exports
CACHE_DIR=./cache
```

### Automatically Provided by Railway:
- `PORT` - Railway provides this automatically
- `RAILWAY_ENVIRONMENT` - Set to "production"

## 3. Deployment

After setting environment variables:
1. Railway will auto-deploy from GitHub
2. Watch the build logs for any errors
3. Once deployed, get your backend URL from Railway dashboard

## 4. Test Endpoints

Test these endpoints with your Railway URL:

### Health Check
```bash
curl https://your-app.railway.app/health
```

Expected response:
```json
{
  "status": "healthy",
  "service": "programmatic-seo-backend",
  "database": "connected",
  "timestamp": "2025-01-07T..."
}
```

### Test API
```bash
curl https://your-app.railway.app/api/test
```

### Business Analysis (POST)
```bash
curl -X POST https://your-app.railway.app/api/analyze-business \
  -H "Content-Type: application/json" \
  -d '{"business_input": "Digital marketing agency", "input_type": "text"}'
```

## 5. Troubleshooting

### If deployment fails:
1. Check build logs in Railway
2. Verify all environment variables are set
3. Ensure `/backend` is set as root directory

### If API returns 500 errors:
1. Check Railway logs
2. Verify API keys are correct
3. Test database connection with /health endpoint

## 6. Database Persistence

For SQLite persistence on Railway:
1. Go to project settings
2. Add a persistent volume
3. Mount at `/app/data`
4. Update DATABASE_URL to `sqlite:///app/data/programmatic_seo.db`

## 7. Your Railway URL

Once deployed, document your Railway backend URL here:
```
RAILWAY_BACKEND_URL=https://programmaticseotool-production.up.railway.app
```

Use this URL in the frontend configuration.