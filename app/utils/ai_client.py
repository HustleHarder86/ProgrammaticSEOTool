"""Unified AI client for multiple providers."""
import logging
from typing import Optional, Dict, Any
from config import settings

logger = logging.getLogger(__name__)

class AIClient:
    """Unified client for AI providers (OpenAI, Anthropic, Perplexity)."""
    
    def __init__(self):
        self.provider = self._determine_provider()
        self.client = self._setup_client()
    
    def _determine_provider(self) -> str:
        """Determine which AI provider to use."""
        if settings.has_perplexity:
            return "perplexity"
        elif settings.has_openai:
            return "openai"
        elif settings.has_anthropic:
            return "anthropic"
        else:
            raise ValueError("No AI provider configured. Please set PERPLEXITY_API_KEY, OPENAI_API_KEY, or ANTHROPIC_API_KEY")
    
    def _setup_client(self):
        """Set up the appropriate AI client."""
        if self.provider == "perplexity":
            # Perplexity uses OpenAI-compatible API
            from openai import OpenAI
            return OpenAI(
                api_key=settings.perplexity_api_key,
                base_url="https://api.perplexity.ai"
            )
        elif self.provider == "openai":
            from openai import OpenAI
            return OpenAI(api_key=settings.openai_api_key)
        elif self.provider == "anthropic":
            from anthropic import Anthropic
            return Anthropic(api_key=settings.anthropic_api_key)
    
    async def generate(self, prompt: str, temperature: float = 0.7, max_tokens: int = 1000) -> str:
        """Generate text using the configured AI provider."""
        try:
            if self.provider in ["perplexity", "openai"]:
                # Use the appropriate model
                model = "llama-3.1-sonar-small-128k-online" if self.provider == "perplexity" else "gpt-3.5-turbo"
                
                response = self.client.chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=temperature,
                    max_tokens=max_tokens
                )
                return response.choices[0].message.content
                
            elif self.provider == "anthropic":
                response = self.client.messages.create(
                    model="claude-3-haiku-20240307",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=temperature,
                    max_tokens=max_tokens
                )
                return response.content[0].text
                
        except Exception as e:
            logger.error(f"Error generating with {self.provider}: {e}")
            raise
    
    def get_provider_info(self) -> Dict[str, Any]:
        """Get information about the current provider."""
        return {
            "provider": self.provider,
            "model": self._get_model_name(),
            "configured": True
        }
    
    def _get_model_name(self) -> str:
        """Get the model name for the current provider."""
        if self.provider == "perplexity":
            return "llama-3.1-sonar-small-128k-online"
        elif self.provider == "openai":
            return "gpt-3.5-turbo"
        elif self.provider == "anthropic":
            return "claude-3-haiku-20240307"
        return "unknown"