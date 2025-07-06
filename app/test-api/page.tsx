'use client';

import { useState } from 'react';
import { apiClient } from '@/lib/api/client';

interface APIResponse {
  status?: string;
  service?: string;
  message?: string;
  timestamp?: string;
}

export default function TestAPIPage() {
  const [result, setResult] = useState<APIResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const testHealth = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await apiClient.get<APIResponse>('/health');
      setResult(response.data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    }
    setLoading(false);
  };

  const testAPI = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await apiClient.get<APIResponse>('/api/test');
      setResult(response.data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    }
    setLoading(false);
  };

  return (
    <div className="container mx-auto p-8">
      <h1 className="text-3xl font-bold mb-8">API Connection Test</h1>
      
      <div className="space-y-4">
        <div>
          <button
            onClick={testHealth}
            disabled={loading}
            className="bg-blue-500 text-white px-4 py-2 rounded mr-4 disabled:opacity-50"
          >
            Test Health Endpoint
          </button>
          
          <button
            onClick={testAPI}
            disabled={loading}
            className="bg-green-500 text-white px-4 py-2 rounded disabled:opacity-50"
          >
            Test API Endpoint
          </button>
        </div>

        {loading && <p>Loading...</p>}
        
        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
            Error: {error}
          </div>
        )}
        
        {result && (
          <div className="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded">
            <pre>{JSON.stringify(result, null, 2)}</pre>
          </div>
        )}
      </div>
    </div>
  );
}