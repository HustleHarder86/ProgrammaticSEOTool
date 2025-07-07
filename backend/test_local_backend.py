#!/usr/bin/env python3
"""Test script to verify backend functionality before Railway deployment"""
import requests
import json
import sys

# Test configuration
BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"✓ Health Check: {response.status_code}")
        print(f"  Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"✗ Health Check Failed: {e}")
        return False

def test_api():
    """Test basic API endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/api/test")
        print(f"\n✓ API Test: {response.status_code}")
        print(f"  Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"\n✗ API Test Failed: {e}")
        return False

def test_business_analysis():
    """Test business analysis endpoint"""
    try:
        payload = {
            "business_input": "Digital marketing agency specializing in SEO",
            "input_type": "text"
        }
        response = requests.post(
            f"{BASE_URL}/api/analyze-business",
            json=payload
        )
        print(f"\n✓ Business Analysis: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"  Project ID: {result.get('project_id')}")
            print(f"  Business Name: {result.get('business_name')}")
            print(f"  Template Opportunities: {len(result.get('template_opportunities', []))}")
        return response.status_code == 200
    except Exception as e:
        print(f"\n✗ Business Analysis Failed: {e}")
        return False

def test_projects():
    """Test projects endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/api/projects")
        print(f"\n✓ Projects List: {response.status_code}")
        print(f"  Projects Count: {len(response.json())}")
        return response.status_code == 200
    except Exception as e:
        print(f"\n✗ Projects List Failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Testing Backend API...")
    print("=" * 50)
    
    tests = [
        test_health,
        test_api,
        test_business_analysis,
        test_projects
    ]
    
    results = [test() for test in tests]
    
    print("\n" + "=" * 50)
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print(f"✅ All tests passed! ({passed}/{total})")
        print("\n🚀 Backend is ready for Railway deployment!")
    else:
        print(f"❌ Some tests failed: {passed}/{total} passed")
        print("\n⚠️  Fix issues before deploying to Railway")
        sys.exit(1)

if __name__ == "__main__":
    main()