# Frontend Fix Instructions for Page Preview & Selection

## Issue
When clicking "Generate Pages" from a template detail page, the user is taken to a generate page that shows "No Templates Found" instead of the page preview/selection interface.

## Root Cause
1. The frontend is not properly passing the template context when navigating to the generate page
2. The generate page expects templates to be loaded but doesn't receive the specific template being generated from

## Required Fix

### Option 1: Quick Fix - Modify Navigation
The template detail page should navigate to generate page with the template ID:
```typescript
// Instead of:
router.push(`/projects/${projectId}/generate`);

// Use:
router.push(`/projects/${projectId}/generate?templateId=${templateId}`);
```

Then modify the generate page to accept and use the templateId query parameter.

### Option 2: Better Fix - Direct Integration
Since we now have the backend endpoints for potential pages, the frontend should:

1. When clicking "Generate Pages" from template detail:
   - Call POST `/api/projects/{projectId}/templates/{templateId}/generate-potential-pages`
   - This automatically generates variables AND creates potential pages
   - Navigate to a page selection view

2. Create a new page selection component that:
   - Calls GET `/api/projects/{projectId}/templates/{templateId}/potential-pages`
   - Shows all potential page titles with checkboxes
   - Allows selecting specific pages
   - Has "Select All", "Select First 10", etc. options
   - On submit, calls POST `/api/projects/{projectId}/templates/{templateId}/generate-selected-pages`

## Backend Endpoints Available

1. **Generate Variables (with auto potential pages creation)**
   ```
   POST /api/projects/{projectId}/templates/{templateId}/generate-variables
   Response includes: potential_pages_generated, potential_pages_url
   ```

2. **Get Potential Pages**
   ```
   GET /api/projects/{projectId}/templates/{templateId}/potential-pages
   Response: List of all potential pages with titles
   ```

3. **Generate Selected Pages**
   ```
   POST /api/projects/{projectId}/templates/{templateId}/generate-selected-pages
   Body: { page_ids: string[] }
   ```

## Recommended User Flow

1. Template Detail Page → Click "Generate Pages"
2. System automatically generates variables and potential pages (if not already done)
3. Show page selection interface with all potential titles
4. User selects which pages to generate
5. Generate selected pages with AI content
6. Show results

## Example Implementation

```typescript
// In template detail page
const handleGeneratePages = async () => {
  // First ensure variables are generated
  const varResponse = await apiClient.post(
    `/api/projects/${projectId}/templates/${templateId}/generate-variables`
  );
  
  // Navigate to selection page
  router.push(`/projects/${projectId}/templates/${templateId}/select-pages`);
};

// New select-pages route
const SelectPagesPage = () => {
  const [potentialPages, setPotentialPages] = useState([]);
  const [selectedIds, setSelectedIds] = useState([]);
  
  useEffect(() => {
    // Load potential pages
    apiClient.get(`/api/projects/${projectId}/templates/${templateId}/potential-pages`)
      .then(res => setPotentialPages(res.data.potential_pages));
  }, []);
  
  const handleGenerate = async () => {
    await apiClient.post(
      `/api/projects/${projectId}/templates/${templateId}/generate-selected-pages`,
      { page_ids: selectedIds }
    );
    router.push(`/projects/${projectId}/pages`);
  };
  
  return (
    <div>
      <h2>Select Pages to Generate</h2>
      {potentialPages.map(page => (
        <label key={page.id}>
          <input 
            type="checkbox" 
            checked={selectedIds.includes(page.id)}
            onChange={(e) => {
              if (e.target.checked) {
                setSelectedIds([...selectedIds, page.id]);
              } else {
                setSelectedIds(selectedIds.filter(id => id !== page.id));
              }
            }}
          />
          {page.title}
        </label>
      ))}
      <button onClick={handleGenerate}>
        Generate {selectedIds.length} Pages
      </button>
    </div>
  );
};
```

## Testing
After implementing:
1. Click "Generate Pages" from template detail
2. Verify potential pages are shown
3. Select some pages
4. Generate and verify content is created