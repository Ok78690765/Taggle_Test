# Agent Console - Web UI Documentation

## Overview

The Agent Console is a comprehensive web-based user interface for code analysis, providing:
- **Authentication Gate**: Secure credential management with API token storage
- **Repository Selector**: Browse and select codebases to analyze
- **Code Explorer**: Interactive file tree with preview and diff modes
- **Prompt Composer**: Submit code snippets for multi-language analysis
- **Live Analysis**: Streaming status updates and progress indicators
- **Quality Dashboards**: Visual metrics, issue breakdowns, and architecture insights

## Architecture

### Tech Stack
- **Framework**: Next.js 14 with App Router
- **Language**: TypeScript with strict mode
- **Styling**: Tailwind CSS with custom design system
- **State**: React Query (server) + Zustand (client)
- **UI Components**: Custom component library (Button, Card, LoadingSpinner, etc.)
- **Code Highlighting**: react-syntax-highlighter with VSCode Dark Plus theme
- **Charts**: Recharts for quality metrics visualization

### Directory Structure

```
frontend/src/
├── app/
│   ├── layout.tsx              # Root layout with providers
│   ├── page.tsx                # Landing page
│   ├── providers.tsx           # React Query provider
│   ├── login/
│   │   └── page.tsx            # Login page
│   └── dashboard/
│       └── page.tsx            # Main console UI
├── components/
│   ├── auth/
│   │   ├── AuthGate.tsx        # Authentication wrapper
│   │   └── LoginForm.tsx       # Login form with test connection
│   ├── repository/
│   │   └── RepositorySelector.tsx
│   ├── explorer/
│   │   ├── CodeExplorer.tsx    # Main explorer component
│   │   ├── FileTree.tsx        # Recursive file tree
│   │   ├── FileViewer.tsx      # Syntax-highlighted preview
│   │   └── DiffViewer.tsx      # Git diff viewer
│   ├── analysis/
│   │   ├── PromptComposer.tsx  # Code submission form
│   │   ├── AnalysisResults.tsx # Results dashboard
│   │   └── QualityScoreCard.tsx # Radial quality chart
│   ├── dashboard/
│   │   └── (future metrics/charts)
│   └── common/
│       ├── Button.tsx
│       ├── Card.tsx
│       ├── LoadingSpinner.tsx
│       ├── ProgressBar.tsx
│       ├── StatusPill.tsx
│       ├── EmptyState.tsx
│       └── ErrorBoundary.tsx
├── lib/
│   ├── api.ts              # Axios client with interceptors
│   ├── analysis-api.ts     # Analysis endpoint wrappers
│   └── github-api.ts       # Repository/file browsing (demo data)
├── store/
│   ├── auth-store.ts       # Auth state (Zustand with persist)
│   ├── explorer-store.ts   # Repository and file state
│   ├── ui-store.ts         # Sidebar/panel toggles
│   └── analysis-store.ts   # Analysis status and results
└── types/
    ├── index.ts
    ├── analysis.ts         # Quality, issues, complexity, etc.
    ├── auth.ts             # User and auth types
    ├── repository.ts       # Repository and file types
    └── prompt.ts           # Prompt templates (future)
```

## Key Features

### 1. Authentication Gate
Located in `components/auth/AuthGate.tsx` and `app/login/page.tsx`.

- **Fields**: Name, email, API token, workspace
- **Test Connection**: Validates backend health endpoint
- **Persistent Auth**: Zustand store with localStorage persistence
- **Axios Interceptors**: Automatically injects bearer token and handles 401s
- **Token Storage**: Stored in both Zustand and localStorage for sync

### 2. Repository Selector
Located in `components/repository/RepositorySelector.tsx`.

- **React Query Integration**: Caches repository list
- **Demo Data**: Falls back to hardcoded repositories if GitHub API not connected
- **UI**: Card-based selector with repository metadata (language, stars, forks)
- **State**: Stores selected repository in `explorer-store`

### 3. Code Explorer
Located in `components/explorer/CodeExplorer.tsx`, `FileTree.tsx`, `FileViewer.tsx`, `DiffViewer.tsx`.

- **File Tree**: Recursive expandable tree with directory/file icons
- **Preview Mode**: Syntax-highlighted code viewer (react-syntax-highlighter)
- **Diff Mode**: Side-by-side or unified diff view
- **Language Detection**: Auto-detects language from file extension
- **Selection Tracking**: Stores selected file path in explorer store

### 4. Prompt Composer
Located in `components/analysis/PromptComposer.tsx`.

- **Multi-Language**: Dropdown for Python, JavaScript, TypeScript, Java, C++
- **Code Input**: Large textarea with character and line count
- **Options**: Checkbox to enable full analysis (quality, issues, architecture, formatting, debug)
- **Streaming Updates**: Shows progress bar during analysis
- **Integration**: Calls `analysisApi.analyzeCode()` and stores results in `analysis-store`

