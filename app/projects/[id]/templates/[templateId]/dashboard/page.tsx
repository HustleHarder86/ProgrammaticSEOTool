'use client';

import { useState, useEffect, useCallback } from 'react';
import { useParams, useRouter } from 'next/navigation';
import Link from 'next/link';
import { apiClient } from '@/lib/api/client';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Progress } from '@/components/ui/progress';
import { Badge } from '@/components/ui/badge';
import { Checkbox } from '@/components/ui/checkbox';
import { Input } from '@/components/ui/input';
import { 
  ArrowLeft, Sparkles, Filter, Download, Eye, 
  CheckCircle, Clock, TrendingUp, LayoutGrid,
  Search, RefreshCw
} from 'lucide-react';

interface TemplateDashboard {
  template_id: string;
  template_name: string;
  template_pattern: string;
  total_combinations: number;
  generated_count: number;
  remaining_count: number;
  completion_percentage: number;
  variables: Record<string, string[]>;
  recent_generations: Array<{
    id: string;
    title: string;
    generated_at: string;
  }>;
  generation_sessions: Array<{
    date: string;
    count: number;
  }>;
}

interface PotentialPage {
  id: string;
  title: string;
  slug: string;
  variables: Record<string, string>;
  is_generated: boolean;
  generated_at?: string;
  priority: number;
}

