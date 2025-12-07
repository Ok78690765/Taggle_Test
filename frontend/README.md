# Frontend Application (Next.js)

A modern web frontend built with Next.js, TypeScript, and Tailwind CSS.

## Features

- **Next.js 14**: React framework with App Router
- **TypeScript**: Type-safe development
- **Tailwind CSS**: Utility-first CSS framework
- **ESLint**: Code linting
- **Prettier**: Code formatting
- **Jest**: Unit testing framework
- **Environment Configuration**: Easy API endpoint configuration
- **Agent Console UI**: Authentication gate, repository explorer, prompt composer, analysis dashboards
- **State Management**: React Query for server state + Zustand stores for auth, explorer, UI, and analysis state
- **Streaming Feedback**: Progress indicators and live status updates while running analysis

## Setup

### Prerequisites

- Node.js 18 or higher
- npm, yarn, or pnpm

### Installation

1. **Install dependencies**
   ```bash
   npm install
   ```

   Or with yarn:
   ```bash
   yarn install
   ```

   Or with pnpm:
   ```bash
   pnpm install
   ```

## Development

### Running the Development Server

```bash
npm run dev
```

Or with your preferred package manager:
```bash
yarn dev
# or
pnpm dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser to see the result.

### File Structure

```
frontend/
├── src/
│   ├── app/
│   │   ├── layout.tsx          # Root layout
│   │   ├── page.tsx            # Home page
│   │   ├── api/                # API routes (optional)
│   │   │   └── health/
│   │   └── components/
│   │       └── (reusable components)
│   ├── components/
│   │   ├── common/             # Common components
│   │   ├── layouts/            # Layout components
│   │   └── features/           # Feature-specific components
│   ├── hooks/                  # Custom React hooks
│   ├── lib/                    # Utility functions
│   │   └── api.ts              # API client
│   ├── styles/                 # Global styles
│   └── types/                  # TypeScript types
├── public/                     # Static assets
├── package.json
├── next.config.js
├── tsconfig.json
├── tailwind.config.js
├── jest.config.js
├── .eslintrc.json
├── .prettierrc
├── Dockerfile
└── README.md
```

## Code Quality

### Linting

Check code quality with ESLint:

```bash
# Using make
make frontend-lint

# Or manually
npm run lint
```

### Formatting

Format code with Prettier:

```bash
# Using make
make frontend-format

# Or manually
npm run format
```

### Type Checking

TypeScript is configured to check types during build and development. In IDEs like VSCode, you get real-time type checking.

## Building

### Development Build

```bash
npm run dev
```

### Production Build

Build for production:

```bash
npm run build
```

Start the production server:

```bash
npm start
```

### Static Export (Optional)

For static site hosting:

```bash
npm run build
```

With `output: 'export'` in `next.config.js`, this generates static HTML files.

## Testing

### Running Tests

Run the test suite:

```bash
npm run test
```

Watch mode:

```bash
npm run test:watch
```

Coverage:

```bash
npm run test:coverage
```

### Writing Tests

Create test files in the same directory as components with `.test.ts` or `.test.tsx` extension:

```typescript
import { render, screen } from '@testing-library/react';
import Home from './page';

describe('Home Page', () => {
  it('renders heading', () => {
    render(<Home />);
    const heading = screen.getByRole('heading');
    expect(heading).toBeInTheDocument();
  });
});
```

## API Integration

### Environment Variables

Create a `.env.local` file in the root directory:

```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

The `NEXT_PUBLIC_` prefix makes it available to the browser.

### Using the API Client

```typescript
import { api } from '@/lib/api';

async function getItems() {
  const response = await api.get('/api/items');
  return response.data;
}
```

### Fetch Data in Components

Using `getServerSideProps`:

```typescript
export const getServerSideProps = async (context) => {
  const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/items`);
  const data = await response.json();
  return { props: { items: data.items } };
};
```

Using `useEffect`:

```typescript
'use client';

import { useEffect, useState } from 'react';

