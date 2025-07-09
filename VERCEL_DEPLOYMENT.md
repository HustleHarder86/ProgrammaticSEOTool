# Vercel Frontend Deployment Instructions

## Architecture Overview

This project uses a **separated architecture**:
- **Frontend**: Next.js on Vercel (this deployment)
- **Backend**: FastAPI on Railway (separate deployment)

The frontend communicates with the Railway backend via the `NEXT_PUBLIC_API_URL` environment variable.

## Fixed Issues

The project has been corrected to use the proper separated architecture:

### 1. Removed Unified Deployment Attempt
- Removed `/api` directory (no Python in Vercel)
- Reverted `vercel.json` to Next.js-only configuration
- Updated API client to use Railway backend URL

### 2. Configuration Changes
- Frontend uses `NEXT_PUBLIC_API_URL` environment variable
- API client properly configured with backend URL
- Fixed all TypeScript build errors

### 3. Environment Variables
- **Required**: `NEXT_PUBLIC_API_URL` - Railway backend URL
- Backend URL: `https://programmaticseotool-production.up.railway.app`

## Deployment Steps

1. **Set up Environment Variable**
   Create `.env.local` file:
   ```bash
   NEXT_PUBLIC_API_URL=https://programmaticseotool-production.up.railway.app
   ```

2. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Fix Vercel deployment - use separated architecture"
   git push
   ```

3. **Deploy to Vercel**
   ```bash
   vercel
   ```
   Or connect your GitHub repo in Vercel dashboard

4. **Set Environment Variables in Vercel Dashboard**
   - Go to your project settings in Vercel
   - Add `NEXT_PUBLIC_API_URL` with the Railway backend URL
   - This ensures the frontend can communicate with the backend

5. **Verify Deployment**
   - Check that the frontend loads at your Vercel URL
   - Test API connectivity on the `/test-api` page
   - Verify no CORS errors in browser console

## Key Configuration Files

1. **vercel.json** - Simple Next.js configuration:
   ```json
   {
     "framework": "nextjs"
   }
   ```

2. **API Client** (`lib/api/client.ts`):
   ```typescript
   const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
   ```

3. **.env.example** - Shows required environment variables

## Testing Locally

```bash
# Install dependencies
npm install

# Create .env.local with backend URL
echo "NEXT_PUBLIC_API_URL=https://programmaticseotool-production.up.railway.app" > .env.local

# Test build
npm run build

# Run locally
npm run dev
```

## Backend Information

The backend is deployed separately on Railway:
- URL: `https://programmaticseotool-production.up.railway.app`
- Repository: Same repo, `/backend` directory
- Has CORS configured to accept the Vercel frontend

## Troubleshooting

If deployment fails:
1. Ensure `NEXT_PUBLIC_API_URL` is set in Vercel environment variables
2. Check that the Railway backend is running
3. Verify no TypeScript errors with `npm run build`
4. Check browser console for CORS errors
5. Ensure the backend URL doesn't have a trailing slash

The frontend should now deploy successfully on Vercel!