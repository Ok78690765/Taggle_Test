'use client';

import React, { useState } from 'react';
import { Card } from '@/components/common/Card';
import { Button } from '@/components/common/Button';
import { analysisApi } from '@/lib/analysis-api';
import { useAnalysisStore } from '@/store/analysis-store';

const languageOptions = [
  { value: 'python', label: 'Python' },
  { value: 'javascript', label: 'JavaScript' },
  { value: 'typescript', label: 'TypeScript' },
  { value: 'java', label: 'Java' },
  { value: 'cpp', label: 'C++' },
];

export function PromptComposer() {
  const [code, setCode] = useState('');
  const [language, setLanguage] = useState('python');
  const [fileName, setFileName] = useState('');
  const [analyzeAll, setAnalyzeAll] = useState(true);
  const [loading, setLoading] = useState(false);

  const { startAnalysis, updateProgress, completeAnalysis, failAnalysis } =
    useAnalysisStore();

  const handleAnalyze = async () => {
    if (!code.trim()) return;

    setLoading(true);
    startAnalysis('Initializing code analysis...');

    try {
      updateProgress('Analyzing code quality...', 25);
      await new Promise((resolve) => setTimeout(resolve, 300));

      updateProgress('Detecting issues and patterns...', 50);
      await new Promise((resolve) => setTimeout(resolve, 300));

      updateProgress('Computing complexity metrics...', 75);
      await new Promise((resolve) => setTimeout(resolve, 300));

      const result = await analysisApi.analyzeCode({
        code,
        language,
        file_name: fileName || undefined,
        analyze_quality: analyzeAll,
        analyze_issues: analyzeAll,
        analyze_architecture: analyzeAll,
        analyze_formatting: analyzeAll,
      });

      updateProgress('Fetching debug insights...', 90);
      const debugResult = await analysisApi.analyzeDebug(code, language, fileName);

      completeAnalysis(result, debugResult);
    } catch (error) {
      console.error('Analysis failed:', error);
      failAnalysis(
        error instanceof Error ? error.message : 'Analysis failed'
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <Card
      title="Prompt composer"
      subtitle="Submit code for real-time quality analysis"
    >
      <div className="space-y-4">
        <div className="grid gap-4 sm:grid-cols-2">
          <div>
            <label
              htmlFor="language"
              className="mb-1 block text-sm font-medium text-gray-700"
            >
              Language
            </label>
            <select
              id="language"
              value={language}
              onChange={(e) => setLanguage(e.target.value)}
              className="w-full rounded-lg border border-gray-300 px-4 py-2 text-gray-900 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
              disabled={loading}
            >
              {languageOptions.map((opt) => (
                <option key={opt.value} value={opt.value}>
                  {opt.label}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label
              htmlFor="fileName"
              className="mb-1 block text-sm font-medium text-gray-700"
            >
              File name (optional)
            </label>
            <input
              id="fileName"
              type="text"
              value={fileName}
              onChange={(e) => setFileName(e.target.value)}
              placeholder="example.py"
              className="w-full rounded-lg border border-gray-300 px-4 py-2 text-gray-900 placeholder-gray-400 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
              disabled={loading}
            />
          </div>
        </div>

        <div>
          <label
            htmlFor="code"
            className="mb-1 block text-sm font-medium text-gray-700"
          >
            Code to analyze
          </label>
          <textarea
            id="code"
            value={code}
            onChange={(e) => setCode(e.target.value)}
            rows={12}
            placeholder="Paste your code here..."
            className="w-full rounded-lg border border-gray-300 px-4 py-3 font-mono text-sm text-gray-900 placeholder-gray-400 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
            disabled={loading}
          />
          <p className="mt-1 text-xs text-gray-500">
            {code.length} characters • {code.split('\n').length} lines
          </p>
        </div>

        <div className="flex items-center gap-2">
          <input
            type="checkbox"
            id="analyzeAll"
            checked={analyzeAll}
            onChange={(e) => setAnalyzeAll(e.target.checked)}
            className="h-4 w-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
            disabled={loading}
          />
          <label htmlFor="analyzeAll" className="text-sm text-gray-700">
            Run full analysis (quality, issues, architecture, formatting, debug)
          </label>
        </div>

        <Button
          variant="primary"
          size="lg"
          fullWidth
          onClick={handleAnalyze}
          disabled={!code.trim() || loading}
          loading={loading}
        >
          {loading ? 'Analyzing code...' : 'Analyze Code'}
        </Button>
      </div>
    </Card>
  );
}
