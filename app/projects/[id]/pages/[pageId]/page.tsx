'use client';

import { useState, useEffect, useCallback } from 'react';
import { useParams, useRouter } from 'next/navigation';
import Link from 'next/link';
import { apiClient } from '@/lib/api/client';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { ArrowLeft, Copy, Download } from 'lucide-react';
import { Project } from '@/types';

interface PageContent {
  title: string;
  meta_description: string;
  content_sections: {
    intro?: string;
    main_content?: string;
    features?: string[];
    benefits?: string[];
    conclusion?: string;
    faq?: Array<{ question: string; answer: string }>;
  };
  schema_markup?: Record<string, unknown>;
  quality_metrics?: {
    word_count: number;
    reading_time: number;
    keyword_density: number;
    quality_score: number;
  };
}

interface GeneratedPageDetail {
  id: string;
  project_id: string;
  template_id: string;
  title: string;
  content: PageContent;
  meta_data: {
    slug: string;
    keyword: string;
    variables: Record<string, string | number>;
  };
  created_at: string;
  updated_at: string;
}

export default function PageDetailPage() {
  const params = useParams();
  const router = useRouter(); // eslint-disable-line @typescript-eslint/no-unused-vars
  const projectId = params?.id as string;
  const pageId = params?.pageId as string;

  const [project, setProject] = useState<Project | null>(null); // eslint-disable-line @typescript-eslint/no-unused-vars
  const [page, setPage] = useState<GeneratedPageDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState('preview');
  const [copying, setCopying] = useState(false);

  const loadPageData = useCallback(async () => {
    try {
      setLoading(true);
      
      // Load project and page data in parallel
      const [projectRes, pageRes] = await Promise.all([
        apiClient.get<Project>(`/api/projects/${projectId}`),
        apiClient.get<GeneratedPageDetail>(`/api/projects/${projectId}/pages/${pageId}`)
      ]);

      setProject(projectRes.data);
      setPage(pageRes.data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load page data');
    } finally {
      setLoading(false);
    }
  }, [projectId, pageId]);

  useEffect(() => {
    if (projectId && pageId) {
      loadPageData();
    }
  }, [projectId, pageId, loadPageData]);

  const handleCopyContent = async () => {
    if (!page) return;
    
    try {
      setCopying(true);
      const content = generateHTMLContent(page);
      await navigator.clipboard.writeText(content);
      // Could add a toast notification here
    } catch (err) {
      console.error('Failed to copy content:', err);
    } finally {
      setCopying(false);
    }
  };

  const generateHTMLContent = (page: GeneratedPageDetail): string => {
    const { content } = page;
    let html = `<h1>${content.title}</h1>\n\n`;
    
    if (content.content_sections.intro) {
      html += `<p>${content.content_sections.intro}</p>\n\n`;
    }
    
    if (content.content_sections.main_content) {
      html += `${content.content_sections.main_content}\n\n`;
    }
    
    if (content.content_sections.features && content.content_sections.features.length > 0) {
      html += `<h2>Features</h2>\n<ul>\n`;
      content.content_sections.features.forEach(feature => {
        html += `  <li>${feature}</li>\n`;
      });
      html += `</ul>\n\n`;
    }
    
    if (content.content_sections.benefits && content.content_sections.benefits.length > 0) {
      html += `<h2>Benefits</h2>\n<ul>\n`;
      content.content_sections.benefits.forEach(benefit => {
        html += `  <li>${benefit}</li>\n`;
      });
      html += `</ul>\n\n`;
    }
    
    if (content.content_sections.conclusion) {
      html += `<p>${content.content_sections.conclusion}</p>\n\n`;
    }
    
    if (content.content_sections.faq && content.content_sections.faq.length > 0) {
      html += `<h2>Frequently Asked Questions</h2>\n`;
      content.content_sections.faq.forEach(item => {
        html += `<h3>${item.question}</h3>\n<p>${item.answer}</p>\n\n`;
      });
    }
    
    return html;
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-600"></div>
      </div>
    );
  }

  if (error || !page) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
          {error || 'Page not found'}
        </div>
        <Link href={`/projects/${projectId}/pages`}>
          <Button variant="outline" className="mt-4">
            <ArrowLeft className="w-4 h-4 mr-2" />
            Back to Pages
          </Button>
        </Link>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8 max-w-6xl">
      {/* Header */}
      <div className="mb-8">
        <Link href={`/projects/${projectId}/pages`}>
          <Button variant="ghost" className="mb-4">
            <ArrowLeft className="w-4 h-4 mr-2" />
            Back to Pages
          </Button>
        </Link>
        
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900 mb-2">
              {page.title}
            </h1>
            <div className="flex items-center gap-4 text-sm text-gray-600">
              <span>Keyword: <strong>{page.meta_data.keyword}</strong></span>
              <span>Slug: <code className="bg-gray-100 px-2 py-1 rounded">/{page.meta_data.slug}</code></span>
            </div>
          </div>
          <div className="flex gap-2">
            <Button variant="outline" onClick={handleCopyContent} disabled={copying}>
              <Copy className="w-4 h-4 mr-2" />
              {copying ? 'Copying...' : 'Copy HTML'}
            </Button>
            <Link href={`/projects/${projectId}/export`}>
              <Button variant="outline">
                <Download className="w-4 h-4 mr-2" />
                Export
              </Button>
            </Link>
          </div>
        </div>
      </div>

      {/* Page Metrics */}
      {page.content.quality_metrics && (
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
          <Card>
            <CardHeader className="pb-2">
              <CardDescription>Word Count</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{page.content.quality_metrics.word_count}</div>
            </CardContent>
          </Card>
          <Card>
            <CardHeader className="pb-2">
              <CardDescription>Reading Time</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{page.content.quality_metrics.reading_time} min</div>
            </CardContent>
          </Card>
          <Card>
            <CardHeader className="pb-2">
              <CardDescription>Keyword Density</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{page.content.quality_metrics.keyword_density}%</div>
            </CardContent>
          </Card>
          <Card>
            <CardHeader className="pb-2">
              <CardDescription>Quality Score</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                <Badge 
                  variant={page.content.quality_metrics.quality_score >= 80 ? 'default' : 
                          page.content.quality_metrics.quality_score >= 60 ? 'secondary' : 'outline'}
                  className="text-lg px-3 py-1"
                >
                  {page.content.quality_metrics.quality_score}%
                </Badge>
              </div>
            </CardContent>
          </Card>
        </div>
      )}

      {/* Content Tabs */}
      <Tabs value={activeTab} onValueChange={setActiveTab}>
        <TabsList className="grid w-full grid-cols-4">
          <TabsTrigger value="preview">Preview</TabsTrigger>
          <TabsTrigger value="content">Content</TabsTrigger>
          <TabsTrigger value="metadata">Metadata</TabsTrigger>
          <TabsTrigger value="schema">Schema</TabsTrigger>
        </TabsList>

        <TabsContent value="preview" className="mt-6">
          <Card>
            <CardContent className="prose prose-gray max-w-none p-8">
              {/* Render HTML content if available, otherwise render sections */}
              {page.content.content_html ? (
                <div dangerouslySetInnerHTML={{ __html: page.content.content_html }} />
              ) : Array.isArray(page.content.content_sections) ? (
                // New format: array of sections
                <>
                  <h1>{page.content.h1 || page.title}</h1>
                  {page.content.content_sections.map((section: any, index: number) => {
                    const sectionType = section.type || '';
                    const content = section.content || '';
                    const heading = section.heading || '';
                    
                    if (sectionType === 'introduction') {
                      return <p key={index} className="lead">{content}</p>;
                    } else if (sectionType === 'faq') {
                      return (
                        <div key={index}>
                          <h2>{heading}</h2>
                          <div dangerouslySetInnerHTML={{ __html: content.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>').replace(/\n\n/g, '<br><br>') }} />
                        </div>
                      );
                    } else if (sectionType === 'statistics') {
                      return (
                        <div key={index}>
                          <h2>{heading}</h2>
                          <div className="statistics" dangerouslySetInnerHTML={{ __html: content.replace(/\n/g, '<br>') }} />
                        </div>
                      );
                    } else if (sectionType === 'conclusion') {
                      return <p key={index} className="conclusion">{content}</p>;
                    } else {
                      // Regular content section
                      return (
                        <div key={index}>
                          {heading && <h2>{heading}</h2>}
                          <p>{content}</p>
                        </div>
                      );
                    }
                  })}
                </>
              ) : (
                // Fallback: display raw content
                <div>
                  <h1>{page.title}</h1>
                  <pre>{JSON.stringify(page.content, null, 2)}</pre>
                </div>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="content" className="mt-6">
          <Card>
            <CardHeader>
              <CardTitle>Raw Content Sections</CardTitle>
            </CardHeader>
            <CardContent>
              <pre className="bg-gray-50 p-4 rounded-lg overflow-auto text-sm">
                {JSON.stringify(page.content.content_sections, null, 2)}
              </pre>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="metadata" className="mt-6">
          <Card>
            <CardHeader>
              <CardTitle>Page Metadata</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <h3 className="font-semibold mb-2">SEO Meta Tags</h3>
                <div className="bg-gray-50 p-4 rounded-lg space-y-2">
                  <div>
                    <span className="text-gray-600">Title:</span>
                    <p className="font-mono text-sm">{page.title}</p>
                  </div>
                  <div>
                    <span className="text-gray-600">Description:</span>
                    <p className="font-mono text-sm">{page.content.meta_description}</p>
                  </div>
                  <div>
                    <span className="text-gray-600">URL:</span>
                    <p className="font-mono text-sm">/{page.meta_data.slug}</p>
                  </div>
                </div>
              </div>
              
              <div>
                <h3 className="font-semibold mb-2">Variables Used</h3>
                <div className="bg-gray-50 p-4 rounded-lg">
                  <pre className="text-sm">{JSON.stringify(page.meta_data.variables, null, 2)}</pre>
                </div>
              </div>
              
              <div>
                <h3 className="font-semibold mb-2">Timestamps</h3>
                <div className="bg-gray-50 p-4 rounded-lg space-y-1 text-sm">
                  <div>Created: {new Date(page.created_at).toLocaleString()}</div>
                  <div>Updated: {new Date(page.updated_at).toLocaleString()}</div>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="schema" className="mt-6">
          <Card>
            <CardHeader>
              <CardTitle>Schema Markup</CardTitle>
              <CardDescription>
                Structured data for search engines
              </CardDescription>
            </CardHeader>
            <CardContent>
              {page.content.schema_markup ? (
                <pre className="bg-gray-50 p-4 rounded-lg overflow-auto text-sm">
                  {JSON.stringify(page.content.schema_markup, null, 2)}
                </pre>
              ) : (
                <p className="text-gray-500">No schema markup generated for this page</p>
              )}
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
}