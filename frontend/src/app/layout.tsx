import type { Metadata } from 'next';
import { Providers } from './providers';
import { ErrorBoundary } from '@/components/common/ErrorBoundary';
import '../styles/globals.css';

export const metadata: Metadata = {
  title: 'Agent Console - Code Analysis Platform',
  description: 'Web agent UI for code analysis, repository exploration, and AI-powered insights',
  viewport: 'width=device-width, initial-scale=1',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        <ErrorBoundary>
          <Providers>{children}</Providers>
        </ErrorBoundary>
      </body>
    </html>
  );
}
