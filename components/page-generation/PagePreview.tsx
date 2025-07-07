'use client';

import { useState, useEffect, useCallback } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { 
  Eye, 
  Code, 
  Globe, 
  Search,
  ChevronLeft,
  ChevronRight,
  RefreshCw,
  ExternalLink
} from 'lucide-react';
import { Template, Dataset } from '@/types';

interface PagePreviewProps {
  template: Template;
  dataset: Dataset;
  settings: {
    max_pages?: number;
    include_variations?: boolean;
    uniqueness_threshold?: number;
    output_format?: 'html' | 'markdown';
  };
}

interface PreviewPage {
  title: string;
  slug: string;
  content: string;
  seo_title: string;
  seo_description: string;
  seo_keywords: string[];
  variables: Record<string, unknown>;
}

export function PagePreview({ template, dataset, settings }: PagePreviewProps) {
  const [previewPages, setPreviewPages] = useState<PreviewPage[]>([]);
  const [currentPageIndex, setCurrentPageIndex] = useState(0);
  const [viewMode, setViewMode] = useState<'preview' | 'html' | 'seo'>('preview');
  const [loading, setLoading] = useState(false);

  const generatePreviewPages = useCallback(async () => {
    if (!template || !dataset) return;
    
    setLoading(true);
    try {
      // Generate sample pages with the first few rows of data
      const sampleData = dataset.data.slice(0, 3);
      const pages: PreviewPage[] = [];

      for (const row of sampleData) {
        const page = generatePageFromTemplate(template, row);
        pages.push(page);
      }

      setPreviewPages(pages);
      setCurrentPageIndex(0);
    } catch (error) {
      console.error('Error generating preview pages:', error);
    } finally {
      setLoading(false);
    }
  }, [template, dataset, generatePageFromTemplate]);

  useEffect(() => {
    generatePreviewPages();
  }, [generatePreviewPages]);

  const generatePageFromTemplate = useCallback((template: Template, data: Record<string, unknown>): PreviewPage => {
    // Simple template variable replacement
    let content = template.template_html;
    let seoTitle = template.seo_settings.meta_title || '';
    let seoDescription = template.seo_settings.meta_description || '';
    
    // Replace variables in content
    template.variables.forEach(variable => {
      const value = data[variable.name] || variable.example || `{${variable.name}}`;
      const regex = new RegExp(`\\{\\{${variable.name}\\}\\}`, 'g');
      content = content.replace(regex, value);
      seoTitle = seoTitle.replace(regex, value);
      seoDescription = seoDescription.replace(regex, value);
    });

    // Generate title from first heading or use template name
    const titleMatch = content.match(/<h1[^>]*>([^<]+)<\/h1>/);
    const title = titleMatch ? titleMatch[1] : template.name;

    // Generate slug from title
    const slug = title.toLowerCase()
      .replace(/[^a-z0-9]+/g, '-')
      .replace(/^-+|-+$/g, '');

    // Extract keywords from content
    const keywords = extractKeywords(content);

    return {
      title,
      slug,
      content,
      seo_title: seoTitle || title,
      seo_description: seoDescription || extractDescription(content),
      seo_keywords: keywords,
      variables: data
    };
  }, []);

  const extractKeywords = (content: string): string[] => {
    // Simple keyword extraction - remove HTML tags and get common words
    const text = content.replace(/<[^>]*>/g, '').toLowerCase();
    const words = text.split(/\s+/).filter(word => word.length > 3);
    const commonWords = new Set(['this', 'that', 'with', 'from', 'your', 'have', 'more', 'will', 'been', 'were', 'they', 'them', 'than', 'what', 'when', 'where', 'how']);
    const keywords = [...new Set(words.filter(word => !commonWords.has(word)))];
    return keywords.slice(0, 10);
  };

  const extractDescription = (content: string): string => {
    // Extract first paragraph or first 160 characters
    const text = content.replace(/<[^>]*>/g, '');
    const paragraphs = text.split('\n').filter(p => p.trim().length > 0);
    const description = paragraphs[0] || text;
    return description.length > 160 ? description.substring(0, 157) + '...' : description;
  };

  const currentPage = previewPages[currentPageIndex];

  const handlePreviousPage = () => {
    if (currentPageIndex > 0) {
      setCurrentPageIndex(currentPageIndex - 1);
    }
  };

  const handleNextPage = () => {
    if (currentPageIndex < previewPages.length - 1) {
      setCurrentPageIndex(currentPageIndex + 1);
    }
  };

  const renderPreviewContent = () => {
    if (!currentPage) return null;

    switch (viewMode) {
      case 'preview':
        return (
          <div className="prose max-w-none">
            <div 
              className="bg-white p-6 rounded-lg border min-h-[400px]"
              dangerouslySetInnerHTML={{ __html: currentPage.content }}
            />
          </div>
        );

      case 'html':
        return (
          <div className="bg-gray-900 text-green-400 p-4 rounded-lg overflow-auto max-h-[400px]">
            <pre className="text-sm">
              <code>{currentPage.content}</code>
            </pre>
          </div>
        );

      case 'seo':
        return (
          <div className="space-y-4">
            {/* SEO Title */}
            <div>
              <h4 className="font-semibold text-gray-700 mb-2">SEO Title</h4>
              <div className="p-3 bg-blue-50 border border-blue-200 rounded-lg">
                <p className="text-blue-800 font-medium">{currentPage.seo_title}</p>
                <p className="text-xs text-blue-600 mt-1">
                  {currentPage.seo_title.length} characters
                </p>
              </div>
            </div>

            {/* SEO Description */}
            <div>
              <h4 className="font-semibold text-gray-700 mb-2">SEO Description</h4>
              <div className="p-3 bg-green-50 border border-green-200 rounded-lg">
                <p className="text-green-800">{currentPage.seo_description}</p>
                <p className="text-xs text-green-600 mt-1">
                  {currentPage.seo_description.length} characters
                </p>
              </div>
            </div>

            {/* Keywords */}
            <div>
              <h4 className="font-semibold text-gray-700 mb-2">Keywords</h4>
              <div className="flex flex-wrap gap-2">
                {currentPage.seo_keywords.map((keyword, index) => (
                  <span
                    key={index}
                    className="px-2 py-1 bg-purple-100 text-purple-800 rounded-full text-sm"
                  >
                    {keyword}
                  </span>
                ))}
              </div>
            </div>

            {/* Variables Used */}
            <div>
              <h4 className="font-semibold text-gray-700 mb-2">Variables Used</h4>
              <div className="bg-gray-50 p-3 rounded-lg">
                {Object.entries(currentPage.variables).map(([key, value]) => (
                  <div key={key} className="flex justify-between py-1">
                    <span className="text-gray-600">{key}:</span>
                    <span className="text-gray-900 font-medium">{value}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        );

      default:
        return null;
    }
  };

  if (loading) {
    return (
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <RefreshCw className="w-5 h-5 mr-2 animate-spin" />
            Generating Preview...
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex items-center justify-center py-8">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-purple-600"></div>
          </div>
        </CardContent>
      </Card>
    );
  }

  if (!currentPage) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Page Preview</CardTitle>
          <CardDescription>No preview available</CardDescription>
        </CardHeader>
        <CardContent>
          <p className="text-gray-500">Unable to generate preview pages.</p>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card>
      <CardHeader>
        <div className="flex items-center justify-between">
          <div>
            <CardTitle className="flex items-center">
              <Eye className="w-5 h-5 mr-2" />
              Page Preview
            </CardTitle>
            <CardDescription>
              Preview of generated pages ({previewPages.length} sample pages)
            </CardDescription>
          </div>
          
          {/* View Mode Selector */}
          <div className="flex bg-gray-100 rounded-lg p-1">
            <Button
              variant={viewMode === 'preview' ? 'default' : 'ghost'}
              size="sm"
              onClick={() => setViewMode('preview')}
            >
              <Eye className="w-4 h-4 mr-1" />
              Preview
            </Button>
            <Button
              variant={viewMode === 'html' ? 'default' : 'ghost'}
              size="sm"
              onClick={() => setViewMode('html')}
            >
              <Code className="w-4 h-4 mr-1" />
              HTML
            </Button>
            <Button
              variant={viewMode === 'seo' ? 'default' : 'ghost'}
              size="sm"
              onClick={() => setViewMode('seo')}
            >
              <Search className="w-4 h-4 mr-1" />
              SEO
            </Button>
          </div>
        </div>
      </CardHeader>
      
      <CardContent>
        {/* Page Navigation */}
        <div className="flex items-center justify-between mb-4 pb-4 border-b">
          <div className="flex items-center space-x-2">
            <Button
              variant="outline"
              size="sm"
              onClick={handlePreviousPage}
              disabled={currentPageIndex === 0}
            >
              <ChevronLeft className="w-4 h-4" />
            </Button>
            
            <span className="text-sm text-gray-600">
              Page {currentPageIndex + 1} of {previewPages.length}
            </span>
            
            <Button
              variant="outline"
              size="sm"
              onClick={handleNextPage}
              disabled={currentPageIndex === previewPages.length - 1}
            >
              <ChevronRight className="w-4 h-4" />
            </Button>
          </div>
          
          <div className="flex items-center space-x-2">
            <Globe className="w-4 h-4 text-gray-500" />
            <span className="text-sm text-gray-600">/{currentPage.slug}</span>
            <ExternalLink className="w-4 h-4 text-gray-400" />
          </div>
        </div>

        {/* Preview Content */}
        <div className="space-y-4">
          {renderPreviewContent()}
        </div>

        {/* Refresh Button */}
        <div className="flex justify-end mt-4 pt-4 border-t">
          <Button
            variant="outline"
            size="sm"
            onClick={generatePreviewPages}
            disabled={loading}
          >
            <RefreshCw className="w-4 h-4 mr-2" />
            Refresh Preview
          </Button>
        </div>
      </CardContent>
    </Card>
  );
}