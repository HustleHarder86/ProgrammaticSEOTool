"""Enhanced Content Variation System with Advanced Pattern Detection"""

import random
import re
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import hashlib
from collections import defaultdict
import json
from pathlib import Path

from prompt_rotation_engine import get_rotation_engine
from config.prompt_manager import get_prompt_manager


class ContentVariationEnhanced:
    """Advanced content variation system to maximize uniqueness at scale"""
    
    def __init__(self):
        self.rotation_engine = get_rotation_engine()
        self.prompt_manager = get_prompt_manager()
        
        # Variation templates for different content elements
        self.variation_templates = {
            "openings": {
                "question": [
                    "Are you wondering {question}?",
                    "Have you ever asked yourself {question}?",
                    "Is it true that {statement}?",
                    "Curious about {topic}?",
                    "Want to know {question}?"
                ],
                "statement": [
                    "When it comes to {topic}, {fact}.",
                    "The truth about {topic} is {fact}.",
                    "Here's what you need to know about {topic}.",
                    "Let's dive into {topic}.",
                    "{topic} has become increasingly important."
                ],
                "data": [
                    "According to recent data, {statistic}.",
                    "Studies show that {statistic}.",
                    "The numbers tell us {statistic}.",
                    "Research indicates {statistic}.",
                    "Data reveals that {statistic}."
                ]
            },
            "transitions": {
                "addition": ["Furthermore", "Additionally", "Moreover", "Also", "Plus"],
                "contrast": ["However", "On the other hand", "Nevertheless", "Yet", "Still"],
                "cause": ["Therefore", "As a result", "Consequently", "Thus", "Hence"],
                "example": ["For instance", "For example", "Such as", "Like", "Including"]
            },
            "closings": {
                "action": [
                    "Ready to get started? {cta}",
                    "Take the next step by {action}.",
                    "Start your journey today.",
                    "Don't wait - {action} now.",
                    "Make it happen by {action}."
                ],
                "summary": [
                    "In summary, {key_point}.",
                    "The bottom line: {key_point}.",
                    "To wrap up, {key_point}.",
                    "All things considered, {key_point}.",
                    "The key takeaway is {key_point}."
                ],
                "question": [
                    "What will you do next?",
                    "Ready to make a change?",
                    "Isn't it time to {action}?",
                    "Why wait any longer?",
                    "What's stopping you?"
                ]
            }
        }
        
        # Synonym banks for common terms
        self.synonym_banks = {
            "important": ["crucial", "essential", "vital", "significant", "key"],
            "good": ["excellent", "great", "superior", "outstanding", "exceptional"],
            "help": ["assist", "support", "aid", "facilitate", "enable"],
            "show": ["demonstrate", "reveal", "indicate", "display", "present"],
            "increase": ["boost", "enhance", "improve", "expand", "grow"]
        }
        
        # Pattern avoidance cache
        self.used_patterns = defaultdict(set)
        self.pattern_history_file = Path("content_patterns_history.json")
        self._load_pattern_history()
    
    def _load_pattern_history(self):
        """Load pattern usage history"""
        if self.pattern_history_file.exists():
            try:
                with open(self.pattern_history_file, 'r') as f:
                    data = json.load(f)
                    self.used_patterns = defaultdict(set, 
                        {k: set(v) for k, v in data.items()})
            except:
                pass
    
    def _save_pattern_history(self):
        """Save pattern usage history"""
        try:
            data = {k: list(v) for k, v in self.used_patterns.items()}
            with open(self.pattern_history_file, 'w') as f:
                json.dump(data, f, indent=2)
        except:
            pass
    
    def create_varied_content(self,
                            base_content: str,
                            content_type: str,
                            variables: Dict[str, str],
                            variation_index: int = 0,
                            total_variations: int = 1) -> Tuple[str, Dict[str, Any]]:
        """Create varied content with advanced pattern avoidance
        
        Args:
            base_content: Base content to vary
            content_type: Type of content for context
            variables: Variables for substitution
            variation_index: Current variation number
            total_variations: Total variations being generated
            
        Returns:
            Tuple of (varied_content, variation_metadata)
        """
        # Select variation strategy
        strategy = self._select_variation_strategy(total_variations)
        
        # Apply variations in sequence
        varied_content = base_content
        variation_metadata = {
            "strategy": strategy,
            "variations_applied": []
        }
        
        # 1. Vary opening
        varied_content, opening_meta = self._vary_opening(
            varied_content, content_type, variables
        )
        variation_metadata["variations_applied"].append(opening_meta)
        
        # 2. Vary transitions
        varied_content, transition_meta = self._vary_transitions(
            varied_content, variation_index
        )
        variation_metadata["variations_applied"].append(transition_meta)
        
        # 3. Apply synonym variations
        varied_content, synonym_meta = self._apply_synonym_variations(
            varied_content, variation_index, total_variations
        )
        variation_metadata["variations_applied"].append(synonym_meta)
        
        # 4. Vary sentence structures
        varied_content, structure_meta = self._vary_sentence_structures(
            varied_content, content_type
        )
        variation_metadata["variations_applied"].append(structure_meta)
        
        # 5. Vary closing
        varied_content, closing_meta = self._vary_closing(
            varied_content, content_type, variables
        )
        variation_metadata["variations_applied"].append(closing_meta)
        
        # 6. Apply final uniqueness pass
        varied_content = self._ensure_uniqueness(
            varied_content, content_type, variation_index
        )
        
        # Record patterns for future avoidance
        self._record_content_patterns(varied_content, content_type)
        
        return varied_content, variation_metadata
    
    def _select_variation_strategy(self, total_variations: int) -> str:
        """Select appropriate variation strategy based on scale"""
        if total_variations < 10:
            return "light"  # Minor variations only
        elif total_variations < 100:
            return "moderate"  # Balanced variations
        elif total_variations < 1000:
            return "heavy"  # Significant variations
        else:
            return "extreme"  # Maximum variation
    
    def _vary_opening(self, content: str, content_type: str, variables: Dict) -> Tuple[str, Dict]:
        """Vary the opening of the content"""
        lines = content.split('\n')
        if not lines:
            return content, {"type": "opening", "changed": False}
        
        # Determine opening type
        first_line = lines[0].strip()
        opening_type = self._determine_opening_type(first_line)
        
        # Get varied opening
        templates = self.variation_templates["openings"].get(opening_type, [])
        if templates:
            # Use rotation engine to select template
            template, _ = self.rotation_engine.select_prompt_variation(
                f"opening_{opening_type}",
                templates,
                strategy="weighted_random"
            )
            
            # Create varied opening
            varied_opening = self._apply_template(template, first_line, variables)
            lines[0] = varied_opening
            
            return '\n'.join(lines), {
                "type": "opening",
                "changed": True,
                "original": first_line,
                "varied": varied_opening
            }
        
        return content, {"type": "opening", "changed": False}
    
    def _determine_opening_type(self, opening: str) -> str:
        """Determine the type of opening"""
        if opening.endswith('?'):
            return "question"
        elif any(char.isdigit() for char in opening):
            return "data"
        else:
            return "statement"
    
    def _vary_transitions(self, content: str, variation_index: int) -> Tuple[str, Dict]:
        """Vary transition words and phrases"""
        transitions_changed = 0
        
        for trans_type, options in self.variation_templates["transitions"].items():
            for transition in options:
                if transition in content:
                    # Select replacement
                    replacement, _ = self.rotation_engine.select_prompt_variation(
                        f"transition_{trans_type}",
                        [opt for opt in options if opt != transition],
                        strategy="least_used"
                    )
                    
                    if replacement:
                        content = content.replace(transition, replacement, 1)
                        transitions_changed += 1
        
        return content, {
            "type": "transitions",
            "changed": transitions_changed > 0,
            "count": transitions_changed
        }
    
    def _apply_synonym_variations(self, content: str, index: int, total: int) -> Tuple[str, Dict]:
        """Apply synonym replacements based on variation needs"""
        # Calculate how many synonyms to replace
        replacement_rate = min(0.3, index / max(total, 1))  # Up to 30% of synonymable words
        words_replaced = 0
        
        for word, synonyms in self.synonym_banks.items():
            if word in content.lower() and random.random() < replacement_rate:
                # Select synonym using rotation
                synonym, _ = self.rotation_engine.select_prompt_variation(
                    f"synonym_{word}",
                    synonyms,
                    strategy="weighted_random"
                )
                
                # Replace with proper case matching
                content = self._replace_with_case_matching(content, word, synonym)
                words_replaced += 1
        
        return content, {
            "type": "synonyms",
            "changed": words_replaced > 0,
            "count": words_replaced,
            "rate": replacement_rate
        }
    
    def _replace_with_case_matching(self, content: str, original: str, replacement: str) -> str:
        """Replace word matching the case of the original"""
        # Handle different case scenarios
        if original.capitalize() in content:
            content = content.replace(original.capitalize(), replacement.capitalize())
        if original.upper() in content:
            content = content.replace(original.upper(), replacement.upper())
        if original.lower() in content:
            content = content.replace(original.lower(), replacement.lower())
        
        return content
    
    def _vary_sentence_structures(self, content: str, content_type: str) -> Tuple[str, Dict]:
        """Vary sentence structures for diversity"""
        sentences = re.split(r'(?<=[.!?])\s+', content)
        structures_changed = 0
        
        # Vary every 3rd sentence structure
        for i in range(2, len(sentences), 3):
            if i < len(sentences):
                original = sentences[i]
                varied = self._restructure_sentence(original)
                if varied != original:
                    sentences[i] = varied
                    structures_changed += 1
        
        return ' '.join(sentences), {
            "type": "structures",
            "changed": structures_changed > 0,
            "count": structures_changed
        }
    
    def _restructure_sentence(self, sentence: str) -> str:
        """Restructure a sentence for variety"""
        # Simple restructuring examples
        if ", but" in sentence:
            parts = sentence.split(", but")
            if len(parts) == 2:
                return f"While {parts[1].strip()}, {parts[0].strip()}"
        
        if sentence.startswith("This "):
            return sentence.replace("This ", "It ", 1)
        
        if sentence.startswith("The "):
            # Sometimes start with dependent clause
            if ", " in sentence:
                parts = sentence.split(", ", 1)
                if len(parts) == 2:
                    return f"{parts[1]}, {parts[0]}"
        
        return sentence
    
    def _vary_closing(self, content: str, content_type: str, variables: Dict) -> Tuple[str, Dict]:
        """Vary the closing of the content"""
        lines = content.split('\n')
        if not lines:
            return content, {"type": "closing", "changed": False}
        
        # Find last substantial line
        last_line_index = -1
        for i in range(len(lines) - 1, -1, -1):
            if lines[i].strip() and len(lines[i].strip()) > 20:
                last_line_index = i
                break
        
        if last_line_index == -1:
            return content, {"type": "closing", "changed": False}
        
        # Determine closing type
        last_line = lines[last_line_index]
        closing_type = self._determine_closing_type(last_line)
        
        # Get varied closing
        templates = self.variation_templates["closings"].get(closing_type, [])
        if templates:
            template, _ = self.rotation_engine.select_prompt_variation(
                f"closing_{closing_type}",
                templates,
                strategy="least_used"
            )
            
            # Apply template
            varied_closing = self._apply_template(template, last_line, variables)
            lines[last_line_index] = varied_closing
            
            return '\n'.join(lines), {
                "type": "closing",
                "changed": True,
                "original": last_line,
                "varied": varied_closing
            }
        
        return content, {"type": "closing", "changed": False}
    
    def _determine_closing_type(self, closing: str) -> str:
        """Determine the type of closing"""
        if closing.endswith('?'):
            return "question"
        elif any(word in closing.lower() for word in ["start", "begin", "try", "get"]):
            return "action"
        else:
            return "summary"
    
    def _apply_template(self, template: str, original: str, variables: Dict) -> str:
        """Apply a template with smart substitution"""
        # Extract key information from original
        result = template
        
        # Simple placeholder replacement
        if "{question}" in template:
            # Extract question from original
            question_match = re.search(r'([^.?!]+\?)', original)
            if question_match:
                result = result.replace("{question}", question_match.group(1).lower())
        
        if "{topic}" in template:
            # Use main variable as topic
            topic = next(iter(variables.values()), "this topic")
            result = result.replace("{topic}", topic)
        
        if "{statement}" in template or "{fact}" in template:
            # Use cleaned original as statement
            statement = original.rstrip('.!?')
            result = result.replace("{statement}", statement)
            result = result.replace("{fact}", statement)
        
        # Add more sophisticated replacements as needed
        return result
    
    def _ensure_uniqueness(self, content: str, content_type: str, index: int) -> str:
        """Final pass to ensure content uniqueness"""
        # Generate content hash
        content_hash = hashlib.md5(content.encode()).hexdigest()[:8]
        
        # Check if we've seen similar content
        pattern_key = f"{content_type}:{content_hash[:4]}"
        if pattern_key in self.used_patterns:
            # Apply additional variation
            content = self._apply_micro_variations(content, index)
        
        return content
    
    def _apply_micro_variations(self, content: str, index: int) -> str:
        """Apply micro-variations for additional uniqueness"""
        micro_variations = [
            (" is ", " remains "),
            (" are ", " remain "),
            (" will ", " would "),
            (" can ", " could "),
            ("In fact, ", "Indeed, "),
            ("Actually, ", "In reality, ")
        ]
        
        # Apply 1-2 micro variations based on index
        num_variations = 1 + (index % 2)
        applied = 0
        
        for original, replacement in random.sample(micro_variations, len(micro_variations)):
            if original in content and applied < num_variations:
                content = content.replace(original, replacement, 1)
                applied += 1
        
        return content
    
    def _record_content_patterns(self, content: str, content_type: str):
        """Record content patterns for future avoidance"""
        # Extract and record patterns
        patterns = self.rotation_engine.detect_content_patterns(content)
        
        # Store pattern hashes
        for pattern_type, pattern_list in patterns.items():
            for pattern in pattern_list:
                pattern_hash = hashlib.md5(pattern.encode()).hexdigest()[:8]
                self.used_patterns[f"{content_type}:{pattern_type}"].add(pattern_hash)
        
        # Save periodically
        if sum(len(v) for v in self.used_patterns.values()) % 100 == 0:
            self._save_pattern_history()
    
    def get_variation_stats(self) -> Dict[str, Any]:
        """Get statistics about content variations"""
        return {
            "total_patterns_tracked": sum(len(v) for v in self.used_patterns.values()),
            "pattern_types": list(self.used_patterns.keys()),
            "rotation_report": self.rotation_engine.get_variation_report(),
            "synonym_usage": self._get_synonym_usage_stats()
        }
    
    def _get_synonym_usage_stats(self) -> Dict[str, int]:
        """Get synonym usage statistics"""
        stats = {}
        for word, synonyms in self.synonym_banks.items():
            usage_count = 0
            for synonym in synonyms:
                key = f"synonym_{word}:{synonym}"
                usage_count += self.rotation_engine.history["usage_counts"].get(key, 0)
            stats[word] = usage_count
        return stats