export interface Project {
  id: string;
  name: string;
  business_input: string;
  business_analysis: {
    business_name?: string;
    business_description?: string;
    target_audience?: string;
    core_offerings?: string[];
    template_opportunities?: TemplateOpportunity[];
  };
  created_at: string;
  updated_at?: string;
}

export interface TemplateOpportunity {
  template_name: string;
  template_pattern: string;
  example_pages: string[];
  estimated_pages: number;
  difficulty: string;
}

export interface Template {
  id: string;
  project_id: string;
  name: string;
  pattern: string;
  template_type?: string;
  template_html?: string;
  variables: string[];
  seo_settings?: SeoSettings;
  template_sections?: {
    seo_structure?: {
      title_template?: string;
      meta_description_template?: string;
      h1_template?: string;
    };
    content_sections?: Array<{
      type: string;
      content: string;
    }>;
  };
  created_at: string;
  updated_at?: string;
}

export interface TemplateVariable {
  name: string;
  type: string;
  description?: string;
  example?: string;
  required?: boolean;
}

export interface SeoSettings {
  meta_title?: string;
  meta_description?: string;
  keywords?: string[];
  h1_tag?: string;
  canonical_url?: string;
}

export interface Dataset {
  id: string;
  project_id: string;
  name: string;
  columns: string[];
  data: Record<string, any>[];
  created_at: string;
  updated_at?: string;
}

export interface GeneratedPage {
  id: string;
  project_id: string;
  template_id: string;
  title: string;
  slug: string;
  content: string;
  seo_title: string;
  seo_description: string;
  seo_keywords: string[];
  variables: Record<string, any>;
  created_at: string;
}

export interface GenerationConfig {
  template_id: string;
  dataset_id: string;
  generation_settings: {
    max_pages?: number;
    include_variations?: boolean;
    uniqueness_threshold?: number;
    output_format?: 'html' | 'markdown';
  };
}

export interface GenerationResult {
  status: 'pending' | 'in_progress' | 'completed' | 'failed';
  total_pages: number;
  generated_pages: number;
  failed_pages: number;
  preview_pages: GeneratedPage[];
  errors?: string[];
}

export interface GenerationProgress {
  current_page: number;
  total_pages: number;
  status: string;
  estimated_time_remaining?: number;
  errors?: string[];
}

export interface PageGenerationWizardStep {
  id: string;
  title: string;
  description: string;
  completed: boolean;
  active: boolean;
}

export interface ExportOptions {
  format: 'csv' | 'json' | 'wordpress' | 'html';
  include_seo: boolean;
  include_variables: boolean;
  filename?: string;
}

export interface ExportJob {
  id: string;
  project_id: string;
  format: string;
  status: 'pending' | 'in_progress' | 'completed' | 'failed' | 'cancelled';
  progress: number;
  total_items: number;
  processed_items: number;
  created_at: string;
  started_at?: string;
  completed_at?: string;
  error_message?: string;
  download_url?: string;
}

export interface ExportRequest {
  format: string;
  options?: Record<string, any>;
}

export interface ExportResponse {
  export_id: string;
  status: string;
  message: string;
}

export interface ExportFormat {
  id: string;
  name: string;
  description: string;
  icon: React.ComponentType<{ className?: string }>;
  fileExtension: string;
  recommended?: boolean;
  options?: ExportFormatOption[];
}

export interface ExportFormatOption {
  id: string;
  name: string;
  description: string;
  type: 'boolean' | 'select' | 'text' | 'number';
  defaultValue: any;
  options?: { value: string; label: string }[];
}