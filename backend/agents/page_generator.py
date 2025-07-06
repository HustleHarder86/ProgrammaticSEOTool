"""Page Generator Agent - Generates complete SEO-optimized pages from templates and data"""
import re
import json
import asyncio
import logging
from typing import List, Dict, Any, Optional, Tuple, Generator
from datetime import datetime
import hashlib
from collections import defaultdict
import random

# Import dependencies
from agents.template_builder import TemplateBuilderAgent
from agents.data_manager import DataManagerAgent
from utils.ai_client import AIClient
from api.content_variation import (
    ContentVariationEngine,
    generate_internal_links,
    insert_contextual_links,
    enhance_content_quality,
    ensure_minimum_quality
)

logger = logging.getLogger(__name__)

class PageGeneratorAgent:
    """
    Agent responsible for generating complete SEO-optimized pages from templates and data.
    Implements content variation, SEO optimization, and internal linking strategies.
    """
    
    def __init__(self):
        """Initialize the Page Generator Agent"""
        self.template_builder = TemplateBuilderAgent()
        self.data_manager = DataManagerAgent()
        self.ai_client = AIClient()
        self.variation_engine = ContentVariationEngine()
        self.generated_pages = {}
        self.page_index = {}  # For internal linking
        self.generation_stats = {
            "total_pages": 0,
            "unique_pages": 0,
            "variations_created": 0,
            "internal_links_added": 0
        }
    
    async def generate_pages(
        self,
        template_id: str,
        data_combinations: List[Dict[str, str]],
        business_info: Optional[Dict[str, Any]] = None,
        content_type: str = "informational",
        batch_size: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Generate all pages from template and data combinations
        
        Args:
            template_id: ID of template to use
            data_combinations: List of variable combinations
            business_info: Business context for content generation
            content_type: Type of content (informational, transactional, comparison)
            batch_size: Number of pages to generate in parallel
            
        Returns:
            List of generated pages
        """
        template = self.template_builder.get_template(template_id)
        if not template:
            raise ValueError(f"Template {template_id} not found")
        
        all_pages = []
        total_combinations = len(data_combinations)
        
        # Process in batches for better performance
        for i in range(0, total_combinations, batch_size):
            batch = data_combinations[i:i + batch_size]
            batch_pages = await asyncio.gather(*[
                self.populate_template(
                    template, 
                    combo, 
                    business_info,
                    content_type,
                    page_index=i+j,
                    total_pages=total_combinations
                )
                for j, combo in enumerate(batch)
            ])
            
            # Add uniqueness to each page
            for page in batch_pages:
                unique_page = await self.add_unique_elements(page, all_pages)
                optimized_page = self.optimize_for_seo(unique_page, template, business_info)
                all_pages.append(optimized_page)
            
            # Update progress
            logger.info(f"Generated {len(all_pages)}/{total_combinations} pages")
        
        # Add internal linking after all pages are generated
        all_pages = self._add_internal_linking(all_pages, business_info)
        
        # Update statistics
        self.generation_stats["total_pages"] = len(all_pages)
        self.generation_stats["unique_pages"] = len(set(p["url"] for p in all_pages))
        
        return all_pages
    
    async def populate_template(
        self,
        template: Dict[str, Any],
        data: Dict[str, str],
        business_info: Optional[Dict[str, Any]] = None,
        content_type: str = "informational",
        page_index: int = 0,
        total_pages: int = 1
    ) -> Dict[str, Any]:
        """
        Fill template with specific data point
        
        Args:
            template: Template configuration
            data: Variable values
            business_info: Business context
            content_type: Type of content
            page_index: Current page index (for variations)
            total_pages: Total number of pages being generated
            
        Returns:
            Generated page with all fields populated
        """
        # Get page structure
        page_structure = self.template_builder.build_page_structure(
            template.get("id", template.get("name", "custom"))
        )
        
        # Fill SEO elements
        seo_data = {
            "title": self._fill_template_string(
                page_structure["seo"]["title_template"], 
                data
            ),
            "meta_description": self._fill_template_string(
                page_structure["seo"]["meta_description_template"], 
                data
            ),
            "h1": self._fill_template_string(
                page_structure["seo"]["h1_template"], 
                data
            ),
            "url": self._generate_url(
                page_structure["seo"]["url_pattern"], 
                data
            )
        }
        
        # Generate content sections
        content_sections = []
        for section_template in page_structure.get("content_sections", []):
            section = await self._generate_content_section(
                section_template,
                data,
                business_info,
                content_type,
                page_index
            )
            content_sections.append(section)
        
        # Create page object
        page = {
            "id": self._generate_page_id(seo_data["url"]),
            "template_id": template.get("id", "custom"),
            "data": data,
            "seo": seo_data,
            "content_sections": content_sections,
            "content_type": content_type,
            "generated_at": datetime.now().isoformat(),
            "variation_index": page_index % 5,  # Create 5 variation types
            "business_info": business_info or {}
        }
        
        # Generate full content
        page["content"] = self._compile_content(page)
        
        # Add to index for internal linking
        self.page_index[page["url"]] = {
            "title": page["seo"]["title"],
            "keywords": self._extract_keywords(page),
            "data": data
        }
        
        return page
    
    async def add_unique_elements(
        self,
        page: Dict[str, Any],
        existing_pages: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Add unique content elements to avoid duplicate penalties
        
        Args:
            page: Page to add uniqueness to
            existing_pages: Previously generated pages
            
        Returns:
            Page with unique elements added
        """
        # Get variation type based on page index
        variation_type = self.variation_engine.get_variation_type(
            page.get("variation_index", 0)
        )
        
        # Generate unique structure
        unique_structure = self.variation_engine.generate_unique_structure(
            page["seo"]["title"],
            page["content_type"]
        )
        
        # Add unique elements to content
        unique_elements = unique_structure["unique_elements"]
        
        # Add statistics or data visualization
        if "statistics_section" in unique_elements:
            stats_section = await self._generate_statistics_section(page)
            page["content_sections"].append(stats_section)
        
        # Add comparison table
        if "comparison_table" in unique_elements:
            comparison = await self._generate_comparison_table(page)
            page["content_sections"].append(comparison)
        
        # Add FAQ section
        if "faq" not in [s.get("type") for s in page["content_sections"]]:
            faq = await self._generate_faq_section(page)
            page["content_sections"].append(faq)
        
        # Add case study or testimonial
        if "case_study" in unique_elements:
            case_study = await self._generate_case_study(page)
            page["content_sections"].append(case_study)
        
        # Add local context if location-based
        if any("location" in str(v).lower() for v in page["data"].values()):
            local_context = await self._add_local_context(page)
            page["content_sections"].append(local_context)
        
        # Vary content structure
        if page.get("variation_index", 0) % 2 == 0:
            # Reorder some sections for variation
            if len(page["content_sections"]) > 3:
                middle_sections = page["content_sections"][1:-1]
                random.shuffle(middle_sections)
                page["content_sections"] = [
                    page["content_sections"][0]
                ] + middle_sections + [
                    page["content_sections"][-1]
                ]
        
        # Update content compilation
        page["content"] = self._compile_content(page)
        
        # Track uniqueness
        uniqueness_score = self._calculate_uniqueness_score(page, existing_pages)
        page["uniqueness_score"] = uniqueness_score
        
        self.generation_stats["variations_created"] += 1
        
        return page
    
    def optimize_for_seo(
        self,
        page: Dict[str, Any],
        template: Dict[str, Any],
        business_info: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Ensure SEO best practices for the page
        
        Args:
            page: Page to optimize
            template: Template configuration
            business_info: Business context
            
        Returns:
            SEO-optimized page
        """
        # Optimize title length
        if len(page["seo"]["title"]) > 60:
            page["seo"]["title"] = self._truncate_smartly(page["seo"]["title"], 60)
        elif len(page["seo"]["title"]) < 30:
            # Add brand name or modifier
            if business_info and "name" in business_info:
                page["seo"]["title"] += f" | {business_info['name']}"
        
        # Optimize meta description
        if len(page["seo"]["meta_description"]) > 160:
            page["seo"]["meta_description"] = self._truncate_smartly(
                page["seo"]["meta_description"], 
                155
            ) + "..."
        elif len(page["seo"]["meta_description"]) < 120:
            # Add call to action
            page["seo"]["meta_description"] += " Learn more and get started today."
        
        # Ensure proper heading structure
        page = self._optimize_heading_structure(page)
        
        # Add schema markup
        page["schema_markup"] = self._generate_schema_markup(page, template, business_info)
        
        # Calculate and optimize keyword density
        page = self._optimize_keyword_density(page)
        
        # Add breadcrumbs
        page["breadcrumbs"] = self._generate_breadcrumbs(page, business_info)
        
        # Ensure minimum content quality
        quality_check = ensure_minimum_quality(page["content"], page["seo"]["h1"])
        page["quality_metrics"] = quality_check
        
        # Add canonical URL
        page["canonical_url"] = page["seo"]["url"]
        
        # Generate meta tags
        page["meta_tags"] = self._generate_meta_tags(page, business_info)
        
        return page
    
    def generate_batch(
        self,
        template_id: str,
        data_combinations: List[Dict[str, str]],
        batch_size: int = 100,
        business_info: Optional[Dict[str, Any]] = None
    ) -> Generator[List[Dict[str, Any]], None, None]:
        """
        Generate pages in batches for better performance
        
        Args:
            template_id: Template to use
            data_combinations: All data combinations
            batch_size: Size of each batch
            business_info: Business context
            
        Yields:
            Batches of generated pages
        """
        template = self.template_builder.get_template(template_id)
        if not template:
            raise ValueError(f"Template {template_id} not found")
        
        total_combinations = len(data_combinations)
        
        for i in range(0, total_combinations, batch_size):
            batch = data_combinations[i:i + batch_size]
            
            # Generate batch asynchronously
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            batch_pages = loop.run_until_complete(
                self.generate_pages(
                    template_id,
                    batch,
                    business_info
                )
            )
            
            loop.close()
            
            yield batch_pages
    
    def preview_page(
        self,
        template_id: str,
        sample_data: Dict[str, str],
        business_info: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Generate a preview of a single page
        
        Args:
            template_id: Template to use
            sample_data: Sample variable values
            business_info: Business context
            
        Returns:
            Preview page
        """
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        pages = loop.run_until_complete(
            self.generate_pages(
                template_id,
                [sample_data],
                business_info
            )
        )
        
        loop.close()
        
        return pages[0] if pages else None
    
    def validate_generation_requirements(
        self,
        template_id: str,
        data_sets: Dict[str, List[str]]
    ) -> Dict[str, Any]:
        """
        Validate that all requirements are met for page generation
        
        Args:
            template_id: Template to validate against
            data_sets: Available data sets
            
        Returns:
            Validation results
        """
        template = self.template_builder.get_template(template_id)
        if not template:
            return {
                "valid": False,
                "errors": ["Template not found"]
            }
        
        # Validate data availability
        validation = self.template_builder.validate_data_for_template(
            template_id,
            data_sets
        )
        
        if not validation["is_valid"]:
            return {
                "valid": False,
                "errors": validation["errors"],
                "warnings": validation.get("warnings", [])
            }
        
        # Check scale
        estimation = self.template_builder.estimate_page_count(
            template_id,
            data_sets
        )
        
        if "error" in estimation:
            return {
                "valid": False,
                "errors": [estimation["error"]]
            }
        
        # Add scale warnings
        warnings = validation.get("warnings", [])
        if estimation["total_pages"] > 10000:
            warnings.append(f"Large scale generation: {estimation['total_pages']:,} pages")
        elif estimation["total_pages"] < 10:
            warnings.append("Low page count may limit SEO impact")
        
        return {
            "valid": True,
            "template": template,
            "estimated_pages": estimation["total_pages"],
            "warnings": warnings
        }
    
    def get_generation_stats(self) -> Dict[str, Any]:
        """Get statistics about page generation"""
        return {
            **self.generation_stats,
            "average_uniqueness": self._calculate_average_uniqueness(),
            "content_types": self._get_content_type_distribution(),
            "quality_summary": self._get_quality_summary()
        }
    
    # Helper methods
    
    def _fill_template_string(self, template_str: str, data: Dict[str, str]) -> str:
        """Fill template string with data values"""
        result = template_str
        for key, value in data.items():
            result = result.replace(f"{{{key}}}", str(value))
            result = result.replace(f"[{key}]", str(value))
        return result
    
    def _generate_url(self, url_pattern: str, data: Dict[str, str]) -> str:
        """Generate SEO-friendly URL from pattern"""
        url = self._fill_template_string(url_pattern, data)
        # Clean and normalize URL
        url = url.lower()
        url = re.sub(r'[^a-z0-9\-/]', '-', url)
        url = re.sub(r'-+', '-', url)
        url = url.strip('-/')
        if not url.startswith('/'):
            url = '/' + url
        return url
    
    def _generate_page_id(self, url: str) -> str:
        """Generate unique page ID from URL"""
        return hashlib.md5(url.encode()).hexdigest()
    
    async def _generate_content_section(
        self,
        section_template: Dict[str, Any],
        data: Dict[str, str],
        business_info: Optional[Dict[str, Any]],
        content_type: str,
        variation_index: int
    ) -> Dict[str, Any]:
        """Generate a single content section"""
        heading = self._fill_template_string(
            section_template.get("heading", ""),
            data
        )
        
        # Generate base content
        content_prompt = self._build_content_prompt(
            section_template,
            data,
            business_info,
            content_type
        )
        
        content = await self.ai_client.generate(
            content_prompt,
            temperature=0.7,
            max_tokens=500
        )
        
        # Apply variations
        if variation_index > 0:
            variations = self.variation_engine.vary_content(
                content,
                heading,
                variations_needed=1
            )
            content = variations[0]["content"] if variations else content
        
        return {
            "heading": heading,
            "content": content,
            "type": section_template.get("type", "generic"),
            "variation_applied": variation_index > 0
        }
    
    def _build_content_prompt(
        self,
        section_template: Dict[str, Any],
        data: Dict[str, str],
        business_info: Optional[Dict[str, Any]],
        content_type: str
    ) -> str:
        """Build prompt for content generation"""
        template_content = self._fill_template_string(
            section_template.get("content", ""),
            data
        )
        
        business_context = ""
        if business_info:
            business_context = f"""
Business Context:
- Name: {business_info.get('name', 'N/A')}
- Industry: {business_info.get('industry', 'N/A')}
- Target Audience: {business_info.get('target_audience', 'General')}
"""
        
        prompt = f"""Generate SEO-optimized content for this section:

Heading: {section_template.get('heading', '')}
Content Type: {content_type}
Template: {template_content}
Variables: {json.dumps(data, indent=2)}
{business_context}

Requirements:
- Write in a {content_type} tone
- Include relevant keywords naturally
- Keep paragraphs short and scannable
- Use bullet points where appropriate
- Be specific and valuable to the reader
- Approximately 150-250 words

Generate the content:"""
        
        return prompt
    
    def _compile_content(self, page: Dict[str, Any]) -> str:
        """Compile all sections into full page content"""
        content_parts = [f"# {page['seo']['h1']}\n"]
        
        for section in page["content_sections"]:
            content_parts.append(f"\n## {section['heading']}\n")
            content_parts.append(section["content"])
        
        # Add schema markup as comment
        if "schema_markup" in page:
            content_parts.append(
                f"\n<!-- Schema Markup:\n{json.dumps(page['schema_markup'], indent=2)}\n-->"
            )
        
        return "\n".join(content_parts)
    
    def _extract_keywords(self, page: Dict[str, Any]) -> List[str]:
        """Extract main keywords from page"""
        keywords = []
        
        # Extract from title and H1
        title_words = page["seo"]["title"].lower().split()
        h1_words = page["seo"]["h1"].lower().split()
        
        # Common words to exclude
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were'
        }
        
        # Extract meaningful keywords
        for word in title_words + h1_words:
            if len(word) > 3 and word not in stop_words:
                keywords.append(word)
        
        # Add data values as keywords
        for value in page["data"].values():
            keywords.extend(str(value).lower().split())
        
        # Remove duplicates while preserving order
        seen = set()
        unique_keywords = []
        for kw in keywords:
            if kw not in seen and kw not in stop_words:
                seen.add(kw)
                unique_keywords.append(kw)
        
        return unique_keywords[:10]  # Top 10 keywords
    
    async def _generate_statistics_section(self, page: Dict[str, Any]) -> Dict[str, Any]:
        """Generate statistics section for uniqueness"""
        stats_prompt = f"""Generate relevant statistics for: {page['seo']['h1']}

Create 4-5 compelling statistics with percentages or numbers that would be relevant.
Format as a bullet list.
Make them specific to the topic and industry.
Keep it under 100 words."""
        
        stats_content = await self.ai_client.generate(stats_prompt, temperature=0.8)
        
        return {
            "heading": "Key Statistics and Insights",
            "content": stats_content,
            "type": "statistics"
        }
    
    async def _generate_comparison_table(self, page: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comparison table for uniqueness"""
        if "vs" in page["seo"]["title"].lower() or "comparison" in page["content_type"]:
            comparison_prompt = f"""Create a comparison table for: {page['seo']['h1']}

Format as markdown table with 3-4 key comparison points.
Keep it concise and scannable."""
            
            table_content = await self.ai_client.generate(comparison_prompt)
            
            return {
                "heading": "Quick Comparison",
                "content": table_content,
                "type": "comparison_table"
            }
        
        return {
            "heading": "Key Features",
            "content": "Feature comparison table would go here",
            "type": "features"
        }
    
    async def _generate_faq_section(self, page: Dict[str, Any]) -> Dict[str, Any]:
        """Generate FAQ section"""
        faq_prompt = f"""Generate 3 frequently asked questions about: {page['seo']['h1']}

Format as:
**Q: [Question]**
A: [Brief answer in 2-3 sentences]

Make questions specific and answers helpful."""
        
        faq_content = await self.ai_client.generate(faq_prompt, temperature=0.7)
        
        return {
            "heading": "Frequently Asked Questions",
            "content": faq_content,
            "type": "faq"
        }
    
    async def _generate_case_study(self, page: Dict[str, Any]) -> Dict[str, Any]:
        """Generate case study or success story"""
        case_prompt = f"""Create a brief success story example for: {page['seo']['h1']}

Include:
- Brief scenario (2 sentences)
- Key results with numbers
- Main takeaway

Keep it under 100 words and make it believable."""
        
        case_content = await self.ai_client.generate(case_prompt, temperature=0.8)
        
        return {
            "heading": "Success Story",
            "content": case_content,
            "type": "case_study"
        }
    
    async def _add_local_context(self, page: Dict[str, Any]) -> Dict[str, Any]:
        """Add local context for location-based pages"""
        location = None
        for key, value in page["data"].items():
            if "location" in key.lower() or "city" in key.lower():
                location = value
                break
        
        if location:
            local_prompt = f"""Add local context for {location}:

Include 2-3 specific local details that make this content unique to {location}.
Keep it brief and relevant."""
            
            local_content = await self.ai_client.generate(local_prompt)
            
            return {
                "heading": f"Why Choose {location}",
                "content": local_content,
                "type": "local_context"
            }
        
        return {
            "heading": "Local Information",
            "content": "Local context information",
            "type": "local_context"
        }
    
    def _calculate_uniqueness_score(
        self,
        page: Dict[str, Any],
        existing_pages: List[Dict[str, Any]]
    ) -> float:
        """Calculate uniqueness score compared to existing pages"""
        if not existing_pages:
            return 100.0
        
        # Sample comparison (don't compare against all for performance)
        sample_size = min(10, len(existing_pages))
        sample_pages = random.sample(existing_pages, sample_size)
        
        uniqueness_scores = []
        for other_page in sample_pages:
            score = self.variation_engine.calculate_uniqueness_score(
                page["content"],
                other_page.get("content", "")
            )
            uniqueness_scores.append(score)
        
        return sum(uniqueness_scores) / len(uniqueness_scores) if uniqueness_scores else 100.0
    
    def _truncate_smartly(self, text: str, max_length: int) -> str:
        """Truncate text at word boundary"""
        if len(text) <= max_length:
            return text
        
        # Find last space before max_length
        truncated = text[:max_length]
        last_space = truncated.rfind(' ')
        
        if last_space > max_length * 0.8:  # If space is reasonably close
            return truncated[:last_space]
        
        return truncated
    
    def _optimize_heading_structure(self, page: Dict[str, Any]) -> Dict[str, Any]:
        """Ensure proper H1-H6 hierarchy"""
        # H1 is already set
        # Ensure all section headings are H2
        for section in page["content_sections"]:
            if not section["heading"].startswith("##"):
                section["heading"] = section["heading"].replace("#", "").strip()
        
        return page
    
    def _generate_schema_markup(
        self,
        page: Dict[str, Any],
        template: Dict[str, Any],
        business_info: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Generate appropriate schema markup"""
        schema_template = template.get("schema_markup", {})
        
        # Fill template with page data
        schema = {}
        for key, value in schema_template.items():
            if isinstance(value, str):
                schema[key] = self._fill_template_string(value, page["data"])
            elif isinstance(value, dict):
                schema[key] = {
                    k: self._fill_template_string(v, page["data"]) if isinstance(v, str) else v
                    for k, v in value.items()
                }
            else:
                schema[key] = value
        
        # Add additional properties
        schema["url"] = page["seo"]["url"]
        schema["datePublished"] = page["generated_at"]
        schema["dateModified"] = page["generated_at"]
        
        if business_info:
            schema["author"] = {
                "@type": "Organization",
                "name": business_info.get("name", "Unknown")
            }
        
        return schema
    
    def _optimize_keyword_density(self, page: Dict[str, Any]) -> Dict[str, Any]:
        """Optimize keyword density in content"""
        main_keywords = self._extract_keywords(page)[:3]  # Top 3 keywords
        
        content = page["content"]
        word_count = len(content.split())
        
        for keyword in main_keywords:
            keyword_count = content.lower().count(keyword.lower())
            density = (keyword_count / word_count) * 100 if word_count > 0 else 0
            
            # Target 1-3% density
            if density < 1 and word_count > 100:
                # Add keyword mentions where natural
                # This is a simplified approach - in production, use NLP
                page["seo"]["keyword_optimization"] = {
                    keyword: {
                        "current_density": density,
                        "target_density": "1-3%",
                        "recommendation": "Consider adding keyword naturally"
                    }
                }
        
        return page
    
    def _generate_breadcrumbs(
        self,
        page: Dict[str, Any],
        business_info: Optional[Dict[str, Any]]
    ) -> List[Dict[str, str]]:
        """Generate breadcrumb navigation"""
        breadcrumbs = [
            {"name": "Home", "url": "/"}
        ]
        
        # Add category if applicable
        if business_info and "industry" in business_info:
            breadcrumbs.append({
                "name": business_info["industry"],
                "url": f"/{business_info['industry'].lower().replace(' ', '-')}"
            })
        
        # Add current page
        breadcrumbs.append({
            "name": page["seo"]["h1"],
            "url": page["seo"]["url"]
        })
        
        return breadcrumbs
    
    def _generate_meta_tags(
        self,
        page: Dict[str, Any],
        business_info: Optional[Dict[str, Any]]
    ) -> Dict[str, str]:
        """Generate additional meta tags"""
        meta_tags = {
            "description": page["seo"]["meta_description"],
            "robots": "index, follow",
            "viewport": "width=device-width, initial-scale=1",
            "charset": "UTF-8"
        }
        
        # Open Graph tags
        meta_tags["og:title"] = page["seo"]["title"]
        meta_tags["og:description"] = page["seo"]["meta_description"]
        meta_tags["og:type"] = "article"
        meta_tags["og:url"] = page["canonical_url"]
        
        if business_info:
            meta_tags["og:site_name"] = business_info.get("name", "")
        
        # Twitter Card tags
        meta_tags["twitter:card"] = "summary"
        meta_tags["twitter:title"] = page["seo"]["title"]
        meta_tags["twitter:description"] = page["seo"]["meta_description"]
        
        return meta_tags
    
    def _add_internal_linking(
        self,
        pages: List[Dict[str, Any]],
        business_info: Optional[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Add internal links between related pages"""
        # Extract all page keywords for linking
        all_keywords = []
        for page in pages:
            all_keywords.extend([
                kw for kw in self._extract_keywords(page)
            ])
        
        # Process each page
        for i, page in enumerate(pages):
            # Find related pages
            page_keywords = self._extract_keywords(page)
            related_pages = []
            
            for j, other_page in enumerate(pages):
                if i != j:  # Don't link to self
                    other_keywords = self._extract_keywords(other_page)
                    
                    # Calculate relevance
                    common_keywords = set(page_keywords) & set(other_keywords)
                    if len(common_keywords) >= 2:  # At least 2 common keywords
                        related_pages.append({
                            "page": other_page,
                            "relevance": len(common_keywords) / len(page_keywords),
                            "common_keywords": list(common_keywords)
                        })
            
            # Sort by relevance
            related_pages.sort(key=lambda x: x["relevance"], reverse=True)
            
            # Add internal links to content
            if related_pages:
                internal_links = []
                for related in related_pages[:5]:  # Top 5 related pages
                    internal_links.append({
                        "url": related["page"]["seo"]["url"],
                        "anchor_text": related["page"]["seo"]["h1"],
                        "relevance": related["relevance"]
                    })
                
                # Store internal links
                page["internal_links"] = internal_links
                
                # Add related articles section
                related_section = self._generate_related_articles_section(internal_links)
                page["content_sections"].append(related_section)
                
                # Update compiled content
                page["content"] = self._compile_content(page)
                
                self.generation_stats["internal_links_added"] += len(internal_links)
        
        return pages
    
    def _generate_related_articles_section(
        self,
        internal_links: List[Dict[str, str]]
    ) -> Dict[str, Any]:
        """Generate related articles section"""
        content = "Explore these related topics:\n\n"
        
        for link in internal_links[:4]:
            content += f"- [{link['anchor_text']}]({link['url']})\n"
        
        return {
            "heading": "Related Articles",
            "content": content,
            "type": "related_articles"
        }
    
    def _calculate_average_uniqueness(self) -> float:
        """Calculate average uniqueness score across all pages"""
        if not self.generated_pages:
            return 0.0
        
        scores = [
            page.get("uniqueness_score", 0)
            for page in self.generated_pages.values()
        ]
        
        return sum(scores) / len(scores) if scores else 0.0
    
    def _get_content_type_distribution(self) -> Dict[str, int]:
        """Get distribution of content types"""
        distribution = defaultdict(int)
        
        for page in self.generated_pages.values():
            distribution[page.get("content_type", "unknown")] += 1
        
        return dict(distribution)
    
    def _get_quality_summary(self) -> Dict[str, Any]:
        """Get summary of content quality metrics"""
        quality_scores = []
        word_counts = []
        
        for page in self.generated_pages.values():
            if "quality_metrics" in page:
                quality_scores.append(page["quality_metrics"].get("quality_score", 0))
                word_counts.append(page["quality_metrics"].get("word_count", 0))
        
        if not quality_scores:
            return {
                "average_quality_score": 0,
                "average_word_count": 0,
                "quality_distribution": {}
            }
        
        return {
            "average_quality_score": sum(quality_scores) / len(quality_scores),
            "average_word_count": sum(word_counts) / len(word_counts),
            "quality_distribution": {
                "excellent": sum(1 for s in quality_scores if s >= 90),
                "good": sum(1 for s in quality_scores if 70 <= s < 90),
                "fair": sum(1 for s in quality_scores if 50 <= s < 70),
                "poor": sum(1 for s in quality_scores if s < 50)
            }
        }