'use client';

import React, { useState } from 'react';
import { Button } from '@/components/common/Button';

interface LoginFormValues {
  name: string;
  email: string;
  apiKey: string;
  workspace?: string;
}

interface LoginFormProps {
  loading?: boolean;
  error?: string | null;
  onSubmit: (values: LoginFormValues) => Promise<void>;
  onTestConnection?: () => Promise<void>;
}

export function LoginForm({
  loading = false,
  error,
  onSubmit,
  onTestConnection,
}: LoginFormProps) {
  const [values, setValues] = useState<LoginFormValues>({
    name: '',
    email: '',
    apiKey: '',
    workspace: 'default',
  });
  const [testStatus, setTestStatus] = useState<'idle' | 'running' | 'success' | 'error'>(
    'idle'
  );

  const handleChange = (key: keyof LoginFormValues, value: string) => {
    setValues((prev) => ({ ...prev, [key]: value }));
  };

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    await onSubmit(values);
  };

  const handleTestConnection = async () => {
    if (!onTestConnection) return;
    setTestStatus('running');
    try {
      await onTestConnection();
      setTestStatus('success');
      setTimeout(() => setTestStatus('idle'), 1500);
    } catch (err) {
      console.error(err);
      setTestStatus('error');
      setTimeout(() => setTestStatus('idle'), 2500);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div className="grid gap-4 sm:grid-cols-2">
        <div>
          <label
            htmlFor="name"
            className="mb-1 block text-sm font-medium text-gray-700"
          >
            Full name
          </label>
          <input
            id="name"
            type="text"
            value={values.name}
            onChange={(e) => handleChange('name', e.target.value)}
            required
            placeholder="Ada Lovelace"
            className="w-full rounded-lg border border-gray-300 px-4 py-2 text-gray-900 placeholder-gray-400 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
            disabled={loading}
          />
        </div>
        <div>
          <label
            htmlFor="email"
            className="mb-1 block text-sm font-medium text-gray-700"
          >
            Work email
          </label>
          <input
            id="email"
            type="email"
            value={values.email}
            onChange={(e) => handleChange('email', e.target.value)}
            required
            placeholder="ada@example.com"
            className="w-full rounded-lg border border-gray-300 px-4 py-2 text-gray-900 placeholder-gray-400 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
            disabled={loading}
          />
        </div>
      </div>

      <div>
        <label
          htmlFor="apiKey"
          className="mb-1 block text-sm font-medium text-gray-700"
        >
          API token
        </label>
        <input
          id="apiKey"
          type="password"
          value={values.apiKey}
          onChange={(e) => handleChange('apiKey', e.target.value)}
          required
          placeholder="sk_live_123..."
          className="w-full rounded-lg border border-gray-300 px-4 py-2 text-gray-900 placeholder-gray-400 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
          disabled={loading}
        />
        <p className="mt-1 text-xs text-gray-500">
          Store your API token securely—used for authenticated analysis requests.
        </p>
      </div>

      <div>
        <label
          htmlFor="workspace"
          className="mb-1 block text-sm font-medium text-gray-700"
        >
          Workspace or organization
        </label>
        <input
          id="workspace"
          type="text"
          value={values.workspace}
          onChange={(e) => handleChange('workspace', e.target.value)}
          placeholder="core-platform"
          className="w-full rounded-lg border border-gray-300 px-4 py-2 text-gray-900 placeholder-gray-400 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
          disabled={loading}
        />
      </div>

      {error && (
        <div className="rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
          {error}
        </div>
      )}

      <div className="flex flex-col gap-3 sm:flex-row">
        <Button
          type="button"
          variant="secondary"
          className="flex-1"
          onClick={handleTestConnection}
          disabled={loading || testStatus === 'running'}
        >
          {testStatus === 'running'
            ? 'Testing connection...'
            : testStatus === 'success'
            ? 'API reachable ✔'
            : testStatus === 'error'
            ? 'Connection failed'
            : 'Test API connection'}
        </Button>
        <Button
          type="submit"
          variant="primary"
          className="flex-1"
          loading={loading}
          disabled={loading}
        >
          Enter console
        </Button>
      </div>
    </form>
  );
}
