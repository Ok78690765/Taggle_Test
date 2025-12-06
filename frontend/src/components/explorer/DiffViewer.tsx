'use client';

import React from 'react';
import { Card } from '@/components/common/Card';
import type { FileDiff } from '@/types';

interface DiffViewerProps {
  diff: FileDiff | null;
}

export function DiffViewer({ diff }: DiffViewerProps) {
  if (!diff) {
    return (
      <Card title="Diff preview">
        <p className="text-sm text-gray-500">
          Switch to diff mode after selecting a file to view git changes.
        </p>
      </Card>
    );
  }

  const changes = [
    ...diff.old_content.split('\n').map((line) => `- ${line}`),
    ...diff.new_content.split('\n').map((line) => `+ ${line}`),
  ];

  return (
    <Card
      title="Diff preview"
      subtitle={`${diff.old_path} → ${diff.new_path}`}
      actions={
        <div className="flex gap-3 text-xs text-gray-500">
          <span className="text-red-500">-{diff.deletions} deletions</span>
          <span className="text-green-500">+{diff.additions} additions</span>
        </div>
      }
    >
      <pre className="max-h-[600px] overflow-auto rounded-xl bg-slate-900 p-5 text-sm text-slate-100">
        {changes.map((line, index) => (
          <div
            key={`${line}-${index}`}
            className={
              line.startsWith('+')
                ? 'text-green-300'
                : line.startsWith('-')
                ? 'text-red-300'
                : 'text-slate-100'
            }
          >
            {line}
          </div>
        ))}
      </pre>
    </Card>
  );
}
