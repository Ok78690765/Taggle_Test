'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { GitHubAuth } from '@/lib/github-auth';
import { RepositoryService, GitHubRepository } from '@/lib/repository-service';

export default function GitHubPage() {
  const router = useRouter();
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [username, setUsername] = useState<string | null>(null);
  const [userId, setUserId] = useState<number | null>(null);
  const [loading, setLoading] = useState(true);
  const [repositories, setRepositories] = useState<GitHubRepository[]>([]);
  const [selectedRepos, setSelectedRepos] = useState<number[]>([]);
  const [syncInProgress, setSyncInProgress] = useState(false);
  const [cloningRepos, setCloningRepos] = useState<Set<number>>(new Set());
  const [error, setError] = useState<string | null>(null);
  const [message, setMessage] = useState<string | null>(null);

  useEffect(() => {
    const checkAuth = async () => {
      try {
        const currentUserId = GitHubAuth.getCurrentUserId();
        const currentUsername = GitHubAuth.getCurrentUsername();

        if (currentUserId && currentUsername) {
          setIsAuthenticated(true);
          setUserId(currentUserId);
          setUsername(currentUsername);
          await loadRepositories(currentUserId);
        }
      } catch (err) {
        console.error('Error checking auth:', err);
      } finally {
        setLoading(false);
      }
    };

    checkAuth();
  }, []);

  const loadRepositories = async (userId: number) => {
    try {
      const result = await RepositoryService.listRepositories(userId);
      setRepositories(result.repositories);

      const selected = result.repositories
        .filter((r) => r.selected_for_sync)
        .map((r) => r.id);
      setSelectedRepos(selected);
    } catch (err) {
      setError('Failed to load repositories');
      console.error(err);
    }
  };

  const handleConnect = async () => {
    try {
      setLoading(true);
      const oauthUrl = await GitHubAuth.getOAuthUrl();
      window.location.href = oauthUrl;
    } catch (err) {
      setError('Failed to initiate OAuth');
      setLoading(false);
    }
  };

  const handleDisconnect = () => {
    GitHubAuth.logout();
    setIsAuthenticated(false);
    setUsername(null);
    setUserId(null);
    setRepositories([]);
    setSelectedRepos([]);
  };

  const handleSyncRepositories = async () => {
    if (!userId) return;

    try {
      setSyncInProgress(true);
      setError(null);
      const result = await RepositoryService.syncRepositories(userId);
      setMessage(
        `Synced ${result.new_repositories} new repositories. Total: ${result.total_repositories}`
      );
      await loadRepositories(userId);
    } catch (err) {
      setError('Failed to sync repositories');
      console.error(err);
    } finally {
      setSyncInProgress(false);
    }
  };

  const handleToggleSelection = async (repoId: number, currentSelection: boolean) => {
    try {
      await RepositoryService.toggleRepositorySelection(
        repoId,
        !currentSelection
      );

      const updated = selectedRepos.includes(repoId)
        ? selectedRepos.filter((id) => id !== repoId)
        : [...selectedRepos, repoId];

      setSelectedRepos(updated);
      setMessage('Repository selection updated');
    } catch (err) {
      setError('Failed to update repository selection');
      console.error(err);
    }
  };

  const handleCloneRepository = async (repoId: number) => {
    try {
      setCloningRepos((prev) => new Set([...prev, repoId]));
      setError(null);

      await RepositoryService.cloneRepository(repoId);
      setMessage('Repository cloned successfully');

      if (userId) {
        await loadRepositories(userId);
      }
    } catch (err) {
      setError('Failed to clone repository');
      console.error(err);
    } finally {
      setCloningRepos((prev) => {
        const next = new Set(prev);
        next.delete(repoId);
        return next;
      });
    }
  };

  return (
    <main className="container mx-auto py-12">
      <div className="max-w-6xl mx-auto">
        <div className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-4xl font-bold mb-2">GitHub Integration</h1>
            <p className="text-gray-600">Manage your GitHub repositories and sync them for analysis</p>
          </div>
          <div className="text-right">
            {isAuthenticated && (
              <div className="mb-4">
                <p className="text-lg font-semibold text-gray-700">{username}</p>
                <p className="text-sm text-gray-500">Connected</p>
              </div>
            )}
          </div>
        </div>

        {error && (
          <div className="mb-6 p-4 bg-red-50 text-red-700 rounded-lg border border-red-200">
            {error}
            <button
              onClick={() => setError(null)}
              className="float-right text-sm underline"
            >
              Dismiss
            </button>
          </div>
        )}

        {message && (
          <div className="mb-6 p-4 bg-green-50 text-green-700 rounded-lg border border-green-200">
            ✓ {message}
            <button
              onClick={() => setMessage(null)}
              className="float-right text-sm underline"
            >
              Dismiss
            </button>
          </div>
        )}

        {loading ? (
          <div className="text-center py-12">
            <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
            <p className="mt-4 text-gray-600">Loading...</p>
          </div>
        ) : !isAuthenticated ? (
          <div className="bg-white rounded-lg shadow-lg p-8 text-center">
            <h2 className="text-2xl font-bold mb-4">Connect GitHub Account</h2>
            <p className="text-gray-600 mb-6">
              Connect your GitHub account to start syncing repositories for analysis
            </p>
            <button
              onClick={handleConnect}
              className="px-8 py-3 bg-gray-800 text-white rounded-lg hover:bg-gray-900 transition font-semibold"
            >
              Connect with GitHub
            </button>
          </div>
        ) : (
          <div className="space-y-6">
            <div className="bg-white rounded-lg shadow p-6">
              <div className="flex justify-between items-center">
                <h2 className="text-2xl font-bold">Repositories</h2>
                <div className="space-x-2">
                  <button
                    onClick={handleSyncRepositories}
                    disabled={syncInProgress}
                    className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50 transition"
                  >
                    {syncInProgress ? 'Syncing...' : 'Sync Repositories'}
                  </button>
                  <button
                    onClick={handleDisconnect}
                    className="px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700 transition"
                  >
                    Disconnect
                  </button>
                </div>
              </div>
            </div>

            {repositories.length === 0 ? (
              <div className="bg-white rounded-lg shadow p-8 text-center">
                <p className="text-gray-600 mb-4">No repositories found</p>
                <button
                  onClick={handleSyncRepositories}
                  className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition"
                >
                  Sync Repositories
                </button>
              </div>
            ) : (
              <div className="grid gap-4">
                {repositories.map((repo) => (
                  <div
                    key={repo.id}
                    className="bg-white rounded-lg shadow p-4 border-l-4 border-blue-600"
                  >
                    <div className="flex justify-between items-start mb-2">
                      <div className="flex-1">
                        <h3 className="text-lg font-semibold text-gray-900">
                          {repo.repo_name}
                        </h3>
                        <p className="text-sm text-gray-500">
                          {repo.repo_full_name}
                        </p>
                        {repo.description && (
                          <p className="text-sm text-gray-600 mt-1">
                            {repo.description}
                          </p>
                        )}
                      </div>
                      <div className="text-right">
                        <span
                          className={`inline-block px-3 py-1 rounded text-sm font-medium ${
                            repo.sync_status === 'synced'
                              ? 'bg-green-100 text-green-800'
                              : repo.sync_status === 'failed'
                                ? 'bg-red-100 text-red-800'
                                : 'bg-yellow-100 text-yellow-800'
                          }`}
                        >
                          {repo.sync_status}
                        </span>
                        {repo.is_private && (
                          <span className="inline-block ml-2 px-2 py-1 bg-gray-200 text-gray-700 text-xs rounded">
                            Private
                          </span>
                        )}
                      </div>
                    </div>

                    <div className="flex items-center space-x-4 mt-4">
                      <label className="flex items-center space-x-2 cursor-pointer">
                        <input
                          type="checkbox"
                          checked={selectedRepos.includes(repo.id)}
                          onChange={() =>
                            handleToggleSelection(
                              repo.id,
                              selectedRepos.includes(repo.id)
                            )
                          }
                          className="w-4 h-4 rounded"
                        />
                        <span className="text-sm text-gray-700">
                          Selected for sync
                        </span>
                      </label>

                      <button
                        onClick={() => handleCloneRepository(repo.id)}
                        disabled={
                          cloningRepos.has(repo.id) ||
                          repo.sync_status === 'synced'
                        }
                        className="px-3 py-1 bg-green-600 text-white text-sm rounded hover:bg-green-700 disabled:opacity-50 transition"
                      >
                        {cloningRepos.has(repo.id)
                          ? 'Cloning...'
                          : 'Clone Repository'}
                      </button>

                      {repo.mirror_path && (
                        <button
                          onClick={() => router.push(`/github/${repo.id}/files`)}
                          className="px-3 py-1 bg-purple-600 text-white text-sm rounded hover:bg-purple-700 transition"
                        >
                          Browse Files
                        </button>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}
      </div>
    </main>
  );
}
