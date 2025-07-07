#!/usr/bin/env python3
"""Quick test to verify deployment status"""

import requests
import json
from datetime import datetime

def test_deployment():
    backend_url = "https://programmaticseotool-production.up.railway.app"
    frontend_url = "https://programmatic-seo-tool.vercel.app"
    
    print("="*50)
    print("DEPLOYMENT VERIFICATION TEST")
    print("="*50)
    print(f"Time: {datetime.utcnow().isoformat()}")
    print()
    
    # Test 1: Backend Health
    print("1. Testing Backend Health...")
    try:
        response = requests.get(f"{backend_url}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Backend is healthy")
            print(f"   - Database: {data.get('database', 'unknown')}")
            print(f"   - Service: {data.get('service', 'unknown')}")
        else:
            print(f"   ❌ Backend returned status: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Backend error: {str(e)}")
    
    # Test 2: API Test Endpoint
    print("\n2. Testing API Endpoint...")
    try:
        response = requests.get(f"{backend_url}/api/test", timeout=5)
        if response.status_code == 200:
            print(f"   ✅ API is working")
            print(f"   - Response: {response.json()}")
        else:
            print(f"   ❌ API returned status: {response.status_code}")
    except Exception as e:
        print(f"   ❌ API error: {str(e)}")
    
    # Test 3: Frontend
    print("\n3. Testing Frontend...")
    try:
        response = requests.get(frontend_url, timeout=10)
        if response.status_code == 200:
            print(f"   ✅ Frontend is accessible")
            print(f"   - Content length: {len(response.content)} bytes")
        else:
            print(f"   ❌ Frontend returned status: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Frontend error: {str(e)}")
    
    # Test 4: API Docs
    print("\n4. Testing API Documentation...")
    try:
        response = requests.get(f"{backend_url}/docs", timeout=5)
        if response.status_code == 200:
            print(f"   ✅ API docs are available")
            print(f"   - URL: {backend_url}/docs")
        else:
            print(f"   ❌ API docs returned status: {response.status_code}")
    except Exception as e:
        print(f"   ❌ API docs error: {str(e)}")
    
    print("\n" + "="*50)
    print("TEST COMPLETE")
    print("="*50)

if __name__ == "__main__":
    test_deployment()