### 5. Live Analysis & Quality Dashboard
Located in `components/analysis/AnalysisResults.tsx` and `QualityScoreCard.tsx`.

- **Quality Score**: Radial progress chart with overall score (0-100)
- **Metrics Breakdown**: Code quality, maintainability, complexity, duplication
- **Issue Detection**: Grouped by severity (error, warning, info) with line numbers
- **Complexity Metrics**: Cyclomatic, cognitive, LOC, nesting depth
- **Architecture Insights**: Detected patterns (Singleton, Factory, Observer) with confidence
- **Debug Insights**: Uninitialized variables, null risks, infinite loops, resource leaks
- **Status Streaming**: Progress bar updates ("Analyzing...", "Detecting issues...", "Complete")

## State Management

### 1. Auth Store (`store/auth-store.ts`)
```typescript
interface AuthStore {
  token: string | null;
  user: UserProfile | null;
  authenticated: boolean;
  setAuth(token, user, expiresAt?): void;
  logout(): void;
  isAuthenticated(): boolean;
}
```
- Persisted via Zustand middleware
- Syncs with axios interceptor
- Expires check on `isAuthenticated()`

### 2. Explorer Store (`store/explorer-store.ts`)
```typescript
interface ExplorerStore {
  repository: Repository | null;
  branch: string | null;
  fileTree: FileNode[];
  selectedPath: string | null;
  fileContent: FileContent | null;
  fileDiff: FileDiff | null;
  viewMode: 'preview' | 'diff';
  syncing: boolean;
}
```

### 3. Analysis Store (`store/analysis-store.ts`)
```typescript
interface AnalysisStore {
  status: 'idle' | 'running' | 'success' | 'error';
  statusMessage: string | null;
  progress: number;
  result: CodeAnalysisResponse | null;
  debugResult: DebugAnalysisResponse | null;
  history: AnalysisHistoryItem[];
  startAnalysis(message?): void;
  updateProgress(message, progress): void;
  completeAnalysis(result, debugResult?): void;
  failAnalysis(message): void;
}
```

### 4. UI Store (`store/ui-store.ts`)
```typescript
interface UIStore {
  sidebarOpen: boolean;
  promptComposerOpen: boolean;
  analysisPanelOpen: boolean;
  toggleSidebar(): void;
  togglePromptComposer(): void;
  toggleAnalysisPanel(): void;
}
```

## API Integration

### Analysis API (`lib/analysis-api.ts`)
Wraps backend endpoints:
- `getSupportedLanguages()`: Returns list of supported languages
- `analyzeCode(request)`: Comprehensive analysis
- `analyzeQuality(code, language)`: Quality metrics only
- `analyzeIssues(code, language)`: Issue detection only
- `analyzeComplexity(code, language)`: Complexity metrics only
- `analyzeArchitecture(code, language)`: Architecture patterns only
- `analyzeFormatting(code, language)`: Style recommendations only
- `analyzeDebug(code, language)`: Debug insights only

### GitHub API (`lib/github-api.ts`)
Mock/demo GitHub integration:
- `listRepositories()`: Lists available repositories
- `getRepositoryTree(repoId, branch)`: Fetches file tree
- `getFileContent(repoId, path)`: Gets file content
- `getFileDiff(repoId, path)`: Gets git diff
- `syncRepository(repoId)`: Triggers repository sync

**Note**: Currently returns demo data. To enable real GitHub integration, implement backend endpoints for GitHub API calls.

## Environment Variables

### Required
- `NEXT_PUBLIC_API_URL`: Backend API base URL (default: `http://localhost:8000`)

### Optional
- `NEXT_PUBLIC_APP_NAME`: Application name (default: "Agent Console")
- `NEXT_PUBLIC_APP_VERSION`: Version string
- `NEXT_PUBLIC_ANALYTICS_ID`: Analytics tracking ID
- `NEXT_PUBLIC_SENTRY_DSN`: Error monitoring DSN

### Local Development
Create `.env.local`:
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Production
Set environment variables in Vercel/Netlify dashboard:
```
NEXT_PUBLIC_API_URL=https://api.yourapp.com
```

## Deployment

### Vercel (Recommended)
1. **Connect Repository**
   - Import project to Vercel
   - Set root directory to `frontend`
   
2. **Configure Build**
   - Build command: `npm run build`
   - Output directory: `.next` (auto-detected)
   - Install command: `npm install`

3. **Environment Variables**
   - Add `NEXT_PUBLIC_API_URL` in project settings
   - Point to production backend URL

4. **Deploy**
   - Automatic deployment on push to main
   - Preview deployments for PRs

