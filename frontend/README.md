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

1. **Connect Repository**
   - Go to [vercel.com](https://vercel.com)
   - Import your repository
   - Vercel auto-detects Next.js

2. **Configure Build Settings**
   - Root Directory: `frontend`
   - Build Command: `npm run build`
   - Output Directory: `.next` (auto-detected)

3. **Environment Variables**
   - Add `NEXT_PUBLIC_API_URL` in project settings
   - Set to your backend API URL in production

4. **Deploy**
   - Automatic deployment on push to main
   - Preview deployments for pull requests

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

Key environment variables:

- `NEXT_PUBLIC_API_URL` - Backend API URL (required)
- `NEXT_PUBLIC_APP_NAME` - Application name
- `NEXT_PUBLIC_DEBUG` - Enable debug mode

See `.env.example` for complete configuration.

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
