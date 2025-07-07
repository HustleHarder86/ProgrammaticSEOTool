"""Content variation engine to ensure uniqueness across generated pages"""
import random
import re
from typing import List, Dict, Any, Optional
from datetime import datetime


class ContentVariationEngine:
    def __init__(self):
        # Initialize variation templates
        self.intro_variations = [
            "Looking for {keyword}? You've come to the right place.",
            "If you're searching for {keyword}, this comprehensive guide covers everything you need to know.",
            "Discover the complete guide to {keyword} with expert insights and practical tips.",
            "{keyword} can be complex, but we've broken it down into simple, actionable steps.",
            "Whether you're a beginner or expert, this {keyword} guide has valuable information for you.",
            "Welcome to the definitive resource for {keyword}. Let's dive into what you need to know.",
            "Understanding {keyword} is crucial for success. Here's your complete guide.",
            "Ready to master {keyword}? This guide will walk you through everything step by step."
        ]
        
        self.transition_phrases = [
            "Furthermore,", "Additionally,", "Moreover,", "It's worth noting that",
            "Another important aspect is", "Let's dive deeper into", "Building on this,",
            "To expand on this point,", "Equally important is", "This brings us to",
            "It's also essential to consider", "Moving forward,", "As we explore further,"
        ]
        
        self.conclusion_variations = [
            "In conclusion, {keyword} is an important topic that requires careful consideration.",
            "To sum up, mastering {keyword} can significantly improve your {benefit}.",
            "Now that you understand {keyword}, you're ready to {action}.",
            "The key takeaway about {keyword} is {main_point}.",
            "By following these {keyword} guidelines, you'll be well on your way to success.",
            "We hope this guide to {keyword} has provided you with valuable insights and actionable strategies.",
            "Remember, {keyword} is a journey, not a destination. Keep learning and improving.",
            "With this knowledge of {keyword}, you're equipped to make informed decisions."
        ]
        
        # Synonym dictionary for variation
        self.synonyms = {
            "important": ["crucial", "essential", "vital", "significant", "key", "critical", "fundamental"],
            "help": ["assist", "aid", "support", "facilitate", "enable", "empower", "guide"],
            "improve": ["enhance", "boost", "optimize", "strengthen", "elevate", "upgrade", "refine"],
            "understand": ["comprehend", "grasp", "master", "learn", "discover", "explore", "uncover"],
            "create": ["develop", "build", "design", "establish", "generate", "construct", "produce"],
            "use": ["utilize", "employ", "apply", "implement", "leverage", "harness", "deploy"],
            "show": ["demonstrate", "illustrate", "reveal", "display", "present", "exhibit", "highlight"],
            "good": ["excellent", "effective", "beneficial", "valuable", "advantageous", "superior", "optimal"],
            "many": ["numerous", "various", "multiple", "several", "diverse", "countless", "abundant"],
            "need": ["require", "demand", "necessitate", "call for", "depend on", "warrant", "entail"],
            "provide": ["offer", "deliver", "supply", "furnish", "present", "give", "yield"],
            "ensure": ["guarantee", "secure", "maintain", "preserve", "safeguard", "protect", "uphold"]
        }
        
        # Content structure variations
        self.structure_variations = [
            ["introduction", "main_points", "examples", "conclusion", "faq"],
            ["overview", "detailed_analysis", "case_studies", "best_practices", "summary"],
            ["quick_answer", "in_depth_explanation", "practical_tips", "common_mistakes", "next_steps"],
            ["executive_summary", "key_concepts", "implementation", "results", "recommendations"],
            ["problem_statement", "solution_overview", "step_by_step", "troubleshooting", "resources"]
        ]

    def generate_unique_intro(self, keyword: str, variation_index: int) -> str:
        """Generate a unique introduction paragraph"""
        # Select intro variation based on index
        intro_template = self.intro_variations[variation_index % len(self.intro_variations)]
        intro = intro_template.format(keyword=keyword)
        
        # Add additional context
        context_additions = [
            f" In today's competitive landscape, {keyword} has become more important than ever.",
            f" This guide will walk you through the essential aspects of {keyword}.",
            f" We'll explore proven strategies and best practices for {keyword}.",
            f" Our experts have compiled this comprehensive resource on {keyword}.",
            f" By the end of this guide, you'll have a solid understanding of {keyword}."
        ]
        
        intro += context_additions[variation_index % len(context_additions)]
        
        return intro

    def vary_sentence_structure(self, content: str) -> str:
        """Vary sentence structure to create unique content"""
        sentences = content.split('. ')
        
        # Skip if content is too short
        if len(sentences) < 3:
            return content
        
        # Apply various transformations
        varied_sentences = []
        
        for i, sentence in enumerate(sentences):
            # Skip empty sentences
            if not sentence.strip():
                continue
                
            # Occasionally add transition phrases
            if i > 0 and i % 3 == 0 and len(self.transition_phrases) > 0:
                transition = random.choice(self.transition_phrases)
                sentence = f"{transition} {sentence.lower()}"
            
            # Vary sentence beginnings
            if i % 4 == 1 and not sentence.startswith(('However', 'Moreover', 'Furthermore')):
                beginnings = [
                    "It's important to note that",
                    "One key aspect is that",
                    "Research shows that",
                    "Experience indicates that",
                    "Industry experts agree that"
                ]
                beginning = random.choice(beginnings)
                sentence = f"{beginning} {sentence.lower()}"
            
            varied_sentences.append(sentence)
        
        return '. '.join(varied_sentences)

    def apply_synonym_variation(self, content: str) -> str:
        """Replace words with synonyms for variation"""
        varied_content = content
        
        # Apply synonym replacements
        for base_word, alternatives in self.synonyms.items():
            if base_word in varied_content.lower():
                # Choose a random synonym
                replacement = random.choice(alternatives)
                
                # Replace with case preservation
                pattern = re.compile(r'\b' + base_word + r'\b', re.IGNORECASE)
                
                def replace_with_case(match):
                    original = match.group()
                    if original.isupper():
                        return replacement.upper()
                    elif original[0].isupper():
                        return replacement.capitalize()
                    else:
                        return replacement
                
                varied_content = pattern.sub(replace_with_case, varied_content)
        
        return varied_content

    def generate_unique_structure(self, keyword: str, content_type: str) -> Dict[str, Any]:
        """Generate a unique content structure"""
        # Determine structure based on content type
        if "comparison" in keyword.lower() or "vs" in keyword.lower():
            structure = ["introduction", "criteria", "comparison_table", "detailed_analysis", "verdict", "alternatives"]
        elif "how to" in keyword.lower():
            structure = ["introduction", "requirements", "step_by_step", "tips", "troubleshooting", "conclusion"]
        elif "best" in keyword.lower() or "top" in keyword.lower():
            structure = ["introduction", "evaluation_criteria", "top_picks", "detailed_reviews", "comparison", "buying_guide"]
        else:
            # Select random structure
            structure = random.choice(self.structure_variations)
        
        return {
            "structure": structure,
            "word_count_target": random.randint(1200, 2000),
            "unique_elements": self._get_unique_elements(keyword)
        }

    def _get_unique_elements(self, keyword: str) -> List[str]:
        """Get unique content elements to add"""
        possible_elements = [
            "custom_infographic",
            "data_visualization",
            "expert_quotes",
            "case_study",
            "interactive_calculator",
            "downloadable_checklist",
            "comparison_table",
            "pros_cons_list",
            "timeline",
            "statistics_section",
            "user_testimonials",
            "related_tools",
            "glossary",
            "quick_reference_guide",
            "video_tutorial",
            "implementation_roadmap"
        ]
        
        # Select 3-5 unique elements
        num_elements = random.randint(3, 5)
        selected_elements = random.sample(possible_elements, num_elements)
        
        return selected_elements

    def add_contextual_content(self, content: str, keyword: str) -> str:
        """Add contextual information to make content more unique"""
        additions = []
        
        # Add temporal context
        current_year = datetime.now().year
        additions.append(
            f"As of {current_year}, {keyword} continues to evolve with new trends and technologies."
        )
        
        # Add industry context
        industries = ["technology", "healthcare", "finance", "retail", "manufacturing", "education"]
        industry = random.choice(industries)
        additions.append(
            f"In the {industry} sector, {keyword} plays a particularly important role in driving innovation and efficiency."
        )
        
        # Add statistical context (mock data for now)
        percentage = random.randint(65, 95)
        additions.append(
            f"Studies show that {percentage}% of professionals consider {keyword} essential for their success."
        )
        
        # Insert additions at appropriate points
        paragraphs = content.split('\n\n')
        
        for addition in additions:
            if len(paragraphs) > 2:
                # Insert at random positions (not at beginning or end)
                insert_pos = random.randint(1, len(paragraphs) - 1)
                paragraphs.insert(insert_pos, addition)
        
        return '\n\n'.join(paragraphs)

    def ensure_keyword_density(self, content: str, keyword: str, target_density: float = 0.02) -> str:
        """Ensure appropriate keyword density (around 2%)"""
        words = content.split()
        word_count = len(words)
        keyword_count = content.lower().count(keyword.lower())
        
        current_density = keyword_count / word_count if word_count > 0 else 0
        
        # If density is too low, add keyword mentions
        if current_density < target_density:
            additions_needed = int((target_density * word_count) - keyword_count)
            
            keyword_additions = [
                f"When considering {keyword}, it's important to evaluate all options.",
                f"The benefits of {keyword} extend beyond the obvious advantages.",
                f"Implementing {keyword} requires careful planning and execution.",
                f"Many professionals rely on {keyword} for optimal results.",
                f"Understanding {keyword} is the first step toward success."
            ]
            
            # Add keyword mentions throughout content
            paragraphs = content.split('\n\n')
            for i in range(min(additions_needed, len(keyword_additions))):
                if len(paragraphs) > 1:
                    insert_pos = random.randint(1, len(paragraphs))
                    paragraphs.insert(insert_pos, keyword_additions[i])
            
            content = '\n\n'.join(paragraphs)
        
        return content

    def generate_unique_conclusion(self, keyword: str, variation_index: int) -> str:
        """Generate a unique conclusion paragraph"""
        # Select conclusion variation
        conclusion_template = self.conclusion_variations[variation_index % len(self.conclusion_variations)]
        
        # Fill in template variables
        conclusion = conclusion_template.format(
            keyword=keyword,
            benefit="overall performance and results",
            action="implement these strategies effectively",
            main_point="that proper implementation leads to success"
        )
        
        # Add call to action
        cta_options = [
            f"Ready to get started with {keyword}? Contact us today for expert guidance.",
            f"Take the next step in your {keyword} journey. Our team is here to help.",
            f"Don't let {keyword} challenges hold you back. Let's work together to find solutions.",
            f"Transform your approach to {keyword} with our proven strategies.",
            f"Start implementing these {keyword} best practices today for immediate results."
        ]
        
        conclusion += " " + cta_options[variation_index % len(cta_options)]
        
        return conclusion


