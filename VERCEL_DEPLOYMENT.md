# Vercel Frontend Deployment Guide

## 1. Environment Variables

Add this environment variable in Vercel Dashboard:

### Go to: Project Settings → Environment Variables

Add the following:

```
Name: NEXT_PUBLIC_API_URL
Value: https://programmaticseotool-production.up.railway.app
Environment: Production, Preview, Development
```

Click "Save"

## 2. Deploy to Vercel

The deployment will happen automatically when you push to GitHub, or you can:

1. Go to your Vercel dashboard
2. Click on your project
3. Click "Redeploy" → "Redeploy with existing Build Cache"

## 3. Verify Deployment

After deployment, test these features:

### 1. Home Page
- Visit: https://programmatic-seo-tool.vercel.app
- Should see the landing page without errors

### 2. Business Analysis
- Click "Analyze Business" 
- Enter: "Digital marketing agency specializing in SEO"
- Should return template opportunities

### 3. Check Browser Console
- Open Developer Tools (F12)
- Go to Console tab
- Should see no CORS errors
- API calls should go to Railway backend

## 4. Common Issues

### CORS Error
- Check Railway backend logs
- Verify CORS origins include your Vercel URL

### 500 Internal Server Error
- Check if PERPLEXITY_API_KEY is set in Railway
- Check Railway logs for specific error

### API Not Found (404)
- Verify NEXT_PUBLIC_API_URL is set correctly
- Should NOT have trailing slash

### Connection Refused
- Check if Railway backend is running
- Verify Railway URL is correct

## 5. Testing Checklist

- [ ] Home page loads
- [ ] Business analysis works
- [ ] No console errors
- [ ] API calls use Railway URL
- [ ] Templates display correctly
- [ ] Can navigate between pages

## 6. Success Indicators

✅ No build errors in Vercel
✅ Environment variable is set
✅ API calls show Railway URL in Network tab
✅ Business analysis returns results
✅ No CORS errors in console