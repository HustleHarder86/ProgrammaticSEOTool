"""Schema Markup Generator for SEO-optimized structured data"""

import json
from typing import Dict, List, Any, Optional
from datetime import datetime
import re
from pathlib import Path


class SchemaGenerator:
    """Generate appropriate schema markup for different content types"""
    
    def __init__(self):
        self.schema_templates = self._load_schema_templates()
        
    def _load_schema_templates(self) -> Dict[str, Any]:
        """Load schema templates for different content types"""
        return {
            "Article": {
                "@context": "https://schema.org",
                "@type": "Article",
                "required": ["headline", "datePublished", "author"],
                "recommended": ["image", "description", "keywords"]
            },
            "FAQPage": {
                "@context": "https://schema.org",
                "@type": "FAQPage",
                "required": ["mainEntity"],
                "recommended": []
            },
            "HowTo": {
                "@context": "https://schema.org",
                "@type": "HowTo",
                "required": ["name", "step"],
                "recommended": ["totalTime", "estimatedCost", "supply", "tool"]
            },
            "LocalBusiness": {
                "@context": "https://schema.org",
                "@type": "LocalBusiness",
                "required": ["name", "address"],
                "recommended": ["telephone", "openingHours", "priceRange"]
            },
            "Product": {
                "@context": "https://schema.org",
                "@type": "Product",
                "required": ["name"],
                "recommended": ["description", "image", "offers", "aggregateRating"]
            },
            "Service": {
                "@context": "https://schema.org",
                "@type": "Service",
                "required": ["name", "provider"],
                "recommended": ["serviceType", "areaServed", "description"]
            },
            "Review": {
                "@context": "https://schema.org",
                "@type": "Review",
                "required": ["itemReviewed", "reviewRating", "author"],
                "recommended": ["reviewBody", "datePublished"]
            },
            "BreadcrumbList": {
                "@context": "https://schema.org",
                "@type": "BreadcrumbList",
                "required": ["itemListElement"],
                "recommended": []
            },
            "WebPage": {
                "@context": "https://schema.org",
                "@type": "WebPage",
                "required": ["name", "url"],
                "recommended": ["description", "breadcrumb", "mainEntity"]
            }
        }
    
    def generate_schema(self,
                       content_type: str,
                       page_data: Dict[str, Any],
                       additional_types: List[str] = None) -> Dict[str, Any]:
        """Generate schema markup based on content type and page data
        
        Args:
            content_type: Type of content (evaluation_question, location_service, etc.)
            page_data: Page data including title, content, variables
            additional_types: Additional schema types to include
            
        Returns:
            Complete schema markup as dictionary
        """
        # Determine primary schema type
        primary_type = self._determine_schema_type(content_type, page_data)
        
        # Generate base schema
        schema = self._generate_base_schema(primary_type, page_data)
        
        # Add additional schemas if requested
        if additional_types:
            schema = self._add_additional_schemas(schema, additional_types, page_data)
        
        # Validate and clean schema
        schema = self._validate_and_clean_schema(schema)
        
        return schema
    
    def _determine_schema_type(self, content_type: str, page_data: Dict) -> str:
        """Determine the most appropriate schema type"""
        # Content type mapping
        type_mapping = {
            "evaluation_question": "FAQPage",
            "location_service": "Service",
            "comparison": "Article",
            "how_to": "HowTo",
            "product_review": "Review",
            "local_business": "LocalBusiness",
            "generic": "Article"
        }
        
        # Check if content has FAQ structure
        content = page_data.get("content", "")
        if "?" in page_data.get("title", "") and content_type != "comparison":
            return "FAQPage"
        
        # Check for how-to indicators
        if any(word in content.lower() for word in ["step 1", "how to", "guide"]):
            return "HowTo"
        
        # Default mapping
        return type_mapping.get(content_type, "Article")
    
    def _generate_base_schema(self, schema_type: str, page_data: Dict) -> Dict[str, Any]:
        """Generate base schema markup"""
        if schema_type == "FAQPage":
            return self._generate_faq_schema(page_data)
        elif schema_type == "Article":
            return self._generate_article_schema(page_data)
        elif schema_type == "Service":
            return self._generate_service_schema(page_data)
        elif schema_type == "HowTo":
            return self._generate_howto_schema(page_data)
        elif schema_type == "LocalBusiness":
            return self._generate_localbusiness_schema(page_data)
        elif schema_type == "Product":
            return self._generate_product_schema(page_data)
        elif schema_type == "Review":
            return self._generate_review_schema(page_data)
        else:
            return self._generate_webpage_schema(page_data)
    
    def _generate_faq_schema(self, page_data: Dict) -> Dict[str, Any]:
        """Generate FAQ schema markup"""
        schema = {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": []
        }
        
        # Extract questions and answers from content
        content = page_data.get("content", "")
        title = page_data.get("title", "")
        
        # Main question from title
        main_qa = {
            "@type": "Question",
            "name": title,
            "acceptedAnswer": {
                "@type": "Answer",
                "text": self._extract_answer_summary(content)
            }
        }
        schema["mainEntity"].append(main_qa)
        
        # Extract additional Q&As from content
        additional_qas = self._extract_questions_answers(content)
        schema["mainEntity"].extend(additional_qas)
        
        return schema
    
    def _generate_article_schema(self, page_data: Dict) -> Dict[str, Any]:
        """Generate Article schema markup"""
        schema = {
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": page_data.get("title", ""),
            "description": page_data.get("meta_description", "")[:160],
            "datePublished": page_data.get("created_at", datetime.now().isoformat()),
            "dateModified": page_data.get("updated_at", datetime.now().isoformat()),
            "author": {
                "@type": "Organization",
                "name": page_data.get("business_name", "Publisher")
            },
            "publisher": {
                "@type": "Organization",
                "name": page_data.get("business_name", "Publisher"),
                "logo": {
                    "@type": "ImageObject",
                    "url": page_data.get("logo_url", "")
                }
            }
        }
        
        # Add image if available
        if page_data.get("image_url"):
            schema["image"] = page_data["image_url"]
        
        # Add keywords
        if page_data.get("keywords"):
            schema["keywords"] = page_data["keywords"]
        
        # Word count
        content = page_data.get("content", "")
        schema["wordCount"] = len(content.split())
        
        return schema
    
    def _generate_service_schema(self, page_data: Dict) -> Dict[str, Any]:
        """Generate Service schema markup"""
        variables = page_data.get("variables", {})
        
        schema = {
            "@context": "https://schema.org",
            "@type": "Service",
            "name": page_data.get("title", ""),
            "description": page_data.get("meta_description", ""),
            "provider": {
                "@type": "Organization",
                "name": page_data.get("business_name", "Service Provider")
            }
        }
        
        # Add service type
        if "service" in variables:
            schema["serviceType"] = variables["service"]
        
        # Add area served
        if "city" in variables or "location" in variables:
            schema["areaServed"] = {
                "@type": "City",
                "name": variables.get("city", variables.get("location", ""))
            }
        
        # Add aggregate rating if available
        if page_data.get("rating_data"):
            schema["aggregateRating"] = self._generate_rating_schema(page_data["rating_data"])
        
        return schema
    
    def _generate_howto_schema(self, page_data: Dict) -> Dict[str, Any]:
        """Generate HowTo schema markup"""
        schema = {
            "@context": "https://schema.org",
            "@type": "HowTo",
            "name": page_data.get("title", ""),
            "description": page_data.get("meta_description", ""),
            "step": []
        }
        
        # Extract steps from content
        content = page_data.get("content", "")
        steps = self._extract_steps(content)
        
        for i, step_text in enumerate(steps):
            step = {
                "@type": "HowToStep",
                "name": f"Step {i+1}",
                "text": step_text
            }
            schema["step"].append(step)
        
        # Add time estimates if available
        if page_data.get("time_estimate"):
            schema["totalTime"] = page_data["time_estimate"]
        
        return schema
    
    def _generate_localbusiness_schema(self, page_data: Dict) -> Dict[str, Any]:
        """Generate LocalBusiness schema markup"""
        variables = page_data.get("variables", {})
        
        schema = {
            "@context": "https://schema.org",
            "@type": "LocalBusiness",
            "name": page_data.get("business_name", "Business"),
            "description": page_data.get("meta_description", ""),
            "address": {
                "@type": "PostalAddress",
                "addressLocality": variables.get("city", "")
            }
        }
        
        # Add additional business info if available
        if page_data.get("phone"):
            schema["telephone"] = page_data["phone"]
        
        if page_data.get("opening_hours"):
            schema["openingHours"] = page_data["opening_hours"]
        
        return schema
    
    def _generate_product_schema(self, page_data: Dict) -> Dict[str, Any]:
        """Generate Product schema markup"""
        schema = {
            "@context": "https://schema.org",
            "@type": "Product",
            "name": page_data.get("title", ""),
            "description": page_data.get("meta_description", "")
        }
        
        # Add offers if price data available
        if page_data.get("price_data"):
            schema["offers"] = {
                "@type": "Offer",
                "price": page_data["price_data"].get("price", "0"),
                "priceCurrency": page_data["price_data"].get("currency", "USD")
            }
        
        return schema
    
    def _generate_review_schema(self, page_data: Dict) -> Dict[str, Any]:
        """Generate Review schema markup"""
        schema = {
            "@context": "https://schema.org",
            "@type": "Review",
            "itemReviewed": {
                "@type": "Thing",
                "name": page_data.get("reviewed_item", page_data.get("title", ""))
            },
            "author": {
                "@type": "Organization",
                "name": page_data.get("business_name", "Reviewer")
            },
            "reviewRating": {
                "@type": "Rating",
                "ratingValue": page_data.get("rating", "4"),
                "bestRating": "5"
            },
            "datePublished": page_data.get("created_at", datetime.now().isoformat())
        }
        
        if page_data.get("content"):
            schema["reviewBody"] = page_data["content"][:500]
        
        return schema
    
    def _generate_webpage_schema(self, page_data: Dict) -> Dict[str, Any]:
        """Generate WebPage schema markup"""
        schema = {
            "@context": "https://schema.org",
            "@type": "WebPage",
            "name": page_data.get("title", ""),
            "description": page_data.get("meta_description", ""),
            "url": page_data.get("url", "")
        }
        
        # Add breadcrumb if available
        if page_data.get("breadcrumb"):
            schema["breadcrumb"] = self._generate_breadcrumb_schema(page_data["breadcrumb"])
        
        return schema
    
    def _generate_breadcrumb_schema(self, breadcrumb_data: List[Dict]) -> Dict[str, Any]:
        """Generate BreadcrumbList schema"""
        schema = {
            "@type": "BreadcrumbList",
            "itemListElement": []
        }
        
        for i, item in enumerate(breadcrumb_data):
            breadcrumb_item = {
                "@type": "ListItem",
                "position": i + 1,
                "name": item["name"],
                "item": item["url"]
            }
            schema["itemListElement"].append(breadcrumb_item)
        
        return schema
    
    def _generate_rating_schema(self, rating_data: Dict) -> Dict[str, Any]:
        """Generate AggregateRating schema"""
        return {
            "@type": "AggregateRating",
            "ratingValue": rating_data.get("average", "4.5"),
            "reviewCount": rating_data.get("count", "100")
        }
    
    def _extract_answer_summary(self, content: str) -> str:
        """Extract a summary answer from content"""
        # Get first paragraph or first 200 characters
        paragraphs = content.split('\n\n')
        if paragraphs:
            return paragraphs[0][:300]
        return content[:300]
    
    def _extract_questions_answers(self, content: str) -> List[Dict[str, Any]]:
        """Extract Q&A pairs from content"""
        qas = []
        
        # Look for question patterns
        lines = content.split('\n')
        current_question = None
        current_answer = []
        
        for line in lines:
            if '?' in line and len(line) < 200:  # Likely a question
                if current_question and current_answer:
                    qas.append({
                        "@type": "Question",
                        "name": current_question,
                        "acceptedAnswer": {
                            "@type": "Answer",
                            "text": ' '.join(current_answer)
                        }
                    })
                current_question = line.strip()
                current_answer = []
            elif current_question and line.strip():
                current_answer.append(line.strip())
        
        # Add last Q&A if exists
        if current_question and current_answer:
            qas.append({
                "@type": "Question",
                "name": current_question,
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": ' '.join(current_answer)
                }
            })
        
        return qas[:5]  # Limit to 5 Q&As
    
    def _extract_steps(self, content: str) -> List[str]:
        """Extract step-by-step instructions from content"""
        steps = []
        
        # Look for numbered steps
        step_patterns = [
            r'\d+\.\s+(.+)',  # 1. Step
            r'Step \d+:?\s+(.+)',  # Step 1: Do this
            r'\* (.+)',  # Bullet points
        ]
        
        for pattern in step_patterns:
            matches = re.findall(pattern, content, re.MULTILINE)
            if matches:
                steps.extend(matches)
                break
        
        # If no pattern matches, split by paragraphs
        if not steps:
            paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
            steps = paragraphs[1:6]  # Skip first paragraph, take next 5
        
        return steps
    
    def _add_additional_schemas(self, 
                               base_schema: Dict[str, Any],
                               additional_types: List[str],
                               page_data: Dict) -> Dict[str, Any]:
        """Add additional schema types using @graph"""
        # Convert to graph format if not already
        if "@graph" not in base_schema:
            base_schema = {
                "@context": "https://schema.org",
                "@graph": [base_schema]
            }
        
        # Add each additional type
        for schema_type in additional_types:
            additional_schema = self._generate_base_schema(schema_type, page_data)
            if additional_schema:
                base_schema["@graph"].append(additional_schema)
        
        return base_schema
    
    def _validate_and_clean_schema(self, schema: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and clean schema markup"""
        # Remove empty values
        cleaned = self._remove_empty_values(schema)
        
        # Ensure required fields
        cleaned = self._ensure_required_fields(cleaned)
        
        return cleaned
    
    def _remove_empty_values(self, obj: Any) -> Any:
        """Recursively remove empty values from schema"""
        if isinstance(obj, dict):
            return {k: self._remove_empty_values(v) 
                   for k, v in obj.items() 
                   if v is not None and v != "" and v != []}
        elif isinstance(obj, list):
            return [self._remove_empty_values(item) 
                   for item in obj 
                   if item is not None]
        return obj
    
    def _ensure_required_fields(self, schema: Dict[str, Any]) -> Dict[str, Any]:
        """Ensure schema has required fields"""
        schema_type = schema.get("@type")
        
        if schema_type and schema_type in self.schema_templates:
            template = self.schema_templates[schema_type]
            
            # Check required fields
            for field in template.get("required", []):
                if field not in schema and field != "@context" and field != "@type":
                    # Add default value
                    schema[field] = self._get_default_value(field)
        
        return schema
    
    def _get_default_value(self, field: str) -> Any:
        """Get default value for required field"""
        defaults = {
            "name": "Untitled",
            "headline": "Untitled Article",
            "author": {"@type": "Organization", "name": "Publisher"},
            "datePublished": datetime.now().isoformat(),
            "mainEntity": [],
            "step": [],
            "itemListElement": []
        }
        return defaults.get(field, "")
    
    def generate_schema_script(self, schema: Dict[str, Any]) -> str:
        """Generate script tag with schema markup"""
        return f'<script type="application/ld+json">\n{json.dumps(schema, indent=2)}\n</script>'
    
    def validate_schema(self, schema: Dict[str, Any]) -> Dict[str, Any]:
        """Validate schema against Google's requirements"""
        validation_result = {
            "valid": True,
            "errors": [],
            "warnings": []
        }
        
        # Check for @context
        if "@context" not in schema and "@graph" not in schema:
            validation_result["errors"].append("Missing @context")
            validation_result["valid"] = False
        
        # Check for @type
        if "@type" not in schema and "@graph" not in schema:
            validation_result["errors"].append("Missing @type")
            validation_result["valid"] = False
        
        # Additional validations can be added here
        
        return validation_result