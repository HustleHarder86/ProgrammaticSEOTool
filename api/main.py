"""Lightweight API for Vercel with Firebase integration"""
from http.server import BaseHTTPRequestHandler
import json
import os
from urllib.parse import urlparse, parse_qs
from urllib.request import urlopen
from urllib.error import URLError
from datetime import datetime

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
        
        # Serve HTML interface at /app
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
        
        # JSON responses for API endpoints
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        if path == '/' or path == '':
            response = {
                'message': 'Programmatic SEO Tool API',
                'version': '1.0.0',
                'status': 'healthy',
                'endpoints': [
                    'GET /',
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
        
        # Simple analysis without heavy dependencies
        if business_url:
            try:
                # Basic URL fetch using urllib
                with urlopen(business_url, timeout=5) as response:
                    html = response.read().decode('utf-8')
                    title = "Business Website"
                    if '<title>' in html:
                        start = html.find('<title>') + 7
                        end = html.find('</title>')
                        title = html[start:end] if end > start else title
                
                return {
                    'success': True,
                    'business_info': {
                        'name': title,
                        'url': business_url,
                        'description': business_description or f"Analysis of {title}",
                        'industry': 'Technology',  # Would use AI in production
                        'target_audience': 'General audience',
                        'content_types': ['blog posts', 'tutorials', 'guides']
                    }
                }
            except:
                pass
        
        return {
            'success': True,
            'business_info': {
                'name': 'Your Business',
                'description': business_description or 'No description provided',
                'industry': 'General',
                'target_audience': 'General audience',
                'content_types': ['blog posts', 'tutorials', 'guides']
            }
        }

    def _generate_keywords(self, data):
        """Generate keyword suggestions"""
        business_info = data.get('business_info', {})
        num_keywords = data.get('num_keywords', 10)
        
        # Mock keywords - in production would use AI
        base_terms = ['how to', 'best', 'guide', 'tutorial', 'tips', 'vs', 'review', 'alternatives']
        business_name = business_info.get('name', 'business').lower()
        
        keywords = []
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
            'total': len(keywords)
        }

    def _generate_content(self, data):
        """Generate content for keywords"""
        keywords = data.get('keywords', [])
        business_info = data.get('business_info', {})
        
        contents = []
        for keyword in keywords[:5]:  # Limit to 5 for demo
            contents.append({
                'keyword': keyword,
                'title': f"{keyword.title()} - Complete Guide",
                'meta_description': f"Learn everything about {keyword} in this comprehensive guide.",
                'content': f"# {keyword.title()}\n\nThis is a comprehensive guide about {keyword}...",
                'word_count': 500,
                'status': 'generated'
            })
        
        return {
            'success': True,
            'contents': contents,
            'total': len(contents)
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