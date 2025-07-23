import { test, expect } from '@playwright/test';
import * as fs from 'fs';
import * as path from 'path';

test.describe('Visual Validation & Feedback', () => {
  const screenshotDir = 'tests/e2e/screenshots/validation';
  
  test.beforeAll(async () => {
    // Create screenshot directory
    if (!fs.existsSync(screenshotDir)) {
      fs.mkdirSync(screenshotDir, { recursive: true });
    }
  });

  test('Visual regression test - Homepage', async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');
    
    // Capture full page screenshot
    await page.screenshot({ 
      path: `${screenshotDir}/homepage-full.png`,
      fullPage: true 
    });
    
    // Capture specific sections
    const sections = [
      { selector: 'section:has-text("Quick Actions")', name: 'quick-actions' },
      { selector: 'section:has-text("Recent Projects")', name: 'recent-projects' },
      { selector: 'section:has-text("Workflow")', name: 'workflow-guide' }
    ];
    
    for (const section of sections) {
      const element = page.locator(section.selector).first();
      if (await element.count() > 0) {
        await element.screenshot({ 
          path: `${screenshotDir}/homepage-${section.name}.png` 
        });
      }
    }
    
    // Check responsive design
    const viewports = [
      { width: 375, height: 667, name: 'mobile' },
      { width: 768, height: 1024, name: 'tablet' },
      { width: 1920, height: 1080, name: 'desktop' }
    ];
    
    for (const viewport of viewports) {
      await page.setViewportSize(viewport);
      await page.waitForTimeout(500);
      await page.screenshot({ 
        path: `${screenshotDir}/homepage-${viewport.name}.png`,
        fullPage: true 
      });
    }
  });

  test('Accessibility check', async ({ page }) => {
    await page.goto('/');
    
    // Check color contrast
    const buttons = await page.locator('button').all();
    const contrastIssues: string[] = [];
    
    for (const button of buttons) {
      const backgroundColor = await button.evaluate(el => 
        window.getComputedStyle(el).backgroundColor
      );
      const color = await button.evaluate(el => 
        window.getComputedStyle(el).color
      );
      
      // Simple contrast check (would use proper WCAG calculation in production)
      if (backgroundColor === color) {
        contrastIssues.push(await button.textContent() || 'Unknown button');
      }
    }
    
    // Check for alt text on images
    const images = await page.locator('img').all();
    const missingAlt: string[] = [];
    
    for (const img of images) {
      const alt = await img.getAttribute('alt');
      if (!alt) {
        const src = await img.getAttribute('src');
        missingAlt.push(src || 'Unknown image');
      }
    }
    
    // Generate accessibility report
    const report = {
      timestamp: new Date().toISOString(),
      contrastIssues,
      missingAltText: missingAlt,
      totalButtons: buttons.length,
      totalImages: images.length
    };
    
    fs.writeFileSync(
      `${screenshotDir}/accessibility-report.json`,
      JSON.stringify(report, null, 2)
    );
  });

  test('Performance metrics', async ({ page }) => {
    const metrics: any[] = [];
    
    // Measure page load times
    const pages = [
      { url: '/', name: 'Homepage' },
      { url: '/analyze', name: 'Analyze' },
      { url: '/projects', name: 'Projects' }
    ];
    
    for (const pageInfo of pages) {
      const startTime = Date.now();
      await page.goto(pageInfo.url);
      await page.waitForLoadState('networkidle');
      const loadTime = Date.now() - startTime;
      
      // Get performance metrics
      const performanceMetrics = await page.evaluate(() => {
        const navigation = performance.getEntriesByType('navigation')[0] as PerformanceNavigationTiming;
        return {
          domContentLoaded: navigation.domContentLoadedEventEnd - navigation.domContentLoadedEventStart,
          loadComplete: navigation.loadEventEnd - navigation.loadEventStart,
          firstContentfulPaint: performance.getEntriesByName('first-contentful-paint')[0]?.startTime || 0
        };
      });
      
      metrics.push({
        page: pageInfo.name,
        url: pageInfo.url,
        loadTime,
        ...performanceMetrics
      });
    }
    
    // Save performance report
    fs.writeFileSync(
      `${screenshotDir}/performance-report.json`,
      JSON.stringify(metrics, null, 2)
    );
  });

  test('UI consistency check', async ({ page }) => {
    await page.goto('/');
    
    // Check button styles consistency
    const buttonStyles = await page.evaluate(() => {
      const buttons = Array.from(document.querySelectorAll('button'));
      return buttons.map(btn => ({
        text: btn.textContent,
        backgroundColor: window.getComputedStyle(btn).backgroundColor,
        color: window.getComputedStyle(btn).color,
        borderRadius: window.getComputedStyle(btn).borderRadius,
        padding: window.getComputedStyle(btn).padding
      }));
    });
    
    // Check heading hierarchy
    const headings = await page.evaluate(() => {
      const h1s = document.querySelectorAll('h1').length;
      const h2s = document.querySelectorAll('h2').length;
      const h3s = document.querySelectorAll('h3').length;
      return { h1s, h2s, h3s };
    });
    
    // Generate UI consistency report
    const uiReport = {
      buttonStyles,
      headingHierarchy: headings,
      recommendations: []
    };
    
    // Add recommendations
    if (headings.h1s > 1) {
      uiReport.recommendations.push('Multiple H1 tags found - consider using only one per page');
    }
    
    fs.writeFileSync(
      `${screenshotDir}/ui-consistency-report.json`,
      JSON.stringify(uiReport, null, 2)
    );
  });

  test('Generate visual feedback summary', async ({ page }) => {
    // Read all reports
    const accessibilityReport = JSON.parse(
      fs.readFileSync(`${screenshotDir}/accessibility-report.json`, 'utf-8')
    );
    const performanceReport = JSON.parse(
      fs.readFileSync(`${screenshotDir}/performance-report.json`, 'utf-8')
    );
    const uiReport = JSON.parse(
      fs.readFileSync(`${screenshotDir}/ui-consistency-report.json`, 'utf-8')
    );
    
    // Generate comprehensive feedback
    const feedback = {
      summary: {
        timestamp: new Date().toISOString(),
        overallScore: calculateOverallScore(accessibilityReport, performanceReport, uiReport)
      },
      accessibility: {
        issues: accessibilityReport.contrastIssues.length + accessibilityReport.missingAltText.length,
        details: accessibilityReport
      },
      performance: {
        averageLoadTime: performanceReport.reduce((acc: number, p: any) => acc + p.loadTime, 0) / performanceReport.length,
        details: performanceReport
      },
      uiConsistency: {
        recommendations: uiReport.recommendations,
        details: uiReport
      },
      improvements: generateImprovements(accessibilityReport, performanceReport, uiReport)
    };
    
    // Save feedback
    fs.writeFileSync(
      `${screenshotDir}/visual-feedback-summary.json`,
      JSON.stringify(feedback, null, 2)
    );
    
    // Log summary to console
    console.log('\n=== Visual Validation Summary ===');
    console.log(`Overall Score: ${feedback.summary.overallScore}/100`);
    console.log(`Accessibility Issues: ${feedback.accessibility.issues}`);
    console.log(`Average Load Time: ${Math.round(feedback.performance.averageLoadTime)}ms`);
    console.log(`UI Recommendations: ${feedback.uiConsistency.recommendations.length}`);
    console.log('\nTop Improvements:');
    feedback.improvements.forEach((imp: string, i: number) => {
      console.log(`${i + 1}. ${imp}`);
    });
  });
});

