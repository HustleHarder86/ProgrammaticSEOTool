"""Template Engine for handling template operations"""
from typing import List, Dict, Any, Optional
import re

class TemplateEngine:
    """Engine for template operations including variable extraction, validation, and preview generation"""
    
    def __init__(self):
        pass
    
    def extract_variables(self, template_string: str) -> List[str]:
        """
        Extract variables from template strings using {variable} syntax
        
        Args:
            template_string: String containing template with {variable} placeholders
            
        Returns:
            List of unique variable names
        """
        # Extract variables using regex for {variable} pattern
        variables = re.findall(r'\{(\w+)\}', template_string)
        
        # Return unique variables while preserving order
        seen = set()
        unique_vars = []
        for var in variables:
            if var not in seen:
                seen.add(var)
                unique_vars.append(var)
        
        return unique_vars
    
    def validate_template(self, template_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate template structure and content
        
        Args:
            template_data: Template data including pattern, sections, etc.
            
        Returns:
            Validation result with is_valid flag and any errors/warnings
        """
        errors = []
        warnings = []
        
        # Check required fields
        if not template_data.get('name'):
            errors.append("Template name is required")
        
        if not template_data.get('pattern'):
            errors.append("Template pattern is required")
        
        # Extract variables from pattern and all sections
        all_template_text = [template_data.get('pattern', '')]
        
        # Add title template
        if template_data.get('title_template'):
            all_template_text.append(template_data['title_template'])
        
        # Add meta description
        if template_data.get('meta_description_template'):
            all_template_text.append(template_data['meta_description_template'])
        
        # Add content sections
        for section in template_data.get('content_sections', []):
            if section.get('heading'):
                all_template_text.append(section['heading'])
            if section.get('content'):
                all_template_text.append(section['content'])
        
        # Extract all variables
        all_variables = set()
        for text in all_template_text:
            variables = self.extract_variables(text)
            all_variables.update(variables)
        
        if not all_variables:
            errors.append("Template must contain at least one {variable} placeholder")
        
        # Validate variable names
        for var in all_variables:
            if not re.match(r'^[a-zA-Z][a-zA-Z0-9_]*$', var):
                errors.append(f"Invalid variable name: {var}. Must start with a letter and contain only letters, numbers, and underscores")
        
        # Check SEO guidelines
        if template_data.get('title_template'):
            sample_title = self._fill_sample_template(template_data['title_template'], all_variables)
            if len(sample_title) > 60:
                warnings.append(f"Title might be too long. Recommended: 50-60 characters")
        
        if template_data.get('meta_description_template'):
            sample_meta = self._fill_sample_template(template_data['meta_description_template'], all_variables)
            if len(sample_meta) > 160:
                warnings.append(f"Meta description might be too long. Maximum: 160 characters")
        
        return {
            'is_valid': len(errors) == 0,
            'errors': errors,
            'warnings': warnings,
            'variables': list(all_variables)
        }
    
    def generate_preview(self, template_data: Dict[str, Any], sample_data: Dict[str, str]) -> Dict[str, Any]:
        """
        Generate a preview of the template with sample data
        
        Args:
            template_data: Template structure with patterns and sections
            sample_data: Sample values for variables
            
        Returns:
            Preview with filled content
        """
        preview = {
            'pattern': template_data.get('pattern', ''),
            'filled_pattern': self._fill_template(template_data.get('pattern', ''), sample_data),
            'seo': {},
            'content_sections': []
        }
        
        # Fill SEO elements
        if template_data.get('title_template'):
            preview['seo']['title'] = self._fill_template(template_data['title_template'], sample_data)
        
        if template_data.get('meta_description_template'):
            preview['seo']['meta_description'] = self._fill_template(template_data['meta_description_template'], sample_data)
        
        if template_data.get('h1_template'):
            preview['seo']['h1'] = self._fill_template(template_data['h1_template'], sample_data)
        
        # Generate URL slug
        if template_data.get('pattern'):
            slug = self._fill_template(template_data['pattern'], sample_data)
            slug = slug.lower().strip()
            slug = re.sub(r'[^\w\s-]', '', slug)
            slug = re.sub(r'[-\s]+', '-', slug)
            preview['seo']['url'] = f"/{slug}"
        
        # Fill content sections
        for section in template_data.get('content_sections', []):
            filled_section = {}
            if section.get('heading'):
                filled_section['heading'] = self._fill_template(section['heading'], sample_data)
            if section.get('content'):
                filled_section['content'] = self._fill_template(section['content'], sample_data)
            preview['content_sections'].append(filled_section)
        
        preview['sample_data'] = sample_data
        
        return preview
    
    def _fill_template(self, template_string: str, data: Dict[str, str]) -> str:
        """Fill template string with data values"""
        result = template_string
        for key, value in data.items():
            result = result.replace(f"{{{key}}}", str(value))
        return result
    
    def _fill_sample_template(self, template_string: str, variables: set) -> str:
        """Fill template with sample data for validation"""
        sample_data = {
            'location': 'Toronto',
            'city': 'Toronto',
            'service': 'plumbing',
            'product': 'software',
            'item': 'product',
            'action': 'install',
            'topic': 'solar panels',
            'category': 'premium',
            'type': 'professional',
            'industry': 'technology',
            'feature': 'automation'
        }
        
        # Add generic sample for any variable not in our samples
        for var in variables:
            if var not in sample_data:
                sample_data[var] = f"Sample {var.title()}"
        
        return self._fill_template(template_string, sample_data)
    
    def create_template_structure(self, template_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a complete template structure from template data
        
        Args:
            template_data: Raw template data from request
            
        Returns:
            Structured template ready for storage
        """
        # Extract variables from all template text
        variables = self.extract_variables(template_data.get('pattern', ''))
        
        # Add variables from other fields
        for field in ['title_template', 'meta_description_template', 'h1_template']:
            if template_data.get(field):
                variables.extend(self.extract_variables(template_data[field]))
        
        # Add variables from content sections
        for section in template_data.get('content_sections', []):
            if section.get('heading'):
                variables.extend(self.extract_variables(section['heading']))
            if section.get('content'):
                variables.extend(self.extract_variables(section['content']))
        
        # Get unique variables
        unique_variables = list(dict.fromkeys(variables))
        
        return {
            'name': template_data.get('name'),
            'pattern': template_data.get('pattern'),
            'variables': unique_variables,
            'seo_structure': {
                'title_template': template_data.get('title_template', '{title}'),
                'meta_description_template': template_data.get('meta_description_template', '{description}'),
                'h1_template': template_data.get('h1_template', template_data.get('pattern', '{heading}'))
            },
            'content_sections': template_data.get('content_sections', []),
            'template_type': template_data.get('template_type', 'custom')
        }