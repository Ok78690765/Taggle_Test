'use client';

import React from 'react';
import { Card } from '@/components/common/Card';
import type { QualityScore } from '@/types';

interface QualityScoreCardProps {
  score: QualityScore;
  title?: string;
}

export function QualityScoreCard({ score, title = 'Code Quality' }: QualityScoreCardProps) {
  const getScoreColor = (value: number) => {
    if (value >= 80) return { bg: 'bg-green-500', text: 'text-green-600', status: 'Excellent' };
    if (value >= 60) return { bg: 'bg-blue-500', text: 'text-blue-600', status: 'Good' };
    if (value >= 40) return { bg: 'bg-amber-500', text: 'text-amber-600', status: 'Fair' };
    return { bg: 'bg-red-500', text: 'text-red-600', status: 'Needs Work' };
  };

  const overallColor = getScoreColor(score.overall_score);

  const metrics = [
    { label: 'Code Quality', value: score.code_quality },
    { label: 'Maintainability', value: score.maintainability },
    { label: 'Complexity', value: score.complexity, inverted: true },
    { label: 'Duplication', value: score.duplication },
  ];

  return (
    <Card title={title} className="h-full">
      <div className="mb-8 flex flex-col items-center gap-6 sm:flex-row">
        <div className="relative">
          <svg className="h-40 w-40 -rotate-90 transform">
            <circle
              cx="80"
              cy="80"
              r="64"
              stroke="currentColor"
              strokeWidth="12"
              fill="transparent"
              className="text-gray-200"
            />
            <circle
              cx="80"
              cy="80"
              r="64"
              stroke="currentColor"
              strokeWidth="12"
              fill="transparent"
              strokeDasharray={`${(score.overall_score / 100) * 402} 402`}
              className={overallColor.text}
              style={{ transition: 'stroke-dasharray 1s ease-in-out' }}
            />
          </svg>
          <div className="absolute inset-0 flex flex-col items-center justify-center">
            <span className="text-4xl font-bold text-gray-900">
              {Math.round(score.overall_score)}
            </span>
            <span className="text-sm font-medium text-gray-500">/ 100</span>
          </div>
        </div>

        <div className="flex-1 text-center sm:text-left">
          <div
            className={`inline-flex items-center gap-2 rounded-full px-4 py-2 ${overallColor.bg} bg-opacity-10`}
          >
            <div className={`h-2 w-2 rounded-full ${overallColor.bg}`} />
            <span className={`font-semibold ${overallColor.text}`}>
              {overallColor.status}
            </span>
          </div>
          <p className="mt-4 text-sm text-gray-600">
            Overall score based on code quality, maintainability, complexity, and
            duplication metrics.
          </p>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-4 sm:grid-cols-4">
        {metrics.map((metric) => {
          const color = getScoreColor(metric.inverted ? 100 - metric.value : metric.value);
          return (
            <div
              key={metric.label}
              className="rounded-lg border border-gray-100 bg-gray-50 p-4"
            >
              <p className="mb-2 text-xs font-medium uppercase tracking-wide text-gray-500">
                {metric.label}
              </p>
              <div className="flex items-baseline gap-1">
                <span className={`text-2xl font-bold ${color.text}`}>
                  {Math.round(metric.value)}
                </span>
                <span className="text-sm text-gray-400">/ 100</span>
              </div>
              <div className="mt-2 h-1.5 w-full overflow-hidden rounded-full bg-gray-200">
                <div
                  className={`h-full ${color.bg}`}
                  style={{
                    width: `${metric.value}%`,
                    transition: 'width 0.5s ease-out',
                  }}
                />
              </div>
            </div>
          );
        })}
      </div>
    </Card>
  );
}
