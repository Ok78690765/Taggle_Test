import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import type { UserProfile, AuthState } from '@/types';
import { api } from '@/lib/api';

interface AuthStore extends AuthState {
  authenticated: boolean;
  setAuth: (token: string, user: UserProfile, expiresAt?: string) => void;
  logout: () => void;
  isAuthenticated: () => boolean;
}

export const useAuthStore = create<AuthStore>()(
  persist(
    (set, get) => ({
      token: null,
      user: null,
      expiresAt: null,
      authenticated: false,

      setAuth: (token, user, expiresAt) => {
        set({
          token,
          user,
          expiresAt: expiresAt || null,
          authenticated: true,
        });
        api.setToken(token);
        if (typeof window !== 'undefined') {
          localStorage.setItem('auth_token', token);
          localStorage.setItem('auth_user', JSON.stringify(user));
        }
      },

      logout: () => {
        set({ token: null, user: null, expiresAt: null, authenticated: false });
        api.setToken('');
        if (typeof window !== 'undefined') {
          localStorage.removeItem('auth_token');
          localStorage.removeItem('auth_user');
        }
      },

      isAuthenticated: () => {
        const state = get();
        if (!state.token || !state.user) {
          set({ authenticated: false });
          return false;
        }
        if (state.expiresAt && new Date(state.expiresAt) < new Date()) {
          get().logout();
          return false;
        }
        if (!state.authenticated) {
          set({ authenticated: true });
        }
        return true;
      },
    }),
    {
      name: 'auth-storage',
    }
  )
);
