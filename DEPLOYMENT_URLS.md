# Deployment URLs

## Backend (Railway)
```
RAILWAY_BACKEND_URL=https://programmaticseotool-production.up.railway.app
```
*Note: Replace with your actual Railway URL after deployment*

## Frontend (Vercel)
```
VERCEL_FRONTEND_URL=https://programmatic-seo-tool.vercel.app
```

## Local Development
```
BACKEND_LOCAL=http://localhost:8000
FRONTEND_LOCAL=http://localhost:3000
```

## Environment Variable Configuration

### For Frontend (.env.local)
```
NEXT_PUBLIC_API_URL=https://programmaticseotool-production.up.railway.app
```

### For Backend (Railway Dashboard)
```
FRONTEND_URL=https://programmatic-seo-tool.vercel.app
PERPLEXITY_API_KEY=your_key_here
```

## Testing the Integration

1. Backend Health Check:
```bash
curl https://programmaticseotool-production.up.railway.app/health
```

2. Frontend API Connection:
- Open https://programmatic-seo-tool.vercel.app
- Check browser console for any CORS errors
- Try analyzing a business

## Update After Deployment

After Railway deployment, update this file with your actual backend URL!