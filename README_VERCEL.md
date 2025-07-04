# Vercel Deployment Guide

This is a lightweight version of the Programmatic SEO Tool optimized for Vercel deployment.

## Architecture

- **API**: Lightweight Python handlers on Vercel
- **Database**: Firebase Firestore (NoSQL)
- **Storage**: Firebase Storage for exports
- **Frontend**: Can be deployed separately or use API directly

## Setup Instructions

### 1. Firebase Setup

1. Create a Firebase project at https://console.firebase.google.com
2. Enable Firestore Database
3. Enable Firebase Storage
4. Get your configuration from Project Settings

### 2. Vercel Environment Variables

Add these to your Vercel project settings:

```
FIREBASE_API_KEY=your-api-key
FIREBASE_AUTH_DOMAIN=your-auth-domain
FIREBASE_PROJECT_ID=your-project-id
FIREBASE_STORAGE_BUCKET=your-storage-bucket
FIREBASE_MESSAGING_SENDER_ID=your-sender-id
FIREBASE_APP_ID=your-app-id
FIREBASE_DATABASE_URL=your-database-url

# AI providers (need at least one)
PerplexityAPI=your-perplexity-key
OPENAI_API_KEY=your-openai-key
ANTHROPIC_API_KEY=your-anthropic-key
```

### 3. Deploy to Vercel

```bash
vercel --prod
```

## API Endpoints

- `GET /` - API information
- `GET /health` - Health check
- `POST /api/analyze-business` - Analyze business from URL/description
- `POST /api/generate-keywords` - Generate keyword opportunities
- `POST /api/generate-content` - Generate content for keywords
- `POST /api/projects` - Create new project
- `GET /api/projects` - List projects

## Frontend Options

1. **Static HTML/JS**: Create a simple frontend that calls the API
2. **React/Next.js**: Deploy on Vercel alongside the API
3. **Streamlit**: Deploy separately on Streamlit Cloud
4. **Direct API**: Use tools like Postman or integrate with other services

## Data Structure in Firebase

### Projects Collection
```
projects/
  {projectId}/
    - name: string
    - businessInfo: object
    - createdAt: timestamp
    - status: string
```

### Keywords Collection
```
keywords/
  {keywordId}/
    - projectId: string
    - keyword: string
    - searchVolume: number
    - difficulty: number
    - intent: string
```

### Content Collection
```
content/
  {contentId}/
    - projectId: string
    - keywordId: string
    - title: string
    - content: string
    - metaDescription: string
    - status: string
```

## Limitations

- No heavy ML processing (use external APIs)
- File uploads limited to 4.5MB
- Function timeout: 10 seconds (Pro: 60 seconds)
- No persistent file storage (use Firebase Storage)

## Next Steps

1. Set up Firebase project
2. Add environment variables to Vercel
3. Deploy the API
4. Build a frontend or use the API directly
5. Gradually add features like AI content generation