export default function Items() {
  const [items, setItems] = useState([]);

  useEffect(() => {
    fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/items`)
      .then(res => res.json())
      .then(data => setItems(data.items));
  }, []);

  return <div>{/* render items */}</div>;
}
```

## Styling

### Tailwind CSS

Tailwind CSS is configured and ready to use. Add classes directly to elements:

```tsx
<div className="flex items-center justify-center h-screen bg-gradient-to-r from-blue-500 to-purple-600">
  <h1 className="text-4xl font-bold text-white">Welcome</h1>
</div>
```

### CSS Modules

For component-scoped styles:

```tsx
import styles from './Component.module.css';

export default function Component() {
  return <div className={styles.container}>Content</div>;
}
```

### Global Styles

Edit `src/styles/globals.css` for global styles:

```css
* {
  @apply box-border;
}

body {
  @apply bg-white text-gray-900;
}
```

## Deployment

### Vercel (Recommended for Next.js)

#### Step-by-Step Vercel Deployment Guide

**Prerequisites:**
- GitHub account with repository access
- Vercel account (sign up at [vercel.com](https://vercel.com) with GitHub)

**Step 1: Sign Up with GitHub Integration**
1. Go to [vercel.com/signup](https://vercel.com/signup)
2. Click "Continue with GitHub"
3. Authorize Vercel to access your GitHub repositories
4. You'll be redirected to the Vercel dashboard

**Step 2: Import Your Repository**
1. On the Vercel dashboard, click "Add New..." → "Project"
2. Search for and select your monorepo repository
3. Click "Import"

**Step 3: Configure Project Settings**
1. **Project Name**: Enter a name for your project
2. **Root Directory**: 
   - Click "Edit" next to Root Directory
   - Select `frontend` folder from the dropdown
   - Click "Continue"
3. **Build & Development Settings**:
   - Build Command: `npm ci && npm run build`
   - Output Directory: `.next` (auto-detected)
   - Install Command: `npm ci` (auto-detected)
   - Development Command: `npm run dev` (auto-detected)

**Step 4: Add Environment Variables**
1. In the "Environment Variables" section, add:
   - **NEXT_PUBLIC_API_URL**: 
     - Development: `http://localhost:8000`
     - Production: Your PythonAnywhere backend URL (e.g., `https://yourusername.pythonanywhere.com`)
   - **NEXT_PUBLIC_APP_NAME**: `Agent Console` (or your app name)
   - **NEXT_PUBLIC_APP_VERSION**: `1.0.0` (or your version)

   **Important**: All `NEXT_PUBLIC_*` variables are public and visible to the browser. Never put secrets here.

2. Click "Deploy"

**Step 5: Configure Production Environment**
After initial deployment, update production environment variables:
1. Go to your Vercel project → Settings → Environment Variables
2. Update `NEXT_PUBLIC_API_URL` to your production backend URL
3. Set the environment to "Production"
4. Click "Save"

**Step 6: Automatic Deployments**
Your project is now set up for automatic deployments:
- **Main branch**: Automatically deploys to production when you push to `main`
- **Pull requests**: Preview deployments are created for each PR
- **Other branches**: Optional preview deployments (can be enabled in settings)

#### Vercel URL Format
- **Production URL**: `https://your-project-name.vercel.app`
- **Branch Preview**: `https://your-project-name-branch-name.vercel.app`
- **Custom Domain**: Configure in Vercel Settings → Domains

#### Testing Locally Before Deployment
Before pushing to production, test the Vercel build locally:

```bash
# Install Vercel CLI globally (if not already installed)
npm install -g vercel

# Test the build (from the frontend directory)
vercel build

# This will:
# - Run npm ci to install dependencies
# - Run npm run build to create the Next.js build
# - Simulate the Vercel production environment
```

If the build succeeds, you should see:
```
✓ Build completed successfully
```

#### API Routes & Backend Integration
The frontend is configured to proxy API calls to your backend:
- **Local**: Requests to `/api/*` are proxied to `http://localhost:8000/api/*`
- **Production**: Requests to `/api/*` are proxied to your `NEXT_PUBLIC_API_URL`

**Important**: You must configure CORS on your backend to accept requests from your Vercel domain:
```
CORS_ORIGINS=https://your-project-name.vercel.app
```

#### Monitoring & Logs
1. Go to your Vercel project → Deployments
2. Click on a deployment to view:
   - Build logs
   - Runtime logs
   - Analytics
   - Performance metrics

#### Troubleshooting Vercel Deployments

**Build fails with "Module not found"**:
- Check that all imports use correct paths
- Ensure dependencies are in `package.json`
- Verify TypeScript compilation: `npm run type-check`

**API calls fail in production**:
- Verify `NEXT_PUBLIC_API_URL` is set to the correct backend URL
- Check that the backend URL is accessible from the internet
- Ensure backend CORS settings include your Vercel domain
- Check browser console for CORS errors

**Environment variables not working**:
- Redeploy after setting environment variables (they're baked in at build time)
- Verify variables are prefixed with `NEXT_PUBLIC_` to be available in the browser
- Non-public variables won't be available to the frontend

**Deployment keeps failing**:
- Run `vercel build` locally to reproduce the error
- Check build logs in Vercel dashboard
- Ensure Node.js version compatibility (requires Node.js 18+)

#### Production Checklist
Before deploying to production:
- [ ] All code merged to `main` branch
- [ ] Environment variables configured in Vercel dashboard
- [ ] `NEXT_PUBLIC_API_URL` points to production backend
- [ ] Backend CORS configured to accept Vercel domain
- [ ] Build passes locally with `vercel build`
- [ ] No console errors in production build
- [ ] API integration tested with production backend
- [ ] Analytics and monitoring configured (if needed)

### Netlify

1. **Connect Repository**
   - Go to [netlify.com](https://netlify.com)
   - Connect your repository
   - Select `frontend` directory

2. **Configure Build Settings**
   - Base Directory: `frontend`
   - Build Command: `npm run build`
   - Publish Directory: `out` (if using export)

3. **Environment Variables**
   - Add `NEXT_PUBLIC_API_URL` in build environment

4. **Deploy**
   - Automatic deployment on push

### Docker

Build the Docker image:

```bash
docker build -t myapp-frontend .
```

Run the container:

```bash
docker run -p 3000:3000 \
  -e NEXT_PUBLIC_API_URL=http://api.example.com \
  myapp-frontend
```

### GitHub Pages

For static site hosting (requires `output: 'export'`):

```bash
npm run build
# Push 'out' directory to gh-pages branch
```

### Self-Hosted

1. Build the application: `npm run build`
2. Install production dependencies: `npm ci --production`
3. Start the server: `npm start`
4. Use a reverse proxy (nginx, Caddy) to serve on port 80/443

## Performance Optimization

### Image Optimization

Use `next/image` for automatic image optimization:

```tsx
import Image from 'next/image';

export default function Hero() {
  return (
    <Image
      src="/hero.jpg"
      alt="Hero"
      width={1200}
      height={600}
      priority
    />
  );
}
```

### Code Splitting

Next.js automatically code-splits pages. Use dynamic imports for large components:

```tsx
import dynamic from 'next/dynamic';

const HeavyComponent = dynamic(() => import('../components/HeavyComponent'));
```

### Metrics

Monitor Core Web Vitals:

```tsx
import { useReportWebVitals } from 'next/web-vitals';

export function reportWebVitals(metric) {
  console.log(metric);
}
```

## Environment Configuration

Environment variables live in `.env.local`. Copy `.env.example` as a starting point:

```bash
cp .env.example .env.local
```

Key environment variables:

- `NEXT_PUBLIC_API_URL` (required) – Backend API base URL, e.g. `http://localhost:8000`
- `NEXT_PUBLIC_APP_NAME` – Display name for headers, titles, etc. (default: Agent Console)
- `NEXT_PUBLIC_APP_VERSION` – Version string shown in dashboards (default: 1.0.0)
- `NEXT_PUBLIC_ANALYTICS_ID` – Optional analytics identifier (PostHog, GA4, etc.)

Configure these variables in Vercel/Netlify project settings for production deployments.

## Common Tasks

```bash
# Create a new page
# Just create app/page-name/page.tsx

# Create a new component
# Create components/MyComponent.tsx

# Run linter with fixes
npm run lint -- --fix

# Format all files
npm run format

# Generate build analysis
npm run build -- --analyze
```

## Troubleshooting

**Port already in use**:
```bash
# Use a different port
npm run dev -- -p 3001
```

**Module not found**:
- Check import paths
- Restart dev server
- Verify tsconfig.json paths

**API connection errors**:
- Check `NEXT_PUBLIC_API_URL` environment variable
- Ensure backend is running
- Verify CORS settings on backend

**Build fails**:
- Check for TypeScript errors: `npx tsc --noEmit`
- Clear `.next` folder: `rm -rf .next`
- Reinstall dependencies: `npm install`

## Resources

- [Next.js Documentation](https://nextjs.org/docs)
- [React Documentation](https://react.dev)
- [TypeScript Documentation](https://www.typescriptlang.org/docs)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [ESLint Documentation](https://eslint.org/docs)
- [Jest Documentation](https://jestjs.io/docs/getting-started)
