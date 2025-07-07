'use client';

import { Button } from "@/components/ui/button";
import { ArrowRight, Zap, Upload, Globe, Sparkles, Database, Download, CheckCircle, TrendingUp, BarChart3, Layers, Rocket } from "lucide-react";
import Link from "next/link";

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-white to-purple-50/30 overflow-hidden">
      {/* Hero Section */}
      <section className="relative px-4 py-24 mx-auto max-w-7xl">
        {/* Background Effects */}
        <div className="absolute inset-0 -z-10">
          <div className="absolute top-0 -left-4 w-96 h-96 bg-purple-300 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob" />
          <div className="absolute top-0 -right-4 w-96 h-96 bg-blue-300 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob animation-delay-2000" />
          <div className="absolute -bottom-8 left-20 w-96 h-96 bg-pink-300 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob animation-delay-4000" />
        </div>
        
        <div className="relative text-center">
          <div className="inline-flex items-center px-5 py-2.5 mb-8 text-sm font-semibold text-purple-700 bg-gradient-to-r from-purple-100 to-blue-100 rounded-full border border-purple-200/50 shadow-sm hover:shadow-md transition-all duration-300 hover:scale-105">
            <Sparkles className="w-4 h-4 mr-2 animate-pulse" />
            Programmatic SEO Made Simple
          </div>
          <h1 className="text-5xl font-black tracking-tight text-gray-900 sm:text-6xl md:text-7xl lg:text-8xl leading-tight">
            Generate Thousands of 
            <span className="block text-transparent bg-clip-text bg-gradient-to-r from-purple-600 via-blue-600 to-purple-600 bg-300% animate-gradient">
              SEO-Optimized Pages
            </span>
          </h1>
          <p className="mt-8 text-xl sm:text-2xl text-gray-700 max-w-3xl mx-auto leading-relaxed font-light">
            Turn your business data into a <span className="font-semibold text-purple-700">powerful SEO machine</span>. Create hundreds of targeted pages 
            in minutes using AI-powered templates and automation. <span className="text-gray-900 font-medium">Perfect for any business type.</span>
          </p>
          <div className="mt-12 flex flex-col sm:flex-row items-center justify-center gap-4">
            <Link href="/projects/new">
              <Button size="lg" className="gap-2 px-10 py-7 text-lg bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 shadow-xl hover:shadow-2xl transition-all duration-300 hover:scale-105 border-0 text-white font-semibold">
                Start Generating Pages <ArrowRight className="w-5 h-5 ml-1 animate-bounce-x" />
              </Button>
            </Link>
            <Link href="/test-api">
              <Button variant="outline" size="lg" className="px-10 py-7 text-lg border-2 border-purple-200 hover:border-purple-400 hover:bg-purple-50/50 transition-all duration-300 hover:scale-105 font-semibold">
                <Rocket className="w-5 h-5 mr-2" />
                Try Live Demo
              </Button>
            </Link>
          </div>
          <div className="mt-8 flex flex-col sm:flex-row items-center justify-center gap-4 text-sm text-gray-600">
            <span className="flex items-center gap-2">
              <CheckCircle className="w-4 h-4 text-green-500" />
              No credit card required
            </span>
            <span className="hidden sm:block text-gray-400">•</span>
            <span className="flex items-center gap-2">
              <CheckCircle className="w-4 h-4 text-green-500" />
              Works with your existing website
            </span>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="px-4 py-24 mx-auto max-w-7xl">
        <div className="text-center mb-20">
          <h2 className="text-5xl font-black text-gray-900 mb-6 tracking-tight">
            Powerful Features for <span className="text-transparent bg-clip-text bg-gradient-to-r from-purple-600 to-blue-600">Scale</span>
          </h2>
          <p className="text-xl sm:text-2xl text-gray-700 max-w-2xl mx-auto font-light">
            Everything you need to create programmatic SEO pages that <span className="font-semibold">actually rank</span>
          </p>
        </div>
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8 mb-20">
          <FeatureCard
            icon={<Database className="w-10 h-10 text-purple-600" />}
            title="Data-Driven Templates"
            description="Create reusable templates with dynamic variables that pull from your data"
            highlight={true}
          />
          <FeatureCard
            icon={<Sparkles className="w-10 h-10 text-purple-600" />}
            title="AI-Powered Analysis"
            description="Our AI analyzes your business and suggests the best template opportunities"
            highlight={false}
          />
          <FeatureCard
            icon={<Zap className="w-10 h-10 text-purple-600" />}
            title="Bulk Generation"
            description="Generate hundreds or thousands of unique pages in minutes, not months"
            highlight={false}
          />
          <FeatureCard
            icon={<Globe className="w-10 h-10 text-purple-600" />}
            title="SEO Optimized"
            description="Every page is automatically optimized with proper meta tags and structure"
            highlight={false}
          />
          <FeatureCard
            icon={<Upload className="w-10 h-10 text-purple-600" />}
            title="Easy Data Import"
            description="Upload CSV files or connect to your database for seamless data integration"
            highlight={false}
          />
          <FeatureCard
            icon={<Download className="w-10 h-10 text-purple-600" />}
            title="Multiple Export Formats"
            description="Export to WordPress, CSV, JSON, or publish directly to your CMS"
            highlight={false}
          />
        </div>
      </section>

      {/* How It Works - 3 Step Process */}
      <section className="relative px-4 py-24 mx-auto max-w-7xl">
        <div className="absolute inset-0 bg-gradient-to-br from-purple-50 to-blue-50 rounded-3xl" />
        <div className="relative">
          <div className="text-center mb-20">
            <h2 className="text-5xl font-black text-gray-900 mb-6 tracking-tight">
              Three Simple Steps to <span className="text-transparent bg-clip-text bg-gradient-to-r from-purple-600 to-blue-600">SEO Success</span>
            </h2>
            <p className="text-xl sm:text-2xl text-gray-700 max-w-2xl mx-auto font-light">
              From idea to thousands of pages in <span className="font-semibold">minutes</span>
            </p>
          </div>
          <div className="grid lg:grid-cols-3 gap-12 relative">
            <div className="hidden lg:block absolute top-1/2 left-1/4 right-1/4 h-1 bg-gradient-to-r from-purple-300 to-blue-300 -translate-y-1/2 rounded-full" />
            <StepCard
              step={1}
              title="Analyze & Plan"
              description="Enter your business URL or description. Our AI analyzes your niche and suggests proven template patterns."
              icon={<Globe className="w-8 h-8 text-white" />}
            />
            <StepCard
              step={2}
              title="Build & Import"
              description="Choose a template and customize it. Import your data via CSV or manual entry. We handle all combinations."
              icon={<Database className="w-8 h-8 text-white" />}
            />
            <StepCard
              step={3}
              title="Generate & Export"
              description="Click generate and watch as hundreds of SEO-optimized pages are created. Export in any format you need."
              icon={<Zap className="w-8 h-8 text-white" />}
            />
          </div>
        </div>
      </section>

      {/* Examples */}
      <section className="px-4 py-24 mx-auto max-w-7xl">
        <div className="text-center mb-20">
          <h2 className="text-5xl font-black text-gray-900 mb-6 tracking-tight">
            See It In <span className="text-transparent bg-clip-text bg-gradient-to-r from-purple-600 to-blue-600">Action</span>
          </h2>
          <p className="text-xl sm:text-2xl text-gray-700 max-w-2xl mx-auto font-light">
            Real examples from businesses using programmatic SEO to <span className="font-semibold">dominate their niches</span>
          </p>
        </div>
        <div className="grid md:grid-cols-3 gap-8">
          <ExampleCard
            business="Real Estate Platform"
            template="[City] [Property Type] Market Analysis"
            result="Toronto Condo Market Analysis"
            pages="500+ pages"
            growth="+312% organic traffic"
          />
          <ExampleCard
            business="E-commerce Store"
            template="Best [Product] for [Use Case]"
            result="Best Running Shoes for Marathon Training"
            pages="1,000+ pages"
            growth="+428% conversions"
          />
          <ExampleCard
            business="SaaS Company"
            template="[Industry] [Software Type] Guide"
            result="Healthcare CRM Software Guide"
            pages="300+ pages"
            growth="+256% qualified leads"
          />
        </div>
      </section>

      {/* CTA */}
      <section className="relative px-4 py-32 mx-auto max-w-7xl text-center overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-purple-600 via-blue-600 to-purple-600 rounded-3xl opacity-90" />
        <div className="absolute inset-0 bg-grid-white/10 [mask-image:radial-gradient(ellipse_at_center,transparent_40%,black)]" />
        <div className="relative z-10">
          <h2 className="text-5xl sm:text-6xl font-black mb-8 text-white tracking-tight">
            Ready to <span className="text-yellow-300">10x</span> Your Organic Traffic?
          </h2>
          <p className="text-xl sm:text-2xl text-white/90 mb-12 max-w-2xl mx-auto font-light leading-relaxed">
            Join thousands of businesses using programmatic SEO to dominate search results. 
            Start generating pages in <span className="font-semibold text-white">minutes, not months.</span>
          </p>
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
            <Link href="/projects/new">
              <Button size="lg" className="gap-2 px-10 py-7 text-lg bg-white text-purple-700 hover:bg-gray-50 shadow-2xl hover:shadow-3xl transition-all duration-300 hover:scale-105 font-semibold">
                Start Free Trial <ArrowRight className="w-5 h-5 ml-1 animate-bounce-x" />
              </Button>
            </Link>
            <Link href="/pricing">
              <Button variant="outline" size="lg" className="px-10 py-7 text-lg border-2 border-white/50 text-white hover:bg-white/10 backdrop-blur-sm transition-all duration-300 hover:scale-105 font-semibold">
                <BarChart3 className="w-5 h-5 mr-2" />
                View Pricing
              </Button>
            </Link>
          </div>
          <div className="mt-10 flex flex-col sm:flex-row items-center justify-center gap-4 text-sm text-white/80">
            <span className="flex items-center gap-2">
              <CheckCircle className="w-4 h-4 text-yellow-300" />
              Free 14-day trial
            </span>
            <span className="hidden sm:block text-white/50">•</span>
            <span className="flex items-center gap-2">
              <CheckCircle className="w-4 h-4 text-yellow-300" />
              No credit card required
            </span>
            <span className="hidden sm:block text-white/50">•</span>
            <span className="flex items-center gap-2">
              <CheckCircle className="w-4 h-4 text-yellow-300" />
              Cancel anytime
            </span>
          </div>
        </div>
      </section>
    </div>
  );
}

