import axios from 'axios';

// Use relative paths for Vercel deployment compatibility
const API_URL = process.env.NEXT_PUBLIC_API_URL || '';

export const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
apiClient.interceptors.request.use(
  (config) => {
    // Add any auth headers here if needed
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor
apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    // Handle common errors
    console.error('API Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

// Export API methods
export const exportAPI = {
  // Start a new export
  startExport: (projectId: string, format: string, options?: Record<string, unknown>) =>
    apiClient.post(`/api/projects/${projectId}/export`, { format, options }),

  // Get export status
  getExportStatus: (exportId: string) =>
    apiClient.get(`/api/exports/${exportId}/status`),

  // Download export file
  downloadExport: (exportId: string) =>
    fetch(`${API_URL}/api/exports/${exportId}/download`),

  // List project exports
  listProjectExports: (projectId: string) =>
    apiClient.get(`/api/projects/${projectId}/exports`),

  // List all exports
  listAllExports: () =>
    apiClient.get('/api/exports'),

  // Cancel export
  cancelExport: (exportId: string) =>
    apiClient.delete(`/api/exports/${exportId}`),

  // Cleanup old exports
  cleanupOldExports: (daysOld: number = 7) =>
    apiClient.post('/api/exports/cleanup', { days_old: daysOld })
};