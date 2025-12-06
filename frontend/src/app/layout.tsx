import type { Metadata } from 'next';
import '../styles/globals.css';

export const metadata: Metadata = {
  title: 'FastAPI + Next.js App',
  description: 'A modern monorepo with FastAPI backend and Next.js frontend',
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
        <div className="min-h-screen bg-gradient-to-b from-blue-50 to-white">
          {children}
        </div>
      </body>
    </html>
  );
}
