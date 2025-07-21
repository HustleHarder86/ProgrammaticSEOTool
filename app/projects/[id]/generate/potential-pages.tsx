'use client';

import { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Checkbox } from '@/components/ui/checkbox';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { apiClient } from '@/lib/api/client';
import { 
  CheckCircle, 
  AlertCircle, 
  Loader2,
  FileText,
  Hash,
  CheckSquare,
  Square
} from 'lucide-react';

interface PotentialPage {
  id: string;
  title: string;
  slug: string;
  variables: Record<string, any>;
  is_generated: boolean;
  priority: number;
  created_at: string;
}

interface PotentialPagesResponse {
  potential_pages: PotentialPage[];
  total_count: number;
  generated_count: number;
  remaining_count: number;
}

interface PotentialPagesProps {
  projectId: string;
  templateId: string;
  templateName: string;
  templatePattern: string;
  onBack: () => void;
  onComplete: (result: any) => void;
}

export default function PotentialPagesSelector({
  projectId,
  templateId,
  templateName,
  templatePattern,
  onBack,
  onComplete
}: PotentialPagesProps) {
  const [potentialPages, setPotentialPages] = useState<PotentialPage[]>([]);
  const [selectedIds, setSelectedIds] = useState<string[]>([]);
  const [loading, setLoading] = useState(true);
  const [generating, setGenerating] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [pageInfo, setPageInfo] = useState({
    total: 0,
    generated: 0,
    remaining: 0
  });

  // Load potential pages
  useEffect(() => {
    loadPotentialPages();
  }, [projectId, templateId]);

  const loadPotentialPages = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const response = await apiClient.get<PotentialPagesResponse>(
        `/api/projects/${projectId}/templates/${templateId}/potential-pages?limit=1000`
      );
      
      setPotentialPages(response.data.potential_pages);
      setPageInfo({
        total: response.data.total_count,
        generated: response.data.generated_count,
        remaining: response.data.remaining_count
      });
      
      // Pre-select first 10 ungeneraged pages
      const ungenerated = response.data.potential_pages
        .filter(p => !p.is_generated)
        .slice(0, 10)
        .map(p => p.id);
      setSelectedIds(ungenerated);
      
    } catch (err) {
      console.error('Failed to load potential pages:', err);
      setError(err instanceof Error ? err.message : 'Failed to load potential pages');
    } finally {
      setLoading(false);
    }
  };

  const handleSelectAll = () => {
    const allIds = potentialPages
      .filter(p => !p.is_generated)
      .map(p => p.id);
    setSelectedIds(allIds);
  };

  const handleSelectNone = () => {
    setSelectedIds([]);
  };

  const handleSelectFirst = (count: number) => {
    const firstIds = potentialPages
      .filter(p => !p.is_generated)
      .slice(0, count)
      .map(p => p.id);
    setSelectedIds(firstIds);
  };

  const handleTogglePage = (pageId: string) => {
    setSelectedIds(prev => 
      prev.includes(pageId) 
        ? prev.filter(id => id !== pageId)
        : [...prev, pageId]
    );
  };

  const handleGenerateSelected = async () => {
    if (selectedIds.length === 0) {
      setError('Please select at least one page to generate');
      return;
    }

    try {
      setGenerating(true);
      setError(null);
      
      const response = await apiClient.post(
        `/api/projects/${projectId}/templates/${templateId}/generate-selected-pages`,
        { page_ids: selectedIds }
      );
      
      onComplete({
        status: 'completed',
        generated_pages: response.data.successful_generations,
        total_pages: selectedIds.length,
        failed_pages: selectedIds.length - response.data.successful_generations,
        message: response.data.message
      });
      
    } catch (err) {
      console.error('Failed to generate pages:', err);
      setError(err instanceof Error ? err.message : 'Failed to generate pages');
    } finally {
      setGenerating(false);
    }
  };

  if (loading) {
    return (
      <Card>
        <CardContent className="flex items-center justify-center py-12">
          <Loader2 className="w-8 h-8 animate-spin text-purple-600" />
        </CardContent>
      </Card>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <FileText className="w-5 h-5 mr-2 text-purple-600" />
            Select Pages to Generate
          </CardTitle>
          <CardDescription>
            Template: {templateName} • Pattern: <code>{templatePattern}</code>
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="text-center p-4 bg-gray-50 rounded-lg">
              <div className="text-2xl font-bold text-gray-900">{pageInfo.total}</div>
              <div className="text-sm text-gray-600">Total Possible Pages</div>
            </div>
            <div className="text-center p-4 bg-green-50 rounded-lg">
              <div className="text-2xl font-bold text-green-600">{pageInfo.generated}</div>
              <div className="text-sm text-gray-600">Already Generated</div>
            </div>
            <div className="text-center p-4 bg-purple-50 rounded-lg">
              <div className="text-2xl font-bold text-purple-600">{pageInfo.remaining}</div>
              <div className="text-sm text-gray-600">Available to Generate</div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Selection Controls */}
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <div>
              <CardTitle className="text-lg">Quick Selection</CardTitle>
              <CardDescription>
                {selectedIds.length} pages selected for generation
              </CardDescription>
            </div>
            <div className="flex gap-2">
              <Button 
                variant="outline" 
                size="sm"
                onClick={handleSelectAll}
                disabled={generating}
              >
                Select All
              </Button>
              <Button 
                variant="outline" 
                size="sm"
                onClick={handleSelectNone}
                disabled={generating}
              >
                Select None
              </Button>
              <Button 
                variant="outline" 
                size="sm"
                onClick={() => handleSelectFirst(10)}
                disabled={generating}
              >
                First 10
              </Button>
              <Button 
                variant="outline" 
                size="sm"
                onClick={() => handleSelectFirst(25)}
                disabled={generating}
              >
                First 25
              </Button>
              <Button 
                variant="outline" 
                size="sm"
                onClick={() => handleSelectFirst(50)}
                disabled={generating}
              >
                First 50
              </Button>
            </div>
          </div>
        </CardHeader>
      </Card>

      {/* Error Alert */}
      {error && (
        <Alert variant="destructive">
          <AlertCircle className="h-4 w-4" />
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      {/* Page List */}
      <Card>
        <CardHeader>
          <CardTitle className="text-lg">Available Pages</CardTitle>
          <CardDescription>
            Select the pages you want to generate. Each page will have unique AI-generated content.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="max-h-[400px] overflow-y-auto space-y-2 pr-2">
            {potentialPages.map((page) => (
              <div 
                key={page.id}
                className={`flex items-center space-x-3 p-3 rounded-lg hover:bg-gray-50 ${
                  page.is_generated ? 'opacity-50' : ''
                }`}
              >
                <Checkbox
                  id={page.id}
                  checked={selectedIds.includes(page.id)}
                  onCheckedChange={() => handleTogglePage(page.id)}
                  disabled={page.is_generated || generating}
                />
                <label 
                  htmlFor={page.id}
                  className="flex-1 cursor-pointer flex items-center justify-between"
                >
                  <span className={page.is_generated ? 'line-through text-gray-500' : ''}>
                    {page.title}
                  </span>
                  {page.is_generated && (
                    <span className="text-xs text-green-600 flex items-center">
                      <CheckCircle className="w-3 h-3 mr-1" />
                      Generated
                    </span>
                  )}
                </label>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Action Buttons */}
      <div className="flex justify-between">
        <Button 
          variant="outline" 
          onClick={onBack}
          disabled={generating}
        >
          Back to Templates
        </Button>
        
        <Button 
          onClick={handleGenerateSelected}
          disabled={selectedIds.length === 0 || generating}
          className="bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700"
        >
          {generating ? (
            <>
              <Loader2 className="w-4 h-4 mr-2 animate-spin" />
              Generating {selectedIds.length} Pages...
            </>
          ) : (
            <>
              <CheckSquare className="w-4 h-4 mr-2" />
              Generate {selectedIds.length} Selected Pages
            </>
          )}
        </Button>
      </div>
    </div>
  );
}