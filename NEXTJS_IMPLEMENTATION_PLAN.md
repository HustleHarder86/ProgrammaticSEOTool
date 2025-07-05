# Next.js Frontend Implementation Plan

## Overview
Build a modern, production-ready frontend for the Programmatic SEO Tool using Next.js 14, TypeScript, Tailwind CSS, and shadcn/ui components.

## Project Structure

```
frontend/
├── app/                          # Next.js 14 App Router
│   ├── layout.tsx               # Root layout with providers
│   ├── page.tsx                 # Landing page
│   ├── dashboard/               # Main dashboard
│   │   ├── page.tsx            # Dashboard overview
│   │   └── layout.tsx          # Dashboard layout
│   ├── projects/                # Project management
│   │   ├── page.tsx            # Projects list
│   │   ├── [id]/               # Individual project
│   │   │   ├── page.tsx        # Project details
│   │   │   ├── templates/      # Template management
│   │   │   ├── data/           # Data management
│   │   │   └── generate/       # Page generation
│   │   └── new/                # New project wizard
│   │       ├── page.tsx        # Step 1: Business Analysis
│   │       ├── templates/      # Step 2: Template Selection
│   │       └── data/           # Step 3: Data Import
│   └── api/                     # API route handlers (if needed)
├── components/                   # Reusable components
│   ├── ui/                      # shadcn/ui components
│   ├── layout/                  # Layout components
│   │   ├── Header.tsx
│   │   ├── Sidebar.tsx
│   │   └── Footer.tsx
│   ├── business/                # Business-specific components
│   │   ├── BusinessAnalyzer.tsx
│   │   ├── BusinessCard.tsx
│   │   └── TemplatesSuggestions.tsx
│   ├── templates/               # Template components
│   │   ├── TemplateEditor.tsx
│   │   ├── TemplatePreview.tsx
│   │   └── VariableExtractor.tsx
│   ├── data/                    # Data management components
│   │   ├── DataImporter.tsx
│   │   ├── CSVUploader.tsx
│   │   └── DataGrid.tsx
│   ├── generation/              # Page generation components
│   │   ├── GenerationSettings.tsx
│   │   ├── GenerationProgress.tsx
│   │   └── PagePreview.tsx
│   └── export/                  # Export components
│       ├── ExportOptions.tsx
│       └── ExportProgress.tsx
├── lib/                         # Utility functions
│   ├── api/                     # API client
│   │   ├── client.ts           # Axios/Fetch wrapper
│   │   ├── business.ts         # Business API calls
│   │   ├── templates.ts        # Template API calls
│   │   ├── data.ts             # Data API calls
│   │   └── generation.ts       # Generation API calls
│   ├── utils/                   # Utility functions
│   ├── hooks/                   # Custom React hooks
│   │   ├── useProjects.ts
│   │   ├── useWebSocket.ts
│   │   └── useFileUpload.ts
│   └── store/                   # Zustand stores
│       ├── projectStore.ts
│       ├── templateStore.ts
│       └── generationStore.ts
├── types/                       # TypeScript types
│   ├── api.ts                  # API response types
│   ├── business.ts             # Business types
│   ├── template.ts             # Template types
│   └── generation.ts           # Generation types
└── styles/                      # Global styles
    └── globals.css             # Tailwind imports

```

## Phase 1: Project Setup and Core Infrastructure (Week 1)

### 1.1 Initialize Next.js Project
```bash
npx create-next-app@latest frontend --typescript --tailwind --app --eslint
cd frontend
```

### 1.2 Install Core Dependencies
```bash
# UI Components
npx shadcn-ui@latest init
npx shadcn-ui@latest add button card dialog form input label select tabs toast

# State Management & Data Fetching
npm install @tanstack/react-query @tanstack/react-query-devtools
npm install zustand immer

# Forms & Validation
npm install react-hook-form @hookform/resolvers zod

# Utilities
npm install axios clsx tailwind-merge
npm install lucide-react recharts
npm install react-dropzone papaparse

# Development
npm install -D @types/papaparse
```

### 1.3 Configure Project
- Set up TypeScript strict mode
- Configure path aliases (@/components, @/lib, etc.)
- Set up environment variables (.env.local)
- Configure CORS in FastAPI backend
- Set up API client with interceptors

