'use client';

import { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Variable, AlertCircle, CheckCircle, Hash } from 'lucide-react';

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

interface VariableManagerProps {
  template: Template;
  onUpdate: (updates: Partial<Template>) => void;
}

export function VariableManager({ template, onUpdate }: VariableManagerProps) {
  const [exampleValues, setExampleValues] = useState<Record<string, string>>(
    template.example_values || {}
  );

  const updateExampleValue = (variable: string, value: string) => {
    const newValues = { ...exampleValues, [variable]: value };
    setExampleValues(newValues);
    onUpdate({ example_values: newValues });
  };

  const getVariableUsage = (variable: string) => {
    const usage = [];
    const pattern = new RegExp(`\\{${variable}\\}`, 'g');
    
    if (template.pattern.match(pattern)) usage.push('URL Pattern');
    if (template.sections.title.match(pattern)) usage.push('Title');
    if (template.sections.meta_description.match(pattern)) usage.push('Meta Description');
    if (template.sections.h1.match(pattern)) usage.push('H1');
    if (template.sections.intro.match(pattern)) usage.push('Introduction');
    
    return usage;
  };

  const getVariableStatus = (variable: string) => {
    const usage = getVariableUsage(variable);
    if (usage.length === 0) return 'unused';
    if (usage.length === 1) return 'minimal';
    return 'good';
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'unused':
        return <AlertCircle className="w-4 h-4 text-amber-500" />;
      case 'minimal':
        return <Hash className="w-4 h-4 text-blue-500" />;
      case 'good':
        return <CheckCircle className="w-4 h-4 text-green-500" />;
      default:
        return null;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'unused':
        return 'bg-amber-50 border-amber-200';
      case 'minimal':
        return 'bg-blue-50 border-blue-200';
      case 'good':
        return 'bg-green-50 border-green-200';
      default:
        return '';
    }
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center">
          <Variable className="w-5 h-5 mr-2 text-purple-600" />
          Template Variables
        </CardTitle>
        <CardDescription>
          Variables found in your template
        </CardDescription>
      </CardHeader>
      <CardContent>
        {template.variables.length === 0 ? (
          <div className="text-center py-8">
            <Variable className="w-12 h-12 mx-auto text-gray-300 mb-3" />
            <p className="text-gray-500 text-sm">
              No variables found yet. Add {'{variables}'} to your template.
            </p>
          </div>
        ) : (
          <div className="space-y-4">
            {template.variables.map((variable) => {
              const usage = getVariableUsage(variable);
              const status = getVariableStatus(variable);
              
              return (
                <div 
                  key={variable}
                  className={`p-3 rounded-lg border ${getStatusColor(status)}`}
                >
                  <div className="flex items-start justify-between mb-2">
                    <div className="flex items-center">
                      {getStatusIcon(status)}
                      <span className="ml-2 font-mono text-sm font-semibold">
                        {'{' + variable + '}'}
                      </span>
                    </div>
                  </div>
                  
                  {usage.length > 0 ? (
                    <div className="text-xs text-gray-600 mb-2">
                      Used in: {usage.join(', ')}
                    </div>
                  ) : (
                    <div className="text-xs text-amber-600 mb-2">
                      Not used in template
                    </div>
                  )}
                  
                  <Input
                    placeholder={`Example value for ${variable}`}
                    value={exampleValues[variable] || ''}
                    onChange={(e) => updateExampleValue(variable, e.target.value)}
                    className="text-sm"
                  />
                </div>
              );
            })}
            
            {/* Variable Stats */}
            <div className="mt-4 pt-4 border-t">
              <div className="text-sm text-gray-600">
                <div className="flex items-center justify-between mb-1">
                  <span>Total Variables:</span>
                  <span className="font-semibold">{template.variables.length}</span>
                </div>
                <div className="flex items-center justify-between">
                  <span>Well-used Variables:</span>
                  <span className="font-semibold">
                    {template.variables.filter(v => getVariableStatus(v) === 'good').length}
                  </span>
                </div>
              </div>
            </div>

            {/* Tips */}
            <div className="mt-4 p-3 bg-gray-50 rounded-lg">
              <p className="text-xs text-gray-600">
                <strong>Tip:</strong> Variables should appear in multiple sections for better SEO variation.
              </p>
            </div>
          </div>
        )}
      </CardContent>
    </Card>
  );
}