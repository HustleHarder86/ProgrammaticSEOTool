'use client';

import { useState } from 'react';
import { ArrowLeft } from 'lucide-react';
import Link from 'next/link';
import { BusinessAnalysisForm } from '@/components/business/BusinessAnalysisForm';
import { LoadingAnimation } from '@/components/business/LoadingAnimation';
import { TemplateResults } from '@/components/business/TemplateResults';

type WizardStep = 'input' | 'loading' | 'results';

interface AnalysisData {
  businessInput: string;
  inputType: 'text' | 'url';
}

interface TemplateResult {
  template_name: string;
  template_pattern: string;
  example_pages: string[];
  estimated_pages: number;
  difficulty: string;
}

interface AnalysisResults {
  business_name: string;
  business_description: string;
  target_audience: string;
  core_offerings: string[];
  template_opportunities: TemplateResult[];
}

export default function NewProjectPage() {
  const [wizardStep, setWizardStep] = useState<WizardStep>('input');
  const [, setAnalysisData] = useState<AnalysisData | null>(null);
  const [analysisResults, setAnalysisResults] = useState<AnalysisResults | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleBusinessSubmit = async (data: AnalysisData) => {
    setAnalysisData(data);
    setWizardStep('loading');
    setError(null);

    try {
      // Call the API
      const response = await fetch('/api/analyze-business', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          business_input: data.businessInput,
          input_type: data.inputType,
        }),
      });

      if (!response.ok) {
        throw new Error(`API error: ${response.status}`);
      }

      const result = await response.json();
      setAnalysisResults(result);
      setWizardStep('results');
    } catch (err) {
      console.error('Analysis error:', err);
      setError('Failed to analyze business. Please try again.');
      setWizardStep('input');
    }
  };

  const handleSelectTemplate = (template: TemplateResult) => {
    // For now, just log the selected template
    console.log('Selected template:', template);
    // In a real implementation, this would move to the next step in the wizard
    alert('Template selected! Next steps: Data import and page generation.');
  };

  const handleBack = () => {
    setWizardStep('input');
    setAnalysisResults(null);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-4xl mx-auto px-4 py-8">
        {/* Header */}
        <div className="mb-8">
          <Link href="/" className="inline-flex items-center text-sm text-gray-600 hover:text-gray-900 mb-4">
            <ArrowLeft className="w-4 h-4 mr-1" />
            Back to Home
          </Link>
          <h1 className="text-3xl font-bold text-gray-900">Create New Project</h1>
          <p className="text-gray-600 mt-2">Generate programmatic SEO pages for your business</p>
        </div>

        {/* Progress Bar */}
        <div className="mb-8">
          <div className="flex items-center justify-between mb-2">
            <span className={`text-sm ${wizardStep !== 'input' ? 'text-blue-600 font-medium' : 'text-gray-900 font-medium'}`}>
              1. Analyze Business
            </span>
            <span className={`text-sm ${wizardStep === 'results' ? 'text-blue-600 font-medium' : 'text-gray-400'}`}>
              2. Select Templates
            </span>
            <span className={`text-sm text-gray-400`}>
              3. Import Data
            </span>
          </div>
          <div className="h-2 bg-gray-200 rounded-full overflow-hidden">
            <div 
              className="h-full bg-blue-600 transition-all duration-300"
              style={{ 
                width: wizardStep === 'input' ? '33%' : wizardStep === 'loading' ? '50%' : '66%' 
              }}
            />
          </div>
        </div>

        {/* Step Content */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-8">
          {wizardStep === 'input' && (
            <div>
              <h2 className="text-2xl font-semibold mb-6">Tell us about your business</h2>
              <p className="text-gray-600 mb-8">
                We&apos;ll analyze your business and suggest the best programmatic SEO templates.
              </p>
              
              {error && (
                <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg text-red-700">
                  {error}
                </div>
              )}
              
              <BusinessAnalysisForm 
                onSubmit={handleBusinessSubmit}
                isLoading={false}
              />
            </div>
          )}

          {wizardStep === 'loading' && (
            <LoadingAnimation />
          )}

          {wizardStep === 'results' && analysisResults && (
            <div>
              <h2 className="text-2xl font-semibold mb-6">Template Suggestions</h2>
              <p className="text-gray-600 mb-8">
                Based on your business analysis, here are our recommended programmatic SEO templates.
              </p>
              
              <TemplateResults
                results={analysisResults}
                onSelectTemplate={handleSelectTemplate}
                onBack={handleBack}
              />
            </div>
          )}
        </div>
      </div>
    </div>
  );
}