"""Content Variation Agent for ensuring unique content generation."""
import hashlib
import re
import random
from typing import List, Dict, Set, Tuple
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class ContentVariationAgent:
    """Ensures content uniqueness across generated pages."""
    
    def __init__(self):
        self.content_fingerprints: Set[str] = set()
        self.used_titles: Set[str] = set()
        self.variation_templates = self._load_variation_templates()
    
    def _load_variation_templates(self) -> Dict[str, List[str]]:
        """Load templates for content variations."""
        return {
            'intro_variations': [
                "In this comprehensive guide, we'll explore {topic}",
                "Discover everything you need to know about {topic}",
                "This article provides detailed insights into {topic}",
                "Learn the essential aspects of {topic}",
                "Understanding {topic}: A complete overview"
            ],
            'data_points': [
                "According to recent studies",
                "Industry research shows",
                "Data indicates that",
                "Statistics reveal",
                "Analysis demonstrates"
            ],
            'unique_elements': [
                'comparison_table',
                'pros_cons_list',
                'faq_section',
                'case_study',
                'infographic_data',
                'checklist',
                'timeline',
                'statistics_box'
            ]
        }
    
    def generate_content_fingerprint(self, content: str) -> str:
        """Generate a fingerprint for content to detect duplicates."""
        # Remove common variations (numbers, dates, specific names)
        normalized = re.sub(r'\d+', 'NUM', content.lower())
        normalized = re.sub(r'\b(january|february|march|april|may|june|july|august|september|october|november|december)\b', 'MONTH', normalized)
        normalized = re.sub(r'\b(monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b', 'DAY', normalized)
        
        # Create hash of normalized content
        return hashlib.md5(normalized.encode()).hexdigest()
    
    def is_content_unique(self, content: str, threshold: float = 0.8) -> Tuple[bool, float]:
        """Check if content is sufficiently unique."""
        fingerprint = self.generate_content_fingerprint(content)
        
        if fingerprint in self.content_fingerprints:
            return False, 0.0
        
        # Calculate similarity with existing content
        # For now, using fingerprint matching; could be enhanced with more sophisticated similarity metrics
        self.content_fingerprints.add(fingerprint)
        return True, 1.0
    
    def ensure_title_uniqueness(self, base_title: str, keyword: str) -> str:
        """Generate a unique title variation."""
        if base_title not in self.used_titles:
            self.used_titles.add(base_title)
            return base_title
        
        # Generate variations
        variations = [
            f"{base_title} - Complete Guide",
            f"{base_title} ({datetime.now().year})",
            f"Ultimate {base_title}",
            f"{base_title}: Everything You Need to Know",
            f"The Definitive Guide to {keyword}",
            f"{base_title} - Expert Insights"
        ]
        
        for variant in variations:
            if variant not in self.used_titles:
                self.used_titles.add(variant)
                return variant
        
        # Fallback with timestamp
        unique_title = f"{base_title} - {datetime.now().strftime('%B %Y')}"
        self.used_titles.add(unique_title)
        return unique_title
    
    def add_unique_elements(self, content: str, keyword: str, content_type: str) -> Dict[str, any]:
        """Add unique elements to differentiate content."""
        elements = []
        
        # Select 2-3 unique elements based on content type
        if content_type == 'comparison':
            elements = ['comparison_table', 'pros_cons_list', 'verdict_box']
        elif content_type == 'how-to':
            elements = ['checklist', 'timeline', 'difficulty_rating']
        elif content_type == 'guide':
            elements = ['faq_section', 'case_study', 'expert_tips']
        else:
            elements = random.sample(self.variation_templates['unique_elements'], 3)
        
        return {
            'unique_elements': elements,
            'custom_data': self._generate_custom_data(keyword, elements)
        }
    
    def _generate_custom_data(self, keyword: str, elements: List[str]) -> Dict[str, any]:
        """Generate custom data for unique elements."""
        custom_data = {}
        
        for element in elements:
            if element == 'comparison_table':
                custom_data[element] = self._generate_comparison_data(keyword)
            elif element == 'pros_cons_list':
                custom_data[element] = self._generate_pros_cons(keyword)
            elif element == 'faq_section':
                custom_data[element] = self._generate_faqs(keyword)
            elif element == 'statistics_box':
                custom_data[element] = self._generate_statistics(keyword)
            elif element == 'checklist':
                custom_data[element] = self._generate_checklist(keyword)
        
        return custom_data
    
    def _generate_comparison_data(self, keyword: str) -> Dict:
        """Generate comparison table data."""
        return {
            'headers': ['Feature', 'Option A', 'Option B', 'Best For'],
            'rows': [
                ['Price', '$', '$$', 'Budget users'],
                ['Ease of Use', 'Beginner', 'Advanced', 'Professionals'],
                ['Support', '24/7', 'Business hours', 'Enterprise']
            ]
        }
    
    def _generate_pros_cons(self, keyword: str) -> Dict:
        """Generate pros and cons list."""
        return {
            'pros': [
                'Cost-effective solution',
                'Easy to implement',
                'Scalable approach',
                'Great support'
            ],
            'cons': [
                'Learning curve',
                'Initial setup time',
                'Limited customization'
            ]
        }
    
    def _generate_faqs(self, keyword: str) -> List[Dict]:
        """Generate FAQ section."""
        return [
            {
                'question': f'What is {keyword}?',
                'answer': f'{keyword} is a comprehensive solution that helps you achieve your goals efficiently.'
            },
            {
                'question': f'How does {keyword} work?',
                'answer': f'It works by implementing proven strategies and best practices in the field.'
            },
            {
                'question': f'Is {keyword} suitable for beginners?',
                'answer': 'Yes, it\'s designed to be accessible for users at all skill levels.'
            }
        ]
    
    def _generate_statistics(self, keyword: str) -> List[Dict]:
        """Generate statistics for the content."""
        return [
            {'stat': '85%', 'label': 'Success Rate'},
            {'stat': '10,000+', 'label': 'Active Users'},
            {'stat': '4.8/5', 'label': 'Average Rating'},
            {'stat': '24/7', 'label': 'Support Available'}
        ]
    
    def _generate_checklist(self, keyword: str) -> List[str]:
        """Generate a checklist."""
        return [
            'Define your objectives clearly',
            'Research available options',
            'Compare features and pricing',
            'Test with a small pilot',
            'Implement gradually',
            'Monitor results',
            'Optimize based on data'
        ]
    
    def apply_content_variations(self, content: str, variations: Dict) -> str:
        """Apply variations to content to ensure uniqueness."""
        # Add unique elements to content
        enhanced_content = content
        
        if 'unique_elements' in variations:
            for element in variations['unique_elements']:
                if element == 'comparison_table' and element in variations.get('custom_data', {}):
                    table_html = self._format_comparison_table(variations['custom_data'][element])
                    enhanced_content += f"\n\n{table_html}"
                elif element == 'pros_cons_list' and element in variations.get('custom_data', {}):
                    pros_cons_html = self._format_pros_cons(variations['custom_data'][element])
                    enhanced_content += f"\n\n{pros_cons_html}"
                elif element == 'faq_section' and element in variations.get('custom_data', {}):
                    faq_html = self._format_faqs(variations['custom_data'][element])
                    enhanced_content += f"\n\n{faq_html}"
        
        return enhanced_content
    
    def _format_comparison_table(self, data: Dict) -> str:
        """Format comparison table as HTML."""
        html = '<div class="comparison-table">\n<table>\n<thead>\n<tr>\n'
        for header in data['headers']:
            html += f'<th>{header}</th>\n'
        html += '</tr>\n</thead>\n<tbody>\n'
        for row in data['rows']:
            html += '<tr>\n'
            for cell in row:
                html += f'<td>{cell}</td>\n'
            html += '</tr>\n'
        html += '</tbody>\n</table>\n</div>'
        return html
    
    def _format_pros_cons(self, data: Dict) -> str:
        """Format pros and cons as HTML."""
        html = '<div class="pros-cons">\n'
        html += '<div class="pros">\n<h3>Pros</h3>\n<ul>\n'
        for pro in data['pros']:
            html += f'<li>{pro}</li>\n'
        html += '</ul>\n</div>\n'
        html += '<div class="cons">\n<h3>Cons</h3>\n<ul>\n'
        for con in data['cons']:
            html += f'<li>{con}</li>\n'
        html += '</ul>\n</div>\n</div>'
        return html
    
    def _format_faqs(self, faqs: List[Dict]) -> str:
        """Format FAQs as HTML."""
        html = '<div class="faq-section">\n<h2>Frequently Asked Questions</h2>\n'
        for faq in faqs:
            html += f'<div class="faq-item">\n'
            html += f'<h3>{faq["question"]}</h3>\n'
            html += f'<p>{faq["answer"]}</p>\n'
            html += '</div>\n'
        html += '</div>'
        return html
    
    def calculate_uniqueness_score(self, content1: str, content2: str) -> float:
        """Calculate uniqueness score between two pieces of content."""
        # Simple word-based comparison
        words1 = set(content1.lower().split())
        words2 = set(content2.lower().split())
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        if not union:
            return 1.0
        
        jaccard_similarity = len(intersection) / len(union)
        uniqueness = 1.0 - jaccard_similarity
        
        return uniqueness