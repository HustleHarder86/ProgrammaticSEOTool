"""Run both FastAPI and Streamlit locally."""
import subprocess
import os
import time
import webbrowser
from threading import Thread

def run_fastapi():
    """Run FastAPI server."""
    subprocess.run(["uvicorn", "app.main:app", "--reload", "--port", "8000"])

def run_streamlit():
    """Run Streamlit UI."""
    # Wait for FastAPI to start
    time.sleep(3)
    subprocess.run(["streamlit", "run", "streamlit_app.py", "--server.port", "8501"])

def main():
    """Run both servers."""
    print("🚀 Starting Programmatic SEO Tool...")
    print("📡 FastAPI will run on http://localhost:8000")
    print("🎨 Streamlit will run on http://localhost:8501")
    print("\nMake sure you have configured your .env file with API keys!")
    
    # Check for .env file
    if not os.path.exists(".env"):
        print("\n⚠️  WARNING: .env file not found!")
        print("Copy .env.example to .env and add your API keys")
        return
    
    # Start FastAPI in a thread
    fastapi_thread = Thread(target=run_fastapi)
    fastapi_thread.daemon = True
    fastapi_thread.start()
    
    # Wait a bit for FastAPI to start
    time.sleep(2)
    
    # Open browser
    webbrowser.open("http://localhost:8501")
    
    # Run Streamlit in main thread
    run_streamlit()

if __name__ == "__main__":
    main()