"use client";

import React, { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '@/components/ui/card';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Loader2, Sparkles, AlertCircle } from 'lucide-react';

interface VariableGenerationFormProps {
  templatePattern: string;
  projectId: string;
  templateId: string;
  businessContext: {
    name: string;
    description: string;
    target_audience: string;
    industry?: string;
  };
  onVariablesGenerated: (data: any) => void;
}

export default function VariableGenerationForm({
  templatePattern,
  projectId,
  templateId,
  businessContext,
  onVariablesGenerated
}: VariableGenerationFormProps) {
  const [additionalContext, setAdditionalContext] = useState('');
  const [targetCount, setTargetCount] = useState(25);
  const [isGenerating, setIsGenerating] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleGenerate = async () => {
    setIsGenerating(true);
    setError(null);

    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/api/projects/${projectId}/templates/${templateId}/generate-variables`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            additional_context: additionalContext,
            target_count: targetCount
          }),
        }
      );

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to generate variables');
      }

      const data = await response.json();
      onVariablesGenerated(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An unexpected error occurred');
    } finally {
      setIsGenerating(false);
    }
  };

  // Extract variables from template pattern
  const variableMatches = templatePattern.match(/\{([^}]+)\}|\[([^\]]+)\]/g) || [];
  const variables = variableMatches.map(match => match.replace(/[\{\}\[\]]/g, ''));

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Sparkles className="h-5 w-5 text-blue-500" />
          Generate Variables with AI
        </CardTitle>
        <CardDescription>
          AI will generate relevant values for your template variables based on your business context
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        {/* Template Display */}
        <div className="bg-gray-50 p-4 rounded-lg">
          <p className="text-sm font-medium text-gray-700 mb-2">Template Pattern:</p>
          <p className="text-lg font-mono">{templatePattern}</p>
          <p className="text-sm text-gray-600 mt-2">
            Variables to generate: {variables.join(', ')}
          </p>
        </div>

        {/* Business Context Summary */}
        <div className="bg-blue-50 p-4 rounded-lg">
          <p className="text-sm font-medium text-blue-900 mb-2">Business Context:</p>
          <div className="text-sm text-blue-800 space-y-1">
            <p><strong>Business:</strong> {businessContext.name}</p>
            <p><strong>Description:</strong> {businessContext.description}</p>
            <p><strong>Target Audience:</strong> {businessContext.target_audience}</p>
            {businessContext.industry && (
              <p><strong>Industry:</strong> {businessContext.industry}</p>
            )}
          </div>
        </div>

        {/* Additional Context Input */}
        <div>
          <label htmlFor="additional-context" className="block text-sm font-medium mb-2">
            Additional Context (Optional)
          </label>
          <Textarea
            id="additional-context"
            placeholder="e.g., Focus on major cities only, Include only enterprise-level features, Target B2B audiences..."
            value={additionalContext}
            onChange={(e) => setAdditionalContext(e.target.value)}
            rows={3}
            className="w-full"
          />
          <p className="text-xs text-gray-500 mt-1">
            Provide any specific requirements or constraints for the AI to consider
          </p>
        </div>

        {/* Target Count */}
        <div>
          <label htmlFor="target-count" className="block text-sm font-medium mb-2">
            Number of Values to Generate
          </label>
          <input
            id="target-count"
            type="number"
            min="5"
            max="100"
            value={targetCount}
            onChange={(e) => setTargetCount(parseInt(e.target.value) || 25)}
            className="w-32 px-3 py-2 border rounded-md"
          />
          <p className="text-xs text-gray-500 mt-1">
            How many values to generate for each variable (5-100)
          </p>
        </div>

        {/* Error Display */}
        {error && (
          <Alert variant="destructive">
            <AlertCircle className="h-4 w-4" />
            <AlertDescription>{error}</AlertDescription>
          </Alert>
        )}

        {/* Generate Button */}
        <Button
          onClick={handleGenerate}
          disabled={isGenerating}
          className="w-full"
          size="lg"
        >
          {isGenerating ? (
            <>
              <Loader2 className="mr-2 h-4 w-4 animate-spin" />
              Generating Variables...
            </>
          ) : (
            <>
              <Sparkles className="mr-2 h-4 w-4" />
              Generate Variables
            </>
          )}
        </Button>

        <p className="text-xs text-center text-gray-500">
          AI will analyze your business and generate relevant values for each variable
        </p>
      </CardContent>
    </Card>
  );
}