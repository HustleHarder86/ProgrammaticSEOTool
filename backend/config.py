"""Configuration management for the application."""
import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings:
    """Application settings."""
    
    # Base paths
    BASE_DIR = Path(__file__).resolve().parent
    DATA_DIR = BASE_DIR / "data"
    CACHE_DIR = DATA_DIR / "cache"
    EXPORTS_DIR = DATA_DIR / "exports"
    
    # Database - Use PostgreSQL for Railway
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/database.db")
    
    # If Railway provides DATABASE_URL, it might use postgres:// instead of postgresql://
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
    
    # API Keys
    PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    
    # CORS Settings
    FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")
    ALLOWED_ORIGINS = [
        FRONTEND_URL,
        "http://localhost:3000",
        "http://localhost:3001",
    ]
    
    # Environment
    ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
    DEBUG = os.getenv("DEBUG", "True").lower() == "true"
    
    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    # API Settings
    API_V1_STR = "/api/v1"
    PROJECT_NAME = "Programmatic SEO Tool"
    
    # Security
    SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")
    
    @property
    def has_perplexity(self) -> bool:
        return bool(self.PERPLEXITY_API_KEY)
    
    @property
    def has_openai(self) -> bool:
        return bool(self.OPENAI_API_KEY)
    
    @property
    def has_anthropic(self) -> bool:
        return bool(self.ANTHROPIC_API_KEY)
    
    @property
    def has_ai_provider(self) -> bool:
        return self.has_perplexity or self.has_openai or self.has_anthropic
    
    def __init__(self):
        """Initialize settings and create directories."""
        # Create necessary directories
        for directory in [self.DATA_DIR, self.CACHE_DIR, self.EXPORTS_DIR]:
            directory.mkdir(parents=True, exist_ok=True)

# Global settings instance
settings = Settings()