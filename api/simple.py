"""Ultra-simple API for Vercel testing"""

def handler(request):
    """Simple HTTP handler for Vercel"""
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': {
            'message': 'Programmatic SEO Tool API is running!',
            'status': 'healthy',
            'endpoints': [
                'GET /',
                'GET /health',
                'POST /api/analyze-business',
                'POST /api/generate-keywords',
                'POST /api/generate-content',
                'POST /api/export'
            ]
        }
    }