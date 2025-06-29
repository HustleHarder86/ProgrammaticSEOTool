"""Configuration management for the Programmatic SEO Tool."""
import os
from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings(BaseSettings):
    """Application settings."""
    
    # API Keys
    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    ubersuggest_api_key: Optional[str] = None
    serpapi_key: Optional[str] = None
    
    # WordPress Integration
    wordpress_url: Optional[str] = None
    wordpress_username: Optional[str] = None
    wordpress_app_password: Optional[str] = None
    
    # Application Settings
    app_env: str = "development"
    debug: bool = True
    log_level: str = "info"
    
    # Database
    database_url: str = "sqlite:///./data/database.db"
    
    # Content Generation
    max_concurrent_generations: int = 5
    content_generation_timeout: int = 30
    
    # Cache
    cache_ttl: int = 3600
    
    # Paths
    base_dir: Path = Path(__file__).parent
    data_dir: Path = base_dir / "data"
    exports_dir: Path = data_dir / "exports"
    cache_dir: Path = data_dir / "cache"
    templates_dir: Path = base_dir / "app" / "templates"
    
    class Config:
        env_file = ".env"
        case_sensitive = False
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Create directories if they don't exist
        self.data_dir.mkdir(exist_ok=True)
        self.exports_dir.mkdir(exist_ok=True)
        self.cache_dir.mkdir(exist_ok=True)
        self.templates_dir.mkdir(exist_ok=True)
    
    @property
    def has_openai(self) -> bool:
        """Check if OpenAI API key is configured."""
        return bool(self.openai_api_key)
    
    @property
    def has_anthropic(self) -> bool:
        """Check if Anthropic API key is configured."""
        return bool(self.anthropic_api_key)
    
    @property
    def has_ai_provider(self) -> bool:
        """Check if at least one AI provider is configured."""
        return self.has_openai or self.has_anthropic

# Create global settings instance
settings = Settings()