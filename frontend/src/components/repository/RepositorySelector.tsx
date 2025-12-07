'use client';

import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { Card } from '@/components/common/Card';
import { LoadingSpinner } from '@/components/common/LoadingSpinner';
import { githubApi } from '@/lib/github-api';
import { useExplorerStore } from '@/store/explorer-store';
import type { Repository } from '@/types';

export function RepositorySelector() {
  const { repository, setRepository } = useExplorerStore();
  const { data: repositories, isLoading } = useQuery({
    queryKey: ['repositories'],
    queryFn: githubApi.listRepositories,
  });

  const handleSelect = (repo: Repository) => {
    setRepository(repo);
  };

  if (isLoading) {
    return (
      <Card title="Repositories">
        <LoadingSpinner text="Loading repositories..." />
      </Card>
    );
  }

  return (
    <Card title="Select repository" subtitle="Choose a codebase to explore">
      <div className="space-y-3">
        {repositories?.map((repo) => (
          <div
            key={repo.id}
            className={`rounded-xl border-2 p-4 transition cursor-pointer ${
              repository?.id === repo.id
                ? 'border-blue-500 bg-blue-50'
                : 'border-gray-200 bg-white hover:border-blue-300'
            }`}
            onClick={() => handleSelect(repo)}
          >
            <div className="flex items-start justify-between">
              <div className="flex-1">
                <div className="flex items-center gap-3">
                  <img
                    src={repo.owner.avatar_url}
                    alt={repo.owner.login}
                    className="h-8 w-8 rounded-full"
                  />
                  <div>
                    <p className="font-semibold text-gray-900">{repo.name}</p>
                    <p className="text-xs text-gray-500">{repo.full_name}</p>
                  </div>
                </div>
                {repo.description && (
                  <p className="mt-2 text-sm text-gray-600">{repo.description}</p>
                )}
                <div className="mt-3 flex flex-wrap items-center gap-3 text-xs text-gray-500">
                  {repo.language && (
                    <span className="flex items-center gap-1">
                      <span className="h-2 w-2 rounded-full bg-blue-500" />
                      {repo.language}
                    </span>
                  )}
                  <span>⭐ {repo.stars}</span>
                  <span>🍴 {repo.forks}</span>
                  <span>Branch: {repo.default_branch}</span>
                </div>
              </div>
              {repository?.id === repo.id && (
                <div className="flex h-6 w-6 items-center justify-center rounded-full bg-blue-500 text-white">
                  ✓
                </div>
              )}
            </div>
          </div>
        ))}
      </div>
    </Card>
  );
}
