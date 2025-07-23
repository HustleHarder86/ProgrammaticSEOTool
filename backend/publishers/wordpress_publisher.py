"""WordPress Publisher - Direct publishing to WordPress via REST API"""

import requests
from requests.auth import HTTPBasicAuth
import json
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import base64
import logging

from .base_publisher import BasePublisher

logger = logging.getLogger(__name__)


class WordPressPublisher(BasePublisher):
    """Publisher for WordPress sites using REST API"""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize WordPress publisher
        
        Args:
            config: Configuration including:
                - api_url: WordPress site URL (e.g., https://site.com)
                - credentials:
                    - username: WordPress username
                    - app_password: Application password
                - options:
                    - default_author: Default author ID
                    - default_category: Default category ID
                    - default_tags: List of default tag IDs
                    - post_type: 'post' or 'page'
                    - custom_taxonomies: Custom taxonomy mappings
        """
        super().__init__(config)
        
        # Build API endpoints
        self.base_url = self.api_url.rstrip('/')
        self.api_base = f"{self.base_url}/wp-json/wp/v2"
        
        # Authentication
        self.auth = HTTPBasicAuth(
            self.credentials.get("username", ""),
            self.credentials.get("app_password", "")
        )
        
        # Options
        self.post_type = self.options.get("post_type", "posts")
        self.default_author = self.options.get("default_author", 1)
        self.default_category = self.options.get("default_category", 1)
        self.default_tags = self.options.get("default_tags", [])
        self.custom_taxonomies = self.options.get("custom_taxonomies", {})
        
        # Session for connection pooling
        self.session = requests.Session()
        self.session.auth = self.auth
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json"
        })
    
    def connect(self) -> bool:
        """Test connection to WordPress API"""
        try:
            # Test authentication by getting user info
            response = self.session.get(f"{self.api_base}/users/me")
            
            if response.status_code == 200:
                user_data = response.json()
                logger.info(f"Connected to WordPress as {user_data.get('name')}")
                self.connected = True
                
                # Get and store user ID
                self.current_user_id = user_data.get('id', self.default_author)
                return True
            else:
                logger.error(f"WordPress connection failed: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"WordPress connection error: {str(e)}")
            return False
    
    def publish_single(self, page_data: Dict[str, Any]) -> Tuple[bool, Dict[str, Any]]:
        """Publish a single page to WordPress"""
        try:
            # Validate data
            is_valid, errors = self.validate_page_data(page_data)
            if not is_valid:
                return False, {"errors": errors}
            
            # Prepare WordPress post data
            wp_data = self._prepare_wordpress_data(page_data)
            
            # Create post
            endpoint = f"{self.api_base}/{self.post_type}"
            response = self.session.post(endpoint, json=wp_data)
            
            if response.status_code in [200, 201]:
                post_data = response.json()
                
                # Add schema markup if provided
                if page_data.get("schema_markup"):
                    self._add_schema_markup(post_data['id'], page_data["schema_markup"])
                
                return True, {
                    "id": post_data['id'],
                    "url": post_data['link'],
                    "status": post_data['status'],
                    "slug": post_data['slug']
                }
            else:
                return False, {
                    "error": f"Publishing failed: {response.status_code}",
                    "details": response.json() if response.content else {}
                }
                
        except Exception as e:
            return False, self.handle_error(e, "publish_single")
    
    def publish_batch(self, pages: List[Dict[str, Any]]) -> List[Tuple[bool, Dict[str, Any]]]:
        """Publish multiple pages to WordPress"""
        results = []
        
        for i, page_data in enumerate(pages):
            # Add delay to avoid rate limiting
            if i > 0 and i % 10 == 0:
                import time
                time.sleep(2)
            
            success, response = self.publish_single(page_data)
            results.append((success, response))
            
            # Log progress
            if i % 10 == 0:
                logger.info(f"Published {i+1}/{len(pages)} pages")
        
        return results
    
    def update_page(self, page_id: str, page_data: Dict[str, Any]) -> Tuple[bool, Dict[str, Any]]:
        """Update existing WordPress post"""
        try:
            # Prepare update data
            wp_data = self._prepare_wordpress_data(page_data)
            
            # Update post
            endpoint = f"{self.api_base}/{self.post_type}/{page_id}"
            response = self.session.post(endpoint, json=wp_data)
            
            if response.status_code == 200:
                post_data = response.json()
                return True, {
                    "id": post_data['id'],
                    "url": post_data['link'],
                    "modified": post_data['modified']
                }
            else:
                return False, {
                    "error": f"Update failed: {response.status_code}",
                    "details": response.json() if response.content else {}
                }
                
        except Exception as e:
            return False, self.handle_error(e, "update_page")
    
    def delete_page(self, page_id: str) -> Tuple[bool, Dict[str, Any]]:
        """Delete WordPress post"""
        try:
            endpoint = f"{self.api_base}/{self.post_type}/{page_id}"
            response = self.session.delete(endpoint)
            
            if response.status_code == 200:
                return True, {"message": "Post deleted successfully"}
            else:
                return False, {
                    "error": f"Delete failed: {response.status_code}",
                    "details": response.json() if response.content else {}
                }
                
        except Exception as e:
            return False, self.handle_error(e, "delete_page")
    
    def get_page_status(self, page_id: str) -> Dict[str, Any]:
        """Get WordPress post status"""
        try:
            endpoint = f"{self.api_base}/{self.post_type}/{page_id}"
            response = self.session.get(endpoint)
            
            if response.status_code == 200:
                post_data = response.json()
                return {
                    "exists": True,
                    "status": post_data['status'],
                    "url": post_data['link'],
                    "modified": post_data['modified'],
                    "author": post_data['author']
                }
            else:
                return {"exists": False, "error": f"Post not found: {response.status_code}"}
                
        except Exception as e:
            return {"exists": False, "error": str(e)}
    
    def _prepare_wordpress_data(self, page_data: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare data for WordPress API format"""
        # Base post data
        wp_data = {
            "title": page_data.get("title", ""),
            "content": page_data.get("content_html", page_data.get("content", "")),
            "excerpt": page_data.get("meta_description", ""),
            "slug": page_data.get("slug", ""),
            "status": page_data.get("status", "publish"),
            "author": page_data.get("author_id", self.current_user_id if hasattr(self, 'current_user_id') else self.default_author),
            "categories": page_data.get("categories", [self.default_category]),
            "tags": page_data.get("tags", self.default_tags)
        }
        
        # Add featured image if provided
        if page_data.get("featured_image_id"):
            wp_data["featured_media"] = page_data["featured_image_id"]
        elif page_data.get("featured_image_url"):
            # Upload image and get ID
            image_id = self._upload_image(page_data["featured_image_url"])
            if image_id:
                wp_data["featured_media"] = image_id
        
        # Add custom fields/meta
        if page_data.get("custom_fields"):
            wp_data["meta"] = page_data["custom_fields"]
        
        # Add Yoast SEO fields if available
        if page_data.get("yoast_meta"):
            wp_data["yoast_meta"] = page_data["yoast_meta"]
        
        return wp_data
    
    def _add_schema_markup(self, post_id: int, schema_markup: Dict[str, Any]):
        """Add schema markup to post using custom field"""
        try:
            # Convert schema to JSON string
            schema_json = json.dumps(schema_markup)
            
            # Update post meta
            meta_data = {
                "meta": {
                    "schema_markup": schema_json
                }
            }
            
            endpoint = f"{self.api_base}/{self.post_type}/{post_id}"
            response = self.session.post(endpoint, json=meta_data)
            
            if response.status_code != 200:
                logger.warning(f"Failed to add schema markup to post {post_id}")
                
        except Exception as e:
            logger.error(f"Error adding schema markup: {str(e)}")
    
    def _upload_image(self, image_url: str) -> Optional[int]:
        """Upload image to WordPress media library"""
        try:
            # Download image
            image_response = requests.get(image_url)
            if image_response.status_code != 200:
                return None
            
            # Prepare upload
            filename = image_url.split('/')[-1]
            headers = {
                'Content-Disposition': f'attachment; filename="{filename}"',
                'Content-Type': 'image/jpeg'  # Adjust based on actual type
            }
            
            # Upload to media library
            endpoint = f"{self.api_base}/media"
            response = self.session.post(
                endpoint,
                data=image_response.content,
                headers=headers
            )
            
            if response.status_code in [200, 201]:
                media_data = response.json()
                return media_data['id']
            else:
                logger.warning(f"Failed to upload image: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Error uploading image: {str(e)}")
            return None
    
    def create_category(self, name: str, slug: str = "", parent: int = 0) -> Optional[int]:
        """Create a new category in WordPress"""
        try:
            category_data = {
                "name": name,
                "slug": slug or self._generate_slug(name),
                "parent": parent
            }
            
            endpoint = f"{self.api_base}/categories"
            response = self.session.post(endpoint, json=category_data)
            
            if response.status_code in [200, 201]:
                cat_data = response.json()
                return cat_data['id']
            else:
                logger.warning(f"Failed to create category: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Error creating category: {str(e)}")
            return None
    
    def create_tag(self, name: str, slug: str = "") -> Optional[int]:
        """Create a new tag in WordPress"""
        try:
            tag_data = {
                "name": name,
                "slug": slug or self._generate_slug(name)
            }
            
            endpoint = f"{self.api_base}/tags"
            response = self.session.post(endpoint, json=tag_data)
            
            if response.status_code in [200, 201]:
                tag_data = response.json()
                return tag_data['id']
            else:
                logger.warning(f"Failed to create tag: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Error creating tag: {str(e)}")
            return None
    
    def get_categories(self) -> List[Dict[str, Any]]:
        """Get all categories from WordPress"""
        try:
            endpoint = f"{self.api_base}/categories?per_page=100"
            response = self.session.get(endpoint)
            
            if response.status_code == 200:
                return response.json()
            else:
                return []
                
        except Exception as e:
            logger.error(f"Error fetching categories: {str(e)}")
            return []
    
    def get_tags(self) -> List[Dict[str, Any]]:
        """Get all tags from WordPress"""
        try:
            endpoint = f"{self.api_base}/tags?per_page=100"
            response = self.session.get(endpoint)
            
            if response.status_code == 200:
                return response.json()
            else:
                return []
                
        except Exception as e:
            logger.error(f"Error fetching tags: {str(e)}")
            return []