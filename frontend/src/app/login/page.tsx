'use client';

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import { LoginForm } from '@/components/auth/LoginForm';
import { useAuthStore } from '@/store/auth-store';
import { api } from '@/lib/api';

export default function LoginPage() {
  const router = useRouter();
  const setAuth = useAuthStore((state) => state.setAuth);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleTestConnection = async () => {
    try {
      await api.get('/health');
    } catch (err) {
      throw new Error('API health check failed. Verify the backend is running.');
    }
  };

  const handleSubmit = async (values: {
    name: string;
    email: string;
    apiKey: string;
    workspace?: string;
  }) => {
    setLoading(true);
    setError(null);

    try {
      await new Promise((resolve) => setTimeout(resolve, 800));

      if (!values.apiKey || values.apiKey.length < 8) {
        throw new Error('Please enter a valid API token.');
      }

      const user = {
        id: crypto.randomUUID(),
        name: values.name,
        email: values.email,
        organization: values.workspace,
      };

      setAuth(values.apiKey, user);
      router.push('/dashboard');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Login failed');
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      <div className="flex min-h-screen items-center justify-center px-4 py-12">
        <div className="w-full max-w-2xl rounded-3xl border border-gray-100 bg-white p-10 shadow-xl">
          <header className="mb-8 text-center">
            <div className="mx-auto mb-6 flex h-16 w-16 items-center justify-center rounded-full bg-blue-100">
              <svg
                className="h-8 w-8 text-blue-600"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
                strokeWidth="1.5"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  d="M16.5 10.5V6.75a4.5 4.5 0 10-9 0v3.75M6 21.75h12a2.25 2.25 0 002.25-2.25v-7.5A2.25 2.25 0 0018 9.75H6a2.25 2.25 0 00-2.25 2.25v7.5A2.25 2.25 0 006 21.75z"
                />
              </svg>
            </div>
            <h1 className="text-3xl font-bold text-gray-900">
              Sign in to Agent Console
            </h1>
            <p className="mt-3 text-sm text-gray-500">
              Provide your credentials and API token to authenticate with the analysis
              platform.
            </p>
          </header>

          <LoginForm
            loading={loading}
            error={error}
            onSubmit={handleSubmit}
            onTestConnection={handleTestConnection}
          />

          <div className="mt-8 border-t border-gray-200 pt-6 text-center text-sm text-gray-500">
            <p>
              Don&apos;t have an account?{' '}
              <a
                href="mailto:admin@example.com"
                className="font-medium text-blue-600 hover:text-blue-700"
              >
                Contact your administrator
              </a>
            </p>
          </div>
        </div>
      </div>
    </main>
  );
}
