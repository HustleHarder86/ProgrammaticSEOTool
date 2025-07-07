'use client';

import { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Info, Sparkles, Variable } from 'lucide-react';

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

interface TemplateEditorProps {
  template: Template;
  onUpdate: (updates: Partial<Template>) => void;
}

export function TemplateEditor({ template, onUpdate }: TemplateEditorProps) {
  const [localTemplate, setLocalTemplate] = useState(template);

  useEffect(() => {
    setLocalTemplate(template);
  }, [template]);

  const extractVariables = (text: string): string[] => {
    const regex = /\{([^}]+)\}/g;
    const matches = text.matchAll(regex);
    const vars = new Set<string>();
    for (const match of matches) {
      vars.add(match[1].trim());
    }
    return Array.from(vars);
  };

  const updateSection = (section: keyof Template['sections'], value: string) => {
    const newSections = { ...localTemplate.sections, [section]: value };
    const allText = Object.values(newSections).join(' ') + ' ' + localTemplate.pattern;
    const variables = extractVariables(allText);
    
    const updates = {
      sections: newSections,
      variables
    };
    
    setLocalTemplate(prev => ({ ...prev, ...updates }));
    onUpdate(updates);
  };

  const updateBasicInfo = (field: 'name' | 'pattern', value: string) => {
    const updates = { [field]: value };
    
    if (field === 'pattern') {
      const allText = Object.values(localTemplate.sections).join(' ') + ' ' + value;
      const variables = extractVariables(allText);
      Object.assign(updates, { variables });
    }
    
    setLocalTemplate(prev => ({ ...prev, ...updates }));
    onUpdate(updates);
  };


  return (
    <div className="space-y-6">
      {/* Basic Information */}
      <Card>
        <CardHeader>
          <CardTitle>Template Information</CardTitle>
          <CardDescription>
            Define your template name and URL pattern
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-2">Template Name</label>
            <Input
              placeholder="e.g., Location-Based Services"
              value={localTemplate.name}
              onChange={(e) => updateBasicInfo('name', e.target.value)}
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium mb-2">URL Pattern</label>
            <Input
              placeholder="e.g., {service} in {city}"
              value={localTemplate.pattern}
              onChange={(e) => updateBasicInfo('pattern', e.target.value)}
            />
            <p className="text-sm text-gray-600 mt-1">
              Use {'{'}variable{'}'} syntax for dynamic content
            </p>
          </div>
        </CardContent>
      </Card>

      {/* SEO Sections */}
      <Card>
        <CardHeader>
          <CardTitle>SEO Content Sections</CardTitle>
          <CardDescription>
            Create templates for each page section using variables
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          {/* Title Tag */}
          <div>
            <label className="block text-sm font-medium mb-2">
              Title Tag
              <span className="text-gray-500 font-normal ml-2">(60 characters recommended)</span>
            </label>
            <Input
              placeholder="e.g., Best {service} in {city} - Professional {service} Services"
              value={localTemplate.sections.title}
              onChange={(e) => updateSection('title', e.target.value)}
              className="font-mono text-sm"
            />
            <div className="mt-1 flex justify-between text-sm">
              <span className="text-gray-600">
                {localTemplate.sections.title.length} characters
              </span>
              {localTemplate.sections.title.length > 60 && (
                <span className="text-amber-600">Too long</span>
              )}
            </div>
          </div>

          {/* Meta Description */}
          <div>
            <label className="block text-sm font-medium mb-2">
              Meta Description
              <span className="text-gray-500 font-normal ml-2">(155 characters recommended)</span>
            </label>
            <Textarea
              placeholder="e.g., Find the best {service} providers in {city}. Compare prices, read reviews, and book {service} services online."
              value={localTemplate.sections.meta_description}
              onChange={(e) => updateSection('meta_description', e.target.value)}
              className="font-mono text-sm min-h-[80px]"
            />
            <div className="mt-1 flex justify-between text-sm">
              <span className="text-gray-600">
                {localTemplate.sections.meta_description.length} characters
              </span>
              {localTemplate.sections.meta_description.length > 155 && (
                <span className="text-amber-600">Too long</span>
              )}
            </div>
          </div>

          {/* H1 Heading */}
          <div>
            <label className="block text-sm font-medium mb-2">
              H1 Heading
            </label>
            <Input
              placeholder="e.g., {service} Services in {city}"
              value={localTemplate.sections.h1}
              onChange={(e) => updateSection('h1', e.target.value)}
              className="font-mono text-sm"
            />
          </div>

          {/* Introduction Paragraph */}
          <div>
            <label className="block text-sm font-medium mb-2">
              Introduction Paragraph
            </label>
            <Textarea
              placeholder="e.g., Looking for reliable {service} in {city}? Our comprehensive guide helps you find trusted {service} providers in the {city} area..."
              value={localTemplate.sections.intro}
              onChange={(e) => updateSection('intro', e.target.value)}
              className="font-mono text-sm min-h-[120px]"
            />
          </div>
        </CardContent>
      </Card>

      {/* Tips */}
      <Card className="bg-purple-50 border-purple-200">
        <CardHeader>
          <CardTitle className="flex items-center text-purple-900">
            <Sparkles className="w-5 h-5 mr-2" />
            Template Tips
          </CardTitle>
        </CardHeader>
        <CardContent>
          <ul className="space-y-2 text-sm text-purple-800">
            <li className="flex items-start">
              <Variable className="w-4 h-4 mr-2 mt-0.5 flex-shrink-0" />
              <span>Use descriptive variable names like {'{city}'}, {'{service}'}, {'{feature}'}</span>
            </li>
            <li className="flex items-start">
              <Info className="w-4 h-4 mr-2 mt-0.5 flex-shrink-0" />
              <span>Keep variables consistent across all sections</span>
            </li>
            <li className="flex items-start">
              <Sparkles className="w-4 h-4 mr-2 mt-0.5 flex-shrink-0" />
              <span>Mix static content with variables for natural-sounding pages</span>
            </li>
          </ul>
        </CardContent>
      </Card>
    </div>
  );
}