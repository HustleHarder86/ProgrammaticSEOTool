#!/usr/bin/env python3
"""
Test production health and connectivity for Programmatic SEO Tool
"""

import requests
import json
import sys
from datetime import datetime

# Production URLs
FRONTEND_URL = "https://programmatic-seo-tool.vercel.app"
BACKEND_URL = "https://programmaticseotool-production.up.railway.app"

def test_production_health():
    """Test all production endpoints and connectivity"""
    
    print("🔍 Production Health Check for Programmatic SEO Tool")
    print("=" * 60)
    print(f"📅 Test Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🌐 Frontend: {FRONTEND_URL}")
    print(f"🚂 Backend: {BACKEND_URL}")
    print("=" * 60)
    
    all_tests_passed = True
    
    # 1. Test Backend Health
    print("\n1️⃣ Testing Backend Health...")
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=10)
        if response.status_code == 200:
            health_data = response.json()
            print(f"✅ Backend Status: {health_data.get('status', 'unknown')}")
            print(f"   - Database: {health_data.get('database', 'unknown')}")
            print(f"   - AI Providers: {health_data.get('ai_providers', 'unknown')}")
            if health_data.get('ai_error'):
                print(f"   ⚠️  AI Error: {health_data.get('ai_error')}")
        else:
            print(f"❌ Backend health check failed: Status {response.status_code}")
            all_tests_passed = False
    except Exception as e:
        print(f"❌ Cannot reach backend: {str(e)}")
        all_tests_passed = False
    
    # 2. Test Frontend Accessibility
    print("\n2️⃣ Testing Frontend Accessibility...")
    try:
        response = requests.get(FRONTEND_URL, timeout=10)
        if response.status_code == 200:
            print(f"✅ Frontend is accessible")
            # Check if it's the Next.js app
            if 'next' in response.headers.get('x-powered-by', '').lower():
                print(f"   - Powered by Next.js")
        else:
            print(f"❌ Frontend returned status: {response.status_code}")
            all_tests_passed = False
    except Exception as e:
        print(f"❌ Cannot reach frontend: {str(e)}")
        all_tests_passed = False
    
    # 3. Test CORS Configuration
    print("\n3️⃣ Testing CORS Configuration...")
    try:
        headers = {
            'Origin': FRONTEND_URL,
            'Referer': FRONTEND_URL
        }
        response = requests.get(f"{BACKEND_URL}/health", headers=headers, timeout=10)
        if response.status_code == 200:
            cors_headers = {
                'access-control-allow-origin': response.headers.get('access-control-allow-origin', 'Not set'),
                'access-control-allow-credentials': response.headers.get('access-control-allow-credentials', 'Not set')
            }
            print(f"✅ CORS headers present:")
            for header, value in cors_headers.items():
                print(f"   - {header}: {value}")
        else:
            print(f"❌ CORS request failed: Status {response.status_code}")
            all_tests_passed = False
    except Exception as e:
        print(f"❌ CORS test failed: {str(e)}")
        all_tests_passed = False
    
    # 4. Test Key API Endpoints
    print("\n4️⃣ Testing Key API Endpoints...")
    endpoints = [
        ("/api/test", "GET", "Test endpoint"),
        ("/api/projects", "GET", "List projects"),
        ("/docs", "GET", "API documentation")
    ]
    
    for endpoint, method, description in endpoints:
        try:
            url = f"{BACKEND_URL}{endpoint}"
            if method == "GET":
                response = requests.get(url, timeout=10)
            
            if response.status_code in [200, 307]:  # 307 for docs redirect
                print(f"✅ {description}: {endpoint} - Status {response.status_code}")
            else:
                print(f"❌ {description}: {endpoint} - Status {response.status_code}")
                all_tests_passed = False
        except Exception as e:
            print(f"❌ {description}: {endpoint} - Error: {str(e)}")
            all_tests_passed = False
    
    # 5. Test Business Analysis (with mock data)
    print("\n5️⃣ Testing Business Analysis Endpoint...")
    try:
        test_data = {
            "business_input": "Test real estate investment platform",
            "input_type": "text"
        }
        response = requests.post(
            f"{BACKEND_URL}/api/analyze-business",
            json=test_data,
            timeout=30
        )
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Business analysis working")
            print(f"   - Project ID: {result.get('project_id', 'N/A')}")
            print(f"   - Templates suggested: {len(result.get('template_opportunities', []))}")
        else:
            print(f"❌ Business analysis failed: Status {response.status_code}")
            if response.text:
                print(f"   Error: {response.text[:200]}")
            all_tests_passed = False
    except Exception as e:
        print(f"❌ Business analysis error: {str(e)}")
        all_tests_passed = False
    
    # 6. Summary
    print("\n" + "=" * 60)
    print("📊 PRODUCTION HEALTH SUMMARY")
    print("=" * 60)
    
    if all_tests_passed:
        print("✅ All production tests passed!")
        print("🚀 System appears to be working correctly")
    else:
        print("❌ Some tests failed - investigation needed")
        print("\n🔧 Recommended Actions:")
        print("1. Check Railway logs for backend errors")
        print("2. Verify environment variables on both platforms")
        print("3. Test with browser developer tools on frontend")
        print("4. Check database migrations in production")
    
    return all_tests_passed

def main():
    """Run production health check"""
    success = test_production_health()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()