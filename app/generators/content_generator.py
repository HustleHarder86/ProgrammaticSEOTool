"""Content generation module using AI."""
import logging
import re
import json
from typing import Dict, List, Optional
from app.templates.content_templates import get_template
from app.utils.ai_client import AIClient
from app.agents.content_variation_agent import ContentVariationAgent
from config import settings
import markdown

logger = logging.getLogger(__name__)

class ContentGenerator:
    """Generates SEO-optimized content using AI."""
    
    def __init__(self):
        self.ai_client = AIClient()
        self.md = markdown.Markdown(extensions=['extra', 'codehilite', 'tables'])
        self.variation_agent = ContentVariationAgent()
    
    async def generate_content(
        self, 
        keyword: str, 
        template_type: str, 
        business_info: Dict,
        variation: int = 1
    ) -> Dict:
        """Generate content for a keyword using a specific template."""
        template = get_template(template_type)
        
        # Generate content variables
        variables = await self._generate_template_variables(
            keyword, template, business_info, variation
        )
        
        # Fill template
        content_markdown = self._fill_template(template["structure"], variables)
        
        # Generate meta information
        meta_info = await self._generate_meta_info(keyword, content_markdown, business_info)
        
        # Ensure title uniqueness
        unique_title = self.variation_agent.ensure_title_uniqueness(meta_info["title"], keyword)
        
        # Add unique elements to content
        unique_elements = self.variation_agent.add_unique_elements(
            content_markdown, keyword, template_type
        )
        
        # Apply variations to ensure uniqueness
        enhanced_markdown = self.variation_agent.apply_content_variations(
            content_markdown, unique_elements
        )
        
        # Check content uniqueness
        is_unique, uniqueness_score = self.variation_agent.is_content_unique(enhanced_markdown)
        
        # Convert to HTML
        content_html = self.md.convert(enhanced_markdown)
        
        # Calculate word count
        word_count = len(enhanced_markdown.split())
        
        return {
            "title": unique_title,
            "meta_description": meta_info["meta_description"],
            "slug": self._generate_slug(unique_title),
            "content_markdown": enhanced_markdown,
            "content_html": content_html,
            "word_count": word_count,
            "template_used": template_type,
            "variation_number": variation,
            "unique_elements": unique_elements.get('unique_elements', []),
            "uniqueness_score": uniqueness_score
        }
    
    async def _generate_template_variables(
        self, 
        keyword: str, 
        template: Dict, 
        business_info: Dict,
        variation: int
    ) -> Dict:
        """Generate all variables needed for a template."""
        prompt = f"""Generate content for this SEO keyword using the template variables.

Keyword: {keyword}
Template Type: {template['name']}
Business Info: {json.dumps(business_info, indent=2)}
Variation Number: {variation}

Generate unique, high-quality content for each variable. Make it informative, engaging, and SEO-friendly.
Aim for comprehensive coverage while maintaining readability.

Variables needed:
{json.dumps(template['variables'], indent=2)}

Important guidelines:
1. Create genuinely helpful content that provides value
2. Use natural language and avoid keyword stuffing
3. Include specific examples and actionable advice
4. For variation {variation}, ensure content is unique from other variations
5. Target 2000-3000 words total when all variables are combined

Respond with a JSON object containing all variables."""

        try:
            content = await self.ai_client.generate(
                prompt=prompt,
                temperature=0.7 + (variation * 0.1),  # Increase randomness for variations
                max_tokens=4000
            )
            
            # Parse JSON response
            variables = json.loads(content)
            return variables
            
        except Exception as e:
            logger.error(f"Error generating template variables: {e}")
            # Return default variables on error
            return {var: f"[Content for {var}]" for var in template['variables']}
    
    def _fill_template(self, template_structure: str, variables: Dict) -> str:
        """Fill template with generated variables."""
        content = template_structure
        
        for var_name, var_content in variables.items():
            placeholder = f"{{{var_name}}}"
            content = content.replace(placeholder, str(var_content))
        
        return content
    
    async def _generate_meta_info(self, keyword: str, content: str, business_info: Dict) -> Dict:
        """Generate SEO meta information."""
        prompt = f"""Generate SEO meta information for this content.

Keyword: {keyword}
Business: {business_info.get('name', 'Business')}
Content Preview: {content[:500]}...

Generate:
1. An engaging, clickable title (50-60 characters) that includes the keyword
2. A compelling meta description (150-160 characters) that includes the keyword and encourages clicks

Respond with JSON containing 'title' and 'meta_description'."""

        try:
            content = await self.ai_client.generate(
                prompt=prompt,
                temperature=0.5,
                max_tokens=200
            )
            
            meta_info = json.loads(content)
            return meta_info
            
        except Exception as e:
            logger.error(f"Error generating meta info: {e}")
            # Return defaults on error
            return {
                "title": f"{keyword} - Complete Guide",
                "meta_description": f"Learn everything about {keyword}. Expert tips, guides, and resources."
            }
    
    def _generate_slug(self, title: str) -> str:
        """Generate URL-friendly slug from title."""
        # Convert to lowercase
        slug = title.lower()
        
        # Replace spaces with hyphens
        slug = re.sub(r'\s+', '-', slug)
        
        # Remove special characters
        slug = re.sub(r'[^a-z0-9-]', '', slug)
        
        # Remove multiple hyphens
        slug = re.sub(r'-+', '-', slug)
        
        # Trim hyphens from ends
        slug = slug.strip('-')
        
        return slug[:100]  # Limit length