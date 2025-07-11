#!/usr/bin/env python3
"""Simple test of ai_client"""

try:
    from ai_client import AIClient
    print("✅ Import successful")
    
    client = AIClient()
    print("✅ Client created")
    
    result = client.analyze_business("Test company")
    print("✅ Analysis completed")
    print(f"Result: {result}")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()