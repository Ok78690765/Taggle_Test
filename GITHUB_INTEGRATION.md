# GitHub Integration Feature Documentation

This document provides an overview of the GitHub OAuth and repository synchronization feature.

## Overview

The GitHub integration allows users to:
- Authenticate with their GitHub account via OAuth
- Automatically discover and list accessible repositories
- Select repositories for mirroring/synchronization
- Clone and maintain local mirrors of repositories
- Browse repository files and inspect code
- Receive real-time updates via webhooks

## Architecture

### Frontend Components

**Location**: `/frontend/src/`

- **`lib/api.ts`**: HTTP client for API communication
- **`lib/github-auth.ts`**: GitHub authentication utilities
- **`lib/repository-service.ts`**: Repository API service
- **`app/auth/github/callback/page.tsx`**: OAuth callback handler
- **`app/github/page.tsx`**: Main repository management dashboard
- **`app/github/[id]/files/page.tsx`**: File browser and code inspector

### Backend Components

**Location**: `/backend/app/`

#### Models (`models/github.py`)
- `GitHubUser`: Stores encrypted OAuth tokens and user metadata
- `GitHubRepository`: Tracks mirrored repositories
- `SyncLog`: Records synchronization operations

#### Services (`services/github.py`)
- `GitHubAPIService`: Handles GitHub API calls (OAuth, user info, repos, webhooks)
- `RepositorySyncService`: Manages local repository mirrors
- `GitHubUserService`: Database operations for GitHub users
- `RepositoryService`: Database operations for repositories

#### API Endpoints (`api/github.py`)
- OAuth flow: `/api/github/auth/`
- User management: `/api/github/user/`
- Repository operations: `/api/github/repositories/`
- Code inspection: `/api/github/repositories/{id}/inspect`
- Webhooks: `/api/github/webhook/`

#### Utilities (`utils/encryption.py`)
- `TokenEncryption`: Encrypts/decrypts GitHub OAuth tokens

## User Flow

### 1. Authentication Flow

```
User → Click "Connect with GitHub" → Redirect to GitHub OAuth →
User Authorizes → Callback to /auth/github/callback →
Exchange code for token → Store encrypted token → Redirect to /github
```

### 2. Repository Discovery

```
User on /github → Click "Sync Repositories" → Fetch from GitHub API →
Store in database → Display repository list
```

### 3. Repository Mirroring

```
User selects repositories → Click "Clone Repository" →
Git clone to REPOS_MIRROR_PATH → Update sync status → Enable file browsing
```

### 4. Code Inspection

```
User browses files → Selects code file → Read from local mirror →
Display syntax-highlighted content
```

## API Integration

### Authentication
```javascript
// Frontend
const oauthUrl = await GitHubAuth.getOAuthUrl();
window.location.href = oauthUrl;

// After callback
const userId = GitHubAuth.getCurrentUserId();
```

### Repository Operations
```javascript
// Sync repositories from GitHub
await RepositoryService.syncRepositories(userId);

// List repositories
const repos = await RepositoryService.listRepositories(userId);

// Clone a repository
await RepositoryService.cloneRepository(repoId);

// Get file tree
const tree = await RepositoryService.getFileTree(repoId);

// Inspect code file
const code = await RepositoryService.inspectCodeFile(repoId, '/path/to/file.py');
```

## Data Storage

### Database
- SQLite (development) / PostgreSQL (production)
- Tables: `github_users`, `github_repositories`, `sync_logs`
- Tokens encrypted before storage

### File System
- Repositories cloned to `REPOS_MIRROR_PATH`
- Mirror format: `username_repo-name/`
- Git objects stored in `.git/` subdirectory

## Security Features

1. **Token Encryption**: OAuth tokens encrypted with Fernet
2. **Encrypted Storage**: Tokens never stored in plaintext
3. **HTTPS Redirect**: OAuth callback uses HTTPS
4. **Scope Limiting**: Only `repo` and `user` scopes requested
5. **Session Management**: User ID stored in browser session storage
6. **CORS Protection**: Configurable CORS origins

## Performance Considerations

1. **Async Operations**: Git operations run asynchronously
2. **Mirror Caching**: Local mirrors reduce API calls
3. **Pagination**: Repository listing paginated (100 per page)
4. **Webhook Updates**: Real-time updates without polling
5. **Lazy Loading**: File tree nodes expand on demand

## Deployment

### Required Environment Variables
```
GITHUB_CLIENT_ID
GITHUB_CLIENT_SECRET
GITHUB_REDIRECT_URI
SECRET_KEY (min 32 chars)
SESSION_SECRET_KEY (min 32 chars)
BACKEND_URL
REPOS_MIRROR_PATH
```

### Dependencies
- Backend: `httpx`, `cryptography`, `pyjwt`, `git` (system)
- Frontend: Standard Next.js dependencies

### Database
- Create tables: Automatic on first run
- Migrations: SQLAlchemy migrations ready for implementation

## Future Enhancements

1. **Polling Mode**: Alternative to webhooks for closed networks
2. **Repository Analytics**: Code metrics and statistics
3. **Multi-Language Support**: More language syntax highlighting
4. **Diff Viewer**: Compare commits and branches
5. **Search Integration**: Full-text search across repositories
6. **Access Control**: Fine-grained permissions per repository
7. **Batch Operations**: Clone multiple repos simultaneously
8. **Repository Deletion**: Clean up mirrored repositories
9. **Token Refresh**: Auto-refresh expired OAuth tokens
10. **Proxy Support**: Support for corporate proxies

## Testing

### Backend Tests
```bash
cd backend
poetry run pytest tests/ -v --cov=app
```

### Frontend Tests
```bash
cd frontend
npm test
```

### Manual Testing Checklist
- [ ] OAuth flow works end-to-end
- [ ] Repositories sync correctly
- [ ] Private repository access works
- [ ] File browser displays correct structure
- [ ] Code inspection shows correct syntax highlighting
- [ ] Webhooks trigger repository updates
- [ ] Token encryption/decryption works
- [ ] Error handling for missing repos
- [ ] Graceful handling of network errors

## Troubleshooting Guide

See [GITHUB_SETUP.md - Troubleshooting Section](./GITHUB_SETUP.md#troubleshooting)

## Related Documentation

- [GitHub Setup Guide](./GITHUB_SETUP.md)
- [Backend README](./backend/README.md)
- [Frontend README](./frontend/README.md)
- [CONTRIBUTING.md](./CONTRIBUTING.md)

## Support

For issues or questions:
1. Check the troubleshooting guide
2. Review GitHub API documentation
3. Check application logs with `DEBUG=true`
4. Verify environment variables are set correctly
