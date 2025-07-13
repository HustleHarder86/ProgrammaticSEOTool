"use client";

import React, { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Progress } from '@/components/ui/progress';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { GenerationResult, Template } from '@/types';
import { 
  ChevronLeft, 
  ChevronRight, 
  FileText, 
  Sparkles, 
  ListChecks,
  Play,
  CheckCircle,
  AlertCircle,
  Loader2
} from 'lucide-react';
import VariableGenerationForm from './VariableGenerationForm';
import TitlePreview from './TitlePreview';
import TitleSelector from './TitleSelector';
import { apiClient } from '@/lib/api/client';


interface AIGenerationWizardProps {
  projectId: string;
  templates: Template[];
  businessContext: Record<string, unknown>;
  onGenerationComplete: (result: GenerationResult) => void;
}

interface GeneratedVariablesData {
  variables: Record<string, string[]>;
  titles: string[];
  total_count: number;
  template_pattern: string;
  variable_types: Record<string, string>;
}

export default function AIGenerationWizard({
  projectId,
  templates,
  businessContext,
  onGenerationComplete
}: AIGenerationWizardProps) {
  const [currentStep, setCurrentStep] = useState(0);
  const [selectedTemplate, setSelectedTemplate] = useState<Template | null>(null);
  const [generatedVariables, setGeneratedVariables] = useState<GeneratedVariablesData | null>(null);
  const [selectedTitles, setSelectedTitles] = useState<string[]>([]);
  const [isGenerating, setIsGenerating] = useState(false);
  const [generationError, setGenerationError] = useState<string | null>(null);
  const [generationProgress, setGenerationProgress] = useState(0);

  const steps = [
    {
      id: 'template',
      title: 'Select Template',
      description: 'Choose the template pattern for your pages',
      icon: FileText,
      completed: !!selectedTemplate
    },
    {
      id: 'variables',
      title: 'Generate Variables',
      description: 'AI will generate relevant variables',
      icon: Sparkles,
      completed: !!generatedVariables
    },
    {
      id: 'selection',
      title: 'Select Pages',
      description: 'Choose which pages to generate',
      icon: ListChecks,
      completed: selectedTitles.length > 0
    },
    {
      id: 'generate',
      title: 'Generate Pages',
      description: 'Create your selected pages',
      icon: Play,
      completed: false
    }
  ];

  const canProceed = () => {
    switch (currentStep) {
      case 0: return !!selectedTemplate;
      case 1: return !!generatedVariables;
      case 2: return selectedTitles.length > 0;
      case 3: return true;
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

  const handleVariablesGenerated = (data: GeneratedVariablesData) => {
    setGeneratedVariables(data);
    setSelectedTitles(data.titles); // Select all by default
    handleNext();
  };

  const handleSelectionChange = (selected: string[]) => {
    setSelectedTitles(selected);
  };

  const handleQuickSelect = (type: string, value?: unknown) => {
    if (!generatedVariables) return;
    
    const allTitles = generatedVariables.titles;
    let newSelection: string[] = [];

    switch (type) {
      case 'first':
        newSelection = allTitles.slice(0, value as number);
        break;
      case 'random':
        const shuffled = [...allTitles].sort(() => Math.random() - 0.5);
        newSelection = shuffled.slice(0, value as number);
        break;
      case 'pattern':
        const patternValue = value as { variable?: string; values?: string[] };
        if (patternValue?.variable && patternValue?.values) {
          newSelection = allTitles.filter(title => 
            patternValue.values?.some((val: string) => title.includes(val)) || false
          );
        }
        break;
    }

    setSelectedTitles(newSelection);
  };

  const handleGeneratePages = async (titles: string[]) => {
    console.log('handleGeneratePages called with titles:', titles.length);
    console.log('selectedTemplate:', selectedTemplate);
    console.log('generatedVariables:', generatedVariables);
    
    if (!selectedTemplate || !generatedVariables) {
      console.error('Missing template or variables');
      return;
    }

    setIsGenerating(true);
    setGenerationError(null);
    setGenerationProgress(0);

    try {
      // Create variables data for only selected titles
      const selectedVariablesData: Record<string, string[]> = {};
      
      // Extract unique values from selected titles
      Object.keys(generatedVariables.variables).forEach(varName => {
        const uniqueValues = new Set<string>();
        titles.forEach(title => {
          generatedVariables.variables[varName].forEach(value => {
            if (title.includes(value)) {
              uniqueValues.add(value);
            }
          });
        });
        selectedVariablesData[varName] = Array.from(uniqueValues);
      });

      console.log('Calling generate endpoint with:', {
        url: `/api/projects/${projectId}/templates/${selectedTemplate.id}/generate`,
        batch_size: 100,
        selected_titles_count: titles.length,
        variables_data: selectedVariablesData
      });

      // Call the generate endpoint with selected data
      const response = await apiClient.post(
        `/api/projects/${projectId}/templates/${selectedTemplate.id}/generate`,
        {
          batch_size: 100,
          selected_titles: titles,
          variables_data: selectedVariablesData
        }
      );

      console.log('Generate response:', response.data);
      
      setGenerationProgress(100);
      onGenerationComplete({
        ...response.data,
        selected_count: titles.length,
        total_available: generatedVariables.total_count
      });

    } catch (error) {
      console.error('Generate pages error:', error);
      setGenerationError(error instanceof Error ? error.message : 'Failed to generate pages');
    } finally {
      setIsGenerating(false);
    }
  };

  const renderStepContent = () => {
    switch (currentStep) {
      case 0: // Template Selection
        return (
          <div className="space-y-4">
            <h3 className="text-lg font-semibold">Select Template Pattern</h3>
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
                          <CardDescription className="font-mono text-sm">
                            {template.pattern}
                          </CardDescription>
                        </div>
                      </div>
                      {selectedTemplate?.id === template.id && (
                        <CheckCircle className="w-5 h-5 text-purple-600" />
                      )}
                    </div>
                  </CardHeader>
                  <CardContent>
                    <div className="text-sm text-gray-600">
                      Variables: {template.variables.join(', ')}
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          </div>
        );

      case 1: // Variable Generation
        return selectedTemplate ? (
          <VariableGenerationForm
            templatePattern={selectedTemplate.pattern}
            projectId={projectId}
            templateId={selectedTemplate.id}
            businessContext={businessContext as {
              name: string;
              description: string;
              target_audience: string;
              industry?: string;
            }}
            onVariablesGenerated={handleVariablesGenerated}
          />
        ) : null;

      case 2: // Title Selection
        return generatedVariables ? (
          <div className="space-y-4">
            <TitleSelector
              variableData={generatedVariables.variables}
              selectedCount={selectedTitles.length}
              totalCount={generatedVariables.total_count}
              onQuickSelect={handleQuickSelect}
            />
            <TitlePreview
              titles={generatedVariables.titles}
              onSelectionChange={handleSelectionChange}
              onGeneratePages={async (titles) => {
                handleNext(); // Move to generation step first
                await handleGeneratePages(titles); // Then generate
              }}
            />
          </div>
        ) : null;

      case 3: // Generation Progress
        return (
          <div className="space-y-6">
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
                    <p className="text-sm text-gray-600 mb-1">Pages to Generate</p>
                    <p className="font-medium">{selectedTitles.length} pages</p>
                  </div>
                </div>
              </CardContent>
            </Card>

            {isGenerating && (
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center">
                    <Loader2 className="w-5 h-5 mr-2 animate-spin" />
                    Generating Pages...
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <Progress value={generationProgress} className="w-full" />
                  <p className="text-sm text-gray-600 mt-2">
                    Creating {selectedTitles.length} unique SEO-optimized pages...
                  </p>
                </CardContent>
              </Card>
            )}

            {generationError && (
              <Alert variant="destructive">
                <AlertCircle className="h-4 w-4" />
                <AlertDescription>{generationError}</AlertDescription>
              </Alert>
            )}

            {!isGenerating && !generationError && (
              <div className="text-center">
                <CheckCircle className="w-16 h-16 text-green-500 mx-auto mb-4" />
                <h3 className="text-xl font-semibold mb-2">Ready to Generate!</h3>
                <p className="text-gray-600">
                  Click &ldquo;Generate Pages&rdquo; in the previous step to create your {selectedTitles.length} pages.
                </p>
              </div>
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
          <Sparkles className="w-5 h-5 mr-2 text-purple-600" />
          AI-Powered Page Generation
        </CardTitle>
        <CardDescription>
          Generate pages automatically with AI-created variables
        </CardDescription>
      </CardHeader>
      <CardContent>
        {/* Progress Steps */}
        <div className="mb-8">
          <div className="flex items-center justify-between">
            {steps.map((step, index) => (
              <div 
                key={step.id}
                className={`flex items-center ${
                  index < steps.length - 1 ? 'flex-1' : ''
                }`}
              >
                <div className={`
                  w-10 h-10 rounded-full flex items-center justify-center
                  ${step.completed 
                    ? 'bg-green-500 text-white' 
                    : index === currentStep 
                      ? 'bg-purple-500 text-white' 
                      : 'bg-gray-200 text-gray-600'
                  }
                `}>
                  {step.completed ? (
                    <CheckCircle className="w-5 h-5" />
                  ) : (
                    <step.icon className="w-5 h-5" />
                  )}
                </div>
                <div className="ml-3 flex-1">
                  <p className={`text-sm font-medium ${
                    index === currentStep ? 'text-purple-600' : 'text-gray-600'
                  }`}>
                    {step.title}
                  </p>
                  <p className="text-xs text-gray-500 hidden md:block">
                    {step.description}
                  </p>
                </div>
                {index < steps.length - 1 && (
                  <div className={`h-0.5 flex-1 mx-4 ${
                    index < currentStep ? 'bg-green-500' : 'bg-gray-200'
                  }`} />
                )}
              </div>
            ))}
          </div>
        </div>

        {/* Step Content */}
        <div className="mb-8 min-h-[400px]">
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
          
          {currentStep < steps.length - 1 && (
            <Button 
              onClick={handleNext}
              disabled={!canProceed()}
            >
              Next
              <ChevronRight className="w-4 h-4 ml-2" />
            </Button>
          )}
        </div>
      </CardContent>
    </Card>
  );
}