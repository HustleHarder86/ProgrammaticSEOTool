"""Prompt Manager - Centralized AI prompt management system."""

import json
import os
import random
from typing import Dict, List, Optional, Any
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class PromptManager:
    """Manages AI prompts from configuration files with rotation and variation support."""
    
    def __init__(self, config_path: str = None):
        """Initialize the prompt manager.
        
        Args:
            config_path: Path to prompts configuration file.
                        Defaults to backend/config/prompts_config.json
        """
        if config_path is None:
            config_path = Path(__file__).parent / "prompts_config.json"
        
        self.config_path = Path(config_path)
        self.config = self._load_config()
        self.usage_history = {}  # Track prompt usage for rotation
        
    def _load_config(self) -> Dict[str, Any]:
        """Load prompts configuration from JSON file."""
        try:
            with open(self.config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.error(f"Prompts config not found at {self.config_path}")
            return self._get_default_config()
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in prompts config: {e}")
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Return minimal default configuration as fallback."""
        return {
            "version": "1.0.0",
            "models": {
                "primary": {
                    "provider": "openai",
                    "model": "gpt-3.5-turbo",
                    "temperature": 0.7
                }
            },
            "prompts": {}
        }
    
    def get_prompt(self, 
                   category: str, 
                   prompt_type: str,
                   variables: Dict[str, str] = None,
                   tone: Optional[str] = None,
                   use_rotation: bool = True) -> Dict[str, str]:
        """Get a prompt with variable substitution and optional tone variation.
        
        Args:
            category: Main category (e.g., 'business_analysis', 'content_generation')
            prompt_type: Specific prompt type (e.g., 'url_based', 'evaluation_question')
            variables: Dictionary of variables to substitute in the prompt
            tone: Optional tone variation to apply
            use_rotation: Whether to rotate through variations
            
        Returns:
            Dictionary with 'system' and 'user' prompts
        """
        try:
            # Get base prompt
            prompt_config = self.config["prompts"][category][prompt_type]
            
            # Get system and user prompts
            system_prompt = prompt_config.get("system", "")
            user_prompt = prompt_config.get("user", "")
            
            # Apply tone variation if requested
            if tone and tone in self.config.get("prompt_styles", {}).get("tones", {}):
                tone_modifier = self.config["prompt_styles"]["tones"][tone]["modifiers"]
                user_prompt = f"{user_prompt}\n\n{tone_modifier}"
            
            # Apply rotation if variations exist
            if use_rotation and "variations" in prompt_config:
                variation = self._get_rotation_variation(category, prompt_type, prompt_config["variations"])
                if variation:
                    user_prompt = f"{user_prompt}\n\nStyle: {variation}"
            
            # Substitute variables
            if variables:
                user_prompt = self._substitute_variables(user_prompt, variables)
                system_prompt = self._substitute_variables(system_prompt, variables)
            
            return {
                "system": system_prompt,
                "user": user_prompt
            }
            
        except KeyError as e:
            logger.error(f"Prompt not found: {category}/{prompt_type} - {e}")
            return self._get_fallback_prompt(category, prompt_type)
    
    def _substitute_variables(self, template: str, variables: Dict[str, str]) -> str:
        """Substitute variables in a prompt template.
        
        Args:
            template: The prompt template with {variable} placeholders
            variables: Dictionary of variable names and values
            
        Returns:
            Prompt with variables substituted
        """
        result = template
        for key, value in variables.items():
            result = result.replace(f"{{{key}}}", str(value))
        return result
    
    def _get_rotation_variation(self, category: str, prompt_type: str, variations: List[str]) -> Optional[str]:
        """Get next variation in rotation for prompt variety.
        
        Args:
            category: Prompt category
            prompt_type: Prompt type
            variations: List of available variations
            
        Returns:
            Selected variation or None
        """
        if not variations:
            return None
            
        # Track usage history
        history_key = f"{category}:{prompt_type}"
        if history_key not in self.usage_history:
            self.usage_history[history_key] = []
        
        # Get unused variations
        used = set(self.usage_history[history_key])
        unused = [v for v in variations if v not in used]
        
        # Reset if all variations used
        if not unused:
            self.usage_history[history_key] = []
            unused = variations
        
        # Select random unused variation
        selected = random.choice(unused)
        self.usage_history[history_key].append(selected)
        
        return selected
    
    def _get_fallback_prompt(self, category: str, prompt_type: str) -> Dict[str, str]:
        """Return a generic fallback prompt when specific prompt not found."""
        return {
            "system": "You are a helpful AI assistant.",
            "user": f"Please help with {category} - {prompt_type}."
        }
    
    def get_model_config(self, use_case: str = "primary") -> Dict[str, Any]:
        """Get model configuration for a specific use case.
        
        Args:
            use_case: The use case (e.g., 'primary', 'business_analysis')
            
        Returns:
            Model configuration dictionary
        """
        models = self.config.get("models", {})
        if use_case in models:
            return models[use_case]
        return models.get("primary", {
            "provider": "openai",
            "model": "gpt-3.5-turbo",
            "temperature": 0.7
        })
    
    def list_prompts(self) -> Dict[str, List[str]]:
        """List all available prompts by category.
        
        Returns:
            Dictionary mapping categories to prompt types
        """
        prompts = self.config.get("prompts", {})
        result = {}
        for category, prompt_types in prompts.items():
            result[category] = list(prompt_types.keys())
        return result
    
    def get_tone_options(self) -> List[str]:
        """Get available tone options.
        
        Returns:
            List of available tone names
        """
        return list(self.config.get("prompt_styles", {}).get("tones", {}).keys())
    
    def validate_content(self, content: str, content_type: str = "default") -> Dict[str, Any]:
        """Validate generated content against configured requirements.
        
        Args:
            content: The generated content to validate
            content_type: Type of content for specific validation rules
            
        Returns:
            Validation results with passed status and any issues
        """
        validation = self.config.get("validation", {}).get("content_requirements", {})
        issues = []
        
        # Check word count
        word_count = len(content.split())
        min_words = validation.get("min_word_count", 300)
        max_words = validation.get("max_word_count", 500)
        
        if word_count < min_words:
            issues.append(f"Content too short: {word_count} words (minimum: {min_words})")
        elif word_count > max_words:
            issues.append(f"Content too long: {word_count} words (maximum: {max_words})")
        
        # Check for placeholder text
        placeholders = ["various options", "${variable}", "{variable}", "[placeholder]"]
        for placeholder in placeholders:
            if placeholder.lower() in content.lower():
                issues.append(f"Placeholder text found: {placeholder}")
        
        # Check required elements
        required = validation.get("required_elements", [])
        if "data_points" in required and not any(char.isdigit() for char in content):
            issues.append("No data points or numbers found")
        
        return {
            "passed": len(issues) == 0,
            "word_count": word_count,
            "issues": issues
        }
    
    def reload_config(self):
        """Reload configuration from file."""
        self.config = self._load_config()
        self.usage_history = {}  # Reset usage history
        logger.info("Prompts configuration reloaded")


# Singleton instance
_prompt_manager = None


def get_prompt_manager(config_path: str = None) -> PromptManager:
    """Get or create the singleton PromptManager instance.
    
    Args:
        config_path: Optional path to configuration file
        
    Returns:
        PromptManager instance
    """
    global _prompt_manager
    if _prompt_manager is None:
        _prompt_manager = PromptManager(config_path)
    return _prompt_manager