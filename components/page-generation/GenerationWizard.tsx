'use client';

import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Progress } from '@/components/ui/progress';
import { 
  ChevronLeft, 
  ChevronRight, 
  Settings, 
  FileText, 
  Database, 
  Play,
  CheckCircle,
  AlertCircle
} from 'lucide-react';
import { PagePreview } from './PagePreview';
import { 
  Template, 
  Dataset, 
  GenerationConfig, 
  GenerationResult,
  PageGenerationWizardStep 
} from '@/types';

interface GenerationWizardProps {
  projectId: string;
  templates: Template[];
  datasets: Dataset[];
  onGenerate: (config: GenerationConfig) => void;
  generationResult: GenerationResult | null;
}

export function GenerationWizard({ 
  templates, 
  datasets, 
  onGenerate, 
  generationResult 
}: GenerationWizardProps) {
  const [currentStep, setCurrentStep] = useState(0);
  const [selectedTemplate, setSelectedTemplate] = useState<Template | null>(null);
  const [selectedDataset, setSelectedDataset] = useState<Dataset | null>(null);
  const [generationSettings, setGenerationSettings] = useState({
    max_pages: 100,
    include_variations: true,
    uniqueness_threshold: 0.7,
    output_format: 'html' as 'html' | 'markdown'
  });

  const steps: PageGenerationWizardStep[] = [
    {
      id: 'template',
      title: 'Select Template',
      description: 'Choose the template to use for page generation',
      completed: !!selectedTemplate,
      active: currentStep === 0
    },
    {
      id: 'dataset',
      title: 'Select Dataset',
      description: 'Choose the data source for your pages',
      completed: !!selectedDataset,
      active: currentStep === 1
    },
    {
      id: 'settings',
      title: 'Configure Settings',
      description: 'Adjust generation parameters',
      completed: currentStep > 2,
      active: currentStep === 2
    },
    {
      id: 'preview',
      title: 'Preview & Generate',
      description: 'Review and start the generation process',
      completed: !!generationResult,
      active: currentStep === 3
    }
  ];

  const canProceed = () => {
    switch (currentStep) {
      case 0: return !!selectedTemplate;
      case 1: return !!selectedDataset;
      case 2: return true;
      case 3: return !!selectedTemplate && !!selectedDataset;
      default: return false;
    }
  };

  const handleNext = () => {
    if (canProceed() && currentStep < steps.length - 1) {
      setCurrentStep(currentStep + 1);
    }
  };

  const handlePrevious = () => {
    if (currentStep > 0) {
      setCurrentStep(currentStep - 1);
    }
  };

  const handleGenerate = () => {
    if (selectedTemplate && selectedDataset) {
      const config: GenerationConfig = {
        template_id: selectedTemplate.id,
        dataset_id: selectedDataset.id,
        generation_settings: generationSettings
      };
      onGenerate(config);
    }
  };

  const getEstimatedPages = () => {
    if (!selectedDataset) return 0;
    const dataRows = selectedDataset.data.length;
    const maxPages = generationSettings.max_pages;
    return Math.min(dataRows, maxPages);
  };

  const renderStepContent = () => {
    switch (currentStep) {
      case 0:
        return (
          <div className="space-y-4">
            <h3 className="text-lg font-semibold">Select Template</h3>
            <div className="grid gap-4">
              {templates.map((template) => (
                <Card 
                  key={template.id}
                  className={`cursor-pointer transition-all ${
                    selectedTemplate?.id === template.id 
                      ? 'border-purple-500 bg-purple-50' 
                      : 'hover:border-gray-300'
                  }`}
                  onClick={() => setSelectedTemplate(template)}
                >
                  <CardHeader className="pb-3">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center">
                        <FileText className="w-5 h-5 text-purple-600 mr-3" />
                        <div>
                          <CardTitle className="text-lg">{template.name}</CardTitle>
                          <CardDescription>{template.template_type}</CardDescription>
                        </div>
                      </div>
                      {selectedTemplate?.id === template.id && (
                        <CheckCircle className="w-5 h-5 text-purple-600" />
                      )}
                    </div>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-2">
                      <div className="text-sm text-gray-600">
                        Variables: {template.variables.join(', ')}
                      </div>
                      <div className="text-sm text-gray-500">
                        Created: {new Date(template.created_at).toLocaleDateString()}
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          </div>
        );

      case 1:
        return (
          <div className="space-y-4">
            <h3 className="text-lg font-semibold">Select Dataset</h3>
            <div className="grid gap-4">
              {datasets.map((dataset) => (
                <Card 
                  key={dataset.id}
                  className={`cursor-pointer transition-all ${
                    selectedDataset?.id === dataset.id 
                      ? 'border-purple-500 bg-purple-50' 
                      : 'hover:border-gray-300'
                  }`}
                  onClick={() => setSelectedDataset(dataset)}
                >
                  <CardHeader className="pb-3">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center">
                        <Database className="w-5 h-5 text-blue-600 mr-3" />
                        <div>
                          <CardTitle className="text-lg">{dataset.name}</CardTitle>
                          <CardDescription>{dataset.data.length} rows</CardDescription>
                        </div>
                      </div>
                      {selectedDataset?.id === dataset.id && (
                        <CheckCircle className="w-5 h-5 text-purple-600" />
                      )}
                    </div>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-2">
                      <div className="text-sm text-gray-600">
                        Columns: {dataset.columns.join(', ')}
                      </div>
                      <div className="text-sm text-gray-500">
                        Created: {new Date(dataset.created_at).toLocaleDateString()}
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          </div>
        );

      case 2:
        return (
          <div className="space-y-6">
            <h3 className="text-lg font-semibold">Generation Settings</h3>
            
            <div className="grid gap-6">
              <div className="space-y-3">
                <label className="block text-sm font-medium text-gray-700">
                  Maximum Pages to Generate
                </label>
                <input
                  type="number"
                  min="1"
                  max="10000"
                  value={generationSettings.max_pages}
                  onChange={(e) => setGenerationSettings({
                    ...generationSettings,
                    max_pages: parseInt(e.target.value)
                  })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                />
                <p className="text-sm text-gray-500">
                  Limit the number of pages to generate (max 10,000)
                </p>
              </div>

              <div className="space-y-3">
                <label className="block text-sm font-medium text-gray-700">
                  Content Uniqueness Threshold
                </label>
                <input
                  type="range"
                  min="0.1"
                  max="1"
                  step="0.1"
                  value={generationSettings.uniqueness_threshold}
                  onChange={(e) => setGenerationSettings({
                    ...generationSettings,
                    uniqueness_threshold: parseFloat(e.target.value)
                  })}
                  className="w-full"
                />
                <div className="flex justify-between text-sm text-gray-500">
                  <span>More Similar</span>
                  <span>{Math.round(generationSettings.uniqueness_threshold * 100)}%</span>
                  <span>More Unique</span>
                </div>
              </div>

              <div className="space-y-3">
                <label className="block text-sm font-medium text-gray-700">
                  Include Content Variations
                </label>
                <div className="flex items-center space-x-2">
                  <input
                    type="checkbox"
                    checked={generationSettings.include_variations}
                    onChange={(e) => setGenerationSettings({
                      ...generationSettings,
                      include_variations: e.target.checked
                    })}
                    className="w-4 h-4 text-purple-600 border-gray-300 rounded focus:ring-purple-500"
                  />
                  <span className="text-sm text-gray-600">
                    Generate variations of content to increase uniqueness
                  </span>
                </div>
              </div>

              <div className="space-y-3">
                <label className="block text-sm font-medium text-gray-700">
                  Output Format
                </label>
                <select
                  value={generationSettings.output_format}
                  onChange={(e) => setGenerationSettings({
                    ...generationSettings,
                    output_format: e.target.value as 'html' | 'markdown'
                  })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                >
                  <option value="html">HTML</option>
                  <option value="markdown">Markdown</option>
                </select>
              </div>
            </div>
          </div>
        );

      case 3:
        return (
          <div className="space-y-6">
            <h3 className="text-lg font-semibold">Preview & Generate</h3>
            
            {/* Generation Summary */}
            <Card>
              <CardHeader>
                <CardTitle>Generation Summary</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <p className="text-sm text-gray-600 mb-1">Template</p>
                    <p className="font-medium">{selectedTemplate?.name}</p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-600 mb-1">Dataset</p>
                    <p className="font-medium">{selectedDataset?.name}</p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-600 mb-1">Estimated Pages</p>
                    <p className="font-medium">{getEstimatedPages().toLocaleString()}</p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-600 mb-1">Output Format</p>
                    <p className="font-medium">{generationSettings.output_format.toUpperCase()}</p>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Page Preview */}
            {selectedTemplate && selectedDataset && (
              <PagePreview
                template={selectedTemplate}
                dataset={selectedDataset}
                settings={generationSettings}
              />
            )}

            {/* Generation Status */}
            {generationResult && (
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center">
                    {generationResult.status === 'completed' ? (
                      <CheckCircle className="w-5 h-5 text-green-600 mr-2" />
                    ) : generationResult.status === 'failed' ? (
                      <AlertCircle className="w-5 h-5 text-red-600 mr-2" />
                    ) : (
                      <div className="w-5 h-5 border-2 border-purple-600 border-t-transparent rounded-full animate-spin mr-2" />
                    )}
                    Generation Status
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    <Progress 
                      value={(generationResult.generated_pages / generationResult.total_pages) * 100}
                      className="w-full"
                    />
                    <div className="text-sm text-gray-600">
                      {generationResult.generated_pages} of {generationResult.total_pages} pages generated
                    </div>
                    {generationResult.errors && generationResult.errors.length > 0 && (
                      <div className="text-red-600 text-sm">
                        {generationResult.errors.join(', ')}
                      </div>
                    )}
                  </div>
                </CardContent>
              </Card>
            )}

            {/* Generate Button */}
            {!generationResult && (
              <Button 
                onClick={handleGenerate}
                className="w-full bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700"
                size="lg"
              >
                <Play className="w-5 h-5 mr-2" />
                Generate {getEstimatedPages().toLocaleString()} Pages
              </Button>
            )}
          </div>
        );

      default:
        return null;
    }
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center">
          <Settings className="w-5 h-5 mr-2" />
          Page Generation Wizard
        </CardTitle>
        <CardDescription>
          Configure and generate your bulk pages
        </CardDescription>
      </CardHeader>
      <CardContent>
        {/* Progress Steps */}
        <div className="mb-8">
          <div className="flex items-center justify-between mb-4">
            {steps.map((step, index) => (
              <div 
                key={step.id}
                className={`flex items-center ${
                  index < steps.length - 1 ? 'flex-1' : ''
                }`}
              >
                <div className={`
                  w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium
                  ${step.completed 
                    ? 'bg-green-500 text-white' 
                    : step.active 
                      ? 'bg-purple-500 text-white' 
                      : 'bg-gray-200 text-gray-600'
                  }
                `}>
                  {step.completed ? (
                    <CheckCircle className="w-4 h-4" />
                  ) : (
                    index + 1
                  )}
                </div>
                <div className="ml-3 flex-1">
                  <p className={`text-sm font-medium ${
                    step.active ? 'text-purple-600' : 'text-gray-600'
                  }`}>
                    {step.title}
                  </p>
                  <p className="text-xs text-gray-500">{step.description}</p>
                </div>
                {index < steps.length - 1 && (
                  <div className="w-12 h-0.5 bg-gray-200 ml-4" />
                )}
              </div>
            ))}
          </div>
        </div>

        {/* Step Content */}
        <div className="mb-8">
          {renderStepContent()}
        </div>

        {/* Navigation */}
        <div className="flex justify-between">
          <Button 
            variant="outline" 
            onClick={handlePrevious}
            disabled={currentStep === 0}
          >
            <ChevronLeft className="w-4 h-4 mr-2" />
            Previous
          </Button>
          
          <Button 
            onClick={handleNext}
            disabled={!canProceed() || currentStep === steps.length - 1}
          >
            Next
            <ChevronRight className="w-4 h-4 ml-2" />
          </Button>
        </div>
      </CardContent>
    </Card>
  );
}