'use client';

import { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { 
  CheckCircle, AlertCircle, Clock, X, RefreshCw, 
  Download, FileText, AlertTriangle
} from 'lucide-react';
import { formatDistanceToNow } from 'date-fns';

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

interface ExportProgressProps {
  exportJob: ExportJob;
  onCancel: () => void;
  onDownload: () => void;
  showActions?: boolean;
  compact?: boolean;
}

export function ExportProgress({ 
  exportJob, 
  onCancel, 
  onDownload, 
  showActions = true,
  compact = false 
}: ExportProgressProps) {
  const [timeElapsed, setTimeElapsed] = useState<string>('');

  useEffect(() => {
    const updateTimeElapsed = () => {
      if (exportJob.started_at) {
        const startTime = new Date(exportJob.started_at);
        const now = new Date();
        const elapsed = now.getTime() - startTime.getTime();
        
        if (elapsed < 60000) {
          setTimeElapsed(`${Math.floor(elapsed / 1000)}s`);
        } else if (elapsed < 3600000) {
          setTimeElapsed(`${Math.floor(elapsed / 60000)}m ${Math.floor((elapsed % 60000) / 1000)}s`);
        } else {
          setTimeElapsed(`${Math.floor(elapsed / 3600000)}h ${Math.floor((elapsed % 3600000) / 60000)}m`);
        }
      } else {
        setTimeElapsed('');
      }
    };

    updateTimeElapsed();
    const interval = setInterval(updateTimeElapsed, 1000);
    return () => clearInterval(interval);
  }, [exportJob.started_at]);

  const getStatusIcon = () => {
    switch (exportJob.status) {
      case 'completed':
        return <CheckCircle className="w-5 h-5 text-green-600" />;
      case 'failed':
        return <AlertCircle className="w-5 h-5 text-red-600" />;
      case 'cancelled':
        return <X className="w-5 h-5 text-gray-600" />;
      case 'in_progress':
        return <RefreshCw className="w-5 h-5 text-blue-600 animate-spin" />;
      default:
        return <Clock className="w-5 h-5 text-yellow-600" />;
    }
  };

  const getStatusColor = () => {
    switch (exportJob.status) {
      case 'completed':
        return 'text-green-700 bg-green-50';
      case 'failed':
        return 'text-red-700 bg-red-50';
      case 'cancelled':
        return 'text-gray-700 bg-gray-50';
      case 'in_progress':
        return 'text-blue-700 bg-blue-50';
      default:
        return 'text-yellow-700 bg-yellow-50';
    }
  };

  const getProgressColor = () => {
    switch (exportJob.status) {
      case 'completed':
        return 'bg-green-600';
      case 'failed':
        return 'bg-red-600';
      case 'cancelled':
        return 'bg-gray-600';
      case 'in_progress':
        return 'bg-blue-600';
      default:
        return 'bg-yellow-600';
    }
  };

  const getStatusMessage = () => {
    switch (exportJob.status) {
      case 'pending':
        return 'Queued for processing...';
      case 'in_progress':
        return `Processing ${exportJob.processed_items} of ${exportJob.total_items} items...`;
      case 'completed':
        return `Export completed successfully! ${exportJob.total_items} items exported.`;
      case 'failed':
        return exportJob.error_message || 'Export failed due to an error.';
      case 'cancelled':
        return 'Export was cancelled.';
      default:
        return 'Unknown status';
    }
  };

  const progressPercentage = Math.round(exportJob.progress);
  const isActive = exportJob.status === 'in_progress' || exportJob.status === 'pending';
  const canCancel = isActive;
  const canDownload = exportJob.status === 'completed';

  if (compact) {
    return (
      <div className="flex items-center justify-between p-3 border rounded-lg">
        <div className="flex items-center space-x-3">
          {getStatusIcon()}
          <div>
            <div className="flex items-center space-x-2">
              <span className="font-medium text-gray-900 uppercase">
                {exportJob.format}
              </span>
              <span className={`px-2 py-1 text-xs rounded-full ${getStatusColor()}`}>
                {exportJob.status}
              </span>
            </div>
            <div className="text-sm text-gray-600">
              {progressPercentage}% complete
              {timeElapsed && ` • ${timeElapsed}`}
            </div>
          </div>
        </div>
        
        {showActions && (
          <div className="flex space-x-2">
            {canDownload && (
              <Button size="sm" onClick={onDownload} className="bg-green-600 hover:bg-green-700">
                <Download className="w-4 h-4 mr-1" />
                Download
              </Button>
            )}
            {canCancel && (
              <Button size="sm" variant="outline" onClick={onCancel}>
                <X className="w-4 h-4 mr-1" />
                Cancel
              </Button>
            )}
          </div>
        )}
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {/* Status Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-3">
          {getStatusIcon()}
          <div>
            <div className="flex items-center space-x-2">
              <span className="font-semibold text-gray-900">
                {exportJob.format.toUpperCase()} Export
              </span>
              <span className={`px-2 py-1 text-xs rounded-full ${getStatusColor()}`}>
                {exportJob.status.replace('_', ' ')}
              </span>
            </div>
            <div className="text-sm text-gray-600">
              Started {formatDistanceToNow(new Date(exportJob.created_at), { addSuffix: true })}
              {timeElapsed && ` • Running for ${timeElapsed}`}
            </div>
          </div>
        </div>
        
        {showActions && (
          <div className="flex space-x-2">
            {canDownload && (
              <Button onClick={onDownload} className="bg-green-600 hover:bg-green-700">
                <Download className="w-4 h-4 mr-2" />
                Download
              </Button>
            )}
            {canCancel && (
              <Button variant="outline" onClick={onCancel}>
                <X className="w-4 h-4 mr-2" />
                Cancel
              </Button>
            )}
          </div>
        )}
      </div>

      {/* Progress Bar */}
      <div className="space-y-2">
        <div className="flex justify-between items-center">
          <span className="text-sm font-medium text-gray-700">Progress</span>
          <span className="text-sm text-gray-600">{progressPercentage}%</span>
        </div>
        <div className="w-full bg-gray-200 rounded-full h-3">
          <div 
            className={`h-3 rounded-full transition-all duration-500 ${getProgressColor()}`}
            style={{ width: `${progressPercentage}%` }}
          />
        </div>
      </div>

      {/* Status Message */}
      <div className={`p-3 rounded-lg ${getStatusColor()}`}>
        <div className="flex items-start space-x-2">
          {exportJob.status === 'failed' && (
            <AlertTriangle className="w-5 h-5 text-red-600 mt-0.5" />
          )}
          <div className="flex-1">
            <p className="text-sm font-medium">{getStatusMessage()}</p>
            {exportJob.status === 'in_progress' && exportJob.total_items > 0 && (
              <p className="text-xs mt-1 opacity-75">
                {exportJob.processed_items} of {exportJob.total_items} items processed
              </p>
            )}
          </div>
        </div>
      </div>

      {/* Export Details */}
      {exportJob.total_items > 0 && (
        <div className="grid grid-cols-2 gap-4 p-4 bg-gray-50 rounded-lg">
          <div className="text-center">
            <div className="text-lg font-semibold text-gray-900">
              {exportJob.processed_items}
            </div>
            <div className="text-sm text-gray-600">Items Processed</div>
          </div>
          <div className="text-center">
            <div className="text-lg font-semibold text-gray-900">
              {exportJob.total_items}
            </div>
            <div className="text-sm text-gray-600">Total Items</div>
          </div>
        </div>
      )}

      {/* Completed Details */}
      {exportJob.status === 'completed' && (
        <Card className="border-green-200 bg-green-50">
          <CardContent className="p-4">
            <div className="flex items-center space-x-2">
              <CheckCircle className="w-5 h-5 text-green-600" />
              <div>
                <p className="font-medium text-green-800">Export Ready!</p>
                <p className="text-sm text-green-700">
                  Your {exportJob.format.toUpperCase()} export is ready for download.
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Error Details */}
      {exportJob.status === 'failed' && exportJob.error_message && (
        <Card className="border-red-200 bg-red-50">
          <CardContent className="p-4">
            <div className="flex items-start space-x-2">
              <AlertCircle className="w-5 h-5 text-red-600 mt-0.5" />
              <div>
                <p className="font-medium text-red-800">Export Failed</p>
                <p className="text-sm text-red-700 mt-1">
                  {exportJob.error_message}
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}