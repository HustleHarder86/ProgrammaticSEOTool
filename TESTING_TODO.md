# Testing TODO List

## High Priority - Core Functionality Testing

- [ ] **Test API connectivity** - verify frontend can reach backend
  - Run `python run_local.py` from project root
  - Visit http://localhost:3000/test-api
  - Confirm successful connection message

- [ ] **Test Business Analysis** - analyze a real business URL
  - Go to http://localhost:3000/projects/new
  - Enter a real business URL (e.g., https://www.canva.com)
  - Click analyze and verify AI suggestions appear

- [ ] **Test Template Creation** - create a template from AI suggestions
  - Select one of the AI-suggested templates
  - Customize the template if needed
  - Save the template successfully

- [ ] **Test Data Import** - upload a CSV with sample data
  - Navigate to data import section
  - Upload a CSV file with relevant data
  - Verify data is parsed and displayed correctly

- [ ] **Test Page Generation** - generate 10-20 pages from template + data
  - Click generate pages
  - Verify preview shows correctly
  - Generate full set of pages

- [ ] **Test Export** - export generated pages as CSV
  - Go to export section
  - Select CSV format
  - Download and verify exported file

## Medium Priority - Bug Fixes

- [ ] **Fix any API connection issues found during testing**
  - Document specific errors
  - Update API client configuration
  - Test fixes

- [ ] **Fix any UI/UX issues found during testing**
  - Note any broken layouts
  - Fix responsive issues
  - Improve error messages

- [ ] **Create sample CSV files for testing**
  - Cities/locations CSV
  - Services/products CSV
  - Combined data CSV

## Low Priority - Documentation

- [ ] **Document any bugs or issues discovered**
  - Create bug report with steps to reproduce
  - Note any workarounds found
  - Prioritize for future fixes

---

## Testing Notes

### Issue Log
1. **Business Analysis** - Returns 0 template suggestions (AI key may not be configured) ✅ FIXED
2. **Page Generation** - Full generation fails with 400 error
3. **Export** - Export status shows "failed" (likely due to no pages being generated)
4. **CRITICAL UX ISSUE** - Users have to manually create CSV files with the right column names. The tool should provide pre-built datasets or automatically generate relevant data based on the template!

### Success Log
✅ Both servers (frontend & backend) are running correctly
✅ API connectivity is working between frontend and backend
✅ Project creation works
✅ Template creation works (with {variable} format, not [variable])
✅ Data import works (expects list of dicts format)
✅ Page preview generation works (3 pages generated)

### Key Findings
- API field names: use `business_input` not `business_info`
- Template variables: use `{Product}` format not `[Product]`
- Data format: expects list of dictionaries, not dict of lists
- Generation endpoints: `/templates/{template_id}/generate` not `/generate`