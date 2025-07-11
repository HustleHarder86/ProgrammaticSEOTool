'use client';

import { useEffect, useState } from 'react';

interface LoadingAnimationProps {
  message?: string;
  steps?: string[];
}

export function LoadingAnimation({ 
  message = 'Analyzing your business...', 
  steps = [
    'Extracting business information',
    'Identifying programmatic SEO opportunities',
    'Generating template suggestions'
  ]
}: LoadingAnimationProps) {
  const [currentStep, setCurrentStep] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentStep((prev) => (prev + 1) % steps.length);
    }, 2000);
    return () => clearInterval(interval);
  }, [steps.length]);

  return (
    <div className="flex flex-col items-center justify-center py-20">
      {/* Main loader */}
      <div className="relative mb-8">
        <div className="w-24 h-24 rounded-full border-4 border-purple-200 animate-pulse"></div>
        <div className="absolute inset-0 w-24 h-24 rounded-full border-4 border-t-purple-600 border-r-purple-600 animate-spin"></div>
        <div className="absolute inset-2 w-20 h-20 rounded-full bg-gradient-to-br from-purple-100 to-blue-100 animate-pulse"></div>
        <div className="absolute inset-0 flex items-center justify-center">
          <svg className="w-10 h-10 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
          </svg>
        </div>
      </div>
      
      {/* Loading message */}
      <h3 className="text-2xl font-bold text-gray-900 mb-6">{message}</h3>
      
      {/* Animated steps */}
      <div className="space-y-4 w-full max-w-md">
        {steps.map((step, index) => (
          <div
            key={index}
            className={`flex items-center p-4 rounded-xl transition-all duration-500 ${
              index === currentStep
                ? 'bg-gradient-to-r from-purple-50 to-blue-50 border border-purple-200 shadow-md scale-105'
                : index < currentStep
                ? 'bg-green-50 border border-green-200'
                : 'bg-gray-50 border border-gray-200 opacity-60'
            }`}
          >
            <div className={`w-8 h-8 rounded-full flex items-center justify-center mr-4 transition-all duration-500 ${
              index === currentStep
                ? 'bg-gradient-to-br from-purple-600 to-blue-600 animate-pulse'
                : index < currentStep
                ? 'bg-green-500'
                : 'bg-gray-300'
            }`}>
              {index < currentStep ? (
                <svg className="w-5 h-5 text-white" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                </svg>
              ) : index === currentStep ? (
                <div className="w-4 h-4 bg-white rounded-full animate-pulse"></div>
              ) : (
                <div className="w-2 h-2 bg-gray-400 rounded-full"></div>
              )}
            </div>
            <span className={`text-base font-medium transition-all duration-500 ${
              index === currentStep ? 'text-purple-700' : index < currentStep ? 'text-green-700' : 'text-gray-500'
            }`}>
              {step}
            </span>
          </div>
        ))}
      </div>
      
      {/* Progress text */}
      <p className="mt-8 text-sm text-gray-500 animate-pulse">
        This usually takes 10-15 seconds...
      </p>
    </div>
  );
}