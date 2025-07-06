"""Integration module to connect Template Builder Agent with existing template_generator.py"""
from typing import Dict, List, Any, Optional
from .template_builder import TemplateBuilderAgent
from api.template_generator import TemplateGenerator

class TemplateBuilderIntegration:
    """
    Integrates the Template Builder Agent with the existing Template Generator
    to provide enhanced validation, structure, and preview capabilities.
    """
    
    def __init__(self):
        self.builder = TemplateBuilderAgent()
        self.generator = TemplateGenerator()
    
    def create_validated_template(
        self,
        business_info: Dict[str, Any],
        template_type: str,
        custom_pattern: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a validated template based on business info
        
        Args:
            business_info: Business analysis data
            template_type: Type of template to create
            custom_pattern: Optional custom pattern override
            
        Returns:
            Created and validated template
        """
        # Get template suggestions from generator
        suggestions = self.generator.get_template_suggestions(
            business_info=business_info,
            use_ai=True
        )
        
        # Find matching template type
        matching_template = None
        for suggestion in suggestions:
            if suggestion.get('category') == template_type:
                matching_template = suggestion
                break
        
        if not matching_template:
            return {"error": f"No template found for type: {template_type}"}
        
        # Extract pattern and variables
        patterns = matching_template.get('templates', [])
        pattern = custom_pattern or (patterns[0] if patterns else "{variable}")
        
        # Create structured template with validation
        template_result = self.builder.create_template(
            name=matching_template.get('name', 'Custom Template'),
            pattern=pattern,
            structure={
                "title_template": self._generate_title_template(pattern, template_type),
                "meta_description_template": self._generate_meta_template(pattern, template_type),
                "h1_template": self._generate_h1_template(pattern, template_type),
                "url_pattern": self._generate_url_pattern(pattern),
                "content_sections": self._generate_content_sections(template_type, pattern)
            },
            template_type=template_type
        )
        
        return template_result
    
    def enhance_template_with_structure(
        self,
        template_category: str,
        business_info: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Enhance an existing template category with proper structure
        
        Args:
            template_category: Category from template_generator
            business_info: Business context
            
        Returns:
            Enhanced template with full structure
        """
        # Get the template configuration from generator
        template_config = self.generator.template_library.get(template_category, {})
        
        if not template_config:
            return {"error": f"Template category '{template_category}' not found"}
        
        # Extract first pattern as example
        patterns = template_config.get('templates', [])
        if not patterns:
            return {"error": "No patterns found in template"}
        
        pattern = patterns[0]
        
        # Create enhanced template
        enhanced = self.builder.create_template(
            name=f"{template_category.replace('_', ' ').title()} Template",
            pattern=pattern,
            structure={
                "title_template": self._generate_title_template(pattern, template_category),
                "meta_description_template": self._generate_meta_template(pattern, template_category),
                "h1_template": self._generate_h1_template(pattern, template_category),
                "url_pattern": self._generate_url_pattern(pattern),
                "content_sections": self._generate_content_sections(template_category, pattern)
            },
            template_type=template_category
        )
        
        # Add all pattern variations
        if enhanced["success"]:
            enhanced["template"]["all_patterns"] = patterns
            enhanced["template"]["variables_config"] = template_config.get('variables', {})
        
        return enhanced
    
    def generate_pages_with_validation(
        self,
        template_name: str,
        data: Dict[str, List[str]],
        limit: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Generate pages using template generator with validation from builder
        
        Args:
            template_name: Template to use
            data: Variable data
            limit: Max pages to generate
            
        Returns:
            Generated pages with validation status
        """
        # First validate the data
        validation = self.builder.validate_data_for_template(
            template_id=template_name,
            data_sets=data
        )
        
        if not validation["is_valid"]:
            return {
                "success": False,
                "errors": validation["errors"],
                "warnings": validation["warnings"]
            }
        
        # Estimate page count
        estimation = self.builder.estimate_page_count(
            template_id=template_name,
            data_sets=data
        )
        
        # Generate pages using template generator
        pages = self.generator.generate_pages_from_template(
            template_name=template_name,
            data=data,
            limit=limit
        )
        
        # Enhance pages with proper structure
        enhanced_pages = []
        for page in pages:
            # Get template structure from builder
            template = self.builder.get_template(template_name)
            if template and "seo_structure" in template:
                structure = template["seo_structure"]
                
                # Apply structure to page
                page["seo"] = {
                    "title": self.builder._fill_template(
                        structure.get("title_template", page["title"]),
                        page["variables"]
                    ),
                    "meta_description": self.builder._fill_template(
                        structure.get("meta_description_template", page["meta_description"]),
                        page["variables"]
                    ),
                    "h1": self.builder._fill_template(
                        structure.get("h1_template", page["title"]),
                        page["variables"]
                    )
                }
            
            enhanced_pages.append(page)
        
        return {
            "success": True,
            "validation": validation,
            "estimation": estimation,
            "pages": enhanced_pages,
            "total_generated": len(enhanced_pages)
        }
    
    def preview_template_variations(
        self,
        template_category: str,
        sample_data: Dict[str, str],
        num_variations: int = 3
    ) -> List[Dict[str, Any]]:
        """
        Preview multiple variations of a template
        
        Args:
            template_category: Template category to preview
            sample_data: Sample data for variables
            num_variations: Number of variations to show
            
        Returns:
            List of preview variations
        """
        template_config = self.generator.template_library.get(template_category, {})
        patterns = template_config.get('templates', [])[:num_variations]
        
        previews = []
        for pattern in patterns:
            # Extract variables from this pattern
            variables = self.builder.extract_variables(pattern)
            
            # Create temporary template for preview
            temp_template = {
                "pattern": pattern,
                "variables": variables,
                "structure": {
                    "title_template": self._generate_title_template(pattern, template_category),
                    "meta_description_template": self._generate_meta_template(pattern, template_category),
                    "url_pattern": self._generate_url_pattern(pattern)
                }
            }
            
            # Generate preview
            preview = self.builder.generate_preview(temp_template, sample_data)
            previews.append(preview)
        
        return previews
    
    # Helper methods for generating template structures
    
    def _generate_title_template(self, pattern: str, template_type: str) -> str:
        """Generate appropriate title template based on pattern and type"""
        if "location" in template_type:
            return pattern + " - Local Services & Reviews"
        elif "comparison" in template_type or "vs" in pattern:
            return pattern + " - Detailed Comparison Guide {year}"
        elif "how" in template_type:
            return "How to " + pattern + " - Step by Step Guide"
        elif "best" in pattern or "top" in pattern:
            return pattern + " - Expert Reviews & Recommendations"
        elif "price" in template_type or "pricing" in template_type:
            return pattern + " - Pricing Guide & Cost Analysis"
        else:
            return pattern + " - Complete Guide"
    
    def _generate_meta_template(self, pattern: str, template_type: str) -> str:
        """Generate meta description template"""
        if "location" in template_type:
            return f"Find the best {pattern}. Compare prices, read reviews, and book services online. Local professionals available."
        elif "comparison" in template_type:
            return f"Comparing {pattern}? See detailed analysis, features, pricing, and recommendations to make the best choice."
        elif "how" in template_type:
            return f"Learn {pattern} with our comprehensive guide. Step-by-step instructions and expert tips included."
        elif "product" in template_type:
            return f"Discover the best {pattern}. Expert reviews, comparisons, and buying guide to help you choose."
        else:
            return f"Everything you need to know about {pattern}. Comprehensive guide with expert insights and recommendations."
    
    def _generate_h1_template(self, pattern: str, template_type: str) -> str:
        """Generate H1 template"""
        if "comparison" in template_type or "vs" in pattern:
            return pattern + ": Which is Better?"
        elif "how" in template_type:
            return "How to " + pattern + ": Complete Guide"
        elif "best" in pattern:
            return pattern + " ({year} Updated)"
        else:
            return pattern
    
    def _generate_url_pattern(self, pattern: str) -> str:
        """Generate URL pattern from template pattern"""
        # Convert to lowercase and replace spaces/special chars
        url = pattern.lower()
        url = re.sub(r'[^a-z0-9\{\}]+', '-', url)
        url = re.sub(r'-+', '-', url)  # Remove multiple hyphens
        url = url.strip('-')
        
        # Ensure it starts with /
        if not url.startswith("/"):
            url = "/" + url
        
        return url
    
    def _generate_content_sections(self, template_type: str, pattern: str) -> List[Dict]:
        """Generate content sections based on template type"""
        if "location" in template_type:
            return [
                {"heading": "Overview", "content": f"Introduction to {pattern} services and options."},
                {"heading": "Service Areas", "content": "Areas we serve and coverage details."},
                {"heading": "Pricing", "content": "Transparent pricing and package options."},
                {"heading": "Why Choose Us", "content": "Benefits and advantages of our services."}
            ]
        elif "comparison" in template_type:
            return [
                {"heading": "Quick Comparison", "content": f"Key differences in {pattern}."},
                {"heading": "Detailed Analysis", "content": "In-depth look at each option."},
                {"heading": "Pros and Cons", "content": "Advantages and disadvantages compared."},
                {"heading": "Recommendation", "content": "Which option is best for your needs."}
            ]
        elif "how" in template_type:
            return [
                {"heading": "What You'll Learn", "content": f"Overview of {pattern} process."},
                {"heading": "Requirements", "content": "What you need before starting."},
                {"heading": "Step-by-Step Guide", "content": "Detailed instructions to follow."},
                {"heading": "Tips & Best Practices", "content": "Expert advice for best results."}
            ]
        else:
            return [
                {"heading": "Introduction", "content": f"Overview of {pattern}."},
                {"heading": "Key Information", "content": "Important details to know."},
                {"heading": "Benefits", "content": "Advantages and benefits."},
                {"heading": "Getting Started", "content": "How to begin and next steps."}
            ]

import re  # Add this import at the top of the file