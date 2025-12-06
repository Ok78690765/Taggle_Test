'use client';

import React from 'react';
import { useRouter } from 'next/navigation';
import { Button } from '@/components/common/Button';

export default function HomePage() {
  const router = useRouter();

  return (
    <main className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      <div className="container mx-auto flex min-h-screen flex-col items-center justify-center px-4 text-center">
        <div className="mb-8 flex h-20 w-20 items-center justify-center rounded-full bg-blue-100 text-blue-600">
          <svg
            className="h-10 w-10"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="1.5"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              d="M17.25 6.75L22.5 12l-5.25 5.25m-10.5 0L1.5 12l5.25-5.25m7.5-3l-4.5 16.5"
            />
          </svg>
        </div>

        <h1 className="mb-4 text-6xl font-bold text-gray-900">
          Agent Console
        </h1>

        <p className="mb-12 max-w-2xl text-xl text-gray-600">
          Comprehensive code analysis platform with repository explorer, live quality
          metrics, and AI-powered insights for modern development teams.
        </p>

        <div className="flex flex-col gap-4 sm:flex-row">
          <Button
            size="lg"
            variant="primary"
            onClick={() => router.push('/dashboard')}
          >
            Launch Console
          </Button>
          <Button size="lg" variant="outline" onClick={() => router.push('/login')}>
            Sign In
          </Button>
        </div>

        <div className="mt-16 grid gap-8 md:grid-cols-3 max-w-4xl">
          <div className="rounded-2xl border border-gray-100 bg-white p-6 text-left shadow-sm">
            <div className="mb-4 flex h-12 w-12 items-center justify-center rounded-full bg-blue-50">
              <svg
                className="h-6 w-6 text-blue-600"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
                />
              </svg>
            </div>
            <h3 className="mb-2 text-lg font-semibold text-gray-900">
              Repository Explorer
            </h3>
            <p className="text-sm text-gray-600">
              Browse codebases with file tree viewer, preview modes, and diff
              comparisons.
            </p>
          </div>

          <div className="rounded-2xl border border-gray-100 bg-white p-6 text-left shadow-sm">
            <div className="mb-4 flex h-12 w-12 items-center justify-center rounded-full bg-green-50">
              <svg
                className="h-6 w-6 text-green-600"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"
                />
              </svg>
            </div>
            <h3 className="mb-2 text-lg font-semibold text-gray-900">
              Live Analysis
            </h3>
            <p className="text-sm text-gray-600">
              Real-time quality scoring, issue detection, complexity metrics, and
              architecture insights.
            </p>
          </div>

          <div className="rounded-2xl border border-gray-100 bg-white p-6 text-left shadow-sm">
            <div className="mb-4 flex h-12 w-12 items-center justify-center rounded-full bg-purple-50">
              <svg
                className="h-6 w-6 text-purple-600"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M13 10V3L4 14h7v7l9-11h-7z"
                />
              </svg>
            </div>
            <h3 className="mb-2 text-lg font-semibold text-gray-900">
              Prompt Composer
            </h3>
            <p className="text-sm text-gray-600">
              Submit code snippets for multi-language analysis with streaming updates
              and progress indicators.
            </p>
          </div>
        </div>

        <footer className="mt-16 text-sm text-gray-500">
          <p>Powered by FastAPI + Next.js • Analysis API v1.0</p>
        </footer>
      </div>
    </main>
  );
}
