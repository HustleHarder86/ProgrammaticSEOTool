'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { apiClient } from '@/lib/api/client';
import { TemplateResults } from '@/components/business/TemplateResults';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Globe, FileText, Loader2, Sparkles } from 'lucide-react';

interface BusinessAnalysisResponse {
  project_id: string;
  business_name: string;
  business_description: string;
  target_audience: string;
  core_offerings: string[];
  template_opportunities: Array<{
    template_name: string;
    template_pattern: string;
    example_pages: string[];
    estimated_pages: number;
    difficulty: string;
  }>;
}

export default function AnalyzePage() {
  const router = useRouter();
  const [inputType, setInputType] = useState<'text' | 'url'>('text');
  const [businessInput, setBusinessInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [analysisResult, setAnalysisResult] = useState<BusinessAnalysisResponse | null>(null);

  const handleAnalyze = async () => {
    if (!businessInput.trim()) {
      setError('Please enter a business description or URL');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const response = await apiClient.post<BusinessAnalysisResponse>('/api/analyze-business', {
        business_input: businessInput,
        input_type: inputType
      });
      
      setAnalysisResult(response.data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to analyze business');
    } finally {
      setLoading(false);
    }
  };

  const handleSelectTemplate = (template: { template_name: string }) => {
    if (analysisResult?.project_id) {
      // Navigate to project page with selected template
      router.push(`/projects/${analysisResult.project_id}?template=${encodeURIComponent(template.template_name)}`);
    }
  };

  const handleBack = () => {
    setAnalysisResult(null);
    setBusinessInput('');
  };

  if (analysisResult) {
    return (
      <div className="container mx-auto px-4 py-8 max-w-6xl">
        <TemplateResults 
          results={analysisResult}
          onSelectTemplate={handleSelectTemplate}
          onBack={handleBack}
        />
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8 max-w-4xl">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-3">Analyze Your Business</h1>
        <p className="text-lg text-gray-600">
          Get personalized programmatic SEO template suggestions based on your business
        </p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Business Information</CardTitle>
          <CardDescription>
            Enter your business URL or describe your business to get started
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          {/* Input Type Selection */}
          <div className="flex gap-4 mb-4">
            <Button
              type="button"
              variant={inputType === 'url' ? 'default' : 'outline'}
              size="sm"
              onClick={() => setInputType('url')}
              className={inputType === 'url' ? 'bg-purple-600 hover:bg-purple-700' : ''}
            >
              <Globe className="w-4 h-4 mr-2" />
              Website URL
            </Button>
            <Button
              type="button"
              variant={inputType === 'text' ? 'default' : 'outline'}
              size="sm"
              onClick={() => setInputType('text')}
              className={inputType === 'text' ? 'bg-purple-600 hover:bg-purple-700' : ''}
            >
              <FileText className="w-4 h-4 mr-2" />
              Text Description
            </Button>
          </div>

          {/* Input Field */}
          {inputType === 'url' ? (
            <div className="space-y-2">
              <label className="text-sm font-medium text-gray-700">Website URL</label>
              <Input
                type="url"
                placeholder="https://example.com"
                value={businessInput}
                onChange={(e) => setBusinessInput(e.target.value)}
                className="w-full"
              />
              <p className="text-sm text-gray-500">
                We&apos;ll analyze your website to understand your business and suggest templates
              </p>
            </div>
          ) : (
            <div className="space-y-2">
              <label className="text-sm font-medium text-gray-700">Business Description</label>
              <Textarea
                placeholder="Describe your business... (e.g., 'We're a digital marketing agency specializing in SEO and content marketing for SaaS companies')"
                value={businessInput}
                onChange={(e) => setBusinessInput(e.target.value)}
                rows={4}
                className="w-full"
              />
              <p className="text-sm text-gray-500">
                Be specific about your products, services, and target audience
              </p>
            </div>
          )}

          {/* Error Message */}
          {error && (
            <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
              {error}
            </div>
          )}

          {/* Analyze Button */}
          <Button
            onClick={handleAnalyze}
            disabled={loading || !businessInput.trim()}
            className="w-full bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700"
            size="lg"
          >
            {loading ? (
              <>
                <Loader2 className="w-5 h-5 mr-2 animate-spin" />
                Analyzing...
              </>
            ) : (
              <>
                <Sparkles className="w-5 h-5 mr-2" />
                Analyze Business
              </>
            )}
          </Button>
        </CardContent>
      </Card>

      {/* Examples */}
      <div className="mt-8 bg-purple-50 rounded-xl p-6 border border-purple-200">
        <h3 className="font-semibold text-purple-900 mb-3">Example Businesses:</h3>
        <div className="grid gap-3 text-sm">
          <button
            onClick={() => {
              setInputType('text');
              setBusinessInput('Digital marketing agency specializing in SEO and PPC for e-commerce brands');
            }}
            className="text-left p-3 bg-white rounded-lg border border-purple-200 hover:border-purple-400 transition-colors"
          >
            <strong>Marketing Agency:</strong> &quot;Digital marketing agency specializing in SEO and PPC for e-commerce brands&quot;
          </button>
          <button
            onClick={() => {
              setInputType('text');
              setBusinessInput('SaaS project management tool for remote teams with features like task tracking, time tracking, and team collaboration');
            }}
            className="text-left p-3 bg-white rounded-lg border border-purple-200 hover:border-purple-400 transition-colors"
          >
            <strong>SaaS Tool:</strong> &quot;Project management tool for remote teams with task tracking and collaboration&quot;
          </button>
          <button
            onClick={() => {
              setInputType('text');
              setBusinessInput('Online fitness coaching platform offering personalized workout plans and nutrition guidance');
            }}
            className="text-left p-3 bg-white rounded-lg border border-purple-200 hover:border-purple-400 transition-colors"
          >
            <strong>Fitness Platform:</strong> &quot;Online fitness coaching with personalized workout plans and nutrition guidance&quot;
          </button>
        </div>
      </div>
    </div>
  );
}