# Makefile for Programmatic SEO Tool
# Provides npm-like commands for Python project

.PHONY: dev api ui test install clean help

# Default target
help:
	@echo "Available commands:"
	@echo "  make dev      - Run both API and UI (equivalent to npm run dev)"
	@echo "  make api      - Run API server only"
	@echo "  make ui       - Run Streamlit UI only"
	@echo "  make test     - Run tests"
	@echo "  make install  - Install dependencies"
	@echo "  make clean    - Clean cache and temporary files"

# Run both API and UI
dev:
	@echo "🚀 Starting development servers..."
	@echo "API: http://localhost:8000"
	@echo "UI:  http://localhost:8501"
	@echo "Docs: http://localhost:8000/docs"
	@python run_local.py

# Run API server only
api:
	@echo "🚀 Starting API server on http://localhost:8000"
	python -m uvicorn app.main:app --reload

# Run Streamlit UI only
ui:
	@echo "🚀 Starting Streamlit UI on http://localhost:8501"
	streamlit run streamlit_wizard.py

# Run tests
test:
	@echo "🧪 Running tests..."
	./test_api.sh

# Install dependencies
install:
	@echo "📦 Installing dependencies..."
	pip install -r requirements.txt

# Clean cache and temporary files
clean:
	@echo "🧹 Cleaning cache and temporary files..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	rm -rf data/cache/*
	@echo "✨ Clean complete!"

# Initialize database
init-db:
	@echo "🗄️ Initializing database..."
	python init_db.py