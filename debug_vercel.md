# Debug Guide for Vercel Deployment

## Common Issues and Solutions

### 1. Check Your Environment Variable Name

The code expects the environment variable to be named exactly: `PerplexityAPI`

**In Vercel Dashboard:**
1. Go to your project settings
2. Navigate to Environment Variables
3. Make sure you have: `PerplexityAPI` (not `PERPLEXITY_API_KEY` or other variations)
4. The value should be your Perplexity API key

### 2. Debug the API

Visit these URLs to check status:

1. **Health Check**: `https://your-app.vercel.app/health`
   - Should show if AI provider is configured

2. **Debug Endpoint**: `https://your-app.vercel.app/debug`
   - Shows which environment variables are detected
   - Look for: `"has_perplexity": true`

### 3. Test Perplexity API Directly

You can test if your Perplexity API key works with this curl command:

```bash
curl https://api.perplexity.ai/chat/completions \
  -H "Authorization: Bearer YOUR_PERPLEXITY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama-3.1-sonar-small-128k-online",
    "messages": [{"role": "user", "content": "Hello"}]
  }'
```

### 4. Common Error Messages

**"Error: undefined"**
- Usually means the API call failed
- Check browser console (F12) for more details
- Look at Network tab for the actual API response

**"No AI provider configured"**
- Environment variable not set correctly
- Variable name mismatch

### 5. Quick Fix Steps

1. **Update Environment Variable**:
   - In Vercel: Settings → Environment Variables
   - Add: `PerplexityAPI` = `your-api-key-here`
   - Redeploy: Click "Redeploy" with existing build

2. **Alternative: Use OpenAI**:
   - If you have an OpenAI key instead
   - Add: `OPENAI_API_KEY` = `your-openai-key`
   - The system will use OpenAI as fallback

3. **Check API Key Format**:
   - Perplexity API keys usually start with `pplx-`
   - Make sure there are no extra spaces or quotes

### 6. Browser Console Commands

Open browser console (F12) and run:

```javascript
// Check if API is responding
fetch('/debug').then(r => r.json()).then(console.log)

// Test analyze endpoint directly
fetch('/api/analyze-business', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    business_url: 'https://example.com',
    business_description: 'Test business'
  })
}).then(r => r.json()).then(console.log)
```

This will show you the exact error from the API.