def enhance_content_quality(content: str, keyword: str, business_info: Dict,
                          all_keywords: Optional[List[str]] = None,
                          cluster_keywords: Optional[List[str]] = None) -> str:
    """Enhance content quality with internal linking and additional elements"""
    enhanced_content = content
    
    # Add internal links if available
    if all_keywords:
        enhanced_content = _add_internal_links(enhanced_content, keyword, all_keywords[:10])
    
    # Add schema markup suggestion
    schema_markup = f"""
<!-- Schema Markup for SEO -->
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "{keyword}",
  "author": {{
    "@type": "Organization",
    "name": "{business_info.get('name', 'Your Business')}"
  }},
  "datePublished": "{datetime.now().isoformat()}",
  "description": "Comprehensive guide to {keyword}"
}}
</script>
"""
    
    enhanced_content += f"\n\n{schema_markup}"
    
    # Add related articles section
    if all_keywords and len(all_keywords) > 3:
        related_section = "\n\n## Related Articles\n\n"
        for related_keyword in all_keywords[:5]:
            if related_keyword != keyword:
                slug = related_keyword.lower().replace(' ', '-')
                related_section += f"- [{related_keyword}](/{slug})\n"
        
        enhanced_content += related_section
    
    return enhanced_content


def _add_internal_links(content: str, current_keyword: str, related_keywords: List[str]) -> str:
    """Add internal links to related content"""
    linked_content = content
    links_added = 0
    max_links = 5
    
    for related_keyword in related_keywords:
        if links_added >= max_links:
            break
        
        if related_keyword.lower() == current_keyword.lower():
            continue
        
        # Find mentions of related terms
        words = related_keyword.lower().split()
        for word in words:
            if len(word) > 4 and word in linked_content.lower():
                # Create link
                slug = related_keyword.lower().replace(' ', '-')
                link = f'[{word}](/{slug})'
                
                # Replace first occurrence
                pattern = re.compile(r'\b' + re.escape(word) + r'\b', re.IGNORECASE)
                linked_content = pattern.sub(link, linked_content, count=1)
                links_added += 1
                break
    
    return linked_content


