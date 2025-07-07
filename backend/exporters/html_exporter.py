"""HTML export functionality with ZIP packaging for static sites."""
import os
import zipfile
from typing import List, Dict, Any, Optional
from datetime import datetime
from pathlib import Path
import shutil
from collections import defaultdict

from config import settings
import logging

logger = logging.getLogger(__name__)


class HTMLExporter:
    """Export content to HTML files with ZIP packaging for static site deployment."""
    
    def __init__(self):
        """Initialize the HTML exporter."""
        self.exports_dir = Path(settings.EXPORTS_DIR)
        self.exports_dir.mkdir(parents=True, exist_ok=True)
    
    def export_content(
        self,
        content_list: List[Dict[str, Any]],
        project_name: str,
        export_options: Dict[str, Any] = None
    ) -> str:
        """Export content to HTML files and package as ZIP."""
        if export_options is None:
            export_options = {}
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Create temporary directory for HTML files
        temp_dir = self.exports_dir / f"temp_{project_name}_{timestamp}"
        temp_dir.mkdir(parents=True, exist_ok=True)
        
        try:
            # Generate HTML files
            self._generate_html_files(content_list, temp_dir, project_name, export_options)
            
            # Create ZIP file
            zip_filename = f"{project_name}_html_{timestamp}.zip"
            zip_filepath = self.exports_dir / zip_filename
            
            self._create_zip_archive(temp_dir, zip_filepath)
            
            logger.info(f"Successfully exported {len(content_list)} HTML pages to ZIP: {zip_filepath}")
            return str(zip_filepath)
            
        finally:
            # Clean up temporary directory
            if temp_dir.exists():
                shutil.rmtree(temp_dir)
    
    def _generate_html_files(
        self,
        content_list: List[Dict[str, Any]],
        output_dir: Path,
        project_name: str,
        options: Dict[str, Any]
    ) -> None:
        """Generate individual HTML files."""
        # Create directory structure
        if options.get('organize_by_template', False):
            self._create_organized_structure(content_list, output_dir, project_name, options)
        else:
            self._create_flat_structure(content_list, output_dir, project_name, options)
        
        # Generate index page
        self._generate_index_page(content_list, output_dir, project_name, options)
        
        # Generate sitemap
        self._generate_sitemap(content_list, output_dir, project_name, options)
        
        # Generate robots.txt
        self._generate_robots_txt(output_dir, options)
        
        # Copy static assets if provided
        if options.get('include_assets', True):
            self._generate_static_assets(output_dir, project_name, options)
    
    def _create_flat_structure(
        self,
        content_list: List[Dict[str, Any]],
        output_dir: Path,
        project_name: str,
        options: Dict[str, Any]
    ) -> None:
        """Create HTML files in flat structure."""
        for item in content_list:
            html_content = self._generate_page_html(item, options)
            
            # Generate filename
            slug = item.get('slug', self._generate_slug(item.get('title', f'page-{item.get("id")}')))
            filename = f"{slug}.html"
            
            # Write file
            filepath = output_dir / filename
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html_content)
    
    def _create_organized_structure(
        self,
        content_list: List[Dict[str, Any]],
        output_dir: Path,
        project_name: str,
        options: Dict[str, Any]
    ) -> None:
        """Create HTML files organized by template/category."""
        # Group content by template
        by_template = defaultdict(list)
        for item in content_list:
            template = item.get('template_used', 'general')
            by_template[template].append(item)
        
        # Create directory for each template
        for template, items in by_template.items():
            template_dir = output_dir / template
            template_dir.mkdir(parents=True, exist_ok=True)
            
            for item in items:
                html_content = self._generate_page_html(item, options)
                
                # Generate filename
                slug = item.get('slug', self._generate_slug(item.get('title', f'page-{item.get("id")}')))
                filename = f"{slug}.html"
                
                # Write file
                filepath = template_dir / filename
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(html_content)
    
    def _generate_page_html(self, item: Dict[str, Any], options: Dict[str, Any]) -> str:
        """Generate HTML content for a single page."""
        template_style = options.get('template_style', 'modern')
        
        if template_style == 'minimal':
            return self._generate_minimal_html(item, options)
        elif template_style == 'blog':
            return self._generate_blog_html(item, options)
        elif template_style == 'landing':
            return self._generate_landing_html(item, options)
        else:
            return self._generate_modern_html(item, options)
    
    def _generate_modern_html(self, item: Dict[str, Any], options: Dict[str, Any]) -> str:
        """Generate modern HTML template."""
        title = item.get('title', 'Untitled')
        meta_description = item.get('meta_description', '')
        content = item.get('content_html', item.get('content', ''))
        keyword = item.get('keyword', '')
        created_at = item.get('created_at', '')
        
        # Parse created_at for display
        try:
            if created_at:
                date_obj = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                formatted_date = date_obj.strftime('%B %d, %Y')
            else:
                formatted_date = 'Unknown'
        except:
            formatted_date = 'Unknown'
        
        css_styles = self._get_modern_css()
        
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <meta name="description" content="{meta_description}">
    {f'<meta name="keywords" content="{keyword}">' if keyword else ''}
    <meta name="robots" content="index, follow">
    <meta name="author" content="Programmatic SEO Tool">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{meta_description}">
    <meta property="og:type" content="article">
    <link rel="canonical" href="{item.get('slug', '')}.html">
    <style>{css_styles}</style>