function FeatureCard({ 
  icon, 
  title, 
  description, 
  highlight = false 
}: { 
  icon: React.ReactNode; 
  title: string; 
  description: string;
  highlight?: boolean;
}) {
  return (
    <div className={`group p-8 rounded-2xl transition-all duration-300 hover:shadow-2xl hover:-translate-y-1 ${
      highlight 
        ? 'bg-gradient-to-br from-purple-50 to-blue-50 border-2 border-purple-200 shadow-lg hover:border-purple-300' 
        : 'bg-white border border-gray-200 shadow-md hover:border-purple-200'
    }`}>
      <div className="mb-6 p-3 bg-gradient-to-br from-purple-100 to-blue-100 rounded-xl w-fit group-hover:scale-110 transition-transform duration-300">
        {icon}
      </div>
      <h3 className="text-2xl font-bold mb-4 text-gray-900">{title}</h3>
      <p className="text-gray-600 leading-relaxed text-lg">{description}</p>
    </div>
  );
}

function StepCard({ 
  step, 
  title, 
  description, 
  icon 
}: { 
  step: number; 
  title: string; 
  description: string; 
  icon: React.ReactNode;
}) {
  return (
    <div className="relative z-10 text-center group">
      <div className="mx-auto w-24 h-24 bg-gradient-to-br from-purple-600 to-blue-600 rounded-full flex items-center justify-center mb-8 shadow-2xl group-hover:scale-110 transition-transform duration-300">
        {icon}
      </div>
      <div className="absolute -top-4 left-1/2 -translate-x-1/2 text-8xl font-black text-purple-100/30 -z-10">
        {step}
      </div>
      <h3 className="text-2xl font-bold mb-4 text-gray-900">{title}</h3>
      <p className="text-gray-600 leading-relaxed max-w-sm mx-auto text-lg">{description}</p>
    </div>
  );
}