### Netlify
1. **Connect Repository**
   - Import to Netlify
   - Base directory: `frontend`

2. **Build Settings**
   - Build command: `npm run build`
   - Publish directory: `.next` (for serverless) or `out` (for static export)

3. **Environment Variables**
   - Add `NEXT_PUBLIC_API_URL` in build settings

4. **Deploy**
   - Automatic deployment on push

### Docker
```bash
# Build image
docker build -t agent-console-frontend -f frontend/Dockerfile frontend/

# Run container
docker run -p 3000:3000 \
  -e NEXT_PUBLIC_API_URL=http://localhost:8000 \
  agent-console-frontend
```

### Self-Hosted
```bash
# Build production bundle
npm run build

# Start server
npm start

# Or use PM2
pm2 start npm --name "agent-console" -- start
```

## Responsive Design

### Breakpoints
- **Mobile**: < 640px (sm)
- **Tablet**: 640-1024px (md, lg)
- **Desktop**: >= 1024px (xl, 2xl)

### Mobile Optimizations
- Collapsible sidebar
- Stacked layout for dashboard
- Responsive file tree
- Touch-friendly buttons
- Mobile-friendly forms

### Accessibility
- ARIA labels on all interactive elements
- Keyboard navigation support
- Focus indicators
- Screen reader compatible
- Color contrast WCAG AA compliant

## Error Handling

### Error Boundary
Located in `components/common/ErrorBoundary.tsx`.
- Catches React render errors
- Shows fallback UI with reload option
- Logs errors to console (can integrate Sentry)

### API Errors
- Axios interceptors handle 401 (redirect to login)
- Network errors show toast/alert
- Retry logic in React Query
- Loading and error states in components

### Validation
- Form validation in login and prompt composer
- Required fields marked with asterisks
- Real-time feedback on input errors

## Testing

### Unit Tests
```bash
npm run test
```
Located in `__tests__` directories alongside components.

### E2E Tests
(Future: Add Playwright/Cypress tests for critical user flows)

### Type Checking
```bash
npm run type-check
```
Strict TypeScript with no implicit any.

## Performance

### Optimization Strategies
- Code splitting (automatic via Next.js)
- React Query caching (30s stale time)
- Lazy loading for heavy components
- Image optimization (Next.js Image component)
- Minimal bundle size (~300KB gzipped)

### Monitoring
- React Query Devtools (development only)
- Web Vitals tracking ready
- Can integrate Google Analytics, PostHog, etc.

## Security

### Best Practices
- API tokens stored in localStorage (consider httpOnly cookies for production)
- No sensitive data in client-side code
- CORS configured on backend
- XSS protection via React's built-in escaping
- Content Security Policy headers (configure in Next.js)

### Authentication Flow
1. User submits credentials + API token
2. Frontend validates and stores token
3. Axios interceptor adds `Authorization: Bearer <token>` to all requests
4. Backend validates token on each request
5. 401 responses trigger automatic logout

## Troubleshooting

### Backend Connection Issues
- Verify `NEXT_PUBLIC_API_URL` is set correctly
- Check backend is running on specified port
- Test with "Test API Connection" button on login
- Check browser console for CORS errors
- Ensure backend CORS allows frontend origin

### Build Errors
- Clear `.next` folder: `rm -rf .next`
- Delete `node_modules`: `rm -rf node_modules && npm install`
- Check TypeScript errors: `npm run type-check`
- Update dependencies: `npm update`

### State Management Issues
- Clear localStorage: `localStorage.clear()`
- Check Zustand devtools
- Verify React Query cache is not stale
- Restart development server

## Future Enhancements

### Planned Features
1. **GitHub Integration**: Real GitHub API connection for repository browsing
2. **Prompt Templates**: Save and reuse analysis configurations
3. **History Panel**: View past analysis results
4. **Comparison Mode**: Compare analysis between file versions
5. **Batch Analysis**: Analyze multiple files at once
6. **Export Reports**: Download analysis as PDF/JSON
7. **Team Collaboration**: Share analysis results with team
8. **Real-time Sync**: WebSocket updates for live collaboration
9. **Custom Rules**: Define custom analysis rules
10. **CI/CD Integration**: Trigger analysis from CI pipeline

### Extensibility
- Plugin system for custom analysis plugins
- Theme customization
- Internationalization (i18n)
- Role-based access control
- Audit logs

## Contributing

Follow the project's `CONTRIBUTING.md` guidelines. Key points:
- Use conventional commits
- Run linter and formatter before committing
- Add tests for new features
- Update documentation

## Support

For issues or questions:
- Check GitHub Issues
- Review backend API documentation (`backend/ANALYSIS_API.md`)
- Contact the development team

---

**Version**: 1.0.0  
**Last Updated**: December 2024  
**Maintainer**: Development Team
