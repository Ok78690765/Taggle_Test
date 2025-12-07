# Environment Variables & Secrets Management

This guide documents all environment variables used across the monorepo, their purposes, default values, and where they should be configured in different deployment environments.

## Table of Contents

- [Overview](#overview)
- [Quick Start](#quick-start)
- [Environment Variable Reference](#environment-variable-reference)
- [Deployment Topology](#deployment-topology)
- [Local Development](#local-development)
- [Production Deployment](#production-deployment)
- [Secrets Rotation](#secrets-rotation)
- [Troubleshooting](#troubleshooting)

## Overview

The monorepo consists of three main components:

- **Backend** (FastAPI) - Runs on port 8000, handles API requests
- **Frontend** (Next.js) - Runs on port 3000, serves the web UI
- **Shared** - Docker Compose configuration for local development

Environment variables are managed differently depending on the deployment target:

| Location | Purpose | Sensitivity |
|----------|---------|------------|
| `backend/.env.example` | Backend configuration template | High (contains secrets) |
| `frontend/.env.example` | Frontend configuration template | Medium (exposed to browser) |
| `shared/.env.example` | Shared Docker Compose config | Medium (local dev only) |
| Vercel Dashboard | Production frontend environment vars | High |
| Railway Dashboard | Production backend environment vars | High |
| `.env` / `.env.local` | Local development files | High (never commit) |

## Quick Start

### Local Development

1. **Backend** (`backend/` directory):
   ```bash
   cp backend/.env.example backend/.env
   # Edit backend/.env with your local settings
   poetry run uvicorn app.main:app --reload
   ```

2. **Frontend** (`frontend/` directory):
   ```bash
   cp frontend/.env.example frontend/.env.local
   # Edit frontend/.env.local with your local settings
   npm run dev
   ```

3. **Docker Compose**:
   ```bash
   cp shared/.env.example .env
   # Edit .env with your local settings
   docker-compose -f shared/docker-compose.yml up
   ```

### Production Deployment

- **Backend**: Set environment variables in Railway dashboard
- **Frontend**: Set environment variables in Vercel dashboard
- See [Production Deployment](#production-deployment) section below

## Environment Variable Reference

### Critical Variables (Frontend ↔ Backend Connection)

These variables establish the communication path between frontend and backend:

| Variable | Owner | Purpose | Default | Storage | Notes |
|----------|-------|---------|---------|---------|-------|
| `NEXT_PUBLIC_API_URL` | Frontend | URL where frontend calls backend API | `http://localhost:8000` | Frontend `.env.local` or Vercel | **CRITICAL**: Must match backend's actual URL. Used by browser. |
| `BACKEND_URL` | Shared | Backend URL for docker-compose | `http://localhost:8000` | Shared `.env` | Internal reference, not used directly by apps |
| `CORS_ORIGINS` | Backend | Allowed frontend URLs for CORS | `http://localhost:3000,http://localhost:5173` | Backend `.env` or Railway | Frontend origin must be listed here |

### Backend Variables (FastAPI)

| Variable | Purpose | Type | Default | Required | Production Notes |
|----------|---------|------|---------|----------|------------------|
| `APP_NAME` | Application display name | String | `FastAPI Backend` | No | Informational only |
| `APP_VERSION` | Application version | String | `0.1.0` | No | Informational only |
| `ENVIRONMENT` | Deployment environment | String (development/staging/production) | `development` | Yes | Set to `production` in Railway. Controls `DEBUG` and `LOG_LEVEL` defaults |
| `DEBUG` | Enable debug mode & auto-reload | Boolean | Auto-set (true in dev, false in prod) | No | Automatically set based on `ENVIRONMENT` |
| `LOG_LEVEL` | Logging verbosity | String (DEBUG/INFO/WARNING/ERROR) | Auto-set (DEBUG in dev, INFO in prod) | No | Automatically set based on `ENVIRONMENT` |
| `BACKEND_HOST` | Server bind address | String | `0.0.0.0` | Yes | `0.0.0.0` for Docker, `127.0.0.1` for local |
| `PORT` | Server listen port | Integer | `8000` | Yes | **PREFERRED**: Railway injects this. Falls back to `BACKEND_PORT` |
| `BACKEND_PORT` | Server listen port (fallback) | Integer | `8000` | No | Used if `PORT` is not set |
| `DATABASE_URL` | Database connection string | String (URI) | `sqlite:///./test.db` | Yes | **Sensitive**: Use platform-provided values in production |
| `SECRET_KEY` | Token/session signing key | String (32+ chars) | `your-secret-key-...` | Yes | **CRITICAL**: Generate strong random value in production |
| `CORS_ORIGINS` | Allowed frontend origins | String (comma-separated) | `http://localhost:3000,http://localhost:5173` | Yes | **Format**: No spaces after commas. Production: set to Vercel frontend URL |
| `API_KEY` | Internal API key (if used) | String | `your-api-key-...` | No | **Sensitive**: Change in production |
| `ENABLE_API_DOCS` | Enable FastAPI docs endpoint | Boolean | `true` | No | Set to `false` in production |

### Frontend Variables (Next.js)

| Variable | Purpose | Type | Default | Required | Production Notes |
|----------|---------|------|---------|----------|------------------|
| `NEXT_PUBLIC_API_URL` | Backend API URL | String (URL) | `http://localhost:8000` | Yes | **CRITICAL**: Set in Vercel to Railway API URL |
| `NEXT_PUBLIC_APP_NAME` | App display name | String | `Agent Console` | No | Used in UI header |
| `NEXT_PUBLIC_APP_VERSION` | App version | String | `1.0.0` | No | Displayed in UI |
| `NODE_ENV` | Node environment | String (development/production) | `development` | Yes | Always `production` in Vercel build |
| `NEXT_PUBLIC_ANALYTICS_ID` | Google Analytics ID | String | (empty) | No | Optional, for analytics tracking |
| `NEXT_PUBLIC_SENTRY_DSN` | Sentry error tracking URL | String (URL) | (empty) | No | Optional, for error monitoring |

### Shared Variables (Docker Compose)

| Variable | Purpose | Type | Default | Notes |
|----------|---------|------|---------|-------|
| `APP_NAME` | Application name | String | `Agent Console` | Informational |
| `ENVIRONMENT` | Deployment env | String | `development` | For both services |
| `DEBUG` | Debug mode | Boolean | `false` | Affects both services |
| `BACKEND_HOST` | Backend bind address | String | `localhost` | See backend docs |
| `BACKEND_PORT` | Backend port | Integer | `8000` | See backend docs |
| `BACKEND_URL` | Backend full URL | String | `http://localhost:8000` | Internal ref |
| `FRONTEND_HOST` | Frontend bind address | String | `localhost` | Internal use |
| `FRONTEND_PORT` | Frontend port | Integer | `3000` | See frontend docs |
| `FRONTEND_URL` | Frontend full URL | String | `http://localhost:3000` | Internal ref |
| `DATABASE_URL` | Database URI | String | `sqlite:///./test.db` | See backend docs |
| `SECRET_KEY` | Session/token signing key | String | `your-secret-key-...` | See backend docs |
| `CORS_ORIGINS` | Allowed CORS origins | String | `http://localhost:3000,http://localhost:5173` | See backend docs |
| `LOG_LEVEL` | Logging level | String | `INFO` | See backend docs |
| `API_KEY` | Internal API key | String | `your-api-key-...` | See backend docs |
| `ENABLE_API_DOCS` | Enable API docs endpoint | Boolean | `true` | See backend docs |

## Deployment Topology

### Local Development

```
┌─────────────────────────────────────────────────────────┐
│ Your Computer                                           │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Frontend (Next.js)           Backend (FastAPI)        │
│  http://localhost:3000        http://localhost:8000    │
│  Port: 3000                   Port: 8000               │
│  .env.local                   .env                     │
│                               test.db (SQLite)         │
│  NEXT_PUBLIC_API_URL=          DATABASE_URL=           │
│  http://localhost:8000        sqlite:///./test.db     │
│                                                        │
│  Browser makes requests:                               │
│  http://localhost:3000 → (NEXT_PUBLIC_API_URL)         │
│                        → http://localhost:8000/api/... │
│                                                        │
└─────────────────────────────────────────────────────────┘
```

### Production Deployment (Recommended)

```
┌───────────────────────────────────────────────────────────────────┐
│ Internet / CDN                                                    │
├───────────────────────────────────────────────────────────────────┤
│                           │                                        │
│                           ▼                                        │
│                    Vercel (Frontend)                               │
│                    https://app.example.com                         │
│                                                                    │
│  Environment Variables (Vercel Dashboard):                        │
│  - NEXT_PUBLIC_API_URL=https://api.railway.app                   │
│  - NEXT_PUBLIC_APP_NAME=Agent Console                             │
│  - NEXT_PUBLIC_APP_VERSION=1.0.0                                  │
│                                                                    │
│  Browser Requests:                                                │
│  https://app.example.com → (NEXT_PUBLIC_API_URL)                 │
│                          → https://api.railway.app/api/...       │
│                                                                    │
│                           │                                        │
│                           ▼                                        │
│                    Railway (Backend)                               │
│                    https://api.railway.app                         │
│                                                                    │
│  Environment Variables (Railway Dashboard):                       │
│  - BACKEND_HOST=0.0.0.0                                          │
│  - PORT=8000 (Railway assigns port)                              │
│  - CORS_ORIGINS=https://app.example.com                          │
│  - DATABASE_URL=postgresql://... (provided by Railway)           │
│  - SECRET_KEY=<strong-random-key> (set in dashboard)             │
│                                                                    │
│                           │                                        │
│                           ▼                                        │
│                    PostgreSQL Database                             │
│                    (Railway managed)                               │
│                                                                    │
└───────────────────────────────────────────────────────────────────┘
```

## Local Development

### Setup Steps

1. **Create backend configuration**:
   ```bash
   cd backend
   cp .env.example .env
   ```
   
   Edit `backend/.env` to match your local setup:
   ```env
   ENVIRONMENT=development
   DEBUG=true
   BACKEND_HOST=127.0.0.1
   BACKEND_PORT=8000
   DATABASE_URL=sqlite:///./test.db
   SECRET_KEY=dev-key-change-in-production
   CORS_ORIGINS=http://localhost:3000
   LOG_LEVEL=INFO
   ```

2. **Create frontend configuration**:
   ```bash
   cd frontend
   cp .env.example .env.local
   ```
   
   Edit `frontend/.env.local`:
   ```env
   NEXT_PUBLIC_API_URL=http://localhost:8000
   NEXT_PUBLIC_APP_NAME=Agent Console
   NODE_ENV=development
   ```

3. **Create shared configuration** (for Docker):
   ```bash
   cd ..  # Root directory
   cp shared/.env.example .env
   ```
   
   Edit `.env` (at root):
   ```env
   ENVIRONMENT=development
   DEBUG=true
   BACKEND_HOST=localhost
   BACKEND_PORT=8000
   BACKEND_URL=http://localhost:8000
   FRONTEND_HOST=localhost
   FRONTEND_PORT=3000
   FRONTEND_URL=http://localhost:3000
   NEXT_PUBLIC_API_URL=http://localhost:8000
   DATABASE_URL=sqlite:///./test.db
   SECRET_KEY=dev-key-change-in-production
   CORS_ORIGINS=http://localhost:3000
   ```

### Running Services

**Option A: Manual (with auto-reload)**:
```bash
# Terminal 1: Backend
cd backend
poetry install
poetry run uvicorn app.main:app --reload

# Terminal 2: Frontend
cd frontend
npm install
npm run dev
```

**Option B: Docker Compose**:
```bash
# Root directory
docker-compose -f shared/docker-compose.yml up
```

### Verifying the Connection

1. Open browser to `http://localhost:3000`
2. Frontend should load
3. Click "Test Connection" button (or try to login)
4. Should successfully reach backend health endpoint
5. If connection fails, check `NEXT_PUBLIC_API_URL` in `frontend/.env.local`

## Production Deployment

### Railway Backend Setup

1. **Create Railway app** for backend:
   - Log in to [Railway](https://railway.app/)
   - Click "New Project" → "Deploy from GitHub repo"
   - Authorize Railway and select your repository
   - Railway will automatically detect the `railway.toml` configuration

2. **Provision PostgreSQL** (optional):
   - In your Railway project dashboard, click "New" → "Database" → "Add PostgreSQL"
   - Railway automatically sets the `DATABASE_URL` environment variable
   - No manual configuration needed

3. **Set environment variables in Railway dashboard**:
   - Navigate to your Railway project → Variables
   - Set each variable (copy from `backend/.env.example`):
   
   ```
   ENVIRONMENT=production
   SECRET_KEY=<generate strong key: python -c "import secrets; print(secrets.token_urlsafe(32))">
   CORS_ORIGINS=https://your-vercel-url.vercel.app
   ```
   
   **Optional Variables**:
   ```
   ENABLE_API_DOCS=false  # Disable in production
   ```
   
   **Note**: 
   - Railway automatically provides `PORT` (no need to set manually)
   - `DEBUG` and `LOG_LEVEL` are auto-set based on `ENVIRONMENT=production`
   - If you provisioned PostgreSQL, `DATABASE_URL` is set automatically
   
4. **Deploy**:
   - Railway automatically builds and deploys using `railway.toml` configuration
   - Monitor deployment logs in the "Deployments" tab
   - Health checks run against the `/health` endpoint

5. **Get your API URL**: 
   - Go to your service's "Settings" tab → "Domains"
   - Railway provides a URL like `https://myapp-backend-production.up.railway.app`
   - Copy this URL for use in your frontend's `NEXT_PUBLIC_API_URL`

### Vercel Frontend Setup

1. **Connect Vercel project**:
   ```bash
   # From frontend directory
   vercel link  # or create new project
   vercel env add NEXT_PUBLIC_API_URL
   # Enter: https://your-railway-api-url  (from Railway dashboard)
   ```

2. **Set environment variables in Vercel dashboard**:
   - Navigate to Settings → Environment Variables
   - Add each variable:
   
   ```
   NEXT_PUBLIC_API_URL = https://your-railway-api-url
   NEXT_PUBLIC_APP_NAME = Agent Console
   NEXT_PUBLIC_APP_VERSION = 1.0.0
   ```

3. **Deploy**:
   ```bash
   vercel --prod
   ```

### Secret Synchronization

When deploying, ensure:

1. **CORS Origins Match**:
   - Backend `CORS_ORIGINS` (Railway) = Frontend URL (Vercel)
   - Example: If Vercel URL is `https://app.example.com`, set in Railway:
     ```
     CORS_ORIGINS=https://app.example.com
     ```

2. **Backend URL Matches**:
   - Frontend `NEXT_PUBLIC_API_URL` (Vercel) = Backend URL (Railway)
   - Example: If Railway URL is `https://api.railway.app`, set in Vercel:
     ```
     NEXT_PUBLIC_API_URL=https://api.railway.app
     ```

3. **Database is Ready**:
   - Railway PostgreSQL must be created before deploying backend
   - Migrations run automatically on first deployment

## Secrets Rotation

### Rotating SECRET_KEY

`SECRET_KEY` is used to sign sessions and tokens. To rotate safely:

1. **Plan**: Existing sessions/tokens will be invalidated (users must re-login)
2. **Generate new key**:
   ```bash
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```
3. **Update locally** first:
   - Edit `backend/.env` with new key
   - Test thoroughly
4. **Update production**:
   - Railway dashboard → Variables
   - Paste new `SECRET_KEY`
   - Deployment restarts with new key
5. **Notify users**: Sessions are invalidated; users need to login again

### Rotating DATABASE_URL

For production PostgreSQL changes:

1. **Do not change** `DATABASE_URL` unless migrating databases
2. **To migrate**:
   - Create new database (Railway handles this)
   - Export data from old database
   - Import to new database
   - Update `DATABASE_URL` in Railway dashboard
   - Restart services
   - Verify data integrity

### Rotating API_KEY (if used)

If your backend uses API keys for external integrations:

1. Generate new key
2. Update in Railway dashboard
3. Services restart automatically

### Rotating CORS_ORIGINS

When changing frontend URL or adding new frontend:

1. Update `CORS_ORIGINS` in Railway dashboard
2. Add all valid frontend URLs (comma-separated)
3. Services restart automatically
4. Verify frontend can reach backend

## Troubleshooting

### "Failed to reach the backend API"

**Symptom**: Frontend shows error when trying to connect to backend

**Causes & Solutions**:

1. **Wrong `NEXT_PUBLIC_API_URL`**:
   - Local dev: Should be `http://localhost:8000`
   - Production: Should be Railway API URL, not frontend URL
   - Check: Open browser console, see what URL requests are going to
   
2. **Backend not running**:
   - Local: Run `poetry run uvicorn app.main:app --reload` in backend dir
   - Production: Check Railway dashboard for service status
   
3. **CORS blocked**:
   - Backend must have frontend URL in `CORS_ORIGINS`
   - Check browser console for CORS error
   - Update backend's `CORS_ORIGINS` variable
   
4. **Network/Firewall**:
   - Can you ping the backend URL from your computer?
   - Are you behind a corporate firewall?

### "DATABASE_URL invalid"

**Symptom**: Backend crashes with database connection error

**Causes & Solutions**:

1. **SQLite file missing** (local dev):
   - `backend/.env` has `DATABASE_URL=sqlite:///./test.db`
   - File will be created automatically on first run
   
2. **PostgreSQL not running** (local dev):
   - If using PostgreSQL: `docker-compose up postgres`
   - Update `DATABASE_URL` to match your setup
   
3. **Invalid connection string** (production):
   - Railway provides correct `DATABASE_URL` automatically
   - Do not manually edit in production

### "Port already in use"

**Symptom**: Backend or frontend won't start, "address already in use"

**Solutions**:

1. **Kill existing process**:
   ```bash
   # Port 8000 (backend)
   lsof -ti:8000 | xargs kill -9
   
   # Port 3000 (frontend)
   lsof -ti:3000 | xargs kill -9
   ```

2. **Use different port**:
   - Edit `BACKEND_PORT` or `FRONTEND_PORT` in respective `.env`
   - Update `NEXT_PUBLIC_API_URL` in frontend if changing backend port

### "SECRET_KEY not strong enough"

**Symptom**: Security warning in logs

**Solution**:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Use the generated 32+ character string in `SECRET_KEY`

### Environment variables not loading

**Symptom**: Variables seem to be using defaults despite setting them

**Causes & Solutions**:

1. **File not in right location**:
   - Backend: `backend/.env` (not `backend/.env.local`)
   - Frontend: `frontend/.env.local` (not `frontend/.env`)
   - Shared: `.env` at repository root
   
2. **Not restarted services**:
   - After editing `.env`, restart the service
   - Env vars are loaded at startup only
   
3. **Wrong syntax**:
   - No spaces around `=`: `KEY=value` (correct)
   - No spaces around `=`: `KEY = value` (incorrect)
   - No quotes needed unless value contains spaces
   
4. **Vercel/Railway not redeployed**:
   - After changing vars in dashboard, service must be restarted
   - Usually happens automatically, but may need manual restart

---

## Summary Checklist

### Local Development

- [ ] Copy `.env.example` to `.env` in each directory
- [ ] Update `NEXT_PUBLIC_API_URL` to backend URL
- [ ] Ensure `CORS_ORIGINS` includes frontend URL
- [ ] Backend and frontend can reach each other
- [ ] Database file/connection works
- [ ] Test connection in UI succeeds

### Production (Railway + Vercel)

- [ ] Backend deployed to Railway
- [ ] Frontend deployed to Vercel
- [ ] `NEXT_PUBLIC_API_URL` in Vercel = Railway API URL
- [ ] `CORS_ORIGINS` in Railway = Vercel frontend URL
- [ ] `SECRET_KEY` is strong random value (not default)
- [ ] Database is created and accessible
- [ ] API docs disabled on production backend (`ENABLE_API_DOCS=false`)
- [ ] Debug mode disabled (`DEBUG=false`)
- [ ] Test login flow end-to-end

---

## Additional Resources

- [FastAPI Environment Variables](https://fastapi.tiangolo.com/advanced/settings/)
- [Next.js Environment Variables](https://nextjs.org/docs/basic-features/environment-variables)
- [Railway Environment Variables](https://docs.railway.app/deploy/environment-variables)
- [Vercel Environment Variables](https://vercel.com/docs/projects/environment-variables)
- [Pydantic Settings](https://docs.pydantic.dev/latest/concepts/settings/)
