import { create } from 'zustand';
import type {
  Repository,
  FileNode,
  FileContent,
  FileDiff,
} from '@/types';

type ViewMode = 'preview' | 'diff';

interface ExplorerStore {
  repository: Repository | null;
  branch: string | null;
  fileTree: FileNode[];
  selectedPath: string | null;
  fileContent: FileContent | null;
  fileDiff: FileDiff | null;
  viewMode: ViewMode;
  syncing: boolean;
  setRepository: (repo: Repository | null, branch?: string) => void;
  setFileTree: (tree: FileNode[]) => void;
  selectPath: (path: string | null) => void;
  setFileContent: (content: FileContent | null) => void;
  setFileDiff: (diff: FileDiff | null) => void;
  setViewMode: (mode: ViewMode) => void;
  setSyncing: (value: boolean) => void;
}

export const useExplorerStore = create<ExplorerStore>((set) => ({
  repository: null,
  branch: null,
  fileTree: [],
  selectedPath: null,
  fileContent: null,
  fileDiff: null,
  viewMode: 'preview',
  syncing: false,

  setRepository: (repository, branch) =>
    set({ repository, branch: branch || repository?.default_branch || null }),

  setFileTree: (tree) => set({ fileTree: tree }),

  selectPath: (selectedPath) => set({ selectedPath }),

  setFileContent: (fileContent) => set({ fileContent }),

  setFileDiff: (fileDiff) => set({ fileDiff }),

  setViewMode: (viewMode) => set({ viewMode }),

  setSyncing: (syncing) => set({ syncing }),
}));
