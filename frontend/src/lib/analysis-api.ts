/**
 * Analysis API Helper
 * Provides methods for interacting with the backend's analysis endpoints
 */

import { api } from './api';
import type { AnalysisRequest, AnalysisResult, CodeAnalysisRequest, CodeAnalysisResponse, DebugAnalysisResponse } from '@/types';

class AnalysisAPI {
  async analyze(request: AnalysisRequest): Promise<AnalysisResult> {
    return api.post('/api/analysis', request);
  }

  async analyzeCode(request: CodeAnalysisRequest): Promise<CodeAnalysisResponse> {
    return api.post('/api/analysis/code', request);
  }

  async analyzeDebug(code: string, language: string, fileName?: string): Promise<DebugAnalysisResponse> {
    return api.post('/api/analysis/debug', {
      code,
      language,
      file_name: fileName,
    });
  }

  async getAnalysisStatus(analysisId: string): Promise<AnalysisResult> {
    return api.get(`/api/analysis/${analysisId}`);
  }

  async listAnalyses(): Promise<AnalysisResult[]> {
    return api.get('/api/analysis');
  }

  async deleteAnalysis(analysisId: string): Promise<void> {
    return api.delete(`/api/analysis/${analysisId}`);
  }

  async streamAnalysis(
    request: AnalysisRequest,
    onChunk: (chunk: string) => void,
    onComplete: () => void,
    onError: (error: Error) => void
  ): Promise<void> {
    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/analysis/stream`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(request),
        }
      );

      if (!response.body) {
        throw new Error('Response body is not available');
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder();

      try {
        while (true) {
          const { done, value } = await reader.read();
          if (done) {
            onComplete();
            break;
          }
          const chunk = decoder.decode(value);
          onChunk(chunk);
        }
      } catch (error) {
        onError(error instanceof Error ? error : new Error('Unknown error'));
      }
    } catch (error) {
      onError(error instanceof Error ? error : new Error('Unknown error'));
    }
  }
}

export const analysisApi = new AnalysisAPI();
