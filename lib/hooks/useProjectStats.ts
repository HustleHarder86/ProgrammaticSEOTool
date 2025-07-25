import { useState, useEffect } from 'react';
import { apiClient } from '@/lib/api/client';

interface TemplateStats {
  template_name: string;
  template_pattern: string;
  potential_pages: number;
  generated_pages: number;
  completion_percentage: number;
}

interface RecentPage {
  id: string;
  title: string;
  template_id: string;
  created_at: string;
  word_count: number;
  quality_score: number;
}

interface ProjectStats {
  project_id: string;
  total_templates: number;
  total_data_rows: number;
  total_potential_pages: number;
  total_generated_pages: number;
  pages_by_template: Record<string, TemplateStats>;
  recent_pages: RecentPage[];
  generation_progress: number;
  next_actions: string[];
}

export function useProjectStats(projectId: string | undefined) {
  const [stats, setStats] = useState<ProjectStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!projectId) {
      setLoading(false);
      return;
    }

    const fetchStats = async () => {
      try {
        setLoading(true);
        setError(null);
        const response = await apiClient.get<ProjectStats>(`/api/projects/${projectId}/stats`);
        setStats(response.data);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to fetch project statistics');
        console.error('Error fetching project stats:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchStats();
  }, [projectId]);

  const refresh = async () => {
    if (!projectId) return;
    
    try {
      setLoading(true);
      const response = await apiClient.get<ProjectStats>(`/api/projects/${projectId}/stats`);
      setStats(response.data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to refresh statistics');
    } finally {
      setLoading(false);
    }
  };

  return { stats, loading, error, refresh };
}