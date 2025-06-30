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
        
        # Redirect root to pro version
        if path == '/' or path == '':
            self.send_response(302)
            self.send_header('Location', '/pro')
            self.send_header('Cache-Control', 'no-cache')
            self.end_headers()
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
        elif path == '/api/generate-keywords':
            response = self._generate_keywords(data)
        elif path == '/api/generate-content':
            response = self._generate_content(data)
        elif path == '/api/projects':
            response = self._create_project(data)
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
                    if '<title>' in html:
                        start = html.find('<title>') + 7
                        end = html.find('</title>')
                        title = html[start:end] if end > start else "Business Website"
                        business_info['name'] = title
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
        
        return {
            'success': True,
            'business_info': business_info,
            'ai_enabled': bool(ai_handler and ai_handler.has_ai_provider())
        }

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
        
        # Try AI generation first
        if ai_handler and ai_handler.has_ai_provider():
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