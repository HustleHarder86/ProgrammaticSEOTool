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
        
        # Analyze content and determine appropriate visuals
        visual_strategy = self._analyze_content_for_visuals(content_html, template_data)
        
        # Generate visuals based on strategy
        enhanced_content = content_html
        
        # Insert visuals at appropriate points
        sections = enhanced_content.split('</p>')
        
        # Add intro visual after first paragraph
        if len(sections) > 1 and visual_strategy.get('intro_visual'):
            sections[0] += '</p>' + self._generate_visual_element(
                visual_strategy['intro_visual'], template_data, enriched_data
            )
        
        # Add main visual after second paragraph
        if len(sections) > 2 and visual_strategy.get('main_visual'):
            sections[1] += '</p>' + self._generate_visual_element(
                visual_strategy['main_visual'], template_data, enriched_data
            )
        
        # Add supporting visual before conclusion
        if len(sections) > 3 and visual_strategy.get('support_visual'):
            sections[-2] += '</p>' + self._generate_visual_element(
                visual_strategy['support_visual'], template_data, enriched_data
            )
        
        enhanced_content = ''.join(sections)
        return enhanced_content
    
    def _analyze_content_for_visuals(self, content: str, template_data: Dict[str, Any]) -> Dict[str, Any]:
        """Use AI to analyze content and determine best visual elements"""
        
        prompt = f"""Analyze this content and suggest appropriate visual elements to enhance it.
        
Content: {content[:500]}...

Template pattern: {template_data.get('pattern', '')}
Service/Topic: {template_data.get('Service', template_data.get('service', ''))}
Location: {template_data.get('City', template_data.get('city', ''))}

Based on the content, suggest 3 visual elements that would enhance user engagement:
1. An intro visual (stats box, quick facts, or comparison)
2. A main visual (table, chart, or infographic)  
3. A supporting visual (checklist, timeline, or process diagram)

Return as JSON with this structure:
{{
    "intro_visual": {{
        "type": "stats_box|comparison_cards|quick_facts",
        "title": "Title for the visual",
        "focus": "what data to highlight"
    }},
    "main_visual": {{
        "type": "comparison_table|pricing_tiers|provider_list|rating_chart",
        "title": "Title for the visual",
        "columns": ["col1", "col2"] // for tables
    }},
    "support_visual": {{
        "type": "checklist|process_steps|benefits_grid",
        "title": "Title for the visual",
        "items": 4 // number of items
    }}
}}"""

        try:
            response = self.ai_handler.generate_content(prompt, max_tokens=300)
            # Extract JSON from response
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start >= 0 and json_end > json_start:
                return json.loads(response[json_start:json_end])
        except:
            pass
        
        # Fallback strategy
        return self._get_default_visual_strategy(template_data)
    
    def _get_default_visual_strategy(self, template_data: Dict[str, Any]) -> Dict[str, Any]:
        """Default visual strategy based on template type"""
        pattern = template_data.get('pattern', '').lower()
        
        if 'service' in pattern and ('city' in pattern or 'location' in pattern):
            return {
                'intro_visual': {'type': 'stats_box', 'title': 'Quick Stats', 'focus': 'providers'},
                'main_visual': {'type': 'comparison_table', 'title': 'Top Providers', 'columns': ['Provider', 'Rating', 'Price']},
                'support_visual': {'type': 'checklist', 'title': 'What to Expect', 'items': 6}
            }
        elif 'investment' in pattern or 'profitable' in pattern or 'roi' in pattern:
            return {
                'intro_visual': {'type': 'stats_box', 'title': 'Investment Overview', 'focus': 'roi'},
                'main_visual': {'type': 'pricing_tiers', 'title': 'Revenue Breakdown', 'columns': ['Basic', 'Standard', 'Premium']},
                'support_visual': {'type': 'checklist', 'title': 'Investment Checklist', 'items': 5}
            }
        else:
            return {
                'intro_visual': {'type': 'quick_facts', 'title': 'Key Information', 'focus': 'general'},
                'main_visual': {'type': 'comparison_cards', 'title': 'Options Available', 'columns': []},
                'support_visual': {'type': 'benefits_grid', 'title': 'Key Benefits', 'items': 4}
            }
    
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
        
        # Select stats based on focus
        stats = []
        if focus == 'providers' or 'service' in template_data.get('pattern', '').lower():
            stats = [
                ('Providers', primary_data.get('provider_count', 45), '#3b82f6'),
                ('Avg Rating', f"{primary_data.get('average_rating', 4.5)}★", '#10b981'),
                ('Price Range', f"${primary_data.get('min_price', 95)}-${primary_data.get('max_price', 350)}", '#8b5cf6'),
                ('Response', primary_data.get('average_response_time', '2-4 hrs'), '#f59e0b')
            ]
        elif focus == 'roi' or 'investment' in template_data.get('pattern', '').lower():
            stats = [
                ('ROI', f"{primary_data.get('roi_percentage', 15)}%", '#10b981'),
                ('Occupancy', f"{primary_data.get('occupancy_rate', 68)}%", '#3b82f6'),
                ('Nightly Rate', f"${primary_data.get('average_nightly_rate', 127)}", '#8b5cf6'),
                ('Listings', primary_data.get('total_listings', 342), '#f59e0b')
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
        # Add a simple stats box after first paragraph
        sections = content_html.split('</p>')
        if len(sections) > 1:
            stats_box = self._generate_stats_box(
                {'title': 'Quick Overview', 'focus': 'general'}, 
                template_data, 
                enriched_data.get('primary_data', {})
            )
            sections[0] += '</p>' + stats_box
        
        return ''.join(sections)