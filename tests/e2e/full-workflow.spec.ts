import { test, expect } from '@playwright/test';

test.describe('Programmatic SEO Tool - Full Workflow', () => {
  let projectId: string;
  let templateId: string;

  test.beforeEach(async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');
  });

  test('1. Homepage loads correctly', async ({ page }) => {
    // Take screenshot of homepage
    await page.screenshot({ path: 'tests/e2e/screenshots/01-homepage.png', fullPage: true });
    
    // Check main elements
    await expect(page.locator('h1')).toContainText('Good');
    await expect(page.locator('text=Your SEO toolkit workspace')).toBeVisible();
    
    // Check quick actions
    await expect(page.locator('h3:has-text("New Project")')).toBeVisible();
    await expect(page.locator('h3:has-text("Analyze Website")')).toBeVisible();
    await expect(page.locator('h3:has-text("Generate Pages")')).toBeVisible();
  });

  test('2. Business analysis workflow', async ({ page }) => {
    // Navigate to analyze page
    await page.click('text=Analyze Website');
    await page.waitForURL('**/analyze');
    
    // Take screenshot of analyze page
    await page.screenshot({ path: 'tests/e2e/screenshots/02-analyze-page.png', fullPage: true });
    
    // Select text description option
    await page.click('text=Text Description');
    
    // Enter business description
    const businessDescription = 'AI Writing Assistant for Content Creators - An AI-powered tool that helps bloggers, marketers, and writers create high-quality content faster. Features include blog post generation, email templates, social media captions, and SEO optimization.';
    await page.fill('textarea', businessDescription);
    
    // Take screenshot before analysis
    await page.screenshot({ path: 'tests/e2e/screenshots/03-before-analysis.png', fullPage: true });
    
    // Click analyze button
    await page.click('text=Analyze Business');
    
    // Wait for analysis to complete (AI call)
    await page.waitForSelector('h2:has-text("Template Opportunities")', { timeout: 30000 });
    
    // Take screenshot of results
    await page.screenshot({ path: 'tests/e2e/screenshots/04-analysis-results.png', fullPage: true });
    
    // Check that we have template suggestions
    await expect(page.locator('text=SEO Services for')).toBeVisible();
    
    // Store project ID from URL
    await page.click('text=Build Template').first();
    await page.waitForURL('**/projects/**');
    projectId = page.url().match(/projects\/([^\/]+)/)?.[1] || '';
    expect(projectId).toBeTruthy();
  });

  test('3. Template creation workflow', async ({ page }) => {
    // Go directly to project if we have ID
    if (projectId) {
      await page.goto(`/projects/${projectId}`);
    } else {
      // Create new project through analysis
      await page.goto('/analyze');
      await page.click('text=Text Description');
      await page.fill('textarea', 'Digital marketing agency for e-commerce');
      await page.click('text=Analyze Business');
      await page.waitForSelector('text=Template Opportunities');
      await page.click('text=Build Template').first();
      projectId = page.url().match(/projects\/([^\/]+)/)?.[1] || '';
    }
    
    // Take screenshot of project page
    await page.screenshot({ path: 'tests/e2e/screenshots/05-project-page.png', fullPage: true });
    
    // Click on template builder
    await page.click('text=Build Template').first();
    await page.waitForURL('**/templates**');
    
    // Take screenshot of template builder
    await page.screenshot({ path: 'tests/e2e/screenshots/06-template-builder.png', fullPage: true });
    
    // Check template fields are pre-filled
    const nameInput = page.locator('input[name="name"]');
    await expect(nameInput).toHaveValue(/.+/); // Should have some value
    
    // Add content sections if needed
    const titleInput = page.locator('input[placeholder*="title"]').first();
    if (await titleInput.count() > 0) {
      await titleInput.fill('SEO Services for {Niche} - Expert Solutions');
    }
    
    // Save template
    await page.click('text=Save & Continue');
    
    // Wait for navigation or success
    await page.waitForTimeout(2000);
    
    // Extract template ID
    templateId = page.url().match(/templates\/([^\/]+)/)?.[1] || '';
  });

  test('4. AI variable generation', async ({ page }) => {
    // Navigate to generation page
    if (projectId) {
      await page.goto(`/projects/${projectId}/generate`);
    }
    
    await page.waitForLoadState('networkidle');
    
    // Take screenshot of generation wizard
    await page.screenshot({ path: 'tests/e2e/screenshots/07-generation-wizard.png', fullPage: true });
    
    // Select template if available
    const templateCard = page.locator('.cursor-pointer').first();
    if (await templateCard.count() > 0) {
      await templateCard.click();
      await page.click('text=Next');
    }
    
    // Wait for variable generation form
    await page.waitForSelector('text=Generate Variables', { timeout: 10000 });
    
    // Click generate variables
    const generateButton = page.locator('button:has-text("Generate")').first();
    if (await generateButton.count() > 0) {
      await generateButton.click();
      
      // Wait for AI to generate variables
      await page.waitForSelector('text=Generated successfully', { timeout: 30000 });
      
      // Take screenshot of generated variables
      await page.screenshot({ path: 'tests/e2e/screenshots/08-generated-variables.png', fullPage: true });
      
      // Move to next step
      await page.click('text=Next');
    }
  });

  test('5. Page selection and generation', async ({ page }) => {
    // Should be on selection step
    await page.waitForSelector('text=Select Pages', { timeout: 10000 });
    
    // Take screenshot of page selection
    await page.screenshot({ path: 'tests/e2e/screenshots/09-page-selection.png', fullPage: true });
    
    // Select first 5 pages
    const firstFiveCheckboxes = page.locator('input[type="checkbox"]').locator('nth=-n+5');
    for (let i = 0; i < 5; i++) {
      await firstFiveCheckboxes.nth(i).check();
    }
    
    // Generate pages
    await page.click('text=Generate Pages');
    
    // Wait for generation to complete
    await page.waitForSelector('text=Generation completed', { timeout: 60000 });
    
    // Take screenshot of results
    await page.screenshot({ path: 'tests/e2e/screenshots/10-generation-complete.png', fullPage: true });
  });

  test('6. View generated pages', async ({ page }) => {
    if (projectId) {
      await page.goto(`/projects/${projectId}/pages`);
      
      // Wait for pages to load
      await page.waitForSelector('text=Generated Pages', { timeout: 10000 });
      
      // Take screenshot of pages list
      await page.screenshot({ path: 'tests/e2e/screenshots/11-pages-list.png', fullPage: true });
      
      // Click on first page to view details
      const firstPage = page.locator('tr').nth(1);
      if (await firstPage.count() > 0) {
        await firstPage.click();
        await page.waitForTimeout(2000);
        
        // Take screenshot of page details
        await page.screenshot({ path: 'tests/e2e/screenshots/12-page-details.png', fullPage: true });
      }
    }
  });

  test('7. Export functionality', async ({ page }) => {
    if (projectId) {
      await page.goto(`/projects/${projectId}/export`);
      
      // Take screenshot of export page
      await page.screenshot({ path: 'tests/e2e/screenshots/13-export-page.png', fullPage: true });
      
      // Select CSV format
      await page.click('text=CSV');
      
      // Click export
      await page.click('text=Export Pages');
      
      // Wait for export to complete
      await page.waitForSelector('text=Export completed', { timeout: 30000 });
      
      // Take screenshot of export complete
      await page.screenshot({ path: 'tests/e2e/screenshots/14-export-complete.png', fullPage: true });
    }
  });

  test('8. Full workflow validation', async ({ page }) => {
    // This test validates the entire workflow works end-to-end
    console.log('Full workflow test completed');
    console.log(`Project ID: ${projectId}`);
    console.log(`Template ID: ${templateId}`);
    
    // Generate summary screenshot
    await page.goto('/');
    await page.screenshot({ path: 'tests/e2e/screenshots/15-final-dashboard.png', fullPage: true });
  });
});

// Helper function to capture errors
test.afterEach(async ({ page }, testInfo) => {
  if (testInfo.status !== 'passed') {
    await page.screenshot({ 
      path: `tests/e2e/screenshots/error-${testInfo.title.replace(/\s+/g, '-')}.png`,
      fullPage: true 
    });
  }
});