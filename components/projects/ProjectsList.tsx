'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import { apiClient } from '@/lib/api/client';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { FolderOpen, Calendar, ArrowRight, Plus, Sparkles } from 'lucide-react';
import { formatDistanceToNow } from 'date-fns';

interface Project {
  id: string;
  name: string;
  business_input: string;
  business_analysis: {
    business_name?: string;
    business_description?: string;
    template_opportunities?: Array<{
      template_name: string;
      estimated_pages: number;
    }>;
  };
  created_at: string;
  updated_at?: string;
}

export function ProjectsList() {
  const [projects, setProjects] = useState<Project[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchProjects();
  }, []);

  const fetchProjects = async () => {
    try {
      setLoading(true);
      const response = await apiClient.get<Project[]>('/api/projects');
      setProjects(response.data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch projects');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center p-12">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-purple-600"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
        Error loading projects: {error}
      </div>
    );
  }

  if (projects.length === 0) {
    return (
      <div className="bg-white rounded-2xl border border-gray-200 p-12 text-center">
        <div className="inline-flex items-center justify-center w-16 h-16 bg-purple-100 rounded-full mb-4">
          <FolderOpen className="w-8 h-8 text-purple-600" />
        </div>
        <h3 className="text-lg font-semibold text-gray-900 mb-2">No projects yet</h3>
        <p className="text-gray-600 mb-6 max-w-md mx-auto">
          Start a new project to begin generating SEO pages.
        </p>
        <Link href="/test-api">
          <Button className="bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700">
            <Plus className="w-4 h-4 mr-2" />
            Create Project
          </Button>
        </Link>
      </div>
    );
  }

  return (
    <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
      {projects.map((project) => {
        const templateCount = project.business_analysis?.template_opportunities?.length || 0;
        const totalPages = project.business_analysis?.template_opportunities?.reduce(
          (sum, t) => sum + (t.estimated_pages || 0), 0
        ) || 0;

        return (
          <Link key={project.id} href={`/projects/${project.id}`}>
            <Card className="h-full hover:shadow-lg transition-all duration-300 hover:border-purple-300 cursor-pointer group">
              <CardHeader>
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <CardTitle className="text-lg group-hover:text-purple-600 transition-colors">
                      {project.business_analysis?.business_name || project.name}
                    </CardTitle>
                    <CardDescription className="mt-2 line-clamp-2">
                      {project.business_analysis?.business_description || project.business_input}
                    </CardDescription>
                  </div>
                  <ArrowRight className="w-5 h-5 text-gray-400 group-hover:text-purple-600 transition-colors" />
                </div>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  <div className="flex items-center justify-between text-sm">
                    <span className="text-gray-600">Templates</span>
                    <span className="font-semibold text-purple-600">{templateCount}</span>
                  </div>
                  <div className="flex items-center justify-between text-sm">
                    <span className="text-gray-600">Potential Pages</span>
                    <span className="font-semibold text-purple-600">{totalPages.toLocaleString()}</span>
                  </div>
                  <div className="pt-3 border-t flex items-center text-sm text-gray-500">
                    <Calendar className="w-4 h-4 mr-1" />
                    {formatDistanceToNow(new Date(project.created_at), { addSuffix: true })}
                  </div>
                </div>
              </CardContent>
            </Card>
          </Link>
        );
      })}
    </div>
  );
}