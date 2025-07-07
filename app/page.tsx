'use client';

import { Button } from "@/components/ui/button";
import { ArrowRight, Zap, Upload, Globe, Sparkles, Database, Download } from "lucide-react";
import Link from "next/link";

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-white to-gray-50">
      {/* Hero Section */}
      <section className="relative px-4 py-20 mx-auto max-w-7xl">
        <div className="absolute inset-0 bg-grid-gray-100 [mask-image:radial-gradient(ellipse_at_center,transparent_20%,black)]" />
        <div className="relative text-center">
          <div className="inline-flex items-center px-4 py-2 mb-6 text-sm font-medium text-primary bg-primary/10 rounded-full">
            <Sparkles className="w-4 h-4 mr-2" />
            Programmatic SEO Made Simple
          </div>
          <h1 className="text-5xl font-bold tracking-tight text-gray-900 sm:text-6xl md:text-7xl">
            Generate Thousands of 
            <span className="block text-transparent bg-clip-text bg-gradient-to-r from-primary to-purple-600">
              SEO-Optimized Pages
            </span>
          </h1>
          <p className="mt-6 text-xl text-gray-600 max-w-3xl mx-auto leading-relaxed">
            Turn your business data into a powerful SEO machine. Create hundreds of targeted pages 
            in minutes using AI-powered templates and automation. Perfect for any business type.
          </p>
          <div className="mt-10 flex flex-col sm:flex-row items-center justify-center gap-4">
            <Link href="/projects/new">
              <Button size="lg" className="gap-2 px-8 py-6 text-lg shadow-lg hover:shadow-xl transition-shadow">
                Start Generating Pages <ArrowRight className="w-5 h-5" />
              </Button>
            </Link>
            <Link href="/test-api">
              <Button variant="outline" size="lg" className="px-8 py-6 text-lg">
                Try Live Demo
              </Button>
            </Link>
          </div>
          <p className="mt-6 text-sm text-gray-500">
            No credit card required • Works with your existing website
          </p>
        </div>
      </section>

      {/* Features Section */}
      <section className="px-4 py-20 mx-auto max-w-7xl">
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold text-gray-900 mb-4">
            Powerful Features for Scale
          </h2>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Everything you need to create programmatic SEO pages that rank
          </p>
        </div>
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8 mb-20">
          <FeatureCard
            icon={<Database className="w-10 h-10 text-primary" />}
            title="Data-Driven Templates"
            description="Create reusable templates with dynamic variables that pull from your data"
            highlight={true}
          />
          <FeatureCard
            icon={<Sparkles className="w-10 h-10 text-primary" />}
            title="AI-Powered Analysis"
            description="Our AI analyzes your business and suggests the best template opportunities"
            highlight={false}
          />
          <FeatureCard
            icon={<Zap className="w-10 h-10 text-primary" />}
            title="Bulk Generation"
            description="Generate hundreds or thousands of unique pages in minutes, not months"
            highlight={false}
          />
          <FeatureCard
            icon={<Globe className="w-10 h-10 text-primary" />}
            title="SEO Optimized"
            description="Every page is automatically optimized with proper meta tags and structure"
            highlight={false}
          />
          <FeatureCard
            icon={<Upload className="w-10 h-10 text-primary" />}
            title="Easy Data Import"
            description="Upload CSV files or connect to your database for seamless data integration"
            highlight={false}
          />
          <FeatureCard
            icon={<Download className="w-10 h-10 text-primary" />}
            title="Multiple Export Formats"
            description="Export to WordPress, CSV, JSON, or publish directly to your CMS"
            highlight={false}
          />
        </div>
      </section>

      {/* How It Works - 3 Step Process */}
      <section className="px-4 py-20 mx-auto max-w-7xl bg-gray-50 rounded-3xl">
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold text-gray-900 mb-4">
            Three Simple Steps to SEO Success
          </h2>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            From idea to thousands of pages in minutes
          </p>
        </div>
        <div className="grid lg:grid-cols-3 gap-12 relative">
          <div className="hidden lg:block absolute top-1/2 left-1/4 right-1/4 h-0.5 bg-gray-300 -translate-y-1/2" />
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
      </section>

      {/* Examples */}
      <section className="px-4 py-20 mx-auto max-w-7xl">
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold text-gray-900 mb-4">
            See It In Action
          </h2>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Real examples from businesses using programmatic SEO to dominate their niches
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
      <section className="relative px-4 py-24 mx-auto max-w-7xl text-center overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-r from-primary/10 to-purple-600/10 rounded-3xl" />
        <div className="relative">
          <h2 className="text-5xl font-bold mb-6 text-gray-900">
            Ready to 10x Your Organic Traffic?
          </h2>
          <p className="text-xl text-gray-600 mb-10 max-w-2xl mx-auto">
            Join thousands of businesses using programmatic SEO to dominate search results. 
            Start generating pages in minutes, not months.
          </p>
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
            <Link href="/projects/new">
              <Button size="lg" className="gap-2 px-8 py-6 text-lg shadow-lg hover:shadow-xl transition-all">
                Start Free Trial <ArrowRight className="w-5 h-5" />
              </Button>
            </Link>
            <Link href="/pricing">
              <Button variant="outline" size="lg" className="px-8 py-6 text-lg">
                View Pricing
              </Button>
            </Link>
          </div>
          <p className="mt-8 text-sm text-gray-500">
            Free 14-day trial • No credit card required • Cancel anytime
          </p>
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
    <div className={`p-8 rounded-xl transition-all hover:shadow-lg ${
      highlight 
        ? 'bg-primary/5 border-2 border-primary/20 shadow-md' 
        : 'bg-white border border-gray-100 shadow-sm'
    }`}>
      <div className="mb-4">{icon}</div>
      <h3 className="text-xl font-semibold mb-3">{title}</h3>
      <p className="text-gray-600 leading-relaxed">{description}</p>
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
    <div className="relative z-10 text-center">
      <div className="mx-auto w-20 h-20 bg-primary rounded-full flex items-center justify-center mb-6 shadow-lg">
        {icon}
      </div>
      <div className="absolute -top-2 left-1/2 -translate-x-1/2 text-6xl font-bold text-gray-100 -z-10">
        {step}
      </div>
      <h3 className="text-2xl font-semibold mb-3">{title}</h3>
      <p className="text-gray-600 leading-relaxed max-w-sm mx-auto">{description}</p>
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
    <div className="p-8 bg-white rounded-xl shadow-sm border border-gray-100 hover:shadow-lg transition-shadow">
      <h4 className="text-xl font-semibold text-gray-900 mb-3">{business}</h4>
      <div className="space-y-3 mb-4">
        <div>
          <p className="text-sm text-gray-500 mb-1">Template:</p>
          <p className="text-sm font-mono bg-gray-50 p-2 rounded">{template}</p>
        </div>
        <div>
          <p className="text-sm text-gray-500 mb-1">Example Result:</p>
          <p className="text-sm font-medium text-primary">{result}</p>
        </div>
      </div>
      <div className="flex justify-between items-center pt-4 border-t">
        <span className="text-sm font-medium text-gray-900">{pages}</span>
        <span className="text-sm font-semibold text-green-600">{growth}</span>
      </div>
    </div>
  );
}