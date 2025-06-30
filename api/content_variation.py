"""Content variation engine to avoid duplicate content penalties"""
import random
import re
from typing import List, Dict, Any

class ContentVariationEngine:
    def __init__(self):
        # Variation templates for different content types
        self.intro_variations = [
            "Looking for {keyword}? You've come to the right place.",
            "If you're searching for {keyword}, this comprehensive guide covers everything you need to know.",
            "Discover the complete guide to {keyword} with expert insights and practical tips.",
            "{keyword} can be complex, but we've broken it down into simple, actionable steps.",
            "Whether you're a beginner or expert, this {keyword} guide has valuable information for you."
        ]
        
        self.structure_variations = [
            ["introduction", "main_points", "examples", "conclusion", "faq"],
            ["overview", "detailed_analysis", "case_studies", "best_practices", "summary"],
            ["quick_answer", "in_depth_explanation", "practical_tips", "common_mistakes", "next_steps"],
            ["executive_summary", "key_concepts", "implementation", "results", "recommendations"],
            ["problem_statement", "solution_overview", "step_by_step", "troubleshooting", "resources"]
        ]
        
        self.transition_phrases = [
            "Furthermore,", "Additionally,", "Moreover,", "It's worth noting that",
            "Another important aspect is", "Let's dive deeper into", "Building on this,",
            "To expand on this point,", "Equally important is", "This brings us to"
        ]
        
        self.conclusion_variations = [
            "In conclusion, {keyword} is an important topic that requires careful consideration.",
            "To sum up, mastering {keyword} can significantly improve your {benefit}.",
            "Now that you understand {keyword}, you're ready to {action}.",
            "The key takeaway about {keyword} is {main_point}.",
            "By following these {keyword} guidelines, you'll be well on your way to success."
        ]

    def generate_unique_structure(self, keyword: str, content_type: str) -> Dict[str, Any]:
        """Generate a unique content structure"""
        # Select random structure
        structure = random.choice(self.structure_variations)
        
        # Add unique elements based on content type
        if "comparison" in keyword.lower() or "vs" in keyword.lower():
            structure = ["introduction", "criteria", "comparison_table", "detailed_analysis", "verdict", "alternatives"]
        elif "how to" in keyword.lower():
            structure = ["introduction", "requirements", "step_by_step", "tips", "troubleshooting", "conclusion"]
        elif "best" in keyword.lower() or "top" in keyword.lower():
            structure = ["introduction", "evaluation_criteria", "top_picks", "detailed_reviews", "comparison", "buying_guide"]
        
        return {
            "structure": structure,
            "word_count_target": random.randint(1500, 2500),
            "unique_elements": self.get_unique_elements(keyword)
        }

    def get_unique_elements(self, keyword: str) -> List[str]:
        """Get unique content elements to add"""
        elements = []
        
        # Always add some unique elements
        possible_elements = [
            "custom_infographic",
            "data_visualization",
            "expert_quotes",
            "case_study",
            "video_embed",
            "interactive_calculator",
            "downloadable_checklist",
            "comparison_table",
            "pros_cons_list",
            "timeline",
            "statistics_section",
            "user_testimonials",
            "related_tools",
            "glossary",
            "quick_reference_guide"
        ]
        
        # Select 3-5 unique elements
        num_elements = random.randint(3, 5)
        elements = random.sample(possible_elements, num_elements)
        
        return elements

    def vary_content(self, base_content: str, keyword: str, variations_needed: int = 1) -> List[Dict[str, str]]:
        """Generate content variations to avoid duplication"""
        variations = []
        
        for i in range(variations_needed):
            # Create variation
            varied_content = base_content
            
            # Vary sentence structure
            varied_content = self.vary_sentences(varied_content)
            
            # Add unique sections
            varied_content = self.add_unique_sections(varied_content, keyword, i)
            
            # Vary vocabulary
            varied_content = self.vary_vocabulary(varied_content)
            
            # Add local/specific context
            varied_content = self.add_contextual_content(varied_content, keyword)
            
            variations.append({
                "content": varied_content,
                "unique_id": f"{keyword}-var-{i}",
                "variation_type": self.get_variation_type(i)
            })
        
        return variations

    def vary_sentences(self, content: str) -> str:
        """Vary sentence structure and order"""
        sentences = content.split('. ')
        
        # Randomly reorder some paragraphs
        if len(sentences) > 5:
            # Keep first and last, shuffle middle
            middle = sentences[1:-1]
            random.shuffle(middle)
            sentences = [sentences[0]] + middle + [sentences[-1]]
        
        # Join with varied punctuation
        varied = '. '.join(sentences)
        
        # Add transition phrases
        for phrase in random.sample(self.transition_phrases, 3):
            # Find a good spot to insert
            sentences = varied.split('. ')
            if len(sentences) > 2:
                insert_pos = random.randint(1, len(sentences)-1)
                sentences[insert_pos] = phrase + " " + sentences[insert_pos]
                varied = '. '.join(sentences)
        
        return varied

    def vary_vocabulary(self, content: str) -> str:
        """Replace words with synonyms"""
        synonyms = {
            "important": ["crucial", "essential", "vital", "significant", "key"],
            "help": ["assist", "aid", "support", "facilitate", "enable"],
            "improve": ["enhance", "boost", "optimize", "strengthen", "elevate"],
            "understand": ["comprehend", "grasp", "master", "learn", "discover"],
            "create": ["develop", "build", "design", "establish", "generate"],
            "use": ["utilize", "employ", "apply", "implement", "leverage"],
            "show": ["demonstrate", "illustrate", "reveal", "display", "present"],
            "good": ["excellent", "effective", "beneficial", "valuable", "advantageous"],
            "many": ["numerous", "various", "multiple", "several", "diverse"],
            "need": ["require", "demand", "necessitate", "call for", "depend on"]
        }
        
        varied_content = content
        for word, alternatives in synonyms.items():
            if word in varied_content.lower():
                replacement = random.choice(alternatives)
                # Replace with proper case
                varied_content = re.sub(
                    r'\b' + word + r'\b',
                    replacement,
                    varied_content,
                    flags=re.IGNORECASE
                )
        
        return varied_content

    def add_unique_sections(self, content: str, keyword: str, variation_idx: int) -> str:
        """Add unique sections to make content substantially different"""
        unique_sections = []
        
        # Add industry-specific insights
        if variation_idx % 2 == 0:
            unique_sections.append(f"""
## Industry Insights: {keyword}

Based on recent market analysis, {keyword} has shown significant growth in the following sectors:
- Technology: 45% adoption rate
- Healthcare: 38% implementation
- Finance: 52% efficiency improvement
- Retail: 41% customer satisfaction increase

These statistics highlight the importance of understanding {keyword} in today's market.
""")
        
        # Add FAQ section
        if variation_idx % 3 == 0:
            unique_sections.append(f"""
## Frequently Asked Questions about {keyword}

**Q: How long does it take to implement {keyword}?**
A: Implementation typically takes 2-4 weeks depending on your specific requirements and scale.

**Q: What are the main challenges with {keyword}?**
A: The primary challenges include initial setup complexity, training requirements, and integration with existing systems.

**Q: Is {keyword} suitable for small businesses?**
A: Yes, {keyword} can be scaled to fit businesses of all sizes with appropriate customization.
""")
        
        # Add case study
        if variation_idx % 4 == 0:
            unique_sections.append(f"""
## Case Study: {keyword} Success Story

A recent implementation of {keyword} at TechCorp resulted in:
- 35% increase in operational efficiency
- $2.5M in cost savings over 12 months
- 89% user satisfaction rate
- 50% reduction in processing time

This demonstrates the real-world impact of properly implementing {keyword}.
""")
        
        # Insert unique sections at appropriate points
        for section in unique_sections:
            # Find a good insertion point (after a paragraph break)
            paragraphs = content.split('\n\n')
            insert_pos = random.randint(len(paragraphs)//2, len(paragraphs)-1)
            paragraphs.insert(insert_pos, section)
            content = '\n\n'.join(paragraphs)
        
        return content

    def add_contextual_content(self, content: str, keyword: str) -> str:
        """Add location, time, or industry-specific context"""
        contextual_additions = []
        
        # Add temporal context
        current_year = 2024
        contextual_additions.append(
            f"As of {current_year}, {keyword} has evolved significantly with new developments in AI and automation."
        )
        
        # Add geographic context if applicable
        if any(loc in keyword.lower() for loc in ["near me", "local", "in"]):
            contextual_additions.append(
                f"When searching for {keyword}, it's important to consider local regulations and market conditions."
            )
        
        # Add industry context
        industries = ["healthcare", "finance", "retail", "technology", "manufacturing"]
        selected_industry = random.choice(industries)
        contextual_additions.append(
            f"In the {selected_industry} sector, {keyword} plays a particularly important role in driving innovation."
        )
        
        # Insert contextual content
        for addition in contextual_additions:
            paragraphs = content.split('\n\n')
            if len(paragraphs) > 2:
                insert_pos = random.randint(1, len(paragraphs)-1)
                paragraphs[insert_pos] = paragraphs[insert_pos] + " " + addition
                content = '\n\n'.join(paragraphs)
        
        return content

    def get_variation_type(self, index: int) -> str:
        """Determine variation type based on index"""
        types = ["comprehensive", "detailed", "expert", "beginner-friendly", "technical", "practical"]
        return types[index % len(types)]

    def calculate_uniqueness_score(self, content1: str, content2: str) -> float:
        """Calculate uniqueness score between two pieces of content"""
        # Simple word-based comparison
        words1 = set(content1.lower().split())
        words2 = set(content2.lower().split())
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        # Jaccard similarity
        similarity = len(intersection) / len(union) if union else 0
        uniqueness = 1 - similarity
        
        return uniqueness * 100  # Return as percentage

# Quality enhancement functions
def generate_internal_links(current_keyword: str, all_keywords: List[str], cluster_info: Dict = None) -> List[Dict[str, str]]:
    """Generate intelligent internal links based on keyword relationships"""
    internal_links = []
    
    # Clean current keyword for comparison
    current_words = set(current_keyword.lower().split())
    
    # Find related keywords
    for keyword in all_keywords:
        if keyword.lower() == current_keyword.lower():
            continue
            
        keyword_words = set(keyword.lower().split())
        
        # Calculate relevance score
        common_words = current_words.intersection(keyword_words)
        relevance_score = len(common_words) / max(len(current_words), len(keyword_words))
        
        # Determine link context
        link_context = "related"
        anchor_text = keyword
        
        # Smart anchor text generation
        if "vs" in current_keyword.lower() and "vs" not in keyword.lower():
            # Comparison article linking to individual topics
            anchor_text = f"learn more about {keyword}"
            link_context = "comparison_to_single"
        elif "how to" in current_keyword.lower() and "how to" in keyword.lower():
            # How-to articles linking to other how-tos
            anchor_text = f"similar guide: {keyword}"
            link_context = "similar_guide"
        elif "best" in current_keyword.lower() and keyword.lower() in current_keyword.lower():
            # List article linking to specific item
            anchor_text = f"detailed review of {keyword}"
            link_context = "list_to_item"
        elif relevance_score > 0.3:
            # General related content
            anchor_text = keyword
            link_context = "related_topic"
        
        if relevance_score > 0.2 or (cluster_info and cluster_info.get('same_cluster')):
            internal_links.append({
                'keyword': keyword,
                'anchor_text': anchor_text,
                'url': f"/guides/{keyword.lower().replace(' ', '-')}",
                'relevance': relevance_score,
                'context': link_context
            })
    
    # Sort by relevance and limit
    internal_links.sort(key=lambda x: x['relevance'], reverse=True)
    return internal_links[:8]  # Return top 8 most relevant links

def insert_contextual_links(content: str, internal_links: List[Dict[str, str]], keyword: str) -> str:
    """Insert internal links naturally within the content"""
    linked_content = content
    links_inserted = 0
    max_links = 5  # Maximum contextual links in body content
    
    # Track which keywords we've already linked to avoid duplicate links
    linked_keywords = set()
    
    for link in internal_links:
        if links_inserted >= max_links:
            break
            
        target_keyword = link['keyword']
        if target_keyword in linked_keywords:
            continue
            
        # Find natural places to insert the link
        # Look for mentions of related concepts
        search_terms = target_keyword.lower().split()
        
        for term in search_terms:
            if len(term) > 3 and term in linked_content.lower() and target_keyword not in linked_keywords:
                # Find the exact position (case-insensitive)
                import re
                pattern = r'\b' + re.escape(term) + r'\b'
                match = re.search(pattern, linked_content, re.IGNORECASE)
                
                if match:
                    # Create the link
                    link_html = f'<a href="{link["url"]}" title="{target_keyword}">{match.group()}</a>'
                    
                    # Replace only the first occurrence
                    linked_content = linked_content[:match.start()] + link_html + linked_content[match.end():]
                    
                    linked_keywords.add(target_keyword)
                    links_inserted += 1
                    break
    
    return linked_content

def enhance_content_quality(content: str, keyword: str, business_info: Dict, 
                          all_keywords: List[str] = None, cluster_keywords: List[str] = None) -> str:
    """Enhance content quality with internal linking"""
    enhancements = []
    
    # Generate internal links
    internal_links = []
    if all_keywords:
        cluster_info = {'same_cluster': True} if cluster_keywords else None
        internal_links = generate_internal_links(keyword, all_keywords, cluster_info)
    
    # Insert contextual links within content
    if internal_links:
        content = insert_contextual_links(content, internal_links[:5], keyword)
    
    # Add schema markup suggestions
    enhancements.append("""
<!-- Schema Markup Suggestion -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "{title}",
  "description": "{meta_description}",
  "author": {
    "@type": "Organization",
    "name": "{business_name}"
  },
  "datePublished": "{date}",
  "dateModified": "{date}"
}
</script>
""")
    
    # Add related articles section with remaining links
    if internal_links:
        related_links_html = f"""
## Related {business_info.get('industry', 'Topic')} Guides

Explore these related guides to deepen your understanding:

"""
        # Add cluster-based links first
        cluster_links = [l for l in internal_links if l['context'] == 'same_cluster'][:4]
        if cluster_links:
            related_links_html += "### In This Series:\n"
            for link in cluster_links:
                related_links_html += f"- [{link['anchor_text'].title()}]({link['url']})\n"
            related_links_html += "\n"
        
        # Add other related links
        other_links = [l for l in internal_links if l['context'] != 'same_cluster'][:4]
        if other_links:
            related_links_html += "### Related Topics:\n"
            for link in other_links:
                related_links_html += f"- [{link['anchor_text'].title()}]({link['url']})\n"
        
        enhancements.append(related_links_html)
    
    # Add navigation breadcrumbs
    breadcrumb_html = f"""
<nav class="breadcrumbs">
<a href="/">Home</a> > <a href="/{business_info.get('industry', 'guides').lower()}">{business_info.get('industry', 'Guides')}</a> > {keyword}
</nav>
"""
    
    # Add hub page link if part of a cluster
    if cluster_keywords and len(cluster_keywords) > 5:
        hub_topic = keyword.split()[0] if len(keyword.split()) > 1 else keyword
        enhancements.append(f"""
## Complete {hub_topic.title()} Guide Series

This article is part of our comprehensive {hub_topic} series. 
<a href="/hubs/{hub_topic.lower().replace(' ', '-')}">View all {len(cluster_keywords)} {hub_topic} guides →</a>
""")
    
    # Add "What's Next" section
    if internal_links and len(internal_links) > 2:
        next_steps = internal_links[:3]
        next_html = """
## What to Read Next

Based on this guide, we recommend:

"""
        for i, link in enumerate(next_steps, 1):
            next_html += f"{i}. **[{link['anchor_text'].title()}]({link['url']})** - "
            if 'how to' in link['keyword'].lower():
                next_html += "Step-by-step tutorial\n"
            elif 'best' in link['keyword'].lower():
                next_html += "Top recommendations\n"
            elif 'vs' in link['keyword'].lower():
                next_html += "Detailed comparison\n"
            else:
                next_html += "Essential guide\n"
        
        enhancements.append(next_html)
    
    # Add multimedia suggestions
    enhancements.append("""
## Visual Guide
[Infographic: {keyword} Process Flow]
[Video Tutorial: {keyword} in Action]
[Interactive Demo: Try {keyword} Yourself]
""")
    
    # Add expert credibility
    enhancements.append(f"""
## Expert Insights
"When it comes to {keyword}, the key is understanding your specific needs and implementing 
a solution that scales with your business." - Industry Expert

Our team at {business_info.get('name', 'Our Company')} has helped over 500 businesses 
implement effective {keyword} strategies.
""")
    
    # Combine enhancements with original content
    enhanced_content = content
    for enhancement in enhancements:
        enhanced_content += "\n\n" + enhancement
    
    return enhanced_content

def ensure_minimum_quality(content: str, keyword: str) -> Dict[str, Any]:
    """Ensure content meets minimum quality standards"""
    word_count = len(content.split())
    
    quality_checks = {
        "word_count": word_count,
        "meets_minimum": word_count >= 800,
        "has_headers": "##" in content or "#" in content,
        "has_lists": "-" in content or "1." in content,
        "has_paragraphs": len(content.split('\n\n')) > 3,
        "keyword_density": content.lower().count(keyword.lower()) / word_count * 100,
        "readability_elements": {
            "short_sentences": len([s for s in content.split('.') if len(s.split()) < 20]) > 5,
            "bullet_points": content.count('\n-') > 2,
            "subheadings": content.count('\n##') > 2
        }
    }
    
    quality_checks["quality_score"] = sum([
        quality_checks["meets_minimum"] * 25,
        quality_checks["has_headers"] * 20,
        quality_checks["has_lists"] * 15,
        quality_checks["has_paragraphs"] * 20,
        (2 < quality_checks["keyword_density"] < 5) * 20
    ])
    
    return quality_checks