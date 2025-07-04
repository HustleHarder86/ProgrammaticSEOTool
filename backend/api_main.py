"""Lightweight API for Vercel with Firebase integration"""
from http.server import BaseHTTPRequestHandler
import json
import os
import sys
from urllib.parse import urlparse, parse_qs
from urllib.request import urlopen, Request
from urllib.error import URLError
from datetime import datetime
import base64

# Import AI handler if available
try:
    from .ai_handler import AIHandler
    ai_handler = AIHandler()
except:
    ai_handler = None

# Import usage tracker
try:
    from .usage_tracker import usage_tracker
except:
    usage_tracker = None

class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_GET(self):
        """Handle GET requests"""
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        # Serve HTML interface at /app or /pro
        if path == '/app':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            # Read and serve the HTML file
            html_path = os.path.join(os.path.dirname(__file__), 'interface.html')
            try:
                with open(html_path, 'r') as f:
                    self.wfile.write(f.read().encode())
            except:
                # Fallback if file not found
                self.wfile.write(b'<h1>Programmatic SEO Tool</h1><p>API is running. Use POST requests to interact.</p>')
            return
        
        # Serve enhanced interface at /pro
        if path == '/pro':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            # Read and serve the enhanced HTML file
            html_path = os.path.join(os.path.dirname(__file__), 'enhanced-interface.html')
            try:
                with open(html_path, 'r') as f:
                    self.wfile.write(f.read().encode())
            except:
                # Fallback to basic interface
                html_path = os.path.join(os.path.dirname(__file__), 'interface.html')
                try:
                    with open(html_path, 'r') as f:
                        self.wfile.write(f.read().encode())
                except:
                    self.wfile.write(b'<h1>Programmatic SEO Tool</h1><p>API is running.</p>')
            return
        
        # Serve wizard interface at /wizard
        if path == '/wizard':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            # Read and serve the wizard HTML file
            html_path = os.path.join(os.path.dirname(__file__), 'enhanced-interface-wizard.html')
            try:
                with open(html_path, 'r') as f:
                    self.wfile.write(f.read().encode())
            except:
                self.wfile.write(b'<h1>Wizard interface not found</h1>')
            return
        
        # Serve template UI at root
        if path == '/' or path == '':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            # Read and serve the template UI file
            html_path = os.path.join(os.path.dirname(__file__), 'template_ui.html')
            try:
                with open(html_path, 'r') as f:
                    self.wfile.write(f.read().encode())
            except:
                self.wfile.write(b'<h1>Programmatic SEO Tool</h1><p>Template UI not found.</p>')
            return
        
        # Serve dashboard at /dashboard
        if path == '/dashboard':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            # Read and serve the dashboard HTML file
            html_path = os.path.join(os.path.dirname(__file__), 'dashboard.html')
            try:
                with open(html_path, 'r') as f:
                    self.wfile.write(f.read().encode())
            except:
                self.wfile.write(b'<h1>Dashboard</h1><p>Error loading dashboard.</p>')
            return
        
        # JSON responses for API endpoints
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        if path == '/api':
            response = {
                'message': 'Programmatic SEO Tool API',
                'version': '1.0.0',
                'status': 'healthy',
                'endpoints': [
                    'GET /api',
                    'GET /health',
                    'POST /api/analyze-business',
                    'POST /api/generate-keywords',
                    'POST /api/generate-content',
                    'POST /api/projects',
                    'GET /api/projects'
                ]
            }
        elif path == '/health':
            response = {'status': 'healthy', 'timestamp': datetime.now().isoformat()}
        elif path == '/api/usage-dashboard':
            # Get dashboard data
            if usage_tracker:
                response = usage_tracker.get_dashboard_data()
            else:
                response = {'error': 'Usage tracking not available'}
        elif path == '/api/projects':
            # In production, this would fetch from Firebase
            response = {
                'projects': [],
                'total': 0
            }
        elif path == '/debug':
            # Debug endpoint to check environment
            response = {
                'status': 'debug mode',
                'env_vars': {
                    'has_firebase_config': bool(os.environ.get('FIREBASE_PROJECT_ID')),
                    'has_openai': bool(os.environ.get('OPENAI_API_KEY')),
                    'has_anthropic': bool(os.environ.get('ANTHROPIC_API_KEY')),
                    'has_perplexity': bool(os.environ.get('PerplexityAPI')),
                },
                'python_version': sys.version,
                'current_time': datetime.now().isoformat()
            }
        else:
            response = {'error': 'Not found', 'path': path}
            
        self.wfile.write(json.dumps(response).encode())

    def do_POST(self):
        """Handle POST requests"""
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data.decode('utf-8')) if post_data else {}
        except:
            data = {}
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        if path == '/api/analyze-business':
            response = self._analyze_business(data)
        elif path == '/api/create-template':
            response = self._create_template(data)
        elif path == '/api/import-data':
            response = self._import_data(data)
        elif path == '/api/generate-pages':
            response = self._generate_pages(data)
        elif path == '/api/export-pages':
            response = self._export_pages(data)
        elif path == '/api/get-templates':
            response = self._get_templates(data)
        elif path == '/api/preview-pages':
            response = self._preview_pages(data)
        elif path == '/api/set-model':
            # Change the model being used
            if usage_tracker:
                model = data.get('model', 'sonar')
                success = usage_tracker.set_model(model)
                response = {
                    'success': success,
                    'model': model if success else usage_tracker.current_model
                }
            else:
                response = {'error': 'Usage tracker not available'}
        else:
            response = {'error': 'Endpoint not found', 'path': path}
            
        self.wfile.write(json.dumps(response).encode())

    def _analyze_business(self, data):
        """Analyze business from URL or description"""
        business_url = data.get('business_url', '')
        business_description = data.get('business_description', '')
        target_audience = data.get('target_audience', 'auto')
        
        # Get basic info first
        business_info = {
            'name': 'Your Business',
            'url': business_url,
            'description': business_description or 'No description provided',
            'target_audience_type': target_audience if target_audience != 'auto' else None
        }
        
        # Try to fetch title from URL
        if business_url:
            try:
                # Add headers to avoid being blocked
                req = Request(business_url, headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                })
                with urlopen(req, timeout=5) as response:
                    html = response.read().decode('utf-8')
                    
                    # Extract title
                    if '<title>' in html:
                        start = html.find('<title>') + 7
                        end = html.find('</title>')
                        title = html[start:end] if end > start else "Business Website"
                        business_info['name'] = title
                    
                    # Extract meta description
                    if 'name="description"' in html:
                        desc_start = html.find('name="description"')
                        if desc_start > 0:
                            content_start = html.find('content="', desc_start) + 9
                            content_end = html.find('"', content_start)
                            if content_end > content_start:
                                meta_desc = html[content_start:content_end]
                                business_info['description'] = business_info.get('description', '') + ' ' + meta_desc
                    
                    # Extract key text from body (first 500 chars of visible text)
                    import re
                    # Remove script and style elements
                    clean_html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
                    clean_html = re.sub(r'<style[^>]*>.*?</style>', '', clean_html, flags=re.DOTALL)
                    # Extract text
                    text = re.sub(r'<[^>]+>', ' ', clean_html)
                    text = ' '.join(text.split())[:500]
                    business_info['page_content'] = text
            except Exception as e:
                # If URL fetch fails, extract domain as name
                from urllib.parse import urlparse
                parsed = urlparse(business_url)
                domain = parsed.netloc.replace('www.', '').split('.')[0]
                business_info['name'] = domain.title() + " Business"
                print(f"URL fetch error: {e}")
        
        # Use AI for deeper analysis if available
        if ai_handler and ai_handler.has_ai_provider():
            ai_analysis = ai_handler.analyze_business_with_ai(business_info)
            # Track API usage
            if usage_tracker:
                usage_tracker.track_usage('analyze_business')
            if ai_analysis:
                business_info.update({
                    'industry': ai_analysis.get('industry', 'General'),
                    'target_audience': ai_analysis.get('target_audience', 'General audience'),
                    'content_types': ai_analysis.get('content_types', ['blog posts', 'tutorials']),
                    'main_keywords': ai_analysis.get('main_keywords', [])
                })
            else:
                # AI failed, check if real estate based on URL/description
                is_real_estate = any(term in (business_url + business_description).lower() 
                                   for term in ['real estate', 'property', 'investment', 'rental', 'realty'])
                business_info.update({
                    'industry': 'Real Estate' if is_real_estate else 'General',
                    'target_audience': 'Real estate investors and agents' if is_real_estate else 'General audience',
                    'content_types': ['analysis tools', 'calculators', 'guides'] if is_real_estate else ['blog posts', 'tutorials', 'guides']
                })
        else:
            # No AI, check if real estate
            is_real_estate = any(term in (business_url + business_description).lower() 
                               for term in ['real estate', 'property', 'investment', 'rental', 'realty'])
            business_info.update({
                'industry': 'Real Estate' if is_real_estate else 'General',
                'target_audience': 'Real estate investors and agents' if is_real_estate else 'General audience',
                'content_types': ['analysis tools', 'calculators', 'guides'] if is_real_estate else ['blog posts', 'tutorials', 'guides']
            })
        
        # Get template suggestions based on business analysis
        template_suggestions = []
        if ai_handler and ai_handler.has_ai_provider():
            # Analyze for template opportunities
            if 'real estate' in business_info.get('industry', '').lower():
                template_suggestions = [
                    {
                        'name': 'Location Property Analysis',
                        'pattern': '{city} {property_type} Investment Analysis',
                        'variables': ['city', 'property_type'],
                        'estimated_pages': 250,
                        'example': 'Toronto Condo Investment Analysis'
                    },
                    {
                        'name': 'ROI Calculator Pages',
                        'pattern': '{city} Real Estate ROI Calculator',
                        'variables': ['city'],
                        'estimated_pages': 50,
                        'example': 'Vancouver Real Estate ROI Calculator'
                    }
                ]
            else:
                # Generic templates for any business
                template_suggestions = [
                    {
                        'name': 'Location Based Service',
                        'pattern': '{service} in {location}',
                        'variables': ['service', 'location'],
                        'estimated_pages': 100,
                        'example': f"{business_info.get('name', 'Service')} in Toronto"
                    },
                    {
                        'name': 'Comparison Pages',
                        'pattern': '{option1} vs {option2} Comparison',
                        'variables': ['option1', 'option2'],
                        'estimated_pages': 50,
                        'example': 'Product A vs Product B Comparison'
                    }
                ]
        
        return {
            'success': True,
            'business_info': business_info,
            'template_suggestions': template_suggestions,
            'ai_enabled': bool(ai_handler and ai_handler.has_ai_provider())
        }

    def _create_template(self, data):
        """Create a new page template"""
        name = data.get('name', '')
        pattern = data.get('pattern', '')
        page_structure = data.get('page_structure', {})
        
        if not name or not pattern:
            return {
                'success': False,
                'error': 'Template name and pattern are required'
            }
        
        try:
            from .template_generator import TemplateGenerator
            tg = TemplateGenerator()
            
            template = tg.create_template(name, pattern, page_structure)
            
            return {
                'success': True,
                'template': template,
                'message': f'Template "{name}" created successfully'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def _import_data(self, data):
        """Import data from CSV for template variables"""
        csv_content = data.get('csv_content', '')
        data_name = data.get('data_name', 'imported_data')
        
        if not csv_content:
            return {
                'success': False,
                'error': 'CSV content is required'
            }
        
        try:
            from .template_generator import TemplateGenerator
            tg = TemplateGenerator()
            
            imported_data = tg.import_data_from_csv(csv_content, data_name)
            
            return {
                'success': True,
                'data': imported_data,
                'columns': list(imported_data.keys()),
                'total_values': {k: len(v) for k, v in imported_data.items()}
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def _generate_pages(self, data):
        """Generate pages from template + data"""
        template_name = data.get('template_name', '')
        data_mapping = data.get('data', {})
        limit = data.get('limit', None)
        
        if not template_name:
            return {
                'success': False,
                'error': 'Template name is required'
            }
        
        try:
            from .template_generator import TemplateGenerator
            tg = TemplateGenerator()
            
            pages = tg.generate_pages_from_template(template_name, data_mapping, limit)
            
            return {
                'success': True,
                'pages': pages,
                'total': len(pages),
                'message': f'Generated {len(pages)} pages successfully'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def _export_pages(self, data):
        """Export generated pages in various formats"""
        export_format = data.get('format', 'csv')
        pages = data.get('pages', [])
        
        if not pages:
            return {
                'success': False,
                'error': 'No pages to export'
            }
        
        try:
            if export_format == 'csv':
                # Create CSV content
                import csv
                from io import StringIO
                
                output = StringIO()
                if pages:
                    writer = csv.DictWriter(output, fieldnames=pages[0].keys())
                    writer.writeheader()
                    writer.writerows(pages)
                
                return {
                    'success': True,
                    'content': output.getvalue(),
                    'format': 'csv',
                    'filename': 'programmatic_seo_pages.csv'
                }
            else:
                return {
                    'success': False,
                    'error': f'Export format "{export_format}" not supported yet'
                }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def _get_templates(self, data):
        """Get available templates"""
        try:
            from .template_generator import TemplateGenerator
            tg = TemplateGenerator()
            
            # Get all templates from library
            templates = []
            for name, template in tg.template_library.items():
                templates.append({
                    'name': name,
                    'pattern': template.get('pattern', template.get('templates', [''])[0]),
                    'variables': template.get('variables', []),
                    'description': template.get('description', '')
                })
            
            return {
                'success': True,
                'templates': templates,
                'total': len(templates)
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def _preview_pages(self, data):
        """Preview a few pages before full generation"""
        template_name = data.get('template_name', '')
        data_mapping = data.get('data', {})
        preview_count = min(data.get('preview_count', 5), 10)
        
        try:
            from .template_generator import TemplateGenerator
            tg = TemplateGenerator()
            
            pages = tg.generate_pages_from_template(template_name, data_mapping, limit=preview_count)
            
            return {
                'success': True,
                'preview': pages,
                'total_preview': len(pages),
                'estimated_total': self._calculate_total_pages(data_mapping)
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def _calculate_total_pages(self, data_mapping):
        """Calculate total number of pages that would be generated"""
        total = 1
        for key, values in data_mapping.items():
            if isinstance(values, list) and len(values) > 0:
                total *= len(values)
        return total
    
    def _generate_keywords(self, data):
        """Generate keyword suggestions"""
        business_info = data.get('business_info', {})
        num_keywords = data.get('num_keywords', 10)
        
        keywords = []
        
        # Import keyword optimizer to check for enhanced keywords
        try:
            from .keyword_optimizer import KeywordOptimizer
            ko = KeywordOptimizer()
        except:
            ko = None
            
        # Check if seed mode
        if data.get('seed_mode', False):
            try:
                from .seed_generator import SeedKeywordGenerator
                sg = SeedKeywordGenerator()
                
                selected_seeds = data.get('selected_seeds', [])
                location = data.get('location', 'Austin')
                
                print(f"Seed mode request - Selected seeds: {selected_seeds}")
                print(f"Business info: {business_info}")
                
                # Map selected seeds to seed configurations
                seed_configs = []
                for seed_id in selected_seeds:
                    # For AI-generated seeds, preserve the original structure
                    seed_configs.append({
                        "category": seed_id,
                        "template_group": seed_id,
                        "id": seed_id
                    })
                
                print(f"Seed configs: {seed_configs}")
                
                # Get market context from request - check both direct fields and nested market_context
                market_ctx = data.get('market_context', {})
                market_context = {
                    'location': data.get('location', 'online'),
                    'location_list': data.get('location_list', '') or market_ctx.get('location_list', ''),
                    'market_region': data.get('market_region', '') or market_ctx.get('market_region', ''),
                    'additional_context': data.get('additional_context', '') or market_ctx.get('additional_context', '')
                }
                
                print(f"Market context: {market_context}")
                
                # Generate from seeds with business info and market context
                seed_results = sg.generate_from_seeds(seed_configs, business_info, market_context)
                
                print(f"Seed results summary: {seed_results.get('summary', {})}")
                
                return {
                    'success': True,
                    'seed_mode': True,
                    'seed_results': seed_results,
                    'ai_generated': True
                }
            except Exception as e:
                print(f"Seed generation error: {e}")
                import traceback
                traceback.print_exc()
                # Fall back to regular generation
        
        # Try AI generation first
        if ai_handler and ai_handler.has_ai_provider():
            # Get intelligent seed suggestions
            if ko:
                from .seed_generator import SeedKeywordGenerator
                sg = SeedKeywordGenerator()
                seed_suggestions = sg.get_seed_suggestions(business_info)
                
                # If seed suggestions requested, return them
                if data.get('get_suggestions', False):
                    # Track minimal usage for suggestions
                    if usage_tracker:
                        usage_tracker.track_usage('generate_keywords_seed')
                    
                    print(f"Returning {len(seed_suggestions)} seed suggestions")
                    return {
                        'success': True,
                        'seed_suggestions': seed_suggestions,
                        'business_info': business_info,
                        'ai_generated': True
                    }
            
            # Check if we should use enhanced real estate generation
            industry = business_info.get('industry', '').lower()
            if ko and 'real estate' in industry:
                # Check if multi-project mode is requested
                if data.get('multi_project_mode', False):
                    # Generate separate B2B and B2C projects
                    multi_projects = ko.generate_multi_audience_projects(business_info, num_keywords // 2)
                    return {
                        'success': True,
                        'multi_project': True,
                        'projects': multi_projects,
                        'ai_generated': True
                    }
                else:
                    # Get full keyword objects from optimizer
                    keywords = ko.generate_real_estate_keywords(business_info, num_keywords)
            else:
                # Standard AI generation
                ai_keywords = ai_handler.generate_keywords_with_ai(business_info, num_keywords)
                # Track usage
                if usage_tracker:
                    usage_tracker.track_usage('generate_keywords')
                if ai_keywords:
                    # Convert AI keywords to structured format
                    for i, kw in enumerate(ai_keywords):
                        keywords.append({
                            'keyword': kw,
                            'search_volume': 1000 - (i * 50),  # Mock volumes for now
                            'difficulty': 30 + (i * 3),
                            'intent': 'informational' if 'how' in kw.lower() else 'commercial',
                            'cpc': 0.5 + (i * 0.1)
                        })
        
        # Fallback to mock keywords if AI fails or not available
        if not keywords:
            base_terms = ['how to', 'best', 'guide', 'tutorial', 'tips', 'vs', 'review', 'alternatives']
            business_name = business_info.get('name', 'business').lower()
            
            for i, term in enumerate(base_terms[:num_keywords]):
                keywords.append({
                    'keyword': f"{term} {business_name}",
                    'search_volume': 1000 - (i * 100),
                    'difficulty': 30 + (i * 5),
                    'intent': 'informational',
                    'cpc': 0.5 + (i * 0.1)
                })
        
        return {
            'success': True,
            'keywords': keywords,
            'total': len(keywords),
            'ai_generated': bool(ai_handler and ai_handler.has_ai_provider() and len(keywords) > 0)
        }

    def _generate_content(self, data):
        """Generate content for keywords"""
        keywords = data.get('keywords', [])
        business_info = data.get('business_info', {})
        all_keywords = data.get('all_keywords', keywords)  # For internal linking
        cluster_keywords = data.get('cluster_keywords', [])  # Keywords in same cluster
        
        contents = []
        
        # Limit to 5 keywords to avoid timeout
        for keyword in keywords[:5]:
            content_data = {
                'keyword': keyword,
                'status': 'generated'
            }
            
            # Try AI generation
            if ai_handler and ai_handler.has_ai_provider():
                # Pass all keywords for internal linking
                ai_content = ai_handler.generate_content_with_ai(keyword, business_info)
                # Track usage - one API call per content piece
                if usage_tracker:
                    usage_tracker.track_usage('generate_content')
                if ai_content:
                    # Enhance with internal links
                    enhanced_content = ai_content.get('content', ai_content.get('intro', ''))
                    
                    # Import enhancement function if available
                    try:
                        from .content_variation import enhance_content_quality
                        enhanced_content = enhance_content_quality(
                            enhanced_content,
                            keyword,
                            business_info,
                            all_keywords,
                            cluster_keywords
                        )
                    except:
                        pass
                    
                    content_data.update({
                        'title': ai_content.get('title', f"{keyword.title()} - Guide"),
                        'meta_description': ai_content.get('meta_description', f"Learn about {keyword}"),
                        'content': enhanced_content,
                        'outline': ai_content.get('outline', []),
                        'unique_elements': ai_content.get('unique_elements', []),
                        'internal_links_count': enhanced_content.count('<a href='),
                        'ai_generated': True
                    })
                else:
                    # AI failed, use fallback
                    content_data.update({
                        'title': f"{keyword.title()} - Complete Guide",
                        'meta_description': f"Learn everything about {keyword} in this guide.",
                        'content': f"This is a guide about {keyword}. AI generation failed.",
                        'ai_generated': False
                    })
            else:
                # No AI available
                content_data.update({
                    'title': f"{keyword.title()} - Complete Guide",
                    'meta_description': f"Learn everything about {keyword} in this comprehensive guide.",
                    'content': f"# {keyword.title()}\n\nThis is a comprehensive guide about {keyword}...",
                    'ai_generated': False
                })
            
            contents.append(content_data)
        
        return {
            'success': True,
            'contents': contents,
            'total': len(contents),
            'ai_enabled': bool(ai_handler and ai_handler.has_ai_provider()),
            'interlinking_enabled': True
        }

    def _create_project(self, data):
        """Create a new project (would save to Firebase)"""
        project = {
            'id': f"proj_{int(datetime.now().timestamp())}",
            'name': data.get('name', 'Untitled Project'),
            'business_info': data.get('business_info', {}),
            'created_at': datetime.now().isoformat(),
            'status': 'active'
        }
        
        # In production, save to Firebase here
        
        return {
            'success': True,
            'project': project
        }
    
    def _generate_seed_suggestions(self, data):
        """Generate AI-powered seed suggestions for a business"""
        business_info = data.get('business_info', {})
        use_ai = data.get('use_ai', True)
        
        print(f"DEBUG: _generate_seed_suggestions called with business_info: {business_info}")
        print(f"DEBUG: use_ai = {use_ai}")
        
        try:
            from .seed_generator import SeedKeywordGenerator
            seed_gen = SeedKeywordGenerator()
            
            suggestions = seed_gen.get_seed_suggestions(business_info, use_ai=use_ai)
            print(f"DEBUG: seed_gen.get_seed_suggestions returned {len(suggestions)} suggestions")
            
            # Track API usage if AI was used
            if use_ai and ai_handler and ai_handler.has_ai_provider() and usage_tracker:
                usage_tracker.track_usage('generate_seed_suggestions')
            
            return {
                'success': True,
                'suggestions': suggestions,
                'ai_generated': use_ai and bool(suggestions)
            }
        except Exception as e:
            print(f"Error generating seed suggestions: {e}")
            return {
                'success': False,
                'error': str(e),
                'suggestions': []
            }
    
    def _generate_from_seeds(self, data):
        """Generate keywords from selected seed templates"""
        business_info = data.get('business_info', {})
        seeds = data.get('seeds', [])
        market_context = data.get('market_context', {})
        
        try:
            from .seed_generator import SeedKeywordGenerator
            seed_gen = SeedKeywordGenerator()
            
            results = seed_gen.generate_from_seeds(seeds, business_info, market_context)
            
            return {
                'success': True,
                'keywords': results.get('keywords', []),
                'summary': results.get('summary', {}),
                'seed_details': results.get('seed_details', [])
            }
        except Exception as e:
            print(f"Error generating from seeds: {e}")
            return {
                'success': False,
                'error': str(e),
                'keywords': []
            }