### 1.4 Create Base Layout
- Implement responsive layout with sidebar navigation
- Create header with user menu and notifications
- Set up dark mode support
- Implement loading states and error boundaries

## Phase 2: Business Analysis Module (Week 2)

### 2.1 Landing Page
- Hero section with value proposition
- Feature highlights
- CTA to start new project
- Examples carousel

### 2.2 Business Analysis Flow
- URL input with validation
- Text description alternative
- Loading state with progress indicator
- Results display with:
  - Business summary
  - Suggested templates
  - Market insights
  - Next steps CTA

### 2.3 Template Suggestions
- Grid/list view of suggested templates
- Template preview with variables highlighted
- Selection mechanism
- Custom template option

## Phase 3: Template Management (Week 3)

### 3.1 Template Editor
- Rich text editor with variable insertion
- Variable placeholder syntax highlighting
- Live preview panel
- SEO fields (title, meta description)
- Save/load template functionality

### 3.2 Template Library
- Pre-built templates by industry
- Search and filter functionality
- Template preview cards
- Usage statistics
- Fork/duplicate templates

### 3.3 Variable Management
- Automatic variable extraction
- Variable type definition (text, number, date, etc.)
- Required/optional flags
- Default values
- Validation rules

## Phase 4: Data Management (Week 4)

### 4.1 Data Import
- CSV drag-and-drop uploader
- Column mapping interface
- Data validation and error handling
- Manual data entry form
- Bulk edit capabilities

### 4.2 Data Grid
- Sortable, filterable table
- Inline editing
- Bulk operations
- Export functionality
- Pagination

### 4.3 Data Validation
- Real-time validation feedback
- Error highlighting
- Suggested corrections
- Data quality score

## Phase 5: Page Generation (Week 5)

### 5.1 Generation Settings
- Select template and data source
- Preview generated combinations
- Set generation options:
  - Content variations
  - SEO optimization level
  - Output format

### 5.2 Generation Process
- Real-time progress tracking
- WebSocket connection for updates
- Pause/resume capability
- Error handling and retry
- Preview generated pages

### 5.3 Results Management
- Generated pages grid
- Individual page preview
- Bulk editing capabilities
- Quality checks
- SEO scoring

## Phase 6: Export & Integration (Week 6)

### 6.1 Export Options
- Format selection (CSV, JSON, WordPress XML)
- Field mapping for exports
- Batch export with progress
- Download management

### 6.2 CMS Integration
- WordPress direct publishing
- API integration setup
- Webhook configuration
- Publishing queue

### 6.3 Project Management
- Project dashboard
- Usage analytics
- Export history
- Team collaboration features

## Technical Implementation Details

### API Client Setup
```typescript
// lib/api/client.ts
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
    // Add auth token if available
    const token = localStorage.getItem('auth_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor
apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    // Handle common errors
    if (error.response?.status === 401) {
      // Redirect to login
    }
    return Promise.reject(error);
  }
);
```

### Zustand Store Example
```typescript
// lib/store/projectStore.ts
import { create } from 'zustand';
import { immer } from 'zustand/middleware/immer';

interface ProjectState {
  currentProject: Project | null;
  projects: Project[];
  isLoading: boolean;
  error: string | null;
  
  // Actions
  setCurrentProject: (project: Project) => void;
  fetchProjects: () => Promise<void>;
  createProject: (data: CreateProjectData) => Promise<void>;
}

export const useProjectStore = create<ProjectState>()(
  immer((set, get) => ({
    currentProject: null,
    projects: [],
    isLoading: false,
    error: null,
    
    setCurrentProject: (project) => {
      set((state) => {
        state.currentProject = project;
      });
    },
    
    fetchProjects: async () => {
      set((state) => {
        state.isLoading = true;
        state.error = null;
      });
      
      try {
        const response = await apiClient.get('/api/projects');
        set((state) => {
          state.projects = response.data;
          state.isLoading = false;
        });
      } catch (error) {
        set((state) => {
          state.error = error.message;
          state.isLoading = false;
        });
      }
    },
    
    createProject: async (data) => {
      // Implementation
    },
  }))
);
```

