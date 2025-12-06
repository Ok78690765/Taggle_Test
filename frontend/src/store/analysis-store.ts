import { create } from 'zustand';
import type { CodeAnalysisResponse, DebugAnalysisResponse } from '@/types';

type AnalysisStatus = 'idle' | 'running' | 'success' | 'error';

interface AnalysisHistoryItem {
  id: string;
  fileName: string | null;
  language: string;
  score: number | null;
  analyzedAt: string;
}

interface AnalysisStore {
  status: AnalysisStatus;
  statusMessage: string | null;
  progress: number;
  result: CodeAnalysisResponse | null;
  debugResult: DebugAnalysisResponse | null;
  history: AnalysisHistoryItem[];
  startAnalysis: (message?: string) => void;
  updateProgress: (message: string, progress: number) => void;
  completeAnalysis: (
    result: CodeAnalysisResponse,
    debugResult?: DebugAnalysisResponse
  ) => void;
  failAnalysis: (message: string) => void;
  resetStatus: () => void;
}

export const useAnalysisStore = create<AnalysisStore>((set) => ({
  status: 'idle',
  statusMessage: null,
  progress: 0,
  result: null,
  debugResult: null,
  history: [],

  startAnalysis: (message = 'Starting analysis...') =>
    set({ status: 'running', statusMessage: message, progress: 5 }),

  updateProgress: (statusMessage, progress) =>
    set({ statusMessage, progress: Math.min(progress, 95) }),

  completeAnalysis: (result, debugResult) =>
    set((state) => ({
      status: 'success',
      statusMessage: 'Analysis complete',
      progress: 100,
      result,
      debugResult: debugResult || state.debugResult,
      history: [
        ...state.history.slice(-9),
        {
          id: crypto.randomUUID(),
          fileName: result.file_name,
          language: result.language,
          score: result.quality_score?.overall_score || null,
          analyzedAt: new Date().toISOString(),
        },
      ],
    })),

  failAnalysis: (statusMessage) =>
    set({ status: 'error', statusMessage, progress: 0 }),

  resetStatus: () =>
    set({ status: 'idle', statusMessage: null, progress: 0 }),
}));
