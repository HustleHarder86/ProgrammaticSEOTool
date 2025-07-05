'use client';

import { Button } from "@/components/ui/button";
import { ArrowRight, Zap, Upload, FileText, Globe } from "lucide-react";
import Link from "next/link";

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-white to-gray-50">
      {/* Hero Section */}
      <section className="px-4 py-20 mx-auto max-w-7xl">
        <div className="text-center">
          <h1 className="text-5xl font-bold tracking-tight text-gray-900 sm:text-6xl">
            Generate Thousands of SEO Pages
            <span className="block text-primary">Automatically</span>
          </h1>
          <p className="mt-6 text-xl text-gray-600 max-w-3xl mx-auto">
            Transform your business with programmatic SEO. Create data-driven pages at scale
            using templates and automation. Works for any business type.
          </p>
          <div className="mt-10 flex items-center justify-center gap-x-6">
            <Link href="/projects/new">
              <Button size="lg" className="gap-2">
                Start Building <ArrowRight className="w-4 h-4" />
              </Button>
            </Link>
            <Link href="/demo">
              <Button variant="outline" size="lg">
                View Demo
              </Button>
            </Link>
          </div>
        </div>
      </section>

      {/* Features Grid */}
      <section className="px-4 py-16 mx-auto max-w-7xl">
        <h2 className="text-3xl font-bold text-center mb-12">How It Works</h2>
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
          <FeatureCard
            icon={<Globe className="w-8 h-8 text-primary" />}
            title="Analyze Your Business"
            description="Enter your URL or description. AI analyzes your business and suggests templates."
          />
          <FeatureCard
            icon={<FileText className="w-8 h-8 text-primary" />}
            title="Choose Templates"
            description="Select from suggested templates or create custom ones with variable placeholders."
          />
          <FeatureCard
            icon={<Upload className="w-8 h-8 text-primary" />}
            title="Import Your Data"
            description="Upload CSV files or enter data manually. We'll generate all combinations."
          />
          <FeatureCard
            icon={<Zap className="w-8 h-8 text-primary" />}
            title="Generate Pages"
            description="Create hundreds of SEO-optimized pages instantly. Export to any format."
          />
        </div>
      </section>

      {/* Examples */}
      <section className="px-4 py-16 mx-auto max-w-7xl bg-gray-50 rounded-lg">
        <h2 className="text-3xl font-bold text-center mb-12">Real Examples</h2>
        <div className="grid md:grid-cols-3 gap-6">
          <ExampleCard
            business="Real Estate Platform"
            template="[City] [Property Type] Market Analysis"
            result="Toronto Condo Market Analysis"
            pages="500+ pages"
          />
          <ExampleCard
            business="E-commerce Store"
            template="Best [Product] for [Use Case]"
            result="Best Running Shoes for Marathon Training"
            pages="1,000+ pages"
          />
          <ExampleCard
            business="SaaS Company"
            template="[Industry] [Software Type] Guide"
            result="Healthcare CRM Software Guide"
            pages="300+ pages"
          />
        </div>
      </section>

      {/* CTA */}
      <section className="px-4 py-20 mx-auto max-w-7xl text-center">
        <h2 className="text-4xl font-bold mb-6">Ready to Scale Your SEO?</h2>
        <p className="text-xl text-gray-600 mb-8">
          Join businesses generating thousands of pages automatically
        </p>
        <Link href="/projects/new">
          <Button size="lg" className="gap-2">
            Get Started Free <ArrowRight className="w-4 h-4" />
          </Button>
        </Link>
      </section>
    </div>
  );
}

function FeatureCard({ icon, title, description }: { icon: React.ReactNode; title: string; description: string }) {
  return (
    <div className="p-6 bg-white rounded-lg shadow-sm border border-gray-100">
      <div className="mb-4">{icon}</div>
      <h3 className="text-lg font-semibold mb-2">{title}</h3>
      <p className="text-gray-600">{description}</p>
    </div>
  );
}

function ExampleCard({ business, template, result, pages }: { business: string; template: string; result: string; pages: string }) {
  return (
    <div className="p-6 bg-white rounded-lg shadow-sm border border-gray-100">
      <h4 className="font-semibold text-gray-900 mb-2">{business}</h4>
      <p className="text-sm text-gray-600 mb-3">Template: {template}</p>
      <p className="text-sm font-medium text-primary mb-1">Example: {result}</p>
      <p className="text-sm text-gray-500">{pages} generated</p>
    </div>
  );
}