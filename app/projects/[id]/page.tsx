'use client';

import { useState, useEffect, useCallback } from 'react';
import { useParams, useSearchParams } from 'next/navigation';
import Link from 'next/link';
import { apiClient } from '@/lib/api/client';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { 
  ArrowLeft, FileText, Sparkles, Download, 
  LayoutTemplate, Database, Calendar, TrendingUp,
  MapPin, Users, Plus
} from 'lucide-react';
import { formatDistanceToNow } from 'date-fns';

interface Project {
  id: string;
  name: string;
  business_input: string;
  business_analysis: {
    business_name?: string;
    business_description?: string;
    target_audience?: string;
    core_offerings?: string[];
    template_opportunities?: Array<{
      template_name: string;
      template_pattern: string;
      example_pages: string[];
      estimated_pages: number;
      difficulty: string;
    }>;
  };
  created_at: string;
  updated_at?: string;
}

export default function ProjectDetailPage() {
  const params = useParams();
  const searchParams = useSearchParams();
  const projectId = params.id as string;
  const selectedTemplate = searchParams.get('template');
  
  const [project, setProject] = useState<Project | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchProject = useCallback(async () => {
    try {
      setLoading(true);
      const response = await apiClient.get<Project>(`/api/projects/${projectId}`);
      setProject(response.data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch project');
    } finally {
      setLoading(false);
    }
  }, [projectId]);

  useEffect(() => {
    if (projectId) {
      fetchProject();
    }
  }, [projectId, fetchProject]);

  const getIcon = (templateName: string) => {
    const name = templateName.toLowerCase();
    if (name.includes('location') || name.includes('city') || name.includes('area')) return MapPin;
    if (name.includes('comparison') || name.includes('vs')) return TrendingUp;
    if (name.includes('industry') || name.includes('business') || name.includes('company')) return Users;
    return FileText;
  };

  const getDifficultyColor = (difficulty: string) => {
    const level = difficulty.toLowerCase();
    if (level.includes('low') || level.includes('easy')) return 'text-green-700 bg-green-50 border-green-200';
    if (level.includes('medium') || level.includes('moderate')) return 'text-yellow-700 bg-yellow-50 border-yellow-200';
    return 'text-red-700 bg-red-50 border-red-200';
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-600"></div>
      </div>
    );
  }

  if (error || !project) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
          {error || 'Project not found'}
        </div>
        <Link href="/">
          <Button variant="outline" className="mt-4">
            <ArrowLeft className="w-4 h-4 mr-2" />
            Back to Dashboard
          </Button>
        </Link>
      </div>
    );
  }

  const analysis = project.business_analysis;
  const templates = analysis?.template_opportunities || [];

  return (
    <div className="container mx-auto px-4 py-8 max-w-7xl">
      {/* Header */}
      <div className="mb-8">
        <Link href="/">
          <Button variant="ghost" className="mb-4">
            <ArrowLeft className="w-4 h-4 mr-2" />
            Back to Dashboard
          </Button>
        </Link>
        
        <div className="flex items-start justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900 mb-2">
              {analysis?.business_name || project.name}
            </h1>
            <p className="text-lg text-gray-600">
              {analysis?.business_description || project.business_input}
            </p>
          </div>
          <div className="text-sm text-gray-500">
            <div className="flex items-center">
              <Calendar className="w-4 h-4 mr-1" />
              Created {formatDistanceToNow(new Date(project.created_at), { addSuffix: true })}
            </div>
          </div>
        </div>
      </div>

      {/* Business Overview */}
      {analysis && (
        <Card className="mb-8">
          <CardHeader>
            <CardTitle>Business Overview</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            {analysis.target_audience && (
              <div>
                <h4 className="font-semibold text-gray-700 mb-1">Target Audience</h4>
                <p className="text-gray-600">{analysis.target_audience}</p>
              </div>
            )}
            {analysis.core_offerings && analysis.core_offerings.length > 0 && (
              <div>
                <h4 className="font-semibold text-gray-700 mb-2">Core Offerings</h4>
                <ul className="list-disc list-inside space-y-1">
                  {analysis.core_offerings.map((offering, index) => (
                    <li key={index} className="text-gray-600">{offering}</li>
                  ))}
                </ul>
              </div>
            )}
          </CardContent>
        </Card>
      )}

      {/* Template Opportunities */}
      <div className="mb-8">
        <h2 className="text-2xl font-bold text-gray-900 mb-6">Template Opportunities</h2>
        {selectedTemplate && (
          <div className="mb-4 p-4 bg-purple-50 border border-purple-200 rounded-lg">
            <p className="text-purple-700">
              Selected template: <strong>{selectedTemplate}</strong>
            </p>
          </div>
        )}
        
        <div className="grid gap-6">
          {templates.map((template, index) => {
            const Icon = getIcon(template.template_name);
            const isSelected = template.template_name === selectedTemplate;
            
            return (
              <Card 
                key={index}
                className={`transition-all duration-300 ${
                  isSelected ? 'border-purple-500 shadow-lg' : 'hover:shadow-md'
                }`}
              >
                <CardHeader>
                  <div className="flex items-start justify-between">
                    <div className="flex items-start">
                      <div className="w-12 h-12 rounded-lg bg-gradient-to-br from-purple-100 to-blue-100 flex items-center justify-center mr-4">
                        <Icon className="w-6 h-6 text-purple-700" />
                      </div>
                      <div>
                        <CardTitle className="text-xl">{template.template_name}</CardTitle>
                        <CardDescription className="mt-1">
                          Pattern: <code className="text-sm bg-gray-100 px-2 py-1 rounded">{template.template_pattern}</code>
                        </CardDescription>
                      </div>
                    </div>
                    <span className={`px-3 py-1 rounded-full text-sm font-semibold border ${getDifficultyColor(template.difficulty)}`}>
                      {template.difficulty}
                    </span>
                  </div>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    <div>
                      <h4 className="font-semibold text-gray-700 mb-2">Example Pages:</h4>
                      <ul className="space-y-1">
                        {template.example_pages.slice(0, 3).map((example, i) => (
                          <li key={i} className="text-gray-600 flex items-start">
                            <span className="text-purple-600 mr-2">→</span>
                            {example}
                          </li>
                        ))}
                      </ul>
                    </div>
                    
                    <div className="flex items-center justify-between pt-4 border-t">
                      <div className="flex items-center text-sm">
                        <Sparkles className="w-4 h-4 text-purple-600 mr-1" />
                        <span className="font-semibold text-purple-600">
                          {template.estimated_pages.toLocaleString()} pages
                        </span>
                        <span className="text-gray-600 ml-1">potential</span>
                      </div>
                      
                      <div className="flex gap-2">
                        <Link href={`/projects/${projectId}/data`}>
                          <Button size="sm" variant="outline">
                            <Database className="w-4 h-4 mr-2" />
                            Import Data
                          </Button>
                        </Link>
                        <Link href={`/projects/${projectId}/templates?template=${encodeURIComponent(template.template_name)}`}>
                          <Button size="sm" variant="outline">
                            <LayoutTemplate className="w-4 h-4 mr-2" />
                            Build Template
                          </Button>
                        </Link>
                        <Link href={`/projects/${projectId}/generate`}>
                          <Button 
                            size="sm"
                            className="bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700"
                          >
                            <Sparkles className="w-4 h-4 mr-2" />
                            Generate Pages
                          </Button>
                        </Link>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            );
          })}
        </div>
      </div>

      {/* Quick Actions */}
      <Card>
        <CardHeader>
          <CardTitle>Next Steps</CardTitle>
          <CardDescription>
            Choose a template above to start building, or explore other options
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="flex flex-wrap gap-4">
            <Link href={`/projects/${projectId}/templates`}>
              <Button variant="outline">
                <FileText className="w-4 h-4 mr-2" />
                Create Custom Template
              </Button>
            </Link>
            <Link href={`/projects/${projectId}/data`}>
              <Button variant="outline">
                <Database className="w-4 h-4 mr-2" />
                Manage Data
              </Button>
            </Link>
            <Link href={`/projects/${projectId}/generate`}>
              <Button className="bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700">
                <Sparkles className="w-4 h-4 mr-2" />
                Generate Pages
              </Button>
            </Link>
            <Link href={`/projects/${projectId}/export`}>
              <Button variant="outline">
                <Download className="w-4 h-4 mr-2" />
                Export Project Data
              </Button>
            </Link>
            <Link href="/analyze">
              <Button variant="outline">
                <Plus className="w-4 h-4 mr-2" />
                Analyze Another Business
              </Button>
            </Link>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}