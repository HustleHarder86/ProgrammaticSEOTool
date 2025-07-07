'use client';

import { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { RefreshCw, Globe, FileText, Hash } from 'lucide-react';

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

interface TemplatePreviewProps {
  template: Template;
}

// Sample data for preview
const SAMPLE_DATA: Record<string, string[]> = {
  city: ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix'],
  service: ['Plumbing', 'Electrical', 'HVAC', 'Landscaping', 'Cleaning'],
  feature: ['Fast Response', '24/7 Support', 'Licensed Pros', 'Free Quotes', 'Guaranteed Work'],
  industry: ['Healthcare', 'Technology', 'Retail', 'Finance', 'Manufacturing'],
  product: ['Laptops', 'Smartphones', 'Tablets', 'Smartwatches', 'Headphones'],
  benefit: ['Save Time', 'Reduce Costs', 'Increase Efficiency', 'Better Results', 'Peace of Mind'],
};

export function TemplatePreview({ template }: TemplatePreviewProps) {
  const [sampleValues, setSampleValues] = useState<Record<string, string>>(() => {
    const initial: Record<string, string> = {};
    template.variables.forEach(variable => {
      // Use example values if provided, otherwise use sample data
      if (template.example_values?.[variable]) {
        initial[variable] = template.example_values[variable];
      } else {
        // Try to match variable name to sample data
        const lowerVar = variable.toLowerCase();
        const matchingKey = Object.keys(SAMPLE_DATA).find(key => lowerVar.includes(key));
        if (matchingKey && SAMPLE_DATA[matchingKey].length > 0) {
          initial[variable] = SAMPLE_DATA[matchingKey][0];
        } else {
          initial[variable] = `[${variable}]`;
        }
      }
    });
    return initial;
  });

  const randomizeSamples = () => {
    const newValues: Record<string, string> = {};
    template.variables.forEach(variable => {
      const lowerVar = variable.toLowerCase();
      const matchingKey = Object.keys(SAMPLE_DATA).find(key => lowerVar.includes(key));
      if (matchingKey && SAMPLE_DATA[matchingKey].length > 0) {
        const randomIndex = Math.floor(Math.random() * SAMPLE_DATA[matchingKey].length);
        newValues[variable] = SAMPLE_DATA[matchingKey][randomIndex];
      } else {
        newValues[variable] = `[${variable}]`;
      }
    });
    setSampleValues(newValues);
  };

  const replaceVariables = (text: string): string => {
    let result = text;
    Object.entries(sampleValues).forEach(([variable, value]) => {
      const regex = new RegExp(`\\{${variable}\\}`, 'g');
      result = result.replace(regex, value);
    });
    return result;
  };

  const generateUrl = () => {
    const slug = replaceVariables(template.pattern)
      .toLowerCase()
      .replace(/[^a-z0-9]+/g, '-')
      .replace(/^-|-$/g, '');
    return `https://example.com/${slug}`;
  };

  return (
    <div className="space-y-6">
      {/* Sample Data Control */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center justify-between">
            <span>Preview with Sample Data</span>
            <Button
              size="sm"
              variant="outline"
              onClick={randomizeSamples}
            >
              <RefreshCw className="w-4 h-4 mr-2" />
              Randomize
            </Button>
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-2 gap-3">
            {Object.entries(sampleValues).map(([variable, value]) => (
              <div key={variable} className="text-sm">
                <span className="font-mono text-gray-600">{variable}:</span>
                <span className="ml-2 font-medium">{value}</span>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Browser Preview */}
      <Card>
        <CardHeader>
          <CardTitle>Browser Preview</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="border rounded-lg overflow-hidden">
            {/* Browser Bar */}
            <div className="bg-gray-100 px-4 py-2 flex items-center">
              <div className="flex space-x-2 mr-4">
                <div className="w-3 h-3 rounded-full bg-red-400"></div>
                <div className="w-3 h-3 rounded-full bg-yellow-400"></div>
                <div className="w-3 h-3 rounded-full bg-green-400"></div>
              </div>
              <div className="flex-1 bg-white rounded px-3 py-1 text-sm text-gray-600 font-mono">
                {generateUrl()}
              </div>
            </div>
            
            {/* Page Content */}
            <div className="bg-white p-6">
              {/* Title in tab */}
              <div className="mb-4 pb-2 border-b">
                <div className="flex items-center text-sm text-gray-600">
                  <Globe className="w-4 h-4 mr-2" />
                  <span className="font-medium">{replaceVariables(template.sections.title)}</span>
                </div>
              </div>
              
              {/* H1 */}
              <h1 className="text-3xl font-bold mb-4">
                {replaceVariables(template.sections.h1)}
              </h1>
              
              {/* Introduction */}
              <p className="text-gray-700 leading-relaxed">
                {replaceVariables(template.sections.intro)}
              </p>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* SEO Preview */}
      <Card>
        <CardHeader>
          <CardTitle>Search Engine Preview</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {/* Google Result Preview */}
            <div className="p-4 bg-gray-50 rounded-lg">
              <div className="text-sm text-gray-600 mb-1">{generateUrl()}</div>
              <h3 className="text-xl text-blue-600 hover:underline cursor-pointer mb-1">
                {replaceVariables(template.sections.title)}
              </h3>
              <p className="text-sm text-gray-700">
                {replaceVariables(template.sections.meta_description)}
              </p>
            </div>
            
            {/* Meta Tags */}
            <div className="mt-4">
              <h4 className="font-medium mb-2 flex items-center">
                <Hash className="w-4 h-4 mr-2" />
                Generated Meta Tags
              </h4>
              <pre className="bg-gray-900 text-gray-100 p-4 rounded-lg overflow-x-auto text-xs">
{`<title>${replaceVariables(template.sections.title)}</title>
<meta name="description" content="${replaceVariables(template.sections.meta_description)}" />
<meta property="og:title" content="${replaceVariables(template.sections.title)}" />
<meta property="og:description" content="${replaceVariables(template.sections.meta_description)}" />
<meta property="og:url" content="${generateUrl()}" />`}
              </pre>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Content Stats */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <FileText className="w-5 h-5 mr-2" />
            Content Analysis
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-2 gap-4 text-sm">
            <div>
              <span className="text-gray-600">Title Length:</span>
              <span className="ml-2 font-medium">{replaceVariables(template.sections.title).length} chars</span>
              {replaceVariables(template.sections.title).length > 60 && (
                <span className="ml-2 text-amber-600">(too long)</span>
              )}
            </div>
            <div>
              <span className="text-gray-600">Meta Description:</span>
              <span className="ml-2 font-medium">{replaceVariables(template.sections.meta_description).length} chars</span>
              {replaceVariables(template.sections.meta_description).length > 155 && (
                <span className="ml-2 text-amber-600">(too long)</span>
              )}
            </div>
            <div>
              <span className="text-gray-600">URL Length:</span>
              <span className="ml-2 font-medium">{generateUrl().length} chars</span>
            </div>
            <div>
              <span className="text-gray-600">H1 Length:</span>
              <span className="ml-2 font-medium">{replaceVariables(template.sections.h1).length} chars</span>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}