'use client';

import { useState, useEffect } from 'react';
import { useParams, useRouter } from 'next/navigation';
import Link from 'next/link';
import { apiClient } from '@/lib/api/client';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { ArrowLeft, Sparkles, AlertCircle, CheckCircle, Clock } from 'lucide-react';
import { GenerationWizard } from '@/components/page-generation/GenerationWizard';
import { 
  Project, 
  Template, 
  Dataset, 
  GenerationConfig, 
  GenerationResult 
} from '@/types';

export default function GeneratePagesPage() {
  const params = useParams();
  const router = useRouter();
  const projectId = params?.id as string;

  const [project, setProject] = useState<Project | null>(null);
  const [templates, setTemplates] = useState<Template[]>([]);
  const [datasets, setDatasets] = useState<Dataset[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [generationResult, setGenerationResult] = useState<GenerationResult | null>(null);

  useEffect(() => {
    if (projectId) {
      loadProjectData();
    }
  }, [projectId]);

  const loadProjectData = async () => {
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
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load project data');
    } finally {
      setLoading(false);
    }
  };

  const handleGeneration = async (config: GenerationConfig) => {
    try {
      setError(null);
      setGenerationResult({ 
        status: 'pending', 
        total_pages: 0, 
        generated_pages: 0, 
        failed_pages: 0,
        preview_pages: []
      });

      // Use backend API structure: /api/projects/{project_id}/templates/{template_id}/generate
      const response = await apiClient.post(
        `/api/projects/${projectId}/templates/${config.template_id}/generate`,
        {
          batch_size: config.generation_settings.max_pages || 100
        }
      );

      const result = response.data;
      setGenerationResult({
        status: result.status === 'completed' ? 'completed' : 'failed',
        total_pages: result.total_generated,
        generated_pages: result.total_generated,
        failed_pages: 0,
        preview_pages: []
      });
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to generate pages');
      setGenerationResult(null);
    }
  };

  const handleViewResults = () => {
    router.push(`/projects/${projectId}/results`);
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

  // Check if we have required data
  const hasTemplates = templates.length > 0;
  const hasDatasets = datasets.length > 0;
  const canGenerate = hasTemplates && hasDatasets;

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
            <span>Bulk Page Generation</span>
          </div>
        </div>
      </div>

      {/* Prerequisites Check */}
      <div className="mb-8">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">Prerequisites</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <Card className={`${hasTemplates ? 'border-green-200 bg-green-50' : 'border-orange-200 bg-orange-50'}`}>
            <CardContent className="p-4">
              <div className="flex items-center">
                {hasTemplates ? (
                  <CheckCircle className="w-5 h-5 text-green-600 mr-3" />
                ) : (
                  <AlertCircle className="w-5 h-5 text-orange-600 mr-3" />
                )}
                <div>
                  <p className="font-medium">Templates</p>
                  <p className="text-sm text-gray-600">
                    {hasTemplates ? `${templates.length} templates ready` : 'No templates found'}
                  </p>
                </div>
              </div>
              {!hasTemplates && (
                <Link href={`/projects/${projectId}/templates`}>
                  <Button size="sm" className="mt-2">
                    Create Template
                  </Button>
                </Link>
              )}
            </CardContent>
          </Card>

          <Card className={`${hasDatasets ? 'border-green-200 bg-green-50' : 'border-orange-200 bg-orange-50'}`}>
            <CardContent className="p-4">
              <div className="flex items-center">
                {hasDatasets ? (
                  <CheckCircle className="w-5 h-5 text-green-600 mr-3" />
                ) : (
                  <AlertCircle className="w-5 h-5 text-orange-600 mr-3" />
                )}
                <div>
                  <p className="font-medium">Data</p>
                  <p className="text-sm text-gray-600">
                    {hasDatasets ? `${datasets.length} datasets ready` : 'No data imported'}
                  </p>
                </div>
              </div>
              {!hasDatasets && (
                <Link href={`/projects/${projectId}/data`}>
                  <Button size="sm" className="mt-2">
                    Import Data
                  </Button>
                </Link>
              )}
            </CardContent>
          </Card>
        </div>
      </div>

      {/* Generation Wizard or Results */}
      {canGenerate ? (
        <div className="space-y-6">
          {/* Error Display */}
          {error && (
            <Card className="border-red-200 bg-red-50">
              <CardContent className="p-4">
                <div className="flex items-center">
                  <AlertCircle className="w-5 h-5 text-red-600 mr-3" />
                  <div>
                    <p className="font-medium text-red-800">Generation Error</p>
                    <p className="text-sm text-red-600">{error}</p>
                  </div>
                </div>
              </CardContent>
            </Card>
          )}

          {/* Generation Results */}
          {generationResult && (
            <Card>
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
                    <div className="text-2xl font-bold text-red-600">
                      {generationResult.failed_pages}
                    </div>
                    <div className="text-sm text-gray-600">Failed Pages</div>
                  </div>
                </div>
                
                {generationResult.status === 'completed' && (
                  <div className="flex justify-center">
                    <Button onClick={handleViewResults} className="bg-gradient-to-r from-purple-600 to-blue-600">
                      View All Results
                    </Button>
                  </div>
                )}
              </CardContent>
            </Card>
          )}

          {/* Generation Wizard */}
          <GenerationWizard
            projectId={projectId}
            templates={templates}
            datasets={datasets}
            onGenerate={handleGeneration}
            generationResult={generationResult}
          />
        </div>
      ) : (
        <Card>
          <CardHeader>
            <CardTitle>Ready to Generate?</CardTitle>
            <CardDescription>
              Complete the prerequisites above to start generating pages.
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <p className="text-gray-600">
                You need at least one template and one dataset to generate pages.
              </p>
              <div className="flex gap-4">
                <Link href={`/projects/${projectId}/templates`}>
                  <Button variant="outline">Create Template</Button>
                </Link>
                <Link href={`/projects/${projectId}/data`}>
                  <Button variant="outline">Import Data</Button>
                </Link>
              </div>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}