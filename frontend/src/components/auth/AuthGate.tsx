'use client';

import React, { useState } from 'react';
import { LoginForm } from './LoginForm';
import { useAuthStore } from '@/store/auth-store';
import { api } from '@/lib/api';

interface AuthGateProps {
  children: React.ReactNode;
}

export function AuthGate({ children }: AuthGateProps) {
  const authenticated = useAuthStore((state) => state.authenticated);
  const setAuth = useAuthStore((state) => state.setAuth);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleLogin = async (values: {
    name: string;
    email: string;
    apiKey: string;
    workspace?: string;
  }) => {
    setLoading(true);
    setError(null);

    try {
      await api.get('/health');
      setAuth(values.apiKey, {
        id: crypto.randomUUID(),
        name: values.name,
        email: values.email,
        organization: values.workspace,
      });
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : 'Failed to reach the backend API. Verify NEXT_PUBLIC_API_URL.'
      );
    } finally {
      setLoading(false);
    }
  };

  if (!authenticated) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
        <div className="flex min-h-screen items-center justify-center px-4 py-12">
          <div className="w-full max-w-lg rounded-3xl bg-white p-10 shadow-2xl">
            <div className="mb-8 text-center">
              <div className="mx-auto mb-6 flex h-16 w-16 items-center justify-center rounded-full bg-blue-100 text-blue-600">
                <svg
                  className="h-8 w-8"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="1.5"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    d="M16.5 10.5V6.75a4.5 4.5 0 10-9 0v3.75M6 21.75h12a2.25 2.25 0 002.25-2.25v-7.5A2.25 2.25 0 0018 9.75H6a2.25 2.25 0 00-2.25 2.25v7.5A2.25 2.25 0 006 21.75z"
                  />
                </svg>
              </div>
              <h1 className="text-2xl font-semibold text-gray-900">
                Agent Console Sign In
              </h1>
              <p className="mt-2 text-sm text-gray-500">
                Authenticate with your workspace credentials to continue
              </p>
            </div>
            <LoginForm
              onSubmit={handleLogin}
              loading={loading}
              error={error}
              onTestConnection={async () => {
                await api.get('/health');
              }}
            />
            <div className="mt-6 text-center text-sm text-gray-500">
              <p>
                Need access?{' '}
                <a
                  href="mailto:admin@example.com"
                  className="font-medium text-blue-600 hover:text-blue-700"
                >
                  Contact the administrator
                </a>
              </p>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return <>{children}</>;
}
