'use client';

interface LoadingAnimationProps {
  message?: string;
}

export function LoadingAnimation({ message = 'Analyzing your business...' }: LoadingAnimationProps) {
  return (
    <div className="flex flex-col items-center justify-center py-16">
      {/* Animated dots loader */}
      <div className="flex space-x-2 mb-6">
        <div className="w-3 h-3 bg-blue-500 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
        <div className="w-3 h-3 bg-blue-500 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
        <div className="w-3 h-3 bg-blue-500 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
      </div>
      
      {/* Loading message */}
      <p className="text-lg font-medium text-gray-700 mb-2">{message}</p>
      
      {/* Substeps */}
      <div className="space-y-2 text-sm text-gray-500 text-center">
        <p className="flex items-center">
          <span className="inline-block w-4 h-4 mr-2">
            <svg className="animate-spin h-4 w-4 text-gray-400" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
          </span>
          Extracting business information...
        </p>
        <p>Identifying programmatic SEO opportunities...</p>
        <p>Generating template suggestions...</p>
      </div>
    </div>
  );
}