# Railway Database Persistence Issue

## Problem
SQLite databases on Railway are NOT persistent between deployments. The database file is stored in the container's filesystem, which gets wiped on each deployment.

## Current Status
- Using SQLite: `sqlite:///./programmatic_seo.db`
- Database is recreated empty on each deployment
- All data is lost when Railway redeploys

## Solutions

### Option 1: Use Railway PostgreSQL (Recommended)
1. Add PostgreSQL plugin in Railway dashboard
2. Railway will automatically set DATABASE_URL environment variable
3. Database will detect PostgreSQL URL and use it automatically

### Option 2: Use External PostgreSQL
1. Use a service like Supabase, Neon, or ElephantSQL
2. Set DATABASE_URL in Railway environment variables

### Option 3: Development Mode
1. Use the `/debug/seed-test-data` endpoint to create test data after each deployment
2. This is only for testing, not production use

## To Switch to PostgreSQL
1. Add PostgreSQL in Railway dashboard
2. The app will automatically use it (no code changes needed)
3. All data will persist between deployments