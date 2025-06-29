"""Vercel serverless function entry point."""
from app.main import app

# Vercel expects a function named 'handler'
handler = app