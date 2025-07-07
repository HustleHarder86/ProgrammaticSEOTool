'use client';

import { Button } from "@/components/ui/button";
import { 
  ArrowRight, Zap, Upload, Globe, Sparkles, Download, 
  FolderOpen, Plus, FileText,
  LayoutTemplate, FileSearch, Activity
} from "lucide-react";
import Link from "next/link";
import { useState, useEffect } from "react";

export default function Home() {
  const [currentTime, setCurrentTime] = useState(new Date());

  useEffect(() => {
    const timer = setInterval(() => setCurrentTime(new Date()), 60000);
    return () => clearInterval(timer);
  }, []);

  const greeting = () => {
    const hour = currentTime.getHours();
    if (hour < 12) return "Good morning";
    if (hour < 18) return "Good afternoon";
    return "Good evening";
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-white to-purple-50/30 overflow-hidden">
      {/* Background Effects */}
      <div className="fixed inset-0 -z-10">
        <div className="absolute top-0 -left-4 w-96 h-96 bg-purple-300 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob" />
        <div className="absolute top-0 -right-4 w-96 h-96 bg-blue-300 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob animation-delay-2000" />
        <div className="absolute -bottom-8 left-20 w-96 h-96 bg-pink-300 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob animation-delay-4000" />
      </div>

      {/* Dashboard Header */}
      <section className="relative px-4 pt-12 pb-8 mx-auto max-w-7xl">
        <div className="relative">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            {greeting()}!
          </h1>
          <p className="text-gray-600 text-lg">
            Your SEO toolkit workspace
          </p>
        </div>
      </section>

      {/* Quick Stats */}
      <section className="px-4 pb-8 mx-auto max-w-7xl">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          <StatCard
            icon={<FolderOpen className="w-5 h-5 text-purple-600" />}
            label="Active Projects"
            value="0"
            subtext="No projects yet"
          />
          <StatCard
            icon={<FileText className="w-5 h-5 text-blue-600" />}
            label="Pages Generated"
            value="0"
            subtext="Start your first project"
          />
          <StatCard
            icon={<LayoutTemplate className="w-5 h-5 text-green-600" />}
            label="Templates Created"
            value="0"
            subtext="Create a template"
          />
          <StatCard
            icon={<Activity className="w-5 h-5 text-orange-600" />}
            label="Last Activity"
            value="Today"
            subtext="Ready to begin"
          />
        </div>
      </section>

      {/* Quick Actions */}
      <section className="px-4 py-8 mx-auto max-w-7xl">
        <h2 className="text-2xl font-bold text-gray-900 mb-6">Quick Actions</h2>
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          <ActionCard
            icon={<Plus className="w-8 h-8 text-white" />}
            title="New Project"
            description="Start a new SEO project"
            href="/projects/new"
            primary={true}
          />
          <ActionCard
            icon={<Globe className="w-8 h-8 text-purple-600" />}
            title="Analyze Website"
            description="Get template suggestions from any URL"
            href="/test-api"
          />
          <ActionCard
            icon={<Upload className="w-8 h-8 text-purple-600" />}
            title="Import Data"
            description="Upload CSV data for bulk generation"
            href="/import"
          />
          <ActionCard
            icon={<LayoutTemplate className="w-8 h-8 text-purple-600" />}
            title="Templates"
            description="Manage your page templates"
            href="/templates"
          />
          <ActionCard
            icon={<Sparkles className="w-8 h-8 text-purple-600" />}
            title="Generate Pages"
            description="Create bulk pages from templates"
            href="/generate"
          />
          <ActionCard
            icon={<Download className="w-8 h-8 text-purple-600" />}
            title="Export"
            description="Export pages as CSV, WordPress, or JSON"
            href="/export"
          />
        </div>
      </section>

      {/* Recent Projects */}
      <section className="px-4 py-8 mx-auto max-w-7xl">
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-2xl font-bold text-gray-900">Recent Projects</h2>
          <Link href="/projects">
            <Button variant="outline" size="sm" className="text-purple-600 border-purple-200 hover:bg-purple-50">
              View All Projects <ArrowRight className="w-4 h-4 ml-2" />
            </Button>
          </Link>
        </div>
        <div className="bg-white rounded-2xl border border-gray-200 p-12 text-center">
          <div className="inline-flex items-center justify-center w-16 h-16 bg-purple-100 rounded-full mb-4">
            <FolderOpen className="w-8 h-8 text-purple-600" />
          </div>
          <h3 className="text-lg font-semibold text-gray-900 mb-2">No projects yet</h3>
          <p className="text-gray-600 mb-6 max-w-md mx-auto">
            Start a new project to begin generating SEO pages.
          </p>
          <Link href="/projects/new">
            <Button className="bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700">
              <Plus className="w-4 h-4 mr-2" />
              Create Project
            </Button>
          </Link>
        </div>
      </section>

      {/* Workflow Guide */}
      <section className="px-4 py-8 mx-auto max-w-7xl mb-12">
        <h2 className="text-2xl font-bold text-gray-900 mb-6">Workflow</h2>
        <div className="bg-gradient-to-br from-purple-50 to-blue-50 rounded-2xl p-8 border border-purple-200/50">
          <div className="grid lg:grid-cols-3 gap-8">
            <GuideStep
              number="1"
              title="Analyze"
              description="Enter a URL or description to get template suggestions."
              icon={<FileSearch className="w-5 h-5 text-purple-700" />}
            />
            <GuideStep
              number="2"
              title="Build"
              description="Create templates with variables and import your data."
              icon={<LayoutTemplate className="w-5 h-5 text-purple-700" />}
            />
            <GuideStep
              number="3"
              title="Export"
              description="Generate pages and export in your preferred format."
              icon={<Zap className="w-5 h-5 text-purple-700" />}
            />
          </div>
        </div>
      </section>
    </div>
  );
}

