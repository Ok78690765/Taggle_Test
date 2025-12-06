'use client';

import { useEffect, useState } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import { GitHubAuth } from '@/lib/github-auth';

export default function GitHubCallback() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const handleCallback = async () => {
      try {
        const code = searchParams.get('code');
        const state = searchParams.get('state');

        if (!code) {
          setError('No authorization code received from GitHub');
          setLoading(false);
          return;
        }

        const response = await GitHubAuth.handleOAuthCallback(code);

        if (response.success) {
          setLoading(false);
          setTimeout(() => {
            router.push('/github');
          }, 1000);
        } else {
          setError(response.message || 'Authentication failed');
          setLoading(false);
        }
      } catch (err) {
        setError(
          err instanceof Error ? err.message : 'Failed to authenticate with GitHub'
        );
        setLoading(false);
      }
    };

    handleCallback();
  }, [searchParams, router]);

  return (
    <main className="container mx-auto py-12">
      <div className="max-w-md mx-auto text-center">
        <h1 className="text-3xl font-bold mb-4">GitHub Authentication</h1>

        {loading && (
          <div className="p-6">
            <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
            <p className="mt-4 text-gray-600">Processing authentication...</p>
          </div>
        )}

        {error && (
          <div className="p-6 bg-red-50 rounded-lg">
            <p className="text-red-700 font-semibold mb-4">Authentication Error</p>
            <p className="text-red-600 mb-4">{error}</p>
            <button
              onClick={() => router.push('/github')}
              className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition"
            >
              Back to GitHub
            </button>
          </div>
        )}

        {!loading && !error && (
          <div className="p-6 bg-green-50 rounded-lg">
            <p className="text-green-700 font-semibold">
              ✓ Authentication successful! Redirecting...
            </p>
          </div>
        )}
      </div>
    </main>
  );
}
