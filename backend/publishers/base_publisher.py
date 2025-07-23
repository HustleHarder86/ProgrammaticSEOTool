"""Base Publisher class for CMS integrations"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class BasePublisher(ABC):
    """Abstract base class for CMS publishers"""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize publisher with configuration
        
        Args:
            config: CMS-specific configuration including:
                - api_url: Base URL for CMS API
                - credentials: Authentication details
                - options: Additional CMS-specific options
        """
        self.config = config
        self.api_url = config.get("api_url", "")
        self.credentials = config.get("credentials", {})
        self.options = config.get("options", {})
        self.connected = False
        
    @abstractmethod
    def connect(self) -> bool:
        """Establish connection to CMS
        
        Returns:
            True if connection successful
        """
        pass
    
    @abstractmethod
    def publish_single(self, page_data: Dict[str, Any]) -> Tuple[bool, Dict[str, Any]]:
        """Publish a single page to CMS
        
        Args:
            page_data: Page data including title, content, meta, etc.
            
        Returns:
            Tuple of (success, response_data)
        """
        pass
    
    @abstractmethod
    def publish_batch(self, pages: List[Dict[str, Any]]) -> List[Tuple[bool, Dict[str, Any]]]:
        """Publish multiple pages to CMS
        
        Args:
            pages: List of page data dictionaries
            
        Returns:
            List of (success, response_data) tuples
        """
        pass
    
    @abstractmethod
    def update_page(self, page_id: str, page_data: Dict[str, Any]) -> Tuple[bool, Dict[str, Any]]:
        """Update existing page in CMS
        
        Args:
            page_id: CMS page identifier
            page_data: Updated page data
            
        Returns:
            Tuple of (success, response_data)
        """
        pass
    
    @abstractmethod
    def delete_page(self, page_id: str) -> Tuple[bool, Dict[str, Any]]:
        """Delete page from CMS
        
        Args:
            page_id: CMS page identifier
            
        Returns:
            Tuple of (success, response_data)
        """
        pass
    
    @abstractmethod
    def get_page_status(self, page_id: str) -> Dict[str, Any]:
        """Get status of published page
        
        Args:
            page_id: CMS page identifier
            
        Returns:
            Status information dictionary
        """
        pass
    
    def validate_page_data(self, page_data: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """Validate page data before publishing
        
        Args:
            page_data: Page data to validate
            
        Returns:
            Tuple of (is_valid, error_messages)
        """
        errors = []
        
        # Check required fields
        required_fields = ["title", "content"]
        for field in required_fields:
            if not page_data.get(field):
                errors.append(f"Missing required field: {field}")
        
        # Check field lengths
        if len(page_data.get("title", "")) > 200:
            errors.append("Title exceeds maximum length (200 characters)")
        
        if len(page_data.get("meta_description", "")) > 160:
            errors.append("Meta description exceeds maximum length (160 characters)")
        
        return len(errors) == 0, errors
    
    def prepare_page_data(self, page_data: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare page data for CMS format
        
        Args:
            page_data: Raw page data
            
        Returns:
            CMS-formatted page data
        """
        # Default preparation - can be overridden by subclasses
        prepared = {
            "title": page_data.get("title", ""),
            "content": page_data.get("content_html", page_data.get("content", "")),
            "excerpt": page_data.get("meta_description", ""),
            "slug": page_data.get("slug", self._generate_slug(page_data.get("title", ""))),
            "status": page_data.get("status", "publish"),
            "date": page_data.get("publish_date", datetime.now().isoformat()),
            "meta": {
                "description": page_data.get("meta_description", ""),
                "keywords": page_data.get("keywords", [])
            }
        }
        
        # Add schema markup if available
        if page_data.get("schema_markup"):
            prepared["schema"] = page_data["schema_markup"]
        
        # Add custom fields
        if page_data.get("custom_fields"):
            prepared["custom_fields"] = page_data["custom_fields"]
        
        return prepared
    
    def _generate_slug(self, title: str) -> str:
        """Generate URL-friendly slug from title
        
        Args:
            title: Page title
            
        Returns:
            URL slug
        """
        import re
        # Convert to lowercase and replace spaces with hyphens
        slug = title.lower().strip()
        slug = re.sub(r'[^\w\s-]', '', slug)
        slug = re.sub(r'[\s_-]+', '-', slug)
        slug = re.sub(r'^-+|-+$', '', slug)
        return slug
    
    def handle_error(self, error: Exception, context: str = "") -> Dict[str, Any]:
        """Handle and log publishing errors
        
        Args:
            error: Exception that occurred
            context: Additional context about the error
            
        Returns:
            Error response dictionary
        """
        error_msg = f"Publishing error in {self.__class__.__name__}"
        if context:
            error_msg += f" ({context})"
        error_msg += f": {str(error)}"
        
        logger.error(error_msg)
        
        return {
            "success": False,
            "error": str(error),
            "error_type": type(error).__name__,
            "context": context,
            "timestamp": datetime.now().isoformat()
        }
    
    def get_publish_stats(self) -> Dict[str, Any]:
        """Get publishing statistics
        
        Returns:
            Statistics dictionary
        """
        # Override in subclasses to provide actual stats
        return {
            "total_published": 0,
            "successful": 0,
            "failed": 0,
            "last_publish": None
        }