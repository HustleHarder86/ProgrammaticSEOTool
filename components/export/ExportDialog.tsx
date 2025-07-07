'use client';

import { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { 
  Download, FileText, Code, Database, Globe, X, 
  Settings, RefreshCw, CheckCircle, AlertCircle 
} from 'lucide-react';

interface ExportDialogProps {
  projectId: string;
  isOpen: boolean;
  onClose: () => void;
  onExportStart: (format: string, options: any) => void;
  isExporting: boolean;
  exportProgress?: {
    status: string;
    progress: number;
    message?: string;
  };
}

interface ExportFormat {
  id: string;
  name: string;
  description: string;
  icon: React.ComponentType<{ className?: string }>;
  fileExtension: string;
  recommended?: boolean;
  options?: ExportOption[];
}

interface ExportOption {
  id: string;
  name: string;
  description: string;
  type: 'boolean' | 'select' | 'text' | 'number';
  defaultValue: any;
  options?: { value: string; label: string }[];
}

const exportFormats: ExportFormat[] = [
  {
    id: 'csv',
    name: 'CSV',
    description: 'Comma-separated values format for spreadsheet applications',
    icon: Database,
    fileExtension: '.csv',
    recommended: true,
    options: [
      {
        id: 'include_metadata',
        name: 'Include Metadata',
        description: 'Include page metadata like creation date, quality scores',
        type: 'boolean',
        defaultValue: true
      },
      {
        id: 'include_content',
        name: 'Include Full Content',
        description: 'Include the complete page content (may result in large files)',
        type: 'boolean',
        defaultValue: false
      }
    ]
  },
  {
    id: 'json',
    name: 'JSON',
    description: 'JavaScript Object Notation for APIs and data exchange',
    icon: Code,
    fileExtension: '.json',
    options: [
      {
        id: 'pretty_print',
        name: 'Pretty Print',
        description: 'Format JSON with indentation for readability',
        type: 'boolean',
        defaultValue: true
      },
      {
        id: 'include_raw_data',
        name: 'Include Raw Data',
        description: 'Include the original template variables and data',
        type: 'boolean',
        defaultValue: true
      }
    ]
  },
  {
    id: 'wordpress',
    name: 'WordPress XML',
    description: 'WordPress import format for direct site publishing',
    icon: Globe,
    fileExtension: '.xml',
    options: [
      {
        id: 'post_status',
        name: 'Post Status',
        description: 'Default status for imported posts',
        type: 'select',
        defaultValue: 'draft',
        options: [
          { value: 'draft', label: 'Draft' },
          { value: 'publish', label: 'Published' },
          { value: 'private', label: 'Private' }
        ]
      },
      {
        id: 'post_type',
        name: 'Post Type',
        description: 'WordPress post type',
        type: 'select',
        defaultValue: 'post',
        options: [
          { value: 'post', label: 'Post' },
          { value: 'page', label: 'Page' }
        ]
      },
      {
        id: 'category',
        name: 'Default Category',
        description: 'Default category for all posts',
        type: 'text',
        defaultValue: 'Programmatic SEO'
      }
    ]
  },
  {
    id: 'html',
    name: 'HTML',
    description: 'Complete HTML files ready for web hosting',
    icon: FileText,
    fileExtension: '.zip',
    options: [
      {
        id: 'include_css',
        name: 'Include CSS',
        description: 'Include basic CSS styling for pages',
        type: 'boolean',
        defaultValue: true
      },
      {
        id: 'create_index',
        name: 'Create Index',
        description: 'Generate an index.html file with links to all pages',
        type: 'boolean',
        defaultValue: true
      },
      {
        id: 'folder_structure',
        name: 'Folder Structure',
        description: 'How to organize files in folders',
        type: 'select',
        defaultValue: 'flat',
        options: [
          { value: 'flat', label: 'All files in root' },
          { value: 'category', label: 'Group by category' },
          { value: 'date', label: 'Group by date' }
        ]
      }
    ]
  }
];

export function ExportDialog({ 
  projectId, 
  isOpen, 
  onClose, 
  onExportStart, 
  isExporting,
  exportProgress 
}: ExportDialogProps) {
  const [selectedFormat, setSelectedFormat] = useState<string>('csv');
  const [exportOptions, setExportOptions] = useState<Record<string, any>>({});
  const [showOptions, setShowOptions] = useState(false);

  useEffect(() => {
    if (isOpen) {
      // Reset options when dialog opens
      const format = exportFormats.find(f => f.id === selectedFormat);
      if (format?.options) {
        const defaultOptions: Record<string, any> = {};
        format.options.forEach(option => {
          defaultOptions[option.id] = option.defaultValue;
        });
        setExportOptions(defaultOptions);
      }
    }
  }, [isOpen, selectedFormat]);

  const handleExportStart = () => {
    onExportStart(selectedFormat, exportOptions);
  };

  const handleOptionChange = (optionId: string, value: any) => {
    setExportOptions(prev => ({
      ...prev,
      [optionId]: value
    }));
  };

  const renderOption = (option: ExportOption) => {
    const value = exportOptions[option.id] ?? option.defaultValue;

    switch (option.type) {
      case 'boolean':
        return (
          <div className="flex items-center space-x-2">
            <input
              type="checkbox"
              id={option.id}
              checked={value}
              onChange={(e) => handleOptionChange(option.id, e.target.checked)}
              className="rounded border-gray-300 text-purple-600 focus:ring-purple-500"
            />
            <label htmlFor={option.id} className="text-sm font-medium text-gray-700">
              {option.name}
            </label>
          </div>
        );
      
      case 'select':
        return (
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              {option.name}
            </label>
            <select
              value={value}
              onChange={(e) => handleOptionChange(option.id, e.target.value)}
              className="w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:ring-purple-500 focus:border-purple-500"
            >
              {option.options?.map(opt => (
                <option key={opt.value} value={opt.value}>
                  {opt.label}
                </option>
              ))}
            </select>
          </div>
        );
      
      case 'text':
        return (
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              {option.name}
            </label>
            <input
              type="text"
              value={value}
              onChange={(e) => handleOptionChange(option.id, e.target.value)}
              className="w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:ring-purple-500 focus:border-purple-500"
              placeholder={option.description}
            />
          </div>
        );
      
      case 'number':
        return (
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              {option.name}
            </label>
            <input
              type="number"
              value={value}
              onChange={(e) => handleOptionChange(option.id, parseInt(e.target.value))}
              className="w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:ring-purple-500 focus:border-purple-500"
              placeholder={option.description}
            />
          </div>
        );
      
      default:
        return null;
    }
  };

  if (!isOpen) return null;

  const selectedFormatData = exportFormats.find(f => f.id === selectedFormat);
  const hasOptions = selectedFormatData?.options && selectedFormatData.options.length > 0;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg shadow-xl max-w-2xl w-full mx-4 max-h-[90vh] overflow-y-auto">
        <div className="flex items-center justify-between p-6 border-b">
          <h2 className="text-xl font-semibold text-gray-900">Export Project</h2>
          <Button
            variant="ghost"
            size="sm"
            onClick={onClose}
            disabled={isExporting}
          >
            <X className="w-4 h-4" />
          </Button>
        </div>

        <div className="p-6 space-y-6">
          {/* Export Progress */}
          {exportProgress && (
            <Card className="border-blue-200 bg-blue-50">
              <CardContent className="p-4">
                <div className="flex items-center">
                  {exportProgress.status === 'completed' ? (
                    <CheckCircle className="w-5 h-5 text-green-600 mr-3" />
                  ) : exportProgress.status === 'failed' ? (
                    <AlertCircle className="w-5 h-5 text-red-600 mr-3" />
                  ) : (
                    <RefreshCw className="w-5 h-5 text-blue-600 mr-3 animate-spin" />
                  )}
                  <div className="flex-1">
                    <div className="flex items-center justify-between">
                      <span className="font-medium text-gray-900">
                        {exportProgress.status === 'completed' ? 'Export Complete' : 
                         exportProgress.status === 'failed' ? 'Export Failed' : 
                         'Exporting...'}
                      </span>
                      <span className="text-sm text-gray-600">
                        {Math.round(exportProgress.progress)}%
                      </span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2 mt-2">
                      <div 
                        className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                        style={{ width: `${exportProgress.progress}%` }}
                      />
                    </div>
                    {exportProgress.message && (
                      <p className="text-sm text-gray-600 mt-1">{exportProgress.message}</p>
                    )}
                  </div>
                </div>
              </CardContent>
            </Card>
          )}

          {/* Format Selection */}
          <div>
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Select Export Format</h3>
            <div className="grid grid-cols-2 gap-4">
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
                          <h4 className="font-semibold text-gray-900 flex items-center">
                            {format.name}
                            {format.recommended && (
                              <span className="ml-2 px-2 py-1 text-xs bg-green-100 text-green-700 rounded-full">
                                Recommended
                              </span>
                            )}
                          </h4>
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
          </div>

          {/* Export Options */}
          {hasOptions && (
            <div>
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-semibold text-gray-900">Export Options</h3>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => setShowOptions(!showOptions)}
                >
                  <Settings className="w-4 h-4 mr-2" />
                  {showOptions ? 'Hide Options' : 'Show Options'}
                </Button>
              </div>
              
              {showOptions && (
                <Card>
                  <CardContent className="p-4">
                    <div className="space-y-4">
                      {selectedFormatData?.options?.map((option) => (
                        <div key={option.id}>
                          {renderOption(option)}
                          <p className="text-sm text-gray-500 mt-1">
                            {option.description}
                          </p>
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              )}
            </div>
          )}
        </div>

        <div className="flex justify-end space-x-3 p-6 border-t">
          <Button
            variant="outline"
            onClick={onClose}
            disabled={isExporting}
          >
            Cancel
          </Button>
          <Button
            onClick={handleExportStart}
            disabled={isExporting}
            className="bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700"
          >
            {isExporting ? (
              <>
                <RefreshCw className="w-4 h-4 mr-2 animate-spin" />
                Exporting...
              </>
            ) : (
              <>
                <Download className="w-4 h-4 mr-2" />
                Start Export
              </>
            )}
          </Button>
        </div>
      </div>
    </div>
  );
}