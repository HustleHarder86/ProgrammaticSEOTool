import axios from 'axios';

// Use relative paths since frontend and backend are in the same deployment
export const apiClient = axios.create({
  baseURL: '', // Empty base URL means relative to current domain
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