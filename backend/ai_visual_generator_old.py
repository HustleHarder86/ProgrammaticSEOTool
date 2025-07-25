"""AI-powered visual element generator for programmatic SEO content"""
import json
from typing import Dict, List, Any
from api.ai_handler import AIHandler

class AIVisualGenerator:
    """Generate visual elements dynamically based on content context"""
    
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
        prompt = f"""You are enhancing a blog post with visual elements. Based on the content and context, generate 2-3 HTML visual elements that would enhance reader understanding and engagement.

CONTENT:
{content_html[:1000]}...

CONTEXT:
- Title: {template_data.get('title', '')}
- Pattern: {template_data.get('pattern', '')}
- Variables: {json.dumps(template_data, indent=2)}

AVAILABLE DATA:
{json.dumps(enriched_data.get('primary_data', {}), indent=2)}

INSTRUCTIONS:
1. Analyze the content type and topic
2. Create 2-3 visual elements that enhance understanding
3. Use the actual data provided above
4. Return ONLY the HTML for the visual elements
5. Use inline CSS for styling
6. Make visuals that match the specific content (e.g., comparison table for "X vs Y", ROI calculator for investment content, provider list for services)

IMPORTANT:
- For comparisons: Create comparison tables, pros/cons lists, feature differences
- For how-to: Create step-by-step guides, process flows, checklists
- For services: Create provider lists, pricing tables, feature comparisons
- For analysis/investment: Create data tables, ROI calculators, market stats

Generate the HTML visual elements that best match this specific content:"""

        try:
            # Generate visuals with AI
            visual_html = self.ai_handler.generate_content(prompt, max_tokens=1500)
            
            if visual_html:
                # Insert visuals into content at appropriate positions
                return self._insert_visuals_into_content(content_html, visual_html)
            
        except Exception as e:
            print(f"AI visual generation error: {str(e)}")
        
        # Fallback to basic visuals
        return self._add_basic_visuals(content_html, template_data, enriched_data)
    
    def _insert_visuals_into_content(self, content_html: str, visual_html: str) -> str:
        """Insert AI-generated visuals at strategic points in content"""
        
        # Parse visual HTML into individual elements
        visuals = self._parse_visual_elements(visual_html)
        
        if not visuals:
            return content_html
        
        # Split content by paragraphs
        sections = content_html.split('</p>')
        
        # Insert visuals at strategic positions
        if len(visuals) >= 1 and len(sections) > 1:
            # First visual after intro paragraph
            sections[0] += '</p>' + visuals[0]
        
        if len(visuals) >= 2 and len(sections) > 3:
            # Second visual in middle of content
            mid_point = len(sections) // 2
            sections[mid_point] += '</p>' + visuals[1]
        
        if len(visuals) >= 3 and len(sections) > 4:
            # Third visual before conclusion
            sections[-2] += '</p>' + visuals[2]
        
        return ''.join(sections)
    
    def _parse_visual_elements(self, visual_html: str) -> List[str]:
        """Parse individual visual elements from AI response"""
        visuals = []
        
        # Try to split by common visual container patterns
        if '<div' in visual_html:
            # Split by top-level divs
            parts = visual_html.split('<div')
            for i, part in enumerate(parts[1:], 1):
                if part.strip():
                    visual = '<div' + part
                    # Find the matching closing div
                    div_count = 1
                    pos = 0
                    while div_count > 0 and pos < len(visual):
                        if visual[pos:pos+5] == '<div':
                            div_count += 1
                            pos += 5
                        elif visual[pos:pos+6] == '</div>':
                            div_count -= 1
                            pos += 6
                            if div_count == 0:
                                visuals.append(visual[:pos])
                                break
                        else:
                            pos += 1
        
        # If no divs found, try tables
        elif '<table' in visual_html:
            tables = visual_html.split('<table')
            for table in tables[1:]:
                if '</table>' in table:
                    end_pos = table.find('</table>') + 8
                    visuals.append('<table' + table[:end_pos])
        
        # If still no visuals, treat entire response as one visual
        if not visuals and visual_html.strip():
            visuals = [visual_html]
        
        return visuals[:3]  # Max 3 visuals
    
    def _get_default_visual_strategy(self, template_data: Dict[str, Any]) -> Dict[str, Any]:
        """Default visual strategy based on template type"""
        pattern = template_data.get('pattern', '').lower()
        
        # Detect content type more accurately
        content_type = self._detect_content_type(pattern, template_data)
        
        # Return content-type-specific visual strategy
        if content_type == 'comparison':
            return {
                'intro_visual': {'type': 'comparison_cards', 'title': 'Quick Comparison', 'focus': 'features'},
                'main_visual': {'type': 'comparison_table', 'title': 'Detailed Comparison', 'columns': ['Feature', 'Option 1', 'Option 2']},
                'support_visual': {'type': 'benefits_grid', 'title': 'Key Differences', 'items': 4}
            }
        elif content_type == 'how_to':
            return {
                'intro_visual': {'type': 'process_steps', 'title': 'Steps Overview', 'focus': 'process'},
                'main_visual': {'type': 'checklist', 'title': 'Requirements Checklist', 'items': 6},
                'support_visual': {'type': 'quick_facts', 'title': 'Tips & Best Practices', 'focus': 'tips'}
            }
        elif content_type == 'investment':
            return {
                'intro_visual': {'type': 'stats_box', 'title': 'Investment Overview', 'focus': 'roi'},
                'main_visual': {'type': 'pricing_tiers', 'title': 'Revenue Breakdown', 'columns': ['Basic', 'Standard', 'Premium']},
                'support_visual': {'type': 'rating_chart', 'title': 'Market Performance', 'focus': 'performance'}
            }
        elif content_type == 'location_service':
            return {
                'intro_visual': {'type': 'stats_box', 'title': 'Quick Stats', 'focus': 'providers'},
                'main_visual': {'type': 'comparison_table', 'title': 'Top Providers', 'columns': ['Provider', 'Rating', 'Price']},
                'support_visual': {'type': 'checklist', 'title': 'What to Expect', 'items': 6}
            }
        elif content_type == 'product':
            return {
                'intro_visual': {'type': 'pricing_tiers', 'title': 'Pricing Options', 'focus': 'pricing'},
                'main_visual': {'type': 'comparison_cards', 'title': 'Product Features', 'columns': []},
                'support_visual': {'type': 'rating_chart', 'title': 'Customer Reviews', 'focus': 'satisfaction'}
            }
        else:
            # Generic fallback
            return {
                'intro_visual': {'type': 'quick_facts', 'title': 'Key Information', 'focus': 'general'},
                'main_visual': {'type': 'comparison_cards', 'title': 'Options Available', 'columns': []},
                'support_visual': {'type': 'benefits_grid', 'title': 'Key Benefits', 'items': 4}
            }
    
    def _detect_content_type(self, pattern: str, template_data: Dict[str, Any]) -> str:
        """Detect the type of content based on pattern and data"""
        pattern_lower = pattern.lower()
        
        # Check for comparison content first (most specific)
        if ' vs ' in pattern_lower or ' versus ' in pattern_lower or 'comparison' in pattern_lower:
            return 'comparison'
        
        # Check for how-to content
        if pattern_lower.startswith('how to') or 'guide' in pattern_lower or 'tutorial' in pattern_lower:
            return 'how_to'
        
        # Check for investment/ROI content
        if any(word in pattern_lower for word in ['investment', 'profitable', 'roi', 'return', 'income', 'revenue']):
            return 'investment'
        
        # Check for product content (with product names or price focus)
        product_indicators = ['iphone', 'samsung', 'laptop', 'camera', 'phone', 'tablet', 'gadget']
        if (any(word in pattern_lower for word in product_indicators) and 
            any(word in pattern_lower for word in ['price', 'cost', 'buy', 'purchase'])):
            return 'product'
        
        # Check for location-based service - look for service words + location indicators
        location_indicators = ['in ', 'near', 'local', ' at ']
        service_words = ['plumber', 'electrician', 'contractor', 'repair', 'service', 'provider', 
                        'lawyer', 'doctor', 'dentist', 'restaurant', 'shop', 'store', 'company', 'companies']
        
        has_location = any(indicator in pattern_lower for indicator in location_indicators)
        has_service = any(word in pattern_lower for word in service_words)
        
        if has_location and (has_service or 'best' in pattern_lower):
            return 'location_service'
        
        # Generic product check (fallback)
        if any(word in pattern_lower for word in ['product', 'buy', 'purchase', 'shop', 'price', 'cost']):
            return 'product'
        
        # Default to generic
        return 'generic'
    
    def _generate_visual_element(self, visual_spec: Dict[str, Any], 
                                template_data: Dict[str, Any], 
                                enriched_data: Dict[str, Any]) -> str:
        """Generate HTML for a specific visual element"""
        
        visual_type = visual_spec.get('type', 'stats_box')
        primary_data = enriched_data.get('primary_data', {})
        
        if visual_type == 'stats_box':
            return self._generate_stats_box(visual_spec, template_data, primary_data)
        elif visual_type == 'comparison_table':
            return self._generate_comparison_table(visual_spec, template_data, primary_data)
        elif visual_type == 'pricing_tiers':
            return self._generate_pricing_tiers(visual_spec, template_data, primary_data)
        elif visual_type == 'checklist':
            return self._generate_checklist(visual_spec, template_data, primary_data)
        elif visual_type == 'rating_chart':
            return self._generate_rating_chart(visual_spec, template_data, primary_data)
        elif visual_type == 'process_steps':
            return self._generate_process_steps(visual_spec, template_data, primary_data)
        else:
            return self._generate_generic_visual(visual_spec, template_data, primary_data)
    
    def _generate_stats_box(self, spec: Dict[str, Any], template_data: Dict[str, Any], 
                           primary_data: Dict[str, Any]) -> str:
        """Generate a statistics info box"""
        title = spec.get('title', 'Quick Stats')
        focus = spec.get('focus', 'general')
        pattern = template_data.get('pattern', '').lower()
        
        # Detect content type for better stat selection
        content_type = self._detect_content_type(pattern, template_data)
        
        # Select stats based on content type and focus
        stats = []
        if content_type == 'comparison':
            # For comparisons, show differentiating stats
            stats = [
                ('Price Difference', f"${abs(primary_data.get('price_diff', 50))}", '#3b82f6'),
                ('Feature Count', f"{primary_data.get('feature_count_1', 12)} vs {primary_data.get('feature_count_2', 10)}", '#10b981'),
                ('User Rating', f"{primary_data.get('rating_1', 4.5)}★ vs {primary_data.get('rating_2', 4.3)}★", '#8b5cf6'),
                ('Market Share', f"{primary_data.get('market_share_1', 35)}% vs {primary_data.get('market_share_2', 28)}%", '#f59e0b')
            ]
        elif content_type == 'how_to':
            # For how-to content, show process stats
            stats = [
                ('Time Required', primary_data.get('time_required', '30 mins'), '#3b82f6'),
                ('Difficulty', primary_data.get('difficulty', 'Beginner'), '#10b981'),
                ('Steps', primary_data.get('step_count', 5), '#8b5cf6'),
                ('Success Rate', f"{primary_data.get('success_rate', 92)}%", '#f59e0b')
            ]
        elif focus == 'providers' or content_type == 'location_service':
            stats = [
                ('Providers', primary_data.get('provider_count', 45), '#3b82f6'),
                ('Avg Rating', f"{primary_data.get('average_rating', 4.5)}★", '#10b981'),
                ('Price Range', f"${primary_data.get('min_price', 95)}-${primary_data.get('max_price', 350)}", '#8b5cf6'),
                ('Response', primary_data.get('average_response_time', '2-4 hrs'), '#f59e0b')
            ]
        elif focus == 'roi' or content_type == 'investment':
            stats = [
                ('ROI', f"{primary_data.get('roi_percentage', 15)}%", '#10b981'),
                ('Occupancy', f"{primary_data.get('occupancy_rate', 68)}%", '#3b82f6'),
                ('Nightly Rate', f"${primary_data.get('average_nightly_rate', 127)}", '#8b5cf6'),
                ('Listings', primary_data.get('total_listings', 342), '#f59e0b')
            ]
        elif content_type == 'product':
            stats = [
                ('Starting Price', f"${primary_data.get('min_price', 29)}", '#3b82f6'),
                ('Avg Rating', f"{primary_data.get('average_rating', 4.4)}★", '#10b981'),
                ('In Stock', f"{primary_data.get('stock_count', 127)} units", '#8b5cf6'),
                ('Ships In', primary_data.get('shipping_time', '2-3 days'), '#f59e0b')
            ]
        else:
            # Generic stats
            stats = [
                ('Options', primary_data.get('count', 50), '#3b82f6'),
                ('Rating', f"{primary_data.get('rating', 4.5)}★", '#10b981'),
                ('Availability', f"{primary_data.get('availability', 85)}%", '#8b5cf6'),
                ('Updated', 'Recently', '#f59e0b')
            ]
        
        html = f'''<div style="background: linear-gradient(135deg, #eff6ff 0%, #f3e8ff 100%); border: 2px solid #c7d2fe; padding: 1.5rem; border-radius: 0.75rem; margin: 2rem 0;">
  <h3 style="margin: 0 0 1rem 0; color: #1e293b; font-size: 1.25rem;">📊 {title}</h3>
  <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 1rem;">'''
        
        for label, value, color in stats:
            html += f'''
    <div style="text-align: center;">
      <div style="font-size: 1.75rem; font-weight: bold; color: {color};">{value}</div>
      <div style="color: #64748b; font-size: 0.875rem;">{label}</div>
    </div>'''
        
        html += '''
  </div>
</div>'''
        return html
    
    def _generate_comparison_table(self, spec: Dict[str, Any], template_data: Dict[str, Any], 
                                  primary_data: Dict[str, Any]) -> str:
        """Generate a comparison table"""
        title = spec.get('title', 'Comparison')
        pattern = template_data.get('pattern', '').lower()
        content_type = self._detect_content_type(pattern, template_data)
        
        # Generate table based on content type
        if content_type == 'comparison':
            # Extract items being compared from pattern or data
            import re
            vs_match = re.search(r'(\w+)\s+vs\s+(\w+)', pattern, re.IGNORECASE)
            if vs_match:
                item1, item2 = vs_match.groups()
            else:
                item1 = template_data.get('item1', 'Option 1')
                item2 = template_data.get('item2', 'Option 2')
            
            html = f'''<div style="margin: 2rem 0;">
  <h3>{title}</h3>
  <div style="overflow-x: auto;">
    <table style="width: 100%; border-collapse: collapse; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
      <thead>
        <tr style="background: #f8fafc;">
          <th style="padding: 0.75rem; text-align: left; border-bottom: 2px solid #e2e8f0;">Feature</th>
          <th style="padding: 0.75rem; text-align: center; border-bottom: 2px solid #e2e8f0;">{item1}</th>
          <th style="padding: 0.75rem; text-align: center; border-bottom: 2px solid #e2e8f0;">{item2}</th>
        </tr>
      </thead>
      <tbody>'''
            
            # Comparison features
            features = [
                ('Price', f"${primary_data.get('price_1', 99)}/mo", f"${primary_data.get('price_2', 149)}/mo"),
                ('Free Trial', '14 days', '30 days'),
                ('User Limit', f"{primary_data.get('users_1', 5)} users", f"{primary_data.get('users_2', 'Unlimited')}"),
                ('Storage', f"{primary_data.get('storage_1', '10GB')}", f"{primary_data.get('storage_2', '100GB')}"),
                ('Support', '24/7 Email', '24/7 Phone & Email'),
                ('Integration', f"{primary_data.get('integrations_1', 50)}+ apps", f"{primary_data.get('integrations_2', 200)}+ apps")
            ]
            
            for i, (feature, val1, val2) in enumerate(features):
                bg = '#ffffff' if i % 2 == 0 else '#f9fafb'
                html += f'''
        <tr style="background: {bg};">
          <td style="padding: 0.75rem; border-bottom: 1px solid #e2e8f0; font-weight: 600;">{feature}</td>
          <td style="padding: 0.75rem; text-align: center; border-bottom: 1px solid #e2e8f0;">{val1}</td>
          <td style="padding: 0.75rem; text-align: center; border-bottom: 1px solid #e2e8f0;">{val2}</td>
        </tr>'''
            
        else:
            # Default provider table for services
            service = template_data.get('Service', 'Service')
            
            # Get or generate provider data
            providers = primary_data.get('top_providers', [])
            if not providers:
                import random
                providers = []
                for i in range(5):
                    providers.append({
                        'name': f'{service} Provider {i+1}',
                        'rating': round(4.0 + random.random(), 1),
                        'reviews': random.randint(50, 500),
                        'price': f'${random.randint(100, 400)}',
                        'response': f'{random.randint(1, 6)}h'
                    })
            
            html = f'''<div style="margin: 2rem 0;">
  <h3>{title}</h3>
  <div style="overflow-x: auto;">
    <table style="width: 100%; border-collapse: collapse; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
      <thead>
        <tr style="background: #f8fafc;">
          <th style="padding: 0.75rem; text-align: left; border-bottom: 2px solid #e2e8f0;">Provider</th>
          <th style="padding: 0.75rem; text-align: center; border-bottom: 2px solid #e2e8f0;">Rating</th>
          <th style="padding: 0.75rem; text-align: center; border-bottom: 2px solid #e2e8f0;">Reviews</th>
          <th style="padding: 0.75rem; text-align: center; border-bottom: 2px solid #e2e8f0;">Est. Price</th>
          <th style="padding: 0.75rem; text-align: center; border-bottom: 2px solid #e2e8f0;">Response</th>
        </tr>
      </thead>
      <tbody>'''
            
            for i, provider in enumerate(providers[:5]):
                bg = '#ffffff' if i % 2 == 0 else '#f9fafb'
                html += f'''
        <tr style="background: {bg};">
          <td style="padding: 0.75rem; border-bottom: 1px solid #e2e8f0; font-weight: 600;">{provider.get('name')}</td>
          <td style="padding: 0.75rem; text-align: center; border-bottom: 1px solid #e2e8f0; color: #10b981; font-weight: bold;">{provider.get('rating')}★</td>
          <td style="padding: 0.75rem; text-align: center; border-bottom: 1px solid #e2e8f0;">{provider.get('reviews')}</td>
          <td style="padding: 0.75rem; text-align: center; border-bottom: 1px solid #e2e8f0; font-weight: 600;">{provider.get('price')}</td>
          <td style="padding: 0.75rem; text-align: center; border-bottom: 1px solid #e2e8f0;">{provider.get('response')}</td>
        </tr>'''
        
        html += '''
      </tbody>
    </table>
  </div>
</div>'''
        return html
    
    def _generate_checklist(self, spec: Dict[str, Any], template_data: Dict[str, Any], 
                           primary_data: Dict[str, Any]) -> str:
        """Generate a checklist visual"""
        title = spec.get('title', 'Key Features')
        num_items = spec.get('items', 6)
        
        # Generate contextual checklist items
        service = template_data.get('Service', 'service')
        items = self._get_contextual_checklist_items(service, num_items)
        
        html = f'''<div style="margin: 2rem 0;">
  <h3>{title}</h3>
  <div style="background: #f9fafb; padding: 1.5rem; border-radius: 0.5rem;">
    <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 0.75rem;">'''
        
        for item, included in items:
            icon = '✅' if included else '❌'
            color = '#10b981' if included else '#94a3b8'
            html += f'''
      <div style="display: flex; align-items: center;">
        <span style="font-size: 1.25rem; margin-right: 0.5rem;">{icon}</span>
        <span style="color: {color};">{item}</span>
      </div>'''
        
        html += '''
    </div>
  </div>
</div>'''
        return html
    
    def _get_contextual_checklist_items(self, service: str, num_items: int) -> List[tuple]:
        """Get context-appropriate checklist items"""
        import random
        
        # Common features for services
        all_features = [
            ('Licensed & Insured', True),
            ('Free Estimates', True),
            ('24/7 Emergency Service', True),
            ('Warranty Included', True),
            ('Online Booking', random.choice([True, False])),
            ('Same-Day Service', random.choice([True, False])),
            ('Senior Discounts', True),
            ('Eco-Friendly Options', random.choice([True, False])),
            ('Payment Plans', random.choice([True, False])),
            ('Mobile Service', random.choice([True, False]))
        ]
        
        # Select requested number of items
        return all_features[:num_items]
    
    def _generate_pricing_tiers(self, spec: Dict[str, Any], template_data: Dict[str, Any], 
                               primary_data: Dict[str, Any]) -> str:
        """Generate pricing tier cards"""
        title = spec.get('title', 'Pricing Options')
        min_price = primary_data.get('min_price', 100)
        max_price = primary_data.get('max_price', 500)
        mid_price = (min_price + max_price) // 2
        
        html = f'''<div style="margin: 2rem 0;">
  <h3>{title}</h3>
  <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem;">
    <div style="background: #f3f4f6; padding: 1.5rem; border-radius: 0.5rem; text-align: center;">
      <h4 style="color: #6b7280; margin: 0 0 0.5rem 0;">Basic</h4>
      <div style="font-size: 2rem; font-weight: bold; color: #1f2937;">${min_price}</div>
      <ul style="list-style: none; padding: 0; margin: 1rem 0 0 0; text-align: left; font-size: 0.875rem; color: #6b7280;">
        <li>• Standard service</li>
        <li>• 30-day warranty</li>
        <li>• Business hours</li>
      </ul>
    </div>
    <div style="background: linear-gradient(135deg, #e0e7ff 0%, #c7d2fe 100%); padding: 1.5rem; border-radius: 0.5rem; text-align: center; border: 2px solid #6366f1;">
      <h4 style="color: #4f46e5; margin: 0 0 0.5rem 0;">Popular</h4>
      <div style="font-size: 2rem; font-weight: bold; color: #4f46e5;">${mid_price}</div>
      <ul style="list-style: none; padding: 0; margin: 1rem 0 0 0; text-align: left; font-size: 0.875rem; color: #4f46e5;">
        <li>• Priority service</li>
        <li>• 90-day warranty</li>
        <li>• Extended hours</li>
      </ul>
    </div>
    <div style="background: #fef3c7; padding: 1.5rem; border-radius: 0.5rem; text-align: center;">
      <h4 style="color: #92400e; margin: 0 0 0.5rem 0;">Premium</h4>
      <div style="font-size: 2rem; font-weight: bold; color: #92400e;">${max_price}+</div>
      <ul style="list-style: none; padding: 0; margin: 1rem 0 0 0; text-align: left; font-size: 0.875rem; color: #92400e;">
        <li>• VIP service</li>
        <li>• 1-year warranty</li>
        <li>• 24/7 availability</li>
      </ul>
    </div>
  </div>
</div>'''
        return html
    
    def _generate_rating_chart(self, spec: Dict[str, Any], template_data: Dict[str, Any], 
                              primary_data: Dict[str, Any]) -> str:
        """Generate a visual rating breakdown"""
        import random
        avg_rating = primary_data.get('average_rating', 4.5)
        
        # Generate rating distribution
        ratings = {
            5: random.randint(60, 75),
            4: random.randint(15, 25),
            3: random.randint(5, 10),
            2: random.randint(1, 3),
            1: random.randint(0, 2)
        }
        
        # Normalize
        total = sum(ratings.values())
        ratings = {k: int(v * 100 / total) for k, v in ratings.items()}
        
        html = f'''<div style="margin: 2rem 0;">
  <h3>Customer Satisfaction</h3>
  <div style="background: #f9fafb; padding: 1.5rem; border-radius: 0.5rem;">
    <div style="text-align: center; margin-bottom: 1.5rem;">
      <div style="font-size: 2.5rem; font-weight: bold; color: #10b981;">{avg_rating}★</div>
      <div style="color: #64748b;">Average Rating</div>
    </div>'''
        
        for stars in range(5, 0, -1):
            pct = ratings[stars]
            color = '#10b981' if stars >= 4 else '#f59e0b' if stars == 3 else '#ef4444'
            html += f'''
    <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
      <span style="width: 3rem; color: #64748b;">{stars}★</span>
      <div style="flex: 1; height: 1.5rem; background: #e5e7eb; border-radius: 0.25rem; margin: 0 0.5rem;">
        <div style="width: {pct}%; height: 100%; background: {color}; border-radius: 0.25rem;"></div>
      </div>
      <span style="width: 3rem; text-align: right; color: #64748b;">{pct}%</span>
    </div>'''
        
        html += '''
  </div>
</div>'''
        return html
    
    def _generate_process_steps(self, spec: Dict[str, Any], template_data: Dict[str, Any], 
                               primary_data: Dict[str, Any]) -> str:
        """Generate process steps visualization"""
        title = spec.get('title', 'How It Works')
        service = template_data.get('Service', 'Service')
        
        steps = [
            ('Contact', f'Reach out for {service.lower()} consultation'),
            ('Quote', 'Receive detailed estimate'),
            ('Schedule', 'Book convenient appointment'),
            ('Service', 'Professional work completed'),
            ('Follow-up', 'Satisfaction guaranteed')
        ]
        
        html = f'''<div style="margin: 2rem 0;">
  <h3>{title}</h3>
  <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">'''
        
        for i, (step, desc) in enumerate(steps):
            html += f'''
    <div style="text-align: center; flex: 1; min-width: 120px; margin: 0.5rem;">
      <div style="width: 3rem; height: 3rem; background: #6366f1; color: white; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 0.5rem; font-weight: bold;">
        {i + 1}
      </div>
      <div style="font-weight: 600; color: #1e293b;">{step}</div>
      <div style="font-size: 0.75rem; color: #64748b; margin-top: 0.25rem;">{desc}</div>
    </div>'''
            
            if i < len(steps) - 1:
                html += '''
    <div style="color: #cbd5e1; font-size: 1.5rem;">→</div>'''
        
        html += '''
  </div>
</div>'''
        return html
    
    def _generate_generic_visual(self, spec: Dict[str, Any], template_data: Dict[str, Any], 
                                primary_data: Dict[str, Any]) -> str:
        """Fallback generic visual element"""
        return self._generate_stats_box(spec, template_data, primary_data)
    
    def _add_basic_visuals(self, content_html: str, template_data: Dict[str, Any], 
                          enriched_data: Dict[str, Any]) -> str:
        """Add basic visuals without AI"""
        # Get default visual strategy based on template
        visual_strategy = self._get_default_visual_strategy(template_data)
        
        # Split content by paragraphs
        sections = content_html.split('</p>')
        
        # Add intro visual after first paragraph
        if len(sections) > 1 and visual_strategy.get('intro_visual'):
            intro_visual = self._generate_visual_element(
                visual_strategy['intro_visual'], template_data, enriched_data
            )
            sections[0] += '</p>' + intro_visual
        
        # Add main visual after second paragraph
        if len(sections) > 2 and visual_strategy.get('main_visual'):
            main_visual = self._generate_visual_element(
                visual_strategy['main_visual'], template_data, enriched_data
            )
            sections[1] += '</p>' + main_visual
        
        # Add support visual before last paragraph
        if len(sections) > 3 and visual_strategy.get('support_visual'):
            support_visual = self._generate_visual_element(
                visual_strategy['support_visual'], template_data, enriched_data
            )
            # Insert before the last paragraph (before CTA)
            sections[-2] += '</p>' + support_visual
        
        return ''.join(sections)