import { useState, useEffect } from 'react';
import { apiClient } from '@/lib/api/client';

interface Project {
  id: string;
  business_analysis?: {
    template_opportunities?: Array<{
      estimated_pages: number;
    }>;
  };
  created_at: string;
}

interface ProjectStats {
  totalProjects: number;
  totalPages: number;
  totalTemplates: number;
  lastActivity: string;
}

export function useProjectStats() {
  const [stats, setStats] = useState<ProjectStats>({
    totalProjects: 0,
    totalPages: 0,
    totalTemplates: 0,
    lastActivity: 'No activity yet'
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchStats();
  }, []);

  const fetchStats = async () => {
    try {
      const response = await apiClient.get<Project[]>('/api/projects');
      const projects = response.data;
      
      let totalPages = 0;
      let totalTemplates = 0;
      let lastActivityDate: Date | null = null;

      projects.forEach(project => {
        // Count templates
        const templates = project.business_analysis?.template_opportunities || [];
        totalTemplates += templates.length;
        
        // Count potential pages
        templates.forEach(template => {
          totalPages += template.estimated_pages || 0;
        });

        // Track last activity
        const createdAt = new Date(project.created_at);
        if (!lastActivityDate || createdAt > lastActivityDate) {
          lastActivityDate = createdAt;
        }
      });

      // Format last activity
      let lastActivity = 'No activity yet';
      if (lastActivityDate) {
        const now = new Date();
        const diffInHours = (now.getTime() - (lastActivityDate as Date).getTime()) / (1000 * 60 * 60);
        
        if (diffInHours < 1) {
          lastActivity = 'Just now';
        } else if (diffInHours < 24) {
          lastActivity = 'Today';
        } else if (diffInHours < 48) {
          lastActivity = 'Yesterday';
        } else if (diffInHours < 168) { // 7 days
          lastActivity = 'This week';
        } else {
          lastActivity = 'Last week';
        }
      }

      setStats({
        totalProjects: projects.length,
        totalPages,
        totalTemplates,
        lastActivity
      });
    } catch (error) {
      console.error('Failed to fetch project stats:', error);
    } finally {
      setLoading(false);
    }
  };

  return { stats, loading };
}