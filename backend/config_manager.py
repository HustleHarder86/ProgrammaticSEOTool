"""Configuration Manager for centralized app settings"""

import json
import os
from typing import Dict, List, Any, Optional
from pathlib import Path
import logging
from datetime import datetime
import copy

logger = logging.getLogger(__name__)


class ConfigManager:
    """Manages application configuration with validation and hot-reloading"""
    
    def __init__(self, config_path: str = "config.json"):
        self.config_path = Path(config_path)
        self.config = {}
        self.defaults = self._get_defaults()
        self.validators = self._get_validators()
        self.change_listeners = []
        self.last_modified = None
        
        # Load initial configuration
        self.load_config()
        
        # Start file watcher for hot-reloading
        self._start_file_watcher()
    
    def _get_defaults(self) -> Dict[str, Any]:
        """Get default configuration values"""
        return {
            "version": "1.0.0",
            "ai_providers": {
                "primary": {
                    "provider": "openai",
                    "model": "gpt-3.5-turbo",
                    "temperature": 0.7
                }
            },
            "content_generation": {
                "word_count": {
                    "min": 300,
                    "max": 500
                }
            },
            "feature_flags": {}
        }
    
    def _get_validators(self) -> Dict[str, callable]:
        """Get configuration validators"""
        return {
            "ai_providers": self._validate_ai_providers,
            "content_generation": self._validate_content_generation,
            "publishing": self._validate_publishing,
            "automation": self._validate_automation
        }
    
    def load_config(self, merge_with_env: bool = True):
        """Load configuration from file
        
        Args:
            merge_with_env: Whether to merge with environment variables
        """
        try:
            # Load from file
            if self.config_path.exists():
                with open(self.config_path, 'r') as f:
                    self.config = json.load(f)
                self.last_modified = os.path.getmtime(self.config_path)
            else:
                logger.warning(f"Config file not found: {self.config_path}")
                self.config = copy.deepcopy(self.defaults)
            
            # Merge with environment variables if requested
            if merge_with_env:
                self._merge_env_variables()
            
            # Validate configuration
            self._validate_config()
            
            # Notify listeners
            self._notify_change_listeners()
            
            logger.info(f"Configuration loaded successfully (version: {self.config.get('version')})")
            
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in config file: {e}")
            self.config = copy.deepcopy(self.defaults)
        except Exception as e:
            logger.error(f"Error loading config: {e}")
            self.config = copy.deepcopy(self.defaults)
    
    def _merge_env_variables(self):
        """Merge environment variables into configuration"""
        # API Keys
        env_mappings = {
            "OPENAI_API_KEY": "ai_providers.primary.api_key",
            "ANTHROPIC_API_KEY": "ai_providers.fallback.api_key",
            "PERPLEXITY_API_KEY": "ai_providers.business_analysis.api_key",
            "WORDPRESS_APP_PASSWORD": "publishing.wordpress.app_password",
            "WEBFLOW_API_TOKEN": "publishing.webflow.api_token"
        }
        
        for env_var, config_path in env_mappings.items():
            value = os.getenv(env_var)
            if value:
                self._set_nested_value(config_path, value)
    
    def _set_nested_value(self, path: str, value: Any):
        """Set a nested configuration value using dot notation"""
        keys = path.split('.')
        current = self.config
        
        for key in keys[:-1]:
            if key not in current:
                current[key] = {}
            current = current[key]
        
        current[keys[-1]] = value
    
    def _validate_config(self):
        """Validate the entire configuration"""
        errors = []
        
        for section, validator in self.validators.items():
            if section in self.config:
                section_errors = validator(self.config[section])
                errors.extend(section_errors)
        
        if errors:
            logger.warning(f"Configuration validation errors: {errors}")
    
    def _validate_ai_providers(self, providers: Dict[str, Any]) -> List[str]:
        """Validate AI provider configuration"""
        errors = []
        
        for name, provider in providers.items():
            if "provider" not in provider:
                errors.append(f"AI provider '{name}' missing 'provider' field")
            
            if "model" not in provider:
                errors.append(f"AI provider '{name}' missing 'model' field")
            
            # Check temperature range
            temp = provider.get("temperature", 0.7)
            if not 0 <= temp <= 2:
                errors.append(f"AI provider '{name}' temperature out of range: {temp}")
        
        return errors
    
    def _validate_content_generation(self, content: Dict[str, Any]) -> List[str]:
        """Validate content generation settings"""
        errors = []
        
        # Validate word count
        word_count = content.get("word_count", {})
        min_words = word_count.get("min", 300)
        max_words = word_count.get("max", 500)
        
        if min_words > max_words:
            errors.append(f"Min word count ({min_words}) exceeds max ({max_words})")
        
        return errors
    
    def _validate_publishing(self, publishing: Dict[str, Any]) -> List[str]:
        """Validate publishing configuration"""
        errors = []
        
        # Validate WordPress settings
        if publishing.get("wordpress", {}).get("enabled"):
            wp = publishing["wordpress"]
            if not wp.get("api_url"):
                errors.append("WordPress enabled but api_url not set")
        
        # Validate Webflow settings
        if publishing.get("webflow", {}).get("enabled"):
            wf = publishing["webflow"]
            if not wf.get("site_id") or not wf.get("collection_id"):
                errors.append("Webflow enabled but site_id or collection_id not set")
        
        return errors
    
    def _validate_automation(self, automation: Dict[str, Any]) -> List[str]:
        """Validate automation settings"""
        errors = []
        
        # Validate job timeout
        timeout = automation.get("job_timeout", 3600)
        if timeout < 60 or timeout > 86400:
            errors.append(f"Job timeout out of range: {timeout} (should be 60-86400)")
        
        return errors
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value with dot notation support
        
        Args:
            key: Configuration key (supports dot notation)
            default: Default value if key not found
            
        Returns:
            Configuration value or default
        """
        keys = key.split('.')
        current = self.config
        
        for k in keys:
            if isinstance(current, dict) and k in current:
                current = current[k]
            else:
                return default
        
        return current
    
    def set(self, key: str, value: Any, save: bool = True):
        """Set configuration value
        
        Args:
            key: Configuration key (supports dot notation)
            value: Value to set
            save: Whether to save to file immediately
        """
        self._set_nested_value(key, value)
        
        if save:
            self.save_config()
        
        # Notify listeners
        self._notify_change_listeners(key, value)
    
    def save_config(self):
        """Save current configuration to file"""
        try:
            # Create backup
            if self.config_path.exists():
                backup_path = self.config_path.with_suffix('.json.bak')
                self.config_path.rename(backup_path)
            
            # Save new config
            with open(self.config_path, 'w') as f:
                json.dump(self.config, f, indent=2)
            
            self.last_modified = os.path.getmtime(self.config_path)
            logger.info("Configuration saved successfully")
            
        except Exception as e:
            logger.error(f"Error saving config: {e}")
            # Restore backup if exists
            backup_path = self.config_path.with_suffix('.json.bak')
            if backup_path.exists():
                backup_path.rename(self.config_path)
    
    def is_feature_enabled(self, feature: str) -> bool:
        """Check if a feature flag is enabled
        
        Args:
            feature: Feature name
            
        Returns:
            True if feature is enabled
        """
        return self.get(f"feature_flags.{feature}", False)
    
    def get_ai_provider(self, use_case: str = "primary") -> Dict[str, Any]:
        """Get AI provider configuration for use case
        
        Args:
            use_case: Use case (primary, fallback, business_analysis)
            
        Returns:
            AI provider configuration
        """
        provider_config = self.get(f"ai_providers.{use_case}", {})
        
        # Add API key from environment if not in config
        if "api_key" not in provider_config:
            env_key = provider_config.get("api_key_env")
            if env_key:
                provider_config["api_key"] = os.getenv(env_key, "")
        
        return provider_config
    
    def register_change_listener(self, callback: callable):
        """Register a callback for configuration changes
        
        Args:
            callback: Function to call on config change
        """
        self.change_listeners.append(callback)
    
    def _notify_change_listeners(self, key: str = None, value: Any = None):
        """Notify registered listeners of configuration changes"""
        for listener in self.change_listeners:
            try:
                listener(key, value, self.config)
            except Exception as e:
                logger.error(f"Error notifying config listener: {e}")
    
    def _start_file_watcher(self):
        """Start watching config file for changes (hot-reload)"""
        # This would use a file watcher library in production
        # For now, we'll check manually when get() is called
        pass
    
    def check_reload(self):
        """Check if config file has changed and reload if needed"""
        if self.config_path.exists():
            current_modified = os.path.getmtime(self.config_path)
            if self.last_modified and current_modified > self.last_modified:
                logger.info("Configuration file changed, reloading...")
                self.load_config()
    
    def export_config(self, include_sensitive: bool = False) -> Dict[str, Any]:
        """Export configuration for sharing
        
        Args:
            include_sensitive: Whether to include sensitive data
            
        Returns:
            Exportable configuration
        """
        config_copy = copy.deepcopy(self.config)
        
        if not include_sensitive:
            # Remove sensitive fields
            sensitive_paths = [
                "ai_providers.*.api_key",
                "publishing.wordpress.app_password",
                "publishing.webflow.api_token",
                "security.api_keys"
            ]
            
            for path in sensitive_paths:
                self._remove_sensitive_field(config_copy, path)
        
        return config_copy
    
    def _remove_sensitive_field(self, config: Dict[str, Any], path: str):
        """Remove sensitive field from configuration"""
        if "*" in path:
            # Handle wildcards
            parts = path.split(".")
            self._remove_wildcard_field(config, parts)
        else:
            # Direct path
            keys = path.split(".")
            current = config
            
            for key in keys[:-1]:
                if key in current:
                    current = current[key]
                else:
                    return
            
            if keys[-1] in current:
                current[keys[-1]] = "<REDACTED>"
    
    def _remove_wildcard_field(self, config: Dict[str, Any], parts: List[str]):
        """Remove fields matching wildcard pattern"""
        if not parts:
            return
        
        if parts[0] == "*":
            # Wildcard at this level
            for key in config:
                if isinstance(config[key], dict):
                    self._remove_wildcard_field(config[key], parts[1:])
        elif parts[0] in config:
            if len(parts) == 1:
                config[parts[0]] = "<REDACTED>"
            elif isinstance(config[parts[0]], dict):
                self._remove_wildcard_field(config[parts[0]], parts[1:])
    
    def validate_all(self) -> Dict[str, List[str]]:
        """Validate entire configuration and return all errors
        
        Returns:
            Dictionary of section -> list of errors
        """
        all_errors = {}
        
        for section, validator in self.validators.items():
            if section in self.config:
                errors = validator(self.config[section])
                if errors:
                    all_errors[section] = errors
        
        return all_errors
    
    def reset_to_defaults(self, section: str = None):
        """Reset configuration to defaults
        
        Args:
            section: Optional section to reset (resets all if None)
        """
        if section:
            if section in self.defaults:
                self.config[section] = copy.deepcopy(self.defaults[section])
                logger.info(f"Reset section '{section}' to defaults")
        else:
            self.config = copy.deepcopy(self.defaults)
            logger.info("Reset entire configuration to defaults")
        
        self.save_config()


# Singleton instance
_config_manager = None


def get_config_manager(config_path: str = None) -> ConfigManager:
    """Get or create singleton ConfigManager instance"""
    global _config_manager
    if _config_manager is None:
        _config_manager = ConfigManager(config_path or "config.json")
    return _config_manager