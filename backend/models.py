"""Database models for the Programmatic SEO Tool."""
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Integer, JSON, Float, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base
import uuid
import enum

# Helper to generate UUIDs
def generate_uuid():
    return str(uuid.uuid4())

class OperationType(enum.Enum):
    """Types of operations that incur API costs."""
    BUSINESS_ANALYSIS = "business_analysis"
    TEMPLATE_GENERATION = "template_generation" 
    VARIABLE_GENERATION = "variable_generation"
    PAGE_GENERATION = "page_generation"
    CONTENT_ENRICHMENT = "content_enrichment"

class Project(Base):
    """A programmatic SEO project containing templates and data."""
    __tablename__ = "projects"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(200), nullable=False)
    business_input = Column(Text)  # Original business description/URL
    business_analysis = Column(JSON)  # Stored analysis results
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    templates = relationship("Template", back_populates="project", cascade="all, delete-orphan")
    data_sets = relationship("DataSet", back_populates="project", cascade="all, delete-orphan")
    generated_pages = relationship("GeneratedPage", back_populates="project", cascade="all, delete-orphan")
    potential_pages = relationship("PotentialPage", cascade="all, delete-orphan")
    api_costs = relationship("ApiCost", back_populates="project", cascade="all, delete-orphan")

class Template(Base):
    """Page template with variable placeholders."""
    __tablename__ = "templates"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    project_id = Column(String(36), ForeignKey("projects.id"), nullable=False)
    name = Column(String(200), nullable=False)
    pattern = Column(Text)  # e.g., "[City] [Service] Providers"
    variables = Column(JSON)  # List of variables extracted from pattern
    template_sections = Column(JSON)  # Stores SEO structure and content sections
    example_pages = Column(JSON)  # Example pages generated from this template
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    project = relationship("Project", back_populates="templates")
    generated_pages = relationship("GeneratedPage", back_populates="template")

class DataSet(Base):
    """Data imported for template variables."""
    __tablename__ = "data_sets"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    project_id = Column(String(36), ForeignKey("projects.id"), nullable=False)
    name = Column(String(200), nullable=False)
    data = Column(JSON)  # Stored as JSON array of objects
    row_count = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    project = relationship("Project", back_populates="data_sets")

class GeneratedPage(Base):
    """Pages generated from templates + data."""
    __tablename__ = "generated_pages"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    project_id = Column(String(36), ForeignKey("projects.id"), nullable=False)
    template_id = Column(String(36), ForeignKey("templates.id"), nullable=False)
    title = Column(String(500), nullable=False)
    content = Column(JSON)  # Full page content structure
    meta_data = Column(JSON)  # SEO metadata, URL slug, etc.
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    project = relationship("Project", back_populates="generated_pages")
    template = relationship("Template", back_populates="generated_pages")

class ApiCost(Base):
    """Track API costs per operation."""
    __tablename__ = "api_costs"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    project_id = Column(String(36), ForeignKey("projects.id"), nullable=False)
    operation_type = Column(Enum(OperationType), nullable=False)
    provider = Column(String(50), nullable=False)  # 'perplexity', 'openai', 'anthropic'
    model = Column(String(100))  # Model name used
    input_tokens = Column(Integer, default=0)
    output_tokens = Column(Integer, default=0)
    total_tokens = Column(Integer, default=0)
    cost = Column(Float, default=0.0)  # Cost in USD
    details = Column(JSON)  # Additional details about the operation
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    project = relationship("Project", back_populates="api_costs")

class PotentialPage(Base):
    """Potential pages that can be generated from templates - stored for preview and selection."""
    __tablename__ = "potential_pages"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    project_id = Column(String(36), ForeignKey("projects.id"), nullable=False)
    template_id = Column(String(36), ForeignKey("templates.id"), nullable=False)
    title = Column(Text, nullable=False)  # Generated title with variables filled
    slug = Column(Text, nullable=False)   # URL slug for the page
    variables = Column(JSON, nullable=False)  # Variable values used for this page
    is_generated = Column(Integer, default=0)  # 0 = not generated, 1 = generated
    generated_page_id = Column(String(36), ForeignKey("generated_pages.id"))  # Link to actual generated page
    priority = Column(Integer, default=0)  # User can set priority for generation order
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    project = relationship("Project")
    template = relationship("Template")
    generated_page = relationship("GeneratedPage")