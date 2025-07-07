'use client';

import { Button } from '@/components/ui/button';
import { CheckCircle2, FileText, MapPin, Users, TrendingUp } from 'lucide-react';

interface TemplateResult {
  template_name: string;
  template_pattern: string;
  example_pages: string[];
  estimated_pages: number;
  difficulty: string;
}

interface BusinessAnalysisResult {
  business_name: string;
  business_description: string;
  target_audience: string;
  core_offerings: string[];
  template_opportunities: TemplateResult[];
}

interface TemplateResultsProps {
  results: BusinessAnalysisResult;
  onSelectTemplate: (template: TemplateResult) => void;
  onBack: () => void;
}

export function TemplateResults({ results, onSelectTemplate, onBack }: TemplateResultsProps) {
  const getDifficultyColor = (difficulty: string) => {
    const level = difficulty.toLowerCase();
    if (level.includes('low') || level.includes('easy')) return 'text-green-600 bg-green-50';
    if (level.includes('medium') || level.includes('moderate')) return 'text-yellow-600 bg-yellow-50';
    return 'text-red-600 bg-red-50';
  };

  const getIcon = (templateName: string) => {
    const name = templateName.toLowerCase();
    if (name.includes('location') || name.includes('city') || name.includes('area')) return MapPin;
    if (name.includes('comparison') || name.includes('vs')) return TrendingUp;
    if (name.includes('industry') || name.includes('business') || name.includes('company')) return Users;
    return FileText;
  };

  return (
    <div className="space-y-6">
      {/* Business Summary */}
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-2">{results.business_name}</h3>
        <p className="text-gray-700">{results.business_description}</p>
        
        <div className="mt-4 space-y-3">
          <div>
            <p className="font-medium text-gray-900 mb-1">Target Audience:</p>
            <p className="text-sm text-gray-700">{results.target_audience}</p>
          </div>
          {results.core_offerings.length > 0 && (
            <div>
              <p className="font-medium text-gray-900 mb-2">Core Offerings:</p>
              <ul className="space-y-1">
                {results.core_offerings.map((offering, index) => (
                  <li key={index} className="flex items-start">
                    <CheckCircle2 className="w-4 h-4 text-green-600 mr-2 mt-0.5 flex-shrink-0" />
                    <span className="text-sm text-gray-700">{offering}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      </div>

      {/* Template Suggestions */}
      <div>
        <h3 className="text-xl font-semibold text-gray-900 mb-4">Recommended Templates</h3>
        <div className="space-y-4">
          {results.template_opportunities.map((template, index) => {
            const Icon = getIcon(template.template_name);
            
            return (
              <div
                key={index}
                className="border border-gray-200 rounded-lg p-6 hover:border-blue-300 transition-colors cursor-pointer"
                onClick={() => onSelectTemplate(template)}
              >
                <div className="flex items-start justify-between mb-4">
                  <div className="flex items-start">
                    <Icon className="w-6 h-6 text-blue-600 mr-3 mt-0.5" />
                    <div>
                      <h4 className="text-lg font-semibold text-gray-900">{template.template_name}</h4>
                      <p className="text-sm text-gray-600 mt-1">{template.template_pattern}</p>
                    </div>
                  </div>
                  <span className={`px-3 py-1 rounded-full text-xs font-medium ${getDifficultyColor(template.difficulty)}`}>
                    {template.difficulty}
                  </span>
                </div>

                {/* Template Pattern */}
                <div className="mb-3">
                  <p className="text-sm font-medium text-gray-700 mb-1">Template Pattern:</p>
                  <code className="text-xs bg-gray-100 px-2 py-1 rounded text-gray-700">
                    {template.template_pattern}
                  </code>
                </div>

                {/* Example Pages */}
                <div className="mb-3">
                  <p className="text-sm font-medium text-gray-700 mb-1">Example Pages:</p>
                  <ul className="text-sm text-gray-600 space-y-1">
                    {template.example_pages.slice(0, 3).map((example, i) => (
                      <li key={i} className="truncate">• {example}</li>
                    ))}
                  </ul>
                </div>

                {/* Potential */}
                <div className="flex items-center justify-between pt-3 border-t border-gray-100">
                  <span className="text-sm text-gray-600">
                    Estimated Pages: <span className="font-medium">{template.estimated_pages.toLocaleString()}</span>
                  </span>
                  <Button size="sm" variant="outline">
                    Select Template
                  </Button>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Action Buttons */}
      <div className="flex justify-between pt-6">
        <Button variant="outline" onClick={onBack}>
          Analyze Different Business
        </Button>
        <Button variant="ghost">
          Create Custom Template
        </Button>
      </div>
    </div>
  );
}