function ExampleCard({ 
  business, 
  template, 
  result, 
  pages,
  growth
}: { 
  business: string; 
  template: string; 
  result: string; 
  pages: string;
  growth: string;
}) {
  return (
    <div className="group p-8 bg-white rounded-2xl shadow-md border border-gray-200 hover:shadow-2xl hover:border-purple-200 transition-all duration-300 hover:-translate-y-1">
      <div className="flex items-center gap-3 mb-6">
        <div className="p-2 bg-gradient-to-br from-purple-100 to-blue-100 rounded-lg">
          <Layers className="w-5 h-5 text-purple-700" />
        </div>
        <h4 className="text-2xl font-bold text-gray-900">{business}</h4>
      </div>
      <div className="space-y-4 mb-6">
        <div>
          <p className="text-sm font-semibold text-gray-500 mb-2 uppercase tracking-wider">Template:</p>
          <p className="text-sm font-mono bg-gradient-to-r from-purple-50 to-blue-50 p-3 rounded-lg border border-purple-100">{template}</p>
        </div>
        <div>
          <p className="text-sm font-semibold text-gray-500 mb-2 uppercase tracking-wider">Example Result:</p>
          <p className="text-base font-medium text-transparent bg-clip-text bg-gradient-to-r from-purple-600 to-blue-600">{result}</p>
        </div>
      </div>
      <div className="flex justify-between items-center pt-6 border-t border-gray-100">
        <span className="flex items-center gap-2 text-base font-semibold text-gray-900">
          <Database className="w-4 h-4 text-purple-600" />
          {pages}
        </span>
        <span className="flex items-center gap-2 text-base font-bold text-green-600 bg-green-50 px-3 py-1 rounded-full">
          <TrendingUp className="w-4 h-4" />
          {growth}
        </span>
      </div>
    </div>
  );
}