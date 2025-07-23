"""Smart AI-powered page generator using centralized prompts - Example Integration"""
import json
import hashlib
from datetime import datetime
from typing import Dict, List, Any, Optional
from efficient_page_generator import EfficientPageGenerator
from data_enricher import DataEnricher
from api.ai_handler import AIHandler
from config.prompt_manager import get_prompt_manager


class SmartPageGeneratorEnhanced(EfficientPageGenerator):
    """Enhanced page generator that uses centralized AI prompts with real data"""
    
    def __init__(self):
        super().__init__()
        self.data_enricher = DataEnricher()
        self.ai_handler = AIHandler()
        self.prompt_manager = get_prompt_manager()
        
    def _generate_ai_content(self, 
                           title: str, 
                           content_type: str,
                           enriched_data: Dict[str, Any],
                           tone: Optional[str] = None) -> str:
        """Generate content using AI with centralized prompts
        
        Args:
            title: The page title
            content_type: Type of content (evaluation_question, location_service, etc.)
            enriched_data: Enriched data from DataEnricher
            tone: Optional tone variation
            
        Returns:
            Generated content
        """
        # Prepare data summary
        data_summary = self._format_data_summary(enriched_data)
        
        # Get prompt from centralized configuration
        prompt_data = self.prompt_manager.get_prompt(
            category="content_generation",
            prompt_type=content_type,
            variables={
                "title": title,
                "data_summary": data_summary,
                "business_context": enriched_data.get("business_context", "")
            },
            tone=tone,
            use_rotation=True  # Enable variation rotation
        )
        
        # Get model configuration for content generation
        model_config = self.prompt_manager.get_model_config("primary")
        
        try:
            # Generate content using AI
            response = self.ai_handler.generate_content_with_config(
                system_prompt=prompt_data["system"],
                user_prompt=prompt_data["user"],
                model_config=model_config
            )
            
            # Validate generated content
            validation = self.prompt_manager.validate_content(response, content_type)
            if not validation["passed"]:
                print(f"Content validation issues: {validation['issues']}")
                # Could retry with different prompt or tone here
            
            return response
            
        except Exception as e:
            print(f"AI generation failed: {str(e)}")
            # Fall back to pattern-based generation
            return self._generate_fallback_content(title, content_type, enriched_data)
    
    def generate_page_content(self, template: Dict, data_row: Dict) -> Dict[str, Any]:
        """Generate complete page content with enhanced AI integration
        
        Args:
            template: Template configuration
            data_row: Data for variable substitution
            
        Returns:
            Complete page content
        """
        # Get enriched data
        enriched_data = self.data_enricher.enrich_data(data_row, template)
        
        # Determine content type from template
        content_type = self._determine_content_type(template)
        
        # Select tone based on template or random rotation
        available_tones = self.prompt_manager.get_tone_options()
        selected_tone = template.get("tone") or (available_tones[0] if available_tones else None)
        
        # Generate title
        title = self._substitute_variables(template["pattern"], data_row)
        
        # Generate AI content with centralized prompts
        ai_content = self._generate_ai_content(
            title=title,
            content_type=content_type,
            enriched_data=enriched_data,
            tone=selected_tone
        )
        
        # Generate meta description using centralized prompt
        meta_description = self._generate_meta_description(title, ai_content)
        
        # Build complete page content
        page_content = {
            "title": title,
            "meta_description": meta_description,
            "h1": title,
            "content": ai_content,
            "content_html": self._format_as_html(ai_content),
            "word_count": len(ai_content.split()),
            "quality_score": enriched_data.get("data_quality", 0.5) * 100,
            "tone": selected_tone,
            "content_type": content_type,
            "generated_at": datetime.now().isoformat(),
            "generation_method": "ai_enhanced_centralized",
            "prompt_version": self.prompt_manager.config.get("version", "1.0.0")
        }
        
        # Add schema markup if applicable
        schema_markup = self._generate_schema_markup(content_type, page_content)
        if schema_markup:
            page_content["schema_markup"] = schema_markup
        
        return page_content
    
    def _generate_meta_description(self, title: str, content: str) -> str:
        """Generate SEO meta description using centralized prompt"""
        # Get first 200 chars of content as summary
        page_summary = content[:200].strip() + "..."
        
        prompt_data = self.prompt_manager.get_prompt(
            category="meta_generation",
            prompt_type="meta_description",
            variables={
                "title": title,
                "page_summary": page_summary
            }
        )
        
        try:
            meta_desc = self.ai_handler.generate_content_with_config(
                system_prompt=prompt_data["system"],
                user_prompt=prompt_data["user"],
                model_config={"max_tokens": 200, "temperature": 0.5}
            )
            # Ensure it's under 155 characters
            if len(meta_desc) > 155:
                meta_desc = meta_desc[:152] + "..."
            return meta_desc
        except:
            # Fallback
            return f"{title}. Get detailed information and insights."
    
    def _determine_content_type(self, template: Dict) -> str:
        """Determine content type from template pattern"""
        pattern = template.get("pattern", "").lower()
        
        if "?" in pattern or "is" in pattern:
            return "evaluation_question"
        elif "in {city}" in pattern or "in {location}" in pattern:
            return "location_service"
        elif "vs" in pattern or "comparison" in pattern:
            return "comparison"
        else:
            return "generic"
    
    def _generate_schema_markup(self, content_type: str, page_content: Dict) -> Optional[Dict]:
        """Generate appropriate schema markup based on content type"""
        # This would be implemented in the schema generator subagent
        # For now, return None
        return None
    
    def _format_data_summary(self, enriched_data: Dict) -> str:
        """Format enriched data into a summary for AI prompt"""
        summary_parts = []
        
        if "rental_rate" in enriched_data:
            summary_parts.append(f"Average rental rate: ${enriched_data['rental_rate']}/night")
        if "occupancy_rate" in enriched_data:
            summary_parts.append(f"Occupancy rate: {enriched_data['occupancy_rate']}%")
        if "market_size" in enriched_data:
            summary_parts.append(f"Market size: {enriched_data['market_size']} properties")
        if "growth_rate" in enriched_data:
            summary_parts.append(f"YoY growth: {enriched_data['growth_rate']}%")
        
        return "\n".join(summary_parts)
    
    def _format_as_html(self, content: str) -> str:
        """Convert content to HTML format"""
        # Simple markdown-like conversion
        html = f"<p>{content}</p>"
        # Add more sophisticated formatting as needed
        return html
    
    def _generate_fallback_content(self, title: str, content_type: str, data: Dict) -> str:
        """Generate fallback content if AI fails"""
        # Use pattern-based generation as fallback
        return f"Information about {title}. Details coming soon."


# Example usage documentation
"""
How to use the enhanced generator with centralized prompts:

1. The generator automatically loads prompts from config/prompts_config.json
2. Prompts are rotated through variations to reduce duplication
3. Tone can be specified per template or will rotate automatically
4. Content is validated against configured requirements
5. Model configuration is centralized and can be changed without code updates

To add new prompts:
1. Edit backend/config/prompts_config.json
2. Add your prompt under the appropriate category
3. Include system prompt, user prompt, and variations
4. The prompt manager will automatically use them

To view available prompts:
    prompt_manager = get_prompt_manager()
    print(prompt_manager.list_prompts())
    print(prompt_manager.get_tone_options())
"""