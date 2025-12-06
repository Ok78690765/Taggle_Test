'use client';

import React from 'react';
import { AuthGate } from '@/components/auth/AuthGate';
import { RepositorySelector } from '@/components/repository/RepositorySelector';
import { CodeExplorer } from '@/components/explorer/CodeExplorer';
import { PromptComposer } from '@/components/analysis/PromptComposer';
import { AnalysisResults } from '@/components/analysis/AnalysisResults';
import { Button } from '@/components/common/Button';
import { useExplorerStore } from '@/store/explorer-store';
import { useUIStore } from '@/store/ui-store';
import { useAuthStore } from '@/store/auth-store';

export default function DashboardPage() {
  const repository = useExplorerStore((state) => state.repository);
  const setRepository = useExplorerStore((state) => state.setRepository);
  const promptComposerOpen = useUIStore((state) => state.promptComposerOpen);
  const togglePromptComposer = useUIStore((state) => state.togglePromptComposer);
  const user = useAuthStore((state) => state.user);
  const logout = useAuthStore((state) => state.logout);

  return (
    <AuthGate>
      <main className="min-h-screen bg-slate-50">
        <header className="sticky top-0 z-10 border-b border-slate-200 bg-white/90 backdrop-blur">
          <div className="mx-auto flex max-w-[1800px] flex-wrap items-center justify-between gap-4 px-6 py-4">
            <div>
              <p className="text-xs font-semibold uppercase tracking-[0.2em] text-blue-600">
                Agent Console
              </p>
              <h1 className="text-2xl font-bold text-gray-900">
                Repository intelligence & code analysis
              </h1>
              <p className="text-sm text-gray-500">
                {repository
                  ? `${repository.full_name} • ${repository.default_branch}`
                  : 'Select a repository to get started'}
              </p>
            </div>

            <div className="flex flex-wrap items-center gap-3">
              {repository && (
                <Button variant="ghost" size="sm" onClick={() => setRepository(null)}>
                  Change repository
                </Button>
              )}
              <Button variant="secondary" size="sm" onClick={togglePromptComposer}>
                {promptComposerOpen ? 'Hide composer' : 'Show composer'}
              </Button>
              <Button size="sm">Sync repository</Button>
              <div className="flex items-center gap-3 rounded-full border border-gray-200 bg-white px-3 py-2">
                <div>
                  <p className="text-sm font-semibold text-gray-900">
                    {user?.name || 'Agent'}
                  </p>
                  <p className="text-xs text-gray-500">{user?.email || 'signed in'}</p>
                </div>
                <Button variant="ghost" size="sm" onClick={logout}>
                  Sign out
                </Button>
              </div>
            </div>
          </div>
        </header>

        <div className="mx-auto max-w-[1800px] px-6 py-6">
          <div className="grid gap-6 xl:grid-cols-[1fr_520px]">
            <div className="space-y-6">
              <RepositorySelector />
              {repository && <CodeExplorer />}
              <AnalysisResults />
            </div>

            <div className="space-y-6">
              {promptComposerOpen && <PromptComposer />}
            </div>
          </div>
        </div>
      </main>
    </AuthGate>
  );
}
