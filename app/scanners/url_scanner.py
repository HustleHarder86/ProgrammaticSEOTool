"""URL-based business scanner and analyzer."""
import logging
import re
from typing import List, Dict, Optional, Set
from urllib.parse import urljoin, urlparse
import asyncio
import aiohttp
from bs4 import BeautifulSoup
from app.scanners.base import BusinessAnalyzer, BusinessInfo, ContentOpportunity
from app.scanners.text_analyzer import TextBusinessAnalyzer

logger = logging.getLogger(__name__)

class URLBusinessScanner(BusinessAnalyzer):
    """Scans and analyzes business websites."""
    
    def __init__(self):
        self.text_analyzer = TextBusinessAnalyzer()
        self.session = None
        
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def _fetch_page(self, url: str) -> Optional[str]:
        """Fetch page content."""
        try:
            async with self.session.get(url, timeout=10) as response:
                if response.status == 200:
                    return await response.text()
        except Exception as e:
            logger.error(f"Error fetching {url}: {e}")
        return None
    
    def _extract_text_from_html(self, html: str) -> str:
        """Extract readable text from HTML."""
        soup = BeautifulSoup(html, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Get text
        text = soup.get_text(separator=' ', strip=True)
        
        # Clean up whitespace
        text = re.sub(r'\s+', ' ', text)
        
        return text[:5000]  # Limit to 5000 chars for AI analysis
    
    def _extract_metadata(self, soup: BeautifulSoup) -> Dict:
        """Extract metadata from the page."""
        metadata = {
            'title': '',
            'description': '',
            'keywords': [],
            'headings': {'h1': [], 'h2': [], 'h3': []}
        }
        
        # Title
        title_tag = soup.find('title')
        if title_tag:
            metadata['title'] = title_tag.get_text(strip=True)
        
        # Meta description
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc:
            metadata['description'] = meta_desc.get('content', '')
        
        # Meta keywords
        meta_keywords = soup.find('meta', attrs={'name': 'keywords'})
        if meta_keywords:
            metadata['keywords'] = [k.strip() for k in meta_keywords.get('content', '').split(',')]
        
        # Headings
        for level in ['h1', 'h2', 'h3']:
            headings = soup.find_all(level)
            metadata['headings'][level] = [h.get_text(strip=True) for h in headings[:5]]
        
        return metadata
    
    def _find_related_pages(self, soup: BeautifulSoup, base_url: str) -> List[str]:
        """Find related pages like About, Services, etc."""
        related_urls = []
        keywords = ['about', 'services', 'products', 'solutions', 'what-we-do', 'portfolio']
        
        for link in soup.find_all('a', href=True):
            href = link['href'].lower()
            text = link.get_text(strip=True).lower()
            
            for keyword in keywords:
                if keyword in href or keyword in text:
                    full_url = urljoin(base_url, link['href'])
                    if urlparse(full_url).netloc == urlparse(base_url).netloc:
                        related_urls.append(full_url)
                        break
        
        # Remove duplicates
        return list(set(related_urls))[:5]  # Limit to 5 pages
    
    async def analyze(self, url: str) -> BusinessInfo:
        """Scan and analyze a business website."""
        if not self.session:
            self.session = aiohttp.ClientSession()
        
        try:
            # Fetch homepage
            homepage_html = await self._fetch_page(url)
            if not homepage_html:
                raise ValueError(f"Could not fetch {url}")
            
            soup = BeautifulSoup(homepage_html, 'html.parser')
            
            # Extract metadata
            metadata = self._extract_metadata(soup)
            
            # Extract main content
            main_text = self._extract_text_from_html(homepage_html)
            
            # Find and fetch related pages
            related_urls = self._find_related_pages(soup, url)
            related_texts = []
            
            if related_urls:
                # Fetch related pages concurrently
                tasks = [self._fetch_page(related_url) for related_url in related_urls[:3]]
                related_pages = await asyncio.gather(*tasks)
                
                for page_html in related_pages:
                    if page_html:
                        related_texts.append(self._extract_text_from_html(page_html))
            
            # Combine all text for analysis
            combined_text = f"""
Website: {url}
Title: {metadata['title']}
Description: {metadata['description']}
Keywords: {', '.join(metadata['keywords'])}

Main Headings:
{' '.join(metadata['headings']['h1'])}
{' '.join(metadata['headings']['h2'])}

Main Content:
{main_text}

Related Pages Content:
{' '.join(related_texts)}
"""
            
            # Use text analyzer to extract business info
            business_info = await self.text_analyzer.analyze(combined_text)
            
            # Enhance with URL-specific data
            if not business_info.name and metadata['title']:
                business_info.name = metadata['title'].split('-')[0].split('|')[0].strip()
            
            # Add keywords from meta tags
            business_info.keywords.extend(metadata['keywords'])
            business_info.keywords = list(set(business_info.keywords))  # Remove duplicates
            
            logger.info(f"Successfully scanned and analyzed {url}")
            return business_info
            
        except Exception as e:
            logger.error(f"Error scanning {url}: {e}")
            # Return basic info on error
            return BusinessInfo(
                name=urlparse(url).netloc,
                description=f"Business website at {url}",
                keywords=[urlparse(url).netloc.replace('.', ' ').split()[0]]
            )
    
    async def identify_opportunities(self, business_info: BusinessInfo) -> List[ContentOpportunity]:
        """Generate content opportunities using the text analyzer."""
        return await self.text_analyzer.identify_opportunities(business_info)