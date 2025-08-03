'use client';

import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { ProjectsList } from '@/components/projects/ProjectsList';
import { ArrowLeft, Plus } from 'lucide-react';

export default function ProjectsPage() {
  return (
    <div className="max-w-7xl">
      {/* Header */}
      <div className="mb-8">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900 mb-2">All Projects</h1>
            <p className="text-lg text-gray-600">
              Manage your programmatic SEO projects
            </p>
          </div>
          <Link href="/analyze">
            <Button className="bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700">
              <Plus className="w-4 h-4 mr-2" />
              New Project
            </Button>
          </Link>
        </div>
      </div>

      {/* Projects List */}
      <ProjectsList />
    </div>
  );
}