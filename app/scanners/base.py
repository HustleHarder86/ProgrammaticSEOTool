"""Base classes for business analysis."""
from typing import List, Dict, Optional
from pydantic import BaseModel
from abc import ABC, abstractmethod

class BusinessInfo(BaseModel):
    """Structured business information extracted from analysis."""
    name: Optional[str] = None
    description: str
    services: List[str] = []
    products: List[str] = []
    industry: Optional[str] = None
    location: Optional[str] = None
    target_audience: List[str] = []
    unique_selling_points: List[str] = []
    keywords: List[str] = []
    competitors: List[str] = []
    
class ContentOpportunity(BaseModel):
    """A content opportunity identified from business analysis."""
    keyword: str
    content_type: str  # comparison, how-to, best-x-for-y, location-based, etc.
    priority: int  # 1-10 scale
    estimated_difficulty: Optional[int] = None
    search_volume: Optional[int] = None
    title_template: str
    description: str

class BusinessAnalyzer(ABC):
    """Abstract base class for business analyzers."""
    
    @abstractmethod
    async def analyze(self, input_data: str) -> BusinessInfo:
        """Analyze the input and extract business information."""
        pass
    
    @abstractmethod
    async def identify_opportunities(self, business_info: BusinessInfo) -> List[ContentOpportunity]:
        """Identify content opportunities from business information."""
        pass