</head>
<body>
    <header class="header">
        <div class="container">
            <nav class="nav">
                <a href="index.html" class="logo">Home</a>
                <div class="nav-links">
                    <a href="index.html">All Pages</a>
                    <a href="sitemap.xml">Sitemap</a>
                </div>
            </nav>
        </div>
    </header>
    
    <main class="main">
        <div class="container">
            <article class="article">
                <header class="article-header">
                    <h1 class="article-title">{title}</h1>
                    <div class="article-meta">
                        <time datetime="{created_at}">{formatted_date}</time>
                        {f'<span class="keyword-tag">{keyword}</span>' if keyword else ''}
                    </div>
                </header>
                
                <div class="article-content">
                    {content}
                </div>
            </article>
        </div>
    </main>
    
    <footer class="footer">
        <div class="container">
            <p>&copy; 2024 Generated with Programmatic SEO Tool</p>
        </div>
    </footer>
</body>
</html>"""
    
    def _generate_minimal_html(self, item: Dict[str, Any], options: Dict[str, Any]) -> str:
        """Generate minimal HTML template."""
        title = item.get('title', 'Untitled')
        meta_description = item.get('meta_description', '')
        content = item.get('content_html', item.get('content', ''))
        
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <meta name="description" content="{meta_description}">
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; color: #333; max-width: 800px; margin: 0 auto; padding: 20px; }}
        h1 {{ color: #2c3e50; margin-bottom: 20px; }}
        h2 {{ color: #34495e; margin-top: 30px; }}
        p {{ margin-bottom: 15px; }}
        a {{ color: #3498db; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
    </style>
</head>
<body>
    <h1>{title}</h1>
    {content}
    <hr>
    <p><a href="index.html">← Back to all pages</a></p>
</body>
</html>"""
    
    def _generate_blog_html(self, item: Dict[str, Any], options: Dict[str, Any]) -> str:
        """Generate blog-style HTML template."""
        title = item.get('title', 'Untitled')
        meta_description = item.get('meta_description', '')
        content = item.get('content_html', item.get('content', ''))
        word_count = item.get('word_count', 0)
        
        css_styles = self._get_blog_css()
        
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <meta name="description" content="{meta_description}">
    <style>{css_styles}</style>
