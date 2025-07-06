"""Database models for the Programmatic SEO Tool."""
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime
from config import settings

Base = declarative_base()

class Project(Base):
    """SEO project containing multiple content pieces."""
    __tablename__ = 'projects'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    business_description = Column(Text)
    business_url = Column(String(500))
    industry = Column(String(100))
    location = Column(String(200))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    keywords = relationship("Keyword", back_populates="project", cascade="all, delete-orphan")
    content_pieces = relationship("Content", back_populates="project", cascade="all, delete-orphan")

class Keyword(Base):
    """Keywords associated with a project."""
    __tablename__ = 'keywords'
    
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.id'), nullable=False)
    keyword = Column(String(200), nullable=False)
    search_volume = Column(Integer)
    difficulty = Column(Integer)
    priority = Column(Integer, default=5)
    content_type = Column(String(50))  # comparison, how-to, etc.
    status = Column(String(20), default='pending')  # pending, generated, published
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    project = relationship("Project", back_populates="keywords")
    content_pieces = relationship("Content", back_populates="keyword", cascade="all, delete-orphan")

class Content(Base):
    """Generated content pieces."""
    __tablename__ = 'content'
    
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.id'), nullable=False)
    keyword_id = Column(Integer, ForeignKey('keywords.id'))
    title = Column(String(500), nullable=False)
    meta_description = Column(Text)
    slug = Column(String(500))
    content_html = Column(Text)
    content_markdown = Column(Text)
    word_count = Column(Integer)
    template_used = Column(String(50))
    variation_number = Column(Integer, default=1)
    status = Column(String(20), default='draft')  # draft, ready, published
    published_at = Column(DateTime)
    published_url = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    project = relationship("Project", back_populates="content_pieces")
    keyword = relationship("Keyword", back_populates="content_pieces")

# Database setup
engine = create_engine(settings.database_url, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Initialize the database."""
    Base.metadata.create_all(bind=engine)

def get_db():
    """Get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()