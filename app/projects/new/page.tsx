'use client';

import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { ArrowLeft } from 'lucide-react';
import Link from 'next/link';

export default function NewProjectPage() {
  const [step, setStep] = useState(1);

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-4xl mx-auto px-4 py-8">
        {/* Header */}
        <div className="mb-8">
          <Link href="/" className="inline-flex items-center text-sm text-gray-600 hover:text-gray-900 mb-4">
            <ArrowLeft className="w-4 h-4 mr-1" />
            Back to Home
          </Link>
          <h1 className="text-3xl font-bold text-gray-900">Create New Project</h1>
          <p className="text-gray-600 mt-2">Generate programmatic SEO pages for your business</p>
        </div>

        {/* Progress Bar */}
        <div className="mb-8">
          <div className="flex items-center justify-between mb-2">
            <span className={`text-sm ${step >= 1 ? 'text-primary font-medium' : 'text-gray-400'}`}>
              1. Analyze Business
            </span>
            <span className={`text-sm ${step >= 2 ? 'text-primary font-medium' : 'text-gray-400'}`}>
              2. Select Templates
            </span>
            <span className={`text-sm ${step >= 3 ? 'text-primary font-medium' : 'text-gray-400'}`}>
              3. Import Data
            </span>
          </div>
          <div className="h-2 bg-gray-200 rounded-full overflow-hidden">
            <div 
              className="h-full bg-primary transition-all duration-300"
              style={{ width: `${(step / 3) * 100}%` }}
            />
          </div>
        </div>

        {/* Step Content */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-8">
          {step === 1 && (
            <div>
              <h2 className="text-2xl font-semibold mb-6">Tell us about your business</h2>
              <p className="text-gray-600 mb-8">
                We'll analyze your business and suggest the best programmatic SEO templates.
              </p>
              <div className="text-center py-12 text-gray-500">
                Business analysis form will go here
              </div>
              <div className="flex justify-end mt-8">
                <Button onClick={() => setStep(2)}>
                  Continue to Templates
                </Button>
              </div>
            </div>
          )}

          {step === 2 && (
            <div>
              <h2 className="text-2xl font-semibold mb-6">Choose your templates</h2>
              <p className="text-gray-600 mb-8">
                Select from our suggestions or create custom templates.
              </p>
              <div className="text-center py-12 text-gray-500">
                Template selection will go here
              </div>
              <div className="flex justify-between mt-8">
                <Button variant="outline" onClick={() => setStep(1)}>
                  Back
                </Button>
                <Button onClick={() => setStep(3)}>
                  Continue to Data Import
                </Button>
              </div>
            </div>
          )}

          {step === 3 && (
            <div>
              <h2 className="text-2xl font-semibold mb-6">Import your data</h2>
              <p className="text-gray-600 mb-8">
                Upload a CSV or enter data manually to generate your pages.
              </p>
              <div className="text-center py-12 text-gray-500">
                Data import interface will go here
              </div>
              <div className="flex justify-between mt-8">
                <Button variant="outline" onClick={() => setStep(2)}>
                  Back
                </Button>
                <Button>
                  Generate Pages
                </Button>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}