def ensure_minimum_quality(content: str, keyword: str) -> Dict[str, Any]:
    """Ensure content meets minimum quality standards"""
    word_count = len(content.split())
    
    quality_metrics = {
        "word_count": word_count,
        "meets_minimum": word_count >= 800,
        "has_headers": "##" in content or "#" in content,
        "has_lists": "-" in content or "1." in content,
        "has_paragraphs": len(content.split('\n\n')) > 3,
        "keyword_density": content.lower().count(keyword.lower()) / word_count * 100 if word_count > 0 else 0,
        "readability_elements": {
            "short_sentences": len([s for s in content.split('.') if 0 < len(s.split()) < 20]) > 5,
            "bullet_points": content.count('\n-') > 2,
            "subheadings": content.count('\n##') > 2
        }
    }
    
    # Calculate quality score
    quality_score = 0
    if quality_metrics["meets_minimum"]:
        quality_score += 25
    if quality_metrics["has_headers"]:
        quality_score += 20
    if quality_metrics["has_lists"]:
        quality_score += 15
    if quality_metrics["has_paragraphs"]:
        quality_score += 20
    if 1.5 < quality_metrics["keyword_density"] < 3.5:
        quality_score += 20
    
    quality_metrics["quality_score"] = quality_score
    
    return quality_metrics