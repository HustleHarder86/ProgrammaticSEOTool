'use client';

import { useState } from 'react';
import { ArrowLeft } from 'lucide-react';
import Link from 'next/link';
import { BusinessAnalysisForm } from '@/components/business/BusinessAnalysisForm';
import { LoadingAnimation } from '@/components/business/LoadingAnimation';
import { TemplateResults } from '@/components/business/TemplateResults';
import { apiClient } from '@/lib/api/client';

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
  project_id: string;
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
  const [loadingAction, setLoadingAction] = useState<'analyzing' | 'creating-template'>('analyzing');

  const handleBusinessSubmit = async (data: AnalysisData) => {
    setAnalysisData(data);
    setWizardStep('loading');
    setLoadingAction('analyzing');
    setError(null);

    try {
      // Call the API using apiClient
      const response = await apiClient.post('/api/analyze-business', {
        business_input: data.businessInput,
        input_type: data.inputType,
      });

      const result = response.data;
      setAnalysisResults(result);
      setWizardStep('results');
    } catch (err: unknown) {
      console.error('Analysis error:', err);
      const errorMessage = (err as Error)?.message || 'Failed to analyze business. Please try again.';
      setError(errorMessage);
      setWizardStep('input');
    }
  };

  const handleSelectTemplate = async (template: TemplateResult) => {
    if (!analysisResults?.project_id) {
      alert('Error: No project found');
      return;
    }

    try {
      setWizardStep('loading');
      setLoadingAction('creating-template');
      console.log('Creating template:', template);
      
      // Extract variables from template pattern (e.g., {Service} in {City} -> [Service, City])
      // const variables = template.template_pattern.match(/\{([^}]+)\}/g)?.map(v => v.slice(1, -1)) || [];
      
      // Create more dynamic content based on the template pattern
      const cleanPattern = template.template_pattern.toLowerCase().replace(/[{}]/g, '');
      
      // Create the template in the database
      const response = await apiClient.post(`/api/projects/${analysisResults.project_id}/templates`, {
        name: template.template_name,
        pattern: template.template_pattern,
        template_type: 'programmatic_seo',
        title_template: `${template.template_pattern} | ${analysisResults.business_name}`,
        meta_description_template: `Discover ${cleanPattern} with ${analysisResults.business_name}. Expert solutions and comprehensive guidance for your needs.`,
        h1_template: template.template_pattern,
        content_sections: [
          {
            heading: 'Overview',
            content: `Welcome to our comprehensive guide on ${cleanPattern}. At ${analysisResults.business_name}, we provide expert solutions tailored to your specific needs.`
          },
          {
            heading: 'Our Expertise', 
            content: `Our team specializes in delivering high-quality ${cleanPattern} services. With years of experience and proven results, we ensure exceptional outcomes for every client.`
          },
          {
            heading: 'Why Choose Us',
            content: `Choose ${analysisResults.business_name} for reliable, professional service. We offer competitive pricing, expert knowledge, and personalized solutions that deliver real results.`
          },
          {
            heading: 'Get Started',
            content: 'Ready to begin? Contact us today to discuss your specific requirements and discover how we can help you achieve your goals.'
          }
        ]
      });

      if (response.status === 200 || response.status === 201) {
        // Template created successfully, redirect to the project's generate page
        setTimeout(() => {
          window.location.href = `/projects/${analysisResults.project_id}/generate`;
        }, 1000);
      } else {
        throw new Error('Failed to create template');
      }
    } catch (error) {
      console.error('Error creating template:', error);
      setError('Failed to create template. Please try again.');
      setWizardStep('results');
    }
  };

  const handleBack = () => {
    setWizardStep('input');
    setAnalysisResults(null);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-white to-purple-50/30 overflow-hidden">
      {/* Background Effects */}
      <div className="fixed inset-0 -z-10">
        <div className="absolute top-20 -left-4 w-96 h-96 bg-purple-300 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob" />
        <div className="absolute top-40 -right-4 w-96 h-96 bg-blue-300 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob animation-delay-2000" />
        <div className="absolute -bottom-8 left-40 w-96 h-96 bg-pink-300 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob animation-delay-4000" />
      </div>
      
      <div className="relative max-w-4xl mx-auto px-4 py-8">
        {/* Header */}
        <div className="mb-12">
          <Link href="/" className="inline-flex items-center text-sm font-medium text-purple-600 hover:text-purple-700 mb-6 transition-colors duration-200 group">
            <ArrowLeft className="w-4 h-4 mr-1 group-hover:-translate-x-1 transition-transform duration-200" />
            Back to Home
          </Link>
          <h1 className="text-5xl font-black text-gray-900 tracking-tight mb-4">
            Create Your <span className="text-transparent bg-clip-text bg-gradient-to-r from-purple-600 to-blue-600">SEO Empire</span>
          </h1>
          <p className="text-xl text-gray-700 font-light">Let&apos;s analyze your business and discover programmatic SEO opportunities</p>
        </div>

        {/* Progress Bar */}
        <div className="mb-12">
          <div className="flex items-center justify-between mb-4">
            <div className={`flex items-center ${wizardStep !== 'input' ? 'text-purple-700' : 'text-gray-900'}`}>
              <div className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold transition-all duration-300 ${
                wizardStep !== 'input' 
                  ? 'bg-gradient-to-br from-purple-600 to-blue-600 text-white shadow-lg' 
                  : 'bg-gradient-to-br from-purple-100 to-blue-100 text-purple-700'
              }`}>
                1
              </div>
              <span className="ml-3 font-semibold">Analyze Business</span>
            </div>
            <div className={`flex items-center ${wizardStep === 'results' ? 'text-purple-700' : 'text-gray-400'}`}>
              <div className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold transition-all duration-300 ${
                wizardStep === 'results' 
                  ? 'bg-gradient-to-br from-purple-600 to-blue-600 text-white shadow-lg' 
                  : 'bg-gray-200 text-gray-500'
              }`}>
                2
              </div>
              <span className="ml-3 font-semibold">Select Templates</span>
            </div>
            <div className="flex items-center text-gray-400">
              <div className="w-8 h-8 rounded-full bg-gray-200 flex items-center justify-center text-sm font-bold text-gray-500">
                3
              </div>
              <span className="ml-3 font-semibold">Import Data</span>
            </div>
          </div>
          <div className="h-2 bg-gray-200 rounded-full overflow-hidden">
            <div 
              className="h-full bg-gradient-to-r from-purple-600 to-blue-600 transition-all duration-500 ease-out"
              style={{ 
                width: wizardStep === 'input' ? '33%' : wizardStep === 'loading' ? '50%' : '66%' 
              }}
            />
          </div>
        </div>

        {/* Step Content */}
        <div className="bg-white rounded-2xl shadow-xl border border-purple-100 overflow-hidden">
          {wizardStep === 'input' && (
            <div className="p-8 lg:p-12">
              <h2 className="text-3xl font-bold mb-4 text-gray-900">Tell us about your business</h2>
              <p className="text-lg text-gray-600 mb-10 font-light">
                We&apos;ll analyze your business and suggest the best programmatic SEO templates that can drive <span className="font-semibold text-purple-700">massive organic traffic</span>.
              </p>
              
              {error && (
                <div className="mb-8 p-4 bg-red-50 border border-red-200 rounded-xl text-red-700 flex items-start">
                  <svg className="w-5 h-5 mr-2 flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                  </svg>
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
            <div className="p-8 lg:p-12">
              {loadingAction === 'analyzing' ? (
                <LoadingAnimation />
              ) : (
                <LoadingAnimation 
                  message="Creating your template..." 
                  steps={[
                    'Processing template structure',
                    'Generating SEO-optimized content',
                    'Setting up variables and patterns'
                  ]}
                />
              )}
            </div>
          )}

          {wizardStep === 'results' && analysisResults && (
            <div className="p-8 lg:p-12">
              <h2 className="text-3xl font-bold mb-4 text-gray-900">
                Perfect! Here are your <span className="text-transparent bg-clip-text bg-gradient-to-r from-purple-600 to-blue-600">Template Opportunities</span>
              </h2>
              <p className="text-lg text-gray-600 mb-10 font-light">
                Based on your business analysis, we&apos;ve identified these high-impact programmatic SEO templates.
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