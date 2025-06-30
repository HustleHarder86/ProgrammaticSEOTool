"""Firebase configuration for Vercel deployment"""
import os
import json

def get_firebase_config():
    """Get Firebase configuration from environment variables"""
    # Firebase config should be stored in Vercel environment variables
    config = {
        'apiKey': os.environ.get('FIREBASE_API_KEY', ''),
        'authDomain': os.environ.get('FIREBASE_AUTH_DOMAIN', ''),
        'projectId': os.environ.get('FIREBASE_PROJECT_ID', ''),
        'storageBucket': os.environ.get('FIREBASE_STORAGE_BUCKET', ''),
        'messagingSenderId': os.environ.get('FIREBASE_MESSAGING_SENDER_ID', ''),
        'appId': os.environ.get('FIREBASE_APP_ID', ''),
        'databaseURL': os.environ.get('FIREBASE_DATABASE_URL', '')
    }
    
    # Alternative: Load from FIREBASE_CONFIG JSON string
    firebase_config_json = os.environ.get('FIREBASE_CONFIG')
    if firebase_config_json:
        try:
            config = json.loads(firebase_config_json)
        except:
            pass
    
    return config

def init_firebase():
    """Initialize Firebase (lightweight version for Vercel)"""
    config = get_firebase_config()
    
    # Return config for client-side initialization
    # Heavy Firebase Admin SDK avoided to keep function small
    return {
        'initialized': bool(config.get('apiKey')),
        'projectId': config.get('projectId', 'not-configured')
    }

# Environment variables to set in Vercel:
# FIREBASE_API_KEY
# FIREBASE_AUTH_DOMAIN
# FIREBASE_PROJECT_ID
# FIREBASE_STORAGE_BUCKET
# FIREBASE_MESSAGING_SENDER_ID
# FIREBASE_APP_ID
# FIREBASE_DATABASE_URL

# Or set a single FIREBASE_CONFIG with the full JSON configuration