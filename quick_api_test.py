#!/usr/bin/env python3
"""Quick API connectivity test"""

import requests
import json

def test_connections():
    print("🔍 Testing API Connections...\n")
    
    # Test Backend
    print("1. Backend API (http://localhost:8000)")
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("   ✅ Backend is running")
            print(f"   - Status: {data.get('status')}")
            print(f"   - Database: {data.get('database_status')}")
            print(f"   - Timestamp: {data.get('timestamp')}")
        else:
            print(f"   ❌ Backend returned status {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("   ❌ Backend is NOT running - Connection refused")
        print("   Run: cd backend && python3 -m uvicorn main:app --reload")
    except Exception as e:
        print(f"   ❌ Backend error: {e}")
    
    print("\n2. Frontend (http://localhost:3000)")
    try:
        response = requests.get("http://localhost:3000", timeout=5)
        if response.status_code == 200:
            print("   ✅ Frontend is running")
        else:
            print(f"   ❌ Frontend returned status {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("   ❌ Frontend is NOT running - Connection refused")
        print("   Run: npm run dev")
    except Exception as e:
        print(f"   ❌ Frontend error: {e}")
    
    print("\n3. Testing Frontend → Backend Connection")
    print("   Visit: http://localhost:3000/test-api")
    print("   This page will test if the frontend can reach the backend")
    
    print("\n4. Quick Business Analysis Test")
    try:
        test_data = {"business_input": "A test company that sells software"}
        response = requests.post(
            "http://localhost:8000/api/analyze-business",
            json=test_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        if response.status_code == 200:
            print("   ✅ Business analysis endpoint working")
            data = response.json()
            if data.get('template_suggestions'):
                print(f"   - Got {len(data['template_suggestions'])} template suggestions")
        else:
            print(f"   ❌ Business analysis returned status {response.status_code}")
            print(f"   - Response: {response.text[:200]}")
    except Exception as e:
        print(f"   ❌ Business analysis error: {e}")

if __name__ == "__main__":
    test_connections()