'use client';

import { useState } from 'react';
import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import {
  FileText,
  Sparkles,
  Database,
  MoreVertical,
  Edit,
  Trash2,
  Copy,
  Eye
} from 'lucide-react';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import { Template } from '@/types';
import { formatDistanceToNow } from 'date-fns';

interface TemplateCardProps {
  template: Template;
  projectId: string;
  onEdit?: (template: Template) => void;
  onDelete?: (template: Template) => void;
  onDuplicate?: (template: Template) => void;
}

export function TemplateCard({ 
  template, 
  projectId,
  onEdit,
  onDelete,
  onDuplicate 
}: TemplateCardProps) {
  const [isExpanded, setIsExpanded] = useState(false);

  const handleGeneratePages = (e: React.MouseEvent) => {
    e.stopPropagation();
    // Navigation is handled by the Link component
  };

  return (
    <Card 
      className="hover:shadow-lg transition-all duration-300 cursor-pointer"
      onClick={() => setIsExpanded(!isExpanded)}
    >
      <CardHeader>
        <div className="flex items-start justify-between">
          <div className="flex items-start space-x-3">
            <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-purple-100 to-blue-100 flex items-center justify-center">
              <FileText className="w-5 h-5 text-purple-700" />
            </div>
            <div className="flex-1">
              <CardTitle className="text-lg">{template.name}</CardTitle>
              <CardDescription className="mt-1">
                <code className="text-sm bg-gray-100 px-2 py-1 rounded">
                  {template.pattern}
                </code>
              </CardDescription>
            </div>
          </div>
          
          <DropdownMenu>
            <DropdownMenuTrigger asChild onClick={(e) => e.stopPropagation()}>
              <Button variant="ghost" size="icon" className="h-8 w-8">
                <MoreVertical className="h-4 w-4" />
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end">
              <DropdownMenuItem onClick={() => onEdit?.(template)}>
                <Edit className="mr-2 h-4 w-4" />
                Edit Template
              </DropdownMenuItem>
              <DropdownMenuItem onClick={() => onDuplicate?.(template)}>
                <Copy className="mr-2 h-4 w-4" />
                Duplicate
              </DropdownMenuItem>
              <DropdownMenuSeparator />
              <DropdownMenuItem 
                onClick={() => onDelete?.(template)}
                className="text-red-600"
              >
                <Trash2 className="mr-2 h-4 w-4" />
                Delete
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        </div>
      </CardHeader>
      
      <CardContent>
        <div className="space-y-4">
          {/* Variables */}
          <div>
            <p className="text-sm font-medium text-gray-700 mb-2">Variables</p>
            <div className="flex flex-wrap gap-2">
              {template.variables.map((variable) => (
                <Badge key={variable} variant="secondary">
                  {variable}
                </Badge>
              ))}
            </div>
          </div>

          {/* Stats */}
          <div className="grid grid-cols-2 gap-4 py-3 border-y">
            <div>
              <p className="text-sm text-gray-600">Potential Pages</p>
              <p className="font-semibold">
                {Math.pow(10, template.variables.length).toLocaleString()}
              </p>
            </div>
            <div>
              <p className="text-sm text-gray-600">Created</p>
              <p className="font-semibold text-sm">
                {formatDistanceToNow(new Date(template.created_at), { addSuffix: true })}
              </p>
            </div>
          </div>

          {/* Actions */}
          <div className="flex gap-2">
            <Link href={`/projects/${projectId}/data?templateId=${template.id}`}>
              <Button size="sm" variant="outline" onClick={handleGeneratePages}>
                <Database className="w-4 h-4 mr-2" />
                Add Data
              </Button>
            </Link>
            <Link href={`/projects/${projectId}/templates/${template.id}`}>
              <Button size="sm" variant="outline" onClick={handleGeneratePages}>
                <Eye className="w-4 h-4 mr-2" />
                Preview
              </Button>
            </Link>
            <Link href={`/projects/${projectId}/generate?templateId=${template.id}`}>
              <Button 
                size="sm"
                className="bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700"
                onClick={handleGeneratePages}
              >
                <Sparkles className="w-4 h-4 mr-2" />
                Generate Pages
              </Button>
            </Link>
          </div>

          {/* Expanded Details */}
          {isExpanded && template.template_sections && (
            <div className="pt-4 border-t space-y-3">
              <div>
                <p className="text-sm font-medium text-gray-700 mb-1">SEO Structure</p>
                <div className="text-sm text-gray-600 space-y-1">
                  {template.template_sections.seo_structure?.title_template && (
                    <p><span className="font-medium">Title:</span> {template.template_sections.seo_structure.title_template}</p>
                  )}
                  {template.template_sections.seo_structure?.meta_description_template && (
                    <p><span className="font-medium">Meta:</span> {template.template_sections.seo_structure.meta_description_template}</p>
                  )}
                </div>
              </div>
              
              {template.template_sections.content_sections && template.template_sections.content_sections.length > 0 && (
                <div>
                  <p className="text-sm font-medium text-gray-700 mb-1">Content Sections</p>
                  <p className="text-sm text-gray-600">
                    {template.template_sections.content_sections.length} sections configured
                  </p>
                </div>
              )}
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  );
}