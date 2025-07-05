#!/bin/bash

# Setup script for Next.js frontend

echo "Setting up Next.js frontend for Programmatic SEO Tool..."

# Create Next.js app with TypeScript, Tailwind, and App Router
npx create-next-app@latest frontend --typescript --tailwind --app --eslint --no-git --import-alias "@/*"

cd frontend

echo "Installing core dependencies..."

# UI Components and styling
npm install @radix-ui/react-dialog @radix-ui/react-dropdown-menu @radix-ui/react-label @radix-ui/react-select @radix-ui/react-slot @radix-ui/react-tabs @radix-ui/react-toast
npm install class-variance-authority clsx tailwind-merge lucide-react

# State management and data fetching
npm install @tanstack/react-query @tanstack/react-query-devtools zustand immer

# Forms and validation
npm install react-hook-form @hookform/resolvers zod

# Data handling
npm install axios recharts react-dropzone papaparse

# Development dependencies
npm install -D @types/papaparse

echo "Setting up shadcn/ui..."
npx shadcn-ui@latest init -y

echo "Adding initial shadcn/ui components..."
npx shadcn-ui@latest add button card dialog form input label select tabs toast badge skeleton alert

echo "Creating directory structure..."
mkdir -p components/{layout,business,templates,data,generation,export}
mkdir -p lib/{api,utils,hooks,store}
mkdir -p types
mkdir -p app/{dashboard,projects,api}

echo "Creating environment file..."
cat > .env.local << EOL
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_NAME=Programmatic SEO Tool
NEXT_PUBLIC_APP_DESCRIPTION=Generate thousands of SEO-optimized pages automatically
EOL

echo "Creating basic API client..."
cat > lib/api/client.ts << 'EOL'
import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
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
EOL

echo "Creating providers component..."
cat > app/providers.tsx << 'EOL'
'use client';

import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ReactQueryDevtools } from '@tanstack/react-query-devtools';
import { useState } from 'react';

export function Providers({ children }: { children: React.ReactNode }) {
  const [queryClient] = useState(
    () =>
      new QueryClient({
        defaultOptions: {
          queries: {
            staleTime: 60 * 1000,
            refetchOnWindowFocus: false,
          },
        },
      })
  );

  return (
    <QueryClientProvider client={queryClient}>
      {children}
      <ReactQueryDevtools initialIsOpen={false} />
    </QueryClientProvider>
  );
}
EOL

echo "Updating layout to include providers..."
cat > app/layout.tsx << 'EOL'
import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import './globals.css';
import { Providers } from './providers';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'Programmatic SEO Tool',
  description: 'Generate thousands of SEO-optimized pages automatically',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}
EOL

echo "Frontend setup complete!"
echo ""
echo "To start the frontend:"
echo "  cd frontend"
echo "  npm run dev"
echo ""
echo "The frontend will be available at http://localhost:3000"
echo "Make sure the backend is running at http://localhost:8000"