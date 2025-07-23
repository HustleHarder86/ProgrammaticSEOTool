"""Advanced Prompt Rotation Engine for content variety and duplication avoidance"""

import json
import random
import hashlib
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from collections import defaultdict, Counter
import re
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class PromptRotationEngine:
    """Sophisticated prompt rotation system with multiple strategies"""
    
    def __init__(self, history_file: str = "prompt_history.json"):
        self.history_file = Path(history_file)
        self.rotation_strategies = {
            "sequential": self._sequential_rotation,
            "weighted_random": self._weighted_random_rotation,
            "least_used": self._least_used_rotation,
            "performance_based": self._performance_based_rotation,
            "time_based": self._time_based_rotation
        }
        self.history = self._load_history()
        self.performance_metrics = defaultdict(lambda: {"success": 0, "total": 0})
        self.pattern_cache = {}
        
    def _load_history(self) -> Dict[str, Any]:
        """Load prompt usage history from file"""
        if self.history_file.exists():
            try:
                with open(self.history_file, 'r') as f:
                    return json.load(f)
            except:
                return self._create_empty_history()
        return self._create_empty_history()
    
    def _create_empty_history(self) -> Dict[str, Any]:
        """Create empty history structure"""
        return {
            "usage_counts": defaultdict(int),
            "last_used": {},
            "performance": defaultdict(dict),
            "ab_tests": {},
            "pattern_frequency": defaultdict(int)
        }
    
    def _save_history(self):
        """Save history to file"""
        try:
            # Convert defaultdicts to regular dicts for JSON serialization
            history_data = {
                "usage_counts": dict(self.history["usage_counts"]),
                "last_used": self.history["last_used"],
                "performance": dict(self.history["performance"]),
                "ab_tests": self.history["ab_tests"],
                "pattern_frequency": dict(self.history["pattern_frequency"])
            }
            with open(self.history_file, 'w') as f:
                json.dump(history_data, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save history: {e}")
    
    def get_rotation_config(self) -> Dict[str, Any]:
        """Get rotation configuration with strategies and weights"""
        return {
            "strategies": {
                "sequential": {
                    "description": "Rotate through options in order",
                    "weight": 0.2
                },
                "weighted_random": {
                    "description": "Random selection with usage weighting",
                    "weight": 0.3
                },
                "least_used": {
                    "description": "Prefer least frequently used options",
                    "weight": 0.3
                },
                "performance_based": {
                    "description": "Select based on past performance",
                    "weight": 0.1
                },
                "time_based": {
                    "description": "Rotate based on time intervals",
                    "weight": 0.1
                }
            },
            "variation_factors": {
                "tone": ["professional", "conversational", "expert", "friendly"],
                "structure": ["question-first", "data-first", "story-first", "fact-first"],
                "length_preference": ["concise", "detailed", "balanced"],
                "emphasis": ["benefits", "features", "data", "comparison"]
            }
        }
    
    def select_prompt_variation(self,
                              prompt_type: str,
                              available_variations: List[str],
                              strategy: str = "auto",
                              context: Dict[str, Any] = None) -> Tuple[str, Dict[str, Any]]:
        """Select a prompt variation using specified or automatic strategy
        
        Args:
            prompt_type: Type of prompt (e.g., 'content_generation/evaluation')
            available_variations: List of available variations
            strategy: Rotation strategy to use or 'auto' for automatic selection
            context: Additional context for selection (e.g., target audience)
            
        Returns:
            Tuple of (selected_variation, metadata)
        """
        if not available_variations:
            return None, {"strategy": "none", "reason": "no_variations"}
        
        # Auto-select strategy based on context and history
        if strategy == "auto":
            strategy = self._select_best_strategy(prompt_type, len(available_variations))
        
        # Apply selected strategy
        if strategy in self.rotation_strategies:
            selected = self.rotation_strategies[strategy](
                prompt_type, available_variations, context
            )
        else:
            selected = random.choice(available_variations)
        
        # Record usage
        self._record_usage(prompt_type, selected, strategy)
        
        # Generate metadata
        metadata = {
            "strategy": strategy,
            "timestamp": datetime.now().isoformat(),
            "usage_count": self.history["usage_counts"].get(f"{prompt_type}:{selected}", 0),
            "alternatives": len(available_variations)
        }
        
        return selected, metadata
    
    def _select_best_strategy(self, prompt_type: str, num_variations: int) -> str:
        """Automatically select the best rotation strategy"""
        # Use performance-based if we have enough data
        type_usage = sum(1 for k in self.history["usage_counts"] if k.startswith(prompt_type))
        if type_usage > num_variations * 3:  # Each variation used at least 3 times
            return "performance_based"
        
        # Use least_used for better distribution early on
        if type_usage < num_variations * 2:
            return "least_used"
        
        # Otherwise use weighted random
        return "weighted_random"
    
    def _sequential_rotation(self, prompt_type: str, variations: List[str], context: Dict) -> str:
        """Rotate through variations sequentially"""
        # Get last used index
        last_key = f"{prompt_type}:last_index"
        last_index = self.history.get("last_index", {}).get(last_key, -1)
        
        # Move to next index
        next_index = (last_index + 1) % len(variations)
        
        # Store for next time
        if "last_index" not in self.history:
            self.history["last_index"] = {}
        self.history["last_index"][last_key] = next_index
        
        return variations[next_index]
    
    def _weighted_random_rotation(self, prompt_type: str, variations: List[str], context: Dict) -> str:
        """Random selection weighted by inverse usage frequency"""
        # Calculate weights based on usage
        weights = []
        for var in variations:
            usage_key = f"{prompt_type}:{var}"
            usage_count = self.history["usage_counts"].get(usage_key, 0)
            # Inverse weight: less used = higher weight
            weight = 1.0 / (usage_count + 1)
            weights.append(weight)
        
        # Normalize weights
        total_weight = sum(weights)
        weights = [w / total_weight for w in weights]
        
        # Weighted random selection
        return random.choices(variations, weights=weights)[0]
    
    def _least_used_rotation(self, prompt_type: str, variations: List[str], context: Dict) -> str:
        """Select the least frequently used variation"""
        usage_counts = []
        for var in variations:
            usage_key = f"{prompt_type}:{var}"
            count = self.history["usage_counts"].get(usage_key, 0)
            usage_counts.append((count, var))
        
        # Sort by usage count and select least used
        usage_counts.sort(key=lambda x: x[0])
        
        # If multiple have same lowest count, randomly select among them
        min_count = usage_counts[0][0]
        least_used = [var for count, var in usage_counts if count == min_count]
        
        return random.choice(least_used)
    
    def _performance_based_rotation(self, prompt_type: str, variations: List[str], context: Dict) -> str:
        """Select based on past performance metrics"""
        performance_scores = []
        
        for var in variations:
            key = f"{prompt_type}:{var}"
            metrics = self.history["performance"].get(key, {"success": 0, "total": 0})
            
            if metrics["total"] > 0:
                success_rate = metrics["success"] / metrics["total"]
                # Add exploration bonus for less-tested variations
                exploration_bonus = 1.0 / (metrics["total"] + 1)
                score = success_rate + 0.1 * exploration_bonus
            else:
                # High score for untested variations to ensure exploration
                score = 1.0
            
            performance_scores.append((score, var))
        
        # Sort by score and select best
        performance_scores.sort(key=lambda x: x[0], reverse=True)
        
        # Add some randomness to top performers
        top_performers = [var for score, var in performance_scores[:3]]
        return random.choice(top_performers)
    
    def _time_based_rotation(self, prompt_type: str, variations: List[str], context: Dict) -> str:
        """Rotate based on time intervals"""
        current_time = datetime.now()
        time_window = timedelta(hours=1)  # Rotate every hour
        
        # Check last used times
        available = []
        for var in variations:
            key = f"{prompt_type}:{var}"
            last_used_str = self.history["last_used"].get(key)
            
            if last_used_str:
                last_used = datetime.fromisoformat(last_used_str)
                if current_time - last_used > time_window:
                    available.append(var)
            else:
                available.append(var)
        
        # If all were used recently, reset and use least recent
        if not available:
            return self._least_recent_variation(prompt_type, variations)
        
        return random.choice(available)
    
    def _least_recent_variation(self, prompt_type: str, variations: List[str]) -> str:
        """Select the least recently used variation"""
        usage_times = []
        
        for var in variations:
            key = f"{prompt_type}:{var}"
            last_used_str = self.history["last_used"].get(key)
            
            if last_used_str:
                last_used = datetime.fromisoformat(last_used_str)
                usage_times.append((last_used, var))
            else:
                # Never used - highest priority
                return var
        
        # Sort by time and return oldest
        usage_times.sort(key=lambda x: x[0])
        return usage_times[0][1]
    
    def _record_usage(self, prompt_type: str, variation: str, strategy: str):
        """Record usage of a prompt variation"""
        key = f"{prompt_type}:{variation}"
        
        # Update usage count
        self.history["usage_counts"][key] = self.history["usage_counts"].get(key, 0) + 1
        
        # Update last used time
        self.history["last_used"][key] = datetime.now().isoformat()
        
        # Save periodically (every 10 uses)
        total_uses = sum(self.history["usage_counts"].values())
        if total_uses % 10 == 0:
            self._save_history()
    
    def record_performance(self, prompt_type: str, variation: str, success: bool, metadata: Dict = None):
        """Record performance metrics for a prompt variation
        
        Args:
            prompt_type: Type of prompt
            variation: The variation used
            success: Whether the generation was successful
            metadata: Additional performance metadata (e.g., quality score)
        """
        key = f"{prompt_type}:{variation}"
        
        if key not in self.history["performance"]:
            self.history["performance"][key] = {"success": 0, "total": 0}
        
        self.history["performance"][key]["total"] += 1
        if success:
            self.history["performance"][key]["success"] += 1
        
        # Store additional metadata if provided
        if metadata:
            if "metadata" not in self.history["performance"][key]:
                self.history["performance"][key]["metadata"] = []
            self.history["performance"][key]["metadata"].append({
                "timestamp": datetime.now().isoformat(),
                **metadata
            })
        
        self._save_history()
    
    def detect_content_patterns(self, content: str) -> Dict[str, Any]:
        """Detect patterns in generated content to avoid repetition
        
        Args:
            content: Generated content to analyze
            
        Returns:
            Dictionary of detected patterns and their frequencies
        """
        patterns = {
            "opening_phrases": self._extract_opening_phrases(content),
            "closing_phrases": self._extract_closing_phrases(content),
            "transition_words": self._extract_transition_words(content),
            "sentence_structures": self._analyze_sentence_structures(content)
        }
        
        # Update pattern frequency history
        for pattern_type, pattern_list in patterns.items():
            for pattern in pattern_list:
                pattern_key = f"{pattern_type}:{pattern}"
                self.history["pattern_frequency"][pattern_key] = \
                    self.history["pattern_frequency"].get(pattern_key, 0) + 1
        
        return patterns
    
    def _extract_opening_phrases(self, content: str) -> List[str]:
        """Extract opening phrases from content"""
        sentences = content.split('.')
        if sentences:
            first_sentence = sentences[0].strip()
            # Extract first 5-7 words as opening phrase
            words = first_sentence.split()[:7]
            return [' '.join(words)] if words else []
        return []
    
    def _extract_closing_phrases(self, content: str) -> List[str]:
        """Extract closing phrases from content"""
        sentences = [s.strip() for s in content.split('.') if s.strip()]
        if sentences:
            last_sentence = sentences[-1]
            # Extract last 5-7 words as closing phrase
            words = last_sentence.split()[-7:]
            return [' '.join(words)] if words else []
        return []
    
    def _extract_transition_words(self, content: str) -> List[str]:
        """Extract transition words and phrases"""
        transitions = [
            "however", "therefore", "moreover", "furthermore",
            "in addition", "on the other hand", "as a result",
            "consequently", "nevertheless", "in conclusion"
        ]
        found = []
        content_lower = content.lower()
        for transition in transitions:
            if transition in content_lower:
                found.append(transition)
        return found
    
    def _analyze_sentence_structures(self, content: str) -> List[str]:
        """Analyze sentence structure patterns"""
        sentences = [s.strip() for s in content.split('.') if s.strip()]
        structures = []
        
        for sentence in sentences[:3]:  # Analyze first 3 sentences
            # Simple structure detection
            if sentence.startswith(("Is", "Are", "Do", "Does", "Can", "Will")):
                structures.append("question")
            elif " because " in sentence or " since " in sentence:
                structures.append("causal")
            elif " and " in sentence or " but " in sentence:
                structures.append("compound")
            else:
                structures.append("simple")
        
        return structures
    
    def get_variation_report(self) -> Dict[str, Any]:
        """Generate a report on prompt variation usage and performance"""
        report = {
            "total_variations_used": len(self.history["usage_counts"]),
            "total_generations": sum(self.history["usage_counts"].values()),
            "most_used": [],
            "least_used": [],
            "best_performing": [],
            "pattern_diversity": self._calculate_pattern_diversity(),
            "recommendations": []
        }
        
        # Find most and least used
        usage_list = [(k, v) for k, v in self.history["usage_counts"].items()]
        usage_list.sort(key=lambda x: x[1], reverse=True)
        
        report["most_used"] = usage_list[:5]
        report["least_used"] = usage_list[-5:]
        
        # Find best performing
        performance_list = []
        for key, metrics in self.history["performance"].items():
            if metrics["total"] > 0:
                success_rate = metrics["success"] / metrics["total"]
                performance_list.append((key, success_rate, metrics["total"]))
        
        performance_list.sort(key=lambda x: x[1], reverse=True)
        report["best_performing"] = performance_list[:5]
        
        # Generate recommendations
        if report["pattern_diversity"] < 0.5:
            report["recommendations"].append(
                "Low pattern diversity detected. Consider adding more prompt variations."
            )
        
        return report
    
    def _calculate_pattern_diversity(self) -> float:
        """Calculate diversity score based on pattern usage"""
        if not self.history["pattern_frequency"]:
            return 1.0
        
        # Calculate entropy of pattern distribution
        total = sum(self.history["pattern_frequency"].values())
        if total == 0:
            return 1.0
        
        entropy = 0
        for count in self.history["pattern_frequency"].values():
            if count > 0:
                probability = count / total
                entropy -= probability * (probability ** 0.5)  # Simplified entropy
        
        # Normalize to 0-1 range
        max_entropy = len(self.history["pattern_frequency"]) ** 0.5
        return min(1.0, entropy / max_entropy) if max_entropy > 0 else 1.0


# Singleton instance
_rotation_engine = None


def get_rotation_engine() -> PromptRotationEngine:
    """Get or create the singleton PromptRotationEngine instance"""
    global _rotation_engine
    if _rotation_engine is None:
        _rotation_engine = PromptRotationEngine()
    return _rotation_engine