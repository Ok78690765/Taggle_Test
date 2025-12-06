'use client';

import React from 'react';
import { Card } from '@/components/common/Card';
import { StatusPill } from '@/components/common/StatusPill';
import { ProgressBar } from '@/components/common/ProgressBar';
import { useAnalysisStore } from '@/store/analysis-store';
import { QualityScoreCard } from './QualityScoreCard';
import type { Issue } from '@/types';

const severityMap: Record<Issue['severity'], { label: string; color: string }> = {
  error: { label: 'Error', color: 'bg-red-500' },
  warning: { label: 'Warning', color: 'bg-amber-500' },
  info: { label: 'Info', color: 'bg-blue-500' },
};

export function AnalysisResults() {
  const { result, debugResult, status, statusMessage, progress } =
    useAnalysisStore();

  if (!result) {
    return (
      <Card title="Live analysis" subtitle="Run a prompt to view results">
        <p className="text-sm text-gray-500">
          Submit code via the prompt composer to see live quality metrics, issue
          breakdowns, and architecture insights.
        </p>
        {status === 'running' && (
          <div className="mt-6 space-y-3">
            <ProgressBar value={progress} showPercentage label={statusMessage || 'Analyzing...'} />
            <p className="text-xs text-gray-400">
              Streaming updates while the analyzer crunches metrics.
            </p>
          </div>
        )}
      </Card>
    );
  }

  const issuesBySeverity = result.issues.reduce(
    (acc, issue) => {
      acc[issue.severity] += 1;
      return acc;
    },
    { error: 0, warning: 0, info: 0 }
  );

  return (
    <div className="space-y-6">
      <QualityScoreCard score={result.quality_score} />

      <div className="grid gap-6 lg:grid-cols-3">
        <Card
          title="Issue detection"
          subtitle="Sorted by severity with remediation tips"
        >
          <div className="flex flex-wrap gap-3">
            {(['error', 'warning', 'info'] as const).map((severity) => (
              <div
                key={severity}
                className="flex flex-1 min-w-[120px] items-center justify-between rounded-xl bg-gray-50 px-4 py-3"
              >
                <div>
                  <p className="text-xs font-medium uppercase tracking-wide text-gray-500">
                    {severityMap[severity].label}
                  </p>
                  <p className="text-2xl font-bold text-gray-900">
                    {issuesBySeverity[severity] || 0}
                  </p>
                </div>
                <span
                  className={`h-10 w-10 rounded-full ${severityMap[severity].color} bg-opacity-10 text-xs font-semibold text-gray-700 flex items-center justify-center`}
                >
                  {issuesBySeverity[severity]}
                </span>
              </div>
            ))}
          </div>

          <div className="mt-6 space-y-4 divide-y divide-gray-100">
            {result.issues.slice(0, 5).map((issue, index) => (
              <div key={`${issue.issue_type}-${index}`} className="pt-4 first:pt-0">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <span
                      className={`h-2 w-2 rounded-full ${severityMap[issue.severity].color}`}
                      aria-hidden="true"
                    />
                    <p className="text-sm font-semibold text-gray-800">
                      {issue.message}
                    </p>
                  </div>
                  <StatusPill
                    label={issue.severity}
                    status={
                      issue.severity === 'error'
                        ? 'error'
                        : issue.severity === 'warning'
                        ? 'warning'
                        : 'info'
                    }
                  />
                </div>
                <p className="mt-2 text-sm text-gray-500">
                  {issue.suggestion || 'Review this section for potential improvements.'}
                </p>
                <div className="mt-2 text-xs text-gray-400">
                  Line {issue.line_number ?? '—'} • Column {issue.column_number ?? '—'}
                </div>
              </div>
            ))}
          </div>
        </Card>

        <Card
          title="Complexity & architecture"
          subtitle="Cyclomatic metrics and detected patterns"
          className="lg:col-span-2"
        >
          <div className="grid gap-4 sm:grid-cols-2">
            <div className="rounded-2xl border border-gray-100 p-5">
              <p className="text-xs font-semibold uppercase tracking-wide text-gray-500">
                Complexity metrics
              </p>
              {result.complexity_metrics ? (
                <dl className="mt-4 grid grid-cols-2 gap-4 text-sm">
                  <div>
                    <dt className="text-gray-500">Cyclomatic</dt>
                    <dd className="text-lg font-semibold text-gray-900">
                      {result.complexity_metrics.cyclomatic_complexity.toFixed(1)}
                    </dd>
                  </div>
                  <div>
                    <dt className="text-gray-500">Cognitive</dt>
                    <dd className="text-lg font-semibold text-gray-900">
                      {result.complexity_metrics.cognitive_complexity.toFixed(1)}
                    </dd>
                  </div>
                  <div>
                    <dt className="text-gray-500">Lines of code</dt>
                    <dd className="text-lg font-semibold text-gray-900">
                      {result.complexity_metrics.lines_of_code}
                    </dd>
                  </div>
                  <div>
                    <dt className="text-gray-500">Nesting depth</dt>
                    <dd className="text-lg font-semibold text-gray-900">
                      {result.complexity_metrics.nesting_depth}
                    </dd>
                  </div>
                </dl>
              ) : (
                <p className="mt-4 text-sm text-gray-500">
                  Complexity metrics unavailable for this analysis run.
                </p>
              )}
            </div>

            <div className="rounded-2xl border border-gray-100 p-5">
              <p className="text-xs font-semibold uppercase tracking-wide text-gray-500">
                Architecture insights
              </p>
              {result.architecture_insights.length > 0 ? (
                <ul className="mt-4 space-y-3 text-sm text-gray-600">
                  {result.architecture_insights.map((insight) => (
                    <li key={insight.pattern_detected}>
                      <p className="font-semibold text-gray-900">
                        {insight.pattern_detected}{' '}
                        <span className="text-xs text-gray-500">
                          {(insight.confidence * 100).toFixed(0)}% confidence
                        </span>
                      </p>
                      <p>{insight.description}</p>
                      {insight.recommendations.length > 0 && (
                        <ul className="mt-2 list-disc space-y-1 pl-4 text-xs text-gray-500">
                          {insight.recommendations.map((recommendation) => (
                            <li key={recommendation}>{recommendation}</li>
                          ))}
                        </ul>
                      )}
                    </li>
                  ))}
                </ul>
              ) : (
                <p className="mt-4 text-sm text-gray-500">
                  No architecture patterns detected in this snippet.
                </p>
              )}
            </div>
          </div>

          {debugResult && (
            <div className="mt-6 rounded-2xl border border-blue-100 bg-blue-50 p-5">
              <p className="text-xs font-semibold uppercase tracking-wide text-blue-600">
                Debug insights
              </p>
              <ul className="mt-3 space-y-3">
                {debugResult.debug_insights.map((insight) => (
                  <li key={insight.potential_issue} className="text-sm text-blue-900">
                    <p className="font-semibold">{insight.potential_issue}</p>
                    <p className="text-xs text-blue-700">
                      Impact: {insight.affected_areas.join(', ')}
                    </p>
                    <ul className="mt-2 list-disc space-y-1 pl-4 text-xs text-blue-800">
                      {insight.debug_steps.map((step) => (
                        <li key={step}>{step}</li>
                      ))}
                    </ul>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </Card>
      </div>
    </div>
  );
}
