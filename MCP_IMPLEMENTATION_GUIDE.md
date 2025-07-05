# MCP Implementation Guide for Programmatic SEO Tool

## Overview
This guide explains how to use the Model Context Protocol (MCP) configurations to build the Next.js frontend following CLAUDE.md best practices.

## MCP Files Created

1. **frontend_setup.mcp.json** - Initial Next.js setup and configuration
2. **cors_config.mcp.json** - CORS configuration for API integration  
3. **landing_page.mcp.json** - Landing page components
4. **business_analysis_wizard.mcp.json** - Step 1 of the workflow
5. **template_builder.mcp.json** - Step 2 of the workflow
6. **data_generation.mcp.json** - Step 3 of the workflow
7. **project_dashboard.mcp.json** - Project management interface

## Implementation Order

### Phase 1: Foundation (Priority: High)
1. **Frontend Setup** (`frontend_setup.mcp.json`)
   - Run `./setup_frontend.sh`
   - Verify structure and dependencies
   - Configure environment variables

2. **CORS Configuration** (`cors_config.mcp.json`)
   - Update `app/main.py` with CORS middleware
   - Test with frontend requests

### Phase 2: Core Features (Priority: High)
3. **Landing Page** (`landing_page.mcp.json`)
   - Create hero section
   - Build features grid
   - Add how-it-works section
   - Implement examples carousel

4. **Business Analysis** (`business_analysis_wizard.mcp.json`)
   - Build input form with validation
   - Create progress indicator
   - Display template suggestions
   - Show market insights

5. **Template Builder** (`template_builder.mcp.json`)
   - Implement rich text editor
   - Add variable management
   - Create live preview
   - Build template library

6. **Data & Generation** (`data_generation.mcp.json`)
   - Create file upload interface
   - Build column mapping
   - Implement generation progress
   - Add results viewer

### Phase 3: Enhancement (Priority: Medium)
7. **Project Dashboard** (`project_dashboard.mcp.json`)
   - Create projects list
   - Add dashboard stats
   - Build detail views

## Key Implementation Principles (from CLAUDE.md)

### 1. Template First
Always think in terms of templates and data, not individual pages.

### 2. Universal Design
Ensure features work for ANY business type.

### 3. Simplicity
- Make every task and code change as simple as possible
- Avoid massive or complex changes
- Every change should impact as little code as possible

### 4. Workflow Rules
1. First think through the problem
2. Create checkable todo items
3. Check in before starting
4. Work systematically
5. Provide high-level explanations
6. Keep it simple
7. Add review section

## Component Structure Example

Following the MCP specifications, here's how to structure a component:

```typescript
// frontend/components/business/BusinessInputForm.tsx
import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { useBusinessStore } from '@/lib/store/businessStore';

const schema = z.object({
  url: z.string().url().optional(),
  description: z.string().min(50).optional(),
}).refine(data => data.url || data.description, {
  message: "Either URL or description is required"
});

export function BusinessInputForm() {
  const { analyzeBusiness, isAnalyzing } = useBusinessStore();
  const form = useForm({
    resolver: zodResolver(schema)
  });

  const onSubmit = async (data) => {
    await analyzeBusiness(data);
  };

  return (
    <form onSubmit={form.handleSubmit(onSubmit)}>
      {/* Implementation following MCP spec */}
    </form>
  );
}
```

## API Integration Pattern

Following the MCP specifications:

```typescript
// frontend/lib/api/business.ts
import { apiClient } from './client';

export const businessAPI = {
  analyze: async (data: { url?: string; description?: string }) => {
    const response = await apiClient.post('/api/analyze-business', data);
    return response.data;
  },
  
  getTemplates: async (businessId: string) => {
    const response = await apiClient.get(`/api/businesses/${businessId}/templates`);
    return response.data;
  }
};
```

## State Management Pattern

Using Zustand as specified:

```typescript
// frontend/lib/store/businessStore.ts
import { create } from 'zustand';
import { immer } from 'zustand/middleware/immer';
import { businessAPI } from '@/lib/api/business';

interface BusinessState {
  businessData: any;
  selectedTemplates: string[];
  isAnalyzing: boolean;
  error: string | null;
  
  analyzeBusiness: (data: any) => Promise<void>;
  selectTemplate: (templateId: string) => void;
}

export const useBusinessStore = create<BusinessState>()(
  immer((set, get) => ({
    businessData: null,
    selectedTemplates: [],
    isAnalyzing: false,
    error: null,
    
    analyzeBusiness: async (data) => {
      set(state => {
        state.isAnalyzing = true;
        state.error = null;
      });
      
      try {
        const result = await businessAPI.analyze(data);
        set(state => {
          state.businessData = result;
          state.isAnalyzing = false;
        });
      } catch (error) {
        set(state => {
          state.error = error.message;
          state.isAnalyzing = false;
        });
      }
    },
    
    selectTemplate: (templateId) => {
      set(state => {
        state.selectedTemplates.push(templateId);
      });
    }
  }))
);
```

## Testing Checklist

For each MCP implementation:
- [ ] Component renders correctly
- [ ] API integration works
- [ ] State management updates properly
- [ ] Error handling is graceful
- [ ] Loading states are shown
- [ ] Mobile responsive
- [ ] Accessibility compliant

## Common Pitfalls to Avoid

1. **Don't over-engineer** - Keep components simple and focused
2. **Don't skip validation** - Always validate user input
3. **Don't ignore errors** - Handle all error cases gracefully
4. **Don't forget loading states** - Users need feedback
5. **Don't break mobile** - Test responsive design

## Next Steps

1. Run the frontend setup script
2. Start with CORS configuration
3. Build components in order of priority
4. Test each component thoroughly
5. Move to the next MCP implementation

Remember: Simplicity is key. Every change should be as minimal and focused as possible.