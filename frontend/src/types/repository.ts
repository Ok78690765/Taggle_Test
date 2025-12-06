export interface Repository {
  id: string;
  name: string;
  full_name: string;
  description: string | null;
  url: string;
  default_branch: string;
  language: string | null;
  stars: number;
  forks: number;
  updated_at: string;
  owner: {
    login: string;
    avatar_url: string;
  };
}

export interface FileNode {
  name: string;
  path: string;
  type: 'file' | 'directory';
  size?: number;
  children?: FileNode[];
}

export interface FileContent {
  path: string;
  content: string;
  encoding?: string;
  size: number;
  language?: string;
}

export interface FileDiff {
  old_path: string;
  new_path: string;
  old_content: string;
  new_content: string;
  additions: number;
  deletions: number;
}
