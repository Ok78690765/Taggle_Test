'use client';

import React from 'react';
import { Card } from '@/components/common/Card';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus } from 'react-syntax-highlighter/dist/cjs/styles/prism';
import type { FileContent } from '@/types';

interface FileViewerProps {
  file: FileContent | null;
}

const langMap: Record<string, string> = {
  python: 'python',
  javascript: 'javascript',
  typescript: 'typescript',
  java: 'java',
  cpp: 'cpp',
  jsx: 'jsx',
  tsx: 'tsx',
  json: 'json',
  yaml: 'yaml',
  md: 'markdown',
  css: 'css',
  scss: 'scss',
};

export function FileViewer({ file }: FileViewerProps) {
  if (!file) {
    return (
      <Card title="File preview">
        <p className="text-sm text-gray-500">
          Select a file from the tree to view its contents.
        </p>
      </Card>
    );
  }

  const extension = file.path.split('.').pop() || '';
  const language = file.language || langMap[extension] || 'text';

  return (
    <Card
      title="File preview"
      subtitle={file.path}
      actions={
        <span className="text-xs text-gray-500">
          {file.size} bytes • {file.content.split('\n').length} lines
        </span>
      }
    >
      <div className="overflow-x-auto rounded-lg">
        <SyntaxHighlighter
          language={language}
          style={vscDarkPlus}
          showLineNumbers
          wrapLongLines={false}
          customStyle={{
            margin: 0,
            borderRadius: '0.75rem',
            fontSize: '0.875rem',
          }}
        >
          {file.content}
        </SyntaxHighlighter>
      </div>
    </Card>
  );
}
