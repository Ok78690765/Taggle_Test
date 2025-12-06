import { create } from 'zustand';

interface UIStore {
  sidebarOpen: boolean;
  promptComposerOpen: boolean;
  analysisPanelOpen: boolean;
  toggleSidebar: () => void;
  togglePromptComposer: () => void;
  toggleAnalysisPanel: () => void;
  setSidebarOpen: (open: boolean) => void;
  setPromptComposerOpen: (open: boolean) => void;
  setAnalysisPanelOpen: (open: boolean) => void;
}

export const useUIStore = create<UIStore>((set) => ({
  sidebarOpen: true,
  promptComposerOpen: false,
  analysisPanelOpen: true,

  toggleSidebar: () =>
    set((state) => ({ sidebarOpen: !state.sidebarOpen })),

  togglePromptComposer: () =>
    set((state) => ({ promptComposerOpen: !state.promptComposerOpen })),

  toggleAnalysisPanel: () =>
    set((state) => ({ analysisPanelOpen: !state.analysisPanelOpen })),

  setSidebarOpen: (sidebarOpen) => set({ sidebarOpen }),

  setPromptComposerOpen: (promptComposerOpen) => set({ promptComposerOpen }),

  setAnalysisPanelOpen: (analysisPanelOpen) => set({ analysisPanelOpen }),
}));
