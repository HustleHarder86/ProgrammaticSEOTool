#!/usr/bin/env python3
"""Development server runner - similar to 'npm run dev'"""
import subprocess
import sys
import time
import os

def main():
    print("🚀 Starting Programmatic SEO Tool in development mode...")
    print("=" * 60)
    print("📡 API Server: http://localhost:8000")
    print("🎨 UI Server:  http://localhost:8501") 
    print("📚 API Docs:   http://localhost:8000/docs")
    print("=" * 60)
    print("\nPress Ctrl+C to stop all servers\n")
    
    # Check if .env exists
    if not os.path.exists('.env'):
        print("⚠️  Warning: .env file not found!")
        print("📝 Copy .env.example to .env and add your API key:")
        print("   cp .env.example .env")
        print("")
    
    try:
        # Run the local development script
        subprocess.run([sys.executable, "run_local.py"])
    except KeyboardInterrupt:
        print("\n\n👋 Shutting down development servers...")
        sys.exit(0)

if __name__ == "__main__":
    main()