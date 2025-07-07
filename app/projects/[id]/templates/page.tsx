'use client';

import { useState, useEffect } from 'react';
import { useParams, useSearchParams, useRouter } from 'next/navigation';
import Link from 'next/link';
import { apiClient } from '@/lib/api/client';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { ArrowLeft, Save, Eye, Database, Sparkles, FileText } from 'lucide-react';
import { TemplateEditor } from '@/components/template-builder/TemplateEditor';
import { VariableManager } from '@/components/template-builder/VariableManager';
import { TemplatePreview } from '@/components/template-builder/TemplatePreview';

interface Template {
  name: string;
  pattern: string;
  sections: {
    title: string;
    meta_description: string;
    h1: string;
    intro: string;
  };
  variables: string[];
  example_values?: Record<string, string>;
}

interface Project {
  id: string;
  name: string;
  business_analysis: {
    business_name?: string;
    template_opportunities?: Array<{
      template_name: string;
      template_pattern: string;
      example_pages: string[];
    }>;
  };
}

export default function TemplateBuilderPage() {
  const params = useParams();
  const searchParams = useSearchParams();
  const router = useRouter();
  const projectId = params?.id as string;
  const templateName = searchParams?.get('template');
  
  const [project, setProject] = useState<Project | null>(null);
  const [template, setTemplate] = useState<Template>({
    name: '',
    pattern: '',
    sections: {
      title: '',
      meta_description: '',
      h1: '',
      intro: ''
    },
    variables: [],
    example_values: {}
  });
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [showPreview, setShowPreview] = useState(false);

  useEffect(() => {
    if (projectId) {
      fetchProject();
    }
  }, [projectId]); // eslint-disable-line react-hooks/exhaustive-deps

  useEffect(() => {
    // Pre-fill template from selected opportunity
    if (templateName && project?.business_analysis?.template_opportunities) {
      const selectedTemplate = project.business_analysis.template_opportunities.find(
        t => t.template_name === templateName
      );
      if (selectedTemplate) {
        setTemplate(prev => ({
          ...prev,
          name: selectedTemplate.template_name,
          pattern: selectedTemplate.template_pattern
        }));
      }
    }
  }, [templateName, project]);

  const fetchProject = async () => {
    try {
      setLoading(true);
      const response = await apiClient.get<Project>(`/api/projects/${projectId}`);
      setProject(response.data);
    } catch (err) {
      console.error('Failed to fetch project:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleTemplateUpdate = (updates: Partial<Template>) => {
    setTemplate(prev => ({ ...prev, ...updates }));
  };

  const handleSaveTemplate = async () => {
    try {
      setSaving(true);
      const response = await apiClient.post('/api/create-template', {
        project_id: projectId,
        ...template
      });
      
      if (response.data.success) {
        // Navigate to data import page
        router.push(`/projects/${projectId}/data?template=${encodeURIComponent(template.name)}`);
      }
    } catch (err) {
      console.error('Failed to save template:', err);
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-600"></div>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8 max-w-7xl">
      {/* Header */}
      <div className="mb-8">
        <Link href={`/projects/${projectId}`}>
          <Button variant="ghost" className="mb-4">
            <ArrowLeft className="w-4 h-4 mr-2" />
            Back to Project
          </Button>
        </Link>
        
        <div className="flex items-start justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900 mb-2">
              Template Builder
            </h1>
            <p className="text-lg text-gray-600">
              Create a reusable template for {project?.business_analysis?.business_name || project?.name}
            </p>
          </div>
          <div className="flex gap-2">
            <Button
              variant="outline"
              onClick={() => setShowPreview(!showPreview)}
            >
              <Eye className="w-4 h-4 mr-2" />
              {showPreview ? 'Hide' : 'Show'} Preview
            </Button>
            <Button
              onClick={handleSaveTemplate}
              disabled={saving || !template.name || !template.pattern}
              className="bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700"
            >
              <Save className="w-4 h-4 mr-2" />
              {saving ? 'Saving...' : 'Save & Continue'}
            </Button>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Template Editor */}
        <div className="lg:col-span-2 space-y-8">
          <TemplateEditor 
            template={template}
            onUpdate={handleTemplateUpdate}
          />
        </div>

        {/* Sidebar */}
        <div className="space-y-6">
          {/* Variable Manager */}
          <VariableManager 
            template={template}
            onUpdate={handleTemplateUpdate}
          />

          {/* Quick Stats */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <Sparkles className="w-5 h-5 mr-2 text-purple-600" />
                Template Potential
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                <div className="flex justify-between">
                  <span className="text-gray-600">Variables Found:</span>
                  <span className="font-semibold">{template.variables.length}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Sections Filled:</span>
                  <span className="font-semibold">
                    {Object.values(template.sections).filter(v => v).length}/4
                  </span>
                </div>
                {template.variables.length >= 2 && (
                  <div className="pt-3 border-t">
                    <p className="text-sm text-gray-600">
                      With 10 values per variable, you could generate{' '}
                      <span className="font-semibold text-purple-600">
                        {Math.pow(10, template.variables.length).toLocaleString()}
                      </span>{' '}
                      unique pages!
                    </p>
                  </div>
                )}
              </div>
            </CardContent>
          </Card>

          {/* Next Steps */}
          <Card>
            <CardHeader>
              <CardTitle>Next Steps</CardTitle>
              <CardDescription>
                After saving your template
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                <div className="flex items-start">
                  <Database className="w-5 h-5 mr-3 text-gray-400 mt-0.5" />
                  <div>
                    <p className="font-medium text-sm">Import Data</p>
                    <p className="text-sm text-gray-600">
                      Upload CSV or enter data for each variable
                    </p>
                  </div>
                </div>
                <div className="flex items-start">
                  <FileText className="w-5 h-5 mr-3 text-gray-400 mt-0.5" />
                  <div>
                    <p className="font-medium text-sm">Generate Pages</p>
                    <p className="text-sm text-gray-600">
                      Create all page combinations automatically
                    </p>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>

      {/* Preview Modal */}
      {showPreview && (
        <div className="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4">
          <div className="bg-white rounded-lg max-w-4xl w-full max-h-[90vh] overflow-auto">
            <div className="sticky top-0 bg-white border-b p-4 flex justify-between items-center">
              <h3 className="text-lg font-semibold">Template Preview</h3>
              <Button
                variant="ghost"
                size="sm"
                onClick={() => setShowPreview(false)}
              >
                Close
              </Button>
            </div>
            <div className="p-6">
              <TemplatePreview template={template} />
            </div>
          </div>
        </div>
      )}
    </div>
  );
}