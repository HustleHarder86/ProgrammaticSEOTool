'use client';

import { useState, useEffect, useCallback } from 'react';
import { useParams, useRouter, useSearchParams } from 'next/navigation';
import Link from 'next/link';
import { apiClient } from '@/lib/api/client';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { ArrowLeft, Sparkles, CheckCircle, Clock, Download, Loader2 } from 'lucide-react';
import { AIGenerationWizard } from '@/components/generation';
import PotentialPagesSelector from './potential-pages';
import { 
  Project, 
  Template, 
  Dataset, 
  GenerationResult 
} from '@/types';

export default function GeneratePagesPage() {
  const params = useParams();
  const router = useRouter();
  const searchParams = useSearchParams();
  const projectId = params?.id as string;
  const templateId = searchParams?.get('templateId');

  const [project, setProject] = useState<Project | null>(null);
  const [templates, setTemplates] = useState<Template[]>([]);
  const [, setDatasets] = useState<Dataset[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [generationResult, setGenerationResult] = useState<GenerationResult | null>(null);
  const [selectedTemplate, setSelectedTemplate] = useState<Template | null>(null);
  const [showPotentialPages, setShowPotentialPages] = useState(false);
  const [generatingVariables, setGeneratingVariables] = useState(false);

  const loadProjectData = useCallback(async () => {
    try {
      setLoading(true);
      
      // Load project, templates, and datasets in parallel
      const [projectRes, templatesRes, datasetsRes] = await Promise.all([
        apiClient.get<Project>(`/api/projects/${projectId}`),
        apiClient.get<Template[]>(`/api/projects/${projectId}/templates`),
        apiClient.get<Dataset[]>(`/api/projects/${projectId}/data`)
      ]);

      setProject(projectRes.data);
      setTemplates(templatesRes.data);
      setDatasets(datasetsRes.data);
      
      // If templateId is provided, find and set the selected template
      if (templateId && templatesRes.data) {
        const template = templatesRes.data.find(t => t.id === templateId);
        if (template) {
          setSelectedTemplate(template);
        }
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load project data');
    } finally {
      setLoading(false);
    }
  }, [projectId, templateId]);

  useEffect(() => {
    if (projectId) {
      loadProjectData();
    }
  }, [projectId, loadProjectData]);

  // Automatically generate variables when a template is selected from URL
  useEffect(() => {
    if (selectedTemplate && !showPotentialPages && !generatingVariables) {
      handleTemplateSelected(selectedTemplate);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [selectedTemplate]);

  const handleTemplateSelected = async (template: Template) => {
    try {
      setGeneratingVariables(true);
      setError(null);
      
      // Generate variables and potential pages
      const response = await apiClient.post(
        `/api/projects/${projectId}/templates/${template.id}/generate-variables`,
        {}
      );
      
      console.log('Variables generated:', response.data);
      
      // If potential pages were generated, show the selection interface
      if (response.data.potential_pages_generated > 0) {
        setShowPotentialPages(true);
      } else {
        setError('Failed to generate potential pages. Please try again.');
      }
    } catch (err) {
      console.error('Failed to generate variables:', err);
      setError(err instanceof Error ? err.message : 'Failed to generate variables');
    } finally {
      setGeneratingVariables(false);
    }
  };

  const handleGenerationComplete = (result: GenerationResult | { status: string; generated_count: number }) => {
    // Handle both types of results
    let generationResult: GenerationResult;
    
    if ('generated_pages' in result) {
      // Already a GenerationResult
      generationResult = result as GenerationResult;
    } else {
      // Convert from simpler format
      generationResult = {
        status: result.status as 'completed' | 'failed',
        total_pages: result.generated_count,
        generated_pages: result.generated_count,
        failed_pages: 0,
        preview_pages: []
      };
    }
    
    setGenerationResult(generationResult);
    
    if (generationResult.status === 'completed') {
      // Could redirect to results page or show inline
      router.push(`/projects/${projectId}/pages`);
    }
  };
  
  const handleBackToTemplates = () => {
    setShowPotentialPages(false);
    setSelectedTemplate(null);
    setGeneratingVariables(false);
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-600"></div>
      </div>
    );
  }

  if (error && !project) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
          {error}
        </div>
        <Link href={`/projects/${projectId}`}>
          <Button variant="outline" className="mt-4">
            <ArrowLeft className="w-4 h-4 mr-2" />
            Back to Project
          </Button>
        </Link>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8 max-w-6xl">
      {/* Header */}
      <div className="mb-8">
        <Link href={`/projects/${projectId}`}>
          <Button variant="ghost" className="mb-4">
            <ArrowLeft className="w-4 h-4 mr-2" />
            Back to Project
          </Button>
        </Link>
        
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900 mb-2">
              Generate Pages
            </h1>
            <p className="text-lg text-gray-600">
              Create bulk pages for {project?.business_analysis?.business_name || project?.name}
            </p>
          </div>
          <div className="flex items-center text-sm text-gray-500">
            <Sparkles className="w-4 h-4 mr-1" />
            <span>AI-Powered Generation</span>
          </div>
        </div>
      </div>

      {/* Show generating variables loader */}
      {generatingVariables && (
        <Card>
          <CardContent className="flex items-center justify-center py-12">
            <div className="text-center">
              <Loader2 className="w-12 h-12 animate-spin text-purple-600 mx-auto mb-4" />
              <p className="text-lg font-semibold">Generating Variables...</p>
              <p className="text-gray-600">AI is creating relevant data for your template</p>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Show potential pages selector if we have a template and pages are ready */}
      {showPotentialPages && selectedTemplate && !generatingVariables ? (
        <PotentialPagesSelector
          projectId={projectId}
          templateId={selectedTemplate.id}
          templateName={selectedTemplate.name}
          templatePattern={selectedTemplate.pattern}
          onBack={handleBackToTemplates}
          onComplete={handleGenerationComplete}
        />
      ) : !generatingVariables && (
        <>
          {/* Show message if no templates */}
          {templates.length === 0 ? (
            <Card>
              <CardHeader>
                <CardTitle>No Templates Found</CardTitle>
                <CardDescription>
                  You need to create a template first before generating pages.
                </CardDescription>
              </CardHeader>
              <CardContent>
                <Link href={`/projects/${projectId}/templates`}>
                  <Button>Create Template</Button>
                </Link>
              </CardContent>
            </Card>
          ) : (
            /* AI Generation Wizard - only show if no template selected */
            !selectedTemplate && (
              <AIGenerationWizard 
                projectId={projectId}
                templates={templates}
                businessContext={project?.business_analysis || {}}
                onGenerationComplete={handleGenerationComplete}
              />
            )
          )}
        </>
      )}

      {/* Generation Results */}
      {generationResult && (
        <Card className="mt-8">
          <CardHeader>
            <CardTitle className="flex items-center">
              {generationResult.status === 'completed' ? (
                <CheckCircle className="w-5 h-5 text-green-600 mr-2" />
              ) : (
                <Clock className="w-5 h-5 text-blue-600 mr-2" />
              )}
              Generation {generationResult.status}
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
              <div className="text-center">
                <div className="text-2xl font-bold text-green-600">
                  {generationResult.generated_pages}
                </div>
                <div className="text-sm text-gray-600">Pages Generated</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-blue-600">
                  {generationResult.total_pages}
                </div>
                <div className="text-sm text-gray-600">Total Pages</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-purple-600">
                  {generationResult.failed_pages}
                </div>
                <div className="text-sm text-gray-600">Failed Pages</div>
              </div>
            </div>
            
            <div className="flex gap-4">
              <Button 
                onClick={() => router.push(`/projects/${projectId}/pages`)}
                className="flex-1"
              >
                View Generated Pages
              </Button>
              <Link href={`/projects/${projectId}/export`}>
                <Button variant="outline">
                  <Download className="w-4 h-4 mr-2" />
                  Export Pages
                </Button>
              </Link>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}