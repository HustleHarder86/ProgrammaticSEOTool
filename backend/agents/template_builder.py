"""Template Builder Agent - Creates and manages reusable page templates for programmatic SEO"""
from typing import List, Dict, Any, Optional, Tuple
import re
import json
from datetime import datetime
import itertools

class TemplateBuilderAgent:
    """
    Agent responsible for creating, validating, and managing SEO page templates.
    Converts template patterns into structured templates with validation and preview capabilities.
    """
    
    def __init__(self):
        """Initialize the Template Builder Agent"""
        self.templates = {}
        self.template_library = self._initialize_template_library()
        
    def _initialize_template_library(self) -> Dict[str, Dict]:
        """Initialize with pre-built template patterns"""
        return {
            "location_service": {
                "name": "Location + Service Template",
                "description": "For location-based service businesses",
                "patterns": [
                    "{location} {service}",
                    "best {service} in {location}",
                    "{service} near me {location}",
                    "affordable {service} {location}",
                    "{location} {service} {year}"
                ],
                "required_variables": ["location", "service"],
                "optional_variables": ["year", "price_range", "business_attribute"],
                "seo_structure": {
                    "title_template": "{service} in {location} - Professional Services",
                    "meta_description_template": "Find the best {service} in {location}. Compare prices, read reviews, and book online.",
                    "h1_template": "{service} Services in {location}",
                    "url_pattern": "/{location}-{service}"
                }
            },
            "comparison": {
                "name": "Comparison Template",
                "description": "For comparing products, services, or options",
                "patterns": [
                    "{item1} vs {item2}",
                    "{item1} or {item2} which is better",
                    "compare {item1} and {item2} {metric}",
                    "{item1} vs {item2} for {use_case}",
                    "{item1} alternatives to {item2}"
                ],
                "required_variables": ["item1", "item2"],
                "optional_variables": ["metric", "use_case", "year"],
                "seo_structure": {
                    "title_template": "{item1} vs {item2} - Detailed Comparison {year}",
                    "meta_description_template": "Compare {item1} and {item2}. See features, pricing, pros and cons to make the best choice.",
                    "h1_template": "{item1} vs {item2}: Which is Better?",
                    "url_pattern": "/{item1}-vs-{item2}"
                }
            },
            "how_to": {
                "name": "How-To Template",
                "description": "For instructional and tutorial content",
                "patterns": [
                    "how to {action} {topic}",
                    "how to {action} {topic} {modifier}",
                    "guide to {action} {topic}",
                    "step by step {action} {topic}",
                    "{action} {topic} tutorial"
                ],
                "required_variables": ["action", "topic"],
                "optional_variables": ["modifier", "audience", "year"],
                "seo_structure": {
                    "title_template": "How to {action} {topic} - Complete Guide {year}",
                    "meta_description_template": "Learn how to {action} {topic} with our step-by-step guide. Easy instructions for beginners.",
                    "h1_template": "How to {action} {topic}: Step-by-Step Guide",
                    "url_pattern": "/how-to-{action}-{topic}"
                }
            },
            "best_for": {
                "name": "Best X for Y Template",
                "description": "For recommendation and listicle content",
                "patterns": [
                    "best {product_type} for {use_case}",
                    "top {number} {product_type} {category}",
                    "{product_type} for {audience} {year}",
                    "{product_type} under {price}",
                    "recommended {product_type} {modifier}"
                ],
                "required_variables": ["product_type"],
                "optional_variables": ["use_case", "audience", "year", "price", "number", "category", "modifier"],
                "seo_structure": {
                    "title_template": "Best {product_type} for {use_case} - Top Picks {year}",
                    "meta_description_template": "Discover the best {product_type} for {use_case}. Expert reviews and recommendations to help you choose.",
                    "h1_template": "Best {product_type} for {use_case}",
                    "url_pattern": "/best-{product_type}-for-{use_case}"
                }
            },
            "question": {
                "name": "Question-Based Template",
                "description": "For FAQ and question-answering content",
                "patterns": [
                    "what is {topic}",
                    "why {question} {topic}",
                    "when to {action} {topic}",
                    "where to {action} {topic}",
                    "is {topic} {attribute}"
                ],
                "required_variables": ["topic"],
                "optional_variables": ["question", "action", "attribute"],
                "seo_structure": {
                    "title_template": "What is {topic}? Everything You Need to Know",
                    "meta_description_template": "Get answers about {topic}. Learn what it is, how it works, and why it matters.",
                    "h1_template": "What is {topic}?",
                    "url_pattern": "/what-is-{topic}"
                }
            }
        }
    
    def create_template(
        self,
        name: str,
        pattern: str,
        structure: Dict[str, Any],
        template_type: str = "custom"
    ) -> Dict[str, Any]:
        """
        Create a new template with variable placeholders
        
        Args:
            name: Template name
            pattern: Template pattern with {variables}
            structure: Page structure (title, meta, content sections)
            template_type: Type of template
            
        Returns:
            Created template with validation results
        """
        # Extract variables from pattern
        variables = self.extract_variables(pattern)
        
        # Validate the template
        validation = self.validate_template({
            "name": name,
            "pattern": pattern,
            "variables": variables,
            "structure": structure,
            "type": template_type
        })
        
        if not validation["is_valid"]:
            return {
                "success": False,
                "errors": validation["errors"],
                "warnings": validation["warnings"]
            }
        
        # Create URL pattern
        url_pattern = self._generate_url_pattern(pattern)
        
        # Store template
        template = {
            "id": f"{template_type}_{name.lower().replace(' ', '_')}",
            "name": name,
            "pattern": pattern,
            "variables": variables,
            "required_variables": variables,  # All extracted variables are required by default
            "optional_variables": [],
            "structure": structure,
            "type": template_type,
            "url_pattern": url_pattern,
            "created_at": datetime.now().isoformat(),
            "validation": validation
        }
        
        self.templates[template["id"]] = template
        
        return {
            "success": True,
            "template": template,
            "preview": self.generate_preview(template, self._get_sample_data(variables))
        }
    
    def extract_variables(self, template_pattern: str) -> List[str]:
        """
        Extract all variables from template pattern
        
        Args:
            template_pattern: Pattern like "[City] [Service] Prices"
            
        Returns:
            List of variable names
        """
        # Support both {variable} and [variable] syntax
        curly_vars = re.findall(r'\{(\w+)\}', template_pattern)
        square_vars = re.findall(r'\[(\w+)\]', template_pattern)
        
        # Combine and deduplicate
        all_vars = list(set(curly_vars + square_vars))
        
        return all_vars
    
    def validate_template(self, template: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate template syntax and SEO-friendliness
        
        Args:
            template: Template to validate
            
        Returns:
            Validation results with errors and warnings
        """
        errors = []
        warnings = []
        
        # Check for required fields
        required_fields = ["name", "pattern"]
        for field in required_fields:
            if field not in template or not template[field]:
                errors.append(f"Missing required field: {field}")
        
        if "pattern" in template:
            pattern = template["pattern"]
            
            # Check for variables
            variables = template.get("variables", [])
            if not variables:
                errors.append("Template must contain at least one variable")
            
            # Validate variable names
            for var in variables:
                if not re.match(r'^[a-zA-Z][a-zA-Z0-9_]*$', var):
                    errors.append(f"Invalid variable name: {var}. Must start with letter and contain only letters, numbers, and underscores")
            
            # Check for duplicate variables
            if len(variables) != len(set(variables)):
                errors.append("Template contains duplicate variables")
        
        # Validate structure if provided
        if "structure" in template:
            structure = template["structure"]
            
            # Check title template
            if "title_template" in structure:
                title = structure["title_template"]
                # Check title length (with sample data)
                sample_title = self._fill_template(title, self._get_sample_data(template.get("variables", [])))
                if len(sample_title) > 60:
                    warnings.append(f"Title may be too long ({len(sample_title)} chars). Recommended: 50-60 characters")
                elif len(sample_title) < 30:
                    warnings.append(f"Title may be too short ({len(sample_title)} chars). Recommended: 30-60 characters")
            
            # Check meta description
            if "meta_description_template" in structure:
                meta = structure["meta_description_template"]
                sample_meta = self._fill_template(meta, self._get_sample_data(template.get("variables", [])))
                if len(sample_meta) > 160:
                    warnings.append(f"Meta description too long ({len(sample_meta)} chars). Maximum: 160 characters")
                elif len(sample_meta) < 120:
                    warnings.append(f"Meta description may be too short ({len(sample_meta)} chars). Recommended: 120-160 characters")
            
            # Check URL pattern
            if "url_pattern" in structure:
                url = structure["url_pattern"]
                if not url.startswith("/"):
                    errors.append("URL pattern must start with /")
                if " " in url:
                    errors.append("URL pattern cannot contain spaces")
                if not all(c.isalnum() or c in "-_{}/." for c in url):
                    warnings.append("URL pattern contains special characters. Recommended: alphanumeric, hyphens, and slashes only")
        
        return {
            "is_valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings
        }
    
    def generate_preview(
        self,
        template: Dict[str, Any],
        sample_data: Dict[str, str]
    ) -> Dict[str, Any]:
        """
        Generate preview of how template will look with sample data
        
        Args:
            template: Template to preview
            sample_data: Sample values for variables
            
        Returns:
            Preview with filled content
        """
        preview = {
            "pattern": template.get("pattern", ""),
            "filled_pattern": self._fill_template(template.get("pattern", ""), sample_data),
            "structure": {}
        }
        
        # Fill structure elements
        if "structure" in template:
            structure = template["structure"]
            
            if "title_template" in structure:
                preview["structure"]["title"] = self._fill_template(structure["title_template"], sample_data)
            
            if "meta_description_template" in structure:
                preview["structure"]["meta_description"] = self._fill_template(structure["meta_description_template"], sample_data)
            
            if "h1_template" in structure:
                preview["structure"]["h1"] = self._fill_template(structure["h1_template"], sample_data)
            
            if "url_pattern" in structure:
                preview["structure"]["url"] = self._fill_template(structure["url_pattern"], sample_data).lower().replace(" ", "-")
            
            # Preview content sections if available
            if "content_sections" in structure:
                preview["structure"]["content_sections"] = []
                for section in structure["content_sections"]:
                    preview_section = {}
                    if "heading" in section:
                        preview_section["heading"] = self._fill_template(section["heading"], sample_data)
                    if "content" in section:
                        preview_section["content"] = self._fill_template(section["content"], sample_data)
                    preview["structure"]["content_sections"].append(preview_section)
        
        # Add sample variables used
        preview["sample_data"] = sample_data
        
        return preview
    
    def build_page_structure(
        self,
        template_id: str,
        custom_sections: Optional[List[Dict]] = None
    ) -> Dict[str, Any]:
        """
        Build complete page structure from template
        
        Args:
            template_id: ID of template to use
            custom_sections: Optional custom content sections
            
        Returns:
            Complete page structure
        """
        template = self.get_template(template_id)
        if not template:
            return {"error": "Template not found"}
        
        # Start with base structure
        base_structure = template.get("seo_structure", {})
        
        # Build default content sections if not provided
        if not custom_sections:
            custom_sections = self._generate_default_sections(template)
        
        page_structure = {
            "template_id": template_id,
            "template_name": template["name"],
            "seo": {
                "title_template": base_structure.get("title_template", "{title}"),
                "meta_description_template": base_structure.get("meta_description_template", "{description}"),
                "h1_template": base_structure.get("h1_template", "{heading}"),
                "url_pattern": base_structure.get("url_pattern", "/{slug}")
            },
            "content_sections": custom_sections,
            "variables": {
                "required": template.get("required_variables", []),
                "optional": template.get("optional_variables", [])
            },
            "schema_markup": self._generate_schema_template(template)
        }
        
        return page_structure
    
    def get_template(self, template_id: str) -> Optional[Dict[str, Any]]:
        """Get a template by ID"""
        # Check custom templates first
        if template_id in self.templates:
            return self.templates[template_id]
        
        # Check library templates
        for key, template in self.template_library.items():
            if key == template_id or template.get("id") == template_id:
                return template
        
        return None
    
    def list_templates(self, template_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """List all available templates"""
        all_templates = []
        
        # Add library templates
        for key, template in self.template_library.items():
            template_info = {
                "id": key,
                "name": template["name"],
                "description": template.get("description", ""),
                "type": "library",
                "patterns": template.get("patterns", []),
                "required_variables": template.get("required_variables", []),
                "optional_variables": template.get("optional_variables", [])
            }
            if not template_type or template_type == "library":
                all_templates.append(template_info)
        
        # Add custom templates
        for template_id, template in self.templates.items():
            template_info = {
                "id": template_id,
                "name": template["name"],
                "type": template.get("type", "custom"),
                "pattern": template["pattern"],
                "variables": template["variables"],
                "created_at": template.get("created_at", "")
            }
            if not template_type or template_type == template.get("type", "custom"):
                all_templates.append(template_info)
        
        return all_templates
    
    def estimate_page_count(
        self,
        template_id: str,
        data_sets: Dict[str, List[str]]
    ) -> Dict[str, Any]:
        """
        Estimate how many pages will be generated
        
        Args:
            template_id: Template to use
            data_sets: Dictionary of variable names to value lists
            
        Returns:
            Estimation details
        """
        template = self.get_template(template_id)
        if not template:
            return {"error": "Template not found"}
        
        # Get required variables
        required_vars = template.get("required_variables", template.get("variables", []))
        
        # Check if all required variables have data
        missing_vars = []
        for var in required_vars:
            if var not in data_sets or not data_sets[var]:
                missing_vars.append(var)
        
        if missing_vars:
            return {
                "error": f"Missing data for required variables: {', '.join(missing_vars)}",
                "required_variables": required_vars,
                "provided_variables": list(data_sets.keys())
            }
        
        # Calculate combinations
        total_combinations = 1
        variable_counts = {}
        
        for var in required_vars:
            if var in data_sets:
                count = len(data_sets[var])
                variable_counts[var] = count
                total_combinations *= count
        
        # Include optional variables if provided
        optional_vars = template.get("optional_variables", [])
        for var in optional_vars:
            if var in data_sets and data_sets[var]:
                count = len(data_sets[var])
                variable_counts[var] = count
                total_combinations *= count
        
        return {
            "template_id": template_id,
            "template_name": template.get("name", "Unknown"),
            "total_pages": total_combinations,
            "variable_counts": variable_counts,
            "calculation": " × ".join([f"{var}({count})" for var, count in variable_counts.items()])
        }
    
    def validate_data_for_template(
        self,
        template_id: str,
        data_sets: Dict[str, List[str]]
    ) -> Dict[str, Any]:
        """
        Validate data sets for a template
        
        Args:
            template_id: Template to validate against
            data_sets: Data to validate
            
        Returns:
            Validation results
        """
        template = self.get_template(template_id)
        if not template:
            return {"is_valid": False, "errors": ["Template not found"]}
        
        errors = []
        warnings = []
        
        # Check required variables
        required_vars = template.get("required_variables", template.get("variables", []))
        for var in required_vars:
            if var not in data_sets:
                errors.append(f"Missing required variable: {var}")
            elif not data_sets[var]:
                errors.append(f"No data provided for required variable: {var}")
        
        # Validate data values
        for var_name, values in data_sets.items():
            if not isinstance(values, list):
                errors.append(f"Data for {var_name} must be a list")
                continue
            
            # Check for empty values
            empty_count = sum(1 for v in values if not str(v).strip())
            if empty_count > 0:
                warnings.append(f"{empty_count} empty values found in {var_name}")
            
            # Check for duplicates
            unique_values = set(str(v).strip().lower() for v in values)
            if len(unique_values) < len(values):
                warnings.append(f"Duplicate values found in {var_name}")
            
            # Check for SEO-unfriendly characters in values
            for value in values:
                if not self._is_seo_friendly(str(value)):
                    warnings.append(f"Value '{value}' in {var_name} contains special characters that may not be SEO-friendly")
        
        return {
            "is_valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
            "data_summary": {
                var: {
                    "count": len(values),
                    "unique_count": len(set(str(v).strip().lower() for v in values)),
                    "sample": values[:3] if len(values) > 3 else values
                }
                for var, values in data_sets.items()
            }
        }
    
    def generate_variations(
        self,
        template_id: str,
        data_sets: Dict[str, List[str]],
        limit: Optional[int] = None
    ) -> List[Dict[str, str]]:
        """
        Generate all variable combinations for a template
        
        Args:
            template_id: Template to use
            data_sets: Variable data
            limit: Maximum number of variations to generate
            
        Returns:
            List of variable combinations
        """
        template = self.get_template(template_id)
        if not template:
            return []
        
        # Get all variables (required + optional that have data)
        all_vars = template.get("required_variables", template.get("variables", []))
        optional_vars = template.get("optional_variables", [])
        
        # Build list of variables to use
        vars_to_use = []
        var_data = []
        
        for var in all_vars:
            if var in data_sets and data_sets[var]:
                vars_to_use.append(var)
                var_data.append(data_sets[var])
        
        for var in optional_vars:
            if var in data_sets and data_sets[var]:
                vars_to_use.append(var)
                var_data.append(data_sets[var])
        
        if not var_data:
            return []
        
        # Generate combinations
        variations = []
        for combo in itertools.product(*var_data):
            variation = dict(zip(vars_to_use, combo))
            variations.append(variation)
            
            if limit and len(variations) >= limit:
                break
        
        return variations
    
    # Helper methods
    
    def _fill_template(self, template_str: str, data: Dict[str, str]) -> str:
        """Fill template string with data"""
        result = template_str
        
        # Replace {variable} syntax
        for key, value in data.items():
            result = result.replace(f"{{{key}}}", str(value))
            # Also replace [variable] syntax
            result = result.replace(f"[{key}]", str(value))
        
        return result
    
    def _get_sample_data(self, variables: List[str]) -> Dict[str, str]:
        """Generate sample data for variables"""
        sample_data = {
            "location": "Toronto",
            "city": "Toronto",
            "service": "plumbing",
            "product": "software",
            "item1": "Product A",
            "item2": "Product B",
            "action": "install",
            "topic": "solar panels",
            "year": "2024",
            "price": "$100",
            "use_case": "small business",
            "audience": "beginners",
            "metric": "pricing",
            "modifier": "quickly",
            "number": "10",
            "category": "premium",
            "attribute": "worth it",
            "question": "choose",
            "product_type": "CRM software",
            "price_range": "affordable",
            "business_attribute": "24/7 service"
        }
        
        # Return only requested variables
        return {var: sample_data.get(var, f"Sample {var}") for var in variables}
    
    def _generate_url_pattern(self, pattern: str) -> str:
        """Generate URL pattern from template pattern"""
        # Convert to lowercase and replace spaces with hyphens
        url = pattern.lower().replace(" ", "-")
        
        # Remove special characters except variables
        url = re.sub(r'[^a-z0-9\-{}\[\]]', '', url)
        
        # Ensure it starts with /
        if not url.startswith("/"):
            url = "/" + url
        
        return url
    
    def _is_seo_friendly(self, value: str) -> bool:
        """Check if a value is SEO-friendly"""
        # Allow letters, numbers, spaces, hyphens, and basic punctuation
        return bool(re.match(r'^[a-zA-Z0-9\s\-.,&\']+$', value))
    
    def _generate_default_sections(self, template: Dict) -> List[Dict]:
        """Generate default content sections based on template type"""
        template_type = template.get("type", "custom")
        
        if template_type == "location_service" or "location" in template.get("name", "").lower():
            return [
                {
                    "heading": "About {service} in {location}",
                    "content": "Overview of {service} services available in {location}."
                },
                {
                    "heading": "Why Choose Our {service} Services",
                    "content": "Benefits and advantages of choosing our {service} services."
                },
                {
                    "heading": "Service Areas",
                    "content": "We provide {service} throughout {location} and surrounding areas."
                },
                {
                    "heading": "Pricing and Packages",
                    "content": "Transparent pricing for {service} services in {location}."
                }
            ]
        elif template_type == "comparison" or "vs" in template.get("name", "").lower():
            return [
                {
                    "heading": "Quick Comparison",
                    "content": "Key differences between {item1} and {item2}."
                },
                {
                    "heading": "{item1} Overview",
                    "content": "Detailed look at {item1} features and benefits."
                },
                {
                    "heading": "{item2} Overview", 
                    "content": "Detailed look at {item2} features and benefits."
                },
                {
                    "heading": "Which Should You Choose?",
                    "content": "Recommendations based on your specific needs."
                }
            ]
        elif template_type == "how_to" or "how" in template.get("name", "").lower():
            return [
                {
                    "heading": "What You'll Learn",
                    "content": "Overview of how to {action} {topic}."
                },
                {
                    "heading": "Step-by-Step Instructions",
                    "content": "Detailed steps to {action} {topic} successfully."
                },
                {
                    "heading": "Common Mistakes to Avoid",
                    "content": "Pitfalls to watch out for when you {action} {topic}."
                },
                {
                    "heading": "Expert Tips",
                    "content": "Professional advice for better results."
                }
            ]
        else:
            # Generic sections
            return [
                {
                    "heading": "Overview",
                    "content": "Introduction and overview of the topic."
                },
                {
                    "heading": "Key Information",
                    "content": "Important details and information."
                },
                {
                    "heading": "Benefits",
                    "content": "Advantages and benefits to consider."
                },
                {
                    "heading": "Next Steps",
                    "content": "How to proceed and take action."
                }
            ]
    
    def _generate_schema_template(self, template: Dict) -> Dict[str, Any]:
        """Generate schema markup template based on template type"""
        template_type = template.get("type", "custom")
        
        if "location" in template_type or "service" in template_type:
            return {
                "@context": "https://schema.org",
                "@type": "LocalBusiness",
                "name": "{business_name}",
                "description": "{service} services in {location}",
                "address": {
                    "@type": "PostalAddress",
                    "addressLocality": "{location}"
                },
                "serviceArea": "{location}"
            }
        elif "how" in template_type:
            return {
                "@context": "https://schema.org",
                "@type": "HowTo",
                "name": "How to {action} {topic}",
                "description": "Learn how to {action} {topic} with step-by-step instructions"
            }
        elif "comparison" in template_type or "vs" in str(template.get("pattern", "")):
            return {
                "@context": "https://schema.org",
                "@type": "Article",
                "headline": "{item1} vs {item2} Comparison",
                "description": "Detailed comparison of {item1} and {item2}"
            }
        else:
            return {
                "@context": "https://schema.org",
                "@type": "Article",
                "headline": "{title}",
                "description": "{meta_description}"
            }
    
    def export_template(self, template_id: str) -> Dict[str, Any]:
        """Export template configuration for storage or sharing"""
        template = self.get_template(template_id)
        if not template:
            return {"error": "Template not found"}
        
        return {
            "id": template_id,
            "name": template.get("name"),
            "type": template.get("type", "custom"),
            "pattern": template.get("pattern"),
            "patterns": template.get("patterns", []),
            "required_variables": template.get("required_variables", []),
            "optional_variables": template.get("optional_variables", []),
            "seo_structure": template.get("seo_structure", {}),
            "structure": template.get("structure", {}),
            "description": template.get("description", ""),
            "created_at": template.get("created_at", ""),
            "version": "1.0"
        }
    
    def import_template(self, template_config: Dict[str, Any]) -> Dict[str, Any]:
        """Import template from configuration"""
        # Validate imported template
        validation = self.validate_template(template_config)
        
        if not validation["is_valid"]:
            return {
                "success": False,
                "errors": validation["errors"],
                "warnings": validation["warnings"]
            }
        
        # Generate ID if not provided
        template_id = template_config.get("id", f"imported_{datetime.now().timestamp()}")
        
        # Store template
        self.templates[template_id] = template_config
        
        return {
            "success": True,
            "template_id": template_id,
            "message": f"Template '{template_config.get('name', 'Unknown')}' imported successfully"
        }