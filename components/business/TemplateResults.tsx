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
    if (level.includes('low') || level.includes('easy')) return 'text-green-700 bg-green-50 border-green-200';
    if (level.includes('medium') || level.includes('moderate')) return 'text-yellow-700 bg-yellow-50 border-yellow-200';
    return 'text-red-700 bg-red-50 border-red-200';
  };

  const getIcon = (templateName: string) => {
    const name = templateName.toLowerCase();
    if (name.includes('location') || name.includes('city') || name.includes('area')) return MapPin;
    if (name.includes('comparison') || name.includes('vs')) return TrendingUp;
    if (name.includes('industry') || name.includes('business') || name.includes('company')) return Users;
    return FileText;
  };

  return (
    <div className="space-y-8">
      {/* Business Summary */}
      <div className="bg-gradient-to-br from-purple-50 to-blue-50 border border-purple-200 rounded-xl p-8 shadow-sm">
        <h3 className="text-xl font-bold text-gray-900 mb-3">{results.business_name}</h3>
        <p className="text-gray-700 text-base leading-relaxed">{results.business_description}</p>
        
        <div className="mt-6 space-y-4">
          <div>
            <p className="font-semibold text-purple-700 mb-2 text-sm uppercase tracking-wider">Target Audience:</p>
            <p className="text-gray-700">{results.target_audience}</p>
          </div>
          {results.core_offerings.length > 0 && (
            <div>
              <p className="font-semibold text-purple-700 mb-3 text-sm uppercase tracking-wider">Core Offerings:</p>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                {results.core_offerings.map((offering, index) => (
                  <div key={index} className="flex items-start">
                    <CheckCircle2 className="w-5 h-5 text-purple-600 mr-2 mt-0.5 flex-shrink-0" />
                    <span className="text-gray-700">{offering}</span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Template Suggestions */}
      <div>
        <h3 className="text-2xl font-bold text-gray-900 mb-6">Recommended Templates</h3>
        <div className="grid gap-6">
          {results.template_opportunities.map((template, index) => {
            const Icon = getIcon(template.template_name);
            
            return (
              <div
                key={index}
                className="group border-2 border-gray-200 rounded-xl p-8 hover:border-purple-300 hover:shadow-xl transition-all duration-300 cursor-pointer bg-white hover:bg-gradient-to-br hover:from-purple-50/30 hover:to-blue-50/30"
                onClick={() => onSelectTemplate(template)}
              >
                <div className="flex items-start justify-between mb-6">
                  <div className="flex items-start">
                    <div className="w-14 h-14 rounded-xl bg-gradient-to-br from-purple-100 to-blue-100 flex items-center justify-center mr-4 group-hover:scale-110 transition-transform duration-300">
                      <Icon className="w-7 h-7 text-purple-700" />
                    </div>
                    <div className="flex-1">
                      <h4 className="text-xl font-bold text-gray-900 mb-2">{template.template_name}</h4>
                      <p className="text-gray-600">{template.template_pattern}</p>
                    </div>
                  </div>
                  <span className={`px-4 py-2 rounded-full text-sm font-semibold border ${getDifficultyColor(template.difficulty)}`}>
                    {template.difficulty}
                  </span>
                </div>

                {/* Template Pattern */}
                <div className="mb-4 bg-gradient-to-r from-purple-50 to-blue-50 p-4 rounded-lg border border-purple-100">
                  <p className="text-sm font-semibold text-purple-700 mb-2 uppercase tracking-wider">Template Pattern:</p>
                  <code className="text-sm font-mono text-purple-900 bg-white px-3 py-2 rounded border border-purple-200 block">
                    {template.template_pattern}
                  </code>
                </div>

                {/* Example Pages */}
                <div className="mb-6">
                  <p className="text-sm font-semibold text-gray-700 mb-3 uppercase tracking-wider">Example Pages:</p>
                  <ul className="space-y-2">
                    {template.example_pages.slice(0, 3).map((example, i) => (
                      <li key={i} className="flex items-start">
                        <span className="text-purple-600 mr-2">→</span>
                        <span className="text-gray-700">{example}</span>
                      </li>
                    ))}
                  </ul>
                </div>

                {/* Potential */}
                <div className="flex items-center justify-between pt-6 border-t border-gray-200">
                  <div className="flex items-center">
                    <div className="bg-gradient-to-br from-purple-100 to-blue-100 px-4 py-2 rounded-lg mr-4">
                      <span className="text-sm font-semibold text-purple-700">
                        {template.estimated_pages.toLocaleString()} pages
                      </span>
                    </div>
                    <span className="text-sm text-gray-600">estimated potential</span>
                  </div>
                  <Button 
                    size="sm" 
                    className="bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 text-white border-0 shadow-md hover:shadow-lg transition-all duration-300 hover:scale-105"
                  >
                    Select Template →
                  </Button>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Action Buttons */}
      <div className="flex flex-col sm:flex-row justify-between gap-4 pt-8">
        <Button 
          variant="outline" 
          onClick={onBack}
          className="border-2 border-purple-200 hover:border-purple-400 hover:bg-purple-50/50 transition-all duration-300 font-semibold"
        >
          ← Analyze Different Business
        </Button>
        <Button 
          variant="ghost"
          className="text-purple-700 hover:text-purple-800 hover:bg-purple-50 font-semibold"
        >
          Create Custom Template
        </Button>
      </div>
    </div>
  );
}