// Dashboard Components
function StatCard({ 
  icon, 
  label, 
  value, 
  subtext 
}: { 
  icon: React.ReactNode; 
  label: string; 
  value: string;
  subtext: string;
}) {
  return (
    <div className="bg-white rounded-xl border border-gray-200 p-6 hover:shadow-lg transition-shadow duration-300">
      <div className="flex items-start justify-between mb-4">
        <div className="p-2 bg-gradient-to-br from-purple-50 to-blue-50 rounded-lg">
          {icon}
        </div>
      </div>
      <p className="text-sm font-medium text-gray-600 mb-1">{label}</p>
      <p className="text-2xl font-bold text-gray-900">{value}</p>
      <p className="text-sm text-gray-500 mt-1">{subtext}</p>
    </div>
  );
}

function ActionCard({ 
  icon, 
  title, 
  description,
  href,
  primary = false
}: { 
  icon: React.ReactNode; 
  title: string; 
  description: string;
  href: string;
  primary?: boolean;
}) {
  return (
    <Link href={href}>
      <div className={`group p-6 rounded-xl border-2 transition-all duration-300 hover:shadow-xl hover:-translate-y-1 cursor-pointer ${
        primary 
          ? 'bg-gradient-to-br from-purple-600 to-blue-600 border-transparent text-white' 
          : 'bg-white border-gray-200 hover:border-purple-300'
      }`}>
        <div className={`mb-4 p-3 rounded-lg w-fit group-hover:scale-110 transition-transform duration-300 ${
          primary ? 'bg-white/20' : 'bg-gradient-to-br from-purple-100 to-blue-100'
        }`}>
          {icon}
        </div>
        <h3 className={`text-xl font-bold mb-2 ${primary ? 'text-white' : 'text-gray-900'}`}>
          {title}
        </h3>
        <p className={`leading-relaxed ${primary ? 'text-white/90' : 'text-gray-600'}`}>
          {description}
        </p>
      </div>
    </Link>
  );
}

function GuideStep({ 
  number, 
  title, 
  description, 
  icon 
}: { 
  number: string; 
  title: string; 
  description: string; 
  icon: React.ReactNode;
}) {
  return (
    <div className="relative">
      <div className="flex items-start gap-4">
        <div className="flex-shrink-0 w-10 h-10 bg-white rounded-full flex items-center justify-center font-bold text-purple-700 border-2 border-purple-300 shadow-sm">
          {number}
        </div>
        <div>
          <h3 className="text-lg font-semibold text-gray-900 mb-2 flex items-center gap-2">
            {icon}
            {title}
          </h3>
          <p className="text-gray-600 leading-relaxed">{description}</p>
        </div>
      </div>
    </div>
  );
}