'use client';

import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { Card } from '@/components/common/Card';
import { Button } from '@/components/common/Button';
import { LoadingSpinner } from '@/components/common/LoadingSpinner';
import { FileTree } from './FileTree';
import { FileViewer } from './FileViewer';
import { DiffViewer } from './DiffViewer';
import { githubApi } from '@/lib/github-api';
import { useExplorerStore } from '@/store/explorer-store';

export function CodeExplorer() {
  const repository = useExplorerStore((state) => state.repository);
  const selectedPath = useExplorerStore((state) => state.selectedPath);
  const selectPath = useExplorerStore((state) => state.selectPath);
  const viewMode = useExplorerStore((state) => state.viewMode);
  const setViewMode = useExplorerStore((state) => state.setViewMode);

  const treeQuery = useQuery({
    queryKey: ['repository-tree', repository?.id, repository?.default_branch],
    queryFn: () =>
      githubApi.getRepositoryTree(repository?.id, repository?.default_branch),
    enabled: Boolean(repository),
  });

  const fileQuery = useQuery({
    queryKey: ['file-content', repository?.id, selectedPath],
    queryFn: () => githubApi.getFileContent(repository?.id, selectedPath || undefined),
    enabled: Boolean(repository && selectedPath && viewMode === 'preview'),
  });

  const diffQuery = useQuery({
    queryKey: ['file-diff', repository?.id, selectedPath],
    queryFn: () => githubApi.getFileDiff(repository?.id, selectedPath || undefined),
    enabled: Boolean(repository && selectedPath && viewMode === 'diff'),
  });

  if (!repository) {
    return (
      <Card title="Code explorer">
        <p className="text-sm text-gray-500">
          Select a repository to browse files, view diffs, and send files to the prompt
          composer.
        </p>
      </Card>
    );
  }

  return (
    <div className="space-y-4">
      <Card
        title="Code explorer"
        subtitle={`${repository.full_name} • ${repository.default_branch}`}
        actions={
          <div className="inline-flex gap-2 rounded-full border border-gray-200 bg-white p-1">
            <Button
              type="button"
              size="sm"
              variant={viewMode === 'preview' ? 'primary' : 'ghost'}
              onClick={() => setViewMode('preview')}
            >
              Preview
            </Button>
            <Button
              type="button"
              size="sm"
              variant={viewMode === 'diff' ? 'primary' : 'ghost'}
              onClick={() => setViewMode('diff')}
            >
              Diff
            </Button>
          </div>
        }
      >
        <div className="grid gap-4 lg:grid-cols-[320px_1fr]">
          <div className="rounded-2xl border border-gray-100 bg-gray-50 p-4">
            {treeQuery.isLoading ? (
              <LoadingSpinner text="Loading repository tree..." />
            ) : treeQuery.data && treeQuery.data.length > 0 ? (
              <FileTree
                nodes={treeQuery.data}
                selectedPath={selectedPath}
                onSelect={(node) => selectPath(node.path)}
              />
            ) : (
              <p className="text-sm text-gray-500">
                No files found in this repository.
              </p>
            )}
          </div>

          <div>
            {viewMode === 'preview' ? (
              fileQuery.isLoading ? (
                <LoadingSpinner text="Loading file content..." />
              ) : (
                <FileViewer file={fileQuery.data || null} />
              )
            ) : diffQuery.isLoading ? (
              <LoadingSpinner text="Loading git diff..." />
            ) : (
              <DiffViewer diff={diffQuery.data || null} />
            )}
          </div>
        </div>
      </Card>
    </div>
  );
}