function calculateOverallScore(accessibility: any, performance: any, ui: any): number {
  let score = 100;
  
  // Deduct for accessibility issues
  score -= (accessibility.contrastIssues.length * 5);
  score -= (accessibility.missingAltText.length * 3);
  
  // Deduct for slow performance
  const avgLoadTime = performance.reduce((acc: number, p: any) => acc + p.loadTime, 0) / performance.length;
  if (avgLoadTime > 3000) score -= 10;
  else if (avgLoadTime > 2000) score -= 5;
  
  // Deduct for UI issues
  score -= (ui.recommendations.length * 2);
  
  return Math.max(0, Math.min(100, score));
}

function generateImprovements(accessibility: any, performance: any, ui: any): string[] {
  const improvements = [];
  
  if (accessibility.missingAltText.length > 0) {
    improvements.push(`Add alt text to ${accessibility.missingAltText.length} images for better accessibility`);
  }
  
  if (accessibility.contrastIssues.length > 0) {
    improvements.push(`Fix color contrast issues on ${accessibility.contrastIssues.length} buttons`);
  }
  
  const slowPages = performance.filter((p: any) => p.loadTime > 2000);
  if (slowPages.length > 0) {
    improvements.push(`Optimize loading time for: ${slowPages.map((p: any) => p.page).join(', ')}`);
  }
  
  ui.recommendations.forEach((rec: string) => improvements.push(rec));
  
  return improvements.slice(0, 5); // Top 5 improvements
}