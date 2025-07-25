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
import './blog-preview.css';

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
  } | Array<any>;  // Also support array format
  content_html?: string;  // New field for pre-rendered HTML
  h1?: string;  // H1 heading
  keyword?: string;  // Main keyword
  slug?: string;  // URL slug
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
    
    // If pre-rendered HTML is available, return it
    if (content.content_html) {
      return content.content_html;
    }
    
    let html = `<h1>${content.title}</h1>\n\n`;
    
    // Check if content_sections is an array (new format) or object (old format)
    if (Array.isArray(content.content_sections)) {
      // New format: array of sections
      content.content_sections.forEach((section: any) => {
        if (section.type === 'introduction' && section.content) {
          html += `<p>${section.content}</p>\n\n`;
        } else if (section.type === 'faq' && section.content) {
          html += `<h2>${section.heading || 'FAQ'}</h2>\n`;
          html += `${section.content}\n\n`;
        } else if (section.type === 'statistics' && section.content) {
          html += `<h2>${section.heading || 'Statistics'}</h2>\n`;
          html += `${section.content}\n\n`;
        } else if (section.type === 'conclusion' && section.content) {
          html += `<p>${section.content}</p>\n\n`;
        } else if (section.content) {
          if (section.heading) {
            html += `<h2>${section.heading}</h2>\n`;
          }
          html += `<p>${section.content}</p>\n\n`;
        }
      });
    } else if (typeof content.content_sections === 'object') {
      // Old format: object with properties
      const sections = content.content_sections as any;
      
      if (sections.intro) {
        html += `<p>${sections.intro}</p>\n\n`;
      }
      
      if (sections.main_content) {
        html += `${sections.main_content}\n\n`;
      }
      
      if (sections.features && sections.features.length > 0) {
        html += `<h2>Features</h2>\n<ul>\n`;
        sections.features.forEach((feature: string) => {
          html += `  <li>${feature}</li>\n`;
        });
        html += `</ul>\n\n`;
      }
      
      if (sections.benefits && sections.benefits.length > 0) {
        html += `<h2>Benefits</h2>\n<ul>\n`;
        sections.benefits.forEach((benefit: string) => {
          html += `  <li>${benefit}</li>\n`;
        });
        html += `</ul>\n\n`;
      }
      
      if (sections.conclusion) {
        html += `<p>${sections.conclusion}</p>\n\n`;
      }
      
      if (sections.faq && sections.faq.length > 0) {
        html += `<h2>Frequently Asked Questions</h2>\n`;
        sections.faq.forEach((item: { question: string; answer: string }) => {
          html += `<h3>${item.question}</h3>\n<p>${item.answer}</p>\n\n`;
        });
      }
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
          <Card className="overflow-hidden">
            <CardContent className="p-0">
              {/* Blog Post Container */}
              <article className="bg-white">
                {/* Blog Header */}
                <header className="px-8 py-12 bg-gradient-to-b from-gray-50 to-white border-b">
                  <div className="max-w-3xl mx-auto">
                    <h1 className="text-4xl font-bold text-gray-900 mb-4 leading-tight">
                      {page.content.h1 || page.title}
                    </h1>
                    <div className="flex items-center gap-4 text-sm text-gray-600">
                      <time dateTime={page.created_at}>
                        {new Date(page.created_at).toLocaleDateString('en-US', { 
                          year: 'numeric', 
                          month: 'long', 
                          day: 'numeric' 
                        })}
                      </time>
                      <span>•</span>
                      <span>{page.content.quality_metrics?.reading_time || 5} min read</span>
                      {page.content.quality_metrics?.word_count && (
                        <>
                          <span>•</span>
                          <span>{page.content.quality_metrics.word_count} words</span>
                        </>
                      )}
                    </div>
                  </div>
                </header>

                {/* Blog Content */}
                <div className="px-8 py-12">
                  <div className="max-w-3xl mx-auto">
                    {/* Render content with proper blog styling */}
                    {page.content.content_html ? (
                      <div 
                        className="blog-content"
                        dangerouslySetInnerHTML={{ 
                          __html: page.content.content_html
                            .replace(/<h1>/g, '<h1 class="text-3xl font-bold text-gray-900 mb-6 mt-8">')
                            .replace(/<h2>/g, '<h2 class="text-2xl font-bold text-gray-800 mb-4 mt-8">')
                            .replace(/<h3>/g, '<h3 class="text-xl font-semibold text-gray-800 mb-3 mt-6">')
                            .replace(/<h4>/g, '<h4 class="text-lg font-semibold text-gray-700 mb-2 mt-4">')
                            .replace(/<p>/g, '<p class="text-gray-700 leading-relaxed mb-4">')
                            .replace(/<p class='intro'>/g, '<p class="text-xl text-gray-600 leading-relaxed mb-6">')
                            .replace(/<p class='cta'>/g, '<p class="text-lg font-medium text-gray-800 bg-blue-50 p-6 rounded-lg mb-6 border-l-4 border-blue-500">')
                            .replace(/<ul>/g, '<ul class="list-disc pl-6 mb-6 space-y-2">')
                            .replace(/<ul class='provider-list'>/g, '<ul class="space-y-3 mb-6">')
                            .replace(/<li>/g, '<li class="text-gray-700 leading-relaxed">')
                            .replace(/<li><strong>/g, '<li class="flex items-start p-3 bg-gray-50 rounded-lg"><strong class="text-gray-900">')
                            .replace(/<div class='comparison'>/g, '<div class="bg-gray-50 p-6 rounded-lg mb-6">')
                            .replace(/<div class='key-metrics'>/g, '<div class="bg-blue-50 p-6 rounded-lg mb-6 border border-blue-100">')
                            .replace(/<div class='service-overview'>/g, '<div class="mb-8">')
                            .replace(/<table>/g, '<table class="w-full border-collapse mb-6">')
                            .replace(/<th>/g, '<th class="bg-gray-50 p-3 text-left font-semibold border-b-2 border-gray-200">')
                            .replace(/<td>/g, '<td class="p-3 border-b border-gray-200">')
                            .replace(/<blockquote>/g, '<blockquote class="border-l-4 border-blue-500 pl-6 my-6 italic text-gray-600">')
                            .replace(/<strong>/g, '<strong class="font-semibold text-gray-900">') 
                        }} 
                      />
                    ) : Array.isArray(page.content.content_sections) ? (
                      // New format: array of sections with blog styling
                      <div className="space-y-6">
                        {page.content.content_sections.map((section: { type?: string; content?: string; heading?: string }, index: number) => {
                          const sectionType = section.type || '';
                          const content = section.content || '';
                          const heading = section.heading || '';
                          
                          if (sectionType === 'introduction') {
                            return <p key={index} className="text-xl text-gray-600 leading-relaxed mb-6">{content}</p>;
                          } else if (sectionType === 'faq') {
                            return (
                              <div key={index} className="bg-gray-50 p-6 rounded-lg mb-6">
                                <h2 className="text-2xl font-bold text-gray-800 mb-4">{heading}</h2>
                                <div 
                                  className="space-y-4"
                                  dangerouslySetInnerHTML={{ 
                                    __html: content
                                      .replace(/\*\*(.*?)\*\*/g, '<strong class="text-gray-900">$1</strong>')
                                      .replace(/\n\n/g, '</p><p class="text-gray-700 mb-4">')
                                      .replace(/^/, '<p class="text-gray-700 mb-4">')
                                      .replace(/$/, '</p>')
                                  }} 
                                />
                              </div>
                            );
                          } else if (sectionType === 'statistics') {
                            return (
                              <div key={index} className="bg-blue-50 p-6 rounded-lg mb-6 border border-blue-100">
                                <h2 className="text-2xl font-bold text-gray-800 mb-4">{heading}</h2>
                                <div 
                                  className="space-y-2 text-gray-700"
                                  dangerouslySetInnerHTML={{ 
                                    __html: content
                                      .replace(/\n/g, '<br>')
                                      .replace(/<strong>/g, '<strong class="text-gray-900 font-semibold">')
                                  }} 
                                />
                              </div>
                            );
                          } else if (sectionType === 'conclusion') {
                            return (
                              <div key={index} className="bg-gradient-to-r from-purple-50 to-blue-50 p-6 rounded-lg mb-6 border-l-4 border-purple-500">
                                <p className="text-lg text-gray-800 leading-relaxed">{content}</p>
                              </div>
                            );
                          } else {
                            // Regular content section
                            return (
                              <div key={index} className="mb-6">
                                {heading && <h2 className="text-2xl font-bold text-gray-800 mb-4">{heading}</h2>}
                                <p className="text-gray-700 leading-relaxed">{content}</p>
                              </div>
                            );
                          }
                        })}
                      </div>
                    ) : (
                      // Fallback: display raw content with styling
                      <div className="bg-gray-50 p-6 rounded-lg">
                        <h1 className="text-3xl font-bold text-gray-900 mb-6">{page.title}</h1>
                        <pre className="text-sm text-gray-600 whitespace-pre-wrap">{JSON.stringify(page.content, null, 2)}</pre>
                      </div>
                    )}

                    {/* Blog Footer */}
                    <footer className="mt-12 pt-8 border-t border-gray-200">
                      <div className="flex items-center justify-between">
                        <div className="text-sm text-gray-600">
                          <p>Published on {new Date(page.created_at).toLocaleDateString('en-US', { 
                            year: 'numeric', 
                            month: 'long', 
                            day: 'numeric' 
                          })}</p>
                        </div>
                        <div className="flex gap-2">
                          <Badge variant="outline">
                            {page.meta_data.keyword}
                          </Badge>
                        </div>
                      </div>
                    </footer>
                  </div>
                </div>
              </article>
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