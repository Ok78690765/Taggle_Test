/**
 * GitHub API Helper
 * Provides methods for interacting with the backend's GitHub API endpoints
 */

import { api } from './api';
import type { Repository, FileNode, FileContent, FileDiff } from '@/types';

class GitHubAPI {
  async listRepositories(): Promise<Repository[]> {
    return api.get('/api/github/repositories');
  }

  async getRepository(owner: string, repo: string): Promise<Repository> {
    return api.get(`/api/github/repositories/${owner}/${repo}`);
  }

  async listBranches(owner: string, repo: string): Promise<string[]> {
    return api.get(`/api/github/repositories/${owner}/${repo}/branches`);
  }

  async getRepositoryTree(repositoryId?: string, branch?: string): Promise<FileNode[]> {
    if (!repositoryId || !branch) {
      return [];
    }
    return api.get(`/api/github/repositories/${repositoryId}/tree`, {
      params: { branch },
    });
  }

  async getFileContent(repositoryId?: string, path?: string): Promise<FileContent> {
    if (!repositoryId || !path) {
      return { path: '', content: '', size: 0 };
    }
    return api.get(`/api/github/repositories/${repositoryId}/file`, {
      params: { path },
    });
  }

  async getFileDiff(repositoryId?: string, path?: string): Promise<FileDiff> {
    if (!repositoryId || !path) {
      return {
        old_path: '',
        new_path: '',
        old_content: '',
        new_content: '',
        additions: 0,
        deletions: 0,
      };
    }
    return api.get(`/api/github/repositories/${repositoryId}/diff`, {
      params: { path },
    });
  }
}

export const githubApi = new GitHubAPI();
