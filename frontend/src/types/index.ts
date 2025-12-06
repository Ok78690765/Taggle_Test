/**
 * Common TypeScript types and interfaces
 */

export interface Item {
  id: number;
  name: string;
  description?: string;
  created_at?: string;
  updated_at?: string;
}

export interface ApiErrorResponse {
  detail?: string;
  error?: string;
}

export * from './analysis';
export * from './auth';
export * from './repository';