### React Query Setup
```typescript
// app/providers.tsx
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
            staleTime: 60 * 1000, // 1 minute
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
```

### WebSocket Integration
```typescript
// lib/hooks/useWebSocket.ts
import { useEffect, useRef, useState } from 'react';

export function useWebSocket(url: string) {
  const [isConnected, setIsConnected] = useState(false);
  const [lastMessage, setLastMessage] = useState<any>(null);
  const ws = useRef<WebSocket | null>(null);

  useEffect(() => {
    ws.current = new WebSocket(url);

    ws.current.onopen = () => {
      setIsConnected(true);
    };

    ws.current.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setLastMessage(data);
    };

    ws.current.onclose = () => {
      setIsConnected(false);
    };

    return () => {
      ws.current?.close();
    };
  }, [url]);

  const sendMessage = (message: any) => {
    if (ws.current?.readyState === WebSocket.OPEN) {
      ws.current.send(JSON.stringify(message));
    }
  };

  return { isConnected, lastMessage, sendMessage };
}
```

## UI/UX Guidelines

### Design Principles
1. **Clarity**: Clear visual hierarchy and intuitive navigation
2. **Feedback**: Immediate feedback for all user actions
3. **Progress**: Show progress for long-running operations
4. **Accessibility**: WCAG 2.1 AA compliance
5. **Responsive**: Mobile-first design approach

### Component Library
- Use shadcn/ui as base components
- Extend with custom business logic
- Maintain consistent spacing and sizing
- Use Tailwind CSS for styling
- Implement proper loading and error states

### Color Scheme
```css
/* Example color variables */
:root {
  --primary: #0070f3;
  --primary-dark: #0051cc;
  --success: #0cce6b;
  --warning: #ffa400;
  --error: #ff4757;
  --background: #ffffff;
  --foreground: #000000;
  --muted: #f4f4f5;
  --border: #e4e4e7;
}
```

## Testing Strategy

### Unit Tests
- Component testing with React Testing Library
- API client testing with MSW
- Store testing with Zustand
- Utility function testing

### Integration Tests
- User flow testing with Cypress
- API integration testing
- WebSocket connection testing

### E2E Tests
- Complete workflow testing
- Cross-browser testing
- Performance testing

## Deployment

### Vercel Deployment
```json
// vercel.json
{
  "functions": {
    "app/api/[...route].ts": {
      "maxDuration": 60
    }
  },
  "rewrites": [
    {
      "source": "/api/:path*",
      "destination": "https://your-api.vercel.app/api/:path*"
    }
  ]
}
```

### Environment Variables
```bash
# .env.local
NEXT_PUBLIC_API_URL=https://your-api.vercel.app
NEXT_PUBLIC_WS_URL=wss://your-api.vercel.app
NEXT_PUBLIC_SITE_URL=https://your-site.vercel.app
```

## Performance Optimization

1. **Code Splitting**: Use dynamic imports for large components
2. **Image Optimization**: Use Next.js Image component
3. **Caching**: Implement proper cache headers
4. **Bundle Size**: Monitor and optimize bundle size
5. **Lazy Loading**: Lazy load non-critical components

## Security Considerations

1. **Authentication**: Implement JWT-based auth
2. **CSRF Protection**: Use CSRF tokens
3. **Input Validation**: Validate all user inputs
4. **XSS Prevention**: Sanitize user content
5. **API Security**: Implement rate limiting

## Monitoring & Analytics

1. **Error Tracking**: Integrate Sentry
2. **Analytics**: Google Analytics or Plausible
3. **Performance**: Web Vitals monitoring
4. **User Feedback**: Implement feedback widget
5. **Usage Tracking**: Track feature usage

## Timeline Summary

- **Week 1**: Project setup and core infrastructure
- **Week 2**: Business analysis module
- **Week 3**: Template management
- **Week 4**: Data management
- **Week 5**: Page generation
- **Week 6**: Export & integration

Total estimated time: 6 weeks for MVP

## Next Steps

1. Set up the Next.js project structure
2. Implement the API client
3. Create the base layout and navigation
4. Build the business analysis flow
5. Iterate based on user feedback