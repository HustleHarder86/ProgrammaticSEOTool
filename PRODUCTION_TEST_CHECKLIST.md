# Production Testing Checklist

## 🧪 Full System Test After Deployment

### 1. Business Analysis Flow
- [ ] Go to https://programmatic-seo-tool.vercel.app
- [ ] Click "Get Started" or "Analyze Business"
- [ ] Enter business description: "Digital marketing agency specializing in SEO and PPC for e-commerce"
- [ ] Click "Analyze"
- [ ] Verify: Loading spinner appears
- [ ] Verify: Results show template opportunities
- [ ] Verify: Can click on a template

### 2. Project Creation
- [ ] From analysis results, select a template
- [ ] Verify: Redirected to project page
- [ ] Verify: Project details show correctly
- [ ] Verify: Template opportunities are listed

### 3. Template Builder
- [ ] Click "Build Template" on a template opportunity
- [ ] Verify: Template editor opens
- [ ] Enter template HTML with variables
- [ ] Preview the template
- [ ] Save the template

### 4. Data Import
- [ ] Navigate to Data Import
- [ ] Upload a CSV file with test data
- [ ] Verify: Data preview shows
- [ ] Verify: Columns are detected
- [ ] Save the dataset

### 5. Page Generation
- [ ] Go to Generate Pages
- [ ] Select template and dataset
- [ ] Configure generation settings
- [ ] Start generation
- [ ] Verify: Progress shows
- [ ] Verify: Pages are generated

### 6. Export
- [ ] Go to Export
- [ ] Select export format (CSV)
- [ ] Start export
- [ ] Verify: Export completes
- [ ] Download the file

## 🔍 Browser Console Checks

Open Developer Tools (F12) → Console:

- [ ] No CORS errors
- [ ] API calls show Railway URL: https://programmaticseotool-production.up.railway.app
- [ ] No 404 errors for API calls
- [ ] No JavaScript errors

## 📊 Network Tab Checks

Open Developer Tools (F12) → Network:

- [ ] API calls go to Railway backend
- [ ] Responses return 200 status codes
- [ ] Response times are reasonable (<3s)

## ✅ Success Criteria

1. **Frontend loads** without errors
2. **API integration works** - data flows between frontend and backend
3. **All features functional** - can complete full workflow
4. **No console errors** - clean browser console
5. **Good performance** - pages load quickly

## 🚨 If Issues Occur

1. **Check Vercel logs** for build/runtime errors
2. **Check Railway logs** for backend errors
3. **Verify environment variables** in both platforms
4. **Test API directly** with curl commands
5. **Check CORS configuration** if getting CORS errors