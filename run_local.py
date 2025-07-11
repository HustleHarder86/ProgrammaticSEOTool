"""Run both FastAPI and Next.js locally."""
import subprocess
import os
import time
import webbrowser
from threading import Thread
import signal
import sys

class ProcessManager:
    def __init__(self):
        self.processes = []
    
    def add_process(self, process):
        self.processes.append(process)
    
    def terminate_all(self):
        for process in self.processes:
            if process.poll() is None:
                process.terminate()
                process.wait()

process_manager = ProcessManager()

def signal_handler(sig, frame):
    print("\n\n🛑 Shutting down servers...")
    process_manager.terminate_all()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def run_fastapi():
    """Run FastAPI server."""
    # Change to backend directory and run
    process = subprocess.Popen(["python3", "-m", "uvicorn", "main:app", "--reload", "--port", "8000"], cwd="backend")
    process_manager.add_process(process)
    process.wait()

def run_nextjs():
    """Run Next.js frontend."""
    # Check if package.json exists (Next.js is in root)
    if not os.path.exists("package.json"):
        print("\n⚠️  Next.js package.json not found!")
        print("Run npm install to install dependencies")
        return None
    
    # Run in current directory (root)
    process = subprocess.Popen(["npm", "run", "dev"])
    process_manager.add_process(process)
    return process

def run_streamlit():
    """Run Streamlit UI (legacy option)."""
    if os.path.exists("streamlit_app.py"):
        process = subprocess.Popen(["streamlit", "run", "streamlit_app.py", "--server.port", "8501"])
        process_manager.add_process(process)
        return process
    return None

def main():
    """Run both servers."""
    print("🚀 Starting Programmatic SEO Tool...")
    print("📡 FastAPI will run on http://localhost:8000")
    
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
    time.sleep(3)
    
    # Check which frontend to use
    if os.path.exists("package.json"):
        print("⚛️  Next.js will run on http://localhost:3000")
        nextjs_process = run_nextjs()
        if nextjs_process:
            # Wait a bit for Next.js to start
            time.sleep(5)
            webbrowser.open("http://localhost:3000")
            # Keep running
            try:
                nextjs_process.wait()
            except KeyboardInterrupt:
                pass
    elif os.path.exists("streamlit_app.py"):
        print("🎨 Streamlit will run on http://localhost:8501")
        streamlit_process = run_streamlit()
        if streamlit_process:
            time.sleep(2)
            webbrowser.open("http://localhost:8501")
            # Keep running
            try:
                streamlit_process.wait()
            except KeyboardInterrupt:
                pass
    else:
        print("\n⚠️  No frontend found!")
        print("Either:")
        print("  1. Run ./setup_frontend.sh to create the Next.js frontend")
        print("  2. Create streamlit_app.py for Streamlit UI")
        print("\nFastAPI is still running at http://localhost:8000")
        print("Press Ctrl+C to stop")
        
        # Keep FastAPI running
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            pass

if __name__ == "__main__":
    main()