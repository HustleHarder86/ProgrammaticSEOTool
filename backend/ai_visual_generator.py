"""AI-powered visual element generator for programmatic SEO content - Version 3"""
import json
import re
from typing import Dict, List, Any, Optional, Tuple
from api.ai_handler import AIHandler


class AIVisualGenerator:
    """Generate visual elements dynamically based on content context using AI"""
    
    def __init__(self):
        self.ai_handler = AIHandler()
        
    def enhance_content_with_visuals(self, content_html: str, template_data: Dict[str, Any], 
                                    enriched_data: Dict[str, Any]) -> str:
        """Enhance content with AI-generated visual elements - AI only, no fallbacks"""
        
        if not self.ai_handler.has_ai_provider():
            # Return content without visuals if no AI available
            print("⚠️ No AI provider configured - returning content without visuals")
            return content_html
        
        # Generate AI visuals based on actual blog content
        enhanced_content = self._generate_ai_visuals(content_html, template_data, enriched_data)
        
        return enhanced_content
    
    def _generate_ai_visuals(self, content_html: str, template_data: Dict[str, Any], 
                             enriched_data: Dict[str, Any]) -> str:
        """Generate contextually appropriate visual elements using AI"""
        
        # Extract key statistics and claims from the content
        content_analysis = self._analyze_blog_content(content_html)
        
        # Prepare comprehensive context for AI
        prompt = f"""You are creating HTML visual elements for a blog post. Your visuals MUST be directly based on the content.

BLOG CONTENT TO ANALYZE:
{content_html}

KEY STATISTICS FOUND IN ARTICLE:
{json.dumps(content_analysis['statistics'], indent=2)}

KEY CLAIMS/POINTS IN ARTICLE:
{json.dumps(content_analysis['key_points'], indent=2)}

ARTICLE CONTEXT:
Title: {template_data.get('title', 'N/A')}
Main Topic: {content_analysis.get('main_topic', 'N/A')}
Content Type: {content_analysis.get('content_type', 'N/A')}

AVAILABLE ENRICHED DATA:
{json.dumps(enriched_data.get('primary_data', {}), indent=2)}

CRITICAL INSTRUCTIONS:
1. READ THE ENTIRE BLOG CONTENT ABOVE
2. Create 2-3 HTML visuals that DIRECTLY SUPPORT the article's specific claims
3. Use ONLY numbers and data mentioned in the article or provided in enriched data
4. Each visual must relate to a specific point made in the article
5. DO NOT create generic visuals - they must be content-specific

VISUAL REQUIREMENTS:
- Use the EXACT statistics mentioned in the article
- Support the article's main arguments with data
- Simple HTML with inline CSS (no external dependencies)
- Focus on clarity and readability

EXAMPLE APPROACH:
- If article says "68% occupancy rate in Winnipeg", create a stat box showing exactly 68%
- If article compares two products, create a table with the specific features discussed
- If article mentions "average nightly rate of $127", show exactly $127 in your visual

ACCEPTABLE VISUAL TYPES:
- Stat boxes with specific numbers from the article
- Comparison tables using actual features discussed
- Data highlights that reinforce article claims
- Simple grids showing real data points
- Info cards with key facts from the content

Return ONLY the HTML for 2-3 visual elements. Each visual must directly support a specific claim or data point from the article."""

        max_retries = 3
        for attempt in range(max_retries):
            try:
                # Generate visuals with AI
                visual_html = self.ai_handler.generate_content(prompt, max_tokens=2500)
                
                if visual_html:
                    # Validate that visuals contain actual data from article
                    if self._validate_visual_relevance(visual_html, content_analysis):
                        # Insert visuals into content at appropriate positions
                        return self._insert_visuals_into_content(content_html, visual_html)
                    else:
                        print(f"Attempt {attempt + 1}: Visuals not relevant enough, retrying...")
                        # Add more specific instructions for retry
                        prompt += f"\n\nRETRY {attempt + 1}: The visuals MUST include these specific numbers: {content_analysis['statistics'][:3]}"
                
            except Exception as e:
                print(f"AI visual generation error (attempt {attempt + 1}): {str(e)}")
        
        # If all attempts fail, return content without visuals
        print("⚠️ Could not generate relevant visuals after multiple attempts")
        return content_html
    
    def _analyze_blog_content(self, content_html: str) -> Dict[str, Any]:
        """Analyze blog content to extract key information for visual generation"""
        
        # Remove HTML tags for analysis
        text_content = re.sub('<.*?>', '', content_html)
        
        # Extract statistics (numbers with context)
        statistics = []
        stat_patterns = [
            r'(\d+\.?\d*)\s*%',  # Percentages
            r'\$\s*(\d+\.?\d*)',  # Dollar amounts
            r'(\d+)\s+(?:providers?|listings?|properties|options?|companies)',  # Counts
            r'(\d+\.?\d*)\s*(?:rating|stars?|★)',  # Ratings
            r'average\s+(?:of\s+)?(\d+\.?\d*)',  # Averages
            r'(\d+)\s*(?:year|month|day|hour)s?',  # Time periods
        ]
        
        for pattern in stat_patterns:
            matches = re.finditer(pattern, text_content, re.IGNORECASE)
            for match in matches:
                context_start = max(0, match.start() - 50)
                context_end = min(len(text_content), match.end() + 50)
                context = text_content[context_start:context_end].strip()
                statistics.append({
                    'value': match.group(1),
                    'context': context,
                    'full_match': match.group(0)
                })
        
        # Extract key points (sentences with important keywords)
        key_points = []
        sentences = text_content.split('.')
        important_keywords = ['profitable', 'best', 'average', 'compared', 'versus', 'better', 
                            'recommended', 'popular', 'rated', 'cost', 'price', 'roi', 'return']
        
        for sentence in sentences[:20]:  # Focus on first 20 sentences
            sentence_lower = sentence.lower()
            if any(keyword in sentence_lower for keyword in important_keywords):
                key_points.append(sentence.strip())
        
        # Determine content type
        content_lower = text_content.lower()
        if ' vs ' in content_lower or ' versus ' in content_lower:
            content_type = 'comparison'
        elif 'profitable' in content_lower or 'investment' in content_lower or 'roi' in content_lower:
            content_type = 'investment_analysis'
        elif 'service' in content_lower or 'provider' in content_lower:
            content_type = 'service_listing'
        else:
            content_type = 'informational'
        
        # Extract main topic
        title_match = re.search(r'<h1[^>]*>(.*?)</h1>', content_html, re.IGNORECASE)
        main_topic = title_match.group(1) if title_match else 'Unknown Topic'
        
        return {
            'statistics': statistics[:10],  # Top 10 statistics
            'key_points': key_points[:5],   # Top 5 key points
            'content_type': content_type,
            'main_topic': main_topic,
            'word_count': len(text_content.split())
        }
    
    def _validate_visual_relevance(self, visual_html: str, content_analysis: Dict[str, Any]) -> bool:
        """Validate that generated visuals actually use data from the article"""
        
        # Check if any statistics from the article appear in the visuals
        stats_found = 0
        for stat in content_analysis['statistics']:
            if stat['value'] in visual_html or stat['full_match'] in visual_html:
                stats_found += 1
        
        # Require at least 2 statistics to be used, or 50% of available stats
        min_stats_required = min(2, len(content_analysis['statistics']) // 2)
        
        return stats_found >= min_stats_required
    
    def _insert_visuals_into_content(self, content_html: str, visual_html: str) -> str:
        """Insert AI-generated visuals at strategic points in content"""
        
        # Clean up the AI response
        visual_html = self._clean_ai_response(visual_html)
        
        # Parse visual HTML into individual elements
        visuals = self._parse_visual_elements(visual_html)
        
        if not visuals:
            return content_html
        
        # Split content by paragraphs
        sections = content_html.split('</p>')
        
        # Insert visuals at strategic positions
        if len(visuals) >= 1 and len(sections) > 1:
            # First visual after intro paragraph (usually 2nd or 3rd paragraph)
            insert_pos = min(2, len(sections) - 1)
            sections[insert_pos - 1] += '</p>\n' + visuals[0] + '\n'
        
        if len(visuals) >= 2 and len(sections) > 4:
            # Second visual in middle of content
            mid_point = len(sections) // 2
            sections[mid_point] += '</p>\n' + visuals[1] + '\n'
        
        if len(visuals) >= 3 and len(sections) > 6:
            # Third visual before conclusion
            sections[-3] += '</p>\n' + visuals[2] + '\n'
        
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