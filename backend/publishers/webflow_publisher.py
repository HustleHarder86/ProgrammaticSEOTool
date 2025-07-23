"""Webflow Publisher - Direct publishing to Webflow via API"""

import requests
import json
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import logging

from .base_publisher import BasePublisher

logger = logging.getLogger(__name__)


class WebflowPublisher(BasePublisher):
    """Publisher for Webflow sites using CMS API"""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize Webflow publisher
        
        Args:
            config: Configuration including:
                - api_url: Not used (Webflow has fixed API)
                - credentials:
                    - api_token: Webflow API token
                    - site_id: Webflow site ID
                    - collection_id: CMS collection ID
                - options:
                    - live: Whether to publish live immediately
                    - archived: Whether to archive by default
                    - draft: Whether to save as draft
        """
        super().__init__(config)
        
        # Webflow API base
        self.api_base = "https://api.webflow.com"
        
        # Authentication
        self.api_token = self.credentials.get("api_token", "")
        self.site_id = self.credentials.get("site_id", "")
        self.collection_id = self.credentials.get("collection_id", "")
        
        # Options
        self.publish_live = self.options.get("live", True)
        self.archived = self.options.get("archived", False)
        self.draft = self.options.get("draft", False)
        
        # Session setup
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_token}",
            "accept-version": "1.0.0",
            "Content-Type": "application/json"
        })
    
    def connect(self) -> bool:
        """Test connection to Webflow API"""
        try:
            # Test by getting site info
            endpoint = f"{self.api_base}/sites/{self.site_id}"
            response = self.session.get(endpoint)
            
            if response.status_code == 200:
                site_data = response.json()
                logger.info(f"Connected to Webflow site: {site_data.get('name')}")
                self.connected = True
                
                # Verify collection exists
                collection_endpoint = f"{self.api_base}/collections/{self.collection_id}"
                collection_response = self.session.get(collection_endpoint)
                
                if collection_response.status_code == 200:
                    collection_data = collection_response.json()
                    self.collection_name = collection_data.get('name')
                    self.collection_fields = collection_data.get('fields', [])
                    return True
                else:
                    logger.error(f"Collection not found: {self.collection_id}")
                    return False
            else:
                logger.error(f"Webflow connection failed: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"Webflow connection error: {str(e)}")
            return False
    
    def publish_single(self, page_data: Dict[str, Any]) -> Tuple[bool, Dict[str, Any]]:
        """Publish a single item to Webflow CMS"""
        try:
            # Validate data
            is_valid, errors = self.validate_page_data(page_data)
            if not is_valid:
                return False, {"errors": errors}
            
            # Prepare Webflow item data
            item_data = self._prepare_webflow_data(page_data)
            
            # Create item
            endpoint = f"{self.api_base}/collections/{self.collection_id}/items"
            response = self.session.post(endpoint, json=item_data)
            
            if response.status_code in [200, 201]:
                item_response = response.json()
                item_id = item_response['_id']
                
                # Publish if requested
                if self.publish_live:
                    self._publish_items([item_id])
                
                return True, {
                    "id": item_id,
                    "slug": item_response.get('slug'),
                    "created": item_response.get('created-on'),
                    "published": self.publish_live
                }
            else:
                return False, {
                    "error": f"Publishing failed: {response.status_code}",
                    "details": response.json() if response.content else {}
                }
                
        except Exception as e:
            return False, self.handle_error(e, "publish_single")
    
    def publish_batch(self, pages: List[Dict[str, Any]]) -> List[Tuple[bool, Dict[str, Any]]]:
        """Publish multiple items to Webflow CMS"""
        results = []
        item_ids_to_publish = []
        
        # Webflow has rate limits - respect them
        for i, page_data in enumerate(pages):
            # Rate limit: 60 requests per minute
            if i > 0 and i % 50 == 0:
                import time
                time.sleep(60)  # Wait a minute
            
            success, response = self.publish_single(page_data)
            results.append((success, response))
            
            if success and self.publish_live:
                item_ids_to_publish.append(response['id'])
            
            # Log progress
            if i % 10 == 0:
                logger.info(f"Created {i+1}/{len(pages)} items in Webflow")
        
        # Bulk publish if needed
        if item_ids_to_publish and self.publish_live:
            self._publish_items(item_ids_to_publish)
        
        return results
    
    def update_page(self, page_id: str, page_data: Dict[str, Any]) -> Tuple[bool, Dict[str, Any]]:
        """Update existing Webflow item"""
        try:
            # Prepare update data
            item_data = self._prepare_webflow_data(page_data)
            
            # Update item
            endpoint = f"{self.api_base}/collections/{self.collection_id}/items/{page_id}"
            response = self.session.patch(endpoint, json=item_data)
            
            if response.status_code == 200:
                item_response = response.json()
                
                # Republish if live
                if self.publish_live:
                    self._publish_items([page_id])
                
                return True, {
                    "id": page_id,
                    "updated": item_response.get('updated-on'),
                    "published": self.publish_live
                }
            else:
                return False, {
                    "error": f"Update failed: {response.status_code}",
                    "details": response.json() if response.content else {}
                }
                
        except Exception as e:
            return False, self.handle_error(e, "update_page")
    
    def delete_page(self, page_id: str) -> Tuple[bool, Dict[str, Any]]:
        """Delete Webflow item"""
        try:
            endpoint = f"{self.api_base}/collections/{self.collection_id}/items/{page_id}"
            response = self.session.delete(endpoint)
            
            if response.status_code in [200, 204]:
                # Republish site to reflect deletion
                if self.publish_live:
                    self._publish_site()
                
                return True, {"message": "Item deleted successfully"}
            else:
                return False, {
                    "error": f"Delete failed: {response.status_code}",
                    "details": response.json() if response.content else {}
                }
                
        except Exception as e:
            return False, self.handle_error(e, "delete_page")
    
    def get_page_status(self, page_id: str) -> Dict[str, Any]:
        """Get Webflow item status"""
        try:
            endpoint = f"{self.api_base}/collections/{self.collection_id}/items/{page_id}"
            response = self.session.get(endpoint)
            
            if response.status_code == 200:
                item_data = response.json()
                return {
                    "exists": True,
                    "archived": item_data.get('_archived', False),
                    "draft": item_data.get('_draft', False),
                    "slug": item_data.get('slug'),
                    "created": item_data.get('created-on'),
                    "updated": item_data.get('updated-on')
                }
            else:
                return {"exists": False, "error": f"Item not found: {response.status_code}"}
                
        except Exception as e:
            return {"exists": False, "error": str(e)}
    
    def _prepare_webflow_data(self, page_data: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare data for Webflow CMS format"""
        # Map common fields to Webflow field names
        # Note: Field mapping depends on your collection structure
        webflow_data = {
            "fields": {
                "name": page_data.get("title", ""),
                "slug": page_data.get("slug", ""),
                "_archived": self.archived,
                "_draft": self.draft
            }
        }
        
        # Map content fields based on collection structure
        field_mapping = {
            "content": "content",  # Rich text field
            "meta_description": "meta-description",
            "excerpt": "excerpt",
            "featured_image_url": "main-image",
            "keywords": "seo-keywords"
        }
        
        for our_field, webflow_field in field_mapping.items():
            if page_data.get(our_field):
                # Check if field exists in collection
                if self._field_exists(webflow_field):
                    webflow_data["fields"][webflow_field] = page_data[our_field]
        
        # Add custom fields
        if page_data.get("custom_fields"):
            for field, value in page_data["custom_fields"].items():
                if self._field_exists(field):
                    webflow_data["fields"][field] = value
        
        # Handle schema markup - might need custom field
        if page_data.get("schema_markup") and self._field_exists("schema-markup"):
            webflow_data["fields"]["schema-markup"] = json.dumps(page_data["schema_markup"])
        
        return webflow_data
    
    def _field_exists(self, field_name: str) -> bool:
        """Check if field exists in collection"""
        if hasattr(self, 'collection_fields'):
            return any(field.get('slug') == field_name for field in self.collection_fields)
        return True  # Assume exists if we can't check
    
    def _publish_items(self, item_ids: List[str]):
        """Publish multiple items"""
        try:
            endpoint = f"{self.api_base}/collections/{self.collection_id}/items/publish"
            data = {"itemIds": item_ids}
            
            response = self.session.put(endpoint, json=data)
            
            if response.status_code == 200:
                logger.info(f"Published {len(item_ids)} items")
            else:
                logger.warning(f"Failed to publish items: {response.status_code}")
                
        except Exception as e:
            logger.error(f"Error publishing items: {str(e)}")
    
    def _publish_site(self):
        """Publish entire site"""
        try:
            endpoint = f"{self.api_base}/sites/{self.site_id}/publish"
            data = {"domains": []}  # Publish to all domains
            
            response = self.session.post(endpoint, json=data)
            
            if response.status_code == 200:
                logger.info("Site published successfully")
            else:
                logger.warning(f"Failed to publish site: {response.status_code}")
                
        except Exception as e:
            logger.error(f"Error publishing site: {str(e)}")
    
    def get_collection_schema(self) -> Dict[str, Any]:
        """Get collection schema to understand fields"""
        try:
            endpoint = f"{self.api_base}/collections/{self.collection_id}"
            response = self.session.get(endpoint)
            
            if response.status_code == 200:
                return response.json()
            else:
                return {}
                
        except Exception as e:
            logger.error(f"Error fetching collection schema: {str(e)}")
            return {}
    
    def create_collection_field(self, field_data: Dict[str, Any]) -> bool:
        """Create a new field in the collection (requires specific permissions)"""
        # Note: This typically requires higher-level API access
        # Most users will need to create fields manually in Webflow Designer
        logger.warning("Creating collection fields via API requires special permissions")
        return False