</head>
<body>
    <div class="blog-container">
        <header class="blog-header">
            <h1 class="blog-title">{title}</h1>
            <div class="blog-meta">
                <span class="reading-time">{self._calculate_reading_time(word_count)} min read</span>
                <span class="word-count">{word_count} words</span>
            </div>
        </header>
        
        <div class="blog-content">
            {content}
        </div>
        
        <footer class="blog-footer">
            <a href="index.html" class="back-link">← View all posts</a>
        </footer>
    </div>
</body>
</html>"""
    
    def _generate_landing_html(self, item: Dict[str, Any], options: Dict[str, Any]) -> str:
        """Generate landing page style HTML template."""
        title = item.get('title', 'Untitled')
        meta_description = item.get('meta_description', '')
        content = item.get('content_html', item.get('content', ''))
        
        css_styles = self._get_landing_css()
        
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <meta name="description" content="{meta_description}">
    <style>{css_styles}</style>
</head>
<body>
    <div class="landing-page">
        <header class="hero">
            <div class="hero-content">
                <h1 class="hero-title">{title}</h1>
                <p class="hero-subtitle">{meta_description}</p>
            </div>
        </header>
        
        <main class="content-section">
            <div class="container">
                {content}
            </div>
        </main>
        
        <footer class="cta-section">
            <div class="container">
                <a href="index.html" class="cta-button">Explore More</a>
            </div>
        </footer>
    </div>
</body>
</html>"""
    
    def _generate_index_page(
        self,
        content_list: List[Dict[str, Any]],
        output_dir: Path,
        project_name: str,
        options: Dict[str, Any]
    ) -> None:
        """Generate index page with links to all content."""
        # Group content by template if organized
        if options.get('organize_by_template', False):
            by_template = defaultdict(list)
            for item in content_list:
                template = item.get('template_used', 'general')
                by_template[template].append(item)
            
            content_html = ""
            for template, items in by_template.items():
                content_html += f'<h2>{template.replace("-", " ").title()}</h2>\n<ul>\n'
                for item in items:
                    slug = item.get('slug', self._generate_slug(item.get('title', f'page-{item.get("id")}')))
                    content_html += f'  <li><a href="{template}/{slug}.html">{item.get("title", "Untitled")}</a></li>\n'
                content_html += '</ul>\n'
        else:
            content_html = "<ul>\n"
            for item in content_list:
                slug = item.get('slug', self._generate_slug(item.get('title', f'page-{item.get("id")}')))
                content_html += f'  <li><a href="{slug}.html">{item.get("title", "Untitled")}</a></li>\n'
            content_html += "</ul>\n"
        
        index_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{project_name} - Content Index</title>
    <meta name="description" content="Index of all pages in {project_name}">
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; color: #333; max-width: 1000px; margin: 0 auto; padding: 20px; }}
        h1 {{ color: #2c3e50; text-align: center; margin-bottom: 30px; }}
        h2 {{ color: #34495e; margin-top: 40px; border-bottom: 2px solid #ecf0f1; padding-bottom: 10px; }}
        ul {{ list-style-type: none; padding: 0; }}
        li {{ margin-bottom: 10px; padding: 10px; background: #f8f9fa; border-radius: 5px; }}
        a {{ color: #3498db; text-decoration: none; font-weight: 500; }}
        a:hover {{ text-decoration: underline; }}
        .stats {{ background: #e8f4f8; padding: 20px; border-radius: 10px; margin-bottom: 30px; text-align: center; }}
        .stats h3 {{ margin: 0 0 10px 0; color: #2c3e50; }}
        .stats p {{ margin: 0; color: #7f8c8d; }}
    </style>
</head>
<body>
    <div class="stats">
        <h3>{project_name}</h3>
        <p>Total Pages: {len(content_list)} | Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>
    
    <h1>Content Index</h1>
    {content_html}
    
    <footer style="margin-top: 50px; text-align: center; padding: 20px; border-top: 1px solid #ecf0f1;">
        <p>Generated with <a href="https://github.com/programmatic-seo-tool">Programmatic SEO Tool</a></p>
    </footer>
</body>
</html>"""
        
        with open(output_dir / 'index.html', 'w', encoding='utf-8') as f:
            f.write(index_html)
    
    def _generate_sitemap(
        self,
        content_list: List[Dict[str, Any]],
        output_dir: Path,
        project_name: str,
        options: Dict[str, Any]
    ) -> None:
        """Generate XML sitemap."""
        base_url = options.get('base_url', 'https://example.com')
        
        sitemap_xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
        sitemap_xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        
        # Add index page
        sitemap_xml += f'  <url>\n'
        sitemap_xml += f'    <loc>{base_url}/index.html</loc>\n'
        sitemap_xml += f'    <lastmod>{datetime.now().strftime("%Y-%m-%d")}</lastmod>\n'
        sitemap_xml += f'    <changefreq>weekly</changefreq>\n'
        sitemap_xml += f'    <priority>1.0</priority>\n'
        sitemap_xml += f'  </url>\n'
        
        # Add all pages
        for item in content_list:
            slug = item.get('slug', self._generate_slug(item.get('title', f'page-{item.get("id")}')))
            
            if options.get('organize_by_template', False):
                template = item.get('template_used', 'general')
                url = f"{base_url}/{template}/{slug}.html"
            else:
                url = f"{base_url}/{slug}.html"
            
            sitemap_xml += f'  <url>\n'
            sitemap_xml += f'    <loc>{url}</loc>\n'
            sitemap_xml += f'    <lastmod>{datetime.now().strftime("%Y-%m-%d")}</lastmod>\n'
            sitemap_xml += f'    <changefreq>weekly</changefreq>\n'
            sitemap_xml += f'    <priority>0.8</priority>\n'
            sitemap_xml += f'  </url>\n'
        
        sitemap_xml += '</urlset>'
        
        with open(output_dir / 'sitemap.xml', 'w', encoding='utf-8') as f:
            f.write(sitemap_xml)
    
    def _generate_robots_txt(self, output_dir: Path, options: Dict[str, Any]) -> None:
        """Generate robots.txt file."""
        base_url = options.get('base_url', 'https://example.com')
        
        robots_txt = f"""User-agent: *
Allow: /

Sitemap: {base_url}/sitemap.xml

# Generated by Programmatic SEO Tool
"""
        
        with open(output_dir / 'robots.txt', 'w', encoding='utf-8') as f:
            f.write(robots_txt)
    
    def _generate_static_assets(self, output_dir: Path, project_name: str, options: Dict[str, Any]) -> None:
        """Generate additional static files."""
        # Create a simple favicon
        favicon_dir = output_dir / 'assets'
        favicon_dir.mkdir(exist_ok=True)
        
        # Generate a simple .htaccess for Apache servers
        htaccess_content = """RewriteEngine On
RewriteRule ^([^.]+)$ $1.html [NC,L]

# Cache static files
<FilesMatch "\.(css|js|png|jpg|jpeg|gif|ico|svg)$">
    Header set Cache-Control "max-age=2592000, public"
</FilesMatch>

# Compress files
<IfModule mod_deflate.c>
    AddOutputFilterByType DEFLATE text/plain
    AddOutputFilterByType DEFLATE text/html
    AddOutputFilterByType DEFLATE text/xml
    AddOutputFilterByType DEFLATE text/css
    AddOutputFilterByType DEFLATE application/xml
    AddOutputFilterByType DEFLATE application/xhtml+xml
    AddOutputFilterByType DEFLATE application/rss+xml
    AddOutputFilterByType DEFLATE application/javascript
    AddOutputFilterByType DEFLATE application/x-javascript
</IfModule>
"""
        
        with open(output_dir / '.htaccess', 'w', encoding='utf-8') as f:
            f.write(htaccess_content)
    
    def _create_zip_archive(self, source_dir: Path, output_zip: Path) -> None:
        """Create ZIP archive from directory."""
        with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(source_dir):
                for file in files:
                    file_path = Path(root) / file
                    arcname = file_path.relative_to(source_dir)
                    zipf.write(file_path, arcname)
    
    def _generate_slug(self, title: str) -> str:
        """Generate URL-friendly slug."""
        import re
        slug = re.sub(r'[^a-zA-Z0-9\s-]', '', title.lower())
        slug = re.sub(r'\s+', '-', slug)
        return slug.strip('-')
    
    def _calculate_reading_time(self, word_count: int) -> int:
        """Calculate reading time in minutes."""
        if word_count == 0:
            return 1
        return max(1, round(word_count / 200))
    
    def _get_modern_css(self) -> str:
        """Get modern CSS styles."""
        return """
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 1200px; margin: 0 auto; padding: 0 20px; }
        .header { background: #fff; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .nav { display: flex; justify-content: space-between; align-items: center; padding: 1rem 0; }
        .logo { font-size: 1.5rem; font-weight: bold; text-decoration: none; color: #2c3e50; }
        .nav-links { display: flex; gap: 2rem; }
        .nav-links a { text-decoration: none; color: #7f8c8d; font-weight: 500; }
        .nav-links a:hover { color: #3498db; }
        .main { padding: 2rem 0; }
        .article { background: #fff; padding: 2rem; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .article-title { font-size: 2.5rem; color: #2c3e50; margin-bottom: 1rem; }
        .article-meta { color: #7f8c8d; margin-bottom: 2rem; }
        .keyword-tag { background: #3498db; color: white; padding: 0.25rem 0.5rem; border-radius: 4px; font-size: 0.8rem; margin-left: 1rem; }
        .article-content { font-size: 1.1rem; line-height: 1.8; }
        .article-content h2 { color: #34495e; margin: 2rem 0 1rem 0; }
        .article-content p { margin-bottom: 1rem; }
        .footer { background: #34495e; color: white; text-align: center; padding: 2rem 0; }
        """
    
    def _get_blog_css(self) -> str:
        """Get blog-style CSS."""
        return """
        body { font-family: Georgia, serif; line-height: 1.7; color: #333; background: #f8f9fa; }
        .blog-container { max-width: 800px; margin: 0 auto; padding: 2rem; background: white; min-height: 100vh; }
        .blog-header { border-bottom: 2px solid #ecf0f1; padding-bottom: 2rem; margin-bottom: 2rem; }
        .blog-title { font-size: 2.5rem; color: #2c3e50; margin-bottom: 1rem; }
        .blog-meta { color: #7f8c8d; font-size: 0.9rem; }
        .blog-content { font-size: 1.1rem; line-height: 1.8; }
        .blog-content h2 { color: #34495e; margin: 2rem 0 1rem 0; }
        .blog-content p { margin-bottom: 1.5rem; }
        .blog-footer { border-top: 1px solid #ecf0f1; padding-top: 2rem; margin-top: 3rem; }
        .back-link { color: #3498db; text-decoration: none; font-weight: 500; }
        .back-link:hover { text-decoration: underline; }
        """
    
    def _get_landing_css(self) -> str:
        """Get landing page CSS."""
        return """
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin: 0; }
        .landing-page { min-height: 100vh; }
        .hero { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 4rem 0; text-align: center; }
        .hero-content { max-width: 800px; margin: 0 auto; padding: 0 2rem; }
        .hero-title { font-size: 3rem; margin-bottom: 1rem; }
        .hero-subtitle { font-size: 1.2rem; opacity: 0.9; }
        .content-section { padding: 4rem 0; }
        .container { max-width: 1200px; margin: 0 auto; padding: 0 2rem; }
        .cta-section { background: #34495e; color: white; padding: 3rem 0; text-align: center; }
        .cta-button { background: #3498db; color: white; padding: 1rem 2rem; border-radius: 5px; text-decoration: none; font-weight: bold; }
        .cta-button:hover { background: #2980b9; }
        """