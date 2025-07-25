"""AI-powered visual element generator for programmatic SEO content - Version 2"""
import json
from typing import Dict, List, Any
from api.ai_handler import AIHandler

class AIVisualGenerator:
    """Generate visual elements dynamically based on content context using AI"""
    
    def __init__(self):
        self.ai_handler = AIHandler()
        
    def enhance_content_with_visuals(self, content_html: str, template_data: Dict[str, Any], 
                                    enriched_data: Dict[str, Any]) -> str:
        """Enhance content with AI-generated visual elements"""
        
        if not self.ai_handler.has_ai_provider():
            # Fallback to basic visual generation if no AI
            return self._add_basic_visuals(content_html, template_data, enriched_data)
        
        # Let AI generate contextually appropriate visuals
        enhanced_content = self._generate_ai_visuals(content_html, template_data, enriched_data)
        
        return enhanced_content
    
    def _generate_ai_visuals(self, content_html: str, template_data: Dict[str, Any], 
                             enriched_data: Dict[str, Any]) -> str:
        """Let AI generate contextually appropriate visual elements"""
        
        # Prepare comprehensive context for AI
        prompt = f"""You are enhancing a blog post with visual elements. Analyze the content and context to create appropriate visual elements.

CONTENT:
{content_html[:1500]}

CONTEXT:
Title: {template_data.get('title', 'N/A')}
Pattern: {template_data.get('pattern', 'N/A')}
All Variables: {json.dumps(template_data, indent=2)[:500]}

AVAILABLE DATA:
{json.dumps(enriched_data.get('primary_data', {}), indent=2)[:800]}

TASK:
Create 2-3 HTML visual elements that enhance this specific content. The visuals should:
1. Be directly relevant to the content topic
2. Use the actual data provided above
3. Enhance reader understanding
4. Be visually appealing with inline CSS

EXAMPLES OF APPROPRIATE VISUALS:
- For "X vs Y" comparisons: Feature comparison table, pros/cons lists, pricing differences
- For investment/ROI content: ROI calculator, market stats table, investment breakdown
- For service listings: Provider comparison table, pricing tiers, service checklist
- For how-to content: Step-by-step process, checklist, timeline
- For product reviews: Feature comparison, rating breakdown, price comparison

CRITICAL: The visuals MUST match the content. If this is about "Viome vs Thorne", create a comparison table of their features, NOT a generic provider stats box.

Return ONLY the HTML for the visual elements. Use inline CSS. Make it specific to THIS content."""

        try:
            # Generate visuals with AI
            visual_html = self.ai_handler.generate_content(prompt, max_tokens=2000)
            
            if visual_html:
                # Insert visuals into content at appropriate positions
                return self._insert_visuals_into_content(content_html, visual_html)
            
        except Exception as e:
            print(f"AI visual generation error: {str(e)}")
        
        # Fallback to basic visuals
        return self._add_basic_visuals(content_html, template_data, enriched_data)
    
    def _insert_visuals_into_content(self, content_html: str, visual_html: str) -> str:
        """Insert AI-generated visuals at strategic points in content"""
        
        # Clean up the AI response - remove any markdown or explanatory text
        visual_html = self._clean_ai_response(visual_html)
        
        # Parse visual HTML into individual elements
        visuals = self._parse_visual_elements(visual_html)
        
        if not visuals:
            return content_html
        
        # Split content by paragraphs
        sections = content_html.split('</p>')
        
        # Insert visuals at strategic positions
        if len(visuals) >= 1 and len(sections) > 1:
            # First visual after intro paragraph
            sections[0] += '</p>\n' + visuals[0] + '\n'
        
        if len(visuals) >= 2 and len(sections) > 3:
            # Second visual in middle of content
            mid_point = len(sections) // 2
            sections[mid_point] += '</p>\n' + visuals[1] + '\n'
        
        if len(visuals) >= 3 and len(sections) > 4:
            # Third visual before conclusion (but not in the very last paragraph)
            sections[-2] += '</p>\n' + visuals[2] + '\n'
        
        return ''.join(sections)
    
    def _clean_ai_response(self, response: str) -> str:
        """Clean AI response to extract only HTML"""
        # Remove markdown code blocks
        if '```html' in response:
            start = response.find('```html') + 7
            end = response.find('```', start)
            if end > start:
                response = response[start:end]
        elif '```' in response:
            start = response.find('```') + 3
            end = response.find('```', start)
            if end > start:
                response = response[start:end]
        
        # Remove any explanatory text before first HTML tag
        if '<' in response:
            first_tag = response.find('<')
            if first_tag > 0:
                # Check if there's non-HTML content before
                prefix = response[:first_tag].strip()
                if prefix and not prefix.endswith('>'):
                    response = response[first_tag:]
        
        return response.strip()
    
    def _parse_visual_elements(self, visual_html: str) -> List[str]:
        """Parse individual visual elements from AI response"""
        visuals = []
        
        # Find all top-level divs or tables
        html = visual_html
        while html:
            # Find next top-level element
            if html.startswith('<div'):
                # Find matching closing div
                end_pos = self._find_closing_tag(html, 'div')
                if end_pos > 0:
                    visuals.append(html[:end_pos])
                    html = html[end_pos:].strip()
                else:
                    break
            elif html.startswith('<table'):
                # Find matching closing table
                end_pos = self._find_closing_tag(html, 'table')
                if end_pos > 0:
                    visuals.append(html[:end_pos])
                    html = html[end_pos:].strip()
                else:
                    break
            else:
                # Skip to next tag
                next_tag = html.find('<', 1)
                if next_tag > 0:
                    html = html[next_tag:]
                else:
                    break
        
        return visuals[:3]  # Max 3 visuals
    
    def _find_closing_tag(self, html: str, tag_name: str) -> int:
        """Find the position after the closing tag for a given opening tag"""
        tag_count = 1
        pos = len(f'<{tag_name}')
        
        while tag_count > 0 and pos < len(html):
            # Look for opening tag
            open_tag = html.find(f'<{tag_name}', pos)
            # Look for closing tag
            close_tag = html.find(f'</{tag_name}>', pos)
            
            if close_tag == -1:
                return -1
            
            if open_tag != -1 and open_tag < close_tag:
                tag_count += 1
                pos = open_tag + len(f'<{tag_name}')
            else:
                tag_count -= 1
                pos = close_tag + len(f'</{tag_name}>')
                
        return pos if tag_count == 0 else -1
    
    def _add_basic_visuals(self, content_html: str, template_data: Dict[str, Any], 
                          enriched_data: Dict[str, Any]) -> str:
        """Add basic visuals without AI - simplified fallback"""
        
        # Detect if this is a comparison
        title = template_data.get('title', '').lower()
        pattern = template_data.get('pattern', '').lower()
        
        # Create a simple visual based on content type
        if ' vs ' in title or ' versus ' in title:
            # Comparison visual
            visual = self._create_simple_comparison_visual(template_data, enriched_data)
        elif any(word in pattern for word in ['investment', 'profitable', 'roi']):
            # Investment visual
            visual = self._create_simple_investment_visual(template_data, enriched_data)
        else:
            # Generic stats visual
            visual = self._create_simple_stats_visual(template_data, enriched_data)
        
        # Insert after first paragraph
        sections = content_html.split('</p>', 1)
        if len(sections) > 1:
            return sections[0] + '</p>\n' + visual + '\n' + sections[1]
        else:
            return content_html + '\n' + visual
    
    def _create_simple_comparison_visual(self, template_data: Dict[str, Any], 
                                       enriched_data: Dict[str, Any]) -> str:
        """Create a simple comparison table for fallback"""
        # Extract the two items being compared
        title = template_data.get('title', '')
        if ' vs ' in title:
            parts = title.split(' vs ')
            item1 = parts[0].strip()
            item2 = parts[1].split()[0].strip() if parts[1] else 'Option B'
        else:
            item1 = 'Option A'
            item2 = 'Option B'
        
        return f"""<div style="margin: 2rem 0; border: 1px solid #e5e7eb; border-radius: 0.5rem; overflow: hidden;">
  <table style="width: 100%; border-collapse: collapse;">
    <thead>
      <tr style="background: #f3f4f6;">
        <th style="padding: 1rem; text-align: left; font-weight: 600;">Feature</th>
        <th style="padding: 1rem; text-align: center; font-weight: 600;">{item1}</th>
        <th style="padding: 1rem; text-align: center; font-weight: 600;">{item2}</th>
      </tr>
    </thead>
    <tbody>
      <tr style="border-top: 1px solid #e5e7eb;">
        <td style="padding: 1rem;">Price</td>
        <td style="padding: 1rem; text-align: center;">Check website</td>
        <td style="padding: 1rem; text-align: center;">Check website</td>
      </tr>
      <tr style="border-top: 1px solid #e5e7eb; background: #f9fafb;">
        <td style="padding: 1rem;">Rating</td>
        <td style="padding: 1rem; text-align: center;">★★★★☆</td>
        <td style="padding: 1rem; text-align: center;">★★★★☆</td>
      </tr>
      <tr style="border-top: 1px solid #e5e7eb;">
        <td style="padding: 1rem;">Best For</td>
        <td style="padding: 1rem; text-align: center;">Various uses</td>
        <td style="padding: 1rem; text-align: center;">Various uses</td>
      </tr>
    </tbody>
  </table>
</div>"""
    
    def _create_simple_investment_visual(self, template_data: Dict[str, Any], 
                                       enriched_data: Dict[str, Any]) -> str:
        """Create a simple investment stats visual for fallback"""
        primary_data = enriched_data.get('primary_data', {})
        
        return f"""<div style="background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%); border: 1px solid #7dd3fc; padding: 1.5rem; border-radius: 0.75rem; margin: 2rem 0;">
  <h3 style="margin: 0 0 1rem 0; color: #0369a1;">📊 Investment Overview</h3>
  <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 1rem;">
    <div style="text-align: center;">
      <div style="font-size: 1.75rem; font-weight: bold; color: #0ea5e9;">{primary_data.get('roi_percentage', '15')}%</div>
      <div style="color: #64748b; font-size: 0.875rem;">Estimated ROI</div>
    </div>
    <div style="text-align: center;">
      <div style="font-size: 1.75rem; font-weight: bold; color: #0ea5e9;">{primary_data.get('occupancy_rate', '68')}%</div>
      <div style="color: #64748b; font-size: 0.875rem;">Occupancy Rate</div>
    </div>
  </div>
</div>"""
    
    def _create_simple_stats_visual(self, template_data: Dict[str, Any], 
                                   enriched_data: Dict[str, Any]) -> str:
        """Create a simple stats visual for fallback"""
        primary_data = enriched_data.get('primary_data', {})
        service = template_data.get('Service', template_data.get('service', 'Options'))
        city = template_data.get('City', template_data.get('city', 'your area'))
        
        return f"""<div style="background: #f8fafc; border: 1px solid #e2e8f0; padding: 1.5rem; border-radius: 0.5rem; margin: 2rem 0;">
  <h3 style="margin: 0 0 1rem 0; color: #1e293b;">📌 {service} in {city}</h3>
  <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 1rem;">
    <div>
      <strong style="color: #64748b;">Available Options:</strong>
      <span style="display: block; font-size: 1.25rem; color: #1e293b;">{primary_data.get('count', 'Multiple')}</span>
    </div>
    <div>
      <strong style="color: #64748b;">Average Rating:</strong>
      <span style="display: block; font-size: 1.25rem; color: #16a34a;">{primary_data.get('average_rating', '4.5')}★</span>
    </div>
  </div>
</div>"""