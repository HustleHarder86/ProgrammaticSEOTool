#!/usr/bin/env python3
"""
Monitor backend logs in real-time.
Helps identify issues during page generation testing.
"""

import subprocess
import sys
import time
import signal

def signal_handler(sig, frame):
    print('\n\nStopping log monitoring...')
    sys.exit(0)

def monitor_logs():
    """Monitor backend logs using tail."""
    print("Monitoring backend logs...")
    print("Press Ctrl+C to stop\n")
    print("="*60)
    
    signal.signal(signal.SIGINT, signal_handler)
    
    try:
        # Find the uvicorn process and monitor its output
        cmd = ["tail", "-f", "-n", "50", "/proc/264540/fd/1", "/proc/264540/fd/2"]
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        
        for line in iter(process.stdout.readline, ''):
            if line:
                # Highlight important lines
                if "ERROR" in line or "Exception" in line:
                    print(f"❌ {line.strip()}")
                elif "DEBUG" in line:
                    print(f"🔍 {line.strip()}")
                elif "Generated" in line or "SUCCESS" in line:
                    print(f"✅ {line.strip()}")
                else:
                    print(line.strip())
    except Exception as e:
        print(f"Error monitoring logs: {e}")
        print("\nAlternative: Run this command in a separate terminal:")
        print("tail -f /proc/$(pgrep -f 'uvicorn main:app')/fd/1 2>/dev/null")

if __name__ == "__main__":
    monitor_logs()