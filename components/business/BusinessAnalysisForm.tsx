'use client';

import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Building2, Globe } from 'lucide-react';

interface BusinessAnalysisFormProps {
  onSubmit: (data: { businessInput: string; inputType: 'text' | 'url' }) => void;
  isLoading?: boolean;
}

export function BusinessAnalysisForm({ onSubmit, isLoading = false }: BusinessAnalysisFormProps) {
  const [inputType, setInputType] = useState<'text' | 'url'>('text');
  const [businessInput, setBusinessInput] = useState('');
  const [errors, setErrors] = useState<{ businessInput?: string }>({});

  const validateForm = () => {
    const newErrors: { businessInput?: string } = {};

    if (!businessInput.trim()) {
      newErrors.businessInput = 'Please provide business information';
    } else if (inputType === 'url') {
      // Basic URL validation
      try {
        new URL(businessInput);
      } catch {
        newErrors.businessInput = 'Please enter a valid URL';
      }
    } else if (businessInput.trim().length < 20) {
      newErrors.businessInput = 'Please provide more details about your business (at least 20 characters)';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (validateForm()) {
      onSubmit({ businessInput: businessInput.trim(), inputType });
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      {/* Input Type Selector */}
      <div className="flex gap-4 mb-6">
        <button
          type="button"
          onClick={() => setInputType('text')}
          className={`flex-1 p-4 rounded-lg border-2 transition-all ${
            inputType === 'text'
              ? 'border-blue-500 bg-blue-50'
              : 'border-gray-200 hover:border-gray-300'
          }`}
        >
          <Building2 className="w-6 h-6 mx-auto mb-2 text-gray-600" />
          <div className="text-sm font-medium">Describe Your Business</div>
          <div className="text-xs text-gray-500 mt-1">Tell us what you do</div>
        </button>

        <button
          type="button"
          onClick={() => setInputType('url')}
          className={`flex-1 p-4 rounded-lg border-2 transition-all ${
            inputType === 'url'
              ? 'border-blue-500 bg-blue-50'
              : 'border-gray-200 hover:border-gray-300'
          }`}
        >
          <Globe className="w-6 h-6 mx-auto mb-2 text-gray-600" />
          <div className="text-sm font-medium">Enter Website URL</div>
          <div className="text-xs text-gray-500 mt-1">We&apos;ll analyze your site</div>
        </button>
      </div>

      {/* Input Field */}
      <div>
        {inputType === 'text' ? (
          <>
            <label htmlFor="businessInput" className="block text-sm font-medium text-gray-700 mb-2">
              Describe your business
            </label>
            <textarea
              id="businessInput"
              value={businessInput}
              onChange={(e) => setBusinessInput(e.target.value)}
              className={`w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 ${
                errors.businessInput ? 'border-red-300' : 'border-gray-300'
              }`}
              rows={6}
              placeholder="Example: We are a project management software company that helps teams collaborate better. Our main features include task tracking, team collaboration, and project analytics..."
              disabled={isLoading}
            />
          </>
        ) : (
          <>
            <label htmlFor="businessInput" className="block text-sm font-medium text-gray-700 mb-2">
              Enter your website URL
            </label>
            <input
              id="businessInput"
              type="url"
              value={businessInput}
              onChange={(e) => setBusinessInput(e.target.value)}
              className={`w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 ${
                errors.businessInput ? 'border-red-300' : 'border-gray-300'
              }`}
              placeholder="https://example.com"
              disabled={isLoading}
            />
          </>
        )}
        {errors.businessInput && (
          <p className="mt-1 text-sm text-red-600">{errors.businessInput}</p>
        )}
      </div>

      {/* Examples */}
      <div className="bg-gray-50 p-4 rounded-lg">
        <p className="text-sm text-gray-600 font-medium mb-2">Examples:</p>
        <ul className="text-sm text-gray-500 space-y-1">
          {inputType === 'text' ? (
            <>
              <li>• &quot;We sell running shoes and athletic gear online&quot;</li>
              <li>• &quot;SaaS platform for real estate investment analysis&quot;</li>
              <li>• &quot;Local plumbing services in major US cities&quot;</li>
            </>
          ) : (
            <>
              <li>• https://www.shopify.com</li>
              <li>• https://www.airbnb.com</li>
              <li>• https://www.uber.com</li>
            </>
          )}
        </ul>
      </div>

      {/* Submit Button */}
      <Button
        type="submit"
        className="w-full"
        size="lg"
        disabled={isLoading}
      >
        {isLoading ? 'Analyzing...' : 'Analyze Business'}
      </Button>
    </form>
  );
}