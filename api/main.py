"""Main API entry point for Vercel deployment"""
import sys
import os

# Add backend to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Import the FastAPI app from backend
from backend.main import app

# Export app for Vercel
application = app