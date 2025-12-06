# GitHub OAuth Setup Guide

This document provides comprehensive instructions for setting up GitHub OAuth integration and repository synchronization in the FastAPI + Next.js application.

## Table of Contents

1. [GitHub OAuth Application Setup](#github-oauth-application-setup)
2. [Environment Variables Configuration](#environment-variables-configuration)
3. [Backend API Endpoints](#backend-api-endpoints)
4. [Frontend Integration](#frontend-integration)
5. [Repository Synchronization](#repository-synchronization)
6. [Webhook Configuration](#webhook-configuration)
7. [Troubleshooting](#troubleshooting)

## GitHub OAuth Application Setup

### Step 1: Create a GitHub OAuth Application

1. Go to [GitHub Developer Settings](https://github.com/settings/developers)
2. Click on "New OAuth App" or navigate to "OAuth Apps" → "New OAuth App"
3. Fill in the application details:
   - **Application name**: Your app name (e.g., "Code Analyzer")
   - **Homepage URL**: `http://localhost:3000` (for development)
   - **Authorization callback URL**: `http://localhost:3000/auth/github/callback`

### Step 2: Get Client ID and Client Secret

1. After creating the OAuth app, you'll see the "Client ID"
2. Click "Generate a new client secret" to create the Client Secret
3. **Important**: Save these credentials securely - the Client Secret will only be shown once

### Step 3: Update Redirect URI for Production

For production deployment, update the Authorization callback URL to:
- `https://yourdomain.com/auth/github/callback`

Then update the `GITHUB_REDIRECT_URI` environment variable accordingly.

## Environment Variables Configuration

### Backend Environment Variables

Add the following to your `.env` file in the root directory:

```bash
# GitHub OAuth Configuration
GITHUB_CLIENT_ID=your-client-id-from-github
GITHUB_CLIENT_SECRET=your-client-secret-from-github
GITHUB_REDIRECT_URI=http://localhost:3000/auth/github/callback

# Security (must be at least 32 characters)
SECRET_KEY=your-secret-key-here-change-in-production-min-32-chars!!!
SESSION_SECRET_KEY=session-secret-key-change-in-production-min-32-chars!!!

# Backend URL (for webhooks)
BACKEND_URL=http://localhost:8000

# Repository Storage
REPOS_MIRROR_PATH=/tmp/github_mirrors
```

### Frontend Environment Variables

Make sure these are set in your `.env.local` (frontend):

```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

Or add to the root `.env` file:
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Backend API Endpoints

### Authentication Endpoints

#### Get OAuth URL
```
GET /api/github/auth/oauth-url
Response: { "oauth_url": "https://github.com/login/oauth/authorize?..." }
```

#### OAuth Callback Handler
```
POST /api/github/auth/callback
Request Body: { "code": "authorization_code", "state": "optional_state" }
Response: {
  "success": true,
  "user_id": 123,
  "username": "github_username",
  "message": "Authentication successful"
}
```

### User Endpoints

#### Get User Info
```
GET /api/github/user/{user_id}
Response: {
  "id": 123,
  "user_id": 456789,
  "username": "github_username",
  "email": "user@example.com",
  "avatar_url": "https://avatars.githubusercontent.com/...",
  "last_synced_at": "2024-01-01T12:00:00",
  "sync_status": "completed",
  "created_at": "2024-01-01T10:00:00",
  "updated_at": "2024-01-01T12:00:00"
}
```

### Repository Endpoints

#### Sync Repositories
Fetches all repositories from GitHub and stores them in the database.
```
POST /api/github/repositories/sync/{user_id}
Response: {
  "success": true,
  "total_repositories": 42,
  "new_repositories": 5,
  "message": "Repository sync completed"
}
```

#### List Repositories
```
GET /api/github/repositories/{user_id}?selected_only=false
Response: {
  "total_count": 42,
  "repositories": [
    {
      "id": 1,
      "repo_id": 789456,
      "repo_name": "my-repo",
      "repo_full_name": "username/my-repo",
      "repo_url": "https://github.com/username/my-repo",
      "description": "Repository description",
      "is_private": false,
      "selected_for_sync": true,
      "mirror_path": "/tmp/github_mirrors/username_my-repo",
      "last_synced_at": "2024-01-01T12:00:00",
      "sync_status": "synced",
      "webhook_id": "12345678",
      "created_at": "2024-01-01T10:00:00",
      "updated_at": "2024-01-01T12:00:00"
    }
  ]
}
```

#### Toggle Repository Selection
```
PUT /api/github/repositories/{repo_id}/select?selected=true
Response: {
  "success": true,
  "repo_id": 1,
  "selected": true,
  "message": "Repository selection updated"
}
```

#### Clone Repository
Creates a mirror clone of the repository locally.
```
POST /api/github/repositories/{repo_id}/clone
Response: {
  "status": "synced",
  "last_synced_at": "2024-01-01T12:00:00",
  "message": "Repository cloned successfully"
}
```

#### Update Repository
Fetches the latest changes from the GitHub repository.
```
POST /api/github/repositories/{repo_id}/update
Response: {
  "status": "synced",
  "last_synced_at": "2024-01-01T12:00:00",
  "message": "Repository updated successfully"
}
```

#### Get Repository Sync Status
```
GET /api/github/repositories/{repo_id}/status
Response: {
  "status": "synced",
  "last_synced_at": "2024-01-01T12:00:00",
  "message": "Status: synced"
}
```

### File Tree and Code Inspection

#### Get File Tree
Returns the directory structure of a repository.
```
GET /api/github/repositories/{repo_id}/files
Response: {
  "root": {
    "path": "/",
    "type": "directory",
    "children": [
      {
        "path": "/src",
        "type": "directory",
        "children": [...]
      },
      {
        "path": "/README.md",
        "type": "file",
        "size": 1024
      }
    ]
  },
  "total_files": 156,
  "total_size": 5242880
}
```

#### Inspect Code File
Retrieves the content of a specific file.
```
POST /api/github/repositories/{repo_id}/inspect
Request Body: { "file_path": "/src/main.py", "repo_id": 1 }
Response: {
  "file_path": "/src/main.py",
  "content": "# Python file content\n...",
  "language": "python",
  "size": 2048,
  "created_at": "2024-01-01T10:00:00",
  "updated_at": "2024-01-01T10:00:00"
}
```

### Webhook Endpoints

#### Create Webhook
```
POST /api/github/repositories/{repo_id}/webhook
Response: {
  "success": true,
  "webhook_id": "12345678"
}
```

#### Handle Push Webhook
```
POST /api/github/webhook/push
Request Body: { GitHub webhook payload }
Response: {
  "success": true,
  "message": "Repository updated via webhook"
}
```

## Frontend Integration

### 1. Connect GitHub Account

Users can initiate OAuth connection through the Connect button on `/github` page:

```typescript
const oauthUrl = await GitHubAuth.getOAuthUrl();
window.location.href = oauthUrl;
```

### 2. OAuth Callback

The callback handler at `/auth/github/callback` processes the authorization code and stores the user session.

### 3. Repository Management

Users can:
- Sync repositories from GitHub
- Select repositories for synchronization
- Clone/mirror selected repositories
- Update repository mirrors
- Browse repository files
- Inspect code files

### Usage Example

```typescript
import { GitHubAuth } from '@/lib/github-auth';
import { RepositoryService } from '@/lib/repository-service';

// Check authentication
if (GitHubAuth.isAuthenticated()) {
  const userId = GitHubAuth.getCurrentUserId();
  
  // Sync repositories
  await RepositoryService.syncRepositories(userId);
  
  // List repositories
  const repos = await RepositoryService.listRepositories(userId);
  
  // Clone a repository
  await RepositoryService.cloneRepository(repoId);
  
  // Get file tree
  const fileTree = await RepositoryService.getFileTree(repoId);
  
  // Inspect code file
  const code = await RepositoryService.inspectCodeFile(repoId, '/src/main.py');
}
```

## Repository Synchronization

### Mirror Repositories

Repositories are mirrored to the local filesystem at `REPOS_MIRROR_PATH` for efficient access and analysis:

```
/tmp/github_mirrors/
├── username_repo1/
│   ├── .git/
│   ├── src/
│   ├── README.md
│   └── ...
└── username_repo2/
    ├── .git/
    ├── src/
    └── ...
```

### Sync Status Values

- **pending**: Waiting to be synced
- **cloning**: Currently cloning repository
- **updating**: Currently updating repository
- **synced**: Successfully synced and ready for analysis
- **failed**: Sync operation failed

### Token Encryption

GitHub OAuth tokens are encrypted using Fernet (symmetric encryption) before storage in the database:

```python
from app.utils.encryption import token_encryption

# Encrypt token for storage
encrypted_token = token_encryption.encrypt(access_token)

# Decrypt token for use
access_token = token_encryption.decrypt(encrypted_token)
```

## Webhook Configuration

Webhooks allow real-time updates when repositories are pushed to GitHub.

### Setting Up Webhooks

1. After cloning a repository, create a webhook:
```
POST /api/github/repositories/{repo_id}/webhook
```

2. GitHub will send `push` and `pull_request` events to:
```
http://your-backend-url/api/github/webhook/push
```

3. The webhook handler automatically updates the local mirror when changes are pushed.

### Webhook Events Monitored

- **push**: Code pushed to repository
- **pull_request**: Pull request created/updated

## Database Schema

### github_users table
```sql
CREATE TABLE github_users (
  id INTEGER PRIMARY KEY,
  user_id INTEGER UNIQUE NOT NULL,
  username VARCHAR(255) UNIQUE NOT NULL,
  email VARCHAR(255),
  avatar_url VARCHAR(512),
  encrypted_token TEXT NOT NULL,
  token_expires_at DATETIME,
  last_synced_at DATETIME,
  sync_status VARCHAR(50),
  created_at DATETIME NOT NULL,
  updated_at DATETIME NOT NULL
);
```

### github_repositories table
```sql
CREATE TABLE github_repositories (
  id INTEGER PRIMARY KEY,
  github_user_id INTEGER NOT NULL,
  repo_id INTEGER NOT NULL,
  repo_name VARCHAR(255) NOT NULL,
  repo_full_name VARCHAR(512) UNIQUE NOT NULL,
  repo_url VARCHAR(512) NOT NULL,
  description TEXT,
  is_private BOOLEAN DEFAULT FALSE,
  mirror_path VARCHAR(512),
  selected_for_sync BOOLEAN DEFAULT FALSE,
  last_synced_at DATETIME,
  sync_status VARCHAR(50),
  webhook_id VARCHAR(255),
  created_at DATETIME NOT NULL,
  updated_at DATETIME NOT NULL,
  FOREIGN KEY (github_user_id) REFERENCES github_users(id)
);
```

### sync_logs table
```sql
CREATE TABLE sync_logs (
  id INTEGER PRIMARY KEY,
  github_repository_id INTEGER NOT NULL,
  sync_type VARCHAR(50) NOT NULL,
  status VARCHAR(50) NOT NULL,
  message TEXT,
  files_changed INTEGER,
  created_at DATETIME NOT NULL,
  updated_at DATETIME NOT NULL,
  FOREIGN KEY (github_repository_id) REFERENCES github_repositories(id)
);
```

## Troubleshooting

### Common Issues

#### "GitHub OAuth not configured"
- Ensure `GITHUB_CLIENT_ID` and `GITHUB_CLIENT_SECRET` are set in `.env`
- Restart the backend server after adding environment variables

#### "Invalid authorization code"
- OAuth code is valid for only 10 minutes
- Ensure the redirect URI matches exactly in GitHub app settings
- Check that `GITHUB_REDIRECT_URI` is correct

#### "Failed to clone repository"
- Ensure `git` is installed on the system
- Check that `REPOS_MIRROR_PATH` directory exists and is writable
- Verify GitHub token has `repo` scope
- For private repositories, ensure token has access

#### "File not found during inspection"
- Repository may not be fully cloned yet
- Check `sync_status` is "synced" before attempting file inspection
- Verify file path starts with "/"

#### "Token encryption fails"
- Ensure `SECRET_KEY` is at least 32 characters
- Check that only one instance of `TokenEncryption` is created

### Debug Mode

Enable debug logging:
```bash
DEBUG=true LOG_LEVEL=DEBUG make backend-dev
```

### Database Issues

Reset the database (development only):
```bash
rm test.db  # Remove SQLite database
make backend-dev  # Restart backend to recreate tables
```

## Security Considerations

1. **Token Storage**: Tokens are encrypted with Fernet before storage
2. **HTTPS**: Always use HTTPS in production for OAuth callbacks
3. **Secret Keys**: Use strong, randomly generated secret keys
4. **Scope Limiting**: OAuth scope is limited to `repo` and `user`
5. **CORS**: Configure CORS appropriately for your domain
6. **Rate Limiting**: Implement rate limiting for API endpoints in production

## Production Deployment

### Pre-Deployment Checklist

- [ ] Update `GITHUB_REDIRECT_URI` to production domain
- [ ] Generate strong `SECRET_KEY` and `SESSION_SECRET_KEY` (minimum 32 characters)
- [ ] Set up database (PostgreSQL recommended)
- [ ] Configure `REPOS_MIRROR_PATH` to persistent storage
- [ ] Enable HTTPS
- [ ] Set `DEBUG=false`
- [ ] Update `CORS_ORIGINS` to production domain
- [ ] Set up monitoring and logging
- [ ] Configure automatic backups

### Heroku Deployment

```bash
# Set environment variables
heroku config:set GITHUB_CLIENT_ID=your-id
heroku config:set GITHUB_CLIENT_SECRET=your-secret
heroku config:set SECRET_KEY=your-key
# ... set other variables

# Push to Heroku
git push heroku main
```

## Additional Resources

- [GitHub OAuth Documentation](https://docs.github.com/en/developers/apps/building-oauth-apps)
- [GitHub API Documentation](https://docs.github.com/en/rest)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Next.js Documentation](https://nextjs.org/docs)
