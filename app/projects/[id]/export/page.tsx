'use client';

import { useState, useEffect, useCallback } from 'react';
import { useParams } from 'next/navigation';
import Link from 'next/link';
import { apiClient } from '@/lib/api/client';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { 
  ArrowLeft, Download, FileText, Code, Database, Globe, 
  CheckCircle, AlertCircle, Clock, X, RefreshCw 
} from 'lucide-react';
import { ExportProgress } from '@/components/export/ExportProgress';
import { formatDistanceToNow } from 'date-fns';

interface Project {
  id: string;
  name: string;
  business_analysis: {
    business_name?: string;
    business_description?: string;
  };
  created_at: string;
}

interface ExportJob {
  id: string;
  project_id: string;
  format: string;
  status: 'pending' | 'in_progress' | 'completed' | 'failed' | 'cancelled';
  progress: number;
  total_items: number;
  processed_items: number;
  created_at: string;
  started_at?: string;
  completed_at?: string;
  error_message?: string;
  download_url?: string;
}

interface ExportFormat {
  id: string;
  name: string;
  description: string;
  icon: React.ComponentType<{ className?: string }>;
  fileExtension: string;
  recommended?: boolean;
}

const exportFormats: ExportFormat[] = [
  {
    id: 'csv',
    name: 'CSV',
    description: 'Comma-separated values format for spreadsheet applications',
    icon: Database,
    fileExtension: '.csv',
    recommended: true
  },
  {
    id: 'json',
    name: 'JSON',
    description: 'JavaScript Object Notation for APIs and data exchange',
    icon: Code,
    fileExtension: '.json'
  },
  {
    id: 'wordpress',
    name: 'WordPress XML',
    description: 'WordPress import format for direct site publishing',
    icon: Globe,
    fileExtension: '.xml'
  },
  {
    id: 'html',
    name: 'HTML',
    description: 'Complete HTML files ready for web hosting',
    icon: FileText,
    fileExtension: '.zip'
  }
];

