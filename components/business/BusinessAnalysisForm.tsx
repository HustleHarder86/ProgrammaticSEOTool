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
    <form onSubmit={handleSubmit} className="space-y-8">
      {/* Input Type Selector */}
      <div className="flex gap-4 mb-8">
        <button
          type="button"
          onClick={() => setInputType('text')}
          className={`flex-1 p-6 rounded-xl border-2 transition-all duration-300 hover:scale-[1.02] ${
            inputType === 'text'
              ? 'border-purple-400 bg-gradient-to-br from-purple-50 to-blue-50 shadow-lg'
              : 'border-gray-200 hover:border-purple-200 bg-white'
          }`}
        >
          <div className={`w-12 h-12 mx-auto mb-3 rounded-xl flex items-center justify-center transition-colors duration-300 ${
            inputType === 'text' ? 'bg-gradient-to-br from-purple-600 to-blue-600' : 'bg-gray-100'
          }`}>
            <Building2 className={`w-6 h-6 ${inputType === 'text' ? 'text-white' : 'text-gray-600'}`} />
          </div>
          <div className="text-base font-semibold text-gray-900">Describe Your Business</div>
          <div className="text-sm text-gray-500 mt-1">Tell us what you do</div>
        </button>

        <button
          type="button"
          onClick={() => setInputType('url')}
          className={`flex-1 p-6 rounded-xl border-2 transition-all duration-300 hover:scale-[1.02] ${
            inputType === 'url'
              ? 'border-purple-400 bg-gradient-to-br from-purple-50 to-blue-50 shadow-lg'
              : 'border-gray-200 hover:border-purple-200 bg-white'
          }`}
        >
          <div className={`w-12 h-12 mx-auto mb-3 rounded-xl flex items-center justify-center transition-colors duration-300 ${
            inputType === 'url' ? 'bg-gradient-to-br from-purple-600 to-blue-600' : 'bg-gray-100'
          }`}>
            <Globe className={`w-6 h-6 ${inputType === 'url' ? 'text-white' : 'text-gray-600'}`} />
          </div>
          <div className="text-base font-semibold text-gray-900">Enter Website URL</div>
          <div className="text-sm text-gray-500 mt-1">We&apos;ll analyze your site</div>
        </button>
      </div>

      {/* Input Field */}
      <div>
        {inputType === 'text' ? (
          <>
            <label htmlFor="businessInput" className="block text-base font-semibold text-gray-700 mb-3">
              Describe your business
            </label>
            <textarea
              id="businessInput"
              value={businessInput}
              onChange={(e) => setBusinessInput(e.target.value)}
              className={`w-full px-6 py-4 border-2 rounded-xl focus:ring-4 focus:ring-purple-100 focus:border-purple-500 transition-all duration-200 resize-none ${
                errors.businessInput ? 'border-red-300 bg-red-50/50' : 'border-gray-200 hover:border-purple-200'
              }`}
              rows={6}
              placeholder="Example: We are a project management software company that helps teams collaborate better. Our main features include task tracking, team collaboration, and project analytics..."
              disabled={isLoading}
            />
          </>
        ) : (
          <>
            <label htmlFor="businessInput" className="block text-base font-semibold text-gray-700 mb-3">
              Enter your website URL
            </label>
            <input
              id="businessInput"
              type="url"
              value={businessInput}
              onChange={(e) => setBusinessInput(e.target.value)}
              className={`w-full px-6 py-4 border-2 rounded-xl focus:ring-4 focus:ring-purple-100 focus:border-purple-500 transition-all duration-200 ${
                errors.businessInput ? 'border-red-300 bg-red-50/50' : 'border-gray-200 hover:border-purple-200'
              }`}
              placeholder="https://example.com"
              disabled={isLoading}
            />
          </>
        )}
        {errors.businessInput && (
          <p className="mt-2 text-sm text-red-600 flex items-center">
            <svg className="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
            </svg>
            {errors.businessInput}
          </p>
        )}
      </div>

      {/* Examples */}
      <div className="bg-gradient-to-br from-purple-50 to-blue-50 p-6 rounded-xl border border-purple-100">
        <p className="text-sm font-semibold text-purple-700 mb-3 uppercase tracking-wider">Examples:</p>
        <ul className="text-sm text-gray-700 space-y-2">
          {inputType === 'text' ? (
            <>
              <li className="flex items-start">
                <span className="text-purple-600 mr-2 mt-0.5">•</span>
                <span>&ldquo;We sell running shoes and athletic gear online&rdquo;</span>
              </li>
              <li className="flex items-start">
                <span className="text-purple-600 mr-2 mt-0.5">•</span>
                <span>&ldquo;SaaS platform for real estate investment analysis&rdquo;</span>
              </li>
              <li className="flex items-start">
                <span className="text-purple-600 mr-2 mt-0.5">•</span>
                <span>&ldquo;Local plumbing services in major US cities&rdquo;</span>
              </li>
            </>
          ) : (
            <>
              <li className="flex items-start">
                <span className="text-purple-600 mr-2 mt-0.5">•</span>
                <span className="font-mono text-sm">https://www.shopify.com</span>
              </li>
              <li className="flex items-start">
                <span className="text-purple-600 mr-2 mt-0.5">•</span>
                <span className="font-mono text-sm">https://www.airbnb.com</span>
              </li>
              <li className="flex items-start">
                <span className="text-purple-600 mr-2 mt-0.5">•</span>
                <span className="font-mono text-sm">https://www.uber.com</span>
              </li>
            </>
          )}
        </ul>
      </div>

      {/* Submit Button */}
      <Button
        type="submit"
        className="w-full bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 text-white font-semibold py-6 text-lg rounded-xl shadow-lg hover:shadow-xl transition-all duration-300 hover:scale-[1.02] border-0"
        size="lg"
        disabled={isLoading}
      >
        {isLoading ? (
          <span className="flex items-center justify-center">
            <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            Analyzing...
          </span>
        ) : (
          'Analyze Business'
        )}
      </Button>
    </form>
  );
}