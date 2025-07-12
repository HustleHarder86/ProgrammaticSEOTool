'use client';

import { useState, useEffect, useCallback } from 'react';
import { useParams, useRouter } from 'next/navigation';
import Link from 'next/link';
import { apiClient } from '@/lib/api/client';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { Badge } from '@/components/ui/badge';
import { ArrowLeft, Eye, Download, Trash2, Search, FileText } from 'lucide-react';
import { Input } from '@/components/ui/input';
import { Project } from '@/types';

interface GeneratedPage {
  id: string;
  title: string;
  slug: string;
  keyword: string;
  variables: Record<string, string | number>;
  created_at: string;
  quality_score: number;
}

interface PageListResponse {
  pages: GeneratedPage[];
  total: number;
  offset: number;
  limit: number;
}

export default function PagesListPage() {
  const params = useParams();
  const router = useRouter();
  const projectId = params?.id as string;

  const [project, setProject] = useState<Project | null>(null);
  const [pages, setPages] = useState<GeneratedPage[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(0);
  const [deletingId, setDeletingId] = useState<string | null>(null);
  
  const itemsPerPage = 50;

  const loadPages = useCallback(async () => {
    try {
      setLoading(true);
      
      const offset = (currentPage - 1) * itemsPerPage;
      const response = await apiClient.get<PageListResponse>(
        `/api/projects/${projectId}/pages?offset=${offset}&limit=${itemsPerPage}`
      );

      setPages(response.data.pages);
      setTotalPages(Math.ceil(response.data.total / itemsPerPage));
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load pages');
    } finally {
      setLoading(false);
    }
  }, [projectId, currentPage]);

  const loadProject = useCallback(async () => {
    try {
      const response = await apiClient.get<Project>(`/api/projects/${projectId}`);
      setProject(response.data);
    } catch (err) {
      console.error('Failed to load project:', err);
    }
  }, [projectId]);

  useEffect(() => {
    if (projectId) {
      loadProject();
      loadPages();
    }
  }, [projectId, loadProject, loadPages]);

  const handleDelete = async (pageId: string) => {
    if (!confirm('Are you sure you want to delete this page?')) return;
    
    try {
      setDeletingId(pageId);
      await apiClient.delete(`/api/projects/${projectId}/pages/${pageId}`);
      await loadPages();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to delete page');
    } finally {
      setDeletingId(null);
    }
  };

  const handleDeleteAll = async () => {
    if (!confirm('Are you sure you want to delete ALL generated pages? This cannot be undone.')) return;
    
    try {
      setLoading(true);
      await apiClient.delete(`/api/projects/${projectId}/pages`);
      await loadPages();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to delete pages');
    } finally {
      setLoading(false);
    }
  };

  const filteredPages = pages.filter(page => 
    page.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
    page.keyword.toLowerCase().includes(searchTerm.toLowerCase())
  );

  if (loading && pages.length === 0) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-600"></div>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8 max-w-6xl">
      {/* Header */}
      <div className="mb-8">
        <Link href={`/projects/${projectId}`}>
          <Button variant="ghost" className="mb-4">
            <ArrowLeft className="w-4 h-4 mr-2" />
            Back to Project
          </Button>
        </Link>
        
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900 mb-2">
              Generated Pages
            </h1>
            <p className="text-lg text-gray-600">
              {project?.business_analysis?.business_name || project?.name} - {pages.length} pages
            </p>
          </div>
          <div className="flex gap-4">
            <Link href={`/projects/${projectId}/generate`}>
              <Button>
                Generate More Pages
              </Button>
            </Link>
            <Link href={`/projects/${projectId}/export`}>
              <Button variant="outline">
                <Download className="w-4 h-4 mr-2" />
                Export All
              </Button>
            </Link>
          </div>
        </div>
      </div>

      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-6">
          {error}
        </div>
      )}

      {/* Search and Actions */}
      <Card className="mb-6">
        <CardHeader>
          <div className="flex items-center justify-between">
            <div className="flex-1 max-w-sm">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-gray-500" />
                <Input
                  placeholder="Search pages..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="pl-10"
                />
              </div>
            </div>
            {pages.length > 0 && (
              <Button 
                variant="destructive" 
                size="sm"
                onClick={handleDeleteAll}
              >
                <Trash2 className="w-4 h-4 mr-2" />
                Delete All
              </Button>
            )}
          </div>
        </CardHeader>
      </Card>

      {/* Pages Table */}
      {filteredPages.length === 0 ? (
        <Card>
          <CardHeader>
            <CardTitle>No Pages Found</CardTitle>
            <CardDescription>
              {searchTerm 
                ? 'No pages match your search criteria.'
                : 'No pages have been generated yet. Click "Generate Pages" to create your first batch.'}
            </CardDescription>
          </CardHeader>
          {!searchTerm && (
            <CardContent>
              <Link href={`/projects/${projectId}/generate`}>
                <Button>
                  <FileText className="w-4 h-4 mr-2" />
                  Generate Pages
                </Button>
              </Link>
            </CardContent>
          )}
        </Card>
      ) : (
        <Card>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Title</TableHead>
                <TableHead>Keyword</TableHead>
                <TableHead>Quality</TableHead>
                <TableHead>Created</TableHead>
                <TableHead className="text-right">Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {filteredPages.map((page) => (
                <TableRow key={page.id}>
                  <TableCell className="font-medium">
                    <div>
                      <div>{page.title}</div>
                      <div className="text-sm text-gray-500">/{page.slug}</div>
                    </div>
                  </TableCell>
                  <TableCell>{page.keyword}</TableCell>
                  <TableCell>
                    <Badge 
                      variant={page.quality_score >= 80 ? 'default' : page.quality_score >= 60 ? 'secondary' : 'outline'}
                    >
                      {page.quality_score}%
                    </Badge>
                  </TableCell>
                  <TableCell className="text-sm text-gray-500">
                    {new Date(page.created_at).toLocaleDateString()}
                  </TableCell>
                  <TableCell className="text-right">
                    <div className="flex justify-end gap-2">
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => router.push(`/projects/${projectId}/pages/${page.id}`)}
                      >
                        <Eye className="w-4 h-4" />
                      </Button>
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => handleDelete(page.id)}
                        disabled={deletingId === page.id}
                      >
                        <Trash2 className="w-4 h-4 text-red-500" />
                      </Button>
                    </div>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </Card>
      )}

      {/* Pagination */}
      {totalPages > 1 && (
        <div className="flex justify-center gap-2 mt-6">
          <Button
            variant="outline"
            size="sm"
            onClick={() => setCurrentPage(prev => Math.max(1, prev - 1))}
            disabled={currentPage === 1}
          >
            Previous
          </Button>
          <span className="flex items-center px-4 text-sm text-gray-600">
            Page {currentPage} of {totalPages}
          </span>
          <Button
            variant="outline"
            size="sm"
            onClick={() => setCurrentPage(prev => Math.min(totalPages, prev + 1))}
            disabled={currentPage === totalPages}
          >
            Next
          </Button>
        </div>
      )}
    </div>
  );
}