export default function ExportPage() {
  const params = useParams();
  const projectId = params?.id as string;
  
  const [project, setProject] = useState<Project | null>(null);
  const [exportJobs, setExportJobs] = useState<ExportJob[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedFormat, setSelectedFormat] = useState<string>('csv');
  const [exporting, setExporting] = useState(false);
  const [activeExportId, setActiveExportId] = useState<string | null>(null);

  const loadData = useCallback(async () => {
    try {
      setLoading(true);
      const [projectRes, exportsRes] = await Promise.all([
        apiClient.get<Project>(`/api/projects/${projectId}`),
        apiClient.get<{ exports: ExportJob[] }>(`/api/projects/${projectId}/exports`)
      ]);

      setProject(projectRes.data);
      setExportJobs(exportsRes.data.exports);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load project data');
    } finally {
      setLoading(false);
    }
  }, [projectId]);

  const checkExportStatus = useCallback(async (exportId: string) => {
    try {
      const response = await apiClient.get<ExportJob>(`/api/exports/${exportId}/status`);
      const updatedJob = response.data;
      
      setExportJobs(prev => 
        prev.map(job => job.id === exportId ? updatedJob : job)
      );

      if (updatedJob.status === 'completed' || updatedJob.status === 'failed') {
        setActiveExportId(null);
        setExporting(false);
      }
    } catch (err) {
      console.error('Failed to check export status:', err);
    }
  }, []);

  useEffect(() => {
    if (projectId) {
      loadData();
    }
  }, [projectId, loadData]);

  useEffect(() => {
    // Poll for export status updates
    const interval = setInterval(() => {
      if (activeExportId) {
        checkExportStatus(activeExportId);
      }
    }, 2000);

    return () => clearInterval(interval);
  }, [activeExportId, checkExportStatus]);

  const startExport = async (format: string) => {
    try {
      setExporting(true);
      setError(null);
      
      const response = await apiClient.post(`/api/projects/${projectId}/export`, {
        format,
        options: {}
      });

      const exportId = response.data.export_id;
      setActiveExportId(exportId);
      
      // Add new job to list
      const newJob: ExportJob = {
        id: exportId,
        project_id: projectId,
        format,
        status: 'pending',
        progress: 0,
        total_items: 0,
        processed_items: 0,
        created_at: new Date().toISOString()
      };
      
      setExportJobs(prev => [newJob, ...prev]);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to start export');
      setExporting(false);
    }
  };

  const cancelExport = async (exportId: string) => {
    try {
      await apiClient.delete(`/api/exports/${exportId}`);
      setExportJobs(prev => 
        prev.map(job => 
          job.id === exportId ? { ...job, status: 'cancelled' as const } : job
        )
      );
      
      if (activeExportId === exportId) {
        setActiveExportId(null);
        setExporting(false);
      }
    } catch (err) {
      console.error('Failed to cancel export:', err);
    }
  };

  const downloadExport = async (exportId: string) => {
    try {
      const response = await fetch(`/api/exports/${exportId}/download`);
      if (!response.ok) throw new Error('Download failed');
      
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `export_${exportId}`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to download export');
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'completed': return <CheckCircle className="w-5 h-5 text-green-600" />;
      case 'failed': return <AlertCircle className="w-5 h-5 text-red-600" />;
      case 'cancelled': return <X className="w-5 h-5 text-gray-600" />;
      case 'in_progress': return <RefreshCw className="w-5 h-5 text-blue-600 animate-spin" />;
      default: return <Clock className="w-5 h-5 text-yellow-600" />;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed': return 'text-green-700 bg-green-50 border-green-200';
      case 'failed': return 'text-red-700 bg-red-50 border-red-200';
      case 'cancelled': return 'text-gray-700 bg-gray-50 border-gray-200';
      case 'in_progress': return 'text-blue-700 bg-blue-50 border-blue-200';
      default: return 'text-yellow-700 bg-yellow-50 border-yellow-200';
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-600"></div>
      </div>
    );
  }

  if (error && !project) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
          {error}
        </div>
        <Link href={`/projects/${projectId}`}>
          <Button variant="outline" className="mt-4">
            <ArrowLeft className="w-4 h-4 mr-2" />
            Back to Project
          </Button>
        </Link>
      </div>
    );
  }

  const activeJob = exportJobs.find(job => job.id === activeExportId);

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
              Export Project
            </h1>
            <p className="text-lg text-gray-600">
              Export generated pages for {project?.business_analysis?.business_name || project?.name}
            </p>
          </div>
          <div className="flex items-center text-sm text-gray-500">
            <Download className="w-4 h-4 mr-1" />
            <span>Project Export</span>
          </div>
        </div>
      </div>

      {/* Error Display */}
      {error && (
        <Card className="border-red-200 bg-red-50 mb-6">
          <CardContent className="p-4">
            <div className="flex items-center">
              <AlertCircle className="w-5 h-5 text-red-600 mr-3" />
              <div>
                <p className="font-medium text-red-800">Export Error</p>
                <p className="text-sm text-red-600">{error}</p>
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Active Export Progress */}
      {activeJob && (
        <Card className="mb-6">
          <CardHeader>
            <CardTitle className="flex items-center justify-between">
              <span className="flex items-center">
                {getStatusIcon(activeJob.status)}
                <span className="ml-2">Export in Progress</span>
              </span>
              <Button
                variant="outline"
                size="sm"
                onClick={() => cancelExport(activeJob.id)}
                disabled={activeJob.status === 'completed' || activeJob.status === 'failed'}
              >
                <X className="w-4 h-4 mr-2" />
                Cancel
              </Button>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <ExportProgress
              exportJob={activeJob}
              onCancel={() => cancelExport(activeJob.id)}
              onDownload={() => downloadExport(activeJob.id)}
            />
          </CardContent>
        </Card>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Export Format Selection */}
        <Card>
          <CardHeader>
            <CardTitle>Select Export Format</CardTitle>
            <CardDescription>
              Choose the format that best suits your needs
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {exportFormats.map((format) => {
                const Icon = format.icon;
                const isSelected = selectedFormat === format.id;
                
                return (
                  <div
                    key={format.id}
                    className={`border rounded-lg p-4 cursor-pointer transition-all ${
                      isSelected 
                        ? 'border-purple-500 bg-purple-50' 
                        : 'border-gray-200 hover:border-gray-300'
                    }`}
                    onClick={() => setSelectedFormat(format.id)}
                  >
                    <div className="flex items-start">
                      <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-purple-100 to-blue-100 flex items-center justify-center mr-3">
                        <Icon className="w-5 h-5 text-purple-700" />
                      </div>
                      <div className="flex-1">
                        <div className="flex items-center justify-between">
                          <h3 className="font-semibold text-gray-900 flex items-center">
                            {format.name}
                            {format.recommended && (
                              <span className="ml-2 px-2 py-1 text-xs bg-green-100 text-green-700 rounded-full">
                                Recommended
                              </span>
                            )}
                          </h3>
                          <span className="text-sm text-gray-500">
                            {format.fileExtension}
                          </span>
                        </div>
                        <p className="text-sm text-gray-600 mt-1">
                          {format.description}
                        </p>
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>

            <div className="mt-6 pt-4 border-t">
              <Button 
                onClick={() => startExport(selectedFormat)}
                disabled={exporting}
                className="w-full bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700"
              >
                {exporting ? (
                  <>
                    <RefreshCw className="w-4 h-4 mr-2 animate-spin" />
                    Starting Export...
                  </>
                ) : (
                  <>
                    <Download className="w-4 h-4 mr-2" />
                    Start Export
                  </>
                )}
              </Button>
            </div>
          </CardContent>
        </Card>

        {/* Export History */}
        <Card>
          <CardHeader>
            <CardTitle>Export History</CardTitle>
            <CardDescription>
              View and download previous exports
            </CardDescription>
          </CardHeader>
          <CardContent>
            {exportJobs.length === 0 ? (
              <div className="text-center py-8">
                <Download className="w-12 h-12 text-gray-400 mx-auto mb-3" />
                <p className="text-gray-500">No exports yet</p>
                <p className="text-sm text-gray-400">Start your first export to see it here</p>
              </div>
            ) : (
              <div className="space-y-3">
                {exportJobs.map((job) => (
                  <div
                    key={job.id}
                    className="border rounded-lg p-4 flex items-center justify-between"
                  >
                    <div className="flex items-center">
                      {getStatusIcon(job.status)}
                      <div className="ml-3">
                        <div className="flex items-center">
                          <span className="font-medium text-gray-900 uppercase">
                            {job.format}
                          </span>
                          <span className={`ml-2 px-2 py-1 text-xs rounded-full border ${getStatusColor(job.status)}`}>
                            {job.status}
                          </span>
                        </div>
                        <p className="text-sm text-gray-500">
                          {formatDistanceToNow(new Date(job.created_at), { addSuffix: true })}
                        </p>
                      </div>
                    </div>
                    
                    <div className="flex items-center space-x-2">
                      {job.status === 'completed' && (
                        <Button
                          size="sm"
                          onClick={() => downloadExport(job.id)}
                          className="bg-green-600 hover:bg-green-700"
                        >
                          <Download className="w-4 h-4 mr-1" />
                          Download
                        </Button>
                      )}
                      {job.status === 'in_progress' && (
                        <Button
                          size="sm"
                          variant="outline"
                          onClick={() => cancelExport(job.id)}
                        >
                          <X className="w-4 h-4 mr-1" />
                          Cancel
                        </Button>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}