export default function TemplateDashboardPage() {
  const params = useParams();
  const router = useRouter();
  const projectId = params?.id as string;
  const templateId = params?.templateId as string;

  const [dashboard, setDashboard] = useState<TemplateDashboard | null>(null);
  const [potentialPages, setPotentialPages] = useState<PotentialPage[]>([]);
  const [selectedPages, setSelectedPages] = useState<Set<string>>(new Set());
  const [loading, setLoading] = useState(true);
  const [generating, setGenerating] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterGenerated, setFilterGenerated] = useState<'all' | 'generated' | 'remaining'>('remaining');
  const [batchSize, setBatchSize] = useState(50);

  const loadDashboard = useCallback(async () => {
    try {
      setLoading(true);
      
      // Load dashboard data
      const dashboardRes = await apiClient.get<TemplateDashboard>(
        `/api/projects/${projectId}/templates/${templateId}/dashboard`
      );
      setDashboard(dashboardRes.data);

      // Load potential pages
      const pagesRes = await apiClient.get<{ pages: PotentialPage[] }>(
        `/api/projects/${projectId}/templates/${templateId}/potential-pages?limit=1000`
      );
      setPotentialPages(pagesRes.data.pages);
    } catch (err) {
      console.error('Failed to load dashboard:', err);
    } finally {
      setLoading(false);
    }
  }, [projectId, templateId]);

  useEffect(() => {
    if (projectId && templateId) {
      loadDashboard();
    }
  }, [projectId, templateId, loadDashboard]);

  const handleSelectAll = () => {
    const filteredPages = getFilteredPages();
    if (selectedPages.size === filteredPages.length) {
      setSelectedPages(new Set());
    } else {
      setSelectedPages(new Set(filteredPages.map(p => p.id)));
    }
  };

  const handleSelectBatch = (count: number) => {
    const available = getFilteredPages().filter(p => !p.is_generated);
    const toSelect = available.slice(0, count);
    setSelectedPages(new Set(toSelect.map(p => p.id)));
  };

  const handleGenerate = async () => {
    if (selectedPages.size === 0) return;

    try {
      setGenerating(true);
      
      const selectedTitles = Array.from(selectedPages).map(id => {
        const page = potentialPages.find(p => p.id === id);
        return page?.title;
      }).filter(Boolean);

      const response = await apiClient.post(
        `/api/projects/${projectId}/templates/${templateId}/generate`,
        { selected_page_titles: selectedTitles }
      );

      if (response.data.pages_generated > 0) {
        // Refresh dashboard
        await loadDashboard();
        setSelectedPages(new Set());
        
        // Navigate to pages view
        router.push(`/projects/${projectId}/pages?template=${templateId}`);
      }
    } catch (err) {
      console.error('Failed to generate pages:', err);
    } finally {
      setGenerating(false);
    }
  };

  const getFilteredPages = () => {
    let filtered = potentialPages;

    // Filter by generation status
    if (filterGenerated === 'generated') {
      filtered = filtered.filter(p => p.is_generated);
    } else if (filterGenerated === 'remaining') {
      filtered = filtered.filter(p => !p.is_generated);
    }

    // Filter by search term
    if (searchTerm) {
      filtered = filtered.filter(p => 
        p.title.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }

    return filtered;
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-600"></div>
      </div>
    );
  }

  const filteredPages = getFilteredPages();
  const remainingPages = potentialPages.filter(p => !p.is_generated);

  return (
    <div className="container mx-auto px-4 py-8 max-w-7xl">
      {/* Header */}
      <div className="mb-8">
        <Link href={`/projects/${projectId}`}>
          <Button variant="ghost" className="mb-4">
            <ArrowLeft className="w-4 h-4 mr-2" />
            Back to Project
          </Button>
        </Link>
        
        <div className="flex items-start justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900 mb-2">
              Template Dashboard
            </h1>
            <p className="text-lg text-gray-600">
              {dashboard?.template_name}
            </p>
            <code className="text-sm bg-gray-100 px-2 py-1 rounded mt-2 inline-block">
              {dashboard?.template_pattern}
            </code>
          </div>
          <Button
            onClick={() => loadDashboard()}
            variant="outline"
            disabled={loading}
          >
            <RefreshCw className="w-4 h-4 mr-2" />
            Refresh
          </Button>
        </div>
      </div>

      {/* Overview Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
        <Card>
          <CardHeader className="pb-2">
            <CardDescription>Total Combinations</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{dashboard?.total_combinations.toLocaleString()}</div>
            <p className="text-sm text-gray-600 mt-1">Possible pages</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-2">
            <CardDescription>Generated</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-green-600">
              {dashboard?.generated_count.toLocaleString()}
            </div>
            <Progress 
              value={dashboard?.completion_percentage || 0} 
              className="mt-2 h-2"
            />
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-2">
            <CardDescription>Remaining</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-blue-600">
              {dashboard?.remaining_count.toLocaleString()}
            </div>
            <p className="text-sm text-gray-600 mt-1">Ready to generate</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-2">
            <CardDescription>Completion</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {Math.round(dashboard?.completion_percentage || 0)}%
            </div>
            <div className="flex items-center gap-2 mt-2">
              {(dashboard?.completion_percentage || 0) === 100 ? (
                <CheckCircle className="w-4 h-4 text-green-600" />
              ) : (
                <Clock className="w-4 h-4 text-blue-600" />
              )}
              <span className="text-sm text-gray-600">
                {(dashboard?.completion_percentage || 0) === 100 ? 'Complete' : 'In Progress'}
              </span>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Generation Controls */}
      <Card className="mb-8">
        <CardHeader>
          <CardTitle>Batch Generation</CardTitle>
          <CardDescription>
            Select pages to generate. Each session creates unique content.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {/* Quick select buttons */}
            <div className="flex flex-wrap gap-2">
              <Button
                variant="outline"
                size="sm"
                onClick={() => handleSelectBatch(25)}
                disabled={remainingPages.length === 0}
              >
                Select 25
              </Button>
              <Button
                variant="outline"
                size="sm"
                onClick={() => handleSelectBatch(50)}
                disabled={remainingPages.length === 0}
              >
                Select 50
              </Button>
              <Button
                variant="outline"
                size="sm"
                onClick={() => handleSelectBatch(100)}
                disabled={remainingPages.length === 0}
              >
                Select 100
              </Button>
              <div className="flex items-center gap-2 ml-auto">
                <Input
                  type="number"
                  value={batchSize}
                  onChange={(e) => setBatchSize(parseInt(e.target.value) || 50)}
                  className="w-20"
                  min={1}
                  max={remainingPages.length}
                />
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => handleSelectBatch(batchSize)}
                  disabled={remainingPages.length === 0}
                >
                  Select Custom
                </Button>
              </div>
            </div>

            {/* Generate button */}
            <div className="flex items-center justify-between pt-4 border-t">
              <div>
                <p className="text-sm text-gray-600">
                  {selectedPages.size} pages selected
                </p>
                {selectedPages.size > 0 && (
                  <p className="text-xs text-gray-500 mt-1">
                    Estimated time: ~{Math.ceil(selectedPages.size * 2)} seconds
                  </p>
                )}
              </div>
              <Button
                onClick={handleGenerate}
                disabled={selectedPages.size === 0 || generating}
                className="bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700"
              >
                {generating ? (
                  <>Generating...</>
                ) : (
                  <>
                    <Sparkles className="w-4 h-4 mr-2" />
                    Generate {selectedPages.size} Pages
                  </>
                )}
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Pages List */}
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <div>
              <CardTitle>All Potential Pages</CardTitle>
              <CardDescription>
                {filteredPages.length} pages shown
              </CardDescription>
            </div>
            <div className="flex items-center gap-4">
              {/* Search */}
              <div className="relative">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
                <Input
                  placeholder="Search pages..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="pl-10 w-64"
                />
              </div>
              
              {/* Filter */}
              <select
                value={filterGenerated}
                onChange={(e) => setFilterGenerated(e.target.value as any)}
                className="px-3 py-2 border rounded-lg"
              >
                <option value="all">All Pages</option>
                <option value="generated">Generated Only</option>
                <option value="remaining">Remaining Only</option>
              </select>
              
              {/* Select all */}
              <Button
                variant="outline"
                size="sm"
                onClick={handleSelectAll}
              >
                {selectedPages.size === filteredPages.length ? 'Deselect All' : 'Select All'}
              </Button>
            </div>
          </div>
        </CardHeader>
        <CardContent>
          <div className="space-y-2 max-h-96 overflow-y-auto">
            {filteredPages.map((page) => (
              <div
                key={page.id}
                className={`flex items-center justify-between p-3 rounded-lg border ${
                  page.is_generated ? 'bg-gray-50 border-gray-200' : 'hover:bg-gray-50 border-gray-200'
                }`}
              >
                <div className="flex items-center gap-3">
                  <Checkbox
                    checked={selectedPages.has(page.id)}
                    onCheckedChange={(checked) => {
                      const newSelected = new Set(selectedPages);
                      if (checked) {
                        newSelected.add(page.id);
                      } else {
                        newSelected.delete(page.id);
                      }
                      setSelectedPages(newSelected);
                    }}
                    disabled={page.is_generated}
                  />
                  <div>
                    <p className={`font-medium ${page.is_generated ? 'text-gray-500' : 'text-gray-900'}`}>
                      {page.title}
                    </p>
                    <p className="text-sm text-gray-500">/{page.slug}</p>
                  </div>
                </div>
                <div className="flex items-center gap-2">
                  {page.is_generated ? (
                    <>
                      <Badge variant="secondary" className="bg-green-100 text-green-800">
                        Generated
                      </Badge>
                      {page.generated_at && (
                        <span className="text-xs text-gray-500">
                          {new Date(page.generated_at).toLocaleDateString()}
                        </span>
                      )}
                    </>
                  ) : (
                    <Badge variant="outline">Ready</Badge>
                  )}
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}