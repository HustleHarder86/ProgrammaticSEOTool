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
  template_type: string;
  template_html: string;
  variables: TemplateVariable[];
  seo_settings: SeoSettings;
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