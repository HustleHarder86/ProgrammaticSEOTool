#!/bin/bash

# Railway startup script
echo "Starting Programmatic SEO Tool Backend..."

# Run database migrations if needed
# python -m alembic upgrade head

# Start the FastAPI application
exec uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}